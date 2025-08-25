from typing import List, Optional, Dict, Any

from fastapi import FastAPI
from fastapi import UploadFile, File, Form
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.chat_loop import run_chat_round
from app.agent_router import detect_intent
from app.agent_tools import tool_rag_answer, tool_reading_card, tool_compare_papers
from app.rag_pipeline import rag_pipeline
from app.agent_card import generate_reading_card
from app.agent_compare import generate_comparison
from app.rag_pipeline import DEFAULT_COLLECTION
from app.chroma_utils import init_chroma, add_documents
import os
import json


app = FastAPI(title="RAG+Agent API", version="0.1.0")

_DEV_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_DEV_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"]
)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
class ChatStreamRequest(BaseModel):
    messages: List[ChatMessage]



class RagRequest(BaseModel):
    query: str
    use_rerank: Optional[bool] = True
    use_bm25: Optional[bool] = True
    temperature: Optional[float] = 0.2


class CardRequest(BaseModel):
    query: str
    use_rerank: Optional[bool] = True
    use_bm25: Optional[bool] = True
    k_ctx: Optional[int] = 6
    temperature: Optional[float] = 0.2
    self_check: Optional[bool] = False


class CompareRequest(BaseModel):
    topic: str
    picks: Optional[List[str]] = None
    use_rerank: Optional[bool] = True
    use_bm25: Optional[bool] = True
    k_ctx: Optional[int] = 8
    temperature: Optional[float] = 0.2
    self_check: Optional[bool] = False


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok"}


@app.get("/config/runtime")
def runtime_config() -> Dict[str, Any]:
    """Return redacted runtime config to verify keys/modes without leaking secrets."""
    dashscope_key = os.getenv("DASHSCOPE_API_KEY", "")
    use_remote = os.getenv("USE_REMOTE_EMBEDDINGS", "").strip() in {"1", "true", "True"}
    embed_model = os.getenv("QWEN_EMBED_MODEL", "").strip() or None
    return {
        "dashscope_key_present": bool(dashscope_key),
        "use_remote_embeddings": bool(use_remote),
        "embed_model": embed_model,
    }


@app.get("/")
def root():
    # 访问根路径时跳转到接口文档
    return RedirectResponse(url="/docs")


@app.post("/chat")
def chat(req: ChatRequest) -> Dict[str, Any]:
    messages = [m.model_dump() for m in req.messages]
    assistant_msg = run_chat_round(messages)
    return {"message": assistant_msg}


def _yield_jsonl(obj: Dict[str, Any]):
    import json
    return (json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8")

def _yield_padding():
    # 用于冲刷代理/浏览器缓冲，确保前端尽快收到首个字节
    return (" " * 2048 + "\n").encode("utf-8")


@app.post("/chat/stream")
def chat_stream(
    req: ChatStreamRequest,
    bm25: Optional[bool] = None,
    rerank: Optional[bool] = None,
    k_ctx: Optional[int] = None,
    temp: Optional[float] = None,
    self_check: Optional[bool] = None,
):
    import time
    messages = [m.model_dump() for m in req.messages]
    # 找到最后一条用户输入
    user_msg = None
    for m in reversed(messages):
        if m.get("role") == "user":
            user_msg = m.get("content")
            break

    def gen():
        if not user_msg:
            yield _yield_jsonl({"type": "final", "content": "请先输入你的问题。"})
            return
        # 先发送一段 padding，降低缓冲导致的首包延迟
        yield _yield_padding()
        # 路由
        intent, args = detect_intent(user_msg)
        yield _yield_jsonl({"type": "step", "status": "router", "intent": intent})

        # 标注工作流
        workflow_label = {
            "reading_card": "速读卡",
            "compare_papers": "论文对比",
            "rag_answer": "知识库问答",
            "chat_free": "闲聊",
        }.get(intent, intent)
        yield _yield_jsonl({"type": "step", "status": "workflow", "label": workflow_label})

        # 预告检索开始（确保前端立刻看到“检索中”）
        if intent in {"reading_card", "compare_papers", "rag_answer"}:
            yield _yield_jsonl({"type": "step", "status": "retrieving_start"})

        # 调用工具（近似：工具内部完成检索与生成，我们在返回后给出检索预览并做伪流式）
        final_sources = []
        try:
            if intent == "reading_card":
                _res = tool_reading_card(
                    args["query"],
                    use_rerank=bool(rerank) if rerank is not None else False,
                    use_bm25=bool(bm25) if bm25 is not None else True,
                    k_ctx=int(k_ctx or 6),
                    temperature=float(temp or 0.2),
                    self_check=bool(self_check) if self_check is not None else False,
                )
                data = (_res or {}).get("data") or {}
                preview = [ (s.get("title") or s.get("source")) for s in data.get("sources", []) ][:3]
                yield _yield_jsonl({"type": "step", "status": "retrieving_done", "preview": preview})
                content = data.get("card", "")
                final_sources = data.get("sources", [])
            elif intent == "compare_papers":
                _res = tool_compare_papers(
                    args.get("topic", user_msg),
                    picks=args.get("picks"),
                    use_rerank=bool(rerank) if rerank is not None else False,
                    use_bm25=bool(bm25) if bm25 is not None else True,
                    k_ctx=int(k_ctx or 8),
                    temperature=float(temp or 0.2),
                    self_check=bool(self_check) if self_check is not None else False,
                )
                data = (_res or {}).get("data") or {}
                preview = [ (s.get("title") or s.get("source")) for s in data.get("sources", []) ][:3]
                yield _yield_jsonl({"type": "step", "status": "retrieving_done", "preview": preview})
                content = data.get("table", "")
                final_sources = data.get("sources", [])
            elif intent == "rag_answer":
                _res = tool_rag_answer(
                    args["query"],
                    use_rerank=bool(rerank) if rerank is not None else False,
                    use_bm25=bool(bm25) if bm25 is not None else True,
                )
                data = (_res or {}).get("data") or {}
                preview = [ s for s in data.get("sources", []) ][:3]
                # sources 可能是字符串列表或对象列表
                prev_titles = []
                for s in preview:
                    if isinstance(s, dict):
                        prev_titles.append(s.get("title") or s.get("source"))
                    else:
                        prev_titles.append(str(s))
                yield _yield_jsonl({"type": "step", "status": "retrieving_done", "preview": prev_titles})
                content = data.get("answer", "")
                try:
                    yield _yield_jsonl({"type": "step", "status": "debug", "content_len": len(content or ""), "sources_len": len(data.get("sources", []))})
                except Exception:
                    pass
                final_sources = data.get("sources", [])
            else:
                # 闲聊走非流式
                from app.qwen_api import qwen_chat
                content = qwen_chat(system_prompt="你是一个友好且克制的助理。", user_prompt=user_msg)
                final_sources = []
        except Exception as e:
            # 输出错误事件，避免前端无响应
            err = str(e)
            yield _yield_jsonl({"type": "step", "status": "error", "message": err})
            content = f"处理出错：{err}"
            final_sources = []

        # 伪流式：按句子/块分片输出，第一行显示“工作流/状态”
        first_line_hint = None
        if intent == "reading_card":
            first_line_hint = "[工作流: 速读卡]"
        elif intent == "compare_papers":
            first_line_hint = "[工作流: 论文对比]"
        elif intent == "rag_answer":
            first_line_hint = "[工作流: 知识库问答]"
        if first_line_hint:
            yield _yield_jsonl({"type": "delta", "content": first_line_hint + "\n\n"})
        yield _yield_jsonl({"type": "step", "status": "generating_start"})
        import re
        # 若生成内容为空，给出友好的兜底提示，避免前端空白
        if not (content or "").strip():
            content = (
                "【系统提示】暂未生成内容。可能原因：\n"
                "- 首次索引或向量模型加载较慢；\n"
                "- 未检索到相关资料；\n"
                "- 生成模型未配置或超时。\n\n"
                "建议：稍后重试；或检查环境变量 DASHSCOPE_API_KEY / USE_REMOTE_EMBEDDINGS，"
                "或先缩小数据集体量以完成首轮索引。"
            )
        chunks = re.split(r"(?<=[。！？!?.])", content)
        buf = ""
        for ch in chunks:
            if not ch:
                continue
            buf += ch
            yield _yield_jsonl({"type": "delta", "content": ch})
            time.sleep(0.02)
        yield _yield_jsonl({"type": "step", "status": "generating_done"})
        yield _yield_jsonl({"type": "final", "content": buf, "sources": final_sources})

    return StreamingResponse(gen(), media_type="text/plain")


@app.post("/tools/rag")
def rag(req: RagRequest) -> Dict[str, Any]:
    res = rag_pipeline(req.query, use_rerank=bool(req.use_rerank), use_bm25=bool(req.use_bm25))
    return res


@app.post("/tools/card")
def card(req: CardRequest) -> Dict[str, Any]:
    res = generate_reading_card(
        req.query,
        use_rerank=bool(req.use_rerank),
        use_bm25=bool(req.use_bm25),
        k_ctx=int(req.k_ctx or 6),
        temperature=float(req.temperature or 0.2),
        self_check=bool(req.self_check),
    )
    return res


@app.post("/tools/compare")
def compare(req: CompareRequest) -> Dict[str, Any]:
    res = generate_comparison(
        req.topic,
        picks=req.picks,
        use_rerank=bool(req.use_rerank),
        use_bm25=bool(req.use_bm25),
        k_ctx=int(req.k_ctx or 8),
        temperature=float(req.temperature or 0.2),
        self_check=bool(req.self_check),
    )
    return res


# ---------------- Ingest API ---------------- #

@app.post("/ingest")
async def ingest(
    file: UploadFile | None = File(None),
    url: Optional[str] = Form(None),
    ocr: Optional[bool] = Form(False),
) -> Dict[str, Any]:
    """Ingest a PDF/MD/TXT file or a URL into Chroma. Returns count and sources."""
    import os
    import tempfile
    from typing import List, Tuple
    import httpx
    try:
        from pypdf import PdfReader
    except Exception:
        PdfReader = None  # type: ignore
    try:
        from pdfminer.high_level import extract_text as pdfminer_extract_text  # type: ignore
    except Exception:
        pdfminer_extract_text = None  # type: ignore
    try:
        import fitz  # PyMuPDF
    except Exception:
        fitz = None  # type: ignore

    docs: List[Tuple[str, str]] = []
    debug: Dict[str, Any] = {}

    # Handle file upload
    if file is not None:
        fname = file.filename or "upload"
        ext = os.path.splitext(fname)[1].lower()
        try:
            content_bytes = await file.read()
        except Exception:
            content_bytes = b""
        debug.update({
            "file_name": fname,
            "ext": ext,
            "bytes_len": len(content_bytes),
            "has_pypdf": bool(PdfReader is not None),
            "has_pdfminer": bool(pdfminer_extract_text is not None),
            "has_pymupdf": bool(fitz is not None),
        })
        is_pdf_guess = ext == ".pdf" or (len(content_bytes) >= 4 and content_bytes[:4] == b"%PDF")
        if ext in {".md", ".txt"}:
            try:
                text = content_bytes.decode("utf-8", errors="ignore").strip()
            except Exception:
                text = ""
            if text:
                docs.append((f"upload://{fname}", text))
        elif is_pdf_guess and (PdfReader is not None or pdfminer_extract_text is not None or fitz is not None):
            # Save to temp and extract
            with tempfile.NamedTemporaryFile(suffix=ext, delete=True) as tmp:
                tmp.write(content_bytes)
                tmp.flush()
                text = ""
                tried: list[str] = []
                # pypdf 优先（若运行时尚未可用，尝试动态导入一次）
                if PdfReader is None:
                    try:
                        from pypdf import PdfReader as _PdfReader  # type: ignore
                        PdfReader = _PdfReader  # type: ignore
                        debug["has_pypdf"] = True
                    except Exception:
                        pass
                if PdfReader is not None:
                    try:
                        reader = PdfReader(tmp.name)
                        pages = []
                        for p in reader.pages:
                            t = p.extract_text() or ""
                            if t.strip():
                                pages.append(t)
                        text = "\n".join(pages).strip()
                        tried.append("pypdf")
                    except Exception:
                        tried.append("pypdf_err")
                        text = ""
                # 若为空尝试 pdfminer 提取
                if pdfminer_extract_text is None:
                    try:
                        from pdfminer.high_level import extract_text as _pdfminer_extract_text  # type: ignore
                        pdfminer_extract_text = _pdfminer_extract_text  # type: ignore
                        debug["has_pdfminer"] = True
                    except Exception:
                        pass
                if (not text) and pdfminer_extract_text is not None:
                    try:
                        text = (pdfminer_extract_text(tmp.name) or "").strip()
                        tried.append("pdfminer")
                    except Exception:
                        tried.append("pdfminer_err")
                        text = ""
                # 若仍为空尝试 PyMuPDF
                if fitz is None:
                    try:
                        import fitz as _fitz  # type: ignore
                        fitz = _fitz  # type: ignore
                        debug["has_pymupdf"] = True
                    except Exception:
                        pass
                if (not text) and fitz is not None:
                    try:
                        with fitz.open(tmp.name) as doc:
                            parts = []
                            for page in doc:
                                t = page.get_text("text") or ""
                                if t.strip():
                                    parts.append(t)
                            text = "\n".join(parts).strip()
                            tried.append("pymupdf")
                    except Exception:
                        tried.append("pymupdf_err")
                        text = ""
                # 如果 PDF 仍为空，默认尝试 OCR（即便未勾选），以提升兼容性
                if (not text):
                    try:
                        import ocrmypdf  # type: ignore
                        with tempfile.NamedTemporaryFile(suffix=ext, delete=True) as tmp_ocr:
                            # 执行 OCR 到新文件
                            ocrmypdf.ocr(tmp.name, tmp_ocr.name, force_ocr=True, skip_text=True, output_type="pdf")
                            # 尝试再走一次提取
                            t2 = ""
                            if PdfReader is not None:
                                try:
                                    reader = PdfReader(tmp_ocr.name)
                                    pages = []
                                    for p in reader.pages:
                                        tt = p.extract_text() or ""
                                        if tt.strip():
                                            pages.append(tt)
                                    t2 = "\n".join(pages).strip()
                                except Exception:
                                    t2 = ""
                            if (not t2) and pdfminer_extract_text is not None:
                                try:
                                    t2 = (pdfminer_extract_text(tmp_ocr.name) or "").strip()
                                except Exception:
                                    t2 = ""
                            if (not t2) and fitz is not None:
                                try:
                                    with fitz.open(tmp_ocr.name) as doc:
                                        parts = []
                                        for page in doc:
                                            tt = page.get_text("text") or ""
                                            if tt.strip():
                                                parts.append(tt)
                                        t2 = "\n".join(parts).strip()
                                except Exception:
                                    t2 = ""
                            if t2:
                                text = t2
                                tried.append("ocrmypdf")
                    except Exception as e:
                        tried.append("ocr_failed")
                debug["pdf_extractors_tried"] = tried
            if text:
                docs.append((f"upload://{fname}", text))
        else:
            # Fallback treat as text
            try:
                text = content_bytes.decode("utf-8", errors="ignore").strip()
                if text:
                    docs.append((f"upload://{fname}", text))
            except Exception:
                pass

    # Handle URL ingestion
    if (not docs) and url:
        u = url.strip()
        try:
            with httpx.Client(timeout=20.0, follow_redirects=True) as client:
                resp = client.get(u)
                ctype = resp.headers.get("content-type", "").lower()
                # arXiv abs 页面仅抽取摘要块
                if "arxiv.org/abs/" in u:
                    try:
                        html = resp.text or ""
                        import re
                        # 兼容 arXiv 经典页面摘要块
                        m = re.search(r"<blockquote[^>]*class=\"abstract\"[^>]*>([\s\S]*?)</blockquote>", html, re.I)
                        if m:
                            block = m.group(1)
                            # 去掉标签与前缀“Abstract:”等
                            block = re.sub(r"<[^>]+>", " ", block)
                            block = re.sub(r"\b(Abstract|ABSTRACT)\s*:\s*", "", block)
                            text = " ".join(block.split()).strip()
                            if text:
                                docs.append((u, text))
                                raise RuntimeError("__INGEST_DONE__")  # 直接跳出外层 try，走后续写库
                    except RuntimeError as _e:
                        if str(_e) != "__INGEST_DONE__":
                            raise
                    except Exception:
                        pass
                is_pdf_guess = ("pdf" in ctype) or (resp.content[:4] == b"%PDF")
                if is_pdf_guess and (PdfReader is not None or pdfminer_extract_text is not None or fitz is not None):
                    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp:
                        tmp.write(resp.content)
                        tmp.flush()
                        text = ""
                        if PdfReader is not None:
                            try:
                                reader = PdfReader(tmp.name)
                                pages = []
                                for p in reader.pages:
                                    t = p.extract_text() or ""
                                    if t.strip():
                                        pages.append(t)
                                text = "\n".join(pages).strip()
                            except Exception:
                                text = ""
                        if (not text) and pdfminer_extract_text is not None:
                            try:
                                text = (pdfminer_extract_text(tmp.name) or "").strip()
                            except Exception:
                                text = ""
                        if (not text) and fitz is not None:
                            try:
                                with fitz.open(tmp.name) as doc:
                                    parts = []
                                    for page in doc:
                                        t = page.get_text("text") or ""
                                        if t.strip():
                                            parts.append(t)
                                    text = "\n".join(parts).strip()
                            except Exception:
                                text = ""
                        if (not text):
                            try:
                                import ocrmypdf  # type: ignore
                                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp_ocr:
                                    ocrmypdf.ocr(tmp.name, tmp_ocr.name, force_ocr=True, skip_text=True, output_type="pdf")
                                    # 再试一次提取
                                    t2 = ""
                                    if PdfReader is not None:
                                        try:
                                            reader = PdfReader(tmp_ocr.name)
                                            pages = []
                                            for p in reader.pages:
                                                tt = p.extract_text() or ""
                                                if tt.strip():
                                                    pages.append(tt)
                                            t2 = "\n".join(pages).strip()
                                        except Exception:
                                            t2 = ""
                                    if (not t2) and pdfminer_extract_text is not None:
                                        try:
                                            t2 = (pdfminer_extract_text(tmp_ocr.name) or "").strip()
                                        except Exception:
                                            t2 = ""
                                    if (not t2) and fitz is not None:
                                        try:
                                            with fitz.open(tmp_ocr.name) as doc:
                                                parts = []
                                                for page in doc:
                                                    tt = page.get_text("text") or ""
                                                    if tt.strip():
                                                        parts.append(tt)
                                                t2 = "\n".join(parts).strip()
                                        except Exception:
                                            t2 = ""
                                    if t2:
                                        text = t2
                            except Exception:
                                # OCR 失败忽略，继续文本兜底
                                pass
                if not text:
                    try:
                        resp.encoding = resp.encoding or "utf-8"
                    except Exception:
                        pass
                    text = (resp.text or "").strip()
        except Exception:
            text = ""
        if text:
            docs.append((u, text))

    if not docs:
        reason = ""
        if file is not None:
            if (debug.get("ext") == ".pdf"):
                if debug.get("pdf_extractors_tried") == []:
                    reason = "无法从PDF提取文本（可能为图片型PDF，建议启用OCR）"
                else:
                    reason = "PDF提取失败（内容可能为扫描图），可尝试启用OCR"
            else:
                reason = "无法读取文件内容或不支持的格式"
        elif url:
            reason = "无法从URL获取文本/PDF内容"
        return {"added": 0, "sources": [], "reason": reason, "debug": debug}

    client = init_chroma()
    add_documents(client, DEFAULT_COLLECTION, docs)
    return {"added": len(docs), "sources": [src for src, _ in docs], "debug": debug}


# ---------------- Eval Summary ---------------- #

@app.get("/eval/summary")
def eval_summary() -> Dict[str, Any]:
    base = os.path.join("data", "eval")
    out: Dict[str, Any] = {}
    if os.path.isdir(base):
        for name in ("summary.json", "generation_summary.json", "hybrid_summary.json"):
            p = os.path.join(base, name)
            if os.path.isfile(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        out[name] = json.load(f)
                except Exception:
                    out[name] = None
    return out or {"message": "no eval outputs found"}


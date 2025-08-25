import os
import hashlib
import re
from typing import List, Tuple, Callable, Optional

import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader
try:
    from rank_bm25 import BM25Okapi
except Exception:
    BM25Okapi = None
try:
    from openai import OpenAI as _OpenAIClient
except Exception:
    _OpenAIClient = None


# 初始化 Chroma 数据库（使用新架构 PersistentClient）
def init_chroma(persist_directory: str = "./data/chroma_db"):
    os.makedirs(persist_directory, exist_ok=True)
    client = chromadb.PersistentClient(path=persist_directory)
    return client


def _get_embedding_function():
    """
    返回一个可调用的 embedding 函数（本地或远程）。

    优先读取环境变量 USE_REMOTE_EMBEDDINGS=1 时使用 DashScope 的 OpenAI 兼容 Embedding 接口：
      - QWEN_EMBED_MODEL (默认 text-embedding-v4)
      - DASHSCOPE_API_KEY
    否则回退为本地 SentenceTransformers（all-MiniLM-L6-v2）。
    """
    use_remote = os.getenv("USE_REMOTE_EMBEDDINGS", "").strip() in {"1", "true", "True"}
    # 尝试从本地配置读取开关与Key/模型
    cfg = None
    try:
        from . import config_local as _cfg1  # python -m 运行
        cfg = _cfg1
    except Exception:
        try:
            import config_local as _cfg2  # 直接运行
            cfg = _cfg2
        except Exception:
            cfg = None
    if not use_remote and cfg is not None:
        use_remote = str(getattr(cfg, "USE_REMOTE_EMBEDDINGS", "")).strip() in {"1", "true", "True"}

    if use_remote and _OpenAIClient is not None:
        api_key = os.getenv("DASHSCOPE_API_KEY", "").strip()
        model = os.getenv("QWEN_EMBED_MODEL", "").strip()
        dim_env = os.getenv("QWEN_EMBED_DIM", "").strip()
        if not api_key and cfg is not None:
            api_key = str(getattr(cfg, "DASHSCOPE_API_KEY", "")).strip()
        if not model and cfg is not None:
            model = str(getattr(cfg, "QWEN_EMBED_MODEL", "qwen-v4")).strip() or "qwen-v4"
        if not dim_env and cfg is not None:
            dim_env = str(getattr(cfg, "QWEN_EMBED_DIM", "")).strip()
        if not model:
            model = "qwen-v4"
        base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        if api_key and model:
            dim = int(dim_env) if dim_env.isdigit() else None
            return _DashscopeEmbeddingFunction(api_key=api_key, model=model, base_url=base_url, dimensions=dim)
    # 本地 ST 嵌入
    return embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")


class _DashscopeEmbeddingFunction:
    """OpenAI 兼容模式的 DashScope Embedding 封装，适配 Chroma 的 embedding_function 接口。"""

    def __init__(self, api_key: str, model: str, base_url: str, dimensions: Optional[int] = None):
        self._client = _OpenAIClient(api_key=api_key, base_url=base_url) if _OpenAIClient else None
        self._model = model
        self._dim = dimensions

    # Chroma 会调用 .name() 来判断冲突
    def name(self) -> str:
        return f"dashscope-embedding::{self._model}"

    def __call__(self, input):  # Chroma expects signature (self, input)
        if not self._client:
            raise RuntimeError("OpenAI client not available for DashScope embedding")
        # 兼容传入单条或批量
        texts = input if isinstance(input, list) else [input]
        # DashScope 限制 batch <= 10
        batch_size = 10
        all_embeddings: list[list[float]] = []
        for i in range(0, len(texts), batch_size):
            chunk = texts[i:i+batch_size]
            kwargs = {"model": self._model, "input": chunk, "encoding_format": "float"}
            if self._dim is not None:
                kwargs["dimensions"] = self._dim
            resp = self._client.embeddings.create(**kwargs)
            all_embeddings.extend([item.embedding for item in resp.data])
        return all_embeddings

    # 兼容可能的接口期望
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.__call__(texts)

    def embed_query(self, text: str) -> list[float]:
        return self.__call__([text])[0]


# 导入文档并向量化
def add_documents(client: chromadb.Client, collection_name: str, documents: List[Tuple[str, str]]):
    """
    将文档加入到 `collection_name` 中。

    documents: List of (source_path, content)
    """
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=_get_embedding_function()
    )

    if not documents:
        return collection

    ids: List[str] = []
    texts: List[str] = []
    metadatas = []
    for source_path, content in documents:
        title = _extract_title_from_content_or_file(source_path, content)
        chunks = _split_text_into_chunks(content)
        for idx, chunk in enumerate(chunks):
            raw_id = f"{source_path}::{idx}"
            stable_id = hashlib.sha1(raw_id.encode("utf-8")).hexdigest()
            ids.append(stable_id)
            texts.append(chunk)
            metadatas.append({"source": source_path, "chunk_index": idx, "title": title})

    if texts:
        # 使用 upsert 防止重复写入
        collection.upsert(documents=texts, metadatas=metadatas, ids=ids)
    return collection


# 查询向量数据库
def query_documents(client: chromadb.Client, collection_name: str, query: str, n_results: int = 3):
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=_get_embedding_function(),
    )
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )
    return results


def load_text_documents_from_dir(directory: str) -> List[Tuple[str, str]]:
    """
    加载目录中的 .txt / .md / .pdf 文本。
    返回 [(source_path, content), ...]
    """
    if not os.path.isdir(directory):
        return []

    supported_exts = {".txt", ".md", ".pdf"}
    loaded: List[Tuple[str, str]] = []
    for root, _, files in os.walk(directory):
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in supported_exts:
                continue
            fpath = os.path.join(root, fname)
            try:
                if ext == ".pdf":
                    text = _extract_text_from_pdf(fpath)
                else:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read().strip()
                if text:
                    loaded.append((fpath, text))
            except Exception:
                # 忽略坏文件
                continue
    return loaded


def _extract_text_from_pdf(path: str) -> str:
    try:
        reader = PdfReader(path)
        texts: List[str] = []
        for page in reader.pages:
            t = page.extract_text() or ""
            if t.strip():
                texts.append(t)
        return "\n".join(texts).strip()
    except Exception:
        return ""


def _extract_title_from_content_or_file(path: str, content: str) -> str:
    try:
        name = os.path.splitext(os.path.basename(path))[0]
        ext = os.path.splitext(path)[1].lower()
        if ext == ".md":
            for line in content.splitlines():
                s = line.strip()
                if not s:
                    continue
                if s.startswith("#"):
                    return _normalize_ws(s.lstrip("#").strip()) or name
            # fallback: first non-empty line
            for line in content.splitlines():
                s = line.strip()
                if s:
                    s = _normalize_ws(s)
                    return (s[:120] + ("…" if len(s) > 120 else ""))
            return name
        if ext == ".txt":
            for line in content.splitlines():
                s = line.strip()
                if s:
                    s = _normalize_ws(s)
                    return (s[:120] + ("…" if len(s) > 120 else ""))
            return name
        if ext == ".pdf":
            try:
                reader = PdfReader(path)
                meta = getattr(reader, "metadata", None)
                if meta and getattr(meta, "title", None):
                    return _normalize_ws(str(meta.title))
            except Exception:
                pass
            return name
        return name
    except Exception:
        return os.path.basename(path)


def _normalize_ws(text: str) -> str:
    if not text:
        return text
    # 替换常见的不可见空白字符为普通空格
    for ch in ("\u00A0", "\u2000", "\u2001", "\u2002", "\u2003", "\u2004", "\u2005", "\u2006", "\u2007", "\u2008", "\u2009", "\u200A", "\u202F", "\u205F", "\u3000"):
        text = text.replace(ch, " ")
    # 折叠多空格
    text = " ".join(text.split())
    return text.strip()


# ---------------- Hybrid Retrieval (BM25 pre-filter) ---------------- #
_bm25_state = {
    "paths": None,  # type: ignore
    "tokens": None,
    "bm25": None,
}


def _simple_tokenize(text: str) -> List[str]:
    text = text.lower()
    # keep words and numbers, split on non-alphanum
    return [t for t in re.split(r"[^a-z0-9_]+", text) if t]


def bm25_select_sources(query: str, data_dir: str = "data", top_n_files: int = 50) -> List[str]:
    if BM25Okapi is None:
        return []
    # Build or reuse BM25 over file-level documents
    if not _bm25_state["bm25"]:
        docs = load_text_documents_from_dir(data_dir)
        paths = [p for p, _ in docs]
        tokens = [_simple_tokenize(txt) for _, txt in docs]
        if not tokens:
            return []
        try:
            bm25 = BM25Okapi(tokens)
        except Exception:
            return []
        _bm25_state["paths"] = paths
        _bm25_state["tokens"] = tokens
        _bm25_state["bm25"] = bm25

    bm25 = _bm25_state["bm25"]
    paths = _bm25_state["paths"] or []
    if not bm25 or not paths:
        return []
    scores = bm25.get_scores(_simple_tokenize(query))
    ranked = sorted(zip(paths, scores), key=lambda x: x[1], reverse=True)
    selected = [p for p, s in ranked[: top_n_files] if s > 0]
    return selected
def bm25_rank_map(query: str, data_dir: str = "data") -> dict:
    """Return {path: 1-based-rank} for current BM25 index; empty if BM25 unavailable."""
    if BM25Okapi is None:
        return {}
    if not _bm25_state["bm25"]:
        # build once
        _ = bm25_select_sources("__warm__", data_dir=data_dir)
    bm25 = _bm25_state["bm25"]
    paths = _bm25_state["paths"] or []
    if not bm25 or not paths:
        return {}
    scores = bm25.get_scores(_simple_tokenize(query))
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    rank_map = {}
    rank = 1
    for idx, sc in ranked:
        if sc <= 0:
            break
        rank_map[paths[idx]] = rank
        rank += 1
    return rank_map


# ---------------- BM25 over chunks + helpers ---------------- #
_bm25_chunk_state = {
    "keys": None,   # [f"{path}::{idx}", ...]
    "tokens": None, # tokenized chunk texts
    "bm25": None,
}


def _build_bm25_chunks(data_dir: str = "data") -> bool:
    docs = load_text_documents_from_dir(data_dir)
    if not docs:
        return False
    keys: List[str] = []
    tokens: List[List[str]] = []
    for path, text in docs:
        for idx, chunk in enumerate(_split_text_into_chunks(text)):
            keys.append(f"{path}::{idx}")
            tokens.append(_simple_tokenize(chunk))
    if not tokens:
        return False
    try:
        bm25 = BM25Okapi(tokens) if BM25Okapi else None
    except Exception:
        bm25 = None
    _bm25_chunk_state["keys"] = keys
    _bm25_chunk_state["tokens"] = tokens
    _bm25_chunk_state["bm25"] = bm25
    return bm25 is not None


def bm25_chunk_rank_map(query: str, data_dir: str = "data") -> dict:
    if BM25Okapi is None:
        return {}
    if not _bm25_chunk_state["bm25"]:
        ok = _build_bm25_chunks(data_dir)
        if not ok:
            return {}
    bm25 = _bm25_chunk_state["bm25"]
    keys: List[str] = _bm25_chunk_state["keys"] or []
    if not bm25 or not keys:
        return {}
    scores = bm25.get_scores(_simple_tokenize(query))
    # rank chunks by score
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    rank_map = {}
    rank = 1
    for idx, sc in ranked:
        if sc <= 0:
            break
        rank_map[keys[idx]] = rank
        rank += 1
    return rank_map


def _split_text_into_chunks(text: str, max_chars: int = 1200, overlap: int = 200) -> List[str]:
    text = text.strip()
    if not text:
        return []
    chunks: List[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end]
        chunks.append(chunk)
        if end >= n:
            break
        start = max(0, end - overlap)
    return chunks
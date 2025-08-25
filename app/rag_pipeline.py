from typing import Dict, List, Optional

from app.chroma_utils import (
    init_chroma,
    add_documents,
    query_documents,
    load_text_documents_from_dir,
    bm25_select_sources,
    bm25_rank_map,
    bm25_chunk_rank_map,
)
from app.qwen_api import qwen_chat


DEFAULT_COLLECTION = "resume_mvp"


_cross_encoder_model = None  # lazy load


def _maybe_load_reranker(model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
    global _cross_encoder_model
    if _cross_encoder_model is None:
        try:
            from sentence_transformers import CrossEncoder
            _cross_encoder_model = CrossEncoder(model_name)
        except Exception:
            _cross_encoder_model = False  # mark unavailable
    return _cross_encoder_model


def _apply_rerank(query: str, sources: List[Dict]) -> List[Dict]:
    model = _maybe_load_reranker()
    if not model or not sources:
        return sources
    pairs = [[query, s["text"]] for s in sources]
    try:
        scores = model.predict(pairs)
        with_scores = []
        for s, sc in zip(sources, scores):
            s2 = dict(s)
            s2["rerank_score"] = float(sc)
            with_scores.append(s2)
        with_scores.sort(key=lambda x: x.get("rerank_score", 0.0), reverse=True)
        return with_scores
    except Exception:
        return sources


def build_context(query: str, n_results: int = 6, use_rerank: bool = False, use_bm25: bool = True) -> List[Dict]:
    client = init_chroma()

    # 若集合为空或需要更新，则索引 data/ 下文档
    try:
        collection = client.get_or_create_collection(name=DEFAULT_COLLECTION)
        need_index = collection.count() == 0
    except Exception:
        need_index = True

    if need_index:
        docs = load_text_documents_from_dir("data")
        if docs:
            add_documents(client, DEFAULT_COLLECTION, docs)

    # 可选：BM25 预过滤，限制检索集合来源（通过简单标题/路径过滤）
    allowed_sources = None
    bm25_ranks = {}
    if use_bm25:
        allowed_sources = set(bm25_select_sources(query) or [])
        bm25_ranks = bm25_rank_map(query)

    results = query_documents(client, DEFAULT_COLLECTION, query, n_results=max(n_results, 8))
    sources = []
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    dists = (results.get("distances", [[]]) or [[None]])[0]
    for i in range(len(docs)):
        doc_text = docs[i]
        meta = metas[i] if i < len(metas) else {}
        dist = dists[i] if i < len(dists) else None
        score = None if dist is None else max(0.0, 1.0 - float(dist))
        item = {
            "text": doc_text,
            "source": meta.get("source", "unknown"),
            "title": meta.get("title", None),
            "score": score,
        }
        if allowed_sources:
            src = item["source"]
            if any(src.endswith(p) or src == p for p in allowed_sources):
                sources.append(item)
        else:
            sources.append(item)

    # RRF 融合（BM25 chunk rank + 向量距离近似Rank）
    if use_bm25 and sources:
        chunk_ranks = bm25_chunk_rank_map(query)
        def approx_vec_rank(s):
            # convert similarity score to a pseudo-rank; higher score -> better rank
            sc = s.get("score") or 0.0
            return max(1, int(100 * (1.0 - sc)))
        fused = []
        for s in sources:
            src = s.get("source", "")
            # 粗略估计chunk_id（文件级无法唯一定位chunk，忽略，退化为文件级RRF）
            # 这里使用文件级rank作为替代
            file_rank = bm25_ranks.get(src)
            vec_rank = approx_vec_rank(s)
            rrf = 0.0
            if file_rank:
                rrf += 1.0 / (60 + file_rank)
            rrf += 1.0 / (60 + vec_rank)
            s2 = dict(s)
            s2["rrf"] = rrf
            fused.append(s2)
        fused.sort(key=lambda x: x.get("rrf", 0.0), reverse=True)
        sources = fused
    if use_rerank:
        sources = _apply_rerank(query, sources)
    return sources


def rag_pipeline(query: str, use_rerank: bool = False, use_bm25: bool = True) -> Dict:
    sources = build_context(query, use_rerank=use_rerank, use_bm25=use_bm25)
    # 组装带编号的上下文
    context_lines = []
    for idx, s in enumerate(sources, start=1):
        display_name = s.get("title") or s.get("source")
        context_lines.append(f"[{idx}] {display_name}\n{s['text']}")
    context_text = "\n\n".join(context_lines)

    system_prompt = (
        "你是一个严谨的AI助手。基于提供的资料回答用户问题。"
        "若资料不足以回答，请明确说明‘资料不足’并给出你能给出的通用建议。"
    )
    user_prompt = (
        f"问题：{query}\n\n"
        f"以下是可用资料（可能不完整）：\n{context_text}\n\n"
        "请基于上述资料进行回答，并在末尾以 [1][2]... 的编号形式给出参考来源。"
    )

    answer = qwen_chat(system_prompt=system_prompt, user_prompt=user_prompt)
    # 去重来源（按出现顺序），同时保留最高相似度分数
    unique: Dict[str, float] = {}
    ordered = []
    for s in sources:
        src = s.get("source", "unknown")
        score = s.get("score")
        if src not in unique:
            unique[src] = score if score is not None else -1.0
            ordered.append(src)
        else:
            if score is not None and score > unique[src]:
                unique[src] = score
    enriched = []
    title_by_src = {}
    for s in sources:
        if s.get("source") not in title_by_src and s.get("title"):
            title_by_src[s["source"]] = s["title"]
    text_by_src = {}
    url_by_src = {}
    for s in sources:
        sc = s.get("source")
        if sc and sc not in text_by_src:
            text_by_src[sc] = s.get("text", "")
        if sc and sc not in url_by_src:
            import re as _re
            txt = s.get("text", "") or ""
            m = _re.search(r"https?://\S+", txt)
            if m:
                url_by_src[sc] = m.group(0)
    for src in ordered:
        # 生成更自然的 snippet：尽量从词/句边界开始，到句末或空白边界结束；避免截断 URL
        raw_text = (text_by_src.get(src, "") or "").strip()
        snippet = ""
        if raw_text:
            import re
            start_off = 0
            head = raw_text[start_off:start_off + 600]
            # 若开头疑似半个英文单词，则跳到下一个空格
            if re.match(r"^[a-z]{2,}\b", head):
                sp = head.find(" ")
                if 0 <= sp <= 40:
                    start_off += sp + 1
                    head = raw_text[start_off:start_off + 600]
            # 结束位置：优先句末标点（在起始后>=200），否则最后一个空白（<=400），否则硬截断
            end_rel = None
            m = re.search(r"[。！？!?.]", head[200:])
            if m:
                end_rel = 200 + m.end()
            else:
                cut = min(len(head), 400)
                last_space = head.rfind(" ", 200, cut)
                end_rel = last_space if last_space != -1 else cut
            end_off = start_off + end_rel
            snippet = raw_text[start_off:end_off].rstrip()
            # 若结尾包含未完的 URL，则补全到下一个空白
            tail = raw_text[end_off:end_off + 200]
            m_url_open = re.search(r"(https?://\S*)$", snippet)
            if m_url_open:
                m_more = re.match(r"\S+", tail)
                if m_more:
                    snippet = snippet + m_more.group(0)
            # 若结尾是“链接:”/“链接：”，尝试拼接后续 URL
            if re.search(r"链接[:：]\s*$", snippet):
                m_tail_url = re.search(r"https?://\S+", tail)
                if m_tail_url:
                    snippet = snippet + " " + m_tail_url.group(0)
        # 去掉开头很短的残词（如 "in ")
        snippet = _trim_leading_short_word(snippet)
        enriched.append({
            "source": src,
            "title": title_by_src.get(src),
            "score": (unique[src] if unique[src] >= 0 else None),
            "snippet": snippet,
            "url": url_by_src.get(src),
        })
    # 正确返回 RAG 问答结果
    return {"answer": answer, "sources": enriched}


def _trim_leading_short_word(s: str) -> str:
    try:
        import re
        return re.sub(r"^[a-zA-Z]{1,3}\b\s+", "", s)
    except Exception:
        return s


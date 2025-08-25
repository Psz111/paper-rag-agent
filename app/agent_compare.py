from typing import Dict, List, Optional

from app.rag_pipeline import build_context
from app.qwen_api import qwen_chat
from app.eval_utils import verify_and_revise


COMPARE_PROMPT = (
    "你是一名严谨的论文对比助手。仅依据提供的资料，输出两到三篇论文的差异对比。\n"
    "要求：\n"
    "- 只用上下文，禁止臆测；缺失处标注‘资料不足’。\n"
    "- 先给一段<=4行的简要总结（要点式，附 [i]）。\n"
    "- 然后输出一个紧凑的 Markdown 表格（窄列）：\n"
    "  列：论文 | 方法要点 | 数据/设置 | 主要指标 | 开源/资源 | 备注。\n"
    "  每格尽量附 [i] 引用编号；控制每格不超过一两句话。\n"
    "- 不要在文末再输出‘参考来源’列表（前端会展示来源 chips）。\n"
)


def generate_comparison(
    topic: str,
    picks: Optional[List[str]] = None,
    use_rerank: bool = True,
    use_bm25: bool = True,
    k_ctx: int = 8,
    temperature: Optional[float] = 0.2,
    self_check: bool = False,
) -> Dict:
    """
    生成论文对比：基于主题检索若干论文（或使用 picks 指定的标题关键字），输出差异表。
    返回 { table: str, sources: List[Dict] }
    """
    sources = build_context(topic, n_results=max(10, k_ctx), use_rerank=use_rerank, use_bm25=use_bm25)
    # 选取2-3个不同来源
    chosen: List[Dict] = []
    seen = set()
    for s in sources:
        title = (s.get("title") or "").strip()
        if picks:
            # 如果提供 picks，则优先包含包含关键字的标题
            if not any(p.lower() in title.lower() for p in picks):
                continue
        src = s.get("source")
        if src and src not in seen:
            seen.add(src)
            chosen.append(s)
        if len(chosen) >= 3:
            break
    if not chosen:
        # 回退前2条
        chosen = sources[:2]

    # 组装上下文
    ctx_lines: List[str] = []
    for idx, s in enumerate(chosen, start=1):
        display = s.get("title") or s.get("source")
        ctx_lines.append(f"[{idx}] {display}\n{s.get('text','')}")
    context_text = "\n\n".join(ctx_lines)

    user_prompt = (
        f"对比主题或需求：{topic}\n\n"
        f"以下为对比所用资料：\n{context_text}\n\n"
        "请输出符合要求的Markdown表格，并在表格后附‘参考来源’的编号清单。"
    )
    table = qwen_chat(system_prompt=COMPARE_PROMPT, user_prompt=user_prompt, temperature=temperature)
    if self_check:
        table = verify_and_revise(context_text, table)
    table = _strip_reference_trailer(table)
    # 生成 snippet（句/空白边界优先）
    def make_snippet(text: str) -> str:
        t = (text or "").strip()
        if not t:
            return ""
        import re
        start_off = 0
        head = t[start_off:start_off + 600]
        if re.match(r"^[a-z]{2,}\b", head):
            sp = head.find(" ")
            if 0 <= sp <= 40:
                start_off += sp + 1
                head = t[start_off:start_off + 600]
        m_end = re.search(r"[。！？!?.]", head[200:])
        if m_end:
            end_rel = 200 + m_end.end()
        else:
            cut = min(len(head), 400)
            last_space = head.rfind(" ", 200, cut)
            end_rel = last_space if last_space != -1 else cut
        end_off = start_off + end_rel
        snip = t[start_off:end_off].rstrip()
        tail = t[end_off:end_off + 200]
        m_url_open = re.search(r"(https?://\S*)$", snip)
        if m_url_open:
            m_more = re.match(r"\S+", tail)
            if m_more:
                snip = snip + m_more.group(0)
        if re.search(r"链接[:：]\s*$", snip):
            m_tail_url = re.search(r"https?://\S+", tail)
            if m_tail_url:
                snip = snip + " " + m_tail_url.group(0)
        return snip

    # 提取 URL（若上下文中含链接）
    def pick_url(text: str) -> Optional[str]:
        import re
        m = re.search(r"https?://\S+", text or "")
        return m.group(0) if m else None

    return {
        "table": table,
        "sources": [
            {
                "source": s.get("source"),
                "title": s.get("title"),
                "score": s.get("score"),
                "snippet": make_snippet(s.get("text", "")),
                "url": pick_url(s.get("text", "")),
            }
            for s in chosen
        ],
    }


def _strip_reference_trailer(text: str) -> str:
    try:
        import re
        return re.sub(r"(?:\n|\r|\r\n)?\s*(参考来源|References)\s*[:：]?[\s\S]*$", "", text).rstrip()
    except Exception:
        return text



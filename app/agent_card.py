from typing import Dict, List, Optional

from app.rag_pipeline import build_context
from app.qwen_api import qwen_chat
from app.eval_utils import verify_and_revise


CARD_PROMPT = (
    "你是一名严谨的论文速读助手。请仅依据提供的资料生成一张‘速读卡’，30秒内可读完。\n"
    "要求：\n"
    "- 严格基于上下文，禁止臆测；资料不足处明确标注‘资料不足’。\n"
    "- 输出使用 Markdown，分为以下小节，且每条要点尽量附一段原文短引文（<=120字）与参考编号 [i]：\n"
    "  1) 题目与来源\n"
    "  2) 核心问题\n"
    "  3) 方法概述（1-3条）\n"
    "  4) 关键贡献（1-3条）\n"
    "  5) 实验与指标（数据集/设置/主要数值）\n"
    "  6) 局限与未来方向（1-2条）\n"
    "- 只在正文中用 [i] 编号标注引用，不要在文末再输出‘参考来源’列表（前端会展示来源）。\n"
)


def generate_reading_card(
    query: str,
    use_rerank: bool = True,
    use_bm25: bool = True,
    k_ctx: int = 6,
    temperature: Optional[float] = 0.2,
    self_check: bool = False,
) -> Dict:
    """
    生成速读卡：检索 -> 组装上下文 -> 生成卡片内容。
    返回 { card: str, sources: List[Dict] }
    """
    sources = build_context(query, n_results=max(8, k_ctx), use_rerank=use_rerank, use_bm25=use_bm25)
    # 组装带编号的上下文（标题优先）
    context_lines: List[str] = []
    for idx, s in enumerate(sources[:k_ctx], start=1):
        display_name = s.get("title") or s.get("source")
        context_lines.append(f"[{idx}] {display_name}\n{s.get('text','')}")
    context_text = "\n\n".join(context_lines)

    user_prompt = (
        f"论文主题或问题：{query}\n\n"
        f"以下为可用资料（可能不完整）：\n{context_text}\n\n"
        "请生成符合要求的速读卡。"
    )
    card = qwen_chat(system_prompt=CARD_PROMPT, user_prompt=user_prompt, temperature=temperature)
    if self_check:
        card = verify_and_revise(context_text, card)
    card = _strip_reference_trailer(card)
    # 返回生成结果与来源（保留 title/score）
    # 生成 snippet（句/空白边界优先）
    def make_snippet(text: str) -> str:
        t = (text or "").strip()
        if not t:
            return ""
        import re
        start_off = 0
        head = t[start_off:start_off + 600]
        # 若开头疑似半个英文单词，则跳到下一个空格
        if re.match(r"^[a-z]{2,}\b", head):
            sp = head.find(" ")
            if 0 <= sp <= 40:
                start_off += sp + 1
                head = t[start_off:start_off + 600]
        # 结束位置
        m_end = re.search(r"[。！？!?.]", head[200:])
        if m_end:
            end_rel = 200 + m_end.end()
        else:
            cut = min(len(head), 400)
            last_space = head.rfind(" ", 200, cut)
            end_rel = last_space if last_space != -1 else cut
        end_off = start_off + end_rel
        snip = t[start_off:end_off].rstrip()
        # URL 补全
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
        "card": card,
        "sources": [
            {
                "source": s.get("source"),
                "title": s.get("title"),
                "score": s.get("score"),
                "snippet": make_snippet(s.get("text", "")),
                "url": pick_url(s.get("text", "")),
            }
            for s in sources[:k_ctx]
        ],
    }


def _strip_reference_trailer(text: str) -> str:
    """移除文末的“参考来源/References”清单，保留正文中的 [i] 编号。"""
    try:
        import re
        # 匹配从“参考来源/References”开始到文末的块
        return re.sub(r"(?:\n|\r|\r\n)?\s*(参考来源|References)\s*[:：]?[\s\S]*$", "", text).rstrip()
    except Exception:
        return text



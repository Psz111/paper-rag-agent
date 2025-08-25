import re
from typing import Dict, Tuple, List, Optional


def detect_intent(query: str) -> Tuple[str, Dict]:
    """
    轻量路由器：根据用户输入判定意图并抽取必要参数。
    返回 (intent, args)
    intent ∈ { chat_free, rag_answer, reading_card, compare_papers, run_eval }
    """
    q = query.strip()
    q_lower = q.lower()

    # 显式命令关键词优先
    if re.search(r"(速读|速读卡|阅读卡|reading\s*card|summar(y|ise))", q_lower):
        return "reading_card", {"query": q}

    if re.search(r"(对比|比较|compare|contrast)", q_lower):
        picks: Optional[List[str]] = None
        # 粗略抽取 A 和 B：对比A和B / compare A and B
        m = re.search(r"对比\s*([^和]+)\s*和\s*([^，。\s]+)", q)
        if m:
            picks = [m.group(1).strip(), m.group(2).strip()]
        return "compare_papers", {"topic": q, "picks": picks}

    if re.search(r"(评估|evaluation|metrics)", q_lower):
        return "run_eval", {"kind": "hybrid"}

    # 论文问答相关关键词 → RAG
    if re.search(r"(论文|paper|方法|贡献|指标|实验|数据集|diffusion|nerf|llm|综述)", q_lower):
        return "rag_answer", {"query": q}

    # 默认闲聊
    return "chat_free", {"query": q}



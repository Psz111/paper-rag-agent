from typing import Dict, List, Optional, Tuple

from app.rag_pipeline import rag_pipeline
from app.agent_card import generate_reading_card
from app.agent_compare import generate_comparison


def tool_rag_answer(query: str, *, use_rerank: bool = True, use_bm25: bool = True, temperature: float = 0.2) -> Dict:
    # 温度在 rag_pipeline 内部 qwen_chat 使用默认值；若需要，也可扩展传参
    res = rag_pipeline(query, use_rerank=use_rerank, use_bm25=use_bm25)
    return {"type": "rag_answer", "data": res}


def tool_reading_card(query: str, *, use_rerank: bool = True, use_bm25: bool = True, k_ctx: int = 6, temperature: float = 0.2, self_check: bool = False) -> Dict:
    res = generate_reading_card(query, use_rerank=use_rerank, use_bm25=use_bm25, k_ctx=k_ctx, temperature=temperature, self_check=self_check)
    return {"type": "reading_card", "data": res}


def tool_compare_papers(topic: str, picks: Optional[List[str]] = None, *, use_rerank: bool = True, use_bm25: bool = True, k_ctx: int = 8, temperature: float = 0.2, self_check: bool = False) -> Dict:
    res = generate_comparison(topic, picks=picks, use_rerank=use_rerank, use_bm25=use_bm25, k_ctx=k_ctx, temperature=temperature, self_check=self_check)
    return {"type": "compare_papers", "data": res}



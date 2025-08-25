import csv
import json
import math
from typing import List, Dict, Tuple

from app.rag_pipeline import build_context
from app.qwen_api import qwen_chat

_nli_pipeline = None


def _load_nli_pipeline():
    global _nli_pipeline
    if _nli_pipeline is None:
        try:
            from transformers import pipeline
            # 一个较稳的多域NLI模型；如不可用可切换 bart-large-mnli
            _nli_pipeline = pipeline("text-classification", model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli")
        except Exception:
            _nli_pipeline = False
    return _nli_pipeline


def _split_sentences(text: str) -> List[str]:
    if not text:
        return []
    # 简单分句：句号/问号/感叹号/换行
    import re
    parts = re.split(r"[。！？!?.\n]+", text)
    return [p.strip() for p in parts if p.strip()]


def _nli_entailment_ratio(context: str, answer: str) -> Dict[str, float]:
    nli = _load_nli_pipeline()
    if not nli:
        return {"entail_ratio": -1.0, "neutral_ratio": -1.0, "contradict_ratio": -1.0}
    sents = _split_sentences(answer)
    if not sents:
        return {"entail_ratio": 0.0, "neutral_ratio": 1.0, "contradict_ratio": 0.0}
    labels = []
    for s in sents:
        try:
            res = nli([(context, s)], truncation=True)
            # pipeline with pair expects using "text-classification" sometimes doesn't support pair; fallback: premise + hypothesis concatenation
        except Exception:
            try:
                res = nli(context + "\n\n" + s)
            except Exception:
                res = [{"label": "NEUTRAL", "score": 1.0}]
        out = res[0]
        label = out.get("label", "NEUTRAL").upper()
        labels.append(label)
    total = len(labels)
    entail = sum(1 for l in labels if "ENTAIL" in l)
    contra = sum(1 for l in labels if "CONTRAD" in l)
    neutral = total - entail - contra
    return {
        "entail_ratio": entail / total if total else 0.0,
        "neutral_ratio": neutral / total if total else 0.0,
        "contradict_ratio": contra / total if total else 0.0,
    }


def run_generation_eval(items: List[Dict], use_rerank: bool = True, use_bm25: bool = True, k_ctx: int = 4) -> Tuple[List[Dict], Dict[str, float]]:
    """
    对每个样例生成答案，并用本地NLI计算句子级蕴含比例作为“faithfulness”近似。
    返回 (per_item_records, summary)
    """
    per_items: List[Dict] = []
    for it in items:
        q = it["question"]
        src = build_context(q, n_results=max(8, k_ctx), use_rerank=use_rerank, use_bm25=use_bm25)
        ctx_text = "\n\n".join(s.get("text", "") for s in src[:k_ctx])
        system_prompt = "你是一个严谨的AI助手。基于提供的资料回答用户问题；若资料不足请明确说明并拒绝臆测。"
        user_prompt = f"问题：{q}\n\n资料：\n{ctx_text}\n\n请给出简洁要点式回答，并在末尾用 [1][2]... 形式列出参考来源编号。"
        ans = qwen_chat(system_prompt, user_prompt)
        nli_scores = _nli_entailment_ratio(ctx_text, ans)
        rec = {
            "question": q,
            "answer": ans,
            **nli_scores,
        }
        per_items.append(rec)
    # summary
    valid = [r for r in per_items if r["entail_ratio"] >= 0]
    if valid:
        entail_avg = sum(r["entail_ratio"] for r in valid) / len(valid)
        contra_avg = sum(r["contradict_ratio"] for r in valid) / len(valid)
        neutral_avg = sum(r["neutral_ratio"] for r in valid) / len(valid)
    else:
        entail_avg = contra_avg = neutral_avg = -1.0
    summary = {
        "entailment_avg": entail_avg,
        "contradiction_avg": contra_avg,
        "neutral_avg": neutral_avg,
        "count": len(per_items),
    }
    return per_items, summary


def verify_and_revise(context: str, answer: str) -> str:
    """
    基于本地NLI对答案逐句进行检查：
    - ENTAIL 保留
    - NEUTRAL 保留（可选）
    - CONTRADICTION 删除或标注
    简化策略：删除矛盾句；在结尾附“已基于上下文自检”的提示。
    """
    scores = _nli_entailment_ratio(context, answer)
    # 如果NLI不可用，直接返回原答案
    if scores.get("entail_ratio", -1.0) < 0:
        return answer
    sents = _split_sentences(answer)
    nli = _load_nli_pipeline()
    kept: List[str] = []
    for s in sents:
        try:
            res = nli([(context, s)])
            label = (res[0].get("label") or "NEUTRAL").upper()
        except Exception:
            label = "NEUTRAL"
        if "CONTRAD" in label:
            continue  # 丢弃矛盾句
        kept.append(s)
    revised = "".join(kept).strip()
    if revised and revised != answer.strip():
        revised += "\n\n（已基于上下文进行自检，可能删除了与上下文矛盾的句子）"
    return revised or answer


def recall_at_k(hit_ranks: List[int], k: int) -> float:
    hits = sum(1 for r in hit_ranks if r is not None and r <= k)
    return hits / len(hit_ranks) if hit_ranks else 0.0


def mrr(hit_ranks: List[int]) -> float:
    vals = [1.0 / r for r in hit_ranks if r is not None and r > 0]
    return sum(vals) / len(vals) if vals else 0.0


def ndcg_at_k(rank: int, k: int) -> float:
    if rank is None or rank <= 0 or rank > k:
        return 0.0
    dcg = 1.0 / math.log2(rank + 1)
    return dcg  # IDCG=1


def collect_details(items: List[Dict], use_rerank: bool, use_bm25: bool, k: int) -> List[Dict]:
    details: List[Dict] = []
    for item in items:
        q = item['question']
        expected_src = item['expected_source']
        expected_title = item['expected_title']
        results = build_context(q, n_results=max(10, k), use_rerank=use_rerank, use_bm25=use_bm25)
        rank = None
        for idx, s in enumerate(results, start=1):
            if s.get('source') == expected_src or s.get('title') == expected_title:
                rank = idx
                break
        details.append({
            'question': q,
            'expected_title': expected_title,
            'expected_source': expected_src,
            'rank': rank,
        })
    return details


def summarize(hit_ranks: List[int], k: int, ndcg_k: int) -> Dict[str, float]:
    return {
        f'Recall@{k}': recall_at_k(hit_ranks, k),
        'MRR': mrr(hit_ranks),
        f'NDCG@{ndcg_k}': sum(ndcg_at_k(r, ndcg_k) for r in hit_ranks) / len(hit_ranks) if hit_ranks else 0.0,
    }


def run_retrieval_eval(items: List[Dict], k: int = 5, ndcg_k: int = 10) -> Tuple[Dict[str, float], Dict[str, float], List[Dict], List[Dict]]:
    details_no = collect_details(items, use_rerank=False, use_bm25=False, k=k)
    details_yes = collect_details(items, use_rerank=True, use_bm25=False, k=k)
    ranks_no = [d['rank'] for d in details_no]
    ranks_yes = [d['rank'] for d in details_yes]
    metrics_no = summarize(ranks_no, k=k, ndcg_k=ndcg_k)
    metrics_yes = summarize(ranks_yes, k=k, ndcg_k=ndcg_k)
    return metrics_no, metrics_yes, details_no, details_yes


def run_hybrid_eval(items: List[Dict], k: int = 5, ndcg_k: int = 10) -> Dict[str, Dict[str, float]]:
    base = collect_details(items, use_rerank=False, use_bm25=False, k=k)
    bm25 = collect_details(items, use_rerank=False, use_bm25=True, k=k)
    rerank = collect_details(items, use_rerank=True, use_bm25=False, k=k)
    both = collect_details(items, use_rerank=True, use_bm25=True, k=k)
    return {
        'base': summarize([d['rank'] for d in base], k=k, ndcg_k=ndcg_k),
        'bm25_only': summarize([d['rank'] for d in bm25], k=k, ndcg_k=ndcg_k),
        'rerank_only': summarize([d['rank'] for d in rerank], k=k, ndcg_k=ndcg_k),
        'bm25_rerank': summarize([d['rank'] for d in both], k=k, ndcg_k=ndcg_k),
    }


def save_eval_outputs(details_no: List[Dict], details_yes: List[Dict], metrics_no: Dict[str, float], metrics_yes: Dict[str, float], out_csv: str, out_json: str, k: int, ndcg_k: int, eval_file: str) -> None:
    with open(out_csv, 'w', encoding='utf-8', newline='') as w:
        writer = csv.writer(w)
        writer.writerow(['question', 'expected_title', 'expected_source', 'rank_no_rerank', 'rank_with_rerank'])
        for d0, d1 in zip(details_no, details_yes):
            writer.writerow([d0['question'], d0['expected_title'], d0['expected_source'], d0['rank'], d1['rank']])
    summary = {
        'no_rerank': metrics_no,
        'with_rerank': metrics_yes,
        'config': {'k': k, 'ndcg_k': ndcg_k, 'eval_file': eval_file},
    }
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)


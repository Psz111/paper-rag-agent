import argparse
import csv
import json
import pathlib
import statistics
import sys
from typing import List, Dict

# 项目根目录优先
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.rag_pipeline import build_context


def recall_at_k(hit_ranks: List[int], k: int) -> float:
    hits = sum(1 for r in hit_ranks if r is not None and r <= k)
    return hits / len(hit_ranks) if hit_ranks else 0.0


def mrr(hit_ranks: List[int]) -> float:
    vals = [1.0 / r for r in hit_ranks if r is not None and r > 0]
    return statistics.mean(vals) if vals else 0.0


def ndcg_at_k(rank: int, k: int) -> float:
    """Single relevant doc NDCG@k. rank is 1-based or None."""
    if rank is None or rank <= 0 or rank > k:
        return 0.0
    # DCG with rel=1 at position rank
    import math
    dcg = 1.0 / math.log2(rank + 1)
    idcg = 1.0  # ideal rank = 1 -> 1/log2(2) = 1
    return dcg / idcg


def collect_details(eval_path: pathlib.Path, use_rerank: bool, use_bm25: bool, k: int) -> List[Dict]:
    details: List[Dict] = []
    with eval_path.open('r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
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
                'expected_source': expected_src,
                'expected_title': expected_title,
                'rank': rank,
            })
    return details


def summarize(hit_ranks: List[int], k: int, ndcg_k: int) -> Dict[str, float]:
    return {
        f'Recall@{k}': recall_at_k(hit_ranks, k),
        'MRR': mrr(hit_ranks),
        f'NDCG@{ndcg_k}': statistics.mean([ndcg_at_k(r, ndcg_k) for r in hit_ranks]) if hit_ranks else 0.0,
    }


def main():
    parser = argparse.ArgumentParser(description='Evaluate retrieval with/without rerank and BM25 prefilter')
    parser.add_argument('--eval', default='data/eval/eval_set.jsonl')
    parser.add_argument('--k', type=int, default=5)
    parser.add_argument('--ndcg_k', type=int, default=10)
    parser.add_argument('--out_csv', default='data/eval/eval_results.csv')
    parser.add_argument('--out_json', default='data/eval/summary.json')
    args = parser.parse_args()

    p = pathlib.Path(args.eval)
    out_csv = pathlib.Path(args.out_csv)
    out_json = pathlib.Path(args.out_json)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    print('Evaluating base (no BM25, no rerank)...')
    details_base = collect_details(p, use_rerank=False, use_bm25=False, k=args.k)
    ranks_base = [d['rank'] for d in details_base]
    metrics_base = summarize(ranks_base, k=args.k, ndcg_k=args.ndcg_k)
    print(metrics_base)

    print('Evaluating BM25 only...')
    details_bm25 = collect_details(p, use_rerank=False, use_bm25=True, k=args.k)
    ranks_bm25 = [d['rank'] for d in details_bm25]
    metrics_bm25 = summarize(ranks_bm25, k=args.k, ndcg_k=args.ndcg_k)
    print(metrics_bm25)

    print('Evaluating rerank only...')
    details_rerank = collect_details(p, use_rerank=True, use_bm25=False, k=args.k)
    ranks_rerank = [d['rank'] for d in details_rerank]
    metrics_rerank = summarize(ranks_rerank, k=args.k, ndcg_k=args.ndcg_k)
    print(metrics_rerank)

    print('Evaluating BM25 + rerank...')
    details_both = collect_details(p, use_rerank=True, use_bm25=True, k=args.k)
    ranks_both = [d['rank'] for d in details_both]
    metrics_both = summarize(ranks_both, k=args.k, ndcg_k=args.ndcg_k)
    print(metrics_both)

    # Save per-sample CSV
    with out_csv.open('w', encoding='utf-8', newline='') as w:
        writer = csv.writer(w)
        writer.writerow(['question', 'expected_title', 'expected_source', 'rank_base', 'rank_bm25', 'rank_rerank', 'rank_bm25_rerank'])
        for i in range(len(details_base)):
            d_base = details_base[i]
            d_bm25 = details_bm25[i] if i < len(details_bm25) else {'rank': None}
            d_rerank = details_rerank[i] if i < len(details_rerank) else {'rank': None}
            d_both = details_both[i] if i < len(details_both) else {'rank': None}
            writer.writerow([
                d_base['question'], d_base['expected_title'], d_base['expected_source'],
                d_base['rank'], d_bm25['rank'], d_rerank['rank'], d_both['rank']
            ])

    # Save summary JSON
    summary = {
        'base': metrics_base,
        'bm25_only': metrics_bm25,
        'rerank_only': metrics_rerank,
        'bm25_rerank': metrics_both,
        'config': {'k': args.k, 'ndcg_k': args.ndcg_k, 'eval_file': str(p)},
    }
    out_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Saved CSV to {out_csv} and summary to {out_json}')


if __name__ == '__main__':
    main()



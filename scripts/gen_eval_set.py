import argparse
import json
import pathlib
import re
import sys
from typing import List, Dict


# 确保本项目根目录优先于 site-packages
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _extract_title_from_md(content: str, fallback: str) -> str:
    # 优先取首个一级/二级标题
    for line in content.splitlines():
        s = line.strip()
        if s.startswith('#'):
            return re.sub(r'^#+\s*', '', s).strip()
    # 回退：第一行非空文本
    for line in content.splitlines():
        s = line.strip()
        if s:
            return s[:200]
    return fallback


def scan_md_files(root: pathlib.Path) -> List[pathlib.Path]:
    files: List[pathlib.Path] = []
    for p in root.rglob('*.md'):
        if p.is_file():
            files.append(p)
    return files


_STOP = {
    'the','of','and','for','with','via','from','into','to','are','is','on','in','a','an','by','at','as','using','use','towards','toward','based','large','language','model','models'
}


def _extract_keywords(title: str, content: str, max_k: int = 3) -> List[str]:
    txt = (title + ' ' + content[:400]).lower()
    tokens = re.split(r"[^a-z0-9\-]+", txt)
    cand = [t for t in tokens if len(t) > 2 and t not in _STOP]
    uniq: List[str] = []
    for t in cand:
        if t not in uniq:
            uniq.append(t)
        if len(uniq) >= max_k:
            break
    return uniq


def build_questions(title: str, content: str, mode: str = 'title') -> List[str]:
    if mode == 'keywords':
        kws = _extract_keywords(title, content)
        hint = '、'.join(kws) if kws else title
        return [
            f"关于{hint}的论文，其核心贡献是什么？请给出要点并附来源编号。",
            f"围绕{hint}，与以往方法相比的关键差异是什么？请附来源编号。",
        ]
    # 默认：带标题，以便弱监督命中文档
    return [
        f"关于《{title}》，这篇论文的核心贡献是什么？请给出要点并附来源编号。",
        f"《{title}》与以往方法相比的关键差异是什么？请附来源编号。",
    ]


def main():
    parser = argparse.ArgumentParser(description='Generate eval set from markdown summaries')
    parser.add_argument('--data_dir', default='data', help='root data directory')
    parser.add_argument('--out', default='data/eval/eval_set.jsonl', help='output eval jsonl')
    parser.add_argument('--max_per_file', type=int, default=2)
    parser.add_argument('--limit', type=int, default=200)
    parser.add_argument('--mode', choices=['title','keywords'], default='title', help='question construction mode')
    args = parser.parse_args()

    root = pathlib.Path(args.data_dir)
    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    files = scan_md_files(root)
    records: List[Dict] = []
    for f in files:
        try:
            content = f.read_text(encoding='utf-8')
        except Exception:
            continue
        title = _extract_title_from_md(content, fallback=f.stem)
        qs = build_questions(title, content, mode=args.mode)[: args.max_per_file]
        for q in qs:
            records.append({
                'question': q,
                'expected_title': title,
                'expected_source': str(f),
            })
        if len(records) >= args.limit:
            break

    with out_path.open('w', encoding='utf-8') as w:
        for r in records:
            w.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(f'Wrote {len(records)} items to {out_path}')


if __name__ == '__main__':
    main()



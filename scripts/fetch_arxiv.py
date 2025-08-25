import argparse
import pathlib
import time
import datetime as dt
from urllib.parse import quote
import sys

import requests
import feedparser

# 同样确保项目根目录优先导入，避免 `app` 包名冲突
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def build_query(query: str, categories: list[str]) -> str:
    cat_clause = " OR ".join([f"cat:{c}" for c in categories]) if categories else "cat:cs.AI"
    # 使用 all: 进行全文检索，结合分类
    return f"(all:{query}) AND ({cat_clause})"


def fetch_arxiv(query: str, categories: list[str], max_results: int) -> feedparser.FeedParserDict:
    base = "http://export.arxiv.org/api/query"
    q = build_query(query, categories)
    url = (
        f"{base}?search_query={quote(q)}&start=0&max_results={max_results}"
        f"&sortBy=submittedDate&sortOrder=descending"
    )
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return feedparser.parse(resp.text)


def within_days(entry, days: int) -> bool:
    if not days or days <= 0:
        return True
    try:
        updated = entry.get("updated_parsed") or entry.get("published_parsed")
        if not updated:
            return True
        updated_dt = dt.datetime(*updated[:6])
        return (dt.datetime.utcnow() - updated_dt) <= dt.timedelta(days=days)
    except Exception:
        return True


def save_markdown(entry, out_dir: pathlib.Path):
    title = (entry.title or "").strip().replace("\n", " ")
    summary = (entry.summary or "").strip()
    pdf_url = next((l.href for l in entry.links if getattr(l, "type", "") == "application/pdf"), entry.link)
    fid = entry.id.split("/")[-1]
    out = out_dir / f"arxiv_{fid}.md"
    content = f"# {title}\n\n{summary}\n\n链接: {pdf_url}\n"
    out.write_text(content, encoding="utf-8")
    return out


def maybe_download_pdf(entry, out_dir: pathlib.Path):
    pdf_url = next((l.href for l in entry.links if getattr(l, "type", "") == "application/pdf"), None)
    if not pdf_url:
        return None
    fid = entry.id.split("/")[-1]
    out = out_dir / f"arxiv_{fid}.pdf"
    try:
        with requests.get(pdf_url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(out, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        return out
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(description="Fetch arXiv papers into data directory")
    parser.add_argument("--query", default="LLM OR diffusion OR NeRF", help="search keywords")
    parser.add_argument("--categories", nargs="*", default=["cs.AI", "cs.LG", "cs.CV", "stat.ML"], help="arXiv categories")
    parser.add_argument("--days", type=int, default=30, help="only keep papers within N days")
    parser.add_argument("--max_results", type=int, default=50, help="max results to fetch from arXiv API")
    parser.add_argument("--download_pdf", action="store_true", help="also download PDFs")
    parser.add_argument("--out_dir", default="data/arxiv", help="output directory under project root")
    args = parser.parse_args()

    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    feed = fetch_arxiv(args.query, args.categories, args.max_results)
    saved = 0
    for entry in feed.entries:
        if not within_days(entry, args.days):
            continue
        md_path = save_markdown(entry, out_dir)
        saved += 1
        if args.download_pdf:
            maybe_download_pdf(entry, out_dir)
        time.sleep(0.2)

    print(f"saved {saved} markdown files to {out_dir}")


if __name__ == "__main__":
    main()



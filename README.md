RAG + Agent MVP
================

Concise, reproducible RAG + Agent demo with:
- Chroma (local persistent vector DB)
- Sentence-Transformers embeddings (fallback) or DashScope Qwen embeddings (remote)
- FastAPI backend, Next.js frontend, optional Streamlit demo

Demo (Video/GIF)
----------------
[▶ Watch the demo](https://github.com/Psz111/paper-rag-agent/releases/latest/download/demo.mp4)

- Optional preview GIF: place `assets/demo.gif` and add the line below to show a thumbnail.

  ![Demo](assets/demo.gif)

- Or host externally (GitHub Release/Issue/OSS/YouTube) and link, e.g. `[▶ Watch the 2‑min demo](https://your.video.link)`

Features
--------
- Multi-tool Agent workflows: knowledge QA, reading card, paper comparison (router + tools + pseudo‑streaming).
- Hybrid retrieval: Chroma + BM25 prefilter + RRF fusion; optional CrossEncoder rerank.
- Fast ingest: PDF/MD/TXT/URL with robust PDF extraction and OCR fallback.
- Eval loop: retrieval (Recall@k/MRR/NDCG) and generation self-check via NLI entailment.

Quickstart
----------
Backend (FastAPI):
```bash
pip install -r requirements.txt
uvicorn app.api:app --reload --port 8000
```

Frontend (Next.js):
```bash
cd frontend
npm ci --no-audit --no-fund
npm run dev -- -p 5173
```

Optional: Docker (Streamlit demo)
```bash
docker compose up --build
```

Embeddings
----------
- Local fallback: Sentence-Transformers `all-MiniLM-L6-v2`.
- Remote (recommended): set environment vars and reindex.

```bash
# Windows PowerShell examples
$env:USE_REMOTE_EMBEDDINGS="1"
$env:DASHSCOPE_API_KEY="<your-key>"
$env:QWEN_EMBED_MODEL="qwen-v4"
Remove-Item -Recurse -Force .\data\chroma_db
python scripts/index_incremental.py --force
```

Ingest
------
- REST: `POST /ingest` with file upload or URL (supports arXiv abs page parsing).
- CLI (examples):

```bash
python scripts/fetch_arxiv.py --query "LLM OR diffusion" --days 30 --max_results 50 --download_pdf
python scripts/index_incremental.py
```

Evaluation (results in data/eval)
---------------------------------
- Retrieval (k=5, NDCG@10):
  - base: Recall@5 0.944, MRR 0.912, NDCG@10 0.893
  - BM25 only: Recall@5 0.956, MRR 0.997, NDCG@10 0.954
  - rerank only: Recall@5 0.956, MRR 0.996, NDCG@10 0.953
  - BM25+rerank: Recall@5 0.956, MRR 0.997, NDCG@10 0.954
- Generation self-check (NLI, 160 samples): entail 0.434, contradiction 0.164, neutral 0.401

API Surface
-----------
- `POST /chat`, `POST /chat/stream` (pseudo‑streaming, workflow markers)
- `POST /tools/rag`, `/tools/card`, `/tools/compare`
- `POST /ingest` (PDF/MD/TXT/URL)
- `GET /eval/summary` (serve JSON summaries)

Project Structure
-----------------
```
app/
  api.py            # FastAPI endpoints (/chat/stream, /tools/*, /ingest)
  rag_pipeline.py   # Retrieval pipeline (BM25/RRF, rerank, context build)
  chroma_utils.py   # Chroma wrapper + loaders + OCR fallback
  agent_*           # Router, tools, chat loop (workflows)
frontend/
  app/              # Next.js pages (chat, eval)
data/               # Your .txt / .md / .pdf documents
scripts/            # fetch_arxiv.py, index_incremental.py, evaluate.py
```

Notes
-----
- Without a DashScope key, the model falls back to a local placeholder response to keep the UI runnable.
- Frontend eval page at `/eval` renders JSON summaries from the backend.


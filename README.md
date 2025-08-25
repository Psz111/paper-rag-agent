RAG + Agent 简易 MVP
=====================

快速启动一个可演示的 RAG（检索增强生成）+ Agent 应用，基于：

- Chroma 向量库（duckdb+parquet 本地持久化）
- Sentence-Transformers 本地嵌入（默认 all-MiniLM-L6-v2）
- Qwen（阿里云 DashScope，可选；无 Key 时使用本地占位回答）
- Next.js 前端（对话式 UI + 引用 chips + 设置/入库弹层）

目录结构
--------

```
app/
  api.py            # FastAPI API（/chat/stream, /tools/*, /ingest）
  rag_pipeline.py   # RAG 流程（加载->索引->检索->生成）
  chroma_utils.py   # 向量库封装 + 文档加载
  qwen_api.py       # Qwen 封装（可选）
frontend/
  app/page.tsx      # 前端对话页（工作流胶囊、引用 chips、设置/入库弹层、快捷按钮）
data/               # 放置你的 .txt / .md 文档
scripts/
  fetch_arxiv.py     # 拉取 arXiv 摘要/可选PDF -> data/arxiv/
  index_incremental.py # 基于文件哈希的增量索引
```

快速开始（本地）
--------

1) 安装依赖

```bash
pip install -r requirements.txt
```

2) 准备数据

- 将你的简历、项目笔记、技术总结等作为 `.txt`、`.md` 或 `.pdf` 放入 `data/` 目录。

3) 配置 Qwen（可选）

- 设置环境变量：`DASHSCOPE_API_KEY=你的阿里云DashScope Key`
- 默认模型通过 `QWEN_MODEL` 指定（默认 `qwen2.5:7b-instruct`）。
- 若未配置，将自动使用本地占位回答，便于先跑通页面。

4) 启动后端与前端

后端：
```powershell
uvicorn app.api:app --reload --port 8000
```

前端：
```powershell
cd frontend
npm ci --no-audit --no-fund
npm run dev -- -p 5173
```

启用 DashScope 远程向量（qwen-v4）
---------------------------------

无需下载本地嵌入模型即可向量化（推荐）：

1) 设置环境变量

```powershell
$env:USE_REMOTE_EMBEDDINGS="1"
$env:DASHSCOPE_API_KEY="你的Key"
# 可选，默认 text-embedding-v4，也可设为 text-embedding-v4-large
$env:QWEN_EMBED_MODEL="qwen-v4"
```

2) 重建索引

```powershell
Remove-Item -Recurse -Force .\data\chroma_db
python scripts/index_incremental.py --force
```

3) 重启后端以生效

备注：未设置 `USE_REMOTE_EMBEDDINGS=1` 时，系统回退为本地 SentenceTransformers（默认 all-MiniLM-L6-v2）。
可选：自动抓 arXiv 摘要到 data/

```bash
python scripts/fetch_arxiv.py --query "LLM OR diffusion OR NeRF" --categories cs.AI cs.LG cs.CV --days 30 --max_results 50 --download_pdf
```

可选：增量索引（仅索引新增/变更）

```bash
python scripts/index_incremental.py
```
```

常见问题
--------

- 没有任何来源显示？确保 `data/` 内有 `.txt/.md` 文件且非空；首次启动会自动索引。
- 如何清空索引？删除 `data/chroma_db/` 目录即可。
- 如何切换嵌入模型？在 `app/chroma_utils.py` 的 `_get_sentence_transformer_embedding` 中修改模型名。

栈与能力
数据摄取/索引: .md/.txt/.pdf → 标题抽取与空白清洗 → 分块(1200/200) → 向量化 → Chroma 持久化
检索: 向量检索 + 可选 BM25 预过滤 + 可选 CrossEncoder 重排；上下文按 [编号] 标题 + 分数组装
生成: Qwen（DashScope / OpenAI兼容）；无 Key 返回占位
评估:
检索：Recall@k/MRR/NDCG@k（支持“重排对比”“混合检索”四配置）
生成：本地 NLI 近似（Entail/Neutral/Contradiction 比例）
工具脚本: arXiv 摘要抓取、增量索引、评测集生成（标题/关键词）、命令行评估
关键优化与结果
嵌入模型：本地 ST → DashScope text-embedding-v4（OpenAI兼容端点）
混合检索：文件级 BM25 预过滤 + 向量检索 +（可选）重排；加入 RRF 融合
指标（关键词评测集，k=5, NDCG@10）
变更前（MiniLM，本地）：Recall@5≈0.77 / MRR≈0.73 / NDCG@10≈0.66
变更后（v4向量）：
base: Recall@5=0.944 / MRR=0.912 / NDCG@10=0.893
BM25 only: Recall@5=0.956 / MRR=0.997 / NDCG@10=0.954
rerank only: Recall@5=0.956 / MRR=0.996 / NDCG@10=0.953
BM25+rerank: Recall@5=0.956 / MRR=0.997 / NDCG@10=0.954
生成质量（NLI近似，旧向量测试一次）：
entail≈0.43，contradiction≈0.16，neutral≈0.40
结论：更强向量与“抽取式提示”预期能进一步提升 entail、压低 contradiction
使用要点
远程向量开关（任选其一）：
环境变量：USE_REMOTE_EMBEDDINGS=1、DASHSCOPE_API_KEY、QWEN_EMBED_MODEL=text-embedding-v4
或在 app/config_local.py 写同名配置
重建与评估（最小流程）：
清索引：删除 data/chroma_db
重建：python scripts/index_incremental.py --force
启动：python -m streamlit run app/main.py
评估页：跑“混合检索评估”“生成质量评估（NLI近似）”；结果落盘 data/eval/*
Docker 一键启动（可选）
----------------------

```bash
cp .env.example .env
docker compose up --build
```

内置 demo 数据
--------------

项目内置少量可用语料，开箱即用：

- `data/arxiv/demo_llm_trends.md`
- `data/arxiv/demo_rag_eval.md`

可直接使用“📥 入库”上传本地 .md，或在前端粘贴 arXiv 摘要页 URL（如 `https://arxiv.org/abs/2508.15746`）进行摘要入库。
默认开启 BM25 预过滤 + 重排
生成温度 0.2–0.3；提示强调“仅基于上下文回答，不足则拒答；每条要点附 [i] 引用”

环境变量说明（.env.example）
-----------------------------

```
# Backend
DASHSCOPE_API_KEY=
USE_REMOTE_EMBEDDINGS=1
QWEN_EMBED_MODEL=qwen-v4

# Frontend
NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000
```

架构（Mermaid）
---------------

```mermaid
graph LR
  A[Next.js Frontend] -- SSE /chat/stream --> B[FastAPI Backend]
  A -- /ingest, /tools --> B
  B -- Embedding --> C[DashScope Qwen-v4]
  B -- Vector I/O --> D[ChromaDB (duckdb+parquet)]
  B -- BM25/重排 --> E[BM25 + CrossEncoder]
  A -. Sources chips .-> A
```

最小演示步骤（2-3分钟）
-----------------------

1) 点击右上角“📥 入库”，粘贴 arXiv 摘要页 URL（如 `https://arxiv.org/abs/2508.15746`），成功后提示。
2) 在输入框询问：例如“LLM 最近有哪些趋势？”。
3) 观察流式生成，回答框内会出现“工作流”胶囊，结束后自动消失。
4) 回答下方引用 chips 可点击展开片段，片段不截词并显示可点击外链。
5) 右上角点击“速读卡/论文对比”，居中模态输入主题或两篇标题，生成结构化结果。

评测与会话分享
---------------

- 前往评测页：导航至 `/eval`，有“← 返回”可回到对话页。
- 会话持久化：URL 参数 `?s=...` 与 `localStorage` 同步，返回时保留上下文。
- 分享会话：复制带有 `?s=...` 的链接即可让他人复现当前对话（不含私钥）。

推荐 Demo 问题
--------------

- “LLM 最近的研究趋势是什么？”
- “对比 A 与 B 两篇论文的任务设置与关键贡献各有什么差异？”
- “基于知识库，回答‘检索增强生成在问答中的优势是什么？’并给出引用。”

注意
----

- 若仓库内无法新增 `.env.example`，请手动创建以下内容：
  - `DASHSCOPE_API_KEY=`（可留空，留空时使用占位回答）
  - `USE_REMOTE_EMBEDDINGS=1`
  - `QWEN_EMBED_MODEL=qwen-v4`
  - `NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000`


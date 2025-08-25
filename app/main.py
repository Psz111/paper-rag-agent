import os
import json
import streamlit as st
from app.rag_pipeline import rag_pipeline
from app.agent_card import generate_reading_card
from app.agent_compare import generate_comparison
from app.chat_loop import run_chat_round
from app.eval_utils import run_retrieval_eval, run_hybrid_eval, run_generation_eval, save_eval_outputs

st.set_page_config(page_title="RAG + Agent MVP", page_icon="🧠", layout="centered")
st.title("RAG + Agent 简易演示")
st.caption("本地向量检索（Chroma + SentenceTransformers） + 大模型生成（Qwen 可选）")

# 自定义来源显示样式：保留块配色，不做语法高亮
st.markdown(
    """
    <style>
    .source-line {
        background: var(--secondary-background-color);
        color: var(--text-color);
        padding: 0.5rem 0.75rem;
        border-radius: 0.25rem;
        font-family: monospace;
        white-space: pre-wrap;
        display: block;
        margin-bottom: 0.25rem;
    }
    .source-line .idx { color: #8ab4f8; }
    .source-line .score { color: #999; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.expander("运行环境检测", expanded=False):
    st.write("数据目录：", os.path.abspath("data"))
    st.write("Chroma 持久化目录：", os.path.abspath("data/chroma_db"))
    qwen_key = os.getenv("DASHSCOPE_API_KEY")
    st.write("DashScope Key: ", "已配置" if qwen_key else "未配置（将使用本地占位回答）")

tab_chat, tab_query, tab_eval, tab_card, tab_compare = st.tabs(["聊天", "问答", "评估", "速读卡", "论文对比"])

with tab_chat:
    st.write("这是统一聊天入口：可自然对话，也可直接让它‘生成速读卡/对比论文/回答库内问题’等。")
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    for m in st.session_state["messages"]:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    user_input = st.chat_input("请输入问题或指令… 如：生成A的速读卡；对比A和B；最近LLM趋势？")
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.spinner("思考中…"):
            assistant_msg = run_chat_round(st.session_state["messages"])
        st.session_state["messages"].append(assistant_msg)
        # 立刻刷新以保证输入框始终在对话列表下方
        st.rerun()

with tab_query:
    query = st.text_input("请输入你的问题")
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        use_rerank = st.checkbox("使用重排", value=False, help="使用 CrossEncoder 对检索结果重排，提升相关性")
    with col2:
        use_bm25 = st.checkbox("BM25预过滤", value=True, help="先用关键词筛文件，再向量检索+重排")
    with col3:
        if st.button("填充模板问题"):
            st.session_state["_template_fill"] = True
            st.rerun()

    if st.session_state.get("_template_fill"):
        st.session_state.pop("_template_fill", None)
        query = "请用要点回答：最近一个月LLM方向论文的主要趋势与代表性工作有哪些？并给出来源编号。"

    run = st.button("查询")
    if run and query.strip():
        with st.spinner("正在生成答案..."):
            result = rag_pipeline(query.strip(), use_rerank=use_rerank, use_bm25=use_bm25)
        st.subheader("答案")
        st.write(result.get("answer", ""))
        st.subheader("参考来源")
        sources = result.get("sources", [])
        if sources:
            for idx, s in enumerate(sources, start=1):
                label_path = s.get("source") if isinstance(s, dict) else str(s)
                title = s.get("title") if isinstance(s, dict) else None
                score = (s.get("score") if isinstance(s, dict) else None)
                try:
                    import os as _os
                    base_name = _os.path.basename(label_path)
                except Exception:
                    base_name = label_path
                display_name = title or base_name
                score_html = f" <span class=\"score\">(score={score:.3f})</span>" if isinstance(score, float) else ""
                st.markdown(f"<span class=\"source-line\"><span class=\"idx\">[{idx}]</span> {display_name}{score_html}</span>", unsafe_allow_html=True)
        else:
            st.write("暂无来源，建议将你的项目文档放入 data/ 目录下的 .txt/.md 文件。")

with tab_eval:
    st.write("上传或选择评测集（jsonl，每行包含 question/expected_title/expected_source）")
    default_path = os.path.abspath("data/eval/eval_set.jsonl")
    eval_path = st.text_input("评测集路径", value=default_path)
    k = st.number_input("k (Recall@k,MRR)", min_value=1, max_value=50, value=5, step=1)
    ndcg_k = st.number_input("NDCG@k", min_value=1, max_value=50, value=10, step=1)
    colx, coly = st.columns([1,1])
    run_basic = colx.button("运行重排对比评估")
    run_hybrid = coly.button("运行混合检索评估")
    run_gen = st.button("运行生成质量评估（NLI近似）")
    if run_basic or run_hybrid or run_gen:
        try:
            items: list[dict] = []
            with open(eval_path, 'r', encoding='utf-8') as f:
                for line in f:
                    items.append(json.loads(line))
            with st.spinner("评估中..."):
                if run_basic:
                    metrics_no, metrics_yes, details_no, details_yes = run_retrieval_eval(items, k=int(k), ndcg_k=int(ndcg_k))
                    out_csv = os.path.abspath("data/eval/eval_results.csv")
                    out_json = os.path.abspath("data/eval/summary.json")
                    save_eval_outputs(details_no, details_yes, metrics_no, metrics_yes, out_csv, out_json, int(k), int(ndcg_k), eval_path)
                    st.success("评估完成")
                    st.write("不开启重排：", metrics_no)
                    st.write("开启重排：", metrics_yes)
                    st.write("已保存：", out_csv, out_json)
                elif run_hybrid:
                    results = run_hybrid_eval(items, k=int(k), ndcg_k=int(ndcg_k))
                    # 保存混合评估汇总结果
                    hybrid_json = os.path.abspath("data/eval/hybrid_summary.json")
                    try:
                        os.makedirs(os.path.dirname(hybrid_json), exist_ok=True)
                        with open(hybrid_json, 'w', encoding='utf-8') as f:
                            json.dump(results, f, ensure_ascii=False, indent=2)
                    except Exception:
                        pass
                    st.success("混合检索评估完成")
                    st.write(results)
                    st.write("已保存：", hybrid_json)
                else:
                    per_items, summary = run_generation_eval(items, use_rerank=True, use_bm25=True, k_ctx=4)
                    gen_json = os.path.abspath("data/eval/generation_summary.json")
                    gen_csv = os.path.abspath("data/eval/generation_details.csv")
                    try:
                        os.makedirs(os.path.dirname(gen_json), exist_ok=True)
                        import csv as _csv
                        with open(gen_csv, 'w', encoding='utf-8', newline='') as w:
                            wr = _csv.writer(w)
                            wr.writerow(["question", "entail_ratio", "neutral_ratio", "contradict_ratio"])
                            for r in per_items:
                                wr.writerow([r["question"], r["entail_ratio"], r["neutral_ratio"], r["contradict_ratio"]])
                        with open(gen_json, 'w', encoding='utf-8') as f:
                            json.dump(summary, f, ensure_ascii=False, indent=2)
                    except Exception:
                        pass
                    st.success("生成质量评估完成（NLI近似）")
                    st.write(summary)
                    st.write("明细与汇总：", gen_csv, gen_json)
        except Exception as e:
            st.error(f"评估失败：{e}")

with tab_card:
    st.write("输入论文主题或关键词，我将基于你的库生成‘速读卡’（严格引用）。")
    q2 = st.text_input("论文主题/关键词", key="card_input")
    c1, c2 = st.columns([1,1])
    with c1:
        card_rerank = st.checkbox("使用重排", value=True)
    with c2:
        card_bm25 = st.checkbox("BM25预过滤", value=True)
    if st.button("生成速读卡") and q2.strip():
        with st.spinner("生成中..."):
            res = generate_reading_card(q2.strip(), use_rerank=card_rerank, use_bm25=card_bm25, k_ctx=6)
        st.subheader("速读卡")
        st.markdown(res.get("card", ""))
        st.subheader("参考来源")
        for idx, s in enumerate(res.get("sources", []), start=1):
            title = s.get("title") or s.get("source")
            score = s.get("score")
            score_html = f" <span class=\"score\">(score={score:.3f})</span>" if isinstance(score, float) else ""
            st.markdown(f"<span class=\"source-line\"><span class=\"idx\">[{idx}]</span> {title}{score_html}</span>", unsafe_allow_html=True)

with tab_compare:
    st.write("输入主题或关键词（可选指定标题关键字），生成论文差异对比表（严格引用）。")
    cmp_topic = st.text_input("对比主题/关键词", key="cmp_topic")
    picks = st.text_input("可选：标题关键字，逗号分隔", key="cmp_picks")
    cc1, cc2 = st.columns([1,1])
    with cc1:
        cmp_rerank = st.checkbox("使用重排", value=True, key="cmp_rerank")
    with cc2:
        cmp_bm25 = st.checkbox("BM25预过滤", value=True, key="cmp_bm25")
    if st.button("生成对比表") and cmp_topic.strip():
        pick_list = [p.strip() for p in picks.split(",") if p.strip()] if picks.strip() else None
        with st.spinner("生成中..."):
            res = generate_comparison(cmp_topic.strip(), picks=pick_list, use_rerank=cmp_rerank, use_bm25=cmp_bm25, k_ctx=8)
        st.subheader("对比表")
        st.markdown(res.get("table", ""))
        st.subheader("参考来源")
        for idx, s in enumerate(res.get("sources", []), start=1):
            title = s.get("title") or s.get("source")
            score = s.get("score")
            score_html = f" <span class=\"score\">(score={score:.3f})</span>" if isinstance(score, float) else ""
            st.markdown(f"<span class=\"source-line\"><span class=\"idx\">[{idx}]</span> {title}{score_html}</span>", unsafe_allow_html=True)
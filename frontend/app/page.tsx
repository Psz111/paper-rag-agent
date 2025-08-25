"use client";
import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type SourceItem = { source?: string; title?: string; score?: number; url?: string } | string;
type Msg = { role: "user" | "assistant"; content: string; sources?: SourceItem[] };

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

export default function Home() {
  const [messages, setMessages] = useState<Msg[]>([
    { role: "assistant", content: "你好，我可以自然聊天，也能生成速读卡/论文对比，或回答知识库问题。" },
  ]);
  const [input, setInput] = useState("");
  const [status, setStatus] = useState<string>("");
  const [flow, setFlow] = useState<string>("");
  const [phase, setPhase] = useState<string>("");
  // 控件参数
  const [bm25, setBm25] = useState<boolean>(true);
  const [rerank, setRerank] = useState<boolean>(false);
  const [selfCheck, setSelfCheck] = useState<boolean>(false);
  const [kCtx, setKCtx] = useState<number>(6);
  const [temp, setTemp] = useState<number>(0.2);
  const endRef = useRef<HTMLDivElement>(null);
  const [showSettings, setShowSettings] = useState<boolean>(false);
  const settingsWrapperRef = useRef<HTMLDivElement>(null);
  const [openSnippets, setOpenSnippets] = useState<Record<string, boolean>>({});
  const [activeIdx, setActiveIdx] = useState<number | null>(null);
  const ingestWrapperRef = useRef<HTMLDivElement>(null);
  const [showIngest, setShowIngest] = useState<boolean>(false);
  const [showQuickCard, setShowQuickCard] = useState<boolean>(false);
  const [showQuickCompare, setShowQuickCompare] = useState<boolean>(false);
  const [quickTopic, setQuickTopic] = useState<string>("");
  const [compareA, setCompareA] = useState<string>("");
  const [compareB, setCompareB] = useState<string>("");
  const quickTopicInputRef = useRef<HTMLInputElement>(null);
  const compareAInputRef = useRef<HTMLInputElement>(null);
  const headerRef = useRef<HTMLDivElement>(null);
  // 分享链接：把当前会话与参数编码到 URL（只做最小实现）
  function buildShareUrl(): string {
    try {
      const payload = { messages, bm25, rerank, selfCheck, kCtx, temp };
      const encoded = encodeURIComponent(btoa(unescape(encodeURIComponent(JSON.stringify(payload)))));
      const url = new URL(window.location.href);
      url.searchParams.set("s", encoded);
      return url.toString();
    } catch {
      return window.location.href;
    }
  }
  function buildStateParam(): string | null {
    try {
      const payload = { messages, bm25, rerank, selfCheck, kCtx, temp };
      return encodeURIComponent(btoa(unescape(encodeURIComponent(JSON.stringify(payload)))));
    } catch { return null; }
  }

  // 初次加载：从 URL 或 localStorage 恢复会话
  useEffect(() => {
    try {
      const url = new URL(window.location.href);
      const s = url.searchParams.get("s");
      if (s) {
        const raw = decodeURIComponent(s);
        const json = JSON.parse(decodeURIComponent(escape(atob(raw))));
        if (Array.isArray(json.messages)) setMessages(json.messages);
        if (typeof json.bm25 === "boolean") setBm25(json.bm25);
        if (typeof json.rerank === "boolean") setRerank(json.rerank);
        if (typeof json.selfCheck === "boolean") setSelfCheck(json.selfCheck);
        if (typeof json.kCtx === "number") setKCtx(json.kCtx);
        if (typeof json.temp === "number") setTemp(json.temp);
        return;
      }
      const saved = localStorage.getItem("chat_state");
      if (saved) {
        const st = JSON.parse(saved);
        if (Array.isArray(st.messages)) setMessages(st.messages);
        if (typeof st.bm25 === "boolean") setBm25(st.bm25);
        if (typeof st.rerank === "boolean") setRerank(st.rerank);
        if (typeof st.selfCheck === "boolean") setSelfCheck(st.selfCheck);
        if (typeof st.kCtx === "number") setKCtx(st.kCtx);
        if (typeof st.temp === "number") setTemp(st.temp);
      }
    } catch {}
  }, []);

  // 状态变化时持久化到 localStorage
  useEffect(() => {
    try {
      const st = { messages, bm25, rerank, selfCheck, kCtx, temp };
      localStorage.setItem("chat_state", JSON.stringify(st));
    } catch {}
  }, [messages, bm25, rerank, selfCheck, kCtx, temp]);

  // 打开模态时自动聚焦
  useEffect(() => { if (showQuickCard) quickTopicInputRef.current?.focus(); }, [showQuickCard]);
  useEffect(() => { if (showQuickCompare) compareAInputRef.current?.focus(); }, [showQuickCompare]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      const t = e.target as Node;
      const inSettings = settingsWrapperRef.current && settingsWrapperRef.current.contains(t);
      const inIngest = ingestWrapperRef.current && ingestWrapperRef.current.contains(t);
      if (!inSettings) setShowSettings(false);
      if (!inIngest) setShowIngest(false);
    }
    function handleKeydown(e: KeyboardEvent) {
      if (e.key === "Escape") {
        setShowSettings(false);
        setShowIngest(false);
        setShowQuickCard(false);
        setShowQuickCompare(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("keydown", handleKeydown);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleKeydown);
    };
  }, []);

  async function send() {
    const q = input.trim();
    if (!q) return;
    const userMsg: Msg = { role: "user", content: q };
    const next = [...messages, userMsg];
    setMessages(next);
    setInput("");
    try {
      // 先插入占位的 assistant 消息，后续流式追加内容
      const idx = next.length; // 将成为新消息索引
      const placeholder: Msg = { role: "assistant", content: "" };
      setMessages((m) => [...m, placeholder]);
      setActiveIdx(idx);
      setStatus("router");
      setFlow("");
      setPhase("路由中…");

      // 追加查询参数控制后端：bm25, rerank, k_ctx, temp, self_check
      const qs = new URLSearchParams({
        bm25: bm25 ? "1" : "0",
        rerank: rerank ? "1" : "0",
        k_ctx: String(kCtx || 6),
        temp: String(temp || 0.2),
        self_check: selfCheck ? "1" : "0",
      }).toString();
      const res = await fetch(`${API_BASE}/chat/stream?${qs}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: next }),
      });
      if (!res.body) throw new Error("后端未返回可读流");
      const reader = res.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let buffer = "";
      let full = "";
      let gotAnyEvent = false;
      const idleTimer = setTimeout(() => {
        if (!gotAnyEvent) {
          setStatus("error");
          setPhase("连接空闲，可能在索引或模型加载…");
        }
      }, 6000);
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        try { console.log("chunk", value?.length ?? 0); } catch {}
        buffer += decoder.decode(value, { stream: true });
        let lines = buffer.split("\n");
        buffer = lines.pop() || "";
        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const evt = JSON.parse(line.trim());
            if (typeof window !== "undefined") {
              try { console.log("evt", evt); } catch {}
            }
            gotAnyEvent = true;
            if (evt.type === "step") {
              const s = String(evt.status || "");
              setStatus(s);
              if (s === "workflow" && evt.label) {
                setFlow(String(evt.label));
                setPhase("准备检索…");
              } else if (s === "retrieving_start") {
                setPhase("检索中…");
              } else if (s === "error") {
                setPhase("发生错误");
              } else if (s === "generating_start") {
                setPhase("生成中…");
              } else if (s === "generating_done") {
                // do nothing,等待final 清空
              }
            } else if (evt.type === "delta") {
              full += evt.content || "";
              const content = full;
              setMessages((m) => m.map((mm, i) => (i === idx ? { ...mm, content } : mm)));
            } else if (evt.type === "final") {
              full = evt.content || full;
              const finalSources = Array.isArray(evt.sources) ? (evt.sources as SourceItem[]) : undefined;
              setMessages((m) => m.map((mm, i) => (i === idx ? { ...mm, content: full, sources: finalSources } : mm)));
              setStatus("");
              setFlow("");
              setPhase("");
              try { clearTimeout(idleTimer); } catch {}
              setActiveIdx(null);
            }
          } catch (e) {
            // 忽略解析失败的行
          }
        }
      }
      try { clearTimeout(idleTimer); } catch {}
    } catch (e: any) {
      setStatus("");
      setMessages((m) => [
        ...m,
        { role: "assistant", content: `请求失败: ${e?.message || e}` },
      ]);
    }
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", maxWidth: 900, margin: "0 auto", padding: 16 }}>
      <div style={{ flex: 1, overflowY: "auto" }}>
        <style jsx global>{`
          .md table { border-collapse: collapse; width: 100%; }
          .md th, .md td { border: 1px solid #E2E8F0; padding: 8px; vertical-align: top; }
          .md th { background: #F8FAFC; font-weight: 600; }
          .md tr:nth-child(even) td { background: #FAFAFA; }
          .md p { margin: 0.25rem 0; }
          .md ol, .md ul { margin: 0.1rem 0; padding-left: 1.1rem; }
          .md li { margin: 0.08rem 0; }
          .md li > p { margin: 0.08rem 0; }
          .md { word-break: break-word; overflow-wrap: anywhere; }
          .md h1, .md h2, .md h3, .md h4, .md h5, .md h6 { margin-top: 0.4rem; margin-bottom: 0.35rem }
          .badge { display:inline-block; padding:4px 10px; border-radius:9999px; background:#DBEAFE; color:#1E40AF; font-size:13px; margin-bottom:8px }
          .card { box-shadow: 0 6px 20px rgba(0,0,0,0.08); border: 1px solid #E2E8F0; }
          .chip { display:inline-flex; align-items:center; gap:6px; padding:4px 10px; border-radius:9999px; background:#F1F5F9; color:#334155; font-size:13px; border:1px solid #E2E8F0 }
          .chip-btn { cursor:pointer; user-select:none }
          .snippet { margin-top:6px; padding:10px; background:#F8FAFC; border:1px dashed #E2E8F0; border-radius:8px; color:#1F2937; font-size:14px; line-height:1.6; white-space:pre-wrap; word-break: break-word; overflow-wrap: anywhere }
          .btn { padding:12px 18px; border-radius:12px; border:1px solid #E2E8F0; background:#FFFFFF; font-size:14px }
          .btn-primary { background:#0EA5E9; color:#FFFFFF; border-color:#0EA5E9 }
          .modal-mask { position:fixed; inset:0; background:rgba(0,0,0,0.35); display:flex; align-items:center; justify-content:center; z-index:50 }
          .modal { width: 520px; max-width: calc(100% - 48px); background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; box-shadow: 0 20px 60px rgba(0,0,0,0.2); padding:16px }
          .md { font-size: 15px; line-height: 1.7; color:#111827 }
          .md h2, .md h3 { color:#0F172A }
          .md code { background:#F1F5F9; padding:2px 6px; border-radius:6px }
        `}</style>
        {/* 参数控件已移至右上角齿轮设置内 */}
        
        {/* 顶部右侧：评测 / 入库 / 速读卡 / 对比 / 设置 */}
        <div ref={headerRef} style={{ marginBottom: 12, display: "flex", justifyContent: "flex-end", gap: 8, flexWrap: "wrap" }}>
          <a href={(buildStateParam() ? `/eval?s=${buildStateParam()}` : "/eval")} style={{ fontSize: 14, color: "#0EA5E9", textDecoration: "none", alignSelf: "center" }} title="查看评测摘要">评测</a>
          {/* 入库 */}
          <div ref={ingestWrapperRef} style={{ position: "relative" }}>
            <button
              onClick={() => setShowIngest((v) => !v)}
              aria-label="Ingest"
              title="入库（上传PDF/文本或URL）"
              className="btn"
            >
              📥
            </button>
            {showIngest && (
              <div className="card" style={{ position: "absolute", top: 40, right: 0, zIndex: 20, width: 420, padding: 12, background: "#FFFFFF", border: "1px solid #E2E8F0", borderRadius: 8, boxShadow: "0 8px 24px rgba(0,0,0,0.12)" }}>
                <form
                  onSubmit={async (e) => {
                    e.preventDefault();
                    const formEl = e.currentTarget as HTMLFormElement;
                    const fd = new FormData(formEl);
                    try {
                      const res = await fetch(`${API_BASE}/ingest`, { method: "POST", body: fd });
                      const j = await res.json().catch(() => ({}));
                      const added = j?.added || 0;
                      const reason = j?.reason;
                      const dbg = j?.debug ? `\n(debug: ${JSON.stringify(j.debug)})` : "";
                      setMessages((m) => [...m, { role: "assistant", content: added ? `入库成功：${added} 项` : `未能入库：${reason || "请检查文件或URL"}${dbg}` }]);
                    } catch (err: any) {
                      setMessages((m) => [...m, { role: "assistant", content: `入库异常：${err?.message || err}` }]);
                    }
                    try { formEl.reset(); } catch {}
                  }}
                  style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}
                >
                  <input type="file" name="file" accept=".pdf,.md,.txt" title="选择本地 PDF/MD/TXT 文件" />
                  <input type="url" name="url" placeholder="粘贴 arXiv 摘要页 URL（如 https://arxiv.org/abs/…）" title="优先使用 arXiv 摘要页链接入库摘要" style={{ flex: 1, minWidth: 200, padding: 6, border: "1px solid #E2E8F0", borderRadius: 6 }} />
                  <button type="submit" style={{ padding: "6px 12px", borderRadius: 6, background: "#10B981", color: "white" }} title="开始入库">入库</button>
                </form>
              </div>
            )}
          </div>
          {/* 速读卡触发：滚至顶部并以模态居中显示 */}
          <button
            className="btn"
            title="一键速读卡"
            onClick={() => { headerRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }); setShowQuickCard(true); setTimeout(() => quickTopicInputRef.current?.focus(), 250); }}
          >📇 速读卡</button>
          {/* 论文对比触发 */}
          <button
            className="btn"
            title="一键论文对比"
            onClick={() => { headerRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }); setShowQuickCompare(true); setTimeout(() => compareAInputRef.current?.focus(), 250); }}
          >📊 论文对比</button>
          {/* 分享链接 */}
          <button
            className="btn"
            title="复制分享链接"
            onClick={() => {
              const u = buildShareUrl();
              try { navigator.clipboard?.writeText(u); } catch {}
              setMessages((m) => [...m, { role: "assistant", content: "已复制分享链接，可粘贴给他人打开相同会话。" }]);
            }}
          >🔗</button>
          {/* 设置 */}
          <div ref={settingsWrapperRef} style={{ position: "relative" }}>
            <button
              onClick={() => setShowSettings((v) => !v)}
              aria-label="Settings"
              title="设置"
              className="btn"
            >
              ⚙️
            </button>
            {showSettings && (
              <div
                className="card"
                style={{
                  position: "absolute",
                  top: 40,
                  right: 0,
                  zIndex: 20,
                  width: 320,
                  padding: 12,
                  background: "#FFFFFF",
                  border: "1px solid #E2E8F0",
                  borderRadius: 8,
                  boxShadow: "0 8px 24px rgba(0,0,0,0.12)"
                }}
              >
                <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                  <label style={{ display: "flex", gap: 6, alignItems: "center" }}>
                    <input type="checkbox" checked={bm25} onChange={(e) => setBm25(e.target.checked)} /> BM25
                  </label>
                  <label style={{ display: "flex", gap: 6, alignItems: "center" }}>
                    <input type="checkbox" checked={rerank} onChange={(e) => setRerank(e.target.checked)} /> 重排
                  </label>
                  <label style={{ display: "flex", gap: 6, alignItems: "center" }}>
                    <input type="checkbox" checked={selfCheck} onChange={(e) => setSelfCheck(e.target.checked)} /> 自检
                  </label>
                  <label style={{ display: "flex", gap: 6, alignItems: "center", justifyContent: "space-between" }}>
                    <span>k_ctx</span>
                    <input type="number" min={1} max={12} step={1} value={kCtx} onChange={(e) => setKCtx(Number(e.target.value))} style={{ width: 80, padding: 4, border: "1px solid #E2E8F0", borderRadius: 6 }} />
                  </label>
                  <label style={{ display: "flex", gap: 6, alignItems: "center", justifyContent: "space-between" }}>
                    <span>温度</span>
                    <input type="number" min={0} max={1} step={0.1} value={temp} onChange={(e) => setTemp(Number(e.target.value))} style={{ width: 80, padding: 4, border: "1px solid #E2E8F0", borderRadius: 6 }} />
                  </label>
                </div>
              </div>
            )}
          </div>
        </div>
        {/* 速读卡模态（居中遮罩，可点击遮罩/Esc 关闭） */}
        {showQuickCard && (
          <div className="modal-mask" onClick={() => setShowQuickCard(false)}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
              <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                <input
                  ref={quickTopicInputRef}
                  value={quickTopic}
                  onChange={(e) => setQuickTopic(e.target.value)}
                  placeholder="输入主题/标题，例如：LLM 趋势"
                  style={{ flex: 1, padding: 10, border: "1px solid #E2E8F0", borderRadius: 8 }}
                />
                <button
                  onClick={() => {
                    const t = quickTopic.trim();
                    if (!t) return;
                    setShowQuickCard(false);
                    setInput(`生成${t}的速读卡`);
                    setTimeout(() => send(), 0);
                  }}
                  className="btn btn-primary"
                >生成</button>
              </div>
            </div>
          </div>
        )}
        {/* 论文对比模态 */}
        {showQuickCompare && (
          <div className="modal-mask" onClick={() => setShowQuickCompare(false)}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
              <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
                <input
                  ref={compareAInputRef}
                  value={compareA}
                  onChange={(e) => setCompareA(e.target.value)}
                  placeholder="论文 A 关键词/标题"
                  style={{ flex: 1, minWidth: 160, padding: 10, border: "1px solid #E2E8F0", borderRadius: 8 }}
                />
                <input
                  value={compareB}
                  onChange={(e) => setCompareB(e.target.value)}
                  placeholder="论文 B 关键词/标题"
                  style={{ flex: 1, minWidth: 160, padding: 10, border: "1px solid #E2E8F0", borderRadius: 8 }}
                />
                <button
                  onClick={() => {
                    const a = compareA.trim();
                    const b = compareB.trim();
                    if (!a || !b) return;
                    setShowQuickCompare(false);
                    setInput(`对比 ${a} 和 ${b}`);
                    setTimeout(() => send(), 0);
                  }}
                  className="btn btn-primary"
                >对比</button>
              </div>
            </div>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: 12, display: "flex", justifyContent: m.role === "user" ? "flex-end" : "flex-start" }}>
            <div style={{ maxWidth: "80%", padding: 12, borderRadius: 8, background: m.role === "user" ? "#DCFCE7" : "#FFFFFF" }} className={m.role === "assistant" ? "card" : undefined}>
              <div style={{ fontSize: 12, color: "#64748B", marginBottom: 4 }}>{m.role}</div>
              <div style={m.role === "assistant" ? undefined : { whiteSpace: "pre-wrap" }}>
                {m.role === "assistant" ? (() => {
                  // 提取工作流徽章
                  const lines = (m.content || "").split("\n");
                  let badge: string | null = null;
                  if (lines.length && /^\[工作流:/.test(lines[0])) {
                    badge = lines[0].replace(/^\[(.*)\]$/, '$1');
                    lines.shift();
                  }
                  const rest = lines.join("\n");
                  return (
                    <>
                      {/* 活跃工作流 chips 展示 */}
                      {typeof i === "number" && activeIdx === i && (
                        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 8 }}>
                          {flow && <span className="chip">{flow}</span>}
                          {phase && <span className="chip">{phase}</span>}
                        </div>
                      )}
                      {badge && <div className="badge">{badge}</div>}
                      <div style={{ overflowX: "auto" }} className="md">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{rest}</ReactMarkdown>
                      </div>
                      {Array.isArray((m as any).sources) && (m as any).sources.length > 0 && (
                        <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginTop: 8 }}>
                          {(m as any).sources.map((s: any, si: number) => {
                            const isObj = typeof s === "object" && s !== null;
                            const title = isObj ? (s.title || s.source || `来源${si+1}`) : String(s);
                            const score = isObj ? s.score : undefined;
                            const url = isObj ? s.url : undefined;
                            const key = `${i}-${si}`;
                            const snippet: string | undefined = isObj ? s.snippet : undefined;
                            const isOpen = !!openSnippets[key];
                            return (
                              <div key={si} style={{ display: "flex", flexDirection: "column", alignItems: "flex-start" }}>
                                <span
                                  className="chip chip-btn"
                                  title={score != null ? `score: ${Number(score).toFixed(3)}` : undefined}
                                  onClick={() => setOpenSnippets((st) => ({ ...st, [key]: !st[key] }))}
                                >
                                  [{si+1}] {title}
                                  {snippet ? (isOpen ? " ▲" : " ▼") : null}
                                  {url && (
                                    <a href={url} target="_blank" rel="noreferrer" style={{ color: "#2563EB", textDecoration: "none", marginLeft: 6 }} onClick={(e) => e.stopPropagation()}>
                                      ↗
                                    </a>
                                  )}
                                </span>
                                {snippet && isOpen && (
                                  <div className="snippet">
                                    {snippet}
                                  </div>
                                )}
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </>
                  );
                })() : m.content}
              </div>
            </div>
          </div>
        ))}
        <div ref={endRef} />
      </div>
      <div style={{ display: "flex", gap: 8, alignItems: "stretch", marginTop: 8 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="输入问题，如：生成A的速读卡；对比A和B；最近LLM趋势？"
          style={{ flex: 1, padding: 12, border: "1px solid #E2E8F0", borderRadius: 8 }}
        />
        <button onClick={send} className="btn btn-primary" style={{ height: "auto" }}>发送</button>
      </div>
      {/* 快捷按钮：已上移到顶部工具栏，这里移除重复区块 */}
    </div>
  );
}



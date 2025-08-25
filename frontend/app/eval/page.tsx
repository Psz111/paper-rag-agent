"use client";
import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

export default function EvalPage() {
  const [data, setData] = useState<any>(null);
  const [err, setErr] = useState<string>("");
  const [stateParam, setStateParam] = useState<string>("");
  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${API_BASE}/eval/summary`);
        const j = await res.json();
        setData(j);
      } catch (e: any) {
        setErr(e?.message || String(e));
      }
    })();
    try {
      const u = new URL(window.location.href);
      const s = u.searchParams.get("s") || "";
      if (s) setStateParam(s);
    } catch {}
  }, []);

  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: 16 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <h2 style={{ margin: 0 }}>评测摘要</h2>
        <a href={`/${stateParam ? `?s=${encodeURIComponent(stateParam)}` : ""}`} style={{ padding: "10px 16px", borderRadius: 12, border: "1px solid #E2E8F0", background: "#FFFFFF", textDecoration: "none", fontSize: 14 }}>← 返回</a>
      </div>
      {err && <div style={{ color: "#B91C1C" }}>加载失败: {err}</div>}
      {!data && !err && <div>加载中…</div>}
      {data && (
        <pre style={{ whiteSpace: "pre-wrap", background: "#F8FAFC", padding: 12, borderRadius: 8, border: "1px solid #E2E8F0" }}>
{JSON.stringify(data, null, 2)}
        </pre>
      )}
    </div>
  );
}



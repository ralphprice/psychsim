// ExecutiveEditor — view/add/edit/delete the frontal-cortex monitor registry (declarative
// specs: {name, target, kind: inhibit|amplify, when_dominant}). DISCIPLINE (design §2.9):
// the registry is EMPTY by default; the executive is consulted on every event but only
// acts on installed monitors, and WHICH patterns must be established by research, never
// hand-invented. This tool installs researched patterns — it is a mechanism, not a way to
// script behaviour.

import { useEffect, useState } from "react";
import { getExecutive, sendCommand } from "../api";
import type { ExecutiveView, MatrixItem } from "../types";

export function ExecutiveEditor() {
  const [view, setView] = useState<ExecutiveView | null>(null);
  const [draft, setDraft] = useState("");
  const [msg, setMsg] = useState("");

  const refresh = () => getExecutive().then(setView).catch(() => {});
  useEffect(() => {
    refresh();
  }, []);

  const save = async () => {
    let item: MatrixItem;
    try {
      item = JSON.parse(draft);
    } catch {
      setMsg("invalid JSON");
      return;
    }
    const r = await sendCommand({ cmd: "executive_upsert", item });
    setMsg(r.error ?? "saved");
    refresh();
  };
  const del = async (name: string) => {
    if (!window.confirm(`Delete executive monitor "${name}"?`)) return;
    await sendCommand({ cmd: "executive_delete", id: name });
    refresh();
    setMsg(`deleted ${name}`);
  };
  const blank = () => {
    const s = view?.systems?.[0] ?? "SEEKING";
    setDraft(JSON.stringify({ name: "", target: s, kind: "inhibit", when_dominant: s }, null, 2));
  };

  return (
    <details className="matrixed">
      <summary>executive functions · frontal cortex</summary>
      {view && <div className="caveat">{view.note}</div>}
      <div className="mx-list">
        {(view?.monitors ?? []).map((m, i) => (
          <div className="mx-row" key={i}>
            <button
              className="mx-id"
              title="view / edit this monitor"
              onClick={() => setDraft(JSON.stringify(m, null, 2))}
            >
              {String(m.name)}
            </button>
            <button className="del" title="delete this monitor" onClick={() => del(String(m.name))}>
              Delete
            </button>
          </div>
        ))}
        {view && view.monitors.length === 0 && (
          <div className="muted">none installed (empty by default — the disciplined state)</div>
        )}
      </div>
      <div className="row">
        <button onClick={blank}>+ new</button>
        {msg && <span className="muted">{msg}</span>}
      </div>
      {view && <div className="caveat">systems: {view.systems.join(", ")}</div>}
      {draft && (
        <div className="mx-edit">
          <textarea value={draft} rows={7} onChange={(e) => setDraft(e.target.value)} />
          <div className="row">
            <button className="primary" onClick={save}>
              save
            </button>
            <button onClick={() => setDraft("")}>cancel</button>
          </div>
        </div>
      )}
    </details>
  );
}

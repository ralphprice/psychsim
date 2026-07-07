// NeuralEditor — an authoring sandbox for the affect model's pathways & networks as
// data: the SVG wiring diagram (excitatory green / inhibitory red), integrity feedback
// (validation + feedback loops), and view/add/edit/delete over circuits, pathways,
// networks, triggers, features. NOT wired into the live substrate (that is the separate
// substrate-overhaul work); designs are saved for that future use.

import { useEffect, useState } from "react";
import { getNeural, sendCommand } from "../api";
import type { NeuralView, MatrixItem } from "../types";

const COLLECTIONS = ["circuit", "pathway", "network", "trigger", "feature"];

export function NeuralEditor() {
  const [view, setView] = useState<NeuralView | null>(null);
  const [coll, setColl] = useState("pathway");
  const [draft, setDraft] = useState("");
  const [msg, setMsg] = useState("");

  const refresh = () => getNeural().then(setView).catch(() => {});
  useEffect(() => {
    refresh();
  }, []);

  const items = (): MatrixItem[] => {
    const lib = view?.library as Record<string, Record<string, MatrixItem>> | undefined;
    const dict = lib?.[coll + "s"];
    return dict ? Object.values(dict) : [];
  };
  const save = async () => {
    let item: MatrixItem;
    try {
      item = JSON.parse(draft);
    } catch {
      setMsg("invalid JSON");
      return;
    }
    const r = await sendCommand({ cmd: "neural_upsert", kind: coll, item });
    setMsg(r.error ?? "saved");
    await refresh();
  };
  const del = async (id: string) => {
    if (!window.confirm(`Delete ${coll} "${id}"? Removing a circuit also removes its pathways.`))
      return;
    await sendCommand({ cmd: "neural_delete", kind: coll, id });
    refresh();
    setMsg(`deleted ${id}`);
  };

  return (
    <details className="matrixed neural">
      <summary>neural design · pathways / networks</summary>
      {view && <div className="neural-svg" dangerouslySetInnerHTML={{ __html: view.svg }} />}
      {view && (view.validation.length > 0 || view.loops.length > 0) && (
        <div className="caveat">
          {view.validation.length > 0 && <>⚠ {view.validation.join("; ")}</>}
          {view.loops.length > 0 && (
            <div>loops: {view.loops.map((l) => l.join("→")).join("  |  ")}</div>
          )}
        </div>
      )}
      <div className="row seg">
        {COLLECTIONS.map((c) => (
          <button
            key={c}
            className={c === coll ? "on" : ""}
            onClick={() => {
              setColl(c);
              setDraft("");
            }}
          >
            {c}
          </button>
        ))}
      </div>
      <div className="mx-hint">Click an item to view / edit it. Use Delete to remove it.</div>
      <div className="mx-list">
        {items().map((it, i) => (
          <div className="mx-row" key={i}>
            <button
              className="mx-id"
              title="view / edit this item"
              onClick={() => setDraft(JSON.stringify(it, null, 2))}
            >
              {String(it.id)}
            </button>
            <button className="del" title="delete this item" onClick={() => del(String(it.id))}>
              Delete
            </button>
          </div>
        ))}
      </div>
      <div className="row">
        <button onClick={() => setDraft(JSON.stringify({ id: "" }, null, 2))}>+ new</button>
        {msg && <span className="muted">{msg}</span>}
      </div>
      {draft && (
        <div className="mx-edit">
          <textarea value={draft} rows={8} onChange={(e) => setDraft(e.target.value)} />
          <div className="row">
            <button className="primary" onClick={save}>
              save
            </button>
            <button onClick={() => setDraft("")}>cancel</button>
          </div>
        </div>
      )}
      <div className="caveat">
        An authoring sandbox (pathways/networks as data). Not wired into the live substrate —
        designs are saved for the coming substrate work.
      </div>
    </details>
  );
}

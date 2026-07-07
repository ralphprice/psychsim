// MatrixEditor — view / add / edit / delete the DEFINITION items of the three interface
// matrices (groups, environment things, social role-pairs). The runtime traces
// (memberships / bonds / ties) are emergent and not edited here. Items are edited as
// JSON (a faithful data editor); edits persist to data files.

import { useEffect, useState } from "react";
import { getMatrixKinds, getMatrixItems, sendCommand } from "../api";
import type { MatrixKindInfo, MatrixItem } from "../types";

export function MatrixEditor() {
  const [kinds, setKinds] = useState<Record<string, MatrixKindInfo>>({});
  const [kind, setKind] = useState("group");
  const [items, setItems] = useState<MatrixItem[]>([]);
  const [draft, setDraft] = useState("");
  const [msg, setMsg] = useState("");

  useEffect(() => {
    getMatrixKinds().then(setKinds).catch(() => {});
  }, []);

  const refresh = (k: string) => getMatrixItems(k).then(setItems).catch(() => setItems([]));
  useEffect(() => {
    refresh(kind);
    setDraft("");
    setMsg("");
  }, [kind]);

  const spec = kinds[kind];
  const idf = spec?.id_field ?? "id";

  const blank = () => {
    const t: MatrixItem = {};
    (spec?.fields ?? []).forEach((f) => {
      t[f] = f === idf ? "" : f === "stimulus" ? {} : 0;
    });
    setDraft(JSON.stringify(t, null, 2));
  };
  const save = async () => {
    let item: MatrixItem;
    try {
      item = JSON.parse(draft);
    } catch {
      setMsg("invalid JSON");
      return;
    }
    const r = await sendCommand({ cmd: "matrix_upsert", kind, item });
    setMsg(r.error ?? "saved");
    refresh(kind);
  };
  const del = async (id: string) => {
    if (!window.confirm(`Delete "${id}" from ${spec?.label ?? kind}? This removes it from the data file.`))
      return;
    await sendCommand({ cmd: "matrix_delete", kind, id });
    refresh(kind);
    setMsg(`deleted ${id}`);
  };

  return (
    <details className="matrixed">
      <summary>matrices · view / edit</summary>
      <div className="row seg">
        {Object.entries(kinds).map(([k, v]) => (
          <button key={k} className={k === kind ? "on" : ""} onClick={() => setKind(k)}>
            {v.label}
          </button>
        ))}
      </div>
      <div className="mx-hint">Click an item to view / edit it. Use Delete to remove it.</div>
      <div className="mx-list">
        {items.map((it, i) => (
          <div className="mx-row" key={i}>
            <button
              className="mx-id"
              title="view / edit this item"
              onClick={() => setDraft(JSON.stringify(it, null, 2))}
            >
              {String(it[idf])}
            </button>
            <button className="del" title="delete this item" onClick={() => del(String(it[idf]))}>
              Delete
            </button>
          </div>
        ))}
      </div>
      <div className="row">
        <button onClick={blank}>+ new</button>
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
        Edits persist to data files. Groups/things apply on next Spawn; social role-pairs on
        server restart. Runtime traces (memberships/bonds/ties) are emergent, not edited here.
      </div>
    </details>
  );
}

// MatrixTab — one component for the three interface-matrix tabs (Social role-pairs, Environment
// things, Groups), parameterised by `kind`. Replaces MatrixEditor's internal kind dropdown: the kind
// IS the tab now. These are DEFINITION items (the matrices' vocabulary); the runtime traces
// (memberships / bonds / ties) are emergent and live on each person, not here.
//
// No server change: /matrix (field spec) and /matrix/items?kind= already discriminate by kind, and
// matrix_upsert / matrix_delete already take a kind. The kind DESCRIPTION below is client-side
// explanatory copy (the metadata carries a label + fields but no description) — presentational, not
// simulation data, same status as the eyebrow.

import { useCallback, useEffect, useState } from "react";
import { getMatrixKinds, getMatrixItems, sendCommand } from "../api";
import type { MatrixKindInfo, MatrixItem } from "../types";
import { MasterDetail } from "../layout/MasterDetail";
import { SkeletonList } from "../layout/Skeleton";
import { initBuffer, buildItem, blankItem, isComplex, type Buffer } from "./matrixForm";

export type MatrixKind = "social" | "environment" | "group";

const NOUN: Record<MatrixKind, string> = { social: "role-pair", environment: "thing", group: "group" };
const LIST_LABEL: Record<MatrixKind, string> = {
  social: "Social role-pairs",
  environment: "Environment things",
  group: "Groups",
};
const DESCRIPTION: Record<MatrixKind, string> = {
  social:
    "A social role-pair is an asymmetric relationship type — a higher and a lower role and the power between them — that residents can instantiate.",
  environment:
    "An environment thing is a perceptible object in the world: an innate attraction / aversion and a stimulus signature the substrate can perceive.",
  group:
    "A group is a collective residents can belong to — its size, cohesion, status and norm strength shape the emergent membership dynamics.",
};

export function MatrixTab({
  kind,
  selectedId,
  onSelect,
}: {
  kind: MatrixKind;
  selectedId: string | null;
  onSelect: (id: string | null) => void;
}) {
  const [spec, setSpec] = useState<MatrixKindInfo | null>(null);
  const [items, setItems] = useState<MatrixItem[]>([]);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    getMatrixKinds()
      .then((ks) => setSpec(ks[kind] ?? null))
      .catch(() => setSpec(null));
  }, [kind]);

  const reload = useCallback(
    () => getMatrixItems(kind).then(setItems).catch(() => setItems([])),
    [kind],
  );
  useEffect(() => {
    setCreating(false);
    reload();
  }, [kind, reload]);

  if (!spec) return <SkeletonList rows={6} label={`Loading ${LIST_LABEL[kind]}`} />;
  const idf = spec.id_field;
  const idOf = (it: MatrixItem) => String(it[idf]);

  // after an upsert / delete: reload the list, close any draft, move selection
  const afterWrite = async (id: string | null) => {
    setCreating(false);
    await reload();
    onSelect(id);
  };

  return (
    <div className="matrix-tab">
      <header className="matrix-head">
        <div className="matrix-eyebrow">Definition items — the runtime traces live on each person.</div>
        <div className="matrix-desc">{DESCRIPTION[kind]}</div>
      </header>
      <MasterDetail
        items={items}
        getId={idOf}
        getText={(it) => `${idOf(it)} ${typeof it.name === "string" ? it.name : ""}`.trim()}
        renderRow={(it) => (
          <span className="mx-row">
            <span className="mx-row-id">{idOf(it)}</span>
            {typeof it.name === "string" && it.name && it.name !== idOf(it) && (
              <span className="mx-row-name">{it.name}</span>
            )}
          </span>
        )}
        renderDetail={(it) => (
          <MatrixItemForm key={idOf(it)} kind={kind} spec={spec} item={it} isNew={false} onDone={afterWrite} />
        )}
        detailOverride={
          creating ? (
            <MatrixItemForm
              key="__new__"
              kind={kind}
              spec={spec}
              item={blankItem(spec.fields, items[0], idf)}
              isNew
              onDone={afterWrite}
              onCancel={() => setCreating(false)}
            />
          ) : undefined
        }
        listFooter={
          <button
            onClick={() => {
              setCreating(true);
              onSelect(null);
            }}
          >
            + New {NOUN[kind]}
          </button>
        }
        selectedId={creating ? null : selectedId}
        onSelect={(id) => {
          setCreating(false);
          onSelect(id);
        }}
        noun={NOUN[kind]}
        label={LIST_LABEL[kind]}
      />
    </div>
  );
}

function MatrixItemForm({
  kind,
  spec,
  item,
  isNew,
  onDone,
  onCancel,
}: {
  kind: MatrixKind;
  spec: MatrixKindInfo;
  item: MatrixItem;
  isNew: boolean;
  onDone: (id: string | null) => void;
  onCancel?: () => void;
}) {
  const idf = spec.id_field;
  const [buf, setBuf] = useState<Buffer>(() => initBuffer(item, spec.fields));
  const [msg, setMsg] = useState<string | null>(null);
  const [confirmDel, setConfirmDel] = useState(false);
  const set = (f: string, v: string) => setBuf((b) => ({ ...b, [f]: v }));

  const save = async () => {
    let rebuilt: MatrixItem;
    try {
      rebuilt = buildItem(buf, item, spec.fields); // types from the edited item (or the blank template)
    } catch {
      setMsg("A field has invalid JSON.");
      return;
    }
    const id = String(rebuilt[idf] ?? "").trim();
    if (!id) {
      setMsg(`${idf} is required.`);
      return;
    }
    const r = await sendCommand({ cmd: "matrix_upsert", kind, item: rebuilt });
    if (r.error) {
      setMsg(r.error);
      return;
    }
    onDone(id);
  };

  const del = async () => {
    const r = await sendCommand({ cmd: "matrix_delete", kind, id: String(item[idf]) });
    if (r.error) {
      setMsg(r.error);
      return;
    }
    onDone(null);
  };

  return (
    <div className="mx-form">
      <div className="mx-form-title">{isNew ? `New ${spec.label}` : String(item[idf])}</div>
      {spec.fields.map((f) => {
        const idLocked = !isNew && f === idf;
        return (
          <label className="mx-field" key={f}>
            <span className="mx-field-name">
              {f}
              {f === idf ? " · id" : ""}
            </span>
            {isComplex(item[f]) ? (
              <textarea className="mono" rows={4} value={buf[f]} onChange={(e) => set(f, e.target.value)} />
            ) : (
              <input
                className="mono"
                value={buf[f]}
                readOnly={idLocked}
                title={idLocked ? "the id is fixed — delete and create to rename" : undefined}
                onChange={(e) => set(f, e.target.value)}
              />
            )}
          </label>
        );
      })}
      <div className="mx-actions">
        <button className="primary" onClick={save}>
          {isNew ? "Create" : "Save changes"}
        </button>
        {isNew ? (
          <button onClick={onCancel}>Cancel</button>
        ) : confirmDel ? (
          <button className="warn" onClick={del}>
            confirm delete 🗑
          </button>
        ) : (
          <button className="warn-ghost" onClick={() => setConfirmDel(true)}>
            Delete
          </button>
        )}
        {msg && <span className="mx-msg">{msg}</span>}
      </div>
    </div>
  );
}

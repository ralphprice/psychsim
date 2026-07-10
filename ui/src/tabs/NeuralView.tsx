// NeuralView — a READ-ONLY window onto the LIVE v9 substrate seed (Phase 6; constraints U2/U3).
// It replaces the old NeuralEditor, which edited a dead parallel sandbox. There is NO write path
// here: no upsert/delete command, no sendCommand import, no editable control. The seed is the single
// source of truth; circuit changes go through a reviewed seed pass, not this browser.
//
// Everything shown is provenance ABOUT THE ORGANISM, read from the seed: sources and confidence come
// from the seed verbatim, and any weight that is a placeholder assumption (not a measured constant)
// carries a SCAFFOLD chip. The circuit/connection structure is read through the same loader the
// engine uses (server side), so the count the banner shows cannot diverge from the running substrate.

import { useEffect, useState } from "react";
import { getNeural } from "../api";
import type { NeuralView as NeuralViewT, NeuralCircuit, NeuralConnection } from "../types";
import { MasterDetail } from "../layout/MasterDetail";
import { SkeletonList } from "../layout/Skeleton";

export function NeuralView({
  selectedId,
  onSelect,
}: {
  selectedId: string | null;
  onSelect: (id: string | null) => void;
}) {
  const [view, setView] = useState<NeuralViewT | null>(null);
  const [err, setErr] = useState<string | null>(null);
  useEffect(() => {
    getNeural()
      .then(setView)
      .catch(() => setErr("Could not load the substrate seed."));
  }, []);
  if (err) return <div className="tab-loading">{err}</div>;
  if (!view) return <SkeletonList rows={8} label="Loading the substrate seed" />;
  return <NeuralViewContent view={view} selectedId={selectedId} onSelect={onSelect} />;
}

// pure presentational half — rendered from a NeuralView object, so it is testable without mocking
export function NeuralViewContent({
  view,
  selectedId,
  onSelect,
}: {
  view: NeuralViewT;
  selectedId: string | null;
  onSelect: (id: string | null) => void;
}) {
  const circuits = [...view.circuits].sort(
    (a, b) => a.domain.localeCompare(b.domain) || a.id.localeCompare(b.id),
  );
  const connsFor = (cid: string) => ({
    out: view.connections.filter((k) => k.source === cid),
    inc: view.connections.filter((k) => k.target === cid),
  });

  return (
    <div className="neural-tab">
      <NeuralBanner meta={view.meta} gaps={view.gaps} />
      <MasterDetail
        items={circuits}
        getId={(c) => c.id}
        getText={(c) => `${c.id} ${c.name} ${c.domain}`}
        renderRow={(c) => (
          <span className="nv-row">
            <b>{c.id}</b>
            <span className="nv-row-name">{c.name}</span>
            <span className="nv-domain">{c.domain}</span>
          </span>
        )}
        renderDetail={(c) => <CircuitCard circuit={c} conns={connsFor(c.id)} />}
        selectedId={selectedId}
        onSelect={onSelect}
        noun="circuit"
        label="Circuits"
      />
    </div>
  );
}

function NeuralBanner({ meta, gaps }: { meta: NeuralViewT["meta"]; gaps: string[] }) {
  return (
    <div className="neural-banner">
      <div className="neural-banner-head">
        <span className="nv-ro">READ-ONLY</span>
        <span className="neural-banner-text">
          The seed <code>{meta.source_of_truth}</code> (<b>{meta.version}</b>) is the single source of
          truth — {meta.n_circuits} circuits, {meta.n_connections} connections, read through the
          substrate loader. Circuit changes go through a reviewed seed pass, <b>not this browser</b>.
        </span>
      </div>
      <div className="neural-banner-note">
        Default weights are the newborn's initial conditions (qualitative, mostly assumptions) — not
        measured effect sizes. Items marked <span className="nv-scaffold">SCAFFOLD</span> are placeholder
        assumptions, so a placeholder is never mistaken for a measured constant.
      </div>
      {gaps.length > 0 && (
        <details className="nv-gaps">
          <summary>seed gaps register ({gaps.length})</summary>
          <ul>
            {gaps.map((g, i) => (
              <li key={i}>{g}</li>
            ))}
          </ul>
        </details>
      )}
    </div>
  );
}

function CircuitCard({
  circuit,
  conns,
}: {
  circuit: NeuralCircuit;
  conns: { out: NeuralConnection[]; inc: NeuralConnection[] };
}) {
  const c = circuit;
  return (
    <div className="nv-detail">
      <div className="nv-title">
        <b>{c.id}</b> {c.name}
      </div>
      <div className="nv-domain-line">
        {c.domain} · {c.sign > 0 ? "excitatory" : "inhibitory"}
      </div>
      {c.function && <div className="nv-function">{c.function}</div>}

      <div className="nv-block">
        <span className="nv-label">provenance (from the seed)</span>
        <div className="nv-provenance">
          {c.confidence && <ConfidenceChip value={c.confidence} />}
          {c.evidence_base && <span className="nv-evidence">{c.evidence_base}</span>}
        </div>
        {c.sources && <div className="nv-sources">{c.sources}</div>}
      </div>

      <div className="nv-block">
        <span className="nv-label">seed parameters</span>
        <div className="nv-params">
          <span className="nv-param">
            baseline <b>{c.baseline}</b>
          </span>
          <span className="nv-param">
            τ <b>{c.tau_ms} ms</b>
          </span>
          <span className="nv-param">
            online age <b>{c.online_age}</b>
          </span>
        </div>
      </div>

      <ConnectionList title="outgoing" conns={conns.out} />
      <ConnectionList title="incoming" conns={conns.inc} />
    </div>
  );
}

function ConnectionList({ title, conns }: { title: string; conns: NeuralConnection[] }) {
  if (conns.length === 0) return null;
  return (
    <div className="nv-block">
      <span className="nv-label">
        {title} ({conns.length})
      </span>
      {conns.map((k, i) => (
        <div className="nv-conn" key={i}>
          <span className="nv-conn-edge">
            {k.source} → {k.target}
          </span>
          <span className="nv-weight">
            w₀ {k.weight0.toFixed(2)}
            {k.default_weight ? ` (${k.default_weight})` : ""}
          </span>
          {k.scaffold && (
            <span className="nv-scaffold" title="placeholder assumption — not a measured constant">
              SCAFFOLD
            </span>
          )}
          {k.basis && <span className="nv-basis">{k.basis}</span>}
          {k.confidence && <ConfidenceChip value={k.confidence} />}
          {k.citation && <div className="nv-conn-source">{k.citation}</div>}
        </div>
      ))}
    </div>
  );
}

function ConfidenceChip({ value }: { value: string }) {
  return (
    <span className="nv-conf" title="confidence (from the seed)">
      {value}
    </span>
  );
}

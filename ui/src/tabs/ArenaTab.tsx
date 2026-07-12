// ArenaTab — the fine-detail lens (Part 6 S12): a few agents in a confined micro-environment,
// developed and watched. It composes an ArenaSpec from DEFINED content, runs it (POST arena_run),
// and renders the ArenaTrace. It wires the existing core/arena.py — it never reimplements the run.
//
// Honesty (Arena-UI spec §1), visible in the UI:
//  * environments are the DEFINED MICRO_ENVS shown as their present Things + STRUCTURAL escape count
//    (never a "stressful" tag); the dropdown offers no free-text environment.
//  * temperament is PARAMETERS (the gain dims), never outcome-named presets.
//  * relationships EMERGE from shared_hours + seeded history — there is no per-slot relationship
//    control (the honest empty is shown, not a hollow dropdown).
//  * the roster is 2–5 (the instrument's design scale, S12.2) — enforced here, matching run_arena.
//  * what the current trace can't show (full mind/memory inspection) is stated, not faked.
import { useEffect, useMemo, useState } from "react";
import {
  getArenaEnvironments, getArenaSources, getArenaRelationships, sendCommand,
} from "../api";
import type {
  ArenaEnvironment, ArenaRosterBounds, ArenaSources, ArenaRelationships,
  ArenaSlotPayload, ArenaTraceResult,
} from "../types";

let _sid = 0;
const newSlot = (): ArenaSlotPayload => ({ slot_id: `S${++_sid}`, source: "newborn", age: 0.5 });

export function ArenaTab() {
  const [envs, setEnvs] = useState<ArenaEnvironment[]>([]);
  const [bounds, setBounds] = useState<ArenaRosterBounds>({ min: 2, max: 5, why: "" });
  const [sources, setSources] = useState<ArenaSources | null>(null);
  const [rel, setRel] = useState<ArenaRelationships | null>(null);

  const [env, setEnv] = useState("");
  const [slots, setSlots] = useState<ArenaSlotPayload[]>(() => [newSlot(), newSlot()]);
  const [sharedHours, setSharedHours] = useState(3);
  const [seed, setSeed] = useState(0);
  const [years, setYears] = useState(18);

  const [running, setRunning] = useState(false);
  const [trace, setTrace] = useState<ArenaTraceResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [ep, setEp] = useState(0);

  useEffect(() => {
    getArenaEnvironments()
      .then((v) => {
        setEnvs(v.environments);
        setBounds(v.roster);
        if (v.environments[0]) setEnv((e) => e || v.environments[0].id);
      })
      .catch(() => {});
    getArenaSources().then(setSources).catch(() => {});
    getArenaRelationships().then(setRel).catch(() => {});
  }, []);

  const selectedEnv = envs.find((e) => e.id === env);
  const canRun = slots.length >= bounds.min && slots.length <= bounds.max && !!env && !running;

  const setSlot = (i: number, patch: Partial<ArenaSlotPayload>) =>
    setSlots((ss) => ss.map((s, k) => (k === i ? { ...s, ...patch } : s)));
  const addSlot = () => setSlots((ss) => (ss.length < bounds.max ? [...ss, newSlot()] : ss));
  const removeSlot = (i: number) =>
    setSlots((ss) => (ss.length > bounds.min ? ss.filter((_, k) => k !== i) : ss));

  const run = async () => {
    setRunning(true);
    setError(null);
    setTrace(null);
    try {
      const res = await sendCommand({
        cmd: "arena_run", micro_env: env, seed, shared_hours: sharedHours,
        childhood_years: years, slots,
      });
      if (res.error) setError(res.error);
      else if (res.trace) {
        setTrace(res.trace);
        setEp(res.trace.records.length - 1);
      }
    } catch (e) {
      setError(String(e));
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="arena">
      <aside className="arena-setup rail-section">
        <div className="rail-eyebrow">Arena setup</div>

        <label className="rail-field">
          <span>environment</span>
          <select value={env} onChange={(e) => setEnv(e.target.value)}>
            {envs.map((e) => (
              <option key={e.id} value={e.id}>{e.id}</option>
            ))}
          </select>
        </label>
        {selectedEnv && (
          <div className="arena-envinfo" title="the environment IS its present Things; escape is structural (a count), never a tag">
            <div className="arena-note">{selectedEnv.note}</div>
            <div className="arena-things">
              present ({selectedEnv.escape}): {selectedEnv.present.join(", ") || "—"}
            </div>
          </div>
        )}

        <div className="rail-eyebrow" style={{ marginTop: "0.8rem" }}>
          Roster <small>({slots.length}/{bounds.max} · min {bounds.min})</small>
        </div>
        {slots.map((s, i) => (
          <SlotRow
            key={s.slot_id} slot={s} sources={sources}
            onChange={(p) => setSlot(i, p)}
            onRemove={slots.length > bounds.min ? () => removeSlot(i) : undefined}
          />
        ))}
        <button className="arena-add" onClick={addSlot} disabled={slots.length >= bounds.max}>
          + add agent
        </button>

        <label className="rail-field">
          <span title="co-located hours/day — the proximity dial">shared hours/day</span>
          <input type="number" min={0} max={24} step={0.5} value={sharedHours}
                 onChange={(e) => setSharedHours(Number(e.target.value))} />
        </label>
        <label className="rail-field">
          <span title="determinism: a run reproduces exactly from the seed">seed</span>
          <input type="number" value={seed} onChange={(e) => setSeed(Number(e.target.value))} />
        </label>
        <label className="rail-field">
          <span>childhood years</span>
          <input type="number" min={1} max={40} value={years}
                 onChange={(e) => setYears(Number(e.target.value))} />
        </label>

        <button className="arena-run" onClick={run} disabled={!canRun}>
          {running ? "running…" : "▶ Run arena"}
        </button>
        {!canRun && !running && (
          <div className="arena-hint">roster must be {bounds.min}–{bounds.max} agents</div>
        )}
        {rel && (
          <div className="arena-relnote" title="relationships are not set per-slot; they emerge">
            <b>relationships:</b> {rel.substrate}
            {rel.defined.length === 0 && " (no named configs defined yet — grounded matrix work)"}
          </div>
        )}
      </aside>

      <section className="arena-stage">
        {error && <div className="arena-error">Run rejected: {error}</div>}
        {!trace && !error && (
          <div className="arena-placeholder">
            <h3>The Arena — the fine-detail lens</h3>
            <p>
              A few agents ({bounds.min}–{bounds.max}) in a confined micro-environment, developed
              over a real childhood and watched. Configure the roster and run.
            </p>
            <p className="arena-fine">
              What each subject <em>does</em> emerges from its own substrate; the environment is only
              what is <em>present</em> to interact with, and bonds form from shared encounters — nothing
              is assigned. (Full per-agent mind/memory inspection is not in this trace yet — flagged for
              a trace extension; the run below shows each subject's emergent trajectory.)
            </p>
          </div>
        )}
        {trace && <TraceView trace={trace} ep={ep} setEp={setEp} />}
      </section>
    </div>
  );
}

function SlotRow({
  slot, sources, onChange, onRemove,
}: {
  slot: ArenaSlotPayload;
  sources: ArenaSources | null;
  onChange: (p: Partial<ArenaSlotPayload>) => void;
  onRemove?: () => void;
}) {
  const [showTemper, setShowTemper] = useState(false);
  const banked = sources?.banked_ids ?? [];
  const dims = sources?.gain_dims ?? [];
  return (
    <div className="arena-slot">
      <div className="arena-slot-head">
        <b>{slot.slot_id}</b>
        <select value={slot.source} onChange={(e) => onChange({ source: e.target.value })}>
          {(sources?.kinds ?? ["newborn"]).map((k) => <option key={k} value={k}>{k}</option>)}
        </select>
        <label title="spawn age (years)">
          age <input type="number" min={0} max={40} step={0.5} value={slot.age}
                     onChange={(e) => onChange({ age: Number(e.target.value) })} />
        </label>
        {onRemove && <button className="arena-x" onClick={onRemove} title="remove">×</button>}
      </div>
      {slot.source === "grown" && (
        <label className="arena-sub">grow years
          <input type="number" min={1} max={40} value={slot.grow_years ?? 18}
                 onChange={(e) => onChange({ grow_years: Number(e.target.value) })} />
        </label>
      )}
      {slot.source === "banked" && (
        <label className="arena-sub">bank id
          <select value={slot.bank_id ?? ""} onChange={(e) => onChange({ bank_id: e.target.value })}
                  disabled={banked.length === 0}>
            <option value="">{banked.length ? "—" : "(no banked agents)"}</option>
            {banked.map((b) => <option key={b} value={b}>{b}</option>)}
          </select>
        </label>
      )}
      {slot.source !== "banked" && (
        <div className="arena-temper">
          <button className="arena-linkbtn" onClick={() => setShowTemper((v) => !v)}>
            temperament: {slot.gains ? "custom" : "intact"} {showTemper ? "▾" : "▸"}
          </button>
          {showTemper && (
            <div className="arena-gains" title="temperament is PARAMETERS (gain dims), never an outcome name; 0.5 = intact">
              {dims.map((d) => (
                <label key={d} className="arena-gain">
                  <span>{d}</span>
                  <input type="number" min={0} max={1} step={0.1}
                         value={slot.gains?.[d] ?? 0.5}
                         onChange={(e) => onChange({ gains: { ...(slot.gains ?? {}), [d]: Number(e.target.value) } })} />
                </label>
              ))}
              {slot.gains && (
                <button className="arena-linkbtn" onClick={() => onChange({ gains: undefined })}>
                  reset to intact
                </button>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function TraceView({
  trace, ep, setEp,
}: {
  trace: ArenaTraceResult;
  ep: number;
  setEp: (n: number) => void;
}) {
  const rec = trace.records[Math.min(ep, trace.records.length - 1)];
  const ids = trace.agent_ids;
  const pairs = Object.keys(rec.strain);
  return (
    <div className="arena-trace">
      <div className={"arena-viab " + (trace.viable ? "ok" : "bad")}>
        <span>{trace.viable ? "✓ viable" : "✗ saturated"}</span>
        <span>{trace.settled ? "settled" : "oscillating"}</span>
        <span title="highest single-circuit activation any agent reached (near 1.0 = pinned)">
          peak activation {trace.peak_activation.toFixed(3)}
        </span>
        <span className="arena-fine">env {trace.spec.micro_env} · escape {trace.spec.escape} · seed {trace.spec.seed} · shared {trace.spec.shared_hours}h</span>
      </div>

      <label className="arena-scrub">
        episode {rec.episode} · age {rec.age.toFixed(1)}
        <input type="range" min={0} max={trace.records.length - 1} value={ep}
               onChange={(e) => setEp(Number(e.target.value))} />
      </label>

      <div className="arena-agents">
        {ids.map((id) => (
          <div key={id} className="arena-agentcard">
            <div className="arena-agenthead"><b>{id}</b> <span className="arena-act">{rec.acts[id]}</span></div>
            <Sparkline series={trace.records.map((r) => r.max_act[id] ?? 0)} cursor={ep} />
            <div className="arena-fine">
              max act {(rec.max_act[id] ?? 0).toFixed(3)} · drift {(rec.drift[id] ?? 0).toFixed(3)}
            </div>
          </div>
        ))}
      </div>

      {pairs.length > 0 && (
        <div className="arena-ties">
          <div className="rail-eyebrow">tie strain (per pair)</div>
          {pairs.map((p) => (
            <div key={p} className="arena-tie">
              <span>{p}</span>
              <div className="arena-bar"><div style={{ width: `${Math.round((rec.strain[p] ?? 0) * 100)}%` }} /></div>
              <span>{(rec.strain[p] ?? 0).toFixed(2)}</span>
            </div>
          ))}
        </div>
      )}

      <div className="arena-counts">
        <div className="rail-eyebrow">emergent acts (whole run)</div>
        {Object.entries(trace.act_counts).sort((a, b) => b[1] - a[1]).map(([act, n]) => (
          <span key={act} className="arena-chip">{act} <b>{n}</b></span>
        ))}
      </div>
    </div>
  );
}

// A minimal saturation sparkline: the agent's max-activation over episodes (near the top = pinned).
function Sparkline({ series, cursor }: { series: number[]; cursor: number }) {
  const W = 220, H = 34;
  const pts = useMemo(() => {
    if (series.length < 2) return "";
    return series
      .map((v, i) => `${(i / (series.length - 1)) * W},${H - Math.max(0, Math.min(1, v)) * H}`)
      .join(" ");
  }, [series]);
  const cx = series.length > 1 ? (cursor / (series.length - 1)) * W : 0;
  return (
    <svg className="arena-spark" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="none" aria-hidden>
      <line x1={0} y1={H * 0.05} x2={W} y2={H * 0.05} className="arena-satline" />
      <polyline points={pts} />
      <line x1={cx} y1={0} x2={cx} y2={H} className="arena-cursor" />
    </svg>
  );
}

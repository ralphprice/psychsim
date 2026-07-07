// Controls — the top of the side panel: transport (play/speed), live population
// controls (add resident, respawn a town), and view options (grid vs plan-view,
// labels, camera-follow).

import { useEffect, useState } from "react";
import type { SimState, SaveMeta, LibraryInfo, Command } from "../types";
import type { ViewMode } from "../view";
import { getLibrary, getProfiles, getRoles } from "../api";

const BASE_INTERVAL = 0.25; // server default seconds/step; speed is a multiplier of this

interface ControlsProps {
  state: SimState;
  saves: SaveMeta[];
  error: string | null;
  mode: ViewMode;
  onMode: (m: ViewMode) => void;
  labels: boolean;
  onLabels: (v: boolean) => void;
  follow: boolean;
  onFollow: (v: boolean) => void;
  hasSelection: boolean;
  command: (cmd: Command) => Promise<unknown>;
}

export function Controls({
  state,
  saves,
  error,
  mode,
  onMode,
  labels,
  onLabels,
  follow,
  onFollow,
  hasSelection,
  command,
}: ControlsProps) {
  const [pop, setPop] = useState(80);
  const [temper, setTemper] = useState("typical");
  const [profile, setProfile] = useState("england_2021");
  const [profiles, setProfiles] = useState<string[]>([]);
  const [role, setRole] = useState("child");
  const [roles, setRoles] = useState<string[]>(["child", "adult"]);
  const [experiment, setExperiment] = useState(false);
  const [library, setLibrary] = useState<LibraryInfo | null>(null);
  const [saveName, setSaveName] = useState("");
  const [chosen, setChosen] = useState("");

  useEffect(() => {
    getLibrary().then(setLibrary).catch(() => {});
    getProfiles().then(setProfiles).catch(() => {});
    getRoles().then((r) => r.length && setRoles(r)).catch(() => {});
  }, []);

  // keep the load dropdown pointed at a real save as the list changes
  useEffect(() => {
    if (saves.length && !saves.some((s) => s.slug === chosen)) setChosen(saves[0].slug);
    if (!saves.length && chosen) setChosen("");
  }, [saves, chosen]);

  const residents = Object.keys(state.people).length;
  const speedMult = state.interval ? BASE_INTERVAL / state.interval : 1;
  const setSpeed = (mult: number) => command({ cmd: "speed", interval: BASE_INTERVAL / mult });

  return (
    <div className="controls">
      <h1>
        PsychSim <span className="clock">{state.clock}</span>
      </h1>
      {error && <div className="err">{error}</div>}

      <div className="row">
        <button className="primary" onClick={() => command({ cmd: state.playing ? "pause" : "play" })}>
          {state.playing ? "❚❚ Pause" : "▶ Start"}
        </button>
        <button onClick={() => setSpeed(speedMult / 2)}>« slower</button>
        <button onClick={() => setSpeed(speedMult * 2)}>faster »</button>
        <span className="spd">{speedMult.toFixed(2)}×</span>
      </div>

      <div className="row">
        <span>
          residents: <b>{residents}</b>
        </span>
        <select
          value={temper}
          onChange={(e) => setTemper(e.target.value)}
          title="temperament of the authored subject: the given inherited reactivity (its personality then grows on the substrate)"
        >
          <option value="typical">typical</option>
          <option value="fearless">fearless</option>
          <option value="fearless_calculating">fearless (calc.)</option>
        </select>
        <select value={role} onChange={(e) => setRole(e.target.value)} title="role from the library">
          {roles.map((r) => (
            <option key={r} value={r}>
              {r}
            </option>
          ))}
        </select>
        <button
          onClick={() => command({ cmd: "add_person", role, temperament: temper } as Command)}
        >
          + add
        </button>
      </div>

      <div className="row">
        <span>spawn town, pop</span>
        <input
          type="number"
          value={pop}
          min={20}
          max={300}
          onChange={(e) => setPop(Number(e.target.value))}
        />
        <button onClick={() => command({ cmd: "respawn", population: pop, experiment, profile })}>
          Spawn
        </button>
      </div>
      <div className="row">
        <span>town type</span>
        <select
          className="grow"
          value={profile}
          onChange={(e) => setProfile(e.target.value)}
          title="country/culture town-type: sets house/family/hospital/shop proportions (data/towntypes/*.json)"
        >
          {(profiles.length ? profiles : [profile]).map((p) => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </select>
      </div>
      <div className="row">
        <label
          className="chk"
          title="load a fixed, grown-adult background from the character library; only the study subjects (children by default) evolve live around them"
        >
          <input
            type="checkbox"
            checked={experiment}
            onChange={(e) => setExperiment(e.target.checked)}
          />{" "}
          controlled experiment (fixed background)
        </label>
      </div>
      {state.experiment && (
        <div className="row exp-status">
          <span className="dot live" /> {state.subjects} live subjects &nbsp;
          <span className="dot bg" /> {state.background} fixed background
        </div>
      )}
      {library && library.count > 0 && (
        <details className="lib">
          <summary>character library · {library.count} grown adults</summary>
          <div className="lib-list">
            {library.adults.map((a, i) => (
              <div className="lib-row" key={i}>
                <b>{a.name}</b> · {a.temperament}/{a.rearing} → {a.dominant}
              </div>
            ))}
          </div>
        </details>
      )}

      <div className="row viewrow">
        <span>view</span>
        <div className="seg">
          <button className={mode === "grid" ? "on" : ""} onClick={() => onMode("grid")}>
            grid
          </button>
          <button className={mode === "plan" ? "on" : ""} onClick={() => onMode("plan")}>
            plan
          </button>
        </div>
      </div>

      <div className="row">
        <label className="chk">
          <input type="checkbox" checked={labels} onChange={(e) => onLabels(e.target.checked)} /> labels
        </label>
        <label className="chk" title={hasSelection ? "" : "select a person first"}>
          <input
            type="checkbox"
            checked={follow}
            disabled={!hasSelection}
            onChange={(e) => onFollow(e.target.checked)}
          />{" "}
          follow
        </label>
      </div>

      <div className="save-block">
        <div className="row">
          <input
            className="grow"
            type="text"
            placeholder="save as…"
            value={saveName}
            onChange={(e) => setSaveName(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && saveName.trim()) {
                command({ cmd: "save", name: saveName.trim() });
                setSaveName("");
              }
            }}
          />
          <button
            disabled={!saveName.trim()}
            onClick={() => {
              command({ cmd: "save", name: saveName.trim() });
              setSaveName("");
            }}
          >
            Save
          </button>
        </div>
        <div className="row">
          <select className="grow" value={chosen} onChange={(e) => setChosen(e.target.value)}>
            {!saves.length && <option value="">no saved sims</option>}
            {saves.map((s) => (
              <option key={s.slug} value={s.slug}>
                {s.name} · {s.clock} · {s.residents} · {s.saved_label}
              </option>
            ))}
          </select>
          <button disabled={!chosen} onClick={() => chosen && command({ cmd: "load", slug: chosen })}>
            Load
          </button>
          <button
            className="del"
            title="delete this save"
            disabled={!chosen}
            onClick={() => chosen && command({ cmd: "delete_save", slug: chosen })}
          >
            🗑
          </button>
        </div>
      </div>
    </div>
  );
}

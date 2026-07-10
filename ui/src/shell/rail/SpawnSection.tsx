// SpawnSection — spawn a fresh town: town type, population, and controlled-experiment mode.
import { useEffect, useState } from "react";
import type { SimState, Command } from "../../types";
import { getProfiles } from "../../api";

export function SpawnSection({
  state,
  command,
}: {
  state: SimState;
  command: (cmd: Command) => Promise<unknown>;
}) {
  const [pop, setPop] = useState(200);
  const [profile, setProfile] = useState("england_2021");
  const [profiles, setProfiles] = useState<string[]>([]);
  const [experiment, setExperiment] = useState(false);

  useEffect(() => {
    getProfiles().then(setProfiles).catch(() => {});
  }, []);

  return (
    <section className="rail-section">
      <div className="rail-eyebrow">Spawn</div>
      <label className="rail-field" title="country/culture town type: sets house/family/hospital/shop proportions">
        <span>town type</span>
        <select value={profile} onChange={(e) => setProfile(e.target.value)}>
          {(profiles.length ? profiles : [profile]).map((p) => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </select>
      </label>
      <label className="rail-field">
        <span>population</span>
        <input type="number" value={pop} min={20} max={300} onChange={(e) => setPop(Number(e.target.value))} />
      </label>
      <label
        className="rail-check"
        title="load a fixed grown-adult background from the library; only the study subjects evolve live around them"
      >
        <input type="checkbox" checked={experiment} onChange={(e) => setExperiment(e.target.checked)} />
        <span>
          controlled experiment
          <em>(fixed background)</em>
        </span>
      </label>
      {state.experiment && (
        <div className="rail-note">
          <span className="dot live" /> {state.subjects} live subjects · <span className="dot bg" />{" "}
          {state.background} fixed background
        </div>
      )}
      <button onClick={() => command({ cmd: "respawn", population: pop, experiment, profile })}>
        Spawn town
      </button>
    </section>
  );
}

// PopulationSection — live population: resident count + author one study subject.
//
// DEPRECATED (U1): the temperament dropdown (typical / fearless / fearless (calc.)) is the
// pre-redesign study interface -- an outcome-adjacent authoring shortcut. It is REPLACED by the
// throttle panel (scan controller), which exposes CIRCUITS (0-100, intact = 100), never outcome
// names; what a configuration produces is measured, never named in advance. Left functional for now,
// marked here the way the Panksepp primitives were marked before their cut.
import { useEffect, useState } from "react";
import type { SimState, Command } from "../../types";
import { getRoles } from "../../api";

export function PopulationSection({
  state,
  command,
}: {
  state: SimState;
  command: (cmd: Command) => Promise<unknown>;
}) {
  const [temper, setTemper] = useState("typical"); // DEPRECATED — replaced by the throttle panel
  const [role, setRole] = useState("child");
  const [roles, setRoles] = useState<string[]>(["child", "adult"]);

  useEffect(() => {
    getRoles().then((r) => r.length && setRoles(r)).catch(() => {});
  }, []);

  const residents = Object.keys(state.people).length;
  return (
    <section className="rail-section">
      <div className="rail-eyebrow">Population</div>
      <div className="rail-readout">
        <span>residents</span>
        <b>{residents}</b>
      </div>
      <label className="rail-field" title="DEPRECATED — replaced by the throttle panel (scan controller)">
        <span>profile</span>
        <select value={temper} onChange={(e) => setTemper(e.target.value)}>
          <option value="typical">typical</option>
          <option value="fearless">fearless</option>
          <option value="fearless_calculating">fearless (calc.)</option>
        </select>
      </label>
      <label className="rail-field">
        <span>role</span>
        <select value={role} onChange={(e) => setRole(e.target.value)}>
          {roles.map((r) => (
            <option key={r} value={r}>
              {r}
            </option>
          ))}
        </select>
      </label>
      <button onClick={() => command({ cmd: "add_person", role, temperament: temper } as Command)}>
        + Add person
      </button>
    </section>
  );
}

// PopulationSection — live population: resident count + author one study subject.
//
// The temperament-preset dropdown was REMOVED (U1, 2.2c-ahead): a preset that named a disposition
// implied a SEEDED OUTCOME, which the substrate does not do (a disposition is MEASURED, never
// selected). Authoring now falls back to standard roles -- a standard agent is seeded and its
// disposition emerges. Cut the way the Panksepp primitives were cut. (The CU-seed dropdown, 2.2c, is
// a separate NEW seeding path added once the CU surface is built -- not a replacement for this preset.
// Configurations are exposed as CIRCUITS via the throttle panel / scan controller; what a
// configuration produces is measured, never named ahead.)
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
      <button onClick={() => command({ cmd: "add_person", role } as Command)}>
        + Add person
      </button>
    </section>
  );
}

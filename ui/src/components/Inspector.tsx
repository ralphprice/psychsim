// Inspector — the click-to-inspect panel: a resident's role, the emergent substrate
// domain profile, group standing, and recent memories. A descriptive read-out only —
// never a "psychopath/sophropath" label (that classifier is gone).

import type { PersonDetail } from "../types";
import { driveColour } from "../theme";

export function Inspector({ p }: { p: PersonDetail }) {
  // `systems` is a normalised domain profile (one scalar per domain, summing to ~1).
  // Scale each bar to the strongest domain so shares stay legible; show the raw share.
  const systems = Object.entries(p.systems);
  const peak = systems.reduce((m, [, v]) => Math.max(m, v), 0) || 1;
  return (
    <div>
      <h2>{p.name}</h2>
      <div className="role">
        {p.role_name || p.role} · home: {p.home ?? "—"}
        {p.work ? ` · works: ${p.work}` : ""}
      </div>
      <div className={`mindstate ${p.subject ? "live" : "bg"}`}>{p.mind_state}</div>
      {p.temperament && (
        <div className="temper">
          temperament (given): <b>{p.temperament}</b>
        </div>
      )}

      <h3>domain profile (normalised activity)</h3>
      {systems.map(([s, v]) => (
        <div className="net" key={s}>
          <span className="n">{s}</span>
          <span className="bar">
            <span
              className="f"
              style={{ width: `${Math.round((v / peak) * 100)}%`, background: driveColour(s) }}
            />
          </span>
          <span className="v">{v.toFixed(2)}</span>
        </div>
      ))}

      <h3>groups &amp; standing</h3>
      {p.groups.length ? (
        p.groups.map((g, i) => (
          <div className="grp" key={i}>
            {g.group}: standing {g.standing}, belonging {g.belonging}{" "}
            <i className="route">({g.route})</i>
          </div>
        ))
      ) : (
        <div className="grp muted">none yet</div>
      )}

      <h3>recent memories ({p.memories.length})</h3>
      {p.memories.length ? (
        p.memories
          .slice()
          .reverse()
          .map((m, i) => (
            <div className="mem" key={i}>
              {m.label}
              <span
                className="v"
                style={{ color: m.valence > 0 ? "#2e8b3f" : m.valence < 0 ? "#b23b3b" : "#888" }}
              >
                {m.valence > 0 ? "+" : ""}
                {m.valence}
              </span>
            </div>
          ))
      ) : (
        <div className="mem muted">no memories yet</div>
      )}
    </div>
  );
}

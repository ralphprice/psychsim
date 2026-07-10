// SessionSection — save / load / delete a whole simulation.
import { useEffect, useState } from "react";
import type { SaveMeta, Command } from "../../types";

export function SessionSection({
  saves,
  command,
}: {
  saves: SaveMeta[];
  command: (cmd: Command) => Promise<unknown>;
}) {
  const [saveName, setSaveName] = useState("");
  const [chosen, setChosen] = useState("");
  const [confirmDel, setConfirmDel] = useState(false);

  useEffect(() => {
    if (saves.length && !saves.some((s) => s.slug === chosen)) setChosen(saves[0].slug);
    if (!saves.length && chosen) setChosen("");
    setConfirmDel(false);
  }, [saves, chosen]);

  const doSave = () => {
    if (saveName.trim()) {
      command({ cmd: "save", name: saveName.trim() });
      setSaveName("");
    }
  };

  return (
    <section className="rail-section">
      <div className="rail-eyebrow">Session</div>
      <div className="rail-two-up">
        <input
          type="text"
          placeholder="save as…"
          value={saveName}
          onChange={(e) => setSaveName(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && doSave()}
        />
        <button disabled={!saveName.trim()} onClick={doSave}>
          Save
        </button>
      </div>
      {saves.length === 0 ? (
        <div className="rail-note">No saved sims. Run a town, then Save.</div>
      ) : (
        <>
          <select value={chosen} onChange={(e) => setChosen(e.target.value)}>
            {saves.map((s) => (
              <option key={s.slug} value={s.slug}>
                {s.name} · {s.clock} · {s.residents}
              </option>
            ))}
          </select>
          <div className="rail-two-up">
            <button disabled={!chosen} onClick={() => chosen && command({ cmd: "load", slug: chosen })}>
              Load
            </button>
            {confirmDel ? (
              <button
                className="warn"
                onClick={() => {
                  if (chosen) command({ cmd: "delete_save", slug: chosen });
                  setConfirmDel(false);
                }}
              >
                confirm 🗑
              </button>
            ) : (
              <button className="del" disabled={!chosen} title="delete this save" onClick={() => setConfirmDel(true)}>
                🗑
              </button>
            )}
          </div>
        </>
      )}
    </section>
  );
}

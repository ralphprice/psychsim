// LibrarySection — the grown-adult character library available as fixed background.
import { useEffect, useState } from "react";
import type { LibraryInfo } from "../../types";
import { getLibrary } from "../../api";

export function LibrarySection() {
  const [library, setLibrary] = useState<LibraryInfo | null>(null);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    getLibrary().then(setLibrary).catch(() => {});
  }, []);

  const count = library?.count ?? 0;
  return (
    <section className="rail-section">
      <div className="rail-eyebrow">Library</div>
      {count > 0 ? (
        <>
          <div className="rail-readout">
            <span>grown adults</span>
            <b>{count}</b>
          </div>
          <button onClick={() => setOpen((v) => !v)}>{open ? "Hide library" : "View library"}</button>
          {open && (
            <div className="rail-list">
              {library!.adults.map((a, i) => (
                <div className="rail-list-row" key={i}>
                  <b>{a.name}</b> · {a.temperament}/{a.rearing} → {a.dominant}
                </div>
              ))}
            </div>
          )}
        </>
      ) : (
        <div className="rail-note">No grown-adult library. Spawn a controlled experiment to build one.</div>
      )}
    </section>
  );
}

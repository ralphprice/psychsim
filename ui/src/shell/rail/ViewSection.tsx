// ViewSection — Town-stage view options (grid/plan, labels, camera-follow). CONTEXTUAL: it only
// affects the Town stage, so on other tabs it renders dimmed + aria-disabled (layout stability over
// purity: do not hide it).
import type { ViewMode } from "../../view";

export function ViewSection({
  active,
  mode,
  onMode,
  labels,
  onLabels,
  follow,
  onFollow,
  hasSelection,
}: {
  active: boolean; // true only on the Town tab
  mode: ViewMode;
  onMode: (m: ViewMode) => void;
  labels: boolean;
  onLabels: (v: boolean) => void;
  follow: boolean;
  onFollow: (v: boolean) => void;
  hasSelection: boolean;
}) {
  return (
    <section className={"rail-section" + (active ? "" : " dim")} aria-disabled={!active}>
      <div className="rail-eyebrow">View {active ? "" : <em>(Town)</em>}</div>
      <div className="rail-seg">
        <button className={mode === "grid" ? "on" : ""} disabled={!active} onClick={() => onMode("grid")}>
          grid
        </button>
        <button className={mode === "plan" ? "on" : ""} disabled={!active} onClick={() => onMode("plan")}>
          plan
        </button>
      </div>
      <div className="rail-two-up">
        <label className="rail-check">
          <input type="checkbox" checked={labels} disabled={!active} onChange={(e) => onLabels(e.target.checked)} />
          <span>labels</span>
        </label>
        <label className="rail-check" title={hasSelection ? "" : "select a person first"}>
          <input
            type="checkbox"
            checked={follow}
            disabled={!active || !hasSelection}
            onChange={(e) => onFollow(e.target.checked)}
          />
          <span>follow</span>
        </label>
      </div>
    </section>
  );
}

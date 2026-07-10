// TownTab — the default tab: a full-width pannable stage (grid or plan background + live people
// overlay), with the Inspector presented as a dismissible right-hand OVERLAY (not a squashed sidebar,
// not a modal). Three ways to dismiss: the × button, Escape, or clicking empty stage.

import { useEffect, useMemo, useRef } from "react";
import type * as React from "react";
import type { PersonDetail, TownGeometry, PlanView, SimState } from "../types";
import { gridViewModel, planViewModel, type ViewMode, type ViewModel } from "../view";
import { Stage, type StageHandle } from "../components/Stage";
import { GridBackground } from "../components/GridBackground";
import { PlanBackground } from "../components/PlanBackground";
import { PeopleLayer } from "../components/PeopleLayer";
import { Inspector } from "../components/Inspector";
import { Legend } from "../components/Legend";

export function TownTab({
  town,
  plan,
  state,
  error,
  mode,
  labels,
  selected,
  selectedCid,
  followCid,
  onPick,
  onClear,
}: {
  town: TownGeometry | null;
  plan: PlanView | null;
  state: SimState;
  error: string | null;
  mode: ViewMode;
  labels: boolean;
  selected: PersonDetail | null;
  selectedCid: string | null;
  followCid: string | null;
  onPick: (cid: string) => void;
  onClear: () => void;
}) {
  const stageRef = useRef<StageHandle>(null);

  // choose the active view model + background, with a graceful grid fallback while the (larger) plan
  // SVG is still loading
  const { vm, background } = useMemo<{ vm: ViewModel | null; background: React.ReactNode }>(() => {
    if (mode === "plan" && plan) {
      return { vm: planViewModel(plan), background: <PlanBackground plan={plan} /> };
    }
    if (town) {
      return { vm: gridViewModel(town), background: <GridBackground town={town} /> };
    }
    return { vm: null, background: null };
  }, [mode, plan, town]);

  // Escape dismisses the inspector overlay
  useEffect(() => {
    if (!selected) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClear();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [selected, onClear]);

  return (
    <div className="town-tab">
      <div className="stage-wrap">
        {vm ? (
          <Stage ref={stageRef} W={vm.W} H={vm.H} onPick={onPick} onEmptyClick={onClear}>
            {background}
            <PeopleLayer
              people={state.people}
              view={vm}
              selectedCid={selectedCid}
              followCid={followCid}
              showLabels={labels}
              stage={stageRef}
            />
          </Stage>
        ) : (
          <div className="loading">{error ?? "Loading town…"}</div>
        )}
        <Legend />
        <div className="hint">scroll = zoom · drag = pan</div>
        {vm && !selected && (
          <div className="town-empty">
            Click a person to inspect their mind, memories, role and standing.
          </div>
        )}
      </div>

      {selected && (
        <aside className="inspector-overlay" role="complementary" aria-label="inspector">
          <div className="overlay-head">
            <button
              className="inspector-close"
              onClick={onClear}
              title="dismiss (Esc)"
              aria-label="close inspector"
            >
              ×
            </button>
          </div>
          <div className="inspect">
            <Inspector p={selected} />
          </div>
        </aside>
      )}
    </div>
  );
}

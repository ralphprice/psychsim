// App — composes the live control panel: a pannable stage (grid or plan-view
// background + live people overlay) beside a control + inspect panel.

import { useEffect, useMemo, useRef, useState } from "react";
import type * as React from "react";
import { useSim } from "./hooks/useSim";
import { getPerson } from "./api";
import type { PersonDetail } from "./types";
import { gridViewModel, planViewModel, type ViewMode, type ViewModel } from "./view";
import { Stage, type StageHandle } from "./components/Stage";
import { GridBackground } from "./components/GridBackground";
import { PlanBackground } from "./components/PlanBackground";
import { PeopleLayer } from "./components/PeopleLayer";
import { Controls } from "./components/Controls";
import { Inspector } from "./components/Inspector";
import { Legend } from "./components/Legend";
import { Development } from "./components/Development";
import { MatrixEditor } from "./components/MatrixEditor";
import { NeuralEditor } from "./components/NeuralEditor";
import { ExecutiveEditor } from "./components/ExecutiveEditor";

const DETAIL_POLL_MS = 700;

export default function App() {
  const { town, plan, state, saves, error, command } = useSim();
  const [mode, setMode] = useState<ViewMode>("plan");
  const [labels, setLabels] = useState(true);
  const [follow, setFollow] = useState(false);
  const [selected, setSelected] = useState<PersonDetail | null>(null);
  const stageRef = useRef<StageHandle>(null);

  // resizable divider: the work happens in the panel, so it can be widened (and the
  // width persists). Drag the divider; double-click resets it.
  const [panelWidth, setPanelWidth] = useState(() => {
    const v = typeof localStorage !== "undefined" ? Number(localStorage.getItem("psychsim.panelW")) : NaN;
    return v >= 300 ? v : 400;
  });
  useEffect(() => {
    if (typeof localStorage !== "undefined")
      localStorage.setItem("psychsim.panelW", String(Math.round(panelWidth)));
  }, [panelWidth]);
  const startResize = (e: React.MouseEvent) => {
    e.preventDefault();
    document.body.classList.add("resizing");
    const move = (ev: MouseEvent) => {
      const w = Math.min(Math.max(window.innerWidth - ev.clientX, 300), window.innerWidth - 200);
      setPanelWidth(w);
    };
    const up = () => {
      document.body.classList.remove("resizing");
      window.removeEventListener("mousemove", move);
      window.removeEventListener("mouseup", up);
    };
    window.addEventListener("mousemove", move);
    window.addEventListener("mouseup", up);
  };

  const selectedCid = selected?.cid ?? null;

  // refresh the inspected person's mind while the sim runs
  useEffect(() => {
    if (!selectedCid) return;
    const id = setInterval(() => {
      getPerson(selectedCid).then(setSelected).catch(() => {});
    }, DETAIL_POLL_MS);
    return () => clearInterval(id);
  }, [selectedCid]);

  // a fresh town (respawn) invalidates the current selection
  const townKey = town ? `${town.cols}x${town.rows}:${town.buildings.length}` : "";
  useEffect(() => {
    setSelected(null);
    setFollow(false);
  }, [townKey]);

  const pick = (cid: string) => {
    getPerson(cid).then(setSelected).catch(() => {});
  };
  const clearSelection = () => {
    setSelected(null);
    setFollow(false);
  };

  // choose the active view model + background, with a graceful grid fallback while
  // the (larger) plan SVG is still loading
  const { vm, background } = useMemo<{ vm: ViewModel | null; background: React.ReactNode }>(() => {
    if (mode === "plan" && plan) {
      return { vm: planViewModel(plan), background: <PlanBackground plan={plan} /> };
    }
    if (town) {
      return { vm: gridViewModel(town), background: <GridBackground town={town} /> };
    }
    return { vm: null, background: null };
  }, [mode, plan, town]);

  const followCid = follow && selectedCid ? selectedCid : null;

  return (
    <div className="root">
      <div className="stage-wrap">
        {vm ? (
          <Stage ref={stageRef} W={vm.W} H={vm.H} onPick={pick} onEmptyClick={clearSelection}>
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
        <div className="hint">scroll = zoom · drag = pan · click a person</div>
      </div>

      <div
        className="divider"
        onMouseDown={startResize}
        onDoubleClick={() => setPanelWidth(400)}
        title="drag to resize the panel · double-click to reset"
      />

      <div className="panel" style={{ width: panelWidth }}>
        <Controls
          state={state}
          saves={saves}
          error={error}
          mode={mode}
          onMode={setMode}
          labels={labels}
          onLabels={setLabels}
          follow={follow}
          onFollow={setFollow}
          hasSelection={!!selectedCid}
          command={command}
        />
        <div className="inspect">
          {selected ? (
            <Inspector p={selected} />
          ) : (
            <div className="hint-block">
              Click a person to inspect their mind, memories, role and standing.
            </div>
          )}
          <Development selectedCid={selectedCid} />
          <MatrixEditor />
          <NeuralEditor />
          <ExecutiveEditor />
        </div>
      </div>
    </div>
  );
}

// App — the console shell: telemetry strip + tab bar + control rail, with the active tab's content
// in the main panel. Tab content lives in tabs/*; the shell owns cross-tab state (active tab, the
// Town selection that the rail's VIEW section reads) and nothing else.

import { useEffect, useState } from "react";
import { useSim } from "./hooks/useSim";
import { getPerson } from "./api";
import type { PersonDetail } from "./types";
import { type ViewMode } from "./view";
import { TownTab } from "./tabs/TownTab";
import { TelemetryStrip } from "./shell/TelemetryStrip";
import { TabBar, TABS, type TabId } from "./shell/TabBar";
import { ControlRail } from "./shell/ControlRail";
import { ErrorBoundary } from "./shell/ErrorBoundary";

const DETAIL_POLL_MS = 700;

export default function App() {
  const { town, plan, state, saves, error, command } = useSim();
  // shell: which subsystem tab is open (persisted), and the control-rail width (persisted).
  const [tab, setTab] = useState<TabId>(
    () => (typeof localStorage !== "undefined"
      ? (localStorage.getItem("psychsim.tab") as TabId) : null) || "town",
  );
  useEffect(() => {
    if (typeof localStorage !== "undefined") localStorage.setItem("psychsim.tab", tab);
  }, [tab]);
  const [railW] = useState(() => {
    const v = typeof localStorage !== "undefined" ? Number(localStorage.getItem("psychsim.railW")) : NaN;
    return v >= 240 ? v : 280;
  });
  const [mode, setMode] = useState<ViewMode>("plan");
  const [labels, setLabels] = useState(true);
  const [follow, setFollow] = useState(false);
  const [selected, setSelected] = useState<PersonDetail | null>(null);

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

  const followCid = follow && selectedCid ? selectedCid : null;

  const townView = (
    <TownTab
      town={town}
      plan={plan}
      state={state}
      error={error}
      mode={mode}
      labels={labels}
      selected={selected}
      selectedCid={selectedCid}
      followCid={followCid}
      onPick={pick}
      onClear={clearSelection}
    />
  );

  const activeLabel = TABS.find((t) => t.id === tab)?.label ?? "";
  return (
    <div className="console">
      <TelemetryStrip state={state} />
      <TabBar active={tab} onTab={setTab} />
      <div className="console-body">
        <ControlRail
          width={railW}
          state={state}
          saves={saves}
          command={command}
          error={error}
          view={{
            active: tab === "town",
            mode,
            onMode: setMode,
            labels,
            onLabels: setLabels,
            follow,
            onFollow: setFollow,
            hasSelection: !!selectedCid,
          }}
        />
        <div className="tab-content" role="tabpanel" aria-label={activeLabel}>
          <ErrorBoundary resetKey={tab}>
            {tab === "town" ? (
              townView
            ) : (
              <div className="tab-placeholder">{activeLabel} — arrives in a later phase.</div>
            )}
          </ErrorBoundary>
        </div>
      </div>
    </div>
  );
}

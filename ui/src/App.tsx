// App — the console shell: telemetry strip + tab bar + control rail, with the active tab's content
// in the main panel. Tab content lives in tabs/*; the shell owns cross-tab state (active tab, the
// Town selection that the rail's VIEW section reads) and nothing else.

import { useEffect, useMemo, useState } from "react";
import { useSim } from "./hooks/useSim";
import { getPerson } from "./api";
import type { PersonDetail } from "./types";
import { type ViewMode } from "./view";
import { isDaytime } from "./shell/clock";
import { TownTab } from "./tabs/TownTab";
import { MatrixTab } from "./tabs/MatrixTab";
import { DevelopmentCohortTab } from "./tabs/DevelopmentCohortTab";
import { NeuralView } from "./tabs/NeuralView";
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
  // per-tab selection for the master-detail tabs (matrices now; cohort/neural later). Kept in the
  // shell so selection persists across tab switches, keyed by tab.
  const [selById, setSelById] = useState<Partial<Record<TabId, string | null>>>({});
  const selectFor = (t: TabId) => (id: string | null) => setSelById((m) => ({ ...m, [t]: id }));

  // monitored agents (Phase 8): a researcher-curated set, pinned from the Development Cohort tab.
  // Order fixes the map badge index (1..N); persisted. A badge is a plain index, never a condition.
  const [monitored, setMonitored] = useState<string[]>(() => {
    try {
      const v = typeof localStorage !== "undefined" ? localStorage.getItem("psychsim.monitored") : null;
      return v ? (JSON.parse(v) as string[]) : [];
    } catch {
      return [];
    }
  });
  useEffect(() => {
    if (typeof localStorage !== "undefined")
      localStorage.setItem("psychsim.monitored", JSON.stringify(monitored));
  }, [monitored]);
  const toggleMonitor = (cid: string) =>
    setMonitored((m) => (m.includes(cid) ? m.filter((c) => c !== cid) : [...m, cid]));
  const monitoredIndex = useMemo(
    () => Object.fromEntries(monitored.map((cid, i) => [cid, i + 1])) as Record<string, number>,
    [monitored],
  );

  // night is a CLOCK read-out (the substrate has no diurnal coupling) — used only to step the town
  // ground a few points darker.
  const night = !isDaytime(state.sim_time);

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
      monitoredIndex={monitoredIndex}
      night={night}
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
        <div
          className="tab-content"
          id="tabpanel"
          role="tabpanel"
          aria-labelledby={`tab-${tab}`}
          tabIndex={-1}
        >
          <ErrorBoundary resetKey={tab}>
            {tab === "town" ? (
              townView
            ) : tab === "cohort" ? (
              <DevelopmentCohortTab
                people={state.people}
                selectedId={selById.cohort ?? null}
                onSelect={selectFor("cohort")}
                monitoredIndex={monitoredIndex}
                onToggleMonitor={toggleMonitor}
              />
            ) : tab === "social" || tab === "environment" || tab === "group" ? (
              <MatrixTab kind={tab} selectedId={selById[tab] ?? null} onSelect={selectFor(tab)} />
            ) : tab === "neural" ? (
              <NeuralView selectedId={selById.neural ?? null} onSelect={selectFor("neural")} />
            ) : (
              <div className="tab-placeholder">{activeLabel} — arrives in a later phase.</div>
            )}
          </ErrorBoundary>
        </div>
      </div>
    </div>
  );
}

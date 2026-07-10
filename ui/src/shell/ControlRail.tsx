// ControlRail — the fixed left rail carrying ONLY the controls that drive the simulation, stacked
// one above the other in labelled sections. Nothing here inspects or edits the organism.

import type { SimState, SaveMeta, Command } from "../types";
import type { ViewMode } from "../view";
import { TransportSection } from "./rail/TransportSection";
import { PopulationSection } from "./rail/PopulationSection";
import { SpawnSection } from "./rail/SpawnSection";
import { LibrarySection } from "./rail/LibrarySection";
import { ViewSection } from "./rail/ViewSection";
import { SessionSection } from "./rail/SessionSection";

export interface RailView {
  active: boolean; // true only on the Town tab
  mode: ViewMode;
  onMode: (m: ViewMode) => void;
  labels: boolean;
  onLabels: (v: boolean) => void;
  follow: boolean;
  onFollow: (v: boolean) => void;
  hasSelection: boolean;
}

export function ControlRail({
  width,
  state,
  saves,
  command,
  error,
  view,
}: {
  width: number;
  state: SimState;
  saves: SaveMeta[];
  command: (cmd: Command) => Promise<unknown>;
  error: string | null;
  view: RailView;
}) {
  return (
    <div className="control-rail" style={{ width }}>
      {error && <div className="rail-err">{error}</div>}
      <TransportSection state={state} command={command} />
      <PopulationSection state={state} command={command} />
      <SpawnSection state={state} command={command} />
      <LibrarySection />
      <ViewSection {...view} />
      <SessionSection saves={saves} command={command} />
    </div>
  );
}

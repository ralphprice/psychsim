// ControlRail — the fixed left rail carrying ONLY the controls that drive the simulation. In
// Phase 0 it is an empty, resizable, persisted container; Phase 1 fills it with the stacked
// sections (transport / population / spawn / library / view / session).

import type { ReactNode } from "react";

export function ControlRail({ width, children }: { width: number; children?: ReactNode }) {
  return (
    <div className="control-rail" style={{ width }}>
      {children}
    </div>
  );
}

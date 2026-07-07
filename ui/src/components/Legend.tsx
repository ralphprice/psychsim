// Legend — the drive colour key, floating over the stage.

import { DRIVES } from "../types";
import { DRIVE_COLOUR } from "../theme";

export function Legend() {
  return (
    <div className="legend">
      <b>drive</b>
      {DRIVES.map((d) => (
        <div key={d}>
          <span className="sw" style={{ background: DRIVE_COLOUR[d] }} />
          {d}
        </div>
      ))}
    </div>
  );
}

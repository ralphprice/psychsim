// GridBackground — the fast top-down grid: terrain, buildings, props. Drawn once
// per town (memoised); the live people ride on top in a separate overlay.

import { memo } from "react";
import type { TownGeometry } from "../types";
import { GRID_CELL, TERRAIN_COLOUR, BUILDING_COLOUR } from "../theme";

function GridBackgroundImpl({ town }: { town: TownGeometry }) {
  const cell = GRID_CELL;
  const W = town.cols * cell;
  const H = town.rows * cell;
  return (
    <svg className="bg" width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
      {town.terrain?.map((row, y) =>
        row.map((t, x) => (
          <rect
            key={`t${x}-${y}`}
            x={x * cell}
            y={y * cell}
            width={cell}
            height={cell}
            fill={TERRAIN_COLOUR[t] ?? "#cfd8c8"}
          />
        )),
      )}
      {town.buildings.map((b) => (
        <rect
          key={b.place}
          x={b.x * cell}
          y={b.y * cell}
          width={b.w * cell}
          height={b.h * cell}
          fill={BUILDING_COLOUR[b.kind] ?? "#bbb"}
          stroke="#5a4030"
          strokeWidth={1.2}
          rx={2}
        />
      ))}
      {town.props.map((p, i) => (
        <circle
          key={`pr${i}`}
          cx={p.x * cell + cell / 2}
          cy={p.y * cell + cell / 2}
          r={cell * 0.18}
          fill="#4f7a3f"
        />
      ))}
    </svg>
  );
}

export const GridBackground = memo(GridBackgroundImpl);

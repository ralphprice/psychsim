// A ViewModel unifies the two backgrounds behind one coordinate space, so the
// live people overlay is positioned the same way regardless of which is shown.
//
//  - grid view: world = cols*GRID_CELL square; a tile centres at (x+0.5)*cell.
//  - plan view: world = plan.width x plan.height; a tile centres at
//    pad + x*cell + cell/2  — exactly render_settlement_plan's own mapping, the
//    one the batch watchable-town renderer uses to drop its dots.

import type { TownGeometry, PlanView } from "./types";
import { GRID_CELL } from "./theme";

export type ViewMode = "grid" | "plan";

export interface ViewModel {
  mode: ViewMode;
  W: number;
  H: number;
  /** tile (x, y) -> pixel centre in world space */
  tileToPx: (x: number, y: number) => [number, number];
}

export function gridViewModel(town: TownGeometry): ViewModel {
  const cell = GRID_CELL;
  return {
    mode: "grid",
    W: town.cols * cell,
    H: town.rows * cell,
    tileToPx: (x, y) => [x * cell + cell / 2, y * cell + cell / 2],
  };
}

export function planViewModel(plan: PlanView): ViewModel {
  const { cell, pad } = plan;
  return {
    mode: "plan",
    W: plan.width,
    H: plan.height,
    tileToPx: (x, y) => [pad + x * cell + cell / 2, pad + y * cell + cell / 2],
  };
}

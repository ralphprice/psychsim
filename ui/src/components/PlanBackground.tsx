// PlanBackground — the designed "glass-roof" plan view. The SVG is rendered
// server-side by sim_viz.floorplan.render_settlement_plan (the picture IS the
// model), so we inject it verbatim and let the live people overlay ride on top
// using the same cell/pad mapping the server drew it with.

import { memo } from "react";
import type { PlanView } from "../types";

function PlanBackgroundImpl({ plan }: { plan: PlanView }) {
  return (
    <div
      className="bg plan-bg"
      style={{ width: plan.width, height: plan.height }}
      // trusted: this SVG comes from our own sim server, not user input
      dangerouslySetInnerHTML={{ __html: plan.svg }}
    />
  );
}

export const PlanBackground = memo(PlanBackgroundImpl);

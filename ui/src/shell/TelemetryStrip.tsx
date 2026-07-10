// TelemetryStrip — the signature element: a full-width monospace readout of the sim's ACTUAL
// state, pinned above the tab bar. `●LIVE` (phosphor) when running, `○IDLE` (faint) when paused.
// It is true at a glance, which is what a researcher watching a long life-course needs.

import type { SimState } from "../types";

const BASE_INTERVAL = 0.25; // server default seconds/step; speed is a multiplier of this

export function TelemetryStrip({ state }: { state: SimState }) {
  const pop = Object.keys(state.people).length;
  const speed = state.interval ? BASE_INTERVAL / state.interval : 1;
  return (
    <div className="telemetry" role="status" aria-live="polite">
      <span className="brand">PSYCHSIM</span>
      {state.playing ? <span className="live">●LIVE</span> : <span className="idle">○IDLE</span>}
      <span><span className="tk">t</span> <b>{state.clock}</b></span>
      <span><span className="tk">tick</span> <b>{state.step.toLocaleString()}</b></span>
      <span><span className="tk">pop</span> <b>{pop}</b></span>
      <span><span className="tk">speed</span> <b>{speed.toFixed(2)}×</b></span>
      {state.seed != null && <span><span className="tk">seed</span> <b>{state.seed}</b></span>}
      {state.version && <b title="substrate seed version">{state.version}</b>}
    </div>
  );
}

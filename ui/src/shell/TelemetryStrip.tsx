// TelemetryStrip — the signature element: a full-width monospace readout of the sim's ACTUAL
// state, pinned above the tab bar. `●LIVE` (phosphor) when running, `○IDLE` (faint) when paused.
// Shows the sim wall-clock ABSOLUTE date and ELAPSED duration with equal prominence — elapsed is the
// number that maps onto developmental age and the 1/n plasticity schedule. The ☀/☾ symbol is a
// CLOCK read-out (the substrate has no diurnal coupling), never a behaviour-state indicator.

import type { SimState } from "../types";
import { formatSimDate, formatElapsed, isDaytime } from "./clock";

export function TelemetryStrip({ state }: { state: SimState }) {
  const pop = Object.keys(state.people).length;
  const speed = state.speed ?? (state.interval ? 0.25 / state.interval : 1);
  const tick = state.tick ?? state.step;
  const day = isDaytime(state.sim_time);
  return (
    <div className="telemetry" role="status" aria-live="polite">
      <span className="brand">PSYCHSIM</span>
      <span
        className="daynight"
        title={day ? "day (sim clock)" : "night (sim clock)"}
        aria-label={day ? "day" : "night"}
      >
        {day ? "☀" : "☾"}
      </span>
      {state.playing ? <span className="live">●LIVE</span> : <span className="idle">○IDLE</span>}
      <b className="tel-date" title="sim date / time">
        {formatSimDate(state.sim_time)}
      </b>
      <b className="tel-elapsed" title="elapsed (maps to developmental age)">
        {formatElapsed(state.elapsed_hours)}
      </b>
      <span>
        <span className="tk">tick</span> <b>{tick.toLocaleString()}</b>
      </span>
      <span>
        <span className="tk">pop</span> <b>{pop}</b>
      </span>
      <b>{speed.toFixed(2)}×</b>
      {state.version && <b title="substrate seed version">{state.version}</b>}
    </div>
  );
}

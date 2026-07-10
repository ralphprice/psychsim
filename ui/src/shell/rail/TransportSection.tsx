// TransportSection — the only filled control in the rail: play/pause, speed, and a mono readout.
import type { SimState, Command } from "../../types";

const BASE_INTERVAL = 0.25; // server default seconds/step; speed is a multiplier of this

export function TransportSection({
  state,
  command,
}: {
  state: SimState;
  command: (cmd: Command) => Promise<unknown>;
}) {
  const speed = state.interval ? BASE_INTERVAL / state.interval : 1;
  const setSpeed = (mult: number) => command({ cmd: "speed", interval: BASE_INTERVAL / mult });
  return (
    <section className="rail-section">
      <div className="rail-eyebrow">Transport</div>
      <button
        className={"rail-primary" + (state.playing ? " running" : "")}
        onClick={() => command({ cmd: state.playing ? "pause" : "play" })}
      >
        {state.playing ? "❚❚ Pause" : "▶ Start"}
      </button>
      <div className="rail-two-up">
        <button onClick={() => setSpeed(speed / 2)}>« slower</button>
        <button onClick={() => setSpeed(speed * 2)}>faster »</button>
      </div>
      <div className="rail-readout">
        <span>speed</span>
        <b>{speed.toFixed(2)}×</b>
      </div>
    </section>
  );
}

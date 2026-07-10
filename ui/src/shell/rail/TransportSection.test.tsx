import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import type { SimState } from "../../types";

// Mock the whole api surface useSim talks to. getState is controllable so we can simulate the
// server flipping `playing`; sendCommand is a spy so we can see exactly what the button sends.
const state = (playing: boolean): SimState => ({
  clock: "Mon 00:00", minutes: 0, step: playing ? 5 : 0, experiment: false,
  subjects: 0, background: 0, people: {}, playing, interval: 0.25,
});
let current = state(false);
const sendCommand = vi.fn(async (_cmd: unknown) => ({ ok: true }));
vi.mock("../../api", () => ({
  getTown: vi.fn(async () => ({ cols: 1, rows: 1, cell: 1, buildings: [], props: [] })),
  getPlan: vi.fn(async () => null),
  getState: vi.fn(async () => current),
  getSaves: vi.fn(async () => []),
  sendCommand: (cmd: unknown) => sendCommand(cmd),
}));

import { useSim } from "../../hooks/useSim";
import { TransportSection } from "./TransportSection";

function Harness() {
  const { state, command } = useSim();
  return <TransportSection state={state} command={command} />;
}

describe("Transport pause bug — full client flow (poll -> button -> command)", () => {
  beforeEach(() => {
    current = state(false);
    sendCommand.mockClear();
  });

  it("shows Start when paused and Pause when the server reports playing", async () => {
    render(<Harness />);
    // first poll: paused
    await waitFor(() => expect(screen.getByRole("button", { name: /Start/ })).toBeInTheDocument());
    // server begins playing -> the poll must flip the button to Pause
    current = state(true);
    await waitFor(() => expect(screen.getByRole("button", { name: /Pause/ })).toBeInTheDocument());
  });

  it("sends pause (not play) when the sim is playing — the reported inert-pause case", async () => {
    current = state(true);
    render(<Harness />);
    await waitFor(() => expect(screen.getByRole("button", { name: /Pause/ })).toBeInTheDocument());
    fireEvent.click(screen.getByRole("button", { name: /Pause/ }));
    expect(sendCommand).toHaveBeenCalledWith({ cmd: "pause" });
  });

  it("sends play when the sim is paused", async () => {
    current = state(false);
    render(<Harness />);
    await waitFor(() => expect(screen.getByRole("button", { name: /Start/ })).toBeInTheDocument());
    fireEvent.click(screen.getByRole("button", { name: /Start/ }));
    expect(sendCommand).toHaveBeenCalledWith({ cmd: "play" });
  });
});

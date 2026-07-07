// useSim — owns all talk to psychsim_server.py: loads the static geometry once,
// polls live state on an interval, and exposes typed control commands.

import { useCallback, useEffect, useRef, useState } from "react";
import { getTown, getPlan, getState, getSaves, sendCommand } from "../api";
import type { CommandResult } from "../api";
import type { TownGeometry, PlanView, SimState, SaveMeta, Command } from "../types";

const POLL_MS = 200;
const UNREACHABLE = "Cannot reach the server. Is psychsim_server.py running?";

export interface Sim {
  town: TownGeometry | null;
  plan: PlanView | null;
  state: SimState;
  saves: SaveMeta[];
  error: string | null;
  reloadGeometry: () => void;
  command: (cmd: Command) => Promise<CommandResult>;
}

const EMPTY_STATE: SimState = {
  clock: "—",
  minutes: 0,
  step: 0,
  experiment: false,
  subjects: 0,
  background: 0,
  people: {},
  playing: false,
  interval: 0.25,
};

export function useSim(): Sim {
  const [town, setTown] = useState<TownGeometry | null>(null);
  const [plan, setPlan] = useState<PlanView | null>(null);
  const [state, setState] = useState<SimState>(EMPTY_STATE);
  const [saves, setSaves] = useState<SaveMeta[]>([]);
  const [error, setError] = useState<string | null>(null);

  const reloadGeometry = useCallback(() => {
    getTown().then(setTown).catch(() => setError(UNREACHABLE));
    getPlan().then(setPlan).catch(() => setError(UNREACHABLE));
  }, []);
  const refreshSaves = useCallback(() => {
    getSaves().then(setSaves).catch(() => {});
  }, []);

  // load geometry + saves once
  useEffect(() => {
    reloadGeometry();
    refreshSaves();
  }, [reloadGeometry, refreshSaves]);

  // poll live state
  useEffect(() => {
    let alive = true;
    const tick = () =>
      getState()
        .then((s) => {
          if (!alive) return;
          setState(s);
          setError(null);
        })
        .catch(() => alive && setError(UNREACHABLE));
    tick();
    const id = setInterval(tick, POLL_MS);
    return () => {
      alive = false;
      clearInterval(id);
    };
  }, []);

  // respawn/load replace the whole town, so pull fresh geometry after they land
  const geomPending = useRef(false);
  const command = useCallback(
    async (cmd: Command) => {
      const res = await sendCommand(cmd);
      if ((cmd.cmd === "respawn" || cmd.cmd === "load") && !geomPending.current) {
        geomPending.current = true;
        // let the server rebuild/swap before re-fetching geometry
        setTimeout(() => {
          reloadGeometry();
          geomPending.current = false;
        }, 150);
      }
      if (cmd.cmd === "save" || cmd.cmd === "load" || cmd.cmd === "delete_save") {
        refreshSaves();
      }
      return res;
    },
    [reloadGeometry, refreshSaves],
  );

  return { town, plan, state, saves, error, reloadGeometry, command };
}

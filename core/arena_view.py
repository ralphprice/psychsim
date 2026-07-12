"""arena_view.py -- JSON-serializable views over the Arena (core/arena.py) for the server + UI.

Read-only listing of DEFINED content (environments, sources) plus a run-and-serialize entry point.
This is the seam between the ARENA tab and the already-built, already-tested `arena.run_arena`; it
composes an `ArenaSpec` from the UI's choices and serialises the resulting `ArenaTrace`. It never
reimplements the run.

Honesty (mirrors arena.py's own wall, and the Arena-UI spec section 1):
  * ENVIRONMENTS ARE THEIR PRESENT THINGS. `environments()` lists each `MicroEnv`'s present Thing ids
    and its STRUCTURAL `escape` count (len(present)) -- never a "stressful"/valence tag. A hollow
    label the substrate can't instantiate is a lie, so the UI can only offer what `MICRO_ENVS` defines.
  * TEMPERAMENT IS PARAMETERS, NOT OUTCOME NAMES. A slot's temperament is exposed as the GAIN DIMS
    (THREAT/SEEKING/...), the same vocabulary `intact_seed` uses, default 0.5 = intact. No
    outcome-named presets (the removed typical/fearless dropdown); the researcher sets circuits, the
    disposition is MEASURED from what emerges.
  * RELATIONSHIPS EMERGE, they are not a per-slot control. There are no named relationship
    configurations DEFINED yet, so `relationships()` returns the honest empty + the emergent
    substrate (shared_hours + seeded encounter history via the matrices), never a hollow dropdown.
  * DETERMINISM PRESERVED. The `seed` flows straight through to `run_arena`; no unseeded path.

Known limits surfaced by wiring the real core (flagged to the design session, NOT worked around):
  * `run_arena` returns only the `ArenaTrace` (per-episode acts/max_act/drift/strain) and discards
    the agents, so full Town-style mind/memory/standing inspection is not available here -- the trace
    supports per-agent TRAJECTORIES (act sequence, max-activation, drift) + per-pair strain +
    viability, which is what this view serialises. Deep per-agent inspection would need the trace
    extended to capture per-episode mind snapshots -- a reviewed core change, not done here.
  * Sampled sex/physical are internal to the agents `run_arena` builds; not in the trace, so not
    surfaced yet (same trace-extension).
"""
from __future__ import annotations
from typing import Dict, List, Optional

import arena as _arena
from affective_engine import TraitSeed
from agent_bank import AgentBank

# The temperament GAIN dimensions a slot can set -- parameters, never outcome names. Same vocabulary
# as intact_seed; default 0.5 == intact/neutral (so an unset slot is exactly the intact reference).
GAIN_DIMS: List[str] = ["THREAT", "ANXIETY", "SEEKING", "FRUSTRATION",
                        "CARE", "SOCIAL_LOSS", "CONTROL", "INSTRUMENTAL_CONTROL"]

# The instrument's design bound (S12.2): run_arena raises ValueError outside 2-5. Surfaced so the UI
# can enforce min 2 / max 5 rather than discover it at run.
ROSTER_MIN, ROSTER_MAX = 2, 5


def environments() -> List[dict]:
    """The DEFINED micro-environments: each is its present Thing ids + the structural escape count."""
    return [{"id": e.name, "note": e.note,
             "present": [t.id for t in e.present], "escape": e.escape}
            for e in _arena.MICRO_ENVS.values()]


def sources(bank: Optional[AgentBank] = None) -> dict:
    """What a roster slot can be sourced from (S12.2), plus the temperament parameter vocabulary."""
    return {"kinds": ["newborn", "grown", "banked"],
            "gain_dims": GAIN_DIMS,                 # temperament = parameters (default 0.5 = intact)
            "default_grow_years": 18.0,
            "banked_ids": bank.ids() if bank is not None else []}


def relationships() -> dict:
    """The DEFINED relationship configurations. None are named/defined yet -- relationships emerge
    from shared encounter history through the matrices, so the honest answer is the emergent
    substrate, never a hollow preset. Adding named configs is grounded matrix content (design-session
    reviewed); until then the UI exposes shared_hours + seeded history, not a relationship dropdown."""
    return {"defined": [],
            "substrate": "shared_hours (co-located fraction) + seeded encounter history via the "
                         "social/group matrices; bonds emerge, never assigned",
            "note": "named relationship configurations (kin/peer/co-worker/classmate) are grounded "
                    "matrix content, added deliberately -- flagged to the design session, not typed here"}


def roster_bounds() -> dict:
    return {"min": ROSTER_MIN, "max": ROSTER_MAX,
            "why": "the Arena's design scale (S12.2): few subjects, high detail. run_arena enforces it."}


def _seed_from(slot: dict) -> TraitSeed:
    """Build the slot's temperament TraitSeed. If the UI set gain dims, use them (parameters);
    otherwise the intact reference (all gains 0.5)."""
    gains = slot.get("gains")
    if gains:
        g = {d: float(gains.get(d, 0.5)) for d in GAIN_DIMS}
        return TraitSeed(name=str(slot.get("slot_id", "slot")), gains=g)
    return _arena.intact_seed(str(slot.get("slot_id", "intact")))


def _build_spec(payload: dict, bank: Optional[AgentBank]) -> "_arena.ArenaSpec":
    slots = []
    for s in payload.get("slots", []):
        src = s.get("source", "newborn")
        slot = _arena.Slot(slot_id=str(s.get("slot_id", f"slot{len(slots)}")),
                           source=src, age=float(s.get("age", 0.5)),
                           seed=_seed_from(s), grow_years=float(s.get("grow_years", 18.0)))
        if src == "banked":
            if bank is None or not s.get("bank_id"):
                raise ValueError(f"banked slot '{slot.slot_id}' needs a bank + bank_id")
            slot.bank = bank
            slot.bank_id = str(s["bank_id"])
        slots.append(slot)
    return _arena.ArenaSpec(micro_env=str(payload["micro_env"]), slots=slots,
                            seed=int(payload.get("seed", 0)),
                            shared_hours=float(payload.get("shared_hours", 3.0)))


def run(payload: dict, bank: Optional[AgentBank] = None) -> dict:
    """Compose an ArenaSpec from the UI payload, run it (run_arena, synchronous ~seconds), and
    serialise the ArenaTrace. run_arena's 2-5 guard raises ValueError, surfaced to the caller."""
    spec = _build_spec(payload, bank)
    trace = _arena.run_arena(spec, childhood_years=float(payload.get("childhood_years", 18.0)))
    return _serialize(spec, trace)


def _serialize(spec, trace) -> dict:
    ids = [s.slot_id for s in spec.slots]
    return {
        "spec": {"micro_env": spec.micro_env, "seed": spec.seed, "shared_hours": spec.shared_hours,
                 "escape": _arena.MICRO_ENVS[spec.micro_env].escape,
                 "slots": [{"slot_id": s.slot_id, "source": s.source, "age": s.age} for s in spec.slots]},
        "agent_ids": ids,
        "records": trace.records,                        # per-episode: acts/max_act/drift (per agent), strain (per pair)
        "act_counts": dict(trace.act_counts()),
        "peak_activation": trace.peak_activation(),      # the saturation signal
        "viable": trace.viable(),                        # no agent driven into persistent saturation
        "settled": trace.settled(),                      # Regime-B: tail-settled, not oscillating
    }

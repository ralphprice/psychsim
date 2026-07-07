"""
behaviour.py (substrate) -- behaviour selection over the LIVE substrate (8b.3).

Appendix F says behaviour is basal-ganglia action selection: candidate tendencies compete via
accumulation-to-threshold; dopamine sets the gain; the executive (PFC->STN) raises the hold. In
8b.3 this reads its parameters FROM the substrate, so behaviour EMERGES from circuit activity,
not a coded arbiter and not a separate age model:

  * the Go drive is the reward/approach circuits' activation, with the gain set by DOPAMINE =
    the SNc/VTA output (engine.neuromod_output('DA'));
  * the hold is the executive circuits' activation feeding STN (the vlPFC/preSMA->STN brake).

The developmental gradient falls out of the seed's own developmental_online_age: reward circuits
are online early, the prefrontal brake late -- so a young agent has a weaker hold and acts more
readily on reward. Nothing here references what a circuit "is" beyond its anatomical domain and
neurotransmitter (both seed data); no rule maps a situation to a behaviour.

Standalone read-out over the substrate; the legacy engine is untouched (retirement is 8b.4).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

from . import params
from .engine import SubstrateEngine

STN_HOLD_GAIN = 1.5        # SCAFFOLD executive/STN hold -> raised decision threshold
GO_THRESHOLD = 1.0        # SCAFFOLD accumulation bound
GO_LEAK = 0.1             # SCAFFOLD accumulator leak
GO_DT = 0.2              # SCAFFOLD
GO_MAX_STEPS = 200       # SCAFFOLD


def _mean_live(engine: SubstrateEngine, domain: str) -> float:
    m = engine.model
    acts = [engine.activity(cid) for cid, c in m.circuits.items()
            if c.domain == domain and engine.live_circuit.get(cid, False)]
    return sum(acts) / len(acts) if acts else 0.0


def go_drive(engine: SubstrateEngine) -> float:
    """The reward/approach tendency's strength: reward-circuit activation, with the gain set by
    dopamine (the SNc/VTA output). This is the 'act on reward' pull."""
    reward = _mean_live(engine, "reward_approach")
    da = engine.neuromod_output("DA")            # dopamine sets the Go gain (F.4)
    return reward * (0.5 + da)


def executive_hold(engine: SubstrateEngine) -> float:
    """The restraint: the online executive circuits feeding the STN brake. Grows with age as
    the prefrontal circuits come online (seed developmental_online_age)."""
    return _mean_live(engine, "executive")


@dataclass
class Behaviour:
    action: str                  # "approach" (acted on reward) | "restrain" (held)
    steps: int                   # accumulation steps (fast = strong pull / weak hold)
    go: float
    hold: float


def select_behaviour(engine: SubstrateEngine) -> Behaviour:
    """Run the BG accumulation: the reward Go drive accumulates against a threshold raised by
    the executive/STN hold. If it crosses, the agent ACTS on reward (approach); if the hold
    holds it off within the window, the agent RESTRAINS. Emergent -- no coded rule."""
    go = go_drive(engine)
    hold = executive_hold(engine)
    threshold = GO_THRESHOLD + STN_HOLD_GAIN * hold
    acc = 0.0
    for step in range(1, GO_MAX_STEPS + 1):
        acc += GO_DT * (go - GO_LEAK * acc)
        if acc >= threshold:
            return Behaviour("approach", step, go, hold)
    return Behaviour("restrain", GO_MAX_STEPS, go, hold)

"""
agent.py (substrate) -- experience and value on the LIVE substrate (8b.2).

The ONE-PLASTICITY principle (design-session ruling): the substrate's DA-gated BCM plasticity
IS the learning mechanism -- there is NO separate temporal-difference learner. Concretely:

  * The reward-prediction / dopamine signal IS `engine.neuromod_output("DA")` -- the live VTA/
    SNc activation the substrate already reads. `reward_signal()` returns exactly that.
  * A primary reinforcer drives VTA/SNc via the seed's INNATE reward links (e.g. the input
    edge IN-GUST:sweet -> VTA); the DA burst then gates BCM consolidation of whatever cue
    pathways were co-active (their eligibility traces). This is how a neutral cue acquires
    value -- the biological rule, not a coded update.
  * ANTICIPATORY VALUE is a READ-OUT of the strengthened pathways: present the cue alone and
    measure how strongly it now drives the reward/value circuits. It is not a maintained V.

Appendix C's value function and RPE (delta = r + gamma*V' - V) are the functional-level
DESCRIPTION of what this biological plasticity computes -- not a second mechanism. If a target
phenomenon fails to emerge from the rule, that is a validation finding to surface, never
something to paper over with a parallel learner.
"""

from __future__ import annotations
from typing import Dict, Iterable, Optional

from .engine import SubstrateEngine

# reward/value circuits the anticipatory-value read-out samples (v7 ids)
REWARD_READOUT = ("OFC", "NAc-core", "NAc-shell", "VTA")


class SubstrateAgent:
    """A thin wrapper that lives an agent's experience on the substrate. It adds NO learning
    of its own -- it injects inputs, steps the engine (whose DA-gated BCM learns), and reads
    value out. Selection over the substrate will build on this (later in 8b)."""

    def __init__(self, engine: Optional[SubstrateEngine] = None, age_years: float = 5.0):
        self.engine = engine or SubstrateEngine(age_years=age_years)

    def reward_signal(self) -> float:
        """The dopaminergic reward-prediction signal -- IS the VTA/SNc circuit output (the
        design's `delta = neuromod_output('DA')`), not a separately computed TD error."""
        return self.engine.neuromod_output("DA")

    def _apply(self, inputs: Dict[str, float]) -> None:
        eng = self.engine
        for key, drive in inputs.items():
            if key in eng.model.circuits:
                eng.inject(key, drive)
            else:
                eng.inject_channel(key, drive)

    def experience(self, inputs: Dict[str, float], ticks: int = 12) -> float:
        """Live one experience: present `inputs` (cue channels/circuits + any reinforcer,
        whose innate link drives VTA), run the substrate so its DA-gated BCM consolidates the
        co-active eligible pathways. Returns the reward signal seen. No coded learning."""
        self.engine.clear_inputs()
        self._apply(inputs)
        self.engine.settle(ticks)
        return self.reward_signal()

    def anticipatory_value(self, cue: Dict[str, float],
                           readout: Iterable[str] = REWARD_READOUT, ticks: int = 25) -> float:
        """The learned anticipatory value of a cue: present the cue ALONE and read how strongly
        it now drives the reward/value circuits. A read-out of the strengthened pathways."""
        eng = self.engine
        eng.clear_inputs()
        self._apply(cue)
        eng.settle(ticks)
        cids = [c for c in readout if c in eng.model.circuits]
        val = sum(eng.activity(c) for c in cids) / len(cids) if cids else 0.0
        eng.clear_inputs()
        return val

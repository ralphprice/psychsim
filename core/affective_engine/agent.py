"""
agent.py -- the affective agent: an episodic memory on the category-free neural substrate.

Behaviour is the substrate's emergent social act: a situation's perturbation pattern fires the
agent's own developing `engine` (core/substrate) and the basal-ganglia race resolves the act
(`social_act`). No outcome categories are selected as primitives or fed back; the categories are
computed only as OBSERVER read-outs (observer.py). The Panksepp drive-engine that once backed
this agent was RETIRED in the substrate-social phase (Part 6 step 3e / stage 5) -- the substrate
is now the sole engine.

The agent holds: its developing substrate `engine`, the temperament `gains` (read by the observer
read-out), and the episodic memory.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional

from .core import TraitSeed
from .memory import MemoryStream

from substrate.engine import SubstrateEngine
from substrate.model import load_substrate
from substrate.social import respond_to_substrate, resting_baseline
from substrate.seeding import seed_substrate

# the substrate STRUCTURE is immutable during a run, so all agents share one read-only model;
# each agent's developing STATE lives on its own engine (proven no-bleed, S8.5).
_SUBSTRATE_MODEL = load_substrate()


@dataclass
class AffectiveAgent:
    """A situated agent on the category-free substrate: its own developing substrate engine, its
    temperament gains, and an episodic memory. Behaviour is the substrate's emergent social act
    (`social_act`); the legacy Panksepp engine is retired."""
    seed: TraitSeed
    use_memory: bool = True
    # retained for API compatibility; the substrate is seeded DETERMINISTICALLY from the seed's
    # gains (seed_substrate), so this no longer affects the agent (the Panksepp brain it once
    # seeded is retired).
    temperament_seed: Optional[int] = None
    gain: Dict[str, float] = field(init=False)
    memory: MemoryStream = field(init=False)
    # display slot only: the last emergent ACTION the agent took (a substrate behaviour like
    # "approach"/"aggress"), set by the world loop for inspection. NOT an outcome category.
    dominant: Optional[str] = field(init=False, default=None)

    def __post_init__(self) -> None:
        self.engine = SubstrateEngine(_SUBSTRATE_MODEL, age_years=0.5)
        seed_substrate(self.engine, self.seed.gains)     # temperament -> substrate biases
        self._rest_baseline = resting_baseline(_SUBSTRATE_MODEL, self.engine.age_years,
                                               self.engine.throttle)
        self.gain = dict(self.seed.gains)
        self.memory = MemoryStream()

    def adopt_engine(self, engine: SubstrateEngine) -> None:
        """Place an already-developed substrate (e.g. a library adult restored from the bank) into
        this agent, replacing its own engine and refreshing the cached resting baseline for the new
        connectome and age. The developed weights are dropped in as-is (restored-never-edited)."""
        self.engine = engine
        self._rest_baseline = resting_baseline(_SUBSTRATE_MODEL, engine.age_years, engine.throttle)

    def social_act(self, appraisal, age_years: Optional[float] = None):
        """The agent's emergent SOCIAL ACT on the substrate: the situation's perturbation pattern
        fires its circuits and the basal-ganglia race resolves the act. The engine develops
        through the moment. Returns a SocialBehaviour (`.behaviour`) the world consumers use."""
        if age_years is not None and age_years >= 0.5:
            self.engine.set_age(age_years)
        return respond_to_substrate(self.engine, appraisal, baseline=self._rest_baseline)

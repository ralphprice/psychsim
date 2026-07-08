"""
agent.py -- the affective agent: an episodic memory on a Panksepp brain.

HONESTY MIGRATION #2 (MASTER Phase 6 / "8b.4"): the outcome-category NETWORK SCORER that used
to live here -- score each category-named Network by circuit activation x the seed's `access`
reachability, then a hysteretic argmax over the outcome categories -- has been REMOVED. It was
the encoded-answer path (behaviour selected among outcome-category primitives). Behaviour now
comes from the emergent Panksepp substrate (`self.brain`, drives.py) via `respond_to_appraisal`;
the outcome categories are computed only as OBSERVER read-outs (observer.py), never selected as
primitives and never fed back.

The agent holds: the Panksepp brain, the temperament `gains` (read by the observer read-out),
and the episodic memory. The Panksepp brain is itself interim-legacy -- its retirement onto the
circuit substrate (core/substrate) is a separate, parity-gated phase, not this cut.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional

from .core import TraitSeed
from .memory import MemoryStream

from substrate.engine import SubstrateEngine
from substrate.model import load_substrate
from substrate.social import respond_to_substrate, resting_baseline

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
    temperament_seed: Optional[int] = None
    gain: Dict[str, float] = field(init=False)
    memory: MemoryStream = field(init=False)
    # display slot only: the last emergent ACTION the agent took (a substrate behaviour like
    # "approach"/"aggress"), set by the world loop for inspection. NOT an outcome category.
    dominant: Optional[str] = field(init=False, default=None)

    def __post_init__(self) -> None:
        self.engine = SubstrateEngine(_SUBSTRATE_MODEL, age_years=0.5)
        self._rest_baseline = resting_baseline(_SUBSTRATE_MODEL, self.engine.age_years)
        self.gain = dict(self.seed.gains)
        self.memory = MemoryStream()
        # interim-legacy: the Panksepp brain is still present while consumers are migrated onto
        # the substrate (staged retirement). Removed once nothing live reads `.brain`.
        import random as _r
        from .drives import brain_from_seed
        _rng = (_r.Random(self.temperament_seed)
                if self.temperament_seed is not None else _r.Random())
        self.brain = brain_from_seed(self.seed, _rng)

    def social_act(self, appraisal, age_years: Optional[float] = None):
        """The agent's emergent SOCIAL ACT on the substrate: the situation's perturbation pattern
        fires its circuits and the basal-ganglia race resolves the act. The engine develops
        through the moment. Returns a SocialBehaviour (`.behaviour`) the world consumers use."""
        if age_years is not None and age_years >= 0.5:
            self.engine.set_age(age_years)
        return respond_to_substrate(self.engine, appraisal, baseline=self._rest_baseline)

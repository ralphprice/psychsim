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


@dataclass
class AffectiveAgent:
    seed: TraitSeed
    use_memory: bool = True
    temperament_seed: Optional[int] = None
    gain: Dict[str, float] = field(init=False)
    memory: MemoryStream = field(init=False)
    # display slot only: the last emergent ACTION the agent took (a Panksepp behaviour like
    # "approach"/"aggress"), set by the world loop for inspection. NOT an outcome category.
    dominant: Optional[str] = field(init=False, default=None)

    def __post_init__(self) -> None:
        import random as _r
        from .drives import brain_from_seed
        _rng = (_r.Random(self.temperament_seed)
                if self.temperament_seed is not None else _r.Random())
        self.brain = brain_from_seed(self.seed, _rng)
        self.gain = dict(self.seed.gains)
        self.memory = MemoryStream()

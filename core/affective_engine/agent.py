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
import random
from dataclasses import dataclass, field
from typing import Dict, Optional

from .core import TraitSeed
from .memory import MemoryStream
from .physical import sample_physical, vmhvl_reactivity

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
    # the per-agent seed (drawn from the world's seeded RNG). v10: it seeds this agent's PHYSICAL
    # endowment draw (E1, __post_init__) -- reproducible from the world seed, distinct per agent.
    # None -> the agent is physical-NEUTRAL (no seed, no fabricated physical): scan probes / demos
    # stay byte-unchanged. (The substrate itself is seeded deterministically from the seed's gains
    # via seed_substrate; this seed does not perturb it.)
    temperament_seed: Optional[int] = None
    gain: Dict[str, float] = field(init=False)
    memory: MemoryStream = field(init=False)
    # v10 physical endowment (E1): this agent's own physical traits + biological sex. Sampled for a
    # FRESH seeded agent; RELOADED verbatim for a banked adult (adopt_developed) -- restored-never-
    # edited. Empty/None for a physical-neutral (seedless) agent. A bearer property, not an outcome.
    physical: Dict[str, float] = field(init=False, default_factory=dict)
    sex: Optional[str] = field(init=False, default=None)
    # display slot only: the last emergent ACTION the agent took (a substrate behaviour like
    # "approach"/"aggress"), set by the world loop for inspection. NOT an outcome category.
    dominant: Optional[str] = field(init=False, default=None)

    def __post_init__(self) -> None:
        self.engine = SubstrateEngine(_SUBSTRATE_MODEL, age_years=0.5)
        seed_substrate(self.engine, self.seed.gains)     # temperament -> substrate biases
        # E1: this agent's physical endowment + sex, sampled FAITHFULLY from its own seeded RNG
        # (reproducible from the world seed, distinct per agent). A seedless agent stays physical-
        # neutral -- no fabricated physical.
        if self.temperament_seed is not None:
            phys = sample_physical(random.Random(self.temperament_seed))
            self.sex = phys.pop("sex")
            self.physical = phys
        # E5/E6: own strength + sex bias this agent's VMHvl reactivity (its response to provocation),
        # before the resting baseline is captured. A calibration on the attack circuit's competition;
        # it cannot fire aggression unprovoked (VMHvl's only input is provocation -- neutral-floor
        # guard). Physical-neutral -> gain 1.0 (no-op). Set on the OWN engine only (a self-effect).
        self._apply_physical_calibration()
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

    def adopt_developed(self, dev) -> None:
        """Place a fully banked adult (a DevelopedAgent) into this agent: its developed substrate AND
        its physical endowment + sex, RELOADED verbatim from the bank -- never re-sampled (restored-
        never-edited + banked-reproducibility). The single restore-into-mind path; use it in place of
        adopt_engine wherever a banked adult carries physical. A pre-v10 snapshot has no physical ->
        the adult restores physical-neutral (never fabricated) until the cache is regrown under v10."""
        self.physical = dict(getattr(dev, "physical", {}) or {})
        self.sex = getattr(dev, "sex", None)
        self.adopt_engine(dev.engine)
        # re-derive the E5/E6 VMHvl calibration from the RELOADED physical (a pure function of it, so
        # this reproduces the gain the adult grew with -- not a re-sample). The rest baseline is a
        # no-input measurement, so the gain (which scales input) does not change it; no re-capture.
        self._apply_physical_calibration()

    def _apply_physical_calibration(self) -> None:
        """Bias the OWN engine's VMHvl reactivity from this agent's physical endowment (E5/E6). Pure
        function of (physical, sex); a physical-neutral agent -> gain 1.0 (no-op)."""
        self.engine.set_reactivity("VMHvl", vmhvl_reactivity(self.physical, self.sex))

    def social_act(self, appraisal, age_years: Optional[float] = None):
        """The agent's emergent SOCIAL ACT on the substrate: the situation's perturbation pattern
        fires its circuits and the basal-ganglia race resolves the act. The engine develops
        through the moment. Returns a SocialBehaviour (`.behaviour`) the world consumers use."""
        if age_years is not None and age_years >= 0.5:
            self.engine.set_age(age_years)
        return respond_to_substrate(self.engine, appraisal, baseline=self._rest_baseline)

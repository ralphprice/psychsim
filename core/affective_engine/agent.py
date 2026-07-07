"""
agent.py -- the affective agent and its per-turn cycle.

The five-step cycle: appraise -> activate circuits -> score networks ->
arbitrate -> act. Both regulatory circuits (CONTROL, INSTRUMENTAL_CONTROL) are
computed after the impulsive circuits, because they are responses to the impulse
pressure those circuits generate. Arbitration is a hysteretic argmax.

Each agent owns an episodic MemoryStream. On meeting a situation the agent primes
its appraisal from similar past episodes (a learned expectation); with an empty
memory this is a no-op, so behaviour is unchanged until the agent has a history.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional

from .core import (Appraisal, Network, TraitSeed, LanguageActuator,
                   CIRCUITS, IMPULSIVE, DECAY, clamp,
                   stimulus_drives, default_catalogue)
from .memory import MemoryStream

# Arbitration constants
CONTROL_BOOST = 0.9      # conscience-control lifts governed networks
CONTROL_DAMP = 0.9       # conscience-control suppresses ungoverned networks
INSTR_GAINAMT = 0.9      # scale of instrumental-control modulation (via net.instr)
ACCESS_FLOOR = 0.35
INCUMBENT_STICK = 0.08
SETTLE_TICKS = 3


@dataclass
class AffectiveAgent:
    seed: TraitSeed
    actuator: LanguageActuator = field(default_factory=LanguageActuator)
    use_memory: bool = True
    temperament_seed: Optional[int] = None
    gain: Dict[str, float] = field(init=False)
    access: Dict[str, float] = field(init=False)
    activation: Dict[str, float] = field(init=False)
    catalogue: Dict[str, Network] = field(init=False)
    memory: MemoryStream = field(init=False)
    dominant: Optional[str] = field(init=False, default=None)

    def __post_init__(self) -> None:
        import random as _r
        from .drives import brain_from_seed
        _rng = _r.Random(self.temperament_seed) if self.temperament_seed is not None else _r.Random()
        self.brain = brain_from_seed(self.seed, _rng)
        self.gain = dict(self.seed.gains)
        self.access = dict(self.seed.access)
        self.catalogue = default_catalogue()
        self.memory = MemoryStream()
        self.reset_activation()

    def reset_activation(self) -> None:
        self.activation = {c: 0.0 for c in CIRCUITS}
        self.dominant = None

    # -- one tick ----------------------------------------------------------
    def tick(self, a: Appraisal) -> None:
        drives = stimulus_drives(a)
        for c, drive in drives.items():
            target = clamp(self.gain[c] * drive)
            self.activation[c] = DECAY * self.activation[c] + (1 - DECAY) * target

        impulse_pressure = max(self.activation[c] for c in IMPULSIVE)

        # CONTROL: conscience-linked, recruited by impulse pressure and more when
        # a goal is at stake (self-command in service of a considered end).
        control_drive = clamp(impulse_pressure * (0.5 + 0.5 * a.goal_relevance))
        control_target = clamp(self.gain["CONTROL"] * control_drive)
        self.activation["CONTROL"] = (
            DECAY * self.activation["CONTROL"] + (1 - DECAY) * control_target)

        # INSTRUMENTAL_CONTROL: cold, strategic; responds to impulse pressure to
        # regulate it, without the goal-conscience recruitment.
        instr_target = clamp(self.gain["INSTRUMENTAL_CONTROL"] * impulse_pressure)
        self.activation["INSTRUMENTAL_CONTROL"] = (
            DECAY * self.activation["INSTRUMENTAL_CONTROL"]
            + (1 - DECAY) * instr_target)

        self.dominant = self._arbitrate()

    def settle(self, a: Appraisal, ticks: int = SETTLE_TICKS) -> str:
        """Prime the appraisal from memory, then run several ticks so activations
        settle, and return the dominant network."""
        if self.use_memory:
            a = self.memory.prime(a)
        for _ in range(ticks):
            self.tick(a)
        return self.dominant

    # -- scoring and arbitration ------------------------------------------
    def network_score(self, net: Network) -> float:
        base = sum(w * self.activation[c] for c, w in net.weights.items())
        ctrl = self.activation["CONTROL"]
        if net.governance == "governed":
            base += CONTROL_BOOST * ctrl
        elif net.governance == "ungoverned":
            base -= CONTROL_DAMP * ctrl
        # instrumental control: net.instr says how this mode responds to cold
        # calculation (negative for reactive rage, positive for calculated
        # exploitation and cool competence).
        base += INSTR_GAINAMT * net.instr * self.activation["INSTRUMENTAL_CONTROL"]
        reach = ACCESS_FLOOR + (1 - ACCESS_FLOOR) * self.access[net.name]
        return max(0.0, base) * reach

    def _arbitrate(self) -> str:
        scores = {name: self.network_score(net)
                  for name, net in self.catalogue.items()}
        if self.dominant is not None:
            scores[self.dominant] += INCUMBENT_STICK
        return max(scores, key=scores.get)

    # -- convenience -------------------------------------------------------
    def respond(self, a: Appraisal) -> str:
        self.reset_activation()
        name = self.settle(a)
        return self.actuator.act(a, self.catalogue[name])

    def coactivation(self, net: Network) -> float:
        pos = {c: w for c, w in net.weights.items() if w > 0}
        if not pos:
            return 0.0
        num = sum(w * self.activation[c] for c, w in pos.items())
        return clamp(num / sum(pos.values()))

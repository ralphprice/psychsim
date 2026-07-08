"""
parallel_world.py -- N independent substrate instances in one shared world (Part 4 S8.5).

Each character is an INDEPENDENT substrate instance carrying its own per-slot settings. The
parallelism is honest **precisely because the substrates do not share state** -- the shared spawn
world gives them something to interact with and be measured in, but the substrates must not bleed,
or any effect (a throttle, a rearing) is confounded with cross-contamination.

Shared infrastructure for the Arena (Part 6 S12) and the scan controller (Part 4 S8): both draw
independent instances -- fresh newborns, system-grown adults, or banked adults (S11) -- into one
world. This module is the harness only; the rich substrate-social INTERACTION between instances is
the substrate-social phase (built next). Here the shared world is a read context and the guarantee
is INDEPENDENCE.

The SubstrateModel (the seed's circuits/connections) is immutable during a run -- engines hold
their own weights/activity -- so instances may share one model read-only while their STATE stays
per-instance. A test proves developing one instance never perturbs another.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from substrate.engine import SubstrateEngine
from substrate.model import load_substrate, SubstrateModel
from agent_bank import DevelopedAgent, AgentBank


@dataclass
class Instance:
    """One character slot: an independent developed agent + its per-slot settings (spawn source,
    age, throttle config, ...). The settings are the slot's, never shared with other slots."""
    instance_id: str
    agent: DevelopedAgent
    settings: Dict = field(default_factory=dict)

    @property
    def age_years(self) -> float:
        return self.agent.age_years


class ParallelWorld:
    """N independent substrate instances sharing one spawn world (S8.5). Instances develop
    independently; nothing couples one substrate's state to another's."""

    def __init__(self, model: Optional[SubstrateModel] = None,
                 world: Optional[Dict] = None):
        # shared, READ-ONLY structure (never mutated by a run); per-instance state lives on the
        # instances' own engines, so sharing this does not couple them.
        self.model = model or load_substrate()
        # the shared spawn world: what is present to interact with (perturbation patterns only,
        # never valences -- honesty carries into the Arena). A plain context here.
        self.world = dict(world or {})
        self.instances: Dict[str, Instance] = {}

    # -- spawning slots (S12.2 per-slot source/age) -----------------------
    def spawn_newborn(self, instance_id: str, age: float = 0.5,
                      settings: Optional[Dict] = None) -> Instance:
        agent = DevelopedAgent(engine=SubstrateEngine(self.model, age_years=age),
                               provenance={"source": "newborn", "spawn_age": age})
        return self._add(instance_id, agent, settings)

    def spawn_from_agent(self, instance_id: str, agent: DevelopedAgent,
                         settings: Optional[Dict] = None) -> Instance:
        """Place an already-GROWN agent (e.g. from a developmental run) into a slot."""
        return self._add(instance_id, agent, settings)

    def spawn_banked(self, instance_id: str, bank: AgentBank, bank_id: str,
                     settings: Optional[Dict] = None) -> Instance:
        """Re-instantiate a BANKED adult into a slot (S11) -- it resumes developing, not frozen.
        Restored, never edited: the bank hands back the grown state as-is."""
        agent = bank.restore(bank_id, self.model)
        return self._add(instance_id, agent, settings)

    def _add(self, instance_id: str, agent: DevelopedAgent,
             settings: Optional[Dict]) -> Instance:
        if instance_id in self.instances:
            raise ValueError(f"slot '{instance_id}' already occupied")
        inst = Instance(instance_id, agent, dict(settings or {}))
        self.instances[instance_id] = inst
        return inst

    # -- running them independently ---------------------------------------
    def step_all(self, ticks: int = 1) -> None:
        """Advance every instance one episode -- each on its OWN substrate. No cross-instance
        coupling: the loop touches one agent's engine at a time and shares no mutable state."""
        for inst in self.instances.values():
            inst.agent.engine.settle(ticks)

    def read_all(self, readout: Callable[[DevelopedAgent], object]) -> Dict[str, object]:
        """Collect a measured read-out per instance (the observer's per-character measurement)."""
        return {iid: readout(inst.agent) for iid, inst in self.instances.items()}

    def ids(self) -> List[str]:
        return list(self.instances.keys())

    def __len__(self) -> int:
        return len(self.instances)

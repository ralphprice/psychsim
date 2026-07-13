"""
agent_bank.py -- the developed-agent bank (Part 6 S11).

Snapshot an agent's COMPLETE developed state -- the sculpted substrate connectome, all four
matrices (social / environmental / group / self-reflection), the interoceptive state vector, its
age, and provenance -- persist it, and re-instantiate it later to keep developing. The primary
capability the project needs to spawn GROWN adults; the Arena (S12) and the scan controller
(Part 4 S8) are its consumers.

THE HONESTY RULE (S11.5, load-bearing):
  * GROWN AND BANKED, NEVER FABRICATED. The only way a state enters the bank is `bank(agent, ...)`
    on an agent that a run actually GREW. There is no path that assigns adult weights directly --
    that would hand-author a developed state (the multi-seed stipulation problem, one level up).
  * RESTORED, NEVER EDITED. `restore(...)` rebuilds the exact banked state to RESUME; it exposes no
    hook to adjust developed weights before dropping the agent in. Snapshot / restore only.

Re-instantiation is pause-and-resume, NOT freeze (S11.4): the restored substrate keeps its
`exp_count`, so plasticity continues under the 1/n experience-decreasing schedule (Part 5 S10.1) --
at an adult age it changes slowly, exactly as it would have unbanked.
"""

from __future__ import annotations
import dataclasses
import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from substrate.engine import SubstrateEngine
from substrate.model import load_substrate, SubstrateModel
from sim_world.relations import RelationshipMatrix, RelationshipSlot
from sim_world.environment_matrix import EnvironmentMatrix, Bond
from sim_world.group_matrix import GroupMatrix, Membership
from sim_world.self_reflection import SelfReflection
from affective_engine.learning import ValueLearner, CueValue
from affective_engine.interocept import StateVector

SNAPSHOT_VERSION = 1
AUTO_BANK_AGES = (18.0, 25.0, 40.0)   # SCAFFOLD adult milestones an ordinary run banks at


# ---------------------------------------------------------------------------
# The developed agent -- the complete resumable organism (S11.2)
# ---------------------------------------------------------------------------

@dataclass
class DevelopedAgent:
    engine: SubstrateEngine
    social: RelationshipMatrix = field(default_factory=RelationshipMatrix)
    environmental: EnvironmentMatrix = field(default_factory=EnvironmentMatrix)
    group: GroupMatrix = field(default_factory=GroupMatrix)
    self_reflection: SelfReflection = field(default_factory=SelfReflection)
    state_vector: StateVector = field(default_factory=StateVector)
    provenance: Dict = field(default_factory=dict)   # growth conditions + RNG seed (S11.2)
    # v10: the GIVEN physical endowment + biological sex this adult grew with (E1). Banked so a
    # restored adult RELOADS its real traits (restored-never-edited + banked-reproducibility) rather
    # than being re-sampled. Empty/None for a physical-neutral adult or a pre-v10 (legacy) snapshot.
    physical: Dict[str, float] = field(default_factory=dict)
    sex: Optional[str] = None
    # v14 kinship: the GIVEN genetic-fingerprint signature this adult grew with, banked verbatim so a
    # restored adult RELOADS it (restored-never-edited) rather than being re-sampled. Empty for a
    # signature-neutral adult or a pre-v14 (legacy) snapshot.
    signature: List[int] = field(default_factory=list)

    @property
    def age_years(self) -> float:
        return self.engine.age_years


# ---------------------------------------------------------------------------
# Component (de)serialisation -- pure state round-trips, no editing surface
# ---------------------------------------------------------------------------

def _reconstruct(cls, d: Dict):
    """Rebuild a dataclass from an asdict() dump, using only its init fields."""
    init = {f.name for f in dataclasses.fields(cls) if f.init}
    return cls(**{k: v for k, v in d.items() if k in init})


def _dump_learner(l: ValueLearner) -> Dict:
    return {k: dataclasses.asdict(v) for k, v in l.values.items()}


def _load_learner(d: Dict) -> ValueLearner:
    l = ValueLearner()
    l.values = {k: _reconstruct(CueValue, v) for k, v in d.items()}
    return l


def _dump_relmatrix(rm: RelationshipMatrix) -> Dict:
    return {"slots": {k: dataclasses.asdict(s) for k, s in rm.slots.items()},
            "learner": _dump_learner(rm.learner),
            "layers": list(rm.layers), "clock": rm._clock}


def _load_relmatrix(d: Dict) -> RelationshipMatrix:
    rm = RelationshipMatrix()
    rm.slots = {k: _reconstruct(RelationshipSlot, s) for k, s in d["slots"].items()}
    rm.learner = _load_learner(d["learner"])
    rm.layers = tuple(d.get("layers", rm.layers))
    rm._clock = d.get("clock", 0)
    return rm


def _dump_envmatrix(em: EnvironmentMatrix) -> Dict:
    return {"bonds": {k: dataclasses.asdict(b) for k, b in em.bonds.items()},
            "learner": _dump_learner(em.learner)}


def _load_envmatrix(d: Dict) -> EnvironmentMatrix:
    em = EnvironmentMatrix()
    em.bonds = {k: _reconstruct(Bond, b) for k, b in d["bonds"].items()}
    em.learner = _load_learner(d["learner"])
    return em


def _dump_groupmatrix(gm: GroupMatrix) -> Dict:
    return {"memberships": {k: dataclasses.asdict(m) for k, m in gm.memberships.items()},
            "learner": _dump_learner(gm.learner)}


def _load_groupmatrix(d: Dict) -> GroupMatrix:
    gm = GroupMatrix()
    gm.memberships = {k: _reconstruct(Membership, m) for k, m in d["memberships"].items()}
    gm.learner = _load_learner(d["learner"])
    return gm


def _dump_statevector(sv: StateVector) -> Dict:
    return {"levels": dict(sv.levels), "set_points": dict(sv.set_points),
            "weights": dict(sv.weights)}


def _load_statevector(d: Dict) -> StateVector:
    return StateVector(levels=dict(d["levels"]), set_points=dict(d["set_points"]),
                       weights=dict(d["weights"]))


def _dump_engine(e: SubstrateEngine) -> Dict:
    """The sculpted connectome + the plasticity state needed to RESUME (weights, per-connection
    experience counts, BCM thresholds, running means, pruning, age). Transient activity/inputs
    are not persisted -- they are re-established on resume."""
    return {"weight": [float(w) for w in e.weight],
            "exp_count": [int(n) for n in e.exp_count],
            "theta": {k: float(v) for k, v in e.theta.items()},
            "mean_activity": {k: float(v) for k, v in e.mean_activity.items()},
            "pruned": [bool(p) for p in e.pruned],
            "throttle": {k: float(v) for k, v in e.throttle.items()},
            "age_years": float(e.age_years), "step_i": int(e._step_i)}


def _restore_engine(model: SubstrateModel, s: Dict) -> SubstrateEngine:
    e = SubstrateEngine(model, age_years=s["age_years"])
    # a banked agent's per-connection arrays are sized to the connectome it GREW on; if the current
    # seed has a different connection count (a version bump added/removed edges), the bank is stale.
    # Fail clearly here rather than IndexError deep in step(); do NOT pad (that would fabricate weights
    # for edges the adult never developed -- restored-never-edited). The fix is to regrow the cache.
    if len(s["weight"]) != len(model.connections):
        raise ValueError(
            f"stale bank: banked agent has {len(s['weight'])} connections but the current seed has "
            f"{len(model.connections)} -- grown on a different connectome version. Regrow the cache "
            f"under the current seed (never pad; restored-never-edited).")
    e.weight = list(s["weight"])
    e.exp_count = list(s["exp_count"])
    e.theta = dict(s["theta"])
    e.mean_activity = dict(s["mean_activity"])
    e.pruned = list(s["pruned"])
    e.throttle = dict(s["throttle"])
    e._step_i = int(s["step_i"])
    e._refresh_live()
    return e


# ---------------------------------------------------------------------------
# Snapshot / restore -- the whole organism
# ---------------------------------------------------------------------------

def snapshot(agent: DevelopedAgent) -> Dict:
    """Serialise a GROWN agent's complete developed state (S11.2). A read of the agent; it does
    not alter it. The result is JSON-able and carries the provenance needed to trace how it grew."""
    return {
        "version": SNAPSHOT_VERSION,
        "engine": _dump_engine(agent.engine),
        "social": _dump_relmatrix(agent.social),
        "environmental": _dump_envmatrix(agent.environmental),
        "group": _dump_groupmatrix(agent.group),
        "self_reflection": _dump_relmatrix(agent.self_reflection.matrix),
        "state_vector": _dump_statevector(agent.state_vector),
        "provenance": dict(agent.provenance),
        "physical": dict(agent.physical),   # v10: the given endowment, banked verbatim (E1)
        "sex": agent.sex,
        "signature": list(agent.signature),  # v14: the given kin signature, banked verbatim
    }


def restore(state: Dict, model: Optional[SubstrateModel] = None) -> DevelopedAgent:
    """Rebuild the exact banked agent to RESUME (S11.4). No editing hook: this returns the state
    as it was grown, ready to keep developing under the same plasticity schedule."""
    m = model or load_substrate()
    return DevelopedAgent(
        engine=_restore_engine(m, state["engine"]),
        social=_load_relmatrix(state["social"]),
        environmental=_load_envmatrix(state["environmental"]),
        group=_load_groupmatrix(state["group"]),
        self_reflection=SelfReflection(matrix=_load_relmatrix(state["self_reflection"])),
        state_vector=_load_statevector(state["state_vector"]),
        provenance=dict(state.get("provenance", {})),
        # v10: RELOAD the banked endowment verbatim. A pre-v10 snapshot has no "physical"/"sex" key
        # -> physical-neutral (never fabricated) until the cache is regrown under v10.
        physical=dict(state.get("physical", {}) or {}),
        sex=state.get("sex", None),
        # v14: RELOAD the banked kin signature verbatim. A pre-v14 snapshot has no "signature" key
        # -> signature-neutral (never fabricated) until the cache is regrown under v14.
        signature=list(state.get("signature", []) or []),
    )


# ---------------------------------------------------------------------------
# The bank -- a growing cache of grown adults, with provenance
# ---------------------------------------------------------------------------

class AgentBank:
    """A store of banked developed states. Grown-and-banked only (there is no fabricate path);
    restored, never edited. Optionally file-backed so the cache accumulates across runs (S11.3)."""

    def __init__(self, path: Optional[str] = None):
        self.records: Dict[str, Dict] = {}
        self.path = path
        if path and os.path.isfile(path):
            self.load(path)

    def bank(self, agent: DevelopedAgent, agent_id: str,
             provenance: Optional[Dict] = None) -> str:
        """Bank a GROWN agent under `agent_id`. `provenance` (growth conditions + RNG seed) is
        merged into the agent's own; a banked adult must be traceable to how it was grown."""
        if provenance:
            agent.provenance = {**agent.provenance, **provenance}
        self.records[agent_id] = snapshot(agent)
        return agent_id

    def auto_bank(self, agent: DevelopedAgent, base_id: str,
                  provenance: Optional[Dict] = None,
                  ages: tuple = AUTO_BANK_AGES) -> List[str]:
        """Auto-bank an adult at the milestone ages it has reached but not yet been banked at
        (S11.3) -- the by-product of an ordinary run that grows the diverse cache. Returns the
        ids banked this call."""
        banked = []
        for milestone in ages:
            if agent.age_years + 1e-9 >= milestone:
                key = f"{base_id}@{int(milestone)}"
                if key not in self.records:
                    self.bank(agent, key, provenance)
                    banked.append(key)
        return banked

    def restore(self, agent_id: str, model: Optional[SubstrateModel] = None) -> DevelopedAgent:
        return restore(self.records[agent_id], model)

    def provenance_of(self, agent_id: str) -> Dict:
        return dict(self.records[agent_id].get("provenance", {}))

    def ids(self) -> List[str]:
        return list(self.records.keys())

    def __len__(self) -> int:
        return len(self.records)

    def __contains__(self, agent_id: str) -> bool:
        return agent_id in self.records

    def save(self, path: Optional[str] = None) -> None:
        p = path or self.path
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(self.records, fh)

    def load(self, path: Optional[str] = None) -> None:
        p = path or self.path
        with open(p, "r", encoding="utf-8") as fh:
            self.records = json.load(fh)

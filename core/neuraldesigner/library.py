"""
library.py -- the neural-pathway design library.

This is the authoring layer for the affective engine. Where the production engine
ships a small, hand-tuned set of circuits and networks, this library lets you
*define* them as data and build up a reusable catalogue -- the tool you need to
scale the model "several hundred times" without hand-coding each piece.

Five kinds of definition, each stored in the library and referenced by id:

  InputFeature -- a named quantity the circuits can respond to: a raw appraisal
                  dimension, or a derived feature (e.g. "uncontrollability",
                  "blocked_goal", or "impulse_pressure" over impulsive circuits).
  CircuitDef   -- a neural-style circuit: a gain, a decay, and a category.
  TriggerDef   -- an external drive: FEATURE --(weight)--> CIRCUIT. This is how a
                  situation activates a circuit.
  PathwayDef   -- an internal connection: CIRCUIT --(weight)--> CIRCUIT. Positive
                  is excitatory, negative inhibitory. Chains of pathways are
                  cascades; a pathway that returns to its source (directly or via
                  others) is a loop. This is the machinery the production engine
                  does not yet have, and the thing that makes circuits "activate
                  together".
  NetworkDef   -- a behavioural network: a weighted coalition of circuits, a set
                  of regulatory modulators, an affordance set, and a policy. The
                  networks are the modes an agent runs.

The whole library serialises to and from JSON, so catalogues can be saved,
shared, versioned and edited outside the code.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
import json


# ---------------------------------------------------------------------------
# Definitions
# ---------------------------------------------------------------------------

@dataclass
class InputFeature:
    id: str
    kind: str                 # "appraisal" (a raw dimension) | "derived" (computed)
    description: str = ""
    # for derived features, the name of the built-in derivation to use
    derivation: Optional[str] = None


@dataclass
class CircuitDef:
    id: str
    name: str = ""
    gain: float = 0.5         # constitutional sensitivity (trait-set, dev-tuned)
    decay: float = 0.5        # leaky-integrator retention of previous activation
    category: str = "affective"   # "affective" | "motivational" | "regulatory"
    impulsive: bool = False   # counts toward impulse_pressure
    description: str = ""


@dataclass
class TriggerDef:
    id: str
    feature: str              # InputFeature id
    circuit: str              # CircuitDef id it drives
    weight: float             # signed contribution to the circuit's external drive


@dataclass
class PathwayDef:
    id: str
    source: str               # CircuitDef id
    target: str               # CircuitDef id
    weight: float             # excitatory (+) or inhibitory (-)
    kind: str = "direct"      # "direct" | "cascade" | "loop"  (documentation only)
    description: str = ""


@dataclass
class NetworkDef:
    id: str
    name: str = ""
    weights: Dict[str, float] = field(default_factory=dict)      # circuit -> coalition weight
    modulators: Dict[str, float] = field(default_factory=dict)   # regulatory circuit -> coefficient
    affordances: List[str] = field(default_factory=list)         # env tokens needed to develop
    policy: str = ""
    category: str = "neutral"   # "governed" | "ungoverned" | "neutral" (documentation)


# ---------------------------------------------------------------------------
# The library
# ---------------------------------------------------------------------------

@dataclass
class NeuralLibrary:
    name: str = "library"
    features: Dict[str, InputFeature] = field(default_factory=dict)
    circuits: Dict[str, CircuitDef] = field(default_factory=dict)
    triggers: Dict[str, TriggerDef] = field(default_factory=dict)
    pathways: Dict[str, PathwayDef] = field(default_factory=dict)
    networks: Dict[str, NetworkDef] = field(default_factory=dict)

    # -- authoring API -----------------------------------------------------
    def add_feature(self, feat: InputFeature) -> InputFeature:
        self.features[feat.id] = feat; return feat

    def add_circuit(self, c: CircuitDef) -> CircuitDef:
        self.circuits[c.id] = c; return c

    def add_trigger(self, t: TriggerDef) -> TriggerDef:
        self._require(t.feature in self.features, f"unknown feature {t.feature}")
        self._require(t.circuit in self.circuits, f"unknown circuit {t.circuit}")
        self.triggers[t.id] = t; return t

    def add_pathway(self, p: PathwayDef) -> PathwayDef:
        self._require(p.source in self.circuits, f"unknown source {p.source}")
        self._require(p.target in self.circuits, f"unknown target {p.target}")
        self.pathways[p.id] = p; return p

    def add_network(self, n: NetworkDef) -> NetworkDef:
        for cid in list(n.weights) + list(n.modulators):
            self._require(cid in self.circuits, f"unknown circuit {cid} in network {n.id}")
        self.networks[n.id] = n; return n

    # -- removal (with cascade) -------------------------------------------
    def remove_feature(self, fid: str) -> bool:
        if fid not in self.features:
            return False
        del self.features[fid]
        self.triggers = {k: t for k, t in self.triggers.items() if t.feature != fid}
        return True

    def remove_circuit(self, cid: str) -> bool:
        """Remove a circuit and everything that referenced it (triggers into it,
        pathways touching it, its weight in any network)."""
        if cid not in self.circuits:
            return False
        del self.circuits[cid]
        self.triggers = {k: t for k, t in self.triggers.items() if t.circuit != cid}
        self.pathways = {k: p for k, p in self.pathways.items()
                         if p.source != cid and p.target != cid}
        for n in self.networks.values():
            n.weights.pop(cid, None)
            n.modulators.pop(cid, None)
        return True

    def remove_trigger(self, tid: str) -> bool:
        return self.triggers.pop(tid, None) is not None

    def remove_pathway(self, pid: str) -> bool:
        return self.pathways.pop(pid, None) is not None

    def remove_network(self, nid: str) -> bool:
        return self.networks.pop(nid, None) is not None

    # -- queries used by the runtime --------------------------------------
    def triggers_for(self, circuit_id: str) -> List[TriggerDef]:
        return [t for t in self.triggers.values() if t.circuit == circuit_id]

    def pathways_into(self, circuit_id: str) -> List[PathwayDef]:
        return [p for p in self.pathways.values() if p.target == circuit_id]

    def impulsive_circuits(self) -> List[str]:
        return [c.id for c in self.circuits.values() if c.impulsive]

    # -- integrity ---------------------------------------------------------
    def validate(self) -> List[str]:
        """Return a list of problems (empty if the library is coherent)."""
        problems: List[str] = []
        for t in self.triggers.values():
            if t.feature not in self.features:
                problems.append(f"trigger {t.id}: unknown feature {t.feature}")
            if t.circuit not in self.circuits:
                problems.append(f"trigger {t.id}: unknown circuit {t.circuit}")
        for p in self.pathways.values():
            if p.source not in self.circuits:
                problems.append(f"pathway {p.id}: unknown source {p.source}")
            if p.target not in self.circuits:
                problems.append(f"pathway {p.id}: unknown target {p.target}")
        for n in self.networks.values():
            for cid in list(n.weights) + list(n.modulators):
                if cid not in self.circuits:
                    problems.append(f"network {n.id}: unknown circuit {cid}")
        return problems

    def find_loops(self) -> List[List[str]]:
        """Detect feedback loops in the pathway graph (cycles). Reported so an
        author can see which circuits form self-sustaining assemblies."""
        adj: Dict[str, List[str]] = {c: [] for c in self.circuits}
        for p in self.pathways.values():
            adj.setdefault(p.source, []).append(p.target)
        loops: List[List[str]] = []
        WHITE, GREY, BLACK = 0, 1, 2
        colour = {c: WHITE for c in adj}
        stack: List[str] = []

        def dfs(u: str) -> None:
            colour[u] = GREY; stack.append(u)
            for v in adj.get(u, []):
                if colour.get(v, WHITE) == GREY:
                    loops.append(stack[stack.index(v):] + [v])
                elif colour.get(v, WHITE) == WHITE:
                    dfs(v)
            stack.pop(); colour[u] = BLACK

        for c in list(adj):
            if colour[c] == WHITE:
                dfs(c)
        return loops

    @staticmethod
    def _require(cond: bool, msg: str) -> None:
        if not cond:
            raise ValueError(msg)

    # -- persistence -------------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "features": {k: asdict(v) for k, v in self.features.items()},
            "circuits": {k: asdict(v) for k, v in self.circuits.items()},
            "triggers": {k: asdict(v) for k, v in self.triggers.items()},
            "pathways": {k: asdict(v) for k, v in self.pathways.items()},
            "networks": {k: asdict(v) for k, v in self.networks.items()},
        }

    def save(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def from_dict(cls, d: dict) -> "NeuralLibrary":
        lib = cls(name=d.get("name", "library"))
        lib.features = {k: InputFeature(**v) for k, v in d.get("features", {}).items()}
        lib.circuits = {k: CircuitDef(**v) for k, v in d.get("circuits", {}).items()}
        lib.triggers = {k: TriggerDef(**v) for k, v in d.get("triggers", {}).items()}
        lib.pathways = {k: PathwayDef(**v) for k, v in d.get("pathways", {}).items()}
        lib.networks = {k: NetworkDef(**v) for k, v in d.get("networks", {}).items()}
        return lib

    @classmethod
    def load(cls, path: str) -> "NeuralLibrary":
        with open(path) as f:
            return cls.from_dict(json.load(f))

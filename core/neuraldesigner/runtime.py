"""
runtime.py -- run an authored library.

A LibraryAgent takes a NeuralLibrary and runs the same appraise -> activate ->
score -> arbitrate cycle as the production engine, but over the *authored*
circuits, triggers, pathways and networks rather than hard-coded ones. This is
what lets a designed library of arbitrary size actually behave.

The one capability beyond the production engine is internal pathway propagation:
each tick, a circuit's activation is driven both by external triggers (from the
situation) and by pathways from other circuits (from the previous tick). Chains
of pathways therefore spread activation across ticks (a cascade), and pathways
that return to their source sustain or oscillate activation (a loop).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional

from .library import NeuralLibrary, NetworkDef

# the raw appraisal dimensions a situation can set (mirrors the production engine)
APPRAISAL_DIMS = (
    "threat", "reward", "social_valence", "goal_relevance", "novelty",
    "agency", "controllability", "other_distress", "provocation", "exclusion",
)

ACCESS_FLOOR = 0.35
INCUMBENT_STICK = 0.08
SETTLE_TICKS = 3


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


@dataclass
class Situation:
    """A bundle of appraisal-dimension values (0..1, social_valence -1..1)."""
    values: Dict[str, float] = field(default_factory=dict)
    label: str = ""

    def get(self, dim: str) -> float:
        return self.values.get(dim, 0.0)


class LibraryAgent:
    def __init__(self, library: NeuralLibrary,
                 gains: Optional[Dict[str, float]] = None,
                 access: Optional[Dict[str, float]] = None):
        self.lib = library
        problems = library.validate()
        if problems:
            raise ValueError("library is not coherent: " + "; ".join(problems))
        self.gain = {c.id: c.gain for c in library.circuits.values()}
        if gains:
            self.gain.update(gains)
        self.access = {n.id: 0.3 for n in library.networks.values()}
        if access:
            self.access.update(access)
        self.activation = {c: 0.0 for c in self.gain}
        self.dominant: Optional[str] = None

    def reset(self) -> None:
        self.activation = {c: 0.0 for c in self.gain}
        self.dominant = None

    # -- feature computation ----------------------------------------------
    def _features(self, s: Situation) -> Dict[str, float]:
        """Compute the value of every input feature for this situation, using the
        previous tick's activations for derived features that read circuits."""
        feats: Dict[str, float] = {}
        for f in self.lib.features.values():
            if f.kind == "appraisal":
                feats[f.id] = s.get(f.id)
            elif f.kind == "derived":
                feats[f.id] = self._derive(f.derivation, s)
        return feats

    def _derive(self, name: Optional[str], s: Situation) -> float:
        if name == "uncontrollability":
            return clamp(1.0 - s.get("controllability"))
        if name == "rejection":
            return clamp(max(0.0, -s.get("social_valence")))
        if name == "warmth":
            return clamp(max(0.0, s.get("social_valence")))
        if name == "blocked_goal":
            return clamp(s.get("goal_relevance") * (1.0 - s.get("controllability")))
        if name == "impulse_pressure":
            imp = self.lib.impulsive_circuits()
            return max((self.activation[c] for c in imp), default=0.0)
        if name == "goal_weighted_pressure":
            imp = self.lib.impulsive_circuits()
            pressure = max((self.activation[c] for c in imp), default=0.0)
            return clamp(pressure * (0.5 + 0.5 * s.get("goal_relevance")))
        return 0.0

    # -- one tick ----------------------------------------------------------
    def tick(self, s: Situation) -> None:
        feats = self._features(s)
        prev = dict(self.activation)
        for cid in self.gain:
            external = sum(t.weight * feats.get(t.feature, 0.0)
                           for t in self.lib.triggers_for(cid))
            internal = sum(p.weight * prev[p.source]
                           for p in self.lib.pathways_into(cid))
            target = clamp(self.gain[cid] * clamp(external + internal))
            decay = self.lib.circuits[cid].decay
            self.activation[cid] = decay * prev[cid] + (1 - decay) * target
        self.dominant = self._arbitrate()

    def settle(self, s: Situation, ticks: int = SETTLE_TICKS) -> str:
        for _ in range(ticks):
            self.tick(s)
        return self.dominant

    # -- scoring and arbitration ------------------------------------------
    def network_score(self, net: NetworkDef) -> float:
        base = sum(w * self.activation.get(c, 0.0) for c, w in net.weights.items())
        base += sum(coef * self.activation.get(c, 0.0)
                    for c, coef in net.modulators.items())
        reach = ACCESS_FLOOR + (1 - ACCESS_FLOOR) * self.access.get(net.id, 0.3)
        return max(0.0, base) * reach

    def _arbitrate(self) -> Optional[str]:
        if not self.lib.networks:
            return None
        scores = {nid: self.network_score(net)
                  for nid, net in self.lib.networks.items()}
        if self.dominant is not None and self.dominant in scores:
            scores[self.dominant] += INCUMBENT_STICK
        return max(scores, key=scores.get)

    # -- inspection --------------------------------------------------------
    def trace(self, s: Situation, ticks: int = SETTLE_TICKS):
        """Run and return the per-tick activation of every circuit, for
        inspecting cascades and loops."""
        self.reset()
        history = []
        for _ in range(ticks):
            self.tick(s)
            history.append(dict(self.activation))
        return history

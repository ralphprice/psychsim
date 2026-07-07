"""
memory.py -- an episodic memory stream for the affective agent.

Each lived event is recorded as an EpisodicMemory: the situation, how it was
appraised, which behavioural network the agent ran, and the valence of the
environment's response (warm/rewarding vs harsh/punishing). Retrieval scores
memories by recency x importance x relevance, following the generative-agents
memory-stream design.

Memory feeds behaviour through *priming*: on meeting a new situation, the agent
retrieves similar past episodes and its appraisal is nudged by what those
episodes were like -- a learned expectation. An agent whose similar past was
threatening becomes threat-primed (hypervigilant); one whose past was warm does
not. The nudge is deliberately small and bounded, so memory adds a second,
realistic pathway by which history shapes the agent without swamping the
circuit-and-development mechanism.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple
import math

from .core import Appraisal, APPRAISAL_DIMS, clamp

# Priming constants (bounded, modest -- memory nudges, it does not dictate)
RECENCY_HALFLIFE = 20.0   # episodes; recency weight halves over this span
PRIME_THREAT_W = 0.20     # how much a threatening past raises threat appraisal
PRIME_SOCIAL_W = 0.15     # how much past valence colours social expectation
RETRIEVE_K = 5


def _appraisal_vector(a: Appraisal) -> List[float]:
    return [getattr(a, d) for d in APPRAISAL_DIMS]


def _similarity(a: Appraisal, b: Appraisal) -> float:
    """Cosine similarity over appraisal dimensions, mapped to [0,1]."""
    va, vb = _appraisal_vector(a), _appraisal_vector(b)
    dot = sum(x * y for x, y in zip(va, vb))
    na = math.sqrt(sum(x * x for x in va))
    nb = math.sqrt(sum(y * y for y in vb))
    if na == 0 or nb == 0:
        return 0.0
    return clamp((dot / (na * nb) + 1.0) / 2.0)


@dataclass
class EpisodicMemory:
    t: int                 # timestep the event occurred
    label: str             # situation archetype
    appraisal: Appraisal   # how it was appraised
    dominant: str          # behavioural network the agent ran
    valence: float         # environment response: +warm/reward .. -harsh/punish
    importance: float      # salience of the event (0..1)


@dataclass
class MemoryStream:
    events: List[EpisodicMemory] = field(default_factory=list)
    _clock: int = 0

    def add(self, label: str, appraisal: Appraisal, dominant: str,
            valence: float, importance: float) -> None:
        self.events.append(EpisodicMemory(
            self._clock, label, appraisal, dominant,
            valence, clamp(importance)))
        self._clock += 1

    def retrieve(self, cue: Appraisal, k: int = RETRIEVE_K
                 ) -> List[Tuple[float, EpisodicMemory]]:
        """Top-k memories by recency x importance x relevance to the cue."""
        scored = []
        now = self._clock
        for m in self.events:
            recency = 0.5 ** ((now - m.t) / RECENCY_HALFLIFE)
            relevance = _similarity(cue, m.appraisal)
            score = recency * (0.4 + 0.6 * m.importance) * relevance
            scored.append((score, m))
        scored.sort(key=lambda s: s[0], reverse=True)
        return scored[:k]

    def prime(self, appraisal: Appraisal) -> Appraisal:
        """Return a copy of the appraisal nudged by retrieved similar memories.
        With an empty stream this is a no-op, so behaviour is unchanged until an
        agent has a history."""
        hits = self.retrieve(appraisal)
        if not hits:
            return appraisal
        wsum = sum(s for s, _ in hits) or 1.0
        threat_assoc = sum(s * clamp(m.appraisal.threat + m.appraisal.provocation)
                           for s, m in hits) / wsum
        valence = sum(s * m.valence for s, m in hits) / wsum

        primed = Appraisal(**{d: getattr(appraisal, d) for d in APPRAISAL_DIMS},
                           label=appraisal.label)
        primed.threat = clamp(primed.threat + PRIME_THREAT_W * threat_assoc)
        # a bad past lowers expected controllability and warms/cools the social read
        if valence < 0:
            primed.controllability = clamp(primed.controllability
                                           + PRIME_SOCIAL_W * valence)  # valence<0 lowers it
        primed.social_valence = clamp(primed.social_valence
                                      + PRIME_SOCIAL_W * valence, -1.0, 1.0)
        return primed

    def summary(self) -> str:
        if not self.events:
            return "(no memories)"
        n = len(self.events)
        avg_val = sum(m.valence for m in self.events) / n
        from collections import Counter
        modes = Counter(m.dominant for m in self.events)
        top = ", ".join(f"{k} x{v}" for k, v in modes.most_common(3))
        return (f"{n} episodes | mean response valence {avg_val:+.2f} | "
                f"most-run modes: {top}")

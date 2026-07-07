"""
self_reflection.py -- the FOURTH matrix (docs/PsychSim_MASTER_Part5.md S10.2).

"A social matrix with oneself on both sides": NOT a new kind of mechanism, but the existing
social-interaction machinery (relations.RelationshipMatrix) with the SELF as both agent and
target. Self-appraisal, rumination, internalised self-talk -- the agent updates its own
weighted strengths by reflecting on itself, not only through others. Same engine as the
relationship / environment / group matrices; the "partner" is the self.

Why it exists: self-reflection is plausibly part of what separates the sophropath from the
psychopath -- an agent that reflects on its own conduct and updates from it vs one that does
not. Having the channel PRESENT (whether or not it is throttled) means the divergence can
arise through it, rather than being absent by omission.

HONESTY CAUTION (S10.2): this must NOT become a back-door conscience. It is the
self-as-social-partner mechanism, meaning-blind like the other three; whether reflection leads
to prosocial updating or not must EMERGE from the substrate, never be coded. There is no line
here mapping "reflected on bad conduct" to "becomes prosocial" -- reflect() takes a computed
valence and updates value by the same RPE as observing anyone else.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional

from .relations import RelationshipMatrix, RelationshipSlot

SELF = "self"


@dataclass
class SelfReflection:
    """The agent's relationship with itself, on the shared relationship-matrix engine."""
    matrix: RelationshipMatrix = field(default_factory=RelationshipMatrix)

    def reflect(self, r: float, attachment_pull: float = 0.0, threat_pull: float = 0.0,
                drive_profile: Optional[Dict[str, float]] = None) -> RelationshipSlot:
        """One act of self-reflection: appraise one's own recent conduct's OUTCOME (the computed
        valence `r`) and update the self-relation -- exactly as observing another would. The
        `attachment_pull`/`threat_pull` are how much reflecting engaged self-directed approach
        vs self-directed threat (self-worth vs self-criticism), left to emerge."""
        return self.matrix.observe(SELF, r, attachment_pull=attachment_pull,
                                   threat_pull=threat_pull, drive_profile=drive_profile)

    def self_value(self) -> float:
        """The learned value of the self -- a read-out, no verdict. Positive/negative/ambivalent
        self-regard EMERGES from the history of self-appraisals; it is not set."""
        slot = self.matrix.slots.get(SELF)
        return slot.value if slot else 0.0

    def self_slot(self) -> Optional[RelationshipSlot]:
        return self.matrix.slots.get(SELF)

    def is_ambivalent_toward_self(self) -> bool:
        """Self-directed approach AND threat both high -- the internal analogue of the
        ambivalent bond (self-conflict / harsh inner critic), emergent, not coded."""
        slot = self.matrix.slots.get(SELF)
        return slot.ambivalent if slot else False

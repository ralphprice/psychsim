"""
relations.py -- the relational fabric of a functioning society (core).

A society is not a set of isolated agents; it is a web of standing relationships,
and a working society *notices* when one is upheld and when it is strained --
because that felt strain is exactly what social norms and restraint exist to
manage. This module is that fabric: the ordinary ties any society has by
definition -- parent and child, teacher and pupil, colleague and colleague,
teammate and teammate, a community group, an employer and an employee -- each a
directed tie carrying a role-pair, a POWER DIFFERENTIAL, and a RELATIONAL STATE
that registers strain and repair.

Reciprocity and restraint are the functioning default: the party with authority
exercises it with care, the other responds with respect, and the tie holds. When
either side presses an advantage or disengages, the tie is strained -- and a
cohesive society repairs it. All of this is *normal* social functioning, so it
lives in the core. What perturbs the fabric -- a particular disposition, and what
its strain-patterns mean developmentally -- is the subject of study, and lives in
an extension.

The core registers whether a relationship worked or was strained. It does not
interpret *why*, or attach any judgement of character to it; that reading is the
extension's.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import json as _json
import os as _os
import random

from affective_engine.core import Appraisal, clamp
from affective_engine.drives import respond_to_appraisal, is_cohesive, is_aggressive


# ---------------------------------------------------------------------------
# Role-pairs -- the standard directed relationships of a working society
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RolePair:
    """A standard relationship: a role over another, with a power differential.
    Peers (colleagues, teammates, community members) have little or none.
    Reciprocity is the norm; the higher party's restraint and the other's respect
    are what keep it functioning."""
    higher: str
    lower: str
    power: float                      # 0 = equals, 1 = strong asymmetry
    kind: str = ""                    # a label for the relationship

    @property
    def peers(self) -> bool:
        return self.power < 0.2


# the ordinary ties a society has by definition. Defaults are hard-coded (so the named
# constants always exist for population wiring); data/social/*.json may override their
# attributes (power/higher/lower) or add role-pairs -- the data-driven, editable form.
_TIE_DEFAULTS = {
    "parent-child":    ("parent", "child", 0.80),
    "teacher-pupil":   ("teacher", "pupil", 0.70),
    "boss-employee":   ("boss", "employee", 0.75),
    "colleagues":      ("colleague", "colleague", 0.05),
    "teammates":       ("teammate", "teammate", 0.10),
    "captain-player":  ("captain", "player", 0.35),
    "community-group": ("organiser", "member", 0.20),
}
_SOCIAL_DIR = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))), "data", "social")


def _load_tie_pairs():
    pairs = dict(_TIE_DEFAULTS)                       # kind -> (higher, lower, power)
    try:
        if _os.path.isdir(_SOCIAL_DIR):
            for fn in sorted(_os.listdir(_SOCIAL_DIR)):
                if not fn.endswith(".json"):
                    continue
                with open(_os.path.join(_SOCIAL_DIR, fn)) as f:
                    data = _json.load(f)
                for t in (data if isinstance(data, list) else data.get("ties", [])):
                    d = _TIE_DEFAULTS.get(t["kind"], ("higher", "lower", 0.5))
                    pairs[t["kind"]] = (t.get("higher", d[0]), t.get("lower", d[1]),
                                        float(t.get("power", d[2])))
    except Exception:
        pass
    return {k: RolePair(h, l, p, k) for k, (h, l, p) in pairs.items()}


_TIES = _load_tie_pairs()
PARENT_CHILD = _TIES["parent-child"]
TEACHER_PUPIL = _TIES["teacher-pupil"]
BOSS_EMPLOYEE = _TIES["boss-employee"]
COLLEAGUES = _TIES["colleagues"]
TEAMMATES = _TIES["teammates"]
CAPTAIN_PLAYER = _TIES["captain-player"]
COMMUNITY = _TIES["community-group"]

STANDARD_TIES = tuple(_TIES.values())


def standard_ties():
    """The role-pair definitions (built-in + data/social overrides), for viewing/editing."""
    return list(_TIES.values())


# ---------------------------------------------------------------------------
# A tie -- the relational state a society tracks
# ---------------------------------------------------------------------------

@dataclass
class Tie:
    """A directed relational tie: `higher` holds the senior role toward `lower`.
    Carries STANDING (how the relationship is going, strained..warm), RECIPROCITY
    (how balanced the exchanges are), and a running STRAIN level. A functioning
    society keeps strain low and repairs it; sustained strain is departure from
    the functioning baseline."""
    higher: str
    lower: str
    pair: RolePair
    standing: float = 0.6             # 0 strained .. 1 warm and upheld
    reciprocity: float = 0.6          # 0 one-sided .. 1 balanced
    strain: float = 0.0               # current strain (0 = none)

    def upheld(self) -> bool:
        return self.standing >= 0.4 and self.strain < 0.5

    def state(self) -> str:
        if self.strain >= 0.6:
            return "ruptured"
        if self.strain >= 0.35:
            return "strained"
        if self.standing >= 0.7:
            return "warm"
        return "working"


@dataclass
class Exchange:
    """The record of one relational exchange."""
    higher: str
    lower: str
    kind: str
    higher_mode: str                  # the network the senior party acted in
    lower_mode: str                   # the network the junior party acted in
    higher_restrained: bool           # did the senior party use authority with restraint
    lower_respectful: bool            # did the junior party respond with respect
    upheld: bool                      # did the tie hold this time
    strain_delta: float
    state: str


# ---------------------------------------------------------------------------
# Running an exchange -- both parties act; the tie holds or is strained
# ---------------------------------------------------------------------------

def _cohesive(network: str) -> bool:
    """A behavioural mode that sustains a relationship: warm or governed conduct
    (cooperation, considered self-command). Not exploitative, not a withdrawal
    that disengages the tie."""
    return network in GOVERNED or network == "affiliative_warmth"


def _appraisal_for_higher(tie: Tie) -> Appraisal:
    # the senior party's situation: responsibility toward the other, coloured by
    # how the relationship is going; the power differential is theirs to hold well
    a = Appraisal(label="relate")
    a.social_valence = clamp(2.0 * tie.standing - 1.0, -1.0, 1.0)
    a.goal_relevance = 0.5
    a.controllability = clamp(0.4 + 0.4 * tie.pair.power)
    a.other_distress = clamp(0.2 * tie.strain)
    return a


def _appraisal_for_lower(tie: Tie) -> Appraisal:
    # the junior party's situation: the power differential is a mild pressure;
    # a strained tie primes worse
    a = Appraisal(label="relate")
    a.social_valence = clamp(2.0 * tie.standing - 1.0, -1.0, 1.0)
    a.goal_relevance = 0.5
    a.controllability = clamp(0.5 - 0.3 * tie.pair.power)
    a.threat = clamp(0.3 * tie.strain + 0.15 * tie.pair.power * (1.0 - tie.standing))
    a.provocation = clamp(0.4 * tie.strain)
    return a


def interact(tie: Tie, higher_mind, lower_mind,
             rng: Optional[random.Random] = None) -> Exchange:
    """Run one relational exchange. Both parties act through the affective engine
    on appraisals coloured by the tie (power, standing, strain); the tie updates
    to reflect whether it held or was strained. Reciprocity and restraint keep it
    functioning; pressing an advantage or disengaging strains it, and the society
    repairs low strain over time."""
    hi_resp = respond_to_appraisal(higher_mind, _appraisal_for_higher(tie))
    lo_resp = respond_to_appraisal(lower_mind, _appraisal_for_lower(tie))
    hi, lo = hi_resp.behaviour, lo_resp.behaviour   # the acts, from the substrate

    higher_restrained = is_cohesive(hi_resp)   # holds authority well (affiliative)
    lower_respectful = is_cohesive(lo_resp)    # responds with engagement/respect

    # the tie updates: both cohesive -> repair & warm; either presses/disengages
    # -> strain, and the more so when the powerful party is the one who does
    if higher_restrained and lower_respectful:
        d_strain = -0.25                       # repair
        d_standing = +0.10
        d_recip = +0.10
    else:
        pressed_by_power = (not higher_restrained)
        base = 0.30 if is_aggressive(hi_resp) or is_aggressive(lo_resp) else 0.15
        d_strain = base + (0.15 * tie.pair.power if pressed_by_power else 0.0)
        d_standing = -0.12 - (0.10 if pressed_by_power else 0.0)
        d_recip = -0.15 if (higher_restrained != lower_respectful) else -0.05

    tie.strain = clamp(tie.strain + d_strain)
    tie.standing = clamp(tie.standing + d_standing)
    tie.reciprocity = clamp(tie.reciprocity + d_recip)
    upheld = tie.upheld()
    return Exchange(tie.higher, tie.lower, tie.pair.kind, hi, lo,
                    higher_restrained, lower_respectful, upheld,
                    round(d_strain, 3), tie.state())


# ---------------------------------------------------------------------------
# A society -- the web of standing ties, and its cohesion
# ---------------------------------------------------------------------------

@dataclass
class Society:
    """The relational fabric: the standing ties between members, and helpers to
    read the society's cohesion (how many relationships are upheld)."""
    ties: List[Tie] = field(default_factory=list)

    def add(self, higher: str, lower: str, pair: RolePair, **kw) -> Tie:
        t = Tie(higher, lower, pair, **kw)
        self.ties.append(t)
        return t

    def tie_between(self, higher: str, lower: str) -> Optional[Tie]:
        for t in self.ties:
            if t.higher == higher and t.lower == lower:
                return t
        return None

    def cohesion(self) -> float:
        """Share of ties currently upheld -- a working society keeps this high."""
        if not self.ties:
            return 1.0
        return sum(1 for t in self.ties if t.upheld()) / len(self.ties)

    def strained(self) -> List[Tie]:
        return [t for t in self.ties if not t.upheld()]

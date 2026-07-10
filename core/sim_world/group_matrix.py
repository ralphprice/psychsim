"""
group_matrix.py -- a person's relationship with GROUPS: the third interface matrix,
parallel to the relationship matrix (beings) and the environment matrix (things).

A group is not reducible to the dyadic ties within it. A group has an identity a
person can belong to, a status hierarchy a person occupies a position in, and norms
a person conforms to or resists -- and belonging as such exerts its own pull. This
matrix models that group-level layer: a per-person ledger of MEMBERSHIPS, from which
a person's social identity (which groups, where they stand in each) can be read.

Grounded in four established frameworks (crude first pass; to be refined against the
literature, cited properly in the research write-up):

  * Social identity theory (Tajfel & Turner, 1979; self-categorization, Turner et
    al., 1987): the self-concept is partly derived from group memberships, through
    categorization, identification, and comparison; group membership carries "value
    and emotional significance"; in-group / out-group distinctions shape behaviour.

  * The need to belong (Baumeister & Leary, 1995): a fundamental, pervasive human
    motivation to form and maintain lasting, positive relationships; an individual-
    difference variable (some need it more), and one that can be satiated.

  * Ostracism / the temporal need-threat model (Williams, 2007; Williams & Nida):
    social exclusion threatens belonging, self-esteem, control, and meaningful
    existence, produces a reflexive pain response (shared representation with
    physical pain; Eisenberger, 2012), and drives aggression, withdrawal, or
    compliance / conformity.

  * The dual model of status (Henrich & Gil-White, 2001; Cheng, Tracy & Henrich,
    2013): status within a group is attained by two distinct routes -- DOMINANCE
    (status taken via threat, fear, coercion) and PRESTIGE (status freely conferred
    for competence and skill others wish to learn).

The discipline is the same as everywhere in PsychSim. A group ENCOUNTER presents a
stimulus bundle in the substrate's own trigger vocabulary (acceptance presents
affiliation and safety; exclusion presents separation and pain; a status contest
presents thwarting and reward; conformity pressure presents restraint). The person's
own substrate settles on that bundle, the dominant domain drives behaviour, and standing,
belonging, contribution and conformity accrue from that EMERGENT behaviour -- never typed in. So
a person whose substrate leans affiliative and one whose leans defensive-aggressive come to
occupy and value the same group differently, and, crucially, gain standing by different ROUTES
(prestige vs dominance), emergently. Group experience also strengthens the pathways it engages, so
a person's groups shape their personality and their personality shapes their standing
-- both, through the same substrate.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import json
import os
import random

from affective_engine.core import clamp
from affective_engine.interocept import reference_child_state, valence_of_event
from affective_engine.learning import ValueLearner
from affective_engine import params as _params

_GROUPS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "data", "groups")

# How a group encounter grounds the one valence engine (App. 3.3): acceptance/synchrony
# relieve the belonging deficit (synchrony via the endorphin channel; Tarr/Dunbar);
# exclusion/rejection deepen it and raise arousal (social pain). SCAFFOLD intensities.
ENCOUNTER_PERTURBATION = {
    "acceptance":   {"acceptance": 0.8},
    "contributing": {"acceptance": 0.5},
    "synchrony":    {"synchrony": 1.0},        # collective effervescence -> endorphin belonging
    "exclusion":    {"rejection": 0.9, "separation": 0.4},
    "rejection":    {"rejection": 0.9},
}


# ---------------------------------------------------------------------------
# A group -- a NEUTRAL container describing a group a person can belong to
# ---------------------------------------------------------------------------

@dataclass
class Group:
    """A group a person can belong to. Descriptive attributes only -- size,
    cohesion (how tight-knit), status (its standing relative to other groups), and
    norm_strength (how strongly it enforces conformity). These colour the intensity
    of the stimuli a group encounter presents; they never encode what belonging
    does to the person."""
    id: str
    name: str
    kind: str = "group"       # family | class | clique | team | workplace | community | ...
    size: int = 12
    cohesion: float = 0.5     # 0 loose .. 1 tight-knit
    status: float = 0.5       # the group's own standing relative to others
    norm_strength: float = 0.5  # 0 permissive .. 1 strongly enforced norms


# ---------------------------------------------------------------------------
# A membership -- the running trace of a person's relationship with one group
# (the parallel of a Tie and a Bond)
# ---------------------------------------------------------------------------

@dataclass
class Membership:
    """A person's accumulating relationship with one group. All quantities are
    running traces that EMERGE from how the person's systems responded across group
    encounters; none is stipulated."""
    group_id: str
    kind: str = "group"
    standing: float = 0.2        # rank within the group: 0 peripheral/low .. 1 central/high
    belonging: float = 0.0       # identification / felt belonging (need-to-belong satisfaction)
    contribution: float = 0.0    # what the person gives to the group
    benefit: float = 0.0         # what the person gets from the group
    conformity: float = 0.5      # 0 resists norms .. 1 conforms
    # the ROUTE by which standing has been gained (Henrich & Gil-White), emergent:
    dominance_route: float = 0.0   # status taken via aggression / coercion
    prestige_route: float = 0.0    # status earned via competence / prosociality
    encounters: int = 0
    system_counts: Dict[str, int] = field(default_factory=dict)  # which systems fired
    # RPE-learned value of the group on the one engine (App. C.9), and the SOCIOMETER --
    # self-esteem as a gauge of social inclusion (Leary), tracking belonging (App. 3.3).
    value: float = 0.0
    esteem: float = 0.0

    def sociometer(self) -> float:
        """Self-esteem read as a gauge of inclusion in this group (Leary sociometer)."""
        return self.esteem

    def social_rank(self) -> float:
        return self.standing

    def identity_centrality(self) -> float:
        """How central this group is to the person's identity (how strongly they
        belong / identify)."""
        return self.belonging

    def status_route(self) -> str:
        """Descriptive read-out of HOW standing was gained -- dominance, prestige,
        or neither yet. A measurement, not a driver."""
        if self.dominance_route > self.prestige_route + 0.1:
            return "dominance"
        if self.prestige_route > self.dominance_route + 0.1:
            return "prestige"
        return "none/mixed"

    def state(self) -> str:
        """A descriptive label for where the person stands in the group."""
        if self.encounters == 0:
            return "unknown"
        if self.belonging <= -0.2:
            return "excluded"
        if self.standing >= 0.6:
            return "central"
        if self.belonging >= 0.3:
            return "belonging"
        if self.standing <= 0.15 and self.belonging <= 0.05:
            return "peripheral"
        return "member"


@dataclass
class GroupMatrix:
    """A person's ledger of memberships -- parallel to a Society of ties and an
    EnvironmentMatrix of bonds, but centred on ONE person. Their social identity is
    read straight off it."""
    memberships: Dict[str, Membership] = field(default_factory=dict)
    learner: ValueLearner = field(default_factory=ValueLearner)  # RPE value store (App. C.9)

    def membership(self, group_id: str, kind: str = "group") -> Membership:
        m = self.memberships.get(group_id)
        if m is None:
            m = Membership(group_id, kind)
            self.memberships[group_id] = m
        return m

    def identities(self, top: Optional[int] = None) -> List[Membership]:
        """The groups the person identifies with / belongs to, strongest first --
        their social identity."""
        ms = sorted((m for m in self.memberships.values() if m.belonging > 0.05),
                    key=lambda m: -m.belonging)
        return ms[:top] if top else ms

    def ranks(self, top: Optional[int] = None) -> List[Membership]:
        """The groups the person stands high in, by rank."""
        ms = sorted(self.memberships.values(), key=lambda m: -m.standing)
        return ms[:top] if top else ms


# ---------------------------------------------------------------------------
# Group encounters -- what different kinds of group moment PRESENT to the substrate
# (stimulus bundles in the neutral trigger vocabulary; never a verdict)
# ---------------------------------------------------------------------------

ENCOUNTER_STIMULI: Dict[str, Dict[str, float]] = {
    # being accepted / included -- affiliation and felt safety
    "acceptance":           {"affiliation": 0.7, "safety": 0.5, "play_signal": 0.3},
    # being excluded / ostracised -- separation, loss, and social pain
    "exclusion":            {"separation": 0.7, "loss": 0.4, "threat": 0.2, "pain": 0.3},
    # a chance to gain standing -- a positional, CONTESTED good: a reward cue AND a
    # competitive thwarting element, so a defensive-aggressive-leaning person may construe it
    # as a fight (taking rank by dominance) and a reward/affiliation-driven person as a
    # chance to excel (earning it by prestige)
    "status_gain":          {"reward_cue": 0.6, "thwarting": 0.4, "affiliation": 0.3,
                             "novelty": 0.3},
    # a challenge to one's standing -- thwarting and threat over a reward
    "status_challenge":     {"thwarting": 0.6, "threat": 0.3, "reward_cue": 0.4},
    # pressure to conform to the group's norms -- restraint and thwarting
    "conformity_pressure":  {"restraint": 0.6, "thwarting": 0.4, "affiliation": 0.3},
    # competition with an out-group -- thwarting/threat, with in-group affiliation
    "outgroup_competition": {"thwarting": 0.5, "threat": 0.4, "affiliation": 0.4},
    # contributing to the group -- giving, with a vulnerable other to tend
    "contributing":         {"affiliation": 0.5, "reward_cue": 0.4, "vulnerable_other": 0.4},
    # collective synchrony / effervescence (dance, song, chant, marching, team sport) --
    # coordinated exertive activity; bonds via the endorphin channel (Tarr/Dunbar)
    "synchrony":            {"affiliation": 0.6, "play_signal": 0.5, "safety": 0.4},
}

# extra endorphin belonging accrued by synchronous collective activity, beyond the
# ordinary affiliative response (App. 3.3). SCAFFOLD.
SYNCHRONY_ENDORPHIN = 0.10
SOCIOMETER_LR = 0.3     # SCAFFOLD rate the sociometer (esteem) tracks felt belonging

ACCRUE = 0.15   # ledger step; crude and tunable, NOT a claim about effect


def group_encounter(agent, group: Group, membership: Membership,
                    encounter_type: str, age_years: float = 30.0, develop: bool = True):
    """One group encounter of a given kind. The encounter's stimulus (scaled by the group's
    cohesion / norm-strength / status) is run through the person's SUBSTRATE; the emergent act IS
    the felt response, and the substrate DEVELOPS through the moment (its own plasticity is the
    use-dependent strengthening). Belonging, standing, contribution and conformity accrue from
    that emergent response -- and, on status encounters, the ROUTE (dominance vs prestige) emerges
    from whether the act was aggressive or appetitive. Nothing about what the group 'should' evoke
    is written in, and no rule arbitrates the result. Returns the FeltResponse."""
    from substrate.social import felt_response
    base = ENCOUNTER_STIMULI.get(encounter_type, {"affiliation": 0.4})
    # the group's own character colours how strongly the moment lands
    intensity = 0.6 + 0.4 * group.cohesion
    if encounter_type == "conformity_pressure":
        intensity = 0.5 + 0.5 * group.norm_strength
    stim = {k: clamp(v * intensity) for k, v in base.items()}

    fr = felt_response(agent.engine, stim, age_years,
                       getattr(agent, "_rest_baseline", None), develop=develop)

    membership.encounters += 1
    membership.system_counts[fr.behaviour] = membership.system_counts.get(fr.behaviour, 0) + 1
    strength = fr.strength
    step = ACCRUE * strength

    # belonging: an appetitive/affiliative act builds it; an aversive (withdrawal / distress)
    # erodes it
    if fr.appetitive:
        membership.belonging = clamp(membership.belonging + step, -1.0, 1.0)
        membership.contribution = clamp(membership.contribution + 0.5 * step)
        membership.benefit = clamp(membership.benefit + 0.5 * step)
    elif fr.aversive:
        membership.belonging = clamp(membership.belonging - step, -1.0, 1.0)

    # standing and its ROUTE: on status-relevant encounters, an aggressive act takes rank by
    # DOMINANCE; an appetitive/competent one earns it by PRESTIGE
    if encounter_type in ("status_gain", "status_challenge", "outgroup_competition"):
        if fr.aggressive:
            membership.standing = clamp(membership.standing + step)
            membership.dominance_route = clamp(membership.dominance_route + step)
        elif fr.appetitive:
            membership.standing = clamp(membership.standing + step)
            membership.prestige_route = clamp(membership.prestige_route + step)
        elif fr.aversive:
            membership.standing = clamp(membership.standing - 0.5 * step)

    # conformity: pressure met with compliance (an appetitive act) raises conformity; met with
    # aggression (resistance) lowers it
    if encounter_type == "conformity_pressure":
        if fr.aggressive:
            membership.conformity = clamp(membership.conformity - step)
        elif fr.appetitive:
            membership.conformity = clamp(membership.conformity + step)

    # synchrony / collective effervescence: an extra endorphin-channel belonging boost,
    # the mechanism that lets group bonding scale past one-to-one contact (App. 3.3)
    if encounter_type == "synchrony":
        membership.belonging = clamp(membership.belonging + SYNCHRONY_ENDORPHIN, -1.0, 1.0)

    # the sociometer: esteem tracks felt inclusion (Leary) -- a read, not a driver
    membership.esteem = clamp(membership.esteem
                              + SOCIOMETER_LR * (membership.belonging - membership.esteem),
                              -1.0, 1.0)

    # RPE value on the one engine (App. C.9): reward = drive reduction the encounter's
    # social perturbation produces (belonging relief / social pain). Per-membership TD
    # update (terminal), so each agent's value for the group is its own. No innate channel
    # -> value learned only by association (r=0 here).
    pert = ENCOUNTER_PERTURBATION.get(encounter_type)
    if pert:
        r, _, _ = valence_of_event(reference_child_state(), pert)
        delta = r - membership.value
        alpha = _params.ALPHA * (_params.AVERSIVE_LR_MULT if delta < 0 else 1.0)
        membership.value = clamp(membership.value + alpha * delta, -1.0, 1.0)

    return fr


# ---------------------------------------------------------------------------
# A small default set of the groups a child ordinarily belongs to
# ---------------------------------------------------------------------------

def _group_from_dict(d: dict) -> Group:
    return Group(id=d["id"], name=d.get("name", d["id"]), kind=d.get("kind", "group"),
                 size=int(d.get("size", 12)), cohesion=float(d.get("cohesion", 0.5)),
                 status=float(d.get("status", 0.5)),
                 norm_strength=float(d.get("norm_strength", 0.5)))


def _load_data_groups() -> List[Group]:
    out: List[Group] = []
    if not os.path.isdir(_GROUPS_DIR):
        return out
    for fn in sorted(os.listdir(_GROUPS_DIR)):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(_GROUPS_DIR, fn)) as f:
            data = json.load(f)
        items = data if isinstance(data, list) else data.get("groups", [])
        out.extend(_group_from_dict(d) for d in items)
    return out


def default_groups() -> List[Group]:
    """The groups a childhood ordinarily involves. Data-driven: data/groups/*.json is
    authoritative if present (a researcher adds a group by adding an entry); otherwise
    the built-in set is used. Attributes are descriptive; nothing about what membership
    does is encoded."""
    data = _load_data_groups()
    return data if data else _builtin_groups()


def _builtin_groups() -> List[Group]:
    return [
        Group("family", "the family", "family", size=4, cohesion=0.8, status=0.5,
              norm_strength=0.6),
        Group("class", "the school class", "class", size=28, cohesion=0.4,
              status=0.5, norm_strength=0.5),
        Group("friends", "a friendship group", "clique", size=6, cohesion=0.7,
              status=0.5, norm_strength=0.6),
        Group("team", "a sports / activity team", "team", size=11, cohesion=0.6,
              status=0.5, norm_strength=0.5),
    ]


# the mix of group moments an ordinary week presents, by rough frequency
DEFAULT_ENCOUNTER_MIX = (
    ("acceptance", 3.0), ("contributing", 2.0), ("status_gain", 1.5),
    ("conformity_pressure", 1.5), ("status_challenge", 1.0),
    ("outgroup_competition", 1.0), ("exclusion", 0.8),
)


def sample_encounter_type(rng: random.Random) -> str:
    kinds = [k for k, _ in DEFAULT_ENCOUNTER_MIX]
    weights = [w for _, w in DEFAULT_ENCOUNTER_MIX]
    return rng.choices(kinds, weights=weights, k=1)[0]

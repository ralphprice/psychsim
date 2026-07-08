"""
environment_matrix.py -- a person's per-THING ledger, the parallel of the Park
relationship matrix for people.

Just as a person accumulates a history with each individual they know (the
relationship matrix: Society of Ties), they accumulate a history with each THING
they encounter -- an object, a pet, a plant, a tree, a food, a place, a stream,
a piece of music. Each encounter runs the thing's presented sensations through
the person's OWN substrate; whichever primary system fires is the felt response,
and it accrues into a running trace of ATTRACTION (drawn to it, sought out) or
AVERSION (repelled, avoided). Over a life this builds an inventory of what a
person seeks out and what they shun -- their favourite places, the nature they
are drawn to, the music and food they love, the things they cannot abide.

Crucially, nothing about what a thing "should" evoke is written in. A thing
merely PRESENTS sensory triggers (a description of what it is, like a situation's
appraisal); whether the person is drawn or repelled EMERGES from their wiring.
Two people can feel oppositely about the same thing, because each responds
through their own substrate -- and the same person's feeling for a thing can
shift as their substrate changes with use. This mirrors, for the world of things,
exactly what the relationship matrix does for people: it registers what happened,
and the disposition is the accumulated trace.
"""

from __future__ import annotations
import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from affective_engine.core import clamp
from affective_engine.interocept import reference_child_state, valence_of_event
from affective_engine.learning import ValueLearner

# How a thing's KIND grounds an innate drive-relevant channel (App. 3.2): food feeds;
# nature (plant/place) reduces arousal/stress; an animal affords affiliative contact; a
# sound soothes. Objects/belongings carry NO innate value -- theirs is learned by
# association (instrumental / extended-self). SCAFFOLD intensities.
_KIND_PERTURBATION = {
    "food":     {"gastric_fill": 1.0},
    "plant":    {"soothing": 0.6},
    "place":    {"soothing": 0.6},
    "creature": {"affiliative_touch": 0.7},
    "sound":    {"soothing": 0.4},
}

# where the data-file environmental inventory lives (repo-root/data/things)
_THINGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "data", "things")


@dataclass
class Thing:
    """Something in the world a person can encounter -- a NEUTRAL container.

    `stimulus` DESCRIBES the sensory triggers the thing presents (novelty, a
    reward cue, a threat, a play signal, comfort, ...), in exactly the vocabulary
    the substrate reads -- like a situation's appraisal describes threat/reward.
    It does NOT encode what the person will feel: the person's systems decide
    that. Supplying a thing's presented sensations is scenario input (a snake
    presents a threat cue; a stream presents gentle novelty); the RESPONSE, and
    hence the attraction or aversion, is the person's own and emerges."""
    id: str
    name: str
    kind: str = "object"      # object | creature | plant | place | food | sound | ...
    stimulus: Dict[str, float] = field(default_factory=dict)
    # inherited (epigenetic) leans present at birth -- a small STARTING bias for
    # evolutionarily-prepared cases (a wariness of predators, say). These are a
    # revisable head-start, NOT a fixed verdict: encounters run through the
    # substrate and can deepen, erode, or overwrite them (a bold child can lose an
    # inherited wariness through exposure). Grounded in prepared-learning findings
    # (e.g. readily-acquired fear of snakes/spiders).
    inherited_aversion: float = 0.0
    inherited_attraction: float = 0.0
    # relative encounter FREQUENCY -- how often this thing is met in ordinary life.
    # High for the mundane (food, screens, other children), low for rare hazards
    # (a snake, a house fire). Real salience is impact (stimulus intensity) x
    # frequency: a car is dangerous AND common; a wild predator, were it here,
    # would be dangerous but vanishingly rare. Frequency weights how often the
    # living world presents the thing, so exposure reflects the real world.
    frequency: float = 1.0
    # optional explicit innate perturbation (interocept triggers) this thing delivers to
    # the body; if empty, derived from `kind` (nature/animal/food grounded, objects learned).
    perturbation: Dict[str, float] = field(default_factory=dict)

    def innate_perturbation(self) -> Dict[str, float]:
        """The innate, drive-relevant channel this thing engages (App. 3.2). Explicit if
        given, else grounded by kind; empty for things whose value must be LEARNED."""
        if self.perturbation:
            return dict(self.perturbation)
        return dict(_KIND_PERTURBATION.get(self.kind, {}))


@dataclass
class Bond:
    """A person's accumulating relationship with ONE thing -- the parallel of a
    Tie. attraction and aversion are running traces that EMERGE from how the
    person's systems responded across encounters; they are not stipulated."""
    thing_id: str
    encounters: int = 0
    attraction: float = 0.0        # drawn toward it (sought out)
    aversion: float = 0.0          # repelled by it (avoided)
    system_counts: Dict[str, int] = field(default_factory=dict)  # which systems fired
    # RPE-learned anticipatory value on the one engine (App. C.9): the predictive value of
    # the thing (+/-) and which drives it is learned to relieve. Distinct from the
    # attraction/aversion traces above, which record the raw emergent responses.
    value: float = 0.0
    value_profile: Dict[str, float] = field(default_factory=dict)

    def disposition(self) -> float:
        """Net pull: +1 strongly sought .. -1 strongly avoided."""
        return self.attraction - self.aversion

    def state(self) -> str:
        d = self.disposition()
        if d >= 0.4:
            return "sought"
        if d >= 0.1:
            return "liked"
        if d <= -0.4:
            return "shunned"
        if d <= -0.1:
            return "disliked"
        return "neutral"


@dataclass
class EnvironmentMatrix:
    """A person's whole ledger of bonds with things -- the parallel of a Society
    of ties, but centred on ONE person and the world of things they meet. The
    inventory of attractions and aversions is read straight off it."""
    bonds: Dict[str, Bond] = field(default_factory=dict)
    learner: ValueLearner = field(default_factory=ValueLearner)  # RPE value store (App. C.9)

    def bond(self, thing_id: str) -> Bond:
        return self.bonds.setdefault(thing_id, Bond(thing_id))

    def disposition_to(self, thing_id: str) -> float:
        b = self.bonds.get(thing_id)
        return b.disposition() if b else 0.0

    def attractions(self, top: Optional[int] = None) -> List[Bond]:
        """The things this person is drawn to -- what they seek out."""
        out = sorted((b for b in self.bonds.values() if b.disposition() > 0),
                     key=lambda b: -b.disposition())
        return out[:top] if top else out

    def aversions(self, top: Optional[int] = None) -> List[Bond]:
        """The things this person is repelled by -- what they avoid."""
        out = sorted((b for b in self.bonds.values() if b.disposition() < 0),
                     key=lambda b: b.disposition())
        return out[:top] if top else out


# how strongly a single encounter moves the attraction/aversion trace. Ledger
# bookkeeping (like the relationship matrix's strain rates), crude and tunable --
# NOT a claim about neural effect.
ACCRUE = 0.15


def encounter(agent, thing: Thing, matrix: EnvironmentMatrix,
              age_years: float = 30.0) -> "object":
    """One encounter with a thing.

    The thing's presented sensations are run through the person's SUBSTRATE; the emergent act IS
    the felt response, and the substrate DEVELOPS through the moment (its own BCM plasticity is
    the use-dependent strengthening -- so what a person keeps being drawn to shapes them). An
    appetitive act (approach/nurture) accrues ATTRACTION; an aversive/aggressive one (avoid/
    seek_comfort/aggress) accrues AVERSION -- in proportion to the emergent drive strength.
    Nothing about what the thing 'should' evoke is written in; it emerges from the wiring, and no
    rule arbitrates the result. Returns the FeltResponse."""
    from substrate.social import felt_response
    fr = felt_response(agent.engine, thing.stimulus, age_years,
                       getattr(agent, "_rest_baseline", None))
    bond = matrix.bond(thing.id)
    bond.encounters += 1
    bond.system_counts[fr.behaviour] = bond.system_counts.get(fr.behaviour, 0) + 1
    if fr.appetitive:
        bond.attraction = clamp(bond.attraction + ACCRUE * fr.strength)
    elif fr.aversive or fr.aggressive:
        bond.aversion = clamp(bond.aversion + ACCRUE * fr.strength)
    # RPE value on the one engine (App. C.9): the reward is the drive reduction this thing's
    # innate channel produces on the state vector (nature soothes, food feeds, ...). Things
    # with no innate channel accrue value only by learned association (r=0 here).
    pert = thing.innate_perturbation()
    if pert:
        r, _, profile = valence_of_event(reference_child_state(), pert)
        matrix.learner.update(thing.id, r, profile)
        bond.value = matrix.learner.value_of(thing.id)
        bond.value_profile = matrix.learner.profile_of(thing.id)
    return fr


# ---------------------------------------------------------------------------
# A small default world -- richer than a sterile stage, not over-engineered.
# The things a child ordinarily meets: a pet, food, the wood, the stream, music,
# and a wild predator. Each PRESENTS a stimulus; a couple carry a small inherited
# (epigenetic) lean at birth that experience then evolves.
# ---------------------------------------------------------------------------

def _thing_from_dict(d: dict) -> Thing:
    return Thing(id=d["id"], name=d.get("name", d["id"]), kind=d.get("kind", "object"),
                 stimulus=dict(d.get("stimulus", {})),
                 inherited_aversion=float(d.get("inherited_aversion", 0.0)),
                 inherited_attraction=float(d.get("inherited_attraction", 0.0)),
                 frequency=float(d.get("frequency", 1.0)))


def _load_data_things() -> List[Thing]:
    """The environmental inventory from data/things/*.json (each file a list, or an
    object with a "things" list). Empty if the directory is absent."""
    out: List[Thing] = []
    if not os.path.isdir(_THINGS_DIR):
        return out
    for fn in sorted(os.listdir(_THINGS_DIR)):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(_THINGS_DIR, fn)) as f:
            data = json.load(f)
        items = data if isinstance(data, list) else data.get("things", [])
        out.extend(_thing_from_dict(d) for d in items)
    return out


def default_things() -> List[Thing]:
    """The world's environmental inventory. Data-driven: if data/things/*.json exists it
    is authoritative (a researcher adds a type by adding an entry); otherwise the built-in
    evidence-based childhood set is used."""
    data = _load_data_things()
    return data if data else _builtin_things()


def _builtin_things() -> List[Thing]:
    """The ordinary things of a childhood world, weighted by REAL salience (impact
    x frequency) from the evidence -- not folk intuition. Feelings are not encoded;
    they emerge. Two grounded principles shape the set:

      * Real hazards are mundane. Traffic and water dominate child-injury mortality
        (road crashes the leading cause worldwide; drowning the leading cause ages
        1-4). Falls, fire and poisoning follow. Stranger-predators are statistically
        negligible (stranger-abduction-homicide odds ~1 in 750,000; most harm to
        children is by known people), so no wild predator or stranger is spawned.

      * Inherited fear is mismatched to modern hazards. Prepared-learning tunes
        inherited wariness to ANCESTRAL threats -- heights, snakes, spiders. The
        high-impact MODERN hazards -- cars, pools, medicines, electricity -- are
        evolutionarily novel and carry NO inherited fear, so a child must learn
        them entirely through exposure and teaching. That gap is exactly why they
        are lethal. So modern hazards below present a strong threat cue but carry
        inherited_aversion = 0, while ancestral ones carry a small inherited lean."""
    return [
        # -- high-frequency mundane exposures (formative by sheer exposure) -------
        Thing("food", "a favourite food", "food",
              {"reward_cue": 0.7, "comfort": 0.5},
              inherited_attraction=0.15, frequency=3.0),
        Thing("screen", "a screen/device", "object",
              {"reward_cue": 0.8, "novelty": 0.6},           # displaces PLAY (Panksepp)
              frequency=3.0),
        Thing("other_children", "other children", "creature",
              {"affiliation": 0.7, "play_signal": 0.6, "novelty": 0.3},
              frequency=2.5),
        Thing("toys", "toys / play things", "object",
              {"play_signal": 0.8, "reward_cue": 0.4}, frequency=2.5),
        Thing("pet_dog", "the family dog", "creature",
              {"vulnerable_other": 0.6, "play_signal": 0.6, "affiliation": 0.6},
              inherited_attraction=0.08, frequency=2.0),
        Thing("music", "music", "sound",
              {"reward_cue": 0.6, "novelty": 0.5}, frequency=2.0),
        Thing("greenspace", "a park / green space", "place",
              {"safety": 0.6, "novelty": 0.4, "affiliation": 0.2}, frequency=1.5),
        Thing("water_play", "a pool / water to play in", "place",
              {"play_signal": 0.6, "novelty": 0.5, "threat": 0.3},  # attractive AND drowning risk
              frequency=1.0),

        # -- real MODERN hazards: high impact, NO inherited fear (must be learned) --
        Thing("road_traffic", "roads and traffic", "object",
              {"threat": 0.8, "novelty": 0.4},               # leading cause of child death
              frequency=2.0),                                 # met daily, no innate wariness
        Thing("fire_stove", "fire / a hot stove", "object",
              {"threat": 0.6, "pain": 0.5}, frequency=0.8),  # burns; pain teaches fast
        Thing("medicine", "medicines / chemicals", "object",
              {"threat": 0.6, "reward_cue": 0.3},            # deceptive: looks like sweets
              frequency=0.5),                                 # why cupboards are child-proofed
        Thing("electrical", "an electrical outlet", "object",
              {"threat": 0.5, "novelty": 0.4}, frequency=0.6),

        # -- ANCESTRAL hazards: inherited fear present (and, for heights, still useful) --
        Thing("height", "a height / stairs", "place",
              {"threat": 0.6, "novelty": 0.3},
              inherited_aversion=0.20, frequency=1.5),        # visual cliff; real fall risk
        Thing("snake_spider", "a snake or spider", "creature",
              {"threat": 0.7, "novelty": 0.4},
              inherited_aversion=0.25, frequency=0.3),        # inherited fear, low real impact
    ]


def birth_matrix(things: Optional[List[Thing]] = None) -> EnvironmentMatrix:
    """A newborn's environment matrix: empty except for the inherited leans some
    things carry (a small prepared wariness of predators, a mild pull toward
    food). These are STARTING biases the substrate then revises through encounter
    -- a bold child can lose the inherited wariness, a fearful one deepen it."""
    things = default_things() if things is None else things
    m = EnvironmentMatrix()
    for t in things:
        if t.inherited_aversion or t.inherited_attraction:
            b = m.bond(t.id)
            b.attraction = clamp(t.inherited_attraction)
            b.aversion = clamp(t.inherited_aversion)
    return m

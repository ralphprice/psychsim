"""
arena.py -- the Arena (Part 6 S12): a small closed micro-world where 2-5 agents live COMPRESSED
lifetimes interacting, so emergent social behaviour can be watched directly. Its standing value is
as a **development-and-regression harness**: run the same Arena with the same seeds before and
after an organism change (a new circuit, a new matrix) and DIFF the behaviour trace.

Built on the substrate-social phase: each slot is an INDEPENDENT AffectiveAgent (its own engine =
the S8.5 independence guarantee), and the agents interact through the substrate social path
(`social_act`) plus their own separate experience streams. A general instrument -- nothing here is
about psychopathy (Part 7 S14.2).

Honesty, held precisely:
  * ENVIRONMENTS ARE PERTURBATION PATTERNS (S12.3). A micro-environment is WHAT IS PRESENT TO
    INTERACT WITH -- a subset of the world's Things, which already carry stimulus dicts in the
    trigger vocabulary ({"reward_cue":0.7,...}), never valences. `escape` is a STRUCTURAL count
    (how many non-social affordances are present to divert to), NEVER a stress multiplier.
    Confinement ("one room") = few things present + low escape = forced, repeated proximity to the
    same other; whether that reads as strain must EMERGE from the substrate's own circuits.
  * THE DYAD TALKS THROUGH A PERCEPTION MAPPING, NOT A TWO-BIT PIPE. The other's emergent act
    becomes self's social perturbation via the vetted perceived-act idiom (speech.acts:
    behaviour -> act -> appraisal_from_act): nurture presents affiliation, aggress presents
    threat/provocation, avoid/seek_comfort present withdrawal/contact-loss. That is a PERCEPTION
    (what the act presents to the senses -- the same category as a Thing's stimulus dict), never a
    valuation. The lossy is_cohesive_act/is_aggressive_act read-outs are used ONLY for tie accrual,
    where they belong.
  * COMPRESSION IS WALL-CLOCK ONLY (S12.5, sacred). E episodes run fast over a REAL childhood span;
    age advances on the real 1/n developmental schedule; the plasticity constants are UNTOUCHED.
    The shared-hours dial is the fraction of episodes that are co-located; the rest is the agent's
    own separate experience stream (the sibling framing, S12.4).
  * THE TRACE DISTINGUISHES EMERGENT DYNAMICS FROM CLOSED-LOOP INSTABILITY (S12.6). Per episode it
    logs each agent's emergent act, max activation, developed-weight drift, and tie strain -- enough
    to tell escalation (acts get aggressive, ties strain, activations stay bounded) from numerical
    instability (activations saturate, acts degenerate).
"""

from __future__ import annotations
from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import math
import random

from affective_engine import AffectiveAgent, TraitSeed
from affective_engine.development import live_stimulus
from affective_engine.activities import sample_activity
from substrate.social import is_cohesive_act, is_aggressive_act, felt_response
from sim_world.environment_matrix import Thing, default_things, birth_matrix, encounter
from sim_world.group_matrix import (GroupMatrix, default_groups, group_encounter,
                                    sample_encounter_type)
from agent_bank import AgentBank

# SCAFFOLD constants (labelled, replace-with-data): initial social presence + tie-accrual step +
# the structural confinement boost. None is a valence or a rate of the plasticity schedule.
_INITIAL_PRESENCE = "approach"     # co-presence, before anyone has acted -- a present, available other
_TIE_STEP = 0.15                   # how fast the (descriptive) tie strain/affect accrues per act
_CONFINE_REF = 3                   # below this many present affordances, forced proximity rises
_CONFINE_BOOST = 0.12              # extra co-located FRACTION per missing affordance (structural)


def intact_seed(name: str = "intact") -> TraitSeed:
    """A neutral, un-throttled temperament: every gain at the reference (0.5), so seed_substrate
    applies NO throttle -- an 'intact' agent (used for the Regime-B stability check)."""
    return TraitSeed(name=name, gains={"THREAT": 0.5, "ANXIETY": 0.5, "SEEKING": 0.5,
                                       "FRUSTRATION": 0.5, "CARE": 0.5, "SOCIAL_LOSS": 0.5,
                                       "CONTROL": 0.5, "INSTRUMENTAL_CONTROL": 0.5})


# ---------------------------------------------------------------------------
# Micro-environments -- WHAT IS PRESENT to interact with (perturbation patterns)
# ---------------------------------------------------------------------------

_ALL_THINGS = {t.id: t for t in default_things()}


def _present(*ids: str) -> List[Thing]:
    # the roster agents ARE the social presence, so environmental Things exclude 'other_children'
    return [_ALL_THINGS[i] for i in ids if i in _ALL_THINGS]


@dataclass(frozen=True)
class MicroEnv:
    """A micro-environment: the Things PRESENT to interact with, plus a documentary note of what it
    affords. `escape` is structural (the count of present non-social affordances), never a tag."""
    name: str
    present: tuple
    note: str = ""

    @property
    def escape(self) -> int:
        return len(self.present)


MICRO_ENVS: Dict[str, MicroEnv] = {
    # a small space with little present and nowhere to divert -- forced proximity (NOT tagged stressful)
    "one_room":     MicroEnv("one_room", tuple(_present("screen", "food")),
                             "a small space, little present, no escape"),
    # an ordinary indoor home: everyday objects and a couple of mundane hazards
    "one_house":    MicroEnv("one_house", tuple(_present("food", "screen", "toys", "music",
                                                         "fire_stove", "height")),
                             "an ordinary indoor home"),
    # home plus outdoor space: room, nature, a pet, water
    "house_garden": MicroEnv("house_garden", tuple(_present("food", "screen", "toys", "music",
                                                            "pet_dog", "greenspace", "water_play",
                                                            "height")),
                             "home plus a garden: space, nature, a pet"),
    # an adult workspace: task objects, few play affordances
    "office":       MicroEnv("office", tuple(_present("screen", "music", "electrical")),
                             "an adult workspace"),
}


# ---------------------------------------------------------------------------
# Slots + the roster
# ---------------------------------------------------------------------------

@dataclass
class Slot:
    """One roster slot: an independent agent + its per-slot source and age. Sources (S12.2):
    a fresh newborn, a system-grown agent, or a banked adult (restored, never edited)."""
    slot_id: str
    source: str = "newborn"                 # "newborn" | "grown" | "banked"
    seed: Optional[TraitSeed] = None        # temperament for newborn/grown (defaults to intact)
    age: float = 0.5                        # spawn age (years)
    grow_years: float = 18.0                # "grown": how far to develop it before the Arena
    bank: Optional[AgentBank] = None        # "banked": the bank + id to restore from
    bank_id: Optional[str] = None


@dataclass
class ArenaSpec:
    micro_env: str
    slots: List[Slot]
    seed: int = 0
    shared_hours: float = 3.0               # co-located hours/day (the sibling dial, S12.4)


# ---------------------------------------------------------------------------
# The trace -- the closed-system watch (S12.6)
# ---------------------------------------------------------------------------

@dataclass
class ArenaTrace:
    spec: ArenaSpec
    records: List[dict] = field(default_factory=list)

    def record(self, episode, age, acts, max_act, drift, strain):
        self.records.append({"episode": episode, "age": round(age, 3), "acts": dict(acts),
                             "max_act": dict(max_act), "drift": dict(drift), "strain": dict(strain)})

    def act_counts(self) -> Counter:
        c = Counter()
        for r in self.records:
            c.update(r["acts"].values())
        return c

    def signature(self) -> tuple:
        """A deterministic behaviour signature for the regression diff (same seeds before/after an
        organism change -> compare). The per-episode emergent acts, in order."""
        return tuple((r["episode"], tuple(sorted(r["acts"].items()))) for r in self.records)

    def peak_activation(self) -> float:
        """The highest single-circuit activation any agent reached -- the saturation signal. Since
        the engine clamps to [0,1], 'blow-up' shows as this pinning near 1.0, not as unbounded growth."""
        return max((max(r["max_act"].values()) for r in self.records if r["max_act"]), default=0.0)

    def viable(self, saturation_ref: float = 0.95) -> bool:
        """Viable = no agent is driven into PERSISTENT saturation (the closed-loop failure mode).
        The integrator clamps activations/weights to [0,1], so instability shows as PINNING near
        the ceiling, never as unbounded growth -- a momentary ceiling touch is normal, a blown-up
        loop keeps activations pinned. So we check each agent's LATER-portion mean max-activation,
        not a single peak."""
        if not self.records:
            return True
        tail_recs = self.records[len(self.records) // 2:]
        for aid in self.records[0]["max_act"]:
            xs = [r["max_act"][aid] for r in tail_recs if aid in r["max_act"]]
            if xs and sum(xs) / len(xs) > saturation_ref:
                return False
        return True

    def settled(self, tail: float = 0.5, osc_ref: float = 0.20) -> bool:
        """Regime-B (Part 5 S9.3): over the LATER portion of the run, each agent's max-activation
        has SETTLED -- low variance, not oscillating. A closed loop that drove agents into
        oscillation would show high tail variance here."""
        if len(self.records) < 4:
            return True
        cut = int(len(self.records) * (1.0 - tail))
        tail_recs = self.records[cut:]
        for aid in self.records[0]["max_act"]:
            xs = [r["max_act"][aid] for r in tail_recs if aid in r["max_act"]]
            if len(xs) >= 2:
                mu = sum(xs) / len(xs)
                var = sum((x - mu) ** 2 for x in xs) / len(xs)
                if math.sqrt(var) > osc_ref:
                    return False
        return True


# ---------------------------------------------------------------------------
# Building agents + the two kinds of episode
# ---------------------------------------------------------------------------

def _new_ctx(present: tuple) -> dict:
    things = list(present)
    return {"things": things, "env_matrix": birth_matrix(things or None),
            "group_matrix": GroupMatrix(), "groups": default_groups()}


def _solo_episode(agent: AffectiveAgent, age_years: float, rng: random.Random, ctx: dict) -> str:
    """The agent's OWN separate experience stream (the non-shared part of the day): an
    age-appropriate activity, an encounter with a present thing, and a moment in a group. The
    substrate develops through it under the real plasticity schedule. Returns the emergent act of
    the group moment (a non-social-toward-the-roster act, recorded for the trace)."""
    act = sample_activity(age_years, rng)
    live_stimulus(agent, act.stimulus, age_years=age_years)
    if ctx["things"]:
        thing = rng.choices(ctx["things"], weights=[t.frequency for t in ctx["things"]], k=1)[0]
        encounter(agent, thing, ctx["env_matrix"], age_years=age_years)
    grp = rng.choice(ctx["groups"])
    mem = ctx["group_matrix"].membership(grp.id, grp.kind)
    return group_encounter(agent, grp, mem, sample_encounter_type(rng), age_years=age_years).behaviour


# What the OTHER's emergent act physically PRESENTS to a perceiver's senses -- in the trigger
# vocabulary Things use (a stimulus dict, e.g. {"affiliation":0.7}), never a valuation of what the
# act MEANS or how bad it is. Same category as a Thing's stimulus. This is the resolved perception
# channel the dyad talks through -- richer than the two-bit is_cohesive/is_aggressive read-outs
# (which are kept only for tie accrual). Precedent: speech.acts' "hearer appraises the perceived
# act". SCAFFOLD intensities. Unknown acts present a faint co-presence.
_ARENA_PERCEPTION: Dict[str, Dict[str, float]] = {
    "nurture":      {"affiliation": 0.7, "vulnerable_other": 0.3},  # caregiving: warmth + tending
    "approach":     {"affiliation": 0.5},                           # a friendly appetitive bid
    "play":         {"affiliation": 0.4, "play_signal": 0.5},
    "court":        {"affiliation": 0.6},
    "aggress":      {"thwarting": 0.7, "threat": 0.3},              # an attack: provocation + threat
    "avoid":        {"separation": 0.4},                           # the other pulling away: contact-loss
    "seek_comfort": {"vulnerable_other": 0.6, "separation": 0.2},   # a distressed other, a contact bid
    "restrain":     {"affiliation": 0.1},                          # present, holding back: faint co-presence
}


def _perceive(other_act: str) -> Dict[str, float]:
    """The perturbation the other's act presents to this agent -- a perception in the trigger
    vocabulary, not a valuation. Fed through felt_response, the same path Things use."""
    return dict(_ARENA_PERCEPTION.get(other_act, {"affiliation": 0.1}))


@dataclass
class _Tie:
    affect: float = 0.0
    strain: float = 0.0


def _social_episode(agent: AffectiveAgent, other_last_act: str,
                    tie: _Tie, age_years: float) -> str:
    """One co-located moment: THIS agent perceives the other's prior act as a social perturbation
    (in the trigger vocabulary) and its substrate resolves an emergent act, developing through the
    moment. The DESCRIPTIVE tie accrues from the feature read-outs of that act (where the two
    booleans belong)."""
    fr = felt_response(agent.engine, _perceive(other_last_act), age_years,
                       getattr(agent, "_rest_baseline", None))
    if is_aggressive_act(fr.behaviour):
        tie.strain = min(1.0, tie.strain + _TIE_STEP); tie.affect = max(-1.0, tie.affect - _TIE_STEP)
    elif is_cohesive_act(fr.behaviour):
        tie.strain = max(0.0, tie.strain - _TIE_STEP); tie.affect = min(1.0, tie.affect + _TIE_STEP)
    return fr.behaviour


def _build_agent(slot: Slot, rng: random.Random, present: tuple) -> AffectiveAgent:
    if slot.source == "banked":
        if slot.bank is None or slot.bank_id is None:
            raise ValueError(f"banked slot '{slot.slot_id}' needs bank + bank_id")
        ag = AffectiveAgent(seed=slot.seed or intact_seed())
        ag.adopt_engine(slot.bank.restore(slot.bank_id).engine)   # stage-4b placement; restored, never edited
        return ag
    ag = AffectiveAgent(seed=slot.seed or intact_seed())
    if slot.source == "grown":
        ctx = _new_ctx(present)
        n = max(6, int(round(slot.grow_years * 3.0)))
        for i in range(n):
            _solo_episode(ag, slot.grow_years * i / n, rng, ctx)   # age it forward via its own stream
    return ag


# ---------------------------------------------------------------------------
# The Arena run
# ---------------------------------------------------------------------------

def _pair(a: str, b: str) -> tuple:
    return tuple(sorted((a, b)))


def run_arena(spec: ArenaSpec, *, childhood_years: float = 18.0,
              episodes_per_year: float = 3.0) -> ArenaTrace:
    """Run the Arena: a compressed childhood in which the roster shares `shared_hours`/day and lives
    its own stream the rest. Deterministic from spec.seed (the regression-harness property)."""
    if not (2 <= len(spec.slots) <= 5):
        raise ValueError("Arena roster must be 2-5 agents (S12.2)")
    env = MICRO_ENVS[spec.micro_env]
    rng = random.Random(spec.seed)

    agents: Dict[str, AffectiveAgent] = {}
    births: Dict[str, list] = {}
    last_act: Dict[str, str] = {}
    for slot in spec.slots:
        ag = _build_agent(slot, rng, env.present)
        agents[slot.slot_id] = ag
        births[slot.slot_id] = list(ag.engine.weight)
        last_act[slot.slot_id] = _INITIAL_PRESENCE
    ids = list(agents)
    ctxs = {iid: _new_ctx(env.present) for iid in ids}
    ties: Dict[tuple, _Tie] = {}

    # the co-located FRACTION: the sibling dial (shared_hours/day) plus a STRUCTURAL confinement
    # boost when few affordances are present (fewer diversions -> more forced proximity). Escape is
    # a count; it shifts the social/solo MIX, it never scales a perturbation's intensity.
    confine = _CONFINE_BOOST * max(0, _CONFINE_REF - env.escape)
    shared_frac = max(0.0, min(1.0, spec.shared_hours / 24.0 + confine))

    E = max(len(ids) + 2, int(round(childhood_years * episodes_per_year)))
    trace = ArenaTrace(spec)
    for i in range(E):
        age = childhood_years * i / E
        acts, max_act, drift = {}, {}, {}
        for iid in ids:
            ag = agents[iid]
            others = [o for o in ids if o != iid]
            if others and rng.random() < shared_frac:
                other = rng.choice(others)
                tie = ties.setdefault(_pair(iid, other), _Tie())
                b = _social_episode(ag, last_act[other], tie, age)
                last_act[iid] = b                       # the perceivable social act toward the roster
            else:
                b = _solo_episode(ag, age, rng, ctxs[iid])   # own stream; not perceivable as a social bid
            acts[iid] = b
            max_act[iid] = max(ag.engine.activation.values()) if ag.engine.activation else 0.0
            drift[iid] = _drift(ag.engine.weight, births[iid])
        trace.record(i, age, acts, max_act, drift, {p: t.strain for p, t in ties.items()})
    return trace


def _drift(weights, birth) -> float:
    return round(math.sqrt(sum((w - b) ** 2 for w, b in zip(weights, birth))), 4)

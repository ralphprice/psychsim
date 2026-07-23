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
from affective_engine.physical import physical_stimulus, sex_weight
from affective_engine.signature import signature_match
from affective_engine.activities import sample_activity
from substrate.social import is_cohesive_act, is_aggressive_act, felt_response, rest_activation
from sim_world.environment_matrix import Thing, default_things, birth_matrix, encounter
from sim_world.group_matrix import (GroupMatrix, default_groups, group_encounter,
                                    sample_encounter_type)
from sim_world.gamemaster import Relationship, accrue_relationship   # dev-social integration (F1/F3)
from agent_bank import AgentBank

# SCAFFOLD constants (labelled, replace-with-data): initial social presence + tie-accrual step +
# the structural confinement boost. None is a valence or a rate of the plasticity schedule.
_INITIAL_PRESENCE = "approach"     # co-presence, before anyone has acted -- a present, available other
_TIE_STEP = 0.15                   # how fast the (descriptive) tie strain/affect accrues per act
# v14 Expression Phase C: what an agent in distress DISPLAYS is its EFFERENT motor output -- the FACE
# (NuFac) and the VOICE (NuAmb-vocal), the emotional-expression effectors -- NOT its internal affective
# circuits (a co-located perceiver cannot see a CeA; the old (CeA, vlPAG, BA) display was reading the
# drive, not the expression). Each effector is presented on the sense that picks it up: the face is
# SEEN, the cry is HEARD. Read above the bearer's FIXED rest activation (rest_activation), never the
# running mean_activity -- so a CHRONICALLY distressed face stays visible (the running mean adapts to
# sustained distress and hides it: the v14 'chronic distress goes invisible' flag, closed here at
# source). Efferent + terminal + perceived-through-the-right-sense = the honest display. Each entry is
# (effector circuit, the perception-channel trigger it presents on). Anatomy, not a valuation.
_DISTRESS_DISPLAY = (("NuFac", "displayed_distress_face"),
                     ("NuAmb-vocal", "displayed_distress_cry"))
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
    relational: bool = False                # dev-social integration (F3): OFF = the descriptive _Tie
                                            # accrual (byte-identical regression harness); ON = the
                                            # canonical gm.rel written by accrue_relationship (P2a) and
                                            # read back into perception as an IN-CONSPEC recognition cue


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
# act". Unknown acts present a faint co-presence.
#
# SCAFFOLD (calibration targets, replace-with-data): the STRUCTURE -- which act presents which
# trigger channel -- is grounded in perception (an attack presents provocation/threat, caregiving
# presents affiliation, withdrawal presents contact-loss). The STRENGTHS below are placeholders,
# not yet calibrated. (Routing acts through the speech INTENTS was rejected in review: it collapsed
# approach->ASSERT, whose appraisal dims appraisal_to_substrate_input ignores, so a warm approach
# presented NOTHING -- a silent null the Arena surfaced on day one; see the core record.)
_ARENA_PERCEPTION: Dict[str, Dict[str, float]] = {   # SCAFFOLD strengths
    "nurture":      {"affiliation": 0.7, "vulnerable_other": 0.3},  # caregiving: warmth + tending
    "approach":     {"affiliation": 0.5},                           # a friendly appetitive bid
    "play":         {"affiliation": 0.4, "play_signal": 0.5},
    "court":        {"affiliation": 0.6},
    "aggress":      {"thwarting": 0.7, "threat": 0.3},              # an attack: provocation + threat
    # ROUTE 1 (harsh-mirror link 1, RULED): being AVOIDED is social rejection, and social rejection is the
    # most-replicated aggression elicitor in the literature (Twenge 2001; Warburton 2006; childhood
    # peer-rejection -> later aggression) -- it requires NO prior aggression, which is what breaks the
    # bootstrap (previously only the "aggress" act carried provocation, so aggression was perceivable only
    # once it existed). Being pulled away from therefore presents contact-loss AND provocation. This is
    # PRESENT-not-assign (the F2 keystone): the rejection is presented; the perceiver's own selector decides
    # whether to aggress, absorb, or withdraw. `thwarting` 0.3 is SCAFFOLD -- deliberately milder than an
    # assault's 0.7 (rejection is an aversive social stimulus, not a physical attack) -- and NOT tuned to a
    # wanted outcome: the emergent act is MEASURED, and a sub-threshold value is reported as a finding, not
    # cranked. See the harsh-mirror link-1 register entry.
    "avoid":        {"separation": 0.4, "thwarting": 0.3},          # being rejected: contact-loss + provocation
    "seek_comfort": {"vulnerable_other": 0.6, "separation": 0.2},   # a distressed other, a contact bid
    "restrain":     {"affiliation": 0.1},                          # present, holding back: faint co-presence
}


def _perceive(other_act: str) -> Dict[str, float]:
    """The perturbation the other's act presents to this agent -- a perception in the trigger
    vocabulary, not a valuation. Fed through felt_response, the same path Things use."""
    return dict(_ARENA_PERCEPTION.get(other_act, {"affiliation": 0.1}))


def _add_physical_percept(percept: Dict[str, float], perceiver: AffectiveAgent,
                          bearer: AffectiveAgent) -> None:
    """E2/E4: the bearer's physical endowment also presents as a conspecific percept -- an
    `attractive_face` and a `formidability_cue`, BEARER-PURE magnitudes (E2) valued by THIS perceiver
    through a genuine sex PAIRING (perceiver x bearer, E4). Merged into the same percept dict fed to
    felt_response, which routes these triggers via the IN-CONSPEC edges into the perceiver's OWN
    reward / defensive circuits -- the keystone: the response emerges from the perceiver's circuits,
    never a coded trait->outcome weight. A physical-neutral bearer presents nothing; an unknown sex
    pairing values neutrally (0.5). What this differential develops into is measured, not coded."""
    bearer_physical = getattr(bearer, "physical", None)
    if not bearer_physical:
        return
    perceiver_sex, bearer_sex = getattr(perceiver, "sex", None), getattr(bearer, "sex", None)
    for cue, mag in physical_stimulus(bearer_physical).items():          # E2: bearer-pure stimulus
        percept[cue] = percept.get(cue, 0.0) + mag * sex_weight(perceiver_sex, bearer_sex, cue)  # E4


def _add_signature_percept(percept: Dict[str, float], perceiver: AffectiveAgent,
                           bearer: AffectiveAgent) -> None:
    """v14 Phase-2 (kinship): the bearer's genetic-fingerprint signature presents as a kin-recognition
    cue -- `signature_match(bearer.signature, perceiver.self_signature)`, a SELF-REFERENT similarity in
    [0,1] the PERCEIVER computes ("does this conspecific smell like me?", the armpit effect / Mateo &
    Johnston 2000). Merged into the same percept dict fed to felt_response, which routes it via the
    IN-CONSPEC:kin_signature edge into the perceiver's OWN oxytocin system (-> the Phase-1 bonding
    scaffold). The KEYSTONE: the cue is self-similarity -- a function of the two signature vectors ONLY
    -- NOT relatedness (relatedness set the shared loci at spawn and never appears here). Nepotism
    EMERGES from the perceiver's circuits valuing self-similarity (OT -> bonding), never a coded
    similarity->affiliation coefficient. A signature-neutral bearer or perceiver presents nothing."""
    bearer_sig = getattr(bearer, "signature", None)
    perceiver_sig = getattr(perceiver, "self_signature", None)
    if not bearer_sig or not perceiver_sig:
        return
    match = signature_match(bearer_sig, perceiver_sig)                   # self-referent, signature-only
    if match > 0.0:
        percept["kin_signature"] = percept.get("kin_signature", 0.0) + match


def _add_consequence_percept(percept: Dict[str, float], perceiver: AffectiveAgent,
                             bearer: AffectiveAgent) -> None:
    """v14 (vicarious routing) + Phase C (the display is the EFFECTOR output): the CONSEQUENCE that
    befell the other is presented to this agent as a PHYSICAL FACT through channels that already
    exist. An agent in distress DISPLAYS it on its emotional-expression EFFECTORS -- the FACE
    (`NuFac`) and the VOICE (`NuAmb-vocal`), the efferent motor output a perceiver can actually
    sense, NOT the internal affective circuits (a co-located perceiver cannot see a CeA). The
    perceiver's distal senses pick that display up on SEPARATE limbs: the face is SEEN
    (`displayed_distress_face` -> IN-VIS:face_like -> SC-Pv -> CeA), the cry is HEARD
    (`displayed_distress_cry` -> IN-AUD:voice -> A1-belt -> LA -> CeA). The two routes DIFFER by
    modality (a short subcortical road for the face, a longer cortical one for the cry) -- emergent,
    not coded; and the bearer-side dissociation (pain drives the face, separation drives the voice)
    means each consequence tends to present on its own limb.

    Read each effector's output ABOVE THE BEARER'S FIXED REST activation (`rest_activation`), never
    the running mean_activity: a face at rest displays nothing (activation ~= rest), and a
    displaced face displays its displacement ACUTE OR CHRONIC. The fixed reference is what keeps a
    CHRONICALLY distressed face visible -- the running mean adapts to sustained distress and would
    hide it (the v14 'chronic distress goes invisible' flag, closed here at source).

    NO vicarious<direct gain term and NO chosen cue intensity: the display magnitude IS the bearer's
    evoked effector output; whatever response results in the perceiver is what results, MEASURED not
    assumed. The perceiver's response emerges from its OWN circuits (felt_response). The route is the
    DISTAL/AFFECTIVE one only -- neither the seen face nor the heard cry carries the
    sensory-discriminative component direct pain has (IN-SOMATO:nociception -> VPL -> S1/S2), which
    is the structural whole of the vicarious/direct difference. A bearer at rest displays nothing."""
    eng = getattr(bearer, "engine", None)
    if eng is None:
        return
    rest = rest_activation(eng.model, eng.age_years, eng.throttle)
    total_displayed = 0.0
    for effector, trigger in _DISTRESS_DISPLAY:
        if not eng.live_circuit.get(effector, False):
            continue
        # the effector's output above the bearer's FIXED rest -- the face/voice displaced from neutral
        displayed = (eng.activation.get(effector, 0.0) - rest.get(effector, 0.0)) * eng._gain(effector)
        if displayed > 0.0:
            d = min(1.0, displayed)
            percept[trigger] = percept.get(trigger, 0.0) + d
            total_displayed += d
    # ROUTE 2 (harsh-mirror link 1, RULED -- the Berkowitz route, and the LOAD-BEARING one). Route 1
    # (avoid->provocation) measured as a no-op because the "avoid" ACT never occurs in the cohort exchange
    # (the mix is locked to nurture/approach/restrain); only graded DISTRESS DISPLAY varies with harshness,
    # so this is where provocation must enter. Berkowitz's reformulation: aversive events produce aggressive
    # inclinations to the extent they produce NEGATIVE AFFECT -- another's displayed distress IS an aversive
    # social stimulus. So the SAME display that presents vicarious distress (empathy, above) ALSO presents
    # provocation. PRESENT-not-assign (F2 keystone): the aversive display is presented; the perceiver's own
    # circuits value it, and its selector decides empathy (CARE) vs aggression -- nothing is written. The
    # 0.5 scale is SCAFFOLD (a display is a milder provocation than a direct attack's 0.7) and is NOT tuned
    # to a wanted outcome: the emergent act is MEASURED; sub-threshold or flooding are reported, not cranked.
    if total_displayed > 0.0:
        percept["thwarting"] = percept.get("thwarting", 0.0) + min(1.0, 0.5 * total_displayed)


@dataclass
class _Tie:
    affect: float = 0.0
    strain: float = 0.0


def _add_relationship_percept(percept: Dict[str, float], rel: Relationship) -> None:
    """dev-social integration (F2, the emergence keystone): the perceiver's stored relationship with
    THIS specific known other presents as an IN-CONSPEC RECOGNITION cue -- recognised as warm
    (familiar_warm -> PVN-OT, oxytocin/approach) or as a threat (familiar_wary -> CeA, defensive). The
    P1 colouring math IN ROLE: FAMILIARITY gates the whole cue (a stranger, familiarity 0, presents
    nothing), the SIGN of stored affect selects the arm, low trust adds to wariness. It presents
    RECOGNITION, NEVER a valuation written onto the affordance channels -- the perceiver's own circuits
    value it (Fork-2 correction; the same discipline as the kin_signature / physical cues). Non-negative
    channels force TWO arms. Gains mirror the P1 read (affect 0.5, trust 0.3); SCAFFOLD."""
    w = rel.familiarity                       # already in [0,1] (accrue clamps); a stranger presents nothing
    if w <= 0.0:
        return
    warm = 0.5 * w * max(0.0, rel.affect)
    wary = 0.5 * w * max(0.0, -rel.affect) + 0.3 * w * (1.0 - rel.trust)
    if warm > 0.0:
        percept["familiar_warm"] = min(1.0, percept.get("familiar_warm", 0.0) + warm)
    if wary > 0.0:
        percept["familiar_wary"] = min(1.0, percept.get("familiar_wary", 0.0) + wary)


def _strain_of(rel: Relationship) -> float:
    """The relationship-ON trace's `strain` is a derived VIEW of the canonical gm.rel (F3): the _Tie is
    demoted to a projection, not an independent store. Strain rises with negative affect and low trust."""
    return max(0.0, min(1.0, 0.5 * max(0.0, -rel.affect) + 0.5 * (1.0 - rel.trust)))


def _social_episode(agent: AffectiveAgent, other_agent: AffectiveAgent, other_last_act: str,
                    tie, age_years: float, relational: bool = False) -> str:
    """One co-located moment: THIS agent perceives the other's prior act AND physical presentation as
    a social perturbation (in the trigger vocabulary) and its substrate resolves an emergent act,
    developing through the moment.

    relational=False (harness default): the DESCRIPTIVE tie accrues from the feature read-outs of that
    act (where the two booleans belong) -- the byte-identical regression path. relational=True: `tie` is
    a canonical gm.rel Relationship; the perceiver's history with this other first COLOURS the percept as
    an IN-CONSPEC recognition cue (F2 read), then the emergent act WRITES the tie via the shared P2a
    accrue_relationship mechanism (F1 write). History shapes behaviour ONLY by re-entering perception."""
    percept = _perceive(other_last_act)
    _add_physical_percept(percept, agent, other_agent)   # E2/E4: the other's endowment, sex-valued
    _add_signature_percept(percept, agent, other_agent)  # v14: the other's kin signature, self-matched
    _add_consequence_percept(percept, agent, other_agent)  # v14: the other's DISPLAYED evoked distress
    if relational:
        _add_relationship_percept(percept, tie)          # F2: the perceiver's history, as a recognition cue
    fr = felt_response(agent.engine, percept, age_years,
                       getattr(agent, "_rest_baseline", None))
    if relational:
        accrue_relationship(tie, fr.behaviour, fr.strength)   # F1/P2a: the SAME emergent write as adjudicate
    elif is_aggressive_act(fr.behaviour):
        tie.strain = min(1.0, tie.strain + _TIE_STEP); tie.affect = max(-1.0, tie.affect - _TIE_STEP)
    elif is_cohesive_act(fr.behaviour):
        tie.strain = max(0.0, tie.strain - _TIE_STEP); tie.affect = min(1.0, tie.affect + _TIE_STEP)
    return fr.behaviour


def _build_agent(slot: Slot, rng: random.Random, present: tuple) -> AffectiveAgent:
    if slot.source == "banked":
        if slot.bank is None or slot.bank_id is None:
            raise ValueError(f"banked slot '{slot.slot_id}' needs bank + bank_id")
        ag = AffectiveAgent(seed=slot.seed or intact_seed())
        # restored, never edited -- reload the whole banked adult (developed substrate AND its given
        # physical endowment + sex), not just the engine, so physical is preserved not re-sampled (v10 E1).
        ag.adopt_developed(slot.bank.restore(slot.bank_id))       # stage-4b placement
        return ag
    ag = AffectiveAgent(seed=slot.seed or intact_seed())
    if slot.source == "grown":
        ctx = _new_ctx(present)
        n = max(6, int(round(slot.grow_years * 3.0)))
        dt_step = slot.grow_years / n                 # TIME-NORMALISATION: each solo aging-step spans grow_years/n
        for i in range(n):
            with ag.engine.developmental_dt(dt_step):
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
    ties: Dict[tuple, _Tie] = {}                   # rel-off: descriptive per-UNORDERED-pair tie
    rels: Dict[tuple, Relationship] = {}           # rel-on (F3): canonical gm.rel per DIRECTED pair

    # the co-located FRACTION: the sibling dial (shared_hours/day) plus a STRUCTURAL confinement
    # boost when few affordances are present (fewer diversions -> more forced proximity). Escape is
    # a count; it shifts the social/solo MIX, it never scales a perturbation's intensity.
    confine = _CONFINE_BOOST * max(0, _CONFINE_REF - env.escape)
    shared_frac = max(0.0, min(1.0, spec.shared_hours / 24.0 + confine))

    E = max(len(ids) + 2, int(round(childhood_years * episodes_per_year)))
    dt_episode = childhood_years / E              # TIME-NORMALISATION: real developmental years ONE arena
    #     episode-slice represents. Applied to EVERY settle in the slice (a solo episode fires three --
    #     activity/thing/group -- as concurrent facets, each carrying dt_episode), so accrual tracks the
    #     18-yr childhood, not the episode count E. Makes drift episode-count-independent (F3 re-measured).
    trace = ArenaTrace(spec)
    for i in range(E):
        age = childhood_years * i / E
        acts, max_act, drift = {}, {}, {}
        for iid in ids:
            ag = agents[iid]
            others = [o for o in ids if o != iid]
            with ag.engine.developmental_dt(dt_episode):
                if others and rng.random() < shared_frac:
                    other = rng.choice(others)
                    if spec.relational:
                        # directed: how iid regards other (read + written); F1/F2/F3
                        rel = rels.setdefault((iid, other), Relationship())
                        b = _social_episode(ag, agents[other], last_act[other], rel, age, relational=True)
                    else:
                        tie = ties.setdefault(_pair(iid, other), _Tie())
                        b = _social_episode(ag, agents[other], last_act[other], tie, age)
                    last_act[iid] = b                   # the perceivable social act toward the roster
                else:
                    b = _solo_episode(ag, age, rng, ctxs[iid])   # own stream; not perceivable as a social bid
            acts[iid] = b
            max_act[iid] = max(ag.engine.activation.values()) if ag.engine.activation else 0.0
            drift[iid] = _drift(ag.engine.weight, births[iid])
        strain = ({p: _strain_of(r) for p, r in rels.items()} if spec.relational
                  else {p: t.strain for p, t in ties.items()})   # rel-on: strain is a derived VIEW (F3)
        trace.record(i, age, acts, max_act, drift, strain)
    return trace


def _drift(weights, birth) -> float:
    return round(math.sqrt(sum((w - b) ** 2 for w, b in zip(weights, birth))), 4)

"""
observer.py -- the observer read-out (docs/PsychSim_MASTER.md App. D.2).

This is where the OUTPUT CATEGORIES legitimately live -- "boldness", "meanness",
"disinhibition", "callous-unemotional", "empathy", "reactive vs instrumental aggression",
"psychopathy". They are computed *over* an agent (its behaviour and substrate activity), by
US, for reporting and validation, and are NEVER fed back into the mechanism. This completes
the substrate principle that named systems are read-outs, not primitives.

Engine-agnostic BY DESIGN: the metrics are computed from a neutral BehaviourProfile of
measurable signals, so the read-out does not depend on how the behaviour was produced. The
adapter that builds a BehaviourProfile is `profile_from_substrate` -- the substrate is the
sole engine since the Panksepp retirement (stage 5), and the earlier legacy-brain adapter is
gone. Nothing here is a verdict on the agent -- it is measurement; whether any label is apt is
a separate interpretive question.

All construct weightings are SCAFFOLD.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict

from .core import clamp


@dataclass
class BehaviourProfile:
    """Neutral, engine-agnostic measurements over an agent. Either substrate produces one;
    the observer computes constructs from it. Values in [0,1] unless noted."""
    fear: float = 0.5                    # threat-system reactivity/strength (read-out)
    seeking: float = 0.5                 # appetitive approach
    care: float = 0.5                    # affiliative / empathic-concern strength
    restraint: float = 0.5               # executive / conscience-linked inhibitory capacity
    moral_orientation: float = 0.5       # affective conscience (Blair; care-based)
    reactive_aggression: float = 0.0     # hot, retaliatory, poorly-governed hostility
    instrumental_aggression: float = 0.0  # cold, calculated exploitation
    vicarious_response: float = 0.5      # response to others' distress (empathy signal)
    punishment_sensitivity: float = 0.5  # learning from punishment (low = reward-dominant)


# ---------------------------------------------------------------------------
# The construct metrics (measured; never fed back)
# ---------------------------------------------------------------------------

def triarchic(bp: BehaviourProfile) -> Dict[str, float]:
    """The triarchic dimensions (Patrick, Fowles & Krueger 2009), measured over the agent."""
    boldness = clamp(0.6 * (1.0 - bp.fear) + 0.4 * bp.seeking)
    meanness = clamp(0.4 * (1.0 - bp.care) + 0.4 * bp.instrumental_aggression
                     + 0.2 * (1.0 - bp.vicarious_response))
    disinhibition = clamp(0.6 * (1.0 - bp.restraint) + 0.4 * bp.reactive_aggression)
    return {"boldness": boldness, "meanness": meanness, "disinhibition": disinhibition}


def empathy(bp: BehaviourProfile) -> float:
    """Empathic concern: vicarious response to another's distress + care-based moral orientation.

    ★ RE-INSTATED (vicarious-pathway build, RULED) after suspension. The vicarious pathway was built and
    grounded on ANATOMY (colliculo-pulvinar->extrastriate; auditory belt->STS; lamina-I spinothalamic->VMpo->
    insula) so the distress-perception channels now reach the shared-affect nodes, and `vicarious_response` is
    re-derived on the nodes that MEASURABLY carry the vicarious signal -- aIns/MeA/dACC (see _OBS_EMPATHY), not
    the own-pain-dominant amygdala nodes that made the old measure read own-pain.

    ★ CAVEAT THAT TRAVELS WITH THE CONSTRUCT (do not strip): the underlying signal is WEAK -- the distress
    response at aIns is +0.016 (multi-hop cortical attenuation), and the weight was NOT tuned to inflate it.
    Therefore: claims using empathy are WITHIN-CONFIGURATION comparisons only; absolute magnitudes are NOT
    quotable. Re-instated on a weak-but-real signal with the weakness stated -- pre-registered criterion met
    (reach +0.0475, ratio 2.26x own/other vs the 6.6x baseline, MeA specificity clean). See the register."""
    return clamp(0.5 * bp.vicarious_response + 0.5 * bp.moral_orientation)


def callous_unemotional(bp: BehaviourProfile) -> float:
    """Callous-unemotional traits (Frick): blunted empathy + weak affective conscience. ★ CU IS THE EXACT
    COMPLEMENT of `empathy` (CU = 1 - empathy -- the SAME variable, written as the explicit complement so a
    figure cannot present one variable as two). RE-INSTATED with `empathy`; inherits its WEAK-SIGNAL CAVEAT
    (within-configuration comparisons only, absolute magnitudes not quotable)."""
    return clamp(1.0 - empathy(bp))


def aggression_profile(bp: BehaviourProfile) -> Dict[str, float]:
    """Reactive vs instrumental aggression (the classic distinction)."""
    return {"reactive": clamp(bp.reactive_aggression),
            "instrumental": clamp(bp.instrumental_aggression)}


def passive_avoidance_deficit(bp: BehaviourProfile) -> float:
    """The classic psychopathy learning signature: poor learning from punishment / reward
    dominance (high = worse punishment learning)."""
    return clamp(1.0 - bp.punishment_sensitivity)


def read_out(bp: BehaviourProfile) -> Dict[str, object]:
    """The full observer read-out over an agent. A MEASUREMENT, never fed back. Deliberately
    returns no single 'psychopathy' verdict -- that is the thesis's interpretive question,
    computed from these constructs, not decided in the mechanism."""
    tri = triarchic(bp)
    return {
        "triarchic": tri,
        # ★ RE-INSTATED (vicarious-pathway build, RULED). empathy/CU were suspended when the affective-empathy
        # read-out was found to measure own-pain 6.6x (no vicarious pathway existed). The pathway was built and
        # grounded on anatomy; `vicarious_response` is now re-derived on the nodes that measurably carry the
        # vicarious signal (aIns/MeA/dACC -- see _OBS_EMPATHY). WEAK-SIGNAL CAVEAT travels with the construct
        # (see empathy()): within-configuration comparisons only, absolute magnitudes not quotable.
        "callous_unemotional": callous_unemotional(bp),
        "empathy": empathy(bp),
        "aggression": aggression_profile(bp),
        "passive_avoidance_deficit": passive_avoidance_deficit(bp),
    }


def observe_agent(agent) -> Dict[str, object]:
    """Convenience: the full observer read-out over an agent (its developed substrate). Duck-
    typed: an agent carrying `.engine`, or an engine. The circuit-engine adapter
    (profile_from_substrate) has superseded the retired legacy-brain adapter."""
    return observe_substrate(getattr(agent, "engine", agent))


# ---------------------------------------------------------------------------
# Circuit-engine adapter (Part 6 substrate-social phase) -- READ-ONLY
# ---------------------------------------------------------------------------

# The circuit populations each measured construct is read from (anatomy). These are MEASUREMENT
# probes over emergent activity -- the same read-out idiom as study.py -- never fed back.
_OBS_THREAT = ("CEl", "vlPAG", "BA", "LA")          # fear / defensive (v14: vlPAG = passive coping/freezing)
_OBS_REWARD = ("VTA", "NAc-core", "NAc-shell", "OFC")   # appetitive approach
_OBS_CARE = ("PVN-OT", "MPOA", "SEPT")              # affiliation / care
_OBS_EXEC = ("dlPFC", "dACC", "vlPFC", "preSMA")    # executive control
# RE-DERIVED (audit, ruled -- an OUTPUT/attack construct must read the attack output, not the selector).
# Was ("CEl", "dPAG", "HYPdm"): CEl is the CeL SELECTOR whose GABAergic CeM output SUPPRESSES the attack
# effectors -- including it made the aggression measure ANTI-CORRELATED with its own signal -- and VMHvl,
# which the seed itself calls the necessary-and-sufficient attack locus, was absent. Now reads the actual
# active-defence/attack output: VMHvl (attack area) + CEm-active (the active-defence CeM population) +
# dPAG (active-coping fight/flight motor) + HYPdm (autonomic defensive drive). This removal is on OUTPUT
# grounds (CEl is not an attack output), independent of the held felt-set question.
_OBS_AGGRESS = ("VMHvl", "CEm-active", "dPAG", "HYPdm")   # threat -> attack: the active-defence OUTPUT
# ★ RE-DERIVED (vicarious-pathway build, RULED) -- on the nodes that MEASURABLY carry the vicarious signal
# after the pathway was built. Was ("LA","BA","CEl","aIns"): those amygdala nodes are OWN-PAIN-dominant (CEl
# +0.94 own vs +0.26 distress) -- they made the construct read own pain 6.6x. Now the shared-affect / conspecific
# / ACC-affective nodes the built distress-perception pathway actually reaches: aIns (shared representation),
# MeA (conspecific-specific -- distress +0.073, own-pain +0.000, the specificity term), dACC (ACC pain-affect;
# carries the distress signal +0.054). CEl is DROPPED from EMPATHY but remains a valid THREAT term (_OBS_THREAT)
# -- it rises with threat (inversion premise refuted), it just is not vicarious. Weak-signal caveat on empathy().
_OBS_EMPATHY = ("aIns", "MeA", "dACC")              # affective empathy (shared representation of another's distress)
_OBS_VMPFC = ("vmPFC",)                             # ventromedial PFC (Blair conscience)
_THREAT_CUE = {"IN-SOMATO:nociception": 0.8}
_REWARD_CUE = {"IN-GUST:sweet": 0.8}
_DISTRESS_CUE = {"IN-VIS:biological_motion": 0.8, "IN-AUD:voice": 0.7, "IN-VIS:face_like": 0.7}
_WARMTH_CUE = {"IN-SOMATO:affective_touch": 0.8, "IN-INTERO:thermal_warmth": 0.6}


def _punishment_sensitivity(engine) -> float:
    """The yoked-control learned aversion, on an isolated copy (never conditions the real engine)."""
    import copy as _c
    from substrate.study import punishment_learning
    return clamp(punishment_learning(_c.deepcopy(engine)))


def profile_from_substrate(engine) -> BehaviourProfile:
    """Build a BehaviourProfile from the developed SUBSTRATE engine's EMERGENT activity (Part 6
    substrate-social phase). This is the circuit-engine adapter that supersedes profile_from_legacy.

    READ-ONLY: it probes the agent's developed reactivity and MEASURES the circuit populations'
    responses, then RESTORES the engine's developed state -- so measuring never develops the agent
    and nothing it computes is fed back into behaviour. The constructs (triarchic, CU, ...) are
    then computed from this profile by the observer, exactly as before; the observer remains a
    measurement layer with no causal path back into the substrate."""
    from substrate import plasticity as _PL
    import copy as _copy

    # -- freeze the FULL developed + transient state so probing is read-only ----
    _FROZEN = ("weight", "theta", "mean_activity", "exp_count", "activation", "pruned",
               "eligibility", "_silent", "_step_i", "external", "channel_drive")
    saved = {a: _copy.copy(getattr(engine, a)) for a in _FROZEN}

    def _mean(cids):
        # DOUBLE-GAIN REMOVED (audit, ruled): the temperament throttle already shaped DEVELOPMENT (it
        # enters the dynamics via _gain during every step), so multiplying the developed activity by
        # _gain AGAIN here counted the manipulation twice -- a construct score that collapsed by the
        # gain factor from the seed alone. Read the developed activity; the throttle is already in it.
        live = [engine.activity(c)
                for c in cids if engine.live_circuit.get(c, False)]
        return sum(live) / len(live) if live else 0.0

    def _probe(cue, cids, ticks=25):
        engine.clear_inputs()
        for k, v in cue.items():
            engine.inject_channel(k, v)
        engine.settle(ticks)
        return clamp(_mean(cids))

    try:
        fear = _probe(_THREAT_CUE, _OBS_THREAT)
        seeking = _probe(_REWARD_CUE, _OBS_REWARD)
        care = _probe(_WARMTH_CUE, _OBS_CARE)
        vicarious = _probe(_DISTRESS_CUE, _OBS_EMPATHY)
        reactive = _probe(_THREAT_CUE, _OBS_AGGRESS)
        engine.clear_inputs(); engine.settle(15)
        restraint = clamp(_mean(_OBS_EXEC)
                          * _PL.maturation("pfc_low_early_high_late", engine.age_years, 6.0))
        moral = clamp(0.5 * care + 0.5 * _mean(_OBS_VMPFC))
    finally:
        for a, v in saved.items():        # restore -> the agent is untouched by measurement
            setattr(engine, a, v)

    return BehaviourProfile(
        fear=fear, seeking=seeking, care=care, restraint=restraint,
        moral_orientation=moral, reactive_aggression=reactive,
        instrumental_aggression=0.0,           # cold/calculated exploitation: not grounded in v8
        vicarious_response=vicarious,
        # ★ punishment_sensitivity -- the REAL yoked-control probe (ruled), replacing the BANNED hardcode
        # `clamp(0.3 + 0.7*fear)` (a direct trait->outcome mapping, and it was standing as the headline
        # learning result). study.punishment_learning is the CS-specific learned aversion measured as a
        # yoked-control DIFFERENCE (paired minus unpaired) -- confound-cancelled and, being a DIFFERENTIAL,
        # robust to the R8 common-mode normalisation (the R8 finding). Run on a deep copy so the frozen
        # engine is never conditioned. NOTE: the absolute magnitude is SMALL (~0.03-0.05, the honest
        # differential value on this substrate) with a ~2x relative discrimination across reactivity; whether
        # the [0,1] construct wants a grounded reference SCALE is a reward/value-characterisation question,
        # registered -- the raw differential is wired here rather than a tuned scale.
        punishment_sensitivity=_punishment_sensitivity(engine),
    )


def observe_substrate(engine) -> Dict[str, object]:
    """The full observer read-out over a developed substrate engine (read-only)."""
    return read_out(profile_from_substrate(engine))

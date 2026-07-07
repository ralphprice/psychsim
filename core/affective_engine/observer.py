"""
observer.py -- the observer read-out (docs/PsychSim_MASTER.md App. D.2).

This is where the OUTPUT CATEGORIES legitimately live -- "boldness", "meanness",
"disinhibition", "callous-unemotional", "empathy", "reactive vs instrumental aggression",
"psychopathy". They are computed *over* an agent (its behaviour and substrate activity), by
US, for reporting and validation, and are NEVER fed back into the mechanism. This completes
the substrate principle that named systems are read-outs, not primitives.

Engine-agnostic BY DESIGN: the metrics are computed from a neutral BehaviourProfile of
measurable signals, so the same read-out works whichever substrate produced the behaviour.
An adapter builds a BehaviourProfile from the current (legacy) engine now; a new-engine
adapter follows when the circuit substrate goes live (Phase 8). Nothing here is a verdict on
the agent -- it is measurement; whether any label is apt is a separate interpretive question.

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


def callous_unemotional(bp: BehaviourProfile) -> float:
    """Callous-unemotional traits (Frick): blunted empathy + weak affective conscience."""
    return clamp(0.5 * (1.0 - bp.vicarious_response) + 0.5 * (1.0 - bp.moral_orientation))


def empathy(bp: BehaviourProfile) -> float:
    """Empathic concern: vicarious response to distress + care-based moral orientation."""
    return clamp(0.5 * bp.vicarious_response + 0.5 * bp.moral_orientation)


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
        "callous_unemotional": callous_unemotional(bp),
        "empathy": empathy(bp),
        "aggression": aggression_profile(bp),
        "passive_avoidance_deficit": passive_avoidance_deficit(bp),
    }


# ---------------------------------------------------------------------------
# Legacy-engine adapter (retired with the legacy engine at Phase 8)
# ---------------------------------------------------------------------------

def profile_from_legacy(agent) -> BehaviourProfile:
    """Build a BehaviourProfile from the current (legacy 7-system) engine's read-outs. This
    reads the emergent substrate -- system strengths, conscience-control, moral orientation --
    NOT the seed, and never writes back. Superseded by a circuit-engine adapter at Phase 8."""
    from .drives import read_mind, System
    from .executive import moral_orientation_readout
    prof = read_mind(agent).profile          # normalised 7-system strengths
    brain = agent.brain

    def sysval(name):
        return prof.get(name, 0.0)

    # blend TEMPERAMENT (the substrate reactivity gains) with the DEVELOPED strengths, so the
    # read-out reflects disposition on a fresh agent and experience on a grown one. Strengths
    # are normalised to their own max so a "high FEAR" reads high regardless of absolute scale.
    mx = max(prof.values()) or 1.0

    def g(name):
        return agent.gain.get(name, 0.5)

    fear = clamp(0.5 * g("THREAT") + 0.5 * sysval("FEAR") / mx)
    seeking = clamp(0.5 * g("SEEKING") + 0.5 * sysval("SEEKING") / mx)
    care = clamp(0.5 * g("CARE") + 0.5 * sysval("CARE") / mx)
    rage = clamp(0.5 * g("FRUSTRATION") + 0.5 * sysval("RAGE") / mx)
    restraint = clamp(agent.gain.get("CONTROL", 0.5))
    instrumental = clamp(agent.gain.get("INSTRUMENTAL_CONTROL", 0.5) * (1.0 - care))
    try:
        moral = clamp(moral_orientation_readout(brain))
    except Exception:
        moral = clamp(0.5 * care + 0.2)
    return BehaviourProfile(
        fear=fear, seeking=seeking, care=care, restraint=restraint,
        moral_orientation=moral, reactive_aggression=rage,
        instrumental_aggression=instrumental, vicarious_response=care,
        punishment_sensitivity=clamp(0.3 + 0.7 * fear),   # low-fear -> reward-dominant
    )


def observe_agent(agent) -> Dict[str, object]:
    """Convenience: the full observer read-out over a (legacy-engine) agent."""
    return read_out(profile_from_legacy(agent))

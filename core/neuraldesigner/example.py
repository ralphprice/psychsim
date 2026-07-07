"""
example.py -- a worked library that exercises every capability of the designer.

It defines input features, a set of circuits, external triggers, and -- the point
of the tool -- internal pathways that form a cascade, a self-sustaining loop, and
an inhibitory regulatory connection. The demo traces the dynamics tick by tick so
you can see activation spreading and being regulated, then shows a new pathway
being added at runtime and changing behaviour.

This is a small library (a handful of circuits) built by hand to be legible. The
same API scales to hundreds of circuits and pathways loaded from JSON.
"""

from __future__ import annotations
from typing import List

from .library import (NeuralLibrary, InputFeature, CircuitDef, TriggerDef,
                      PathwayDef, NetworkDef)
from .runtime import LibraryAgent, Situation


def build_example_library() -> NeuralLibrary:
    lib = NeuralLibrary(name="example_affective_library")

    # -- input features ----------------------------------------------------
    for dim in ("threat", "reward", "social_valence", "goal_relevance", "novelty",
                "controllability", "other_distress", "provocation", "exclusion"):
        lib.add_feature(InputFeature(dim, "appraisal"))
    lib.add_feature(InputFeature("uncontrollability", "derived", derivation="uncontrollability"))
    lib.add_feature(InputFeature("warmth", "derived", derivation="warmth"))
    lib.add_feature(InputFeature("blocked_goal", "derived", derivation="blocked_goal"))
    lib.add_feature(InputFeature("goal_weighted_pressure", "derived", derivation="goal_weighted_pressure"))

    # -- circuits ----------------------------------------------------------
    lib.add_circuit(CircuitDef("THREAT", "Threat", gain=0.6, impulsive=True, category="affective"))
    lib.add_circuit(CircuitDef("ANXIETY", "Anxiety", gain=0.6, category="affective"))
    lib.add_circuit(CircuitDef("VIGILANCE", "Vigilance", gain=0.7, category="affective",
                               description="driven only by the cascade from THREAT"))
    lib.add_circuit(CircuitDef("SEEKING", "Seeking", gain=0.75, impulsive=True, category="motivational"))
    lib.add_circuit(CircuitDef("FRUSTRATION", "Frustration", gain=0.62, impulsive=True, category="affective"))
    lib.add_circuit(CircuitDef("CARE", "Care", gain=0.5, category="affective"))
    lib.add_circuit(CircuitDef("CONTROL", "Conscience control", gain=0.4, category="regulatory"))

    # -- external triggers (situation -> circuit) --------------------------
    lib.add_trigger(TriggerDef("t_threat", "threat", "THREAT", 0.9))
    lib.add_trigger(TriggerDef("t_threat_unctrl", "uncontrollability", "THREAT", 0.1))
    lib.add_trigger(TriggerDef("t_anx_unctrl", "uncontrollability", "ANXIETY", 0.4))
    lib.add_trigger(TriggerDef("t_anx_novel", "novelty", "ANXIETY", 0.3))
    lib.add_trigger(TriggerDef("t_seek_reward", "reward", "SEEKING", 0.7))
    lib.add_trigger(TriggerDef("t_seek_goal", "goal_relevance", "SEEKING", 0.3))
    lib.add_trigger(TriggerDef("t_frust_prov", "provocation", "FRUSTRATION", 0.6))
    lib.add_trigger(TriggerDef("t_frust_block", "blocked_goal", "FRUSTRATION", 0.6))
    lib.add_trigger(TriggerDef("t_care_distress", "other_distress", "CARE", 0.7))
    lib.add_trigger(TriggerDef("t_care_warmth", "warmth", "CARE", 0.3))
    lib.add_trigger(TriggerDef("t_control_pressure", "goal_weighted_pressure", "CONTROL", 1.0))

    # -- pathways (circuit -> circuit) : the new capability ----------------
    # CASCADE: a threat spreads to vigilance and anxiety over the next ticks
    lib.add_pathway(PathwayDef("p_threat_vigilance", "THREAT", "VIGILANCE", 0.7, kind="cascade",
                               description="threat recruits vigilance"))
    lib.add_pathway(PathwayDef("p_threat_anx", "THREAT", "ANXIETY", 0.5, kind="cascade",
                               description="threat feeds anxiety"))
    # LOOP: frustration and threat amplify each other (escalation)
    lib.add_pathway(PathwayDef("p_frust_threat", "FRUSTRATION", "THREAT", 0.4, kind="loop",
                               description="feeling thwarted feels threatening"))
    lib.add_pathway(PathwayDef("p_threat_frust", "THREAT", "FRUSTRATION", 0.4, kind="loop",
                               description="feeling threatened feels thwarting -> escalation"))
    # INHIBITORY regulation: conscience control damps frustration at the circuit level
    lib.add_pathway(PathwayDef("p_control_frust", "CONTROL", "FRUSTRATION", -0.7, kind="direct",
                               description="conscience control inhibits frustration"))

    # -- behavioural networks ---------------------------------------------
    lib.add_network(NetworkDef(
        "cool_instrumental_boldness", "Cool instrumental boldness",
        weights={"SEEKING": 0.7, "THREAT": -0.5, "ANXIETY": -0.4},
        modulators={"CONTROL": 0.9}, affordances=["structure"], category="governed",
        policy="calm, goal-directed action under pressure"))
    lib.add_network(NetworkDef(
        "reactive_aggression", "Reactive aggression",
        weights={"FRUSTRATION": 0.9, "THREAT": 0.5},
        modulators={"CONTROL": -0.9}, affordances=["harshness"], category="ungoverned",
        policy="explosive, retaliatory hostility"))
    lib.add_network(NetworkDef(
        "affiliative_warmth", "Affiliative warmth",
        weights={"CARE": 0.9}, modulators={}, affordances=["warmth"], category="governed",
        policy="nurturant, cooperative conduct"))
    lib.add_network(NetworkDef(
        "fearful_withdrawal", "Fearful withdrawal",
        weights={"THREAT": 0.5, "ANXIETY": 0.7, "VIGILANCE": 0.4, "SEEKING": -0.5},
        modulators={}, affordances=[], category="neutral",
        policy="avoidance, retreat"))
    return lib


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def _fmt(hist, circuits) -> List[str]:
    lines = ["      tick " + " ".join(f"{c[:5]:>6}" for c in circuits)]
    for i, snap in enumerate(hist, 1):
        lines.append(f"      {i:>4} " + " ".join(f"{snap[c]:6.2f}" for c in circuits))
    return lines


def report() -> str:
    lib = build_example_library()
    L: List[str] = []
    W = L.append
    W("=" * 74)
    W("  NEURAL-PATHWAY DESIGNER -- example library")
    W("=" * 74)
    W(f"  circuits: {len(lib.circuits)} | triggers: {len(lib.triggers)} | "
      f"pathways: {len(lib.pathways)} | networks: {len(lib.networks)}")
    problems = lib.validate()
    W(f"  library validates: {'YES' if not problems else problems}")
    loops = lib.find_loops()
    W(f"  feedback loops detected: {[' -> '.join(l) for l in loops] or 'none'}")
    W("")

    # 1. CASCADE: a pure threat, no external anxiety/vigilance input
    W("  (1) CASCADE -- a threat spreads to VIGILANCE and ANXIETY over ticks")
    W("      (VIGILANCE has no external trigger; it activates only via the pathway)")
    ag = LibraryAgent(lib)
    hist = ag.trace(Situation({"threat": 0.9, "controllability": 0.3}, "threat event"), ticks=5)
    L += _fmt(hist, ["THREAT", "VIGILANCE", "ANXIETY"])
    W("")

    # 2. LOOP: provocation with WEAK conscience control -> escalation
    W("  (2) LOOP -- provocation, weak control: FRUSTRATION<->THREAT amplify")
    weak = LibraryAgent(lib, gains={"CONTROL": 0.2})
    hist = weak.trace(Situation({"provocation": 0.7, "goal_relevance": 0.6,
                                 "controllability": 0.3}, "provocation"), ticks=5)
    L += _fmt(hist, ["FRUSTRATION", "THREAT", "CONTROL"])
    W(f"      -> dominant network: {weak.dominant}")
    W("")

    # 3. INHIBITION: same provocation, STRONG conscience control
    W("  (3) INHIBITION -- same provocation, strong control damps FRUSTRATION")
    strong = LibraryAgent(lib, gains={"CONTROL": 0.9})
    hist = strong.trace(Situation({"provocation": 0.7, "goal_relevance": 0.6,
                                   "controllability": 0.3}, "provocation"), ticks=5)
    L += _fmt(hist, ["FRUSTRATION", "THREAT", "CONTROL"])
    W(f"      -> dominant network: {strong.dominant}")
    W("      (note FRUSTRATION and THREAT held lower than in (2): the inhibitory")
    W("       CONTROL->FRUSTRATION pathway breaks the escalation loop)")
    W("")

    # 4. AUTHORING AT RUNTIME: add a new pathway and see behaviour change
    W("  (4) AUTHORING -- add CARE->CONTROL (compassion recruits restraint), re-run (2)")
    from .library import PathwayDef
    lib.add_pathway(PathwayDef("p_care_control", "CARE", "CONTROL", 0.5,
                               description="compassion recruits restraint"))
    W(f"      library now has {len(lib.pathways)} pathways and still validates: "
      f"{'YES' if not lib.validate() else 'NO'}")
    W("=" * 74)
    return "\n".join(L)


if __name__ == "__main__":
    print(report())

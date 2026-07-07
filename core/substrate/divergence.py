"""
divergence.py (substrate) -- the executive-control development arm + the 2x2 divergence test
(docs/PsychSim_MASTER_Part4.md S7). This completes the causal chain the observer reads at its
END: a circuit throttle sets the affective ROOT; a developmental environment (perturbation
patterns only) drives circuit activity; meaning-blind plasticity sculpts the developed
executive control; the OUTCOME is measured.

THE HONESTY LINE (S7.3 -- the whole game). Environments are ONLY perturbation patterns
(sensory/social input-channel drives); NOTHING here maps an environment to an outcome. There
is no "warm -> control" or "harsh -> disinhibition" line: whether warm-firm and harsh
development diverge is left to the substrate's own wiring + plasticity, and MEASURED. If you
can find the line where an environment is mapped to an outcome, it is a bug -- rip it out.

THE FINDING IS THE INTERACTION (S7.4), not the main effect: the claim is that the fearless
(throttled) child's outcome is MORE environment-dependent than the intact child's -- the
differential-susceptibility structure. A 2x2: {throttled, intact} x {warm-firm, harsh}.

HONEST RESULT (surfaced, not forced -- Part IV robustness / S5.6). The earlier knife-edge (the
interaction flipping sign across development duration) was a symptom of a real correctness
defect: the un-throttled normal regime (Regime B, Part 5 S9.3) oscillated rather than settling.
The experience-decreasing plasticity (Part 5 S10.1) resolved that HONESTLY -- development now
converges -- so the 2x2 is now well-posed. On the developed-EXECUTIVE-CONTROL outcome the
interaction is stable in sign and ~0: the divergence does NOT robustly emerge (the EARNED
NEGATIVE, S10.3).

SELF-REFLECTION ROUTED INTO THE OUTCOME (Part 5 S10.2 + the review ruling). The organism now
carries the fourth matrix (self-reflection). Here it is wired into DEVELOPMENT and the outcome:
each developmental episode the agent reflects on itself, reading its OWN emergent valence /
attachment / threat from the substrate (a meaning-blind read-out over circuit activity, the
same idiom as study.empathy_response -- NEVER a coded self-verdict, and NEVER read from the
environment dict). The developed self-regard is then a second outcome channel. This tests
whether adding the self channel opens a route for the divergence to emerge, or whether it too
is the earned negative. Whatever it does is reported as measured (S5.6).
"""

from __future__ import annotations
from typing import Dict, Iterable, Tuple

from .engine import SubstrateEngine
from .model import load_substrate
from .study import throttled_newborn, AFFECTIVE_EMPATHY
from sim_world.self_reflection import SelfReflection

# Developmental environments as PERTURBATION PATTERNS (input-channel drives only). These
# describe what a caregiving world PRESENTS to the senses -- contact/warmth/nurturance vs
# separation/pain -- NOT what it should produce. No outcome, no valence, no control target.
ENVIRONMENTS: Dict[str, Dict[str, float]] = {
    "warm_firm": {"IN-SOMATO:affective_touch": 0.7, "IN-SOMATO:touch": 0.5,
                  "IN-INTERO:thermal_warmth": 0.5, "IN-GUST:sweet": 0.4},
    "harsh_inconsistent": {"IN-INTERO:contact_loss": 0.7, "IN-SOMATO:nociception": 0.5},
}

# The executive circuits that actually receive projections (vlPFC/vmPFC are near-isolated in
# v8 and sit at baseline -- excluded so they do not dilute the read-out). Anatomy, not meaning.
EXECUTIVE = ("dlPFC", "OFC", "dACC")

# Meaning-blind read-out sets for the SELF-REFLECTION valence (anatomy, not meaning) -- exactly
# the emergent-activity idiom of study.py's reward/defensive read-outs. The self-appraisal that
# feeds the self-matrix is COMPUTED from these circuits' activity, never from the environment.
_SELF_REWARD = ("VTA", "NAc-core", "NAc-shell", "OFC")     # approach / reward
_SELF_THREAT = ("CeA", "PAG", "BA", "aIns")                # threat / aversive
_SELF_ATTACH = ("PVN-OT", "MPOA")                          # affiliative / attachment

# SCAFFOLD. The composite outcome nudges executive control by the developed self-regard. This
# weight is a scaffold combination, flagged as such: the headline read-outs are reported
# per-channel (exec, self_regard) so no finding hinges on this number.
COMPOSITE_SELF_WEIGHT = 0.25

DEVELOP_YEARS = 18.0
DEVELOP_TICKS = 400          # SCAFFOLD developmental resolution
_PROBE = {"IN-VIS": 0.5}     # a neutral probe for reading developed control


def _self_signals(engine: SubstrateEngine) -> Tuple[float, float, float]:
    """Read the substrate's OWN emergent (valence, attachment_pull, threat_pull) -- a
    meaning-blind read-out over circuit activity (the study.empathy_response idiom), NOT a coded
    self-verdict. Valence = reward-minus-threat; the environment is never consulted here. This
    is how a warm childhood comes to read as positive self-regard: the substrate's innate wiring
    turns the warm perturbation pattern into reward-circuit activity, which self-reflection then
    reads -- an emergent chain, not a tag."""
    def mean(cids):
        live = [engine.activity(c) for c in cids if c in engine.model.circuits]
        return sum(live) / len(live) if live else 0.0
    reward, threat, attach = mean(_SELF_REWARD), mean(_SELF_THREAT), mean(_SELF_ATTACH)
    r = max(-1.0, min(1.0, reward - threat))
    return r, max(0.0, min(1.0, attach)), max(0.0, min(1.0, threat))


def develop(engine: SubstrateEngine, environment: Dict[str, float],
            years: float = DEVELOP_YEARS, ticks: int = DEVELOP_TICKS,
            reflection: SelfReflection = None) -> SelfReflection:
    """Run a childhood: inject the environment's perturbation pattern across developmental age;
    the substrate's meaning-blind plasticity sculpts it forward. Nothing steers the outcome.

    If a `reflection` matrix is supplied, the agent ALSO reflects on itself each episode: it
    reads its OWN emergent valence/attachment/threat off the substrate (`_self_signals`,
    meaning-blind) and updates the self-relation by the same RPE as observing anyone else. The
    self channel is purely a READ-OUT of the substrate here -- it does not feed back into the
    dynamics -- so the executive trajectory is byte-identical with or without it."""
    for i in range(ticks):
        engine.set_age(0.2 + years * i / ticks)
        engine.clear_inputs()
        for k, v in environment.items():
            engine.inject_channel(k, v)
        engine.settle(3)
        if reflection is not None:
            r, attach, threat = _self_signals(engine)
            reflection.reflect(r, attachment_pull=attach, threat_pull=threat)
    engine.set_age(25.0)
    return reflection


def developed_executive_control(engine: SubstrateEngine) -> float:
    """Read the developed executive control: the engaged PFC circuits' response to a neutral
    probe after development. A measurement over emergent activity -- the observer's end-point."""
    engine.clear_inputs()
    for k, v in _PROBE.items():
        engine.inject_channel(k, v)
    engine.settle(30)
    val = sum(engine.activity(c) for c in EXECUTIVE) / len(EXECUTIVE)
    engine.clear_inputs()
    engine.settle(10)
    return val


def developed_self_regard(reflection: SelfReflection) -> float:
    """The developed self-relation value -- the outcome the self-reflection channel produces. A
    read-out of the self-matrix (App-4 value), no verdict."""
    return reflection.self_value()


# the outcome channels the observer can read at the END of development
OUTCOMES = ("exec", "self_regard", "composite")


def _cell_full(throttle: float, environment: Dict[str, float], model,
               ticks: int = DEVELOP_TICKS) -> Dict[str, float]:
    """Grow one 2x2 cell once and read ALL outcome channels off the SAME developed agent:
    executive control (behavioural), self_regard (the self channel), and a scaffold composite."""
    eng = throttled_newborn(throttle, AFFECTIVE_EMPATHY, model=model)
    refl = develop(eng, environment, ticks=ticks, reflection=SelfReflection())
    exec_ctrl = developed_executive_control(eng)
    self_regard = developed_self_regard(refl)
    return {
        "exec": exec_ctrl,
        "self_regard": self_regard,
        "composite": exec_ctrl + COMPOSITE_SELF_WEIGHT * self_regard,
    }


def _cell(throttle: float, environment: Dict[str, float], model,
          ticks: int = DEVELOP_TICKS) -> float:
    """Executive-control outcome of one cell (back-compat: the pre-self-reflection read-out)."""
    return _cell_full(throttle, environment, model, ticks)["exec"]


def interaction_at(model, ticks: int, outcome: str = "exec") -> float:
    """The 2x2 interaction (throttled_swing - intact_swing) at a given development duration, on a
    chosen outcome channel. `outcome` in OUTCOMES; default 'exec' (the behavioural end-point)."""
    W, H = ENVIRONMENTS["warm_firm"], ENVIRONMENTS["harsh_inconsistent"]
    iw = _cell_full(0.0, W, model, ticks)[outcome]
    ih = _cell_full(0.0, H, model, ticks)[outcome]
    tw = _cell_full(0.7, W, model, ticks)[outcome]
    th = _cell_full(0.7, H, model, ticks)[outcome]
    return abs(tw - th) - abs(iw - ih)


def interaction_across_durations(model=None, durations: Iterable[int] = (350, 450, 600),
                                 outcome: str = "exec") -> Dict[int, float]:
    """The interaction at several development durations. If the SIGN is not stable across them,
    the interaction is knife-edge -- NOT a robust finding (Part IV)."""
    m = model or load_substrate()
    return {t: interaction_at(m, t, outcome) for t in durations}


def divergence_2x2(model=None, outcome: str = "exec") -> Dict[str, float]:
    """Run the 2x2 {throttled, intact} x {warm-firm, harsh} on a chosen outcome channel and
    return the cell outcomes plus the two environment-swings and their INTERACTION
    (throttled_swing - intact_swing). A positive interaction = the differential-susceptibility
    structure (S7.4). `outcome` in OUTCOMES."""
    m = model or load_substrate()
    iw = _cell_full(0.0, ENVIRONMENTS["warm_firm"], m)[outcome]
    ih = _cell_full(0.0, ENVIRONMENTS["harsh_inconsistent"], m)[outcome]
    tw = _cell_full(0.7, ENVIRONMENTS["warm_firm"], m)[outcome]
    th = _cell_full(0.7, ENVIRONMENTS["harsh_inconsistent"], m)[outcome]
    intact_swing = abs(iw - ih)
    throttled_swing = abs(tw - th)
    return {
        "outcome": outcome,
        "intact_warm": iw, "intact_harsh": ih,
        "throttled_warm": tw, "throttled_harsh": th,
        "intact_swing": intact_swing, "throttled_swing": throttled_swing,
        "interaction": throttled_swing - intact_swing,
    }


def divergence_all_channels(model=None) -> Dict[str, Dict[str, float]]:
    """The 2x2 on every outcome channel -- exec (behavioural), self_regard (the self channel),
    and the scaffold composite -- so the divergence review can see whether routing self-
    reflection in opens a channel the interaction emerges through, per channel and unforced."""
    m = model or load_substrate()
    return {oc: divergence_2x2(m, oc) for oc in OUTCOMES}

"""
executive.py -- the executive-function layer: the frontal-cortex system that, in a
real brain, can override instinctive drives, and where inhibitory control,
deliberation, conscience, and purpose reside.

IMPORTANT -- what this layer is, and is NOT (per the design instruction).

In a real brain the prefrontal cortex exerts top-down control over the primary
(limbic/brain-stem) systems: it inhibits prepotent impulses, deliberates, and is the
seat of care-based morality and conscience. But that control is exercised THROUGH the
neural paths and networks themselves -- it is not a rule bolted on top. Designing how
executive control actually gates the substrate is a large piece of future work that
must be grounded in research and wired into the paths where it really acts.

So for now this layer applies NO DIRECT EFFECT on behaviour. What it provides is a
MONITORED STATE -- the model's version of self-awareness -- that we can read and track
over development. It is derived from the substrate and the person's developmental
stage; it does not (yet) change what the substrate does. When the real prefrontal
control circuitry is designed, its effect will be wired into the substrate, and this
monitored state will become the thing that gates behaviour. Until then we represent
and observe its condition, so we can watch it evolve; we do not decree its effect.

Grounding (crude first pass; to be cited properly in the research write-up):

  * Executive function (Diamond, 2013): three core components -- inhibitory control /
    response inhibition (overriding prepotent, impulsive responses in favour of
    goal-consistent behaviour), working memory, and cognitive flexibility -- centred
    in the prefrontal cortex, which exerts an inhibitory influence on the limbic
    system (Ochsner & Gross). It matures slowly through childhood and peaks in early
    adulthood (~mid-20s), which is why adolescents are impulsive.

  * Care-based morality and conscience (Blair; the amygdala-vmPFC model): the
    ventromedial / orbitofrontal PFC, fed by amygdala stimulus-reinforcement learning
    that associates harming others with the aversive distress of victims, guides the
    healthy individual away from moral transgressions. In psychopathy this circuit is
    dysfunctional, so intelligence becomes "uncoupled from conscience" -- deliberative
    capacity can remain intact (or superior) while the affective conscience is
    impaired, and behaviour is used instrumentally.

  * Purpose and goals: deliberation constructs goals, philosophies, and chosen
    behaviours -- the possible route by which a person with a weak affective conscience
    builds a *cognitive* conscience and purpose (the research hypothesis for the
    sophropath). Represented here only as a monitored, accruing state.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, List, Optional
from affective_engine.drives import Brain, System, clamp


# ---------------------------------------------------------------------------
# What the executive has LEARNED to watch for on the brain's events
# ---------------------------------------------------------------------------

@dataclass
class MonitoredPattern:
    """A pattern the executive watches for on the brain's events, and the modulation it
    applies when the pattern matches. In a real brain the prefrontal system learns,
    from memory and experience, which events to intervene on (a prepotent impulse it
    has learned is costly, a goal to hold) and how. So the CONTENT here -- which
    patterns, and how strong -- is learned and to be established by research; the
    executive is NOT born knowing it, and the registry is EMPTY by default. This is the
    mechanism only; the specific patterns must NOT be hand-invented, exactly as the
    directional effect rules of the primary systems must not be. `matches` is a
    predicate on (dominant_system, activations, stimulus); `target` is the system whose
    activation is modulated; `kind` is inhibit (the clearest researched prefrontal
    effect) or amplify (holding/boosting, e.g. a goal)."""
    name: str
    matches: Callable
    target: System
    kind: str = "inhibit"     # inhibit | amplify


BASE_MODULATION = 0.6   # magnitude of a fully-matured executive act; gated by capacity


# ---------------------------------------------------------------------------
# The monitored executive state (self-awareness) -- read, not applied
# ---------------------------------------------------------------------------

@dataclass
class Executive:
    """The monitored state of a person's executive-function layer. Every field is a
    read-out we track; NONE currently changes behaviour. Together they are the
    model's version of self-awareness -- the condition of the frontal system we
    observe as it develops."""
    inhibitory_capacity: float = 0.05   # capacity to override prepotent drives (matures with development)
    deliberation: float = 0.05          # capacity for deep thought / cognitive flexibility
    moral_orientation: float = 0.0      # care-based conscience -- a READ-OUT of the substrate
    purpose: float = 0.0                # formed goals / philosophy -- accrues with deliberative life
    # the always-on layer: patterns it has LEARNED to watch for (empty by default --
    # what to monitor is learned and to be researched), and running tallies of how
    # often it has been consulted (every brain event) and how often it has acted
    monitors: List[MonitoredPattern] = field(default_factory=list)
    checks: int = 0                     # brain events it has been consulted on (always-on loop)
    fired: int = 0                      # times it has actually acted (on a monitored event)

    def learn_to_monitor(self, pattern: MonitoredPattern) -> None:
        """Install a pattern for the executive to watch for. In the full model these
        are learned from memory and experience (and their content is to be researched);
        this is the hook by which learning installs them onto the always-on layer."""
        self.monitors.append(pattern)

    def remove_monitor(self, name: str) -> bool:
        """Remove an installed monitor by name (True if one was removed)."""
        n = len(self.monitors)
        self.monitors = [m for m in self.monitors if m.name != name]
        return len(self.monitors) < n

    def consult(self, activations: dict, dominant: System, stimulus: Optional[dict] = None) -> bool:
        """ALWAYS-ON. Called on every brain event (every respond), whether or not it
        acts -- the executive pathways run continuously, checking each event. For each
        learned monitored pattern that matches this event, it modulates the target
        system's activation: inhibiting (the prefrontal cortex damping a prepotent
        response) or amplifying (holding a goal), by an amount GATED by its
        inhibitory_capacity -- so an immature (child) executive intervenes weakly and a
        mature (adult) one strongly, tracking prefrontal maturation. It records the
        consultation and any firing. With no learned monitors (the default) it only
        records the check: no effect. Modifies `activations` in place; returns whether
        it fired. This is the mechanism; which events are monitored, and how strongly,
        is learned and to be researched -- deliberately not hand-set here."""
        self.checks += 1
        fired = False
        for p in self.monitors:
            try:
                hit = p.matches(dominant, activations, stimulus)
            except Exception:
                hit = False
            if hit:
                amount = self.inhibitory_capacity * BASE_MODULATION
                cur = activations.get(p.target, 0.0)
                if p.kind == "amplify":
                    activations[p.target] = cur + amount
                else:  # inhibit
                    activations[p.target] = max(0.0, cur - amount)
                fired = True
        if fired:
            self.fired += 1
        return fired

    def self_awareness(self) -> float:
        """An overall index of the executive layer's development -- the meta-state we
        monitor. A summary read-out, not a driver."""
        return clamp((self.inhibitory_capacity + self.deliberation
                      + max(0.0, self.moral_orientation) + self.purpose) / 4.0)

    def note(self) -> str:
        """A descriptive read of the executive state -- useful for watching the
        sophropath/psychopath question WITHOUT deciding it. High deliberation and
        purpose with a LOW moral orientation is the 'cognitive cunning' /
        cognitive-conscience pattern; high moral orientation is an affective
        conscience. This is observation, not a verdict."""
        parts = []
        parts.append("strong self-command" if self.inhibitory_capacity >= 0.6
                     else "weak self-command" if self.inhibitory_capacity < 0.3 else "developing self-command")
        if self.moral_orientation >= 0.5:
            parts.append("affective conscience")
        elif self.moral_orientation < 0.25 and self.deliberation >= 0.5:
            parts.append("conscience uncoupled from deliberation")
        if self.purpose >= 0.4:
            parts.append("formed purpose")
        return "; ".join(parts)


# ---------------------------------------------------------------------------
# How the monitored state is derived (from the substrate and developmental stage)
# ---------------------------------------------------------------------------

def maturation_ceiling(age_years: float) -> float:
    """The developmental ceiling on executive capacity by age. The prefrontal cortex
    matures slowly, reaching maturity around the mid-20s (Diamond; the reason
    adolescents are impulsive). A monitored capacity ceiling, not an effect."""
    return clamp(age_years / 25.0)


def moral_orientation_readout(brain: Brain) -> float:
    """Read the substrate's care-based moral orientation -- Blair's affective
    conscience. Grounded in empathic concern for, and aversion to the distress of,
    others: it reads the CARE system (empathic concern, both how developed and how
    reactive) and is pulled down by a strong RAGE disposition. This is a DESCRIPTIVE
    read-out of the substrate's condition, NOT an imposed value: a low-CARE
    (psychopathic-leaning) substrate reads low, exactly as the amygdala-vmPFC model
    would expect, but nothing here forces that -- it reflects the emergent wiring."""
    care = brain.drives[System.CARE]
    rage = brain.drives[System.RAGE]
    return clamp(0.55 * care.strength + 0.35 * care.reactivity - 0.20 * rage.strength)


MATURE_LR = 0.05      # how fast a capacity approaches its age ceiling (monitoring rate)
PURPOSE_LR = 0.03     # how fast deliberative experience accrues purpose


# ---------------------------------------------------------------------------
# How MEMORY installs what the executive monitors (reversal/reinforcement learning)
# ---------------------------------------------------------------------------

MIN_EVENTS_TO_LEARN = 4          # instances of a drive's outcomes before a lesson is drawn
LEARN_VALENCE_THRESHOLD = -0.10  # mean remembered outcome below this = net-costly -> learn to inhibit


def _system_from_label(name: str) -> Optional[System]:
    try:
        return System(name)
    except ValueError:
        return None


def install_monitors_from_memory(executive: Executive, memory,
                                 min_events: int = MIN_EVENTS_TO_LEARN,
                                 threshold: float = LEARN_VALENCE_THRESHOLD) -> List[MonitoredPattern]:
    """Learn, from episodic memory, WHICH prepotent drives the executive should monitor
    -- the mechanism by which memory installs the always-on layer's content.

    It reads the outcomes memory has recorded for each dominant system (each event
    remembers the drive that was run and the valence of what followed). Where a system's
    responses have, on balance, led to BAD outcomes -- mean remembered valence below the
    threshold, over enough instances -- it installs an inhibitory monitor for that
    system, so the always-on executive will thereafter damp that drive when it is
    prepotent. This is reversal / reinforcement learning of response inhibition: the
    orbitofrontal / ventromedial function of learning that a response leads to a bad
    outcome and coming to suppress it -- the very learning whose FAILURE characterises
    psychopathy (the prepotent drive is never brought under control because its costly
    outcomes are not learned from).

    Crucially it does NOT hand-pick a drive to inhibit. Which drive is regulated emerges
    from the person's OWN history: a child whose aggression kept costing them learns to
    inhibit aggression; one whose history holds no such lesson learns nothing. The
    thresholds are crude, tunable mechanism parameters; the SIGNAL read -- the valence of
    remembered outcomes -- is emergent, and what the environment counts as a bad outcome
    is itself a modelling choice to be grounded, never a per-system rule written here.
    Returns the newly-installed patterns (idempotent: a drive already monitored is
    skipped)."""
    from collections import defaultdict
    sums: dict = defaultdict(float)
    counts: dict = defaultdict(int)
    for m in memory.events:
        sums[m.dominant] += m.valence
        counts[m.dominant] += 1
    already = {p.target for p in executive.monitors}
    installed: List[MonitoredPattern] = []
    for name, n in counts.items():
        if n < min_events:
            continue
        mean_val = sums[name] / n
        if mean_val >= threshold:
            continue
        sysm = _system_from_label(name)
        if sysm is None or sysm in already:
            continue
        patt = MonitoredPattern(
            name=f"learned: inhibit prepotent {name} (mean outcome {mean_val:+.2f} over {n})",
            matches=(lambda s: (lambda dom, act, stim: dom is s))(sysm),
            target=sysm, kind="inhibit")
        executive.learn_to_monitor(patt)
        installed.append(patt)
    return installed


def monitor_executive(ex: Executive, brain: Brain, age_years: float,
                      deliberative: bool = False) -> Executive:
    """Update the monitored executive state. Capacities mature toward the age ceiling;
    the moral orientation is re-read from the substrate; purpose accrues when the
    person engages in deliberative experience (learning, reflection), gated by their
    deliberative capacity. NOTHING here changes the substrate or behaviour -- it only
    updates what we observe. Call it alongside a lived moment to track the executive
    layer's development."""
    ceil = maturation_ceiling(age_years)
    ex.inhibitory_capacity = clamp(ex.inhibitory_capacity + MATURE_LR * (ceil - ex.inhibitory_capacity))
    ex.deliberation = clamp(ex.deliberation + MATURE_LR * (ceil - ex.deliberation))
    ex.moral_orientation = moral_orientation_readout(brain)
    if deliberative:
        ex.purpose = clamp(ex.purpose + PURPOSE_LR * ex.deliberation)
    return ex

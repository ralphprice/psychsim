"""
system.py -- the criminogenic-justice module (Study 4 Part E.8; optional).

Mechanism, not magnitude. This module implements the labelling-theory
hypothesis (Becker, 1963; Lemert, 1967) as a manipulable mechanism: contact
with the justice system attaches a label, and the label degrades the
developmental environment the child subsequently grows in -- less access to
ordered institutions (structure down), stigma from adults and peers (warmth
down), fewer legitimate routes to recognition (recognition down). If the
hypothesis is right, part of the forensic 'criminal psychopath' phenotype is
manufactured by the system that studies it; if it is wrong, switching this
module on should barely move the outcome distribution. The module makes the
question runnable; it does not answer it. Every constant below is an explicit,
sweepable assumption, and nothing produced here is evidence about people --
outputs are hypotheses about how such a mechanism WOULD behave if the
parameters were in these ranges.

Design notes. The module wraps the core `develop()` loop without forking it:
development runs in segments, and between segments the justice system reads
the agent's newly lived episodes from its own memory stream, rolls detection
on visible antisocial acts (seeded), escalates a contact ladder, and derives
the labelled environment the next segment is lived in. With `justice=None`
the segmented runner reduces exactly to plain segmented development, so the
ON/OFF comparison isolates the mechanism.

Simplifications, stated honestly: (1) label effects act only through the
three environment channels the development rule already has -- deviant-peer
exposure is not modelled as a separate channel and is subsumed, imperfectly,
in the warmth/structure degradation; (2) detection treats offence visibility
as binary by situation kind ('temptation_unobserved' is invisible, the rest
visible); (3) the ladder does not decay -- labels, once acquired, persist,
which is the strong form of the labelling claim and therefore an upper bound
on the mechanism, not an estimate of it.
"""

from __future__ import annotations
from dataclasses import dataclass, field, replace
from typing import List, Optional
import random

from affective_engine.agent import AffectiveAgent
from affective_engine.core import EXPLOITATIVE, clamp
from affective_engine.development import Environment, develop


# ---------------------------------------------------------------------------
# Parameters -- every number an explicit, sweepable assumption
# ---------------------------------------------------------------------------

@dataclass
class JusticeParams:
    base_detect: float = 0.35        # P(detection) per visible antisocial act
    severity_callous: float = 1.00   # detection multiplier, calculated acts
    severity_reactive: float = 0.85  # detection multiplier, reactive acts
    warn_at: int = 1                 # contacts -> label level 1 (warned)
    charge_at: int = 3               # contacts -> label level 2 (charged)
    convict_at: int = 5              # contacts -> label level 3 (convicted)
    warmth_per_level: float = 0.08   # stigma: warmth lost per label level
    structure_per_level: float = 0.10  # exclusion: structure lost per level
    recognition_per_level: float = 0.10  # legitimate routes lost per level
    env_floor: float = 0.05          # environments never degrade below this

    def label_level(self, contacts: int) -> int:
        if contacts >= self.convict_at:
            return 3
        if contacts >= self.charge_at:
            return 2
        if contacts >= self.warn_at:
            return 1
        return 0


LABEL_NAMES = ("none", "warned", "charged", "convicted")

# Situation kinds in which an antisocial act has no witness and so cannot be
# detected. Everything else in the childhood cycle is treated as visible.
UNOBSERVED_KINDS = ("temptation_unobserved",)


@dataclass
class ContactEvent:
    segment: int
    kind: str            # situation the offence occurred in
    network: str         # the antisocial network expressed
    label_after: int     # label level once this contact is counted


@dataclass
class JusticeSystem:
    """Tracks one agent's contact history and derives its labelled world."""
    params: JusticeParams = field(default_factory=JusticeParams)
    seed: int = 20260705
    contacts: int = 0
    history: List[ContactEvent] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    @property
    def label_level(self) -> int:
        return self.params.label_level(self.contacts)

    @property
    def label(self) -> str:
        return LABEL_NAMES[self.label_level]

    # -- observation ---------------------------------------------------------

    def observe_segment(self, agent: AffectiveAgent, since_event: int,
                        segment_index: int) -> int:
        """Read the episodes the agent lived since `since_event`, roll
        detection on each visible antisocial act, escalate the ladder.
        Returns the number of new detections."""
        p = self.params
        new = 0
        for ev in agent.memory.events[since_event:]:
            if ev.dominant not in EXPLOITATIVE:
                continue
            if ev.label in UNOBSERVED_KINDS:
                continue
            sev = (p.severity_callous if ev.dominant == "callous_exploitation"
                   else p.severity_reactive)
            if self._rng.random() < p.base_detect * sev:
                self.contacts += 1
                new += 1
                self.history.append(ContactEvent(
                    segment_index, ev.label, ev.dominant, self.label_level))
        return new

    # -- the labelled world --------------------------------------------------

    def labelled_environment(self, base: Environment) -> Environment:
        """The environment as lived by a labelled child: same world, degraded
        access to its warm, ordered, recognising parts."""
        lvl = self.label_level
        if lvl == 0:
            return base
        p = self.params
        return Environment(
            name=f"{base.name}+label:{LABEL_NAMES[lvl]}",
            warmth=clamp(base.warmth - p.warmth_per_level * lvl,
                         p.env_floor, 1.0),
            structure=clamp(base.structure - p.structure_per_level * lvl,
                            p.env_floor, 1.0),
            recognition=clamp(base.recognition - p.recognition_per_level * lvl,
                              p.env_floor, 1.0),
        )


# ---------------------------------------------------------------------------
# The segmented developmental runner
# ---------------------------------------------------------------------------

def develop_with_justice(agent: AffectiveAgent, base_env: Environment,
                         justice: Optional[JusticeSystem] = None,
                         segments: int = 8, episodes_per_segment: int = 6,
                         seed: int = 20260704, graded: bool = True) -> None:
    """Run development in `segments` blocks. Between blocks, if a justice
    system is fitted, it observes the block just lived and re-derives the
    environment for the next. With justice=None this is plain segmented
    development -- the exact OFF condition for the comparison, sharing every
    seed and situation with the ON condition."""
    total = segments * episodes_per_segment
    for s in range(segments):
        env = justice.labelled_environment(base_env) if justice else base_env
        before = len(agent.memory.events)
        e0 = s * episodes_per_segment
        w = (e0 / max(1, total - 1),
             (e0 + episodes_per_segment - 1) / max(1, total - 1))
        develop(agent, env, n_episodes=episodes_per_segment,
                situation_seed=seed + 1000 * s, graded=graded,
                age_window=w, cycle_offset=e0)
        if justice is not None:
            justice.observe_segment(agent, before, s)

"""
lifecourse.py -- run one whole life, end to end.

The experiment's unit of observation is a single life course: a seeded
disposition, raised through a sequence of life stages in a configured moral
environment, ending in a classified outcome. This module assembles the three
stages the design specifies -- childhood (home + classroom), the transition
(further education / first job), and adulthood (an occupational role with a risk
profile) -- carrying the SAME person across all of them so the trajectory is
continuous, and reading the outcome from behaviour at the end.

It reuses the affective engine's validated development rule at each stage; the
only thing that changes stage to stage is the environment the person is embedded
in, so the moral environment can differ across the life course (a harsh home
followed by a structured first job, say).
"""

from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from affective_engine import AffectiveAgent, TraitSeed, classify
from affective_engine.development import Environment, develop, _moral_moment


# ---------------------------------------------------------------------------
# Environment specification per life stage
# ---------------------------------------------------------------------------

@dataclass
class StageEnv:
    """The moral environment for one life stage, as warmth/structure/recognition
    knobs plus the number of developmental episodes spent in it."""
    name: str
    warmth: float
    structure: float
    recognition: float
    episodes: int

    def to_environment(self) -> Environment:
        return Environment(self.name, self.warmth, self.structure, self.recognition)


@dataclass
class LifeCourseSpec:
    """A full life course: an ordered list of stage environments. Later studies
    vary these; presets are provided in conditions.py."""
    label: str
    stages: List[StageEnv]


# ---------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------

@dataclass
class LifeResult:
    seed_name: str
    condition_label: str
    classification: str                                    # the emergent dominant primary system
    stage_trace: List[str] = field(default_factory=list)   # classification after each stage
    # The classification is a bare ARGMAX over a normalised profile, and this project has now been bitten
    # by that twice in opposite directions: it EXAGGERATED a fragile psychopathic flip (~0.05 margin) and
    # HID a real graded F4 effect (0.0021 margin). MindReadout already carries the diagnostic -- it was
    # computed and then DISCARDED here, so no consumer could tell a confident label from a coin flip.
    # Carrying it means a label difference can be asked "is this real?" instead of being taken on trust.
    margin: float = 0.0                                    # normalised gap dominant - runner_up
    runner_up: str = ""                                    # the domain it beat


class _RelationalChildhood:
    """F4 -- the developed-alongside cohort and the directed relationships the subject accumulates
    across its moral-environment childhood.

    The subject's develop() is the CLOCK. Per moral moment (via the on_episode hook), this (a) advances
    each of K cohort agents ONE age-matched moral moment on its OWN persistent rng (a genuine parallel
    childhood -- NOT n_episodes=1 re-seeded calls, which relive one situation), then (b) with probability
    `cadence` fires ONE relational episode between the subject and a uniformly-sampled cohort member (the
    F1-F3 _social_episode, relational=True) -- ADDED after the moral moment, never replacing it, so the
    subject's moral-schedule episode count is invariant across arms. Directed rels (subject->member)
    persist across stages; warmth/wariness EMERGES from the episodes (accrue_relationship), never set.

    Byte-identity: `rel_rng` and every cohort rng are STRUCTURALLY-DISJOINT tuple seeds, so no relational
    draw reaches the subject's develop() rng; the subject's moral-env situation stream is identical
    whether relational is on or off (only the substrate STATE later moments read diverges -- the claim)."""

    def __init__(self, situation_seed: int, cohort_size: int, cadence: float):
        # imported here (not module-top) to keep the arena dependency off the baseline import path
        from arena import _social_episode, intact_seed
        from sim_world.gamemaster import Relationship
        self._social_episode = _social_episode
        self._Relationship = Relationship
        self.cadence = cadence
        # STRING seeds (deterministic, hashable) structurally disjoint from the subject's INT
        # situation_seed -- so no relational/cohort draw can collide with the subject's stream
        self.rel_rng = random.Random(f"{situation_seed}:rel")
        self.ids = [f"peer{k}" for k in range(cohort_size)]
        # neutral-temperament cohort (warmth/wariness must EMERGE), each with a distinct physical/
        # signature from a disjoint seed, and its OWN persistent situation stream
        self.cohort: Dict[str, AffectiveAgent] = {}
        self.member_rng: Dict[str, random.Random] = {}
        for k, cid in enumerate(self.ids):
            temper = random.Random(f"{situation_seed}:{k}:cohort").getrandbits(31)
            self.cohort[cid] = AffectiveAgent(seed=intact_seed(), temperament_seed=temper)
            self.member_rng[cid] = random.Random(f"{situation_seed}:{k}:cohort-stream")
        self.rels: Dict[tuple, "Relationship"] = {}
        # each side's last act TOWARD the other (what the OTHER perceives next episode) -- so the
        # exchange is MUTUAL: each perceives the other's real prior act, not its own echoed back
        self.member_last: Dict[str, str] = {cid: "approach" for cid in self.ids}   # member -> subject
        self.subject_last: Dict[str, str] = {cid: "approach" for cid in self.ids}  # subject -> member
        self._env: Optional[Environment] = None
        self._n = 0

    def stage_hook(self, stage: StageEnv, age_window: tuple = (0.0, 1.0)):
        self._env = stage.to_environment()
        self._n = stage.episodes
        self._window = age_window     # the cohort lives the SAME life-stage slice as the subject
        return self._on_episode

    def _on_episode(self, subject, i: int, age_years: float) -> None:
        # (a) advance each cohort member one AGE-MATCHED moral moment on its own persistent rng
        for cid in self.ids:
            _moral_moment(self.cohort[cid], self._env, self.member_rng[cid], i,
                          n_episodes=self._n, cycle_offset=0, span=18.0,
                          age_window=getattr(self, "_window", (0.0, 1.0)))
        # (b) ADD one relational episode with probability cadence -- a MUTUAL exchange with one
        # uniformly-sampled partner: each perceives the other's PRIOR act + the recognition cue from
        # its OWN stored history, each acts, each accrues its own directed tie. Warm/wary EMERGES from
        # how the two genuinely-developing agents come to treat each other -- never assigned.
        if self.rel_rng.random() < self.cadence:
            cid = self.rel_rng.choice(self.ids)
            member = self.cohort[cid]
            rel_s = self.rels.setdefault(("subject", cid), self._Relationship())   # subject's history of member
            rel_m = self.rels.setdefault((cid, "subject"), self._Relationship())   # member's history of subject
            s_act = self._social_episode(subject, member, self.member_last[cid], rel_s, age_years, relational=True)
            m_act = self._social_episode(member, subject, self.subject_last[cid], rel_m, age_years, relational=True)
            self.member_last[cid] = m_act
            self.subject_last[cid] = s_act


def run_life(seed: TraitSeed, spec: LifeCourseSpec,
             situation_seed: int = 20260704, trace: bool = False,
             relational: bool = False, cohort_size: int = 2,
             cadence: float = 0.35) -> LifeResult:
    """Raise one agent from `seed` through the stages of `spec`. With `relational=True` (F4) the subject
    ALSO lives co-present relational episodes with a developed-alongside cohort, interleaved into the
    SAME moral-environment childhood (ADD-not-replace, so the moral development is byte-identical to the
    relational=False baseline). Any divergence in the classified outcome is then attributable to the
    accumulated relational history alone."""
    agent = AffectiveAgent(seed=seed, temperament_seed=situation_seed)
    childhood = _RelationalChildhood(situation_seed, cohort_size, cadence) if relational else None
    stage_trace: List[str] = []
    # ---- each stage occupies its OWN, MONOTONIC slice of the lifespan -------------------------
    # BUG FIXED HERE (found by an independent construct-validity audit): develop()'s `age_window`
    # defaults to (0.0, 1.0), and run_life never passed one -- so EVERY stage re-lived ages 0->18 and
    # the "adulthood" stage was lived at age 0. Every age-gated mechanism (maturation curves,
    # developmental_online_age, plasticity schedules) reset to infancy at each stage boundary, which
    # silently violated the project's hardest constraint: never compress or reorder developmental time.
    # Any claim with life-course ORDERING in it (e.g. the harsh-home-then-warm-turn condition) was
    # measured through this -- the "turn" happened to an agent that had become age 0 again.
    # The window is allocated in proportion to each stage's episode count, so a stage that is lived in
    # more episodes occupies more of the lifespan and the age axis advances monotonically across stages.
    # RESIDUAL, FLAGGED NOT DECIDED: develop() hardcodes span = 18.0, so even with correct windows the
    # final "adulthood" stage maps onto late adolescence rather than adult years. Extending the span is
    # a model decision (it changes what the life course IS), not a bug fix, so it is left for ruling.
    _total = sum(st.episodes for st in spec.stages) or 1
    _acc = 0
    for i, stage in enumerate(spec.stages):
        _a0 = _acc / _total
        _acc += stage.episodes
        _a1 = _acc / _total
        # a distinct situation stream per stage, but reproducible
        develop(agent, stage.to_environment(), n_episodes=stage.episodes,
                situation_seed=situation_seed + i * 1000, age_window=(_a0, _a1),
                on_episode=(childhood.stage_hook(stage, (_a0, _a1)) if childhood else None))
        if trace:
            stage_trace.append(f"{stage.name}: {classify(agent).classification}")

    o = classify(agent)
    return LifeResult(
        seed_name=seed.name,
        condition_label=spec.label,
        classification=o.classification,
        stage_trace=stage_trace,
        margin=o.margin,
        runner_up=o.runner_up,
    )

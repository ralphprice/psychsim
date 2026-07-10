"""
report.py -- honest development reports for the sophropath study.

The live engine runs REAL time (never compressed), so a development report is a
*trajectory of samples* over the run, plus a cohort snapshot -- not a fast-forwarded
life. Every read-out is DESCRIPTIVE: a subject's "dominant" is the emergent substrate
domain, never a psychopath/sophropath verdict. At this crude substrate stage the output
is expected to be undifferentiated/chaotic; that is correct and not to be tuned away.

Samples exactly what the engine already exposes (`person_detail`/`read_mind`).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from substrate.readout import read_mind, profile_axis
from affective_engine.observer import observe_agent
from sim_experiment.readout import dominant_distribution, mean_profile, axis_stats

_CAVEAT = ("Descriptive read-out only: 'dominant' is the emergent substrate domain, NOT a "
           "psychopath/sophropath verdict. At this crude substrate stage output is "
           "expected to be undifferentiated/chaotic -- that is correct.")


@dataclass
class SubjectSnapshot:
    """One moment in a subject's emergent trajectory."""
    step: int
    minutes: int
    clock: str
    dominant: str                       # emergent primary system value (not a verdict)
    axis: float                         # neutral appetitive-minus-aversive projection
    systems: Dict[str, list]            # {system: [strength, reactivity]}

    def to_dict(self) -> dict:
        return {"step": self.step, "minutes": self.minutes, "clock": self.clock,
                "dominant": self.dominant, "axis": self.axis, "systems": self.systems}


@dataclass
class SubjectReport:
    cid: str
    temperament: Optional[str]
    home: Optional[str]
    trajectory: List[SubjectSnapshot] = field(default_factory=list)
    # the App. D / E.5 observer read-out (triarchic / CU / empathy / aggression), MEASURED
    # over the subject's emergent substrate and never fed back. Populated in subject_report().
    observer: Optional[dict] = None

    def to_dict(self) -> dict:
        return {"cid": self.cid, "temperament": self.temperament, "home": self.home,
                "trajectory": [s.to_dict() for s in self.trajectory],
                "observer": self.observer, "caveat": _CAVEAT}

    def text(self) -> str:
        head = f"subject {self.cid} (temperament: {self.temperament or 'inherited'}, home: {self.home})"
        if not self.trajectory:
            return head + "\n  (no samples yet -- run the sim to accumulate a trajectory)\n" + _CAVEAT
        path = " -> ".join(dict.fromkeys(s.dominant for s in self.trajectory))  # de-duped sequence
        first, last = self.trajectory[0], self.trajectory[-1]
        return (f"{head}\n  samples: {len(self.trajectory)}  "
                f"({first.clock} -> {last.clock})\n"
                f"  emergent-dominant sequence: {path}\n"
                f"  axis {first.axis:+.3f} -> {last.axis:+.3f}\n{_CAVEAT}")


@dataclass
class CohortReport:
    n: int
    distribution: Dict[str, int]
    mean_profile: Dict[str, float]
    axis_mean: float
    axis_stdev: float

    def to_dict(self) -> dict:
        return {"n": self.n, "distribution": self.distribution,
                "mean_profile": self.mean_profile, "axis_mean": self.axis_mean,
                "axis_stdev": self.axis_stdev, "caveat": _CAVEAT}

    def text(self) -> str:
        dist = ", ".join(f"{k}:{v}" for k, v in sorted(self.distribution.items(),
                                                       key=lambda kv: -kv[1]))
        return (f"cohort of {self.n} study subjects\n"
                f"  emergent-dominant distribution: {dist or '(none)'}\n"
                f"  axis mean {self.axis_mean:+.3f} (sd {self.axis_stdev:.3f})\n{_CAVEAT}")


def sample_subject(engine, cid: str) -> SubjectSnapshot:
    """One trajectory sample from the live engine's own read-outs."""
    person = engine.pop.persons[cid]
    r = read_mind(person.mind)
    systems = {k: round(v, 4) for k, v in r.profile.items()}   # emergent domain profile
    return SubjectSnapshot(step=engine.step_count, minutes=engine.minutes,
                           clock=engine.clock_label(), dominant=r.dominant.value,
                           axis=round(profile_axis(r.profile), 4), systems=systems)


def subject_report(engine, cid: str) -> SubjectReport:
    """A subject's accumulated trajectory (from the engine's subject log), plus the observer
    read-out of the study's constructs over the subject's emergent substrate (App. E.5)."""
    log = getattr(engine, "_subject_log", {}).get(cid, [])
    temper = getattr(engine, "tempers", {}).get(cid)
    home = engine.info[cid][1] if cid in getattr(engine, "info", {}) else None
    person = getattr(engine, "pop", None) and engine.pop.persons.get(cid)
    observer = observe_agent(person.mind) if person is not None else None
    return SubjectReport(cid=cid, temperament=temper, home=home, trajectory=list(log),
                         observer=observer)


def cohort_report(engine, cids=None) -> CohortReport:
    """A descriptive snapshot over the study subjects (or a given set of ids)."""
    ids = list(cids) if cids is not None else list(getattr(engine, "subjects", engine.info))
    reads = [read_mind(engine.pop.persons[c].mind) for c in ids if c in engine.pop.persons]
    ax = axis_stats(reads)
    return CohortReport(n=len(reads), distribution=dominant_distribution(reads),
                        mean_profile={k: round(v, 4) for k, v in mean_profile(reads).items()},
                        axis_mean=round(ax["axis_mean"], 4), axis_stdev=round(ax["axis_stdev"], 4))


def report(target, params=None) -> CohortReport:
    """Module.report hook: a cohort report over the engine's subjects."""
    return cohort_report(target)

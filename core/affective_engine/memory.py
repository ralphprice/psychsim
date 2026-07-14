"""
memory.py -- a purely-DESCRIPTIVE event log for the affective agent.

**Memory, behaviourally, is the substrate's plasticity** -- developed connection weights are the
engrams, BCM + neuromodulator-gated consolidation is the LTP-analogue (emotionally weighted: high-
arousal events drive the neuromodulatory circuits high, so they consolidate MORE -- the amygdala
emotional-tagging analogue), eligibility is the short-term trace, R7 pruning is forgetting. An agent's
history shapes its behaviour through those developed weights; there is no separate symbolic memory in
the behavioural path.

This module is what SURVIVES the v-next Memory-Layer Phase-1 un-bolting: a NON-BEHAVIOURAL record of
lived episodes, kept for inspection / UI / trace. It is read-back-into-NOTHING in the self-priming sense
-- no code path reads it into an agent's OWN behaviour. (The former symbolic `prime()`/`retrieve()`
"generative-agents" priming device -- a parallel scaffold that nudged an appraisal from an episode-list
-- was retired: it was DEAD CODE, never called, and the history-effect it approximated is produced,
better and emotionally-weighted, by the substrate's own developed weights.)

The ONE non-display reader is the justice system, which reads the log as the **public record of emitted
acts** (`events[].dominant` / `.label`) to detect antisocial behaviour -- a societal/environmental
process observing what publicly happened, NOT the agent consulting a symbolic self-memory to decide how
to act. That is a legitimate use of the record and does not reintroduce a parallel behavioural memory.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict

from .core import Appraisal, clamp


@dataclass
class EpisodicMemory:
    """One lived event, recorded for the log (descriptive; not read into the agent's own behaviour)."""
    t: int                 # timestep the event occurred
    label: str             # situation archetype (part of the public act-record)
    appraisal: Appraisal   # how it was appraised (descriptive record)
    dominant: str          # behavioural network the agent ran (part of the public act-record)
    valence: float         # response value -- the computed drive reduction
    importance: float      # salience of the event (0..1) -- descriptive (was retrieval-scoring input; now a record field)
    # optional per-variable drive reduction -- feeds anticipatory-value learning (App. C.5). Absent for legacy call sites.
    drive_reduction: Optional[Dict[str, float]] = None


@dataclass
class MemoryStream:
    """A write-mostly descriptive event log. `add()` records an episode; `summary()`/`events` are read
    for inspection/UI/trace and (for `events[].dominant`/`.label`) by the justice system as the public
    act-record. Nothing here reads back into the recording agent's OWN behaviour -- the behavioural
    memory is the substrate."""
    events: List[EpisodicMemory] = field(default_factory=list)
    _clock: int = 0

    def add(self, label: str, appraisal: Appraisal, dominant: str,
            valence: float, importance: float,
            drive_reduction: Optional[Dict[str, float]] = None) -> None:
        self.events.append(EpisodicMemory(
            self._clock, label, appraisal, dominant,
            valence, clamp(importance), drive_reduction))
        self._clock += 1

    def summary(self) -> str:
        if not self.events:
            return "(no memories)"
        n = len(self.events)
        avg_val = sum(m.valence for m in self.events) / n
        from collections import Counter
        modes = Counter(m.dominant for m in self.events)
        top = ", ".join(f"{k} x{v}" for k, v in modes.most_common(3))
        return (f"{n} episodes | mean response valence {avg_val:+.2f} | "
                f"most-run modes: {top}")

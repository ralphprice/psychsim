"""
readout.py -- study-neutral aggregation over emergent mind read-outs.

Given any iterable of `MindReadout` (from `affective_engine.drives.read_mind`), summarise
the cohort descriptively: the distribution of dominant primary systems, the mean strength
profile, and stats on a neutral projection axis. No verdict, no study vocabulary -- any
module reuses this.
"""

from __future__ import annotations
from collections import Counter
from statistics import mean, pstdev
from typing import Dict, List

from substrate.readout import profile_axis


def dominant_distribution(readouts: List) -> Dict[str, int]:
    """Count of the emergent dominant primary system across the cohort."""
    return dict(Counter(r.dominant.value for r in readouts))


def mean_profile(readouts: List) -> Dict[str, float]:
    """Per-system mean strength across the cohort."""
    readouts = list(readouts)
    if not readouts:
        return {}
    keys = list(readouts[0].profile.keys())
    return {k: mean(r.profile.get(k, 0.0) for r in readouts) for k in keys}


def axis_stats(readouts: List) -> Dict[str, float]:
    """Mean and population stdev of the neutral appetitive-minus-aversive axis."""
    vals = [profile_axis(r.profile) for r in readouts]
    if not vals:
        return {"axis_mean": 0.0, "axis_stdev": 0.0, "n": 0}
    return {"axis_mean": mean(vals),
            "axis_stdev": pstdev(vals) if len(vals) > 1 else 0.0,
            "n": len(vals)}

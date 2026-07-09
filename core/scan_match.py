"""
scan_match.py -- the scan controller's SEARCH-FOR-MATCH arm (Part 4 S8.2). Find the throttle
configuration whose developed profile best matches an EXTERNAL, held-out real-world field pattern.
This is the independent-corroboration mode: if a meaning-blind throttle + development independently
lands on a configuration that reproduces field data it was never told about, that is convergent
evidence -- BECAUSE nothing about the mechanism moved to achieve it.

Honesty (S8.3), held structurally:
  * FITNESS = DISTANCE TO AN EXTERNAL FIELD PATTERN, loaded from data/field/*.json. The substrate
    stays FIXED and only throttles vary (inherited from develop_and_measure -> set_throttle; no
    model handle here); the field data NEVER touches the mechanism -- it is only ever read to score
    a distance. That is what makes a hit corroboration rather than curve-fitting.
  * PER-SIGNATURE DISTANCE, never a weighted metric over a vector. A weighted metric would be a
    hand-drawn target profile through the back door (and an "unweighted" euclidean over signatures
    of different scales is implicitly scale-weighted). So a pattern names ONE signature and one
    target value; the distance is |developed_signature - target| for that single named read-out --
    the exact same no-weighting discipline as the search-for-effect objective.
  * PROVENANCE IS A VALIDATED REQUIRED FIELD. The loader REJECTS a pattern that lacks source,
    population, instrument, or the explicit `not_used_in_calibration: true` -- the corroboration
    claim rests on that last clause, so it is enforced, not assumed.
  * A PLACEHOLDER IS NEVER REPORTED AS CORROBORATION. A pattern whose source is marked PLACEHOLDER
    is allowed (so the plumbing can be built/tested), but every result it produces carries
    status='placeholder_not_corroboration' and cannot be promoted. Even a real pattern yields only
    a 'candidate_hypothesis' from the scan -- corroboration needs the robustness gate.
"""

from __future__ import annotations
import json
import os
from dataclasses import dataclass, field
from typing import Dict, List

from scan import SIGNATURE_NAMES
from scan_search import scan, ScanResult

_FIELD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "field")

_REQUIRED_PROVENANCE = ("source", "population", "instrument", "not_used_in_calibration")


@dataclass(frozen=True)
class FieldPattern:
    """An external, held-out field pattern to match against: ONE named signature and its target
    value, plus validated provenance. `is_placeholder` marks a synthetic pattern that must never be
    reported as corroboration."""
    name: str
    signature: str
    target: float
    provenance: Dict
    is_placeholder: bool

    def provenance_line(self) -> str:
        p = self.provenance
        return (f"{p.get('source','?')} | pop={p.get('population','?')} | "
                f"instrument={p.get('instrument','?')} | not_used_in_calibration="
                f"{p.get('not_used_in_calibration')}")


def load_field_pattern(path: str) -> FieldPattern:
    """Load + VALIDATE an external field pattern. Rejects (ValueError) any pattern missing the
    required provenance -- including the explicit `not_used_in_calibration: true`, without which the
    corroboration claim is void. Never touches the mechanism; this is read-only external data."""
    if not os.path.isabs(path):
        path = os.path.join(_FIELD_DIR, path)
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    for k in ("name", "signature", "target", "provenance"):
        if k not in d:
            raise ValueError(f"field pattern {path!r} missing required field '{k}'")
    if d["signature"] not in SIGNATURE_NAMES:
        raise ValueError(f"field pattern signature '{d['signature']}' is not a measured signature "
                         f"(one of {SIGNATURE_NAMES})")
    prov = d["provenance"]
    for k in _REQUIRED_PROVENANCE:
        if k not in prov:
            raise ValueError(f"field pattern {path!r} provenance missing required '{k}' -- provenance "
                             f"is mandatory (source, population, instrument, not_used_in_calibration)")
    if prov["not_used_in_calibration"] is not True:
        raise ValueError(f"field pattern {path!r} must declare not_used_in_calibration: true -- the "
                         f"corroboration claim requires the pattern was NOT used to calibrate the substrate")
    is_placeholder = "PLACEHOLDER" in str(prov["source"]).upper()
    return FieldPattern(d["name"], d["signature"], float(d["target"]), dict(prov), is_placeholder)


@dataclass(frozen=True)
class MatchObjective:
    """A search-for-match objective: fitness = NEGATIVE per-signature distance to the field target
    (higher = closer). ONE named signature only -- no weighted metric over a vector. Exposes the
    objective interface `scan_search.scan` expects (.name/.signature/.orientation/.value)."""
    pattern: FieldPattern

    @property
    def name(self) -> str:
        return f"match:{self.pattern.name}"

    @property
    def signature(self) -> str:
        return self.pattern.signature

    @property
    def orientation(self) -> int:
        return 0        # distance-based (minimise |dev - target|); not a signature +/- direction

    def value(self, result, baseline) -> float:
        """-|developed_signature - field_target| for the ONE named signature (higher = closer).
        The intact `baseline` is recorded for context but the match fitness is distance-to-FIELD,
        not distance-to-intact. The field value only ever scores a distance -- never sets a throttle
        or a weight."""
        return -abs(result.signatures[self.pattern.signature] - self.pattern.target)


def scan_for_match(pattern: FieldPattern, seeds: List[int], **scan_kw) -> ScanResult:
    """Coarse-to-fine search for the throttle config whose developed profile best matches `pattern`
    on its ONE named signature. Reuses the search-for-effect machinery (viable-first, intact control
    arm, coarse-to-fine, trajectory, no model handle). Tags the result with the field provenance and
    sets the honesty status: a PLACEHOLDER pattern -> 'placeholder_not_corroboration' (never
    promotable); a real pattern -> 'candidate_hypothesis' (a match is a candidate, not corroboration
    until it survives the robustness gate)."""
    result = scan(MatchObjective(pattern), seeds, **scan_kw)
    result.status = ("placeholder_not_corroboration" if pattern.is_placeholder
                     else "candidate_hypothesis")
    result.provenance["field_pattern"] = pattern.name
    result.provenance["field_signature"] = pattern.signature
    result.provenance["field_target"] = pattern.target
    result.provenance["field_provenance"] = pattern.provenance_line()
    result.provenance["is_placeholder"] = pattern.is_placeholder
    result.provenance["corroboration"] = False   # the scan NEVER reports a match as corroboration
    return result

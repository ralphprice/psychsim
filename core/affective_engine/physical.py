"""
physical.py -- v10 physical endowment: the PURE logic of per-agent physical traits and how they
present to (and are valued by) a perceiver. No engine, no I/O, so the honesty-critical parts are
unit-testable in isolation:

  * sample_physical  (E1): a FAITHFUL, SEEDED draw from the seed's physical_endowment distributions.
    Fresh agents only -- banked agents RELOAD their traits from the snapshot, never re-sample
    (restored-never-edited + banked-reproducibility). sex resolves PH-SIZE's mean ONLY via
    mean_by_age_sex; no hand-shaped trait correlations.
  * physical_stimulus (E2): the bearer-PURE stimulus a conspecific presents -- the same regardless of
    who is looking (B's musculature is B's musculature). Fed via felt_response into IN-CONSPEC edges.
  * sex_weight (E4): the perceiver's sex-conditioned valuation of that stimulus -- a genuine 2x2
    (perceiver x bearer) pairing (Aharon: male->female reward), NOT sex_weight(bearer) masquerading as
    a pairing. The dimorphism is in A's valuation of B, not in B's face.

Every magnitude here is SCAFFOLD (labelled): the literature gives direction, not magnitude. The
population outcomes (beauty premium; CU sex ratio) are NEVER computed here -- they are scan_match
targets that must emerge from the develop-and-accrue loop. Nothing in this module maps a trait or a
sex to a social outcome.
"""
from __future__ import annotations

import math
import random
from typing import Dict

SEX_MALE = "male"
SEX_FEMALE = "female"

# --- SCAFFOLD constants (direction grounded, magnitude assumed; replace with data) --------------
# PH-SIZE is the one trait the seed makes sex-dependent: "normal(mean_by_age_sex, sd)". Males are
# larger on average (anthropometric); magnitude is a placeholder. Every OTHER trait is drawn
# sex-NEUTRAL, exactly as the seed states (PH-ATTRACT/PH-MUSCLE/PH-HEALTH = normal(0,1)).
SCAFFOLD = {
    "size_mean_by_sex": {SEX_MALE: 0.35, SEX_FEMALE: -0.35},  # z-shift of PH-SIZE mean by sex
    "size_sd": 1.0,
    # E4 sex-conditioned reward weight: a genuine 2x2 (perceiver, bearer). Grounded direction only --
    # het-male reward response to attractive FEMALE faces is the studied effect (Aharon 2001). This is
    # a modulation of the PERCEIVER'S valuation, applied to the edge drive; the bearer's stimulus is
    # unchanged. Values are placeholders; only the ORDERING (male->female > others) is claimed.
    "attract_sex_weight": {
        (SEX_MALE, SEX_FEMALE): 1.0,   # the studied pairing (highest)
        (SEX_FEMALE, SEX_MALE): 0.7,
        (SEX_MALE, SEX_MALE): 0.5,
        (SEX_FEMALE, SEX_FEMALE): 0.5,
    },
    # formidability valuation is more accurate/studied for male perceivers (Sell); a mild pairing.
    "formid_sex_weight": {
        (SEX_MALE, SEX_MALE): 1.0,
        (SEX_MALE, SEX_FEMALE): 0.85,
        (SEX_FEMALE, SEX_MALE): 0.85,
        (SEX_FEMALE, SEX_FEMALE): 0.7,
    },
}


def sample_physical(rng: random.Random, age_years: float = 0.0) -> Dict[str, float]:
    """E1: draw one agent's physical endowment + sex, FAITHFULLY from the seed's distributions, using
    the SEEDED per-agent `rng` (reproducible from the world seed). Returns raw trait z-scores (the
    seed's normal(0,1)) plus `sex`. sex is an independent 50/50 draw; it conditions PH-SIZE's mean ONLY
    (mean_by_age_sex), which is the seed's single stated sex->trait link -- no other trait is reshaped
    by sex, and no trait-trait correlation is hand-imposed."""
    sex = SEX_MALE if rng.random() < 0.5 else SEX_FEMALE
    size_mean = SCAFFOLD["size_mean_by_sex"][sex]  # (+ age term would go here; flat at this scaffold)
    return {
        "sex": sex,
        "PH-ATTRACT": rng.gauss(0.0, 1.0),
        "PH-MUSCLE": rng.gauss(0.0, 1.0),
        "PH-SIZE": rng.gauss(size_mean, SCAFFOLD["size_sd"]),
        "PH-HEALTH": rng.gauss(0.0, 1.0),
    }


def _z_to_unit(z: float) -> float:
    """Map a z-score trait to a [0,1] stimulus magnitude (logistic). A presentation transform, not a
    valuation -- monotone, bearer-only."""
    return 1.0 / (1.0 + math.exp(-z))


def physical_stimulus(physical: Dict[str, float]) -> Dict[str, float]:
    """E2: the BEARER-PURE stimulus this agent presents to a conspecific's senses (fed to felt_response
    on the IN-CONSPEC channel). Magnitudes depend on the BEARER's traits only -- identical regardless
    of who perceives. attractiveness (health folded in) -> attractive_face; musculature (primary) +
    size (secondary) -> formidability_cue. NOT sex-conditioned (that is the perceiver's valuation, E4)."""
    if not physical:
        return {}
    attract = _z_to_unit(0.7 * physical.get("PH-ATTRACT", 0.0) + 0.3 * physical.get("PH-HEALTH", 0.0))
    formid = _z_to_unit(0.7 * physical.get("PH-MUSCLE", 0.0) + 0.3 * physical.get("PH-SIZE", 0.0))
    return {"attractive_face": attract, "formidability_cue": formid}


def sex_weight(perceiver_sex: str, bearer_sex: str, cue: str) -> float:
    """E4: how strongly THIS perceiver's valuation responds to the bearer's cue -- a genuine 2x2
    (perceiver_sex x bearer_sex) pairing, applied to the perceiver's edge drive (NOT the bearer's
    stimulus). `cue` is 'attractive_face' or 'formidability_cue'. Falls back to 0.5 (neutral) for an
    unknown pairing/cue rather than silently privileging a bearer sex."""
    table = SCAFFOLD["attract_sex_weight"] if cue == "attractive_face" else SCAFFOLD["formid_sex_weight"]
    return table.get((perceiver_sex, bearer_sex), 0.5)

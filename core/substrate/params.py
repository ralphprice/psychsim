"""
params.py (substrate) -- SCAFFOLD dynamics constants for the v7 substrate engine.

These are the CODE-SIDE dynamics parameters the seed does not carry (integration dt, the
qualitative-weight -> number map, plasticity rates, the eta schedule shapes). Everything the
SEED carries (time constants, baselines, bounds, set-points, developmental ages, gating
neuromodulators, eligibility taus) is read from v7 and is NOT duplicated here -- the seed is
the single source of truth (Part 2 S1.3). Every value below is a placeholder to be
calibrated (master Part IV); nothing is fitted.
"""

from __future__ import annotations

DT_MS = 50.0                      # SCAFFOLD integration step (ms) for the Euler update

# qualitative newborn connection weights (seed `default_weight`) -> numeric. SCAFFOLD.
WEIGHT_QUALITATIVE = {
    "low": 0.20, "low-moderate": 0.35, "moderate": 0.50,
    "moderate-strong": 0.70, "strong": 0.85, "high": 0.85, "none": 0.0,
}
DEFAULT_WEIGHT = 0.30             # SCAFFOLD fallback for an unrecognised qualitative weight

# innate default_birth_strength (catalogue) -> numeric. SCAFFOLD.
BIRTH_STRENGTH = {"weak": 0.25, "moderate": 0.5, "strong": 0.8, "very strong": 0.95}

# plasticity (R3-BCM / R5-NMOD / R4-HOMEO). SCAFFOLD rates.
BCM_LR = 0.02                     # weight-change rate scaling the gated eligibility
THETA_LR = 0.02                   # rate the BCM threshold tracks the circuit's own mean activity
HOMEO_RATE = 0.002                # slow homeostatic incoming-weight scaling (must beat BCM growth)
HOMEO_EVERY = 20                  # apply R4-HOMEO every N steps (slow clock)
STRUCT_EVERY = 200                # apply R7-STRUCT every N steps (slow clock)
PRUNE_BELOW = 0.02                # weights held below this are prune candidates
PRUNE_AFTER = 500                 # ...for this many steps -> pruned
NORMALISE = True                  # R8 competitive normalisation of incoming weights

# eta(age, schedule) shape library. The seed ASSIGNS a schedule to each circuit
# (`plasticity_coeff_schedule_ref`); these curve SHAPES are scaffold. Keyed by shape family
# parsed from the ref name (S2.4: high early, adolescent bump, low adult; PFC protracted).
ETA_BASE_EARLY = 0.9              # SCAFFOLD high-early plasticity
ETA_ADULT_FLOOR = 0.15           # SCAFFOLD low adult plasticity
ETA_FLAT = 0.35                  # SCAFFOLD constant-plasticity level
ADOLESCENT_PEAK_AGE = 16.0       # SCAFFOLD
ADOLESCENT_WIDTH = 6.0           # SCAFFOLD
PFC_LATE_PEAK_AGE = 22.0         # SCAFFOLD (protracted; low early, high late)
MATURE_AGE = 25.0                # SCAFFOLD age by which the high-early curves reach the floor

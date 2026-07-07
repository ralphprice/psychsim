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

# --- Experience-decreasing plasticity (Part 5 S10.1) --------------------------
# Weights are highly plastic early and rigidify with accumulated relevant experience: the nth
# co-activation event for a connection carries ~1/n of the weight (2nd ~50%, ~1000th ~0.1%),
# i.e. an incremental RUNNING AVERAGE -- so the developed state naturally settles, with no
# separate stabiliser. This is a plasticity RATE, not an outcome; it composes with R6.
EXP_PLASTICITY_FLOOR = 0.001      # SCAFFOLD adult floor (nonzero lifelong plasticity)
EXP_COACTIVE_THRESHOLD = 0.15     # SCAFFOLD both endpoints above this = one 'relevant experience'

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

# --- maturation(age, schedule): functional CONTROL/REWARD CAPACITY (Part 3 S5.4 / 8b.6) -------
# A [0,1] capacity that RISES with age from a circuit's onset to a schedule-dependent maturity --
# distinct from eta (a plasticity RATE). Fed into behaviour selection so the executive's control
# capacity keeps strengthening into the mid-20s (late/PFC schedules) while reward capacity matures
# by adolescence; the adolescent-risk imbalance then EMERGES from the seed's schedule shapes, never
# a coded rule. Age enters only as a rate; nothing references a circuit's meaning.
MATURE_AGE_LATE = 26.0           # SCAFFOLD PFC-protracted control capacity matures mid/late-20s
MATURE_AGE_EARLY = 8.0           # SCAFFOLD subcortical/early capacities mature in childhood
# Reward-system CAPACITY: present from early life (the DA system is online at birth), peaking in
# mid-adolescence and gently declining after -- the Steinberg dual-systems curvilinear shape. A
# nonzero FLOOR (a child still acts on reward) with an adolescent bump on top; paired with the
# late-maturing control capacity above, the adolescent-risk imbalance emerges. SCAFFOLD.
REWARD_CAP_PEAK_AGE = 16.0       # SCAFFOLD reward-sensitivity peak (mid-adolescence)
REWARD_CAP_WIDTH = 7.0           # SCAFFOLD width of the reward-capacity hump
REWARD_CAP_FLOOR = 0.7           # SCAFFOLD reward system works from early life; adolescence adds sensitivity

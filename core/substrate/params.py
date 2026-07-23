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
# TIME-NORMALISATION (prototype after-item): a 'relevant experience' accrues per unit developmental TIME, not
# per episode, so exp_count (-> S10.1 rigidification) no longer tracks an arbitrary harness episode count. This
# is the years one relevant co-activation experience represents. SCAFFOLD, but TIME-referenced (grounded-able)
# rather than episode-referenced (arbitrary); its value is set so the adult:developmental ratio lands inside the
# literature <=0.5 band N-INDEPENDENTLY (= 18yr span / 64 ep, the config that already landed in band). The
# specific value within the band is NOT pinned by the literature -- the band is the grounded constraint.
EXP_PERIOD_YEARS = 0.28

# qualitative newborn connection weights (seed `default_weight`) -> numeric. SCAFFOLD.
WEIGHT_QUALITATIVE = {
    "low": 0.20, "low-moderate": 0.35, "moderate": 0.50,
    "moderate-strong": 0.70, "strong": 0.85, "high": 0.85, "none": 0.0,
}
DEFAULT_WEIGHT = 0.30             # SCAFFOLD fallback for an unrecognised qualitative weight

# innate default_birth_strength (catalogue) -> numeric. SCAFFOLD.
BIRTH_STRENGTH = {"weak": 0.25, "moderate": 0.5, "strong": 0.8, "very strong": 0.95}

# v12a -- receptor -> postsynaptic SIGN (+1 excitatory / -1 inhibitory), by G-protein / ionotropic class.
# A connection's sign is DERIVED from its cited `dominant_receptor` (model._receptor_sign), NOT set
# directly: a dishonest flip would require citing a FALSE receptor (a checkable lie, not a silent tune).
# This is fixed pharmacology, not a per-edge judgement. Edges with no cited receptor fall back to the
# source's principal transmitter (glutamate +, GABA -). Standard classification (Guide to Pharmacology).
RECEPTOR_SIGN = {
    # ionotropic
    "AMPA": +1, "NMDA": +1, "kainate": +1, "nicotinic": +1,          # cation -> depolarising
    "GABA-A": -1, "GABA-C": -1, "glycine": -1,                        # anion -> hyperpolarising
    # metabotropic Gs/Gq -> excitatory
    "D1": +1, "D5": +1,
    "5-HT2": +1, "5-HT2A": +1, "5-HT2C": +1, "5-HT4": +1, "5-HT6": +1, "5-HT7": +1,
    "alpha1": +1, "beta": +1, "beta1": +1, "beta2": +1,
    "M1": +1, "M3": +1, "M5": +1, "mGluR1": +1, "mGluR5": +1,
    "H1": +1, "OX": +1, "OX1": +1, "OX2": +1, "V1a": +1, "OTR": +1,   # orexin, vasopressin, oxytocin
    "CRF-R1": +1,   # corticotropin-releasing factor R1: Gs-coupled -> excitatory (standard CRF-R1 pharmacology)
    # metabotropic Gi/Go -> inhibitory
    "D2": -1, "D3": -1, "D4": -1,
    "5-HT1A": -1, "5-HT1B": -1, "5-HT1D": -1, "5-HT5": -1,
    "alpha2": -1, "M2": -1, "M4": -1, "GABA-B": -1,
    "mu-opioid": -1, "kappa-opioid": -1, "delta-opioid": -1,
    "mGluR2": -1, "mGluR3": -1, "mGluR4": -1, "CB1": -1, "H3": -1,
}

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

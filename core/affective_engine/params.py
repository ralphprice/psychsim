"""
params.py -- the SCAFFOLD registry for the valence/motivation subsystem.

Per the build discipline (docs/PsychSim_MASTER.md, Part III §0 invariant 5 and the
cross-cutting requirements): EVERY set-point, gain, rate, threshold and capacity introduced
by the valence engine is a PLACEHOLDER, collected here so the calibration plan (Part IV) has
one surface to target. Nothing here is fitted to data; each value is marked `# SCAFFOLD`.

The *structure* that consumes these numbers (which state variables exist, which innate
sensor moves which variable, in which direction) is the grounded claim and lives in
interocept.py; only the *magnitudes* are here.
"""

from __future__ import annotations

# --- Valence scale (App. C.2): r = BETA * (D_prev - D_now) ------------------
BETA = 1.0                       # SCAFFOLD

# --- Learning: TD/RPE and its asymmetries (App. C) --------------------------
GAMMA = 0.90                     # SCAFFOLD temporal discount
ALPHA = 0.30                     # SCAFFOLD value learning rate
LAMBDA = 0.80                    # SCAFFOLD eligibility-trace decay (reserved for TD(lambda))
AVERSIVE_LR_MULT = 1.6           # SCAFFOLD aversive/threat learning is faster & higher-gain (C.8)
EXTINCTION_LR_MULT = 0.4         # SCAFFOLD extinction (new learning) is slower than acquisition (C.8)
THREE_FACTOR_LR = 0.06           # SCAFFOLD substrate three-factor plasticity rate (App. C.4)

# Per-cue LEARNING-RATE multipliers for prepared learning (App. B.3). A prior on how FAST
# a cue acquires value -- NOT an innate value. The cue is not innately aversive; the fear is
# merely learned in one/few trials. Unknown cues default to 1.0.
PREPARED_LEARNING = {            # SCAFFOLD
    "snake": 3.0, "spider": 3.0, "angry_face": 2.0, "height": 2.0,
    "blood": 1.5, "contamination": 1.5,
}

# --- Behaviour selection (App. F): basal-ganglia accumulation-to-threshold ---
SEL_THRESHOLD = 1.0              # SCAFFOLD commit threshold (bound)
SEL_GO_BASE = 0.40              # SCAFFOLD baseline Go gain
SEL_DOPAMINE_GAIN = 0.80        # SCAFFOLD tonic-dopamine -> Go gain / vigour
SEL_DOPAMINE_PEAK = 0.60        # SCAFFOLD inverted-U operating point (Cools)
SEL_LEAK = 0.08                 # SCAFFOLD accumulator leak
SEL_LATERAL = 0.15              # SCAFFOLD surround inhibition among candidates
SEL_STN_HOLD_GAIN = 1.20        # SCAFFOLD executive/STN global hold -> raised threshold
SEL_CONFLICT_HOLD = 0.60        # SCAFFOLD dACC: candidate proximity -> extra hold
SEL_MAX_STEPS = 300             # SCAFFOLD accumulation step cap (unresolved conflict)
SEL_DT = 0.1                    # SCAFFOLD integration step
# maturation of the selection systems (App. F.7 / doc §6; Steinberg dual-systems): the
# reward/sensation-seeking system is CURVILINEAR, peaking mid-adolescence; the PFC->STN
# control brake rises monotonically into the mid/late-20s. Their imbalance peaks in
# adolescence, from which risk-taking emerges (not coded).
SEL_REWARD_PEAK_AGE = 16.0      # SCAFFOLD sensation-seeking peak
SEL_REWARD_WIDTH = 9.0          # SCAFFOLD width of the reward hump
SEL_BRAKE_ONSET_AGE = 12.0      # SCAFFOLD control begins to firm up
SEL_BRAKE_MATURE_AGE = 28.0     # SCAFFOLD control matures (protracted into late 20s)
# how much unresolved approach/avoid conflict (BIS) holds the arousal variable elevated.
SEL_BIS_AROUSAL_GAIN = 0.5      # SCAFFOLD

# RECONCILIATION NOTE (design-review flag, for the coupled substrate integration): the
# STATE_VARIABLES set-points below and the PERTURBATION_GAINS further down are SCAFFOLD
# placeholders that currently have nothing to read from. When the v7 substrate is made live,
# they must be READ FROM THE SEED -- set-points from `seed.homeostatic_setpoint`, the
# perturbation SET from `seed.innate_wiring_catalogue` -- so the seed is the single source of
# that data (the Part-2 S1.3 drift warning). After that, params.py must hold ONLY genuine
# code-side scaffold (BETA/GAMMA/thresholds/rates), never a parallel copy of seed data, or
# the two will diverge.
#
# --- State-vector variables (App. A): set-point, weight, polarity, allostatic ---
# polarity "deficit": aversive when level < set_point (energy, warmth, attachment, ...)
# polarity "excess":  aversive when level > set_point (arousal, pain, CO2, uncertainty)
# level and set_point are in [0,1]; weight w_k is how much this need matters (endowment).
STATE_VARIABLES = {
    # survival (near-fixed set-points, online at/near birth)
    "tissue_integrity": {"set_point": 1.00, "weight": 1.00, "polarity": "deficit", "allostatic": False},  # SCAFFOLD
    "energy":           {"set_point": 0.80, "weight": 0.70, "polarity": "deficit", "allostatic": False},  # SCAFFOLD
    "hydration":        {"set_point": 0.80, "weight": 0.60, "polarity": "deficit", "allostatic": False},  # SCAFFOLD
    "thermal":          {"set_point": 0.80, "weight": 0.60, "polarity": "deficit", "allostatic": False},  # SCAFFOLD
    "respiratory":      {"set_point": 0.90, "weight": 1.00, "polarity": "deficit", "allostatic": False},  # SCAFFOLD
    "rest":             {"set_point": 0.80, "weight": 0.50, "polarity": "deficit", "allostatic": False},  # SCAFFOLD
    # autonomic (allostatic baseline)
    "arousal":          {"set_point": 0.20, "weight": 0.70, "polarity": "excess",  "allostatic": True},   # SCAFFOLD
    # social (allostatic; attachment dominant in infancy, belonging widens)
    "attachment":       {"set_point": 0.80, "weight": 0.80, "polarity": "deficit", "allostatic": True},   # SCAFFOLD
    "belonging":        {"set_point": 0.70, "weight": 0.65, "polarity": "deficit", "allostatic": True},   # SCAFFOLD
    # epistemic (extension, allostatic)
    "uncertainty":      {"set_point": 0.30, "weight": 0.40, "polarity": "excess",  "allostatic": True},   # SCAFFOLD
}

# --- Innate perturbation gains (App. B): trigger -> {variable: signed level delta} ------
# The SET (which sensor moves which variable, in which direction) is the grounded claim
# (interocept.PERTURBATION_LINKS); these MAGNITUDES are scaffold and are where temperament
# variation lives (App. B.5). Sign convention: + raises the variable's level, - lowers it.
# At substrate integration this SET must be read from `seed.innate_wiring_catalogue` (see the
# reconciliation note above); only the gains stay as code-side scaffold.
PERTURBATION_GAINS = {
    # physiological / survival (unconditioned)
    "nociception":        {"tissue_integrity": -0.60},                                   # SCAFFOLD
    "sweet_taste":        {"energy": +0.30},                                             # SCAFFOLD
    "bitter_taste":       {"energy": -0.05},                                             # SCAFFOLD
    "gastric_fill":       {"energy": +0.50},                                             # SCAFFOLD
    "drinking":           {"hydration": +0.50},                                          # SCAFFOLD
    "warmth_contact":     {"thermal": +0.40, "arousal": -0.10},                          # SCAFFOLD
    "cold":               {"thermal": -0.50},                                            # SCAFFOLD
    "heat":               {"thermal": -0.40},                                            # SCAFFOLD
    "co2_hypoxia":        {"respiratory": -0.60, "arousal": +0.40},                      # SCAFFOLD
    "rest_sleep":         {"rest": +0.50},                                               # SCAFFOLD
    # social (partly-primary; App. B.2.B)
    "affiliative_touch":  {"attachment": +0.30, "belonging": +0.20, "arousal": -0.30,
                           "tissue_integrity": +0.10},                                   # SCAFFOLD
    "contact_caregiver":  {"attachment": +0.40},                                         # SCAFFOLD
    "separation":         {"attachment": -0.50, "arousal": +0.30},                       # SCAFFOLD
    "soothing":           {"arousal": -0.40, "attachment": +0.20},                       # SCAFFOLD
    "synchrony":          {"belonging": +0.40, "arousal": -0.10},                        # SCAFFOLD
    "acceptance":         {"belonging": +0.30},                                          # SCAFFOLD
    "rejection":          {"belonging": -0.40, "arousal": +0.20},                        # SCAFFOLD
    # defensive / arousal (unconditioned responses)
    "looming":            {"arousal": +0.50},                                            # SCAFFOLD
    "startle":            {"arousal": +0.50},                                            # SCAFFOLD
    # epistemic
    "predictability":     {"uncertainty": -0.30},                                        # SCAFFOLD
    "surprise":           {"uncertainty": +0.30},                                        # SCAFFOLD
}

# --- Epigenetics (doc §5.2 / App. A.1(3)): early-window shift of allostatic parameters ---
EPI_RATE = 0.4                 # SCAFFOLD how strongly early experience moves allostatic params
EPI_WINDOW_END_AGE = 5.0       # SCAFFOLD the early sensitive window (years) for the shift
SUSCEPTIBILITY_BASE = 1.2      # SCAFFOLD differential susceptibility = BASE - fear reactivity

# A mild-deficit reference state a developing agent sits in (so relief/deepening of an
# ongoing need has room to register as valence). SCAFFOLD baseline levels.
REFERENCE_CHILD_LEVELS = {
    "tissue_integrity": 1.00, "energy": 0.65, "hydration": 0.70, "thermal": 0.70,
    "respiratory": 0.90, "rest": 0.65, "arousal": 0.40, "attachment": 0.50,
    "belonging": 0.45, "uncertainty": 0.45,
}  # SCAFFOLD

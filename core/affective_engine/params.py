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

# A mild-deficit reference state a developing agent sits in (so relief/deepening of an
# ongoing need has room to register as valence). SCAFFOLD baseline levels.
REFERENCE_CHILD_LEVELS = {
    "tissue_integrity": 1.00, "energy": 0.65, "hydration": 0.70, "thermal": 0.70,
    "respiratory": 0.90, "rest": 0.65, "arousal": 0.40, "attachment": 0.50,
    "belonging": 0.45, "uncertainty": 0.45,
}  # SCAFFOLD

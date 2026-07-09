"""
affective_engine -- a functional, circuit-level model of emotional and mental
process for generative-agent simulation.  See README.md.
"""

from .core import (
    Appraisal, TraitSeed,
    shared_root_seed, shared_root_calculating_seed,
    sophropathic_seed, psychopathic_seed, psychopathic_successful_seed,
)
from .memory import MemoryStream, EpisodicMemory
from .agent import AffectiveAgent
from .development import (
    Environment, warm_firm_home, harsh_inconsistent_home,
    develop, classify,
)
# NOTE: the Panksepp drive-engine (drives.py: System/Brain/Drive/imprint/read_mind/...) was
# RETIRED in Part 6 step 3e / stage 5. The substrate (core/substrate) is the sole engine: its
# feature read-outs are substrate.social.is_cohesive_act/is_aggressive_act and its disposition
# read-out is substrate.readout.read_mind.

__all__ = [
    "Appraisal", "TraitSeed",
    "shared_root_seed", "shared_root_calculating_seed",
    "sophropathic_seed", "psychopathic_seed", "psychopathic_successful_seed",
    "MemoryStream", "EpisodicMemory",
    "AffectiveAgent",
    "Environment", "warm_firm_home", "harsh_inconsistent_home",
    "develop", "classify",
]

__version__ = "0.2.0"

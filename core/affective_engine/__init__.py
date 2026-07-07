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
from .drives import (System, Brain, Drive, imprint, window_plasticity,
                     dominant_profile, read_mind, MindReadout,
                     brain_from_seed, appraisal_to_stimulus,
                     respond_to_appraisal, is_cohesive, is_aggressive)

__all__ = [
    "Appraisal", "TraitSeed",
    "shared_root_seed", "shared_root_calculating_seed",
    "sophropathic_seed", "psychopathic_seed", "psychopathic_successful_seed",
    "MemoryStream", "EpisodicMemory",
    "AffectiveAgent",
    "Environment", "warm_firm_home", "harsh_inconsistent_home",
    "develop", "classify",
    "System", "Brain", "Drive", "imprint", "window_plasticity",
    "dominant_profile", "read_mind", "MindReadout", "brain_from_seed",
    "respond_to_appraisal", "is_cohesive", "is_aggressive",
]

__version__ = "0.2.0"

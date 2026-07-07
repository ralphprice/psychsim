"""
affective_engine -- a functional, circuit-level model of emotional and mental
process for generative-agent simulation.  See README.md.
"""

from .core import (
    Appraisal, Network, TraitSeed, LanguageActuator,
    shared_root_seed, shared_root_calculating_seed,
    sophropathic_seed, psychopathic_seed, psychopathic_successful_seed,
    default_catalogue, GOVERNED, EXPLOITATIVE, CIRCUITS,
)
from .memory import MemoryStream, EpisodicMemory
from .agent import AffectiveAgent
from .development import (
    Environment, warm_firm_home, harsh_inconsistent_home,
    develop, probe, classify, Outcome,
)
from .drives import (System, Brain, Drive, imprint, window_plasticity,
                     dominant_profile, read_mind, MindReadout,
                     brain_from_seed, appraisal_to_stimulus)

__all__ = [
    "Appraisal", "Network", "TraitSeed", "LanguageActuator",
    "shared_root_seed", "shared_root_calculating_seed",
    "sophropathic_seed", "psychopathic_seed", "psychopathic_successful_seed",
    "default_catalogue", "GOVERNED", "EXPLOITATIVE", "CIRCUITS",
    "MemoryStream", "EpisodicMemory",
    "AffectiveAgent",
    "Environment", "warm_firm_home", "harsh_inconsistent_home",
    "develop", "probe", "classify", "Outcome",
    "System", "Brain", "Drive", "imprint", "window_plasticity",
    "dominant_profile", "read_mind", "MindReadout", "brain_from_seed",
]

__version__ = "0.2.0"

"""
core.substrate -- the live v7 neural substrate (Part 2 S2, sub-phase 8a).

A loader + leaky-integrator dynamical engine that runs the v7 seed's 73 nucleus-level
circuits and 159 connections under the 8 meaning-blind plasticity rules. Standalone: it
produces circuit ACTIVITY; wiring it into the valence engine / retiring the legacy engine is
8b. The seed is the single source of truth for structure and parameters; this package
supplies only the dynamics (and clearly-scaffold numeric mappings for the seed's qualitative
fields). Nothing in the dynamics references a circuit's meaning.
"""

from .model import SubstrateModel, Circuit, Connection, load_substrate
from .engine import SubstrateEngine

__all__ = ["SubstrateModel", "Circuit", "Connection", "load_substrate", "SubstrateEngine"]

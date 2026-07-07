"""
neuraldesigner -- an authoring tool for the affective engine's neural substrate.

Define circuits, input features, external triggers, internal pathways (cascades
and loops), and behavioural networks; store them in a library; save/load as JSON;
and run them with LibraryAgent. Built to scale the affective model far beyond the
hand-coded production set.
"""
from .library import (NeuralLibrary, InputFeature, CircuitDef, TriggerDef,
                      PathwayDef, NetworkDef)
from .runtime import LibraryAgent, Situation
from .example import build_example_library

__all__ = ["NeuralLibrary", "InputFeature", "CircuitDef", "TriggerDef",
           "PathwayDef", "NetworkDef", "LibraryAgent", "Situation",
           "build_example_library"]
__version__ = "0.1.0"

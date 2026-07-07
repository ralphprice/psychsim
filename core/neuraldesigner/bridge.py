"""
bridge.py -- export designed networks into the production affective engine.

A library is the authoring format; the production engine (affective_engine) runs
the tuned model. This bridge converts a library's NetworkDefs into the engine's
Network objects, so networks designed in the tool can be loaded by the engine.
Circuit-level pathways (cascades/loops) are a capability of the library runtime;
when the production engine gains a data-driven circuit layer, the same library
loads there too (roadmap).
"""

from __future__ import annotations
from typing import Dict

from .library import NeuralLibrary


def to_engine_networks(lib: NeuralLibrary) -> Dict[str, dict]:
    """Return engine-compatible network specs. Kept as plain dicts so this module
    has no hard dependency on the engine being importable; the engine's
    Network(**spec) consumes them where governance is derived from category and
    modulators are folded into the scoring as the engine expects."""
    out: Dict[str, dict] = {}
    for nid, net in lib.networks.items():
        # fold the CONTROL/INSTRUMENTAL modulators into the engine's fields
        instr = net.modulators.get("INSTRUMENTAL_CONTROL", 0.0)
        out[nid] = {
            "name": nid,
            "weights": dict(net.weights),
            "governance": net.category,
            "affordances": set(net.affordances),
            "policy": net.policy,
            "instr": instr,
        }
    return out

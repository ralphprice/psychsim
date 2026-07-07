"""
store.py -- a persisted, editable neural-design library: view (with the SVG wiring
diagram, validation and loop detection), add/edit (pathways, networks, circuits,
triggers, features) and delete (with cascade). Persists to data/neural/library.json;
if none exists the worked example is the starting point.

This is an AUTHORING sandbox for the affect model's pathways and networks-as-data. It is
NOT wired into the live substrate (that is the separate substrate-overhaul work); it lets
a researcher design and inspect networks and save them for that future use.
"""

from __future__ import annotations
import os
from typing import Dict, Tuple

from .library import (NeuralLibrary, InputFeature, CircuitDef, TriggerDef,
                      PathwayDef, NetworkDef)
from .example import build_example_library
from .viz import to_svg

_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "data", "neural")
_PATH = os.path.join(_DIR, "library.json")

# kind -> (add-method name, dataclass, remove-method name)
_COLLECTIONS: Dict[str, Tuple[str, type, str]] = {
    "feature": ("add_feature", InputFeature, "remove_feature"),
    "circuit": ("add_circuit", CircuitDef, "remove_circuit"),
    "trigger": ("add_trigger", TriggerDef, "remove_trigger"),
    "pathway": ("add_pathway", PathwayDef, "remove_pathway"),
    "network": ("add_network", NetworkDef, "remove_network"),
}


def load_library() -> NeuralLibrary:
    if os.path.isfile(_PATH):
        return NeuralLibrary.load(_PATH)
    return build_example_library()


def save_library(lib: NeuralLibrary) -> None:
    os.makedirs(_DIR, exist_ok=True)
    lib.save(_PATH)


def collections() -> Dict[str, list]:
    """The editable collection kinds and their field names (for an editor UI)."""
    from dataclasses import fields
    return {kind: [f.name for f in fields(cls)] for kind, (_, cls, _) in _COLLECTIONS.items()}


def library_view() -> dict:
    """The library as JSON, its SVG wiring diagram, and integrity feedback."""
    lib = load_library()
    return {"library": lib.to_dict(), "svg": to_svg(lib),
            "validation": lib.validate(), "loops": lib.find_loops(),
            "collections": collections()}


def upsert(kind: str, item: dict) -> dict:
    """Add or overwrite an item (add_* overwrites by id). Referential-integrity errors
    (e.g. a pathway to an unknown circuit) raise ValueError, surfaced as feedback."""
    add_name, cls, _ = _COLLECTIONS[kind]
    lib = load_library()
    getattr(lib, add_name)(cls(**item))
    save_library(lib)
    return item


def remove(kind: str, item_id: str) -> bool:
    _, _, rm_name = _COLLECTIONS[kind]
    lib = load_library()
    ok = getattr(lib, rm_name)(item_id)
    save_library(lib)
    return ok

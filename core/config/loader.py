"""
loader.py -- data-file-first configuration: load town/culture profiles and module
params from editable JSON, mapping onto the existing dataclasses. Stdlib only
(`json`, `os`, `dataclasses`).
"""

from __future__ import annotations
import json
import os
from dataclasses import fields
from typing import Dict

from sim_viz.settlement import DemographyProfile
from sim_world.population import HouseholdProfile
from .townprofile import TownProfile

# repo-root/data
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(_ROOT, "data")
TOWNTYPES_DIR = os.path.join(DATA_DIR, "towntypes")
MODULES_DIR = os.path.join(DATA_DIR, "modules")
ROLES_DIR = os.path.join(DATA_DIR, "roles")


def dataclass_from_dict(cls, d: dict):
    """Build a dataclass from a dict, ignoring unknown keys (forward-compatible).
    Dict-valued fields (e.g. tenure weights) pass straight through."""
    names = {f.name for f in fields(cls)}
    return cls(**{k: v for k, v in d.items() if k in names})


def load_town_profile(d: dict) -> TownProfile:
    """One town/culture profile from a parsed JSON object with `demography` and
    `household` sub-objects. JSON object keys are strings, so the one int-keyed
    field (`child_count_weights`) is coerced back to int."""
    demo = dataclass_from_dict(DemographyProfile, d.get("demography", {}))
    hh_raw = dict(d.get("household", {}))
    if "child_count_weights" in hh_raw:
        hh_raw["child_count_weights"] = {int(k): v
                                         for k, v in hh_raw["child_count_weights"].items()}
    household = dataclass_from_dict(HouseholdProfile, hh_raw)
    return TownProfile(name=d.get("name", "town"), demography=demo, household=household)


def load_town_profiles(directory: str = TOWNTYPES_DIR) -> Dict[str, TownProfile]:
    """Every town-type JSON in a directory, keyed by profile name."""
    out: Dict[str, TownProfile] = {}
    if not os.path.isdir(directory):
        return out
    for fn in sorted(os.listdir(directory)):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(directory, fn)) as f:
            tp = load_town_profile(json.load(f))
        out[tp.name] = tp
    return out


def load_roles(directory: str = ROLES_DIR) -> Dict[str, dict]:
    """Role schedule definitions from data/roles/<name>.json, keyed by role name. Each
    is `{name, child: bool, weekday: [[hour, place, room], ...], weekend: [...]}`."""
    out: Dict[str, dict] = {}
    if not os.path.isdir(directory):
        return out
    for fn in sorted(os.listdir(directory)):
        if fn.endswith(".json"):
            with open(os.path.join(directory, fn)) as f:
                d = json.load(f)
            out[d.get("name", fn[:-5])] = d
    return out


def load_module_params(directory: str = MODULES_DIR) -> Dict[str, dict]:
    """Per-module default params from `data/modules/<name>.json` (editable overrides
    of a module's in-code `default_params`)."""
    out: Dict[str, dict] = {}
    if not os.path.isdir(directory):
        return out
    for fn in sorted(os.listdir(directory)):
        if fn.endswith(".json"):
            with open(os.path.join(directory, fn)) as f:
                out[fn[:-5]] = json.load(f)
    return out

"""
exec_store.py -- an editable registry of executive ("frontal cortex") functions, as
DECLARATIVE monitor specs that compile to the executive's `MonitoredPattern` callables.

DISCIPLINE (design doc §2.9): the executive's monitor registry is EMPTY by default. The
prefrontal layer is consulted on every event but does not ACT until patterns it monitors
are installed -- and WHICH patterns, and how strongly, must be established by research,
never hand-invented (exactly as the primary systems' directional effect rules must not
be). So the shipped data/executive/monitors.json is empty. This interface lets a
researcher install patterns they have GROUNDED in research; it is a mechanism, not a way
to script behaviour.

A monitor spec: {name, target (a System), kind: inhibit|amplify, when_dominant (a System)}
-> "modulate `target` when `when_dominant` is the dominant system". This is exactly the
form the memory-driven learner (`install_monitors_from_memory`) produces.
"""

from __future__ import annotations
import json
import os
from typing import Dict, List

from .drives import System
from .executive import MonitoredPattern

_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "data", "executive")
_PATH = os.path.join(_DIR, "monitors.json")


def load_monitor_specs() -> List[dict]:
    if not os.path.isfile(_PATH):
        return []
    with open(_PATH) as f:
        d = json.load(f)
    return list(d.get("monitors", []) if isinstance(d, dict) else d)


def _save_specs(specs: List[dict]) -> None:
    os.makedirs(_DIR, exist_ok=True)
    with open(_PATH, "w") as f:
        json.dump({"description": "Executive-function monitors (frontal-cortex patterns). "
                                  "EMPTY by default -- install only researched patterns.",
                   "monitors": specs}, f, indent=2)


def spec_to_pattern(spec: dict) -> MonitoredPattern:
    """Compile a declarative spec to a MonitoredPattern (a `matches` callable)."""
    target = System[spec["target"]]
    kind = spec.get("kind", "inhibit")
    when = spec.get("when_dominant")
    if when:
        wsys = System[when]
        def matches(dom, activations, stimulus, _w=wsys):
            return dom is _w
    else:
        def matches(dom, activations, stimulus):
            return True
    return MonitoredPattern(name=spec.get("name", f"{kind}:{spec['target']}"),
                            matches=matches, target=target, kind=kind)


def install_data_monitors(executive):
    """Install every data-file monitor onto an executive. With the default (empty) file
    this is a no-op, so the executive is consulted but does not act -- the disciplined
    default. Invalid specs are skipped."""
    for spec in load_monitor_specs():
        try:
            executive.learn_to_monitor(spec_to_pattern(spec))
        except Exception:
            pass
    return executive


# -- CRUD over the spec file (for the editor) --------------------------------
def list_monitors() -> List[dict]:
    return load_monitor_specs()


def upsert_monitor(item: dict) -> dict:
    if not str(item.get("name", "")).strip():
        raise ValueError("monitor is missing its 'name'")
    if "target" in item and item["target"] not in System.__members__:
        raise ValueError(f"unknown target system {item['target']}")
    if item.get("when_dominant") and item["when_dominant"] not in System.__members__:
        raise ValueError(f"unknown when_dominant system {item['when_dominant']}")
    specs = load_monitor_specs()
    for i, s in enumerate(specs):
        if s.get("name") == item["name"]:
            specs[i] = {**s, **item}
            _save_specs(specs)
            return specs[i]
    specs.append(item)
    _save_specs(specs)
    return item


def delete_monitor(name: str) -> bool:
    specs = load_monitor_specs()
    kept = [s for s in specs if s.get("name") != name]
    _save_specs(kept)
    return len(kept) < len(specs)


def executive_view() -> dict:
    """For the editor: the monitor specs, the available systems, and the discipline note."""
    return {"monitors": load_monitor_specs(),
            "systems": [s.value for s in System],
            "kinds": ["inhibit", "amplify"],
            "note": ("The registry is EMPTY by default. The executive is consulted on every "
                     "event but only ACTS on installed monitors. Install ONLY patterns "
                     "grounded in research -- this is a mechanism, not a way to script "
                     "behaviour (design doc §2.9).")}

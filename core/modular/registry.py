"""
registry.py -- the neutral plug-in module system.

A PsychSim *module* is a research study plugged into the neutral core: it declares
how it perturbs the baseline spawn (child/adult disposition sources), what world
content it supplies, how it reads behaviour into its own categories, its default
params, and how it reports. The core stays psychology-free -- this file names NO
system, disposition, or study; it only carries callables a study provides.

A module is discovered by dropping a package under `extensions/<name>/` whose
`__init__.py` exposes a top-level `MODULE = Module(...)`. Nothing in `project.py`
is edited to add a study.
"""

from __future__ import annotations
import importlib
import os
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


@dataclass(frozen=True)
class Module:
    """What a research study declares to the platform. Every hook is optional;
    `None` means "use the core default". Hook signatures (kept as comments so this
    file imports nothing from a study):

      child_source(rng, params) -> (() -> TraitSeed)   # the child disposition source
      adult_source(rng, params) -> (() -> TraitSeed)   # the adult disposition source
      world_content(city, population, params) -> dict  # {venues, categorise, groups, ...}
      categorise(network, affordance) -> str           # study reading of a settled network
      report(engine_or_universe, params) -> object     # an object with .to_dict()/.text()
    """
    name: str                                   # registry key == extensions/<name>/ dir
    title: str
    description: str = ""
    child_source: Optional[Callable] = None
    adult_source: Optional[Callable] = None
    world_content: Optional[Callable] = None
    categorise: Optional[Callable] = None
    report: Optional[Callable] = None
    default_params: Dict[str, object] = field(default_factory=dict)

    def hooks(self) -> List[str]:
        """The hooks this module actually supplies (for display/introspection)."""
        return [h for h in ("child_source", "adult_source", "world_content",
                            "categorise", "report")
                if getattr(self, h) is not None]

    def info(self) -> Dict[str, object]:
        """A JSON-serialisable description for a selection UI."""
        return {"name": self.name, "title": self.title,
                "description": self.description,
                "params": dict(self.default_params), "hooks": self.hooks()}


def discover_modules(ext_dir: str) -> Dict[str, "Module"]:
    """Lazily scan `ext_dir` for packages exposing a top-level `MODULE`. Sorted and
    deterministic; a package that fails to import is skipped, not fatal (one broken
    study cannot take down the platform). Call this at spawn time only -- never at
    import time -- so the extensions' imports have settled (avoids import cycles)."""
    out: Dict[str, Module] = {}
    if not os.path.isdir(ext_dir):
        return out
    for name in sorted(os.listdir(ext_dir)):
        if name.startswith((".", "_")):
            continue
        if not os.path.isdir(os.path.join(ext_dir, name)):
            continue
        try:
            pkg = importlib.import_module(name)          # extensions/ is on sys.path
        except Exception:
            continue
        m = getattr(pkg, "MODULE", None)
        if isinstance(m, Module):
            out[m.name] = m
    return out

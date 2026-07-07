"""
project.py -- new-project startup: name it, pick extensions, spawn the universe.

This is the reset / start point for any new piece of research. A project is
described by a name, a target community size, a demography profile, and a choice
of extensions (the "dropdown"); spawning it builds a demographically convincing
settlement (from real ONS/DfT ratios), populates it with a society, and applies
whatever the selected extensions contribute -- for the sophropathy study, seeding
a minority of children with the fearless (proto-psychopath) disposition it exists
to follow. The result is a runnable universe.

The core stays neutral: it spawns a balanced society working as it should. Each
extension declares, in the registry below, how it perturbs that baseline, so a
different study is a different selection -- the core is untouched.
"""

from __future__ import annotations
import sys, os
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional
import random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "core"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "extensions"))

from sim_viz import (SettlementSpec, generate_settlement, settlement_inventory,
                     DemographyProfile, ENGLAND_2021, RURAL_VILLAGE, INNER_CITY,
                     spec_for_population)
from sim_viz.mapmodel import CityMap, Actor
from sim_world import populate, Population
from sim_world.population import HouseholdProfile
from affective_engine.core import sophropathic_seed
from modular import discover_modules
from config.loader import load_town_profiles, load_module_params
from config.townprofile import TownProfile


# ---------------------------------------------------------------------------
# Modules (the "dropdown") + town/culture profiles -- discovered, not hard-coded.
# The core names no study: modules are found under extensions/, profiles under data/.
# ---------------------------------------------------------------------------

_EXT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extensions")

# built-in town profiles resolve to their Python constants (identity), so their
# demography/garden behaviour is byte-for-byte unchanged; JSON under data/towntypes/ is
# authoritative for any NEW town-type.
_BUILTIN_DEMO = {"england_2021": ENGLAND_2021, "rural_village": RURAL_VILLAGE,
                 "inner_city": INNER_CITY}


def _modules():
    return discover_modules(_EXT_DIR)


def available_modules() -> List[Dict[str, object]]:
    """Full descriptions of the plug-in modules found under extensions/ (for a UI)."""
    return [m.info() for m in _modules().values()]


def available_extensions() -> Dict[str, str]:
    """name -> title, for a selection dropdown (discovered modules)."""
    return {m.name: m.title for m in _modules().values()}


def available_profiles() -> List[str]:
    """Built-in town-types first, then any JSON town-types under data/towntypes/."""
    names = list(_BUILTIN_DEMO)
    for n in load_town_profiles():
        if n not in names:
            names.append(n)
    return names


def resolve_profile(name: str) -> TownProfile:
    """A town/culture profile (demography + household composition). Built-ins are the
    Python constants (identity, so existing spawns are unchanged); other names load from
    data/towntypes/<name>.json; an unknown name falls back to england_2021."""
    if name in _BUILTIN_DEMO:
        return TownProfile(name, _BUILTIN_DEMO[name], HouseholdProfile())
    profiles = load_town_profiles()
    if name in profiles:
        return profiles[name]
    return TownProfile("england_2021", ENGLAND_2021, HouseholdProfile())


# ---------------------------------------------------------------------------
# Project spec and the spawned universe
# ---------------------------------------------------------------------------

@dataclass
class ProjectSpec:
    name: str = "New Project"
    target_population: int = 250
    profile: str = "england_2021"                          # a town-type key (built-in or JSON)
    extensions: List[str] = field(default_factory=list)    # selected module names
    fearless_frac: Optional[float] = None                  # DEPRECATED alias -> module_params["sophropathy"]
    seed: int = 0
    module_params: Dict[str, dict] = field(default_factory=dict)  # per-module params


@dataclass
class Universe:
    project: ProjectSpec
    spec: SettlementSpec
    city: CityMap
    population: Population
    extensions: List[str]
    content: Dict[str, dict] = field(default_factory=dict)   # per-module world content

    def summary(self) -> Dict[str, object]:
        return {"project": self.project.name,
                "extensions": self.extensions,
                "inventory": settlement_inventory(self.city),
                "society": self.population.summary()}


def spawn_universe(spec: ProjectSpec, place_residents: bool = True) -> Universe:
    """Spawn a runnable universe for a project: size a settlement from real
    demography, generate and populate it, and apply the selected extensions."""
    rng = random.Random(spec.seed)
    profile = resolve_profile(spec.profile)
    demo = profile.demography

    # 1. size + generate the settlement from the profile's demography ratios
    sett = spec_for_population(spec.target_population, demo, name=spec.name, seed=spec.seed)
    city = generate_settlement(sett)

    # 2. disposition sources: ordinary by default; selected modules may override.
    #    Params layer: module defaults <- data/modules/<name>.json <- spec.module_params
    #    (+ the deprecated spec.fearless_frac alias, for the sophropathy module only).
    modules = _modules()
    file_params = load_module_params()
    adult_source = sophropathic_seed
    child_source = sophropathic_seed
    selected = {}
    for ext in spec.extensions:
        m = modules.get(ext)
        if not m:
            continue
        params = {**m.default_params, **file_params.get(ext, {})}
        if spec.fearless_frac is not None and ext == "sophropathy":
            params["fearless_frac"] = spec.fearless_frac        # deprecated alias (base)
        params.update(spec.module_params.get(ext, {}))          # explicit module_params win
        selected[ext] = (m, params)
        if m.child_source:
            child_source = m.child_source(rng, params)
        if m.adult_source:
            adult_source = m.adult_source(rng, params)

    # 3. populate as a society, with the profile's household composition
    pop = populate(city, seed=spec.seed, adult_seed=adult_source, child_seed=child_source,
                   mean_household=demo.mean_household, household_profile=profile.household)

    # 3b. modules' world content (needs the populated society)
    content = {}
    for ext, (m, params) in selected.items():
        if m.world_content:
            content[ext] = m.world_content(city, pop, params)

    # 3c. outdoor space: garden access and size by tenure AND settlement type
    grng = random.Random(spec.seed + 101)
    base_size = {"owner": 0.7, "private_rent": 0.5, "social_rent": 0.4}
    for hh in pop.households:
        gp = demo.garden_prob_by_tenure.get(hh.tenure, 0.8) * demo.garden_area_multiplier
        hh.garden = grng.random() < min(1.0, gp)
        hh.garden_size = (min(1.0, base_size.get(hh.tenure, 0.5) * demo.garden_size_scale)
                          if hh.garden else 0.0)
        if hh.garden:                                   # a garden adds to comfort/space
            hh.comfort = min(1.0, hh.comfort + 0.08 * hh.garden_size)

    # 4. optionally place resident figures on the map at their homes
    if place_residents:
        home_cell = {p.place: (p.x, p.y) for p in city.objects
                     if p.place and p.place.startswith("home")}
        for hh in pop.households:
            if hh.home in home_cell:
                x, y = home_cell[hh.home]
                for mm in hh.members()[:2]:
                    sprite = "char_child_a" if mm in pop.pupils else "char_adult_a"
                    city.actors.append(Actor(sprite=sprite, x=x, y=y, agent_id=mm))

    return Universe(spec, sett, city, pop, list(spec.extensions), content)


# ---------------------------------------------------------------------------
# CLI: spawn and report (a startup demonstration)
# ---------------------------------------------------------------------------

def _demo():
    print("Available extensions (dropdown):")
    for k, title in available_extensions().items():
        print(f"  [{k}] {title}")
    print("Available demography profiles:", available_profiles(), "\n")

    proj = ProjectSpec(name="Ashcombe study", target_population=250,
                       profile="rural_village", extensions=["sophropathy"], seed=7)
    uni = spawn_universe(proj)
    s = uni.summary()
    print(f"Spawned universe for project: {s['project']}")
    print(f"  extensions applied : {s['extensions']}")
    print(f"  settlement          : {s['inventory']}")
    print(f"  society             : {s['society']}")
    return uni


if __name__ == "__main__":
    _demo()

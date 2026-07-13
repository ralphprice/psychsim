"""
library.py -- a cached library of GROWN adults (the controlled-experiment population).

The discipline (design doc §0/§2) forbids scripting a personality via attributes. A
mind's strength profile must be GROWN by living experience through the substrate; the
only "given" attributes are the temperament seed (inherited reactivity bias), the
rearing environment, role, and position. This module respects that:

    grow_adult(temperament_seed, rearing_environment) -> a mind grown to adulthood
    on the substrate, by the SAME developmental machinery the life-stepper runs
    (activities -> live_stimulus, world things -> encounter, groups -> group_encounter,
    the always-on executive monitored). It mirrors timeline_driver's `_episode`,
    decoupled from a spawned universe so each adult's temperament and rearing can be
    set explicitly -- which IS the point of a controlled background population.

Why cache adults at all (design decision, permanent -- not a stepping stone):
    A controlled experiment needs a FIXED, evolved background population -- identical
    across conditions -- around which only the study subjects (the children under
    study) evolve live. Growing that background once and caching it (brain + seed +
    rearing + role) makes it reproducible and cheap to reuse. See the two modes in the
    handover.

Honest caveat: the quality of a grown-adult library depends on substrate maturity. The
current crude substrate funnels most minds toward SEEKING, so a library cached today is
weakly differentiated -- fine as background scenery (temperaments still vary via the
seed) and it gets richer as the substrate matures.
"""

from __future__ import annotations
import json
import os
import random
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from affective_engine.core import Appraisal, TraitSeed
from substrate.readout import read_mind
from affective_engine.agent import AffectiveAgent
from affective_engine.development import (Environment, live_moment, live_stimulus,
                                          situation, _colour_by_env, CHILDHOOD_CYCLE,
                                          warm_firm_home, harsh_inconsistent_home)
from affective_engine.activities import sample_activity
from sim_world.environment_matrix import default_things, birth_matrix, encounter
from sim_world.group_matrix import (default_groups, GroupMatrix, group_encounter,
                                    sample_encounter_type)

from .society import (typical_child_seed, fearless_child_seed,
                      fearless_calculating_child_seed)

# where the shipped/generated library lives (repo-root/library)
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIBRARY_DIR = os.path.join(_ROOT, "library")
DEFAULT_LIBRARY = os.path.join(LIBRARY_DIR, "adults.json")

_DELIBERATIVE = {"learning", "achievement", "independence", "exploration"}


def a_middling_home() -> Environment:
    """An ordinary, middling rearing environment (neither the warm-firm ideal nor
    the harsh-inconsistent one)."""
    return Environment("ordinary", 0.55, 0.55, 0.55)


# the temperament seeds we grow the background from (given inherited reactivity only)
TEMPERAMENTS: Dict[str, Callable[[], TraitSeed]] = {
    "typical": typical_child_seed,
    "fearless": fearless_child_seed,                       # the shared proto-psychopath root
    "fearless_calculating": fearless_calculating_child_seed,
}
REARINGS: Dict[str, Callable[[], Environment]] = {
    "warm_firm": warm_firm_home,
    "ordinary": a_middling_home,
    "harsh": harsh_inconsistent_home,
}


def new_dev_context() -> dict:
    """A fresh developmental context: the world's things and the child's evolving
    environment-matrix and group-matrix. One per developing mind. There is no separate
    executive layer -- control is the substrate's own STN brake (behaviour.py), which matures
    with age in the selection race; the Panksepp learned-monitor executive was retired."""
    return {"env_matrix": birth_matrix(default_things()),
            "group_matrix": GroupMatrix(),
            "things": default_things(),
            "groups": default_groups()}


def develop_episode(agent: AffectiveAgent, rearing: Environment, age_years: float,
                    rng: random.Random, ctx: dict, *, situation_step: bool = False):
    """ONE developmental episode on the substrate, at the child's current age. This is
    the single source of truth for "a developmental moment", used both to grow the
    library's adults and to develop live study subjects in the engine. It mirrors the
    life-stepper's `_episode`: an age-appropriate activity (or, on a `situation_step`, a
    rearing-coloured situation), an encounter with one of the world's things, a moment in
    a group, and the always-on executive monitored. GIVEN: temperament (in the agent) +
    rearing; GROWN: what the episode strengthens. Nothing about the outcome is typed in."""
    things, groups = ctx["things"], ctx["groups"]
    if situation_step:
        # a rearing-coloured situation -- the home's tone shapes WHICH situations arise,
        # never their effect; the child's own systems decide.
        appr = _colour_by_env(situation(rng.choice(CHILDHOOD_CYCLE), rng), rearing)
        live_moment(agent, appr, age_years=age_years)
        deliberative = False
    else:
        act = sample_activity(age_years, rng)
        live_stimulus(agent, act.stimulus, age_years=age_years)
        deliberative = act.id in _DELIBERATIVE
    thing = rng.choices(things, weights=[t.frequency for t in things], k=1)[0]
    encounter(agent, thing, ctx["env_matrix"], age_years=age_years)
    grp = rng.choice(groups)
    mem = ctx["group_matrix"].membership(grp.id, grp.kind)
    pre = mem.standing + mem.belonging
    gresp = group_encounter(agent, grp, mem, sample_encounter_type(rng),
                            age_years=age_years)
    post = mem.standing + mem.belonging
    agent.memory.add(label=grp.kind, appraisal=Appraisal(label=grp.kind),
                     dominant=gresp.behaviour,
                     valence=max(-1.0, min(1.0, post - pre)), importance=0.5)
    return gresp


def grow_adult(temperament: TraitSeed, rearing: Environment, *, seed: int,
               childhood_years: float = 18.0, episodes_per_year: float = 3.0) -> AffectiveAgent:
    """Grow ONE mind to adulthood on the substrate, from a temperament seed and a
    rearing environment. GIVEN: temperament (reactivity bias) + rearing. GROWN: the
    whole strength profile, from what a childhood of activities, things and groups
    happens to engage. Nothing about the outcome is written in. Returns the grown
    AffectiveAgent (its `.engine` is the developed substrate; `read_mind(agent)` reads it out)."""
    rng = random.Random(seed)
    agent = AffectiveAgent(seed=temperament, temperament_seed=seed)
    ctx = new_dev_context()
    total_ep = max(6, int(round(childhood_years * episodes_per_year)))
    for i in range(total_ep):
        age_years = childhood_years * (i / total_ep)
        develop_episode(agent, rearing, age_years, rng, ctx, situation_step=(i % 3 == 2))
    return agent


# ---------------------------------------------------------------------------
# a cached entry + the library
# ---------------------------------------------------------------------------

@dataclass
class LibraryEntry:
    """A cached grown adult: the given inputs (temperament, rearing, role, seed) and
    the grown result (the serialised brain + its descriptive read-out)."""
    name: str
    temperament: str
    rearing: str
    role: str
    seed: int
    state: dict                    # the AgentBank snapshot of the grown DevelopedAgent (substrate)
    dominant: str
    profile: Dict[str, float]

    def make_agent(self):
        """Restore the grown DevelopedAgent (substrate) for placement into a running sim.
        Restored-never-edited, via the bank's own restore -- the single serialization path."""
        from agent_bank import restore
        return restore(self.state)

    def to_dict(self) -> dict:
        return {"name": self.name, "temperament": self.temperament,
                "rearing": self.rearing, "role": self.role, "seed": self.seed,
                "state": self.state, "dominant": self.dominant, "profile": self.profile}

    @staticmethod
    def from_dict(d: dict) -> "LibraryEntry":
        return LibraryEntry(name=d["name"], temperament=d["temperament"],
                            rearing=d["rearing"], role=d.get("role", "adult"),
                            seed=int(d["seed"]), state=d["state"],
                            dominant=d["dominant"], profile=d["profile"])


@dataclass
class CharacterLibrary:
    """A library of grown adults, serialisable to/from JSON."""
    entries: List[LibraryEntry] = field(default_factory=list)

    def grow(self, name: str, temperament_key: str, rearing_key: str, *, seed: int,
             role: str = "adult", **grow_kw) -> LibraryEntry:
        """Grow one adult from named temperament + rearing and add it to the library."""
        temperament = TEMPERAMENTS[temperament_key]()
        rearing = REARINGS[rearing_key]()
        agent = grow_adult(temperament, rearing, seed=seed, **grow_kw)
        r = read_mind(agent)
        # persist the GROWN developed substrate through the bank's serialization -- the single
        # substrate-serialization path (grown-and-banked, restored-never-edited). No parallel serializer.
        from agent_bank import DevelopedAgent, snapshot
        # carry the GIVEN physical endowment + sex the adult grew with, so a restored adult reloads
        # its real traits (restored-never-edited), not a fresh sample (v10 E1).
        dev = DevelopedAgent(engine=agent.engine,
                             physical=dict(agent.physical), sex=agent.sex,
                             signature=list(agent.signature),   # v14: carry the given kin signature
                             provenance={"temperament": temperament_key, "rearing": rearing_key,
                                         "seed": seed})
        entry = LibraryEntry(name=name, temperament=temperament_key, rearing=rearing_key,
                             role=role, seed=seed, state=snapshot(dev),
                             dominant=r.dominant.value, profile=r.profile)
        self.entries.append(entry)
        return entry

    def save(self, path: str = DEFAULT_LIBRARY) -> str:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump({"adults": [e.to_dict() for e in self.entries]}, f, indent=2)
        return path

    @staticmethod
    def load(path: str = DEFAULT_LIBRARY) -> "CharacterLibrary":
        with open(path) as f:
            data = json.load(f)
        return CharacterLibrary([LibraryEntry.from_dict(e) for e in data.get("adults", [])])

    @staticmethod
    def exists(path: str = DEFAULT_LIBRARY) -> bool:
        return os.path.isfile(path)


# a small, fixed roster of names so the shipped library is stable and readable
_NAMES = ["Alan", "Bea", "Cora", "Dev", "Esme", "Finn", "Greta", "Hugo",
          "Iris", "Joel", "Kira", "Liam", "Mara", "Noor", "Omar", "Petra",
          "Quinn", "Rhys", "Sena", "Tariq"]


def build_default_library(seed: int = 20260706) -> CharacterLibrary:
    """Grow a small, curated, DETERMINISTIC background library over varied temperament
    seeds x rearing environments. Deterministic (fixed per-adult seeds) so the shipped
    `library/adults.json` is reproducible. Weakly differentiated at this crude stage --
    honest background scenery whose temperaments still vary by seed."""
    lib = CharacterLibrary()
    i = 0
    for temp in TEMPERAMENTS:
        for rear in REARINGS:
            name = _NAMES[i % len(_NAMES)]
            lib.grow(name, temp, rear, seed=seed + i * 101, role="adult")
            i += 1
    return lib

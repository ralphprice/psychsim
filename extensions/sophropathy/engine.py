"""
engine.py -- a LIVE, continuously-steppable PsychSim town simulation.

Where townlife.simulate_townlife pre-computes a whole clip in one go, SimEngine holds a
running simulation you advance one tick at a time (`step()`), snapshot at any moment
(`snapshot()`), inspect per person (`person_detail()`), and control live (spawn a new
town, add a person, change the tick rate). This is the Park-style loop: is -> decide ->
move -> repeat, streamable to a frontend.

The mind stays on the substrate throughout: the engine decides where people are and how
they move; what they feel and remember when they meet still emerges (townlife encounters
run through the group matrix and write to each person's memory stream).
"""

from __future__ import annotations
import json
import os
import pickle
import random
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from project import ProjectSpec, spawn_universe
from substrate.readout import read_mind
from affective_engine.agent import _SUBSTRATE_MODEL as _SUB_MODEL   # shared v9 seed (read-only)
from affective_engine.core import Appraisal
from sim_world.group_matrix import (GroupMatrix, default_groups, group_encounter,
                                     sample_encounter_type)

from sim_world.person import Person

from .world import venues_for
from .townlife import (build_town_space, scheduled_block, role_block, role_is_child,
                       ROLE_SCHEDULES, _people_roles_homes, astar, _WALK_SPEED)
from .society import (typical_child_seed, fearless_child_seed,
                      fearless_calculating_child_seed)
from .module import live_spec                     # canonical live ProjectSpec (single source)

# temperament seeds a caller may author a fresh study subject from. GIVEN temperament
# only (inherited reactivity bias); the personality then GROWS on the substrate, over a
# REAL life span -- development is the life-stepper's job, tied to the real clock; the
# live engine does NOT run any separate/compressed developmental clock.
TEMPERAMENT_SEEDS = {
    "typical": typical_child_seed,
    "fearless": fearless_child_seed,                       # the shared proto-psychopath root
    "fearless_calculating": fearless_calculating_child_seed,
}

Cell = Tuple[int, int]
_DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# --- Sim wall-clock (Phase 8) ---------------------------------------------
# The sim clock starts at this epoch and each tick advances the world by `tick_minutes` sim-minutes
# (the explicit tick<->time mapping; default 15 -> 4 ticks/hour). The epoch is a constant OF THE SIM
# CLOCK, not a client offset: sim_time = SIM_EPOCH + minutes, and the UI only formats it.
SIM_EPOCH = datetime(2000, 1, 1, 0, 0, 0)

# where saved simulations live (repo-root/sims), and a safe filename maker
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAVE_DIR = os.path.join(_ROOT, "sims")


def _slug(name: str) -> str:
    """A safe filename stem from a save name (no path separators, no surprises)."""
    s = re.sub(r"[^A-Za-z0-9_-]+", "_", (name or "").strip()).strip("_")
    return s or "sim"


class SimEngine:
    """A running town. Advance it with step(); read it with snapshot()."""

    # how many residents' (expensive, read-only) drive read-out to refresh per /state poll;
    # the rest serve a cached label, so a polled snapshot stays fast (see snapshot()).
    _DRIVE_REFRESH_PER_POLL = 8

    def __init__(self, population: int = 80, seed: int = 7, tick_minutes: int = 15,
                 name: str = "Ashcombe", experiment: bool = False,
                 library=None, study_subjects: Optional[List[str]] = None,
                 fearless_frac: float = 0.4, profile: str = "england_2021"):
        self.tick_minutes = tick_minutes
        self.name = name
        # controlled-experiment mode: a FIXED, grown-adult background (from the
        # character library) around which only the study subjects evolve live.
        self.experiment = experiment
        self.library = library
        self.study_subjects = study_subjects
        self.fearless_frac = fearless_frac      # the sophropath module's live knob
        self.profile = profile                  # town-type / culture profile at spawn
        self._spawn(population, seed)

    # -- construction / (re)spawn ------------------------------------------
    def _spawn(self, population: int, seed: int):
        self.population_n = population
        self.seed = seed
        self.rng = random.Random(seed)
        self.spec = live_spec(self.name, population, seed,
                              fearless_frac=getattr(self, "fearless_frac", 0.4),
                              profile=getattr(self, "profile", "england_2021"))
        self.uni = spawn_universe(self.spec, place_residents=False)
        self.pop = self.uni.population
        self.venues = venues_for(self.uni.city, self.pop)
        self.space = build_town_space(self.uni.city, self.venues)
        self.info = _people_roles_homes(self.uni)
        self.groups = default_groups()
        self.gmats: Dict[str, GroupMatrix] = {cid: GroupMatrix() for cid in self.info}
        a_tile = next(iter(self.space.walk), (0, 0))
        self.state = {}
        for cid, (is_child, home, work) in self.info.items():
            hc = self.space.place_cell(home) or a_tile
            self.state[cid] = {"tile": hc, "path": [], "pi": 0, "target": home,
                               "jitter": self.rng.uniform(-0.5, 0.5)}
        self.minutes = 0
        self.step_count = 0
        self._leisure = {"shop": next((p for p in self.space.cells if p.startswith("shop")), None),
                         "pub": next((p for p in self.space.cells if p.startswith("pub")), None)}
        self._a_park = a_tile
        # who evolves live. Default (open-ended mode): everyone. Experiment mode:
        # only the study subjects; the rest are a fixed, grown background.
        self.roles: Dict[str, str] = self._assign_roles()   # fine role per resident
        self.frozen: set = set()
        self.subjects: set = set(self.info)
        self.tempers: Dict[str, str] = {}          # authored subjects' chosen temperament
        self._subject_log: Dict[str, list] = {}    # per-subject trajectory (report samples)
        if self.experiment:
            self._load_background()

    def _assign_roles(self) -> Dict[str, str]:
        """Assign each resident a fine role from the library, deterministically (a
        SEPARATE rng, so the main stream is untouched). Children split into
        preschooler / teenager / child; adults into teacher / retired / adult by the
        town-type's elderly fraction. Roles beyond child/adult only apply if their data
        file is present (else everyone stays child/adult -- byte-identical)."""
        rng = random.Random(self.seed + 202)
        pop = self.uni.population
        _t = getattr(pop, "teachers", {})            # {school -> teacher_id}
        teachers = set(_t.values() if isinstance(_t, dict) else _t)
        try:
            from project import resolve_profile
            demo = resolve_profile(self.uni.project.profile).demography
            elderly_of_adults = demo.elderly_frac / max(1e-6, demo.working_age_frac + demo.elderly_frac)
        except Exception:
            elderly_of_adults = 0.22
        has = lambda r: r in ROLE_SCHEDULES
        out: Dict[str, str] = {}
        for cid, (is_child, home, work) in self.info.items():
            if is_child:
                r = rng.random()
                out[cid] = ("preschooler" if has("preschooler") and r < 0.22 else
                            "teenager" if has("teenager") and r < 0.55 else "child")
            else:
                out[cid] = ("teacher" if cid in teachers and has("teacher") else
                            "retired" if has("retired") and rng.random() < elderly_of_adults
                            else "adult")
        return out

    def _load_background(self):
        """Controlled-experiment mode: replace the non-subject ADULTS' minds with
        FIXED, grown-adult brains from the character library, and freeze every
        non-subject so its personality (brain) does not drift -- an identical evolved
        background across conditions is the experimental control. Subjects default to
        the children under study; an explicit study_subjects list overrides."""
        from .library import CharacterLibrary, DEFAULT_LIBRARY, build_default_library
        lib = self.library
        if lib is None:
            lib = (CharacterLibrary.load(DEFAULT_LIBRARY)
                   if CharacterLibrary.exists(DEFAULT_LIBRARY) else build_default_library())
        self.library = lib
        entries = lib.entries or build_default_library().entries
        if self.study_subjects is not None:
            subjects = set(self.study_subjects) & set(self.info)
        else:
            subjects = {cid for cid, (is_child, _, _) in self.info.items() if is_child}
        self.subjects = subjects
        self.frozen = set()
        i = 0
        for cid in sorted(self.info):
            if cid in subjects:
                continue
            is_child, home, work = self.info[cid]
            person = self.pop.persons.get(cid)
            if person is not None and not is_child:
                # a grown library adult's developed substrate, restored from the bank and
                # dropped in deterministically so the background is identical across
                # conditions/runs of the same town (restored-never-edited).
                person.mind.adopt_engine(entries[i % len(entries)].make_agent().engine)
                i += 1
            self.frozen.add(cid)

    def respawn(self, population: Optional[int] = None, seed: Optional[int] = None,
                experiment: Optional[bool] = None, study_subjects="__keep__",
                fearless_frac: Optional[float] = None, profile: Optional[str] = None):
        if experiment is not None:
            self.experiment = experiment
        if study_subjects != "__keep__":
            self.study_subjects = study_subjects
        if fearless_frac is not None:
            self.fearless_frac = float(fearless_frac)
        if profile:
            self.profile = profile
        self._spawn(population or self.population_n,
                    seed if seed is not None else self.seed + 1)

    # -- one tick of the world ---------------------------------------------
    def _resolve(self, cid, place_key, room):
        is_child, home, work = self.info[cid]
        if place_key == "home":
            return home
        if place_key == "school":
            return next((p for p in self.space.cells if p.startswith("school")), home)
        if place_key == "work":
            return work or home
        if place_key == "leisure":
            lp = self._leisure.get(room)
            return lp if lp else "__park__"
        return home

    def step(self):
        """Advance the world one tick: move everyone along their schedule, and run
        encounters where people share a place (emergent, remembered)."""
        hour = ((self.minutes // self.tick_minutes) % (24 * 60 // self.tick_minutes)
                * self.tick_minutes) / 60.0
        day = self.minutes // (24 * 60)
        is_weekend = (day % 7) >= 5
        for cid, st in self.state.items():
            is_child, home, work = self.info[cid]
            pk, room = role_block(self.roles.get(cid, "child" if is_child else "adult"),
                                  hour + st["jitter"], is_weekend)
            place = self._resolve(cid, pk, room)
            if place == "__park__":
                goal, target = self._a_park, None
            else:
                goal, target = self.space.place_cell(place), place
            if st["target"] != target:
                st["target"] = target
                st["path"] = (self.space.route(st["tile"], target) if target
                              else (astar(st["tile"], goal, self.space.walk) if goal else []))
                st["pi"] = 0
            if st["path"] and st["pi"] < len(st["path"]) - 1:
                st["pi"] = min(st["pi"] + _WALK_SPEED, len(st["path"]) - 1)
                st["tile"] = st["path"][st["pi"]]
            elif goal:
                st["tile"] = goal
        # encounters where people co-locate
        byplace: Dict[Cell, List[str]] = {}
        for cid, st in self.state.items():
            byplace.setdefault(st["tile"], []).append(cid)
        for cell, here in byplace.items():
            if len(here) >= 2:
                for cid in here[:4]:
                    person = self.pop.persons.get(cid)
                    if person is None:
                        continue
                    grp = self.groups[hash(cell) % len(self.groups)]
                    mem = self.gmats[cid].membership(grp.id, grp.kind)
                    before = mem.standing + mem.belonging
                    # background (frozen) minds still ACT, but their personality does
                    # not change: gate use-dependent strengthening off for them.
                    r = group_encounter(person.mind, grp, mem,
                                        sample_encounter_type(self.rng), age_years=20,
                                        develop=(cid not in self.frozen))
                    after = mem.standing + mem.belonging
                    person.mind.memory.add(
                        label=f"with {len(here)-1} others at {grp.name}",
                        appraisal=Appraisal(label=grp.name),
                        dominant=r.behaviour,
                        valence=max(-1.0, min(1.0, after - before)), importance=0.4)
        prev_day = self.minutes // (24 * 60)
        self.minutes += self.tick_minutes
        self.step_count += 1
        if self.minutes // (24 * 60) != prev_day:      # sample study subjects on day rollover
            self._log_subjects()

    def library_info(self) -> dict:
        """Describe the grown-adult library available as fixed background (the current
        one if in experiment mode, else the shipped/default one)."""
        from .library import CharacterLibrary, DEFAULT_LIBRARY, build_default_library
        lib = self.library
        if lib is None:
            lib = (CharacterLibrary.load(DEFAULT_LIBRARY)
                   if CharacterLibrary.exists(DEFAULT_LIBRARY) else build_default_library())
        return {"count": len(lib.entries),
                "adults": [{"name": e.name, "temperament": e.temperament,
                            "rearing": e.rearing, "dominant": e.dominant}
                           for e in lib.entries]}

    # -- reading the world -------------------------------------------------
    def clock_label(self) -> str:
        day = self.minutes // (24 * 60)
        hh = (self.minutes % (24 * 60)) // 60
        mm = self.minutes % 60
        return f"{_DAY_NAMES[day % 7]} {hh:02d}:{mm:02d}"

    def town(self) -> dict:
        """Static town geometry for the frontend to draw once."""
        c = self.uni.city
        return {
            "cols": c.cols, "rows": c.rows,
            "terrain": c.terrain,
            "roads": [[p.x, p.y] for p in c.roads],
            "buildings": [{"place": o.place, "kind": o.tile, "x": o.x, "y": o.y,
                           "w": o.footprint[0], "h": o.footprint[1]}
                          for o in c.objects if o.tile.startswith("building")
                          and getattr(o, "place", None)],
            "props": [{"kind": o.tile, "x": o.x, "y": o.y}
                      for o in c.objects if o.tile.startswith("prop")],
        }

    def plan(self, cell: int = 64, pad: int = 20) -> dict:
        """The designed top-down "glass-roof" plan view, as an SVG string, plus the
        grid->pixel mapping so a frontend can overlay live people on it.

        The picture IS the model: every building is drawn by render_settlement_plan
        from the SAME Venue/Area/AffordanceObject data the simulation runs on. A
        person at snapshot tile (x, y) belongs at pixel
        (pad + x*cell + cell/2, pad + y*cell + cell/2) -- the same mapping the batch
        watchable-town renderer uses to place its dots."""
        from sim_viz.floorplan import render_settlement_plan
        c = self.uni.city
        svg = render_settlement_plan(c, self.venues, occupants=None,
                                     cell=cell, pad=pad)
        return {"svg": svg, "cell": cell, "pad": pad,
                "cols": c.cols, "rows": c.rows,
                "width": c.cols * cell + 2 * pad,
                "height": c.rows * cell + 2 * pad}

    def snapshot(self) -> dict:
        """Live per-person state: position + emergent drive, plus the clock.

        The per-person `drive` is a read_mind() dominant-domain read-out. Since the substrate
        migration read_mind runs a 25-tick freeze-restore settle (~20ms/resident), so computing it
        for the whole town on every /state poll costs ~1s and makes a polled endpoint unusable
        (the browser aborts the slow poll -> BrokenPipeError). We AMORTISE it: refresh only a few
        residents' drive per call (round-robin) and serve the cached label for the rest, so a poll
        stays fast. This is a pure STALENESS/caching change -- read_mind is the same read-only
        measurement (freeze-restore, no development), just called on fewer residents per poll; a
        drive label lags a few polls while positions/clock stay live. The read-only wall holds:
        snapshotting never develops an agent."""
        if not hasattr(self, "_drive_cache"):
            self._drive_cache = {}                        # cid -> last drive read-out (string)
            self._drive_rr = 0                            # round-robin cursor across residents
        cids = list(self.state.keys())
        n = len(cids)
        k = min(self._DRIVE_REFRESH_PER_POLL, n)
        refresh = {cids[(self._drive_rr + i) % n] for i in range(k)} if n else set()
        self._drive_rr = (self._drive_rr + k) % n if n else 0
        people = {}
        for cid, st in self.state.items():
            person = self.pop.persons.get(cid)
            if person is not None and cid in refresh:     # read_mind: read-only measurement, no develop
                dom = read_mind(person.mind).dominant
                self._drive_cache[cid] = (dom.value if hasattr(dom, "value") else str(dom)) if dom else ""
            people[cid] = {
                "x": st["tile"][0], "y": st["tile"][1],
                "drive": self._drive_cache.get(cid, ""),  # cached; "" until this cid's first refresh
                "role": "child" if self.info[cid][0] else "adult",
                "role_name": self.roles.get(cid),        # fine role (child/teenager/retired/...)
                "subject": cid not in self.frozen,       # evolves live vs fixed background
            }
        sim_dt = SIM_EPOCH + timedelta(minutes=self.minutes)
        return {"clock": self.clock_label(), "minutes": self.minutes,
                "step": self.step_count, "tick": self.step_count,
                # sim wall-clock: epoch is a server-side constant; sim_time = epoch + elapsed minutes
                "epoch": SIM_EPOCH.isoformat(), "sim_time": sim_dt.isoformat(),
                "elapsed_hours": self.minutes // 60,
                "experiment": self.experiment,
                "subjects": len(self.subjects), "background": len(self.frozen),
                "seed": self.seed, "version": _SUB_MODEL.meta.get("version", "?"),
                "people": people}

    def person_detail(self, cid: str) -> dict:
        """Full inspectable state for one person."""
        person = self.pop.persons.get(cid)
        if person is None or cid not in self.info:
            return {}
        is_child, home, work = self.info[cid]
        return {
            "cid": cid, "name": getattr(person, "name", cid),
            "role": "child" if is_child else "adult", "home": home, "work": work,
            "role_name": self.roles.get(cid),
            "subject": cid not in self.frozen,
            "mind_state": "background (fixed)" if cid in self.frozen else "study subject (live)",
            "temperament": self.tempers.get(cid),        # set for authored subjects
            "systems": {k: round(v, 3) for k, v in read_mind(person.mind).profile.items()},
            "memories": [{"label": m.label, "valence": round(m.valence, 2)}
                         for m in person.mind.memory.events[-15:]],
            "groups": [{"group": m.group_id, "standing": round(m.standing, 2),
                        "belonging": round(m.belonging, 2), "route": m.status_route()}
                       for m in self.gmats[cid].memberships.values()],
        }

    # -- development reports (descriptive read-outs, honest about real time) ----
    def _log_subjects(self, cap: int = 400) -> None:
        """Append one trajectory sample per study subject (on day rollover). Bounded.
        Development runs over REAL time -- samples accrue as real sim-days pass."""
        from .report import sample_subject
        for cid in self.subjects:
            if cid in self.pop.persons and cid in self.info:
                log = self._subject_log.setdefault(cid, [])
                log.append(sample_subject(self, cid))
                if len(log) > cap:
                    del log[0:len(log) - cap]

    def subject_report(self, cid: str):
        from .report import subject_report as _sr
        return _sr(self, cid)

    def cohort_report(self, cids=None):
        from .report import cohort_report as _cr
        return _cr(self, cids)

    # -- live control ------------------------------------------------------
    def set_tick_minutes(self, m: int):
        self.tick_minutes = max(1, int(m))

    def add_person(self, role: str = "child", home: Optional[str] = None,
                   temperament: str = "typical") -> str:
        """Author a fresh STUDY SUBJECT from a chosen temperament seed and place it in a
        home. This is disciplined authoring: only the temperament (inherited reactivity)
        is given -- the substrate is seeded fresh from that temperament's gains (deterministic,
        `seed_substrate`), NOT cloned from a grown resident. An authored person evolves live
        (never frozen). Returns the id."""
        homes = [p for p in self.space.cells if p.startswith("home")]
        if not homes:
            return ""
        home = home if home in homes else self.rng.choice(homes)
        cid = f"new_{len(self.info)}_{self.rng.randint(1000,9999)}"
        seed_fn = TEMPERAMENT_SEEDS.get(temperament, typical_child_seed)
        # the substrate is seeded deterministically from the temperament's gains in the agent's
        # __post_init__, so an authored person is reproducible from its seed alone.
        person = Person(agent_id=cid, name=cid, seed=seed_fn())
        self.pop.persons[cid] = person
        # role may be a fine role from the library (teenager/retired/...) or child/adult
        is_child = role_is_child(role) if role in ROLE_SCHEDULES else (role == "child")
        self.info[cid] = (is_child, home, None if is_child
                          else next((p for p in self.space.cells
                                     if p.startswith(("office", "shop", "pub"))), None))
        self.roles[cid] = role if role in ROLE_SCHEDULES else ("child" if is_child else "adult")
        self.gmats[cid] = GroupMatrix()
        self.tempers[cid] = temperament
        hc = self.space.place_cell(home) or self._a_park
        self.state[cid] = {"tile": hc, "path": [], "pi": 0, "target": home,
                           "jitter": self.rng.uniform(-0.5, 0.5)}
        # an authored person is a STUDY SUBJECT: it evolves live around any fixed background
        self.subjects.add(cid)
        self.frozen.discard(cid)
        return cid

    # -- save / load (a whole running world, evolved minds and all) ---------
    def _meta(self, name: str, slug: str) -> dict:
        return {
            "name": name or slug, "slug": slug,
            "clock": self.clock_label(), "minutes": self.minutes, "step": self.step_count,
            "residents": len(self.state), "population": self.population_n, "seed": self.seed,
            "saved_at": time.time(),
            "saved_label": time.strftime("%Y-%m-%d %H:%M", time.localtime()),
        }

    def save(self, name: str, directory: str = SAVE_DIR) -> dict:
        """Persist the ENTIRE running world -- town, every mind (its developed substrate,
        memories, group standing), positions and clock -- to disk, plus a small JSON sidecar
        of metadata for listing. Returns that metadata."""
        os.makedirs(directory, exist_ok=True)
        slug = _slug(name)
        with open(os.path.join(directory, slug + ".psychsim"), "wb") as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
        meta = self._meta(name, slug)
        with open(os.path.join(directory, slug + ".json"), "w") as f:
            json.dump(meta, f, indent=2)
        return meta

    @staticmethod
    def list_saves(directory: str = SAVE_DIR) -> List[dict]:
        """Metadata for every save on disk, newest first (from the JSON sidecars)."""
        out: List[dict] = []
        if not os.path.isdir(directory):
            return out
        for fn in os.listdir(directory):
            if not fn.endswith(".json"):
                continue
            try:
                with open(os.path.join(directory, fn)) as f:
                    meta = json.load(f)
                if os.path.isfile(os.path.join(directory, meta.get("slug", "") + ".psychsim")):
                    out.append(meta)
            except Exception:
                pass
        out.sort(key=lambda m: m.get("saved_at", 0), reverse=True)
        return out

    @staticmethod
    def load(name: str, directory: str = SAVE_DIR) -> "SimEngine":
        """Reload a saved world into a fresh, fully-runnable engine."""
        slug = _slug(name)
        with open(os.path.join(directory, slug + ".psychsim"), "rb") as f:
            obj = pickle.load(f)
        if not isinstance(obj, SimEngine):
            raise ValueError("file is not a PsychSim save")
        return obj

    @staticmethod
    def delete_save(name: str, directory: str = SAVE_DIR) -> bool:
        """Remove a save (both its blob and its sidecar). True if anything was removed."""
        slug = _slug(name)
        removed = False
        for ext in (".psychsim", ".json"):
            p = os.path.join(directory, slug + ext)
            if os.path.isfile(p):
                os.remove(p)
                removed = True
        return removed

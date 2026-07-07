"""
population.py -- fill a settlement with a society (the population generator).

A spawned town is a place; this makes it a society. Given a generated settlement
(its homes, school, offices and shops), this creates the people who live in it --
households in the homes (adults and children), pupils in the school, workers in
the workplaces -- and wires the standard relational ties among them (parent-child
within households, teacher-pupil at school, boss-employee and colleagues at work).
The result is a population whose lives can be run through the world.

The baseline is a balanced society working as it should: dispositions default to
ordinary, well-functioning ones. A study injects whatever it perturbs -- a
fearless child in a household, say -- by passing its own disposition source. This
is generic society-building; it belongs in the core.

Rough and revisable: household composition is a simple draw, not calibrated
demography (a demography profile supplies realistic ratios separately).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional
import random

from .person import Person
from .relations import (Society, PARENT_CHILD, TEACHER_PUPIL, BOSS_EMPLOYEE,
                        COLLEAGUES)
from affective_engine.core import sophropathic_seed, clamp


@dataclass
class Household:
    home: str
    adults: List[str] = field(default_factory=list)
    children: List[str] = field(default_factory=list)
    child_bedrooms: int = 0                 # bedrooms for the children (some may share)
    tenure: str = "owner"                   # owner / private_rent / social_rent (SES proxy)
    spare_rooms: int = 0                    # extra rooms (study/guest) -- comfort of wealthier homes
    comfort: float = 0.6                    # 0..1 ease-of-living (space per person, SES)
    garden: bool = True                     # a private garden (outdoor space)
    garden_size: float = 0.5                # 0..1 relative garden size
    warmth: float = 0.75                    # parenting climate: warmth of the home
    structure: float = 0.70                 # parenting climate: firmness/consistency

    def members(self) -> List[str]:
        return self.adults + self.children


@dataclass
class HouseholdProfile:
    """How households are composed, anchored to ONS 2021/2022 and the English
    Housing Survey (England). Family-size distribution (of families with
    dependent children): 1 child 44%, 2 children 41%, 3+ 15%; ~22% lone-parent;
    ~30% of homes have dependent children.

    Room-sharing is governed by SOCIO-ECONOMIC status, not family size alone:
    overall only ~3% of households are overcrowded, and most children have their
    own room -- but overcrowding is concentrated in social renting (~22% of
    social-rented households with children vs ~2-3% of owner-occupiers, EHS).
    Conversely 55% of owner-occupiers are UNDER-occupied (spare rooms). Tenure
    split in England: ~64% owner, ~19% private rent, ~16% social rent (EHS 2024).
    Comfort of living -- space per person -- is itself a developmental input."""
    child_household_frac: float = 0.30
    lone_parent_frac: float = 0.22
    one_person_frac: float = 0.42
    child_count_weights: Dict[int, float] = field(
        default_factory=lambda: {1: 0.44, 2: 0.41, 3: 0.11, 4: 0.04})
    tenure_weights: Dict[str, float] = field(
        default_factory=lambda: {"owner": 0.64, "private_rent": 0.19, "social_rent": 0.16})
    # probability a child household's siblings share a room, by tenure (EHS overcrowding)
    share_prob_by_tenure: Dict[str, float] = field(
        default_factory=lambda: {"owner": 0.10, "private_rent": 0.28, "social_rent": 0.55})
    # probability of a spare room (under-occupation / comfort), by tenure
    spare_prob_by_tenure: Dict[str, float] = field(
        default_factory=lambda: {"owner": 0.45, "private_rent": 0.18, "social_rent": 0.05})
    comfort_by_tenure: Dict[str, float] = field(
        default_factory=lambda: {"owner": 0.75, "private_rent": 0.55, "social_rent": 0.45})


def _draw_children(rng: random.Random, weights: Dict[int, float]) -> int:
    r, cum = rng.random(), 0.0
    for n, w in sorted(weights.items()):
        cum += w
        if r <= cum:
            return n
    return max(weights)


def _draw_tenure(rng: random.Random, weights: Dict[str, float]) -> str:
    r, cum = rng.random(), 0.0
    for t, w in weights.items():
        cum += w
        if r <= cum:
            return t
    return "owner"


@dataclass
class Population:
    persons: Dict[str, Person]
    households: List[Household]
    society: Society
    pupils: List[str]
    workplaces: Dict[str, List[str]]        # workplace place-name -> worker ids
    schools: Dict[str, List[str]]           # school place-name -> pupil ids
    teachers: Dict[str, str]                # school -> teacher id

    def size(self) -> int:
        return len(self.persons)

    def summary(self) -> Dict[str, object]:
        adults = sum(len(h.adults) for h in self.households)
        children = sum(len(h.children) for h in self.households)
        return {"people": self.size(), "households": len(self.households),
                "adults": adults, "children": children,
                "teachers": len(self.teachers), "pupils": len(self.pupils),
                "workers": sum(len(w) for w in self.workplaces.values()),
                "ties": len(self.society.ties)}


def _places(city, *prefixes) -> List[str]:
    out = []
    for p in city.objects:
        if p.place and p.place.startswith(prefixes):
            out.append(p.place)
    return out


def populate(city, seed: int = 0,
             adult_seed: Callable = sophropathic_seed,
             child_seed: Callable = sophropathic_seed,
             mean_household: float = 2.4, max_children: int = 4,
             household_profile: Optional[HouseholdProfile] = None) -> Population:
    """Populate a generated settlement. `adult_seed`/`child_seed` are disposition
    sources -- ordinary by default (a balanced society); a study overrides them.
    Household composition follows real ONS proportions (see HouseholdProfile), so
    there are childless homes, one- and two-child families, and some three- and
    four-child families, with bedroom-sharing rising in the larger ones."""
    rng = random.Random(seed)
    hp = household_profile or HouseholdProfile()
    homes = _places(city, "home", "apartment")
    offices = _places(city, "office")
    commercial = _places(city, "shop", "pub", "cafe")
    schools = _places(city, "school")
    workplaces = offices + commercial

    persons: Dict[str, Person] = {}
    households: List[Household] = []
    pupils: List[str] = []
    soc = Society()
    wp_workers: Dict[str, List[str]] = {w: [] for w in workplaces}
    pid = [0]

    def _new(seed_fn) -> str:
        i = f"p{pid[0]}"; pid[0] += 1
        persons[i] = Person(i, i, seed_fn())
        return i

    for home in homes:
        hh = Household(home)
        hh.tenure = _draw_tenure(rng, hp.tenure_weights)
        hh.comfort = hp.comfort_by_tenure.get(hh.tenure, 0.6)
        # parenting climate varies across the population: most homes warm and
        # firm, a minority harsher or less consistent -- the developmental signal
        hh.warmth = clamp(rng.gauss(0.72, 0.18))
        hh.structure = clamp(rng.gauss(0.68, 0.18))
        if rng.random() < hp.child_household_frac:
            n_children = _draw_children(rng, hp.child_count_weights)
            n_adults = 1 if rng.random() < hp.lone_parent_frac else 2
            # socio-economics governs sharing: most children have their own room,
            # sharing concentrated in lower-SES tenures; larger families a bit more
            share_p = hp.share_prob_by_tenure.get(hh.tenure, 0.3) * (1 + 0.25 * (n_children - 1))
            if n_children >= 2 and rng.random() < share_p:
                hh.child_bedrooms = -(-n_children // 2)          # siblings pair up
            else:
                hh.child_bedrooms = n_children                   # a room each
            # wealthier, uncrowded homes often have a spare room (comfort)
            if hh.child_bedrooms == n_children and rng.random() < hp.spare_prob_by_tenure.get(hh.tenure, 0.1):
                hh.spare_rooms = 1
            # comfort reflects space per person
            rooms = 1 + hh.child_bedrooms + hh.spare_rooms       # bedrooms
            hh.comfort = clamp(hh.comfort + 0.12 * (rooms - (n_adults + n_children) / 2) / 3)
        else:
            n_children = 0
            n_adults = 1 if rng.random() < hp.one_person_frac else 2
            if rng.random() < hp.spare_prob_by_tenure.get(hh.tenure, 0.1):
                hh.spare_rooms = 1
        for _ in range(n_adults):
            hh.adults.append(_new(adult_seed))
        for _ in range(min(n_children, max_children)):
            c = _new(child_seed)
            hh.children.append(c)
            pupils.append(c)
        households.append(hh)
        # parent-child ties (functioning by default)
        for a in hh.adults:
            for c in hh.children:
                soc.add(a, c, PARENT_CHILD, standing=0.7, strain=0.1)
        # assign each working adult a workplace
        for a in hh.adults:
            if workplaces:
                wp = rng.choice(workplaces)
                wp_workers[wp].append(a)

    # teachers: one per school, drawn as a working adult; pupils tie to the teacher
    teachers: Dict[str, str] = {}
    for sch in schools:
        t = _new(adult_seed)
        teachers[sch] = t
        for c in pupils:
            soc.add(t, c, TEACHER_PUPIL, standing=0.65, strain=0.1)

    school_pupils = {sch: list(pupils) for sch in schools}

    # workplaces: a boss over employees, and a few colleague ties among peers
    # (not all-pairs -- one does not hold a peer tie with every colleague)
    for wp, workers in wp_workers.items():
        if not workers:
            continue
        boss = workers[0]
        for e in workers[1:]:
            soc.add(boss, e, BOSS_EMPLOYEE, standing=0.6, strain=0.15)
        peers = workers[1:]
        for idx, a in enumerate(peers):
            for b in peers[idx + 1: idx + 4]:      # up to 3 nearby colleagues each
                soc.add(a, b, COLLEAGUES, standing=0.6, strain=0.1)

    return Population(persons, households, soc, pupils, wp_workers,
                      school_pupils, teachers)

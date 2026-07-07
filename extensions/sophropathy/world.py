"""
world.py -- the sophropathy study's world content (a research extension).

The core provides only neutral machinery: interiors, access, affordances, the
day loop, and a norm mechanism with no categories of its own. This module
supplies what THIS study needs, and does so openly -- another researcher would
replace it wholesale with their own.

The study is about the functioning, non-offending end of the spectrum, so its
world is about ordinary social conduct, not offences. Its behaviour categories
are a neutral, symmetric spectrum with the POSITIVE pole the sophropathy
construct centres on -- reciprocity, restraint, honouring the access one is
granted, respect for the rules of a place -- as first-class as the negative
pole. Nothing here concerns crime; there is no theft, no lock, no offence
vocabulary. A "disruptive" act is simply conduct a place does not accept, and a
"considerate" one is conduct that respects it.

Provided: the study's categories, the formative venues (home with a family
interior and an optional shared sibling bedroom, a school, an adult workplace, a
community setting) with their local norms, and matching daily routines.
"""

from __future__ import annotations
from typing import Dict, Tuple

from sim_world import (Affordance, AffordanceObject, Area, Door, Access, Venue,
                       Norm, Block, Routine)
from affective_engine.core import clamp

# ---------------------------------------------------------------------------
# The study's behaviour categories (a neutral, symmetric social spectrum)
# ---------------------------------------------------------------------------

WARM = "warm"                 # affiliative, caring conduct
COOPERATIVE = "cooperative"   # working with others, reciprocity
CONSIDERATE = "considerate"   # respecting the rules of a place; restraint; honouring access
SELF_DIRECTED = "self_directed"   # neutral, task- or self-focused conduct
BOISTEROUS = "boisterous"     # high-spirited, loud -- fine in some places, not others
DISRUPTIVE = "disruptive"     # acting against the social expectations of a place

CATEGORIES = (WARM, COOPERATIVE, CONSIDERATE, SELF_DIRECTED, BOISTEROUS, DISRUPTIVE)

# map the engine's EMERGENT ACTIONS (Panksepp behaviours) onto the study's norm-conduct
# categories. This is the STUDY's reading of what an act means socially (a study observer
# construct, App. E.5) -- keyed on the emergent behaviour, never on an outcome-category label,
# and distinct from the psychopathy outcome categories (which live only in observer.py).
BEHAVIOUR_CATEGORY = {
    "nurture": WARM,
    "court": WARM,
    "play": BOISTEROUS,
    "approach": SELF_DIRECTED,
    "avoid": SELF_DIRECTED,
    "seek_comfort": SELF_DIRECTED,
    "aggress": DISRUPTIVE,
}


def study_category(behaviour: str, affordance=None) -> str:
    """The study's norm-conduct category for an act: the affordance's own category if it
    declares one, else the study's reading of the emergent behaviour the agent took."""
    cat = getattr(affordance, "category", None)
    if cat:
        return cat
    return BEHAVIOUR_CATEGORY.get(behaviour, SELF_DIRECTED)


# ---------------------------------------------------------------------------
# Norm profiles -- what conduct each kind of place expects (study's values)
# ---------------------------------------------------------------------------

def _profile(overrides: Dict[str, Norm] = None) -> Dict[str, Norm]:
    base = {WARM: Norm.ENCOURAGED, COOPERATIVE: Norm.ENCOURAGED,
            CONSIDERATE: Norm.ENCOURAGED, SELF_DIRECTED: Norm.ACCEPTED,
            BOISTEROUS: Norm.TOLERATED, DISRUPTIVE: Norm.DISCOURAGED}
    if overrides:
        base.update(overrides)
    return base

NORMS = {
    "home_common": _profile({BOISTEROUS: Norm.ACCEPTED}),            # relaxed
    "home_private": _profile(),                                     # a bedroom
    "classroom": _profile({SELF_DIRECTED: Norm.ENCOURAGED,
                           BOISTEROUS: Norm.DISCOURAGED,
                           DISRUPTIVE: Norm.UNACCEPTABLE}),         # orderly
    "playground": _profile({BOISTEROUS: Norm.ENCOURAGED}),         # permissive
    "workplace": _profile({SELF_DIRECTED: Norm.ENCOURAGED,
                           BOISTEROUS: Norm.DISCOURAGED,
                           DISRUPTIVE: Norm.UNACCEPTABLE}),        # formal
    "community": _profile({BOISTEROUS: Norm.ACCEPTED}),            # a public street
}


# ---------------------------------------------------------------------------
# Formative venues
# ---------------------------------------------------------------------------

def build_home(name: str = "Home", warmth: float = 0.85, structure: float = 0.80,
               children: int = 1, shared_bedroom: bool = False,
               child_bedrooms: Optional[int] = None, spare_rooms: int = 0,
               garden: bool = False, garden_size: float = 0.5) -> Venue:
    """A home sized to its family AND its means, connected to the outside: a
    kitchen and lounge, a bathroom, a parents' bedroom, child bedrooms (siblings
    share in poorer homes), optional spare rooms (wealthier homes), and -- where
    the household has one -- a private GARDEN reached by a back door, with a front
    door onto the street. Outdoor space (safe play, greenery) and comfort are
    developmental inputs. Bedrooms are private; the garden is the household's."""
    val = clamp(2.0 * warmth - 1.0, -1.0, 1.0)
    care = {"social_valence": val, "controllability": 0.3 + 0.5 * structure}

    kitchen = Area("kitchen", [AffordanceObject("table", [
        Affordance("eat", "self_care", {**care, "reward": 0.3}, category=SELF_DIRECTED),
        Affordance("share_meal", "cooperation",
                   {"social_valence": val, "goal_relevance": 0.5, "reward": 0.3},
                   category=COOPERATIVE)])], norms=NORMS["home_common"])
    lounge = Area("lounge", [
        AffordanceObject("sofa", [
            Affordance("relax", "opportunity",
                       {"reward": 0.4, "social_valence": val, "novelty": 0.3,
                        "controllability": 0.6}, category=SELF_DIRECTED),
            Affordance("family_time", "cooperation",
                       {"social_valence": val, "goal_relevance": 0.4, "reward": 0.3},
                       category=WARM)]),
        AffordanceObject("floor", [
            Affordance("play_rough", "opportunity",
                       {"reward": 0.5, "novelty": 0.6, "social_valence": 0.3},
                       category=BOISTEROUS)])], norms=NORMS["home_common"])
    bathroom = Area("bathroom", [AffordanceObject("sink", [
        Affordance("wash", "self_care", {**care}, category=SELF_DIRECTED)])],
        norms=NORMS["home_common"])

    areas = {"kitchen": kitchen, "lounge": lounge, "bathroom": bathroom}
    areas["parents_bedroom"] = Area("parents_bedroom", [AffordanceObject("bed", [
        Affordance("sleep", "rest", {**care, "reward": 0.2}, category=SELF_DIRECTED),
        Affordance("consider_others", "opportunity",
                   {"social_valence": val, "controllability": 0.5},
                   category=CONSIDERATE)])], norms=NORMS["home_private"])

    def _child_room(label, shared):
        obj = "bunks" if shared else "bed"
        affs = [Affordance("sleep", "rest", {**care, "reward": 0.2}, category=SELF_DIRECTED)]
        if shared:
            affs.append(Affordance("share_space", "cooperation",
                                   {"social_valence": val, "goal_relevance": 0.4},
                                   category=CONSIDERATE))
        return Area(label, [AffordanceObject(obj, affs)], norms=NORMS["home_private"])

    n_children = max(children, child_bedrooms or 0)
    if child_bedrooms is None:
        if shared_bedroom:
            child_bedrooms = 1
            n_children = max(2, children)          # a shared room implies siblings
        else:
            child_bedrooms = max(1, children)
            n_children = children if children else child_bedrooms
    child_bedrooms = max(1, child_bedrooms)
    # if there are fewer bedrooms than children, the earlier rooms are shared
    shared_count = max(0, n_children - child_bedrooms)
    for i in range(child_bedrooms):
        shared = i < shared_count
        if shared and child_bedrooms == 1:
            label = "shared_bedroom"
        elif shared:
            label = f"shared_bedroom_{i+1}"
        else:
            label = f"child_bedroom_{i+1}"
        areas[label] = _child_room(label, shared)

    for i in range(max(0, spare_rooms)):
        label = "study" if i == 0 else f"spare_room_{i+1}"
        areas[label] = Area(label, [AffordanceObject("desk", [
            Affordance("quiet_time", "opportunity",
                       {"reward": 0.35, "controllability": 0.7, "social_valence": val},
                       category=SELF_DIRECTED)])], norms=NORMS["home_private"])

    names = list(areas)
    for n in names:
        for o in names:
            if o == n:
                continue
            if "bedroom" in o:
                role = "parent" if o == "parents_bedroom" else "child"
                areas[n].doors.append(Door(o, Access(roles={role})))
            else:
                areas[n].doors.append(Door(o))

    v = Venue(name, "home", areas, entry="kitchen",
              warmth=warmth, structure=structure, norms=NORMS["home_common"])
    if garden:
        # a private garden reached by a back door from the kitchen: outdoor play
        # and greenery, a developmental input scaled by the garden's size
        g = Area("garden", [AffordanceObject("lawn", [
            Affordance("play_outside", "opportunity",
                       {"reward": 0.5 + 0.3 * garden_size, "novelty": 0.6,
                        "social_valence": 0.3, "controllability": 0.6},
                       category=BOISTEROUS),
            Affordance("potter", "opportunity",
                       {"reward": 0.3, "controllability": 0.7, "social_valence": val},
                       category=SELF_DIRECTED)])], norms=NORMS["community"])
        v.areas["garden"] = g
        v.areas["kitchen"].doors.append(Door("garden"))        # back door
        g.doors.append(Door("kitchen"))
        g.garden_size = garden_size          # for the floor-plan renderer
    return v


def build_school(name: str = "School") -> Venue:
    """A school: an orderly classroom and a permissive playground. The SAME
    boisterous act is accepted in the yard and out of place in the class -- local
    social rules, not offences. A staff room is access-restricted to teachers,
    so entering it is a question of respecting a boundary."""
    classroom = Area("classroom", [AffordanceObject("desk", [
        Affordance("study", "opportunity",
                   {"goal_relevance": 0.6, "reward": 0.3, "controllability": 0.6},
                   category=SELF_DIRECTED),
        Affordance("work_together", "cooperation",
                   {"social_valence": 0.5, "goal_relevance": 0.6, "reward": 0.3},
                   category=COOPERATIVE),
        Affordance("be_boisterous", "opportunity",
                   {"reward": 0.5, "novelty": 0.6, "social_valence": 0.2},
                   category=BOISTEROUS)])], norms=NORMS["classroom"])
    playground = Area("playground", [AffordanceObject("play_area", [
        Affordance("play", "opportunity",
                   {"reward": 0.5, "social_valence": 0.4, "novelty": 0.4},
                   category=BOISTEROUS),
        Affordance("include_others", "cooperation",
                   {"social_valence": 0.5, "goal_relevance": 0.4},
                   category=CONSIDERATE),
        Affordance("provoked", "provocation",
                   {"provocation": 0.7, "threat": 0.4, "social_valence": -0.5})])],
        norms=NORMS["playground"])
    staff_room = Area("staff_room", [AffordanceObject("kettle", [
        Affordance("rest", "rest", {"reward": 0.2}, category=SELF_DIRECTED)])],
        norms=NORMS["classroom"])
    classroom.doors.append(Door("playground"))
    playground.doors.append(Door("classroom"))
    classroom.doors.append(Door("staff_room", Access(roles={"teacher"})))  # respect the boundary
    staff_room.doors.append(Door("classroom"))
    return Venue(name, "school",
                 {"classroom": classroom, "playground": playground,
                  "staff_room": staff_room}, entry="classroom",
                 norms=NORMS["classroom"])


def build_workplace(name: str = "Workplace") -> Venue:
    """An adult workplace: focused work and collegial cooperation are the norm;
    a considerate colleague respects its rules. A restricted back office models a
    granted-access boundary."""
    floor = Area("work_floor", [AffordanceObject("workstation", [
        Affordance("work", "opportunity",
                   {"goal_relevance": 0.7, "controllability": 0.6, "reward": 0.3},
                   category=SELF_DIRECTED),
        Affordance("collaborate", "cooperation",
                   {"social_valence": 0.4, "goal_relevance": 0.6},
                   category=COOPERATIVE)])], norms=NORMS["workplace"])
    back_office = Area("back_office", [AffordanceObject("records", [
        Affordance("work", "opportunity", {"goal_relevance": 0.6},
                   category=SELF_DIRECTED)])], norms=NORMS["workplace"])
    floor.doors.append(Door("back_office", Access(roles={"manager"})))
    back_office.doors.append(Door("work_floor"))
    return Venue(name, "workplace", {"work_floor": floor, "back_office": back_office},
                 entry="work_floor", norms=NORMS["workplace"])


def build_community(name: str = "High Street") -> Venue:
    """A public communal setting: a relaxed norm, where reciprocity and restraint
    still register but high spirits are fine."""
    street = Area("street", [AffordanceObject("bench", [
        Affordance("pass_time", "opportunity", {"reward": 0.3, "novelty": 0.3},
                   category=SELF_DIRECTED),
        Affordance("greet_others", "cooperation",
                   {"social_valence": 0.5}, category=WARM),
        Affordance("be_boisterous", "opportunity",
                   {"reward": 0.4, "novelty": 0.5}, category=BOISTEROUS)])],
        norms=NORMS["community"])
    return Venue(name, "community", {"street": street}, entry="street",
                 norms=NORMS["community"])


# ---------------------------------------------------------------------------
# Routines for the study's life stages
# ---------------------------------------------------------------------------

def child_routine(home: str, school: str, bedroom: str = "child_bedroom_1") -> Routine:
    d = {6: Block("wash", home, "bathroom"), 7: Block("share_meal", home, "kitchen"),
         8: Block("study", school, "classroom"), 9: Block("study", school, "classroom"),
         10: Block("play", school, "playground"), 11: Block("study", school, "classroom"),
         12: Block("play", school, "playground"), 13: Block("work_together", school, "classroom"),
         14: Block("relax", home, "lounge"), 15: Block("play", school, "playground"),
         16: Block("family_time", home, "lounge"), 18: Block("share_meal", home, "kitchen"),
         20: Block("family_time", home, "lounge"), 21: Block("sleep", home, bedroom)}
    return Routine("child", d, home, "kitchen")


def worker_routine(home: str, work: str) -> Routine:
    d = {6: Block("wash", home, "bathroom"), 7: Block("share_meal", home, "kitchen")}
    for h in range(9, 17):
        d[h] = Block("work", work, "work_floor")
    d.update({18: Block("share_meal", home, "kitchen"),
              20: Block("family_time", home, "lounge"),
              21: Block("sleep", home, "parents_bedroom")})
    return Routine("worker", d, home, "kitchen")


# ---------------------------------------------------------------------------
# Running a study day (threads the study's category reading into the core loop)
# ---------------------------------------------------------------------------

def run_study_day(venues, inhabitants, **kw):
    """run_day with the study's network->category reading supplied."""
    from sim_world import run_day
    return run_day(venues, inhabitants, categorise=study_category, **kw)


def demo() -> str:
    """A day in the study's world, and how the same conduct is read by place --
    no offences, no locks: ordinary social conduct, respect for boundaries, and
    local social rules."""
    from sim_world import Person, Inhabitant, assess
    from affective_engine.core import sophropathic_seed
    out = []

    home = build_home(warmth=0.9); school = build_school()
    venues = {"Home": home, "School": school}
    alex = Inhabitant(Person("alex", "Alex", sophropathic_seed()),
                      child_routine("Home", "School"))
    out.append("A CHILD'S DAY (ordinary social conduct):")
    out.append(run_study_day(venues, {"alex": alex}).transcript())

    out.append("\nLOCAL SOCIAL RULES (the same conduct, read by place):")
    for cat in (BOISTEROUS, DISRUPTIVE, CONSIDERATE):
        cells = []
        for area in ("classroom", "playground", "workplace", "community"):
            lvl, dep = assess(cat, NORMS[area])
            cells.append(f"{area}={lvl.name.lower()}" + ("*" if dep else ""))
        out.append(f"  {cat:12}: " + "   ".join(cells))
    out.append("  (* = a departure from what the place expects; no offence is implied)")

    out.append("\nACCESS AS RESPECT FOR A BOUNDARY (not a lock):")
    sd = school.area("classroom").door_to("staff_room")
    bd = home.area("kitchen").door_to("parents_bedroom")
    out.append(f"  staff room: teacher may enter={sd.permits('teacher')}, "
               f"pupil may enter={sd.permits('child')}")
    out.append(f"  parents' room: parent may enter={bd.permits('parent')}, "
               f"child may enter={bd.permits('child')}")
    out.append("\nThe core is neutral machinery; this study supplies its own venues, "
               "its symmetric social categories (a positive pole -- warmth, cooperation, "
               "restraint -- as first-class as any departure), and its local norms. "
               "Another study would replace this module entirely.")
    return "\n".join(out)


def venues_for(city, population=None, shared_bedroom: bool = False) -> Dict[str, object]:
    """Map each building in a spawned settlement to a Venue, so the top-down
    floor-plan renderer can draw its rooms. If `population` is given, each home is
    built to its assigned household -- the number of child bedrooms matching that
    family (with siblings sharing where the family is larger or poorer). Homes ->
    a family home, schools -> a school, offices/shops/pubs -> a workplace floor."""
    home_beds: Dict[str, int] = {}
    home_spare: Dict[str, int] = {}
    home_kids: Dict[str, int] = {}
    home_garden: Dict[str, tuple] = {}
    home_climate: Dict[str, tuple] = {}
    if population is not None:
        for hh in population.households:
            home_spare[hh.home] = hh.spare_rooms
            home_garden[hh.home] = (hh.garden, hh.garden_size)
            home_climate[hh.home] = (hh.warmth, hh.structure)
            if hh.children:
                home_beds[hh.home] = max(1, hh.child_bedrooms or len(hh.children))
                home_kids[hh.home] = len(hh.children)
    out = {}
    for p in city.objects:
        if not p.place:
            continue
        pref = p.place.rsplit("_", 1)[0]
        if pref in ("home", "apartment"):
            beds = home_beds.get(p.place)
            spare = home_spare.get(p.place, 0)
            grd, gsize = home_garden.get(p.place, (True, 0.5))
            wm, st = home_climate.get(p.place, (0.85, 0.80))
            if beds is not None:
                out[p.place] = build_home(p.place, warmth=wm, structure=st,
                                          children=home_kids[p.place],
                                          child_bedrooms=beds, spare_rooms=spare,
                                          garden=grd, garden_size=gsize)
            else:
                out[p.place] = build_home(p.place, warmth=wm, structure=st,
                                          child_bedrooms=1, spare_rooms=spare,
                                          garden=grd, garden_size=gsize)
        elif pref == "school":
            out[p.place] = build_school(p.place)
        elif pref in ("office", "shop", "pub", "cafe", "civic", "sports",
                      "hospital", "clinic", "worship", "market"):
            # non-home institutions: a workplace floor is a reasonable placeholder
            # interior for now (a hospital/place-of-worship interior is future work)
            out[p.place] = build_workplace(p.place)
    return out

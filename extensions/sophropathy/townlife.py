"""
townlife.py -- the day-to-day life layer for PsychSim, modelled on the Park sim.

This is the spatial half: it gives the spawned CityMap a light address layer
(world -> place -> room), an entrance tile for every building, a walkable surface, and
A* pathfinding, so people can have an (x, y) position and WALK between places. The
daily schedule, the day-cycle stepper, and the animated player build on this.

The mind stays on the substrate: this layer only decides where people are and how they
get there; what they feel and do when they arrive still emerges (Park's LLM cognition
is replaced by our substrate throughout).
"""

from __future__ import annotations
import heapq
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

Cell = Tuple[int, int]
_WALK_SPEED = 3          # tiles a person advances along their path per tick


# ---------------------------------------------------------------------------
# The walkable surface + building entrances (the spatial address layer)
# ---------------------------------------------------------------------------

def walkable_cells(city) -> set:
    """The tiles a person may stand on / walk over: pavement (roads), park, and paths.
    Grass and building footprints are not walkable through."""
    walk = set()
    if city.terrain:
        for gy, row in enumerate(city.terrain):
            for gx, t in enumerate(row):
                if "pavement" in t or "park" in t or "path" in t:
                    walk.add((gx, gy))
    for p in city.roads:                      # roads are the through-routes
        walk.add((p.x, p.y))
    return walk


def building_cells(city) -> Dict[str, List[Cell]]:
    """Every place name -> the grid cells its footprint occupies."""
    out: Dict[str, List[Cell]] = {}
    for o in city.objects:
        if o.tile.startswith("building") and getattr(o, "place", None):
            fpw, fph = o.footprint
            out[o.place] = [(o.x + dx, o.y + dy)
                            for dx in range(fpw) for dy in range(fph)]
    return out


def _neighbours(c: Cell) -> List[Cell]:
    x, y = c
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def building_entrances(city, walk: Optional[set] = None) -> Dict[str, Cell]:
    """A walkable entrance tile for each building: a walkable cell adjacent to the
    building's footprint (its door onto the street). People path to the entrance, then
    step onto the building cell to 'enter'."""
    walk = walk if walk is not None else walkable_cells(city)
    ents: Dict[str, Cell] = {}
    for place, cells in building_cells(city).items():
        best = None
        for c in cells:
            for n in _neighbours(c):
                if n in walk:
                    best = n
                    break
            if best:
                break
        # fall back to any walkable cell near the footprint centre
        if best is None and cells:
            cx = sum(c[0] for c in cells) // len(cells)
            cy = sum(c[1] for c in cells) // len(cells)
            best = min(walk, key=lambda w: abs(w[0] - cx) + abs(w[1] - cy)) if walk else cells[0]
        ents[place] = best
    return ents


# ---------------------------------------------------------------------------
# A* over the walkable grid
# ---------------------------------------------------------------------------

def astar(start: Cell, goal: Cell, walk: set,
          extra_ok: Optional[set] = None) -> List[Cell]:
    """Shortest path of cells from start to goal over the walkable set. `extra_ok`
    tiles (e.g. the goal building's own cell) are traversable too, so a person can step
    off the pavement into the place they are entering. Returns [] if unreachable."""
    ok = set(walk)
    if extra_ok:
        ok |= extra_ok
    ok.add(start); ok.add(goal)

    def h(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    openq = [(h(start, goal), 0, start)]
    came: Dict[Cell, Cell] = {}
    g = {start: 0}
    seen = set()
    while openq:
        _, gc, cur = heapq.heappop(openq)
        if cur == goal:
            path = [cur]
            while cur in came:
                cur = came[cur]; path.append(cur)
            return path[::-1]
        if cur in seen:
            continue
        seen.add(cur)
        for n in _neighbours(cur):
            if n not in ok:
                continue
            ng = gc + 1
            if ng < g.get(n, 1 << 30):
                g[n] = ng
                came[n] = cur
                heapq.heappush(openq, (ng + h(n, goal), ng, n))
    return []


# ---------------------------------------------------------------------------
# The town's spatial index (built once from a spawned CityMap)
# ---------------------------------------------------------------------------

@dataclass
class TownSpace:
    """The spatial address layer over a spawned town: walkable tiles, building
    entrances, and the rooms each place contains (from its venue)."""
    walk: set
    cells: Dict[str, List[Cell]]        # place -> footprint cells
    entrances: Dict[str, Cell]          # place -> entrance tile
    rooms: Dict[str, List[str]] = field(default_factory=dict)  # place -> room names

    def place_cell(self, place: str) -> Optional[Cell]:
        cs = self.cells.get(place)
        return cs[0] if cs else None

    def route(self, start: Cell, place: str) -> List[Cell]:
        """A path from `start` to the given building (ending on its entrance/cell)."""
        ent = self.entrances.get(place)
        if ent is None:
            return []
        extra = set(self.cells.get(place, []))
        path = astar(start, ent, self.walk, extra_ok=extra)
        # then a final step onto the building itself, if adjacent
        pc = self.place_cell(place)
        if path and pc and pc != path[-1] and abs(pc[0] - path[-1][0]) + abs(pc[1] - path[-1][1]) == 1:
            path.append(pc)
        return path


def build_town_space(city, venues: Dict[str, object]) -> TownSpace:
    walk = walkable_cells(city)
    cells = building_cells(city)
    ents = building_entrances(city, walk)
    rooms: Dict[str, List[str]] = {}
    for place in cells:
        v = venues.get(place)
        if v is not None and hasattr(v, "areas"):
            rooms[place] = [n for n in v.areas.keys() if n != "garden"]
    return TownSpace(walk=walk, cells=cells, entrances=ents, rooms=rooms)


# ---------------------------------------------------------------------------
# Daily schedules by role -- a grounded table of role-typical days (no LLM)
# ---------------------------------------------------------------------------
# Each block is (start_hour, place_key, room). place_key resolves per person to a real
# place: "home" -> their home, "school" -> the school, "work" -> their workplace,
# "leisure" -> a shared place (park / shop / pub). Rooms that a place lacks fall back
# to just being at the building.

WEEKDAY_CHILD = [(0, "home", "shared_bedroom"), (7, "home", "kitchen"),
                 (9, "school", "classroom"), (12, "school", "playground"),
                 (13, "school", "classroom"), (15, "home", "lounge"),
                 (17, "leisure", "park"), (18, "home", "kitchen"),
                 (20, "home", "shared_bedroom")]

WEEKDAY_ADULT = [(0, "home", "parents_bedroom"), (7, "home", "kitchen"),
                 (9, "work", None), (17, "home", "lounge"),
                 (19, "home", "kitchen"), (21, "home", "parents_bedroom")]

WEEKEND_CHILD = [(0, "home", "shared_bedroom"), (9, "home", "kitchen"),
                 (10, "leisure", "park"), (13, "home", "lounge"),
                 (15, "leisure", "park"), (18, "home", "kitchen"),
                 (21, "home", "shared_bedroom")]

WEEKEND_ADULT = [(0, "home", "parents_bedroom"), (9, "home", "kitchen"),
                 (11, "leisure", "shop"), (14, "home", "lounge"),
                 (17, "leisure", "pub"), (19, "home", "kitchen"),
                 (22, "home", "parents_bedroom")]


# The role LIBRARY: built-in child/adult (the tables above, unchanged) plus any roles
# defined as data under data/roles/*.json (preschooler, teenager, retired, teacher, ...).
# A role is data: {child: bool, weekday: [(hour, place_key, room)], weekend: [...]}.
_BUILTIN_ROLES = {
    "child": {"child": True, "weekday": WEEKDAY_CHILD, "weekend": WEEKEND_CHILD},
    "adult": {"child": False, "weekday": WEEKDAY_ADULT, "weekend": WEEKEND_ADULT},
}


def _load_role_schedules():
    roles = {k: dict(v) for k, v in _BUILTIN_ROLES.items()}
    try:
        from config.loader import load_roles
        for name, d in load_roles().items():
            if name in ("child", "adult"):
                continue                        # built-ins stay authoritative (byte-identical)
            roles[name] = {"child": bool(d.get("child", False)),
                           "weekday": [tuple(r) for r in d.get("weekday", [])],
                           "weekend": [tuple(r) for r in d.get("weekend", [])]}
    except Exception:
        pass
    return roles


ROLE_SCHEDULES = _load_role_schedules()


def available_roles():
    """The role names in the library (built-in + data/roles/)."""
    return sorted(ROLE_SCHEDULES)


def role_is_child(role: str) -> bool:
    return bool(ROLE_SCHEDULES.get(role, _BUILTIN_ROLES["adult"]).get("child", False))


def role_block(role: str, hour: float, is_weekend: bool):
    """The (place_key, room) a person of `role` should be at, at this hour."""
    spec = ROLE_SCHEDULES.get(role) or _BUILTIN_ROLES["adult"]
    table = spec["weekend"] if is_weekend else spec["weekday"]
    if not table:
        table = _BUILTIN_ROLES["adult"]["weekend" if is_weekend else "weekday"]
    cur = table[0]
    for blk in table:
        if blk[0] <= hour:
            cur = blk
        else:
            break
    return cur[1], cur[2]


def scheduled_block(hour: float, is_weekend: bool, is_child: bool):
    """Back-compat: the (place_key, room) for the coarse child/adult role."""
    return role_block("child" if is_child else "adult", hour, is_weekend)


# ---------------------------------------------------------------------------
# The day-cycle stepper: advance people along their schedules, capture a trajectory
# ---------------------------------------------------------------------------

def _people_roles_homes(universe):
    """Map each person -> (is_child, home_place, work_place)."""
    pop = universe.population
    pupils = set(getattr(pop, "pupils", []))
    info = {}
    # workplaces to hand out to working adults
    works = [o.place for o in universe.city.objects
             if o.tile in ("building_workplace", "building_shop", "building_pub")
             and getattr(o, "place", None)]
    wi = 0
    for hh in pop.households:
        for cid in getattr(hh, "children", []):
            info[cid] = (True, hh.home, None)
        for cid in getattr(hh, "adults", []):
            work = works[wi % len(works)] if works else None
            wi += 1
            info[cid] = (False, hh.home, work)
    return info


def simulate_townlife(universe, days: int = 1, tick_minutes: int = 30, seed: int = 0):
    """Step the town through `days` of day-to-day life and return an animation
    trajectory. Each person follows their role's daily schedule, walking between
    places along A* paths; when co-located at a place, their encounter runs through the
    substrate (emergent). Returns (town_space, frames), where each frame is
    {"t": minutes, "label": "Mon 08:30", "pos": {cid:(x,y)}, "drive": {cid: SYSTEM}}.
    """
    import random
    from .world import venues_for
    from substrate.readout import read_mind
    from affective_engine.core import Appraisal
    from sim_world.group_matrix import (GroupMatrix, default_groups,
                                        group_encounter, sample_encounter_type)

    pop = universe.population
    venues = venues_for(universe.city, pop)
    space = build_town_space(universe.city, venues)
    info = _people_roles_homes(universe)

    parks = [c for c in space.walk]                        # park/pavement leisure fallback
    leisure_places = {"park": None,                        # None -> a park tile
                      "shop": next((p for p in space.cells if p.startswith("shop")), None),
                      "pub": next((p for p in space.cells if p.startswith("pub")), None)}
    a_park_tile = next((c for c in space.walk), (0, 0))

    def resolve(cid, place_key, room):
        is_child, home, work = info[cid]
        if place_key == "home":
            return home, room
        if place_key == "school":
            return next((p for p in space.cells if p.startswith("school")), home), room
        if place_key == "work":
            return work or home, room
        if place_key == "leisure":
            lp = leisure_places.get(room)
            return (lp, None) if lp else ("__park__", None)
        return home, room

    rng = random.Random(seed)
    # per-person live state: current tile, current path, target place
    state = {}
    for cid in info:
        is_child, home, work = info[cid]
        hc = space.place_cell(home) or a_park_tile
        state[cid] = {"tile": hc, "path": [], "pi": 0, "target": home,
                      "jitter": rng.uniform(-0.5, 0.5)}

    groups = default_groups()
    gmats = {cid: GroupMatrix() for cid in info}

    frames = []
    ticks_per_day = int(24 * 60 / tick_minutes)
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for day in range(days):
        is_weekend = (day % 7) >= 5
        for tk in range(ticks_per_day):
            minutes = (day * 24 * 60) + tk * tick_minutes
            hour = (tk * tick_minutes) / 60.0
            # advance each person
            for cid, st in state.items():
                is_child, home, work = info[cid]
                pk, room = scheduled_block(hour + st["jitter"], is_weekend, is_child)
                place, _room = resolve(cid, pk, room)
                if place == "__park__":
                    goal_cell = a_park_tile
                    target_place = None
                else:
                    goal_cell = space.place_cell(place)
                    target_place = place
                # (re)plan if the goal changed
                if st["target"] != target_place:
                    st["target"] = target_place
                    if target_place is not None:
                        st["path"] = space.route(st["tile"], target_place)
                    else:
                        st["path"] = astar(st["tile"], goal_cell, space.walk) if goal_cell else []
                    st["pi"] = 0
                # walk several tiles along the path per tick, so a cross-town
                # journey takes about an hour rather than the whole day
                if st["path"] and st["pi"] < len(st["path"]) - 1:
                    st["pi"] = min(st["pi"] + _WALK_SPEED, len(st["path"]) - 1)
                    st["tile"] = st["path"][st["pi"]]
                elif goal_cell:
                    st["tile"] = goal_cell            # arrived / stay put
            # when several people share a place, let a couple interact via the substrate
            byplace = {}
            for cid, st in state.items():
                byplace.setdefault(st["tile"], []).append(cid)
            for cell, here in byplace.items():
                if len(here) >= 2:
                    for cid in here[:4]:
                        person = pop.persons.get(cid)
                        if person is None:
                            continue
                        grp = groups[hash(cell) % len(groups)]
                        mem = gmats[cid].membership(grp.id, grp.kind)
                        before = mem.standing + mem.belonging
                        r = group_encounter(person.mind.brain, grp, mem,
                                            sample_encounter_type(rng), age_years=20)
                        after = mem.standing + mem.belonging
                        # remember the encounter: who they were with, where, and how
                        # it went (emergent valence) -- so the inspector can show it
                        person.mind.memory.add(
                            label=f"with {len(here)-1} others at {grp.name}",
                            appraisal=Appraisal(label=grp.name),
                            dominant=r.dominant.value,
                            valence=max(-1.0, min(1.0, after - before)),
                            importance=0.4)
            # snapshot this tick
            pos = {cid: st["tile"] for cid, st in state.items()}
            drive = {}
            for cid in info:
                person = pop.persons.get(cid)
                if person is not None:
                    dom = read_mind(person.mind).dominant
                    drive[cid] = dom.value if hasattr(dom, "value") else str(dom)
            label = f"{day_names[day % 7]} {int(hour):02d}:{int((hour%1)*60):02d}"
            frames.append({"t": minutes, "label": label, "pos": pos, "drive": drive})

    # per-person inspectable state (as of the end of the run): role, the strength +
    # reactivity of each neural system, recent memories, and group standing
    people_info = {}
    from substrate.readout import read_mind
    for cid, (is_child, home, work) in info.items():
        person = pop.persons.get(cid)
        if person is None:
            continue
        systems = {k: round(v, 2)
                   for k, v in read_mind(person.mind).profile.items()}
        mems = [{"label": m.label, "valence": round(m.valence, 2)}
                for m in person.mind.memory.events[-10:]]
        groups_state = [{"group": m.group_id, "standing": round(m.standing, 2),
                         "belonging": round(m.belonging, 2), "route": m.status_route()}
                        for m in gmats[cid].memberships.values()]
        people_info[cid] = {
            "name": getattr(person, "name", cid),
            "role": "child" if is_child else "adult",
            "home": home, "work": work,
            "systems": systems, "memories": mems, "groups": groups_state,
        }
    return space, frames, people_info


# ---------------------------------------------------------------------------
# The animated player: watch people move through their day in the town
# ---------------------------------------------------------------------------

def render_townlife_html(universe, days: int = 1, tick_minutes: int = 15,
                         seed: int = 1, path: str = "town_life.html",
                         cell: int = 72, pad: int = 20):
    """Simulate day-to-day life and write a self-contained HTML page that plays it:
    the plan-view town with people walking between home, school, work and leisure,
    each coloured by their emergent drive. Controls: Start/Pause, faster/slower, a
    timeline slider, pan/zoom. Click a person to inspect their role, neural-network
    strengths, recent memories and group standing. Returns the path."""
    import json
    from .world import venues_for
    from sim_viz.floorplan import render_settlement_plan
    from sim_viz.compositor import NETWORK_COLOUR

    space, frames, people_info = simulate_townlife(
        universe, days=days, tick_minutes=tick_minutes, seed=seed)
    venues = venues_for(universe.city, universe.population)
    backdrop = render_settlement_plan(universe.city, venues, occupants=None,
                                      cell=cell, pad=pad)

    def px(gx): return pad + gx * cell + cell * 0.5
    ids = list(frames[0]["pos"].keys())
    packed = []
    for fr in frames:
        ppl = {}
        for cid in ids:
            t = fr["pos"].get(cid)
            if t is None:
                continue
            ppl[cid] = [round(px(t[0]), 1), round(px(t[1]), 1), fr["drive"].get(cid, "")]
        packed.append({"label": fr["label"], "ppl": ppl})

    people_groups = "".join(
        f'<g id="p_{cid}" class="person" data-cid="{cid}" transform="translate('
        f'{px(frames[0]["pos"][cid][0])},{px(frames[0]["pos"][cid][1])})">'
        f'<circle r="5" fill="#8a8a8a" stroke="#333" stroke-width="0.7"/></g>'
        for cid in ids)
    svg = backdrop.replace("</svg>", f'<g id="people">{people_groups}</g></svg>')

    colours = {k: v for k, v in NETWORK_COLOUR.items()
               if k in ("SEEKING", "CARE", "PLAY", "LUST", "FEAR", "RAGE", "PANIC")}
    tween = int(tick_minutes * 1000 / 15 * 0.6)

    html = (_TOWNLIFE_HTML
            .replace("__TITLE__", getattr(universe, "name", "town"))
            .replace("__SVG__", svg)
            .replace("__FRAMES__", json.dumps(packed))
            .replace("__INFO__", json.dumps(people_info))
            .replace("__COLOURS__", json.dumps(colours))
            .replace("__TWEEN__", str(tween))
            .replace("__NPEOPLE__", str(len(ids))))
    with open(path, "w") as f:
        f.write(html)
    return path


_TOWNLIFE_HTML = r"""<!doctype html><html><head><meta charset="utf-8"><title>__TITLE__ - a day</title>
<style>
html,body{margin:0;height:100%;background:#EAF0F2;overflow:hidden;font-family:Arial,sans-serif}
#stage{width:100vw;height:100vh;cursor:grab}#stage:active{cursor:grabbing}
#stage svg{transform-origin:0 0}
#people g{transition:transform __TWEEN__ms linear}
#people circle{transition:fill 400ms linear}
.person{cursor:pointer}
#bar{position:fixed;left:0;right:0;bottom:0;background:#fffe;border-top:1px solid #ccc;
padding:8px 12px;display:flex;gap:10px;align-items:center;font-size:13px;color:#333;z-index:5}
button.ctrl{cursor:pointer;border:1px solid #888;background:#fff;border-radius:5px;padding:4px 12px}
#slider{flex:1}#clock{min-width:110px;font-weight:bold;font-variant-numeric:tabular-nums}
#spd{min-width:70px;text-align:center;color:#555}
#legend{position:fixed;top:8px;left:8px;background:#fff9;padding:8px 10px;border-radius:6px;
font-size:12px;color:#444;line-height:1.5}#legend b{display:block;margin-bottom:3px}
.sw{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:5px;vertical-align:-1px}
#hint{position:fixed;top:8px;right:8px;background:#fff9;padding:6px 10px;border-radius:6px;font-size:12px;color:#666}
#panel{position:fixed;top:0;right:-360px;width:330px;height:100%;background:#fffef8;
border-left:1px solid #ccc;box-shadow:-2px 0 8px #0002;padding:14px 16px;overflow-y:auto;
font-size:13px;color:#333;transition:right .25s;z-index:10;box-sizing:border-box}
#panel.open{right:0}
#panel h2{margin:0 0 2px;font-size:16px}#panel .role{color:#666;margin-bottom:10px}
#panel h3{font-size:13px;margin:14px 0 6px;color:#333;border-bottom:1px solid #eee;padding-bottom:3px}
.netrow{display:flex;align-items:center;gap:6px;margin:3px 0;font-size:12px}
.netname{width:64px}.netbar{flex:1;height:9px;background:#eee;border-radius:4px;overflow:hidden;position:relative}
.netfill{height:100%}.netval{width:64px;text-align:right;color:#888;font-size:11px}
.mem{font-size:12px;padding:3px 0;border-bottom:1px dotted #eee}
.mem .v{float:right;font-variant-numeric:tabular-nums}
.grp{font-size:12px;padding:2px 0}
#close{position:absolute;top:10px;right:12px;cursor:pointer;color:#999;font-size:18px;border:none;background:none}
</style></head><body>
<div id="hint">scroll = zoom &middot; drag = pan &middot; click a person &middot; __NPEOPLE__ residents</div>
<div id="legend"></div>
<div id="stage">__SVG__</div>
<div id="panel"><button id="close">&times;</button><div id="pcontent"></div></div>
<div id="bar">
<button id="play" class="ctrl">&#9654; Start</button>
<button id="slower" class="ctrl">&#171; slower</button>
<span id="spd">1&times;</span>
<button id="faster" class="ctrl">faster &#187;</button>
<span id="clock"></span>
<input id="slider" type="range" min="0" max="0" value="0"/>
</div>
<script>
const FRAMES=__FRAMES__, INFO=__INFO__, COLOURS=__COLOURS__;
const stage=document.getElementById('stage'), svg=stage.querySelector('svg');
const play=document.getElementById('play'), slider=document.getElementById('slider');
const clock=document.getElementById('clock'), spd=document.getElementById('spd');
slider.max=FRAMES.length-1;
const leg=document.getElementById('legend');
leg.innerHTML='<b>emergent drive</b>'+Object.keys(COLOURS).map(k=>
 `<div><span class="sw" style="background:${COLOURS[k]}"></span>${k}</div>`).join('');
// pan + zoom
let scale=1,tx=0,ty=0,drag=false,lx=0,ly=0,moved=0;
function apply(){svg.style.transform=`translate(${tx}px,${ty}px) scale(${scale})`;}
stage.addEventListener('wheel',e=>{e.preventDefault();const f=e.deltaY<0?1.1:0.9;
 const r=stage.getBoundingClientRect();const mx=e.clientX-r.left,my=e.clientY-r.top;
 tx=mx-(mx-tx)*f;ty=my-(my-ty)*f;scale*=f;apply();},{passive:false});
stage.addEventListener('mousedown',e=>{drag=true;lx=e.clientX;ly=e.clientY;moved=0;});
window.addEventListener('mousemove',e=>{if(!drag)return;tx+=e.clientX-lx;ty+=e.clientY-ly;
 moved+=Math.abs(e.clientX-lx)+Math.abs(e.clientY-ly);lx=e.clientX;ly=e.clientY;apply();});
window.addEventListener('mouseup',()=>drag=false);
// playback with variable speed
const BASE=280; let mult=1,i=0,playing=false,timer=null;
const MULTS=[0.25,0.5,1,2,4,8];
function delay(){return BASE/mult;}
function draw(k){const fr=FRAMES[k];clock.textContent=fr.label;slider.value=k;
 for(const cid in fr.ppl){const el=document.getElementById('p_'+cid);if(!el)continue;
  const d=fr.ppl[cid];el.setAttribute('transform',`translate(${d[0]},${d[1]})`);
  const c=el.querySelector('circle');if(c)c.setAttribute('fill',COLOURS[d[2]]||'#8a8a8a');}
 if(selected)renderPanel(selected,fr);}
function tick(){draw(i);i=(i+1)%FRAMES.length;timer=setTimeout(tick,delay());}
function start(){playing=true;play.innerHTML='&#10073;&#10073; Pause';clearTimeout(timer);tick();}
function stop(){playing=false;play.innerHTML='&#9654; Start';clearTimeout(timer);}
play.onclick=()=>playing?stop():start();
document.getElementById('faster').onclick=()=>{let x=MULTS.indexOf(mult);
 if(x<MULTS.length-1)mult=MULTS[x+1];spd.textContent=mult+'\u00d7';};
document.getElementById('slower').onclick=()=>{let x=MULTS.indexOf(mult);
 if(x>0)mult=MULTS[x-1];spd.textContent=mult+'\u00d7';};
slider.oninput=()=>{stop();i=parseInt(slider.value);draw(i);};
// click-to-inspect
let selected=null;
function renderPanel(cid,fr){const info=INFO[cid];if(!info)return;
 const nowDrive=(fr&&fr.ppl[cid])?fr.ppl[cid][2]:'';
 let h=`<h2>${info.name}</h2><div class="role">${info.role} &middot; home: ${info.home||'-'}`+
  (info.work?` &middot; works: ${info.work}`:'')+`</div>`;
 h+=`<div>current drive: <b style="color:${COLOURS[nowDrive]||'#555'}">${nowDrive||'-'}</b></div>`;
 h+='<h3>neural networks (strength / reactivity)</h3>';
 for(const s in info.systems){const st=info.systems[s][0],re=info.systems[s][1];
  h+=`<div class="netrow"><span class="netname">${s}</span>`+
     `<span class="netbar"><span class="netfill" style="width:${Math.min(100,st*100)}%;`+
     `background:${COLOURS[s]||'#888'}"></span></span>`+
     `<span class="netval">${st.toFixed(2)} / ${re.toFixed(2)}</span></div>`;}
 h+='<h3>groups &amp; standing</h3>';
 if(info.groups.length)for(const g of info.groups){
  h+=`<div class="grp">${g.group}: standing ${g.standing}, belonging ${g.belonging} `+
     `<i style="color:#888">(${g.route})</i></div>`;}
 else h+='<div class="grp" style="color:#aaa">none yet</div>';
 h+=`<h3>recent memories (${info.memories.length})</h3>`;
 if(info.memories.length)for(const m of info.memories.slice().reverse()){
  const col=m.valence>0?'#2e8b3f':(m.valence<0?'#b23b3b':'#888');
  h+=`<div class="mem">${m.label}<span class="v" style="color:${col}">${m.valence>0?'+':''}${m.valence}</span></div>`;}
 else h+='<div class="mem" style="color:#aaa">no memories yet</div>';
 document.getElementById('pcontent').innerHTML=h;}
function select(cid){selected=cid;renderPanel(cid,FRAMES[i]);
 document.getElementById('panel').classList.add('open');
 document.querySelectorAll('.person circle').forEach(c=>c.setAttribute('stroke','#333'));
 const el=document.getElementById('p_'+cid);if(el)el.querySelector('circle').setAttribute('stroke','#111');}
document.getElementById('people').addEventListener('click',e=>{
 if(moved>4)return; const g=e.target.closest('.person');if(g)select(g.dataset.cid);});
document.getElementById('close').onclick=()=>{selected=null;
 document.getElementById('panel').classList.remove('open');};
draw(0);
</script></body></html>"""

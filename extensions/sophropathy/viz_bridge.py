"""
viz_bridge.py -- wire the time-clock's aged world to the PLAN-VIEW visualiser.

The world is laid out by the town spawn generator (generate_settlement) and lives on
`universe.city`; the time-clock ages a population on it (make_life_stepper). This
module renders that settlement in the top-down "glass roof" plan view
(render_settlement_plan): every house drawn as its floor plan -- rooms off a corridor,
doorways, furniture, a garden behind -- with each aged child placed in a room of their
real home and coloured by their EMERGENT dominant drive.

It does not invent a layout or a view: the settlement is the generator's output, the
plan view is the designed one, and a child's colour is their emergent readout.
"""

from __future__ import annotations
from typing import Dict

from sim_viz.floorplan import render_settlement_plan
from sim_viz.compositor import NETWORK_COLOUR

# where in the home to show the children, in order of preference
_PREFERRED_ROOMS = ("lounge", "living", "shared_bedroom", "kitchen")


def _pick_room(venue) -> str:
    areas = getattr(venue, "areas", {})
    names = list(areas.keys()) if isinstance(areas, dict) else [
        getattr(a, "name", a) for a in areas]
    for r in _PREFERRED_ROOMS:
        if r in names:
            return r
    for n in names:                       # any room that isn't the garden
        if n != "garden":
            return n
    return names[0] if names else "lounge"


def render_aged_town(universe, step, path: str = "aged_town.svg", cell: int = 72):
    """Render the spawned town in plan view, each aged child in a room of their real
    home coloured by their emergent drive. `universe` is the spawned world after
    `TimeController(step).run(...)`; `step` is the life-stepper (carrying `.dev`).
    Writes an SVG to `path` and returns (path, occupants)."""
    from .world import venues_for

    pop = universe.population
    venues = venues_for(universe.city, pop)
    home_of = {c: hh.home for hh in pop.households for c in hh.children}

    # place each child in a room of their home, coloured by emergent drive
    occupants: Dict[str, Dict[str, list]] = {}
    for cid, d in step.dev.items():
        home = home_of.get(cid)
        if home not in venues:
            continue
        room = _pick_room(venues[home])
        colour = NETWORK_COLOUR.get(d.get("outcome", ""), "#7BA05B")
        occupants.setdefault(home, {}).setdefault(room, []).append(colour)

    svg = render_settlement_plan(universe.city, venues, occupants=occupants, cell=cell)
    with open(path, "w") as f:
        f.write(svg)
    return path, occupants


# ---------------------------------------------------------------------------
# A WATCHABLE, animated view: spawn a town, run the clock, play it back
# ---------------------------------------------------------------------------

def render_watchable_town(spec, seed: int = 1, years: int = 18,
                          path: str = "town_live.html", cell: int = 72, pad: int = 20):
    """Spawn a town, run the clock year by year, and write a SELF-CONTAINED HTML page
    that plays the run back: the plan-view town with its people, play/pause, a speed
    control, a timeline slider, and pan/zoom. Each person is a dot in their home whose
    colour updates as their emergent dominant drive develops over the run.

    This is the first 'press play and watch' step. It animates DEVELOPMENTAL time (the
    population growing up); day-to-day movement of people between places on a schedule
    is a further layer, not yet built. Returns the path."""
    import json
    from project import spawn_universe
    from sim_world import TimeController, TimeScale
    from affective_engine.drives import read_mind
    from sim_viz.floorplan import render_settlement_plan
    from sim_viz.compositor import NETWORK_COLOUR
    from .world import venues_for

    uni = spawn_universe(spec, place_residents=False)
    pop = uni.population
    venues = venues_for(uni.city, pop)
    home_of = {c: hh.home for hh in pop.households for c in hh.children}
    city = uni.city

    step = __import__("sophropathy").make_life_stepper(uni, seed=seed)

    # town backdrop (no baked-in occupants -- we animate a people layer over it)
    backdrop = render_settlement_plan(city, venues, occupants=None, cell=cell, pad=pad)

    # a screen position for each child, spread within their home's footprint
    building_cell = {o.place: (o.x, o.y) for o in city.objects
                     if o.tile.startswith("building") and getattr(o, "place", None)}
    people_pos, used = {}, {}
    for cid in step.dev:
        c = building_cell.get(home_of.get(cid))
        if not c:
            continue
        gx, gy = c
        k = used.get((gx, gy), 0); used[(gx, gy)] = k + 1
        ox = (k % 3 - 1) * cell * 0.22
        oy = ((k // 3) % 3 - 1) * cell * 0.22
        people_pos[cid] = (pad + gx * cell + cell * 0.5 + ox,
                           pad + gy * cell + cell * 0.5 + oy)

    # run the clock year by year, snapshotting each child's CURRENT drive
    tc = TimeController(step)
    frames = []
    for yr in range(years):
        tc.run(TimeScale.YEAR, steps=1)
        drives = {}
        for cid, d in step.dev.items():
            if cid in people_pos:
                dom = read_mind(d["mind"]).dominant
                drives[cid] = dom.value if hasattr(dom, "value") else str(dom)
        frames.append({"label": f"age ~{yr + 1}", "drives": drives})

    circles = "".join(
        f'<circle id="c_{cid}" cx="{px:.1f}" cy="{py:.1f}" r="4.6" '
        f'fill="#8a8a8a" stroke="#333" stroke-width="0.6"/>'
        for cid, (px, py) in people_pos.items())
    svg = backdrop.replace("</svg>", f'<g id="people">{circles}</g></svg>')

    colours = {k: v for k, v in NETWORK_COLOUR.items()
               if k in ("SEEKING", "CARE", "PLAY", "LUST", "FEAR", "RAGE", "PANIC")}

    html = _WATCH_HTML.replace("__TITLE__", getattr(spec, "name", "town")) \
                      .replace("__SVG__", svg) \
                      .replace("__FRAMES__", json.dumps(frames)) \
                      .replace("__COLOURS__", json.dumps(colours)) \
                      .replace("__NPEOPLE__", str(len(people_pos)))
    with open(path, "w") as f:
        f.write(html)
    return path


_WATCH_HTML = """<!doctype html><html><head><meta charset="utf-8"><title>__TITLE__ - live</title>
<style>
html,body{margin:0;height:100%;background:#EAF0F2;overflow:hidden;font-family:Arial,sans-serif}
#stage{width:100vw;height:100vh;cursor:grab}#stage:active{cursor:grabbing}
#stage svg{transform-origin:0 0}
#bar{position:fixed;left:0;right:0;bottom:0;background:#fffd;border-top:1px solid #ccc;
padding:8px 12px;display:flex;gap:12px;align-items:center;font-size:13px;color:#333}
#play{cursor:pointer;border:1px solid #888;background:#fff;border-radius:5px;padding:4px 12px}
#slider{flex:1}#clock{min-width:90px;font-weight:bold}
#legend{position:fixed;top:8px;left:8px;background:#fff9;padding:8px 10px;border-radius:6px;
font-size:12px;color:#444;line-height:1.5}#legend b{display:block;margin-bottom:3px}
.sw{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:5px;vertical-align:-1px}
#hint{position:fixed;top:8px;right:8px;background:#fff9;padding:6px 10px;border-radius:6px;font-size:12px;color:#666}
</style></head><body>
<div id="hint">scroll = zoom &middot; drag = pan &middot; __NPEOPLE__ children</div>
<div id="legend"></div>
<div id="stage">__SVG__</div>
<div id="bar"><button id="play">&#9654; Play</button>
<span id="clock">day 0</span>
<input id="slider" type="range" min="0" max="0" value="0"/>
<label>speed <select id="speed"><option value="700">slow</option>
<option value="350" selected>normal</option><option value="120">fast</option></select></label></div>
<script>
const FRAMES=__FRAMES__, COLOURS=__COLOURS__;
const stage=document.getElementById('stage'), svg=stage.querySelector('svg');
const play=document.getElementById('play'), slider=document.getElementById('slider');
const clock=document.getElementById('clock'), speedSel=document.getElementById('speed');
slider.max=FRAMES.length-1;
// legend
const leg=document.getElementById('legend');
leg.innerHTML='<b>emergent drive</b>'+Object.keys(COLOURS).map(k=>
 `<div><span class="sw" style="background:${COLOURS[k]}"></span>${k}</div>`).join('');
// pan + zoom
let scale=1, tx=0, ty=0, dragging=false, lx=0, ly=0;
function apply(){svg.style.transform=`translate(${tx}px,${ty}px) scale(${scale})`;}
stage.addEventListener('wheel',e=>{e.preventDefault();const f=e.deltaY<0?1.1:0.9;
 const r=stage.getBoundingClientRect();const mx=e.clientX-r.left,my=e.clientY-r.top;
 tx=mx-(mx-tx)*f;ty=my-(my-ty)*f;scale*=f;apply();},{passive:false});
stage.addEventListener('mousedown',e=>{dragging=true;lx=e.clientX;ly=e.clientY;});
window.addEventListener('mousemove',e=>{if(!dragging)return;tx+=e.clientX-lx;ty+=e.clientY-ly;
 lx=e.clientX;ly=e.clientY;apply();});
window.addEventListener('mouseup',()=>dragging=false);
// playback
let i=0, playing=false, timer=null;
function draw(k){const fr=FRAMES[k];clock.textContent=fr.label;slider.value=k;
 for(const cid in fr.drives){const el=document.getElementById('c_'+cid);
  if(el)el.setAttribute('fill',COLOURS[fr.drives[cid]]||'#8a8a8a');}}
function tick(){draw(i);i++;if(i>=FRAMES.length){i=0;stop();}else
 timer=setTimeout(tick,parseInt(speedSel.value));}
function start(){playing=true;play.innerHTML='&#10073;&#10073; Pause';tick();}
function stop(){playing=false;play.innerHTML='&#9654; Play';clearTimeout(timer);}
play.onclick=()=>playing?stop():start();
slider.oninput=()=>{stop();i=parseInt(slider.value);draw(i);};
draw(0);
</script></body></html>"""

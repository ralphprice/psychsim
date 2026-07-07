"""demo.py -- render a town from sim_world with placeholder tiles, and show the
   PNG-tileset slot the AI art drops into."""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sim_world import build_world, Person, GameMaster, SocialEvent
from affective_engine import shared_root_seed
from .mapmodel import CityMap
from .binding import Layout, build_map, add_people, overlays_from_state
from .compositor import render_svg, save_svg
from .tileset import PlaceholderTileset, PngTileset, default_manifest


def build_demo_city():
    # a warm home so the climate tint reads "warm"
    world = build_world(home_warmth=0.9, home_structure=0.85)
    world.institutions["Family"].add_member("alex", "child")
    world.institutions["School"].add_member("alex", "pupil")
    gm = GameMaster(world)

    alex = Person("alex", "Alex", shared_root_seed())
    world.place_agent("alex", "classroom")
    # run one episode so Alex has a current dominant network to display
    gm.run_episode(alex, SocialEvent("offered cooperation", "classmate",
                   {"reward": 0.5, "social_valence": 0.5, "goal_relevance": 0.6}))

    layout = Layout(
        place_cells={"home": (2, 3), "street": (5, 5), "classroom": (9, 4),
                     "playground": (11, 6), "office": (5, 10)},
        cols=15, rows=14, base_terrain="terrain_grass")
    m = build_map(world, layout, name="demo_town")
    # a little greenery
    from .mapmodel import Placement
    for (x, y, t) in [(3, 5, "prop_tree"), (10, 6, "prop_playground"),
                      (6, 5, "prop_streetlight"), (1, 3, "prop_tree")]:
        m.objects.append(Placement(tile=t, x=x, y=y))
    add_people(m, world, {"alex": alex})
    ov = overlays_from_state(world, {"alex": alex})
    return world, m, ov, alex


def report() -> str:
    world, m, ov, alex = build_demo_city()
    save_svg(m, "demo_town.svg", PlaceholderTileset(), ov)

    L = ["=" * 70,
         "  SIM CITY VISUALISATION -- demo render (placeholder tiles)",
         "=" * 70,
         f"  town '{m.name}': {m.cols}x{m.rows} grid",
         f"  buildings: {sum(1 for o in m.objects if o.tile.startswith('building'))}"
         f" | props: {sum(1 for o in m.objects if o.tile.startswith('prop'))}"
         f" | roads: {len(m.roads)} | sims: {len(m.actors)}",
         f"  Alex is at: {world.location_of('alex')} "
         f"| dominant network: {alex.mind.dominant}",
         f"  climate overlay: {ov.place_climate}",
         "  wrote demo_town.svg (placeholder render)",
         "",
         "  THE SLOT: to render with real AI art instead, no code changes -- just:",
         "     from sim_viz import PngTileset, default_manifest, save_svg",
         "     ts = PngTileset('tiles/', default_manifest())   # folder of spec PNGs",
         "     save_svg(m, 'town.svg', ts, ov)",
         "  default_manifest() already names every tile per the graphics spec:",
         f"     {len(default_manifest())} tiles expected (terrain, roads, buildings, props, chars)",
         "=" * 70]
    return "\n".join(L)


if __name__ == "__main__":
    print(report())

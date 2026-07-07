import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

import unittest, tempfile

from sim_viz import (CityMap, Placement, Actor, PlaceholderTileset, PngTileset,
                     TileArt, default_manifest, render_svg, Overlays,
                     Layout, build_map, add_people, overlays_from_state, cell_to_screen)
from sim_viz.iso import TILE_W, TILE_H, iso_box_faces
from sim_world import build_world, Person, GameMaster, SocialEvent
from affective_engine import shared_root_seed


class TestGeometry(unittest.TestCase):
    def test_iso_transform(self):
        # origin cell at origin
        self.assertEqual(cell_to_screen(0, 0, 0, 0), (0, 0))
        # (1,0) shifts right+down by half a tile; (0,1) shifts left+down
        self.assertEqual(cell_to_screen(1, 0, 0, 0), (TILE_W/2, TILE_H/2))
        self.assertEqual(cell_to_screen(0, 1, 0, 0), (-TILE_W/2, TILE_H/2))

    def test_box_faces_present(self):
        faces = iso_box_faces(0, 0, 100)
        self.assertEqual(set(faces), {"top", "left", "right"})
        for v in faces.values():
            self.assertTrue(len(v.split()) == 4)  # four vertices each


class TestMapModel(unittest.TestCase):
    def test_json_round_trip(self):
        m = CityMap("t", 6, 6); m.fill_terrain("terrain_grass")
        m.objects.append(Placement("building_home", 1, 1, (1, 1), place="home"))
        m.actors.append(Actor("char_adult_a", 1, 1, agent_id="x"))
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            path = f.name
        m.save(path); m2 = CityMap.load(path)
        self.assertEqual(m2.cols, 6)
        self.assertEqual(m2.objects[0].place, "home")
        self.assertEqual(m2.actors[0].agent_id, "x")


class TestTilesets(unittest.TestCase):
    def test_placeholder_renders_all_categories(self):
        ts = PlaceholderTileset()
        self.assertIn("polygon", ts.render_ground("terrain_grass", 0, 0))
        self.assertIn("polygon", ts.render_object("building_home", 0, 0))
        self.assertIn("circle", ts.render_object("prop_tree", 0, 0))
        self.assertIn("path", ts.render_actor("char_adult_a", 0, 0))

    def test_png_tileset_emits_image_refs_and_skips_missing(self):
        ts = PngTileset("tiles", default_manifest())
        self.assertIn("<image", ts.render_ground("terrain_grass", 0, 0))
        self.assertIn("building_home.png", ts.render_object("building_home", 0, 0))
        # a tile not in the manifest renders nothing (partial sets still work)
        self.assertEqual(ts.render_ground("terrain_nonexistent", 0, 0), "")

    def test_default_manifest_covers_spec_categories(self):
        man = default_manifest()
        for tid in ("terrain_grass", "road_cross", "building_school",
                    "prop_tree", "char_child_a"):
            self.assertIn(tid, man)


class TestCompositor(unittest.TestCase):
    def test_render_produces_valid_svg(self):
        m = CityMap("t", 4, 4); m.fill_terrain("terrain_grass")
        m.objects.append(Placement("building_home", 1, 1, (1, 1)))
        svg = render_svg(m)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.rstrip().endswith("</svg>"))
        self.assertIn("viewBox", svg)

    def test_state_overlay_colours_actor(self):
        m = CityMap("t", 4, 4); m.fill_terrain("terrain_grass")
        m.actors.append(Actor("char_adult_a", 1, 1, agent_id="a"))
        ov = Overlays(actor_state={"a": "aggress"})   # emergent action, not a category
        svg = render_svg(m, overlays=ov)
        # the aggressive-action colour appears (state ring + legend)
        self.assertIn("#C0392B", svg)


class TestBinding(unittest.TestCase):
    def test_build_map_from_world(self):
        world = build_world()
        layout = Layout(place_cells={"home": (2, 2), "classroom": (6, 3),
                                     "office": (3, 7), "street": (4, 4)},
                        cols=12, rows=12)
        m = build_map(world, layout)
        kinds = {o.tile for o in m.objects if o.tile.startswith("building")}
        self.assertIn("building_home", kinds)
        self.assertIn("building_school", kinds)
        self.assertGreater(len(m.roads), 0)   # connections became roads

    def test_overlays_read_dominant_network_and_climate(self):
        world = build_world(home_warmth=0.2)   # harsh
        world.institutions["Family"].add_member("kid", "child")
        gm = GameMaster(world)
        kid = Person("kid", "Kid", shared_root_seed())
        world.place_agent("kid", "home")
        gm.run_episode(kid, SocialEvent("provoked", "sib",
                       {"provocation": 0.8, "social_valence": -0.6, "goal_relevance": 0.6}))
        ov = overlays_from_state(world, {"kid": kid})
        # the overlay reflects the substrate-driven dominant the episode set
        self.assertEqual(ov.actor_state["kid"], kid.mind.dominant)
        self.assertIsNotNone(kid.mind.dominant)
        self.assertEqual(ov.place_climate.get("home"), "harsh")


class TestProceduralTileset(unittest.TestCase):
    """The vector procedural tileset draws valid SVG for every layer, is a
    drop-in for the compositor, and renders deterministically."""

    def setUp(self):
        from sim_viz import ProceduralTileset
        self.ts = ProceduralTileset()

    def test_ground_object_actor_emit_svg(self):
        g = self.ts.render_ground("terrain_grass", 0, 0)
        r = self.ts.render_ground("road_straight_ns", 0, 0)
        b = self.ts.render_object("building_home", 0, 0, (1, 1))
        p = self.ts.render_object("prop_tree", 0, 0)
        a = self.ts.render_actor("char_child_a", 0, 0, state_colour="#8CB369")
        for frag in (g, r, b, p, a):
            self.assertTrue(frag.strip(), "empty SVG fragment")
        self.assertIn("polygon", g)      # ground is a diamond
        self.assertIn("polygon", b)      # building has faces
        self.assertIn("circle", a)       # actor has a head

    def test_building_has_walls_roof_and_openings(self):
        svg = self.ts.render_object("building_home", 0, 0, (1, 1))
        # walls + a pitched roof + at least one window and a door = many polygons
        self.assertGreaterEqual(svg.count("polygon"), 6)

    def test_deterministic(self):
        from sim_viz import ProceduralTileset
        a = ProceduralTileset().render_object("building_workplace", 128, 64, (1, 1))
        b = ProceduralTileset().render_object("building_workplace", 128, 64, (1, 1))
        self.assertEqual(a, b)

    def test_swaps_into_the_compositor(self):
        from sim_viz import ProceduralTileset
        m = CityMap(name="t", cols=4, rows=4)
        m.fill_terrain("terrain_grass")
        m.objects.append(Placement(tile="building_home", x=1, y=1,
                                   footprint=(1, 1), place="home"))
        svg = render_svg(m, ProceduralTileset(), Overlays())
        self.assertTrue(svg.startswith("<svg") or "<svg" in svg[:200])
        self.assertIn("polygon", svg)

    def test_every_building_type_renders(self):
        from sim_viz.procedural import BUILDING
        self.assertGreaterEqual(len(BUILDING), 12)   # broad catalogue
        for tid, spec in BUILDING.items():
            fp = (2, 2) if spec.get("wh", 0) and "sports" in tid or "school" in tid else (1, 1)
            svg = self.ts.render_object(tid, 0, 0, fp)
            self.assertTrue(svg.strip(), f"{tid} rendered empty")
            self.assertGreaterEqual(svg.count("polygon"), 3, f"{tid} too sparse")

    def test_broadened_terrain_and_props_render(self):
        for tid in ("terrain_garden", "terrain_plaza", "terrain_sand", "path_straight"):
            self.assertTrue(self.ts.render_ground(tid, 0, 0).strip(), tid)
        for tid in ("prop_hedge", "prop_flowerbed", "prop_fountain", "prop_bin",
                    "prop_bollard", "prop_bus_stop"):
            self.assertTrue(self.ts.render_object(tid, 0, 0).strip(), tid)

    def test_vehicles_render_on_the_actor_layer(self):
        for sprite in ("vehicle_car_a", "vehicle_car_b", "vehicle_bus", "vehicle_bike"):
            svg = self.ts.render_actor(sprite, 0, 0)
            self.assertTrue(svg.strip(), f"{sprite} rendered empty")
        # a vehicle is not drawn as a person (no head circle at figure height)
        car = self.ts.render_actor("vehicle_car_a", 0, 0)
        person = self.ts.render_actor("char_adult_a", 0, 0)
        self.assertNotEqual(car, person)


if __name__ == "__main__":
    unittest.main(verbosity=2)

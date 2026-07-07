import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core")); _S.path.insert(0, _O.path.join(_ROOT, "extensions"))

"""The top-down glass-roof renderer draws buildings from their Venue/Area/
AffordanceObject data: rooms, furniture and occupants, in one pannable SVG."""
import unittest
from sim_viz import (SettlementSpec, generate_settlement, render_settlement_plan,
                     render_building_plan)
from sophropathy.world import build_home, build_school, venues_for


class TestFloorplan(unittest.TestCase):
    def test_building_plan_draws_rooms_and_furniture(self):
        svg = render_building_plan(build_home(), 0, 0, 320, 260,
                                   occupants={"kitchen": [False, True]})
        # a home has >=5 rooms, each a rect; furniture and a sim present
        self.assertGreaterEqual(svg.count("<rect"), 5)
        self.assertIn("#B6A98E", svg)          # furniture fill
        self.assertIn("<circle", svg)          # an occupant

    def test_rooms_are_labelled_from_the_model(self):
        svg = render_building_plan(build_home(), 0, 0, 400, 400)
        for room in ("kitchen", "lounge", "bathroom"):
            self.assertIn(room.replace("_", " "), svg)

    def test_settlement_plan_renders_buildings_as_plans(self):
        city = generate_settlement(SettlementSpec(homes=8, offices=1, schools=1,
                                                  shops=1, seed=1))
        venues = venues_for(city)
        svg = render_settlement_plan(city, venues, cell=90)
        self.assertIn("<svg", svg[:120])
        self.assertIn("viewBox", svg[:200])    # pannable/zoomable
        self.assertIn("#F3E7C9", svg)          # kitchen floor tint -> homes drawn as plans
        self.assertGreater(svg.count("<rect"), 50)

    def test_occupants_placed_in_rooms(self):
        city = generate_settlement(SettlementSpec(homes=4, seed=2))
        venues = venues_for(city)
        home0 = [o.place for o in city.objects if o.place and o.place.startswith("home")][0]
        occ = {home0: {"kitchen": [False, True]}}
        svg = render_settlement_plan(city, venues, occupants=occ, cell=90)
        self.assertIn("#5B7BA0", svg)          # an adult dot
        self.assertIn("#7BA05B", svg)          # a child dot



class TestCorridorLayout(unittest.TestCase):
    def test_plan_has_walls_with_doorways_not_solid_blocks(self):
        svg = render_building_plan(build_home(children=2, child_bedrooms=2),
                                   0, 0, 380, 300)
        self.assertGreater(svg.count("<line"), 12)      # walls as segments
        self.assertIn("#9A8F79", svg)                   # doorway leaves
        self.assertIn("#E7E2D6", svg)                   # a corridor



class TestGardenAndDoors(unittest.TestCase):
    def test_home_with_garden_draws_outdoor_space_and_back_door(self):
        v = build_home(children=2, child_bedrooms=2, garden=True, garden_size=0.7)
        self.assertIn("garden", v.areas)                 # garden is part of the model
        svg = render_building_plan(v, 0, 0, 400, 340)
        self.assertIn(">garden<", svg)                   # garden drawn
        self.assertIn("#9A8F79", svg)                    # front/back door leaves

    def test_flat_without_garden_has_no_garden_area(self):
        v = build_home(children=1, child_bedrooms=1, garden=False)
        self.assertNotIn("garden", v.areas)

    def test_garden_affords_outdoor_play(self):
        v = build_home(garden=True, garden_size=0.6)
        affs = [a.name for a in v.areas["garden"].affordances()]
        self.assertIn("play_outside", affs)


if __name__ == "__main__":
    unittest.main(verbosity=2)

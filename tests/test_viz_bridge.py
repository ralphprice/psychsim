import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

"""The clock<->graphics bridge: rendering the spawned town in PLAN VIEW (the glass-
roof floor-plan design) with each aged child placed in a room of their real home,
coloured by their emergent drive."""
import os, tempfile, unittest
from project import ProjectSpec, spawn_universe
from sim_world import TimeController, TimeScale
from sophropathy import make_life_stepper, render_aged_town


class TestVizBridge(unittest.TestCase):
    def _aged(self):
        uni = spawn_universe(ProjectSpec(name="t", target_population=60,
                             profile="england_2021", extensions=["sophropathy"],
                             fearless_frac=0.4, seed=7), place_residents=False)
        step = make_life_stepper(uni, seed=1)
        TimeController(step).run(TimeScale.YEAR, steps=22)
        return uni, step

    def test_renders_the_spawned_town_in_plan_view(self):
        uni, step = self._aged()
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "aged.svg")
            out, occupants = render_aged_town(uni, step, path=path)
            self.assertTrue(os.path.exists(out))
            svg = open(out).read()
            # plan-view markers: floor-plan rooms/walls and gardens, NOT isometric
            self.assertIn("<rect", svg)
            self.assertIn(">garden<", svg)
            self.assertNotIn("<polygon", svg)          # no isometric geometry

    def test_children_placed_in_rooms_coloured_by_emergent_drive(self):
        uni, step = self._aged()
        with tempfile.TemporaryDirectory() as td:
            _, occupants = render_aged_town(uni, step, path=os.path.join(td, "a.svg"))
            self.assertTrue(occupants)                  # some homes occupied
            # each occupant entry is a colour string (the emergent-drive colour)
            colours = [c for rooms in occupants.values()
                       for lst in rooms.values() for c in lst]
            self.assertTrue(colours)
            self.assertTrue(all(isinstance(c, str) and c.startswith("#") for c in colours))


if __name__ == "__main__":
    unittest.main(verbosity=2)

import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

"""The day-to-day life layer (modelled on Park): positions + addresses, A* over the
spawned town, role schedules, and a day-cycle stepper producing a movement trajectory."""
import os, tempfile, unittest
from project import ProjectSpec, spawn_universe
from sophropathy.world import venues_for
from sophropathy.townlife import (build_town_space, astar, scheduled_block,
                                   simulate_townlife, render_townlife_html)


def _town():
    uni = spawn_universe(ProjectSpec(name="t", target_population=60,
                         profile="england_2021", extensions=["sophropathy"],
                         fearless_frac=0.4, seed=7), place_residents=False)
    return uni, venues_for(uni.city, uni.population)


class TestTownSpace(unittest.TestCase):
    def test_walkable_and_entrances_and_rooms(self):
        uni, venues = _town()
        sp = build_town_space(uni.city, venues)
        self.assertGreater(len(sp.walk), 0)
        self.assertIn("school_0", sp.entrances)
        self.assertIn("classroom", sp.rooms.get("school_0", []))

    def test_astar_routes_home_to_school(self):
        uni, venues = _town()
        sp = build_town_space(uni.city, venues)
        homes = [p for p in sp.cells if p.startswith("home")]
        reachable = sum(1 for h in homes if sp.route(sp.entrances[h], "school_0"))
        self.assertEqual(reachable, len(homes))     # every home reaches the school

    def test_astar_returns_empty_for_unreachable(self):
        # an isolated goal off the walkable graph yields no path
        self.assertEqual(astar((0, 0), (999, 999), {(0, 0), (0, 1)}), [])


class TestSchedule(unittest.TestCase):
    def test_children_at_school_midday_weekday_home_at_night(self):
        # weekday: a child is at school around midday, home at night
        self.assertEqual(scheduled_block(11, False, True)[0], "school")
        self.assertEqual(scheduled_block(2, False, True)[0], "home")

    def test_adults_at_work_midday_weekday(self):
        self.assertEqual(scheduled_block(11, False, False)[0], "work")

    def test_weekend_has_no_school_or_work(self):
        keys = {scheduled_block(h, True, True)[0] for h in range(24)}
        self.assertNotIn("school", keys)
        keys_a = {scheduled_block(h, True, False)[0] for h in range(24)}
        self.assertNotIn("work", keys_a)


class TestDayCycle(unittest.TestCase):
    def test_people_move_over_the_day(self):
        uni, _ = _town()
        space, frames, _info = simulate_townlife(uni, days=1, tick_minutes=15, seed=1)
        self.assertGreater(len(frames), 0)
        moved = sum(1 for i in range(1, len(frames))
                    if frames[i]["pos"] != frames[i - 1]["pos"])
        self.assertGreater(moved, 0)                # somebody walks somewhere

    def test_children_gather_at_school_during_the_day(self):
        uni, _ = _town()
        space, frames, _info = simulate_townlife(uni, days=1, tick_minutes=15, seed=1)
        sc = space.place_cell(next(p for p in space.cells if p.startswith("school")))
        peak = max(sum(1 for t in fr["pos"].values() if t == sc) for fr in frames)
        self.assertGreaterEqual(peak, 2)            # a class forms at the school

    def test_renders_watchable_html(self):
        uni, _ = _town()
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "life.html")
            out = render_townlife_html(uni, days=1, tick_minutes=30, seed=1, path=path)
            self.assertTrue(os.path.exists(out))
            h = open(out).read()
            self.assertIn('id="play"', h)           # a player
            self.assertIn('id="people"', h)         # a people layer


if __name__ == "__main__":
    unittest.main(verbosity=2)

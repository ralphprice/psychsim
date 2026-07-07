import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core")); _S.path.insert(0, _O.path.join(_ROOT, "extensions")); _S.path.insert(0, _ROOT)

"""The time controller: one clock scalable from real time (interaction by
interaction) to yearly, surfacing events at the chosen granularity."""
import unittest
from sim_world import (TimeController, TimeScale, Event, Instant, SimClock,
                       Period)
from sim_world.timeline import MIN_PER_DAY


class TestClockAndScales(unittest.TestCase):
    def test_scales_are_minutes(self):
        self.assertEqual(int(TimeScale.HOUR), 60)
        self.assertEqual(int(TimeScale.DAY), 60 * 24)
        self.assertEqual(int(TimeScale.WEEK), MIN_PER_DAY * 7)
        self.assertEqual(int(TimeScale.YEAR), MIN_PER_DAY * 365)

    def test_instant_addresses_every_granularity(self):
        i = Instant(MIN_PER_DAY * 400 + 60 * 14 + 30)   # ~1yr 35d, 14:30
        self.assertEqual(i.hour, 14)
        self.assertEqual(i.minute, 30)
        self.assertEqual(i.year, 1)                      # 400 days -> year index 1
        self.assertIn("Y2", i.label())

    def test_clock_advances(self):
        c = SimClock()
        c.advance(90)
        self.assertEqual(c.total_minutes, 90)
        self.assertEqual(c.now.hour, 1)


class TestController(unittest.TestCase):
    def _counter_step(self):
        def step(clock, minutes):
            clock.advance(minutes)
            return [Event(clock.total_minutes, "tick", text="t")]
        return step

    def test_runs_at_any_scale_and_advances_clock(self):
        tc = TimeController(self._counter_step())
        tc.run(TimeScale.DAY, steps=3)
        self.assertEqual(tc.clock.total_minutes, 3 * MIN_PER_DAY)
        self.assertEqual(len(tc.events), 3)

    def test_step_moves_clock_even_if_stepfn_forgets(self):
        def lazy(clock, minutes):
            return []                                    # doesn't advance
        tc = TimeController(lazy)
        tc.run(TimeScale.HOUR, steps=2)
        self.assertEqual(tc.clock.total_minutes, 120)    # controller advanced it

    def test_fine_scale_lists_events_coarse_aggregates(self):
        def step(clock, minutes):
            start = clock.total_minutes
            clock.advance(minutes)
            return [Event(start + i, "interaction", text=f"e{i}") for i in range(5)]
        tc = TimeController(step)
        fine = tc.run(TimeScale.REALTIME, steps=1)[0]
        self.assertIn("e0", fine.summary())              # individual events shown
        tc2 = TimeController(step)
        coarse = tc2.run(TimeScale.YEAR, steps=1)[0]
        self.assertIn("interaction", coarse.summary())   # aggregated count
        self.assertIn("5", coarse.summary())

    def test_notable_events_capped(self):
        def step(clock, minutes):
            start = clock.total_minutes
            clock.advance(minutes)
            return [Event(start, "rupture", text=f"r{i}") for i in range(20)]
        p = TimeController(step).run(TimeScale.YEAR, steps=1)[0]
        self.assertIn("more", p.summary())               # capped with '... and N more'


class TestUniverseDriver(unittest.TestCase):
    def test_driver_emits_events_across_scales(self):
        from project import ProjectSpec, spawn_universe
        from sophropathy import make_stepper
        uni = spawn_universe(ProjectSpec(name="P", target_population=80,
                                         extensions=["sophropathy"], seed=3),
                             place_residents=False)
        tc = TimeController(make_stepper(uni, seed=1))
        rt = tc.run(TimeScale.REALTIME, steps=3)
        self.assertTrue(any(e.kind == "interaction" for p in rt for e in p.events))
        yr = tc.run(TimeScale.YEAR, steps=1)[0]
        self.assertTrue(any(e.kind == "milestone" for e in yr.events))



class TestClockDrivesDevelopment(unittest.TestCase):
    """Advancing the clock ages the population through their lived days to
    classified outcomes -- the clock, day loop and development rule connected."""

    def _universe(self):
        from project import ProjectSpec, spawn_universe
        return spawn_universe(ProjectSpec(name="P", target_population=160,
                                          extensions=["sophropathy"],
                                          fearless_frac=0.2, seed=5),
                              place_residents=False)

    def test_advancing_clock_ages_children(self):
        from sophropathy import make_life_stepper
        uni = self._universe()
        step = make_life_stepper(uni, seed=1)
        before = {c: d["age"] for c, d in step.dev.items()}
        tc = TimeController(step)
        tc.run(TimeScale.YEAR, steps=3)
        aged = [step.dev[c]["age"] > before[c] for c in before if not step.dev[c]["done"]]
        self.assertTrue(all(aged) and aged)              # every developing child aged

    def test_children_reach_classified_outcomes(self):
        from sophropathy import make_life_stepper
        uni = self._universe()
        step = make_life_stepper(uni, seed=1)
        tc = TimeController(step)
        tc.run(TimeScale.YEAR, steps=25)                 # a full childhood span
        outcomes = [d["outcome"] for d in step.dev.values() if d["done"]]
        self.assertTrue(outcomes)                        # some grew up
        from affective_engine.drives import System
        valid = {s.value for s in System}
        self.assertTrue(all(o in valid for o in outcomes))   # emergent system readouts

    def test_outcome_tracks_home_climate(self):
        # the environment must transmit: warmer homes -> more sophropathic
        import statistics as st
        from sophropathy import make_life_stepper
        uni = self._universe()
        step = make_life_stepper(uni, seed=1)
        TimeController(step).run(TimeScale.YEAR, steps=25)
        by = {}
        for d in step.dev.values():
            if d["done"]:
                by.setdefault(d["outcome"], []).append(d["warmth"])
        if "sophropathic" in by and "intermediate" in by:
            self.assertGreater(st.mean(by["sophropathic"]), st.mean(by["intermediate"]))

    def test_outcomes_emit_as_milestones(self):
        from sophropathy import make_life_stepper
        uni = self._universe()
        tc = TimeController(make_life_stepper(uni, seed=1))
        periods = tc.run(TimeScale.YEAR, steps=25)
        milestones = [e for p in periods for e in p.events if e.kind == "milestone"]
        self.assertTrue(any("reaches adulthood" in e.text for e in milestones))


if __name__ == "__main__":
    unittest.main(verbosity=2)

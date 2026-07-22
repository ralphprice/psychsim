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

    # PERF: three of these tests each re-ran the SAME 160-agent x 25-year development (same seed=5
    # universe, same seed=1 stepper) to assert three different things about the one result -- three of
    # the most expensive tests in the suite computing an identical simulation. They now share ONE run
    # in setUpClass. Behaviour-neutral: same seeds, same computation, read three ways. (The 3-step
    # ageing test below builds its own fresh universe -- it reads state BEFORE running, so it cannot
    # share the developed fixture.)
    @classmethod
    def setUpClass(cls):
        from project import ProjectSpec, spawn_universe
        from sophropathy import make_life_stepper
        uni = spawn_universe(ProjectSpec(name="P", target_population=160, extensions=["sophropathy"],
                                         fearless_frac=0.2, seed=5), place_residents=False)
        cls._step = make_life_stepper(uni, seed=1)
        cls._periods = TimeController(cls._step).run(TimeScale.YEAR, steps=25)   # a full childhood span

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
        outcomes = [d["outcome"] for d in self._step.dev.values() if d["done"]]
        self.assertTrue(outcomes)                        # some grew up
        from substrate.readout import _READOUT_DOMAINS as valid
        self.assertTrue(all(o in valid for o in outcomes))   # emergent system readouts

    @unittest.skip("retired verdict vocabulary; re-enable after the read-out re-derivation "
                   "(maps outcome DOMAINS -> the sophropathy gradient this test asserts a direction on)")
    def test_outcome_tracks_home_climate(self):
        # ★ SUSPENDED, NOT SILENTLY-GREEN (audit / perf sweep -- the 4th vacuous guard this session, and the
        # most expensive: a full 25-year run that asserted NOTHING). The old body guarded
        #     if "sophropathic" in by and "intermediate" in by: self.assertGreater(...)
        # but `by` is keyed on d["outcome"], and outcomes are now _READOUT_DOMAINS members
        # (reward_approach/affiliation/defensive_threat/social_cognition/executive). "sophropathic" and
        # "intermediate" are the RETIRED verdict vocabulary and can NEVER be keys, so the guard never fired.
        #
        # I did NOT replace it with a proxy. Measured on this fixture: warmth by outcome is
        # defensive_threat 0.674 (n=36) vs social_cognition 0.653 (n=8) -- a 0.021 spread on small,
        # unequal n (noise-scale), and the direction does not obviously match the old "warmer -> more
        # sophropathic (prosocial)" intent (here warmth weakly tracks defensive_threat). Asserting
        # "max-min > 0" would pass on almost any two subsamples -- a second near-vacuous guard, which is the
        # exact defect being removed. And asserting the DIRECTION requires a domain->sophropathy mapping that
        # does not exist yet.
        #
        # RESOLUTION CONDITION: the RULED read-out re-derivation supplies the domain->sophropathy-gradient
        # mapping. Re-enable then, asserting the real intent (warmer homes -> more of the sophropathic
        # domain) against a null, on adequate n. Until then this stays visibly skipped, not falsely green.
        self.fail("unreachable -- skipped")

    def test_outcomes_emit_as_milestones(self):
        milestones = [e for p in self._periods for e in p.events if e.kind == "milestone"]
        self.assertTrue(any("reaches adulthood" in e.text for e in milestones))


if __name__ == "__main__":
    unittest.main(verbosity=2)

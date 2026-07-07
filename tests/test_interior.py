import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

"""Core spatial-interaction machinery: access rules, the neutral norm mechanism,
and the day loop -- all with NO built-in venues, routines or categories."""
import unittest

from sim_world import (Access, Affordance, AffordanceObject, Area, Door, Venue,
                       Norm, assess, departure_magnitude, observer_reaction,
                       category_of, Person, Inhabitant, Routine, Block, run_day)
from affective_engine import sophropathic_seed


class TestAccess(unittest.TestCase):
    """Access is a generic boundary -- open, role-restricted or closed. A lock is
    just the closed case; the universal feature is who may enter where."""

    def test_open_by_default(self):
        self.assertTrue(Access().permits())
        self.assertTrue(Access().permits("anyone"))

    def test_role_restricted(self):
        a = Access(roles={"staff"})
        self.assertTrue(a.permits("staff"))
        self.assertFalse(a.permits("guest"))
        self.assertFalse(a.permits(None))

    def test_closed(self):
        self.assertFalse(Access(is_open=False).permits("staff"))

    def test_door_permits(self):
        d = Door("back", Access(roles={"resident"}))
        self.assertTrue(d.permits("resident"))
        self.assertFalse(d.permits("visitor"))


class TestNeutralNorms(unittest.TestCase):
    """The norm mechanism carries no categories of its own; a study supplies the
    profile. Acting below what a place expects is a neutral departure."""

    def test_assess_against_a_supplied_profile(self):
        profile = {"disruptive": Norm.UNACCEPTABLE, "cooperative": Norm.ENCOURAGED}
        self.assertEqual(assess("disruptive", profile), (Norm.UNACCEPTABLE, True))
        self.assertEqual(assess("cooperative", profile), (Norm.ENCOURAGED, False))

    def test_unmentioned_category_is_tolerated(self):
        self.assertEqual(assess("whatever", {"x": Norm.ENCOURAGED}),
                         (Norm.TOLERATED, False))

    def test_no_category_or_no_profile(self):
        self.assertEqual(assess(None, {"x": Norm.ENCOURAGED}), (Norm.TOLERATED, False))
        self.assertEqual(assess("x", {}), (Norm.TOLERATED, False))

    def test_departure_magnitude_and_observer_reaction(self):
        self.assertGreater(departure_magnitude(Norm.UNACCEPTABLE), 0)
        self.assertEqual(departure_magnitude(Norm.ACCEPTED), 0.0)
        self.assertLess(observer_reaction(Norm.UNACCEPTABLE)["social_valence"], 0)
        self.assertEqual(observer_reaction(Norm.ACCEPTED), {})

    def test_category_of_reads_only_the_affordance(self):
        aff = Affordance("act", "opportunity", {}, category="cooperative")
        self.assertEqual(category_of("callous_exploitation", aff), "cooperative")
        # no affordance category -> None (the core does not map networks)
        self.assertIsNone(category_of("callous_exploitation", None))


class TestCoreShipsNoContent(unittest.TestCase):
    def test_no_builtin_venues_or_categories(self):
        import sim_world
        for name in ("build_home", "build_school", "build_shop", "norms_for",
                     "child_routine", "CATEGORIES"):
            self.assertNotIn(name, sim_world.__all__,
                             f"{name} should not be in the neutral core")


class TestDayLoopMachinery(unittest.TestCase):
    """The loop runs over a hand-built neutral venue: no builders needed."""

    def _tiny_world(self, act_category, area_norms):
        area = Area("room", [AffordanceObject("thing", [
            Affordance("act", "opportunity", {"reward": 0.4, "social_valence": 0.3},
                       category=act_category)])], norms=area_norms)
        return {"V": Venue("V", "generic", {"room": area}, entry="room")}

    def test_runs_and_records(self):
        venues = self._tiny_world("neutral", {"neutral": Norm.ACCEPTED})
        agent = Person("a", "A", sophropathic_seed())
        r = Routine("x", {9: Block("act", "V", "room")}, "V", "room")
        log = run_day(venues, {"a": Inhabitant(agent, r)}, hours=range(9, 10))
        self.assertEqual(len(log.records), 1)
        self.assertEqual(log.records[0].category, "neutral")
        self.assertFalse(log.records[0].departure)

    def test_departure_flagged_from_local_norms(self):
        venues = self._tiny_world("rowdy", {"rowdy": Norm.UNACCEPTABLE})
        agent = Person("a", "A", sophropathic_seed())
        r = Routine("x", {9: Block("act", "V", "room")}, "V", "room")
        log = run_day(venues, {"a": Inhabitant(agent, r)}, hours=range(9, 10))
        self.assertTrue(log.records[0].departure)

    def test_access_restricted_area_present_in_a_hand_built_venue(self):
        area = Area("lobby", [], [Door("vault", Access(roles={"keyholder"}))])
        self.assertFalse(area.door_to("vault").permits("visitor"))
        self.assertTrue(area.door_to("vault").permits("keyholder"))


if __name__ == "__main__":
    unittest.main(verbosity=2)

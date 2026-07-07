import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

"""The sophropathy study's world extension: the formative venues, the study's
symmetric social categories (with a positive pole), local norms, access as
respect for a boundary, and a child's day -- all about social conduct, with no
offence framing anywhere."""
import unittest

from sim_world import assess, Norm, Person, Inhabitant, run_day
from sophropathy.world import (build_home, build_school, build_workplace,
                               build_community, child_routine, run_study_day,
                               study_category, NORMS, CATEGORIES,
                               WARM, COOPERATIVE, CONSIDERATE, SELF_DIRECTED,
                               BOISTEROUS, DISRUPTIVE)
from affective_engine import sophropathic_seed, psychopathic_seed


class TestStudyCategories(unittest.TestCase):
    def test_positive_pole_is_first_class(self):
        # the construct's positive pole exists as categories in their own right
        for pos in (WARM, COOPERATIVE, CONSIDERATE):
            self.assertIn(pos, CATEGORIES)

    def test_no_offence_categories(self):
        for bad in ("theft", "criminal", "aggression", "reckless"):
            self.assertNotIn(bad, CATEGORIES)

    def test_affordance_category_precedes_network_reading(self):
        from sim_world import Affordance
        buy_like = Affordance("share", "cooperation", {}, category=COOPERATIVE)
        self.assertEqual(study_category("callous_exploitation", buy_like), COOPERATIVE)


class TestFamilyInterior(unittest.TestCase):
    def test_home_has_family_areas(self):
        home = build_home(children=1)
        for a in ("kitchen", "lounge", "bathroom", "parents_bedroom", "child_bedroom_1"):
            self.assertIn(a, home.areas)

    def test_shared_sibling_bedroom(self):
        home = build_home(shared_bedroom=True)
        self.assertIn("shared_bedroom", home.areas)
        self.assertNotIn("child_bedroom_1", home.areas)

    def test_bedroom_access_is_private(self):
        # a bedroom is a boundary: only its occupant role may enter (respect,
        # not a lock)
        home = build_home()
        d = home.area("kitchen").door_to("parents_bedroom")
        self.assertTrue(d.permits("parent"))
        self.assertFalse(d.permits("child"))


class TestLocalNorms(unittest.TestCase):
    def test_same_conduct_read_by_place(self):
        # boisterousness: encouraged in the playground, out of place in the class
        self.assertFalse(assess(BOISTEROUS, NORMS["playground"])[1])
        self.assertTrue(assess(BOISTEROUS, NORMS["classroom"])[1])
        self.assertTrue(assess(BOISTEROUS, NORMS["workplace"])[1])
        self.assertFalse(assess(BOISTEROUS, NORMS["community"])[1])

    def test_considerate_conduct_is_welcome_everywhere(self):
        for kind in ("classroom", "playground", "workplace", "community"):
            self.assertFalse(assess(CONSIDERATE, NORMS[kind])[1])


class TestSchoolAndAccess(unittest.TestCase):
    def test_staff_room_is_access_restricted(self):
        school = build_school()
        d = school.area("classroom").door_to("staff_room")
        self.assertTrue(d.permits("teacher"))
        self.assertFalse(d.permits("child"))

    def test_workplace_back_office_restricted(self):
        wp = build_workplace()
        d = wp.area("work_floor").door_to("back_office")
        self.assertTrue(d.permits("manager"))
        self.assertFalse(d.permits("visitor"))


class TestStudyDay(unittest.TestCase):
    def test_a_childs_day_runs_as_social_conduct(self):
        venues = {"Home": build_home(warmth=0.9), "School": build_school()}
        alex = Person("alex", "Alex", sophropathic_seed())
        log = run_study_day(venues, {"alex": Inhabitant(alex, child_routine("Home", "School"))})
        self.assertGreater(len(log.records), 8)
        # every recorded category is one of the study's social categories
        for r in log.records:
            self.assertIn(r.category, CATEGORIES)
        # no record carries any offence label (there are none to carry)
        self.assertTrue(all(r.category in CATEGORIES for r in log.records))



class TestHomeSizing(unittest.TestCase):
    def test_home_built_to_child_bedroom_count(self):
        h = build_home(children=3, child_bedrooms=3)
        beds = [a for a in h.areas if "child_bedroom" in a]
        self.assertEqual(len(beds), 3)

    def test_more_children_than_bedrooms_creates_shared_rooms(self):
        h = build_home(children=4, child_bedrooms=2)
        shared = [a for a in h.areas if "shared_bedroom" in a]
        self.assertTrue(shared)          # siblings share when bedrooms < children


if __name__ == "__main__":
    unittest.main(verbosity=2)

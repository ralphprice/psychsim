import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

"""Stage 4: significant life-activities as age-gated stimulus bundles. Tests check
the machinery (bundles present triggers, age-gating works) and, importantly, the
child-safety age-gate on the intimacy bundle."""
import random
import unittest
from affective_engine.activities import (Activity, ACTIVITIES, activities_for_age,
                                          sample_activity)


class TestActivities(unittest.TestCase):
    def test_activities_present_trigger_bundles(self):
        for a in ACTIVITIES:
            self.assertIsInstance(a.stimulus, dict)
            self.assertTrue(a.stimulus)                       # a non-empty bundle
            self.assertTrue(all(0.0 <= v <= 1.0 for v in a.stimulus.values()))

    def test_age_gating_offers_age_appropriate_activities(self):
        young = {a.id for a in activities_for_age(3)}
        teen = {a.id for a in activities_for_age(16)}
        self.assertIn("play", young)
        self.assertIn("sport", teen)
        # sport and formal learning are not offered to a 3-year-old
        self.assertNotIn("sport", young)

    def test_intimacy_is_age_gated_away_from_children(self):
        # child safety: the intimacy bundle must never be offered to children
        for age in (2, 5, 8, 10, 12, 13):
            self.assertNotIn("intimacy", {a.id for a in activities_for_age(age)})
        self.assertIn("intimacy", {a.id for a in activities_for_age(16)})

    def test_sample_activity_respects_age(self):
        rng = random.Random(0)
        for _ in range(200):
            self.assertNotEqual(sample_activity(6, rng).id, "intimacy")

    def test_a_real_diet_includes_hard_experiences(self):
        ids = {a.id for a in ACTIVITIES}
        # a life is not all reward: adversity is represented (realism, not outcome)
        self.assertTrue({"failure", "rejection", "loss", "being_told_off"} <= ids)


if __name__ == "__main__":
    unittest.main(verbosity=2)

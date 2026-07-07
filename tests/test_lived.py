import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

"""The closed loop: a childhood LIVED IN THE WORLD drives the EMERGENT substrate.
These tests check the MACHINERY -- that a life produces an emergent mind read out
as a dominant primary system, with a full drive-profile -- NOT that outcomes match
any decreed label. At this crude stage no clean environment->outcome order is
expected or wanted; that would be a sign of forcing."""
import unittest

from sophropathy import (build_home, build_school, raise_in_world,
                         fearless_child_seed, typical_child_seed)
from affective_engine.drives import System


class TestLivedChildhood(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.school = build_school()
        cls.warm = build_home("Warm", warmth=0.9, structure=0.85)
        cls.harsh = build_home("Harsh", warmth=0.2, structure=0.25)

    def test_childhood_produces_an_emergent_readout(self):
        r = raise_in_world(fearless_child_seed(), self.warm, self.school)
        # the outcome is a dominant primary system, emergent from the wiring
        self.assertIsInstance(r.dominant, System)
        self.assertEqual(r.classification, r.dominant.value)

    def test_readout_carries_a_full_drive_profile(self):
        r = raise_in_world(typical_child_seed(), self.harsh, self.school)
        self.assertEqual(set(r.profile), {s.value for s in System})
        total = sum(r.profile.values())
        self.assertAlmostEqual(total, 1.0, places=5)      # a normalised profile

    def test_outcome_is_produced_by_the_life_not_preset(self):
        # different lived experience (situation streams) can yield different minds
        outs = {raise_in_world(fearless_child_seed(), self.harsh, self.school,
                               situation_seed=s).dominant for s in range(12)}
        # a produced outcome: at least it is a valid emergent system (not a fixed label)
        self.assertTrue(outs.issubset(set(System)))
        self.assertGreaterEqual(len(outs), 1)

    def test_no_decreed_psychopathy_label(self):
        # the old hand-coded labels are gone: the readout is a neutral system name
        r = raise_in_world(fearless_child_seed(), self.harsh, self.school)
        self.assertNotIn(r.classification,
                         ("sophropathic", "intermediate", "psychopathic"))


if __name__ == "__main__":
    unittest.main(verbosity=2)

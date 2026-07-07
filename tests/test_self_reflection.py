import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""S10.2 -- the fourth matrix (self-reflection). Self on both sides, same engine as the other
three; whether reflection yields prosocial updating must EMERGE (no coded conscience)."""

import tokenize
import unittest

from sim_world.self_reflection import SelfReflection, SELF
from sim_world.relations import RelationshipMatrix
from sim_world import self_reflection as sr_module


class TestSelfAsBothSides(unittest.TestCase):
    def test_uses_the_same_relationship_engine(self):
        sr = SelfReflection()
        self.assertIsInstance(sr.matrix, RelationshipMatrix)

    def test_positive_self_appraisal_raises_self_value(self):
        sr = SelfReflection()
        for _ in range(10):
            sr.reflect(r=0.4, attachment_pull=0.5)
        self.assertGreater(sr.self_value(), 0.0)

    def test_negative_self_appraisal_lowers_self_value(self):
        sr = SelfReflection()
        for _ in range(10):
            sr.reflect(r=-0.4, threat_pull=0.5)
        self.assertLess(sr.self_value(), 0.0)

    def test_self_is_the_partner(self):
        sr = SelfReflection()
        sr.reflect(r=0.3)
        self.assertIn(SELF, sr.matrix.slots)

    def test_ambivalent_self_emerges(self):
        # self-directed approach AND threat both high -> the internal ambivalent bond
        sr = SelfReflection()
        for _ in range(8):
            sr.reflect(r=-0.1, attachment_pull=0.8, threat_pull=0.7)
        self.assertTrue(sr.is_ambivalent_toward_self())


class TestNoCodedConscience(unittest.TestCase):
    def test_reflection_codes_no_moral_mapping(self):
        # S10.2: no line maps "reflected on bad conduct" -> "becomes prosocial". The code has
        # no conscience/remorse/prosocial/moral tokens; reflect() just takes a valence.
        with open(sr_module.__file__, "rb") as fh:
            names = {t.string.lower() for t in tokenize.tokenize(fh.readline)
                     if t.type == tokenize.NAME}
        for banned in ("conscience", "remorse", "prosocial", "moral", "guilt", "virtue"):
            self.assertNotIn(banned, names)

    def test_reflect_signature_is_just_a_valence_update(self):
        import inspect
        params = set(inspect.signature(SelfReflection.reflect).parameters)
        self.assertEqual(params, {"self", "r", "attachment_pull", "threat_pull",
                                  "drive_profile"})


if __name__ == "__main__":
    unittest.main()

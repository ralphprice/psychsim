import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""8b divergence loop (PsychSim_MASTER Part 3 S4/S5) -- the proto-psychopath THROTTLE study.

The CU signatures EMERGE from a graded hypofunction throttle on the affective-empathy
circuitry of an ORDINARY newborn -- measured, not seeded. Honesty (S5.5): the manipulation is a
numeric gain on circuits, never an outcome-category weight; the profile is a read-out over
emergent activity. Directional/graded assertions only."""

import tokenize
import unittest

from substrate.model import load_substrate
from substrate.study import (throttled_newborn, punishment_learning, empathy_response,
                             cu_profile, AFFECTIVE_EMPATHY, COGNITIVE_MENTALIZING)
from substrate import study as study_module

_MODEL = load_substrate()


class TestPunishmentLearningDeficit(unittest.TestCase):
    def test_normal_newborn_learns_from_punishment(self):
        # an ordinary substrate acquires a defensive response to a cue paired with punishment
        learned = punishment_learning(throttled_newborn(0.0, model=_MODEL))
        self.assertGreater(learned, 0.0)

    def test_throttling_the_amygdala_impairs_punishment_learning(self):
        # the sharpest CU signature: a throttled affective system fails to learn from punishment
        normal = punishment_learning(throttled_newborn(0.0, model=_MODEL))
        throttled = punishment_learning(throttled_newborn(1.0, model=_MODEL))
        self.assertLess(throttled, normal)

    def test_deficit_is_graded_in_the_throttle(self):
        # a throttle, not a switch: more hypofunction -> less punishment learning
        full = punishment_learning(throttled_newborn(0.0, model=_MODEL))
        half = punishment_learning(throttled_newborn(0.5, model=_MODEL))
        none = punishment_learning(throttled_newborn(1.0, model=_MODEL))
        self.assertGreaterEqual(full, half)
        self.assertGreaterEqual(half, none)


class TestReadsButDoesntFeel(unittest.TestCase):
    def test_throttle_blunts_affect_while_sparing_cognition(self):
        # the psychopathy dissociation v8 was built to express: throttle the affective side,
        # the cognitive mentalizing network stays comparatively intact ("reads but doesn't feel")
        aff0, cog0 = empathy_response(throttled_newborn(0.0, model=_MODEL))
        aff1, cog1 = empathy_response(throttled_newborn(1.0, model=_MODEL))
        # affective empathy collapses far more than cognitive mentalizing
        self.assertLess(aff1, aff0)
        aff_drop = (aff0 - aff1) / (aff0 + 1e-9)
        cog_drop = (cog0 - cog1) / (cog0 + 1e-9)
        self.assertGreater(aff_drop, cog_drop)

    def test_dissociation_index_rises_with_throttle(self):
        # affective-minus-cognitive falls as the throttle silences the felt response
        low = cu_profile(0.0, model=_MODEL)["affective_minus_cognitive"]
        high = cu_profile(1.0, model=_MODEL)["affective_minus_cognitive"]
        self.assertGreater(low, high)


class TestHonestyLine(unittest.TestCase):
    def test_throttle_set_is_anatomy_not_outcome_category(self):
        # the manipulation targets circuit ids (anatomy), never an outcome-category weight
        for cid in AFFECTIVE_EMPATHY + COGNITIVE_MENTALIZING:
            self.assertIn(cid, _MODEL.circuits)

    def test_study_codes_no_outcome_category(self):
        # source-level: no callousness/psychopathy/aggression token appears as a code name;
        # the profile is measured, not defined by a seeded category.
        with open(study_module.__file__, "rb") as fh:
            names = {t.string.lower() for t in tokenize.tokenize(fh.readline)
                     if t.type == tokenize.NAME}
        for banned in ("callousness", "psychopath", "sophropath", "callous_high",
                       "aggression", "meanness"):
            self.assertNotIn(banned, names)

    def test_cu_profile_is_all_readouts(self):
        prof = cu_profile(0.5, model=_MODEL)
        for key in ("punishment_learning", "affective_empathy", "cognitive_mentalizing",
                    "affective_minus_cognitive"):
            self.assertIn(key, prof)


if __name__ == "__main__":
    unittest.main()

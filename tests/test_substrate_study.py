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


class TestPunishmentLearning(unittest.TestCase):
    def test_normal_newborn_acquires_some_aversion(self):
        # an ordinary substrate acquires a (small) defensive response to a punished cue
        learned = punishment_learning(throttled_newborn(0.0, model=_MODEL))
        self.assertGreater(learned, -0.05)

    def test_punishment_deficit_is_not_robust_under_correct_plasticity(self):
        # HONEST FINDING (Part 5): under the experience-decreasing plasticity (S10.1) the
        # graded punishment-learning DEFICIT does NOT robustly emerge -- it is weak and
        # non-monotonic in the throttle (0%~0.02, 50%~0.02, 100%~0.03), i.e. it was partly an
        # artifact of the earlier (non-experience-decreasing) plasticity. We assert the
        # non-robustness honestly rather than a deficit that is not there. The robust CU
        # signature is the dissociation (below), not this.
        vals = [punishment_learning(throttled_newborn(t, model=_MODEL))
                for t in (0.0, 0.5, 1.0)]
        monotone_deficit = vals[0] >= vals[1] >= vals[2]
        self.assertFalse(monotone_deficit, f"unexpected clean deficit: {vals}")


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

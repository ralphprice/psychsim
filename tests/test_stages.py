import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

import unittest

from sophropathy import (parent_to_environment, typical_child_seed,
                        fearless_child_seed, normal_parent_seed, PARENT_SEEDS,
                        FAMILY_ENVIRONMENTS, run_stage1, run_stage2, run_stage3,
                        run_stage4, run_stage5, run_stage6, run_stage7)
from affective_engine import sophropathic_seed, psychopathic_seed


def _modal(conds, needle):
    for c in conds:
        if needle in c.label:
            return c.modal
    raise AssertionError(f"no condition matching {needle}")


class TestSociety(unittest.TestCase):
    def test_parent_disposition_shapes_environment(self):
        soph = parent_to_environment(sophropathic_seed())
        psych = parent_to_environment(psychopathic_seed())
        # sophropathic parent -> warm & structured; psychopathic -> harsh & chaotic
        self.assertGreater(soph.warmth, 0.5)
        self.assertGreater(soph.structure, 0.5)
        self.assertLess(psych.warmth, 0.5)
        self.assertLess(psych.structure, 0.5)

    def test_child_seeds_differ_in_fear(self):
        t, f = typical_child_seed(), fearless_child_seed()
        self.assertGreater(t.gains["THREAT"], f.gains["THREAT"])   # typical has intact fear


class TestStagesRun(unittest.TestCase):
    def test_stage1_and_2_build_societies(self):
        s1, s2 = run_stage1(), run_stage2()
        self.assertGreater(len(s1.society.families), 0)
        # imbalance lowers mean warmth vs the perfect condition
        self.assertLess(s2.society.environment_profile()["mean_warmth"],
                        s1.society.environment_profile()["mean_warmth"])

    def test_stages3_and_4_report_emergent_profiles(self):
        # at this crude stage we do NOT assert a decreed environment->outcome order;
        # we check each condition reports a well-formed emergent readout
        from substrate.readout import _READOUT_DOMAINS as _DOMAINS
        valid = set(_DOMAINS)
        for stage in (run_stage3(n=8), run_stage4(n=8)):
            for c in stage.conditions:
                self.assertIn(c.modal, valid)                     # dominant system
                self.assertAlmostEqual(sum(c.mean_profile.values()), 1.0, places=4)
                self.assertTrue(-1.0 <= c.mean_axis <= 1.0)

    def test_stage5_has_placeholder_calibration_flag(self):
        s5 = run_stage5(n=6)
        self.assertTrue(any("PLACEHOLDER" in n for n in s5.notes))

    def test_stages6_and_7_run_and_report_profiles(self):
        from substrate.readout import _READOUT_DOMAINS as _DOMAINS
        valid = set(_DOMAINS)
        for stage in (run_stage6(n=8), run_stage7(n=8)):
            self.assertTrue(stage.conditions)
            for c in stage.conditions:
                self.assertIn(c.modal, valid)


class TestDeterminism(unittest.TestCase):
    def test_reproducible(self):
        a = run_stage4(n=6); b = run_stage4(n=6)
        self.assertEqual([c.distribution for c in a.conditions],
                         [c.distribution for c in b.conditions])


if __name__ == "__main__":
    unittest.main(verbosity=2)

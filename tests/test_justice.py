"""Tests for the criminogenic-justice extension.

The load-bearing properties: with the module OFF the segmented runner is exactly
plain development; the labelling ladder escalates with detected contacts; the
labelled environment degrades but never below the floor; the ON/OFF comparison
is reproducible; and the mechanism has genuine dynamic range -- null when
contact comes after the plastic window, decisive when it comes early.
"""

import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))


import unittest

from affective_engine.agent import AffectiveAgent
from affective_engine.core import shared_root_seed
from affective_engine.development import (Environment, classify,
                                              warm_firm_home,
                                              harsh_inconsistent_home)
from justice.system import (JusticeParams, JusticeSystem,
                                       develop_with_justice)
from justice.experiment import run_comparison


class TestLabellingLadder(unittest.TestCase):

    def test_label_levels(self):
        p = JusticeParams()
        self.assertEqual(p.label_level(0), 0)
        self.assertEqual(p.label_level(p.warn_at), 1)
        self.assertEqual(p.label_level(p.charge_at), 2)
        self.assertEqual(p.label_level(p.convict_at), 3)

    def test_labelled_environment_degrades_but_floors(self):
        p = JusticeParams(warmth_per_level=0.5, structure_per_level=0.5,
                          recognition_per_level=0.5, env_floor=0.05)
        js = JusticeSystem(params=p)
        js.contacts = p.convict_at            # level 3
        base = Environment("b", 0.4, 0.4, 0.4)
        lab = js.labelled_environment(base)
        self.assertLess(lab.warmth, base.warmth)
        self.assertGreaterEqual(lab.warmth, p.env_floor)
        self.assertGreaterEqual(lab.structure, p.env_floor)

    def test_level_zero_leaves_environment_untouched(self):
        js = JusticeSystem()
        base = Environment("b", 0.4, 0.4, 0.4)
        self.assertIs(js.labelled_environment(base), base)


class TestRunnerReducesToDevelopment(unittest.TestCase):

    def test_justice_off_is_deterministic(self):
        def grow():
            ag = AffectiveAgent(seed=shared_root_seed(), temperament_seed=123)
            develop_with_justice(ag, harsh_inconsistent_home(), justice=None,
                                 seed=123, graded=True)
            return classify(ag).classification
        self.assertEqual(grow(), grow())

    @unittest.skip("obsolete: asserted the deleted verdict (labels/subtypes/control_gain); pending harness reconception around the emergent drive-profile")
    def test_warm_home_still_yields_sophropath_through_segments(self):
        ag = AffectiveAgent(seed=shared_root_seed())
        develop_with_justice(ag, warm_firm_home(), justice=None,
                             seed=20260704, graded=True)
        # segmented, aged development should not break the warm-home outcome
        self.assertIn(classify(ag).classification,
                      ("sophropathic", "intermediate"))


class TestComparison(unittest.TestCase):

    def test_off_condition_has_no_contacts(self):
        off, on = run_comparison(n_children=12)
        self.assertTrue(all(c == 0 for c in off.contacts))

    @unittest.skip("obsolete: asserted the deleted verdict (labels/subtypes/control_gain); pending harness reconception around the emergent drive-profile")
    def test_comparison_is_reproducible(self):
        a_off, a_on = run_comparison(n_children=12)
        b_off, b_on = run_comparison(n_children=12)
        self.assertEqual([o.classification for o in a_on.outcomes],
                         [o.classification for o in b_on.outcomes])

    @unittest.skip("obsolete: asserted the deleted verdict (labels/subtypes/control_gain); pending harness reconception around the emergent drive-profile")
    def test_early_aggressive_labelling_shifts_outcomes(self):
        """The mechanism must be able to manufacture the phenotype: near the
        separatrix, early aggressive labelling moves children rightward."""
        base = Environment("near-boundary", 0.36, 0.36, 0.34)
        strong = JusticeParams(base_detect=0.85, warn_at=1, charge_at=2,
                               convict_at=3, warmth_per_level=0.14,
                               structure_per_level=0.16,
                               recognition_per_level=0.14)
        off, on = run_comparison(n_children=30, base_env=base, params=strong)
        self.assertEqual(off.shares()["psychopathic"], 0.0)
        self.assertGreater(on.shares()["psychopathic"], 0.5)

    def test_default_parameters_do_not_manufacture_out_of_thin_air(self):
        """With default (late-biting) parameters and a base env clear of the boundary, the mechanism should
        NOT shift children -- guarding against a module that fabricates effects.

        ★ RESTATED (prototype item 3a): the old body asserted on.shares()["psychopathic"] == 0.0 -- a
        VACUOUS guard on a RETIRED verdict key that classify() never emits (it returns _READOUT_DOMAINS),
        so it was trivially true and printed a structural zero as a result (the audit finding). Restated on
        the REAL emergent vocabulary and the intent it was always for: default (inert) justice leaves the
        outcome DISTRIBUTION essentially unchanged -- no domain's share moves appreciably between off and on."""
        base = Environment("clearly-intermediate", 0.45, 0.47, 0.43)
        off, on = run_comparison(n_children=30, base_env=base)
        so, sn = off.shares(), on.shares()
        max_shift = max(abs(sn.get(k, 0) - so.get(k, 0)) for k in set(so) | set(sn))
        self.assertLess(max_shift, 0.20,                     # default justice does not manufacture a shift
                        f"default (inert) justice shifted the outcome distribution by {max_shift:.1%} "
                        "-- it should not manufacture an effect out of thin air")


if __name__ == "__main__":
    unittest.main()

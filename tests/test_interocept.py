import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""Phase 1 (PsychSim_MASTER) -- the valence core. Value is COMPUTED as drive reduction over
an interoceptive state vector, never stipulated. Assertions are directional/structural
(signs, orderings, which variable moved) -- magnitudes are scaffold."""

import unittest

from affective_engine.interocept import (StateVector, newborn_state,
                                          reference_child_state, apply_event,
                                          valence, valence_of_event, VARIABLES)
from affective_engine import params
from affective_engine.development import (warm_firm_home, harsh_inconsistent_home)


class TestDrive(unittest.TestCase):
    def test_newborn_at_setpoints_has_zero_drive(self):
        _, D = newborn_state().drive()
        self.assertAlmostEqual(D, 0.0, places=6)

    def test_deficit_raises_drive(self):
        s = newborn_state()
        s.levels["attachment"] = s.set_points["attachment"] - 0.4  # below set-point
        per, D = s.drive()
        self.assertGreater(D, 0.0)
        self.assertGreater(per["attachment"], 0.0)

    def test_reference_child_has_standing_deficits(self):
        self.assertGreater(reference_child_state().scalar_drive(), 0.0)

    def test_drive_is_vector_and_scalar(self):
        per, D = reference_child_state().drive()
        self.assertEqual(set(per.keys()), set(VARIABLES))
        self.assertAlmostEqual(sum(per.values()), D, places=6)


class TestPerturbationsAndValence(unittest.TestCase):
    def test_valence_is_drive_reduction(self):
        self.assertGreater(valence(1.0, 0.4), 0.0)   # drive fell -> positive
        self.assertLess(valence(0.4, 1.0), 0.0)      # drive rose -> negative
        self.assertAlmostEqual(valence(0.5, 0.5), 0.0)

    def test_soothing_relieves_a_distressed_child(self):
        # a lonely, aroused child: contact/soothing should reduce drive (positive valence)
        r, _, red = valence_of_event(reference_child_state(),
                                     {"affiliative_touch": 1.0, "soothing": 1.0})
        self.assertGreater(r, 0.0)
        self.assertGreater(red["attachment"], 0.0)   # attachment deficit reduced
        self.assertGreater(red["arousal"], 0.0)      # arousal deviation reduced

    def test_separation_is_aversive(self):
        r, _, red = valence_of_event(reference_child_state(), {"separation": 1.0})
        self.assertLess(r, 0.0)
        self.assertLess(red["attachment"], 0.0)      # attachment deficit deepened

    def test_perturbation_moves_the_named_variable_only(self):
        s = newborn_state()
        after = apply_event(s, {"drinking": 1.0})
        self.assertGreater(after.levels["hydration"], s.levels["hydration"])
        self.assertEqual(after.levels["attachment"], s.levels["attachment"])

    def test_unknown_trigger_carries_no_innate_value(self):
        # a neutral cue is not innately valued (it must be LEARNED -- Phase 2)
        r, _, _ = valence_of_event(reference_child_state(), {"a_particular_face": 1.0})
        self.assertAlmostEqual(r, 0.0, places=6)


class TestPunishmentForOneRewardForAnother(unittest.TestCase):
    def test_same_event_opposite_value_across_endowment(self):
        # the honesty-critical consequence: identical external event, different valence
        # for agents whose endowment (need weights) differs. A touch-averse, low-affiliation
        # agent gains far less social relief from the same affiliative contact.
        affiliative = reference_child_state()
        avoidant = reference_child_state()
        avoidant.weights["attachment"] = 0.05      # affiliation barely matters to this one
        avoidant.weights["belonging"] = 0.05
        r_aff, _, _ = valence_of_event(affiliative, {"affiliative_touch": 1.0,
                                                     "contact_caregiver": 1.0})
        r_avd, _, _ = valence_of_event(avoidant, {"affiliative_touch": 1.0,
                                                  "contact_caregiver": 1.0})
        self.assertGreater(r_aff, r_avd)


class TestEnvironmentValenceComputed(unittest.TestCase):
    def test_warm_positive_harsh_negative_ordering(self):
        # parity with the old qualitative behaviour: sign + ordering preserved, exact
        # numbers differ (now computed, not stipulated clamp(2*warmth-1)).
        warm = warm_firm_home().response_valence()
        harsh = harsh_inconsistent_home().response_valence()
        self.assertGreater(warm, 0.0)
        self.assertLess(harsh, 0.0)
        self.assertGreater(warm, harsh)

    def test_no_stipulated_constant_in_environment(self):
        # response_valence must route through the computed engine, not a hand-set number.
        import inspect
        from affective_engine.development import Environment
        src = inspect.getsource(Environment.response_valence)
        self.assertIn("valence_of_event", src)
        self.assertNotIn("2.0 * self.warmth", src)


class TestScaffoldMarked(unittest.TestCase):
    def test_params_are_marked_scaffold(self):
        import inspect
        src = inspect.getsource(params)
        self.assertIn("SCAFFOLD", src)
        self.assertGreaterEqual(src.count("SCAFFOLD"), 10)


if __name__ == "__main__":
    unittest.main()

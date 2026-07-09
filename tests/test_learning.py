import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""Phase 2 (PsychSim_MASTER) -- RPE learning + anticipatory value + three-factor plasticity.
Directional/convergence assertions only; rates are scaffold."""

import random
import unittest

from affective_engine.learning import (ValueLearner, three_factor, prepared_multiplier)
from affective_engine import params


class TestRPEConvergence(unittest.TestCase):
    def test_value_converges_to_reward(self):
        # repeatedly presenting a terminal cue with fixed reward -> V -> r
        vl = ValueLearner()
        for _ in range(80):
            vl.update("cue", r=0.5, next_value=0.0)
        self.assertAlmostEqual(vl.value_of("cue"), 0.5, places=2)

    def test_positive_reward_gives_positive_anticipatory_value(self):
        vl = ValueLearner()
        for _ in range(10):
            vl.update("friend", r=0.4)
        self.assertGreater(vl.value_of("friend"), 0.0)

    def test_aversive_reward_gives_negative_value(self):
        vl = ValueLearner()
        for _ in range(10):
            vl.update("bully", r=-0.4)
        self.assertLess(vl.value_of("bully"), 0.0)

    def test_rpe_sign(self):
        vl = ValueLearner()
        self.assertGreater(vl.rpe("x", r=0.5), 0.0)          # better than a 0 prior
        vl.update("x", r=0.5)
        # once value has risen, the same reward is less surprising
        self.assertLess(vl.rpe("x", r=0.5), 0.5)


class TestPreparedLearning(unittest.TestCase):
    def test_prepared_cue_acquires_fear_faster(self):
        # §B.3: a snake is not innately aversive, but aversive value is learned FAST.
        # Same aversive reward, same trials -> the prepared cue reaches a larger aversion.
        vl = ValueLearner()
        for _ in range(3):
            vl.update("a snake in the grass", r=-0.3)
            vl.update("a blue arbitrary cue", r=-0.3)
        self.assertLess(vl.value_of("a snake in the grass"),
                        vl.value_of("a blue arbitrary cue"))

    def test_prepared_multiplier_defaults_to_one(self):
        self.assertEqual(prepared_multiplier("an ordinary teapot"), 1.0)
        self.assertGreater(prepared_multiplier("SNAKE"), 1.0)


class TestAsymmetries(unittest.TestCase):
    def test_aversive_learning_faster_than_appetitive(self):
        va, vp = ValueLearner(), ValueLearner()
        va.update("x", r=-0.5)   # one aversive trial
        vp.update("y", r=+0.5)   # one appetitive trial
        self.assertGreater(abs(va.value_of("x")), abs(vp.value_of("y")))

    def test_extinction_slower_than_acquisition(self):
        # acquire an aversion, then present neutral/positive outcomes; it decays back to 0
        # more slowly than a fresh cue would acquire the same magnitude.
        vl = ValueLearner()
        for _ in range(6):
            vl.update("dog", r=-0.4)
        aversion = vl.value_of("dog")
        vl.update("dog", r=+0.4)             # extinction trial (better than expected)
        moved = vl.value_of("dog") - aversion
        # a fresh cue acquiring positive value in one trial moves further than extinction does
        fresh = ValueLearner()
        fresh.update("newdog", r=+0.4)
        self.assertLess(moved, fresh.value_of("newdog"))


class TestGatesAndProfile(unittest.TestCase):
    def test_closed_gate_licenses_no_plasticity(self):
        vl = ValueLearner()
        vl.update("social_cue", r=0.5, gate=0.0)   # oxytocin/opioid gate shut
        self.assertEqual(vl.value_of("social_cue"), 0.0)

    def test_learns_drive_reduction_profile(self):
        vl = ValueLearner()
        for _ in range(20):
            vl.update("blanket", r=0.3, drive_profile={"thermal": 0.5, "arousal": 0.2})
        prof = vl.profile_of("blanket")
        self.assertGreater(prof.get("thermal", 0.0), 0.0)
        self.assertGreater(prof["thermal"], prof.get("arousal", 0.0))

    def test_anticipated_value_is_state_dependent(self):
        # a food cue is worth more when the matching drive is high than when it is zero
        vl = ValueLearner()
        for _ in range(20):
            vl.update("food_cue", r=0.4, drive_profile={"energy": 0.6})
        hungry = vl.anticipated("food_cue", {"energy": 1.0})
        sated = vl.anticipated("food_cue", {"energy": 0.0})
        self.assertGreater(hungry, sated)


class TestThreeFactor(unittest.TestCase):
    def test_meaning_blind_multiplicative(self):
        self.assertGreater(three_factor(1.0, 1.0, 1.0), 0.0)
        self.assertEqual(three_factor(1.0, 1.0, 0.0), 0.0)     # no neuromodulator -> no change
        self.assertEqual(three_factor(1.0, 0.0, 1.0), 0.0)     # no post-activity -> no change
        self.assertEqual(three_factor(1.0, 1.0, 1.0, window=0.0), 0.0)  # window shut -> no change
        # a negative neuromodulator (worse than expected) weakens
        self.assertLess(three_factor(1.0, 1.0, -1.0), 0.0)

    def test_signature_carries_no_semantic_argument(self):
        import inspect
        argnames = set(inspect.signature(three_factor).parameters)
        self.assertEqual(argnames, {"pre", "post", "neuromod", "window", "lr"})


# NOTE: the former TestImprintParity (Panksepp Brain.imprint strengthening) was removed with the
# Panksepp drive-engine in Part 6 step 3e / stage 5. The substrate's own use-dependent
# strengthening (the BCM/three-factor plasticity in the settle loop) is covered by
# test_substrate_learning.py; the three_factor rule itself is tested above.


if __name__ == "__main__":
    unittest.main()

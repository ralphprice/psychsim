import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""8b divergence arm (PsychSim_MASTER Part 4 S7) -- executive-control development arm + 2x2.

HONEST RESULT: the arm is built to the S7.3 honesty line (environments are perturbation
patterns; no code maps an environment to an outcome) and the environment differentially
engages the executive EMERGENTLY. But the differential-susceptibility INTERACTION is
KNIFE-EDGE -- it flips sign across the arbitrary development duration -- so per Part IV it is
flagged as NON-ROBUST, NOT reported as the divergence finding. These tests assert exactly that
honest state; they do NOT assert the interaction (that would be cherry-picking one tuning)."""

import tokenize
import unittest

from substrate.model import load_substrate
from substrate.engine import SubstrateEngine
from substrate.divergence import (ENVIRONMENTS, EXECUTIVE, interaction_at,
                                  interaction_across_durations)
from substrate import divergence as divergence_module

_MODEL = load_substrate()


class TestArmHonestyLine(unittest.TestCase):
    def test_environments_are_pure_perturbation_patterns(self):
        # every environment value is a sensory/social input CHANNEL, never an outcome
        for env in ENVIRONMENTS.values():
            for key in env:
                self.assertTrue(key.startswith("IN-"), f"{key} is not a sensory input channel")

    def test_no_environment_to_outcome_mapping_in_code(self):
        # S7.3 acceptance: no code name maps an environment to an outcome/control target
        with open(divergence_module.__file__, "rb") as fh:
            names = {t.string.lower() for t in tokenize.tokenize(fh.readline)
                     if t.type == tokenize.NAME}
        for banned in ("sophropath", "psychopath", "callous", "control_target",
                       "adaptive", "antisocial", "disinhibition"):
            self.assertNotIn(banned, names)


class TestCausalChainIsEmergent(unittest.TestCase):
    def test_environment_differentially_engages_the_executive(self):
        # S7.3 step 2, emergent: the warm (reward-containing) environment drives the executive
        # circuits more than the harsh one, via the substrate's own reward->PFC wiring.
        def engage(env):
            e = SubstrateEngine(_MODEL, age_years=8.0)
            e.clear_inputs()
            for k, v in env.items():
                e.inject_channel(k, v)
            e.settle(40)
            return sum(e.activity(c) for c in EXECUTIVE) / len(EXECUTIVE)
        self.assertGreater(engage(ENVIRONMENTS["warm_firm"]),
                           engage(ENVIRONMENTS["harsh_inconsistent"]))


class TestDivergenceIsKnifeEdge(unittest.TestCase):
    def test_interaction_sign_is_not_stable_across_development_duration(self):
        # the honest finding: the interaction flips sign with an arbitrary scaffold parameter
        # (development duration) -> knife-edge -> NOT a robust divergence (Part IV). We assert
        # the NON-robustness, not the interaction.
        vals = interaction_across_durations(_MODEL, durations=(350, 500))
        signs = {v > 0 for v in vals.values()}
        self.assertEqual(len(signs), 2, f"expected sign flip (knife-edge); got {vals}")

    def test_deterministic_at_a_fixed_duration(self):
        # the substrate has no RNG: at a FIXED duration the result is reproducible (so the
        # instability is the dynamics, not randomness)
        self.assertAlmostEqual(interaction_at(_MODEL, 400), interaction_at(_MODEL, 400),
                               places=6)


if __name__ == "__main__":
    unittest.main()

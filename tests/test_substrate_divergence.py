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
                                  interaction_across_durations, divergence_2x2,
                                  _cell_full)
from substrate import divergence as divergence_module

_MODEL = load_substrate()


class TestArmHonestyLine(unittest.TestCase):
    def test_environments_are_pure_perturbation_patterns(self):
        # every environment value is a sensory/social input CHANNEL, never an outcome
        for env in ENVIRONMENTS.values():
            for key in env:
                self.assertTrue(key.startswith("IN-"), f"{key} is not a sensory input channel")

    def test_no_environment_to_outcome_mapping_in_code(self):
        # S7.3 acceptance: no code name maps an environment to an outcome/control target; and the
        # self-reflection routing smuggles in no coded self-verdict (conscience/remorse/...).
        with open(divergence_module.__file__, "rb") as fh:
            names = {t.string.lower() for t in tokenize.tokenize(fh.readline)
                     if t.type == tokenize.NAME}
        for banned in ("sophropath", "psychopath", "callous", "control_target",
                       "adaptive", "antisocial", "disinhibition",
                       "conscience", "remorse", "prosocial", "moral", "guilt"):
            self.assertNotIn(banned, names)

    def test_self_reflection_valence_is_read_from_circuits_not_environment(self):
        # the honesty crux of routing self-reflection in: `_self_signals` must read the
        # substrate's OWN circuit activity, never the environment dict. Same warmed engine +
        # two different (unused) "environment" labels -> identical self-signals, because the
        # environment is never consulted by the read-out.
        from substrate.divergence import _self_signals
        from substrate.study import throttled_newborn, AFFECTIVE_EMPATHY
        eng = throttled_newborn(0.0, AFFECTIVE_EMPATHY, model=_MODEL)
        for k, v in ENVIRONMENTS["warm_firm"].items():
            eng.inject_channel(k, v)
        eng.settle(5)
        r1, a1, t1 = _self_signals(eng)
        r2, a2, t2 = _self_signals(eng)     # a pure read-out: repeatable, side-effect free
        self.assertEqual((r1, a1, t1), (r2, a2, t2))
        self.assertTrue(-1.0 <= r1 <= 1.0 and 0.0 <= a1 <= 1.0 and 0.0 <= t1 <= 1.0)


class TestCausalChainIsEmergent(unittest.TestCase):
    @unittest.expectedFailure
    def test_environment_differentially_engages_the_executive(self):
        # ENGAGEMENT vs CAPACITY -- the substrate is right and this ASSERTION is wrong (v14
        # Expression Phase B+, ruled). The test asserts warm > harsh, on the premise that the
        # reward-containing environment engages the executive MORE. The substrate says the
        # opposite, and CORRECTLY: a harsh, unpredictable environment produces more conflict ->
        # more dACC conflict/error MONITORING -> more control RECRUITMENT via the grounded
        # dACC->dlPFC edge (Botvinick's conflict-monitoring model; the edge is in the seed). So
        # `warm < harsh` for ENGAGEMENT is the right emergent answer. Confirmed after dACC-GABA:
        # even control-only (dlPFC+OFC, dropping dACC) stays warm<harsh, because dACC recruits
        # dlPFC -- so re-expressing the READ-OUT SET cannot fix it; the set is not the error.
        #
        # The test wants CAPACITY (does adversity LOWER the control an agent can exert?). Capacity
        # is a DIFFERENT CONSTRUCT, not a small variant of engagement, and NO measure of it exists.
        # A passive read-out of executive ACTIVATION can never separate capacity from demand -- it
        # conflates them by construction, whatever set it sums. The literature expects BOTH
        # (adversity RAISES engagement AND LOWERS capacity); we now measure the first honestly and
        # the second not at all.
        #
        # RESOLUTION CONDITION (xfail clears -> unexpected success -> suite RED -> revisit): build
        # a CAPACITY measure probed at MATCHED DEMAND (same challenge to warm- and harsh-reared
        # agents, measure the control exerted), and assert on THAT. Do NOT satisfy this by inverting
        # to harsh>warm -- that manufactures the opposite finding. See gaps-register S19 (read-out
        # audit) + the capacity-at-matched-demand pass.
        def engage(env):
            e = SubstrateEngine(_MODEL, age_years=8.0)
            e.clear_inputs()
            for k, v in env.items():
                e.inject_channel(k, v)
            e.settle(40)
            return sum(e.activity(c) for c in EXECUTIVE) / len(EXECUTIVE)
        self.assertGreater(engage(ENVIRONMENTS["warm_firm"]),
                           engage(ENVIRONMENTS["harsh_inconsistent"]))


class TestRegimeBStability(unittest.TestCase):
    """S9.3 Regime B correctness property: normal (un-throttled) development must not
    destabilise a viable person. With the experience-decreasing plasticity (S10.1), the
    developed state SETTLES on its own -- no bolted-on stabiliser (S9.1)."""

    def test_un_throttled_development_settles(self):
        from substrate.divergence import _cell, ENVIRONMENTS
        W = ENVIRONMENTS["warm_firm"]
        early = _cell(0.0, W, _MODEL, ticks=400)
        late = _cell(0.0, W, _MODEL, ticks=800)
        # the developed state converges (small change over a long extra span), not oscillates
        self.assertLess(abs(late - early), 0.1)


class TestDivergenceWellPosedAndNear_Zero(unittest.TestCase):
    def test_interaction_is_stable_across_durations(self):
        # now development settles, the interaction is well-posed: stable sign + magnitude
        vals = interaction_across_durations(_MODEL, durations=(350, 500, 600))
        signs = {v > 0 for v in vals.values()}
        self.assertEqual(len(signs), 1, f"expected a stable sign (well-posed); got {vals}")
        self.assertLess(max(vals.values()) - min(vals.values()), 0.05)

    @unittest.expectedFailure
    def test_divergence_does_not_robustly_emerge(self):
        # THE EARNED NEGATIVE -- HELD, NOT RETIRED (v14 Expression Phase B+, ruled). It reads
        # 0.0534 (was 0.0755 before dACC-GABA; the grounded brake removed 29%). The margin over the
        # 0.05 near-zero line is 7%. That 7% sits INSIDE two unquantified sources of error, BOTH of
        # which point UPWARD (gaps-register S18): (1) EIGHT more cortical brakes are still absent --
        # the layer is 3 of 11; (2) THIS brake's own strength is SCAFFOLD (baseline 0.05 / setpoint
        # 0.1, unpaired, like its E-I twins), so the 29% it removed is itself a scaffold quantity.
        # ONE brake removed FOUR TIMES the current margin. We therefore CANNOT yet tell whether the
        # divergence emerges, and the direction of the unknown is known (downward, as brakes land).
        # Do NOT move the threshold. Do NOT retire the finding by attrition. What this now IS: a
        # small, stable, well-posed structural value (0.0534) that emerged from a grounded edge and
        # survived a grounded brake -- test_interaction_is_stable_across_durations passes, so it is
        # NOT a saturation artifact. It may be real; it is not yet a finding.
        #
        # RESOLUTION CONDITION (xfail clears -> unexpected success -> suite RED -> re-measure): when
        # the cortical brake layer is COMPLETE (all 11 nodes braked; S18), re-run this. If it then
        # sits below 0.05 the earned negative holds on a grounded substrate; if it stays above, the
        # divergence is a real finding earned honestly. Not before.
        self.assertLess(abs(interaction_at(_MODEL, 500)), 0.05)


class TestSelfReflectionRoutedIntoOutcome(unittest.TestCase):
    """Part 5 S10.2 + the review ruling: self-reflection is now wired into development and the
    outcome (meaning-blind read-out of the substrate's own valence). The 2x2 is re-run on this
    second outcome channel. HONEST RESULT: it opens a rich channel but does NOT make the
    differential-susceptibility divergence emerge -- the earned negative now holds across two
    independent outcomes."""

    def test_self_reflection_does_not_perturb_the_substrate(self):
        # the self channel is a pure read-out during development: exec is byte-identical whether
        # or not reflection is present, so it cannot secretly steer the behavioural outcome.
        W = ENVIRONMENTS["warm_firm"]
        with_refl = _cell_full(0.0, W, _MODEL, ticks=400)["exec"]
        # develop() without a reflection matrix (reflection=None) must give the same exec value
        from substrate.divergence import develop, developed_executive_control
        from substrate.study import throttled_newborn, AFFECTIVE_EMPATHY
        eng = throttled_newborn(0.0, AFFECTIVE_EMPATHY, model=_MODEL)
        develop(eng, W, ticks=400)   # reflection=None
        self.assertAlmostEqual(with_refl, developed_executive_control(eng), places=6)

    def test_self_regard_tracks_environment_emergently(self):
        # the self channel is alive: a warm childhood yields higher developed self-regard than a
        # harsh one -- a MAIN effect that emerges through the substrate's own valence (reward vs
        # threat circuits), never coded from the environment.
        d = divergence_2x2(_MODEL, outcome="self_regard")
        self.assertGreater(d["intact_warm"], d["intact_harsh"])
        self.assertGreater(d["throttled_warm"], d["throttled_harsh"])

    def test_self_regard_interaction_is_well_posed_and_not_diff_susceptibility(self):
        # well-posed (sign-stable across durations) AND the interaction is negative -- the
        # throttled child's self-regard swings LESS, the opposite of differential susceptibility.
        # So the divergence does not emerge in the self channel either (earned negative).
        vals = interaction_across_durations(_MODEL, durations=(350, 500, 600),
                                            outcome="self_regard")
        self.assertTrue(all(v < 0 for v in vals.values()), f"expected stable negative: {vals}")
        self.assertLess(max(vals.values()) - min(vals.values()), 0.05)   # stable magnitude


if __name__ == "__main__":
    unittest.main()

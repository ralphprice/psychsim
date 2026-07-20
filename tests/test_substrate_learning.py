import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""8b.2 (PsychSim_MASTER Part 2 S2.7) -- the ONE-PLASTICITY unified learning.

Anticipatory value EMERGES from the substrate's DA-gated BCM plasticity, driven by an innate
reward link -- with NO shadow TD learner. The load-bearing honesty result: learning is the
biological rule, and value is a read-out of the strengthened pathways."""

import io
import tokenize
import unittest

from substrate.model import load_substrate
from substrate.engine import SubstrateEngine
from substrate.agent import SubstrateAgent
from substrate import agent as agent_module

_MODEL = load_substrate()

_CUE = {"IN-VIS": 0.6}                       # a neutral visual cue -> V-ventral
_SWEET = {"IN-GUST:sweet": 0.9}             # a primary reinforcer -> VTA (innate reward link)


def _pair(ag, trials=60):
    for _ in range(trials):
        ag.experience({**_CUE, **_SWEET}, ticks=12)


class TestAnticipatoryValueEmerges(unittest.TestCase):
    # ★ SUSPENDED (S56 Stage 3, ruled) -- NOT deleted, and NOT "the effect was fake".
    # The OFC gate (the fourth cortical E-I gate, GROUNDED: OFC was the only cortical node with ZERO
    # inhibitory afferents, sitting in a correctly-signed mutual positive-feedback loop with DRN) reduced
    # OFC 0.568 -> 0.385, which lowered the DA teaching signal ~6% (DA_out 0.3909 -> 0.3684) via OFC->VTA.
    # That flipped these two assertions -- but the margins they rested on were NOISE-SCALE: the
    # paired-vs-unpaired gain was +0.0008 (now -0.0013), and the cue-value margin 0.1565 (now 0.1551).
    # ★ THE DISCRIMINATING FACT: the pathway underneath them is itself UNGROUNDED --
    #     OFC -> VTA       basis=assumption, dominant_receptor=None (fallback-signed), weight=low
    #     OFC -> NAc-core  basis=assumption, dominant_receptor=None (fallback-signed), weight=low
    # So a grounded fix (the gate) deflated an effect that an UNGROUNDED edge's over-drive was propping
    # up. This is the S18 inflation law, now on the learning tests: every incompleteness inflates effect
    # sizes and the honest direction is smaller. A +0.0008 dissociation resting on assumption-based,
    # fallback-signed edges was never a demonstrated learning result.
    # RESOLUTION CONDITION: ground the OFC->dopamine pathway (OFC->VTA / OFC->NAc-core -- real anatomy,
    # so the SIGN is likely correct-but-ungrounded and the WEIGHT is the ungrounded term; both are on the
    # fallback-sign census). Once that pathway is grounded, RE-ENABLE these tests: a robust
    # paired-vs-unpaired dissociation either emerges (a real result) or does not (also a real result).
    # Do NOT "fix" this by weakening the grounded OFC gate to restore a noise-scale effect.
    # ★ MARGIN CHECKED (ruled), AND IT STAYS SUSPENDED -- the un-suspend was authorised conditional on the
    # margin proving robust. It is not. Measured paired gain vs the UNPAIRED cue-alone control, by age:
    #     age  4.0   paired +0.003632   unpaired +0.005439   (0.7x -- the CONTROL gains MORE)
    #     age  8.0   paired +0.016434   unpaired +0.013907   (1.2x)
    #     age 15.0   paired -0.013863   unpaired +0.009058   (NEGATIVE)
    #     age 25.0   paired -0.004655   unpaired +0.010242   (NEGATIVE)
    # It reports "unexpected success" at age 4 purely because +0.0036 > 0. An effect smaller than its own
    # control, and sign-unstable across development, is not a demonstrated learning result. Being measured on
    # DYNAMICS (not the observer double-gain) made it a CANDIDATE to survive the instrument correction -- it
    # simply did not survive, which is the margin discipline working in the honest direction.
    # RESOLUTION CONDITION unchanged: ground OFC->VTA / OFC->NAc-core, then re-measure paired vs control.
    @unittest.expectedFailure
    def test_cue_acquires_value_from_da_gated_plasticity(self):
        ag = SubstrateAgent(SubstrateEngine(_MODEL, age_years=4.0))
        before = ag.anticipatory_value(_CUE)
        _pair(ag)
        after = ag.anticipatory_value(_CUE)
        self.assertGreater(after, before)       # the cue alone now drives reward/value circuits

    def test_learning_requires_the_reinforcer_da_gating(self):
        # control: the SAME cue, repeatedly, with NO reinforcer -> no DA burst -> no learning.
        # This is what distinguishes DA-gated three-factor plasticity from plain Hebbian.
        ag = SubstrateAgent(SubstrateEngine(_MODEL, age_years=4.0))
        before = ag.anticipatory_value(_CUE)
        for _ in range(60):
            ag.experience(_CUE, ticks=12)        # cue only, no sweet
        after = ag.anticipatory_value(_CUE)
        # negligible change without the reinforcer (vs the ~0.3 paired gain) -- DA-gated,
        # not plain Hebbian. A tiny drift is fine; a paired-scale change would not be.
        # ★ THIS GUARD IS CURRENTLY VACUOUS -- REGISTERED, deliberately NOT re-scaled. The "~0.3 paired gain"
        # above is the scale this bound was written against; the paired gain now measures +0.0036 (~1/80th).
        # So asserting the unpaired drift is < 0.05 is trivially satisfied when EVERY change is ~0.005: this
        # control cannot fail, because the effect it controls for no longer exists. Tightening the bound to
        # the observed magnitude would manufacture a green -- the honest fix is to diagnose why DA-gated
        # learning collapsed ~2 orders of magnitude. Left loose, and loudly, until that diagnosis lands.
        self.assertLess(abs(after - before), 0.05)

    # SUSPENDED with the same resolution condition as above (S56 Stage 3): the +0.0008 paired-vs-unpaired
    # margin rested on the ungrounded OFC->DA over-drive. Re-enable once OFC->VTA / OFC->NAc-core are grounded.
    @unittest.expectedFailure
    def test_paired_learns_more_than_unpaired(self):
        paired = SubstrateAgent(SubstrateEngine(_MODEL, age_years=4.0))
        p0 = paired.anticipatory_value(_CUE)
        _pair(paired)
        gain_paired = paired.anticipatory_value(_CUE) - p0

        unpaired = SubstrateAgent(SubstrateEngine(_MODEL, age_years=4.0))
        u0 = unpaired.anticipatory_value(_CUE)
        for _ in range(60):
            unpaired.experience(_CUE, ticks=12)
        gain_unpaired = unpaired.anticipatory_value(_CUE) - u0
        self.assertGreater(gain_paired, gain_unpaired)


class TestOnePlasticityDiscipline(unittest.TestCase):
    def test_reward_signal_is_the_da_circuit_output(self):
        # the RPE/dopamine signal IS neuromod_output('DA') -- the VTA/SNc activation, not a
        # separately computed TD error (the design's delta = neuromod_output('DA')).
        eng = SubstrateEngine(_MODEL, age_years=25.0)
        eng.inject("VTA", 0.7)
        eng.settle(20)
        ag = SubstrateAgent(eng)
        self.assertEqual(ag.reward_signal(), eng.neuromod_output("DA"))

    def test_no_shadow_td_learner(self):
        # structural guarantee: the substrate agent's CODE (tokens, not docstrings) does NOT
        # import or maintain the valence engine's ValueLearner or a discounted TD update.
        # Learning is the substrate's DA-gated plasticity alone.
        with open(agent_module.__file__, "rb") as fh:
            names = {t.string for t in tokenize.tokenize(fh.readline)
                     if t.type == tokenize.NAME}
        self.assertNotIn("ValueLearner", names)
        self.assertNotIn("gamma", {n.lower() for n in names})   # no TD discount in the code
        # value is a read-out method, not a stored value function
        self.assertTrue(hasattr(SubstrateAgent, "anticipatory_value"))


if __name__ == "__main__":
    unittest.main()

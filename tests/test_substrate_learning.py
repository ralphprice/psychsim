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
        self.assertLess(abs(after - before), 0.05)

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

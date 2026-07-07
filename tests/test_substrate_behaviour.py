import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""8b.3 (PsychSim_MASTER Part 2) -- behaviour selection over the LIVE substrate.

Behaviour EMERGES from basal-ganglia accumulation reading substrate activity (reward Go drive,
dopamine gain, executive/STN hold) -- no coded situation->behaviour arbiter. Asserts what
genuinely emerges; the adolescent-risk *bump* is documented as a mechanism gap (binary
developmental_online_age), NOT asserted -- per the discipline of surfacing, not forcing."""

import tokenize
import unittest

from substrate.model import load_substrate
from substrate.engine import SubstrateEngine
from substrate.behaviour import select_behaviour, go_drive, executive_hold
from substrate import behaviour as behaviour_module

_MODEL = load_substrate()


def _with_reward_cue(age):
    e = SubstrateEngine(_MODEL, age_years=age)
    e.inject_channel("IN-GUST:sweet", 0.8)
    e.settle(40)
    return e


class TestEmergentBehaviour(unittest.TestCase):
    def test_behaviour_emerges_from_substrate_activity(self):
        e = _with_reward_cue(25)
        b = select_behaviour(e)
        self.assertIn(b.action, ("approach", "restrain"))
        # a reward cue drives the reward circuits -> a positive Go drive -> the agent acts
        self.assertGreater(b.go, 0.0)
        self.assertEqual(b.action, "approach")

    def test_go_drive_scales_with_dopamine(self):
        e = _with_reward_cue(25)
        low = go_drive(e)
        e.inject("VTA", 0.9)                 # raise the dopamine gain (SNc/VTA output)
        e.settle(15)
        self.assertGreater(go_drive(e), low)

    def test_no_reward_cue_gives_weaker_go(self):
        cued = _with_reward_cue(25)
        rest = SubstrateEngine(_MODEL, age_years=25)
        rest.settle(40)
        self.assertGreater(go_drive(cued), go_drive(rest))


class TestDevelopmentalRestraint(unittest.TestCase):
    def test_executive_hold_grows_as_prefrontal_comes_online(self):
        # emergent from the seed's developmental_online_age: a young agent has fewer executive
        # circuits online -> a weaker STN brake than an older one.
        young = _with_reward_cue(4)
        older = _with_reward_cue(12)
        self.assertLess(executive_hold(young), executive_hold(older))

    def test_young_agent_acts_at_least_as_readily_as_older(self):
        # weaker brake in the young -> approach is reached no slower than in the older agent
        young = select_behaviour(_with_reward_cue(4))
        older = select_behaviour(_with_reward_cue(12))
        self.assertLessEqual(young.steps, older.steps + 1)


class TestNoCodedArbiter(unittest.TestCase):
    def test_selection_reads_activity_not_meaning(self):
        # source-level: the selection code references circuit DOMAINS (seed data) and dopamine,
        # but no psychological outcome/meaning token and no situation->behaviour mapping.
        with open(behaviour_module.__file__, "rb") as fh:
            names = {t.string.lower() for t in tokenize.tokenize(fh.readline)
                     if t.type == tokenize.NAME}
        for banned in ("fear", "callous", "psychopath", "aggression", "avoid_if", "approach_if"):
            self.assertNotIn(banned, names)


if __name__ == "__main__":
    unittest.main()

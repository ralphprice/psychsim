import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""Part 6 substrate-social phase -- the substrate is the SOLE engine (Panksepp retired, stage 5).

Invariant 6 was met before the cut: the substrate REPRODUCES the social behaviour the town sim
consumes. These tests demonstrate that on the substrate alone -- it produces observable social
acts (approach/nurture/avoid/seek_comfort/aggress) that the engine-agnostic consumers (gamemaster
adjudication, the substrate feature read-outs is_cohesive_act/is_aggressive_act, the observer
read-out) accept. The former cross-engine parity assertion (substrate == Panksepp) is gone with
the Panksepp engine; what remains is the substrate-native seam the consumers key on."""

import unittest

from affective_engine.core import Appraisal, shared_root_seed
from substrate.social import is_cohesive_act, is_aggressive_act
from affective_engine.observer import observe_substrate
from sim_world import build_world, Person, GameMaster, SocialEvent


class TestSubstrateProducesConsumableSocialBehaviour(unittest.TestCase):
    def test_warm_situation_yields_a_cohesive_substrate_act(self):
        p = Person("a", "A", shared_root_seed())
        b = p.social_act(Appraisal(social_valence=0.8, reward=0.4, label="warm"), age_years=25.0)
        self.assertTrue(is_cohesive_act(b.behaviour), f"warm -> {b.behaviour}")

    def test_threat_situation_is_not_cohesive(self):
        p = Person("a", "A", shared_root_seed())
        b = p.social_act(Appraisal(threat=0.8, social_valence=-0.4, label="threat"), age_years=25.0)
        self.assertFalse(is_cohesive_act(b.behaviour), f"threat -> {b.behaviour}")

    def test_separation_seeks_comfort(self):
        p = Person("a", "A", shared_root_seed())
        b = p.social_act(Appraisal(exclusion=0.8, label="separation"), age_years=25.0)
        self.assertEqual(b.behaviour, "seek_comfort")


class TestConsumersAdjudicateSubstrateActs(unittest.TestCase):
    def test_gamemaster_adjudicates_a_substrate_response(self):
        w = build_world()
        gm = GameMaster(w)
        p = Person("kid", "Kid", shared_root_seed())
        w.institutions["Family"].add_member("kid", "child")
        w.place_agent("kid", "home")
        appr = p.perceive(w, SocialEvent("warmth", "mother", {"social_valence": 0.8, "reward": 0.4}))
        resp = p.social_act(appr, age_years=10.0)
        inter = gm.adjudicate(p, resp, SocialEvent("warmth", "mother"))
        # the emergent substrate act was adjudicated into a world event
        self.assertEqual(inter.behaviour, resp.behaviour)
        self.assertEqual(len(gm.log), 1)


class TestFeatureSeamIsSubstrateNative(unittest.TestCase):
    def test_feature_read_outs_key_on_the_emergent_substrate_act(self):
        # the seam the consumers use: the feature read-outs classify the substrate's emergent act
        # (a behaviour string) -- no per-engine branch. A warm situation yields a cohesive,
        # non-aggressive act; the read-outs agree on that from the act alone.
        p = Person("a", "A", shared_root_seed())
        warm = p.social_act(Appraisal(social_valence=0.8, reward=0.5, label="warm"), age_years=25.0)
        self.assertTrue(is_cohesive_act(warm.behaviour))
        self.assertFalse(is_aggressive_act(warm.behaviour))


class TestObserverAdapterMeasuresThePerson(unittest.TestCase):
    def test_observer_reads_out_over_the_developed_substrate(self):
        p = Person("a", "A", shared_root_seed())
        for _ in range(15):
            p.social_act(Appraisal(social_valence=0.7, reward=0.4, label="warm"), age_years=20.0)
        out = observe_substrate(p.engine)   # circuit-engine adapter, read-only
        # ★ SUSPENDED (CEl-discrimination, ruled): empathy/callous_unemotional are NOT IMPLEMENTED (no vicarious
        # pathway); the observer reports the raw quantity under its true name instead.
        for key in ("triarchic", "distress_cue_amygdala_reactivity"):
            self.assertIn(key, out)
        self.assertNotIn("empathy", out)


if __name__ == "__main__":
    unittest.main()

import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""Part 6 substrate-social phase (3d) -- PARITY demonstrated with the legacy still present.

Invariant 6: the Panksepp Brain is retired only once the substrate REPRODUCES the social
behaviour the town sim consumes. These tests demonstrate that the substrate does -- it produces
observable social acts (approach/nurture/avoid/seek_comfort) that the existing, now engine-
agnostic consumers (gamemaster adjudication, the is_cohesive/is_aggressive feature read-outs, the
observer read-out) accept -- while the Panksepp engine is still in place. The retirement cut is a
separate, reviewed step."""

import unittest

from affective_engine.core import Appraisal, shared_root_seed
from affective_engine.drives import is_cohesive, is_aggressive, respond_to_appraisal
from affective_engine.observer import observe_substrate
from sim_world import build_world, Person, GameMaster, SocialEvent


class TestSubstrateProducesConsumableSocialBehaviour(unittest.TestCase):
    def test_warm_situation_yields_a_cohesive_substrate_act(self):
        p = Person("a", "A", shared_root_seed())
        b = p.social_act(Appraisal(social_valence=0.8, reward=0.4, label="warm"), age_years=25.0)
        self.assertTrue(is_cohesive(b), f"warm -> {b.behaviour}")

    def test_threat_situation_is_not_cohesive(self):
        p = Person("a", "A", shared_root_seed())
        b = p.social_act(Appraisal(threat=0.8, social_valence=-0.4, label="threat"), age_years=25.0)
        self.assertFalse(is_cohesive(b), f"threat -> {b.behaviour}")

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


class TestFeatureSeamIsEngineAgnostic(unittest.TestCase):
    def test_is_cohesive_agrees_across_engines_for_warmth(self):
        # the feature read-outs give the SAME verdict for the Panksepp Response and the substrate
        # SocialBehaviour to the same warm situation -- the seam that lets either engine drive the
        # sim, and the reason the consumers did not need per-engine branches.
        p = Person("a", "A", shared_root_seed())
        warm = Appraisal(social_valence=0.8, reward=0.5, label="warm")
        pan = respond_to_appraisal(p.mind, warm)          # Panksepp
        sub = p.social_act(warm, age_years=25.0)          # substrate
        self.assertTrue(is_cohesive(pan))
        self.assertEqual(is_cohesive(pan), is_cohesive(sub))
        self.assertFalse(is_aggressive(sub))


class TestObserverAdapterMeasuresThePerson(unittest.TestCase):
    def test_observer_reads_out_over_the_developed_substrate(self):
        p = Person("a", "A", shared_root_seed())
        for _ in range(15):
            p.social_act(Appraisal(social_valence=0.7, reward=0.4, label="warm"), age_years=20.0)
        out = observe_substrate(p.engine)   # circuit-engine adapter, read-only
        for key in ("triarchic", "callous_unemotional", "empathy"):
            self.assertIn(key, out)


if __name__ == "__main__":
    unittest.main()

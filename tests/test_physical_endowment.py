import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""v10 physical endowment -- E1 honesty tests (Part 6, v10 DESIGN_SPEC E1).

Physical endowment is a GIVEN input parameter: each agent is born with physical traits + a
biological sex, sampled FAITHFULLY from the seed's stated distributions using a seeded per-agent
RNG (reproducible from the world seed). The load-bearing honesty properties, asserted here
(ordinal/structural only -- never a target social outcome):

  * FAITHFUL sample: ATTRACT/MUSCLE/HEALTH ~ normal(0,1); sex ~50/50; PH-SIZE is the ONLY
    sex-conditioned trait (mean_by_sex); no OTHER trait is reshaped by sex; no hand-imposed
    trait-trait correlation.
  * PER-AGENT variance (the uniformity trap defeated): a population has distinct physical per
    agent, none trait-less -- the precondition for the beauty-premium / CU-ratio scans to measure
    something real, rather than a single shared value.
  * REPRODUCIBLE: the same world seed reproduces the same population physical.
  * BEARER-PURE stimulus + GENUINE 2x2 valuation: the stimulus an agent presents is the same
    regardless of who looks; the sex conditioning is a perceiver x bearer PAIRING, not a bearer
    property in disguise.
  * BANK invariant: a banked adult RELOADS its grown physical (restored-never-edited +
    banked-reproducibility); a pre-v10 snapshot restores physical-neutral, never fabricated.

Nothing here maps a trait to a social outcome -- population outcomes are scan_match targets that
must EMERGE from the develop-and-accrue loop, not be computed from a trait.
"""

import random
import statistics as st
import unittest

from affective_engine.physical import (sample_physical, physical_stimulus, sex_weight,
                                        SEX_MALE, SEX_FEMALE)
from affective_engine.agent import AffectiveAgent
from arena import intact_seed
from agent_bank import DevelopedAgent, snapshot, restore
from substrate.model import load_substrate
from sophropathy.engine import SimEngine


class TestFaithfulSample(unittest.TestCase):
    def setUp(self):
        self.pop = [sample_physical(random.Random(i)) for i in range(6000)]

    def test_sex_neutral_traits_are_standard_normal(self):
        for key in ("PH-ATTRACT", "PH-MUSCLE", "PH-HEALTH"):
            vals = [p[key] for p in self.pop]
            self.assertAlmostEqual(st.mean(vals), 0.0, delta=0.1, msg=f"{key} mean")
            self.assertAlmostEqual(st.pstdev(vals), 1.0, delta=0.1, msg=f"{key} sd")

    def test_sex_is_roughly_balanced(self):
        males = sum(1 for p in self.pop if p["sex"] == SEX_MALE)
        self.assertAlmostEqual(males / len(self.pop), 0.5, delta=0.05)

    def test_size_is_the_only_sex_conditioned_trait(self):
        m = [p for p in self.pop if p["sex"] == SEX_MALE]
        f = [p for p in self.pop if p["sex"] == SEX_FEMALE]
        # SIZE: males larger on average (the seed's single sex->trait link, mean_by_sex)
        self.assertGreater(st.mean([p["PH-SIZE"] for p in m]),
                           st.mean([p["PH-SIZE"] for p in f]) + 0.3)
        # MUSCLE (and the rest) must NOT differ by sex -- the seed states normal(0,1), sex-neutral
        self.assertAlmostEqual(st.mean([p["PH-MUSCLE"] for p in m]),
                               st.mean([p["PH-MUSCLE"] for p in f]), delta=0.12)

    def test_no_hand_imposed_trait_trait_correlation(self):
        a = [p["PH-ATTRACT"] for p in self.pop]
        mus = [p["PH-MUSCLE"] for p in self.pop]
        h = [p["PH-HEALTH"] for p in self.pop]
        for x, y, label in ((a, mus, "attract-muscle"), (a, h, "attract-health"),
                            (mus, h, "muscle-health")):
            self.assertLess(abs(st.correlation(x, y)), 0.1, msg=f"{label} should be ~0")


class TestBearerPureStimulusAndGenuinePairing(unittest.TestCase):
    def test_stimulus_is_bearer_pure_and_sex_neutral(self):
        b = {"sex": SEX_FEMALE, "PH-ATTRACT": 1.2, "PH-MUSCLE": -0.3, "PH-SIZE": 0.4, "PH-HEALTH": 0.5}
        b_as_male = dict(b, sex=SEX_MALE)
        # the stimulus an agent PRESENTS is a property of the bearer's traits, not their sex, and
        # not who perceives -- identical regardless of the bearer's sex label.
        self.assertEqual(physical_stimulus(b), physical_stimulus(b_as_male))
        self.assertEqual(set(physical_stimulus(b)), {"attractive_face", "formidability_cue"})

    def test_sex_weight_is_a_genuine_two_by_two(self):
        # same BEARER, different PERCEIVER -> different weight: the dimorphism lives in the
        # perceiver's valuation, not the bearer's face (Aharon: male->female reward highest).
        mf = sex_weight(SEX_MALE, SEX_FEMALE, "attractive_face")
        ff = sex_weight(SEX_FEMALE, SEX_FEMALE, "attractive_face")
        self.assertNotEqual(mf, ff)
        self.assertGreater(mf, ff)
        # an unknown pairing falls back neutral -- never silently privileges a bearer sex
        self.assertEqual(sex_weight("x", "y", "attractive_face"), 0.5)


class TestAgentLevel(unittest.TestCase):
    def test_seeded_agent_has_physical_seedless_is_neutral(self):
        a = AffectiveAgent(seed=intact_seed(), temperament_seed=42)
        self.assertEqual(set(a.physical), {"PH-ATTRACT", "PH-MUSCLE", "PH-SIZE", "PH-HEALTH"})
        self.assertIn(a.sex, (SEX_MALE, SEX_FEMALE))
        n = AffectiveAgent(seed=intact_seed())
        self.assertEqual(n.physical, {})
        self.assertIsNone(n.sex)

    def test_physical_is_reproducible_and_per_agent_distinct(self):
        a = AffectiveAgent(seed=intact_seed(), temperament_seed=42)
        same = AffectiveAgent(seed=intact_seed(), temperament_seed=42)
        other = AffectiveAgent(seed=intact_seed(), temperament_seed=43)
        self.assertEqual((a.physical, a.sex), (same.physical, same.sex))
        self.assertNotEqual(a.physical, other.physical)


class TestBankInvariant(unittest.TestCase):
    def test_banked_adult_reloads_physical_never_resamples(self):
        m = load_substrate()
        grown = AffectiveAgent(seed=intact_seed(), temperament_seed=99)
        dev = DevelopedAgent(engine=grown.engine, physical=dict(grown.physical), sex=grown.sex)
        rebuilt = restore(snapshot(dev), m)
        self.assertEqual(rebuilt.physical, grown.physical)
        self.assertEqual(rebuilt.sex, grown.sex)
        # adopt into a fresh mind that had its OWN sample -> the banked value must win
        target = AffectiveAgent(seed=intact_seed(), temperament_seed=1)
        fresh = dict(target.physical)
        target.adopt_developed(rebuilt)
        self.assertEqual(target.physical, grown.physical)
        self.assertNotEqual(target.physical, fresh)

    def test_pre_v10_snapshot_restores_physical_neutral(self):
        m = load_substrate()
        grown = AffectiveAgent(seed=intact_seed(), temperament_seed=99)
        dev = DevelopedAgent(engine=grown.engine, physical=dict(grown.physical), sex=grown.sex)
        legacy = snapshot(dev)
        legacy.pop("physical"); legacy.pop("sex")           # a v9-era snapshot has no such keys
        r = restore(legacy, m)
        self.assertEqual(r.physical, {})                    # neutral, never fabricated
        self.assertIsNone(r.sex)


class TestPopulationHasRealVariance(unittest.TestCase):
    """The uniformity trap defeated at the town level: a spawned population carries distinct,
    reproducible, faithfully-distributed physical, with NO trait-less agents."""

    def test_town_population_is_fully_and_faithfully_endowed(self):
        eng = SimEngine(population=120, seed=7)
        persons = list(eng.pop.persons.values())
        phys = [p.mind.physical for p in persons]
        self.assertTrue(all(ph for ph in phys), "every spawned person is endowed (none trait-less)")
        attract = [ph["PH-ATTRACT"] for ph in phys]
        self.assertGreater(len(set(attract)), 0.9 * len(attract), "per-agent distinct")
        self.assertAlmostEqual(st.mean(attract), 0.0, delta=0.35)
        sexes = [p.mind.sex for p in persons]
        self.assertGreater(sexes.count(SEX_MALE), 0)
        self.assertGreater(sexes.count(SEX_FEMALE), 0)

    def test_town_physical_is_reproducible_from_world_seed(self):
        a = [p.mind.physical for p in SimEngine(population=60, seed=7).pop.persons.values()]
        b = [p.mind.physical for p in SimEngine(population=60, seed=7).pop.persons.values()]
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()

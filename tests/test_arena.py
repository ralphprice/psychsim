import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""The Arena (Part 6 S12): a small closed micro-world + development-and-regression harness.

Ordinal/structural assertions only. The honesty-critical properties: environments are
perturbation patterns (never valences); the dyad talks through a resolved perception mapping (not
a two-bit channel); compression is wall-clock only; and the trace distinguishes an emergent social
dynamic from closed-loop instability (Regime-B, Part 5 S9.3)."""
import unittest

import arena
from arena import (ArenaSpec, Slot, run_arena, intact_seed, MICRO_ENVS, _ARENA_PERCEPTION)
from agent_bank import AgentBank, DevelopedAgent
from affective_engine import AffectiveAgent

_VALENCE_WORDS = ("pleasant", "unpleasant", "nice", "nasty", "stressful", "good", "bad")


def _pair(seed_a="A", seed_b="B", env="house_garden", shared=4.0, seed=7):
    return ArenaSpec(env, [Slot("A", seed=intact_seed(seed_a)), Slot("B", seed=intact_seed(seed_b))],
                     seed=seed, shared_hours=shared)


class TestEnvironmentsArePerturbationPatterns(unittest.TestCase):
    def test_micro_envs_present_things_not_valences(self):
        for name, env in MICRO_ENVS.items():
            self.assertTrue(env.present, f"{name} has nothing present")
            for thing in env.present:
                self.assertTrue(thing.stimulus, f"{thing.id} carries no perturbation stimulus")
                # the stimulus is a trigger-vocabulary dict, never a valence tag
                self.assertNotIn("valence", thing.stimulus)
            # the documentary note describes what is present, never how it feels
            self.assertFalse(any(w in env.note.lower() for w in _VALENCE_WORDS),
                             f"{name} note carries a valence word: {env.note}")

    def test_escape_is_a_structural_affordance_count(self):
        # escape is how many things are present to divert to -- a count, not a stress multiplier
        self.assertEqual(MICRO_ENVS["one_room"].escape, len(MICRO_ENVS["one_room"].present))
        self.assertLess(MICRO_ENVS["one_room"].escape, MICRO_ENVS["house_garden"].escape)


class TestPerceptionHasResolution(unittest.TestCase):
    def test_distinct_acts_present_distinct_perturbations(self):
        # NOT a two-bit channel: aggress, nurture, avoid present DIFFERENT perturbation patterns
        agg, nur, avo = _ARENA_PERCEPTION["aggress"], _ARENA_PERCEPTION["nurture"], _ARENA_PERCEPTION["avoid"]
        self.assertNotEqual(agg, nur)
        self.assertNotEqual(nur, avo)
        self.assertIn("thwarting", agg)        # an attack presents provocation/threat
        self.assertIn("affiliation", nur)      # caregiving presents affiliation
        self.assertIn("separation", avo)       # withdrawal presents contact-loss
        # perceptions are in the trigger vocabulary, never a valuation dimension
        for pat in _ARENA_PERCEPTION.values():
            self.assertNotIn("valence", pat)


class TestRegressionHarness(unittest.TestCase):
    def test_deterministic_from_seed(self):
        self.assertEqual(run_arena(_pair()).signature(), run_arena(_pair()).signature())

    def test_changed_roster_diffs_the_behaviour(self):
        two = run_arena(_pair())
        three = run_arena(ArenaSpec("house_garden",
                                    [Slot("A", seed=intact_seed("A")), Slot("B", seed=intact_seed("B")),
                                     Slot("C", seed=intact_seed("C"))], seed=7, shared_hours=4))
        self.assertNotEqual(two.signature(), three.signature())


class TestCompressionIsWallClockOnly(unittest.TestCase):
    def test_lifetimes_are_lived_across_the_childhood_span(self):
        # the agents live a compressed CHILDHOOD (age advances 0 -> near childhood_years); the run
        # takes no plasticity-rate parameter, so compression cannot touch the developmental schedule
        t = run_arena(_pair(), childhood_years=18.0)
        self.assertLess(t.records[0]["age"], 1.0)
        self.assertGreater(t.records[-1]["age"], 15.0)
        import inspect
        params = set(inspect.signature(run_arena).parameters)
        self.assertEqual(params, {"spec", "childhood_years", "episodes_per_year"})  # no learning-rate knob


class TestClosedSystemViabilityAndRegimeB(unittest.TestCase):
    def test_small_arena_stays_viable(self):
        # a closed 2-agent world does not drive itself into persistent saturation
        self.assertTrue(run_arena(_pair()).viable())

    def test_two_intact_agents_settle_and_do_not_escalate(self):
        # Regime-B (Part 5 S9.3): normal interaction must not destabilise a viable person. Two
        # intact (un-throttled) agents in a benign environment over a compressed childhood remain
        # viable AND settle (no oscillation), and do NOT escalate into aggression -- a cooperative
        # dyad, emergent, not scripted. If they DID drive each other into oscillation or a fight,
        # this test catches it rather than the Arena quietly exhibiting it.
        t = run_arena(_pair(env="house_garden"))
        self.assertTrue(t.viable(), "intact dyad lost viability")
        self.assertTrue(t.settled(), "intact dyad oscillated instead of settling")
        counts = t.act_counts()
        cohesive = counts.get("approach", 0) + counts.get("nurture", 0) + counts.get("play", 0)
        aggressive = counts.get("aggress", 0)
        self.assertGreater(cohesive, aggressive)                       # cooperative, not hostile
        self.assertLess(aggressive, 0.1 * sum(counts.values()))        # no escalation into fighting


class TestSlotSources(unittest.TestCase):
    def test_newborn_grown_banked_all_build(self):
        bank = AgentBank()
        donor = AffectiveAgent(seed=intact_seed("D"))
        bank.bank(DevelopedAgent(engine=donor.engine, provenance={"src": "test"}), "donor1")
        t = run_arena(ArenaSpec("one_house", [
            Slot("N", source="newborn", seed=intact_seed("N")),
            Slot("G", source="grown", seed=intact_seed("G"), grow_years=8.0),
            Slot("K", source="banked", bank=bank, bank_id="donor1"),
        ], seed=3, shared_hours=3))
        self.assertEqual(set(t.records[0]["acts"]), {"N", "G", "K"})
        self.assertTrue(t.viable())

    def test_roster_size_bounds_enforced(self):
        with self.assertRaises(ValueError):
            run_arena(ArenaSpec("one_room", [Slot("A", seed=intact_seed())], seed=1))  # <2


class TestHonestyNoVerdictVocabulary(unittest.TestCase):
    def test_env_and_perception_data_carry_no_valence_or_verdict(self):
        # the honesty-relevant surface is the DATA the Arena runs on -- environment notes and the
        # perception mapping. Neither may carry a valence tag or an outcome-category verdict (the
        # docstring is free to state the discipline, e.g. "not about psychopathy"; the data may not).
        banned = ("psychopath", "sophropath", "callous", "verdict", "meanness",
                  *_VALENCE_WORDS)
        for env in MICRO_ENVS.values():
            self.assertFalse(any(w in env.note.lower() for w in banned), env.note)
        for act, pat in _ARENA_PERCEPTION.items():
            self.assertFalse(any(w in act.lower() for w in banned), act)
            for key in pat:                       # perception keys are trigger channels, not verdicts
                self.assertFalse(any(w in key.lower() for w in banned), key)


if __name__ == "__main__":
    unittest.main(verbosity=2)

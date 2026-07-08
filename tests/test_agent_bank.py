import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""Part 6 S11 -- the developed-agent bank.

Grown-and-banked never fabricated; restored never edited; re-instantiation resumes (not freeze).
Tests assert the honesty rule structurally, plus round-trip fidelity and that a restored agent
keeps developing under the 1/n schedule."""

import tempfile
import tokenize
import unittest

from substrate.model import load_substrate
from substrate.engine import SubstrateEngine
from sim_world.environment_matrix import Bond
from sim_world.group_matrix import Membership
import agent_bank
from agent_bank import DevelopedAgent, AgentBank, snapshot, restore

_MODEL = load_substrate()


def _grow_agent(age: float = 25.0, ticks: int = 150, rearing: str = "warm") -> DevelopedAgent:
    """GROW an agent through a fast standard developmental run (never assign adult weights)."""
    eng = SubstrateEngine(_MODEL, age_years=0.5)
    cue = "IN-SOMATO:affective_touch" if rearing == "warm" else "IN-SOMATO:nociception"
    for i in range(ticks):
        eng.set_age(0.5 + age * i / ticks)
        eng.clear_inputs()
        eng.inject_channel(cue, 0.6)
        eng.settle(3)
    eng.set_age(age)
    a = DevelopedAgent(engine=eng, provenance={"seed": "shared_root", "rng_seed": 7,
                                               "rearing": rearing})
    for _ in range(6):
        a.social.observe("mother", r=0.4, attachment_pull=0.6, threat_pull=0.1)
        a.self_reflection.reflect(r=0.3, attachment_pull=0.4)
    a.environmental.bonds["toy"] = Bond("toy", encounters=3, attraction=0.5, value=0.3)
    a.group.memberships["team"] = Membership("team", belonging=0.4, standing=0.3)
    a.state_vector.levels["energy"] = 0.6
    return a


class TestRoundTripFidelity(unittest.TestCase):
    def test_snapshot_restore_reproduces_developed_state(self):
        a = _grow_agent()
        b = restore(snapshot(a), _MODEL)
        # the sculpted connectome, bit-for-bit
        self.assertEqual(a.engine.weight, b.engine.weight)
        self.assertEqual(a.engine.exp_count, b.engine.exp_count)
        self.assertEqual(a.engine.pruned, b.engine.pruned)
        self.assertEqual(a.engine.age_years, b.engine.age_years)
        # the four matrices
        self.assertEqual(a.social.slots["mother"].attachment, b.social.slots["mother"].attachment)
        self.assertEqual(a.social.slots["mother"].value, b.social.slots["mother"].value)
        self.assertEqual(a.self_reflection.self_value(), b.self_reflection.self_value())
        self.assertEqual(a.environmental.bonds["toy"].value, b.environmental.bonds["toy"].value)
        self.assertEqual(a.group.memberships["team"].belonging, b.group.memberships["team"].belonging)
        # the state vector + provenance
        self.assertEqual(a.state_vector.levels["energy"], b.state_vector.levels["energy"])
        self.assertEqual(a.provenance["rng_seed"], b.provenance["rng_seed"])

    def test_snapshot_is_json_stable(self):
        import json
        a = _grow_agent()
        s = snapshot(a)
        self.assertEqual(json.loads(json.dumps(s)), s)   # fully JSON-able


class TestResumeKeepsDeveloping(unittest.TestCase):
    """S11.4: a re-instantiated adult is NOT frozen -- plasticity continues under 1/n."""

    def test_restored_agent_continues_to_develop(self):
        a = _grow_agent()
        b = restore(snapshot(a), _MODEL)
        before = list(b.engine.weight)
        b.engine.clear_inputs()
        b.engine.inject_channel("IN-SOMATO:affective_touch", 0.6)
        for _ in range(20):
            b.engine.settle(3)
        self.assertNotEqual(before, b.engine.weight)   # it kept developing (not frozen)

    def test_exp_count_preserved_so_adult_steps_are_small(self):
        # the 1/n schedule resumes from where it was: an adult keeps its high exp_count, so a
        # further experience moves weights only slightly -- exactly as if never banked.
        a = _grow_agent()
        self.assertGreater(max(a.engine.exp_count), 0)
        b = restore(snapshot(a), _MODEL)
        self.assertEqual(a.engine.exp_count, b.engine.exp_count)


class TestHonestyGrownNotFabricated(unittest.TestCase):
    def test_bank_source_has_no_fabricate_path(self):
        # S11.5: grown-and-banked, never fabricated. No code name assigns adult weights directly.
        with open(agent_bank.__file__, "rb") as fh:
            names = {t.string.lower() for t in tokenize.tokenize(fh.readline)
                     if t.type == tokenize.NAME}
        for banned in ("fabricate", "assign_adult", "set_adult_weights", "adult_weights",
                       "stipulate", "synthesize_adult"):
            self.assertNotIn(banned, names)

    def test_restore_does_not_edit_the_banked_state(self):
        # S11.5: restored, never edited. A restore + re-snapshot reproduces the banked state
        # exactly (no mutation hook, no drift).
        s = snapshot(_grow_agent())
        again = snapshot(restore(s, _MODEL))
        self.assertEqual(s["engine"]["weight"], again["engine"]["weight"])
        self.assertEqual(s["social"], again["social"])


class TestBankCacheAndProvenance(unittest.TestCase):
    def test_auto_bank_records_adults_at_milestones(self):
        bank = AgentBank()
        adult = _grow_agent(age=25.0)
        banked = bank.auto_bank(adult, "alex", provenance={"rearing": "warm"})
        self.assertIn("alex@18", banked)          # milestones reached by age 25
        self.assertIn("alex@25", banked)
        self.assertNotIn("alex@40", banked)       # not yet 40
        self.assertEqual(bank.provenance_of("alex@25")["rng_seed"], 7)

    def test_file_persistence_round_trips(self):
        bank = AgentBank()
        bank.bank(_grow_agent(), "a1")
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            path = fh.name
        try:
            bank.save(path)
            reloaded = AgentBank(path=path)
            self.assertIn("a1", reloaded)
            b = reloaded.restore("a1", _MODEL)
            self.assertEqual(b.provenance["rng_seed"], 7)
        finally:
            _O.unlink(path)


if __name__ == "__main__":
    unittest.main()

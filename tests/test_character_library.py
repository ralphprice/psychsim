import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

"""The controlled-experiment character library: developed-substrate serialisation (through
the AgentBank -- the single serialization path), growing an adult to adulthood on the
substrate from a temperament seed + rearing, and caching a library.

The discipline: only temperament (given reactivity) and rearing are set; the strength
profile is GROWN. These tests check the machinery is faithful and reproducible -- NOT
that any particular outcome arises (at this crude stage the substrate funnels to a
narrow read-out, which is correct, not a target)."""
import json
import tempfile
import unittest

from substrate.readout import read_mind, _READOUT_DOMAINS
from affective_engine.development import warm_firm_home, harsh_inconsistent_home
from agent_bank import DevelopedAgent, snapshot, restore
from sophropathy.society import fearless_child_seed, typical_child_seed
from sophropathy.library import (grow_adult, CharacterLibrary, LibraryEntry,
                                 build_default_library, TEMPERAMENTS, REARINGS)


def _domain_throttle(engine, domain: str) -> float:
    """The maximum temperament throttle applied to any circuit of `domain` (0 if none)."""
    return max([engine.throttle.get(cid, 0.0) for cid, c in engine.model.circuits.items()
                if c.domain == domain] + [0.0])


class TestDevelopedSubstrateSerialisation(unittest.TestCase):
    def test_round_trips_developed_substrate(self):
        # a grown adult's developed substrate serialises and restores through the bank exactly
        a = grow_adult(fearless_child_seed(), warm_firm_home(), seed=1)
        s = snapshot(DevelopedAgent(engine=a.engine))
        self.assertIn("engine", s)
        self.assertIsInstance(json.dumps(s), str)          # plain JSON
        back = restore(s)
        self.assertEqual(back.engine.weight, a.engine.weight)      # exact weight round-trip
        self.assertEqual(back.engine.age_years, a.engine.age_years)


class TestGrowAdult(unittest.TestCase):
    def test_reproducible_from_seed(self):
        a1 = grow_adult(fearless_child_seed(), warm_firm_home(), seed=42)
        a2 = grow_adult(fearless_child_seed(), warm_firm_home(), seed=42)
        self.assertEqual(a1.engine.weight, a2.engine.weight)       # identical developed substrate

    def test_grows_strength_and_has_readout(self):
        a = grow_adult(typical_child_seed(), harsh_inconsistent_home(), seed=7)
        r = read_mind(a)
        self.assertIn(r.dominant.value, _READOUT_DOMAINS)
        self.assertAlmostEqual(sum(r.profile.values()), 1.0, places=5)   # a distribution
        self.assertTrue(a.memory.events)                                 # a lived history

    def test_temperament_is_given_and_preserved(self):
        # the given reactivity bias is present in the substrate: a fearless temperament (low
        # THREAT/ANXIETY) throttles the defensive-threat circuits; a typical one (at reference)
        # does not. The bias is GIVEN via the seed, not written into the grown outcome.
        fearless = grow_adult(fearless_child_seed(), warm_firm_home(), seed=5)
        typical = grow_adult(typical_child_seed(), warm_firm_home(), seed=5)
        self.assertGreater(_domain_throttle(fearless.engine, "defensive_threat"),
                           _domain_throttle(typical.engine, "defensive_threat"))


class TestCharacterLibrary(unittest.TestCase):
    def test_grow_save_load_round_trip(self):
        lib = CharacterLibrary()
        lib.grow("Test A", "typical", "warm_firm", seed=1)
        lib.grow("Test B", "fearless", "harsh", seed=2)
        self.assertEqual(len(lib.entries), 2)
        with tempfile.TemporaryDirectory() as d:
            path = lib.save(_O.path.join(d, "adults.json"))
            back = CharacterLibrary.load(path)
        self.assertEqual(len(back.entries), 2)
        self.assertEqual([e.name for e in back.entries], ["Test A", "Test B"])
        # the serialised developed state round-trips exactly through the bank snapshot
        self.assertEqual(back.entries[0].state, lib.entries[0].state)
        # a loaded entry restores a usable developed substrate (restored-never-edited)
        dev = back.entries[0].make_agent()
        self.assertIsInstance(dev, DevelopedAgent)
        self.assertEqual(dev.engine.weight, lib.entries[0].state["engine"]["weight"])

    def test_default_library_is_deterministic_and_varied(self):
        a = build_default_library(seed=123)
        b = build_default_library(seed=123)
        self.assertEqual(len(a.entries), len(TEMPERAMENTS) * len(REARINGS))
        self.assertEqual([e.to_dict() for e in a.entries],
                         [e.to_dict() for e in b.entries])          # reproducible
        # every temperament x rearing combination is represented
        combos = {(e.temperament, e.rearing) for e in a.entries}
        self.assertEqual(combos, {(t, r) for t in TEMPERAMENTS for r in REARINGS})


if __name__ == "__main__":
    unittest.main(verbosity=2)

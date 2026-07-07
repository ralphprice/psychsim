import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

"""The controlled-experiment character library: Brain serialisation, growing an adult
to adulthood on the substrate from a temperament seed + rearing, and caching a library.

The discipline: only temperament (given reactivity) and rearing are set; the strength
profile is GROWN. These tests check the machinery is faithful and reproducible -- NOT
that any particular outcome arises (at this crude stage the substrate funnels to SEEKING,
which is correct, not a target)."""
import json
import tempfile
import unittest

from affective_engine.drives import Brain, System, read_mind
from affective_engine.development import warm_firm_home, harsh_inconsistent_home
from sophropathy.society import fearless_child_seed, typical_child_seed
from sophropathy.library import (grow_adult, CharacterLibrary, LibraryEntry,
                                 build_default_library, TEMPERAMENTS, REARINGS)


class TestBrainSerialisation(unittest.TestCase):
    def test_round_trips_reactivity_and_strength(self):
        a = grow_adult(fearless_child_seed(), warm_firm_home(), seed=1)
        d = a.brain.to_dict()
        self.assertEqual(set(d), {s.value for s in System})
        for pair in d.values():
            self.assertEqual(len(pair), 2)            # [reactivity, strength]
        b = Brain.from_dict(d)
        self.assertEqual(b.to_dict(), d)              # exact round-trip
        self.assertIsInstance(json.dumps(d), str)     # plain JSON

    def test_from_dict_defaults_missing_systems(self):
        b = Brain.from_dict({"SEEKING": [0.9, 0.8]})  # only one system given
        self.assertAlmostEqual(b.drives[System.SEEKING].reactivity, 0.9)
        self.assertAlmostEqual(b.drives[System.FEAR].reactivity, 0.5)   # neutral fallback


class TestGrowAdult(unittest.TestCase):
    def test_reproducible_from_seed(self):
        a1 = grow_adult(fearless_child_seed(), warm_firm_home(), seed=42)
        a2 = grow_adult(fearless_child_seed(), warm_firm_home(), seed=42)
        self.assertEqual(a1.brain.to_dict(), a2.brain.to_dict())

    def test_grows_strength_and_has_readout(self):
        a = grow_adult(typical_child_seed(), harsh_inconsistent_home(), seed=7)
        r = read_mind(a)
        self.assertIn(r.dominant, list(System))
        self.assertAlmostEqual(sum(r.profile.values()), 1.0, places=5)   # a distribution
        self.assertTrue(a.memory.events)                                 # a lived history

    def test_temperament_is_given_and_preserved(self):
        # inherited reactivity differs by seed even where grown strengths converge
        fearless = grow_adult(fearless_child_seed(), warm_firm_home(), seed=5)
        typical = grow_adult(typical_child_seed(), warm_firm_home(), seed=5)
        self.assertLess(fearless.brain.drives[System.FEAR].reactivity,
                        typical.brain.drives[System.FEAR].reactivity)


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
        # a loaded entry rebuilds a usable grown brain
        b = back.entries[0].make_brain()
        self.assertEqual(len(b.drives), 7)
        self.assertEqual(b.to_dict(), lib.entries[0].brain)

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

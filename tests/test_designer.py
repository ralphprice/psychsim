import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

import unittest, tempfile

from neuraldesigner import (NeuralLibrary, InputFeature, CircuitDef, TriggerDef,
                            PathwayDef, NetworkDef, LibraryAgent, Situation,
                            build_example_library)
from neuraldesigner.bridge import to_engine_networks


class TestLibrary(unittest.TestCase):
    def test_authoring_and_validation(self):
        lib = build_example_library()
        self.assertEqual(lib.validate(), [])
        self.assertGreaterEqual(len(lib.circuits), 7)
        self.assertGreaterEqual(len(lib.pathways), 5)

    def test_bad_reference_rejected(self):
        lib = NeuralLibrary()
        lib.add_circuit(CircuitDef("A"))
        with self.assertRaises(ValueError):
            lib.add_pathway(PathwayDef("p", "A", "GHOST", 0.5))

    def test_json_round_trip(self):
        lib = build_example_library()
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            path = f.name
        lib.save(path)
        lib2 = NeuralLibrary.load(path)
        self.assertEqual(set(lib.circuits), set(lib2.circuits))
        self.assertEqual(set(lib.pathways), set(lib2.pathways))
        self.assertEqual(lib2.validate(), [])

    def test_loop_detection(self):
        lib = build_example_library()
        loops = lib.find_loops()
        flat = {frozenset(l) for l in loops}
        self.assertIn(frozenset({"THREAT", "FRUSTRATION"}), flat)


class TestRuntime(unittest.TestCase):
    def test_cascade_activates_a_circuit_with_no_trigger(self):
        lib = build_example_library()
        ag = LibraryAgent(lib)
        # VIGILANCE has no external trigger; a threat should still activate it
        hist = ag.trace(Situation({"threat": 0.9, "controllability": 0.3}), ticks=5)
        self.assertAlmostEqual(hist[0]["VIGILANCE"], 0.0, places=6)
        self.assertGreater(hist[-1]["VIGILANCE"], 0.1)

    def test_inhibitory_pathway_reduces_frustration(self):
        lib = build_example_library()
        weak = LibraryAgent(lib, gains={"CONTROL": 0.2})
        strong = LibraryAgent(lib, gains={"CONTROL": 0.9})
        s = Situation({"provocation": 0.7, "goal_relevance": 0.6, "controllability": 0.3})
        hw = weak.trace(s, ticks=6); hs = strong.trace(s, ticks=6)
        self.assertLess(hs[-1]["FRUSTRATION"], hw[-1]["FRUSTRATION"])
        self.assertGreater(strong.activation["CONTROL"], weak.activation["CONTROL"])

    def test_determinism(self):
        lib = build_example_library()
        a = LibraryAgent(lib); b = LibraryAgent(lib)
        s = Situation({"threat": 0.6, "provocation": 0.4})
        self.assertEqual(a.settle(s), b.settle(s))
        self.assertEqual(a.activation, b.activation)


class TestBridge(unittest.TestCase):
    def test_export_keys_match_engine_network_fields(self):
        specs = to_engine_networks(build_example_library())
        self.assertIn("reactive_aggression", specs)
        for spec in specs.values():
            self.assertEqual(set(spec), {"name", "weights", "governance",
                                         "affordances", "policy", "instr"})


if __name__ == "__main__":
    unittest.main(verbosity=2)

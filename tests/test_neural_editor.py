import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""The neural-design authoring store: view (SVG + integrity), CRUD over pathways/networks/
circuits with referential-integrity feedback, and circuit removal cascading."""
import unittest

from neuraldesigner.store import library_view, upsert, remove
from neuraldesigner.library import NeuralLibrary, CircuitDef, PathwayDef


class TestNeuralStore(unittest.TestCase):
    def test_view_has_svg_and_collections(self):
        v = library_view()
        self.assertTrue(v["svg"].startswith("<svg"))
        for c in ("circuit", "pathway", "network", "trigger", "feature"):
            self.assertIn(c, v["collections"])
        self.assertIsInstance(v["validation"], list)
        self.assertIsInstance(v["loops"], list)

    def test_pathway_crud_and_integrity_feedback(self):
        circuits = list(library_view()["library"]["circuits"])
        a, b = circuits[0], circuits[1]
        upsert("pathway", {"id": "__t_pw__", "source": a, "target": b, "weight": -0.5,
                           "kind": "direct", "description": ""})
        try:
            self.assertIn("__t_pw__", library_view()["library"]["pathways"])
            with self.assertRaises(ValueError):                     # integrity feedback
                upsert("pathway", {"id": "__bad__", "source": "nope", "target": b, "weight": 0.1})
        finally:
            self.assertTrue(remove("pathway", "__t_pw__"))          # cleanup
        self.assertNotIn("__t_pw__", library_view()["library"]["pathways"])

    def test_remove_circuit_cascades(self):
        lib = NeuralLibrary()
        lib.add_circuit(CircuitDef("A", "A"))
        lib.add_circuit(CircuitDef("B", "B"))
        lib.add_pathway(PathwayDef("ab", "A", "B", 0.5))
        self.assertTrue(lib.remove_circuit("A"))
        self.assertNotIn("ab", lib.pathways)                       # cascade dropped the pathway


if __name__ == "__main__":
    unittest.main(verbosity=2)

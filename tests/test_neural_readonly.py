import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)  # repo root, for `import psychsim_server`

import re
import unittest

from substrate.model import load_substrate
from substrate.view import substrate_view


class TestSubstrateViewMatchesEngine(unittest.TestCase):
    """The /neural view reads through the SAME loader the engine uses, so the UI can never show a
    different substrate than the one that runs."""

    def setUp(self):
        self.model = load_substrate()
        self.view = substrate_view()

    def test_counts_match_the_engine_loader(self):
        self.assertEqual(self.view["meta"]["n_circuits"], len(self.model.circuits))
        self.assertEqual(len(self.view["circuits"]), len(self.model.circuits))
        self.assertEqual(self.view["meta"]["n_connections"], len(self.model.connections))
        self.assertEqual(len(self.view["connections"]), len(self.model.connections))

    def test_reports_the_seed_version_and_is_read_only(self):
        self.assertEqual(self.view["meta"]["version"], self.model.meta.get("version"))
        self.assertTrue(self.view["meta"]["source_of_truth"].endswith("psychsim_substrate_seed_v13.json"))
        self.assertTrue(self.view["read_only"])


class TestProvenanceFromSeed(unittest.TestCase):
    """Sources/confidence are provenance ABOUT THE ORGANISM and must come from the seed, verbatim."""

    def setUp(self):
        self.view = substrate_view()

    def test_circuits_carry_seed_provenance(self):
        for c in self.view["circuits"]:
            self.assertIn("confidence", c)
            self.assertIn("sources", c)
        self.assertTrue(any(c["sources"] for c in self.view["circuits"]))
        self.assertTrue(any(c["confidence"] for c in self.view["circuits"]))

    def test_scaffold_flags_assumption_weights_only(self):
        conns = self.view["connections"]
        for k in conns:
            # scaffold iff the seed's basis is a bare assumption -- a placeholder, not a measurement
            self.assertEqual(k["scaffold"], k["basis"] == "assumption")
        self.assertTrue(any(k["scaffold"] for k in conns), "seed has assumption-basis weights")
        self.assertTrue(any(not k["scaffold"] for k in conns), "seed has better-grounded weights too")


class TestViewHasNoWritePath(unittest.TestCase):
    """The view module only reads -- no file write, no JSON dump."""

    def test_view_module_never_writes(self):
        import substrate.view as v
        with open(v.__file__) as fh:
            code = re.sub(r"#.*", "", fh.read())
        self.assertNotIn("json.dump", code)
        self.assertIsNone(re.search(r"open\([^)]*['\"][wa]", code))  # no open(..., "w"/"a")


class TestServerHasNoNeuralWritePath(unittest.TestCase):
    """The server exposes /neural as the read-only substrate view and has no neural write command."""

    def test_neural_endpoint_is_the_readonly_substrate_view(self):
        import psychsim_server as srv
        self.assertIs(srv.neural_view, substrate_view)

    def test_old_neural_write_imports_are_gone(self):
        import psychsim_server as srv
        self.assertFalse(hasattr(srv, "neural_upsert_item"))
        self.assertFalse(hasattr(srv, "neural_remove_item"))

    def test_no_neural_write_command_in_dispatch(self):
        # assert about CODE, not the explanatory comments
        with open(_O.path.join(_ROOT, "psychsim_server.py")) as fh:
            code = re.sub(r"#.*", "", fh.read())
        self.assertNotIn('"neural_upsert"', code)
        self.assertNotIn('"neural_delete"', code)
        self.assertNotIn("neuraldesigner", code)  # the dead sandbox is no longer wired in


if __name__ == "__main__":
    unittest.main()

import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""The executive-function (frontal-cortex) editor: declarative monitor specs compile to
patterns, CRUD with validation, an installed monitor actually modulates -- and the
registry is EMPTY by default (the disciplined state: no hand-invented patterns)."""
import unittest

from affective_engine.exec_store import (load_monitor_specs, spec_to_pattern,
                                         install_data_monitors, upsert_monitor,
                                         delete_monitor, executive_view)
from affective_engine.executive import Executive
from affective_engine.drives import System


class TestExecStore(unittest.TestCase):
    def test_registry_empty_by_default(self):
        self.assertEqual(load_monitor_specs(), [])           # discipline: empty registry
        ex = Executive()
        install_data_monitors(ex)
        self.assertEqual(ex.monitors, [])                    # no-op by default

    def test_spec_compiles_to_predicate(self):
        p = spec_to_pattern({"name": "t", "target": "RAGE", "kind": "inhibit",
                             "when_dominant": "RAGE"})
        self.assertEqual(p.target, System.RAGE)
        self.assertTrue(p.matches(System.RAGE, {}, {}))      # fires when RAGE dominant
        self.assertFalse(p.matches(System.SEEKING, {}, {}))  # not otherwise

    def test_crud_validation_and_effect(self):
        with self.assertRaises(ValueError):
            upsert_monitor({"target": "RAGE"})               # missing name
        with self.assertRaises(ValueError):
            upsert_monitor({"name": "x", "target": "NOPE"})  # unknown system
        upsert_monitor({"name": "__t_mon__", "target": "RAGE", "kind": "inhibit",
                        "when_dominant": "RAGE"})
        try:
            self.assertIn("__t_mon__", [m["name"] for m in load_monitor_specs()])
            ex = Executive()
            ex.inhibitory_capacity = 1.0
            install_data_monitors(ex)
            act = {System.RAGE: 1.0}
            ex.consult(act, System.RAGE, {})
            self.assertLess(act[System.RAGE], 1.0)           # the installed monitor inhibited
        finally:
            self.assertTrue(delete_monitor("__t_mon__"))     # cleanup
        self.assertEqual(load_monitor_specs(), [])           # back to empty

    def test_view_shape(self):
        v = executive_view()
        self.assertEqual(v["monitors"], [])
        self.assertIn("SEEKING", v["systems"])
        self.assertIn("note", v)


if __name__ == "__main__":
    unittest.main(verbosity=2)

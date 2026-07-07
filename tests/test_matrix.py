import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""View / add / edit / delete of the three matrices' definition items, persisted to data
files. Edits to groups flow into the runtime default_groups(); the emergent traces are
not touched here."""
import unittest

from config.matrixstore import kinds, list_items, upsert_item, delete_item


class TestMatrixStore(unittest.TestCase):
    def test_kinds_metadata(self):
        k = kinds()
        for kind in ("environment", "group", "social"):
            self.assertIn(kind, k)
            self.assertIn("fields", k[kind])
            self.assertIn("id_field", k[kind])

    def test_list_all_kinds(self):
        self.assertGreaterEqual(len(list_items("environment")), 15)
        self.assertGreaterEqual(len(list_items("group")), 4)
        self.assertEqual(len(list_items("social")), 7)

    def test_upsert_requires_id(self):
        with self.assertRaises(ValueError):
            upsert_item("group", {"name": "no id"})

    def test_crud_flows_into_runtime(self):
        from sim_world.group_matrix import default_groups
        self.assertNotIn("__test_grp__", {g.id for g in default_groups()})
        upsert_item("group", {"id": "__test_grp__", "name": "t", "kind": "clique",
                              "size": 5, "cohesion": 0.5, "status": 0.5, "norm_strength": 0.5})
        try:
            self.assertIn("__test_grp__", {g.id for g in default_groups()})   # added
            upsert_item("group", {"id": "__test_grp__", "cohesion": 0.9})     # edited
            self.assertEqual(next(g.cohesion for g in default_groups()
                                  if g.id == "__test_grp__"), 0.9)
        finally:
            self.assertTrue(delete_item("group", "__test_grp__"))            # deleted (cleanup)
        self.assertNotIn("__test_grp__", {g.id for g in default_groups()})


if __name__ == "__main__":
    unittest.main(verbosity=2)

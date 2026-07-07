import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""The environment inventory is data-driven (data/things/*.json) and expandable: the
core evidence-based hazards are preserved and ordinary exposures added; the matrix
mechanism (inherited leans, encounter) still works over the expanded set."""
import unittest

from sim_world.environment_matrix import default_things, _load_data_things, birth_matrix


class TestThings(unittest.TestCase):
    def test_inventory_is_data_driven_and_expanded(self):
        ids = {t.id for t in default_things()}
        for core in ("road_traffic", "water_play", "snake_spider", "food"):
            self.assertIn(core, ids)                      # evidence-based core preserved
        for extra in ("books", "grandparents", "household_conflict"):
            self.assertIn(extra, ids)                     # ordinary exposures added
        self.assertGreaterEqual(len(default_things()), 15)

    def test_data_files_present(self):
        self.assertTrue(_load_data_things())              # loaded from data/things/*.json

    def test_inherited_leans_still_seed_birth_matrix(self):
        m = birth_matrix()
        self.assertGreater(m.bond("snake_spider").aversion, 0.0)   # ancestral wariness


if __name__ == "__main__":
    unittest.main(verbosity=2)

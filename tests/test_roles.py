import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""The data-driven role library: expanded roles load, child/adult stay byte-identical,
scheduling is role-driven, and the engine assigns varied roles deterministically."""
import unittest

from sophropathy.townlife import (available_roles, role_block, scheduled_block,
                                  role_is_child, ROLE_SCHEDULES)
from sophropathy.engine import SimEngine


class TestRoles(unittest.TestCase):
    def test_library_has_expanded_roles(self):
        roles = available_roles()
        for r in ("child", "adult", "preschooler", "teenager", "retired", "teacher"):
            self.assertIn(r, roles)

    def test_child_adult_back_compat_byte_identical(self):
        for hour in range(0, 24):
            for wk in (False, True):
                self.assertEqual(scheduled_block(hour, wk, True), role_block("child", hour, wk))
                self.assertEqual(scheduled_block(hour, wk, False), role_block("adult", hour, wk))

    def test_role_is_child(self):
        self.assertTrue(role_is_child("child"))
        self.assertTrue(role_is_child("teenager"))
        self.assertFalse(role_is_child("adult"))
        self.assertFalse(role_is_child("retired"))

    def test_engine_assigns_varied_roles_deterministically(self):
        a = SimEngine(population=200, seed=7).roles
        b = SimEngine(population=200, seed=7).roles
        self.assertEqual(a, b)                              # deterministic
        self.assertGreater(len(set(a.values())), 2)        # more than child/adult
        for r in set(a.values()):
            self.assertIn(r, ROLE_SCHEDULES)               # every role is in the library

    def test_author_any_role(self):
        e = SimEngine(population=40, seed=7)
        cid = e.add_person("retired", temperament="typical")
        self.assertEqual(e.roles[cid], "retired")
        self.assertFalse(e.info[cid][0])                   # retired is an adult role


if __name__ == "__main__":
    unittest.main(verbosity=2)

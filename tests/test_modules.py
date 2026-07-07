import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)   # repo root, for `import project`

"""The plug-in module system: discovery, the selection API, the deprecated fearless_frac
alias equivalence, and the study-neutrality of the new platform infra."""
import unittest

from modular import discover_modules, Module
from project import (ProjectSpec, spawn_universe, available_modules,
                     available_extensions)

_EXT = _O.path.join(_ROOT, "extensions")


def _fearless_selection(spec):
    """Which children are seeded fearless -- the SEEDED (deterministic) part of the
    spawn (the reactivity values around the bias are drawn unseeded, by design)."""
    pop = spawn_universe(spec, place_residents=False).population
    return sorted(c for c in pop.pupils
                  if pop.persons[c].mind.seed.name == "shared_root")


class TestModules(unittest.TestCase):
    def test_discovers_both_studies(self):
        mods = discover_modules(_EXT)
        self.assertIn("sophropathy", mods)
        self.assertIn("justice", mods)
        self.assertIsInstance(mods["sophropathy"], Module)
        self.assertIn("child_source", mods["sophropathy"].hooks())

    def test_available_modules_and_extensions(self):
        infos = available_modules()
        one = next(m for m in infos if m["name"] == "sophropathy")
        self.assertIn("hooks", one)
        self.assertIn("params", one)
        self.assertIn("sophropathy", available_extensions())     # back-compat key

    def test_fearless_frac_alias_equals_module_params(self):
        alias = ProjectSpec(name="t", target_population=120, extensions=["sophropathy"],
                            fearless_frac=0.4, seed=3)
        modp = ProjectSpec(name="t", target_population=120, extensions=["sophropathy"],
                           module_params={"sophropathy": {"fearless_frac": 0.4}}, seed=3)
        off = ProjectSpec(name="t", target_population=120, extensions=[], seed=3)
        self.assertEqual(_fearless_selection(alias), _fearless_selection(modp))  # equivalent
        self.assertTrue(_fearless_selection(modp))                               # perturbs
        self.assertEqual(_fearless_selection(off), [])                           # off: none

    def test_world_content_collected_on_universe(self):
        uni = spawn_universe(ProjectSpec(name="t", target_population=80,
                                         extensions=["sophropathy"], seed=1),
                             place_residents=False)
        self.assertIn("sophropathy", uni.content)

    def test_new_platform_infra_is_study_neutral(self):
        # core/modular and core/config must name no study (no psychology in the platform)
        for pkg in ("core/modular", "core/config"):
            for root, _dirs, files in _O.walk(_O.path.join(_ROOT, pkg)):
                for fn in files:
                    if not fn.endswith(".py"):
                        continue
                    with open(_O.path.join(root, fn)) as f:
                        txt = f.read().lower()
                    for banned in ("sophropath", "fearless", "psychopath"):
                        self.assertNotIn(banned, txt, f"{fn} leaks study term '{banned}'")


if __name__ == "__main__":
    unittest.main(verbosity=2)

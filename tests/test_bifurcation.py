import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

import unittest
from bifurcation import (Config, run_config, sweep_1d, phase_map_2d,
                         boundary_cells, bisect_edge)
from bifurcation.viz import render_phase_svg, render_sweep_svg


class TestRun(unittest.TestCase):
    def test_run_returns_emergent_measures(self):
        from affective_engine.drives import System
        r = run_config(Config(warmth=0.9, structure=0.9))
        self.assertIn(r.classification, {s.value for s in System})   # a dominant system
        self.assertAlmostEqual(sum(r.profile.values()), 1.0, places=5)
        self.assertTrue(-1.0 <= r.score <= 1.0)

    def test_both_extremes_yield_wellformed_profiles(self):
        # at this crude stage we do NOT force the extremes to diverge; we check the
        # harness measures both honestly (a finite axis, a normalised profile)
        for w in (0.95, 0.05):
            r = run_config(Config(warmth=w, structure=w))
            self.assertTrue(-1.0 <= r.score <= 1.0)
            self.assertAlmostEqual(sum(r.profile.values()), 1.0, places=5)


class TestSweep(unittest.TestCase):
    def test_sweep_returns_a_score_per_cell(self):
        sw = sweep_1d(Config(structure=0.3), "warmth", 0.0, 1.0, steps=21)
        self.assertEqual(len(sw.results), 21)
        self.assertTrue(all(-1.0 <= r.score <= 1.0 for r in sw.results))

    def test_phase_map_classifies_all_cells(self):
        pm = phase_map_2d(Config(), "warmth", 0.0, 1.0, "structure", 0.0, 1.0, nx=9, ny=9)
        counts = pm.region_counts()
        self.assertEqual(sum(counts.values()), 81)       # every cell is classified
        self.assertGreaterEqual(len(counts), 1)          # >=1 basin (crude: may be uniform)
        _ = boundary_cells(pm)                            # separatrix extraction runs


class TestBisection(unittest.TestCase):
    def test_bisect_runs_and_returns_boundary_or_none(self):
        # depending on the (crude) substrate the ends may or may not differ; either
        # way bisection must run and return a well-formed result or None
        e = bisect_edge(Config(structure=0.3), "warmth", 0.0, 1.0, tol=1e-3)
        if e is not None:
            self.assertNotEqual(e["below"][1], e["above"][1])

    def test_bisect_none_when_ends_agree(self):
        # two clearly-good configs -> same classification -> no boundary
        e = bisect_edge(Config(warmth=0.9, structure=0.9), "recognition", 0.6, 0.9)
        self.assertIsNone(e)


class TestViz(unittest.TestCase):
    def test_svgs_render(self):
        pm = phase_map_2d(Config(), "warmth", 0.0, 1.0, "structure", 0.0, 1.0, nx=7, ny=7)
        sv = render_phase_svg(pm)
        self.assertTrue(sv.startswith("<svg") and sv.rstrip().endswith("</svg>"))
        sw = sweep_1d(Config(structure=0.3), "warmth", 0.0, 1.0, steps=11)
        self.assertIn("polyline", render_sweep_svg(sw))


class TestDeterminism(unittest.TestCase):
    def test_reproducible(self):
        a = run_config(Config(warmth=0.4, structure=0.4))
        b = run_config(Config(warmth=0.4, structure=0.4))
        self.assertEqual(a.classification, b.classification)
        self.assertAlmostEqual(a.score, b.score, places=9)


if __name__ == "__main__":
    unittest.main(verbosity=2)

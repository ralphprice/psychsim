import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""The scan controller's AUTO search layer (Part 4 S8) -- the honesty checklist the design session
settled: single named objective recorded by name with NO scalarisation; coarse-to-fine (binary
screen -> graded only on survivors); viable-first (broken = expected background, never scored);
intact control arm with scores relative to it; every 'best' a hypothesis, not a finding; the
trajectory logged; and no model handle (only set_throttle via the primitive)."""
import inspect
import unittest

import scan_search
from scan_search import scan, OBJECTIVES, Objective, ScanResult, robustness_across_seeds
from scan import Throttle, AFFECTIVE_EMPATHY

_SUBSET = list(AFFECTIVE_EMPATHY)      # 5 circuits -- keep the search fast


def _run():
    return scan("dissociation", seeds=[5], circuits=_SUBSET, screen_delta=0.02, top_k=2)


class TestObjectiveIsSingleNamedNotBlended(unittest.TestCase):
    def test_objective_holds_exactly_one_signature(self):
        for obj in OBJECTIVES.values():
            self.assertIsInstance(obj.signature, str)          # ONE key, not a vector of keys
            self.assertIn(obj.orientation, (+1, -1))

    def test_result_records_objective_by_name(self):
        r = _run()
        self.assertEqual(r.objective, "dissociation")          # positive record: the name travels
        self.assertEqual(r.signature, "dissociation_index")

    def test_no_scalarisation_over_multiple_signatures(self):
        # negative test: Objective.value indexes `signatures[...]` ONLY by the single self.signature
        # key (used for both the config and the intact baseline -- a contrast of ONE read-out), with
        # no iteration/summation over multiple signatures. A weighted blend of read-outs (a drawn
        # profile in disguise) has nowhere to live.
        src = inspect.getsource(Objective.value)
        self.assertEqual(src.count("signatures["), src.count("[self.signature]"))  # every lookup is the one key
        self.assertNotIn("for ", src)                          # no iteration over signatures
        self.assertNotIn("sum(", src)                          # no summation/blend


class TestCoarseToFine(unittest.TestCase):
    def test_phase1_is_binary_and_phase2_grades_only_survivors(self):
        r = _run()
        p1 = [e for e in r.trajectory if e.phase == 1]
        p2 = [e for e in r.trajectory if e.phase == 2]
        # Phase 1: single circuits, binary (fully attenuated = slider 0)
        for e in p1:
            self.assertEqual(len(e.config), 1)
            self.assertTrue(all(v in (0.0, 100.0) for v in e.config.values()))
        # Phase 2: only touches survivors, and includes GRADED levels (never the whole set)
        touched = set().union(*[set(e.config) for e in p2]) if p2 else set()
        self.assertTrue(touched.issubset(set(r.survivors)))
        graded = any(v in (25.0, 50.0, 75.0) for e in p2 for v in e.config.values())
        self.assertTrue(graded)
        self.assertLessEqual(len(r.survivors), 2)              # top_k honoured; never grade all 5


class TestViableFirst(unittest.TestCase):
    def test_non_viable_configs_are_not_scored(self):
        r = _run()
        for e in r.trajectory:
            if not e.viable:
                self.assertIsNone(e.objective)                 # broken = background, never scored
        if r.best is not None:
            self.assertTrue(r.best.viable)                     # the winner is viable by construction


class TestControlArmAndHypothesisStatus(unittest.TestCase):
    def test_intact_baseline_present_and_scores_relative(self):
        r = _run()
        self.assertIn("dissociation_index", r.baseline)        # the intact control arm is recorded
        # the best score is a CONTRAST from intact, not a raw magnitude
        if r.best is not None:
            self.assertIsInstance(r.best.objective, float)

    def test_every_best_is_a_candidate_not_a_finding(self):
        self.assertEqual(_run().status, "candidate_hypothesis")

    def test_trajectory_is_logged_not_just_the_winner(self):
        r = _run()
        self.assertGreater(len(r.trajectory), len(r.survivors))  # the landscape, not just the best
        self.assertIn("seeds", r.provenance)


class TestNoModelHandle(unittest.TestCase):
    def test_search_reaches_substrate_only_through_the_primitive(self):
        # structural found-not-fitted: the search layer imports nothing that can write the model; it
        # reaches the substrate only via scan.develop_and_measure (-> set_throttle).
        # check the IMPORTS/code, not the docstring (which names set_throttle to explain the design):
        src = inspect.getsource(scan_search)
        imports = [ln for ln in src.splitlines() if ln.strip().startswith(("import ", "from "))]
        joined = "\n".join(imports)
        self.assertNotIn("substrate.model", joined)            # no model import -> no model handle
        self.assertNotIn("substrate.engine", joined)
        self.assertIn("from scan import", joined)              # reaches the substrate only via the primitive
        # and no direct model-write expression anywhere in the code
        self.assertNotIn(".weight0 =", src)
        self.assertNotIn(".connections[", src)


class TestDeterminismAndRobustnessProbe(unittest.TestCase):
    def test_deterministic(self):
        a, b = _run(), _run()
        self.assertEqual([(e.config, e.objective) for e in a.trajectory],
                         [(e.config, e.objective) for e in b.trajectory])

    def test_robustness_probe_available(self):
        # the check that promotes a candidate toward a finding is available (per-seed spread)
        out = robustness_across_seeds({"CeA": Throttle.fully_attenuated()}, "dissociation", [5, 6])
        self.assertEqual(set(out), {"5", "6"})


if __name__ == "__main__":
    unittest.main(verbosity=2)

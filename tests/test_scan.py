import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""The scan controller's trusted PRIMITIVE (Part 4 S8): develop_and_measure (manual mode).

These are the honesty-critical guards the design session settled at the boundary: the throttle
convention is pinned at both fixed points (no silent inversion), the substrate model is never
written (found-not-fitted is architectural), the throttleable set is seed-derived, the objective
is per-signature (no weighting vector), and the manipulation scope travels with the result."""
import unittest

import scan
from scan import (Throttle, throttleable_circuits, develop_and_measure, intact_baseline,
                  measure_signatures, ProfileResult, MANIPULATION_SCOPE,
                  _THROTTLEABLE_DOMAINS, _intact_seed, _neutral_env)
from affective_engine import AffectiveAgent
from affective_engine.development import develop
from affective_engine.agent import _SUBSTRATE_MODEL


def _developed_weights(config, seed):
    ag = AffectiveAgent(seed=_intact_seed())
    for cid, thr in config.items():
        ag.engine.set_throttle(cid, thr.fraction)
    develop(ag, _neutral_env(), n_episodes=48, situation_seed=seed)
    return list(ag.engine.weight)


class TestThrottleConventionIsStructural(unittest.TestCase):
    def test_slider_maps_to_fraction_both_ends(self):
        self.assertEqual(Throttle.intact().fraction, 0.0)          # 100 = full function = no throttle
        self.assertEqual(Throttle.fully_attenuated().fraction, 1.0)  # 0 = silent
        self.assertEqual(Throttle.from_slider(75).fraction, 0.25)
        self.assertTrue(Throttle.intact().is_intact)

    def test_fixed_point_intact_equals_no_throttle(self):
        # THE correctness landmine: slider 100 on every throttleable circuit must develop a
        # BIT-IDENTICAL agent to one with no throttle applied at all. If this fails, the convention
        # is inverted and every experiment runs backwards.
        allc = {c: Throttle.intact() for c in throttleable_circuits()}
        self.assertEqual(_developed_weights(allc, 11), _developed_weights({}, 11))

    def test_fixed_point_fully_attenuated_silences_the_target(self):
        ag = AffectiveAgent(seed=_intact_seed())
        ag.engine.set_throttle("CeA", Throttle.fully_attenuated().fraction)
        self.assertEqual(ag.engine._gain("CeA"), 0.0)               # output silenced


class TestFoundNotFittedIsArchitectural(unittest.TestCase):
    def test_the_substrate_model_is_never_written(self):
        before = [c.weight0 for c in _SUBSTRATE_MODEL.connections]
        develop_and_measure({c: Throttle.fully_attenuated() for c in throttleable_circuits()[:5]}, seed=3)
        develop_and_measure({}, seed=4)
        after = [c.weight0 for c in _SUBSTRATE_MODEL.connections]
        self.assertEqual(before, after)   # only set_throttle (per-instance); the seed is read-only

    def test_module_exposes_no_model_write_helper(self):
        # the primitive's only channel to the substrate is set_throttle; there is no scan-side
        # function that writes weights/connections. (Structural, not just disciplined.)
        import inspect
        src = inspect.getsource(scan)
        self.assertNotIn(".weight0 =", src)
        self.assertNotIn(".connections[", src)


class TestThrottleableSetIsSeedDerived(unittest.TestCase):
    def test_set_is_a_query_over_seed_domains_not_a_literal_list(self):
        tc = throttleable_circuits()
        self.assertGreater(len(tc), 20)                            # ~48 (the affective/empathy net + PFC)
        for cid in tc:                                            # every member is IN one of the queried domains
            self.assertIn(_SUBSTRATE_MODEL.circuits[cid].domain, _THROTTLEABLE_DOMAINS)
        # and every seed circuit in those domains is INCLUDED (derived, not curated)
        expected = {cid for cid, c in _SUBSTRATE_MODEL.circuits.items()
                    if c.domain in _THROTTLEABLE_DOMAINS}
        self.assertEqual(set(tc), expected)


class TestObjectiveIsPerSignatureNotBlended(unittest.TestCase):
    def test_signatures_are_named_individual_read_outs(self):
        sigs = measure_signatures(AffectiveAgent(seed=_intact_seed()).engine)
        self.assertIn("punishment_learning", sigs)
        self.assertIn("dissociation_index", sigs)
        for v in sigs.values():
            self.assertIsInstance(v, float)                       # each a single scalar read-out

    def test_dissociation_index_sign_is_pinned(self):
        # The objective's DIRECTION must be unambiguous or a search would hunt the wrong end of the
        # space with perfect internal consistency. Fixed point: throttling the affective-empathy
        # network RAISES dissociation_index (more reads-but-doesn't-feel). If the sign ever flips,
        # this fails -- "maximise dissociation_index" would silently mean its opposite.
        from scan import AFFECTIVE_EMPATHY
        intact = develop_and_measure({}, seed=5).signatures["dissociation_index"]
        throttled = develop_and_measure(
            {c: Throttle.fully_attenuated() for c in AFFECTIVE_EMPATHY}, seed=5
        ).signatures["dissociation_index"]
        self.assertLess(intact, throttled)                        # higher = more reads-but-doesn't-feel

    def test_no_single_blended_fitness_exists(self):
        # the objective must be ONE named read-out at a time -- structurally, the primitive keeps
        # the signatures SEPARATE (a dict of named read-outs) and carries NO single blended
        # fitness/score field where a weighted composite (a hand-drawn profile in disguise) could
        # live. The search layer will pick one named signature; it never blends them.
        sigs = measure_signatures(AffectiveAgent(seed=_intact_seed()).engine)
        self.assertGreaterEqual(len(sigs), 2)                    # kept separate, not collapsed to one score
        fields = set(ProfileResult.__dataclass_fields__)
        for blend in ("fitness", "score", "composite", "objective_value"):
            self.assertNotIn(blend, fields)                     # no place a blended objective could live


class TestPrimitiveResultAndDeterminism(unittest.TestCase):
    def test_result_records_scope_and_provenance(self):
        r = develop_and_measure({"CeA": Throttle.fully_attenuated()}, seed=7)
        self.assertIsInstance(r, ProfileResult)
        self.assertEqual(r.manipulation_scope, MANIPULATION_SCOPE)   # "nodes only" -- scope travels
        self.assertEqual(r.throttles["CeA"], 0.0)                    # recorded in slider convention
        self.assertIn("substrate", r.provenance)

    def test_deterministic_from_seed(self):
        cfg = {"CeA": Throttle.from_slider(0), "aIns": Throttle.from_slider(0)}
        self.assertEqual(develop_and_measure(cfg, 5).signatures,
                         develop_and_measure(cfg, 5).signatures)

    def test_intact_baseline_self_checks(self):
        # the control arm is intact == no throttle -- the fixed point again, at the result level
        self.assertEqual(intact_baseline(9).signatures, develop_and_measure({}, 9).signatures)


if __name__ == "__main__":
    unittest.main(verbosity=2)

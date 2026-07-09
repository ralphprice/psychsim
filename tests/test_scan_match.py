import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""The scan controller's SEARCH-FOR-MATCH arm (Part 4 S8.2). The corroboration surface: provenance
is validated, a placeholder is never reported as corroboration, the distance is per-signature (no
weighted metric = no drawn target through the back door), and the field data never touches the
mechanism (inherited: no model handle)."""
import inspect
import json
import os
import tempfile
import unittest

import scan_match
from scan_match import (load_field_pattern, scan_for_match, MatchObjective, FieldPattern,
                        _REQUIRED_PROVENANCE)
from scan import AFFECTIVE_EMPATHY, SIGNATURE_NAMES

_SUBSET = list(AFFECTIVE_EMPATHY)


def _write(d):
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    json.dump(d, f); f.close()
    return f.name


def _good(**over):
    d = {"name": "p", "signature": "punishment_learning", "target": 0.0,
         "provenance": {"source": "Journal X 2020", "population": "adult male, n=40",
                        "instrument": "PPI-R", "not_used_in_calibration": True}}
    d.update(over)
    return d


class TestProvenanceIsValidated(unittest.TestCase):
    def test_placeholder_loads_with_all_required_fields(self):
        pat = load_field_pattern("placeholder_cu_punishment.json")
        self.assertTrue(pat.is_placeholder)
        for k in _REQUIRED_PROVENANCE:
            self.assertIn(k, pat.provenance)

    def test_rejects_missing_provenance_field(self):
        for missing in _REQUIRED_PROVENANCE:
            prov = {k: v for k, v in _good()["provenance"].items() if k != missing}
            path = _write(_good(provenance=prov))
            with self.assertRaises(ValueError):
                load_field_pattern(path)
            os.unlink(path)

    def test_rejects_not_used_in_calibration_false(self):
        prov = dict(_good()["provenance"], not_used_in_calibration=False)
        path = _write(_good(provenance=prov))
        with self.assertRaises(ValueError):        # the corroboration claim requires this clause
            load_field_pattern(path)
        os.unlink(path)

    def test_rejects_unknown_signature(self):
        path = _write(_good(signature="not_a_real_signature"))
        with self.assertRaises(ValueError):
            load_field_pattern(path)
        os.unlink(path)


class TestPlaceholderNeverCorroboration(unittest.TestCase):
    def test_placeholder_result_carries_non_corroboration_status(self):
        pat = load_field_pattern("placeholder_cu_punishment.json")
        r = scan_for_match(pat, seeds=[5], circuits=_SUBSET, top_k=2)
        self.assertEqual(r.status, "placeholder_not_corroboration")   # cannot be promoted
        self.assertFalse(r.provenance["corroboration"])               # the scan never claims corroboration
        self.assertTrue(r.provenance["is_placeholder"])
        self.assertIn("PLACEHOLDER", r.provenance["field_provenance"].upper())

    def test_even_a_real_pattern_is_only_a_candidate(self):
        # a non-placeholder match is still just a candidate_hypothesis -- corroboration needs the
        # robustness gate; the scan generates candidates, it does not validate them.
        path = _write(_good(name="real_like"))
        pat = load_field_pattern(path)
        r = scan_for_match(pat, seeds=[5], circuits=_SUBSET, top_k=2)
        self.assertEqual(r.status, "candidate_hypothesis")
        self.assertFalse(r.provenance["corroboration"])
        os.unlink(path)


class TestDistanceIsPerSignatureNotWeighted(unittest.TestCase):
    def test_pattern_names_exactly_one_signature(self):
        pat = load_field_pattern("placeholder_cu_punishment.json")
        self.assertIn(pat.signature, SIGNATURE_NAMES)
        self.assertIsInstance(pat.signature, str)                    # ONE named signature, not a vector

    def test_match_objective_distance_uses_one_signature_no_blend(self):
        # inspect the CODE (after the docstring), not the prose: the distance reads a single named
        # signature, with no iteration/summation over a vector (a weighted metric would be a target).
        code = inspect.getsource(MatchObjective.value).split('"""')[-1]
        self.assertIn("self.pattern.signature", code)                # the one named signature
        self.assertNotIn("for ", code)                              # no iteration over a vector
        self.assertNotIn("sum(", code)                              # no summation/weighted metric

    def test_objective_records_by_name(self):
        pat = load_field_pattern("placeholder_cu_punishment.json")
        r = scan_for_match(pat, seeds=[5], circuits=_SUBSET, top_k=2)
        self.assertTrue(r.objective.startswith("match:"))            # recorded by name
        self.assertEqual(r.signature, pat.signature)

    def test_distance_sign_is_a_fixed_point(self):
        # orientation pin (same spirit as the throttle/dissociation fixed points): a config whose
        # signature EQUALS the target scores 0.0 -- the MAXIMUM, since fitness = -|dev - target| and
        # scan() maximises -- and a config further from the target scores STRICTLY LOWER. Makes the
        # metric's direction unambiguous.
        from scan import ProfileResult
        pat = load_field_pattern("placeholder_cu_punishment.json")
        obj = MatchObjective(pat)
        at_target = ProfileResult({}, {pat.signature: pat.target}, True, 0)
        further = ProfileResult({}, {pat.signature: pat.target + 0.3}, True, 0)
        self.assertEqual(obj.value(at_target, at_target), 0.0)       # at target = max
        self.assertLess(obj.value(further, at_target), obj.value(at_target, at_target))  # further = lower


class TestInheritsStructuralGuards(unittest.TestCase):
    def test_field_data_never_reaches_the_mechanism(self):
        # scan_match reads external data to score a distance only; it imports nothing that can write
        # the model, and reuses the search layer (which reaches the substrate only via set_throttle)
        imports = [ln for ln in inspect.getsource(scan_match).splitlines()
                   if ln.strip().startswith(("import ", "from "))]
        joined = "\n".join(imports)
        self.assertNotIn("substrate.model", joined)
        self.assertNotIn("substrate.engine", joined)
        self.assertNotIn(".set_throttle", inspect.getsource(scan_match))   # not even directly

    def test_viable_first_and_trajectory_inherited(self):
        pat = load_field_pattern("placeholder_cu_punishment.json")
        r = scan_for_match(pat, seeds=[5], circuits=_SUBSET, top_k=2)
        for e in r.trajectory:
            if not e.viable:
                self.assertIsNone(e.objective)                       # broken = background, never scored
        self.assertGreater(len(r.trajectory), 0)                     # landscape logged

    def test_deterministic(self):
        pat = load_field_pattern("placeholder_cu_punishment.json")
        a = scan_for_match(pat, seeds=[5], circuits=_SUBSET, top_k=2)
        b = scan_for_match(pat, seeds=[5], circuits=_SUBSET, top_k=2)
        self.assertEqual([(e.config, e.objective) for e in a.trajectory],
                         [(e.config, e.objective) for e in b.trajectory])


if __name__ == "__main__":
    unittest.main(verbosity=2)

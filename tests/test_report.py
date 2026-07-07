import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)   # repo root, for `import project`

"""Development reports: JSON-serialisable, honest (classifications are only Panksepp
system names -- never a psychopath/sophropath verdict), and trajectory sampling works."""
import json
import unittest

from sophropathy.engine import SimEngine

_SYSTEMS = {"SEEKING", "CARE", "PLAY", "LUST", "FEAR", "RAGE", "PANIC"}


class TestReport(unittest.TestCase):
    def test_cohort_report_json_and_no_verdict(self):
        e = SimEngine(population=40, seed=7)
        for _ in range(120):
            e.step()
        d = e.cohort_report().to_dict()
        json.dumps(d)                                          # serialisable
        self.assertEqual(sum(d["distribution"].values()), d["n"])   # counts sum to n
        # every classification is an emergent primary system -- never a verdict label
        for k in d["distribution"]:
            self.assertIn(k, _SYSTEMS)
        self.assertIn("caveat", d)

    def test_subject_report_accumulates_over_days(self):
        e = SimEngine(population=30, seed=7)
        for _ in range(200):                                   # > 1 sim-day of ticks
            e.step()
        cid = next(iter(e.subjects))
        sr = e.subject_report(cid)
        json.dumps(sr.to_dict())
        self.assertEqual(sr.cid, cid)
        self.assertGreater(len(sr.trajectory), 0)              # sampled on day rollover
        for snap in sr.trajectory:
            self.assertIn(snap.dominant, _SYSTEMS)


if __name__ == "__main__":
    unittest.main(verbosity=2)

import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""8b.5 -- params <- seed reconciliation guard.

Enforces the single-source-of-truth discipline (Part 2 S1.3) and the S2.5 two-set-point
separation, so the substrate parameters and the seed cannot silently drift and the
developed-state/params representation stays FINAL (the gate the Part 6 bank waits on).

Reconciliation outcome (8b.5): the substrate reads ALL per-circuit/connection parameters from
the seed; substrate/params.py holds only code-side dynamics scaffold. The interoceptive
state-vector set-points and perturbation gains are a DIFFERENT quantity that legitimately stays
scaffold (S2.5) -- the seed's uniform firing-rate homeostatic_setpoint is not the regulated
body-variable set-points -- and the state-vector STRUCTURE is grounded in the substrate via the
S2.5 bridge, not by copying seed numbers."""

import json
import os
import tempfile
import unittest

from substrate.model import load_substrate
from substrate import params as sub_params
from affective_engine import params as ae_params
from affective_engine import interocept

# reconcile against the CURRENT canonical seed -- the same file load_substrate() reads (v11).
# (each version has no new circuits, only new edges, so the per-circuit reconciliation is unchanged.
# Kept in lockstep with core/substrate/model._SEED_PATH.)
_SEED_PATH = os.path.join(_ROOT, "docs", "neuralnetworks", "psychsim_substrate_seed_v12.json")
_SEED = json.load(open(_SEED_PATH, encoding="utf-8"))
_MODEL = load_substrate()


class TestSubstrateReadsFromSeed(unittest.TestCase):
    """The substrate is populated FROM the seed -- one source of truth (S1.3)."""

    def test_per_circuit_params_match_the_seed_file(self):
        by_id = {c["id"]: c for c in _SEED["circuits"]}
        for cid, circ in _MODEL.circuits.items():
            s = by_id[cid]
            self.assertEqual(circ.tau_ms, float(s["time_constant_tau_ms"]))
            self.assertEqual(circ.homeostatic_setpoint, float(s["homeostatic_setpoint"]))
            self.assertEqual(circ.baseline, float(s["baseline_activation"]))
            self.assertEqual(circ.online_age, float(s.get("developmental_online_age", 0.0) or 0.0))

    def test_changing_the_seed_changes_the_model(self):
        # single source: the model is driven by the seed FILE, so a change propagates -- proof
        # the values are read, not hardcoded in a parallel copy that would drift.
        d = json.loads(json.dumps(_SEED))
        cid = d["circuits"][0]["id"]
        d["circuits"][0]["time_constant_tau_ms"] = 987.0
        tmp = None
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
                json.dump(d, fh)
                tmp = fh.name
            m = load_substrate(path=tmp)
            self.assertEqual(m.circuits[cid].tau_ms, 987.0)
            self.assertNotEqual(_MODEL.circuits[cid].tau_ms, 987.0)  # canonical model unaffected
        finally:
            if tmp:
                os.unlink(tmp)


class TestNoSeedDataDuplicatedInParams(unittest.TestCase):
    """params modules hold only code-side scaffold -- no attribute is a per-circuit copy of
    seed data (which would be the drift the reconciliation exists to prevent)."""

    def test_substrate_params_not_keyed_by_circuit_ids(self):
        circuit_ids = set(_MODEL.circuits)
        for name in dir(sub_params):
            if name.startswith("_"):
                continue
            val = getattr(sub_params, name)
            if isinstance(val, dict):
                overlap = circuit_ids & set(map(str, val.keys()))
                self.assertFalse(overlap, f"substrate.params.{name} is keyed by circuit ids {overlap}")


class TestTwoSetPointsStaySeparate(unittest.TestCase):
    """S2.5: the seed's firing-rate homeostatic_setpoint is a DIFFERENT quantity from the
    interoceptive body-variable set-points; the latter stay scaffold, never read from the seed."""

    def test_seed_homeostatic_setpoint_is_uniform_firing_rate(self):
        sps = {c.homeostatic_setpoint for c in _MODEL.circuits.values()}
        self.assertEqual(len(sps), 1, "homeostatic_setpoint is firing-rate homeostasis (uniform)")

    def test_interoceptive_setpoints_are_varied_and_not_the_seed_value(self):
        body = {v["set_point"] for v in ae_params.STATE_VARIABLES.values()}
        self.assertGreater(len(body), 1, "body-variable set-points are varied, not a single value")
        seed_sp = next(iter({c.homeostatic_setpoint for c in _MODEL.circuits.values()}))
        self.assertNotEqual(body, {seed_sp}, "body set-points must not be the seed's firing-rate value")


class TestStateVectorGroundedInSubstrate(unittest.TestCase):
    """S2.5: each interoceptive variable reads its ACTIVITY from designated REAL substrate
    circuits (grounding the structure in the substrate), while set-points stay scaffold."""

    def test_every_readout_variable_grounds_in_a_real_circuit(self):
        for var, (cids, _mode) in interocept.SUBSTRATE_READOUT.items():
            present = [c for c in cids if c in _MODEL.circuits]
            self.assertTrue(present, f"{var} reads from no real substrate circuit: {cids}")


if __name__ == "__main__":
    unittest.main()

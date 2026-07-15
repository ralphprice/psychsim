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

# reconcile against the CURRENT canonical seed -- the same file load_substrate() reads (v14).
# (the reconciliation loads the seed dynamically and is per-circuit, so it tracks whatever the
# current seed contains -- later versions may add circuits and/or edges. Kept in lockstep with
# core/substrate/model._SEED_PATH.)
_SEED_PATH = os.path.join(_ROOT, "docs", "neuralnetworks", "psychsim_substrate_seed_v14.json")
_SEED = json.load(open(_SEED_PATH, encoding="utf-8"))
_MODEL = load_substrate()

# S2.5 firing-rate homeostasis: the SCAFFOLD default every circuit carries until its own physiology is
# grounded (uniform-0.1 is a placeholder, NOT a grounding -- see the gaps register). Any circuit that
# deviates from it must be individually GROUNDED + CITED and listed here, paired with its baseline.
_SCAFFOLD_SETPOINT = 0.1
_GROUNDED_SETPOINT_CIRCUITS = {
    "LC",         # pacemaker rate 0.15 (Aston-Jones & Cohen 2005), paired with its grounded baseline
    "dPAG-GABA",  # tonic escape-threshold gate: 0.19 = intrinsic 6.2 Hz (measured under SYNAPTIC BLOCKADE --
                  # which is exactly what baseline_activation means) / 32.2 Hz dPAG strong-drive reference
                  # (Stempel & Evans et al. 2024 Curr Biol, DOI 10.1016/j.cub.2024.05.068). Paired with its
                  # baseline. Set from the electrophysiology BEFORE the floor was looked at -- not from what
                  # restores it (the LC pacemaker ruling). It then restored the floor anyway, and independently
                  # matched the paper's near-silent VGluT2+ output (0.11 Hz) at dPAG = 0.0000.
}


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

    def test_seed_setpoints_are_per_circuit_firing_rates_not_body_variables(self):
        # (a) THE SUBSTANTIVE S2.5 CLAIM: the seed's homeostatic_setpoint is PER-CIRCUIT firing-rate
        # homeostasis -- "the target mean activity of a nucleus" (MASTER Part2 S2.5) -- consumed by
        # R4-HOMEO. It is a DIFFERENT quantity from the interoceptive body-variable set-points, which
        # stay scaffold in params and are never read from the seed.
        sps = {c.homeostatic_setpoint for c in _MODEL.circuits.values()}
        self.assertTrue(all(0.0 < s <= 1.0 for s in sps))          # firing-rate targets, per-circuit
        body = {v["set_point"] for v in ae_params.STATE_VARIABLES.values()}
        self.assertNotEqual(body, sps, "body set-points are a distinct quantity from the seed's firing rates")

    def test_setpoint_deviations_from_the_scaffold_are_grounded_and_cited(self):
        # (b) THE ANTI-TUNING GUARD (v14, design-session ruled).
        # The old assertion was `len(setpoints) == 1` ("uniform"). That PINNED CURRENT STATE while
        # wearing a design guard's name: S2.5 defines the setpoint as PER-CIRCUIT ("the target mean
        # activity of a nucleus"), and uniformity held only because every circuit still carried the
        # ungrounded scaffold default. Uniformity cannot be a design principle -- different nuclei have
        # materially different intrinsic rates (LC pacemakers ~1-3 Hz tonic; DA neurons burst; cortical
        # pyramidals far lower) -- and the uniform 0.1 default demonstrably produced an artifact (see
        # LC, below). BUT the old guard had a real protective property: it caught ANY per-circuit
        # setpoint change. That anti-tuning property is PRESERVED here -- a grounded fidelity correction
        # passes; "adjust a per-circuit setpoint until it works" FAILS.
        #
        # LC (the FIRST grounded deviation; dPAG-GABA is the second -- see the list above): its setpoint is its PACEMAKER
        # RATE (0.15), grounded in the same electrophysiology as its baseline (Aston-Jones & Cohen 2005)
        # and PAIRED with it -- baseline_activation and homeostatic_setpoint describe ONE quantity (the
        # circuit's intrinsic target firing rate). At the default 0.1 the R4 homeostat fought the
        # pacemaker: LC fires on aversive events -> mean_activity rises above 0.1 -> homeo eroded LC's
        # afferents, so CeA->LC decayed IN PROPORTION TO THREAT EXPERIENCED (-7.4%/60k with events; 0.0%
        # at 0.15). That would have silently biased the core warm-vs-harsh rearing comparison.
        deviants = {cid for cid, c in _MODEL.circuits.items()
                    if c.homeostatic_setpoint != _SCAFFOLD_SETPOINT}
        self.assertEqual(deviants, _GROUNDED_SETPOINT_CIRCUITS,
                         "a per-circuit setpoint deviating from the scaffold default must be explicitly "
                         "GROUNDED + CITED and listed in _GROUNDED_SETPOINT_CIRCUITS; an unlisted "
                         "deviation is a tune, not a grounding")
        seed_circuits = {c["id"]: c for c in _SEED["circuits"]}
        for cid in deviants:
            self.assertIn("homeostatic_setpoint", seed_circuits[cid].get("function", ""),
                          f"{cid}: a grounded setpoint must carry its grounding + citation in the seed")
            # the paired-value rule: setpoint and baseline are the same quantity -> set together
            self.assertEqual(_MODEL.circuits[cid].homeostatic_setpoint, _MODEL.circuits[cid].baseline,
                             f"{cid}: a grounded setpoint must be PAIRED with its baseline")

    def test_interoceptive_setpoints_are_varied_and_not_the_seed_value(self):
        body = {v["set_point"] for v in ae_params.STATE_VARIABLES.values()}
        self.assertGreater(len(body), 1, "body-variable set-points are varied, not a single value")
        # v14: was `next(iter(seed_sps))` -- an arbitrary pick over a SET, non-deterministic the moment
        # more than one setpoint exists (exposed by grounding LC's). Compare against the whole set.
        seed_sps = {c.homeostatic_setpoint for c in _MODEL.circuits.values()}
        self.assertTrue(body.isdisjoint(seed_sps),
                        "body set-points must not be the seed's firing-rate values")


class TestStateVectorGroundedInSubstrate(unittest.TestCase):
    """S2.5: each interoceptive variable reads its ACTIVITY from designated REAL substrate
    circuits (grounding the structure in the substrate), while set-points stay scaffold."""

    def test_every_readout_variable_grounds_in_a_real_circuit(self):
        for var, (cids, _mode) in interocept.SUBSTRATE_READOUT.items():
            present = [c for c in cids if c in _MODEL.circuits]
            self.assertTrue(present, f"{var} reads from no real substrate circuit: {cids}")


if __name__ == "__main__":
    unittest.main()

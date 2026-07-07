import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""8b sub-step 1 (PsychSim_MASTER Part 2 S2.5) -- the interocept<->substrate bridge.
The interoceptive state variables read their ACTIVITY from designated live-substrate circuits;
the set-point magnitudes stay scaffold. Directional assertions only."""

import unittest

from affective_engine import params
from affective_engine.interocept import (state_from_substrate, SUBSTRATE_READOUT, VARIABLES)
from substrate.model import load_substrate
from substrate.engine import SubstrateEngine

_MODEL = load_substrate()


class TestBridge(unittest.TestCase):
    def _engine(self):
        return SubstrateEngine(_MODEL, age_years=25.0)

    def test_state_reads_from_substrate(self):
        sv = state_from_substrate(self._engine())
        # every state variable got a level in [0,1]
        for v in VARIABLES:
            self.assertIn(v, sv.levels)
            self.assertTrue(0.0 <= sv.levels[v] <= 1.0)

    def test_setpoints_stay_scaffold_not_seed_firing_rate(self):
        # S2.5: set-points are the scaffold body-variable targets (params), NOT the seed's
        # firing-rate homeostatic_setpoint (which is 0.1 for interoception circuits).
        sv = state_from_substrate(self._engine())
        self.assertEqual(sv.set_points["arousal"], params.STATE_VARIABLES["arousal"]["set_point"])
        self.assertNotEqual(sv.set_points["arousal"], 0.1)   # not the firing-rate setpoint

    def test_driving_arousal_circuits_raises_arousal_drive(self):
        calm = self._engine()
        calm.settle(20)
        aroused = self._engine()
        aroused.inject("RVLM", 0.8)
        aroused.inject("SympOut", 0.8)
        aroused.settle(20)
        d_calm = state_from_substrate(calm).drive()[1]
        d_aroused = state_from_substrate(aroused).drive()[1]
        # a sympathetically-driven substrate reads a higher arousal deviation -> higher drive
        sv_c = state_from_substrate(calm)
        sv_a = state_from_substrate(aroused)
        self.assertGreater(sv_a.levels["arousal"], sv_c.levels["arousal"])
        self.assertGreater(sv_a.deviations()["arousal"], sv_c.deviations()["arousal"])

    def test_driving_affiliation_reduces_attachment_deficit(self):
        base = self._engine()
        base.settle(20)
        bonded = self._engine()
        bonded.inject("PVN-OT", 0.8)
        bonded.inject("SEPT", 0.8)
        bonded.settle(20)
        dev_base = state_from_substrate(base).deviations()["attachment"]
        dev_bonded = state_from_substrate(bonded).deviations()["attachment"]
        # affiliation activity raises the attachment level -> smaller attachment deficit
        self.assertLess(dev_bonded, dev_base)

    def test_pain_afferent_lowers_tissue_integrity(self):
        base = self._engine()
        base.settle(20)
        hurt = self._engine()
        hurt.inject("PBN", 0.8)
        hurt.inject("pIns", 0.8)
        hurt.settle(20)
        self.assertLess(state_from_substrate(hurt).levels["tissue_integrity"],
                        state_from_substrate(base).levels["tissue_integrity"])

    def test_mapping_targets_exist_in_the_substrate(self):
        # every mapped circuit id is a real v7 circuit (the grounding is faithful)
        for var, (cids, _mode) in SUBSTRATE_READOUT.items():
            for cid in cids:
                self.assertIn(cid, _MODEL.circuits, f"{var} maps to missing circuit {cid}")


if __name__ == "__main__":
    unittest.main()

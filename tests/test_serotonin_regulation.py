import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""v13 (2.1b) -- the DRN (5-HT) node: serotonergic regulation of aggression, EMERGENT not coded.

The dorsal raphe is the principal aggression/impulsivity regulator. Under the v12a receptor-sign
convention its projections carry OPPOSITE signs across targets -- 5-HT1A INHIBITORY on the attack
area (DRN->VMHvl/CeA), 5-HT2A EXCITATORY on the PFC controllers (DRN->OFC/vmPFC/dACC) -- the exact
representability problem that forced the sign upgrade. The clinical fact (low 5-HT <-> impulsive
aggression) must EMERGE from that signed loop under a 5-HT-tone manipulation; it is NEVER a coded
`5HT -> less aggression` weight, and it is a scan_match target for the CU study.

Honesty properties (ordinal/structural only):
  * EMERGENT DAMPENING: lowering 5-HT tone (throttling DRN -- the model's own study manipulation)
    INCREASES provoked aggression, net of the competing signed pathways (DRN->VMHvl- dampens attack;
    DRN->CeA- disinhibits attack effectors; DRN->PFC+ facilitates control). The net emerges.
  * OPPOSITE SIGNS ACROSS TARGETS: DRN inhibits the attack area (5-HT1A) and excites the PFC
    controllers (5-HT2A) -- both anti-aggression, via opposite signs (only representable post-2.1a).
  * REGULATION LOOP: vmPFC/OFC/LHb -> DRN are excitatory (top-down/aversion drive onto the raphe).
  * V9 CLOSURE INTACT: adding the serotonergic regulator does not break provocation -> aggression.
"""
import unittest

from substrate.model import load_substrate, NEUROMOD_SOURCE
from substrate.engine import SubstrateEngine
from substrate.social import respond_to_substrate
from affective_engine.core import Appraisal

_MODEL = load_substrate()


def _provoked_aggress(drn_throttle, age=25.0):
    e = SubstrateEngine(_MODEL, age_years=age)
    if drn_throttle:
        e.set_throttle("DRN", drn_throttle)              # throttle DRN = LOW 5-HT tone
    return respond_to_substrate(e, Appraisal(provocation=0.9)).drives["aggress"]


class TestSerotoninDampensAggressionEmergently(unittest.TestCase):
    def test_low_5ht_increases_provoked_aggression(self):
        # lowering 5-HT tone raises provoked aggression -- the robust clinical direction, EMERGENT from
        # the signed loop (no coded 5HT->aggression). Ordinal: low-5-HT > intact, at both ages.
        for age in (2.0, 25.0):
            intact = _provoked_aggress(0.0, age)
            low5ht = _provoked_aggress(0.9, age)
            self.assertGreater(low5ht, intact, f"age {age}: low 5-HT should raise provoked aggression")

    def test_effect_is_a_regulation_not_a_switch(self):
        # 5-HT MODULATES (a graded dampening), it does not gate aggression on/off: provocation still
        # drives aggression at intact tone (the regulator dampens, it is not the driver).
        self.assertGreater(_provoked_aggress(0.0, 25.0), 0.0)


class TestOppositeSignsAcrossTargets(unittest.TestCase):
    """The property that forced the sign upgrade: one nucleus, opposite signs by target receptor."""

    def _sign(self, src, tgt):
        for c in _MODEL.connections:
            if c.source == src and c.target == tgt:
                return c.sign
        return None

    def test_drn_inhibits_attack_area_excites_pfc(self):
        self.assertEqual(self._sign("DRN", "VMHvl"), -1.0)   # 5-HT1A, dampens the attack area
        self.assertEqual(self._sign("DRN", "CeA"), -1.0)     # 5-HT1A
        self.assertEqual(self._sign("DRN", "OFC"), +1.0)     # 5-HT2A, facilitates control
        self.assertEqual(self._sign("DRN", "vmPFC"), +1.0)   # 5-HT2A
        self.assertEqual(self._sign("DRN", "dACC"), +1.0)    # 5-HT2A

    def test_pfc_raphe_loop_self_limits_through_the_interneuron(self):
        # The PFC->raphe loop runs through a DRN GAD2+ interneuron (the missing self-limiting element):
        # vmPFC/OFC EXCITE both the 5-HT neurons (direct +) AND the interneuron (+), which INHIBITS the
        # 5-HT neurons (GABA-A -). Net PFC->5-HT inhibitory; stability EMERGES from the interneuron.
        self.assertEqual(self._sign("LHb", "DRN"), +1.0)              # aversion drive
        self.assertEqual(self._sign("vmPFC", "DRN"), +1.0)           # direct excitation of 5-HT neurons
        self.assertEqual(self._sign("OFC", "DRN"), +1.0)
        self.assertEqual(self._sign("vmPFC", "DRN-GABA"), +1.0)      # excites the interneuron
        self.assertEqual(self._sign("OFC", "DRN-GABA"), +1.0)
        self.assertEqual(self._sign("DRN-GABA", "DRN"), -1.0)        # feed-forward inhibition (GABA-A)
        self.assertEqual(self._sign("DRN", "VTA"), -1.0)            # 5-HT dampens DA reward responding

    def test_silencing_the_interneuron_lets_the_loop_run_hot(self):
        # THE proof the stability is anatomy, not a tuned weight: with the interneuron active the raphe
        # settles at a tonic level; silence it and the PFC->DRN excitation is revealed (DRN runs hot).
        e = SubstrateEngine(_MODEL, age_years=25.0); e.clear_inputs(); e.settle(80)
        tonic = e.activation["DRN"]
        es = SubstrateEngine(_MODEL, age_years=25.0); es.clear_inputs()
        es.set_throttle("DRN-GABA", 1.0); es.settle(80)             # silence the interneuron
        self.assertGreater(es.activation["DRN"], tonic + 0.3)       # runs hot without the cap

    def test_drn_registered_as_serotonergic_source(self):
        self.assertEqual(NEUROMOD_SOURCE.get("5HT"), ["DRN"])


class TestClosureIntactWithRegulator(unittest.TestCase):
    def test_provocation_still_drives_aggression(self):
        # adding the inhibitory serotonergic regulator must NOT over-suppress the attack circuit:
        # provocation still makes aggression the dominant impulse (v9 closure preserved).
        b = respond_to_substrate(SubstrateEngine(_MODEL, age_years=25.0), Appraisal(provocation=0.9))
        self.assertGreater(b.drives["aggress"], b.drives["avoid"])


if __name__ == "__main__":
    unittest.main()

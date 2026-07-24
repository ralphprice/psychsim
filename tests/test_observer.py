import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""Phase 6 additive (PsychSim_MASTER App. D.2) -- the observer read-out. Outcome categories
are MEASURED over an agent, engine-agnostically, and NEVER fed back. Directional only."""

import copy
import unittest

from affective_engine.observer import (BehaviourProfile, triarchic, callous_unemotional,
                                        empathy, read_out, observe_agent)
from affective_engine.core import shared_root_seed, sophropathic_seed, psychopathic_seed
from affective_engine.agent import AffectiveAgent
from sophropathy.society import typical_child_seed


def _agent(seed_fn):
    return AffectiveAgent(seed_fn(), temperament_seed=99)


class TestConstructsAreBoundedReadouts(unittest.TestCase):
    def test_read_out_shape_no_single_verdict(self):
        r = read_out(BehaviourProfile())
        for key in ("triarchic", "distress_cue_amygdala_reactivity", "aggression",
                    "passive_avoidance_deficit"):
            self.assertIn(key, r)
        # deliberately NO single "psychopathy" verdict baked in
        self.assertNotIn("psychopathy", r)
        # ★ SUSPENDED (CEl-discrimination, ruled): empathy/CU are declared NOT IMPLEMENTED and removed as
        # measures (no vicarious pathway in the substrate); assert they are NOT reported.
        self.assertNotIn("empathy", r)
        self.assertNotIn("callous_unemotional", r)

    def test_all_metrics_bounded(self):
        bp = BehaviourProfile(fear=0.9, seeking=0.8, care=0.1, restraint=0.2,
                              moral_orientation=0.1, reactive_aggression=0.9,
                              instrumental_aggression=0.8, vicarious_response=0.1)
        tri = triarchic(bp)
        for v in tri.values():
            self.assertTrue(0.0 <= v <= 1.0)
        # empathy/CU boundedness dropped: those constructs are SUSPENDED (not implemented).


class TestConstructsTrackTheSignals(unittest.TestCase):
    def test_boldness_rises_as_fear_falls(self):
        bold = triarchic(BehaviourProfile(fear=0.1, seeking=0.7))["boldness"]
        timid = triarchic(BehaviourProfile(fear=0.9, seeking=0.7))["boldness"]
        self.assertGreater(bold, timid)

    @unittest.skip("SUSPENDED (CEl-discrimination, ruled): empathy/callous_unemotional are NOT IMPLEMENTED -- "
                   "the vicarious_response term is amygdala aversive tone, not vicarious distress (no vicarious "
                   "pathway in the substrate). Re-enable once the distress-perception -> pSTS -> rSMG-TPJ -> aIns "
                   "pathway is built and the construct is re-derived on it.")
    def test_callous_unemotional_rises_as_empathy_conscience_fall(self):
        cu_low = callous_unemotional(BehaviourProfile(vicarious_response=0.9,
                                                      moral_orientation=0.9))
        cu_high = callous_unemotional(BehaviourProfile(vicarious_response=0.1,
                                                       moral_orientation=0.1))
        self.assertGreater(cu_high, cu_low)

    def test_disinhibition_rises_as_restraint_falls(self):
        d_lo = triarchic(BehaviourProfile(restraint=0.9))["disinhibition"]
        d_hi = triarchic(BehaviourProfile(restraint=0.1, reactive_aggression=0.6))["disinhibition"]
        self.assertGreater(d_hi, d_lo)


class TestPluginReportIntegration(unittest.TestCase):
    def test_subject_report_exposes_the_observer_readout(self):
        # Phase 7: the sophropathy plugin's subject report carries the App. E.5 observer
        # constructs (measured, never fed back).
        from sophropathy.report import SubjectReport
        r = SubjectReport(cid="s1", temperament="fearless", home="warm",
                          observer=read_out(BehaviourProfile()))
        d = r.to_dict()
        self.assertIn("observer", d)
        self.assertIn("triarchic", d["observer"])


class TestLegacyAdapterNeverFedBack(unittest.TestCase):
    def test_observe_does_not_mutate_the_agent(self):
        ag = _agent(shared_root_seed)
        before = list(ag.engine.weight)                # the developed substrate connectome
        _ = observe_agent(ag)
        self.assertEqual(list(ag.engine.weight), before)   # measurement, not a driver

    def test_reads_emergent_substrate(self):
        r = observe_agent(_agent(shared_root_seed))
        self.assertIn("triarchic", r)
        self.assertTrue(0.0 <= r["triarchic"]["boldness"] <= 1.0)

    def test_fearless_reads_bolder_than_typical(self):
        # the fearless proto-disposition reads higher boldness than the control child --
        # a MEASUREMENT over emergent substrate, not a coded outcome.
        fearless = observe_agent(_agent(shared_root_seed))["triarchic"]["boldness"]
        typical = observe_agent(_agent(typical_child_seed))["triarchic"]["boldness"]
        self.assertGreater(fearless, typical)


if __name__ == "__main__":
    unittest.main()

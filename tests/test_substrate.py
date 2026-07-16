import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""Sub-phase 8a (PsychSim_MASTER Part 2, S2.6) -- STANDALONE substrate acceptance.

MECHANISTIC criteria only (the substrate alone produces circuit activity, not psychological
phenomena -- those are 8b). The load-bearing check is the honesty wall at the dynamics level:
plasticity is meaning-blind and every modulator is a circuit output, not a set scalar."""

import io
import tokenize
import unittest

from substrate.model import load_substrate
from substrate.engine import SubstrateEngine
from substrate import plasticity as P

_MODEL = load_substrate()


class TestInstantiation(unittest.TestCase):
    def test_loads_the_v9_substrate(self):
        m = _MODEL
        # v14 Expression Phase A -- the DELTA, named (a pin that records a number is a speed bump; a pin
        # that records WHY is a guard). 83 -> 88:  -PAG (lumped; its own function field named two opposite
        # columns)  +vlPAG  +dPAG  +vlPAG-GABA (CeA's cited Tovote-2016 target cell)  +dPAG-GABA (the
        # tonically-active escape-threshold gate, Stempel & Evans 2024)  +NuAmb-vocal  +NuFac.
        # NuAmb -> NuAmb-cardiac is a RENAME (mis-scoped, not mixed) -- no count change.
        # v14 Expression Phase B, 88 -> 89:  +NRA (nucleus retroambiguus) -- the PAG's premotor relay to the
        # vocal motoneurons. The spec had wired PAG -> NuAmb-vocal DIRECTLY; that projection does not exist
        # (Holstege: the PAG uses the NRA as a relay; kainic acid into NRA ABOLISHES PAG-induced vocalisation).
        # v14 Expression Phase B+, 89 -> 90:  +dACC-GABA -- the missing cortical feedback interneuron (principle
        # 1). Grounding BA->dACC gave dACC real drive and it SATURATED (no local inhibition; 3 excitatory
        # afferents), driving dlPFC to ceiling and manufacturing a 'divergence emerges' artifact. dACC-GABA is
        # the cortical E/I brake (mirrors dlPFC-GABA; Ferguson & Gao 2018) -- FIRST of a systemic gap (the
        # cortical brake layer is 2-of-11; gaps-register S18), not the last closed.
        self.assertEqual(len(m.circuits), 90)
        self.assertGreater(len(m.connections), 130)     # circuit->circuit edges
        self.assertGreater(len(m.input_edges), 15)      # sensory channel entry edges
        # inhibitory nuclei derived from principal transmitter (GABAergic)
        inh = [c.id for c in m.circuits.values() if c.sign < 0]
        self.assertIn("DStr", inh)
        self.assertIn("CeA", inh)
        self.assertNotIn("LA", inh)                     # glutamatergic projection

    def test_gaps_register_carried_not_invented(self):
        self.assertTrue(_MODEL.gaps_register)           # the seed's audit trail is preserved
        self.assertTrue(any("connectome gap" in w for w in _MODEL.warnings))

    def test_live_set_gates_by_age(self):
        young = SubstrateEngine(_MODEL, age_years=0.0)
        adult = SubstrateEngine(_MODEL, age_years=25.0)
        self.assertLess(len(young.live_circuits()), len(adult.live_circuits()))
        self.assertEqual(len(adult.live_circuits()), 90)   # v14 Phase B+: all 90 online by adulthood (+dACC-GABA online 5.0; see the named delta above)


class TestLeakyIntegrator(unittest.TestCase):
    def test_activation_propagates_and_relaxes(self):
        e = SubstrateEngine(_MODEL, age_years=25.0)
        e.inject_channel("IN-GUST", 0.3)
        e.settle(60)
        driven = e.activity("NAc-shell")
        self.assertGreater(driven, _MODEL.circuits["NAc-shell"].baseline)  # propagated
        e.clear_inputs()
        e.settle(200)
        self.assertLess(e.activity("NAc-shell"), driven)                    # relaxes

    def test_leaf_circuit_relaxes_to_baseline(self):
        # a circuit with no live incoming edges is a pure leaky integrator -> returns to baseline
        m = _MODEL
        leaves = [cid for cid in m.circuits
                  if not m.incoming.get(cid) and not m.incoming_channel.get(cid)]
        self.assertTrue(leaves)
        e = SubstrateEngine(m, age_years=25.0)
        lf = leaves[0]
        e.inject(lf, 0.5)
        e.settle(20)
        self.assertGreater(e.activity(lf), m.circuits[lf].baseline)
        e.clear_inputs()
        e.settle(100)
        self.assertAlmostEqual(e.activity(lf), m.circuits[lf].baseline, places=2)

    def test_bounded_and_homeostatic_rest(self):
        e = SubstrateEngine(_MODEL, age_years=8.0)
        for _ in range(1500):
            e.step()                                    # no input at all
        acts = list(e.activation.values())
        self.assertTrue(all(0.0 <= a <= 1.0 for a in acts))         # bounded
        mean = sum(acts) / len(acts)
        self.assertLess(mean, 0.25)                     # homeostasis keeps rest low (near setpoint)


class TestPlasticity(unittest.TestCase):
    def test_coactive_connection_strengthens(self):
        m = _MODEL
        e = SubstrateEngine(m, age_years=4.0)
        j = 0
        k = m.connections[j]
        before = e.weight[j]
        e.inject(k.source, 0.9)
        e.settle(300)
        self.assertGreater(e.weight[j], before)         # BCM potentiation of co-active pair

    def test_weights_stay_bounded_over_a_long_run(self):
        e = SubstrateEngine(_MODEL, age_years=6.0)
        e.inject_channel("IN-GUST", 0.9)
        e.inject_channel("IN-SOMATO", 0.7)
        for _ in range(1200):
            e.step()
        for j, k in enumerate(_MODEL.connections):
            self.assertTrue(k.bounds[0] <= e.weight[j] <= k.bounds[1])

    def test_theta_tracks_the_circuits_own_activity(self):
        e = SubstrateEngine(_MODEL, age_years=25.0)
        cid = _MODEL.connections[0].target
        e.inject(_MODEL.connections[0].source, 0.6)
        e.settle(80)
        # the BCM threshold has moved up toward the (now elevated) activity of the circuit
        self.assertGreater(e.theta[cid], _MODEL.circuits[cid].baseline)

    def test_plasticity_rules_are_meaning_blind(self):
        # source-level: strip comments AND string literals (docstrings), then confirm the CODE
        # references no circuit identity/meaning or outcome -- only activity/weights/age.
        src = _O.path.join(_ROOT, "core", "substrate", "plasticity.py")
        with open(src, "rb") as fh:
            names = set()
            for tok in tokenize.tokenize(fh.readline):
                if tok.type == tokenize.NAME:
                    names.add(tok.string.lower())
        for banned in ("domain", "fear", "threat", "reward", "callous", "psychopath",
                       "aggression", "outcome", "meaning", "valence"):
            self.assertNotIn(banned, names, f"plasticity rule references '{banned}'")


class TestTemperamentIsNotAGateDial(unittest.TestCase):
    """v14 (ruled): the TEMPERAMENT throttle is a MODEL CLAIM about what varies between individuals -- and a
    local inhibitory GATE is not a thing an individual is 'less of'. Throttling a gate DISINHIBITS its target,
    so a 'less reactive' dial yields MORE output: directionally perverse. The alpha2 argument verbatim -- a
    structural element is not a reactivity dial any more than it is a learned association. (The SCAN is a
    different act -- an experiment, not a claim -- and gates stay lesionable there; see test_scan.)"""

    def test_temperament_does_not_throttle_structural_gates(self):
        from substrate.seeding import seed_substrate
        low = {"THREAT": 0.1, "ANXIETY": 0.1, "SEEKING": 0.1, "FRUSTRATION": 0.1,
               "CARE": 0.1, "SOCIAL_LOSS": 0.1, "CONTROL": 0.1, "INSTRUMENTAL_CONTROL": 0.1}
        eng = SubstrateEngine(_MODEL, age_years=25.0)
        seed_substrate(eng, low)                       # every dial at the floor
        gates = [cid for cid, c in _MODEL.circuits.items() if c.structural_element]
        self.assertTrue(gates)
        for cid in gates:                              # no gate is touched by any dial...
            self.assertEqual(eng.throttle.get(cid, 0.0), 0.0,
                             f"{cid}: a structural gate must not be a reactivity dial")
        # ...while the DRIVEN circuits of those same domains are throttled (the dial still works)
        self.assertGreater(eng.throttle.get("CeA", 0.0), 0.0)

    def test_the_gate_class_is_marked_in_the_seed_not_inferred_in_code(self):
        # data, like dominant_receptor -- so the exclusion stays derived and never becomes an id list
        gates = {cid for cid, c in _MODEL.circuits.items() if c.structural_element}
        self.assertIn("ITC", gates)          # the extinction gate + the cell the PFC control route runs through
        self.assertIn("dPAG-GABA", gates)    # the escape threshold


class TestDevelopmentalGating(unittest.TestCase):
    def test_eta_high_early_low_adult(self):
        self.assertGreater(P.eta("amygdala_high_early", 2.0), P.eta("amygdala_high_early", 30.0))

    def test_eta_adolescent_peak(self):
        s = "da_system_high_adolescent_peak"
        self.assertGreater(P.eta(s, 16.0), P.eta(s, 5.0))
        self.assertGreater(P.eta(s, 16.0), P.eta(s, 35.0))

    def test_eta_pfc_protracted_low_early_high_late(self):
        s = "pfc_low_early_high_late"
        self.assertGreater(P.eta(s, 22.0), P.eta(s, 5.0))

    def test_eta_flat_schedule_is_roughly_constant(self):
        s = "brainstem_low_flat"
        self.assertAlmostEqual(P.eta(s, 2.0), P.eta(s, 40.0), places=6)


class TestNeuromodulatorDiscipline(unittest.TestCase):
    def test_modulator_is_a_circuit_output(self):
        # R5 danger point: the DA modulator IS the live output of VTA/SNc, not a set scalar.
        e = SubstrateEngine(_MODEL, age_years=25.0)
        e.inject("VTA", 0.8)
        e.settle(30)
        expected = (e.activity("VTA") + e.activity("SNc")) / 2.0
        self.assertAlmostEqual(e.neuromod_output("DA"), expected, places=6)

    def test_modulator_tracks_the_source_circuit(self):
        # driving the neuromodulator source circuit changes the modulator (wired from activity)
        e = SubstrateEngine(_MODEL, age_years=25.0)
        low = e.neuromod_output("DA")
        e.inject("VTA", 0.9)
        e.settle(30)
        self.assertGreater(e.neuromod_output("DA"), low)

    def test_ungated_connections_have_unit_modulator(self):
        e = SubstrateEngine(_MODEL, age_years=25.0)
        self.assertEqual(e.neuromod_output("none"), 1.0)

    def test_consolidate_takes_modulator_as_an_argument(self):
        # structural guarantee: the rule cannot fetch or set the modulator; it is passed in.
        import inspect
        self.assertIn("modulator", inspect.signature(P.consolidate).parameters)


if __name__ == "__main__":
    unittest.main()

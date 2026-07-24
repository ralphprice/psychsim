import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""Lump #13 -- the CeL winner-take-all selection microcircuit.

The central amygdala was one lumped node whose saturated GABAergic output FLATTENED all six of its
targets rather than driving them. It is now split into an afferent/selector division (CEl, carrying all
17 external afferents and the SOM+/PKC-delta+ mutually-inhibitory populations) and a differentiated
output stage (CEm-freeze -> vlPAG-GABA, CEm-active -> HYPdm).

These tests existed nowhere when the microcircuit shipped: the entire test delta for the build was 21
lines of find-and-replace to keep pre-existing tests passing, so the suite would have stayed green with
the selector completely broken. That is the "a passing test on an incomplete substrate is MISLEADING"
failure arrived at by the back door, and this file is the repair.

★ THE LOAD-BEARING TEST IS `test_the_winner_follows_the_drive_balance`. Building a winner-take-all
correctly is NOT evidence that the selection emerges -- a WTA whose outcome is fixed by one ungrounded
weight would look identical in every structural assertion. So the emergence is verified by PERTURBING
THE DRIVES AND WATCHING THE SELECTOR FOLLOW, never by observing that the circuit was built right.

Ordinal/structural assertions only; no magnitude is pinned."""

import unittest

from arena import intact_seed
from affective_engine.agent import AffectiveAgent
from substrate.social import felt_response
from substrate.model import load_substrate
from scan import Throttle

_MODEL = load_substrate()
_CONNS = {(c.source, c.target): c for c in _MODEL.connections}


def _settle(trig, throttles=None):
    ag = AffectiveAgent(seed=intact_seed(), temperament_seed=1)
    for k, v in (throttles or {}).items():
        ag.engine.set_throttle(k, v)
    felt_response(ag.engine, dict(trig), 25.0, getattr(ag, "_rest_baseline", None))
    return ag.engine.activation


class TestTheSelectorSelects(unittest.TestCase):
    def test_different_contexts_produce_different_winners(self):
        # the minimum claim: the microcircuit is not stuck on one population
        thr = _settle({"threat": 1.0})
        aff = _settle({"affiliation": 1.0})
        self.assertGreater(thr["CEl-SOM"], thr["CEl-PKCd"])      # threat -> passive/freezing arm
        self.assertGreater(aff["CEl-PKCd"], aff["CEl-SOM"])      # affiliation -> the other arm

    def _crossover(self, affiliation):
        """The threat level at which SOM+ overtakes PKCd+, or None if it never does."""
        prev = None
        for i in range(21):
            a = _settle({"threat": i / 20.0, "affiliation": affiliation})
            cur = a["CEl-SOM"] > a["CEl-PKCd"]
            if prev is not None and cur and not prev:
                return i / 20.0
            prev = cur
        return None

    def test_the_winner_follows_the_drive_balance(self):
        # ★ THE EMERGENCE TEST. A winner-take-all whose outcome is fixed by one ungrounded weight would
        # satisfy every OTHER assertion in this file. What distinguishes real competition is that the
        # winner MOVES WITH THE DRIVES -- so this asserts a BOUNDARY EXISTS in the drive space and that it
        # MOVES in the predicted direction, rather than pinning the coordinate where the flip happens.
        # That distinction is not pedantry: this test originally hardcoded threat=0.25 as the flip point,
        # and adding the grounded CRF+ population moved the boundary to 0.35 -- the PROPERTY was intact
        # and the coordinate was not. A test that pins the coordinate breaks on legitimate structural
        # change and tempts you to bump the number, which is fitting.
        # (An audit argued the selection was decided solely by the PVN-OT edge because LA and PBN carry
        # equal WEIGHTS. That compared static weights; drive is weight x SOURCE ACTIVATION. The boundary
        # below moves with threat alone, PVN-OT untouched, which is the refutation.)
        alone = self._crossover(affiliation=0.0)
        self.assertIsNotNone(alone, "no crossover anywhere in the drive range -- the winner is fixed, "
                                    "which means the selection is not emerging from the drives")
        self.assertGreater(alone, 0.0)          # PKCd+ leads at rest...
        self.assertLess(alone, 1.0)             # ...and SOM+ takes over within range: a real contest

        # ...and a competing drive MOVES the boundary against SOM+ (either later, or out of range)
        contested = self._crossover(affiliation=0.5)
        self.assertTrue(contested is None or contested > alone,
                        f"affiliation did not push the boundary against SOM+ ({alone} -> {contested})")

    def test_the_margin_is_graded_by_drive_not_saturated(self):
        # the competition is continuous in the drive, not a latch: SOM+'s lead over PKCd+ grows with threat
        m = [_settle({"threat": t})["CEl-SOM"] - _settle({"threat": t})["CEl-PKCd"] for t in (0.25, 0.5, 1.0)]
        self.assertLess(m[0], m[1])
        self.assertLess(m[1], m[2])


class TestItIsAWinnerTakeAllNotADivider(unittest.TestCase):
    def test_the_loser_is_suppressed_not_merely_lower(self):
        # what distinguishes a WTA from a divider: under a strongly lateralised context the LOSER falls
        # BELOW ITS OWN RESTING LEVEL -- it is actively suppressed, not just out-competed.
        rest = _settle({})["CEl-SOM"]
        aff = _settle({"affiliation": 1.0})["CEl-SOM"]
        self.assertLess(aff, rest)

    def test_silencing_one_limb_frees_the_other(self):
        # the silence-the-element counterfactual: the mutual inhibition must be LOAD-BEARING, not
        # decorative. Remove PKCd+ and SOM+ must rise -- if it does not, the "competition" does nothing.
        intact = _settle({"affiliation": 1.0})["CEl-SOM"]
        lesion = _settle({"affiliation": 1.0}, {"CEl-PKCd": Throttle.fully_attenuated().fraction})["CEl-SOM"]
        self.assertGreater(lesion, intact)


class TestTheMicrocircuitIsWiredAsClaimed(unittest.TestCase):
    def test_mutual_inhibition_is_bidirectional_and_inhibitory(self):
        for a, b in (("CEl-SOM", "CEl-PKCd"), ("CEl-PKCd", "CEl-SOM")):
            e = _CONNS.get((a, b))
            self.assertIsNotNone(e, f"{a}->{b} missing: there is no mutual inhibition")
            self.assertLess(e.sign, 0.0, f"{a}->{b} must be inhibitory")

    def test_the_routing_is_selective_not_blanket(self):
        # THE DEFECT THE UN-LUMPING FIXED: one interneuron population delivering a BLANKET brake.
        # ★ UPDATED after CEl-SOM->CEm-active was REMOVED on a citation (Fadok 2017: SOM+ suppresses flight by
        # LOCAL inhibition within CeL, not by projecting to a CeM output population). The selector now reaches
        # the output stage through ONE grounded arm -- PKC-delta+ gating CEm-freeze (Haubensak 2010) -- and the
        # blanket-brake property is what still matters: that arm must gate ONE output, not all of them.
        pkc = {t for (s, t) in _CONNS if s == "CEl-PKCd" and t.startswith("CEm")}
        som = {t for (s, t) in _CONNS if s == "CEl-SOM" and t.startswith("CEm")}
        self.assertEqual(pkc, {"CEm-freeze"}, "the grounded arm must gate the freeze output and only that")
        self.assertEqual(som, set(), "SOM+ acts by LOCAL CeL inhibition; a CeM projection is refuted (Fadok 2017)")

    def test_the_differential_afferents_exist_and_are_excitatory(self):
        # the structural precondition for contextual selection: without DIFFERENTIAL drive the WTA has
        # nothing to arbitrate on and its winner would be set by noise or by a fixed asymmetry.
        for src, tgt in (("LA", "CEl-SOM"), ("PBN", "CEl-PKCd")):
            e = _CONNS.get((src, tgt))
            self.assertIsNotNone(e, f"{src}->{tgt} missing: the selector has no differential drive")
            self.assertGreater(e.sign, 0.0)

    def test_the_shared_drive_carries_no_built_in_preference(self):
        # CEl drives BOTH populations byte-identically, so any preference must come from the differential
        # afferents (above) rather than from a thumb on the scale in the shared limb.
        a, b = _CONNS[("CEl", "CEl-SOM")], _CONNS[("CEl", "CEl-PKCd")]
        self.assertAlmostEqual(a.weight0, b.weight0, places=9)
        self.assertEqual(a.sign, b.sign)

    def test_oxytocin_reaches_the_freezing_arm_mechanistically(self):
        # Knobloch 2012's "OT attenuates fear" is reproduced as MECHANISM, not asserted: OT excites the
        # population that gates the freezing output, so the fear reduction falls out of the microcircuit.
        e = _CONNS.get(("PVN-OT", "CEl-PKCd"))
        self.assertIsNotNone(e)
        self.assertGreater(e.sign, 0.0)
        self.assertIn("CEm-freeze", {t for (s, t) in _CONNS if s == "CEl-PKCd"})

    def test_the_grounded_gate_onto_the_freeze_output_is_inhibitory(self):
        # the surviving, cited arm: PKC-delta+ inhibits the CeM freeze output (Haubensak 2010), so when SOM+
        # wins the local competition PKC-delta+ is suppressed and the freeze output is RELEASED.
        self.assertLess(_CONNS[("CEl-PKCd", "CEm-freeze")].sign, 0.0)


class TestTheS56ExitMeasurement(unittest.TestCase):
    """★ THE S56 EXIT -- freezing and active defence as DISTINCT emergent selector states.

    This replaces two earlier honest negatives, both now resolved by grounded anatomy rather than by
    weakening the criterion: (1) the freezing column was dead until PL->vlPAG gave it excitation, and
    (2) the active arm had no selector until the CRF+ population -- the missing half of Fadok 2017's
    competing pair -- was added.

    The criterion is the DISSOCIATION, asserted ordinally: each context must drive its OWN column and
    NOT the other. No magnitude is pinned, because the point was never "freezing is large" -- it was
    that one activation could not previously serve two opposite modes."""

    def test_freezing_and_active_defence_are_distinct_selector_states(self):
        thr = _settle({"threat": 1.0})           # nociceptive threat -> passive defence
        pro = _settle({"thwarting": 1.0})        # provocation -> active defence
        # threat drives the FREEZING column and not the flight column
        self.assertGreater(thr["vlPAG"], thr["dPAG"])
        self.assertGreater(thr["Mc"], _settle({})["Mc"])          # freezing effector above rest
        # provocation drives the FLIGHT/ATTACK column and not the freezing column
        self.assertGreater(pro["dPAG"], pro["vlPAG"])
        self.assertGreater(pro["VMHvl"], thr["VMHvl"])
        # ...and they do not trade: neither context drives BOTH columns. ★ RE-BASELINED to the ORDINAL form
        # (vicarious-pathway build, ruled): was assertEqual(...,0.0). An exact-zero on a continuous quantity is
        # brittle BY CONSTRUCTION -- the grounded vicarious pathway (aIns->CEl etc.) adds a hair of tonic drive
        # (pro vlPAG 0.0->0.0027) that breaks == 0.0 without touching the CLAIM. The claim is the DISTINCTION:
        # the off-column stays below the on-column. Asserting the relation survives future grounded changes; a
        # loosened number would be the same brittle shape at a new value.
        self.assertLess(thr["dPAG"], thr["vlPAG"])     # threat: flight column stays below the freezing column
        self.assertLess(pro["vlPAG"], pro["dPAG"])     # provocation: freezing column stays below the flight column

    def test_the_crf_population_is_load_bearing_for_the_flight_column(self):
        # silence-the-element: the flight column must depend on CRF+ disinhibition, or the "selection"
        # of active defence is really just the provocation->VMHvl->dPAG route with CRF+ decorative.
        intact = _settle({"thwarting": 1.0})["dPAG"]
        lesion = _settle({"thwarting": 1.0}, {"CEl-CRF": Throttle.fully_attenuated().fraction})["dPAG"]
        self.assertGreater(intact, lesion)
        self.assertEqual(lesion, 0.0)            # without CRF+ the column cannot open at all

    def test_the_flight_column_needs_drive_AND_disinhibition(self):
        # the lesson the freezing column taught, asserted so it cannot regress: disinhibition alone
        # produces nothing. CRF+ is MORE active under threat than provocation, yet dPAG fires only under
        # provocation -- because that is when VMHvl supplies the excitatory drive the gate releases.
        thr = _settle({"threat": 1.0})
        pro = _settle({"thwarting": 1.0})
        self.assertGreater(thr["CEl-CRF"], pro["CEl-CRF"])        # more disinhibition under threat...
        self.assertEqual(thr["dPAG"], 0.0)                        # ...and yet no flight, for lack of drive
        self.assertGreater(pro["VMHvl"], 0.0)                     # provocation supplies the drive
        self.assertGreater(pro["dPAG"], 0.0)                      # so the column opens

    def test_the_crf_population_brakes_its_competitor(self):
        # the competing pair is genuinely competitive: removing CRF+ lets SOM+ run to saturation
        intact = _settle({"threat": 1.0})["CEl-SOM"]
        lesion = _settle({"threat": 1.0}, {"CEl-CRF": Throttle.fully_attenuated().fraction})["CEl-SOM"]
        self.assertGreater(lesion, intact)
        self.assertLess(intact, 1.0)             # and the brake is what keeps SOM+ off its ceiling


if __name__ == "__main__":
    unittest.main()

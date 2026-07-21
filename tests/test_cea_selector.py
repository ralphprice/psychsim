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

    def test_the_winner_follows_the_drive_balance(self):
        # ★ THE EMERGENCE TEST. A winner-take-all whose outcome is decided by one ungrounded weight would
        # satisfy every OTHER assertion in this file. What distinguishes real competition is that the
        # winner MOVES WITH THE DRIVES -- so perturb the drive balance and watch the selector follow, in
        # BOTH directions, with no weight touched.
        # (An audit argued the selection was decided solely by the PVN-OT edge because LA and PBN carry
        # equal WEIGHTS. That compared static weights; drive is weight x SOURCE ACTIVATION. Raising
        # threat alone flips the winner with PVN-OT untouched, which is the refutation.)
        low_t = _settle({"threat": 0.0, "affiliation": 0.0})
        hi_t = _settle({"threat": 1.0, "affiliation": 0.0})
        self.assertGreater(low_t["CEl-PKCd"], low_t["CEl-SOM"])  # no threat -> PKCd+ leads
        self.assertGreater(hi_t["CEl-SOM"], hi_t["CEl-PKCd"])    # threat alone FLIPS it (no OT change)

        # ...and the flip goes back the other way when the competing drive rises
        mid = _settle({"threat": 0.25, "affiliation": 0.0})
        mid_aff = _settle({"threat": 0.25, "affiliation": 0.5})
        self.assertGreater(mid["CEl-SOM"], mid["CEl-PKCd"])
        self.assertGreater(mid_aff["CEl-PKCd"], mid_aff["CEl-SOM"])   # affiliation flips it back

        # ...and MORE threat flips it once more: the boundary tracks the ratio, not a fixed side
        strong = _settle({"threat": 1.0, "affiliation": 0.5})
        self.assertGreater(strong["CEl-SOM"], strong["CEl-PKCd"])

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
        # THE DEFECT THE UN-LUMPING FIXED: one interneuron population delivering a BLANKET brake. Each
        # population must gate a DIFFERENT output, or the lump is merely relocated.
        som = {t for (s, t) in _CONNS if s == "CEl-SOM" and t.startswith("CEm")}
        pkc = {t for (s, t) in _CONNS if s == "CEl-PKCd" and t.startswith("CEm")}
        self.assertTrue(som and pkc)
        self.assertNotEqual(som, pkc, "both populations gate the same CEm target -- that is blanket, not routed")
        self.assertEqual(som & pkc, set(), "a population gating BOTH outputs re-creates the blanket brake")

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

    def test_the_two_output_populations_are_oppositely_gated(self):
        # the whole point of the un-lumping: one activation can no longer drive both opposite-signed
        # outputs, because the outputs are gated by populations that cannot both be active.
        self.assertLess(_CONNS[("CEl-PKCd", "CEm-freeze")].sign, 0.0)
        self.assertLess(_CONNS[("CEl-SOM", "CEm-active")].sign, 0.0)


class TestTheOutputStageIsStillFloored(unittest.TestCase):
    """★ THE HONEST NEGATIVE. The selector selects (verified above, by perturbation), but the exit
    measurement of the S56 descent -- freezing and aggression DRIVABLE as distinct output states -- is
    NOT met: both CEm populations sit at or near their floor in every context (max ~0.07 across a full
    threat x affiliation sweep). Encoding this as a passing "outputs are low" test would certify the
    defect; encoding it as the FAILING claim keeps the debt visible and self-clearing.

    DIAGNOSED CAUSE (measured, not assumed): the disinhibitory motif is built without the drive it is
    meant to release, three times over -- CEm's excitation is outweighed ~2:1 by its gate, and vlPAG (the
    freezing column itself) has exactly ONE excitatory afferent, VMH, which is not threat-driven and sits
    flat at 0.112 under both threat and provocation. So CEm-freeze correctly drives vlPAG-GABA to 0.000
    -- perfect disinhibition -- and vlPAG still cannot fire, because there is no drive to release.

    RESOLUTION CONDITION: a grounded excitatory driver for the freezing column (whether the CEm-freeze
    population itself proves sufficient once CEm is properly driven, or vlPAG needs a separately-grounded
    afferent -- the mPFC prelimbic/infralimbic projection is the canonical candidate). Do NOT resolve this
    by lowering the gate weights: the blanket-brake fix was the mutual-inhibition MECHANISM, and the same
    discipline applies here -- build the missing drive, do not shrink the inhibition."""

    @unittest.expectedFailure
    def test_freezing_and_aggression_are_drivable_as_distinct_output_states(self):
        thr = _settle({"threat": 1.0})
        aff = _settle({"affiliation": 1.0})
        # each mode should actually DRIVE its own output, not merely be gated toward it
        self.assertGreater(thr["CEm-freeze"], 0.20)
        self.assertGreater(aff["CEm-active"], 0.20)


if __name__ == "__main__":
    unittest.main()

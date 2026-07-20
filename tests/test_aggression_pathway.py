import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

"""OBS-3 closure test: the v9 provocation -> hypothalamic-attack (VMHvl) pathway.

Context. In v8, provocation entered the substrate ONLY folded into IN-SOMATO:nociception, which
drives the GABAergic CeA -- the dominant inhibitor of both attack effectors (CeA->PAG/HYPdm
-0.70). So more provocation only DEEPENED attack suppression: aggression could not be driven at
all (OBS-3). v9 adds VMHvl (the hypothalamic attack area) with a provocation-specific drive
(IN-INTERO:provocation->VMHvl) and attack-effector recruitment (VMHvl->PAG, VMHvl->HYPdm), and
re-grounds the `aggress` affordance onto (VMHvl,PAG,HYPdm) instead of the self-inhibiting CeA.

Discipline (design-session ruling): DIRECTION-ONLY, never a rate. Assert (1) provocation shifts
the race toward aggression relative to plain threat, (2) plain threat still -> avoid (fear stays
the baseline), and -- the required control -- (3) neutral -> restrain with NO aggression leak (the
pathway is provocation-specific, not an always-on additive bias). The CeA->PAG/HYPdm inhibition is
NOT touched (no hand-dis-inhibition). Weights are SCAFFOLD; whether provoked aggression crosses the
overt-act threshold in adulthood is a calibration question, reported as-is, never tuned to win."""
import unittest

from substrate.model import load_substrate
from substrate.engine import SubstrateEngine
from substrate.social import respond_to_substrate
from affective_engine.core import Appraisal

_MODEL = load_substrate()
_EPS = 1e-6


def _act(appr, age=25.0):
    """The emergent act + per-affordance phasic drives for one appraisal on a fresh engine."""
    e = SubstrateEngine(_MODEL, age_years=age)
    return respond_to_substrate(e, appr)


class TestFreezingFloor(unittest.TestCase):
    """v14 defensive-drive (A): the analogue of the aggression floor, for the FREEZING column. The
    MeA->VMH sign flip (glutamatergic, MePV predator-defence -- was -1 by transmitter-field TYPING
    ORDER, S44) makes MeA DRIVE the defensive column, and MeA fires on any olfactory/conspecific cue
    (PIR, V-ventral). So the concern the ruling named: a NEUTRAL or CONSPECIFIC encounter must not
    produce freezing.

    ★ ASSERTS BOTH HALVES (defensive-drive ruling): "no threat -> no freezing" AND "threat -> freezing."
    A floor that asserts only the NEGATIVE half is PASSED BY A CORPSE -- Mc cannot fire, so it cannot
    fire at rest, so the negative half is green and proves nothing (the v9 lesson: a passing guard can
    certify an absence, not a mechanism). So the positive half is asserted too, and it is CURRENTLY RED.

    ★ READS THE EFFECTOR, NOT THE COLUMN (v14 freezing OUTPUT). Earlier this measured `vlPAG` -- but
    freezing is a BEHAVIOUR, and a behaviour is READ at its effector, not at the felt-state column
    (exactly the defect _DISTRESS_DISPLAY had, which Phase C fixed by pointing the display at the
    effectors). vlPAG's only prior efferent was NRA (the VOCAL relay): the freezing column had a driver
    and a felt state but NO FREEZING EFFECTOR -- the premotor target `Mc` (magnocellular medulla) named
    in the SECOND CLAUSE of the very Tovote 2016 sentence we cite on CeA->vlPAG-GABA was never built
    (partial-completion, 4th instance). `Mc` is now built (motor_effector terminal), and this floor
    reads `Mc` -- freezing, where it gets read.

    Why the positive half is STILL red, now measured honestly: building the output revealed the drive
    gap it was hiding. Under threat CeA disinhibits the selector (vlPAG-GABA -> 0) and VMH is driven
    (0.205), yet vlPAG-glut reads ~0.001 -- it actually DROPS under threat, because the DRN->vlPAG
    anxiolytic suppressor (Deakin & Graeff; ruled correct) is threat-driven and OVERPOWERS the weak
    VMH->vlPAG drive. So Mc stays at baseline.

    ★ THE D6-CLOSEOUT VERDICT (v14 -- two of the four terms now GROUNDED; the residual is one named item):
    the positive half's colour was resting on four ungrounded quantities balancing. Two are now grounded:
      (1) VMH->vlPAG STRONG (BUILD 1 -- Wang/Chen/Lin 2015, a behaviourally-decisive immobility drive; the
          driver was never weak), and
      (2) DRN's baseline on its S57 MATURATION CURVE (BUILD 2 -- adult ~0.30, the developmental-baseline
          mechanism that its scaffold-low was standing in for).
    And the GROUNDED DRIVER AND BRAKE BALANCE CORRECTLY: VMH-strong tolerates a tonic DRN up to ~0.48, and
    the grounded DRN sits at 0.30 -- comfortable margin. Cut the residual and the floor FIRES (Mc 0.141).
    The floor is held RED by ONE thing only: S56 -- DRN's threat-spike to 0.617 is 100% CORTICALLY
    MANUFACTURED (dlPFC saturates -> vmPFC/OFC -> DRN; DRN measurably does NOT respond to acute threat,
    Wilkinson & Jacobs). Terms (3) DRN's threat-artifact and (4) the gate-family bands are the SAME item:
    the S56 nine-node cortical-brake calibration. So: THE FREEZING COLUMN IS GROUNDED-CORRECT; the floor is
    held red SOLELY by the deferred S56/dlPFC cortical over-drive. This is the reviewer's predicted outcome
    -- a residual red that points cleanly at the next real term. RETIRE THIS RED WHEN S56 IS GROUNDED; do
    NOT touch S56 by hand to green it (cutting DRN's over-drive to make the floor fire is the exact move the
    whole arc refused -- a green bought by tuning a deferred term is worse than a red with a named, grounded
    reason). NB the positive cue uses a predator-type olfactory threat as a proxy -- the true predator-odor
    channel is a registered gap (S45)."""

    def _mc(self, **channels):
        # freezing is read at the EFFECTOR (Mc), not the vlPAG column (v14 freezing OUTPUT).
        e = SubstrateEngine(_MODEL, age_years=25.0)
        e.clear_inputs()
        for ch, v in channels.items():
            e.inject_channel(ch.replace("__", ":").replace("_DASH_", "-"), v)
        e.settle(35)
        return e.activity("Mc")

    def test_neutral_and_conspecific_do_not_produce_freezing(self):
        # NEGATIVE half -- NO THREAT -> NO FREEZING at the effector. Neutral and a plain conspecific-odour
        # encounter must leave Mc low. (Currently trivially held; becomes load-bearing once the positive
        # half below can pass -- see the class docstring.)
        self.assertLess(self._mc(), 0.10)                                    # neutral
        self.assertLess(self._mc(**{"IN_DASH_OLF__conspecific": 0.9}), 0.10)  # conspecific odour

    def test_defensive_threat_produces_freezing(self):
        # POSITIVE half -- THREAT -> FREEZING at the effector. CURRENTLY RED, and the D6-closeout verdict
        # names why precisely (see the class docstring): the driver (VMH->vlPAG STRONG) and brake (DRN on
        # its S57 curve) are now GROUNDED and BALANCE correctly -- the floor fires (Mc 0.141) the moment the
        # residual is removed -- but Mc stays ~0.05 because S56's cortical over-drive spikes DRN to 0.617
        # under threat. The residual is SOLELY S56 (the nine-node gate calibration, backlog). Do NOT touch
        # S56 to green this, and do NOT lower the threshold -- the red is grounded-and-named; it retires
        # when S56 is grounded (its own pass), not by hand here.
        self.assertGreater(self._mc(**{"IN_DASH_SOMATO__nociception": 0.9, "IN_DASH_OLF": 0.9}), 0.10)


class TestAggressionPathwayClosesOBS3(unittest.TestCase):
    def test_provocation_drives_the_attack_area(self):
        # OBS-3 fix: under provocation, aggression is now the DOMINANT drive (in v8 it was 0 --
        # the attack effectors could not be driven at all). Direction-only: aggress > avoid.
        b = _act(Appraisal(provocation=0.9))
        self.assertGreater(b.drives["aggress"], b.drives["avoid"])
        self.assertGreater(b.drives["aggress"], _EPS)          # actually driven, not ~0

    def test_plain_threat_still_avoids(self):
        # fear stays the baseline threat response: un-provoked threat -> avoid, aggression ~0.
        b = _act(Appraisal(threat=0.9))
        self.assertEqual(b.behaviour, "avoid")
        self.assertLess(b.drives["aggress"], b.drives["avoid"])
        self.assertLess(b.drives["aggress"], _EPS)             # not driven by pure threat

    def test_neutral_no_aggression_leak(self):
        # REQUIRED control: aggression is PROVOCATION-SPECIFIC, not a global additive shift -- asserted
        # two ways (neutral is small AND provoked >> neutral), which is the real claim.
        # ★ D6 (ruled): the epsilon documents an EMERGENT property, NOT a loosened measure. With DRN on
        # its S57 curve (adult ~0.30 instead of scaffold 0.05), DRN's twelve-target tonic 5-HT modulation
        # nets a hair of baseline defensive activity (0.000 -> 0.004) -- real 5-HT network physiology the
        # scaffold-low DRN was zeroing out (SS18 in miniature). The DRN->VMHvl aggression arm is correctly
        # INHIBITORY (5-HT1A, -) and provoked aggression is unchanged (~0.24, ~60x the floor). The old
        # <1e-6 was calibrated against the scaffold state where DRN zeroed its own network effect; a
        # neutral floor of LITERAL zero was itself the artifact (real brains have tonic network activity).
        neutral = _act(Appraisal())
        provoked = _act(Appraisal(provocation=0.9))
        self.assertEqual(neutral.behaviour, "restrain")
        self.assertLess(neutral.drives["aggress"], 0.01)                                  # small tonic floor
        self.assertGreater(provoked.drives["aggress"], 10 * neutral.drives["aggress"])    # provocation-specific

    def test_provocation_shifts_the_differential(self):
        # the aggress-minus-avoid contrast is strictly greater under provocation than under plain
        # threat -- the pathway is provocation-SPECIFIC, not a uniform lift of aggression.
        prov = _act(Appraisal(provocation=0.9)).drives
        threat = _act(Appraisal(threat=0.9)).drives
        self.assertGreater(prov["aggress"] - prov["avoid"],
                           threat["aggress"] - threat["avoid"])

    def test_pathway_is_behaviourally_efficacious_and_maturationally_restrained(self):
        # the pathway CAN produce overt aggression -- so OBS-3's "aggression cannot win even under
        # strong threat" is genuinely falsified, not merely nudged. Before executive control
        # matures (age 2) provocation -> overt aggress; in adulthood (age 25) the same provocation
        # is the dominant impulse but held sub-threshold. ★ CORRECTED (S56 diagnosis, verified): the
        # brake is NOT the STN hold -- removing STN_HOLD_GAIN entirely leaves the outcome unchanged, so
        # the hold is causally INERT. The real brake is an EFFECTOR-RECRUITMENT failure: VMHvl fires,
        # but the aggress population (mean VMHvl/dPAG/HYPdm) stays low because dPAG and HYPdm cannot be
        # recruited through their standing inhibition -- dPAG suppressed by the cortically-over-driven
        # DRN (+ dPAG-GABA<-DRN), HYPdm by the saturating CeA. The young->aggress / adult->restrain
        # course is still DEVELOPMENTAL (the cortical circuitry matures and its S56 over-drive of DRN
        # grows with it) -- but the maturing brake is the cortical over-drive, not the STN. NB grounding
        # S56 Stage 1 (cortical E-I loop gains) may lift the dPAG suppressor and let the adult aggress:
        # RE-CHECK this assertion after S56.
        #
        # ★ WHAT HOLDS THE young->aggress HALF (v14, ruled -- the v9 lesson: know what holds a green):
        # it depends on DRN's baseline being LOW at age 2. That is CORRECT -- toddlers aggress (Tremblay:
        # physical aggression peaks ~2-3 then declines, credited to maturing inhibitory control AND
        # maturing SEROTONERGIC function) -- but it is correct for a reason the substrate CANNOT YET
        # EXPRESS. DRN's baseline_activation is STATIC; there is no developmental trajectory for a
        # neuromodulator's tonic rate (the substrate models circuit ONSET and PLASTICITY curves, not
        # baselines). Grounding DRN to its ADULT pacemaker rate (~0.25-0.40) as a CONSTANT breaks this
        # half (young->restrain) -- because it gives a two-year-old an adult 5-HT brake on the attack
        # area (via DRN->VMHvl 5-HT1A). So DRN's 0.05 is NOT scaffold here; it is a PLACEHOLDER standing
        # where a maturing-5-HT mechanism should be (registered: developmental-baseline mechanism). This
        # half is not a coincidence to be filed away -- it is principle 1 (a missing mechanism) caught by
        # a green test. Do NOT "fix" it by grounding DRN as a constant.
        young = _act(Appraisal(provocation=0.9), age=2.0)
        adult = _act(Appraisal(provocation=0.9), age=25.0)
        self.assertEqual(young.behaviour, "aggress")           # efficacious before restraint matures
        self.assertEqual(adult.behaviour, "restrain")          # dominant impulse, held sub-threshold
        self.assertGreater(adult.drives["aggress"], adult.drives["avoid"])


class TestCeAInhibitionUntouched(unittest.TestCase):
    """Guardrail proof: v9 does NOT dis-inhibit the attack effectors by hand -- CeA is GABAergic and
    its drive onto the defensive effectors is unaltered (inhibitory synapse, weight untouched).

    v14 Phase A -- RE-EXPRESSED to what this guard PROTECTS, not what it literally asserted. It
    previously pinned `CeA->PAG` byte-exactly; `PAG` has since been SPLIT (its own function field read
    "Defensive output: freeze (vlPAG) / flight (dPAG)" -- two functionally opposite columns in one
    node), and CeA's target cell is now explicit: CeA's GABAergic projection targets vlPAG GABAergic
    INTERNEURONS (Tovote et al. 2016 -- the paper the edge already cited), which disinhibit the vlPAG
    output. What the guard protected is UNCHANGED and still asserted here: (a) CeA is GABAergic, and
    (b) the CeA->defensive-effector drive is byte-identical -- same inhibitory sign, same 0.70. Only
    the target cell became explicit. A state pin is not a design guard (principle 11)."""

    def test_cea_to_attack_effectors_still_inhibitory_and_unchanged(self):
        conns = {(c.source, c.target): c for c in _MODEL.connections}
        self.assertEqual(_MODEL.circuits["CEm"].sign, -1.0)     # CEm output neurons are GABAergic (inhibitory)
        self.assertEqual(_MODEL.circuits["CEl"].sign, -1.0)     # CEl is GABAergic too
        # the defensive-effector drive: target now explicit (vlPAG-GABA), drive untouched
        for tgt in ("vlPAG-GABA", "HYPdm"):
            edge = conns.get(("CEm", tgt))
            self.assertIsNotNone(edge, f"CeA->{tgt} missing")
            self.assertLess(edge.sign, 0.0, f"CeA->{tgt} must stay an INHIBITORY synapse")
            # moderate-strong == 0.70 (params.WEIGHT_QUALITATIVE); the v8 value, untouched
            self.assertAlmostEqual(edge.weight0, 0.70, places=6)

    def test_cea_reaches_the_vlpag_output_only_through_its_cited_target_cell(self):
        # v14 Phase A: the Tovote 2016 mechanism is IMPLEMENTED, not merely cited -- CeA does not
        # synapse on the vlPAG output directly; it acts through the interneuron, which inhibits vlPAG.
        conns = {(c.source, c.target): c for c in _MODEL.connections}
        self.assertIsNone(conns.get(("CEm", "vlPAG")), "CeA must reach vlPAG via vlPAG-GABA, not directly")
        gate = conns.get(("vlPAG-GABA", "vlPAG"))
        self.assertIsNotNone(gate, "the vlPAG-GABA -> vlPAG inhibitory gate must exist")
        self.assertLess(gate.sign, 0.0)                        # interneuron inhibits the output
        # net effect on vlPAG OUTPUT is DISINHIBITORY: (-1 onto the cell) x (-1 cell->output) = +1.
        # Inhibitory as a synapse, excitatory as a net effect on output -- both true, no contradiction.
        self.assertGreater(conns[("CEm", "vlPAG-GABA")].sign * gate.sign, 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

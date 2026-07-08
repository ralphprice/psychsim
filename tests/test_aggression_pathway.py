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
        # REQUIRED control: the new VMHvl drive must not leak an aggression tendency into neutral
        # states. Neutral -> restrain, and the aggression drive is ~0 (provocation-specific, not a
        # global additive shift).
        b = _act(Appraisal())
        self.assertEqual(b.behaviour, "restrain")
        self.assertLess(b.drives["aggress"], _EPS)

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
        # is the dominant impulse but held below the act threshold by the maturing STN brake ->
        # restrain. Reactive aggression's real developmental course (early expression, progressive
        # restraint), EMERGENT from the v9 pathway meeting the existing maturation mechanism.
        young = _act(Appraisal(provocation=0.9), age=2.0)
        adult = _act(Appraisal(provocation=0.9), age=25.0)
        self.assertEqual(young.behaviour, "aggress")           # efficacious before restraint matures
        self.assertEqual(adult.behaviour, "restrain")          # dominant impulse, held sub-threshold
        self.assertGreater(adult.drives["aggress"], adult.drives["avoid"])


class TestCeAInhibitionUntouched(unittest.TestCase):
    """Guardrail proof: v9 does NOT dis-inhibit the attack effectors by hand -- the CeA->PAG and
    CeA->HYPdm inhibitory edges are byte-identical to v8 (weight and inhibitory sign)."""

    def test_cea_to_attack_effectors_still_inhibitory_and_unchanged(self):
        conns = {(c.source, c.target): c for c in _MODEL.connections}
        self.assertEqual(_MODEL.circuits["CeA"].sign, -1.0)     # CeA is GABAergic (inhibitory)
        for tgt in ("PAG", "HYPdm"):
            edge = conns.get(("CeA", tgt))
            self.assertIsNotNone(edge, f"CeA->{tgt} missing")
            # moderate-strong == 0.70 (params.WEIGHT_QUALITATIVE); the v8 value, untouched
            self.assertAlmostEqual(edge.weight0, 0.70, places=6)


if __name__ == "__main__":
    unittest.main(verbosity=2)

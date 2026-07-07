import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""8b.6 -- the emergent-phenomena battery (CORE-validation, universal organism; NOT psychopathy).

Runnable checks that the named validation targets EMERGE from the mechanism rather than being
coded (App. D / Part IV): the adolescent-risk imbalance and DA/satiety state-dependence (the two
engine-side mechanism gaps, both circuit-side + meaning-blind), negativity bias, the ambivalent
bond, and 'a punishment for one is a reward for another'. Assertions are ORDINAL/structural,
never target values. Where a phenomenon did NOT emerge it is recorded as the honest result --
differential susceptibility is the gate-A earned negative (see test_substrate_divergence + the
core record), deliberately not re-litigated here."""

import tokenize
import unittest

from substrate.model import load_substrate
from substrate import phenomena
from substrate.phenomena import adolescent_risk_curve, satiety_modulates_reward
from affective_engine.learning import ValueLearner
from affective_engine.interocept import StateVector, valence_of_event
from sim_world.relations import RelationshipMatrix

_MODEL = load_substrate()


class TestAdolescentRisk(unittest.TestCase):
    """Mechanism-gap 1: continuous maturation fed into the executive's control CAPACITY (not
    just plasticity) makes control lag reward through adolescence, so risk peaks in adolescence
    -- emergent from the seed's schedule shapes, not a coded 'adolescent risk' rule."""

    def test_risk_peaks_in_adolescence(self):
        curve = adolescent_risk_curve(_MODEL, ages=(6, 10, 14, 16, 18, 22, 30))
        peak_age = max(curve, key=curve.get)
        self.assertTrue(14 <= peak_age <= 20, f"risk peak not adolescent: {curve}")
        # an inverted-U: higher in adolescence than in BOTH childhood and adulthood
        self.assertGreater(curve[16], curve[6])
        self.assertGreater(curve[16], curve[30])


class TestDaSatiety(unittest.TestCase):
    """Mechanism-gap 2: an energy deficit drives nutritive_state -> LH -> VTA (the seed's own
    chain), amplifying the food-reward DA; satiety attenuates it. Circuit modulation, never DA
    scaled by a computed r (R5-clean)."""

    def test_deficit_amplifies_and_satiety_attenuates(self):
        hungry, sated = satiety_modulates_reward(_MODEL, hungry=0.15, sated=0.95)
        self.assertGreater(hungry, sated)

    def test_modulator_is_a_circuit_not_a_computed_value(self):
        # the DA/satiety code modulates via the LH interoceptive circuit; a source-token check
        # confirms no computed drive-reduction 'r' is used to scale DA (would breach R5).
        with open(phenomena.__file__, "rb") as fh:
            names = {t.string.lower() for t in tokenize.tokenize(fh.readline)
                     if t.type == tokenize.NAME}
        for banned in ("drive_reduction", "computed_r", "scale_da"):
            self.assertNotIn(banned, names)


class TestNegativityBias(unittest.TestCase):
    """App. D bias: aversive learning is faster/higher-gain than appetitive (C.8), so a loss
    looms larger than an equal-magnitude gain -- emergent from one asymmetric rule."""

    def test_loss_looms_larger_than_equal_gain(self):
        pos, neg = ValueLearner(), ValueLearner()
        for _ in range(5):
            pos.update("good", +0.5)
            neg.update("bad", -0.5)
        self.assertGreater(abs(neg.value_of("bad")), abs(pos.value_of("good")))


class TestAmbivalentBond(unittest.TestCase):
    """App. 4.3 / F.6: co-active attachment AND threat toward the same person is the destructive
    ambivalent bond -- kept close (an inner slot) despite a negative learned value. Emergent from
    the salience-allocated matrix + the two pulls, not coded."""

    def test_ambivalent_bond_emerges_and_is_held_despite_negative_value(self):
        rm = RelationshipMatrix()
        for _ in range(8):
            rm.observe("caregiver", r=-0.2, attachment_pull=0.7, threat_pull=0.6)
        slot = rm.slots["caregiver"]
        self.assertTrue(slot.ambivalent)
        self.assertLess(slot.value, 0.0)                 # net aversive
        self.assertIn(slot, rm.inner_circle())           # yet salient enough to hold an inner slot
        self.assertIn(slot, rm.ambivalent_bonds())


class TestPunishmentForOneRewardForAnother(unittest.TestCase):
    """The #1 honesty payoff (App. C.2): value is COMPUTED from each agent's own state, so the
    SAME event is a reward for one agent and a punishment for another -- decided by their
    interoceptive states, never stipulated."""

    def test_same_event_opposite_valence_across_agents(self):
        hungry = StateVector(); hungry.levels["energy"] = 0.30; hungry.levels["arousal"] = 0.20
        sated = StateVector(); sated.levels["energy"] = 0.95; sated.levels["arousal"] = 0.20
        event = {"sweet_taste": 1.0, "gastric_fill": 0.5, "startle": 0.3}  # eating amid a loud onset
        r_hungry, _, _ = valence_of_event(hungry, event)
        r_sated, _, _ = valence_of_event(sated, event)
        self.assertGreater(r_hungry, 0.0)   # reward for the hungry (food relief dominates)
        self.assertLess(r_sated, 0.0)       # punishment for the sated (only the startle registers)


if __name__ == "__main__":
    unittest.main()

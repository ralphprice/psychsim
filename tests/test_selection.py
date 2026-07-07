import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""Phase 4 (PsychSim_MASTER) -- behaviour selection as basal-ganglia action selection.
The winner emerges from competition; the executive biases parameters, never the outcome.
Conflict/impulsivity/the adolescent risk gradient all emerge. Directional/structural only."""

import unittest

from affective_engine.selection import (Candidate, ExecutiveBias, select, bis_arousal,
                                         bias_from_maturation, reward_gain, brake_capacity)

_DRIVE = {"energy": 0.6, "belonging": 0.4}


class TestBasicSelection(unittest.TestCase):
    def test_dominant_value_wins_quickly_low_conflict(self):
        o = select([Candidate("A", anticipated_value=0.9),
                    Candidate("B", anticipated_value=0.2)], _DRIVE)
        self.assertEqual(o.winner, "A")
        self.assertTrue(o.committed)
        self.assertLess(o.conflict, 0.5)

    def test_state_dependent_value(self):
        # a food candidate wins when hungry, loses when sated (App. C.5 / F.2)
        food = Candidate("food", drive_profile={"energy": 0.8})
        chat = Candidate("chat", drive_profile={"belonging": 0.8})
        hungry = select([food, chat], {"energy": 1.0, "belonging": 0.1})
        sated = select([food, chat], {"energy": 0.0, "belonging": 1.0})
        self.assertEqual(hungry.winner, "food")
        self.assertEqual(sated.winner, "chat")


class TestConflictAndBIS(unittest.TestCase):
    def test_near_tie_is_high_conflict_and_slower(self):
        dom = select([Candidate("A", anticipated_value=0.9),
                      Candidate("B", anticipated_value=0.2)], _DRIVE)
        tie = select([Candidate("approach", anticipated_value=0.7),
                      Candidate("avoid", anticipated_value=0.7)], _DRIVE)
        self.assertGreater(tie.conflict, dom.conflict)
        self.assertGreaterEqual(tie.steps, dom.steps)

    def test_bis_holds_arousal_elevated_under_conflict(self):
        dom = select([Candidate("A", anticipated_value=0.9),
                      Candidate("B", anticipated_value=0.1)], _DRIVE)
        tie = select([Candidate("approach", anticipated_value=0.7),
                      Candidate("avoid", anticipated_value=0.7)], _DRIVE)
        self.assertGreater(bis_arousal(tie), bis_arousal(dom))
        self.assertGreater(bis_arousal(tie), 0.0)


class TestExecutiveBiasesNotDecides(unittest.TestCase):
    def test_executive_biases_the_competition(self):
        cands = [Candidate("x", anticipated_value=0.6), Candidate("y", anticipated_value=0.6)]
        # a NoGo pre-load on x hands the tie to y -- but the competition still resolves,
        # and biasing y instead flips the winner: the executive sets parameters, the
        # competition picks. (App. F.5)
        bx = select(cands, _DRIVE, bias=ExecutiveBias(nogo={"x": 0.6}))
        by = select(cands, _DRIVE, bias=ExecutiveBias(nogo={"y": 0.6}))
        self.assertEqual(bx.winner, "y")
        self.assertEqual(by.winner, "x")

    def test_impulsivity_is_a_weak_brake_letting_a_prepotent_candidate_win(self):
        # tested at the impulse peak (adolescence) and varying ONLY the executive brake, to
        # isolate its causal role: a strong prepotent (impulse) beats a deliberate high-value
        # option when the brake is weak, not when it is strong. (App. F.7)
        imp = Candidate("grab", prepotent=0.9)
        delib = Candidate("wait", anticipated_value=0.6)
        weak = select([imp, delib], _DRIVE, age_years=16,
                      bias=ExecutiveBias(stn_hold=0.1, nogo={"grab": 0.1}))
        strong = select([imp, delib], _DRIVE, age_years=16,
                        bias=ExecutiveBias(stn_hold=1.0, nogo={"grab": 1.0}))
        self.assertEqual(weak.winner, "grab")
        self.assertEqual(strong.winner, "wait")


class TestDevelopmentalGradient(unittest.TestCase):
    def _risk_margin(self, age):
        risky = Candidate("risky", prepotent=0.9)
        safe = Candidate("safe", anticipated_value=0.42)
        o = select([risky, safe], _DRIVE, dopamine=0.7, age_years=age,
                   bias=bias_from_maturation(age, monitors={"risky": 1.0}))
        return o.accumulators["risky"] - o.accumulators["safe"]

    def test_adolescent_risk_bump(self):
        # the risk margin peaks in adolescence and resolves into adulthood -- emergent from
        # the reward/brake maturation imbalance, not a coded "adolescent risk" rule.
        child, adolescent, adult = self._risk_margin(8), self._risk_margin(16), self._risk_margin(30)
        self.assertGreater(adolescent, child)
        self.assertGreater(adolescent, adult)

    def test_maturation_curves(self):
        # reward/sensation-seeking is humped (peaks in adolescence); the brake rises monotonically
        self.assertGreater(reward_gain(16), reward_gain(8))
        self.assertGreater(reward_gain(16), reward_gain(30))
        self.assertLess(brake_capacity(10), brake_capacity(20))
        self.assertLess(brake_capacity(20), brake_capacity(30))

    def test_brake_weak_in_childhood(self):
        self.assertLess(brake_capacity(8), 0.2)
        self.assertGreater(brake_capacity(30), 0.9)


if __name__ == "__main__":
    unittest.main()

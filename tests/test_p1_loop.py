import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""P1 -- the loop carries FEELING and reads HISTORY (the first top-down loop-fidelity pass).

The two-agent exchange already CLOSED (A's act reaches B's substrate and drives B's next act).
P1 adds the two bands that made it hollow:

  Change A -- the affect band crosses. A's DISPLAYED valence (read off its expression effectors,
  masking baked in by the two L7 pathways) rides the act and folds into B's appraisal -- but on a
  SEPARATE vigilance roll from the act's own deception, so a believed lie can still leak its
  coldness to a vigilant hearer. The substrate produces only a distress display (no warmth
  effector), so the crossed valence is <= 0.

  Change B -- perception reads the record. Person.perceive reads rel(self, other) (the per-other
  history: affect/trust/familiarity) and lets it COLOUR the appraisal -- warmth remembered reads
  warmer/safer, low trust reads more threatening -- gated by familiarity so a stranger is not
  coloured. A directed event still dominates.

The honesty wall: every assertion here is about what B PERCEIVES (the input band). None asserts
what B DOES -- the behaviour stays emergent from B's substrate. All gains are SCAFFOLD; the tests
are ordinal/structural, never target values."""

import random
import unittest

from speech.acts import (SpeechAct, appraisal_from_act, perceive_act, perceive_affect,
                         act_from_behaviour)
from sim_world import build_world, Person, GameMaster, SocialEvent
from sim_world.gamemaster import Relationship
from substrate.social import displayed_distress
from affective_engine import shared_root_seed
from affective_engine.core import Appraisal


# ---------------------------------------------------------------------------
# CLAIM 1 -- feeling crosses the channel, honestly (Change A)
# ---------------------------------------------------------------------------
class TestP1AffectBandCrosses(unittest.TestCase):

    def test_displayed_read_is_a_nonnegative_distress_magnitude(self):
        # the effector read is a magnitude in [0,1]; a settled agent on a neutral encounter shows
        # little; whatever it shows, the SIGNED valence carried is <= 0 (no warmth effector exists)
        p = Person("a", "A", shared_root_seed(), birth_day=-9000)
        p.social_act(Appraisal(), 25.0)
        d = displayed_distress(p.engine)
        self.assertGreaterEqual(d, 0.0)
        self.assertLessEqual(d, 1.0)
        act = act_from_behaviour("avoid", "a", "b", displayed_affect=-d)
        self.assertLessEqual(act.displayed_affect, 0.0)   # distress-only: the crossed valence is <= 0

    def test_caught_affect_moves_the_appraisal_missed_does_not(self):
        # the SAME act, resolved two ways: a caught display raises the receiver's distress/threat
        # read and lowers warmth; a missed display leaves the act-only reading untouched
        act = SpeechAct("a", "b", "THREATEN", intensity=0.5, displayed_affect=-0.6)
        caught = appraisal_from_act(act, "THREATEN", affect_seen=True)
        missed = appraisal_from_act(act, "THREATEN", affect_seen=False)
        self.assertGreater(caught.threat, missed.threat)
        self.assertGreater(caught.other_distress, missed.other_distress)
        self.assertLess(caught.social_valence, missed.social_valence)

    def test_neutral_face_crosses_nothing(self):
        # displayed_affect == 0 -> the roll never fires and the appraisal is act-only
        act = SpeechAct("a", "b", "ASSERT", displayed_affect=0.0)
        self.assertFalse(perceive_affect(act, 0.99, random.Random(0)))
        caught = appraisal_from_act(act, "ASSERT", affect_seen=True)
        plain = appraisal_from_act(act, "ASSERT", affect_seen=False)
        self.assertEqual((caught.threat, caught.other_distress, caught.social_valence),
                         (plain.threat, plain.other_distress, plain.social_valence))

    def test_affect_roll_is_vigilance_graded(self):
        # catching the leak is more likely for a vigilant perceiver -- emergent from the seeded roll
        act = SpeechAct("a", "b", "THREATEN", intensity=0.5, displayed_affect=-0.6)
        rng = random.Random(1)
        low = sum(perceive_affect(act, 0.1, rng) for _ in range(3000)) / 3000
        high = sum(perceive_affect(act, 0.9, rng) for _ in range(3000)) / 3000
        self.assertGreater(high, low)

    def test_affect_roll_dissociates_from_the_act_roll(self):
        # THE CU-RELEVANT SIGNAL: the act band and the affect band resolve on SEPARATE rolls, so
        # a deception can be believed (act missed) while the leaked coldness is still caught (affect
        # seen) -- the masked-affect dissociation. Proven by finding, over seeds, a case where the
        # two rolls disagree; if they were one roll this could never happen.
        act = SpeechAct("a", "b", "AFFILIATE", surface="AFFILIATE",
                        intensity=0.6, displayed_affect=-0.6)
        deceptive = SpeechAct("a", "b", "THREATEN", surface="AFFILIATE",
                              intensity=0.6, displayed_affect=-0.6)
        disagreements = 0
        for s in range(400):
            rng = random.Random(s)
            act_detected = perceive_act(deceptive, 0.5, rng)        # was the lie seen?
            affect_caught = perceive_affect(deceptive, 0.5, rng)    # was the leak caught?
            if (act_detected == deceptive.intent) != affect_caught:
                disagreements += 1
        self.assertGreater(disagreements, 0,
                           "act and affect rolls never dissociate -- they are not separate")


# ---------------------------------------------------------------------------
# CLAIM 2 -- history shapes the read (Change B)
# ---------------------------------------------------------------------------
class TestP1RecordFeedback(unittest.TestCase):

    def setUp(self):
        self.w = build_world()
        self.a = Person("a", "A", shared_root_seed(), birth_day=-9000)
        self.w.place_agent("a", "street")

    def test_warm_history_reads_warmer_and_safer_than_harsh(self):
        warm = Relationship(familiarity=0.8, affect=+0.8, trust=0.8)
        harsh = Relationship(familiarity=0.8, affect=-0.8, trust=0.1)
        aw = self.a.perceive(self.w, None, partner_rel=warm)
        ah = self.a.perceive(self.w, None, partner_rel=harsh)
        self.assertGreater(aw.social_valence, ah.social_valence)
        self.assertLess(aw.threat, ah.threat)

    def test_a_stranger_is_not_coloured(self):
        # familiarity 0 gates the whole read off -> a stranger appraises IDENTICALLY to no-record.
        # (Without the gate, trust 0 would read (1 - 0) = maximal threat -- the bug the gate closes.)
        stranger = Relationship()                       # familiarity/affect/trust all 0
        a_str = self.a.perceive(self.w, None, partner_rel=stranger)
        a_none = self.a.perceive(self.w, None, partner_rel=None)
        self.assertAlmostEqual(a_str.social_valence, a_none.social_valence)
        self.assertAlmostEqual(a_str.threat, a_none.threat)

    def test_a_directed_event_still_dominates_the_record(self):
        # the record only COLOURS -- a directed event's override still wins
        harsh = Relationship(familiarity=0.9, affect=-0.9, trust=0.1)
        ev = SocialEvent("warmth", "b", {"social_valence": 0.9})
        a = self.a.perceive(self.w, ev, partner_rel=harsh)
        self.assertEqual(a.social_valence, 0.9)


# ---------------------------------------------------------------------------
# END TO END -- the whole converse path carries both bands
# ---------------------------------------------------------------------------
class TestP1EndToEnd(unittest.TestCase):

    def _pair(self, seed=7):
        w = build_world()
        a = Person("a", "A", shared_root_seed(), birth_day=-9000)
        b = Person("b", "B", shared_root_seed(), birth_day=-9000)
        w.place_agent("a", "street"); w.place_agent("b", "street")
        return w, GameMaster(w, seed=seed), a, b

    def test_converse_carries_the_affect_band(self):
        # the opener act produced by the real loop carries A's displayed valence (<= 0), and the
        # conversation is still reproducible with the extra seeded affect roll in the channel
        w, gm, a, b = self._pair(seed=7)
        convo = gm.converse(a, b, topic="the plan")
        self.assertLessEqual(convo.opener.act.displayed_affect, 0.0)
        w2, gm2, a2, b2 = self._pair(seed=7)
        self.assertEqual(convo.transcript(), gm2.converse(a2, b2, topic="the plan").transcript())

    def test_converse_reads_history_via_gm_rel(self):
        # exactly the wiring converse uses: gm.rel(actor, target) -> perceive(partner_rel=...).
        # A warm vs harsh record on the SAME encounter yields a different opener appraisal.
        w, gm, a, b = self._pair(seed=7)
        gm.relationships[("a", "b")] = Relationship(familiarity=0.8, affect=+0.8, trust=0.8)
        warm = a.perceive(w, None, partner_rel=gm.rel("a", "b"))
        gm.relationships[("a", "b")] = Relationship(familiarity=0.8, affect=-0.8, trust=0.1)
        harsh = a.perceive(w, None, partner_rel=gm.rel("a", "b"))
        self.assertGreater(warm.social_valence, harsh.social_valence)
        self.assertLess(warm.threat, harsh.threat)


if __name__ == "__main__":
    unittest.main()

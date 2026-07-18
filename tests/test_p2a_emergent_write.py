import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""P2a -- the relationship record is WRITTEN emergently (magnitude by winner drive intensity).

P1 made perceive READ rel. P2a makes the WRITE emergent: after an exchange, adjudicate moves
rel(actor, target) by a magnitude that scales with the WINNER'S OWN emergent drive INTENSITY --
resp.drives[resp.behaviour], the phasic pull the winning affordance emerged with (== social.py:269's
'strength' for the winner, a quantity in [0,1]). Before P2a the sign was emergent (is_cohesive_act
/is_aggressive_act on the behaviour string) but the magnitude was a hardcoded step (+/-0.15 etc.). Now:

  * a STRONGLY-driven warm act builds more affect/trust than a WEAKLY-driven one;
  * a strongly-driven aggressive act erodes more than a weakly-driven one;
  * every magnitude traces to a substrate quantity (band * win_drive) -- no fixed step;
  * the SIGN is still emergent, keyed on the category-free behaviour feature (honesty migration #2).

This is drive INTENSITY, not MARGIN over the runner-up (a narrowly-won and an uncontested act with
equal winning drive move the tie the same -- margin-decisiveness is a separate scalar, flagged to the
design session). The bands (0.15/0.1/0.2/0.15) are the pre-P2a constants kept UNCHANGED -- P2a adds no
new tunable number, only the drive factor. Familiarity is contact-count, unscaled. Trust keeps its 0
floor. Ordinal/structural assertions only; the specific-value checks assert delta == band*win_drive
(that the magnitude IS the drive-scaled band), never a tuned target."""

import unittest

from sim_world import build_world, Person, GameMaster, SocialEvent
from substrate.social import SocialBehaviour
from affective_engine import shared_root_seed


def _cohesive(win_drive):
    # a cohesive winner ('nurture') whose winning drive == win_drive
    return SocialBehaviour("nurture", 5, {"nurture": win_drive, "avoid": 0.05})


def _aggressive(win_drive):
    return SocialBehaviour("aggress", 5, {"aggress": win_drive, "avoid": 0.05})


class TestP2aEmergentWrite(unittest.TestCase):

    def setUp(self):
        self.w = build_world()
        self.gm = GameMaster(self.w, seed=1)
        self.p = Person("a", "A", shared_root_seed(), birth_day=-9000)
        self.w.place_agent("a", "street")
        self.ev = SocialEvent("affiliate", "b")     # target = b (event.source_id)

    def _affect_after(self, resp):
        self.gm.relationships.clear()
        self.gm.adjudicate(self.p, resp, self.ev)
        return self.gm.rel("a", "b")

    def test_warm_magnitude_scales_with_conviction(self):
        decisive = self._affect_after(_cohesive(0.9)).affect
        marginal = self._affect_after(_cohesive(0.2)).affect
        self.assertGreater(decisive, marginal)              # conviction scales the magnitude
        self.assertGreater(marginal, 0.0)                   # a warm act still warms (sign emergent)

    def test_warm_delta_is_band_times_conviction_not_a_fixed_step(self):
        # the magnitude IS the band (0.15) times the substrate's conviction -- proving it is no longer
        # a fixed step. (Fresh rel starts at affect 0, so the value equals the delta.)
        for c in (0.2, 0.5, 0.9):
            r = self._affect_after(_cohesive(c))
            self.assertAlmostEqual(r.affect, 0.15 * c)
            self.assertAlmostEqual(r.trust, 0.10 * c)

    def test_aggressive_erosion_scales_with_conviction(self):
        decisive = self._affect_after(_aggressive(0.9)).affect
        marginal = self._affect_after(_aggressive(0.2)).affect
        self.assertLess(decisive, marginal)                 # a decisive strain erodes MORE (more negative)
        self.assertLess(marginal, 0.0)                      # an aggressive act still strains (sign emergent)
        self.assertAlmostEqual(decisive, -0.2 * 0.9)        # delta == band * conviction

    def test_sign_is_still_emergent_by_act_feature(self):
        # same conviction, opposite behaviour feature -> opposite sign; the sign keys on the emergent
        # behaviour string, never on a conviction magnitude or an outcome category
        warm = self._affect_after(_cohesive(0.7)).affect
        cold = self._affect_after(_aggressive(0.7)).affect
        self.assertGreater(warm, 0.0)
        self.assertLess(cold, 0.0)

    def test_familiarity_is_contact_count_unscaled(self):
        # familiarity moves the SAME +0.1 regardless of conviction (contact-count, not tie-strength);
        # its scaling is a registered fork, deliberately not part of P2a
        hi = self._affect_after(_cohesive(0.9)).familiarity
        lo = self._affect_after(_cohesive(0.1)).familiarity
        self.assertAlmostEqual(hi, lo)
        self.assertAlmostEqual(hi, 0.1)

    def test_trust_keeps_its_zero_floor(self):
        # a strong aggressive outcome cannot drive trust below 0 in P2a (betrayal-as-negative-trust is
        # a separate grounded pass, registered)
        r = self._affect_after(_aggressive(1.0))
        self.assertGreaterEqual(r.trust, 0.0)

    def test_neutral_act_moves_only_familiarity(self):
        # a withdrawal/restrain act (neither cohesive nor aggressive) leaves affect/trust untouched --
        # the two-bucket partition is unchanged by P2a (its dissolution is a registered fork)
        r = self._affect_after(SocialBehaviour("avoid", 5, {"avoid": 0.8}))
        self.assertAlmostEqual(r.affect, 0.0)
        self.assertAlmostEqual(r.trust, 0.0)
        self.assertAlmostEqual(r.familiarity, 0.1)


if __name__ == "__main__":
    unittest.main()

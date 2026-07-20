import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""v10 physical endowment -- E2/E4 perceiver-side perception (the Arena keystone).

A physical trait is a STIMULUS the bearer presents; the response emerges from the PERCEIVER's own
circuits, fed through the vetted felt_response path onto the IN-CONSPEC edges -- never a coded
trait->outcome weight. E2: the stimulus is bearer-pure. E4: the perceiver's valuation of it is
sex-conditioned, a genuine perceiver x bearer 2x2.

Load-bearing honesty properties (ordinal/structural only):
  * DIRECTIONS SEPARATE: an attractive other drives the perceiver's REWARD circuits (NAc-shell/OFC);
    a formidable other drives the perceiver's DEFENSIVE submission (CeA) and NOT its attack area
    (VMHvl) -- seeing strength makes you defer, not attack (the attack area is the bearer's own, E5).
  * BEARER-PURE (E2): the stimulus a bearer presents is the same regardless of who perceives it;
    only the perceiver's sex-pairing weight differs.
  * GENUINE 2x2 (E4): the valuation depends on BOTH perceiver and bearer sex -- same bearer, different
    perceiver -> different valuation. Not sex_weight(bearer) in disguise.
  * NON-BLEED: A perceiving B develops A's OWN substrate only; B is untouched (independent reads).
  * DIFFERENTIAL, NOT OUTCOME: the weight yields a per-moment circuit-response differential, but the
    tie accrues only from the emergent ACT (is_cohesive/is_aggressive) -- there is no coded
    attractiveness->tie shortcut. Whether a beauty premium emerges needs the full develop-and-accrue
    loop and is a scan_match target, never predictable from this weight.
"""
import unittest

from arena import _add_physical_percept, _perceive, _social_episode, _Tie, intact_seed
from affective_engine.agent import AffectiveAgent
from substrate.social import felt_response
from affective_engine.physical import SEX_MALE, SEX_FEMALE


class _Bearer:
    """A minimal stand-in carrying just what E2/E4 read off a perceived agent."""
    def __init__(self, physical, sex):
        self.physical = physical
        self.sex = sex


ATTRACTIVE = _Bearer({"PH-ATTRACT": 2.5, "PH-HEALTH": 1.5, "PH-MUSCLE": 0.0, "PH-SIZE": 0.0}, SEX_FEMALE)
PLAIN = _Bearer({"PH-ATTRACT": -2.5, "PH-HEALTH": -1.5, "PH-MUSCLE": 0.0, "PH-SIZE": 0.0}, SEX_FEMALE)
STRONG = _Bearer({"PH-ATTRACT": 0.0, "PH-HEALTH": 0.0, "PH-MUSCLE": 2.5, "PH-SIZE": 2.0}, SEX_MALE)


def _perceiver(seed=1):
    return AffectiveAgent(seed=intact_seed(), temperament_seed=seed)


def _settle(perceiver, bearer):
    p = _perceive("restrain")                      # a neutral baseline act as the backdrop
    _add_physical_percept(p, perceiver, bearer)
    felt_response(perceiver.engine, p, 25.0, getattr(perceiver, "_rest_baseline", None))
    return perceiver.engine.activation


class TestPerceiverDirectionsSeparate(unittest.TestCase):
    def test_attractiveness_drives_reward(self):
        att = _settle(_perceiver(), ATTRACTIVE)
        pln = _settle(_perceiver(), PLAIN)
        self.assertGreater(att["NAc-shell"], pln["NAc-shell"])
        self.assertGreater(att["OFC"], pln["OFC"])

    def test_formidability_drives_defensive_submission_not_attack(self):
        strong = _settle(_perceiver(), STRONG)
        plain = _settle(_perceiver(), PLAIN)
        self.assertGreater(strong["CEl"], plain["CEl"])          # submission/wariness dominates
        # the perceiver's attack area is NOT driven to attack by seeing strength. Sign history: v10 exact
        # baseline; v11 slightly BELOW (inhibitory MeA->VMHvl brake); v12a the sign is (correctly)
        # EXCITATORY so the perceiver's own MeA tone primes VMHvl slightly ABOVE baseline -- but only
        # sub-threshold (well below the ~1.0 attack level), and DEFENSIVE (CeA) still dominates. The
        # honest invariant is "attack sub-threshold + defensive dominates", not an exact-baseline value.
        self.assertLess(strong["VMHvl"], 0.20)                   # sub-threshold: not driven to attack
        self.assertGreater(strong["CEl"], strong["VMHvl"])       # defensive >> attack


class TestBearerPureStimulus(unittest.TestCase):
    def test_stimulus_same_regardless_of_perceiver_up_to_pairing(self):
        # two perceivers of the SAME sex see the same bearer stimulus identically (same pairing)
        a = _perceiver(seed=1); b = _perceiver(seed=2)
        a.sex = b.sex = SEX_MALE
        pa, pb = _perceive("restrain"), _perceive("restrain")
        _add_physical_percept(pa, a, ATTRACTIVE)
        _add_physical_percept(pb, b, ATTRACTIVE)
        self.assertEqual(pa["attractive_face"], pb["attractive_face"])


class TestGenuineTwoByTwoPairing(unittest.TestCase):
    def test_same_bearer_different_perceiver_sex_differs(self):
        male = _perceiver(); male.sex = SEX_MALE
        female = _perceiver(); female.sex = SEX_FEMALE
        pm, pf = _perceive("restrain"), _perceive("restrain")
        _add_physical_percept(pm, male, ATTRACTIVE)      # male -> female bearer
        _add_physical_percept(pf, female, ATTRACTIVE)    # female -> female bearer
        self.assertNotEqual(pm["attractive_face"], pf["attractive_face"])
        self.assertGreater(pm["attractive_face"], pf["attractive_face"])   # the studied pairing higher


class TestNonBleed(unittest.TestCase):
    def test_perceiving_other_does_not_touch_the_other(self):
        a = _perceiver(seed=1)
        b_agent = _perceiver(seed=2)
        b_weights_before = list(b_agent.engine.weight)
        b_act_before = dict(b_agent.engine.activation)
        # A perceives B (as a bearer) and develops through the moment
        _social_episode(a, b_agent, "restrain", _Tie(), 10.0)
        self.assertEqual(list(b_agent.engine.weight), b_weights_before)     # B's connectome untouched
        self.assertEqual(dict(b_agent.engine.activation), b_act_before)     # B's state untouched


class TestDifferentialNotOutcome(unittest.TestCase):
    def test_reward_differential_exists_but_tie_is_from_the_act_only(self):
        # the differential is real (attractive -> more reward drive) ...
        att = _settle(_perceiver(), ATTRACTIVE)
        pln = _settle(_perceiver(), PLAIN)
        self.assertGreater(att["NAc-shell"], pln["NAc-shell"])
        # ... but the tie change is a function of the emergent ACT, not of attractiveness: two
        # episodes whose perceiver emits the same act-class move the tie identically, whatever the
        # bearer's looks. (No coded attractiveness->tie shortcut; a premium needs develop-and-accrue.)
        from substrate.social import is_cohesive_act, is_aggressive_act
        t_att, t_pln = _Tie(), _Tie()
        a1, a2 = _perceiver(seed=5), _perceiver(seed=5)
        b_att = _social_episode(a1, ATTRACTIVE, "restrain", t_att, 10.0)
        b_pln = _social_episode(a2, PLAIN, "restrain", t_pln, 10.0)
        if (is_cohesive_act(b_att) == is_cohesive_act(b_pln)
                and is_aggressive_act(b_att) == is_aggressive_act(b_pln)):
            self.assertEqual((t_att.affect, t_att.strain), (t_pln.affect, t_pln.strain))


if __name__ == "__main__":
    unittest.main()

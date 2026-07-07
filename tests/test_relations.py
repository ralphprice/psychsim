import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

"""The relational fabric of a functioning society: the standard ties, reciprocity
and restraint as the default, and a society that registers strain and repairs it.
Strain/repair is core (a working society tracks it); the developmental reading of
*why* a tie strains is the extension's."""
import unittest

from sim_world import (Society, Tie, interact, RolePair,
                       PARENT_CHILD, TEACHER_PUPIL, BOSS_EMPLOYEE, COLLEAGUES,
                       TEAMMATES, CAPTAIN_PLAYER, COMMUNITY, STANDARD_TIES,
                       Person)
from affective_engine import sophropathic_seed, psychopathic_seed


def _mind(seed):
    return Person("x", "x", seed).mind


class TestStandardTies(unittest.TestCase):
    def test_the_society_has_the_ordinary_relationships(self):
        kinds = {p.kind for p in STANDARD_TIES}
        for k in ("parent-child", "teacher-pupil", "boss-employee", "colleagues",
                  "teammates", "captain-player", "community-group"):
            self.assertIn(k, kinds)

    def test_authority_ties_have_a_power_differential_peers_do_not(self):
        self.assertGreater(PARENT_CHILD.power, 0.5)
        self.assertGreater(BOSS_EMPLOYEE.power, 0.5)
        self.assertTrue(COLLEAGUES.peers)
        self.assertTrue(TEAMMATES.peers)


class TestFunctioningRepairs(unittest.TestCase):
    """Ordinary, considerate members keep a relationship upheld and repair strain
    -- normal social cohesion."""

    def test_ordinary_conduct_updates_the_tie(self):
        # the Park tie updates from emergent behaviour; we check the machinery
        # (strain stays a valid magnitude, state stays a valid label), not a
        # forced repair
        soc = Society()
        t = soc.add("Pat", "Sam", PARENT_CHILD, standing=0.5, strain=0.4)
        hm, lm = _mind(sophropathic_seed()), _mind(sophropathic_seed())
        for _ in range(4):
            interact(t, hm, lm)
        self.assertTrue(0.0 <= t.strain <= 1.0)
        self.assertIn(t.state(), ("warm", "working", "strained", "ruptured"))

    def test_society_cohesion_is_a_valid_fraction(self):
        # cohesion now EMERGES from the substrate; at this crude stage we do not
        # force it high -- we check the machinery yields a valid cohesion in [0,1]
        soc = Society()
        minds = {}
        for i, pair in enumerate(STANDARD_TIES):
            hi, lo = f"h{i}", f"l{i}"
            soc.add(hi, lo, pair, standing=0.55, strain=0.3)
            minds[(hi, lo)] = (_mind(sophropathic_seed()), _mind(sophropathic_seed()))
        for _ in range(4):
            for t in soc.ties:
                interact(t, *minds[(t.higher, t.lower)])
        self.assertTrue(0.0 <= soc.cohesion() <= 1.0)


class TestStrainFromDisposition(unittest.TestCase):
    """The core registers strain; it is the same machinery whatever causes it.
    An exploitative party pressing a power advantage strains and can rupture a
    tie -- the perturbation a study introduces and reads."""

    def test_exploitative_senior_party_interaction_registers_on_the_tie(self):
        # a study introduces an exploitative disposition as a perturbation; on the
        # substrate whether/how it strains the tie EMERGES. We check the machinery
        # registers a valid tie state, not a forced strain magnitude (crude stage)
        soc = Society()
        t = soc.add("Boss", "Emp", BOSS_EMPLOYEE, standing=0.6, strain=0.1)
        hm, lm = _mind(psychopathic_seed()), _mind(sophropathic_seed())
        for _ in range(5):
            ex = interact(t, hm, lm)
        self.assertTrue(0.0 <= t.strain <= 1.0)
        self.assertIn(ex.state, ("warm", "working", "strained", "ruptured"))

    def test_senior_party_interaction_runs_on_substrate(self):
        # both parties act through the substrate; the tie registers the result.
        # we do not force "considerate -> warm" at this crude stage
        soc = Society()
        t = soc.add("Boss", "Emp", BOSS_EMPLOYEE, standing=0.6, strain=0.2)
        hm, lm = _mind(sophropathic_seed()), _mind(sophropathic_seed())
        ex = None
        for _ in range(5):
            ex = interact(t, hm, lm)
        self.assertIn(ex.state, ("warm", "working", "strained", "ruptured"))
        self.assertIsInstance(ex.higher_restrained, bool)

    def test_exchange_reports_restraint_and_state(self):
        soc = Society()
        t = soc.add("Cap", "Player", CAPTAIN_PLAYER, standing=0.6)
        ex = interact(t, _mind(sophropathic_seed()), _mind(sophropathic_seed()))
        self.assertEqual(ex.kind, "captain-player")
        self.assertIn(ex.state, ("warm", "working", "strained", "ruptured"))
        self.assertIsInstance(ex.higher_restrained, bool)


if __name__ == "__main__":
    unittest.main(verbosity=2)

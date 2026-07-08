import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))

"""The environment matrix: a per-person ledger of attractions and aversions to
things, parallel to the Park relationship matrix. These tests check the MACHINERY
and that disposition EMERGES from each person's substrate -- NOT that any given
thing attracts everyone (that would be forcing)."""
import random
import unittest
from affective_engine.core import TraitSeed
from affective_engine.agent import AffectiveAgent
from sim_world.environment_matrix import (Thing, Bond, EnvironmentMatrix, encounter)

_G = {"THREAT": 0.5, "ANXIETY": 0.5, "SEEKING": 0.5, "FRUSTRATION": 0.5,
      "CARE": 0.5, "SOCIAL_LOSS": 0.5, "CONTROL": 0.5, "INSTRUMENTAL_CONTROL": 0.5}


def _brain(gains, seed=0):
    # a substrate-backed agent with the given temperament gains (env encounter takes an agent)
    return AffectiveAgent(seed=TraitSeed("t", gains={**_G, **gains}), temperament_seed=seed)


class TestBondBookkeeping(unittest.TestCase):
    def test_disposition_and_state(self):
        b = Bond("x", attraction=0.6, aversion=0.1)
        self.assertAlmostEqual(b.disposition(), 0.5)
        self.assertEqual(b.state(), "sought")
        b2 = Bond("y", attraction=0.0, aversion=0.6)
        self.assertEqual(b2.state(), "shunned")
        self.assertEqual(Bond("z").state(), "neutral")


class TestEncounterMachinery(unittest.TestCase):
    def test_appetitive_response_accrues_attraction(self):
        # a strongly reward-seeking brain meeting a reward cue -> drawn to it
        brain = _brain({"SEEKING": 0.9, "THREAT": 0.2, "ANXIETY": 0.2}, seed=1)
        m = EnvironmentMatrix()
        thing = Thing("treat", "a treat", "food", {"reward_cue": 0.9})
        for _ in range(5):
            encounter(brain, thing, m)
        self.assertGreater(m.bond("treat").attraction, 0.0)
        self.assertEqual(m.bond("treat").encounters, 5)

    def test_aversive_response_accrues_aversion(self):
        # a fearful brain meeting a pure threat -> repelled by it
        brain = _brain({"THREAT": 0.9, "ANXIETY": 0.9, "SEEKING": 0.3}, seed=2)
        m = EnvironmentMatrix()
        thing = Thing("danger", "a danger", "creature", {"threat": 0.9})
        for _ in range(5):
            encounter(brain, thing, m)
        self.assertGreater(m.bond("danger").aversion, 0.0)

    def test_encounter_records_which_system_fired(self):
        brain = _brain({"SEEKING": 0.9}, seed=3)
        m = EnvironmentMatrix()
        encounter(brain, Thing("t", "t", stimulus={"reward_cue": 0.8}), m)
        self.assertTrue(sum(m.bond("t").system_counts.values()) == 1)


class TestEmergentAndPersonSpecific(unittest.TestCase):
    """The heart of it: disposition to a thing is the person's own, and emerges
    -- two temperaments can feel oppositely about the same thing."""

    def test_same_thing_different_people(self):
        snake = Thing("snake", "a snake", "creature", {"threat": 0.9, "novelty": 0.4})
        m_bold = EnvironmentMatrix(); m_fear = EnvironmentMatrix()
        bold = _brain({"THREAT": 0.15, "ANXIETY": 0.15, "SEEKING": 0.85}, seed=4)
        fearful = _brain({"THREAT": 0.9, "ANXIETY": 0.9, "SEEKING": 0.3}, seed=5)
        for _ in range(6):
            encounter(bold, snake, m_bold)
            encounter(fearful, snake, m_fear)
        # the fearful person is more averse to the snake than the bold one --
        # emergent from their substrates, not stipulated
        self.assertGreater(m_fear.disposition_to("snake") * -1,
                           m_bold.disposition_to("snake") * -1 - 1e-9)
        # (i.e. fearful person's disposition is lower/more negative)
        self.assertLessEqual(m_fear.disposition_to("snake"),
                             m_bold.disposition_to("snake"))


class TestInventory(unittest.TestCase):
    def test_attractions_and_aversions_sorted(self):
        brain = _brain({"SEEKING": 0.8, "THREAT": 0.7, "ANXIETY": 0.7}, seed=6)
        m = EnvironmentMatrix()
        for _ in range(5):
            encounter(brain, Thing("good", "g", stimulus={"reward_cue": 0.9}), m)
            encounter(brain, Thing("bad", "b", stimulus={"threat": 0.9}), m)
        att = m.attractions()
        avr = m.aversions()
        self.assertTrue(all(b.disposition() > 0 for b in att))
        self.assertTrue(all(b.disposition() < 0 for b in avr))


if __name__ == "__main__":
    unittest.main(verbosity=2)


import unittest as _ut


class TestEnvironmentMatrixWiredIntoLife(_ut.TestCase):
    """The environment matrix wired into the living world: as children live, they
    encounter the world's things and build inventories of attraction/aversion,
    and inherited birth leans EVOLVE through experience (differently per child)."""

    def _run(self):
        import sys, os
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, os.path.join(root, "core"))
        sys.path.insert(0, os.path.join(root, "extensions"))
        from sim_world import TimeController, TimeScale
        from project import ProjectSpec, spawn_universe
        from sophropathy import make_life_stepper
        uni = spawn_universe(ProjectSpec(name="P", target_population=120,
                             profile="england_2021", extensions=["sophropathy"],
                             fearless_frac=0.3, seed=3), place_residents=False)
        step = make_life_stepper(uni, seed=1)
        TimeController(step).run(TimeScale.YEAR, steps=22)
        return step

    def test_children_build_inventories(self):
        step = self._run()
        mats = [d["env_matrix"] for d in step.dev.values() if d.get("env_matrix")]
        self.assertTrue(mats)
        # at least some child has accrued a bond with encounters recorded
        self.assertTrue(any(any(b.encounters > 0 for b in m.bonds.values())
                            for m in mats))

    def test_inherited_predator_lean_evolves_and_differs(self):
        step = self._run()
        preds = [d["env_matrix"].bonds["snake_spider"].disposition()
                 for d in step.dev.values()
                 if d.get("env_matrix") and "snake_spider" in d["env_matrix"].bonds]
        self.assertTrue(preds)
        # the -0.25 birth lean has NOT stayed fixed: children differ (some deepen
        # it, some erode/overwrite it) -- emergent, not decreed
        # a rarely-encountered inherited-lean thing evolves modestly but still
        # DIFFERS across children (some deepen it, some erode it) -- emergent
        self.assertGreater(max(preds) - min(preds), 0.1)


if __name__ == "__main__":
    _ut.main(verbosity=2)

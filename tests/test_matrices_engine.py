import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""Phase 3 (PsychSim_MASTER) -- the three matrices adopt the one engine.
Relationship matrix: Dunbar layered capacity, slot allocation by |salience|, the enemy and
ambivalent cases. Environment/group entries acquire RPE value. Directional/structural only."""

import random
import unittest

from sim_world.relations import (RelationshipMatrix, RelationshipSlot, DUNBAR_LAYERS)
from sim_world.environment_matrix import Thing, EnvironmentMatrix, encounter
from sim_world.group_matrix import Group, GroupMatrix, group_encounter
from affective_engine.core import TraitSeed
from affective_engine.agent import AffectiveAgent
_G = {"THREAT": 0.5, "ANXIETY": 0.5, "SEEKING": 0.5, "FRUSTRATION": 0.5,
      "CARE": 0.5, "SOCIAL_LOSS": 0.5, "CONTROL": 0.5, "INSTRUMENTAL_CONTROL": 0.5}
def _mk_agent(seed=2):
    return AffectiveAgent(seed=TraitSeed("t", gains=dict(_G)), temperament_seed=seed)


class TestDunbarSlots(unittest.TestCase):
    def test_capacity_and_eviction_by_salience(self):
        rm = RelationshipMatrix()
        # 200 acquaintances of increasing salience (later ones move the agent more)
        for i in range(200):
            rm.observe(f"person{i:03d}", r=0.1, attachment_pull=i / 200.0)
        self.assertLessEqual(len(rm.slots), DUNBAR_LAYERS[-1])   # capped at ~150
        # the LOW-salience early ones were evicted; a high-salience late one survives
        self.assertNotIn("person000", rm.slots)
        self.assertIn("person199", rm.slots)

    def test_inner_circle_is_most_salient(self):
        rm = RelationshipMatrix()
        rm.observe("close", r=0.5, attachment_pull=0.9)
        for i in range(20):
            rm.observe(f"acq{i}", r=0.05, attachment_pull=0.1)
        inner = [s.entity for s in rm.inner_circle()]
        self.assertIn("close", inner)
        self.assertEqual(rm.layer_of("close"), 0)

    def test_slots_decay_without_contact_and_evict(self):
        rm = RelationshipMatrix()
        rm.observe("faded", r=0.1, attachment_pull=0.3)
        base = rm.slots["faded"].salience
        for _ in range(50):
            rm.tick()
        self.assertTrue("faded" not in rm.slots or rm.slots["faded"].salience < base)


class TestEnemyAndAmbivalent(unittest.TestCase):
    def test_enemy_holds_an_inner_slot(self):
        # an abuser/rival: strongly NEGATIVE value but high salience -> occupies an inner
        # slot and would control behaviour (App. 4.2), even surrounded by pleasant others.
        rm = RelationshipMatrix()
        for _ in range(6):
            rm.observe("rival", r=-0.6, threat_pull=0.9)
        for i in range(10):
            rm.observe(f"pleasant{i}", r=0.2, attachment_pull=0.15)
        slot = rm.slots["rival"]
        self.assertEqual(slot.valence_sign, -1)
        self.assertEqual(rm.layer_of("rival"), 0)
        self.assertIn("rival", [s.entity for s in rm.enemies()])

    def test_ambivalent_bond_is_flagged(self):
        # attachment AND threat both high toward the SAME person (App. 4.3)
        rm = RelationshipMatrix()
        for _ in range(6):
            rm.observe("parent", r=-0.1, attachment_pull=0.8, threat_pull=0.7)
        slot = rm.slots["parent"]
        self.assertTrue(slot.ambivalent)
        self.assertIn("parent", [s.entity for s in rm.ambivalent_bonds()])

    def test_a_purely_warm_bond_is_not_ambivalent(self):
        rm = RelationshipMatrix()
        for _ in range(6):
            rm.observe("friend", r=0.4, attachment_pull=0.8, threat_pull=0.0)
        self.assertFalse(rm.slots["friend"].ambivalent)


class TestRelationshipValueByRPE(unittest.TestCase):
    def test_repeated_warmth_builds_positive_value(self):
        rm = RelationshipMatrix()
        for _ in range(10):
            rm.observe("ally", r=0.4, attachment_pull=0.5)
        self.assertGreater(rm.slots["ally"].value, 0.0)

    def test_betrayal_writes_negative_value(self):
        rm = RelationshipMatrix()
        for _ in range(10):
            rm.observe("betrayer", r=-0.5, threat_pull=0.6)
        self.assertLess(rm.slots["betrayer"].value, 0.0)


class TestEnvironmentValue(unittest.TestCase):
    def _brain(self):
        return _mk_agent(2)

    def test_food_acquires_positive_value(self):
        m = EnvironmentMatrix()
        food = Thing("apple", "an apple", "food")
        a = self._brain()
        for _ in range(8):
            encounter(a, food, m)
        self.assertGreater(m.bond("apple").value, 0.0)

    def test_nature_acquires_positive_value(self):
        m = EnvironmentMatrix()
        wood = Thing("wood", "the wood", "plant")
        a = self._brain()
        for _ in range(8):
            encounter(a, wood, m)
        self.assertGreater(m.bond("wood").value, 0.0)   # nature reduces arousal (App. 3.2)

    def test_painful_thing_acquires_negative_value(self):
        m = EnvironmentMatrix()
        stove = Thing("stove", "a hot stove", "object", perturbation={"nociception": 0.7})
        a = self._brain()
        for _ in range(8):
            encounter(a, stove, m)
        self.assertLess(m.bond("stove").value, 0.0)

    def test_plain_object_has_no_innate_value(self):
        m = EnvironmentMatrix()
        rock = Thing("rock", "a rock", "object")
        a = self._brain()
        for _ in range(5):
            encounter(a, rock, m)
        self.assertEqual(m.bond("rock").value, 0.0)     # learned only, not innate


class TestGroupValueAndSynchrony(unittest.TestCase):
    def _team(self):
        return Group("team", "a team", "team", cohesion=0.6, norm_strength=0.6)

    def test_acceptance_builds_positive_group_value(self):
        brain = _mk_agent(1)
        gm = GroupMatrix(); mem = gm.membership("team", "team")
        for _ in range(8):
            group_encounter(brain, self._team(), mem, "acceptance", age_years=12)
        self.assertGreater(mem.value, 0.0)

    def test_synchrony_adds_belonging_endorphin(self):
        brain = _mk_agent(1)
        gm = GroupMatrix()
        m_sync = gm.membership("choir", "team")
        m_plain = gm.membership("club", "team")
        team = self._team()
        for _ in range(6):
            group_encounter(brain, team, m_sync, "synchrony", age_years=12)
            group_encounter(brain, team, m_plain, "acceptance", age_years=12)
        self.assertGreater(m_sync.belonging, m_plain.belonging)

    def test_sociometer_tracks_belonging(self):
        brain = _mk_agent(1)
        gm = GroupMatrix(); mem = gm.membership("team", "team")
        for _ in range(8):
            group_encounter(brain, self._team(), mem, "acceptance", age_years=12)
        # esteem (the sociometer) has moved in the same direction as belonging
        self.assertGreater(mem.sociometer(), 0.0)


if __name__ == "__main__":
    unittest.main()

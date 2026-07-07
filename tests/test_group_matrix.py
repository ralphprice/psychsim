import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

"""The group matrix (third interface matrix): a person's standing and belonging in
groups, emergent from the substrate. Tests check the machinery and the grounded
dominance-vs-prestige distinction (Henrich & Gil-White) -- that status route
EMERGES from temperament, never typed in."""
import random
import unittest
from affective_engine.drives import Brain, System
from sim_world.group_matrix import (Group, Membership, GroupMatrix, group_encounter,
                                     default_groups, sample_encounter_type,
                                     ENCOUNTER_STIMULI)


class TestGroupMatrix(unittest.TestCase):
    def _team(self):
        return Group("team", "a team", "team", cohesion=0.6, norm_strength=0.6)

    def test_encounter_updates_membership_from_the_substrate(self):
        brain = Brain.from_temperament(random.Random(1))
        m = GroupMatrix(); mem = m.membership("team", "team")
        r = random.Random(3)
        for _ in range(20):
            group_encounter(brain, self._team(), mem, sample_encounter_type(r), age_years=12)
        self.assertGreater(mem.encounters, 0)
        self.assertTrue(-1.0 <= mem.belonging <= 1.0)
        self.assertTrue(0.0 <= mem.standing <= 1.0)
        self.assertIn(mem.state(), ("unknown", "excluded", "peripheral", "member",
                                    "belonging", "central"))

    def test_status_route_emerges_dominance_vs_prestige(self):
        # a strongly dominance-disposed temperament takes rank by DOMINANCE; a
        # prosocial one earns it by PRESTIGE -- emergent, not decreed
        dom_brain = Brain.from_temperament(random.Random(1),
                        {System.RAGE: 0.95, System.SEEKING: 0.15, System.CARE: 0.1})
        pro_brain = Brain.from_temperament(random.Random(1),
                        {System.CARE: 0.85, System.SEEKING: 0.7, System.RAGE: 0.15})

        def run(brain):
            m = GroupMatrix(); mem = m.membership("team", "team"); r = random.Random(7)
            for _ in range(40):
                group_encounter(brain, self._team(), mem, sample_encounter_type(r), age_years=12)
            return mem

        dom, pro = run(dom_brain), run(pro_brain)
        self.assertGreater(dom.dominance_route, pro.dominance_route)   # coercive: more dominance
        self.assertGreater(pro.prestige_route, dom.dominance_route)    # prosocial: earns by prestige

    def test_encounter_stimuli_are_neutral_bundles(self):
        for kind, stim in ENCOUNTER_STIMULI.items():
            self.assertTrue(stim)
            self.assertTrue(all(0.0 <= v <= 1.0 for v in stim.values()))

    def test_matrix_reads_out_identity_and_rank(self):
        brain = Brain.from_temperament(random.Random(1), {System.CARE: 0.8})
        m = GroupMatrix()
        for g in default_groups():
            mem = m.membership(g.id, g.kind); r = random.Random(2)
            for _ in range(15):
                group_encounter(brain, g, mem, "acceptance", age_years=10)
        self.assertTrue(m.identities())          # belongs to some groups
        self.assertTrue(m.ranks())


class TestGroupMatrixWiredIntoLife(unittest.TestCase):
    def test_children_accumulate_group_memberships(self):
        from sim_world import TimeController, TimeScale
        from project import ProjectSpec, spawn_universe
        from sophropathy import make_life_stepper
        uni = spawn_universe(ProjectSpec(name="P", target_population=100,
                             profile="england_2021", extensions=["sophropathy"],
                             fearless_frac=0.4, seed=3), place_residents=False)
        step = make_life_stepper(uni, seed=1)
        TimeController(step).run(TimeScale.YEAR, steps=22)
        gms = [d["group_matrix"] for d in step.dev.values() if d.get("group_matrix")]
        self.assertTrue(gms)
        self.assertTrue(any(any(mem.encounters > 0 for mem in gm.memberships.values())
                            for gm in gms))


if __name__ == "__main__":
    unittest.main(verbosity=2)

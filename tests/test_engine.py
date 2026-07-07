import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

"""The live step-loop engine behind the streaming server: continuous stepping,
JSON-serialisable snapshots, per-person inspection, and live controls."""
import json
import unittest
from sophropathy.engine import SimEngine


class TestSimEngine(unittest.TestCase):
    def test_steps_continuously_and_clock_advances(self):
        e = SimEngine(population=50, seed=7, tick_minutes=15)
        c0 = e.clock_label()
        for _ in range(20):
            e.step()
        self.assertEqual(e.step_count, 20)
        self.assertNotEqual(e.clock_label(), c0)     # time moved on

    def test_snapshot_is_json_serialisable(self):
        e = SimEngine(population=40, seed=7)
        e.step()
        json.dumps(e.snapshot())                     # must not raise
        json.dumps(e.town())

    def test_snapshot_has_people_with_positions_and_drives(self):
        e = SimEngine(population=40, seed=7)
        snap = e.snapshot()
        self.assertTrue(snap["people"])
        one = next(iter(snap["people"].values()))
        self.assertIn("x", one); self.assertIn("y", one); self.assertIn("drive", one)

    def test_person_detail_has_networks_memories_groups(self):
        e = SimEngine(population=40, seed=7)
        for _ in range(30):
            e.step()
        cid = next(iter(e.snapshot()["people"]))
        d = e.person_detail(cid)
        self.assertEqual(len(d["systems"]), 7)
        self.assertIn("memories", d)
        self.assertIn("groups", d)

    def test_plan_is_json_serialisable_svg_with_mapping(self):
        e = SimEngine(population=40, seed=7)
        p = e.plan(cell=64)
        json.dumps(p)                                # must not raise
        self.assertTrue(p["svg"].startswith("<svg"))
        self.assertIn("</svg>", p["svg"])
        # the grid->pixel mapping the frontend overlays people with
        self.assertEqual(p["cell"], 64)
        self.assertEqual(p["width"], p["cols"] * 64 + 2 * p["pad"])
        self.assertEqual(p["height"], p["rows"] * 64 + 2 * p["pad"])
        # plan grid dims agree with the grid-view town geometry
        t = e.town()
        self.assertEqual((p["cols"], p["rows"]), (t["cols"], t["rows"]))

    def test_save_load_round_trip(self):
        import tempfile
        e = SimEngine(population=25, seed=7)
        for _ in range(15):
            e.step()
        with tempfile.TemporaryDirectory() as d:
            meta = e.save("My Run!", directory=d)
            self.assertTrue(meta["slug"])                # name was slugged to a safe stem
            self.assertEqual(meta["clock"], e.clock_label())

            saves = SimEngine.list_saves(directory=d)
            self.assertEqual(len(saves), 1)
            self.assertEqual(saves[0]["slug"], meta["slug"])

            loaded = SimEngine.load(meta["slug"], directory=d)
            self.assertEqual(loaded.snapshot(), e.snapshot())   # evolved state preserved
            cid = next(iter(e.snapshot()["people"]))
            self.assertEqual(loaded.person_detail(cid), e.person_detail(cid))

            loaded.step()                                # the reloaded world keeps running
            self.assertEqual(loaded.step_count, e.step_count + 1)

            self.assertTrue(SimEngine.delete_save(meta["slug"], directory=d))
            self.assertEqual(SimEngine.list_saves(directory=d), [])

    def test_live_controls(self):
        e = SimEngine(population=40, seed=7)
        e.set_tick_minutes(30); self.assertEqual(e.tick_minutes, 30)
        n0 = len(e.snapshot()["people"])
        cid = e.add_person("child")
        self.assertTrue(cid)
        self.assertEqual(len(e.snapshot()["people"]), n0 + 1)
        e.respawn(population=25)                      # fresh town, clock reset
        self.assertEqual(e.minutes, 0)

    def test_experiment_mode_freezes_background_evolves_subjects(self):
        e = SimEngine(population=40, seed=7, experiment=True)
        snap = e.snapshot()
        self.assertTrue(snap["experiment"])
        self.assertGreater(snap["subjects"], 0)
        self.assertGreater(snap["background"], 0)
        bg = [c for c, p in snap["people"].items() if not p["subject"]]
        subj = [c for c, p in snap["people"].items() if p["subject"]]
        bg0 = {c: e.pop.persons[c].mind.brain.to_dict() for c in bg}
        subj0 = {c: e.pop.persons[c].mind.brain.to_dict() for c in subj}
        for _ in range(400):
            e.step()
        # every background personality is fixed; at least one subject evolved
        self.assertTrue(all(bg0[c] == e.pop.persons[c].mind.brain.to_dict() for c in bg))
        self.assertTrue(any(subj0[c] != e.pop.persons[c].mind.brain.to_dict() for c in subj))

    def test_experiment_subjects_default_children_and_explicit_override(self):
        e = SimEngine(population=40, seed=7, experiment=True)
        children = {c for c, (is_child, _, _) in e.info.items() if is_child}
        self.assertEqual(e.subjects, children)                 # default: children
        one = sorted(e.info)[0]
        e2 = SimEngine(population=40, seed=7, experiment=True, study_subjects=[one])
        self.assertEqual(e2.subjects, {one})                   # explicit list overrides

    def test_experiment_engine_still_saves_and_loads(self):
        import tempfile
        e = SimEngine(population=25, seed=7, experiment=True)
        for _ in range(10):
            e.step()
        with tempfile.TemporaryDirectory() as d:
            meta = e.save("exp", directory=d)
            loaded = SimEngine.load(meta["slug"], directory=d)
        self.assertTrue(loaded.experiment)
        self.assertEqual(loaded.frozen, e.frozen)
        self.assertEqual(loaded.snapshot()["people"], e.snapshot()["people"])

    def test_author_subject_by_temperament(self):
        from affective_engine.drives import System

        def mean_fear_reactivity(temperament, seed):
            e = SimEngine(population=30, seed=seed)
            cids = [e.add_person("child", temperament=temperament) for _ in range(8)]
            return sum(e.pop.persons[c].mind.brain.drives[System.FEAR].reactivity
                       for c in cids) / len(cids)

        # GIVEN temperament is a reactivity BIAS (individual draws vary): a fearless
        # cohort has lower mean FEAR reactivity than a typical one.
        self.assertLess(mean_fear_reactivity("fearless", 7),
                        mean_fear_reactivity("typical", 7))
        # authoring is reproducible now that the fresh mind is seeded from the engine rng
        self.assertEqual(mean_fear_reactivity("fearless", 7),
                         mean_fear_reactivity("fearless", 7))

    def test_authored_subject_is_tracked_and_live(self):
        e = SimEngine(population=30, seed=7)
        f = e.add_person("child", temperament="fearless")
        self.assertIn(f, e.subjects)                       # a live study subject
        self.assertNotIn(f, e.frozen)
        self.assertEqual(e.person_detail(f)["temperament"], "fearless")

    def test_authored_subject_evolves_live_in_experiment_mode(self):
        e = SimEngine(population=30, seed=7, experiment=True)
        cid = e.add_person("child", temperament="fearless")
        self.assertIn(cid, e.subjects)
        self.assertNotIn(cid, e.frozen)                    # authored -> live, not background
        before = e.pop.persons[cid].mind.brain.to_dict()
        for _ in range(400):
            e.step()
        self.assertNotEqual(before, e.pop.persons[cid].mind.brain.to_dict())


if __name__ == "__main__":
    unittest.main(verbosity=2)

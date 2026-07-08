import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""Part 4 S8.5 -- N independent substrate instances in one shared world.

The honesty crux is INDEPENDENCE: the parallelism is only honest if the substrates do not bleed.
The key test proves that developing one instance never perturbs another."""

import unittest

from substrate.model import load_substrate
from substrate.engine import SubstrateEngine
from agent_bank import DevelopedAgent, AgentBank
from parallel_world import ParallelWorld

_MODEL = load_substrate()


class TestIndependence(unittest.TestCase):
    """Substrates must not bleed (S8.5) -- else a per-slot effect is confounded."""

    def test_developing_one_instance_does_not_change_another(self):
        pw = ParallelWorld(_MODEL)
        pw.spawn_newborn("a", age=5.0)
        pw.spawn_newborn("b", age=5.0)
        b_before = list(pw.instances["b"].agent.engine.weight)
        # heavily develop ONLY instance 'a'
        a = pw.instances["a"].agent.engine
        for _ in range(30):
            a.clear_inputs(); a.inject_channel("IN-SOMATO:affective_touch", 0.7); a.settle(3)
        self.assertNotEqual(list(a.weight), b_before)              # 'a' developed
        self.assertEqual(pw.instances["b"].agent.engine.weight, b_before)  # 'b' untouched

    def test_instances_hold_separate_engine_objects(self):
        pw = ParallelWorld(_MODEL)
        pw.spawn_newborn("a"); pw.spawn_newborn("b")
        self.assertIsNot(pw.instances["a"].agent.engine, pw.instances["b"].agent.engine)
        self.assertIsNot(pw.instances["a"].agent.engine.weight,
                         pw.instances["b"].agent.engine.weight)


class TestPerSlotSettings(unittest.TestCase):
    def test_each_slot_carries_its_own_settings(self):
        pw = ParallelWorld(_MODEL)
        pw.spawn_newborn("a", settings={"throttle": 0.0})
        pw.spawn_newborn("b", settings={"throttle": 0.7})
        self.assertEqual(pw.instances["a"].settings["throttle"], 0.0)
        self.assertEqual(pw.instances["b"].settings["throttle"], 0.7)


class TestSpawnSources(unittest.TestCase):
    def test_spawn_newborn_grown_and_banked(self):
        # a banked adult can be re-instantiated into a slot and resumes (S11 x S8.5)
        eng = SubstrateEngine(_MODEL, age_years=25.0)
        grown = DevelopedAgent(engine=eng, provenance={"source": "grown"})
        bank = AgentBank(); bank.bank(grown, "adult1", provenance={"rng_seed": 3})

        pw = ParallelWorld(_MODEL)
        pw.spawn_newborn("fresh", age=0.5)
        pw.spawn_from_agent("grown", grown)
        pw.spawn_banked("rehydrated", bank, "adult1")
        self.assertEqual(len(pw), 3)
        self.assertEqual(pw.instances["rehydrated"].agent.provenance["rng_seed"], 3)
        # the rehydrated adult keeps developing (not frozen)
        r = pw.instances["rehydrated"].agent.engine
        before = list(r.weight)
        r.clear_inputs(); r.inject_channel("IN-SOMATO:affective_touch", 0.6)
        for _ in range(15):
            r.settle(3)
        self.assertNotEqual(before, r.weight)


class TestSharedWorldAndReadout(unittest.TestCase):
    def test_step_all_and_read_all(self):
        pw = ParallelWorld(_MODEL, world={"place": "one room"})
        pw.spawn_newborn("a", age=10.0); pw.spawn_newborn("b", age=10.0)
        pw.step_all(3)
        ages = pw.read_all(lambda ag: ag.age_years)
        self.assertEqual(set(ages), {"a", "b"})
        self.assertEqual(pw.world["place"], "one room")   # a shared read context

    def test_occupied_slot_rejects_double_spawn(self):
        pw = ParallelWorld(_MODEL)
        pw.spawn_newborn("a")
        with self.assertRaises(ValueError):
            pw.spawn_newborn("a")


if __name__ == "__main__":
    unittest.main()

import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

"""The executive-function layer: a MONITORED self-awareness state with NO direct
effect. Tests check the machinery (matures with development, moral orientation is a
read-out of the substrate, purpose accrues with deliberation) and, critically, that
it does NOT change behaviour."""
import random
import unittest
from affective_engine.drives import Brain, System
from affective_engine.executive import (Executive, monitor_executive,
                                         maturation_ceiling, moral_orientation_readout)


class TestExecutive(unittest.TestCase):
    def test_capacity_matures_with_development(self):
        # PFC matures slowly, peaks ~mid-20s
        self.assertLess(maturation_ceiling(3), maturation_ceiling(14))
        self.assertLess(maturation_ceiling(14), maturation_ceiling(25))
        self.assertEqual(maturation_ceiling(25), 1.0)
        self.assertEqual(maturation_ceiling(40), 1.0)  # ceiling, not decline

    def test_monitoring_matures_the_capacities(self):
        b = Brain.from_temperament(random.Random(1))
        ex = Executive()
        start = ex.inhibitory_capacity
        for i in range(50):
            monitor_executive(ex, b, age_years=20 * i / 50)
        self.assertGreater(ex.inhibitory_capacity, start)

    def test_moral_orientation_is_a_readout_of_the_substrate(self):
        # a caring wiring reads high; a psychopathic-leaning one reads low -- reflects
        # the substrate, is not imposed
        pro = Brain.from_temperament(random.Random(1), {System.CARE: 0.9})
        psy = Brain.from_temperament(random.Random(1), {System.CARE: 0.1, System.RAGE: 0.8})
        pro.drives[System.CARE].strength = 0.9
        psy.drives[System.RAGE].strength = 0.9
        self.assertGreater(moral_orientation_readout(pro), moral_orientation_readout(psy))

    def test_purpose_accrues_only_with_deliberation(self):
        b = Brain.from_temperament(random.Random(1))
        engaged, idle = Executive(), Executive()
        for i in range(60):
            age = 25 * i / 60
            monitor_executive(engaged, b, age, deliberative=True)
            monitor_executive(idle, b, age, deliberative=False)
        self.assertGreater(engaged.purpose, idle.purpose)
        self.assertEqual(idle.purpose, 0.0)

    def test_monitoring_has_NO_effect_on_behaviour(self):
        # the whole point: the executive layer is observed, not applied
        b = Brain.from_temperament(random.Random(5))
        stim = {"threat": 0.8}
        before = b.respond(stim).dominant
        ex = Executive()
        monitor_executive(ex, b, age_years=22, deliberative=True)
        after = b.respond(stim).dominant
        self.assertEqual(before, after)

    def test_self_awareness_and_note_are_valid(self):
        ex = Executive(inhibitory_capacity=0.7, deliberation=0.7,
                       moral_orientation=0.1, purpose=0.5)
        self.assertTrue(0.0 <= ex.self_awareness() <= 1.0)
        # low moral + high deliberation -> the 'uncoupled' observation (not a verdict)
        self.assertIn("uncoupled", ex.note())


class TestExecutiveWiredIntoLife(unittest.TestCase):
    def test_children_accumulate_a_monitored_executive_state(self):
        from sim_world import TimeController, TimeScale
        from project import ProjectSpec, spawn_universe
        from sophropathy import make_life_stepper
        uni = spawn_universe(ProjectSpec(name="P", target_population=100,
                             profile="england_2021", extensions=["sophropathy"],
                             fearless_frac=0.4, seed=3), place_residents=False)
        step = make_life_stepper(uni, seed=1)
        TimeController(step).run(TimeScale.YEAR, steps=22)
        exs = [d["executive"] for d in step.dev.values() if d.get("executive")]
        self.assertTrue(exs)
        # capacity has matured above the newborn floor for at least some children
        self.assertTrue(any(ex.inhibitory_capacity > 0.2 for ex in exs))


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestExecutiveAlwaysOn(unittest.TestCase):
    """The executive as an ALWAYS-ON layer: consulted on every brain event, acting
    only on patterns it has learned to monitor, with a direct inhibitory effect when
    it fires -- gated by maturation. The learned CONTENT is deferred; these test the
    mechanism."""

    def test_consulted_on_every_event_but_empty_registry_is_a_noop(self):
        b = Brain.from_temperament(random.Random(5), {System.RAGE: 0.9})
        b.executive = Executive(inhibitory_capacity=0.9)   # mature, nothing learned
        stim = {"thwarting": 0.8, "restraint": 0.5}
        before = b.respond(stim).dominant
        after = b.respond(stim).dominant
        self.assertEqual(before, after)               # no effect on outcome
        self.assertEqual(b.executive.checks, 2)       # but it WAS consulted each event
        self.assertEqual(b.executive.fired, 0)

    def test_a_learned_pattern_inhibits_gated_by_maturation(self):
        from affective_engine.executive import MonitoredPattern
        patt = MonitoredPattern("inhibit prepotent RAGE",
                                matches=lambda dom, act, stim: dom is System.RAGE,
                                target=System.RAGE, kind="inhibit")

        def rage_activation(cap):
            b = Brain.from_temperament(random.Random(5), {System.RAGE: 0.9})
            ex = Executive(inhibitory_capacity=cap); ex.learn_to_monitor(patt)
            b.executive = ex
            r = b.respond({"thwarting": 0.8, "restraint": 0.5})
            return r.activations[System.RAGE], ex.fired

        base, _ = (Brain.from_temperament(random.Random(5), {System.RAGE: 0.9})
                   .respond({"thwarting": 0.8, "restraint": 0.5}).activations[System.RAGE], 0)
        immature, f_i = rage_activation(0.15)
        mature, f_m = rage_activation(0.9)
        self.assertGreater(f_i, 0)                    # it fired (pattern matched)
        self.assertGreater(f_m, 0)
        self.assertLess(mature, immature)             # mature inhibits more
        self.assertLess(immature, base)               # both reduce the prepotent drive

    def test_children_executives_are_consulted_across_life(self):
        from sim_world import TimeController, TimeScale
        from project import ProjectSpec, spawn_universe
        from sophropathy import make_life_stepper
        uni = spawn_universe(ProjectSpec(name="P", target_population=80,
                             profile="england_2021", extensions=["sophropathy"],
                             fearless_frac=0.4, seed=3), place_residents=False)
        step = make_life_stepper(uni, seed=1)
        TimeController(step).run(TimeScale.YEAR, steps=22)
        exs = [d["executive"] for d in step.dev.values() if d.get("executive")]
        self.assertTrue(exs)
        self.assertTrue(all(e.checks > 0 for e in exs))   # always-on: consulted every event


class TestMemoryInstallsMonitors(unittest.TestCase):
    """How MEMORY installs what the executive monitors: reversal/reinforcement learning
    of response inhibition. The installer learns, from remembered outcomes, which
    prepotent drive to inhibit -- emergent from history, never hand-picked."""

    def _mem(self, entries):
        from affective_engine.core import Appraisal
        from affective_engine.memory import MemoryStream
        m = MemoryStream()
        for dom, val, k in entries:
            for _ in range(k):
                m.add("e", Appraisal(label="e"), dom, valence=val, importance=0.5)
        return m

    def test_installs_monitor_for_a_net_costly_drive_only(self):
        from affective_engine.executive import install_monitors_from_memory
        mem = self._mem([("RAGE", -0.5, 6), ("SEEKING", +0.4, 6)])
        ex = Executive(inhibitory_capacity=0.9)
        installed = install_monitors_from_memory(ex, mem)
        targets = {p.target for p in ex.monitors}
        self.assertIn(System.RAGE, targets)        # kept costing -> learned to inhibit
        self.assertNotIn(System.SEEKING, targets)  # went well -> not inhibited
        self.assertEqual(len(installed), 1)

    def test_learned_monitor_then_inhibits_that_drive(self):
        from affective_engine.executive import install_monitors_from_memory
        import random
        mem = self._mem([("RAGE", -0.5, 6)])
        ex = Executive(inhibitory_capacity=0.9); install_monitors_from_memory(ex, mem)
        b = Brain.from_temperament(random.Random(5), {System.RAGE: 0.9}); b.executive = ex
        base = Brain.from_temperament(random.Random(5), {System.RAGE: 0.9}) \
            .respond({"thwarting": 0.8, "restraint": 0.5}).activations[System.RAGE]
        withx = b.respond({"thwarting": 0.8, "restraint": 0.5}).activations[System.RAGE]
        self.assertLess(withx, base)               # the lesson now damps the drive

    def test_clean_history_learns_nothing_and_is_idempotent(self):
        from affective_engine.executive import install_monitors_from_memory
        mem = self._mem([("SEEKING", +0.3, 6), ("PLAY", +0.2, 6)])
        ex = Executive(inhibitory_capacity=0.9)
        self.assertEqual(len(install_monitors_from_memory(ex, mem)), 0)  # nothing to regulate
        costly = self._mem([("RAGE", -0.5, 6)])
        install_monitors_from_memory(ex, costly)
        self.assertEqual(len(install_monitors_from_memory(ex, costly)), 0)  # idempotent

    def test_below_min_events_does_not_learn(self):
        from affective_engine.executive import install_monitors_from_memory
        mem = self._mem([("RAGE", -0.9, 2)])           # costly but too few instances
        ex = Executive(inhibitory_capacity=0.9)
        self.assertEqual(len(install_monitors_from_memory(ex, mem)), 0)

    def test_installer_runs_in_the_life_stepper(self):
        # the installer runs end-to-end without error and memory is recorded; whether any
        # monitor is learned depends on the (crude) environment's outcomes
        from sim_world import TimeController, TimeScale
        from project import ProjectSpec, spawn_universe
        from sophropathy import make_life_stepper
        uni = spawn_universe(ProjectSpec(name="P", target_population=80,
                             profile="england_2021", extensions=["sophropathy"],
                             fearless_frac=0.5, seed=3), place_residents=False)
        step = make_life_stepper(uni, seed=1)
        TimeController(step).run(TimeScale.YEAR, steps=22)
        mems = [len(d["mind"].memory.events) for d in step.dev.values() if d.get("mind")]
        self.assertTrue(any(n > 0 for n in mems))   # outcomes are recorded to memory


if __name__ == "__main__":
    unittest.main(verbosity=2)

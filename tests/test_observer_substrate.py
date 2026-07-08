import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""Part 6 substrate-social phase (3b) -- the circuit observer adapter.

Fills observer.py's parked profile_from_legacy slot with a circuit-engine adapter that measures
social/behavioural constructs over the developed substrate's EMERGENT activity. The load-bearing
property is READ-ONLY: probing measures but never develops the agent, and nothing it computes is
fed back into behaviour."""

import unittest

from substrate.model import load_substrate
from substrate.engine import SubstrateEngine
from affective_engine.observer import (profile_from_substrate, observe_substrate,
                                        BehaviourProfile, read_out)

_MODEL = load_substrate()


def _grow(cue: str, ticks: int = 120, age: float = 25.0) -> SubstrateEngine:
    e = SubstrateEngine(_MODEL, age_years=0.5)
    for i in range(ticks):
        e.set_age(0.5 + age * i / ticks)
        e.clear_inputs(); e.inject_channel(cue, 0.7); e.settle(3)
    e.set_age(age)
    return e


class TestReadOnly(unittest.TestCase):
    """The observer adapter must not develop the agent (no feedback into the substrate)."""

    def test_profiling_leaves_the_developed_state_bit_identical(self):
        e = _grow("IN-SOMATO:affective_touch")
        w0, x0, t0 = list(e.weight), list(e.exp_count), dict(e.theta)
        profile_from_substrate(e)
        self.assertEqual(e.weight, w0)          # weights unchanged
        self.assertEqual(e.exp_count, x0)       # experience counts unchanged
        self.assertEqual(e.theta, t0)           # BCM thresholds unchanged

    def test_repeated_profiling_is_stable(self):
        e = _grow("IN-SOMATO:affective_touch")
        p1 = profile_from_substrate(e)
        p2 = profile_from_substrate(e)
        self.assertEqual(p1.fear, p2.fear)
        self.assertEqual(p1.care, p2.care)


class TestProfileIsAMeasurement(unittest.TestCase):
    def test_profile_fields_are_bounded_readouts(self):
        p = profile_from_substrate(_grow("IN-SOMATO:affective_touch"))
        self.assertIsInstance(p, BehaviourProfile)
        for v in (p.fear, p.seeking, p.care, p.restraint, p.moral_orientation,
                  p.reactive_aggression, p.vicarious_response, p.punishment_sensitivity):
            self.assertTrue(0.0 <= v <= 1.0)

    def test_constructs_compute_over_the_substrate_profile(self):
        out = observe_substrate(_grow("IN-SOMATO:affective_touch"))
        for key in ("triarchic", "callous_unemotional", "empathy", "aggression",
                    "passive_avoidance_deficit"):
            self.assertIn(key, out)
        self.assertNotIn("psychopathy", out)    # no single verdict -- measurement only

    def test_restraint_grows_with_maturation(self):
        # a read-out property: executive control capacity is higher in an adult than a child
        child = profile_from_substrate(_grow("IN-SOMATO:affective_touch", age=8.0))
        adult = profile_from_substrate(_grow("IN-SOMATO:affective_touch", age=30.0))
        self.assertGreater(adult.restraint, child.restraint)


if __name__ == "__main__":
    unittest.main()

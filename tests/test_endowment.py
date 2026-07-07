import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""Phase 5 (PsychSim_MASTER) -- endowment re-parameterisation + epigenetics.
The seed carries engine PARAMETERS (derived from legacy gains when unset); early experience
shifts allostatic parameters, scaled by differential susceptibility. Directional only."""

import unittest

from affective_engine.core import (TraitSeed, shared_root_seed, sophropathic_seed,
                                    psychopathic_seed)
from affective_engine.endowment import endowment_of, state_vector_from_endowment
from affective_engine.epigenetics import (susceptibility, apply_early_experience,
                                          environmental_swing, window_factor)
from sophropathy.society import typical_child_seed, fearless_child_seed


class TestEndowmentFromGains(unittest.TestCase):
    def test_legacy_seed_resolves_to_an_endowment(self):
        e = endowment_of(shared_root_seed())
        for key in ("set_points", "weights", "reactivities"):
            self.assertTrue(getattr(e, key))
        # fearless (low THREAT gain) -> low fear reactivity
        self.assertLess(e.reactivities["fear"], 0.5)

    def test_low_affiliation_weights_social_needs_less(self):
        warm = endowment_of(sophropathic_seed())      # CARE ~0.45
        cold = endowment_of(psychopathic_seed())       # CARE 0.20
        self.assertGreater(warm.weights["attachment"], cold.weights["attachment"])

    def test_explicit_fields_override_gains(self):
        seed = TraitSeed("x", gains={"THREAT": 0.9}, access={},
                         reactivities={"fear": 0.1})
        self.assertEqual(endowment_of(seed).reactivities["fear"], 0.1)

    def test_state_vector_seeded_from_endowment(self):
        e = endowment_of(psychopathic_seed())
        sv = state_vector_from_endowment(e)
        self.assertEqual(sv.weights["attachment"], e.weights["attachment"])


class TestDifferentialSusceptibility(unittest.TestCase):
    def test_fearless_more_susceptible_than_typical(self):
        fearless = endowment_of(fearless_child_seed())
        typical = endowment_of(typical_child_seed())
        self.assertGreater(susceptibility(fearless), susceptibility(typical))

    def test_fearless_swings_more_by_environment(self):
        # the fearless child is more malleable in BOTH directions -- the same environmental
        # extremes move its parameters further than the typical child's (Belsky & Pluess).
        fearless = endowment_of(fearless_child_seed())
        typical = endowment_of(typical_child_seed())
        self.assertGreater(environmental_swing(fearless), environmental_swing(typical))


class TestEpigeneticShift(unittest.TestCase):
    def test_early_adversity_shifts_arousal_setpoint_and_persists(self):
        e = endowment_of(typical_child_seed())
        base = e.set_points["arousal"]
        adverse = apply_early_experience(e, early_valence=-0.8, age_years=1.0)
        warm = apply_early_experience(e, early_valence=+0.8, age_years=1.0)
        self.assertLess(adverse.set_points["arousal"], base)   # allostatic load: less tolerance
        self.assertGreater(warm.set_points["arousal"], base)   # secure: more tolerance
        # the shift is on the returned (persistent) endowment; the original is untouched
        self.assertEqual(e.set_points["arousal"], base)

    def test_adversity_lowers_oxytocin_function(self):
        e = endowment_of(typical_child_seed())
        adverse = apply_early_experience(e, early_valence=-0.8, age_years=1.0)
        self.assertLess(adverse.reactivities["oxytocin"], e.reactivities["oxytocin"])

    def test_window_closes_with_age(self):
        e = endowment_of(typical_child_seed())
        self.assertGreater(window_factor(0.5), window_factor(4.0))
        self.assertEqual(window_factor(10.0), 0.0)
        # after the window closes, early experience no longer shifts the endowment
        late = apply_early_experience(e, early_valence=-0.8, age_years=10.0)
        self.assertEqual(late.set_points["arousal"], e.set_points["arousal"])

    def test_typical_internalises_under_adversity(self):
        # the fear-intact typical child's fear reactivity rises under adversity (the anxiety /
        # internalising route), a shift that is present but smaller for the low-fear child.
        typ = endowment_of(typical_child_seed())
        adverse = apply_early_experience(typ, early_valence=-0.8, age_years=1.0)
        self.assertGreater(adverse.reactivities["fear"], typ.reactivities["fear"])


if __name__ == "__main__":
    unittest.main()

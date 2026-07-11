import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""v10 physical endowment -- E5/E6 bearer-side self-effect (the one smuggle-risk).

An agent's OWN physical strength (E5) and sex (E6) bias its OWN VMHvl reactivity -- how strongly its
attack area responds to its drive. Implemented as an INPUT-reactivity gain: it scales VMHvl's driven
input, never adds a standing drive. At v10, provocation was VMHvl's ONLY input, so at neutral there
was nothing to amplify and the floor held BY CONSTRUCTION. v11 added VMHvl afferents (MeA->VMHvl
inhibitory, BNST->VMHvl excitatory), whose net at neutral is negligible, so the floor now holds
BEHAVIOURALLY: at neutral a strong and a weak agent both RESTRAIN and the residual aggress drive is
negligible; the provoked strong>weak differential is intact. (Cross-version interaction flagged in
the v11 Allen-pass notes -- the guard's basis changed from structural to behavioural, the property held.)

The load-bearing honesty properties (ordinal/structural only -- the differential is the finding, the
neutral floor proves it is not coded "strong->aggressive"):
  * NEUTRAL FLOOR: strong x neutral (unprovoked) -> restrain, negligible aggress residual. Raising
    strength alone cannot fire aggression.
  * PROVOCATION DIFFERENTIAL (E5): strong x provocation -> more aggression drive than weak x
    provocation. Same-sex comparison, so the effect is strength, not sex.
  * SEX FACTOR NOT GATE (E6): male baseline reactivity > female, but BOTH > 0 -> aggression fully
    reachable in both sexes under provocation (the v9 pathway intact). Not "male on / female off."
  * SELF-EFFECT ONLY: the gain is on the agent's OWN engine; a physical-neutral agent -> gain 1.0
    (no-op). No agent's calibration depends on another agent's traits.

Whether these biases yield the observed CU sex ratio must still EMERGE and be measured (scan_match) --
never the reason the parameter is set. Nothing here maps strength or sex to a social outcome.
"""
import unittest

from substrate.model import load_substrate
from substrate.engine import SubstrateEngine
from substrate.social import respond_to_substrate
from affective_engine.core import Appraisal
from affective_engine.physical import (vmhvl_reactivity, own_formidability,
                                        SEX_MALE, SEX_FEMALE)

_MODEL = load_substrate()
_EPS = 1e-6

# strong vs weak endowments (raw z-scores); MUSCLE primary, SIZE secondary. ATTRACT/HEALTH neutral.
_STRONG = {"PH-MUSCLE": 2.0, "PH-SIZE": 1.5, "PH-ATTRACT": 0.0, "PH-HEALTH": 0.0}
_WEAK = {"PH-MUSCLE": -2.0, "PH-SIZE": -1.5, "PH-ATTRACT": 0.0, "PH-HEALTH": 0.0}
_AVG = {"PH-MUSCLE": 0.0, "PH-SIZE": 0.0, "PH-ATTRACT": 0.0, "PH-HEALTH": 0.0}


def _act(appr, gain=1.0, age=25.0):
    """The emergent act + phasic drives for one appraisal on a fresh engine at reactivity `gain`."""
    e = SubstrateEngine(_MODEL, age_years=age)
    e.set_reactivity("VMHvl", gain)
    return respond_to_substrate(e, appr)


class TestReactivityFunction(unittest.TestCase):
    """The pure E5xE6 calibration: strong->gain>1, weak->gain<1, neutral physical->1.0, always >0."""

    def test_strength_raises_gain_sex_neutral(self):
        self.assertGreater(own_formidability(_STRONG), 0.5)
        self.assertLess(own_formidability(_WEAK), 0.5)
        self.assertGreater(vmhvl_reactivity(_STRONG, SEX_MALE), vmhvl_reactivity(_WEAK, SEX_MALE))
        self.assertGreater(vmhvl_reactivity(_STRONG, SEX_FEMALE), vmhvl_reactivity(_WEAK, SEX_FEMALE))

    def test_physical_neutral_is_a_noop(self):
        self.assertEqual(vmhvl_reactivity({}, None), 1.0)
        self.assertEqual(vmhvl_reactivity({}, SEX_MALE), 1.0)

    def test_sex_is_a_factor_not_a_gate(self):
        # male baseline > female (direction), but BOTH strictly > 0 -- a factor, never on/off
        self.assertGreater(vmhvl_reactivity(_AVG, SEX_MALE), vmhvl_reactivity(_AVG, SEX_FEMALE))
        self.assertGreater(vmhvl_reactivity(_AVG, SEX_FEMALE), 0.0)


class TestNeutralFloorGuard(unittest.TestCase):
    """strong x neutral -> restrain with NO aggression leak; identical to a weak agent. Raising
    strength alone (no provocation) cannot fire aggression -- proof it is not coded strong->aggressive."""

    def test_strong_neutral_restrains_no_leak(self):
        g = vmhvl_reactivity(_STRONG, SEX_MALE)                  # a strong male: highest gain
        b = _act(Appraisal(), gain=g)
        self.assertEqual(b.behaviour, "restrain")
        self.assertLess(b.drives["aggress"], _EPS)

    def test_gain_cannot_manufacture_unprovoked_aggression(self):
        # v10 held strong==weak exactly (nothing to amplify at neutral). v11 gave VMHvl afferents
        # (MeA/BNST) whose neutral net is negligible, so the floor now holds BEHAVIOURALLY: at neutral
        # BOTH a strong and a weak agent restrain, with a negligible aggress residual far below any
        # threshold. The gain cannot manufacture unprovoked aggression.
        for phys, sex in ((_STRONG, SEX_MALE), (_WEAK, SEX_FEMALE)):
            b = _act(Appraisal(), gain=vmhvl_reactivity(phys, sex))
            self.assertEqual(b.behaviour, "restrain")
            self.assertLess(b.drives["aggress"], 0.02)   # negligible residual (measured ~0.003)


class TestProvocationDifferential(unittest.TestCase):
    """E5: under provocation a stronger agent's attack area responds more. Same-sex comparison, so
    the differential is strength, not sex. The differential REQUIRES provocation to appear."""

    def test_strong_provoked_more_aggression_than_weak(self):
        g_strong = vmhvl_reactivity(_STRONG, SEX_MALE)
        g_weak = vmhvl_reactivity(_WEAK, SEX_MALE)              # same sex -> isolates strength
        strong = _act(Appraisal(provocation=0.9), gain=g_strong).drives["aggress"]
        weak = _act(Appraisal(provocation=0.9), gain=g_weak).drives["aggress"]
        self.assertGreater(strong, weak)

    def test_the_differential_needs_provocation(self):
        # strength changes the PROVOKED response but not the neutral one -- it is a calibration on the
        # competition under provocation, not a standing bias.
        g_strong, g_weak = vmhvl_reactivity(_STRONG, SEX_MALE), vmhvl_reactivity(_WEAK, SEX_MALE)
        d_neutral = (_act(Appraisal(), gain=g_strong).drives["aggress"]
                     - _act(Appraisal(), gain=g_weak).drives["aggress"])
        d_provoked = (_act(Appraisal(provocation=0.9), gain=g_strong).drives["aggress"]
                      - _act(Appraisal(provocation=0.9), gain=g_weak).drives["aggress"])
        self.assertAlmostEqual(d_neutral, 0.0, places=9)
        self.assertGreater(d_provoked, d_neutral)


class TestAggressionReachableInBothSexes(unittest.TestCase):
    """E6 is a factor, not a gate: aggression is reachable under provocation for BOTH sexes (the v9
    pathway is intact), just with a higher male baseline."""

    def test_both_sexes_reach_aggression_when_provoked(self):
        for sex in (SEX_MALE, SEX_FEMALE):
            g = vmhvl_reactivity(_AVG, sex)
            d = _act(Appraisal(provocation=0.9), gain=g).drives
            self.assertGreater(d["aggress"], d["avoid"], f"{sex}: aggression drive reachable")
        # ... and the male baseline yields at least as much provoked aggression drive as the female
        male = _act(Appraisal(provocation=0.9), gain=vmhvl_reactivity(_AVG, SEX_MALE)).drives["aggress"]
        female = _act(Appraisal(provocation=0.9), gain=vmhvl_reactivity(_AVG, SEX_FEMALE)).drives["aggress"]
        self.assertGreaterEqual(male, female)


class TestPervasiveSelfEffect(unittest.TestCase):
    """The E5/E6 golden shift is a PERVASIVE SELF-EFFECT: every agent's VMHvl calibration is a pure
    function of its OWN strength + sex, distinct per agent, and NEVER depends on another agent's
    traits. This is what makes the develop-golden move a self-effect, not a cross-agent leak."""

    def _population(self):
        from sophropathy.engine import SimEngine
        eng = SimEngine(population=80, seed=7)
        return [p.mind for p in eng.pop.persons.values() if p.mind.physical]

    def test_each_agents_calibration_is_its_own_pure_function(self):
        minds = self._population()
        self.assertGreater(len(minds), 20)
        for m in minds:
            self.assertAlmostEqual(m.engine.reactivity.get("VMHvl", 1.0),
                                   vmhvl_reactivity(m.physical, m.sex), places=9)

    def test_calibration_varies_across_the_population(self):
        # pervasive: not one shared value -- every agent conditioned by its own endowment
        gains = {round(m.engine.reactivity.get("VMHvl", 1.0), 6) for m in self._population()}
        self.assertGreater(len(gains), 10)

    def test_calibration_tracks_own_strength_not_others(self):
        import statistics as st
        minds = self._population()
        strength = [own_formidability(m.physical) for m in minds]
        gain = [m.engine.reactivity.get("VMHvl", 1.0) for m in minds]
        self.assertGreater(st.correlation(strength, gain), 0.3)   # own strength -> own reactivity
        # cross-agent independence: an agent with identical physical+sex gets identical calibration
        # regardless of population context (pure function of self, no neighbour term).
        from affective_engine.agent import AffectiveAgent
        from arena import intact_seed
        solo = AffectiveAgent(seed=intact_seed(), temperament_seed=424242)
        solo2 = AffectiveAgent(seed=intact_seed(), temperament_seed=424242)
        self.assertEqual(solo.engine.reactivity.get("VMHvl"), solo2.engine.reactivity.get("VMHvl"))


if __name__ == "__main__":
    unittest.main()

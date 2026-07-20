import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""The developmental-social integration pass -- partner-specific relational learning routed through
the ontogenetic (Arena) timecourse.

Before this pass the Arena wrote a descriptive dead-end _Tie and the developing life never accumulated
a relationship. Now, with ArenaSpec.relational=True:
  * the canonical gm.rel is WRITTEN by the emergent act via the SHARED accrue_relationship mechanism
    (F1 -- the SAME write as GameMaster.adjudicate, not a second implementation);
  * that history RE-ENTERS perception as an IN-CONSPEC RECOGNITION cue (F2) -- familiar_warm -> PVN-OT
    (oxytocin/approach) or familiar_wary -> CeA (defensive), the perceiver's OWN circuits valuing it;
  * so an agent's behaviour and its developing substrate DIVERGE as a function of the relationships it
    accumulated -- emergent, not scripted.

The emergence keystone (Fork-2): the history enters as RECOGNITION on IN-CONSPEC, NEVER as a valuation
written onto the affordance channels (affiliation/threat). relational=False stays the byte-identical
regression harness. Structural/ordinal assertions only."""

import unittest

from arena import (run_arena, ArenaSpec, Slot, intact_seed,
                   _add_relationship_percept, _perceive)
from sim_world.gamemaster import Relationship


def _spec(relational, seed=7):
    slots = [Slot("a", "newborn", seed=intact_seed()),
             Slot("b", "newborn", seed=intact_seed()),
             Slot("c", "newborn", seed=intact_seed())]
    return ArenaSpec("one_room", slots, seed=seed, shared_hours=10.0, relational=relational)


class TestRelOffIsTheRegressionHarness(unittest.TestCase):
    def test_rel_off_is_deterministic(self):
        a = run_arena(_spec(False), childhood_years=8.0)
        b = run_arena(_spec(False), childhood_years=8.0)
        self.assertEqual(a.signature(), b.signature())     # the regression-diff property is preserved
        self.assertTrue(a.viable())


class TestHistoryAccumulatesAndShapesBehaviour(unittest.TestCase):
    def test_directed_relationships_accumulate(self):
        t = run_arena(_spec(True), childhood_years=18.0)
        strains = t.records[-1]["strain"]
        self.assertTrue(strains)                            # ties formed
        # rel is DIRECTED: (a,b) and (b,a) are distinct edges (each agent's own history of the other)
        self.assertIn(("a", "b"), strains)
        self.assertIn(("b", "a"), strains)

    def test_history_shapes_behaviour(self):
        # THE PASS CLAIM at the Arena level: the SAME roster, seed and environment develops a DIFFERENT
        # behavioural distribution when the accumulated relationship re-enters perception -- and the
        # difference traces entirely to the relationship history (nothing else changed). Emergent.
        off = run_arena(_spec(False), childhood_years=18.0)
        on = run_arena(_spec(True), childhood_years=18.0)
        self.assertNotEqual(off.act_counts(), on.act_counts())
        self.assertTrue(on.viable())                        # history shaping does not destabilise the loop

    def test_history_shaping_is_reproducible(self):
        # the divergence is deterministic (seeded), never noise
        a = run_arena(_spec(True), childhood_years=12.0)
        b = run_arena(_spec(True), childhood_years=12.0)
        self.assertEqual(a.signature(), b.signature())


class TestTheEmergenceKeystone(unittest.TestCase):
    def test_familiarity_gates_the_cue(self):
        # a stranger (familiarity 0) presents NO recognition cue -- history only colours a KNOWN other
        p = _perceive("approach")
        before = dict(p)
        _add_relationship_percept(p, Relationship(familiarity=0.0, affect=0.9, trust=0.9))
        self.assertEqual(p, before)

    def test_warm_history_presents_on_the_warm_arm_only(self):
        p = _perceive("approach")
        _add_relationship_percept(p, Relationship(familiarity=1.0, affect=1.0, trust=1.0))
        self.assertIn("familiar_warm", p)
        self.assertNotIn("familiar_wary", p)

    def test_hostile_history_presents_on_the_wary_arm(self):
        p = _perceive("approach")
        _add_relationship_percept(p, Relationship(familiarity=1.0, affect=-1.0, trust=0.0))
        self.assertIn("familiar_wary", p)

    def test_history_is_recognition_never_a_valuation_on_affordance_channels(self):
        # THE FORK-2 KEYSTONE: the cue is written ONLY onto the IN-CONSPEC recognition channels
        # (familiar_warm/wary), NEVER onto the affordance/valuation channels (affiliation/threat).
        # The perceiver's circuits VALUE the recognition; the history is not pre-valued and injected.
        for rel in (Relationship(familiarity=1.0, affect=1.0, trust=1.0),
                    Relationship(familiarity=1.0, affect=-1.0, trust=0.0)):
            p = {}
            _add_relationship_percept(p, rel)
            self.assertNotIn("affiliation", p)
            self.assertNotIn("threat", p)
            self.assertTrue(set(p).issubset({"familiar_warm", "familiar_wary"}))


class TestF4RelationalLifecourse(unittest.TestCase):
    """F4 -- the relational childhood interleaved into run_life's moral-environment life course, so
    the CU study's CLASSIFIED outcome can diverge by relational history. The subject develops under the
    SAME moral environment in both arms; relational=True ADDS co-present relational episodes with a
    developed-alongside cohort. Any classification divergence is attributable to the relationships alone,
    because the moral-env development is byte-identical across arms."""

    def _spec(self):
        from sim_experiment.lifecourse import StageEnv, LifeCourseSpec
        return LifeCourseSpec("t", [StageEnv("home", 0.6, 0.6, 0.6, 32),
                                    StageEnv("school", 0.5, 0.7, 0.5, 32)])

    def test_baseline_life_is_reproducible_and_default_off(self):
        from sim_experiment.lifecourse import run_life
        from affective_engine import shared_root_seed
        S, spec = shared_root_seed(), self._spec()
        a = run_life(S, spec, situation_seed=3102)                       # default relational=False
        b = run_life(S, spec, situation_seed=3102, relational=False)
        self.assertEqual(a.classification, b.classification)

    def test_moral_env_appraisal_stream_is_byte_identical_across_arms(self):
        # THE HONESTY GUARANTEE: the subject's moral-env situation/appraisal stream is IDENTICAL whether
        # relational is off or on -- the relational episodes cannot perturb develop()'s rng. Verify the
        # STREAM (not the weights: weights legitimately diverge -- that IS the phenomenon).
        import affective_engine.development as D
        from affective_engine import AffectiveAgent, shared_root_seed
        from affective_engine.development import develop, Environment
        from sim_experiment.lifecourse import _RelationalChildhood, StageEnv
        S = shared_root_seed()
        orig, rec = D.live_moment, {}
        def cap(agent, appr, age_years):
            rec.setdefault(id(agent), []).append(
                (round(appr.threat, 6), round(appr.reward, 6), round(appr.social_valence, 6),
                 round(appr.provocation, 6), round(appr.other_distress, 6)))
            return orig(agent, appr, age_years=age_years)
        D.live_moment = cap
        try:
            env = Environment("home", 0.6, 0.6, 0.6)
            sa = AffectiveAgent(seed=S, temperament_seed=3102)
            rec.clear(); develop(sa, env, n_episodes=32, situation_seed=3102); stream_off = list(rec[id(sa)])
            sb = AffectiveAgent(seed=S, temperament_seed=3102)
            ch = _RelationalChildhood(3102, 3, 0.6)
            rec.clear()
            develop(sb, env, n_episodes=32, situation_seed=3102,
                    on_episode=ch.stage_hook(StageEnv("home", 0.6, 0.6, 0.6, 32)))
            stream_on = list(rec[id(sb)])
        finally:
            D.live_moment = orig
        self.assertEqual(stream_off, stream_on)                          # moral-env stream identical
        self.assertNotEqual(list(sa.engine.weight), list(sb.engine.weight))  # substrate diverged (the point)

    def test_relationships_accumulate_and_differentiate(self):
        # over a childhood the subject forms DIFFERENTIATED, directed relationships with the cohort --
        # warm/wary emerges from the mutual exchanges, never assigned; a stranger would have none
        from affective_engine import AffectiveAgent, shared_root_seed
        from affective_engine.development import develop, Environment
        from sim_experiment.lifecourse import _RelationalChildhood, StageEnv
        ch = _RelationalChildhood(3102, 3, 0.7)
        subj = AffectiveAgent(seed=shared_root_seed(), temperament_seed=3102)
        develop(subj, Environment("home", 0.6, 0.6, 0.6), n_episodes=48, situation_seed=3102,
                on_episode=ch.stage_hook(StageEnv("home", 0.6, 0.6, 0.6, 48)))
        subj_rels = [v for k, v in ch.rels.items() if k[0] == "subject"]
        self.assertTrue(subj_rels)
        self.assertTrue(all(r.familiarity > 0 for r in subj_rels))       # ties formed
        affects = [round(r.affect, 3) for r in subj_rels]
        self.assertGreater(len(set(affects)), 1)                         # DIFFERENTIATED, not uniform

    # ★ SUSPENDED (S56 ruling) -- the MECHANISM survives; only this LABEL-reordering claim is retracted.
    # F4 originally measured ~50% of seeds diverging (executive -> reward_approach). That was measured on an
    # OVER-DRIVEN, UNGATED cortex. With S56's grounded cortical E-I gate family in place the effect deflates
    # to 0/10 seeds -- the S18 inflation law (every incompleteness inflates effect sizes; the honest direction
    # is smaller), for the third time in one session alongside the divergence sentinel (0.0585 -> 0.0401) and
    # the DA-learning tests (+0.0008 -> -0.0013).
    # WHAT STILL HOLDS (all green, this class's other tests): relationships form and DIFFERENTIATE warm/wary
    # emergently; the act distribution differs by history; the SUBSTRATE still diverges (weights differ); and
    # affiliation moves +0.0088 in the PREDICTED direction (warm childhood -> more affiliation), traceable to
    # the relationship alone (the moral-env appraisal stream is byte-identical across arms).
    # WHY THE LABEL NO LONGER FLIPS: the classification is a bare ARGMAX over a knife-edge profile -- the
    # margin is 0.0021 (social_cognition 0.2263 vs executive 0.2242). A real +0.0088 affiliation shift cannot
    # reorder domains from there. The effect is REAL and visible in the PROFILE; it is invisible only in the
    # discretized LABEL. (Second time the bare argmax has proven the wrong instrument -- it exaggerated the
    # fragile psychopathic flip and now hides a genuine graded effect. Registered.)
    # RESOLUTION CONDITION (TIGHTENED after this test began passing for the wrong reason): re-enable only when
    # the classified outcome diverges AND BOTH lives are confidently classified (margin >= _BLEND_MARGIN). The
    # bare label is not sufficient evidence and never was -- see the margin gate at the end of this test. Do NOT
    # weaken S56 to restore this, and do NOT re-base to a seed that happens to flip -- both would be fitting to a
    # wanted result. NOTE the trap this test walked into: it went GREEN (unexpected success) while the effect was
    # SHRINKING, because the margin collapsed to 0.000158 and the argmax started landing on the other side of a
    # coin flip. A green here without the margin gate would have re-instated a retracted claim on noise.
    @unittest.expectedFailure
    def test_classified_outcome_diverges_by_relational_history(self):
        # THE PASS CLAIM: same seed, same moral environment, run twice -- the relational life reaches a
        # DIFFERENT classified outcome than the environment-only life, and (by the byte-identical stream
        # above) the divergence traces to the relationship history alone. Emergent, not scripted.
        from sim_experiment.lifecourse import run_life
        from affective_engine import shared_root_seed
        S, spec = shared_root_seed(), self._spec()
        base = run_life(S, spec, situation_seed=3102, relational=False)
        rel = run_life(S, spec, situation_seed=3102, relational=True, cohort_size=3, cadence=0.6)
        rel_b = run_life(S, spec, situation_seed=3102, relational=True, cohort_size=3, cadence=0.6)
        self.assertEqual(rel.classification, rel_b.classification)       # deterministic, not noise
        self.assertNotEqual(base.classification, rel.classification)     # relational history diverted it
        # ★ THE MARGIN GATE (added after this test began passing again for the WRONG REASON). A label
        # difference is only a RESULT if the label itself is trustworthy. The classification is a bare
        # argmax, so when the top two domains are a near-tie the label is decided by noise and will
        # "diverge" on a coin flip. That is exactly what happened here: the test started passing not
        # because the relational effect grew, but because the margin COLLAPSED to 0.000158 -- a label
        # difference sitting on ~1/300th of the tie threshold. Without this assertion an unexpected
        # success would read as confirmation and would silently re-instate the claim that was retracted.
        # So: divergence counts only if BOTH lives are confidently classified. Below _BLEND_MARGIN the
        # readout's own docstring says the top two are "effectively a tie".
        from substrate.readout import _BLEND_MARGIN
        self.assertGreaterEqual(base.margin, _BLEND_MARGIN,               # baseline is a real label...
                                f"baseline label is a near-tie (margin {base.margin}) -- not a result")
        self.assertGreaterEqual(rel.margin, _BLEND_MARGIN,                # ...and so is the relational one
                                f"relational label is a near-tie (margin {rel.margin}) -- not a result")


if __name__ == "__main__":
    unittest.main()

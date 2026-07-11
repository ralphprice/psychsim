import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""Part 6 substrate-social phase (3a) -- multi-affordance social behaviour over the substrate.

The substrate produces observable SOCIAL ACTS from the same basal-ganglia accumulation-to-
threshold race as all behaviour: candidate action tendencies grounded in circuit populations
compete, biased by phasic circuit drive, dopamine gain, and the executive hold. NO social-
specific arbiter -- the act EMERGES from which population wins. Tests are ordinal/structural."""

import tokenize
import unittest

from substrate.model import load_substrate
from substrate.engine import SubstrateEngine
from substrate import social as social_module
from substrate.social import (select_social_behaviour, SOCIAL_AFFORDANCES,
                              is_cohesive_act, is_aggressive_act)

_MODEL = load_substrate()


def _act(pattern, age=25.0, ticks=30):
    e = SubstrateEngine(_MODEL, age_years=age)
    e.clear_inputs()
    for k, v in pattern.items():
        e.inject_channel(k, v)
    e.settle(ticks)
    return select_social_behaviour(e)


class TestEmergentSocialActs(unittest.TestCase):
    def test_reward_cue_yields_a_cohesive_approach(self):
        b = _act({"IN-GUST:sweet": 0.8})
        self.assertEqual(b.behaviour, "approach")
        self.assertTrue(is_cohesive_act(b.behaviour))

    def test_separation_yields_comfort_seeking(self):
        b = _act({"IN-INTERO:contact_loss": 0.8})
        self.assertEqual(b.behaviour, "seek_comfort")

    def test_warmth_yields_a_cohesive_act(self):
        b = _act({"IN-SOMATO:affective_touch": 0.8, "IN-INTERO:thermal_warmth": 0.6})
        self.assertTrue(is_cohesive_act(b.behaviour))

    def test_rest_and_neutral_restrain_no_default_act(self):
        # phasic drives: at rest nothing is elevated above baseline, so the agent RESTRAINS --
        # no tonic circuit (e.g. a high-baseline hub) forces a default social act.
        self.assertEqual(_act({}).behaviour, "restrain")
        self.assertEqual(_act({"IN-VIS": 0.3}).behaviour, "restrain")

    def test_multi_affordance_not_degenerate(self):
        # several DISTINCT acts emerge across situations -- a real repertoire, not one winner
        acts = {_act(p).behaviour for p in [
            {"IN-GUST:sweet": 0.8}, {"IN-SOMATO:nociception": 0.9},
            {"IN-INTERO:contact_loss": 0.8}, {}]}
        self.assertGreaterEqual(len(acts), 3)


class TestNoSocialArbiter(unittest.TestCase):
    def test_selection_codes_no_situation_to_act_rule_or_category(self):
        # the act emerges from the BG race; no outcome-category label and no coded social verdict
        with open(social_module.__file__, "rb") as fh:
            names = {t.string.lower() for t in tokenize.tokenize(fh.readline)
                     if t.type == tokenize.NAME}
        for banned in ("callous_exploitation", "strategic_prosociality", "prosocial",
                       "antisocial", "callous", "meanness", "if_threat", "situation_to_act"):
            self.assertNotIn(banned, names)

    def test_affordances_are_circuit_populations(self):
        # each candidate is grounded in real substrate circuits (anatomy), not a rule
        for act, cids in SOCIAL_AFFORDANCES.items():
            present = [c for c in cids if c in _MODEL.circuits]
            self.assertTrue(present, f"{act} grounds in no real circuit: {cids}")


class TestThreatResponseIsEmergent(unittest.TestCase):
    """The substrate is fear-dominant for GENERIC threat, and (v9) aggression is PROVOCATION-
    specific: a purely nociceptive threat drives avoidance and does NOT drive the attack area.
    The v9 pathway routes attack via IN-INTERO:provocation -> VMHvl, not via nociception -> the
    GABAergic CeA (which inhibits the attack effectors). So generic threat -> avoid, aggress ~0;
    aggression appears only under provocation (see test_aggression_pathway). This is the corrected
    OBS-3 property, not a tuned one -- the CeA->PAG/HYPdm inhibition is untouched."""

    def test_generic_threat_drives_avoidance_not_aggression(self):
        e = SubstrateEngine(_MODEL, age_years=25.0)
        e.clear_inputs(); e.inject_channel("IN-SOMATO:nociception", 0.9); e.settle(30)
        b = select_social_behaviour(e)
        self.assertEqual(b.behaviour, "avoid")          # generic threat -> avoidance (fear baseline)
        # NOT driven by generic threat -- provocation-specific (v9). v12a: MeA->VMHvl is now (correctly)
        # excitatory, so the attack area carries a negligible standing prime (~1e-6) from MeA tone --
        # the exact-zero of the old inhibitory sign is gone, but aggression is still not driven (avoid).
        self.assertLess(b.drives["aggress"], 1e-4)


if __name__ == "__main__":
    unittest.main()

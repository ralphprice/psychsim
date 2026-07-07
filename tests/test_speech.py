"""Tests for the two-channel language layer.

The causal claims: acts (not words) drive appraisal; deception is a property of
the act with seeded, reproducible detection; the template renderer passes the
faithfulness gate; and nothing on the rendering side leaks back into the
engine.
"""

import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))


import random
import unittest

from speech.acts import (SpeechAct, SpeechChannel, act_from_network,
                              perceive_act, appraisal_from_act)
from speech.render import TemplateRenderer, LLMRenderer, articulacy_band
from speech.faithfulness import evaluate, passes, probe_line


class TestSpeechActs(unittest.TestCase):

    def test_network_maps_to_act(self):
        a = act_from_network("callous_exploitation", "X", "Y")
        self.assertTrue(a.deceptive)
        self.assertEqual(a.intent, "DECEIVE")
        self.assertEqual(a.surface, "AFFILIATE")
        self.assertFalse(act_from_network("affiliative_warmth", "X", "Y").deceptive)

    def test_unknown_network_speaks_neutrally(self):
        a = act_from_network("some_extension_network", "X", "Y")
        self.assertEqual(a.intent, "ASSERT")

    def test_honest_act_appraised_as_itself(self):
        threat = SpeechAct("A", "B", "THREATEN", intensity=0.9)
        ap = appraisal_from_act(threat, perceived_as="THREATEN")
        self.assertGreater(ap.threat, 0.3)
        self.assertLess(ap.social_valence, 0.0)

    def test_believed_deception_reads_as_its_surface(self):
        lie = SpeechAct("A", "B", "DECEIVE", surface="AFFILIATE", intensity=0.5)
        ap = appraisal_from_act(lie, perceived_as="AFFILIATE")
        self.assertGreater(ap.social_valence, 0.0)  # warmth, not threat

    def test_detected_deception_reads_as_betrayal(self):
        lie = SpeechAct("A", "B", "DECEIVE", surface="AFFILIATE", intensity=0.8)
        ap = appraisal_from_act(lie, perceived_as="DECEIVE")
        self.assertLess(ap.social_valence, 0.0)
        self.assertGreater(ap.provocation, 0.0)

    def test_detection_is_seeded_and_reproducible(self):
        lie = SpeechAct("A", "B", "DECEIVE", surface="AFFILIATE", intensity=0.7)
        r1 = [perceive_act(lie, 0.5, random.Random(3)) for _ in range(1)]
        r2 = [perceive_act(lie, 0.5, random.Random(3)) for _ in range(1)]
        self.assertEqual(r1, r2)

    def test_vigilance_raises_detection_rate(self):
        lie = SpeechAct("A", "B", "DECEIVE", surface="AFFILIATE", intensity=0.5)
        def rate(vig):
            rng = random.Random(11)
            return sum(perceive_act(lie, vig, rng) == "DECEIVE"
                       for _ in range(400)) / 400
        self.assertGreater(rate(0.9), rate(0.1))

    def test_channel_returns_appraisal_to_run_receiver_on(self):
        ch = SpeechChannel()
        act = SpeechAct("A", "B", "COMFORT", intensity=0.6)
        ap = ch.exchange(act, receiver_vigilance=0.5, rng=random.Random(1))
        self.assertGreater(ap.social_valence, 0.0)
        self.assertEqual(len(ch.acts), 1)


class TestRendering(unittest.TestCase):

    def test_template_renderer_passes_faithfulness(self):
        scores = evaluate(TemplateRenderer())
        self.assertTrue(passes(scores),
                        f"template renderer must pass the gate: {scores}")

    def test_rendering_is_seeded(self):
        r = TemplateRenderer()
        act = SpeechAct("A", "B", "PROPOSE", register="adult", articulacy=0.5)
        self.assertEqual(r.render(act, "PROPOSE", random.Random(9)),
                         r.render(act, "PROPOSE", random.Random(9)))

    def test_deception_renders_as_surface_not_intent(self):
        r = TemplateRenderer()
        lie = SpeechAct("A", "B", "DECEIVE", surface="AFFILIATE",
                        register="adult", articulacy=0.5)
        line = r.render(lie, "AFFILIATE", random.Random(2))
        # the words sound affiliative; the probe should NOT recover a threat
        act_guess, _, _ = probe_line(line)
        self.assertNotIn(act_guess, ("THREATEN", "TAUNT"))

    def test_articulacy_band_boundaries(self):
        self.assertEqual(articulacy_band(0.1), "low")
        self.assertEqual(articulacy_band(0.5), "mid")
        self.assertEqual(articulacy_band(0.9), "high")

    def test_llm_renderer_is_a_documented_stub(self):
        with self.assertRaises(NotImplementedError):
            LLMRenderer().render(SpeechAct("A", "B", "ASSERT"),
                                 "ASSERT", random.Random(0))


if __name__ == "__main__":
    unittest.main()

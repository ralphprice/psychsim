"""speech -- the two-channel language layer.

Causal channel: SpeechAct / SpeechChannel (acts.py) -- agents exchange and
appraise structured acts; fully seeded and mechanistic.
Observer channel: Renderer (render.py) -- acts voiced as dialogue for humans;
nothing causal reads it. faithfulness.py is the gate any renderer must pass.
"""
from .acts import (SpeechAct, SpeechChannel, ACT_TYPES, REGISTERS,
                   act_from_behaviour, perceive_act, appraisal_from_act)
from .render import TemplateRenderer, LLMRenderer, articulacy_band
from .faithfulness import evaluate, passes, probe_line

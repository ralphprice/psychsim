# speech — the language layer (core)

**Two channels: structured speech-acts that drive the simulation, and a
renderer that voices them for human observers.** This is the "AI as voice, not
mind" architecture — the deliberate inversion of Park et al. (2023), in which
the language model *is* the cognition. Here the model, when one is fitted at
all, only renders; nothing it produces is ever read back into the engine.

This is a **core** layer: a universal capability, not specific to the
sophropathy research. Any agent simulation that wants legible dialogue without
letting a language model's cultural priors leak into the mechanism can use it.

## The two channels

1. **The causal channel (`acts.py`).** Agents exchange typed, parameterised
   `SpeechAct`s — `AFFILIATE`, `PROPOSE`, `THREATEN`, `DECEIVE`, and so on — and
   each receiver appraises the *act*, never any wording of it. Everything that
   matters causally therefore stays inside the seeded, inspectable engine.
   - **Deception is a property of the act**, not the words: a `SpeechAct` carries
     an `intent` (what it really is) hidden behind a `surface` (what it presents
     itself as). A receiver appraises the surface unless it detects the intent,
     and detection is a *seeded roll* against the receiver's vigilance — an engine
     matter, not a linguistic one.
   - **Articulacy is a rendering knob; capability is an engine parameter.** How
     well an agent pursues its goals lives in the engine; how fluently its acts
     are voiced lives here, and changes nothing causal.

2. **The observer channel (`render.py`).** `TemplateRenderer` is to voice what
   `PlaceholderTileset` is to graphics: a deterministic, dependency-free
   stand-in that voices acts as dialogue for humans. `LLMRenderer` is the
   documented drop-in slot for a fine-tuned small model (LoRA-adapted,
   conditioned on act × register × articulacy). Swapping renderers changes
   nothing causal.

## The acceptance gate (`faithfulness.py`)

A renderer may only be trusted for observer transcripts if, from a rendered line
alone, an independent probe can recover the act, the register band and the
articulacy band. Targets: act ≥ .90, register ≥ .80, articulacy ≥ .80. The
template renderer currently clears the gate at roughly .92 / .91 / .88. Intent
is deliberately *not* recoverable — a deception must sound like its surface.

## Wired into the world

This layer is not a bolt-on. `sim_world`'s Game-Master calls it through
`GameMaster.converse`, so agents in a running world actually talk: the speaker
emits the act its settled behavioural network makes (register from its
life-stage, articulacy a rendering-only knob), the hearer's vigilance — grounded
in its threat gain and its trust in the speaker — sets the seeded detection
probability, and the hearer then appraises the *perceived* act and settles its
own reply. A believed exploit is remembered as warmth; a detected one as
betrayal. The words never touch the causal path.

## Use it

```python
from speech import act_from_network, SpeechChannel, TemplateRenderer
import random

# a callous agent's act: exploitation wearing an affiliative surface
lie = act_from_network("callous_exploitation", "A", "B",
                       intensity=0.7, register="adult",
                       articulacy=0.7, topic="the deal")
rng = random.Random(0)
channel = SpeechChannel()
appraisal = channel.exchange(lie, receiver_vigilance=0.9, rng=rng)  # what B is run on
line = TemplateRenderer().transcript_line(*channel.acts[-1], rng=rng)
print(line)   # voiced as warmth; annotated if the deception was detected
```

In a running world, prefer `GameMaster.converse(actor, target, topic=...)`,
which does all of the above and adjudicates both turns into the world.

## Layout

```
speech/
  acts.py           SpeechAct, the causal channel, deception + perception
  render.py         Renderer protocol; TemplateRenderer (now) + LLMRenderer (slot)
  faithfulness.py   the acceptance gate any renderer must clear
```

See `docs/ARCHITECTURE.md` for how this layer sits in the platform.

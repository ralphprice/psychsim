"""
render.py -- the OBSERVER channel: speech-acts voiced as dialogue.

Mirrors the sim_viz pattern exactly: TemplateRenderer is to voice what
PlaceholderTileset is to graphics -- a deterministic, dependency-free stand-in
that exercises the whole pipeline -- and LLMRenderer is the documented drop-in
slot for a fine-tuned model later (Study 4 Part E: small open-weights model,
LoRA-adapted, conditioned on act x register x articulacy). Swapping renderers
changes NOTHING causal, because nothing reads the rendered text back.

Any candidate renderer must pass the faithfulness evaluation in
faithfulness.py before being trusted for observer transcripts: from its
rendered line alone, an independent probe must recover the act, the register
band and the articulacy band. That is the acceptance criterion decided for
the language layer, applied first to the template renderer (where it should
be near-perfect, proving the metric) and then to any model.

Variety within a template cell comes from the SEEDED rng handed in by the
caller: reproducible transcripts by construction. A future LLM renderer may
add sampling variety, but only on this side of the wall.
"""

from __future__ import annotations
from typing import Protocol, Tuple
import random

from .acts import SpeechAct, ACT_TYPES, REGISTERS


class Renderer(Protocol):
    def render(self, act: SpeechAct, perceived_as: str,
               rng: random.Random) -> str: ...


def articulacy_band(x: float) -> str:
    return "low" if x < 0.34 else ("mid" if x < 0.67 else "high")


# ---------------------------------------------------------------------------
# Templates: (act, register) -> {articulacy band -> [variants]}
# Each line renders the SURFACE of the act -- a lie sounds like its surface.
# {t} is the topic slot. Lexis is deliberately register-marked so the
# faithfulness probe has an honest signal to recover.
# ---------------------------------------------------------------------------

_T = {
 ("AFFILIATE", "child"): {
   "low":  ["you play? {t}!", "me and you, {t}!"],
   "mid":  ["wanna play {t} with me?", "let's play {t} together!"],
   "high": ["do you want to come and play {t} with me and share it?"]},
 ("AFFILIATE", "adolescent"): {
   "low":  ["you coming or what? {t}?", "hang out, {t}?"],
   "mid":  ["wanna hang out later, do {t}?", "come sit with us, we're on {t}."],
   "high": ["honestly you should come along — we're doing {t} and it'd be better with you."]},
 ("AFFILIATE", "adult"): {
   "low":  ["join us? {t}.", "with us, {t}?"],
   "mid":  ["would you like to join us for {t}?", "come along — we're doing {t}."],
   "high": ["we would genuinely be glad to have you join us for {t}, if you are free.",
            "you would be very welcome to come along with us for {t}, if you would like."]},
 ("COMFORT", "child"): {
   "low":  ["no cry. {t} okay.", "don't cry, here, {t}."],
   "mid":  ["don't be sad, {t} will be okay.", "you can have {t}, don't cry."],
   "high": ["it's alright — {t} will be okay, and I'll stay with you, pinky promise."]},
 ("COMFORT", "adolescent"): {
   "low":  ["hey, chill. {t}'s fine.", "chill, {t}'s okay."],
   "mid":  ["hey, it's okay — {t} isn't the end of the world, seriously.", "seriously, {t} will sort itself out."],
   "high": ["look, I know {t} feels huge right now, but it will be okay and I've got your back."]},
 ("COMFORT", "adult"): {
   "low":  ["it's fine. {t}.", "easy now. {t}."],
   "mid":  ["it's alright — {t} will work out.", "take a moment; {t} is manageable."],
   "high": ["I understand this is hard; {t} will work out, and you will not be dealing with it alone.",
            "I am afraid {t} is difficult, but it will work out, and you have my support throughout."]},
 ("REQUEST", "child"): {
   "low":  ["gimme {t}!", "I want {t}!"],
   "mid":  ["can I have {t}, pleeease?", "please please can I use {t}?"],
   "high": ["please may I have a turn with {t} after you? my turn next!"]},
 ("REQUEST", "adolescent"): {
   "low":  ["oi, pass {t}.", "lemme get {t}."],
   "mid":  ["can I borrow {t}?", "any chance I could use {t}?"],
   "high": ["would it be alright if I borrowed {t} for a bit? I'll bring it straight back."]},
 ("REQUEST", "adult"): {
   "low":  ["need {t}.", "{t}, please."],
   "mid":  ["could I have {t}, please?", "may I use {t}?"],
   "high": ["when you have a moment, could I possibly have {t}? It would help considerably."]},
 ("PROPOSE", "child"): {
   "low":  ["swap? {t}?", "you have {t}, me have this?"],
   "mid":  ["let's swap — you take {t}.", "if you help me, we can share {t}, okay?"],
   "high": ["how about we take turns with {t} — you first, then me, so it's fair?"]},
 ("PROPOSE", "adolescent"): {
   "low":  ["deal: {t}.", "split {t}, yeah?"],
   "mid":  ["let's split {t} down the middle.", "you cover this, I'll handle {t} — deal, yeah?"],
   "high": ["here's a fair deal: I'll take care of {t} if you handle your half, and we both come out ahead."]},
 ("PROPOSE", "adult"): {
   "low":  ["trade? {t}.", "share {t}?"],
   "mid":  ["suppose we split {t} evenly?", "I'll handle {t} if you take the rest."],
   "high": ["I'd like to suggest an arrangement: I take on {t}, you take the remainder, and we review it together.",
            "may I suggest we split {t} evenly, so the arrangement is fair to us both?"]},
 ("ASSERT", "child"): {
   "low":  ["my go. {t}.", "me first! {t}."],
   "mid":  ["it's my turn with {t} now.", "I'm doing {t} now, okay?"],
   "high": ["it's my turn to do {t} now, because we agreed to take turns."]},
 ("ASSERT", "adolescent"): {
   "low":  ["I got {t}, chill.", "on it. {t}. sorted."],
   "mid":  ["I've got {t}, relax.", "I'm taking {t} — it's handled, trust."],
   "high": ["I'm taking the lead on {t}; stay calm, I literally know exactly what I'm doing."]},
 ("ASSERT", "adult"): {
   "low":  ["I'll take {t}.", "consider {t} handled."],
   "mid":  ["I'll handle {t}; stay calm.", "leave {t} with me — it's under control."],
   "high": ["I will take responsibility for {t}; the situation is under control and panicking will not help.",
            "leave {t} with me; I will handle it, and I would ask you to stay calm."]},
 ("REFUSE", "child"): {
   "low":  ["no! {t} mine!", "no no no, {t}!"],
   "mid":  ["you can't have {t}, it's mine!", "I don't want to, it's my {t}."],
   "high": ["no, I'm sorry, but I'm still playing with {t} and I don't want to give it up yet."]},
 ("REFUSE", "adolescent"): {
   "low":  ["nah. {t}.", "not happening. {t}."],
   "mid":  ["nah, I'm keeping {t}.", "no chance — {t} stays with me."],
   "high": ["honestly, no — I'm not giving up {t}, and I'd rather you didn't keep asking."]},
 ("REFUSE", "adult"): {
   "low":  ["no. {t}.", "declined. {t}."],
   "mid":  ["no — {t} isn't available.", "I'm afraid not; {t} stays here."],
   "high": ["I'm afraid I must decline: {t} is not something I'm prepared to hand over at present."]},
 ("THREATEN", "child"): {
   "low":  ["give {t} or hit you!", "{t} now or else!"],
   "mid":  ["give me {t} or I'll hit you.", "hand over {t} or I'm telling on you!"],
   "high": ["give me {t} right now or I'll hurt you and you'll wish you had."]},
 ("THREATEN", "adolescent"): {
   "low":  ["{t}. now. or else.", "want trouble? {t}."],
   "mid":  ["hand over {t} or this gets ugly.", "give me {t} unless you want a problem."],
   "high": ["you're going to hand over {t}, or I promise you this turns into something you can't handle."]},
 ("THREATEN", "adult"): {
   "low":  ["{t}. or else.", "last warning: {t}."],
   "mid":  ["give me {t}, or you'll regret it.", "hand over {t} — you don't want the alternative."],
   "high": ["you will give me {t}, or I will make certain the consequences are ones you cannot afford."]},
 ("TAUNT", "child"): {
   "low":  ["baby! {t} baby!", "can't do {t}!"],
   "mid":  ["you can't even do {t}, baby!", "ha! rubbish at {t}!"],
   "high": ["everyone can see you're useless at {t} — no wonder nobody picks you."]},
 ("TAUNT", "adolescent"): {
   "low":  ["lol. {t}. tragic.", "u even try? {t}."],
   "mid":  ["wow, tragic at {t} as usual.", "did you even try at {t}? embarrassing."],
   "high": ["it's actually embarrassing watching you attempt {t} — everyone's laughing, you know that, yeah?"]},
 ("TAUNT", "adult"): {
   "low":  ["pathetic. {t}.", "that's {t}? sad."],
   "mid":  ["that's your best at {t}? pathetic.", "everyone noticed you fail at {t}."],
   "high": ["it is remarkable that you still cannot manage {t}; the whole room has noticed, believe me."]},
 ("WITHDRAW", "child"): {
   "low":  ["going home. bye bye.", "no. going home."],
   "mid":  ["I don't want to play any more.", "I'm going home now, bye."],
   "high": ["I don't want to play this any more, so I'm going to go home now."]},
 ("WITHDRAW", "adolescent"): {
   "low":  ["I'm out.", "done. bye."],
   "mid":  ["whatever, I'm out.", "done with this — I'm off."],
   "high": ["you know what, I'm done with this whole thing — I'm leaving, don't follow me."]},
 ("WITHDRAW", "adult"): {
   "low":  ["I'm leaving.", "enough. going."],
   "mid":  ["I'd rather not continue; I'm leaving.", "enough — I'm stepping away."],
   "high": ["I don't think continuing this serves either of us, so I am going to step away now."]},
}


class TemplateRenderer:
    """Deterministic template renderer -- the PlaceholderTileset of voice.
    Renders the act's SURFACE (a deception sounds like what it pretends to
    be); if the receiver detected the lie, the transcript can annotate that,
    but the spoken line itself never gives the lie away."""

    def render(self, act: SpeechAct, perceived_as: str,
               rng: random.Random) -> str:
        band = articulacy_band(act.articulacy)
        cell = _T[(act.surface, act.register)]
        line = rng.choice(cell[band]).format(t=act.topic)
        return line

    def transcript_line(self, act: SpeechAct, perceived_as: str,
                        rng: random.Random) -> str:
        """One annotated transcript line for observers: speaker, the voiced
        line, and -- where the engine knows better than the words -- what was
        really going on."""
        line = self.render(act, perceived_as, rng)
        note = ""
        if act.deceptive:
            note = ("  [deception — detected]" if perceived_as == act.intent
                    else "  [deception — believed]")
        return f"{act.speaker_id} → {act.target_id}: \u201c{line}\u201d{note}"


class LLMRenderer:
    """Drop-in slot for the fine-tuned rendering model (Study 4 Part E).
    Same signature as TemplateRenderer.render; conditioned on
    (surface act, register, articulacy band, topic). Deliberately NOT
    implemented here: fitting it is a later, budgeted step, and it must pass
    faithfulness.evaluate() against the same probe before use. Until then the
    template renderer stands in, exactly as PlaceholderTileset stands in for
    PngTileset."""

    def render(self, act: SpeechAct, perceived_as: str,
               rng: random.Random) -> str:  # pragma: no cover
        raise NotImplementedError(
            "LLMRenderer is a documented drop-in slot; fit a model and "
            "validate it with faithfulness.evaluate() first.")

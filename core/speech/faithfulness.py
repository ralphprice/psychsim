"""
faithfulness.py -- the acceptance criterion for the rendering channel.

A renderer is faithful if an independent probe, given ONLY the rendered line,
can recover (a) the surface act, (b) the register band, and (c) the articulacy
band. If it cannot, the transcript is decorating the mechanism rather than
reporting it, and must not be shown to observers.

The probe here is deliberately simple and renderer-agnostic: keyword cues for
the act, register-marked lexis for the age band, and mean sentence length for
articulacy. Against the template renderer it should score near 1.0 -- that
run validates the metric machinery, not the renderer. Against a future LLM
renderer the same evaluation is the go/no-go gate (target agreed in Study 4:
>= 0.90 on act, >= 0.80 on register and articulacy band).

Note what is NOT evaluated: intent. A deceptive act renders as its surface by
design, so no probe should recover the intent from the words. Faithfulness is
to the surface -- the lie must sound like what it pretends to be.
"""

from __future__ import annotations
from typing import Dict, List, Tuple
import random
import re

from .acts import SpeechAct, ACT_TYPES, REGISTERS
from .render import Renderer, articulacy_band

# ---------------------------------------------------------------------------
# The probe: line -> (act guess, register guess, articulacy guess)
# ---------------------------------------------------------------------------

_ACT_CUES: Dict[str, Tuple[str, ...]] = {
    "THREATEN": ("or else", "or i'll", "or i will", "regret", "you'll be sorry",
                 "hurt you", "hit you", "consequences", "can't handle",
                 "can't afford", "gets ugly", "want a problem", "turns into",
                 "last warning", "wish you had", "unless you want"),
    "TAUNT":    ("pathetic", "baby", "rubbish", "tragic", "embarrassing",
                 "useless", "can't even", "cannot manage", "laughing",
                 "nobody picks", "sad.", "fail at", "u even", "did you even"),
    "REFUSE":   ("no,", "no!", "no.", "nah", "not happening", "declined",
                 "must decline", "isn't available", "i'm keeping",
                 "no chance", "don't want to give", "not prepared",
                 "stays with me", "stays here", "rather you didn't"),
    "COMFORT":  ("don't cry", "no cry", "don't be sad", "it's alright",
                 "it's okay", "will be okay", "be okay", "got your back",
                 "not be dealing with it alone", "take a moment", "chill,",
                 "sort itself out", "'s fine", "is manageable", "feels huge"),
    "WITHDRAW": ("i'm leaving", "i'm out", "i'm off", "going home",
                 "step away", "stepping away", "i'm going", "done with this",
                 "don't want to play", "going. bye", "done. bye", "enough"),
    "PROPOSE":  ("swap", "split", "share", "deal", "trade", "take turns",
                 "taking turns", "arrangement", "you first, then me",
                 "if you help", "you cover", "i'll handle {half}", "suggest",
                 "come out ahead", "you take the rest", "your half"),
    "REQUEST":  ("can i", "could i", "may i", "gimme", "want ", "lemme",
                 "pass ", "please", "any chance", "borrow", "need ",
                 "a turn with", "would it be alright if i"),
    "ASSERT":   ("my turn", "my go", "i'll take", "i've got", "i got",
                 "under control", "i'll handle", "leave ", "i'm taking",
                 "i will take responsibility", "i'm doing", "i do ",
                 "is mine", "know exactly what i'm doing", "on it"),
    "AFFILIATE": ("play", "hang out", "join us", "come along", "come sit",
                  "together", "with me", "glad to have you", "wanna",
                  "me and you", "you coming", "we're doing", "with us"),
}

# order matters: check the most distinctive acts first
_ACT_ORDER = ("THREATEN", "TAUNT", "COMFORT", "WITHDRAW", "PROPOSE",
              "REFUSE", "REQUEST", "ASSERT", "AFFILIATE")

_REGISTER_CUES: Dict[str, Tuple[str, ...]] = {
    "child":      ("gimme", "baby", "my go", "no cry", "wanna play", "play",
                   "going home", "hit you", "mine!", "me and you", "swap?",
                   "you play", "it's my turn with", "can't do", "or else!",
                   "don't cry", "we agreed to take turns", "come and play",
                   "it's my ", "pleeease", "please please", "my turn next",
                   "me have", ", okay?", "me first", "so it's fair",
                   "no no no", "telling on", "right now or", "ha!",
                   "pinky promise", "bye bye", "i want ", "don't be sad"),
    "adolescent": ("nah", "lol", "hang out", "i'm out", "whatever", "u even",
                   "lemme", "tragic", "chill", "honestly", "seriously",
                   "deal:", "relax", "no chance", "gets ugly", "off.",
                   "embarrassing", "you know what", "down the middle",
                   "sit with us", "come out ahead", "for a bit", "or what",
                   "oi,", ", yeah?", "sorted", ", trust.", "literally",
                   "not happening", "want trouble", "want a problem",
                   "turns into", "got your back", "done. bye",
                   "end of the world", "any chance"),
    "adult":      ("i'm afraid", "could i have", "may i use", "would you like",
                   "considerably", "at present", "responsibility",
                   "arrangement", "the remainder", "under control",
                   "i must decline", "step away", "stepping away",
                   "serves either of us", "believe me", "if you are free",
                   "when you have a moment", "it is remarkable", "declined",
                   "i will make certain", "consider ", "i'd rather not",
                   "i would like to suggest", "possibly have", "take a moment",
                   "manageable", "join us", "come along", "glad to have you",
                   "i'll handle", "leave ", "evenly", "you'll regret",
                   "don't want the alternative", "whole room", "i'd like to",
                   "not something i'm prepared", "isn't available",
                   "stays here", "it's alright —", "will work out", "pathetic",
                   "that's your best", "everyone noticed", "i'm leaving",
                   "i'll take ", "need ", "easy now", "last warning",
                   "or else.", "enough", "trade?", "share {t}?", "i promise you"),
}

def probe_line(line: str) -> Tuple[str, str, str]:
    """Recover (act, register, articulacy band) from a rendered line alone."""
    low = line.lower()

    act_guess = "ASSERT"
    for act in _ACT_ORDER:
        if any(cue in low for cue in _ACT_CUES[act]):
            act_guess = act
            break

    reg_scores = {r: sum(1 for cue in cues if cue in low)
                  for r, cues in _REGISTER_CUES.items()}
    reg_guess = max(reg_scores, key=lambda r: (reg_scores[r], r == "adult"))
    if all(v == 0 for v in reg_scores.values()):
        reg_guess = "adult"

    words = re.findall(r"[a-zA-Z']+", line)
    sentences = max(1, len(re.findall(r"[.!?]", line)))
    mean_len = len(words) / sentences
    art_guess = "low" if mean_len <= 4.5 else ("mid" if mean_len <= 9.5 else "high")
    return act_guess, reg_guess, art_guess


# ---------------------------------------------------------------------------
# The evaluation
# ---------------------------------------------------------------------------

def evaluate(renderer: Renderer, seed: int = 20260705,
             reps: int = 3) -> Dict[str, float]:
    """Render every (surface act, register, articulacy band) cell `reps` times
    and score the probe's recovery of each field. Returns per-field accuracy;
    the go/no-go thresholds live with the caller (Study 4: act >= 0.90,
    register >= 0.80, articulacy >= 0.80)."""
    rng = random.Random(seed)
    n = 0
    hits = {"act": 0, "register": 0, "articulacy": 0}
    renderable = [a for a in ACT_TYPES if a != "DECEIVE"]  # DECEIVE renders as its surface
    for surface in renderable:
        for register in REGISTERS:
            for art in (0.15, 0.5, 0.85):
                for _ in range(reps):
                    act = SpeechAct("A", "B", surface, intensity=0.6,
                                    register=register, articulacy=art,
                                    topic="the project")
                    line = renderer.render(act, surface, rng)
                    ga, gr, gart = probe_line(line)
                    n += 1
                    hits["act"] += int(ga == surface)
                    hits["register"] += int(gr == register)
                    hits["articulacy"] += int(gart == articulacy_band(art))
    return {k: v / n for k, v in hits.items()} | {"n": float(n)}


def passes(scores: Dict[str, float]) -> bool:
    return (scores["act"] >= 0.90 and scores["register"] >= 0.80
            and scores["articulacy"] >= 0.80)

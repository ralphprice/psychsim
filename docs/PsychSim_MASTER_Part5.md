# PsychSim — Master Design & Build Document, Part 5 (Supplements & Addenda, continued)

*Sealed, versioned supplement to `PsychSim_MASTER.md` and Parts 1–4. Not updatable once distributed;
further guidance becomes a new Part. Section numbering continues the global sequence (this Part =
S9–S10).*

**This Part corrects a design-session error.** During the pre-8b.4 review the design session verbally
proposed "fixing the developmental-dynamics stability" of a non-settling developed state using the
R4/R8 machinery. **That framing was wrong and is withdrawn here.** It is tuning-to-outcome in
disguise — reaching into the mechanism to make a developed state settle is deciding what the outcome
*should* be (a stable trait) and adjusting until it complies. The honest position, and the additions
the review surfaced, are below.

---

## S9. Correction — a non-settling developed state is an OUTPUT, not a defect (and the two regimes)

### S9.1 The withdrawal

The substrate is wired from first principles, with parameters set once by the researcher as the given
biology (S10.1). If, under some throttle setting, it produces an **oscillating / non-viable developed
state**, that is a **legitimate model output** — the model saying "this lesion breaks the organism."
It is **reported, never patched.** No stabiliser, no damping term, no "settling" mechanism is added.
The only things that change weighted strengths in a life are the matrices (S10.2), through the
substrate's own plasticity — nothing else has write access to the developed state, least of all a
correction applied to make a result appear.

### S9.2 The finding, stated honestly

An interaction measure that flips sign with development duration is not a real interaction — that
observation stands. But the honest conclusion is **not** "fix the dynamics." It is: **under that
configuration the developed state does not settle, so differential susceptibility is not a well-defined
outcome there, so the divergence does not robustly emerge — and that is the finding for that
configuration.** Where the biology-as-specified settles on its own, the divergence question is
well-posed and the 2×2 reads honestly. Where it does not settle, "no stable outcome here" is itself
informative about that lever. The instability is not in the way of the answer; it *is* an answer.

### S9.3 The two regimes (the distinction the review missed)

Oscillation means different things depending on how it arose, and the two must be told apart:

- **Regime A — module manipulation (crude throttling).** A non-viable / oscillating developed state is
  a **legitimate output**. Crude throttling is brain surgery with a hammer; most of the throttle space
  *should* produce disordered or non-viable outcomes (S9.4). Reported, not fixed.
- **Regime B — the sim world running normally** (slow change through the matrices over a life, no
  throttle). Instability here would be a **severe problem**: ordinary social/environmental interaction
  must **not** drive a viable person into oscillation. This is a real **correctness property** of the
  substrate.

**Action for the session:**
1. **Determine which regime produced the `intact_warm` oscillation.** If it arose under a *throttle*,
   it is data about that lever. If it arose under *normal, un-throttled developmental interaction*,
   that is the severe case — an intact child should not destabilise from a warm upbringing alone — and
   it is surfaced as a real defect of the wired dynamics (still not patched; reported).
2. **Add a stability-property test for Regime B:** normal (un-throttled) interaction over a life
   preserves a viable, settled person. Write this test regardless of the divergence result — it is a
   first-principles correctness property the substrate must satisfy. The test *checks* the property; if
   the substrate fails it, that failure is a real finding about the dynamics, not something to correct
   into compliance.

### S9.4 The scan's expected background — "broken" is the norm, not a failure

Crude throttling breaks the agent almost everywhere. So the coarse 0/100 screen (Part 4 S8.4) mostly
maps the **cliff edges** — the regions where the agent becomes non-viable — **not** the CU profile
directly. The interesting phenotype structure may live in **narrow bands** (the difference between a
99.1% and a 99.2% throttle) that a binary screen steps straight over; the resolution is unknown yet.
Therefore **most scan hits will be "broken," and that is the expected background, not a failure.** The
scan should be read as mapping **viable vs non-viable regions first**, phenotype second, with the real
phenotype search done at fine resolution inside whatever viable bands survive.

---

## S10. Two architecture additions (first-principles, build now)

These are components the organism should have on first-principles grounds and currently lacks. They are
added because they are **correct and missing** — not to make any result appear. Whatever the completed
model then does with the divergence is read honestly, including an earned negative.

### S10.1 The age/experience-decreasing plasticity schedule

Weighted strengths are **default at birth, highly plastic in early childhood, and progressively rigid
with accumulated experience and age** — the researcher's specified shape: the **2nd** experience of a
kind carries ~**50%** weight, and by ~**1000** lifetime events the marginal impact is ~**0.1% or
less**. That curve is exactly an **incremental running-average** learning rate (α_n ≈ 1/n: 2nd event =
1/2, 1000th ≈ 1/1000), so the developed state is a running integration of experience that **naturally
rigidifies** — no separate "rigidify" mechanism required.

- **Make it explicit:** a developmental plasticity schedule the researcher **sets as scaffold**, not
  left implicit — the matrix-driven weight update's learning rate decays with accumulated relevant
  experience (~1/n form), optionally with an age term via **R6-DEVGATE** (age enters only as a rate)
  and an adult **floor** if the researcher wants nonzero lifelong plasticity (the "or even less" leaves
  that open — researcher's call).
- **Honesty:** this is a plasticity *rate* (how fast weights change), never an outcome. It composes
  with the substrate's meaning-blind rules; it does not know what any weight means.

### S10.2 The fourth matrix — self-reflection

Add **now**, while the matrix architecture is fresh (retrofitting a fourth interaction pathway later is
far messier). It is **"a social matrix with oneself on both sides"** — *not a new kind of mechanism*,
but the existing social-interaction machinery with the self as **both agent and target**.

- **Function:** self-appraisal, rumination, internalised self-talk — the agent updates its own weighted
  strengths by reflecting on itself, not only through others. Same engine as `relations.py` /
  `environment_matrix.py` / `group_matrix.py`; the "partner" is the self.
- **Why now, and why it matters for the study:** self-reflection is plausibly part of what separates
  the sophropath from the psychopath — an agent that reflects on its own conduct and updates from it
  versus one that does not. Having the channel **present** (whether or not it is throttled) means it is
  **available to emerge** rather than absent by omission. It is one more lever the throttle panel can
  act on, and one more mechanism the divergence can (or cannot) arise through.
- **Honesty caution:** self-reflection must **not** become a back-door arbiter — a coded "conscience"
  that hands over a moral outcome. It is the self-as-social-partner mechanism, meaning-blind like the
  other three; whether reflection leads to prosocial updating or not must **emerge** from the
  substrate, never be coded. The check is the same grep test: no line maps "reflected on bad conduct"
  to "becomes prosocial."

### S10.3 Sequencing

These are first-principles additions to the organism, not tuning. Add the plasticity schedule and the
self-reflection matrix; determine the regime of the `intact_warm` oscillation and add the Regime-B
stability test (S9.3); **report the throttle sweep honestly** (viable vs non-viable regions; the
divergence where the state settles on its own). Then re-examine the divergence with the completed
architecture. If it robustly emerges, report it; if it does not, that is now the **earned** negative,
because the outcome is well-defined and the organism is complete. Legacy stays untouched; **no 8b.4
until this concludes.**

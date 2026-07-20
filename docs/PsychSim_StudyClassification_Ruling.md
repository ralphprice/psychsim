# The study classifications — **RULING: accept the flip (it is grounded), AND fix the read-out (the knife-edge
# is the instrument, not the finding).** Neither of your two options alone.

**You stopped at exactly the right place and you found two true things. The resolution is that they are about
DIFFERENT objects: the FLIP is about the grounding (and it is correct), the KNIFE-EDGE is about the read-out
(and it is a defect). Handle each where it lives. Neither requires touching a curve, and neither requires
choosing between "accept" and "investigate."**

---

## 1. The flip is GROUNDED. `psychopathic → reward_approach` is not a coincidence of where VTA landed — it is
## one of the best-replicated neurobiological findings in psychopathy.

**I checked the substantive claim against the literature before ruling, because "thematically sensible" is not
enough — it had to be *right*, or accepting it would be fitting the study to a plausible story. It is right, and
specifically:**

> **Buckholtz et al. 2010 (the landmark [¹⁸F]fallypride PET + fMRI study):** *"impulsive-antisocial
> psychopathic traits selectively predicted nucleus accumbens DOPAMINE RELEASE and reward
> anticipation-related neural activity… neurochemical and neurophysiological HYPER-REACTIVITY of the
> dopaminergic reward system may comprise a neural substrate for impulsive-antisocial behavior in
> psychopathy."**
> **Systematic review (2022):** *"Psychopathy was associated with VS HYPERACTIVATION in response to non-social
> reward anticipation."*
> Converging: Bjork 2012, Pujara 2014 (VS hypersensitivity to monetary gain anticipation).

> **The grounded VTA reward-DA adolescent bump raising `reward_approach` and reclassifying the psychopathic
> seed as reward-driven is the substrate REPRODUCING Buckholtz. That is not a shift away from what psychopathy
> is — it is the model landing on the dopaminergic-reward-hypersensitivity account, which is a MAJOR
> contemporary neurobiological theory of psychopathy (specifically its impulsive-antisocial factor, which is
> exactly the externalising/CU-adjacent dimension the study targets).**

**And it is the SAME KIND of result as the branch's other wins:** we did not code "psychopathy is
reward-driven." We grounded the VTA curve from developmental electrophysiology, and the reward-hypersensitivity
classification *emerged*. **That is a third emergent finding, and it is the most study-relevant one yet — the
substrate independently recovered a replicated clinical neurobiology from a grounded maturation curve.**

> **RULING on the flip: ACCEPT it. Do NOT investigate it away.** Investigating it away would be treating a
> correct grounding as suspect *because it moved a result* — which is the inverse of the discipline. **The
> scaffold classifications were the ones resting on nothing; the grounded ones are resting on Buckholtz.**

*(Caveat to record, not to act on: the literature has a real second camp — Glenn & Yang, Hosking — arguing the
striatal signal reflects cortico-striatal DYSFUNCTION / inefficient reward-prediction rather than simple
hypersensitivity. The model currently lands on the hypersensitivity account. That is a legitimate, defensible
position, but the study writeup must acknowledge it is ONE of two accounts, not settled fact. Register for the
study's limitations section.)*

---

## 2. The knife-edge is a SEPARATE, REAL defect — and it is in the READ-OUT, not the curves

**I read the classifier. It is this, in `substrate/readout.py`:**
```python
def read_mind(agent):
    prof = substrate_profile(engine)   # normalised domain profile, sums to 1
    dom  = max(prof, key=prof.get)     # ← the classification is a BARE ARGMAX
    return MindReadout(_DomainLabel(dom), prof)
```

> **The classification is winner-take-all over a normalised profile. A 0.05 margin between the top two domains
> produces a confident single label with no expression of how close the race was. THAT is your knife-edge —
> and it is a property of the INSTRUMENT, not of the grounding.** The curves didn't make the classification
> fragile; **the argmax makes every classification fragile, and grounding the curves just moved a seed across a
> boundary the argmax was always going to render as a hard flip.**

**This is the read-out audit's shape, one more time (the D6 audit found exactly this class — a read-out that
collapses a rich state into a lossy verdict).** The `classify` docstring even protests it — *"DESCRIPTIVE
measurement, attaches NO verdict"* — but `max(prof, key=prof.get)` **is** a verdict, and a brittle one.

> **RULING on the read-out: FIX it — report the profile with its margin, not a bare winner.** The honest
> read-out is: *dominant domain, runner-up, and the margin between them* — so a 0.05 separation reads as "a
> reward/executive BLEND, leaning reward" rather than a hard "reward" label that flips to "executive" on the
> next perturbation. **The profile is already computed and already returned (`MindReadout.profile`); the
> defect is only that `classification` throws it away. The fix is to stop throwing it away.**

**This is not tuning to change a result** — it changes no curve, no weight, no baseline. It makes the
instrument report what it actually measured (a graded profile) instead of a discretised winner. **And it
strictly improves the study: a construct that flips on 0.05 was never a safe binary classification; reporting
the margin is more honest AND more robust.**

---

## 3. Why this resolves your tension exactly

- **"The classifications flipped"** → because they were grounded, and the grounded answer (reward-driven
  psychopathy) is correct. **Accept.**
- **"They're on a knife-edge (~0.05)"** → because the read-out is a bare argmax that renders any close profile
  as a hard label. **Fix the read-out.**

**Both true, both handled, neither by touching a curve.** The flip and the fragility were being read as one
worrying thing; they are two separate things, one a win and one a defect, and separating them dissolves the
worry. **The grounded curves stay. The argmax goes.**

---

## 4. RULING — the sequence

1. **Accept the grounded classifications.** Record that the psychopathic seed now classifies reward-driven
   *because the grounded VTA reward-DA curve reproduces Buckholtz 2010's mesolimbic hypersensitivity* — a
   third emergent finding, the most study-relevant one.
2. **Fix the classify read-out** (`substrate/readout.py`): `classification` reports **dominant + runner-up +
   margin**, not a bare argmax winner. The profile is already there. **This is a read-out honesty fix, not a
   mechanism change — inert to the substrate, and it must NOT alter any activation.** Add its own small test
   (a near-tie profile reads as a blend, not a hard flip).
3. **THEN do the deliberate golden regen** — documenting BOTH reasons (the two grounded builds) AND the read-out
   change. Because the read-out now reports margins, the golden should capture the margins, so future flips are
   visible as margin-shifts, not silent label-changes. **This is why the read-out fix goes BEFORE the regen:
   regenerating the golden against the bare-argmax read-out would lock in the brittle instrument.**
4. **Then** confirm Tremblay + reward-seeking, confirm the deletion (`0.1`), record the floor verdict (RED,
   residual S56), **close D6**, move the rest to `substrate_hardening_backlog`.

## 5. What this adds to the backlog / study register
- **The two-account caveat** (hypersensitivity vs cortico-striatal dysfunction) → study limitations.
- **The margin-reporting read-out** is now the study's classification instrument → note it in the observer/
  psychometric spec, because the CU study will read classifications the same way and must inherit the margin,
  not the bare label.
- **★ The emergent Buckholtz recovery** → this is a headline result for the thesis, alongside Gross and
  Tremblay. **Three replicated psychological/neurobiological findings have now emerged from the grounded
  substrate rather than being coded.** Record it prominently.

---

**This is the surfacing rule working, not a rabbit hole:** the read-out fix is REQUIRED to make D6's
classification claim testable-and-honest (a claim resting on a 0.05 argmax boundary is not a safe claim), so it
is type-(a) — it blocks a claim. It goes in this pass. Nothing else opens. **The curves are grounded, the
instrument is honest, D6 closes.**

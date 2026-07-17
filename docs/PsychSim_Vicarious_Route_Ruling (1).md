# Vicarious Route — RULING — Claude Code

**Excellent diagnostic. The §4 flag is the most important thing in it and you were right to raise it above
the build decisions. Rulings below. One of them is "neither of your options," and one is a new flag that
bears on your own accumulation caveat.**

---

## §4 — CONFIRMED, and I set the trap. This is the headline.

Verified on the remote:
- `study.py:23` — `AFFECTIVE_EMPATHY = ("LA", "BA", "CeA", "MeA", "aIns")`
- LC afferents = `['CeA', 'LC']`

**CeA is in the throttle set and is the sole afferent of LC.** The manipulation contains the mechanism. "Low
affective empathy impairs vicarious aversive learning" is **true by construction**. Your reading is exactly
right, including the nuance: the overlap is *anatomically honest* (CeA genuinely belongs to both the
affective-empathy network and the CeA-CRF→LC projection), so the **structural claim is real and worth
stating** — *the affective-empathy network and the aversive-teaching pathway share CeA, so hypofunction of the
former necessarily impairs the latter* — but it is a statement about **shared anatomy, not an independent
test.** Record it that way. Do **not** run it as a test of the hypothesis.

**I set this trap and should own it.** My clearance said the substrate "will be able to speak to whether low
affective empathy impairs vicarious learning — whatever it says, read off, never aimed at." I thought "never
aimed at" made it safe. It didn't, and you found why:

> **"No result is a target" protects against *aiming at* an answer. It does not protect against an experiment
> that *cannot* answer.** A tautological manipulation passes the no-aiming check and still yields nothing.

**New standing check — construct validity, distinct from no-result-is-a-target:** *before any
throttle/lesion-based claim, verify the manipulation set does not contain the mechanism's own nodes.* If it
does, the result is entailed and can only be reported as structure.

**REGISTER — audit the throttle sets, this generalises and it matters for the studies:** `AFFECTIVE_EMPATHY`
contains **CeA**, which is also (i) the sole afferent of LC → the NA teaching signal, (ii) the source of
`CeA→PAG/HYPdm` → the aggression effectors, (iii) the threat hub. **So the affective-empathy throttle
simultaneously manipulates aversive teaching, aggression, and threat.** It is the CU study's primary
instrument. Every claim drawn from it needs this check — some existing ones may be partly structural. Audit
the throttle sets against each mechanism they are used to test, and record which claims are independent and
which are entailed.

## Decision 1 (reduced gain) — NEITHER (a) NOR (b). Do not build it at all.

**"Vicarious < direct" is a FINDING. It is not a mechanism.** Building it in — by *either* route, a gain term
or a chosen cue intensity — makes the model **a theory of vicarious learning instead of a substrate that can
test theories of vicarious learning.** After that, the substrate can never tell us whether vicarious < direct,
because we assumed it. That is the line: *the model must not be a theory.*

(Your instinct that (b) "risks being a coded constant" was right — but (a) has the same problem one step
removed: an intensity chosen *because it produces the reduction* is a coded constant wearing a perceptual
costume. The tell is whether the value comes from the physics or from the wanted result.)

**Build the faithful STRUCTURAL difference instead, and measure what emerges.** The difference between
observed and direct aversive events is structural and the substrate largely already has it:
- **Direct**: `IN-SOMATO:nociception` → CeA **and** the sensory-discriminative route (VPL→S1/S2).
- **Observed**: distal senses (`biological_motion`/`face_like`/`voice`) → SC-Pv → CeA — the **affective route
  only**, no sensory-discriminative component. This is the well-established vicarious-pain dissociation
  (observing pain engages the affective pain network but not S1/S2).

So: present the observed consequence as **the physical fact it is** — a visual/auditory distress display —
through the existing channels, and **whatever CeA drive results is what results.** Then **measure the
vicarious/direct relationship and report it, in either direction.** If it comes out ≈ equal (as it does now,
0.212 vs 0.208), that is a **finding to investigate** — something missing, or a measurement problem — **not
something to code around.**

**And your §5 note is exactly that measurement problem — same class as the punishment read-out:** CeA rests
at 0.550 with a ceiling of 1.000, so **both** vicarious and direct saturate and **the measure cannot
discriminate them at all.** That is not evidence that vicarious ≈ direct; it is evidence the measure is
blind at CeA's current operating point. Report it as such. (See the flag below.)

## Decision 2 (routing) — CONFIRMED

Extend `_social_episode` to present the other's **consequence** as it already presents the other's **act** —
flowing through the existing `felt_response` → CeA → LC → phasic NA path. **No parallel module.** This is
presenting a physical fact (the other displays distress) through channels that already exist. Clean, small,
and it is the actual gap.

## NEW FLAG — CeA's operating point makes your accumulation caveat currently UNANSWERABLE

You flagged: *"the magnitudes are tiny per-exposure (~1e-4–1e-3); whether they accumulate into a
behaviourally-real disposition over a life-course is a measurement question, not yet established. Do not
assume."* Correct — and here is why it is not merely unestablished but **not currently establishable**:

Verified: **CeA baseline=0.05, setpoint=0.1 — but it RESTS at 0.550.** That is a **5.5× mismatch**, giving
`homeo_factor = 0.9991` — **~9× the erosion pressure LC had (0.9999)**. And **all 17 CeA afferents have bounds
`[0.0, 1.0]` — none bounds-pinned — including `IN-SOMATO:nociception`**, the innate primary threat link (and
R4 has no plasticity guard, per the register).

Unlike LC, this is **self-limiting rather than unsatisfiable** — CeA's elevation is afferent-driven, so the
homeostat *can* reach its target by scaling those afferents down. **That is the problem.** It means CeA's
threat responsiveness will drift downward over developmental time **toward an ungrounded scaffold constant** —
a developmental trajectory driven by a placeholder, not by biology or experience. This is the registered
systematic bias with a concrete, severe instance **sitting directly on the vicarious pathway.**

**Consequence for this phase:** vicarious learning accumulates at ~1e-4/exposure while the homeostat erodes
the same pathway's drive on the same timescale. **Any life-course accumulation measurement would be
accumulation-against-erosion of unknown size — uninterpretable.**

**So: build routing (Decision 2), measure the per-exposure mechanism and the vicarious/direct relationship,
and report both — but DEFER the life-course accumulation verification until CeA's operating point is
resolved.** Do not attempt it and do not assume it either way. Register the deferral with this reasoning.

(Note the two flags interact: CeA's 0.550 resting level is *also* what saturates the vicarious/direct
comparison. One ungrounded operating point, two blocked measurements.)

## Land
- Routing built; **no vicarious<direct coded**; vicarious/direct relationship measured and reported as-found,
  with the saturation caveat.
- §4 recorded as **structurally entailed**; throttle-set audit registered; the construct-validity check added
  as a standing rule.
- CeA operating-point flag registered; life-course accumulation **deferred** with reasoning.
- Full suite green; **commit + push + STOP for clearance.**

## Process
The model is a representation, not a theory — findings are measured, never built in. Construct validity is a
separate check from no-result-is-a-target. Diagnose → surface → build.

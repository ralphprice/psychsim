# PsychSim — Master Design & Build Document, Part 7 (Supplements & Addenda, continued)

*Sealed, versioned supplement to `PsychSim_MASTER.md` and Parts 1–6. Not updatable once distributed;
further guidance becomes a new Part. Section numbering continues the global sequence (this Part =
S14–S15).*

Two closures: the **core/module boundary** made explicit, with the gate-A result recorded at its true
width as a **core-validation observation** (S14); and the resolution of the **DA/satiety
state-dependence** item — **already wired in v8, no seed edit needed** (S15).

---

## S14. The core/module boundary, and gate A recorded as a core-validation observation

### S14.1 The boundary (made explicit for the record)

- **The core** is the universal organism and its machinery: the substrate, the **four matrices**
  (social, environmental, group, **self-reflection**), the 1/n developmental plasticity, behaviour
  selection, and the general instruments (the **bank**, the **Arena**). None of this is about
  psychopathy. Self-reflection is a human faculty; the Arena is a general testbed; banking is a general
  capability. All of it would exist if psychopathy had never been mentioned.
- **The circuit-breaker module** is *only* the throttle panel that attenuates specified circuits on a
  given character. That is the **entire** footprint of the study-specific plugin. Switch it off and you
  have a complete, ordinary simulated human. **The module is done** (the breakers were built; that was
  it).

### S14.2 Reframe of everything since the breakers

Everything built after the circuit breakers — self-reflection, the Arena, banking, the 1/n schedule —
has been **core completion and validation**, not psychopathy work. The throttle was used as a
**probe/stressor to exercise the core** (attenuate a circuit, check the core still behaves sanely), so
its framing bled into the descriptions and the reviews spoke of a "psychopathy divergence." That was a
labelling error. What was actually being tested was whether the **core organism** is complete, honest,
and well-behaved. The psychopathy **study** — the slider sweeps, the scan controller, the search for CU
signatures or field-data matches (Part 4 S8, Part 6) — has **not been run**; it is deferred work
conducted *on* the finished core.

### S14.3 The gate-A result, recorded at its earned width

Recorded as a **core-validation observation**, not a study finding:

> On the complete core organism (age/experience-decreasing 1/n plasticity; all four matrices, with
> self-reflection routed as a **non-feedback read-out**), under a graded attenuation of the
> affective-empathy circuitry: **development converges** (the developed state settles, it does not
> oscillate), and the developed outcome is **well-posed and stable across two independent channels**
> (behavioural executive control and developed self-regard) and across development duration. The
> behaviour is stable and mechanistically traceable throughout. The hypothesised
> differential-susceptibility interaction between fearlessness and childhood environment **does not
> robustly emerge**; what *does* robustly emerge is the reads-but-doesn't-feel dissociation
> (structural/activation-level) and a strong main effect of childhood environment on developed
> self-regard.

Two notes attached to the record:
- **A mechanistically-legible wrong-way result** was observed and is flagged as a candidate finding for
  later study, not buried: the attenuated (fearless) agent is somewhat *buffered* against a harsh
  childhood — less environment-driven self-criticism — because the same attenuation that blunts
  threat-based responses also blunts threat-colouring of self-appraisal. It runs *opposite* to
  differential susceptibility, and it is traceable, which makes it a checkable claim about the world.
- **The width of the null is bounded:** self-reflection was tested as a **non-feedback read-out** (it
  observed the developed state without altering it — byte-identical executive trajectory with/without
  it). So the earned statement is "self-reflection *as a non-feedback read-out* does not carry the
  effect," **not** "self-reflection cannot." Whether self-reflection *as a feedback loop* would behave
  differently is a distinct, untested question — deliberately not opened, and recorded as a boundary.

### S14.4 What is validated vs what is still ahead

Validated: the core organism is complete and behaves stably, traceably, and well-posedly under a
circuit-attenuation probe. Still ahead (deferred): the psychopathy **study** proper — throttle sweeps,
the scan controller, field-data matching — run on this finished core. Core-validation observations
belong in the core record; psychopathy findings will belong to the study when it is run.

---

## S15. DA/satiety state-dependence — resolved: already wired in v8, no seed edit needed

### S15.1 The finding

Part 3 S5.4 flagged that motivational state-dependence (a reward is valuable when the matching drive is
high, near-worthless when sated) should be **circuit modulation, not DA scaling**, and that *if v8
lacked a deficit→VTA edge it would need a seed edit in a future Part.* **v8 already carries the full
chain**, and it is cited:

```
IN-INTERO:nutritive_state  ->  LH  ->  VTA
     (energy-deficit signal)   (orexin/Glu)   (dopamine)
```

- `LH` function is explicitly *"appetitive drive hub; links homeostatic/energy state to VTA
  (SEEKING)"* — sourced to **Stuber & Wise 2016**.
- `IN-INTERO:nutritive_state → LH` — the energy-state input channel drives LH (catalogue, cited).
- `LH → VTA` — the orexin/glutamate appetitive-drive projection to dopamine (anatomy).

So the honest mechanism — hunger raises LH drive to VTA, amplifying the dopaminergic reward response to
food cues; satiety lowers it — is **present, grounded, and meaning-blind by construction** (it is
circuit activity, not DA scaled by a computed `r`). **No seed edit, no v9, is required for this.**

### S15.2 What remains (8b.6 — verification and loop-closure, not a seed change)

- **Close the loop:** ensure the state vector's **energy variable** (via the interocept↔substrate
  bridge, 8b.1 / Part 2 S2.5) actually **drives** the `IN-INTERO:nutritive_state` input channel, so LH
  tracks *real* hunger/satiety. The wiring exists; confirm nothing leaves it open (the substrate can't
  gate reward by hunger if nothing injects the current hunger state).
- **Verify it functions:** an energy deficit should amplify the food-reward DA response and a sated
  state attenuate it — the motivational-modulation signature. This is **circuit dynamics + bridge
  wiring**, an 8b.6 validation target, not a design task.
- **Honesty (unchanged):** the modulator remains a circuit output (LH activity), never DA scaled by a
  computed value.

### S15.3 Roadmap update (supersedes the Part 6 S13 note on this item)

Of the two mechanism gaps: **DA/satiety needs no seed edit** — it is wired in v8; it is verified and
loop-closed at 8b.6 as circuit dynamics. **Continuous maturation** (the adolescent-risk bump) remains
an **engine change** (feed the late schedules into the executive's control capacity, not just
plasticity — Part 3 S5.4), *also* not a seed edit. **Therefore neither mechanism gap requires a seed
edit, and no v9 is needed for them.** The Part 6 S13 line "DA/satiety … needs a seed edit → a future
Part" is superseded: it does not.

# Expression — BUILD HANDOVER (the full system)
**Researcher ruling: build it all, including the volitional limb. Values stay SCAFFOLD — grounding and
tuning belong to the 209-edge audit and the self-regulation mechanism, not to this level. Build the
structure faithfully; do not tune.**

Four phases, dependency-ordered. **Commit + push each; stop for clearance.** Prior ruling
(`PsychSim_Expression_Diagnostic_Ruling.md`) stands — read it first; it carries the Q1 resolution, the
keystone re-expression, and why the construct-validity failure dissolves rather than gets fixed.

---

## Why this order

Everything needs the **right nodes** before it needs edges (A). The involuntary limb is *completing hubs that
already exist* — the PVN-OT/LC precedent — so it is the natural first build (B). The display can only read an
effector once one exists (C), and reading **effectors** means it does **not** change again when the volitional
route lands — so it comes before D and the two re-homed branches close earlier. The volitional limb is
meaningless until there is an involuntary display to suppress and effectors to drive (D).

---

## PHASE A — the effector layer (grain + the missing effector)

**A1. Split `PAG` per its own function field.** It reads *"Defensive output: freeze (vlPAG) / flight (dPAG)"* —
two functionally opposite columns in one node, the §9 amygdala violation, self-declared. Split to **`vlPAG`**
(passive coping: freezing, quiescence, **and vocalisation**) and **`dlPAG`/`lPAG`** (active coping:
fight/flight). Grounding: Bandler & Keay 1994; Tovote et al. 2016; Holstege.

**A2. Re-target PAG's six afferents onto the right column — ground each, do not distribute by guess.**
`CeA`, `BNST`, `SC-Pv`, `VMH`, `VMHvl`, `DRN`. Two are load-bearing and known:
- **`CeA → vlPAG` with its cited target cell.** Tovote et al. 2016 — *the paper the edge already cites* —
  establishes CeA's GABAergic projection targets **vlPAG GABAergic interneurons**, disinhibiting the
  glutamatergic output. So add the **`vlPAG-GABA`** interneuron (the `CeA-GABA`/`ITC` precedent) and route
  through it. **CeA's sign stays −1.0; the weight stays 0.70; only the target becomes explicit.**
- **`VMHvl → dlPAG`** — the attack pathway. **Untouched.**
Bring the other four to review with grounding before committing them.

**A3. Split `NuAmb` per its formations.** Seeded as *"Parasympathetic CARDIAC outflow"* only — but the nucleus
is genuinely two things: the **compact/semicompact formation** (laryngeal/pharyngeal — the common effector for
voluntary *and* involuntary vocalisation) and the **loose/external formation** (vagal cardiac preganglionics).
Split to **`NuAmb-vocal`** and **`NuAmb-cardiac`**; re-target `PVN`/`NTS` → `NuAmb-cardiac`. **`NuAmb-vocal`
currently has no existence in the model at all.**

**A4. Add `NuFac` (facial motor nucleus) — absent entirely.** It is the **convergence point for both
pathways** (Kuypers 1958; Morecraft et al. 2004), so it must exist before either can reach it.

**A5. Re-express `test_cea_to_attack_effectors_still_inhibitory_and_unchanged`** to what it *protects* — CeA is
GABAergic (−1.0) and the CeA→defensive-effector drive is unaltered (0.70) — not to the literal node name.

**Done =** splits landed, afferents re-targeted with citations, `NuFac` present, keystone re-expressed,
**neutral floor + phenomena battery re-run and REPORTED.** If the split flips a prior behavioural finding
(e.g. "damping CeA disinhibits attack"), **that is a finding — surface it, do not tune around it.**

---

## PHASE B — the involuntary limb (the emotional/extrapyramidal route)

The dead ends get their outputs. **All grounded; this is completion, not addition.**

- **`vlPAG → NuAmb-vocal`** — PAG's defining output. Holstege: **PAG lesions cause complete mutism** in cats,
  monkeys and humans.
- **`PAG-PANIC → NuAmb-vocal`** — the in-seed *"infant-cry/protest output"* finally outputs.
- **The emotional route to the face.** Ground it before building: the cingulate motor areas (`dACC`/MCC)
  project to the facial nucleus (Morecraft et al. 2004) — the emotional motor system's cortical hub. Note
  `dACC → PAG-PANIC` is currently `basis: "assumption"` — **the one cortical→expression link is ungrounded;
  ground it or flag it.**
- **The respiratory limb** — the faciorespiratory coordination PAG drives (Holstege 2014). Diagnose what
  exists before adding.
- **`SympOut` — complete its efferent.** Same finding (dead end, 1 in / 0 out), same class. **It is also
  load-bearing later:** the signature cost of suppression is that expression falls while **autonomic arousal
  rises** (Gross). Without an autonomic output that cost cannot be measured, and we would return here.

**Done =** no dead ends left in the emotional motor system; every edge cited; suite re-run.

---

## PHASE C — the honest display

**`_DISTRESS_DISPLAY` reads the EFFECTORS** (`NuFac`, `NuAmb-vocal`) — **never the affective circuits.**

- **Present it on the channels the effectors actually reach:** the face is a visual cue (`IN-CONSPEC` /
  `face_like`), the cry is an **auditory** cue (`IN-AUD`). *A consequence worth expecting rather than
  designing: what a perceiver picks up now depends on which channel it has — that should fall out, not be
  coded.*
- **This closes both re-homed branches at their source.** Chronic-distress invisibility (CeA=1.000 → display
  0.000 by tick 800) and contagion damping were artifacts of phasic-differencing a limbic signal to fake a
  display. Close them out here.
- **This dissolves the construct-validity failure.** Overlap with `AFFECTIVE_EMPATHY` goes to zero on its own.
  **Do not touch the throttle set.**
- **Re-measure the vicarious route. Expect the numbers to move — that is the point.** `vicarious < direct`
  must be **re-derived, not preserved.** If it no longer holds, report that.

**Done =** display reads effectors; both branches closed; overlap zero; vicarious re-measured and reported.

---

## PHASE D — the volitional limb (the model's first motor output)

**Note what this is:** the substrate has nine sensory input channels and **zero motor output** — behaviour is
a read-out. This is the first instance of the output side. Build it narrow: **the face and voice only**, not a
general motor system.

- **Add `M1-face`** (primary motor, face representation) and **`PMC-l`** (lateral premotor).
- **`M1-face → NuFac`** — the pyramidal/corticobulbar route. **The posed expression.**
- **`PMC-l → PAG` — the SUPPRESSOR.** The PLC model's volitional system, which *suppresses* laughter and
  crying; its loss produces pathological laughing/crying — the agent we currently have.
- **Do NOT author a developmental schedule.** Q7 established the suppressors already come online at 4–8 y on
  PFC-protracted schedules. **Thompson's trajectory is encoded; it needs a pathway to act on.** If a curve has
  to be authored, something is wrong — stop and surface it.

**Done =** both pathways reach the effectors; suppression is structurally possible; no authored schedule.

---

## THEN — the measurement (nothing here is built)

Once both pathways exist, these become **askable for the first time**, and each is measured or it isn't:

1. **Does suppression emerge**, and does it carry Gross's signature — expression down ~50–70%, **felt intensity
   unchanged**, autonomic arousal **up**?
2. **Are display rules learned?** They are acquired by **modelling, correction and reinforcement** — which is
   exactly the learning-pathways work. **Never code a display rule.**
3. **Is the display audience-dependent?** (Zeman & Garber: *it depends on who is watching.*) The social matrix
   already carries ties and status. It should fall out.
4. **★ The dual-pathway dissociation.** Throttle `AFFECTIVE_EMPATHY` → is the **involuntary** display blunted
   while the **volitional** route stays intact? That is the psychopathy expression signature — shallow affect
   and reduced mimicry alongside intact deceptive expression. **It emerges or it does not. It is never built.**

---

## Standing rules
- **The two-pathway difference is STRUCTURAL, never a gain** (the vicarious precedent).
- **Suppression strength, expressivity, display rules: LEARNED or DEVELOPED, never coded.** A constant means a
  missing mechanism (principle 2).
- **Instability = a missing pathway** (principle 1). Giving four dead-end hubs their outputs **will** move the
  dynamics. **Expect it. Report it. Do not rebalance** — and per the researcher's ruling, **do not tune**:
  values stay scaffold for the audit and the self-regulation mechanism.
- **Splits are additions, not cuts.** Byte-additive; nothing removed without both permissions, asked first.
- **Nothing about the psychopathy signature may be built.** The model is a representation, not a theory.

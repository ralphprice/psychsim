# Expression — BUILD HANDOVER v2 (consolidated · supersedes both prior documents)

**This is the only document to build from.** It supersedes `PsychSim_Expression_Diagnostic_Ruling.md` and
`PsychSim_Expression_Build_Handover.md` (v1) — both are superseded in full; their reasoning is folded in
here. Where v1's Phase A conflicts with this, **this wins.**

**Researcher ruling: build it all, including the volitional limb. Values stay SCAFFOLD** — grounding and
tuning belong to the 209-edge audit and the self-regulation mechanism, not to this level. **Build the
structure faithfully; do not tune.** Four phases, dependency-ordered; **commit + push each and stop for
clearance.**

### The finding this level rests on
The emotional motor system **exists and is entirely UNEFFERENTED** — `PAG` 6/0, `PAG-PANIC` 5/0, `NuAmb` 2/0,
`SympOut` 1/0. Not a missing read-out: a **missing output**. Third instance of one pattern (`PVN-OT`
unafferented → `LC` unafferented → this, unefferented). **A hub gets wired in one direction and the missing
direction is invisible until something exercises it.**

### Order
Right **nodes** before edges (A). The involuntary limb is *completing hubs that already exist* — the
PVN-OT/LC precedent — so it is the natural first build (B). The display can only read an effector once one
exists (C); and because it reads **effectors**, it does not change again when the volitional route lands, so
it comes before D and the two re-homed branches close earlier. The volitional limb is meaningless until there
is an involuntary display to suppress (D).

---

## PHASE A — the effector layer (grain + the missing effectors)

### A1. Split `PAG` — **into two, not three. `PAG-PANIC` is already the third column.**
`PAG`'s own `function` reads *"Defensive output: freeze (vlPAG) / flight (dPAG)"* and its `nodes` field says
*"dorsal PAG / ventrolateral PAG"* — **two functionally opposite columns in one node; the §9 amygdala
violation, self-declared.** Split, using the seed's own naming:
- **`vlPAG`** — passive coping: freezing, quiescence.
- **`dPAG`** — active coping: flight/escape.

**`PAG-PANIC` is NOT touched.** It already self-describes as *"separation-distress & vocalisation system
(distinct column from the threat PAG)"* — **it is already a separate column and already the vocalisation
system.** Do not give vocalisation to `vlPAG` (v1 said to; that was written before your find and is
withdrawn) — that would duplicate a column the model already has.

Grounding: Bandler & Shipley 1994; Tovote et al. 2016 (dlPAG activation → flight; l/vlPAG → freezing).

### A2. Route PAG's six afferents — **all six are now ruled. Do not re-litigate; do not guess.**

| edge | column | grounding |
|---|---|---|
| `CeA → vlPAG` | **vlPAG**, via a new **`vlPAG-GABA`** interneuron | **Tovote et al. 2016 — the paper the edge already cites.** CeA's GABAergic projection targets vlPAG GABAergic interneurons → disinhibits the glutamatergic output. **Sign stays −1.0; weight stays 0.70; only the target becomes explicit.** |
| `VMHvl → dPAG` | **dPAG** | its own source names the column (Wang 2015; Falkner & Lin 2014). **Attack pathway — untouched.** |
| `VMH → vlPAG` | **vlPAG** | its cited function (sexual-behaviour motor output / lordosis). Route by the cited function. |
| `SC-Pv → dPAG` | **dPAG** | SC excitatory input mostly targets dorsal PAG; **vlPAG does not participate in *unconditioned* defence** — which is what a looming reinforcer is. |
| `BNST → vlPAG` | **vlPAG** | BSTdm→vlPAG by retrograde tracing (Gray & Magnuson 1992). **⚠ The BNST→anterior-vlPAG projection is GABAergic (Hao et al. 2019, *Cell Rep*) — so this is a second target-cell case, same shape as CeA.** Ground the target cell and bring it with the CeA one. **Do not sign it off the transmitter fallback.** |
| `DRN → vlPAG` **and** `DRN → dPAG` | **both** | Not a hedge — a diffuse raphe modulator reaching both columns **is** the documented character. **Carry the existing 5-HT1A/2A receptor flag onto both.** It then holds two disclosed ambiguities (receptor + column) — both honest, both registered for the audit. |

**⚠ A Point-1 finding — SURFACE IT, do not fold it into this split.** Threat reaches dPAG from the deep
medial SC **via weak, unreliable synapses, so that only very salient and imminent threats fire dPAG neurons —
the threat-imminence threshold lives in the synapse's weakness.** Our `SC-Pv → PAG` is **0.50 (moderate)**.
That is a **grounded qualitative weight statement** (Point-1 class, like the reward-pathway grounding), not a
tune — but it is an **innate-reinforcer link** and moving it changes the looming response. **Report it as a
candidate for its own reviewed pass. Do not change it here.**

### A3. Weights on the split — **do not conserve; do not split the number.** *(On the record, as asked.)*
1. **Nobody measured 0.50.** `basis: "anatomy"` means *the projection is real; the number is a placeholder band*.
2. **0.25/0.25 invents a ratio to preserve a quantity that was never real** — a fudge with a conservation law painted on it, worse than an honest band because it looks principled.
3. **0.50/0.50 doubles nothing real** — it represents two projections that were always there and were carried as one. **The lumped edge was under-representing.**
4. **Rule 8 already answers it.** `normalise_incoming` holds each target's incoming at `max(1.0, len × 0.5)`; **`vlPAG` and `dPAG` each normalise their own afferent set independently.** Do not invent a second conservation law on top of the one the substrate has.

**Each resolved edge takes the band its own anatomy supports.** Where the literature does not differentiate, **both inherit the parent's band, marked `# SCAFFOLD`.**

### A4. `NuAmb` — **rename + add. NOT a split.** *(v1 said split; withdrawn.)*
`NuAmb` is **correctly built but mis-scoped**: its `function` (*"Parasympathetic CARDIAC outflow"*), its
citation (Saper & Stornetta 2015) and **both** its afferents (`PVN`, `NTS`) are **purely cardiac**. It is the
loose/external formation wearing the whole nucleus's name. **There is nothing vocal inside it to divide.**
- **Re-mark the existing node `NuAmb-cardiac`** (rename + function/source correction; nothing moves; the cited cardiac edges stay intact).
- **ADD `NuAmb-vocal`** — compact/semicompact formation; laryngeal/pharyngeal; the common effector for voluntary *and* involuntary vocalisation. **It has no existence in the model at all.**

> **The general rule, and it will recur through the 209-edge audit: SPLIT a node when its content is genuinely
> mixed (`PAG`). RENAME-AND-ADD when it is correctly built but mis-scoped (`NuAmb`).**

### A5. Add `NuFac` (facial motor nucleus) — absent entirely.
The **convergence point for both pathways** (Kuypers 1958; Morecraft et al. 2004) — it must exist before either can reach it.

### A6. Re-express the keystone test.
`test_cea_to_attack_effectors_still_inhibitory_and_unchanged` asserts (a) `CeA.sign == -1.0` — **true,
grounded, keep** — and (b) `weight0 == 0.70` — **a byte-exact state pin.** It says **nothing** about CeA's net
effect on PAG output. Per principle 11, re-express to **what it protects**: CeA is GABAergic; the
CeA→defensive-effector drive is unaltered; the target is now explicit.

### A7. Sweep every reference. **A split breaks callers silently.**
`grep` all of `core/`, `tests/`, and the seed for **`PAG`** and **`NuAmb`** and re-point each. `_DISTRESS_DISPLAY = ("CeA","PAG","BA")` (arena.py:61) is one — leave it reading `vlPAG` for now; **Phase C replaces it.**

**Done =** splits landed; `PAG-PANIC` untouched; six afferents routed as ruled (CeA + BNST target cells brought to review before signing); `NuAmb` renamed + `NuAmb-vocal` added; `NuFac` present; keystone re-expressed; all references swept; **neutral floor + phenomena battery re-run and REPORTED.**
**If the split flips a prior behavioural finding — e.g. "damping CeA disinhibits attack" — that is a FINDING. Surface it. Do not tune around it.**

---

## PHASE B — the involuntary limb (the emotional / extrapyramidal route)

The dead ends get their outputs. **Completion, not addition.**

- **`PAG-PANIC → NuAmb-vocal`** — the in-seed *"infant-cry/protest output"* finally outputs. **This is the primary vocal route: PAG-PANIC is the model's self-declared vocalisation column.**
- **❓ `vlPAG → NuAmb-vocal` — GROUND IT BEFORE BUILDING.** Holstege's vocalisation PAG is the **lateral/ventrolateral** region, which suggests vlPAG also reaches NuAmb-vocal — but with `PAG-PANIC` already carrying the vocalisation function, **establish whether both columns project or only one.** *This is a question the split created; do not resolve it by symmetry.*
- **The emotional route to the face.** Ground before building: the cingulate motor areas (`dACC`/MCC) project to the facial nucleus (Morecraft et al. 2004). **Note `dACC → PAG-PANIC` is `basis: "assumption"` — the sole cortical→expression link is ungrounded. Ground it or flag it.**
- **The respiratory limb** — the faciorespiratory coordination PAG drives (Holstege 2014). **Diagnose what exists first.**
- **`SympOut` — complete its efferent.** Same finding, same class (1 in / 0 out). **Load-bearing later:** the signature cost of suppression is expression falling **while autonomic arousal rises** (Gross). Without an autonomic output that cost cannot be measured and we return here.

**Done =** no dead ends left in the emotional motor system; every edge cited; suite re-run.

---

## PHASE C — the honest display

**`_DISTRESS_DISPLAY` reads the EFFECTORS** (`NuFac`, `NuAmb-vocal`) — **never the affective circuits.**

- **Present on the channels the effectors actually reach:** the face is visual (`IN-CONSPEC`/`face_like`); the cry is **auditory** (`IN-AUD`). *A consequence to expect rather than design: what a perceiver picks up now depends on which channel it has. That should fall out.*
- **Closes both re-homed branches at source.** Chronic-distress invisibility (CeA=1.000 → display 0.000 by tick 800) and contagion damping were artifacts of phasic-differencing a limbic signal to fake a display.
- **Dissolves the construct-validity failure.** `AFFECTIVE_EMPATHY` ∩ `_DISTRESS_DISPLAY` is currently **CeA, BA — two of three display nodes**, so *"CU agents show blunted involuntary expression"* is **true by construction**. It is a **symptom**, not a separate defect: we read affect and call it expression, so an affect throttle explains it *by identity*. **Overlap goes to zero on its own. DO NOT touch the throttle set.**
- **⚠ Re-measure the vicarious route.** `vicarious < direct` (NA 0.127 vs 0.208) was measured off the **fake** display. It must be **re-derived, not preserved.** **If it no longer holds, report that.** It would be the easiest thing in the world to quietly keep a result we are fond of.

**Done =** display reads effectors; both branches closed; overlap zero; vicarious re-measured and reported.

---

## PHASE D — the volitional limb (the model's first motor output)

**What this is:** the substrate has nine sensory input channels and **zero motor output** — behaviour is a
read-out. This is the first instance of the output side. **Build it narrow: face and voice only**, not a
general motor system.

- **Add `M1-face`** (primary motor, face representation) and **`PMC-l`** (lateral premotor).
- **`M1-face → NuFac`** — the pyramidal/corticobulbar route. **The posed expression.**
- **❓ `PMC-l → ?` — the SUPPRESSOR. GROUND THE TARGET COLUMN BEFORE BUILDING.** The PLC model has the volitional system descending from lateral premotor to suppress the PAG faciorespiratory/laughter-crying centre — **which is now three nodes (`vlPAG`, `dPAG`, `PAG-PANIC`), not one.** *This question did not exist before the split. Establish which it acts on; do not distribute by symmetry.*
- **Do NOT author a developmental schedule.** The suppressors already come online at 4–8 y on PFC-protracted schedules. **Thompson's trajectory is already encoded; it needs a pathway to act on.** If a curve has to be authored, something is wrong — stop and surface it.

**Done =** both pathways reach the effectors; suppression is structurally possible; no authored schedule.

---

## THEN — the measurement (nothing here is built)

Askable for the first time once both pathways exist. Each is measured or it isn't:
1. **Does suppression emerge**, with Gross's signature — expression down ~50–70%, **felt intensity unchanged**, autonomic arousal **up**?
2. **Are display rules learned?** Acquired by modelling, correction and reinforcement — the learning-pathways work. **Never code a display rule.**
3. **Is the display audience-dependent?** (Zeman & Garber: *it depends on who is watching.*) The social matrix already carries ties and status. It should fall out.
4. **★ The dual-pathway dissociation.** Throttle `AFFECTIVE_EMPATHY` → **involuntary** display blunted while the **volitional** route stays intact? That is the psychopathy expression signature — shallow affect and reduced mimicry alongside intact deceptive expression. **It emerges or it does not. It is never built.**

---

## Standing rules
- **The two-pathway difference is STRUCTURAL, never a gain** (the vicarious precedent).
- **Structure is the one thing this model claims is grounded.** Weights may be scaffold; **structure may not.** An ungrounded structural call gets researched, never guessed.
- **Suppression strength, expressivity, display rules: LEARNED or DEVELOPED, never coded.** A constant means a missing mechanism (principle 2).
- **Instability = a missing pathway** (principle 1). Giving four dead-end hubs their outputs **will** move the dynamics. **Expect it. Report it. Do not rebalance — and do not tune.**
- **Splits and renames are additions, not cuts.** Byte-additive; nothing removed without both permissions, asked first.
- **Nothing about the psychopathy signature may be built.** The model is a representation, not a theory.

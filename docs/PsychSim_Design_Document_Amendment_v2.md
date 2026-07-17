# PsychSim — Design Document AMENDMENT v2
### Brings `PsychSim_Design_Document.md` (2026-07-07) current to 2026-07-15

**Status of this amendment.** The design document is the authority we return to when a session balloons,
and it has repeatedly already contained the answer — **§2.11's three weight categories killed the entire
HSO arc**. That mechanism only works if the document is true. It is eight days stale, and in that time the
architecture it describes as "current" was **retired** and the architecture it describes as "the successor"
was **built and substantially exceeded**. This amendment supersedes the sections named below. Sections not
named here stand, but are **unverified against current code** and should not be trusted without a check.

**Supersedes:** §0 (status) · §2.1–2.9 (retired) · §2.10 (resolved) · §2.11 (built) · §11 (rewritten) · §13
(relations). **Adds:** §2.15–2.20 (the systems built since) · §15 (the development pathway) · §16 (the
governing principles).

---

## §0 (REPLACED) — Status, purpose, and the governing discipline

The document's opening claim — *"Everything in this document is a crude scaffold. Not one construct here is
a claim about how minds actually work"* — **is no longer true, and its replacement must be precise, because
overclaiming here is exactly what the platform's value rests on not doing.**

**What is now grounded, not scaffold:**
- **Structure** — which circuits exist, which connect to which: catalogued at nucleus grain, per-edge
  citations, `evidence_base` (`human` / `human+animal` / `animal_dominant`) and `confidence` tiers coded.
- **Signs** — derived from cited receptors via the `RECEPTOR_SIGN` table, never written. **A dishonest sign
  requires citing a false receptor: a checkable lie, not a quiet tweak.**
- **Target cells** — where established (the CeA-GABA interneuron, the vlPFC→ITC re-target, DRN, the α2
  autoreceptor): a projection's *net* effect follows from which cell type it lands on.

**What remains scaffold, and is disclosed as such:**
- **Weights** — symbolic bands (`low`/`moderate`/`moderate-strong`/`strong`), not fitted decimals. This is
  *more* honest than false precision — there is no `0.447` threaded into a window — but **74 of 208 edges
  self-declare `default_weight_basis: "assumption"`.**
- **Baselines and homeostatic setpoints** — 82 of 83 circuits carry the ungrounded uniform pair
  (0.05 / 0.1). **LC is the sole grounded exception** (0.15 / 0.15, pacemaker electrophysiology).
- **Timescales** — near-uniform (78×200 ms), not the measured ionotropic ≪ metabotropic ≪ neuromodulatory
  hierarchy.

**The standing honesty caveat, and it governs every claim the thesis makes:**

> **Until the 209-edge target-cell audit is complete, "nothing in the substrate was coded for convenience"
> is NOT established — it is the thing the audit will make true, or reveal the exceptions to.** Every result
> produced before it, including the emergent adolescent inverted-U, is *provisional in that specific sense*:
> it emerged from a mostly-grounded, not an audited, substrate. The audit is what upgrades results from
> "emerged from a mostly-grounded substrate" to "emerged from an audited one" — the standard the thesis
> needs. See §15.

The three governing principles of §0 stand unchanged and remain non-negotiable: **no encoded psychological
effect**; **the substrate is a neutral stage**; **at a crude stage the model should produce chaos, not
order**. To them, §16 adds the principles that have since been *earned* rather than assumed.

---

## §2.1–2.9 (RETIRED) · §2.10 (RESOLVED)

**The seven Panksepp systems as the "networks" are RETIRED** (2026-07-10). The category-free substrate is
no longer "the successor" — **it is the system.** Panksepp is a **read-out, not a foundation**: adult
activity patterns (including anything Panksepp would name) are *emergent validation targets, never inputs*.

**§2.10's "known architectural inconsistency" (two affect pathways coexisting) is RESOLVED** — by the
retirement, not by reconciliation. World behaviour and speech-acts now derive from the substrate's emergent
read-out.

---

## §2.11 (UPDATED — the successor, as built)

**The premise stands verbatim and is the design's spine.** So does the honesty wall on the learning rules:
a rule may update a connection using only *local, activity-derived* quantities. *"Co-active connections
strengthen"* is allowed (mechanism); *"threat strengthens avoidance"* is forbidden (outcome). **No circuit
knows it is "fear"; no state knows it is "threat."**

### The three weight categories — UNCHANGED, and the most load-bearing paragraph in the document
> Value enters the newborn **only** through a small set of cited **primary-reinforcer** links (nociception,
> looming, startle) — the single unavoidable seed of innate value — with every other weight either
> **hardwired-backbone anatomy** or a **near-zero associative site** that experience grows.

**This paragraph already answered the entire HSO arc** (§15.4). It is the authority to return to when weight
grounding is questioned. Do not restate it elsewhere; return to it.

### The substrate as built (v14 seed, 2026-07-15)
- **83 circuits · 214 connections · 9 input channels · 7 domains** (defensive threat 14 · reward & approach
  12 · sensory 18 · interoception 14 · executive 10 · affiliation 6 · social cognition 4).
- **Input channels — the only way in:** `IN-VIS · IN-AUD · IN-OLF · IN-GUST · IN-SOMATO · IN-PROPRIO ·
  IN-VESTIB · IN-INTERO · IN-CONSPEC` (the last a dedicated social-visual channel — persons are not generic
  objects). **The world cannot reach a circuit directly; it can only present a stimulus to a sense.**
- **Neuromodulator hubs and what they gate:** DA (VTA, 8 afferents → 17 edges) · OT/VP (PVN-OT, 3 afferents
  → 9) · CRF (PVN/BNST → 2) · **NA (LC → 17 — afferented 2026-07-15, previously DEAD)** · **ACh (BF-ACh → 26
  — STILL UNAFFERENTED)** · SNc (DA, unafferented but masked by VTA).
- **Plasticity rules:** R4 homeostatic incoming-weight scaling (`homeo_factor = 1 − rate·(mean_activity −
  setpoint)`, `HOMEO_RATE=0.002`, every 20 steps); **R5 the neuromodulator gate — now PHASIC**; R8
  competitive normalisation (`target = len × 0.5` — the conserved-resource scaffold constant, and the
  principled operating point the uniform-start diagnostic adopted); BCM `theta`; 1/n developmental
  plasticity.
- **Receptor-sign additions since v13:** OTR, V1a (Gq → +1), **CRF-R1 (Gs-coupled → +1)**.
- **Provenance coded, not assumed** — unchanged and still enforced.

---

## §2.15 (NEW) — v14: kinship and attachment

**The keystone, and the acceptance gate for every phase:**
> **Relatedness is an upstream spawn-time FACT that sets *cue similarity* — nothing more. Every bond
> EMERGES from the perceiver's own recognition and reward circuits. A bond is measured, never set.**
Grep-clean of any coded bond/relatedness→behaviour term is a per-phase gate.

**Phase 1 + 1.1 (BUILT).** Ten PVN-OT/MPOA edges given receptor-honest signs (OTR/V1a → Gq → +, each cited);
the OT→reward core is `PVN-OT → NAc-shell` via OTR (Dölen et al. 2013) — **it makes social cues *rewardable*,
not bonded; a bond still requires repeated interaction.** The **vasopressin duality is preserved as
emergent**: V1a → septum/reward = pair-maintenance; V1a → BNST/threat = territorial aggression; **both `+`
from the receptor — the valence emerges from which target the excitation reaches, never from the sign.** The
**CeA target-cell subtlety** was honoured, not forced: OT excites CeA-lateral GABAergic interneurons → net
inhibition of CeA output (Knobloch et al. 2012), so a `CeA-GABA` interneuron carries it rather than asserting
"OT excites CeA output."

**Phase 2 (BUILT) — the signature is a VECTOR, and this was a keystone ruling, not a preference.** Each agent
carries a multi-locus signature (the MHC/scent analogue); relatedness sets the *shared-locus fraction*; the
perceiver computes component-wise overlap against **its own self-signature** (self-referent matching via
MeA → aIns/dmPFC). **Nepotism emerged.** *Why the scalar was inadmissible:* producing a scalar similarity
requires computing `relatedness → a number` and handing it to the perceiver — **relatedness reaching in
pre-digested. That is the forbidden step with one layer of indirection.** The vector keeps relatedness
genuinely upstream. **Post-spawn, relatedness appears in no computation.** And the elegance is the biology's:
no agent needs to know "this is my offspring" — a parent perceives a cue that partially matches *itself*, and
affiliation emerges. (Mateo & Johnston 2000; Lieberman, Tooby & Cosmides 2007.)

**Phases 3–5 (OPEN — see §15).** Phase 3: imprinting critical-period window (the Westermarck/familiarity
engine — needs NO relatedness) + parturition/lactation priming of MPOA care-readiness. Phase 4: pair-bond
maintenance/dissolution + confinement fractiousness. Phase 5: spawn-time kinship structure incl. extended kin
+ the §2.6 relocation primitive + household UI.

**The three emergence tests (REQUIRED, need Phases 2+3) — the keystone's honesty proof:** ① co-rearing
UNRELATED agents → a bond forms; ② relatedness WITHOUT co-rearing → NO bond; ③ incest-aversion emerges from
co-rearing regardless of relatedness. **If a bond ever appears from relatedness alone, the keystone is
violated — STOP.**

---

## §2.16 (NEW) — The representational-memory-executive layer

**What it is for** (and it is the reason the whole current cascade exists): the mind builds **models of
understanding within itself — beliefs, attitudes, opinions** — held with **variable strength and
accessibility**, which **control behaviour through the executive** and **form the personality**. This is
where **rules, law-obedience, morality, ethics and the higher emotions** evolve — the crux of the
sophropathy/CU work. Their **origins are heterogeneous**: some innate/congenital, some built from
experience, some **reasoned** (derived by the executive itself), some linked to base survival instincts down
to the brainstem.

**Rank is one instance of this**, not a thing of its own — which is why the dominance-hierarchy primitive
was paused (§15.3).

**Memory Phase 1 (BUILT).** Unified to **ONE sub-symbolic substrate** — the symbolic MemoryStream overlay
retired. *(Reading A; deliberately unlike Park's generative-agents model, which stores retrievable symbolic
events.)*

**PFC↔memory presentation loop (MECHANISM LIVE, CLOSURE OPEN).** `vlPFC→LA` was re-targeted to **`vlPFC→ITC`**
— vlPFC is glutamatergic and cannot directly inhibit LA; it routes through the GABAergic intercalated cells,
joining vmPFC→ITC (Milad & Quirk 2002). **Closure is blocked on a learned control-disposition** — which
forced the descent into the learning pathways.

**★ The higher-order read-outs — beliefs, attitudes, morality, rules — are NOT BUILT.** This is the layer's
purpose and it remains ahead of us.

---

## §2.17 (NEW) — Learning pathways

**Valence-matched routing** (verified, not assumed): observed **reward → DA**; observed **punishment → NA**.
The control edges are **NA-gated** (`dmPFC→LA`, `vlPFC→ITC`) or **DA-gated** (`vmPFC→ITC`) — re-gating them
to whichever neuromodulator happened to work would be a **false-mechanism dodge**; they are NA-gated because
noradrenergic threat-regulation learning is correct anatomy.

**Vicarious learning (ROUTING BUILT).** Substantially **emergent** once NA was live: observed distress
(`biological_motion`/`face_like` → SC-Pv → CeA → LC → phasic NA) reaches the NA-gated control edges.
`_add_consequence_percept` presents **the bearer's own evoked distress** (defensive population above the
bearer's running baseline — bearer-pure, phasic) through the existing `vulnerable_other` trigger.
**`vicarious < direct` EMERGED UNCODED** (NA 0.127 vs 0.208) from the transduction chain — the bearer's
display (0.472) is sub-maximal relative to the noxious stimulus (0.9) that caused it. **Nothing chose that
number**, and the structural difference carries it alone: direct engages CeA **and** VPL/S1/S2; observed
engages the affective route only — the vicarious-pain dissociation.

**Modeling / imitation — NOT STARTED.** The second learning pathway.

---

## §2.18 (NEW) — The noradrenergic system (the LC arc)

Entered because vicarious aversive learning needs an NA teaching signal, and **LC had ZERO afferents — a
neuromodulator hub wired to distribute but never driven, structurally dead, exactly the PVN-OT pattern.**

- **`CeA→LC` via CRF-R1.** CeA is GABAergic, so a plain excitatory edge would come out *inhibitory* — threat
  *lowering* NA. The honest mechanism is the cited one: the **CeA-CRF→LC** projection acting on **CRF-R1
  (Gs-coupled → excitatory)** — Van Bockstaele. Not sign gymnastics: citing the real receptor the grounding
  names.
- **The teaching signal is PHASIC.** R5 gates on `max(0, mean(source activation) − mean(source
  mean_activity))` — a deviation, not a level. A tonic teaching signal over-consolidates at baseline. This
  **also resolved the deferred VTA-DA tonic/phasic case** in the same stroke.
- **`CeA→LC` is a PHASIC/adapting drive** (grounded: CRF release fires on the event and adapts, it does not
  clamp). This **dissolved the CeA↔LC latch at its source, regardless of α2**, and left baseline/acute CeA
  untouched — preserving the v9 aggression keystone.
- **α2 autoreceptor (`LC→LC`)** — **non-plastic** (an autoreceptor is a *structural element*, not a learned
  association: plasticity was a category error) and **bounds-pinned**; at its grounded value, and **verified
  not load-bearing**.
- **LC is an autonomous pacemaker** — baseline **0.15**, grounded in electrophysiology (Aston-Jones & Cohen
  2005), **NOT selected from the window where tests pass**, with its **homeostatic setpoint paired to it**
  (they describe one quantity: the circuit's intrinsic target firing rate).

**★ The headline finding: the CU punishment "signature" was a DOUBLY-CONFOUNDED ARTIFACT.** It first
appeared as a large graded deficit under a *tonic-NA-confounded teaching signal*, read through a
*tonic-NA-confounded measurement* (the read-out summed CeA/PAG/BA — and **LC projects directly into CeA and
BA**, so it could never be tone-invariant *by construction*; it was only ever valid while LC was dead). On
the cleaned mechanism with a **yoked-unpaired read-out validated tone-invariant to ±0.0000**: **every
throttle learns; there is no CU-style failure-to-learn; "weak, not a failure" HOLDS.** **The robust CU
signature is the reads-but-doesn't-feel dissociation — not the punishment deficit.** Retired as an artifact,
reasoning recorded. *It was caught precisely because it looked like the finding we most wanted.*

---

## §2.19 (NEW) — Emotional expression (THE GAP — nothing built)

`_DISTRESS_DISPLAY = ("CeA","PAG","BA")` — **affective circuits, not effectors. We read the *felt* state and
call it the *shown* state.** Display is a deterministic function of feeling, so **an agent cannot show what it
doesn't feel, nor hide what it does.** This forbids voluntary suppression, learned display rules, expressivity
variation, developmental change — **and displays-without-feeling, the manipulation/mimicry half of
psychopathy. The model forbids a phenomenon the thesis is about.**

**The literature (dive complete — `Emotional_Expression_Master_Reference.md`):** expression is **not a
read-out in the brain either.** Two anatomically separate descending systems converge on the same effectors —
**involuntary/emotional** (subcortical/limbic → extrapyramidal) and **voluntary/volitional** (motor cortex →
pyramidal) — **doubly dissociable in patients** (volitional facial paresis: can't smile on command, smiles at
a joke; emotional facial paresis: the reverse). **PAG is the expression hub**, controlled by **two descending
pathways: an *emotional* system exerting *excitatory* control, and a *volitional* system from lateral
premotor cortex that *suppresses*.** Pathological laughing/crying is what happens when the suppressor is lost
— **which is precisely what we have built.** Suppression cuts expression ~50–70% while leaving felt intensity
unchanged *and raising* autonomic arousal. Display rules are **learned** (modelling, correction,
reinforcement) and **audience-dependent** (*"It Depends on Who Is Watching"* — Zeman & Garber 1996).
Development runs from the newborn who cries uncontrollably to the school-age child who **can control its
expression to others** — driven by protracted PFC maturation **and** experience, with **amygdala–mPFC
connectivity flipping from positive to negative** across childhood.

**The payoff:** the psychopathy expression profile *is* a dual-pathway dissociation (involuntary blunted:
shallow affect, reduced mimicry, reduced contagious yawning; volitional intact and used strategically:
increased deceptive expression). **Build the two pathways faithfully and the signature should emerge — we
would not code "psychopaths fake emotion."**

**Present and unused:** PAG · **PAG-PANIC (in-seed: *"the infant-cry/protest output"*)** · SympOut · IML ·
preSMA (*"motor inhibition interface"*) · the dlPFC/vlPFC/dACC regulation network · the social matrix for
audience · the learning pathways by which display rules are acquired.

---

## §2.20 (NEW) — Known systemic conditions of the substrate

1. **Unafferented hubs.** A neuromodulator hub can be wired to *distribute* while never being *driven* —
   inert, and invisible until something exercises it. Found and fixed: PVN-OT, LC. **Outstanding: BF-ACh (26
   edges — the cholinergic attention/social-cognition system, entirely dead), SNc (masked by VTA).**
2. **Read-outs validated while a hub was dead may not be robust to its revival.** The punishment read-out is
   the pinned instance. **This will recur as BF-ACh and SNc are completed.**
3. **The ungrounded uniform setpoint is a systematic bias.** Any circuit whose true target rate exceeds 0.1
   is **persistently over-suppressed in proportion to its activity** — and we do not know which. **CeA is a
   severe instance: it rests at 0.550 against a setpoint of 0.1 (~9× LC's erosion pressure), with 17
   afferents, none bounds-pinned, including innate `nociception→CeA`.** Unlike LC's (whose pacemaker floor
   made the pressure unsatisfiable and therefore *visible*), CeA's is **self-limiting and therefore
   invisible** — it settles by dragging threat responsiveness toward a placeholder over developmental time.
4. **R4 has no plasticity guard.** `plasticity_schedule=None` does **not** exempt an edge from homeostatic
   scaling — only bounds-pinning does. "Non-plastic" currently requires two mechanisms to mean what it says.
5. **Per-edge phasic character is now load-bearing in four places** — the teaching signal, `CeA→LC`, the
   distress display, and the cross-agent contagion loop. One property; several consequences.

---

## §11 (REWRITTEN) — The replaceability map

| Construct | Stands in for | Replaced by / status |
|---|---|---|
| ~~Seven Panksepp systems~~ | the real machinery | **DONE — retired 2026-07-10.** Panksepp is a read-out. |
| ~~Two affect pathways (§2.10)~~ | — | **DONE — resolved by the retirement.** |
| ~~Legacy circuit/network engine~~ | — | **DONE — world behaviour/speech derive from the emergent read-out.** |
| **74 `assumption`-basis weights** | real birth-strength connectivity | **the 209-edge audit** (§15.5) |
| **Uniform baselines + paired setpoints (82 circuits at 0.05/0.1)** | per-population intrinsic target rates | **the faithful self-regulation mechanism** — the audit home. LC is the only grounded exception. |
| **Near-uniform timescales (78×200 ms)** | the measured ionotropic ≪ metabotropic ≪ neuromodulatory hierarchy | measured values; currently the root of the tonic/phasic conflations |
| **BF-ACh unafferented (26 edges)** | the cholinergic attention/social-cognition system | grounded afferent completion (PVN-OT/LC class) when its edges are on the path |
| **SNc unafferented** | nigrostriatal DA | completion when it specifically matters (masked by VTA) |
| **No expression system** | the emotional motor system + its volitional suppressor | **§2.19** |
| **No modeling/imitation** | the second learning pathway | §15 |
| **No higher-order read-outs** | beliefs, attitudes, morality, rules, higher emotions | **§2.16 — the layer's purpose** |
| **No rank representation** | learned social status | §15.3 — rank as emergent circuit-tuning |
| **`AFFECTIVE_EMPATHY` as a throttle** | a physiological manipulation | **the throttle-set audit** — it contains CeA (LC's sole afferent, the aggression source, the threat hub), so at least one claim from it is **structurally entailed**; it is the CU study's primary instrument |
| **R4 plasticity guard** | "non-plastic" meaning non-plastic | resolve so it holds in one place |
| **`reward_signal()` absolute while called "the RPE"** | consistency | a teaching-signal-consistency pass |
| Executive layer — mechanism + memory route built | prefrontal top-down control | **partially advanced**: vlPFC→ITC re-targeted; loop closure blocked on the learned disposition |
| Genetic/physical endowment · embodiment · TRIGGER_AFFINITY · window_plasticity · behaviour lookup · tie/environment/group rates · activity bundles · schedules · demography · renderer · every numeric parameter | — | **unchanged from v1 — not re-verified in this amendment** |

**Newly disclosed limitations (were not in v1):** the U-shape in the throttle sweep (`[0.117, 0.016, 0.093]`)
is **robustly non-monotone across 12/12 seeds and unexplained** — it graduates to investigation the moment
the throttle carries inferential load. `teen ≤ child` acting-readiness is **not robust** (flips with reward
intensity at 1–2 step margins); `teen ≤ adult` is. A chronically distressed agent **displays 0.000 at
CeA=1.000 by tick 800** — total signal loss, so **chronic-adversity conditions are off-limits for study
claims** until §2.19 lands.

---

## §15 (NEW) — The development pathway

*(Full detail: `PsychSim_Return_Path_Register.md` — the authority on where we are.)*

**§15.1 The spine (the researcher's CU §9 answers, 2026-07-13, never superseded).** The CU study was task 1
until its requirements were defined rigorously; **the definition moved it to last:**
**v14 → v15 → daily-life-course & multi-environment → psychometric observer → the 209-edge audit → the CU
study → the interventions.**

**§15.2 The family module.** v14 Phases 1/1.1/2 done; **3–5 open**; the three emergence tests pending Phase 3.
**The family needs no special machinery** — the research shows shared family environment explains remarkably
little variance and that family power is **structural: proximity, duration, interaction density**, with
non-shared experience driving divergence. The researcher's framing: *families are a hothouse — and **the
Arena already is one.***

**§15.3 Dominance hierarchy (PAUSED).** Diagnostic: **17 of 18 circuits already present**; the hothouse and
the agonistic interactions already exist; **the only genuinely-missing piece is rank as a learned quantity.**
The PFC override pathway exists but is thin (`dmPFC→LA` still unsigned/fallback) and has no rank signal to
regulate. **Two questions unanswered:** (Q1) rank as **emergent circuit-tuning from agonistic history**
rather than a bookkept `status: 0.7` tally? (Q2) override in the same pass, or rank first? **Paused because
rank is a *belief* — an instance of §2.16, which must exist first.**

**§15.4 The descent.** v14 Phase 3 → family-psychology dive → dominance hierarchy → **§2.16 the
representational layer** → learning pathways → **the LC arc** → vicarious → **expression (current)**. Each
step was entered because a diagnostic found the level below load-bearing. **The cascade returns to v14 Phase
3, which is where it started.**

**§15.5 The 209-edge target-cell audit — a MANDATORY pre-study gate.** **Dual** (build session + reviewer
independently against the remote — *an audit for fitting cannot be certified by the entity that may have
fitted*). Per edge: is the **target cell** cited? does the sign follow from it? Classification: **GROUNDED /
WRONG-TARGET / MISSING-ELEMENT / UNGROUNDED-BUT-UNRESOLVED.** That last is the honest release valve — **an
edge marked "target-cell unresolved in the literature" is a documented limitation; only a *hidden* guess is
a fudge.** Output = a permanent per-edge grounding record, **which IS the first rigorous pass of the
anatomical reference document.** *Expect corrections; if it returns "all 209 perfectly grounded," the audit
was not strict enough.*

**§15.6 Side branches (not the spine).** **HSO** — a full cross-homeostatic architecture proposed for a
problem **§2.11 had already solved**; audited (machinery present-but-hollow), M3 spec'd, **rethought and
shelved**; replaced by uniform-start (0.5 = the R8 normalisation equilibrium) + existing plasticity, with
the learning caveat resolved by a **grounded** reward-pathway strength, *not* by moving the operating point.
**Episodic memory / plug-and-play** — feasibility and inertness *proven*, **deferred as a future parallel
version** for cross-system comparison; the unsolved part is the population→rate lossy readout. **Deliverables**
(System Overview, Technical Spec, Deck, Arena UI, scan controller) — done, off-spine.
**The test that separates them: can the level above be built without it? HSO — yes. The LC arc — no.**

---

## §16 (NEW) — The governing principles, as earned

*§0's three principles are the design's premises. These twelve were **learned**, each from a case where the
project nearly got it wrong. They are recorded nowhere else authoritative.*

1. **Instability = a MISSING PATHWAY, not a wrong weight.** Research it, add it cited. Never rebalance.
2. **When a value is load-bearing for a functional result, the arbitrariness is in a mechanism the value
   compensates for. Trace the mechanism; do not tune the value.** *(The α2 latch: the strong-α2 requirement
   was the tell that the drive was unphysiologically tonic.)*
3. **No result is a target — BOTH ways.** Don't aim at a wanted result; **and don't ACCEPT a wanted-looking
   result a mechanism artifact might have produced.** *(The CU signature. Cleaning a mechanism can only
   strengthen a real finding or dissolve a false one — either way the answer becomes trustworthy.)*
4. **Construct validity is a SEPARATE check.** *"No result is a target" protects against **aiming at** an
   answer; it does not protect against an experiment that **cannot answer**.* Before any throttle/lesion
   claim: **verify the manipulation set does not contain the mechanism's own nodes.**
5. **The model is a REPRESENTATION, not a theory. Findings are MEASURED, never built in.** Coding a finding
   (e.g. `vicarious < direct`) destroys the substrate's ability to test it. **The tell: does the value come
   from the physics, or from the wanted result?** A chosen "perceptual" cue intensity is a coded constant one
   step removed.
6. **No grounded values into a partial assembly.** The system is *expected* to be unstable until all real
   components are present; then go to the research for what is missing. **Ground a value only where it is
   groundable in isolation** (LC's pacemaker: yes — an intrinsic, citable rate; CeA's operating point: no —
   afferent-driven, a property of an unfinished system).
7. **Diagnose against the actual code FIRST, surface, then build.** It has caught a wrong premise every time.
8. **Integrate, don't bolt on. Register co-revealed gaps; don't bundle them.** Complete the hub the current
   work needs; register the rest with the phase that owns it. *(PVN-OT and LC were completed; BF-ACh was
   registered.)*
9. **The design document is the authority — return to it.** §2.11 had already answered HSO. **This only works
   if the document is true**, which is why this amendment exists.
10. **Paired values describe one quantity and must be set together.** `baseline_activation` and
    `homeostatic_setpoint` are a circuit's intrinsic target rate; setting one alone made the homeostat fight
    the pacemaker. **A grounded deviation must be listed, cited, and paired — enforced by test, verified by
    injection.**
11. **A committed test that pins current state is not a design guard — but re-expressing one must preserve
    what it actually protected**, not merely what it literally asserted.
12. **The two-role split is itself an honesty mechanism, and the reviewer is not always right.** The build
    session has falsified reviewer rulings with clean data repeatedly (A+B broke the aggression keystone; the
    CS+/CS− read-out failed tone-invariance; the erosion was event- not rest-driven). **Each time the
    corrected version was more faithful *and* more minimal.**

---

## §13 (UPDATED) — Document relations

- **`PsychSim_Return_Path_Register.md`** — **the authority on where we are**: the descent, every open branch,
  the climb back. Update at every level exit.
- **`docs/neuralnetworks/psychsim_substrate_seed_v14.json`** — **the authority on what the substrate IS.**
  Current and **self-documenting**: grounding travels in the `function` field, which is why the guards can
  enforce it. **When this document and the seed disagree, the seed wins.**
- **`Emotional_Expression_Master_Reference.md`** · **`Episodic_Memory_Master_Reference.md`** — the research
  knowledge bases.
- **`PSYCHSIM_MASTER_DOCUMENT_v6.md`** — the versioned substrate master. **Also stale** (v6 prose against a
  v14 seed); needs the same treatment as this.
- **`PsychSim_Handover.md`** / **`ARCHITECTURE.md`** — **known stale**: still describe the retired Panksepp
  engine and carry stale in-code counts.
- **`PsychSim_CORE_RECORD.md`** — the living record of core-validation observations. Study findings belong to
  the study, not here.
- **When code and this document disagree, the code and the Handover win.**

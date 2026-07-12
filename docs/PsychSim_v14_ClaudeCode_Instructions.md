# v14 — Claude Code implementation instructions (kinship, attachment & pair-bonding)

**Sealed build hand-off. Design authority: `docs/PsychSim_v14_Kinship_Attachment_SPEC.md`.**
Build against that spec; this document is the implementable, phased instruction set. Researcher has
accepted the dependency order (v14 → v15 → daily-life-course → psychometric observer → CU study →
interventions) and greenlit v14 as the first buildable task, phased.

---

## 0. THE KEYSTONE (the acceptance gate for every phase)

> **Relatedness (% shared DNA) is an upstream spawn-time FACT that sets *cue similarity* between agents
> — nothing more. Every bond — its strength, its fractiousness, its dissolution — EMERGES from the
> perceiver's own recognition and reward circuits responding to those cues and to early co-rearing. A
> bond is measured, never set.**

No line may map relatedness → bond, kinship → behaviour, or any family variable → an outcome. This is
the v10 pattern exactly (a trait is a *stimulus the bearer presents*; the response emerges from the
perceiver's circuits). **Grep-clean of any coded bond/relatedness→behaviour term is a per-phase gate.**

## 0.1 Standing rules (all inherited from the v9–v13 discipline — non-negotiable)

- **Signs come from cited receptors, never written.** Every new/changed edge gets a
  `dominant_receptor` + `dominant_receptor_basis` (citation); the sign is DERIVED via the v12a
  `RECEPTOR_SIGN` table. A dishonest sign requires citing a false receptor — a checkable lie.
- **Instability = a MISSING PATHWAY, not a wrong weight.** If receptor-signing or an addition makes a
  circuit saturate or a loop run hot, DO NOT rebalance or remove an edge. Research the missing element
  (an interneuron, an autoreceptor, a competing projection) in the literature, bring it to review, add
  it grounded. Positive-feedback saturation almost always means a missing inhibitory element. (OT has
  known PVN autoregulation; if OT→reward saturates NAc, the missing element is likely an autoreceptor
  or a local inhibitory partner — research it, don't tune it away.)
- **The substrate only GROWS. Never cut/defer/omit any real edge or circuit without explicit
  permission from BOTH researcher and reviewer, asked BEFORE acting.** Declining a same-session
  speculative addition that a diagnostic refutes is the working tree self-correcting — not a cut.
- **Weights are scaffold; mark them `# SCAFFOLD`.** You may set a scaffold magnitude so a grounded
  property holds (e.g. a bond can form), but never touch a sign to get behaviour, and always re-prove
  the property emerges.
- **Byte-additive per phase.** 0 circuits/edges removed vs. the prior version; verify with a git diff.
- **Two-role protocol:** you build, commit, and push each phase to `origin/main`; the reviewer pulls
  the remote and verifies before clearing. Do NOT proceed to phase N+1 until phase N is cleared.
  Surface anything substrate-touching for review; never self-resolve it.

---

## 1. PHASE 1 — the OT/VP bonding pathway (the buildable unit NOW)

**Goal:** give the existing oxytocin/vasopressin projections their receptor-honest signs, and complete
the OT→reward gating, so that OT/VP can make a specific conspecific's cues rewarding (bonding) and can
drive territorial aggression (the same peptide, opposite valence by target) — WITHOUT coding any bond.
This is the core mechanism every later phase builds on. It is mostly *activating what exists*.

### 1.1 Receptor-sign these 10 existing edges (all currently on the transmitter fallback)
`PVN-OT` carries **oxytocin + vasopressin**; each target's dominant receptor sets the sign. Assign
`dominant_receptor` + a cited `dominant_receptor_basis` to each; the sign follows from `RECEPTOR_SIGN`:

| edge (exists on remote v13) | dominant_receptor | sign via table | grounding for basis |
|---|---|---|---|
| `PVN-OT → NAc-shell` | **OTR** (Gq) | **+ excitatory** | Oxytocin drives social reward via OTR in NAc (Dölen et al. 2013, *Nature* 501:179; Young & Wang 2004). *The OT→reward core.* |
| `PVN-OT → MeA` | OTR (Gq) | + | OT modulates social/chemosensory processing in MeA (social recognition). |
| `PVN-OT → CeA` | OTR (Gq) | + (on CeA-GABA) | OT excites CeA-lateral GABA interneurons → net inhibition of CeA output (Knobloch et al. 2012, *Neuron*). **NOTE the target-cell subtlety — see 1.3.** |
| `PVN-OT → SEPT` (lateral septum) | **V1a** (Gq) | + | Vasopressin V1a in lateral septum: social recognition + pair-maintenance (Young & Wang). |
| `PVN-OT → MPOA` | OTR (Gq) | + | OT modulation of the parental-care hub. |
| `PVN-OT → BNST` | **V1a** (Gq) | + | Vasopressin V1a in BNST — sustained social/threat; the pair-maintenance↔territorial-aggression node. |
| `PVN-OT → PAG-PANIC` | OTR (Gq) | + | OT modulation of separation-distress/panic circuitry. |
| `MPOA → VTA` | (glutamatergic / cited) | + | MPOA→VTA drive to reward for parental motivation. |
| `MPOA → PAG-PANIC` | (cited) | per receptor | MPOA→PAG parental/defensive interface. |
| `MPOA → VMH` | (cited) | per receptor | MPOA→VMH parental/social interface. |

- For the two peptide receptors: **OTR and V1a are both Gq-coupled → +1** in `RECEPTOR_SIGN`. Confirm
  both are present in the table; if not, ADD them as Gq/excitatory with citation (metabotropic Gq →
  excitatory, consistent with the existing convention) — this is a table addition, flag it in review.
- Do NOT change any weight in 1.1 unless a receptor sign flip forces a re-proof of a property (as in
  v12a) — and if so, only the weight, never the sign, with the property re-proven.

### 1.2 Complete the OT→reward gating (add only what's genuinely missing, against v13)
The pathway needs OT to gate whether a *specific conspecific's cues* gain incentive salience. Enumerate
against v13 what's missing for that — likely candidate: **OTR modulation of `VTA` DA responses to
social cues** (if `PVN-OT`/`MPOA` don't already reach the DA teaching signal in a way that lets social
cues be learned as rewarding). Add the minimal grounded edge(s), receptor-signed, `# SCAFFOLD` weights.
Bring the enumerated list to review BEFORE adding — do not add speculatively.

### 1.3 The vasopressin duality + the CeA target-cell subtlety (get these right)
- **Vasopressin does both bonding and aggression, and that's the point:** `V1a → SEPT`/reward regions =
  pair-maintenance; `V1a → BNST`/threat = territorial aggression. Both are `+` from V1a — the *valence*
  (affiliative vs. aggressive) EMERGES from which target the excitation reaches, never from the sign.
  This is the v12a insight (same transmitter, opposite behavioural valence via different targets).
- **`PVN-OT → CeA` needs the target-cell care from v13's DRN work:** OT excites CeA-lateral GABAergic
  interneurons, which then inhibit CeA output — so the *net* effect on CeA output is inhibitory via an
  excitatory synapse onto an inhibitory cell. If v13's CeA is a single node (no CeA-GABA interneuron
  split), signing `PVN-OT → CeA` as `+` would assert OT *excites* CeA output, the opposite of the
  biology. **If the single-node CeA can't carry this, FLAG it** (like the α2A-in-PFC and PFC→DRN cases)
  — either the sign is deferred with a recorded reason (un-representable as a single edge, needs a
  CeA-GABA interneuron), or a CeA-GABA interneuron is added (grounded — Knobloch et al. 2012). **Bring
  this to review; do not force a sign that asserts a false effect.**

### 1.4 Phase 1 verification (definition of done)
- All 10 edges receptor-signed (or flagged per 1.3); OTR/V1a in the `RECEPTOR_SIGN` table.
- **The bonding-pathway emergence check:** with OT-gating present, a conspecific's cues *can* become
  rewarding through repeated interaction — but a bond does NOT appear merely from the pathway existing
  (no bond without interaction). This is the Phase-1 form of "earned, not coded."
- If any instability appears (e.g. `PVN-OT → NAc-shell +` saturates NAc): **STOP, research the missing
  regulatory element (OT autoreceptor / local inhibition), bring it to review.** Do not rebalance.
- v9 aggression closure holds; phenomena battery 5/5; DA stable (VTA not zeroed, not saturated);
  the adolescent inverted-U still emerges.
- Byte-additive vs. v13 (0 removed). Golden regenerated; report any classification flips with the
  near-tie/decisive distinction.
- Every new/changed edge has `dominant_receptor_basis` with a real citation.
- **Commit, push to `origin/main`, and STOP for reviewer clearance before Phase 2.**

---

## 2. PHASES 2–5 — structure (each detailed into full instructions when reached, after prior clears)

Per the phased discipline, later phases are specified in full only when the prior phase clears review
(each phase's outcome informs the next — especially instability→missing-pathway findings). The
structure, from the spec:

- **Phase 2 — perceptual signature + phenotype matching.** Add the genetic-fingerprint cue (the
  MHC/scent analogue) on `IN-OLF`/`IN-CONSPEC`; relatedness sets signature *similarity* (bearer
  property); the perceiver's `MeA`→`aIns`/`dmPFC` self-referent matching responds to similarity-to-self;
  nepotism + incest-aversion EMERGE. **Signature representation (scalar similarity vs. component-wise
  vector) is RESOLVED AT BUILD here** (locked researcher ruling) — resolve against the trigger
  vocabulary, bring the chosen representation to review. Grounding: Mateo & Johnston 2000; Lieberman,
  Tooby & Cosmides 2007; the insula/dmPFC kin-recognition substrate.

- **Phase 3 — imprinting critical-period window + role-based reproductive priming.** The
  bonding-specific sensitivity window (OT-gated plasticity on the recognition/reward association for
  co-located conspecifics — the Westermarck/familiarity engine, needs NO relatedness); + parturition/
  lactation priming of `MPOA` care-readiness and infant innate dependency (`SEPT` distress →
  distress-relief-is-rewarding). Grounding: Bowlby 1969; Lorenz 1935; Lieberman/Tooby/Cosmides;
  Pedersen (OT/VP parental priming).

- **Phase 4 — pair-bond maintenance/dissolution + confinement fractiousness.** OT/VP-gated
  pair-maintenance sustained by ongoing rewarding interaction; dissolution when the maintaining signal
  decays (nonapeptide plasticity returns to baseline — Scientific Reports 2023); fractiousness emerges
  when confinement (`escape = len(present)`, already in the Arena) forces interaction into the threat
  system; the child-link modifies the pair bond via shared caregiving. All EMERGENT.

- **Phase 5 — spawn-time kinship structure (Arena + town) + the relocation framework (§2.6) + UI.**
  Who is kin of whom; co-rearing arrangement; **the spawn structure MUST represent extended kin —
  aunts, uncles, cousins, grandparents** (locked researcher ruling; mechanically free — extended kin
  fall out of lower signature similarity + actual co-rearing, so the structure just records the
  relationships so signatures are set correctly, no new mechanism); household membership as a mutable
  fact; the gateable relocation primitive + the dissolution hook (bond-decay → one partner relocates —
  emergent trigger, structural mechanism); the household-definition UI. **v15 (generational relocation
  + economics) plugs into this framework's gateable primitive — do NOT build v15 here.**

---

## 3. THE THREE EMERGENCE TESTS (the honesty proof — required once Phases 2–3 exist)

Analogous to the aggression neutral-floor. These are the load-bearing proof that no bond is coded:

1. **Co-rearing UNRELATED agents produces a bond** — proves the bond comes from co-rearing (the
   Westermarck/imprinting mechanism), NOT from relatedness.
2. **Relatedness WITHOUT co-rearing does NOT auto-produce a bond** — proves relatedness alone is not
   coded to bond (it only sets cue similarity).
3. **Incest-aversion EMERGES between co-reared agents regardless of actual relatedness** — the
   Westermarck check; proves the aversion is from co-rearing familiarity, not a relatedness rule.

If any of these fails in the coded direction (a bond appears from relatedness alone; co-reared
unrelated agents don't bond), the keystone is violated — STOP and surface it.

---

## 4. Build-time rulings locked by the researcher (do not re-litigate)
- **Signature representation** — resolved at build in Phase 2, against the trigger vocabulary.
- **Spawn structure represents aunts/uncles/cousins/grandparents** — in Phase 5; mechanically free
  (falls out of signature similarity + co-rearing), the structure records the relationships.
- **Phasing** — the 5 phases above, each reviewed before the next.
- **v15** — a separate spec written AFTER v14 lands; it plugs into the §2.6 relocation framework.

## 5. Hand-off note (for the implementation session)

> **Build v14 Phase 1 — the OT/VP bonding pathway.** Design authority:
> `docs/PsychSim_v14_Kinship_Attachment_SPEC.md`; instructions: this document. The bonding scaffold
> mostly EXISTS on v13 (`PVN-OT` already projects to NAc-shell/MeA/CeA/SEPT/MPOA/BNST/PAG-PANIC, all on
> the transmitter fallback). Phase 1 = give those 10 edges their receptor-honest signs (OTR/V1a → Gq →
> excitatory, cited per §1.1) + complete the OT→reward gating (enumerate what's missing against v13,
> bring to review before adding).
>
> **The keystone (acceptance gate): relatedness sets cue similarity ONLY; every bond EMERGES. No coded
> bond/relatedness→behaviour term — grep-clean.** Two things need care, both to be brought to review,
> not forced: (a) `PVN-OT → CeA` — OT excites CeA-GABA interneurons → net inhibition of CeA output; if
> the single-node CeA can't carry this, FLAG it (add a CeA-GABA interneuron, grounded — Knobloch 2012 —
> or defer the sign with a recorded reason; never assert OT excites CeA output). (b) vasopressin's
> bonding↔aggression duality is CORRECT and emergent (V1a → reward = pair-maintenance; V1a → BNST/threat
> = territorial aggression; both `+`, valence from the target).
>
> **Standing rules:** signs from cited receptors never written; **instability = a missing pathway
> (research + add the missing inhibitory/regulatory element, NEVER rebalance or cut)**; the substrate
> only grows (no cut without both researcher + reviewer permission, asked first); weights `# SCAFFOLD`;
> byte-additive; commit + push each phase and STOP for reviewer clearance before the next.
>
> **Phase 1 done =** 10 edges receptor-signed (or flagged), OT→reward gating completed, the
> bond-can-form-but-only-through-interaction check passes, v9 closure + phenomena 5/5 + DA stable, no
> edges cut, citations on every edge. Then push and stop. Phases 2–5 are detailed as each is reached.

# PsychSim v12a — the sign-convention upgrade (projection/receptor-specific signs): DESIGN SPEC (for review)

**Status: design specification, for design-session review. The BLOCKING prerequisite for the DRN/5-HT node
(2.1b). NOTHING is built until this is reviewed.** Register: §2.1a. Ruled: option (C) — upgrade the sign
convention so 5-HT (and every neuromodulator/mixed projection) can be signed honestly.

This is the most delicate pass since the Panksepp cut: it changes the excitatory/inhibitory **sign** of
existing, already-reviewed edges. Every sign is re-derived from **cited neurochemistry at finer resolution**
— never from desired behaviour. It is not a mechanical find-replace.

---

## 1. The rule change

**Current** (`core/substrate/model._sign`): `sign = f(source transmitter)` — a leading `GABA…` → −1, else
+1. Nucleus-level. This conflates *transmitter* (a property of the source neuron — Dale's principle) with
*postsynaptic effect* (a property of the **target receptor**). The two coincide only for classical
ionotropic transmitters; for neuromodulators the effect lives at the receptor, and the same transmitter is
excitatory or inhibitory depending on which receptor it hits.

**New:** `sign = f(source transmitter, dominant target receptor)`, both taken from the literature. This is
**more** meaning-blind, not less — it defers to the neuroscience at higher resolution. The sign is still a
cited neurochemical fact; the rule just reads it at the receptor.

## 2. The mechanism (meaning-blind: sign derived from receptor pharmacology, receptor cited per edge)

Two layers, so the per-edge work is bounded and the derivation stays a fact, not an assertion:

**(a) A fixed receptor→sign pharmacology table** (in `params.py`, the standard G-protein / ionotropic
classification — not a per-edge choice):
- **Excitatory (+):** ionotropic AMPA/NMDA/kainate (glutamate), nicotinic-ACh; Gs/Gq-coupled metabotropic —
  **D1, 5-HT2, α1, β-adrenergic, M1/M3/M5, mGluR1/5**.
- **Inhibitory (−):** ionotropic GABA-A, glycine; Gi/Go-coupled metabotropic — **D2, 5-HT1(A/B), α2,
  M2/M4, GABA-B, μ-opioid, mGluR2/3**.

**(b) A per-connection `dominant_receptor` field (cited) — required only where the sign is
receptor-determined**, i.e. neuromodulator projections and genuinely-mixed nuclei (§3). The sign is then
*derived* from (a). For classical ionotropic glutamate/GABA projections the receptor is implied by the
transmitter (glutamate→AMPA, GABA→GABA-A), so **no per-edge datum is needed** and those ~120 edges are
unchanged. `_sign()` becomes `_edge_sign(connection)`: use the derived sign if `dominant_receptor` is
present, else fall back to the transmitter rule.

This keeps the honesty property intact: the sign comes from a cited receptor + a fixed pharmacology table,
**never** hand-set to obtain a function — the same discipline as the Allen afferents, at receptor resolution.

> Alternative considered: an explicit per-edge `sign` + `sign_basis` citation (no receptor table). Rejected
> as *less* meaning-blind — it lets a human write the sign directly. Deriving from the cited receptor keeps
> the sign one step removed from choice.

## 3. Scope — the in-scope edges (each examined + cited; NOT all flip)

Only edges whose sign is receptor-determined are in scope. Classical glutamate(+)/GABA(−) ionotropic
projections (the majority) are untouched.

**Neuromodulator projections (14) — currently all `+`; receptor-determined:**
- **DA:** `VTA→{NAc-core, NAc-shell, OFC, vmPFC, dlPFC}`, `SNc→DStr`. D1 (Gs, +) vs D2 (Gi, −) by target
  population — the "dominant receptor" is itself a cited research question per target (e.g. NAc D1 direct
  vs D2 indirect); build-time determination, reviewed.
- **NA:** `LC→{LA, BA, CeA, dlPFC, IML}`. α1/β (+) vs α2 (−) by target.
- **ACh:** `BF-ACh→{dlPFC, V1, S1}`. nicotinic (+) vs muscarinic M2 (−) by target.

**Genuinely-mixed projection nuclei — the projecting population's transmitter/receptor decides:**
- GABA-leading (currently `−`, may flip `+` where the projection is glutamatergic): `MeA→{MPOA, BNST, VMH,
  ATL-TP, VMHvl}`, `VP→{VTA, LHb}`, `MPOA→{VTA, PAG-PANIC, VMH}`, `SEPT→PAG-PANIC`.
- Non-GABA-leading (currently `+`, may flip `−` where the projection is GABAergic): `BNST→{PAG, HYPdm,
  VMHvl}`, `LH→{VTA, LHb}`, `HYPdm→PVN`, `PVN→{RVLM, IML, DMV, NuAmb, Pituitary}`, `VMH→PAG`.

The clear, already-grounded determinations that anchor the pass:
- **`VP→LHb` flips `−`→`+`** — the LHb-projecting VP population is **glutamatergic** (Knowland 2020;
  Stephenson-Jones 2016). This resolves the v11 sign-fidelity gap honestly (receptor, not override).
- **`LH→LHb` stays `+`** — glutamatergic aversion input (Lecca 2017), consistent with v11.

## 4. The high-stakes re-examination: v11's aggression-circuit edges may re-sign

**This pass re-derives the signs of the v11 Allen afferents too — it does not preserve them.**
- **`MeA→VMHvl`** was signed `−` at v11 (MeA nucleus GABA-leading), measured as a "conspecific-cue brake."
  But the MeApd→VMHvl *aggression* projection is substantially **glutamatergic** (Lin 2011; Hashikawa 2017) —
  so under the receptor rule it may **flip `−`→`+`** (an excitatory conspecific-cue drive to the attack area).
  That would change the v11 measured effect (brake → drive) **and** the E5 neutral-floor net (already flagged
  weight-dependent). This is expected and honest: v11's sign was the best the *nucleus* rule could do; 2.1a
  re-derives it at the projection. Whichever way the receptor citation lands is kept, and the downstream
  effects re-measured — never chosen.
- **`BNST→VMHvl`** (currently `+`): BNST→hypothalamus is substantially GABAergic — may flip `+`→`−`.

So 2.1a is not sign-neutral for the aggression circuit; it can move exactly the pathway the CU study
measures. That is why it is spec-first, reviewed, and re-verified edge-by-edge — and why it must land
*before* the DRN node, so the node is built on final aggression-circuit signs.

## 5. Re-verification plan (measured, nothing tuned)

Every sign change is (i) cited to a target receptor, and (ii) checked for its downstream consequence, which
is **surfaced, not tuned**:
- **v9 aggression closure** re-verified (provocation→aggress, plain threat→avoid, neutral→restrain). If a
  re-sign breaks it, that is a real finding about the balance to report — and possibly a signal that a
  receptor determination is wrong, to re-check against the literature (never to fudge the sign for behaviour).
- **E5 neutral floor** re-checked (it is now weight-dependent; a MeA→VMHvl flip changes the VMHvl afferent net).
- **DA dynamics** re-checked (any VTA/SNc re-sign perturbs reward/DA — Regime-B: normal operation stays bounded).
- **Emergent-phenomena battery** (5/5) re-run — the signs feed all of them.
- **Characterisation golden** regenerated, and its diff inspected **edge-by-edge against the sign flips** —
  each moved read-out must trace to a cited sign change, not appear unexplained.
- **Background library regrown** (a sign change alters developed weights → a v11-grown bank is stale; the
  v11 `_restore_engine` guard will catch it).

## 6. Versioning & sequencing

- **v12 = v11 + the sign-convention upgrade** (schema: an optional per-connection `dominant_receptor`;
  `model._edge_sign`; the `params` receptor→sign table; the in-scope edges annotated + cited). Connectome
  topology byte-identical to v11 (same edges, same directions) — **only signs change**, each cited. Archive v11.
- **Then 2.1b = v13 = v12 + the DRN node**, built on final signs. (Or a single combined v12 if the design
  session prefers one review — but two reviews is safer given 2.1a's risk. Proposed: **two**.)

## 7. What I am asking the design session to rule

1. **The mechanism (§2):** per-edge cited `dominant_receptor` + fixed pharmacology table (recommended) vs
   explicit per-edge `sign`+citation. Confirm the receptor-derived approach.
2. **The scope (§3):** the in-scope edge set — accept, or include/exclude any.
3. **The re-sign of v11's aggression edges (§4):** confirm that MeA→VMHvl / BNST→VMHvl are re-derived from
   their projection receptor **wherever it lands** (accepting that v11's measured "brake" may become a
   "drive"), with the effects re-measured and surfaced — this is the honest consequence of the upgrade, not
   a regression.
4. **Sequencing (§6):** two versions (v12 sign upgrade, v13 DRN) vs one combined. Proposed: two.

I have built nothing. On your ruling I execute 2.1a as a full, cited, re-verified pass, then bring the DRN
(2.1b) spec/build on the upgraded convention.

---
*Sources anchoring the clear determinations (full per-edge citation table is the 2.1a BUILD deliverable,
reviewed):* VP→LHb glutamatergic — [Knowland 2020, PubMed 32009492](https://pubmed.ncbi.nlm.nih.gov/32009492/),
Stephenson-Jones 2016 Nature 539:289; LH→LHb glutamatergic — [Lecca 2017 eLife 30697](https://elifesciences.org/articles/30697);
MeApd→VMHvl glutamatergic aggression projection — Lin 2011 Nature 470:221, Hashikawa 2017 Nat Neurosci 20:1580;
receptor G-protein classification — standard pharmacology (Alexander et al., *Guide to Pharmacology*).

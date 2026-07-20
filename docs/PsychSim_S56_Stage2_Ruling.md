# S56 — after Stage 1: **open Stage 2 (CeA), and the sign audit sharpened its fix.** Stage 1 confirmed.

**I verified Stage 1 landed and audited the Stage-2 attribution against the literature before ruling — because
"CeA saturation suppresses HYPdm" rested on a fallback-signed edge, and a wrong sign there would have made
Stage 2 a sign-fix rather than an interneuron addition. The audit resolves it: the attribution is correct, and
the literature sharpens the fix from "add an interneuron" to "add the specific CeA selection microcircuit."
Here is the ruling.**

---

## 1. Stage 1 confirmed — the grounding worked, and its limitation is honest

**The proportional-inhibition grounding landed correctly:** `vmPFC → vmPFC-GABA` at 0.833 (true proportionality,
load 5 vs dACC's 3), `dlPFC → dlPFC-GABA` at 1.0 (**clamped** — load 9 wants 1.5, the `[0,1]` weight ceiling
binds). dACC unchanged as the reference.

- **The dlPFC ceiling clamp is an honest limitation, not a defect in the grounding.** The relation is correct
  (proportional to load); the *representation* (a single `[0,1]` weight) cannot express the gain the heaviest
  node needs. **Register it: the heaviest cortical node is under-corrected because the weight ceiling binds,
  not because the relation is wrong.** *(There is a lever if it proves load-bearing: the missing 0.5× could go
  on the `gate → node` return weight — verified `dlPFC-GABA → dlPFC` is `moderate-strong`, with headroom. But
  do NOT apply it now — it is a Stage-1 refinement to hold in reserve, and splitting the gain across both loop
  weights should only be done if a later measurement shows dlPFC's residual over-drive is load-bearing on a
  standing red. Registered, not built.)*
- **The divergence xfail is RESOLVED and the prediction was beaten** (0.0585 → 0.0401, below the never-moved
  0.05 line, its resolution condition estimated ~0.0504). **The S18 inflation law holds a FOURTH time**
  (0.0755 → 0.0534 → 0.0335 → 0.0585 → 0.0401). This is the earned-negative sentinel doing exactly its job.
- **The golden regen was honest — verified the right way:** no classification flipped (zero outcome changes),
  the shifts small and uniformly directional (the signature of reduced cortical over-drive), and the diff was
  extracted and reported rather than re-baselined blind. **Correct discipline.**

## 2. The sign audit — the Stage-2 attribution is CORRECT, resolved by literature

**Both edges into HYPdm are fallback-signed (`receptor: None`), so I could not take "CeA suppresses HYPdm" on
faith — the fallback sign could be wrong (the S44/S59 hazard). I checked the anatomy:**

> **`CeA → HYPdm` is genuinely INHIBITORY.** The physiology literature is explicit: *"The CEm cells directly
> INHIBIT the dorsomedial hypothalamus (DMH), rostral ventrolateral medulla, and anterior BNST"* (Gilpin/
> Physiology of Fear). CeA's medial output is GABAergic and it inhibits the dorsomedial hypothalamus. **The
> fallback sign is correct — by accident, but correct. The build session's attribution holds: at VMHvl = 0.361,
> HYPdm sits at 0.023 because saturated CeA inhibits it.**

*(And `VMHvl → HYPdm` is correctly excitatory (+) — VMHvl's core is glutamatergic. So the two edges are
correctly signed: VMHvl drives HYPdm, CeA suppresses it, and a saturated CeA wins. The aggression output is
blocked by CeA suppression, not a sign error. Register both as verified-correct fallback signs — two more off
the S59 census, confirmed rather than assumed.)*

## 3. ★ The literature SHARPENS Stage 2 — it is not a generic interneuron, it is the CeA SELECTION microcircuit

**The build session proposed "add the CeL→CeM interneuron." The literature says something more specific and
more mechanistically important:**

> **CeA is a mutually-inhibitory, winner-take-all selection microcircuit.** *"the mutually inhibitory circuits
> of the CeA use a winner-takes-all strategy that supports transitioning across defensive modes"* (Moscarello/
> threat-imminence). The internal wiring: *"the SOM+ cells of the CEl inhibit… the PKC-δ+ cells of the CEl,
> which directly inhibit the output neurons of the CEm"* and *"CEl cells also inhibit CEm cells"; ITC cells
> inhibit both.*

> **★ This is the mechanism: real CeA does NOT saturate all its outputs at once — its internal mutual
> inhibition SELECTS one output mode (one defensive behaviour) and suppresses the others. The model's CeA lacks
> this internal microcircuit, so it saturates as a single lump and drives ALL its targets (and suppresses
> HYPdm) simultaneously. The missing element is not a generic feedback interneuron — it is the CEl→CEm internal
> inhibitory selection circuit that makes CeA a SELECTOR rather than a saturating relay.**

**This is the same finding the branch has hit repeatedly, now at CeA: a region modelled as a single lump that
biology implements as an internal selecting microcircuit** (the PAG columns, the vlPAG-GABA selector, the VMH
core/shell — and now CeA). **Stage 2's fix is grounded and sharpened: add the CeA internal inhibitory selection
microcircuit (CEl→CEm), which lets CeA select an output rather than saturating all of them — including
releasing HYPdm when the selected mode is aggression rather than freezing.** It is the add-the-cited-missing-
element fix, and the cited element is specifically the mutual-inhibition selector, not a generic interneuron.

## 4. RULING — open Stage 2 (the CeA selection microcircuit) next. Not Stage 3.

1. **Stage 2 is measurement-indicated** — aggression fails to recruit HYPdm (0.023), and the audit confirms
   this is CeA suppression, not a sign error. The defect survived Stage 1, as predicted.
2. **CeA is more load-bearing than OFC** — CeA's saturation is implicated beyond the aggression output: CeA
   feeds the whole defensive column, and its saturating-lump behaviour is a broader distortion than OFC's
   single ungated loop. Fixing CeA's selection is higher-value.
3. **The fix is grounded and sharpened** (§3) — the CEl→CEm internal selection microcircuit, not a generic
   interneuron. This is a diagnose-first build: confirm the CeA internal structure the model has (it currently
   has `CeA` + `CeA-GABA` feedforward-from-PVN-OT; the missing piece is the CEl→CEm mutual inhibition driven by
   CeA's own activity, making it recurrent-selecting rather than feedforward-lumped).
4. **Stage 3 (OFC gate) stays indicated but second** — the OFC→DRN residual is real (DRN 0.391 → 0.384) and
   will still need addressing, but it is the smaller, more contained defect. **Measure after Stage 2: does the
   freezing floor fire once CeA selects rather than saturates? Does the residual DRN drive through OFC now
   matter, or was it partly CeA-driven?** That measurement rules whether Stage 3 is still needed and at what
   magnitude.

> **The honest expectation continues: Stage 2 (CeA selection) should release the HYPdm aggression suppressor
> and may also help the freezing floor (CeA's saturation distorts the whole defensive column). But the OFC
> residual (Stage 3) and the dlPFC ceiling clamp (registered Stage-1 limitation) may each still cap the result.
> Measure after Stage 2; let the measurement rule Stage 3.**

## 5. Handoff

**Open Stage 2: add the CeA internal inhibitory selection microcircuit (CEl→CEm mutual inhibition, driven by
CeA's own activity), grounded in the winner-take-all CeA literature — the fix that makes CeA select an output
mode rather than saturating all outputs, releasing the HYPdm aggression suppressor. Diagnose-first: confirm the
model's current CeA internal structure and the exact insertion for the CEl→CEm selection, report, then build.**

**Gate on the full suite and measure: (a) does aggression now recruit HYPdm/dPAG? (b) does the freezing floor
fire once CeA selects rather than saturates? (c) what residual DRN drive remains through OFC (ruling Stage 3)?
(d) does any classification flip (it should not — this is a substrate-selection fix, not an outcome change).**

**Register: the dlPFC ceiling-clamp limitation (with the return-weight lever held in reserve); the two
verified-correct HYPdm fallback signs (CeA→HYPdm inhibitory, VMHvl→HYPdm excitatory — off the S59 census); and
CeA as the latest lump resolved into an internal selecting microcircuit (the twelve-plus lump pattern, now at
CeA).**

> **Stage 1 grounded the cortical loops and cleared the divergence red on a beaten prediction — the S18 law's
> fourth confirmation. The sign audit confirmed CeA genuinely suppresses HYPdm and sharpened Stage 2 from a
> generic interneuron to the specific CeA selection microcircuit the biology implements. Open Stage 2 — make
> CeA a selector, not a saturating lump — then measure what the freezing floor and the OFC residual still owe.
> Root-first, measure between stages, add only what survives.**

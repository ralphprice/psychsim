# The freezing DRIVER — grounding diagnostic (Q2 step 3, DIAGNOSE-ONLY, surfaced for ruling)

The `Mc` output gap is closed (committed `98a6196`); the freezing floor stays the one authorized red for the
**drive gap** — `vlPAG`-glut reads ~0.001 under threat, so `Mc` stays at baseline. This is the grounding
diagnostic for what closes it. **Nothing built. `DRN→vlPAG` and `VMH→vlPAG` untouched.**

Produced by an 8-agent DIAGNOSE-ONLY sweep (5 candidate/alternative angles + adversarial refutation +
synthesis); **every load-bearing claim below was then re-verified by hand against the seed** (the sweep's
one wrong candidate — a "direct CeA→vlPAG-glut driver" — was caught: CeA is GABAergic, verified sign −1).

---

## ★★ The finding underneath the fork: the SOLE driver is fallback-signed on a lump

`VMH` transmitters = `"glutamate/GABA; gonadal-steroid-sensitive"` (the **11th lump**, S41/S43). `VMH→vlPAG`
has `dominant_receptor: None`, weight `low-moderate` — its **+1 sign is a TYPING-ORDER ARTIFACT** ("glutamate"
first → +1), not a cited receptor (S44). **If the cited receptor is GABA-dominant, the one excitatory driver
of the whole freezing column flips to inhibitory.** So before hunting a *new* driver OR gating DRN, the honest
first question is whether the *existing* sole driver is even correctly signed. Code-provable; highest certainty
of anything here. (Consistent with "a result is only as trustworthy as its sign convention," and "value seems
load-bearing? suspect the mechanism.")

---

## THE FORK — missing-driver (a) vs DRN-over-activation (b): both code-real, complementary, unresolved

Both explain the same net-input deficit (≈ −0.056 onto `vlPAG` under threat); either alone fires `Mc`. Not
mine to resolve.

**(a) missing / mis-signed drive.** `vlPAG`-glut's excitatory afferent set is `{VMH}` and nothing else, at
`low-moderate` (0.35) against a co-active `moderate` (0.50) DRN brake — **the sole driver is out-banded by its
own co-active brake**, and that sole driver is the fallback-signed lump edge above.

**(b) DRN over-activation.** `DRN`'s threat-rise (0.185→0.30) is **100% cortically manufactured**: afferents are
`{LHb, vmPFC, OFC, DRN-GABA}` — **no direct noci/olf/spinal/PAG-panic input** (verified). It rises only via
`dlPFC`→`vmPFC`→`DRN`, and `dlPFC↔... ↔DRN` runs through an **un-damped positive-feedback loop**
(`vmPFC→DRN` AMPA, `DRN→vmPFC` 5-HT2A) — provisional-upward per the house rule. And `dlPFC` **saturating to 1.0
under an acute predator cue is itself suspect** (acute stress classically takes dlPFC *offline*). Counterfactual:
hold VMH constant, remove DRN's threat-delta (silence `vmPFC+OFC`) → VMH alone suffices, `Mc` fires. **But**
silencing DRN with *no* cue also fires `Mc` — DRN provides legitimate **tonic** gating, so the defect (if any)
is DRN's threat-**delta**, not its existence. You cannot globally reduce DRN.

---

## Driver candidate-connection-list (ranked; adversarially verified)

| candidate | verdict | why |
|---|---|---|
| **`VMH→vlPAG` band (incumbent)** | **not grounded — do NOT crank** | sweep says `w0≈0.65–0.70` (~2× seed) crosses the floor, but only for noci+olf (olf drives VMH via MeA); under **pure nociception** VMH stays idle (0.116), so a crank does not fix somatic-only freezing. LOW confidence it is a dense vl-column projection. **And its sign is unpinned (above).** A band-crank, not a correction. |
| **direct `CeA→vlPAG-glut`** | **REJECTED (anatomy)** | CeA is **GABAergic (sign −1, verified)** — it cannot excite `vlPAG`-glut. The disinhibition route `CeA→vlPAG-GABA→vlPAG` *is* the CeA freezing mechanism, already built. (Sweep error, caught.) |
| **`PBN→vlPAG-glut` (standalone)** | **REJECTED-as-single-edge** | `PBN` is **inert under the cue** — nociception bypasses it (PBN afferents = touch/intero, not noci; PBN=0.148 flat under threat). A bare edge delivers ≤ the VMH drive that already loses. **Separate real finding:** the missing `IN-SOMATO:nociception→PBN` afferent — PBN's own function advertises a lamina-I spinothalamic arm that is unwired. If grounded, PBN carries signal (→~1.0 when its real afferents fire) and re-enters as a *two-edge* candidate. |
| **`SC-Pv→vlPAG`** | **REJECTED (3 grounds)** | (1) wrong modality — pure visual-looming channel, sits at baseline (0.130) under noci+olf; (2) **wrong column** — SC-Pv correctly drives `dPAG`/FLIGHT; routing it to `vlPAG`/freezing conflates the two opposite columns; (3) won't overcome DRN. Its looming→freeze route is already carried as `SC-Pv→CeA`. |
| **`PMd` / `AHN` / `DMH`** | **REJECTED (not in model + wrong column)** | canonical medial-hypothalamic defensive outputs, but their principal PAG target is the **dorsal/dorsolateral** (escape) column, not ventrolateral freezing. Adding them deepens incompleteness a synapse AND aims at the wrong column. |

---

## The magnitude (scaffold estimate)

- Corrected threshold: `Mc ≈ 0.056 + 0.85·vlPAG`, so `Mc` crosses 0.10 at **`vlPAG ≈ 0.053`** — *lower* than the
  ~0.12 assumed. Net-input deficit ≈ **−0.056**; needs ≈ **+0.055 net excitation** onto `vlPAG` (~one more
  VMH-worth).
- A single new edge **saturates** (homeostatic setpoint scales incoming weight): one edge plateaus at
  `vlPAG≈0.098 / Mc≈0.135` — modest freezing, not maximal. Robust freezing may need more than one lever.

---

## What only the reviewer can ground (the ruling I'm holding for)

1. **Pin `VMH→vlPAG`'s receptor.** `dominant_receptor: None` on a `glutamate/GABA` source → the sole driver's
   +1 is a string-order artifact. Is the vl-column projection glutamatergic (driver) or GABA-dominant (a
   brake)? Code-provable and independent of everything else. **This is the first question.**
2. **Which excitatory projection to `vlPAG`-glut is real, and its target cell?** Do not assign by symmetry.
3. **Complete `PBN`'s nociceptive afferent (`noci→PBN`)?** A real spino-parabrachial gap PBN's own function
   advertises — prerequisite before PBN can be any kind of threat driver.
4. **Should `DRN` be gated DOWN under acute threat?** Activation-**level** question, NOT sign (`DRN→vlPAG`'s
   sign is ruled correct — do not reopen). Its rise is cortically manufactured via an un-damped loop with no
   threat afferent; but "tonic restraint, phasically gated at the acute moment" cannot be represented by the
   single-DRN-level model, and the Deakin–Graeff frame is dPAG/panic, not vlPAG/freezing (cross-column
   extrapolation). Genuinely unsettled.

**Provenance:** nothing built/edited; no git in the sweep. All figures reproduce from `load_substrate()` +
`SubstrateEngine` at age 25 against the seed. Named lineages (Tovote 2016, Deakin–Graeff, Canteras/Motta) are
reviewer-confirmable, not asserted.

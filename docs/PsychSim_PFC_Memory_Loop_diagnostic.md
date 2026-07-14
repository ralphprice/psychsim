# PFC↔Memory Presentation Loop — code diagnostic (for review; NOTHING built)

Per the spec's governing rule (diagnose against the actual code, surface for review, before any build).
Confirms/extends the preliminary reviewer diagnostic. **Headline: the substrate is substantially present
and the PFC→control HALF is genuinely LIVE — but the loop does not functionally CLOSE, for an upstream
reason that signing the inert edges will not fix.**

## 1. Structural (confirms the preliminary diagnostic)
- **PFC circuits present:** vmPFC, dlPFC, dmPFC, OFC, dACC, vlPFC (+ FPC, FEF, preSMA).
- **PFC→subcortical control edges present** (14 to the core limbic/BG targets; more if PFC→PFC-GABA
  interneurons are counted — the "22" is in range). **10 of 14 are `fallback`/unsigned** (recv=None →
  transmitter-default), mostly `assumption` basis; 4 signed (vmPFC/OFC→DRN & →DRN-GABA, AMPA/anatomy).
- **The inhibitory-control ROUTES exist:** `vmPFC→ITC→CeA` (ITC is GABAergic, sign −1 — the intercalated-cell
  gate), `vlPFC/preSMA→STN` (hyperdirect braking), `vmPFC/OFC→DRN-GABA` (serotonergic top-down).
- **Memory reaches the executive:** `HPCv→vmPFC`, `HPCv→dlPFC` (both fallback, `low`). HPCv also →LA, →BA,
  →NAc-shell (memory→limbic, direct).

## 2. Functional — the PFC→control half is LIVE (not inert)
Driving a PFC circuit measurably modulates its downstream targets:
- **`vmPFC` inhibits threat via ITC:** vmPFC 0→1.0 raises ITC (0.086→0.232) and **halves CeA** (0.301→0.103).
  The canonical executive→amygdala inhibition works.
- **`OFC`** also inhibits CeA (−0.16) and strongly drives DRN-GABA (+0.69); **`vlPFC/preSMA→STN`** braking is
  strong (STN +0.75); PFC modulates NAc/reward and the serotonergic loop.
- **One genuine sign concern:** `vlPFC→LA` is fallback-**excitatory** (+0.33) — a regulatory region *raising*
  threat, backwards for control. A candidate mis-signed edge (grounding it inhibitory / via ITC would help).

So the executive **can** modulate behaviour. The downstream control edges are functional.

## 3. Functional — the loop does NOT CLOSE (the key finding)
The memory-derived disposition does not drive contextual executive modulation:
- **Memory net-drives threat, not executive inhibition.** Driving `HPCv` 0→1.0 raises vmPFC (0.20→0.44) *and*
  raises CeA (0.30→0.47): the direct `HPCv→LA/BA` excitation **outweighs** the `HPCv→vmPFC→ITC→CeA`
  inhibition. Memory reaching the executive loses to memory reaching the limbic circuits directly.
- **The developed disposition does not differentially engage the executive.** Bad-history (harsh) vs
  warm-history developed agents are **identical** in the executive↔threat balance — at rest (vmPFC 0.274 vs
  0.270; CeA 0.308 vs 0.319) **and under provocation** (aggress-drive 0.095 vs 0.093; vmPFC 0.276 vs 0.272;
  CeA 0.576 vs 0.587). No PFC-mediated, history-dependent modulation emerges.

## 4. Why — the upstream reason (connects to the Phase-1 finding)
The loop can't close on the current substrate because **there is no history-dependent control-disposition
for the executive to surface.** From Memory Phase 1: the developed history-effect lives in the **plastic
bonding/OT edges** (warm > harsh affiliation), while the **threat/aggression/executive-control dimension is
innate/saturating and history-invariant** (the `nociception→CeA/LA` edges are non-plastic input edges). So a
"this went badly → inhibit the proposed response" signal that *differs by history* does not exist in the
control dimension — the executive has nothing history-specific to present there.

**Therefore the spec's proposed build — "sign/ground the inert edges to make the loop function" — is
necessary-at-most, not sufficient:** most fallback edges are already correctly-signed-by-fallback (PFC
glutamate → excitatory drive onto the inhibitory intermediaries ITC/STN/DRN-GABA), so signing them is largely
a no-op for function (the one real fix is the `vlPFC→LA` mis-sign). The loop's non-closure is **upstream** —
the memory-derived control-disposition isn't there to route — not a matter of unsigned edges.

## 5. What this means (for the design session to rule — I have leans, not rulings)
The honest options:
- **(a) The loop's *mechanism* is already there and correct** — the executive genuinely inhibits threat via
  ITC and brakes via STN. What's missing is a **history-dependent control-disposition** to drive it. That is
  the *learning* question (does experience tune an anticipated-bad-consequence signal in the control
  dimension?), which points at the **next phase (learning pathways)** more than at this one — this loop may
  be "present and correct, waiting for a disposition to present," and the honest Phase deliverable is to
  *sign the genuinely-mis-signed edge(s), document the loop as mechanism-live, and record that its closure
  depends on a control-dimension disposition that current development doesn't produce."
- **(b) Make the closure work now within this phase** — which would require more than signing: e.g.
  strengthening/grounding the `HPCv→PFC` memory→executive channel relative to `HPCv→limbic`, and/or a
  grounded mechanism by which the developed disposition reaches the control dimension. That is a larger,
  more structural build than "sign inert edges," and risks tuning-for-outcome unless each step is grounded.
- **(c) Reframe** — recognize (per Phase 1's finding, now reconfirmed) that the substrate's history-effect
  is dispositional-in-bonding, and scope the "executive presents the learned disposition" loop where a
  history-dependent disposition actually exists, rather than the threat/aggression example.

**My lean:** (a) — the loop's mechanism is live and mostly correctly-signed; the one honest, in-scope fix is
the `vlPFC→LA` sign (a marked-connection completion, per receptor facts, cited); and the real finding to
record is that the loop is *mechanism-live but has no history-dependent control-disposition to present*,
which is the learning-pathways question downstream, not something to force here by re-weighting. But whether
to (a) minimally-fix-and-document, (b) attempt closure now, or (c) reframe is the design session's call —
and it turns on the same tension the Phase-1 diagnostic surfaced: the history-effect is in bonding, the
control dimension is innate/invariant.

**Nothing built.** Surfacing the diagnostic before any change, as ruled. How do you want to proceed?

---

## CLOSE-OUT (reviewer-ruled option (a): minimal fix + documented finding)

The reviewer accepted the diagnostic and closed the phase with one genuine fix + the resequencing finding.
Forcing closure and reframing-to-bonding were both rejected (they would manufacture a disposition that must
emerge from learning, or dodge the finding on the one dimension that already has a plastic history-effect).

**The one fix (done): `vlPFC→LA` sign correction, as a re-target to `vlPFC→ITC`.**
The edge's own source note always intended "lateral-PFC down-regulation of threat (reappraisal)", but it was
`fallback`-EXCITATORY — a regulatory region *raising* threat, backwards. vlPFC is glutamatergic and cannot
directly inhibit LA (there is no inhibitory glutamate receptor to cite — signing it inhibitory would be a
false-receptor dodge). Its NET regulatory effect on the amygdala is via the GABAergic **intercalated cells
(ITC)** — exactly the `vmPFC→ITC` extinction route (Milad & Quirk 2002; reappraisal engages lateral-PFC →
amygdala down-regulation indirectly). So the marked connection is completed faithfully by re-targeting
`vlPFC→LA → vlPFC→ITC`: vlPFC excites the ITC gate → ITC inhibits CeA → down-regulation of threat. Verified:
vlPFC drive now *lowers* CeA (0.28→0.13 at vlPFC 0→1.0) and no longer excites LA. Band unchanged; a
marked-connection completion, not a value change. Edge count unchanged (re-target, not add).

**The resequencing finding (recorded):**
- The PFC↔memory presentation loop is **mechanism-complete and correctly wired**: PFC→control is live
  (vmPFC/OFC→ITC→CeA inhibition, vlPFC/preSMA→STN braking, PFC→DRN-GABA), and the PFC→control edges are
  **plastic and ready** to hold a learned control-disposition.
- But **functional closure is blocked upstream** — there is no *history-dependent control-disposition* for
  the executive to surface, because the plastic control edges are not yet being *driven to learn* one. The
  learning mechanism that would tune them (vicarious/observational learning) does not exist yet.
- **The presentation loop presupposes a learned disposition to present; that disposition's learning is the
  next phase.** So the roadmap **resequences: the learning pathways come BEFORE the loop closes.** The loop
  will close as a *consequence* once vicarious learning can tune the plastic control edges toward "in this
  context, inhibit" — never forced here by re-weighting (that would be coding the answer). This phase is
  therefore complete as far as it honestly goes.

# Learning Pathways — LC Afferent Completion (ruling on outcome (ii)) — Claude Code

**Outcome (ii) is confirmed and accepted, reviewer-verified on the remote. The finding is clean and it is
structurally identical to the PVN-OT afferent completion we already did. RULING: complete LC's afferents as
its own reviewed foundation step, grounded exactly like PVN-OT — THEN build the vicarious mechanism on it.
The build session was right to stop and not force it (re-gating control edges to DA would be a
false-mechanism dodge — they are NA-gated because noradrenergic threat-regulation learning is correct
anatomy).**

## The finding (reviewer-verified at `72908b0`)
- **LC is present with ZERO afferents** — nothing drives noradrenaline, so `neuromod_output("NA")` stays flat
  (~0.05) under every aversive condition. The NA-gated control edges (`dmPFC→LA`, `vlPFC→ITC`) are gated by a
  signal that never fires.
- **LC has efferents** (LA, BA, CeA, dlPFC, IML) — wired to *distribute* NA but not *driven*. Same structural
  gap as PVN-OT: a neuromodulator hub wired to send, not to receive its drive.
- **Contrast confirming the diagnosis:** VTA (the DA hub) has 8 afferents — which is why DA fires to reward
  and NA does not to aversive events. The mechanism is sound (LC→NA gate → control edges); the drive is
  missing.
- **The proposed drivers all exist as circuits** (CeA, PBN, NTS) — so the afferents are grounded additions,
  not new anatomy.

## The build — complete LC's afferents (the grounded aversive drivers of NA)
Add the excitatory afferents that make LC fire on aversive events — each cited, at band, a
**marked-connection completion** (the PVN-OT precedent: NTS→PVN-OT, affective_touch→PVN-OT were added the
same way). No sign gymnastics, no interneuron (these are excitatory drives to LC), no weight change elsewhere.

| edge | role | grounding |
|---|---|---|
| `CeA→LC` (**primary**) | central-amygdala threat/arousal drive to LC — the threat→NA-teaching-signal route that tunes the control edges | CeA→LC noradrenergic arousal to threat (Van Bockstaele et al.; the canonical amygdala→LC projection) |
| `PBN→LC` | spino-parabrachial pain/aversive drive to LC | parabrachial→LC pain-arousal pathway |
| `NTS→LC` | A2 visceral/noradrenergic drive (the same NTS that drives PVN-OT) | Sawchenko & Swanson lineage; NTS→LC visceral drive |

`CeA→LC` is the load-bearing one for the control-disposition: CeA (threat) → LC (NA teaching signal) → gates
the NA-gated control edges toward inhibition — the exact route that unblocks the PFC loop.

## Verify (this is a foundation step, landed on its own — like the PVN-OT completion)
- **The NA teaching signal now FIRES:** an aversive event (nociception / CeA / provocation) drives LC →
  `neuromod_output("NA")` rises (the way reward drives VTA → DA rises 0.049→0.382). Report the aversive→NA
  gradient.
- **It reaches the control edges:** the risen NA actually gates `dmPFC→LA` / `vlPFC→ITC` consolidation (the
  NA-gated control edges are now drivable by an aversive teaching signal). This is the load-bearing
  confirmation — the NA analogue of "OT is now drivable by touch."
- **Grounded + additive:** the 3 afferents cited, at band, excitatory; no other edge changed
  (weight/sign/basis); plasticity/engine byte-identical; edge count = +3.
- **Full suite green** (golden regen honestly if behaviour shifts — an aversive NA signal now firing may
  shift behaviour; understood, not tuned); v9 + Phase-1 + consequence-learning intact.

## Then (next step, after this lands + is cleared) — the vicarious mechanism
With a functional NA teaching signal, build aversive vicarious learning: observed punishment → NA teaching
signal at reduced gain → tunes the NA-gated control edges toward inhibition (the resequencing payoff that
unblocks the PFC loop); observed reward → DA at reduced gain. Valence-matched routing, per the revised steer.
That is a SEPARATE step, after LC's afferents are cleared.

## The dependency chain (why this ordering)
PFC loop closure → needs a learned control-disposition → needs vicarious aversive learning → needs a
functional NA teaching signal → **needs LC's afferents (this step).** Each layer surfaced the next by being
exercised; each resolved by completing a real grounded structural gap, never by forcing. Complete LC's
afferents and the chain resolves upward. (And this is why the control dimension was history-invariant in
Phase 1: not because it's non-plastic — it's plastic — but because the NA teaching signal that would tune it
never fired. This is the missing piece.)

## Process
- **This is its own reviewed foundation step** (like PVN-OT). Complete LC's afferents, verify the NA signal
  fires + reaches the control edges, full suite green — commit + push + STOP for reviewer clearance BEFORE the
  vicarious mechanism.
- Current architecture only; integrate don't bolt on; grounded/cited per edge; dual-reviewed on the remote;
  no result is a target.

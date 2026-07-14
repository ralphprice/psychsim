# PFC↔Memory Loop — Phase Close-Out — Claude Code note

**The diagnostic (already surfaced, `docs/PsychSim_PFC_Memory_Loop_diagnostic.md`) resolved this phase: the
loop's mechanism is LIVE and correctly wired, but functional closure is blocked upstream — on the
learning-pathways phase, not on unsigned edges. This note closes the phase with the one genuine in-scope fix
+ the documented finding. Do NOT force closure; do NOT reframe to bonding.** (Both rejected by the reviewer:
forcing closure would manufacture a disposition that must emerge from learning; reframing to bonding would
demonstrate on the one dimension that already has a plastic history-effect, dodging the real finding.)

## What the diagnostic established (reviewer-confirmed against the remote)
- **PFC→control is genuinely live** (not present-but-inert): vmPFC→ITC→CeA inhibition works (CeA halves under
  vmPFC drive); OFC inhibits CeA + drives DRN-GABA; vlPFC/preSMA→STN braking is strong; PFC modulates NAc
  and the serotonergic loop. The executive→behaviour modulation mechanism is real.
- **The PFC control edges are PLASTIC** (vmPFC→ITC, dmPFC→LA, vlPFC→STN, vmPFC→DRN, OFC→DRN, LA→CeA all
  plastic) — so they *can* hold a learned control-disposition. What is non-plastic is the *innate threat
  input* (nociception/provocation/formidability → LA/CeA/VMHvl), correctly innate.
- **The loop does NOT functionally close:** memory net-drives threat not inhibition (HPCv→LA/BA excitation
  outweighs HPCv→vmPFC→ITC→CeA); bad-vs-warm history are identical under provocation. **No history-dependent,
  PFC-mediated control-modulation emerges.**
- **The upstream reason:** there is no history-dependent control-*disposition* for the executive to surface.
  The plastic PFC→control edges are *ready* but are not being *driven to learn* a "this went badly → inhibit"
  disposition — because the learning mechanism that would tune them (the learning-pathways phase) does not
  exist yet. **The presentation loop presupposes a learned disposition to present; that disposition's
  learning is the next phase.** So the roadmap resequences: learning pathways BEFORE the loop closes.

## The one fix (do this)
- **`vlPFC→LA` sign correction.** It is currently `fallback`-excitatory (+0.33, `assumption`) — a regulatory
  region excitatorily *raising* threat, which is backwards. Sign it correctly from the receptor facts: vlPFC's
  regulatory projection onto LA is net-regulatory/inhibitory (via the ITC/GABAergic intercalated route, like
  the vmPFC→ITC→amygdala precedent), NOT direct excitation onto LA. Per-edge cited (the ventrolateral/lateral
  PFC → amygdala regulatory pathway), at band — a **marked-connection completion** (the DRN/interneuron
  re-mark precedent), not a value change. Verify vlPFC now regulates rather than excites LA.

## Document (do this)
- Record in the diagnostic ledger the **resequencing finding**: the PFC↔memory presentation loop is
  mechanism-complete and correctly wired; PFC→control is live and the control edges are plastic-and-ready;
  but **functional closure is blocked on the learning-pathways phase** — the control-disposition the executive
  presents must be *learned* into the plastic control edges, and that learning is built next. The loop closes
  as a *consequence* after the learning pathways exist — never forced here by re-weighting (that would be
  coding the answer).

## Verify + close
- The `vlPFC→LA` fix is correctly signed + cited; vlPFC now regulates (not excites) LA.
- Full suite green (the sign fix may shift behaviour a little — golden regen HONESTLY if so; no result is a
  target); v9 + Phase-1 memory intact.
- **Commit the one fix + the documented finding; push; STOP.** This phase is complete as far as it honestly
  goes. The next phase (resequenced) is the **learning pathways** — separate handover.

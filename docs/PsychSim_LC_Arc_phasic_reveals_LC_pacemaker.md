# Phasic CeA→LC works — and reveals the last piece: LC needs its intrinsic PACEMAKER tonic drive — finding (HOLDING commit)

Built the corrected ruling (phasic/adapting `CeA→LC`, drop A+B). It **resolves latch + α2-load-bearing +
aggression cleanly** — verified. But the load-bearing DA-learning regression (`test_substrate_learning`)
**broke**, and tracing it surfaced the final coupled piece: **LC has no legitimate tonic drive.** A grounded fix
(LC intrinsic pacemaker) restores everything; it's a new element + a load-bearing value + it raises tonic NA
globally, so I'm **holding for your steer** before the full-suite gate.

## Phasic CeA→LC is confirmed correct (not in question)
- **Latch dissolved by the phasic drive**, not by α2: CeA recovers to 0.36 (≈ HEAD 0.33) through neutral episodes.
- **α2 empirically NOT load-bearing:** loop stable across α2 = **0.0, 0.2, 0.5, 0.85** (all recover to ~0.36,
  *including α2=0.0*). The phasic drive→0 at plateau prevents the latch; α2 sits at its grounded moderate value.
- **Aggression keystone preserved** (baseline/acute CeA untouched — the thing B broke).
- **NA still fires phasically** (rest 0.05 / aversive 0.24). B dropped + registered; per-edge-phasic registered.
- Mechanism built cleanly: a per-edge `phasic_drive` flag (model.py + engine.py) routing the source through
  `activation − mean_activity`, floored at 0 — the existing teaching-signal machinery. One grounded citation
  (phasic CRF release).

## The regression phasic CeA→LC exposed
`test_substrate_learning::test_paired_learns_more_than_unpaired` flipped: paired DA-gated learning **collapsed
7×** (0.035 → 0.005) and fell below unpaired. Traced cleanly:
- Under phasic `CeA→LC`, **LC's tonic level collapses to 0.033** over the pairing (below its 0.05 baseline — the
  α2 autoreceptor over-suppresses the now-undriven LC). LC reaches the reward read-out (NAc-core) 2-hop via
  dlPFC/BA, so tonic NA sets the value-circuit gain; with LC dead, paired learning collapses.
- **Root:** `CeA→LC` (tonic) was **wrongly providing LC's tonic drive** — via CeA's resting 0.34. It was doing
  double duty: LC's tonic tone *and* the phasic stress signal. Making it correctly phasic removes the wrong
  tonic prop and reveals **LC lacks its intrinsic tonic drive**. (Same class as the unafferented-hub findings:
  a source held up by the wrong mechanism.)

## The grounded fix: LC intrinsic PACEMAKER tonic firing
LC neurons are **autonomous pacemakers** (~1–3 Hz tonic firing, intrinsic pacemaker currents, independent of
afferents) — the baseline noradrenergic tone. In the model this is LC's **baseline activation**, which at 0.05
is too low (it was propped by tonic `CeA→LC`). Raise it to represent the pacemaker. Then: tonic NA from LC's own
pacemaker (supports the learning gain + baseline NA tone), phasic CRF bursts on top (`CeA→LC`), α2 autoregulation
— **a complete, faithful LC.** No tonic-teaching artifact returns (teaching is phasic — deviation above baseline
→ 0 at rest).

**Window map (LC baseline vs the two constraints):**
| LC baseline | DA-learning discrimination | CeA↔LC latch |
|---|---|---|
| 0.05 (current) | **FAIL** (paired<unpaired) | recovers |
| 0.10 | pass | recovers (0.41) |
| **0.15** | pass | recovers (0.45) ← candidate |
| 0.20 | pass | recovers (0.49) |
| 0.25 | pass | recovers (0.54) |
| 0.30 | pass | recovers (0.58, nearing re-latch) |

Comfortable window **[0.10, 0.25]** — both hold; not knife-edge. Candidate **0.15** (mid-window). Above ~0.30 the
higher LC baseline tonically drives CeA enough to approach re-latching.

## Held state (nothing committed)
Tree = **complete candidate**: phasic `CeA→LC` + α2 non-plastic moderate (0.5, verified not load-bearing) + **LC
pacemaker baseline 0.15** + B dropped. **20 targeted tests green** (all learning incl. paired>unpaired,
aggression keystone, arena viability, coactive NA-gated learning, neuromod discipline).

## The decision I need
1. **Approve the LC pacemaker tonic drive** (raise LC baseline to represent its intrinsic pacemaker firing) —
   my recommendation; it's the grounded completion of the phasic-`CeA→LC` ruling (LC needs its own tonic drive
   once its afferent is phasic), and it makes a faithful LC (pacemaker + phasic CRF + α2). **Value:** ~0.15
   (mid the [0.10,0.25] safe window) — your steer on the exact grounded band; and
2. it **raises tonic NA globally** (LC→LA/BA/CeA/dlPFC/IML) — expected to shift the golden + possibly some
   behaviours. Honest regen at the gate, understood not tuned — flagging the breadth so it's authorized, not
   sprung.

Then: full suite is the gate (golden regen honestly), commit + push + STOP, then the two CU-shift
re-examinations on the fully-clean mechanism.

**No result is a target — both ways.** The candidate greens all 20 targeted tests (the wanted look), but the LC
baseline is load-bearing for the learning gain and it broadly lifts NA tone — so I'm surfacing the new element +
the value + the global impact for authorization rather than committing it. Phasic `CeA→LC` is the right
mechanism; the LC pacemaker is what completes it honestly.

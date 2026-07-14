# LC Arc — A+B FALSIFIED (B breaks the aggression keystone AND doesn't de-load-bear α2); the real fix is a PHASIC CeA→LC — finding (HOLDING commit)

Built A+B as ruled. The load-bearing verification the ruling demanded **failed in the honest direction**: B
does **not** de-load-bear α2, and it **breaks a committed v9 keystone** (reactive-aggression maturational
restraint). Traced to root: the latch is sustained by the **tonic** `CeA→LC` drive at plateau — so the
grounded fix is a **phasic/adapting `CeA→LC`** (CRF release is phasic), the *same* phasic-vs-tonic insight that
resolved the teaching signal. **Holding the commit; tree set to candidate A as the coherent viable fallback.**

## The clean α2 × B map (fresh subprocess per config; bounds-set, not engine-overridden)
| α2 | B | loop (threat→12 neutral) | aggression @25 (provocation) |
|---|---|---|---|
| 0.50 | none | **LATCH** 1.000 | restrain (0.179) |
| **0.85** | **none** | **stable 0.376** | **restrain (0.193)** ← candidate A |
| 0.50 | 0.50 | LATCH 0.677 | restrain (0.223) |
| 0.50 | 0.70 | LATCH 0.620 | **aggress** (0.236) |
| 0.50 | 0.85 | stable 0.594 | **aggress** (0.245) |
| 0.85 | 0.30 | stable 0.335 | restrain (0.220) |
| 0.85 | 0.50 | stable 0.303 | **aggress** (0.234) |

Reading it:
- **B does NOT de-load-bear α2.** To make the loop stable at α2=0.5 needs **B ≥ 0.85**. At α2=0.5, B=0.5 still
  latches (0.677). The loop needs α2 at its **strong** value regardless of B — the ruling's premise ("B carries
  CeA-side stability → α2 no longer load-bearing") is **empirically false** in the model.
- **B breaks the aggression keystone.** `test_aggression_pathway` (a committed v9 result: adult reactive
  aggression is the dominant impulse held **sub-threshold** by the maturing STN brake → `restrain`) flips to
  `aggress` at **B ≥ ~0.5** (α2=0.85) / **B ≥ 0.7** (α2=0.5). Mechanism: `CeA→PAG` / `CeA→HYPdm` are
  **inhibitory** (CeA gates the attack effectors — the v9 guardrail). B damps CeA → disinhibits the attack
  effectors → aggress drive crosses the (thin: baseline 0.193, threshold ~0.23) act threshold.
- **No B does both.** The B that de-load-bears α2 (≥0.85) is well past the B that breaks aggression (~0.5–0.7).
  A tonic CeA self-brake can only break the latch by also lowering the **acute/baseline** CeA — which is
  exactly the aggression cost. The keystone has thin headroom; any tonic CeA damping eats it.

## Root cause — the latch is sustained by the TONIC `CeA→LC` drive at plateau
At sustained CeA≈1.0, the **tonic** `CeA→LC` (CRF) drive holds LC up, which holds CeA up — a latch. Confirmed
directly: at α2=0.5 (latched), **adapting `CeA→LC`→0 during the neutral episodes lets CeA recover** (1.000 →
0.433). So the sustaining path is the tonic drive, not the α2 or CeA-brake magnitudes.

This is the **same phasic-vs-tonic insight** that resolved the teaching signal earlier in this very arc: a
**tonic** `CeA→LC` is what created both the tonic-NA teaching artifact (fixed at the R5 gate) *and* now the
latch. The physiological ground: **CRF release from the central amygdala is phasic** — it adapts during
sustained activation; a tonic CRF drive of LC is the unphysiological part.

## The grounded fix (recommended): make `CeA→LC` a PHASIC / adapting drive
Drive LC from CeA's **deviation above baseline** (the `_phasic_drive` / `mean_activity` machinery already in the
substrate), not its absolute level. Then at plateau the `CeA→LC` drive → 0, the loop cannot latch — **regardless
of α2 strength**, and **without touching baseline/acute CeA** (so the aggression keystone is untouched). It also
means α2 sits at its grounded pharmacological value without being load-bearing (the phasic drive, not the α2
magnitude, prevents the latch). One grounded mechanism resolves the latch, the α2-load-bearing concern, and the
aggression cost at once — and it's consistent with the phasic teaching-signal fix already in the arc.

**Why this over the alternatives:**
- **A+B (ruled):** B can't de-load-bear α2 and breaks the aggression keystone. Rejected by the data.
- **A-alone (α2 strong, no B):** viable + preserves aggression (candidate A, 13 targeted tests green), but α2
  is load-bearing (moderate latches) — the value carries the loop, which you rightly flagged as suspect.
- **Phasic `CeA→LC`:** the mechanism carries it; α2 grounded-not-load-bearing; aggression untouched. The
  honest one — *if* the phasic-edge mechanism is acceptable.

**The catch:** substrate edges are currently **tonic linear** drives. A phasic/adapting edge is a **new
mechanism** (a per-edge "phasic drive" flag routing through `activation − mean_activity`, flooring at 0). That's
an architectural addition — I will not build it unilaterally. It is modest (the machinery exists) and grounded
(CRF adaptation), but it's your call.

## Held state (nothing committed)
Tree = **candidate A**: phasic teaching signal + `CeA→LC` (CRF-R1) + `LC→LC` α2 **non-plastic strong** [0.85],
**B removed** (it breaks the aggression keystone). BF-ACh + SNc registered. 13 targeted tests green (aggression
keystone, arena viability, coactive NA-gated learning, all learning). This is the coherent viable fallback if
you choose A-alone; it is **not** committed.

## The decision I need
1. **Add the phasic/adapting `CeA→LC`** (my recommendation — grounded in CRF adaptation, resolves latch +
   α2-load-bearing + aggression in one, consistent with the arc's phasic teaching fix), as a small new
   per-edge phasic-drive mechanism; then drop α2 back toward its own grounded value and re-verify it's no
   longer load-bearing; OR
2. **Take candidate A** (α2 strong, no B) and accept α2=strong as its grounded pharmacological value (dominant
   LC brake), noting the load-bearing-at-moderate as a documented property; OR
3. something else.

**No result is a target — both ways.** Candidate A greens and preserves the keystone (the wanted look), but I'm
not accepting it because α2 is still value-carrying; and I'm not landing A+B despite the ruling because it
breaks the aggression keystone. Surfacing the falsification + the phasic root for your steer.

# `VMH → vlPAG` — the grounding is not a weight. **It is a COLUMN question, and the literature disagrees with
# our wiring.**

**I went to ground the weight and the literature would not let me, for the same reason the census wouldn't
let me ground `MeA→ATL-TP`'s sign without asking whether the edge should exist. The weight is not groundable
in isolation because WHERE the edge lands is itself unresolved — and the model and the literature disagree,
with grounding on both sides.**

---

## 1. What the literature actually says — VMH drives immobility via the DORSOLATERAL PAG, not the vlPAG

**The definitive circuit paper (Wang, Chen & Lin, *Neuron* 2015, the collateral-pathways study) is explicit
about the column:**
> **"VMHdm/c projection to the DORSOLATERAL periaqueductal gray (dlPAG) induces inflexible immobility, while
> the VMHdm/c → anterior hypothalamic nucleus (AHN) pathway promotes avoidance."**
> *"the main descending projection to the dorsolateral periaqueductal gray (dlPAG)… activation of the VMH→PAG
> pathway elicits immobility, but not avoidance."*

**Our edge is `VMH → vlPAG`. The literature's edge is `VMH → dlPAG`. Different column.** And the immobility
type differs too: **VMHdm→dlPAG produces INFLEXIBLE / attentive / threat-oriented immobility** (the
predator-confrontation "stop and assess" freeze), which is **not the same** as the **passive, quiescent,
hyporeactive freezing** the model assigns to `vlPAG` (the `CeA→vlPAG` Tovote route). **Two different freezes,
from two different columns, and we have wired the hypothalamic one into the passive column.**

## 2. What the model has — and why the edge had nowhere right to land

```
Our PAG columns:  dPAG   = "ACTIVE-coping: flight / escape / fight"   (v14 Phase A split)
                  vlPAG  = "PASSIVE-coping: freezing / quiescence"
                  (PAG-PANIC = separation distress)
VMH -> vlPAG (AMPA, low-moderate)
VMHvl -> dPAG (strong)          ← note: VMHvl already goes to dPAG
```

> **The substrate collapsed the DORSOLATERAL and LATERAL columns into a single `dPAG` node** (the dl/l lump —
> already on the register). **So the VMHdm→dlPAG "inflexible immobility" projection has no correct target: its
> real target, the dlPAG, is fused into our `dPAG`, which the model defines as the ACTIVE/flight column.**
> **Routing VMH's immobility drive to `dPAG` would put it on the flight column (wrong function); routing it to
> `vlPAG` puts it on the passive-freeze column (wrong column, wrong immobility type).** **Neither is right,
> and that is WHY the edge sat ungrounded — there was no anatomically correct node for it.**

**This is the dl/l lump biting exactly where the register predicted it would.** The `VMH→vlPAG` edge is an
**artifact of the missing dorsolateral column** — the freezing drive was pointed at the only "freezing-ish"
node available, because the node it belongs to does not exist as such.

## 3. Why the weight cannot be grounded in isolation (principle 6, again)
**A weight is groundable only once the edge's endpoints are right.** `VMH → vlPAG`'s magnitude is a question
about a projection that, as the literature describes it, **does not go where our edge goes.** **Grounding the
weight now would be putting a precise number on a mis-routed edge** — the exact error shape of grounding
`MeA→ATL-TP`'s sign without asking whether the edge belonged. **The honest answer is: the column must be
resolved before the weight means anything.**

---

## 4. RULING — do not pin the weight. Resolve the column first.

**Two paths, and this is a genuine fork for you — I am not resolving it unilaterally because it is a
substrate-shape decision, and it interacts with the dl/l split already on the register.**

**(a) Split `dPAG` into dorsolateral and lateral (resolve the lump), THEN route `VMH → dlPAG`.**
- This is the anatomically correct fix. The dl/l split is already registered as a known lump.
- **`VMHdm → dlPAG` = inflexible immobility; `dl`-column freezing is DISTINCT from `vlPAG` passive freezing.**
- Cost: a real substrate change (new node, re-pointed edges), and it is bigger than a grounding pass.
- **Payoff: the freezing column becomes CORRECT, not just grounded** — two freeze types on two columns, which
  is a real distinction the CU/defensive literature cares about (attentive vs passive freezing map to
  different threat-imminence stages, Fanselow's threat-imminence continuum).

**(b) Hold `VMH → vlPAG` as a KNOWN dl/l-lump artifact; ground the weight to the VMH→dlPAG immobility
literature WITH the column caveat recorded.**
- Keeps the edge, records that it stands in for `VMH → dlPAG` pending the split, grounds the magnitude from
  the immobility-drive literature (a strong, behaviorally-decisive projection — optogenetic activation drives
  immobility outright, so **not `low-moderate`; the functional projection is strong**).
- Cost: the edge remains on the wrong column, flagged.
- **This is the `MeA→ATL-TP`-into-the-gap-register move applied to a mis-routing instead of a deletion** — keep
  it, mark it, condition its correctness on a named future fix.

**My recommendation: (b) now, (a) when the dl/l split is opened as its own pass.** Rationale: the split is a
substrate-shape change that deserves its own diagnosis (which VMH population, dm vs c; how the dl and l
columns differ in afferents/efferents; whether `VMHvl→dPAG` also needs re-pointing), and stacking it onto a
grounding pass repeats the "balloon toward complexity" failure. **But the weight, grounded under (b), should
be corrected from `low-moderate` to `strong`** — because the one thing the literature is unambiguous about is
that this projection, wherever it lands, is a **behaviorally decisive immobility driver, not a weak modulator.**

> ★ **And note what this does to the freezing-column story: the driver was never weak. `VMH→vlPAG` at
> `low-moderate` was under-weighting a projection the literature calls a decisive immobility drive — which is
> part of why freezing wouldn't fire. The weight WAS wrong, just not in the direction "needs grounding to a
> plausible value" — it needs grounding to a STRONG value. That is a real correction, and it is testable:
> under (b), does freezing fire once the driver is at its grounded strength AND DRN is on its curve?**

## 5. What to do
1. **Do NOT pin `low-moderate`.** Ground the weight to **strong** (behaviorally-decisive immobility drive;
   Wang/Chen/Lin 2015), basis `literature`.
2. **Record the column caveat**: the edge stands in for `VMH → dlPAG`; it currently lands on `vlPAG` because
   the dorsolateral column is fused into `dPAG` (the dl/l lump). Reinstatement/correction condition: the dl/l
   split.
3. **Register the dl/l split as the next substrate-shape pass** (not this one) — with the open sub-questions:
   which VMH population, how dl vs l differ, whether `VMHvl→dPAG` re-points too.
4. **This is behaviorally live** (weight change low-moderate→strong on the freezing driver) — **so it needs the
   full suite + the keystone, on a confirmed machine.** It is NOT inert. **Do not gate it partial.**

**S57 stays machine-gated. This is now ALSO machine-gated (it changes behaviour). The genuinely
machine-independent grounding left is `noci→PBN` and the opioid system — both additive (new afferent / new
system), neither re-weights a live edge. If you want a machine-independent pass while WSL is down, one of those
is the safer pick; `VMH→vlPAG`'s weight correction should run with a suite.**

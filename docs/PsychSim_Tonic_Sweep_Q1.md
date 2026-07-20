# The tonic sweep — Q1, run. **The answer rescopes the queue.**

**I ran it against `565b1bf`. It is a seed query and it was free.**

---

## 1. ★ The result

```
baseline 0.05  :  94 circuits
baseline 0.19  :   1 circuit   (dPAG-GABA)
baseline 0.15  :   1 circuit   (LC)
```

> **94 of 96 baselines are the same number. Exactly TWO were ever chosen deliberately — both by us, both in
> this arc, both grounded from electrophysiology.**

**A low baseline is defensible for a DRIVEN node, and most of the 94 are driven. That is not the finding.**
**The finding is who else is in there:**

| pacemaker | baseline | |
|---|---|---|
| **`LC`** | **0.15** | ✅ grounded (this arc) |
| **`DRN`** (5-HT) | 0.05 | ❌ `UNGROUNDED — pending` |
| **`VTA`** (DA) | 0.05 | ❌ |
| **`SNc`** (DA) | 0.05 | ❌ — **and SNc is *the* textbook autonomous pacemaker** |
| **`BF-ACh`** | 0.05 | ❌ |

> **Form 3 — a pacemaker at a driven baseline — is not a `DRN` problem. It is a CLASS, and we have fixed one
> of five.** Every one of these nodes has, in reality, an intrinsic rate that dominates its synaptic input.
> **In our substrate, all four have afferents that ARE their activity.** **`LHb → DRN` carrying 100 % is not
> a special case; it is what the class looks like.**

## 2. And it settles two other registered items — both worse than recorded

- **The gate family: EIGHT gates at 0.05, one at 0.19.** I told Ralph four. **It is eight** — `DRN-GABA`,
  `vlPAG-GABA`, `dACC-GABA`, `dlPFC-GABA`, `vmPFC-GABA`, `CeA-GABA`, `ITC`, `PAG-PANIC-GABA`, `VMHvl-GABA`.
  **`dlPFC` has nine excitatory afferents; `dACC` has few. Same brake band, same brake baseline.** **S56 is
  not a `dlPFC` question. It is a nine-node question.**
- **The "82 uniform setpoints" item is really 94 uniform BASELINES.** It has been on the register as
  housekeeping. **It is not housekeeping.**

## 3. ★ The §18 entry — and it outranks the brake layer

> **Every effect size this substrate has ever produced rides on a baseline layer that is ONE NUMBER, chosen
> once, for everything.** **That is not a caveat about a few nodes — it is the substrate's operating point.**
> **It belongs in §18 above the cortical brake layer, and in the thesis's limitations — and it is now
> MEASURED rather than suspected.**

*(The consolation is the one §18 always gives: the direction is known. A uniform-low baseline layer under-
states tonic tone everywhere, which means every brake in this model is weaker than its biology — and
**that inflates**, exactly as the law predicts. Nothing here reverses §18; it explains why it has held four
times.)*

---

## 4. RULING: **do not open #1 yet. The sweep just changed its scope — and #1 and #2 are the same pass.**

**The circularity has to be broken in the right place:**
- **You cannot ask "does this rate MATURE?" before you know what the ADULT rate is.**
- **And you cannot ground an adult rate as a CONSTANT without knowing whether it matures — that is exactly
  the `DRN` lesson, and it cost us a keystone scare to learn.**

> **So both questions are one question, asked per node: *what is the adult tonic rate, and does it mature?*
> Neither half is buildable alone, and both halves are literature. They are mine.**

**THE CALL: I take the grounding pass for all four — `DRN`, `VTA`, `SNc`, `BF-ACh` — adult rate AND
developmental trajectory, and hand back a table. Nothing builds until it is in.** **Call for it when you want
it and I will run it as one piece.**

**And when it lands, expect the DRN shape to repeat**: for any node whose rate matures, **grounding the adult
constant is a category error and the answer is the S57 mechanism** — which is why building S57 before this
table would be building machinery for an unknown number of nodes. **After the table we will know whether S57
serves one node or five, and that decides whether it is a mechanism or an over-engineering.**

## 5. Everything else holds
`DRN` at 0.05 `UNGROUNDED — pending` · keystone green and annotated · freezing floor the one authorized red,
now four terms · `DRN→vlPAG`, `VMH→vlPAG`, `DRN→VMHvl`, the attack drive: untouched.

**S56 re-scoped to nine nodes. S58 answered for Q1 and folded into the grounding pass. `noci→PBN`, the opioid
system, and the VMHvl fallback-sign census entry stay queued.**

**And `files.zip` handled correctly — gitignored, kept on disk, no rewrite.**

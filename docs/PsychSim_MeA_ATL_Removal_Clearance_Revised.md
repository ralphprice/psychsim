# `MeA → ATL-TP` removal — **CLEARED, with one amendment: delete INTO the gap register, not into nothing.**

**Your clearance is correct on every ground and every mechanic. One change only, and it came from Ralph's
question — *why remove rather than switch off?* — which is the right question and which your clearance (and my
original ruling) did not yet answer. The amendment preserves the reinstatement path for free and it sets the
precedent more defensibly than a plain deletion would.**

**This is the project's first connectome deletion, so the form we choose here is the form every future
deletion inherits. That is the reason to get it exactly right.**

---

## 1. What stands, unchanged

- **Both required grounds hold.** **Inert on measurement** — silencing leaves all four labels byte-identical
  (`soph|warm`, `soph|harsh` = executive; `psy|warm`, `psy|harsh` = social_cognition); the label holds
  entirely on `BA → ATL-TP`. **Ungrounded in provenance** — `basis: assumption`, the only assumption-based
  `MeA` efferent, and anatomically the wrong source (in primates the TP–amygdala relation runs through the
  basolateral complex; `BA → ATL-TP`, basal, is the grounded edge doing the work).
- **The sign is already correctly grounded** (−1 / GABA-A; Choi 2005; Swanson & Petrovich 1998) and committed
  as the pre-removal checkpoint at `554db0e`. The census hazard was the WRONG sign (+1 would have flipped
  `soph`'s label); the correct −1 is inert.
- **The golden regeneration stands as specified** — deliberate and documented, 4-decimal exact, confirm only
  `ATL-TP`-adjacent values shift and the four labels stay byte-identical.
- **The full-suite gate stands** — expect `failures=1` (the authorized freezing-floor red), `0 errors`.
- **S63 stands and sharpens** — the substrate's single worst object was worst along four axes at once
  (fallback-signed, load-bearing on a green, assumption-based, carrying a thesis label), and the discipline
  held at exactly that point.

---

## 2. The amendment: **remove from `connections` AND add a `gaps_register` entry**

**Ralph's question exposed that "delete" was hiding a choice between two different end-states:**
- **erased** — gone from the file, the hypothesis it encoded lost with it; or
- **removed from the live connectome but preserved as a known gap** — out of the 240, but its claim and its
  reinstatement condition recorded in the structure built for exactly that.

**The second is strictly better and costs nothing.** The seed already has a top-level `gaps_register`
alongside `circuits` and `connections`. **Use it.**

**On the go, the deletion is TWO file operations, not one:**
1. **Remove `MeA → ATL-TP` from `connections`** (240 → 239).
2. **Add a `gaps_register` entry** recording:
   - **what was removed**: the `MeA → ATL-TP` connection;
   - **why**: `basis: assumption`, load-free on measurement (silencing left all four classification labels
     invariant), anatomically superseded by the grounded `BA → ATL-TP` (TP–amygdala relation runs through the
     basolateral complex, not the medial nucleus);
   - **the reinstatement condition**: reinstate if a direct medial-amygdala → anterior-temporal projection is
     ever grounded in the literature.

**This keeps the hypothesis as a hypothesis, in the place designed for hypotheses — reversible, honest about
the uncertainty, and recoverable — while removing the connection from every computation.**

---

## 3. Why NOT the obvious alternative (weight-0-and-keep)

**Ralph's phrasing — "switch it off for now so it's there to reinstate" — points naturally at zeroing the
weight rather than deleting the connection. That is the one option to avoid, for a mechanical reason:**

- The connection carries **`calibration_active_default: True`** and **`plasticity_coeff_schedule_ref:
  social_cortex_late`.**
- **A zeroed-but-plasticity-active connection can relearn a nonzero weight during a run.** It would read as
  disabled in the file and quietly reanimate in simulation.
- That is worse than either honest state — a dead connection in the list that can come back to life without a
  decision.

**The gap-register form gives Ralph exactly the property he wants — off now, reinstatable later — without the
silent-reanimation risk. If for any reason a weight-0 hold is preferred instead, it MUST be paired with
freezing the connection's plasticity (`calibration_active_default: False`), or it is not the stable off-state
it appears to be. The gap-register form is cleaner and is the ruling.**

---

## 4. The precedent — lock it, because this is the first one

**Record the removal precedent in the sharper form the amendment requires:**

> **A connection earns deletion only by being INERT on measurement AND UNGROUNDED in provenance — both
> required. Inert-alone stays (absence of current effect is not absence of anatomy). Assumed-alone is
> escalated, not deleted. Only the intersection is removed.**
> **AND: deletion means removal from `connections` PAIRED WITH a `gaps_register` entry carrying the
> reinstatement condition — never bare erasure. The claim a connection encoded survives its removal from the
> live graph.**

**That second clause is what makes the first-ever deletion defensible: it establishes that we can take a
connection out of the live connectome without losing the claim it made — not that we can delete things that
happen to be quiet.** **Locking it now means every future deletion inherits the reinstatement path
automatically, and no connection can ever leave the model without a recorded route back.**

*(This is a standing-rule change, so it is Ralph's to ratify as a rule — but I am ruling that THIS deletion
takes this form, and recommending the rule be locked for all deletions. Ralph clears both.)*

---

## 5. Revised go — one clean commit
1. **Remove `MeA → ATL-TP`** (240 → 239) — the first deletion.
2. **Add the `gaps_register` entry** (what / why / reinstatement condition) — the amendment.
3. **Regenerate the golden** deliberately and documented; only `ATL-TP`-adjacent values move, four labels
   byte-identical.
4. **Record the precedent in the locked form** (§4): inert-AND-assumed earns deletion; deletion is
   removal-plus-gap-register, never erasure. Register the `basis: assumption` census as the fallback-sign
   census's provenance sibling (flagged, not run this pass). Sharpen S63.
5. **Full-suite gate** (`failures=1`, `0 errors`), then push.

**Both regions at the connection's ends are retained — only the projection between them is removed, and its
claim is preserved in the gap register. `DRN` 0.05 `UNGROUNDED — pending`; keystone green; freezing floor the
one authorized red. The four-pacemaker table remains mine to run on your call; the two `LA` receptor pins
remain cheap grounding whenever wanted.**

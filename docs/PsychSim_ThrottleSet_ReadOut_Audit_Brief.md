# D6 — THE THROTTLE-SET & READ-OUT AUDIT
### The first actionable of the climb back. **Diagnostic only — build nothing.**

*(The return-path register is a map, not an order. This is the order.)*

---

## Why this, why now
- **Cheap**, and **independent of operating points** — it does not wait on the self-regulation mechanism, the
  brake layer, or the defensive-drive pass.
- **It gets worse with delay.** Every circuit added extends the derived sets automatically; **L7 just added
  10 circuits and a whole new domain.**
- **It is study-critical.** `AFFECTIVE_EMPATHY` is the CU study's **primary instrument**. **Until this runs,
  we do not know how many of the study's claims are true by construction.** That is not a housekeeping
  question — it is whether the study can answer anything.
- **We have caught four of these reactively and every one was live.** Four found by accident is a strong prior
  that the systematic pass finds more.

## The two checks — one pass, both directions
This is **one audit with two halves**, and they are the same question from opposite ends:

**A. THE MANIPULATION SIDE** — *does the set contain the mechanism's own nodes?*
> Principle 4: *"no result is a target" protects against AIMING at an answer; it does not protect against an
> experiment that CANNOT answer.*

**B. THE READ-OUT SIDE** — *does the measure measure what it names?*
> Three failure modes, all found live in L7: a term that **does not carry**; terms that are **not
> commensurate**; a set that **spans two constructs**.

---

## What to enumerate

**Manipulation surfaces (all of them — there are more than two):**
- Every **named circuit set** used as a throttle (`AFFECTIVE_EMPATHY`, `COGNITIVE_MENTALIZING`, any others).
- The **domain-derived scan set** (`throttleable_circuits()` — **auto-extends**, so enumerate what it
  *currently returns*, not what it was written to return).
- The **temperament dials** (`_TEMPERAMENT_DOMAIN` → applied by `seed_substrate` **to every agent**).
- Any lesion/ablation surface.

**Read-out surfaces (all of them):**
- Every named set (`DEFENSIVE_OUTPUT`, the executive set, `_DISTRESS_DISPLAY`, …).
- Every computed signature (`punishment_learning`, `dissociation_index`, `empathy_response`, the acting-
  readiness measures, the golden's per-domain aggregates, anything the UI or a study reports).

## Per set, four questions

| # | question | failure |
|---|---|---|
| 1 | Does this **manipulation** set contain any node of the **mechanism** a claim about it would rest on? | **ENTAILED** — the claim is true by construction |
| 2 | Does every term of this **read-out** set actually **carry** (non-zero under the conditions it is read in)? | **HOLLOW** — the measure rests on a subset |
| 3 | Are the terms **commensurate** — same sign, same units, same direction? | **INCOMMENSURATE** — drivers summed with their brakes |
| 4 | Does the set span **one construct** or two? | **CONFLATED** |
| 5 | For scans: are the **manipulation set** and the **signature set** DISJOINT? | **SELF-SEARCHING** |

**Classification, mirroring the 209-edge audit: `CLEAN` / `ENTAILED` / `HOLLOW` / `INCOMMENSURATE` /
`CONFLATED` / `SELF-SEARCHING` / `UNRESOLVED`.** **`UNRESOLVED` is the honest release valve — a disclosed
limitation is a limitation; only a hidden one is a fudge.**

---

## The eight known cases — use them to calibrate, and expect them to reappear
1. `AFFECTIVE_EMPATHY` ∩ `_DISTRESS_DISPLAY` → **DISSOLVED** in Phase C (by fixing the display, not the set).
2. **`AFFECTIVE_EMPATHY` contains `CeA` — LC's sole afferent, the aggression source, the threat hub.** So
   *"low affective empathy impairs vicarious learning"* is **ENTAILED**. ⚠️ **Still live. This is the big one.**
3. The amygdala's only route to the face ran through **`COGNITIVE_MENTALIZING` — the network CU spares.**
   Would have **inverted** the signature. Fixed by `BA→dACC`.
4. The effectors inherited `defensive_threat` → a low-THREAT dial throttled the facial nucleus. Fixed.
5. The gate class was temperament-throttled → **directionally perverse**. Fixed (7 tagged).
6. **`DEFENSIVE_OUTPUT` = (`CeA`, `vlPAG`, `BA`) computes on 2 of 3** — `vlPAG` is 0.000. **HOLLOW. Live.**
7. **The executive read-out CONFLATES** monitoring with control (`dACC` is conflict-monitoring; it correctly
   rises under harsh). **Live, xfailed.**
8. **Domain aggregates are INCOMMENSURATE** — they contain drivers *and* their gates, so the number moves
   opposite to its name. **Live.**

---

## Rules
- **DUAL AUDIT — build session and reviewer, independently, then reconcile.** Non-negotiable, and the evidence
  is that **of the four caught this arc, we caught two each.** Neither side finds them all. *(And the
  209-edge precedent: an audit for a defect cannot be certified by the entity that may have introduced it.)*
- **Report, do not fix.** Every fix is a separate ruling. **Do not edit a throttle set to make an overlap go
  away** — Phase C is the precedent: the overlap dissolved because the *display* was fixed, not the set. **A
  set edited to remove an overlap hides the defect; it does not resolve it.**
- **Enumerate what the code returns, not what it says.** The derived sets auto-extend.
- **Expect `UNRESOLVED` entries.** If the audit returns "all sets clean," it was not strict enough.

## Output
A table: **set · type · every member · verdict · the claim it would entail or hollow · evidence.**
Then surface. **Nothing is fixed in this pass.**

*After this: the CeA operating point (needs the self-regulation mechanism), then D4 modelling/imitation, then
D3 — where `M1-face`'s socket waits.*

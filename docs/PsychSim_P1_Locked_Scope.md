# P1 — LOCKED. Close the exchange so it carries FEELING and reads HISTORY.
### The first top-down loop-fidelity pass. Scope fixed against the confirmed seams.

**I read both seams. The result is precise and good: the loop already CLOSES — but it carries the wrong thing,
and it doesn't yet read history. P1 is the two smallest changes that fix exactly that. Here is what the code
actually does, then the locked scope.**

---

## 1. WHAT THE SEAMS ACTUALLY DO (verified, not inferred)

### Seam 1 — the exchange DOES close. This is the good news.
`GameMaster.converse()` / `_one_turn()` runs a real coupled exchange:
> A `perceive`s the situation → A's substrate emits `social_act` (emergent) → the act goes through a
> `SpeechChannel.exchange()` → **B perceives it (vigilance-seeded) → B's substrate runs on the resulting
> appraisal → B answers.** Both acts are adjudicated into the world and **written to each mind's memory.**

**The loop is wired end to end. A's output reaches B's input and drives B's next act, and both are recorded.**
That is ARC3→ARC1→ARC2→ARC4, already turning. **P1 is NOT "build the coupling" — it exists.**

### But it carries the ACT LABEL, not the FEELING — Gap 1
What crosses the channel is `act_from_behaviour(resp.behaviour, …)` — **the behaviour label** (what network A
settled on), rendered to a line, and perceived through a vigilance roll (deception can be seen or missed).
**What does NOT cross: A's affective/expressive STATE — the display.** B learns *what A did* (an act, possibly
deceptive) but not *how A felt or showed it* — the smile, the tension, the non-verbal leakage. **The L7
expression apparatus (NuFac, the display routes, the two-pathway leakage) produces A's display, and the
channel does not carry it to B.** The transmitting side (ARC3) is built and the receiving side (ARC1,
`IN-CONSPEC`) exists, but **the affective band of the exchange is not connected** — only the propositional/act
band is.

> **This is exactly the "non-verbal, smiling, all the many facets" exchange you named as central. It is the
> gap. A's feeling is produced and B could perceive it, but the wire between them carries only the act.**

### Seam 2 — the record does NOT yet feed back into perception — Gap 2
`Person.perceive()` builds the appraisal from: institutional climate (warmth/structure), body needs
(reward/safety/belonging), and the directed event's overrides. **It does NOT read the relationship record.**
The `GameMaster` maintains `rel(a,b)` (affect, trust) and each mind has a `memory`, and these are WRITTEN on
every exchange — **but `perceive` never reads them.** So an agent appraises an encounter with someone it has a
long fraught history with **identically** to an encounter with a stranger, given the same institutional
setting and body state. **The record accumulates and does not yet shape the person.**

> **This is the second frontier question, answered: the matrices record, but the record does not feed back. The
> logbook exists; it is not yet memory-as-lived-experience.**

---

## 2. ★ P1 SCOPE — LOCKED. Two changes, both small, both loop-completing.

**P1 closes the two gaps that stop the existing loop from carrying feeling and reading history. Nothing else.**

### Change A — the exchange carries AFFECT (connect ARC3's display to ARC1's perception)
- When A acts, the channel must carry **A's displayed affective state** alongside the act label — sourced from
  A's substrate expression (the L7 effectors / the affect that drove them), not invented.
- B's `perceive` must fold that displayed affect into B's appraisal — through `IN-CONSPEC` (the conspecific
  channel that already exists for exactly this) — so **B's substrate runs on WHAT A did AND HOW A showed it.**
- ★ **The display is subject to the same two-pathway honesty L7 built:** what A *shows* may diverge from what A
  *feels* (suppression leaks; deception may be seen or missed by B's vigilance — which the channel ALREADY
  models for the act band; extend it to the affect band). **A low-empathy agent showing a mask, and B's
  substrate reading the leakage or not, is the CU-relevant phenomenon — and it must EMERGE from the two
  substrates, never be scripted.**

### Change B — perception READS the relationship record (connect ARC4 back to ARC2)
- `Person.perceive()` must read `rel(self, other)` (affect/trust) and/or the mind's memory of this specific
  other, and let it **colour the appraisal** — history of warmth raises `social_valence` toward this person;
  history of harm raises `threat`/lowers `trust` in the read.
- **This is the minimal record-feedback: the same encounter appraised differently by an agent who remembers
  the other.** It is what makes the accumulated record change who the person is in the next encounter.

### What P1 is NOT (the guardrails)
- **NOT scripting the response.** Both changes wire what B's substrate PERCEIVES; B's act remains emergent from
  B's substrate. We connect the input band; the behaviour still falls out of the mechanism. **The honesty wall
  holds: we make B perceive A's feeling and their shared history; we do NOT tell B how to respond.**
- **NOT building new substrate.** Both changes use existing pieces — L7's display, `IN-CONSPEC`, `rel`, the
  mind's memory. P1 is COUPLING work in `sim_world`/the channel, not new circuits. (If a specific missing
  circuit surfaces, it goes to the ARC-2 backlog and is drawn only if P1's claim needs it.)
- **NOT the accumulation story (that's P3).** P1 makes ONE exchange carry feeling and read history. Whether
  repeated exchanges build stable relationships and divergent life-histories is P3 — opened only when P1's
  claim holds.

---

## 3. THE P1 CLAIM (S35 — the exit test, a claim not completion)

**P1 is done — and only done — when both are demonstrable in a two-agent encounter:**
1. **Feeling crosses:** A's emotional display measurably moves B's affective/substrate state through B's
   perception — and a *masked* display (A suppressing/deceiving) moves B differently depending on whether B's
   vigilance reads the leakage. **The affective band of the exchange is live and honest.**
2. **History shapes the read:** the SAME encounter produces a different appraisal in B toward someone B has a
   recorded warm vs harsh history with. **The record feeds back.**

**Both emergent from the two substrates. When both hold, P1 closes and P2 opens** (P2 = deepen the
record-feedback into genuine development — the memory not just colouring one appraisal but shaping trajectory).

---

## 4. WHY THIS IS THE RIGHT FIRST PASS (top-down, whole-loop)
- It makes the **whole loop** more faithful, not one arc deeper: the exchange now carries feeling (ARC3↔ARC1)
  AND the record now shapes perception (ARC4↔ARC2) — **two arcs of the loop upgraded in one pass, which is the
  breadth-first discipline you asked for.**
- It connects pieces that **already exist** (L7 display, `IN-CONSPEC`, `rel`, memory) — **low risk, no rabbit
  hole, no new substrate.**
- It directly enables the study: **the masked-display / read-or-missed-leakage exchange is the CU phenomenon**,
  and it now runs between two agents rather than being a single-agent read-out.
- It is the honest first turn of the crank: the loop was closed but hollow (carried acts, not feeling; recorded
  but didn't remember). **P1 makes it carry feeling and remember. That is the "great exchange mechanism"
  becoming real.**

---

## 5. HANDOFF
**P1 is locked. The build session's first move is the same discipline as always — diagnose before building:
confirm in code (a) exactly where the channel drops the affect band (it carries `act`, not A's display) and
(b) exactly where `perceive` could read `rel`/memory — then wire the two bands, keeping every response
emergent.**

**This needs no ruling from me to start the diagnosis; it needs the scope above, which is now fixed. When the
build session has the two insertion points, I'll confirm them against the seams and we build Change A then
Change B, test the P1 claim, and turn the crank.**

> **The architecture is locked (the four-arc loop). The forward plan is top-down fidelity passes. P1 is the
> first: make the exchange carry feeling and read history — the two smallest changes that turn a wired-but-
> hollow loop into the living exchange the model exists to show. The behaviour emerges; we only connect the
> bands.**

# Covering instruction — P1, and the architecture reset
### Paste this ahead of the two documents. It tells you how to use them.

**Two documents accompany this. They play DIFFERENT roles — read this first so you use each correctly.**

---

## The two documents

1. **`PsychSim_Locked_Architecture.md` — STANDING CONTEXT, not a task.**
   This resets the project's frame. The layer-ladder (D2–D7 as cognitive rungs) is RETIRED as an architecture;
   it was a build-order for the substrate, and the substrate is built. **The model is a four-arc coupled
   body-brain loop that records** (perception-in → brain → expression-out → the record, coupled between agents
   through the world). D6/D7 = the brain arc, done and hardened; its leftovers are the ARC-2 backlog. **Read
   this once to reset your model of what we're building. It does not get "done" — it is the frame every future
   pass is checked against.** The forward plan is top-down whole-loop fidelity passes (P1, P2, …), NOT more
   substrate descent.

2. **`PsychSim_P1_Locked_Scope.md` — THE WORK ORDER.**
   This is what you execute. It is scoped, fixed, and grounded in the confirmed seams. Everything below refers
   to it.

---

## What P1 is, in one line
**The exchange between two agents already CLOSES (converse/_one_turn is wired end to end), but it carries the
ACT LABEL not the FEELING, and perception does NOT read the relationship record. P1 fixes exactly those two
gaps — nothing else.**

## Your first move: DIAGNOSE, don't build (the usual discipline)
Before writing anything, confirm the two insertion points in code and report them:
- **(A) where the channel drops the affect band** — `_one_turn` sends `act_from_behaviour(resp.behaviour, …)`
  through `SpeechChannel.exchange()`; it carries the act, not A's displayed affective state. Find exactly where
  A's L7 display/affect could be attached to what crosses, and where B's `perceive` folds it in via
  `IN-CONSPEC`.
- **(B) where `perceive` could read the record** — `Person.perceive()` builds the appraisal from institutional
  climate + body needs + the directed event; it never reads `rel(self, other)` or the mind's memory of this
  other. Find exactly where the relationship record could colour the appraisal.

**Report both insertion points. The reviewer confirms them against the seams before you build.** (This is the
diagnose-before-build rule that has caught every rabbit hole so far.)

## Then build, in this order
1. **Change A — the exchange carries affect.** The channel carries A's displayed affective state (from L7's
   expression, not invented) alongside the act; B's `perceive` folds it into the appraisal via `IN-CONSPEC`.
   **Subject to L7's two-pathway honesty: a masked/deceptive display leaks, and B's vigilance reads it or
   misses it — extend the act-band deception model you ALREADY have to the affect band.**
2. **Change B — perception reads the record.** `perceive` reads `rel(self, other)`/memory and lets history
   colour the appraisal (warm history → higher `social_valence`; harm → higher `threat`/lower trust).

## The guardrail that must not be crossed
**Wire what B PERCEIVES; never script what B DOES.** Both changes connect the input bands (A's feeling, the
shared history) into B's appraisal. B's act still falls out of B's substrate, emergent. **If you find yourself
writing a rule for how B should respond, stop — that is the honesty wall, and P1 does not touch it.** No new
circuits either; P1 is coupling work in `sim_world`/the channel using existing pieces (L7 display,
`IN-CONSPEC`, `rel`, memory). If a specific missing circuit surfaces, register it to the ARC-2 backlog and
draw it only if P1's claim needs it.

## When P1 is DONE (and when to hold)
**P1 closes — and only closes — when BOTH are demonstrable in a two-agent encounter, both emergent:**
1. **Feeling crosses:** A's emotional display measurably moves B's substrate state through B's perception, AND
   a masked display moves B differently depending on whether B's vigilance reads the leakage.
2. **History shapes the read:** the SAME encounter produces a different appraisal in B toward someone B has a
   recorded warm vs harsh history with.

**When both hold, P1 is done — HOLD and report to the reviewer. Do NOT roll on into P2** (deepening the
record-feedback into genuine development). P2 opens only after the reviewer confirms P1's claim. **The
progression rule: a pass opens when the previous pass's claim is demonstrated — not before, and one pass at a
time.**

## Where to hold for a ruling (vs proceed)
- **Proceed without a ruling:** the diagnosis (insertion points), and — once the reviewer confirms them —
  Changes A and B as scoped.
- **Hold for a ruling:** if the affect band can't attach without a design choice (e.g. what dimension of A's
  display crosses); if reading the record needs a choice about how history maps to appraisal dimensions; if any
  new circuit seems required; or if either change threatens to script B's response. **When in doubt, surface it
  — the reviewer rules, you build.**

---

**Summary: read the architecture doc to reset the frame; execute the P1 scope doc. First diagnose the two
insertion points and report. Then wire affect-across and record-into-perception, keeping every response
emergent. P1 is done when feeling crosses and history shapes the read — then hold for the reviewer. One pass at
a time; the loop gets more faithful each turn.**

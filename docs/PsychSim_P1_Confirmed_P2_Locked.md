# P1 CONFIRMED. P2 LOCKED — the record shapes development.

**I verified the P1 claim against the code, not the report. It holds, and the honesty wall is intact. One
finding from the build needs registering (not fixing). Then P2 is locked below.**

---

## 1. P1 confirmed — verified, not accepted

- **Change A landed as ruled:** `displayed_affect` rides the `SpeechAct`; `perceive_affect` is a *separate*
  vigilance roll (`0.15 + 0.55·vigilance + 0.15·|affect|`) from the act's deception roll; `appraisal_from_act`
  folds the affect band **only if `affect_seen`**. The act/affect dissociation is real and seeded.
- **Change B landed as ruled:** `perceive(partner_rel=…)` reads `rel`, `affect → social_valence` additively
  (`+ affect·0.5·w`), `trust → threat` via `(1−trust)·0.3·w`, and **`familiarity` gates the whole read
  (`w = clamp(familiarity)`)** so a stranger (familiarity 0) is uncoloured — the trust-0→max-threat trap is
  closed exactly as ruled. Source is `rel`, not the retired `prime()`.
- **★ The honesty check — the one that matters at a pass boundary — passes:** `appraisal_from_act` builds
  **only the Appraisal the receiver is run on.** It sets no response, no behaviour, no act. B's reply still
  falls out of B's substrate. **We wired what B perceives; we did not script what B does. The emergence wall is
  intact.**
- **Zero regressions:** 557 tests, the same 1 authorized fail (freezing floor / S56) + 2 expected failures.
  Pure coupling, no connectome change, no regrow.

> **P1's claim holds: feeling crosses (a masked display moves the hearer differently by a dissociable roll) and
> history shapes the read (the same encounter reads differently by `rel`, and a stranger is uncoloured). Both
> emergent. P1 is CLOSED.** The loop now carries feeling and reads history — the first honest turn of the
> crank, confirmed.

---

## 2. The finding to REGISTER (not fix): the expression apparatus is ASYMMETRIC

**The build surfaced something real, and it's more than an operational note:**

> **The substrate produces a DISTRESS/HOSTILITY display but NO WARMTH display. `displayed_affect ≤ 0` always;
> the positive branch (warmth → raising the hearer's `social_valence`) is coded but LATENT because there is no
> warmth/smile effector.** L7 built `NuFac`/`NuAmb-vocal`, freezing, and the two volitional routes — all of
> which express negative/distress affect. **The smile has no effector.**

**Why this is a finding and not just a gap:**
- **The expression aperture is currently half-built** — agents can show that they are distressed or hostile,
  but cannot show warmth. **Every positive exchange is therefore mute on the affect band.** Two agents who feel
  warmly toward each other cannot yet SHOW it — the warmth lives only in the `rel` record (Change B), never
  crosses the channel (Change A).
- **This matters for the study directly.** Prosocial bonding, the Duchenne smile, the warmth signal that builds
  relationships — these are exactly the affiliative displays a CU/sophropathy model needs, because their
  ABSENCE or INSTRUMENTAL USE is diagnostic. **A model where warmth cannot be displayed cannot yet show the
  sophropath's *deployed* warmth (charm as a mask) vs the ordinary person's *felt* warmth.** The masked-affect
  machinery (A4) is built and waiting, but it can currently only mask distress, not deploy warmth.

**RULING: register the warmth-display effector as a real ARC-3 gap** (the affiliative/Duchenne display —
likely a periaqueductal/hypothalamic-to-facial affiliative route, grounded when opened). **Do NOT build it in
P1 — correctly deferred; it is a new circuit.** But it is NOT mere backlog dust: **it is the highest-value ARC-3
fidelity item, because the warmth band is half of the exchange and the whole of the prosocial/charm signal.**
It will be a natural P-pass of its own (an expression-fidelity pass), and it should be flagged as study-relevant
now so the CU work knows the warmth band is currently latent.

> This is the branch's pattern one more time, in the loop instead of the substrate: **building the coupling
> revealed that one side of the aperture (negative affect) is wired and the other (warmth) is not — invisible
> until the exchange tried to carry it.** The scaffold (distress-only expression) was hiding the asymmetry;
> connecting the band exposed it. Register it; the honest exchange needs both valences.

---

## 3. P2 — LOCKED: the record shapes DEVELOPMENT (not just one appraisal)

**P1 made the record COLOUR a single encounter. P2 makes the record ACCUMULATE and SHAPE THE PERSON over
time.** This is the ARC-4→ARC-2 feedback deepened from a read into genuine development — the difference between
"an agent appraises a friend differently" (P1, done) and "an agent BECOMES someone through the history of who
it has met" (P2).

### The gap P2 closes
Right now `rel` is READ by `perceive` (P1) — but how is `rel` WRITTEN? P2's precondition is to confirm the
write side: **does the outcome of each exchange UPDATE `rel` (affect/trust/familiarity), such that a history of
warm exchanges builds trust and a history of harm erodes it — and does that accumulated `rel` then feed the
next encounter (via P1's read)?** If the write side is thin or scripted, P2 builds it: **the relationship
record must be shaped BY the exchanges, emergently, so that trajectory diverges by history.**

### P2 scope (to be fixed exactly after the write-side diagnosis, same as P1)
1. **The record updates from outcomes:** after an exchange, `rel(a,b)` moves as a function of what happened —
   warmth reciprocated raises affect/trust/familiarity; hostility or caught deception erodes them. **Emergent
   from the exchange outcome, not a scripted increment.**
2. **The accumulated record shapes trajectory:** because P1 already reads `rel` into appraisal, a written-by-
   history `rel` means **an agent's future appraisals — and therefore its emergent behaviour — diverge by its
   relational history.** Two agents with identical substrates but different histories behave differently. **That
   divergence is development, and it must EMERGE from the accumulated record, never be assigned.**

### The P2 claim (S35 — the exit test)
**P2 closes when, over repeated exchanges, an agent's behaviour toward a specific other DIVERGES as a function
of their accumulated history — and that divergence emerges from the record being written by outcomes and read
by perception, with no scripted trajectory.** Concretely: run two agents through a series of warm exchanges and
another pair through hostile ones; the warm pair should develop trust/affiliative appraisal and the hostile
pair suspicion/threat appraisal, **and the difference should trace entirely to the accumulated `rel`, not to
any coded divergence.**

### The guardrail (unchanged)
**Wire what gets RECORDED and how the record is READ — never script the trajectory.** The write rule maps
outcomes to `rel` changes; the read (P1) maps `rel` to appraisal; the behaviour still emerges. **If P2 finds
itself assigning a developmental path rather than letting one accumulate, stop — that's the honesty wall.**

### Why P2 is the right next turn (top-down, whole-loop)
- It upgrades the SAME arc P1 touched (ARC-4↔ARC-2) from a read to a full read-write loop — **the record now
  both shapes and is shaped, which is the minimal closure of development.**
- It uses existing pieces (`rel`, the exchange outcome, P1's read) — **coupling work, no new substrate**, same
  low-risk profile as P1.
- It is the precondition for P3 (relationships and life-histories accumulating across a population): you cannot
  have divergent life-histories until a single relationship can be shaped by its own exchanges. **P2 is that
  single-dyad development; P3 scales it to the population.**

---

## 4. HANDOFF
**P1 is confirmed closed. P2 is locked in scope above. The build session's first P2 move is the same
discipline: DIAGNOSE the write side — where and how is `rel` currently updated by an exchange outcome? — and
report before building.** Then P2 builds the two halves (record-written-by-outcome, trajectory-shaped-by-record),
tests the P2 claim, and holds.

**One register add now (no build): the warmth-display effector as the highest-value ARC-3 gap, study-flagged
(warmth band latent; charm-as-mask not yet expressible).**

> **The loop carries feeling and reads history (P1, done). Next it learns to be SHAPED by that history over time
> (P2). Each pass, the whole loop more faithful. The behaviour emerges; we only wire what crosses and what
> records. Turn the crank.**

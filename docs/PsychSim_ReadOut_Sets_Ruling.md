# The six read-out sets — RULING. **Your principle is right; the verification changes the answer. CEl comes
# out of the felt sets.**

**The double-gain fix and the two output-set re-derivations are unambiguous. On the felt-set question — you
were right not to touch it unilaterally, and your reasoning is sound in principle. But I verified CEl's
post-un-lumping wiring, and it is no longer the node your reasoning describes.**

---

## 1. Confirmed without change

- **The double-gain:** `observer.py:134` → read `activity(c)`. The throttle already shaped development;
  re-applying `_gain(c)` counts it twice. **Build it.** ✓
- **`DEFENSIVE_OUTPUT` → `(CEm-freeze, CEm-active, vlPAG, dPAG, HYPdm)`** — the actual output stage, CEl (the
  input selector) and BA (a relay) removed. ✓ Matches the audit's explicit direction.
- **`_OBS_AGGRESS` → `(VMHvl, CEm-active, dPAG, HYPdm)`** — VMHvl (the attack locus the seed itself calls
  necessary-and-sufficient) added, CEl (which SUPPRESSES attack) removed. ✓ This corrects a measure that was
  anti-correlated with its own signal.

## 2. ★ The felt-set question — your principle is right, but CEl is no longer a registration node

**Your reasoning is correct as stated: affective empathy is FELT distress (Blair's aversive-response-to-distress
— the limbic/input response, not a motor act), and replacing CEl with output populations would make an empathy
measure read a defensive motor act. That would be wrong, and you were right to refuse it.**

**But the verification shows CEl is no longer the node that reasoning assumes:**

```
CEl-SOM   -> CEl : GABA-A, strong
CEl-PKCd  -> CEl : GABA-A, strong          ← ALL THREE selector populations inhibit CEl
CEl-CRF   -> CEl : GABA-A, strong
CEl efferents: CEl-SOM, CEl-PKCd, CEl-CRF   (only the selector populations)
```

> **★ CEl's activity is NOT registration. It is registration MINUS selector feedback. All three selector
> populations project back onto it with strong GABA-A inhibition, and its only efferents are to those same
> populations. So an agent that selects a defensive mode STRONGLY shows LOWER CEl activity — which means a
> felt-empathy or felt-threat construct reading CEl partly reads the INVERSE of selection strength. The agent
> that mounts the strongest defensive response would read as LESS empathic, not because it feels less, but
> because its own selector inhibits the registration node.**

**This is a construct-validity defect of exactly the audit's shape — a set whose activity is driven by something
other than what the construct names — and it is NEWLY INTRODUCED BY THE UN-LUMPING.** Pre-split CeA had no such
internal feedback, so CEl inheriting CeA's registration role was defensible when the sets were written and is
not defensible now. **The un-lumping changed what the node measures.**

**RULING: drop CEl from all four felt sets.** And the replacement requires no new nodes — **the felt/limbic core
is already present in every one of them:**
- `AFFECTIVE_EMPATHY` → **(LA, BA, MeA, aIns)** — basolateral complex + social + interoceptive. The felt-distress
  core, uncontaminated.
- `_OBS_EMPATHY` → **(LA, BA, aIns)**
- `_OBS_THREAT` → **(BA, LA, …)** — see §3 on vlPAG
- `_SELF_THREAT` → **(BA, aIns, …)** — see §3 on vlPAG

## 3. The question you didn't ask, same class — vlPAG in the two threat sets

**`_OBS_THREAT` and `_SELF_THREAT` both contain `vlPAG`, and vlPAG's efferents are `NRA` and `Mc` — it is a
MOTOR OUTPUT (the freezing effector), sitting in a felt-state set.** The audit flagged it as *dead*; now that
`PL→vlPAG` has made it live, the question is whether it belongs at all.

**By your own principle — felt states read the registration/limbic side, motor nodes belong in output
constructs — vlPAG should come out.** But "felt threat" is arguably more integrated than "felt distress" (a
threat state plausibly includes defensive mobilisation in a way empathy does not). **RULING: state which. If
`_OBS_THREAT`/`_SELF_THREAT` are meant as felt/registered threat, drop vlPAG for the same reason as CEl. If they
are meant as integrated threat-state including defensive mobilisation, keep it and say so in the set's
docstring — but then they are not purely "felt" sets and should not be described as such.** Either is
defensible; leaving it undecided is not.

## 4. ★ The change must be MEASURED and REPORTED, not absorbed

**`AFFECTIVE_EMPATHY` is the CU study's primary instrument, and it is changing.** So:

> **Measure the construct scores BEFORE and AFTER the set re-derivation and the double-gain removal, and report
> the direction and magnitude.** The S18 expectation is that they DEFLATE — the double-gain was inflating them
> by counting the throttle twice, and dropping CEl removes a selector-contaminated term. **A change to the
> study's primary instrument must be reported as a re-measurement with its own before/after, not silently
> absorbed into a green suite.** If any construct-level finding depends on the old sets, it needs restating
> against the new ones — which is precisely what the audit ruling meant by "re-verify the emergent findings on
> corrected instruments."

---

## 5. Handoff

**Build: the double-gain removal (`activity(c)`), the two output-set re-derivations as you proposed, and drop
CEl from all four felt sets (the LA/BA/MeA/aIns core is already present — no new nodes). State the vlPAG
decision for the two threat sets and apply it. Gate all three changes together with the harsh-mirror routes, as
planned — one cycle.**

**Then measure and report: construct scores before/after, direction and magnitude, and which construct-level
findings need restating against the corrected instrument. Expect deflation.**

> **Your principle was right and your refusal to touch the felt sets unilaterally was right — an empathy
> measure must read felt distress, not a defensive motor act. But the un-lumping changed what CEl measures: all
> three selector populations now inhibit it, so its activity is registration minus selection, and a felt
> construct reading it would partly read the inverse of defensive selection strength. That is the audit's own
> failure shape, newly created by our own fix. Drop CEl from the four felt sets — the LA/BA/MeA/aIns core is
> already there — decide vlPAG's status in the two threat sets on the same principle, remove the double-gain,
> and then MEASURE what the corrected instrument does to the study's primary constructs. The instrument is
> being made honest; the numbers it produces must be re-reported, not inherited.**

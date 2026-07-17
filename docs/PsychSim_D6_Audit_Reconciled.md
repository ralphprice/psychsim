# D6 audit — RECONCILED (both halves)

---

## 1. The enumeration: **58 is right. 49 was mine, and it was wrong.**

I read the current function instead of remembering it:

```python
def throttleable_circuits(model=None):
    # v14 (ruled): `structural_element` circuits are DELIBERATELY NOT excluded here...
    return sorted(cid for cid, c in m.circuits.items() if c.domain in _THROTTLEABLE_DOMAINS)
```

**No exclusion — exactly per my own §1b ruling.** My 49 was computed with `and not c.structural_element`:
**the exclusion I personally ruled should be removed, one commit after you removed it at my instruction.**
49 + the 9 gates (affiliation 1, defensive_threat 6, executive 2) = **58.** Your number, your table's baseline.
**Reconciliation item #1 closed against me.**

### ★ And that is the fifth of the same error — which makes it a pattern, not a slip
`source: None` · `structural_element_basis` · `plasticity_schedule` · `COGNITIVE_MENTALIZING` · now
`throttleable_circuits()`. **Every one: I queried a version I remembered instead of the one that exists.** And
the structural reason is worth recording, because it will not go away:

> **The reviewer's memory of the code freezes at his last read, and this codebase changes every commit —
> often at his own instruction. So the reviewer's recollection goes stale IN PROPORTION TO HOW EFFECTIVE HIS
> RULINGS ARE.** The more I rule, the further my picture drifts from the thing I audit. **That is the
> reviewer-side analogue of "the build session cannot certify its own work."**

> **RULE — record it: when the two halves of a dual audit disagree on a COUNT, the prior is that the REVIEWER
> is stale.** You run the code; I remember it. **Reconcile by reading the file, not by arguing.** And a
> reviewer's half must be computed mechanically from the file — never from recollection. I wrote "an audit
> performed from memory is not an audit" and then did it twice more in the same pass.

---

## 2. My half's findings — outstanding, not yet reconciled with yours

**(a) ★ THREAT → `LC` resurrects the artifact the LC arc killed.** Follow your own finding one step further:
`seed_substrate` applies the dial **to every agent at seed time**; **low threat IS the CU temperament**;
therefore **every CU agent is born with a throttled teaching signal.** The LC arc killed the punishment
"signature" in the **read-out**. **The dial brings it back through the SEED — before the first tick.**

**(b) The diagnosis demotes a registered item.** The dial reaches `LC` because **`LC` is two things** — the
arousal/gain system (a legitimate temperament dimension) *and* the teaching signal (not one). A
domain-uniform scalar cannot separate them. **Third instance of one defect: the dial is a DOMAIN-UNIFORM
SCALAR over a FUNCTIONALLY HETEROGENEOUS domain.** So the registered "reactivity/regulation fusion" **is not
an item — it is an instance.** The item is: **the temperament model must be per-function, not per-domain.**

**(c) ★ `DEFENSIVE_OUTPUT`: the split did not REVEAL the hollow — it CREATED it in the read-out.** Your own
source comment is the evidence: `# v14 Phase A: PAG split -> vlPAG (conditioned freezing / passive coping)`.
Before the split it read the lumped `PAG` — **alive, but conflating freezing with flight.** After, it reads
`vlPAG` — **correctly named, and dead.** **So the defensive read-out has never measured conditioned freezing:
before it read a lump, now it reads a corpse.** Two consequences: **defensive results across the split are not
comparable**, and **the read-out is correct while the substrate is incomplete** — so **do not re-point
`DEFENSIVE_OUTPUT` to a live node to restore the measure. Give `vlPAG` its drive.**

**(d) Correction: "LC is the teaching signal for all DA-gated learning" — `LC` is NORADRENERGIC.** The DA gate
is `VTA`. The entailment covers the **NA-gated** control edges (`dmPFC→LA`, `vlPFC→ITC`), **not** the DA-gated
one (`vmPFC→ITC`). **The `ENTAILED` verdict stands; its scope is narrower than the table states.** An audit
that overstates its own finding mis-scopes the fix.

---

## 3. The six new surfaces — accepted, with three additions

**(a) ★ The #2 entailment has THREE doors, not two.** The manipulation contains `CeA` → `LC`'s sole afferent ·
**the scan's search target maximises exactly that throttle** · **and the temperament dial reaches `LC`
directly.** **This is not three items. It is one defect with three entrances — and a fix that closes one
closes none.** Whatever the resolution is, it must be tested against all three.

**(b) ★ `DEGENERATE` is a new verdict class, and it is a LUMPING artifact — the ninth instance.**
`energy ≡ hydration` (both `NTS`), `respiratory ≡ −thermal` (both `PBN`). **Not two constructs in one set —
two names for one number.** Sharper than `CONFLATED`, and the cause is familiar: **`NTS` is one node standing
for a nucleus that genuinely carries energy *and* hydration**, so no read-out can pull two independent
variables out of it.

> **Count the lumps: `PAG` · `NuAmb` · `dPAG` (dl+l) · `dACC` (cognitive+motor) · `NuFac` (upper+lower) ·
> `PMC-l` (suppress+produce) · `NuAmb-vocal` (cry+speech) · `NTS` (energy+hydration) · `PBN`
> (respiratory+thermal). NINE. Lumping is this substrate's characteristic defect — and you have now found it
> from a completely independent direction: the READ-OUTS.** That is a strong independent confirmation of what
> the 209-edge audit will look like, and it should be recorded as such: **the audit's WRONG-TARGET /
> MISSING-ELEMENT categories will be dominated by lumped nodes, and now we have evidence rather than a
> prediction.**

**(c) The triplicate is NOT a DRY smell — it is a live hazard by this project's own discipline.**
`_OBS_REWARD` / `_SELF_REWARD` / `REWARD_READOUT` are **three curated lists where the project has already
ruled there should be one derivation** — `structural_element` was made *derived, not curated*, precisely
because "a curated list drifts." **Three copies of a set drift silently, and the audit only catches it if all
three are enumerated.** `CLEAN` today; register the divergence hazard.

**(d) Record the propagation rule you stated — it is a rule, not an observation:** *"a construct is only as
valid as the set it reads."* **Every verdict propagates upward through every derived construct.** So the
audit's table is not a list of defects; **it is a list of roots**, and `aggression_profile` is the first
demonstration.

**(e) And note the reach:** the domain-mean `INCOMMENSURATE` feeds **the golden AND the UI**. So the number
that moves against its name **is on screen**. That is not an internal defect; it is a presented one.

---

## 4. Reconciled. The ruling order.
1. ~~The enumeration~~ — **closed: 58.**
2. **The #2 entailment**, scoped to NA-gated learning, **and tested against all three doors.**
3. **`vlPAG`'s drive** — it resolves `DEFENSIVE_OUTPUT`, `_OBS_THREAT`, `_SELF_THREAT` at once, and it is a
   substrate fix, not a read-out edit.
4. The temperament model, per-function not per-domain.
5. The rest of the table, verdict by verdict.

**Nothing edited. Fix the mechanism, not the measure.**

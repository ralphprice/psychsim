# `dACC-GABA` — the three decisions

**Hold confirmed against the remote: 89 circuits, no `dACC-GABA`, nothing pushed. This rules on the
reasoning, not on verified code — I verify after the commit.**

---

## 0. ★ The grounding is the finding, and it corrects my ruling

I said *"rate grounded from cortical FS/PV electrophysiology."* **You went to the electrophysiology and it
said the premise was wrong: cortical PV⁺ fast-spiking interneurons are not autonomous pacemakers — their
no-input rate is ~0, and the high in-vivo rate is synaptically driven.** So there is **no rate to ground**,
and forcing one would have invented a pacemaker the biology does not have.

**You did not force it. That is the fourth time this arc a ruling's premise has been checked and found
wrong, and every one of them made the build more honest.**

**Verified against the remote — the taxonomy is already in the seed, and your call is byte-consistent with
its twins:**

| gate | baseline | setpoint | class |
|---|---|---|---|
| `LC` | **0.15** | **0.15** | **pacemaker** — fires under synaptic blockade; grounded rate; **paired deviant** |
| `dPAG-GABA` | **0.19** | **0.19** | **pacemaker** — same |
| `dlPFC-GABA` | 0.05 | 0.1 | **recurrent E-I** — scaffold baseline |
| `vmPFC-GABA` | 0.05 | 0.1 | **recurrent E-I** — scaffold baseline |
| `dACC-GABA` | *0.05* | *0.1* | **recurrent E-I** — correct, and correctly **not** a setpoint deviant |

> **THE GATE TAXONOMY — record it; it governs the eight still to come.**
> **Pacemaker gates** (`LC`, `dPAG-GABA`): an intrinsic rate exists → ground it → paired setpoint deviant.
> **Recurrent E-I gates** (the cortical interneurons): **no intrinsic rate exists** → **the grounded content
> is the LOOP, not the rate** → baseline stays scaffold. **Do not force a rate onto an E-I gate. When we build
> the remaining eight, this is the default, not the exception.**

> **And it refines principle 6.** "Ground a value only where it is groundable in isolation" assumed the thing
> to ground is a *value*. **Sometimes what is groundable in isolation is a RELATION, not a value — and then
> the honest move is to ground the relation and leave the value scaffold.** `dACC-GABA` grounds a topology
> (Ferguson & Gao's recurrent E-I loop) and declares its rate scaffold. **That is more honest than a grounded
> number would have been.**

**And the silence test carries it (principle 1): the loop pulls `dlPFC` off 1.000 to 0.858; lesion the gate
and it runs hot again.** Demonstrated, not assumed. ✅

---

## 1. Executive engagement — the condition is met, but the fix is not what the test thinks

**My condition was *"if it still conflates once the brake is in, re-express it."* It is met. But re-expressing
it would be fixing the wrong thing, and your own evidence is why:**

> *"Even control-only (dlPFC+OFC) is warm<harsh, because `dACC` conflict-monitoring correctly rises under
> harsh and drives `dlPFC`."*

**Removing `dACC` from the read-out does not help, because `dACC → dlPFC` is real anatomy carrying a real
function: conflict monitoring RECRUITS control** (Botvinick's conflict-monitoring model — canonical, and the
edge is in the seed). **So a harsh, unpredictable environment produces more conflict → more monitoring → more
control recruitment. `warm < harsh` for ENGAGEMENT is CORRECT. The substrate is right and the test is
wrong.**

**The test wants CAPACITY. Capacity is not a small variant of engagement — it is a different construct, and
no measure of it exists.** And the literature says the model should eventually show **both**: adversity
raises engagement *and* lowers capacity. **We are now measuring the first honestly and not measuring the
second at all.**

**RULING: do not "fix" the engagement measure — it works. Register the capacity measure as its own construct
pass, with the design constraint named:**

> **Capacity must be probed at MATCHED DEMAND** — present the same challenge to warm- and harsh-reared
> agents and measure the control exerted. **A passive read-out of executive activation can never separate
> capacity from demand; it will conflate them by construction, whatever set it sums.**

**This is the READ-OUT AUDIT's first real case, and the phase produced two: `DEFENSIVE_OUTPUT` resting on 2
of 3 terms, and this one conflating two constructs.** The read-out audit is no longer a hypothetical.

---

## 2. ★ The earned negative — **HOLD. Do not retire it.** Here is the quantified reason.

**Not because the result is false. Because we cannot yet tell, and the direction of the unknown is known.**

- **One brake removed 29 % of it** (0.0755 → 0.0534).
- **The margin is 7 %** (0.0534 vs 0.05).
- **Eight more cortical brakes are missing.**
- **And this brake's own strength is SCAFFOLD** — baseline 0.05, setpoint 0.1, unpaired, exactly like its
  twins. **So the 29 % it removed is itself a scaffold quantity.**

> **A 7 % margin sits inside two unquantified sources of error, both of which the substrate's own §18 caution
> says point upward: eight absent brakes, and a scaffold brake strength. One brake removed four times the
> margin.**

**RULING: mark it `xfail` with the reason and a NAMED RESOLUTION CONDITION — re-measure when the cortical
brake layer is complete.** Do not touch the threshold. Do not retire the finding.

> **An xfail carrying a resolution condition is a disclosed limitation — the audit's UNGROUNDED-BUT-UNRESOLVED
> pattern, applied to a test. An xfail without one is a permanent lie with a green tick over it.** Put the
> condition in the test, not the commit message.

**And record what this now is: the divergence is a small, stable, well-posed structural value of 0.0534 that
emerged from a grounded edge and survived a grounded brake.** That is not nothing. **It may be real. It is
not yet a finding, and it must not become one by attrition.**

---

## 3. The golden — regenerate, with the reason

Mechanical. **The pin did its job: it moved because a real brake changed real dynamics, and the silence test
already demonstrated the mechanism.** Regenerate; record the reason (`dACC-GABA`'s recurrent E-I loop pulls
`dlPFC` off the ceiling — expected, demonstrated, not tuned) in the commit and in the test.

---

## Then commit and push
`dACC-GABA` (scaffold baseline, loop grounded, `structural_element`, scan-lesionable, temperament-excluded) ·
executive-engagement **left red or xfailed with the construct reason** — your call which, but the reason must
be recorded either way · earned negative **xfailed with its resolution condition** · golden regenerated with
its reason. **`BA → dACC`'s band untouched. Nothing tuned. I verify after the push.**

**Registered this pass:** the gate taxonomy (governs the remaining eight) · principle 6's refinement
(relations vs values) · the cortical brake layer at 3 of 11 · the capacity measure at matched demand · the
read-out audit (two live cases) · the divergence at 0.0534 pending the brake layer.

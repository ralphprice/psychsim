# Phase B — RESPEC RULING (the diagnostic stands; the spec was wrong)

**You checked the premise of my grounding question and the premise was false. That is the whole point of the
step, and it is the second time this arc that diagnosing first has killed a spec before it became a commit.**
Nothing built — correct.

---

## 1. VERIFIED — and the sources give three things nobody asked for

**Confirmed, overwhelmingly:** *"The PAG uses the nucleus retroambiguus (NRA) as a relay to excite the
vocalization muscle motoneurons"* (Boers/Holstege 2002). *"The NRA projects directly to the laryngeal and
pharyngeal motoneurons in the nucleus ambiguus"* (Holstege 1989; Boers 2002). **And it is NECESSARY, by
lesion: bilateral kainic acid into NRA ABOLISHED PAG-induced vocalisation** — the same shape of proof as
silencing the dPAG gate. **My spec would have wired a monosynaptic projection that does not exist.**

### 1a. 🎁 NRA's afferent set is CLOSED — and that is a gift
> *"the NRA receives strong projections from the lateral, ventrolateral, and to a lesser extent the
> dorsomedial part of the caudal midbrain PAG (Holstege, 1989), **but not from any other suprapontine brain
> structure** (Holstege, 1991)."*

**Above the pons, the PAG is NRA's only input.** We rarely get a closed afferent set. It also means **no
cortical route reaches NRA** — which matters for §1b.

### 1b. ★ The DUAL PATHWAY is explicit in the vocal domain — Phase D is now grounded
> *"They generate vocalization by activating the **prefrontal-PAG-NRA-motoneuronal pathway**, and, at the
> same time, they modulate this vocalization into words and sentences by activating the **cortico-bulbar
> fibers to the face, mouth, tongue, larynx and pharynx motoneurons**."*

**Two routes to the same motoneurons, stated in one sentence.** The volitional route **bypasses PAG and NRA
entirely** and lands on the motoneuron pools directly. So `NuAmb-vocal` and `NuFac` are **both** convergence
points — emotional via PAG→NRA, volitional via cortico-bulbar. **Phase D wires to the motoneurons, not into
the PAG limb.** Register; do not build.

### 1c. ⚠️ NRA does NOT answer the whole respiratory limb
> *"PAG-induced inspiratory excitation remained even after the injections… **an additional pathway from the
> PAG to respiratory motoneurons other than through the NRA** is important for mediating PAG-induced
> inspiratory activation."*

**NRA carries the expiratory/vocal drive; inspiration has a separate PAG route.** Your "one node answers two
items" is *half* right — take the half that is grounded, and **disclose the inspiratory route as
unmodelled.** Do not stretch NRA to cover it.

---

## 2. The column call — right, and here is the sub-grain it rests on

**Your method was right: you went and got the anatomy and it returned both, for a reason.** That is exactly
what "do not resolve by symmetry" was asking for.

**But the grounding is narrower than "both columns", and the disclosure has to say so.** The sources are
specific: NRA receives from **lateral, ventrolateral, and (weakly) dorsomedial** — and *"stimulatory
activation of the **lateral and ventrolateral** PAG generates vocalization"*, while **dorsolateral** produces
hyperpneic tachypnea, *not* vocalisation. **The dorsolateral column is the one column that does not
project.**

Our `dPAG` is seeded *"dorsal PAG / flight"* — i.e. Bandler's **dl** — but carries `VMHvl → dPAG` for
**attack**, which is the **lateral** column's function. **So `dPAG` is in fact the dl-l complex**, and your
reading holds. **Route `vlPAG → NRA` (unambiguous) and `dPAG → NRA` (grounded via its lateral component) —
and DISCLOSE: `dPAG` lumps dorsolateral + lateral; NRA's input is the lateral; the model cannot currently
express that the dorsolateral half does not project.**

> **REGISTER (do not act): the dl/l dissociation meets the §9 grain test — different afferents, different
> outputs, different analgesia, and now a different projection to NRA.** `dPAG` is the next split. **Not now:
> it would re-open the aggression keystone** (`VMHvl → attack` lands in the lateral column), and that is
> bigger than expression needs. Same class as the registered "anterior vlPAG". **The dorsomedial column is
> unrepresented entirely** — register that too.

---

## 3. preBötC — ❌ NOT the third gate instance, and it does NOT close the PAG-PANIC item

**Over-generalising a real pattern is its own failure mode, and this is that.** Compare:
- **`vlPAG-GABA` / `dPAG-GABA`** — a **local, tonic, autonomous** population that **sets a threshold**, and
  the behaviour is released by **disinhibition**.
- **preBötC → RAmVOC** — a **remote rhythm generator** imposing a **priority**: you cannot inhale and close
  the vocal cords at once, so inspiration wins. **Phasic, rhythmic arbitration between incompatible motor
  acts.**

**Both are inhibition. They are not the same architecture — one is a threshold, the other is a traffic
rule.** A fourth inhibitory thing is not automatically the third instance of a pattern.

**And therefore it does not answer the registered `PAG-PANIC` gate question — that item STANDS.** The escape
source names vocalisation explicitly among the behaviours *"initiated by disinhibition… of local GABAergic
circuits within the PAG."* **So PAG-PANIC should still have its own local tonic gate, AND preBötC should
gate the premotor. Two mechanisms, two places, both real.**

**SCOPE: preBötC is its own pass — the respiratory system.** It is a rhythm generator (an autonomous
pacemaker, the LC/dPAG-GABA class) and building it means building respiratory rhythm, which is a system, not
a node. **Not load-bearing for Phase C:** NRA is driven-only, so nothing leaks; the display tracks
PAG→NRA→NuAmb-vocal. What is lost is the breath rhythm — **fidelity, not floor. DISCLOSE: vocalisation is
currently un-breath-gated.**

---

## 4. `SympOut` — my error. Owned.

**You are right and the item was mine, not yours.** I took your Phase A dead-end table and added a
requirement on top of it **without asking whether the node was a hub or a terminal.** That is the reviewer
failing to check a premise — the same failure this diagnostic just caught in my Phase B spec.

**The refinement, and it is worth recording because it corrects the pattern itself:**
> **"Unefferented" needs a second question: is this a HUB or a TERMINAL?** A terminal *should* be
> unefferented — the body is not modelled as circuits. **`PAG` was a hub with no output: a real gap.
> `SympOut` is the output.**
> **`AdrenalCortex` is the exception that proves the test: it has efferents because cortisol re-enters the
> brain.** So the test is: **does the node's product return to the modelled system?** If yes, it needs
> efferents; if no, it is terminal and complete.

And your point closes it: **Gross's cost reads from `SympOut`'s activation**, exactly as Phase C reads the
expression effectors. **The item dissolves. Struck.**

---

## 5. Domain call — `NRA` → `motor_effector`, and widen the domain's stated definition

`NRA` is a **premotor interneuron pool** ("premotor interneurons with direct projections to the
motoneurons"). It is **not** a `structural_element` — it is a driven relay, not a tonic gate. It is excluded
**by domain**, and the reason is decisive:

> **`motor_effector` exists so the display is not reachable by a temperament dial. `NRA` is UPSTREAM of
> `NuAmb-vocal`. If `NRA` is dial-reachable, the display is dial-reachable *through it*, and Phase C's
> construct validity collapses through the back door — the same failure, one synapse earlier.**

**So state the domain as THE MOTOR LIMB — premotor and motoneuron pools — not "terminal effectors",** or the
next premotor node gets the wrong call for the same reason.

> **REGISTER for Phase C — a different question I have not ruled and you should not assume:** `motor_effector`
> is currently excluded from the **scan** too. By §1b's logic (lesioning is an experiment — kainic acid into
> NRA is *exactly* the experiment that proved it) that looks wrong. **But it turns on the signature set, not
> the domain: a search must not range over the nodes its own signature reads.** Once Phase C makes the display
> a read-out, that question becomes live. **The rule to test then: a scan's manipulation set and its signature
> set must be DISJOINT.** Joins the throttle-set audit — same class.

---

## 6. Build
`NRA` (motor_effector; PAG-only afferents — a closed set) · `vlPAG → NRA` · `dPAG → NRA` (disclosed) ·
`NRA → NuAmb-vocal` · `PAG-PANIC → NRA` **if grounded** — check it; PAG-PANIC is a PAG column, so the
PAG→NRA rule should cover it, but verify rather than infer · the emotional route to the face
(`dACC`/MCC → `NuFac`, Morecraft) **with citations, and resolve `dACC → PAG-PANIC`'s `assumption` basis in
the same pass — same source region, same question.**

**Registered, not built:** preBötC + respiratory rhythm (own pass; vocalisation un-breath-gated) · the
inspiratory PAG route (unmodelled) · `PAG-PANIC`'s own gate (**stands**) · the `dPAG` dl/l split · the
dorsomedial column · Phase D's cortico-bulbar route **to the motoneurons, bypassing PAG/NRA** · the
scan-vs-signature disjointness rule.

*One forward note, free: NRA is a combinatorial pool — the PAG selects which of its premotor populations
fire, giving vocalisation, vomiting, coughing, sneezing, **mating posture**, or childbirth. **So v14 Phase 5's
reproduction wiring already has its premotor node the moment you build this one** — and `VMH → vlPAG` (the
lordosis edge we routed in Phase A) is the other half of that circuit. Note it in the seed; do not build it.*

# Expression Phase B — diagnostic (NOTHING built; the spec is overturned, surfacing first)

Phase B's grounding question was answered, and **the answer invalidates the spec's premise**. Two further
findings, one of them a correction to my own Phase A diagnostic. Surfacing before building.

## 1. ★ The vocal limb does not exist as specced — the relay is MISSING
The ruling said of `vlPAG → NuAmb-vocal`: *"GROUND IT BEFORE BUILDING… do not resolve it by symmetry."*
Grounded. **The premise is wrong: the PAG does not project directly to nucleus ambiguus at all.**

> The **nucleus retroambiguus (NRA)** *"receives strong projections from the **lateral, ventrolateral**, and to
> a lesser extent the dorsomedial part of the caudal midbrain PAG"*, and *"**the NRA projects directly to the
> laryngeal and pharyngeal motoneurons in the nucleus ambiguus** in the lateral medulla."*
> — [Holstege; VanderHorst & Holstege 2000, J Comp Neurol 424:251](https://onlinelibrary.wiley.com/doi/abs/10.1002/1096-9861(20000821)424:2%3C251::AID-CNE5%3E3.0.CO;2-D)

**`NRA` is ABSENT from the model** (verified: no retroambiguus/ambiguus circuit besides the NuAmb split).
So **both** specced edges — `PAG-PANIC → NuAmb-vocal` and `vlPAG → NuAmb-vocal` — would wire a monosynaptic
projection that **does not exist**, skipping the relay. The real chain is:

**`PAG (l/vl) → NRA → NuAmb-vocal`**

**And the column question answers itself from the anatomy, not by symmetry:** NRA receives from **lateral AND
ventrolateral** (+ some dorsomedial). Our `vlPAG` *is* the ventrolateral; our `dPAG` is "dorsal/**dorsolateral**"
(Bandler's active-coping dl-**l**PAG), which carries the lateral. **So both columns project — because the
anatomy says both, not because two nodes looked symmetric.**

## 2. ★ NRA is the respiratory limb too — one node answers two Phase-B items
The ruling listed the vocal limb and *"the respiratory limb (diagnose what exists first)"* as separate items.
**Diagnosed: the respiratory substrate is essentially absent** — the only candidate is `PBN`, whose own
function field is *"Relays NTS + lamina-I spinothalamic (pain/thermal/visceral) signals to thalamus,
hypothalamus and amygdala"* — a **sensory relay, not a rhythm generator**. No preBötzinger, no RTN, no KF.

But the NRA **is** the faciorespiratory coordinator the master reference described:
- **Vocal premotor:** contains excitatory vocalisation-specific laryngeal premotor neurons (**RAmVOC**),
  *"necessary and sufficient for driving vocal-cord closure and eliciting… vocalizations"*.
- **Expiratory drive:** *"predominantly expiration-related neurons with axonal projections to motoneurons in
  the thoracic, lumbar, and upper sacral spinal cord that mediate excitatory expiratory drive to the external
  intercostal and abdominal muscles."*
- **It is where vocalisation and respiration are coordinated** — see §3.

So **`NRA` is the vocal limb and the respiratory limb in one grounded node.** ([Brainstem control of
vocalization and its coordination with respiration, *Science* 2024](https://www.science.org/doi/10.1126/science.adi8081); [The Nucleus Retroambiguus Control of Respiration, *J Neurosci* 29:3824](https://www.jneurosci.org/content/29/12/3824))

## 3. The coordination is a GATE — and it is the same architecture again
> *"RAmVOC neurons receive **inhibition from the preBötzinger complex**, and inspiration-needs **override**
> RAmVOC-mediated vocal-cord closure. Ablating inhibitory synapses in RAmVOC-neurons compromised inspiration
> gating of laryngeal adduction, resulting in **discoordination of vocalization with respiration**."*

**preBötC is also absent.** Without it, vocalisation is not respiration-gated — an agent could vocalise
through an inspiration. Note the shape: **an inhibitory gate that sets when the output may fire** — the third
instance of the architecture (`vlPAG-GABA` freezing, `dPAG-GABA` escape threshold, now preBötC→RAmVOC
vocal-respiratory gating). *"Every column has a gate"* keeps holding.

**This also refines the registered "PAG-PANIC needs its own gate" item:** the vocal gate the literature names
is not inside the PAG column at all — it is **preBötC onto the NRA premotor**. Whether `PAG-PANIC` *also*
needs a local gate is a separate question and should not be assumed from the pattern.

## 4. ⚠️ Correction to my own Phase A diagnostic: `SympOut` is NOT the same dead-end class
I classified `SympOut` with `PAG`/`PAG-PANIC`/`NuAmb` as "unefferented"; the ruling carried that forward
(*"complete its efferent. Same finding, same class"*). **That classification was mine and it was wrong.**

| circuit | function | out |
|---|---|---|
| `SympOut` | *"Sympathetic **effector** ('fight-flight'): cardiac, vascular, metabolic, adrenal"* | 0 |
| `NuAmb-cardiac` | *"Parasympathetic CARDIAC **outflow**"* | 0 |
| `DMV` | *"Parasympathetic visceral **outflow**"* | 0 |
| `AdrenalCortex` | HPA effector — **its product (cortisol) re-enters the brain** | 4 |

**The autonomic effectors are terminal by design**: their target is the **body**, which is not modelled as
circuits. Only the one whose product re-enters the brain has efferents. `PAG` was a **hub** with no output —
a real gap. `SympOut` **is** the output. Its 0-out is correct, not a dead end.

**And the Phase-D purpose still works:** Gross's suppression cost is *expression falls while autonomic arousal
rises* — that is **read from `SympOut`'s activation**, exactly as Phase C reads the expression effectors.
`NuFac`/`NuAmb-vocal` will be terminal too (their target is muscle). **The effector layer is read, not
traversed.** Nothing to build here; the item dissolves.

## 5. What Phase B actually requires (for the ruling — nothing built)
- **ADD `NRA`** — the vocal/expiratory premotor relay. **New circuit** (`motor_effector`? or a premotor
  domain? — it is premotor, not an effector; it is also not a reactivity dial). *A domain call I will not
  make alone, given §2a's lesson.*
- `vlPAG → NRA` **and** `dPAG → NRA` — both, grounded (lateral + ventrolateral), not symmetry.
- `NRA → NuAmb-vocal` — the laryngeal/pharyngeal motoneurons.
- **`PAG-PANIC → NRA`?** — *inference, not citation.* All vocalisation routes through NRA, and PAG-PANIC is
  our self-declared vocalisation column, so its cry must reach the larynx somehow. But the cited PAG→NRA
  projection is from the **threat** columns (l/vl/dm); PAG-PANIC's own routing is **not directly cited** in
  what I found. **Flagging rather than assuming.**
- **preBötC + the inspiration gate** — a further new circuit. **Is the respiratory limb in scope, or does it
  become its own pass?** Without it the vocal output is ungated by breathing.
- `dACC`/MCC → `NuFac` — still to ground (Morecraft). And `dACC → PAG-PANIC` remains `basis: "assumption"`,
  the sole cortical→expression link, **ungrounded**.
- **`SympOut`: nothing** (§4).

**Nothing built.** The spec's two vocal edges are anatomically wrong; the fix needs at least one new circuit
(`NRA`), possibly two (`preBötC`), and a domain decision. That is a scope call.

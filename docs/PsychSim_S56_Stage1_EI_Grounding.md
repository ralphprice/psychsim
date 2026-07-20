# S56 Stage 1 — the E-I relation, GROUNDED. **Proportional tracking (detailed balance); the rest falls out.**

**I researched the inhibition-stabilized-network and detailed-balance literature rather than pick a functional
form, because whether inhibition tracks excitation linearly or sublinearly is an empirical question with an
answer. The literature is decisive, and it resolves all four of your questions — with the important result
that you should impose ONE thing (proportional inhibitory tracking) and let the rest emerge, not impose
several.**

---

## 1. What the literature establishes (two grounded facts)

**Fact 1 — DETAILED BALANCE: inhibition tracks excitation proportionally, per input, across a wide range.**
> *"stimulus-invariant proportionality of excitation and inhibition for any randomly selected input, over a
> large range of stimulus strengths"* (eLife, CA3–CA1). The inhibitory conductance a population produces is
> **proportional to the excitatory drive it receives** — the feedback interneuron receives the local
> population's excitation and returns proportional inhibition. This is the grounded form of your proposal:
> **inhibitory feedback gain scales with afferent excitatory load.**

**Fact 2 — the cortex is an INHIBITION-STABILIZED NETWORK; the proportional inhibition NORMALIZES the node.**
> Cortical networks *"operate in inhibitory-stabilized regimes"* with *"dominant recurrent inhibition"* (k > 1)
> (Science Advances). And the membrane consequence of detailed balance is **sublinear / divisive**: *"an
> initial linear zone followed by a sublinear zone for higher excitation values… inhibition divisively
> [normalizes]"* (eLife). **The node's settled activity is held roughly stable (normalized) as excitation
> grows, because inhibition grows proportionally with it.**

> **★ The key insight for the build: you impose ONE grounded relation — inhibitory feedback proportional to
> excitatory load (detailed balance, Fact 1) — and the normalization/sublinearity (Fact 2) EMERGES from it in
> the divisive integrator. You do NOT separately impose a sublinear law. Proportional inhibition IN the model's
> `a = baseline + Σinputs` integrator already produces `a_node ≈ E/(1 + loop_gain)` with `loop_gain ∝ E`, which
> is exactly the normalized/stabilized settling the literature describes. Imposing both would be double-
> counting. Ground the proportionality; the stabilization is the emergent consequence — and that it emerges
> rather than being imposed is the honest form.**

---

## 2. RULING on the four questions

### Q1 — the law + the set-point → **PROPORTIONAL tracking (`loop_gain ∝ load`); set-point EMERGES, read from the reference node.**
- **The law is proportional (detailed balance):** inhibitory feedback gain scales **linearly with afferent
  excitatory load**. This is Fact 1, and it is grounded, not chosen. The membrane-level sublinearity (Fact 2)
  is the *consequence* of proportional inhibition in the divisive integrator — **do not impose it separately;
  it falls out.**
- **The set-point is NOT a number you set — it is what a normally-driven cortical node settles at once
  inhibition tracks its excitation.** **Read it from the lightest-load reference node (dACC), whose current
  loop is the existing calibration.** The other nodes are scaled so they settle at the *same E-I balance* dACC
  does — that is what "detailed balance" means (proportionality to a common ratio), and it means the set-point
  is inherited from the reference, not authored.
- **★ CRITICAL — the set-point must NOT be tuned to fire the freezing floor.** The floor firing is the
  PREDICTION this grounding makes, not the target it is fitted to. **Ground the proportionality from the
  reference node's existing balance; then measure whether the floor fires. If it does, the grounding is
  confirmed. If it doesn't (the OFC residual, per your Stage-1 validation), that is the staging working — it
  points at Stage 3, not at re-tuning the set-point.** Tuning the E-I ratio until the floor greens would be
  the `BA→dACC`-to-"low" move at the gate-family scale, and it is forbidden.

### Q2 — which weight carries the scaling → **the `node → gate` feedback-excitation weight.** ✓ your proposal, grounded.
The interneuron's inhibitory output reflects **the excitation it receives from the local population**
(detailed balance: the feedback interneuron is driven by the population it inhibits). So the biologically
correct locus is **the node → gate drive** — dlPFC drives its interneuron proportionally more than dACC because
dlPFC's population is more excited. Scale `w(node → gate)` by afferent load; the `gate → node` return stays at
its grounded value (the GABA-A inhibitory strength is a synaptic property, not a load-dependent one). **The
E-I *ratio* then scales with load through the excitation side, which is where the biology puts it.**

### Q3 — reference / normalization → **relative to the lightest-load node (dACC); dACC stays the reference, unchanged.**
Detailed balance is about **proportionality**, not absolute values — so the natural and grounded
representation is **relative to a reference**. **dACC (lightest load, ~2 afferents) is the reference at
gain 1×, and its current loop is left unchanged** — it is the calibration point the others are scaled against.
dlPFC (~7–9 afferents) and vmPFC (~3–5) get proportionally higher `node → gate` drive. **This also means the
change is minimal and self-anchoring: one node is fixed, two are scaled to match its balance — no free absolute
parameter, which is the anti-tuning property we want.** *(If dACC's own loop turns out to be miscalibrated, that
is a separate finding — but nothing in the diagnosis suggests it; dACC is not a load-bearing gate and is not
implicated in either red. Leave it as the reference.)*

### Q4 — afferent-load definition → **circuit afferents, for the three cortical nodes.** ✓ confirmed.
For dlPFC/vmPFC/dACC the excitatory drive is from circuit afferents (these cortical nodes are not directly
sensory-channel-driven, unlike CeA). **Count circuit excitatory afferents.** *(The sensory-input-channel
contribution is the CeA-style case — that is Stage 2 territory, where CeA's direct nociceptive channel drive is
exactly why its feedforward gate can't hold it. For the three cortical nodes, circuit afferents are the load.)*

---

## 3. The honest expectation (unchanged, and the literature sharpens it)

**Stage 1 grounds the three cortical loops to proportional inhibition, which should lower the cortical DRN
over-drive and fire the freezing floor — but your own Stage-1 validation already showed the OFC residual
persists (DRN 0.391→0.384 with cortical loops strengthened, because ungated OFC keeps feeding it).** That is
expected and it is the staging working:
- **Stage 1 may green the divergence xfail and fire the floor partially, but the OFC→DRN residual (Stage 3) and
  CeA saturation (Stage 2) may survive** — because OFC is ungated and CeA is feedforward-blind, and neither is
  fixed by the cortical loop grounding.
- **Measure after Stage 1: which reds greened, does aggression recruit dPAG, and what residual DRN drive
  remains through OFC.** That measurement rules Stage 2 and Stage 3 — each opened only if its target defect
  survives, exactly as the scope ruling set.

> **Do not be surprised if Stage 1 alone does not fully green both reds. The literature confirms the mechanism
> (proportional inhibition normalizes the cortical nodes), and your validation confirms the direction — but it
> also confirmed the OFC residual, which Stage 1 structurally cannot reach. The grounding is correct even if
> the floor only partially fires; the remaining gap is Stage 3's OFC gate, and that it survives Stage 1 is the
> evidence that OFC needs its own step, not that Stage 1 failed.**

---

## 4. Handoff

**Build Stage 1: scale the `node → gate` feedback-excitation weight of the three cortical recurrent-E-I loops
(dlPFC-GABA, vmPFC-GABA) proportionally to circuit afferent load, with dACC as the fixed reference (gain 1×,
unchanged). The relation is proportional inhibitory tracking (detailed balance); the normalized settling
emerges from the divisive integrator and must NOT be separately imposed or tuned. The set-point is inherited
from the dACC reference, NOT fitted to fire the floor.**

**Gate on the full suite and measure explicitly: (a) does the divergence xfail green? (b) does the freezing
floor fire (fully / partially)? (c) does aggression now recruit dPAG? (d) what residual DRN drive remains
through the ungated OFC? Report all four — they rule Stage 2 (CeA interneuron) and Stage 3 (OFC gate), each
opened only if its defect survives.**

> **The relation is grounded from the detailed-balance / inhibition-stabilized-network literature: inhibitory
> feedback scales proportionally with excitatory load, one grounded proportionality, with the node's stabilized
> activity emerging from it rather than imposed. dACC is the fixed reference; the two heavy nodes scale to its
> balance; no free absolute parameter, nothing tuned to the wanted result. Build it, measure the four outcomes,
> and let the measurement — not a tuned set-point — decide what Stage 2 and Stage 3 owe.**

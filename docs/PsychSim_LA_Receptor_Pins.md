# The `LA` receptor pins — **GROUNDED: AMPA on both.** Closing a known fallback hazard.

**These were the census's "correct-but-ungrounded" pair — signs right (LA projects glutamatergically; local
GABA doesn't project), carrying `dominant_receptor: None`, load-bearing on the keystone. Not a question, a
debt. Paid.**

---

## 1. The receptor: **AMPA** — dominant fast transmission; NMDA is the plasticity partner

**The intra-amygdala glutamatergic synapse is the most-characterised synapse in the fear literature, and the
receptor split is unambiguous:**
> Amygdala afferent synapses are **"glutamatergic synapse[s] with AMPA and NMDA receptors"** (Palchaudhuri et
> al. 2024, review). At LA projection-neuron and BA glutamatergic synapses, **AMPA carries fast transmission;
> NMDA is the coincidence-detector for plasticity** — *"LTP… at glutamatergic synapses in the basal
> amygdala"* is GluR1(AMPA)-dependent (J Neurosci 2007, 27:10947), and LTP/LTD are *"NMDA
> receptor-dependent"* (PMID 18466342).

> **For a single `dominant_receptor` field, the answer is AMPA — it is the receptor that carries the
> moment-to-moment excitatory drive the model computes. NMDA's role is plasticity, which in this substrate
> lives in the `plasticity_coeff_schedule_ref`, not the receptor field.** So the pin is AMPA, and the NMDA
> half is already represented by the connection's plasticity schedule — **no information is lost.**

## 2. It matches the model's own precedent
**`MeA → VMH` is already AMPA** (the one intra-amygdala/hypothalamic glutamatergic edge we grounded this
branch). **`LA → BA` and `LA → CeA` are the same kind of synapse — a glutamatergic amygdala projection —
and take the same receptor.** The check I ran found no *existing* glutamatergic afferent into BA or CeA to
copy (the pinned ones are all neuromodulator: `LC` alpha1, `DRN` 5-HT1A), which is exactly why these two were
left on the fallback — **there was no in-file precedent to copy, so they defaulted.** AMPA is the grounded
fill.

## 3. RULING
1. **`LA → BA`: `dominant_receptor` = AMPA.** Sign +1 unchanged, weight `moderate` unchanged, basis stays
   `anatomy`. Behaviorally inert (fallback already gave +1; this makes the +1 grounded instead of accidental).
2. **`LA → CeA`: `dominant_receptor` = AMPA.** Same — inert, sign now grounded.
3. **Gate on library byte-identical** (both should be, since fallback +1 = AMPA +1) **+ keystone green.** If
   either is NOT byte-identical, stop — that would mean the fallback was giving something other than a clean
   +1 and there's a hidden interaction to understand.

## 4. What this closes, and what it leaves
- **Closes:** two fallback-signed, keystone-load-bearing connections — the exact object the census was built
  to hunt. **The census found one hazard (`MeA→ATL-TP`, since removed) and two debts (`LA→BA`, `LA→CeA`);
  all three are now resolved.** The census's actionable output is fully discharged.
- **Note for the record:** `LA → CeA` grounded is a **fully-grounded glutamatergic drive onto the `CeA`
  output hub** — worth having solid, since `CeA` is load-bearing across the defensive, vicarious, and
  aggression systems (it is the `LC` afferent, the effector driver, and the freezing-column input). One more
  of its inputs is now grounded rather than assumed.
- **Leaves (unchanged):** the remaining grounding I owe — `S56` (nine-node gates), the `VMH→vlPAG` band, the
  opioid system, `noci→PBN`. None needs the machine; none is a fallback hazard (the census cleared that
  category). They are genuine grounding questions, openable on your word.

**S57 stays gated on the machine (all five curves specified, `VTA` resolved). The deletion's `0.1`
confirmation stays gated on the machine. This pin needs only the byte-identical + keystone gate — it can go in
the next time the build session runs, machine or not, since it changes nothing behaviorally.**

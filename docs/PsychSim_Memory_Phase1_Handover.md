# v-next Memory Layer, Phase 1 — Claude Code handover

**Unify memory as ONE sub-symbolic substrate by dissolving the parallel symbolic town-layer
`MemoryStream` into the substrate's existing plasticity-memory (Reading A — integrate/unify, not extend).**
Design authority: `PsychSim_Memory_Phase1_SPEC.md` (reviewed + ruled). This is the foundation of the
representational layer (beliefs/attitudes/morality/rules → emerge later; dominance-hierarchy is the first
application, paused behind the layer). Governing discipline: **integrate, don't bolt on** — the symbolic
`MemoryStream` is an existing bolt-on; Phase 1 un-bolts it.

**Resource note:** nothing in the model is simplified or reduced to save compute. The substrate stays
full-depth; compute is found as needed. (Phase 1 in fact *removes* a redundant parallel computation.)

---

## 1. The diagnostic (verified against the remote — build on this, don't re-litigate)

- **The substrate ALREADY has honest sub-symbolic memory: its plasticity.** `engine.py`: `self.weight[]`
  (developed weights = engram) + `self.eligibility[]` (short-term trace). `plasticity.py`: BCM → eligibility
  → R5 consolidation → R4 homeostasis → R7 prune-long-silent. Engrams-as-weights, LTP-analogue consolidation,
  graceful decay, forgetting-by-pruning. **Memory, sub-symbolically, exists.**
- **A separate symbolic `MemoryStream` (`affective_engine/memory.py`) runs at the TOWN layer only.** Episode
  records retrieved by recency×importance×relevance ("generative-agents design"), feeding behaviour by
  **priming** an appraisal. Called ONLY in `sim_world` (`gamemaster.py:170,218`, `daily.py:131`) — **never in
  the substrate life-course** (`affective_engine/development.py` does not call `prime()`/`retrieve()`).
- **The town layer already runs the substrate** (`person.social_act`→`mind.social_act`→emergent act;
  `person.mind.engine` is the developing substrate). So the symbolic stream runs *alongside* the substrate,
  `.add()`-ing records that don't feed back through it. **It is a parallel scaffold, not a rival memory
  system inside the substrate.**

**CRUX — verified present:** the substrate's consolidation is **emotionally weighted**. `consolidate() = lr *
eta * modulator * eligibility`, and the modulator is `neuromod_output()` = the **live activation of the
gating neuromodulator's SOURCE CIRCUIT(S)** (`engine.py:114-122`, applied at `:178`). So high-emotional/arousal
events (which drive the neuromodulatory circuits high) consolidate MORE strongly — the amygdala
emotional-tagging analogue, built in and honest (modulator is a live circuit output, never an outcome value).
**This is why the developed weights faithfully carry the history-effect: high-emotion events left deeper
weight-marks.** The symbolic stream's crude `importance` scalar was approximating what the substrate does
better via neuromodulator dynamics.

---

## 2. What Phase 1 IS / IS NOT
- **IS:** make the priming effect emerge from the substrate's developed weights (which already produce it,
  emotionally weighted), and retire the symbolic `MemoryStream` from the **behavioural path** — so memory is
  ONE sub-symbolic thing everywhere.
- **IS NOT:** richer/episodic/retrieval memory (Phase 2), the PFC↔memory loop (Phase 3), new learning
  pathways (Phase 4), new circuits, weight changes, or any plasticity change. A *consolidation/un-bolting*,
  not an extension.

---

## 3. The build

### 3.1 Source the history-effect from the substrate (retire symbolic priming)
The symbolic `prime()` injects a "learned expectation" (threatening past → threat-primed appraisal). The
substrate **already produces this**: a threatening history gives threat-tuned weights (via
emotionally-weighted consolidation), so the substrate responds to threat cues more strongly on its own.
- **Remove the `prime()`-based appraisal nudging from the behavioural path** (the `sim_world` call sites).
  Behaviour is shaped by the substrate: run the substrate on the cue; its developed weights carry the
  emotionally-weighted history-effect. Do NOT override the appraisal with a symbolic prime.
- If any *fast* carryover between adjacent events is genuinely needed beyond the developed weights, use the
  substrate's **own short-term state** (the eligibility trace / recent activation the engine already has) —
  NOT a symbolic record.

### 3.2 Keep a NON-BEHAVIOURAL descriptive log (researcher-ruled)
- **Retire the `MemoryStream` as a behavioural device, but KEEP a purely-descriptive event log** (the
  `.summary()`-style record: events, valences, modes run) for inspection / UI / trace.
- **Hard requirement:** the log is **read-back-into-nothing** — no code path may read it into behaviour. It
  is a record, not a memory mechanism. Structure it so it *cannot* drift back into being a parallel memory
  (e.g. a write-only trace log, clearly separated from any behavioural read). The behavioural memory is the
  substrate; the log is just a record.

### 3.3 What must NOT change
- **Plasticity untouched** — BCM, eligibility, consolidation (incl. the neuromodulator gating), homeostasis,
  pruning all byte-identical. Phase 1 does not change *how* the substrate remembers; it makes the substrate
  the *sole* memory.
- **No new circuits, no weight/sign/basis changes** — the seed connectome is untouched. This is
  code-architecture (retire a parallel device + keep a non-behavioural log), not a substrate change.
- **Nothing simplified for compute** — full-depth substrate stays.

---

## 4. Verification
- **Memory is one sub-symbolic thing:** grep-confirm the behavioural path no longer routes through
  `MemoryStream.prime()`/`retrieve()`. Any surviving `MemoryStream` use is the descriptive log only, read
  into nothing.
- **History-effect sourced from the substrate (the priming effect, now emergent):** an agent developed under
  a threatening history responds to a new threat cue more strongly than one developed under a warm history —
  sourced from the developed weights, demonstrated by running the substrate (not a symbolic prime). Report
  the threatening-history vs warm-history response gradient.
- **Emotional-salience is real in the developed weights (the ruled check):** demonstrate that a
  **high-emotional-state history tunes the weights more deeply than a low-emotion history** — i.e. the
  neuromodulator-gated consolidation actually produces a meaningful emotional-memory difference, strongly
  enough that the developed weights carry the history-effect. If the gating is too weak to make a meaningful
  difference, **surface it as a finding** (emotional-tagging under-powered — do NOT re-add the symbolic prime
  to compensate; report it for a separate decision). The mechanism is confirmed present (§1 crux); this
  confirms its *strength*.
- **Plasticity byte-identical:** confirm no change to `plasticity.py` / the engine's learning path.
- **Full suite green** — the gate. Town-layer behaviour may shift (priming now from the substrate, not the
  overlay); if the golden regenerates it regenerates HONESTLY (history-effect now sourced from the
  substrate). Any behavioural shift is understood and recorded — NEVER re-add the symbolic prime to hit the
  old behaviour (no result is a target).
- **v9 closure + all prior phenomena intact** — this touches memory architecture, not circuits.

---

## 5. Process
- **Integrate, don't bolt on** — success = memory is one sub-symbolic thing, history-effect from the
  substrate that already produces it (emotionally weighted), symbolic scaffold retired from the behavioural
  path, non-behavioural log kept.
- **We differ from Joon Park (ruled):** memory is the sub-symbolic substrate, not a symbolic episode-stream.
- **No result is a target.** Full suite is the gate; golden regenerates honestly; library regrows.
- **Dual-reviewed:** reviewer verifies against the remote — (a) behavioural path no longer uses symbolic
  memory, (b) history-effect sourced from the substrate (gradient), (c) emotional-salience real in developed
  weights (the strength check) or the under-powered finding surfaced, (d) plasticity byte-identical, (e) the
  surviving log is non-behavioural, (f) suite green, (g) any behavioural shift understood/recorded.
- **Commit + push + STOP for reviewer clearance before Phase 2** (richer sub-symbolic episodic/retrieval
  memory).

---

## 6. Hand-off note (for the implementation session)

> **Memory Phase 1 — unify memory as ONE sub-symbolic substrate.** Authority:
> `PsychSim_Memory_Phase1_SPEC.md`. The substrate ALREADY has honest sub-symbolic memory (plasticity:
> weights=engram, BCM+consolidation=LTP, prune=forgetting), and its consolidation is emotionally weighted
> (R5 modulator = a neuromodulator circuit's live output, so high-arousal events consolidate more —
> `engine.py:114-122,178`). A separate symbolic `MemoryStream` (`affective_engine/memory.py`) runs ONLY at
> the town layer (`gamemaster.py`, `daily.py`), priming an appraisal from episode records — a parallel
> scaffold, never in the substrate life-course.
>
> **Do:** (1) remove the `prime()`-based appraisal nudging from the behavioural path — let the substrate's
> developed weights carry the emotionally-weighted history-effect (run the substrate; don't override the
> appraisal); any fast carryover uses the substrate's own eligibility/recent-activation, not a record. (2)
> Retire `MemoryStream` as a behavioural device but KEEP a purely-descriptive, read-back-into-nothing event
> log for UI/trace (must not drift into a parallel memory). (3) Change NOTHING in plasticity / circuits /
> weights. Nothing simplified for compute.
>
> **Verify:** behavioural path no longer uses symbolic memory (grep); the threatening-vs-warm history
> response gradient is sourced from the developed weights (run the substrate); high-emotion history tunes
> weights more deeply than low-emotion history (the emotional-salience strength check — if too weak, surface
> as a finding, don't re-add the prime); plasticity byte-identical; surviving log is non-behavioural; full
> suite green (golden regen honestly if behaviour shifts — never re-add the prime to hit old behaviour); v9
> + phenomena intact.
>
> **Process:** integrate don't bolt on; no result is a target; full suite is the gate; dual-reviewed
> (reviewer verifies on the remote); commit + push + STOP for clearance before Phase 2.

# Memory Layer Phase 1 — un-bolting the symbolic MemoryStream (ledger)

**Design authority:** `PsychSim_Memory_Phase1_SPEC.md` + `PsychSim_Memory_Phase1_Handover.md`.
**Goal:** make memory ONE sub-symbolic thing — the substrate's plasticity — by retiring the parallel
symbolic `MemoryStream` from the behavioural path (Reading A: integrate, don't extend). Reading the code
first changed the shape of the phase; both changes were verified by the reviewer on the remote and ruled.

## Two findings that corrected the handover's premise
1. **The symbolic behavioural prime was already DEAD CODE.** `MemoryStream.prime()` / `retrieve()` had
   **zero call sites** (the only reference to `retrieve()` was inside `prime()`; `prime()` was called
   nowhere). The `gamemaster.py`/`daily.py` sites the handover cited as "priming" are `.add()` — writing
   the log. So the symbolic behavioural priming was *already* out of the behavioural path; the un-bolting
   was mostly already true. Real work: **formally retire the dead device**, not "remove a live prime."
2. **The substrate's history-effect is bonding-tuning, not threat-tuning.** The SPEC's premise
   ("threatening history → threat-tuned weights → stronger threat response") does **not hold**: the
   `nociception→CeA/LA` threat edges are innate input edges (non-plastic), so threat response is
   history-invariant (warm ≈ harsh). But the substrate **does** carry a robust history-effect — in the
   **plastic bonding/OT edges**: warm rearing develops `NTS→PVN-OT` (0.90 vs 0.54) and `PVN-OT→NAc-shell`
   (0.72 vs 0.45) far stronger, so **warm-history agents bond more** (affil-drive 0.325 vs 0.282, robust
   across 3 seeds). The premise (substrate carries the history-effect) is validated; the *location* was
   wrong. This ties directly to the Part-1 OT completion: warm rearing tunes the now-drivable OT bonding.

## What was done (reviewer-ruled)
- **Retired the dead behavioural device** in `memory.py`: removed `prime()`, `retrieve()`, the helpers
  `_similarity()`/`_appraisal_vector()`, and the orphaned constants (`RECENCY_HALFLIFE`, `PRIME_THREAT_W`,
  `PRIME_SOCIAL_W`, `RETRIEVE_K`). Rewrote the module docstring (it described a generative-agents priming
  design that was dead) to state that behavioural memory is the substrate's plasticity and this module is
  a purely-descriptive, non-behavioural event log.
- **Kept a NON-BEHAVIOURAL descriptive log** (reviewer ruling): `EpisodicMemory` + `MemoryStream.add()` /
  `summary()` / `events` survive, for inspection / UI / trace. Read-back-into-nothing in the self-priming
  sense — no code reads it into a recording agent's OWN behaviour.
- **Justice-read confirmed acceptable (reviewer ruling):** `justice/system.py:124` reads
  `events[].dominant`/`.label` — the **public act-record** (what acts occurred), used by a societal
  detection process, not the agent's self-priming. It reads act-record fields, not any retired
  priming-specific field, so no re-sourcing was needed.
- **Plasticity / circuits / seed untouched** — `plasticity.py` and `engine.py` are **byte-identical** (0
  changed lines). No new circuits, no weight/sign/basis changes. Code-architecture only.

## Verification
- **Behavioural path free of symbolic memory:** grep-clean — no `prime()`/`retrieve()` anywhere.
- **History-effect substrate-sourced:** the **bonding gradient** (warm > harsh affiliation, 0.325 vs 0.282,
  robust across seeds), from the developed weights — not a symbolic prime. (The threat gradient the SPEC
  named does not exist; the verification target moved to bonding, where the plastic effect lives.)
- **Emotional-salience mechanism present + honest:** consolidation is `rate·eta·modulator·eligibility`
  where the modulator is a neuromodulator source circuit's **live activation** — so high-arousal events
  consolidate more (the amygdala emotional-tagging analogue; the modulator is a live circuit output, never
  an outcome value). The warm>harsh bonding effect is the emotionally-weighted history-effect made
  concrete.
- **Behaviourally inert removal:** because `prime()` was dead, retiring it changed **no** behaviour — the
  golden is unchanged and the full suite stays green with no regen. That is itself the confirmation that
  the prime was dead.

## Recorded finding (reviewer-ruled: characterize, don't tune)
The warm-vs-harsh bonding history-effect is **real and robust (~15%, 3 seeds)** — Phase 1's requirement
(the effect is real and substrate-sourced) is **met**. Its *magnitude* (whether ~15% is developmentally
realistic, or the neuromodulator-gated emotional-tagging is under-powered) is **flagged for a later phase**
that addresses consolidation/salience strength — **not tuned now** (tuning would be choosing-for-outcome;
the pre-ruling "don't re-add the prime to compensate" is honored — we characterize, we don't compensate).

## Net
`memory.py` only: the dead symbolic behavioural priming device retired, a non-behavioural descriptive log
kept, docstring corrected. Plasticity/circuits/seed untouched. Memory is now one sub-symbolic thing — the
substrate — with a descriptive record alongside it. The foundation for the richer sub-symbolic memory,
the PFC↔memory loop, and the learning pathways that follow.

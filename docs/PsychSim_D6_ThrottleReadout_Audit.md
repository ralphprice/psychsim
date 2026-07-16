# D6 — Throttle-set & Read-out audit (build-session pass)

**Diagnostic only. Nothing fixed.** This is the **build-session half** of the dual audit — to be reconciled
with the reviewer's independent pass. Enumerated from **what the code returns**, not what it was written to
return. Classification mirrors the 209-edge audit: `CLEAN · ENTAILED · HOLLOW · INCOMMENSURATE · CONFLATED ·
SELF-SEARCHING · UNRESOLVED`. The audit is **not clean** — as expected.

## ★ Headline — three live, one of them study-critical

1. **`AFFECTIVE_EMPATHY` contains `CeA`, and `CeA` is `LC`'s SOLE afferent** (`LC ← CeA` verified; LC's only
   other "afferent" is its own pacemaker self-term). `LC` is the teaching signal for **all** DA-gated
   learning. **So "low affective empathy impairs vicarious learning" is `ENTAILED` — true by construction:**
   the study's primary instrument throttles the learning mechanism's sole afferent. *This is case #2, and it is
   the one that decides whether the CU study can answer its central question.* **The manipulation cannot
   answer it, because the manipulation is the mechanism.**
2. **`AFFECTIVE_EMPATHY` is itself `HOLLOW` (3 of 5).** Under the distress cue it is read with, `MeA` and `aIns`
   are inert (Δ<0.02); the instrument rests on `LA`/`BA`/`CeA`. **The study's primary instrument measures on 3
   of its 5 terms.**
3. **`_OBS_AGGRESS` = (`CeA`,`dPAG`,`HYPdm`) is `HOLLOW` (1 of 3) AND `CONFLATED`.** It is read under the
   *threat* cue (`observer.py:151`), where `dPAG` and `HYPdm` are correctly silent (Phase A's floor: threat →
   avoid, not attack). So "reactive aggression" is read via **`CeA` alone — a threat/defense hub, not an attack
   circuit.** `HYPdm` stays 0.000 even under provocation. **The reactive-aggression measure reads defense.**

## CHECK A — manipulation surfaces (does the set contain the mechanism's own nodes?)

| set | type | members (current) | verdict | the claim it entails · evidence |
|---|---|---|---|---|
| **`AFFECTIVE_EMPATHY`** | throttle (CU study primary) | LA, BA, CeA, MeA, aIns | **`ENTAILED`** | contains `CeA`→`LC` (sole afferent, teaching signal) ⇒ "impairs vicarious learning" true by construction; contains `BA`→`dACC`→`NuFac` ⇒ the dual-pathway "involuntary blunted" arm is entailed (the volitional-spared arm is clean). |
| `AFFECTIVE_EMPATHY` ∩ `DEFENSIVE_OUTPUT` | throttle × read-out | shared {CeA, BA} | **`ENTAILED` (mitigated)** | `punishment_learning` reads 2/3 of a set it also throttles — **the yoked control (`dc−dy`) cancels the tonic component**; disclosed, not hidden. Keep the yoked control; without it the result is by construction. |
| `AFFECTIVE_EMPATHY` ∩ `COGNITIVE_MENTALIZING` | throttle × read-out | ∅ | **`CLEAN`** | the affective/cognitive dissociation's **cognitive arm is construct-valid** — the throttle does not touch it. |
| **`throttleable_circuits()`** | scan node set (derived, auto-extends) | **58 circuits** (incl. all 8 `-GABA` gates, `ITC`; excl. `motor_effector`) | **`SELF-SEARCHING`** (latent) | the domain-derived throttle set and the `_OBS_*` signature sets are **not disjoint** (both domain-derived), so a future auto-search maximising `_OBS_THREAT` could throttle `_OBS_THREAT`'s own circuits. Manual mode is safe; the search layer isn't built. Gates lesionable **by design** (gate-class ruling) — not a defect. `motor_effector` correctly excluded (the Phase-A near-miss). |
| **`_TEMPERAMENT_DOMAIN`** | temperament dials (applied to **every** agent) | THREAT/ANX→defensive_threat, SEEKING→reward, CARE/LOSS→affiliation, CONTROL→executive | **`ENTAILED`** (over-reach) | the `defensive_threat` domain contains **`LC`** — so a low-THREAT temperament throttles the **universal teaching signal**, impairing *all* learning, not just threat reactivity. A fearless seed should not be a global-learning deficit by construction. |
| `COGNITIVE_MENTALIZING` | read-out only (never throttled) | — | n/a | verified: only read (`cog`), never a `throttled_newborn` target. |

## CHECK B — read-out surfaces (does the measure measure what it names?)

| set | members | carries | verdict | evidence |
|---|---|---|---|---|
| **`DEFENSIVE_OUTPUT`** | CeA, vlPAG, BA | **2/3** | **`HOLLOW`** | `vlPAG`=0.000 always (S20: excitation-unafferented). Every freezing/defensive result rests on `CeA`+`BA`. (case #6) |
| **`AFFECTIVE_EMPATHY`** (as read-out) | LA, BA, CeA, MeA, aIns | **3/5** | **`HOLLOW`** | `MeA`, `aIns` inert under the distress cue. |
| **`_OBS_AGGRESS`** | CeA, dPAG, HYPdm | **1/3** | **`HOLLOW` + `CONFLATED`** | read under threat; `dPAG`/`HYPdm` silent (correct); reads reactive aggression via the **defense** hub `CeA`. `HYPdm` dead even under provocation. |
| **`_OBS_THREAT`** | CeA, vlPAG, BA, LA | 3/4 | **`HOLLOW`** | `vlPAG` dead. |
| **`_SELF_THREAT`** | CeA, vlPAG, BA, aIns | 2/4 | **`HOLLOW`** | `vlPAG` dead + `aIns` inert. |
| **`COGNITIVE_MENTALIZING`** | rSMG-TPJ, pSTS, PCun-PCC, ATL-TP | 3/4 | **`HOLLOW`** (mild) | `PCun-PCC` inert under the distress cue (a DMN/self node — may need a different cue). |
| **`EXECUTIVE`** | dlPFC, OFC, dACC | 3/3 | **`CONFLATED`** | `dACC` = conflict monitoring (correctly rises under harsh); `dlPFC`/`OFC` = control. Spans two constructs. (case #7, xfailed) |
| **`_OBS_EXEC`** | dlPFC, dACC, vlPFC, preSMA | 2/4* | **`CONFLATED`** | monitoring (`dACC`) + control (`dlPFC`/`vlPFC`) + motor-inhibition (`preSMA`); read at rest for `restraint`, so *carries reassessed at rest, but three constructs summed. |
| **domain aggregates** | (scan domain-means; golden per-domain) | — | **`INCOMMENSURATE`** | a domain contains its **drivers and its gates** (e.g. `defensive_threat` ⊇ vlPAG, vlPAG-GABA, dPAG-GABA): the gate's activation moves opposite to the construct, so the mean moves against its name. (case #8) |
| `_OBS_REWARD` / `_SELF_REWARD` | VTA, NAc-core, NAc-shell, OFC | 4/4 | **`CLEAN`** | all carry under reward; one construct. |
| `_OBS_CARE` / `_SELF_ATTACH` | PVN-OT, MPOA, (SEPT) | 3/3, 2/2 | **`CLEAN`** | all carry under warmth. |
| **`_DISTRESS_DISPLAY`** | NuFac, NuAmb-vocal | 2/2 | **`CLEAN`** | Phase C reads the effectors — the throttle set does not contain them (case #1, dissolved by fixing the display, not the set). |

## CHECK B — computed signatures
- **`punishment_learning`** — `ENTAILED` at the read-out (AE∩DEF), **mitigated by the yoked control**. The mitigation is real; keep it.
- **`empathy_response` / `affective_minus_cognitive`** — the **affective arm is `ENTAILED`** (it reads the throttled set) and **`HOLLOW`** (3/5); the **cognitive arm is `CLEAN`**; the dissociation-*as-contrast* is clean because the cognitive side is untouched. The magnitude of the index is part-manipulation, part-finding — disclose which.
- **`reactive_aggression`** (`_OBS_AGGRESS`) — `HOLLOW`+`CONFLATED` (above).

## `UNRESOLVED` (the honest valve)
- `_OBS_EXEC` "carrying" — it is read at rest (for `restraint`), not under a cue; my probe used threat. Its carrying needs a rest/executive-load assessment, not this one. **`UNRESOLVED` pending the right probe.**
- `PCun-PCC` / `MeA` / `aIns` inertness — whether these are *dead* (never carry) or *cue-specific* (carry under a different empathy/self cue than the one tested) is **`UNRESOLVED`**; the audit tested the cue each is *read with*, but a fuller probe set would settle dead-vs-cue-specific.

## ⚠️ Strict-completeness sweep — the first pass was NOT strict enough
A systematic grep for *every* named circuit-set and *every* computed signature found **six more surfaces** the
first pass missed. Per the ruling ("if it returns all clean, it was not strict enough"), these are the audit's
real yield — and two are new verdicts, not repeats.

| set / signature | type | members / source | verdict | evidence |
|---|---|---|---|---|
| `REWARD_READOUT` (`agent.py`) | read-out | OFC, NAc-core, NAc-shell, VTA | **`CLEAN`** | 4/4 carry under reward; one construct. (a third copy of the reward set — `_OBS_REWARD`, `_SELF_REWARD`, `REWARD_READOUT` are triplicated — a DRY smell, not a defect.) |
| **`substrate_profile` / `dominant_profile`** (domain means, `_READOUT_DOMAINS`) | read-out (feeds **golden per-domain + UI**) | mean of every circuit in a domain | **`INCOMMENSURATE`** | `_domain_activity` averages **drivers WITH their gates**: `defensive_threat` mean includes ITC, dPAG-GABA, vlPAG-GABA, DRN-GABA, vmPFC-GABA, CeA-GABA (6 gates in 21); `executive` includes dlPFC-GABA, dACC-GABA. When threat rises the gates rise too — the mean moves against its name. This is the concrete locus of case #8. |
| **`SUBSTRATE_READOUT`** (interocept state-vector) | read-out | 10 body variables → circuits | **`CONFLATED` (degenerate)** | `energy` and `hydration` are the **same number** (both = `NTS` level); `respiratory` = −`PBN`, `thermal` = +`PBN` → **`respiratory ≡ −thermal` by construction**; `PBN` alone serves 3 variables. 6 of 10 vars are single-circuit ("coarse", disclosed in-code). A study distinguishing energy from hydration would measure nothing. |
| **`measure_signatures` → `dissociation_index`** (`scan.py`) | scan search target | `cog − aff` | **`SELF-SEARCHING` / `ENTAILED`** | the scan maximises this by throttling; `AFFECTIVE_EMPATHY` (the `aff` set) ⊂ `throttleable_circuits()`, so "maximise dissociation" **is** "throttle affective empathy" — the search target and the entailed claim (#2) are the same act. Concrete, not latent. `punishment_learning` as a scan target: mitigated by the yoked control. |
| `risk_index` (`phenomena.py`) | signature | `go_drive / (thr + gain·executive_hold)` | **`UNRESOLVED`** | `go_drive` reads `DA`; `executive_hold` computes via helpers not traced here — go/hold *look* disjoint (approach vs restraint) but disjointness is **not confirmed** in this pass. |
| derived constructs (`aggression_profile`, `callous_unemotional`, `passive_avoidance_deficit`, `triarchic`) | computed from `BehaviourProfile` | inherit their `_OBS_*` sets | **INHERIT** | `aggression_profile` inherits `_OBS_AGGRESS` → **`HOLLOW`+`CONFLATED`** (reactive aggression read via the defense hub); `callous_unemotional` inherits `_OBS_EMPATHY`; etc. A construct is only as valid as the set it reads. |

**So the audit's live verdicts are broader than the first pass showed: the `INCOMMENSURATE` domain means feed
the golden and the UI; the interoceptive read-out is degenerate; and the scan's own search target is the
entailed claim.**

## Reconciliation note
This is the build-session pass. **Nothing was edited** — per the ruling, a set edited to remove an overlap
hides the defect (Phase C is the precedent: the overlap dissolved because the *display* was fixed, not the
set). Each verdict is a **separate future ruling**. The one that gates the study is **`AFFECTIVE_EMPATHY` ⇒
ENTAILED "impairs vicarious learning"** — until it is resolved, that claim is true by construction, and the CU
study cannot make it.

# PsychSim — CU study §9: decision-brief for the researcher

**Purpose.** `PsychSim_CU_Study_Spec.md` §9 lists four open questions that gate the CU control-surface
build (2.2). Their answers are **research-design decisions — yours to make; the thesis is defended on
them.** This brief does *not* answer them. For each it (a) states what the substrate already supports,
grounded in code; (b) lays out the options and trade-offs; (c) gives a **recommended default** for you
to confirm or adjust; (d) marks what only you can decide. Lock the four and the CU surface can be built.

**Two constraints hold across all four** (the study's method, §6 of the spec):
- **Signatures are MEASURED, never coded.** A CU read-out is computed over emergent behaviour; nothing
  stamps "callous."
- **Environment enters as PERTURBATION PATTERNS, never coded effects.** A family/SES variable configures
  *what stimuli are present*; what it does to the child **emerges**.

---

## Q1 — The CU signature set (which measured read-outs *are* the CU phenotype)

**What exists now (grounded).** The scan controller already names and computes two of the current triad:
- `punishment_learning` — the passive-avoidance / punishment-learning deficit ([study.py:55](../core/substrate/study.py#L55); also `passive_avoidance_deficit`, [observer.py:71](../core/affective_engine/observer.py#L71)).
- `dissociation_index` — "reads but doesn't feel": cognitive-mentalizing **minus** affective-empathy, over two distinct circuit sets (`COGNITIVE_MENTALIZING` = rSMG-TPJ/pSTS/PCun-PCC/ATL-TP; `AFFECTIVE_EMPATHY` = LA/BA/CeA/MeA/aIns) ([scan.py:130](../core/scan.py#L130), [study.py:22-23](../core/substrate/study.py#L22)).

The triad's third element, **low-affiliation**, is *structurally present* (the affiliation network + the
empathy path touch it) but is **not yet promoted to a named signature** in `SIGNATURE_NAMES`
([scan.py:114](../core/scan.py#L114)). Adding it is a small, grounded extension (a stated read-out over
the affiliation circuits), not new anatomy.

**Options.** (a) Confirm the triad as-is (punishment-learning + dissociation + low-affiliation). (b)
Extend it (e.g. add a fearlessness / low-threat-reactivity read-out, or a shallow-affect read-out). (c)
Reduce to the two already-named.

**Recommended default (confirm/adjust):** keep the **triad**, and promote **low-affiliation** to a named
signature so all three are first-class. Assess **per-signature with convergence-across-signatures** as the
strong result (a profile that is CU on all three is far more credible than one hitting a composite score) —
and **never** blend them into a single composite (a composite re-introduces a hidden weighting the honesty
wall forbids; the spec §6 is explicit).

**Your call:** the exact signature set and its clinical justification — which read-outs *constitute* the CU
phenotype for your thesis. (I can wire whichever set you name; I can't decide which is the right construct.)

---

## Q2 — Held-out clinical CU profiles (for search-for-match)

**What this is.** The search-for-match arm looks for a substrate configuration whose *measured* signatures
match a **real** clinical CU profile the model never saw during calibration. That profile is **empirical
data you supply** — I cannot generate it (a fabricated "clinical profile" would be the exact dishonesty the
held-out design exists to prevent).

**What the study needs from you:**
- The **instrument(s)** the profile is expressed in — e.g. the **ICU** (Inventory of Callous-Unemotional
  traits), or whichever CU measure your literature uses — and how its scores **map onto the Q1 signatures**
  (so a clinical profile becomes a target in the same measured space).
- The profiles carrying `not_used_in_calibration` provenance (the spec's requirement) — properly sourced,
  citable, and genuinely held out.

**Recommended default (confirm/adjust):** name the **ICU** (or your chosen instrument) as the profile
source, supply 1–3 held-out profiles spanning the CU range, and define the ICU→signature mapping with me so
the match is computed honestly in signature space.

**Your call:** the data itself and its sourcing — this is irreducibly the researcher's; the platform
consumes what you provide, it cannot invent the clinical ground truth.

---

## Q3 — Family/environment variable set + each one's perturbation-pattern definition

**Framing (the honest form).** Each variable is a **perturbation pattern**: it configures *what is present*
(stimuli, co-presence, encounter history), and the child's outcome **emerges**. Nothing here codes an
effect ("harsh → callous"); the world supplies the experience and the existing development rule consumes it.

**A candidate set to react to — a STARTING PROPOSAL, not a decision** (ground, extend, or replace each):
| Variable | Candidate perturbation-pattern definition (what it configures) |
|---|---|
| Siblings (number/spacing) | co-present roster in the developmental environment (the Arena is exactly this instrument) + shared encounter history |
| Caregiving quality | the warm-firm ↔ harsh-inconsistent home already defined (`warm_firm_home` / `harsh_inconsistent_home`) as present-stimulus + response patterns |
| SES | resource-affordance density (what Things/opportunities are present) + stressor frequency — as present-Thing sets, never a "poverty" tag |
| Household structure | which caregiver/relationship ties are present in the encounter matrix |
| School/peer environment | the peer roster + institutional encounter patterns (the group matrix) |

**Recommended default (confirm/adjust):** start from the variables your CU literature treats as the
established moderators, define each strictly as *what it makes present* (a Things/encounter pattern), and
add them incrementally — each new variable is grounded content reviewed like a substrate change (§9 of the
Arena spec makes the same point for environments/relationships).

**Your call:** the *actual* variable list and the grounding of each definition — which moderators the study
must include, and what real configuration each represents. (I can define the patterns with you; the choice
of which variables matter is the research design.)

---

## Q4 — Target-age default + the assessment battery

**What's settled.** ~**18** is confirmed as the default target age. Development runs over **real time**
(never compressed), so "assess at 18" means a life lived to 18.

**The open choice:** assess the signature **once at the target age**, or **across a developmental window**.
- *Once at 18* — a single clean cross-section; simplest; matches an adult-outcome framing.
- *Across a window* (e.g. 14–18, or a trajectory 6→18) — captures the *developmental course* of the CU
  signature (when the deficit appears, whether it stabilises), which is a richer and more defensible thesis
  claim, and the substrate supports it (the trajectory is already what the Arena/adolescent-risk work reads).

**Recommended default (confirm/adjust):** assess **across a short window at target age** (a few
assessments around 18) for the primary read-out, and optionally record the **full trajectory** (the
developmental course) as a secondary, since the model produces it for free and it strengthens the account.
If you want the simplest defensible design, once-at-18 is fine.

**Your call:** once vs. window, and the exact ages — a measurement-design decision for your thesis.

---

## What to lock (confirming these four unblocks the CU-surface build)
1. **Q1** — the CU signature set (recommend: the triad; promote low-affiliation to a named signature;
   per-signature + convergence; no composite).
2. **Q2** — the held-out clinical instrument + profiles you'll supply (recommend: ICU or your chosen
   measure; define the score→signature mapping with me).
3. **Q3** — the family/environment variable list + each one's perturbation-pattern definition (recommend:
   start from your literature's moderators, defined as present-stimulus patterns; grow incrementally).
4. **Q4** — target-age assessment battery (recommend: a short window around 18 + optional full trajectory).

None of these is mine to decide. When you've locked them, the CU control surface (2.2) — the backtester on
the scan controller + validated-CU-seed save/load + spawn integration — can be built against them, and the
fearless-preset removal (2.2c) is already done.

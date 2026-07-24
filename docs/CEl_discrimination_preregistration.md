# CEl-discrimination — PRE-REGISTRATION (written before measuring)

Construct-validity test on the CU study's PRIMARY instrument (`empathy` / `AFFECTIVE_EMPATHY`). Pre-registered
because this is exactly where a generous reading of a marginal result would be most tempting. Committed before
the measurement is run.

## The question (the direct, non-arguable form — ruled)

Does an isolated agent experiencing its OWN aversive state (no conspecific present) show an elevated affective-
empathy read-out? If own-pain drives the empathy nodes comparably to a conspecific-distress cue, the construct
partly reads general aversive reactivity rather than vicarious distress — on the thesis's headline measure.

## Instruments (as they exist in code)

- `_OBS_EMPATHY = (LA, BA, CEl, aIns)` (observer.py) — feeds `empathy = 0.5·vicarious + 0.5·moral_orientation`.
- `AFFECTIVE_EMPATHY = (LA, BA, CEl, MeA, aIns)` (study.py) — the scan/study set (includes MeA; `_OBS_EMPATHY` omits it).
- Read-out = mean live-circuit activity of the set after settling on a cue (the `_probe` idiom, read-only).
- CEl receives 20 afferents, most non-social aversive (nociception, bitter, sour, CO2, SC-Pv/looming, PBN, LC).

## Cues (isolated agent, fresh adult engine age 25; also a developed agent for robustness)

- **CONSPECIFIC-DISTRESS** (the intended empathy signal): `IN-VIS:biological_motion 0.8, IN-AUD:voice 0.7, IN-VIS:face_like 0.7` (the existing `_DISTRESS_CUE`).
- **OWN-PAIN / non-social aversive** (no conspecific): `IN-SOMATO:nociception 0.8, IN-GUST:bitter 0.8, IN-GUST:sour 0.8, IN-INTERO:CO2_acidosis 0.8`. (Looming/startle have no dedicated input channel — they are internal detectors — so the available non-social aversive channels are used.)
- **BASELINE**: empty cue (resting activity of the set).

## Metrics

For each set S ∈ {`_OBS_EMPATHY`, `AFFECTIVE_EMPATHY`}:
- `distress_elevation = probe(DISTRESS,S) − probe(∅,S)`
- `ownpain_elevation  = probe(OWN_PAIN,S) − probe(∅,S)`
- `contamination_ratio = ownpain_elevation / distress_elevation`
- PER-NODE elevation (own-pain and distress) for every node in the set — to locate the source.
- Construct values: `empathy_distress = 0.5·probe(DISTRESS,_OBS_EMPATHY)+0.5·moral` vs `empathy_ownpain = 0.5·probe(OWN_PAIN,_OBS_EMPATHY)+0.5·moral`.

## Disqualifying threshold (with rationale) — SET this before the numbers exist

- **CONTAMINATED** if `contamination_ratio ≥ 0.5` — own-pain drives the empathy read-out at least half as much as conspecific distress. Rationale: a vicarious-distress construct should respond to ANOTHER's distress; own-pain elevation should be near zero. 0.5 is deliberately generous because the sets legitimately share interoceptive nodes.
- **CLEAN** if `contamination_ratio < 0.2` — own-pain barely moves the empathy nodes relative to conspecific distress.
- **AMBIGUOUS** 0.2–0.5 — partial; the per-node breakdown decides.

## ★ The principled-vs-contaminated distinction (must not be lost)

`aIns` responding to own pain is **correct neuroscience**, not contamination: the anterior insula is the shared-
representation node — it codes self-pain AND witnessed other-pain (Singer et al. 2004). So own-pain elevation
CONCENTRATED IN aIns is the shared-affect mechanism working, and is NOT disqualifying. The contamination concern
is specifically **CEl** — a general-aversive selector with no vicarious-specific role. Therefore the verdict is
decided by the PER-NODE source:
- If the set-level ratio is high AND **CEl's own-pain elevation ≥ its distress elevation** → CEl is contaminating → remove CEl.
- If the set-level ratio is high but the elevation is carried by **aIns** (shared-representation) → principled, NOT a defect → document, keep.

## Predicted outcome (honest, including the live possibility of failure)

**Prediction: the test FAILS and CEl is implicated.** CEl's afferents are dominated by non-social aversive
channels (nociception/bitter/sour/CO2), so it should respond strongly to own-pain. I predict `contamination_ratio
≥ 0.5` for `_OBS_EMPATHY`, with CEl the dominant own-pain responder (own-pain elevation ≈ or > its distress
elevation). The prior "kept CEl because the inversion premise measured false" only established that CEl RISES with
threat — which is the contamination signature, not a defense. I expect `AFFECTIVE_EMPATHY` (which also carries MeA,
a conspecific-specific node) to discriminate somewhat better than `_OBS_EMPATHY`. I could be wrong — CEl's threat
afferents may be gated such that its net own-pain response is small; if so, the set is clean and stands.

## Consequence of each result (decided before measuring)

- **CONTAMINATED, CEl-driven** → remove CEl from `_OBS_EMPATHY` and `AFFECTIVE_EMPATHY`. Replacement is the
  LA/BA/**MeA**/aIns core (add MeA to `_OBS_EMPATHY`; it is already in `AFFECTIVE_EMPATHY`). NO new nodes. Re-measure
  the construct; then a full gate (this changes the study read-out). Surface for ruling before editing.
- **CONTAMINATED, aIns-driven (shared-representation)** → NOT a defect. Document the shared-affect account; sets stand.
- **CLEAN** → the felt sets stand; the registered CEl-discrimination question closes. Report the numbers regardless.

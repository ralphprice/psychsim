# P1 — the fork rulings. **And two corrections to my own work order.**

**The diagnosis was exact and it caught two places where my work order was wrong about the code. I'll correct
those first, plainly, then rule every fork. Where the code contradicts my scope, the code wins.**

---

## Corrections to the work order (mine, not yours)

1. **"B's `perceive` folds it via `IN-CONSPEC`" — WRONG, verified.** The incoming act becomes B's appraisal in
   `appraisal_from_act` (via `exchange`), NOT `perceive`. And `IN-CONSPEC` is not on the appraisal path — its
   only seed bands are `attractive_face`/`formidability_cue`/`kin_signature`, and the displayed-distress
   precedent already routes affect via the appraisal dimensions, not a conspecific channel. **I wrote
   `IN-CONSPEC`/`perceive` from the architecture doc's abstraction, not the code. The real receive seam is
   `appraisal_from_act`. Scope corrected: Change A attaches at `appraisal_from_act`, and there is NO
   `IN-CONSPEC` circuit involved.**
2. **This means Change A needs NO new circuit** — which resolves the biggest fork before we reach it. Good.

**This is the two-role split doing exactly its job: my map was one abstraction too high, your diagnosis pinned
the real seam. Build against the seam.**

---

## CHANGE A — the forks

### A1 — new `IN-CONSPEC:displayed_affect` edge vs fold onto existing dims → **FOLD. No new circuit.**
Verified: `appraisal_from_act` already maps a received act onto appraisal dimensions (`provocation`,
`social_valence`, `threat`, …) with an intensity scale and a deception branch. **A's displayed affect folds
into THIS, as an additional contribution to the same dimensions.** A new `IN-CONSPEC` edge would (a) require a
regrow, (b) contradict "no new circuits," and (c) duplicate a path the code already has. **Fold onto existing
dimensions in `appraisal_from_act`. This is the minimal, correct, precedent-matching move.**

### A2 — which display dimension crosses → **a general affect VALENCE, mapped to `social_valence` (+ the
### matching arousal dimension), not distress-only.**
Distress-only is too narrow — the phenomenon you named is the *whole* non-verbal band (the smile as much as the
wince). **Cross ONE scalar: A's displayed affective valence** — the net sign/intensity of A's live display
(from the effector read: `NuFac`/`NuAmb-vocal` above rest, which already bakes in the two-pathway masking).
Map it in `appraisal_from_act`:
- **displayed positive affect → raises B's `social_valence`** (warmth read: A looks warm/happy → B appraises
  the encounter as more benign).
- **displayed negative affect → raises B's `threat`/`other_distress` and lowers `social_valence`** (A looks
  hostile → threat; A looks distressed → `other_distress`, the existing dimension).

**One displayed-valence scalar, mapped to the dimensions already in `appraisal_from_act`. Not a new affect
taxonomy — the minimal thing that carries "how A showed" onto the dimensions B already appraises.** *(If the
substrate exposes a cleaner two-scalar display (valence + arousal), use both; if only a net display scalar is
cleanly available, valence alone is sufficient for P1. Use what the effector read gives cleanly — do not invent
a dimension the substrate doesn't produce.)*

### A3 — fold at `appraisal_from_act` vs restructure `converse` through `perceive` → **`appraisal_from_act`.**
It is the true seam (A1). **Do NOT restructure `converse` through `perceive` for Change A** — that was my
error's knock-on. The act-band and the affect-band cross at the same point (`exchange`→`appraisal_from_act`);
keep them together there.

### A4 — roll semantics: same seeded roll as the act band, or a separate roll → **SEPARATE roll.**
This is the richer and more honest choice, and it's the CU-relevant one. **Two dissociable perceptions:**
- the **act** may be seen or its deception missed (the existing `p_detect` roll), AND
- the **affect-mask** may be seen or missed (a *separate* seeded roll).

**Why separate:** a skilled manipulator's *words* may be believed while their *leaked affect* is caught — or
vice versa. Tying them to one roll collapses that. **A separate roll lets "act believed but the coldness
underneath was felt" happen — which is exactly the sophropathic/CU signal (the mask that mostly works but
leaks to a vigilant perceiver).** Use the same `vigilance`+`rng` in scope; draw a second `p_detect`-style roll
for the affect band. **The dissociation must EMERGE from the two rolls against B's vigilance — never scripted.**

---

## CHANGE B — the forks

### B1 — how to plumb `rel` + partner id into `perceive` → **pass the `Relationship` (or a lookup) into
### `perceive`; restructure `converse` to call `perceive` with the partner.**
Here the restructure IS warranted (unlike A3), because the record-read genuinely belongs in `perceive` (it
colours the *situational appraisal*, which is `perceive`'s job — distinct from the act-appraisal). **Cleanest
option: give `perceive` an optional `partner_rel` argument** (a `Relationship`, or `None` for no-history/ambient),
and have `converse` look up `rel(actor, target)` and pass it. **Do NOT relocate all relationships onto `World`**
— that's a larger refactor than P1 needs and touches more than the loop; passing the `Relationship` (or a
`rel`-lookup callable) into `perceive` is the minimal seam. *(The reply turn currently never calls `perceive`;
for P1, the partner-history read applies at the points where `perceive` IS called with a known partner. If the
reply turn needs the same read, pass the reply-side `rel` there too — but keep it to passing the record in, not
restructuring the turn engine.)*

### B2 — source = `rel` or memory → **`rel`. Confirmed. NOT memory.**
`Relationship` holds `familiarity`/`affect`(−1..+1)/`trust` — the clean per-other history, exactly what "does
this agent appraise a friend differently from a stranger" needs. **The `MemoryStream` is the wrong source: it
has no per-other key, and reading the descriptive log back to prime the substrate is the retired symbolic
`prime()` anti-pattern we explicitly rejected.** **Source is `rel`. This is settled — build against `rel`.**

### B3 — mapping `rel` → appraisal dimensions → **as follows, gains SCAFFOLD (not tuned).**
- **`rel.affect → social_valence`**, additively combined with the institutional `inst.warmth` contribution
  already there. **Combine rule: additive then clamp** (same pattern `appraisal_from_act` uses — `current + w`,
  clamped). History of warmth and a warm institution both push `social_valence` up; both-negative pushes down;
  they can offset. **Do not overwrite `inst.warmth`'s write — add to it.**
- **`rel.trust → reduces `threat`** (and/or raises `controllability`), using the existing precedent:
  `_vigilance_of` already treats `1 − trust` as threat-vigilance, so **low trust → higher threat read** is the
  code's own established mapping. Reuse it: `threat` contribution scales with `(1 − trust)`.
- **`familiarity`** can gate the strength of the whole record-read (a barely-known other colours the appraisal
  weakly; a long history colours it strongly) — optional for P1, but it's the honest gain and it's already the
  right variable. **All gains are scaffold — set them plausibly, mark them, do not tune to produce a wanted
  encounter outcome.**

---

## THE GUARDRAIL (restated, because both changes touch the input band)
**Every ruling above wires what B PERCEIVES — the affect A showed, the history B carries. NONE scripts what B
DOES.** B's act still falls out of B's substrate. **The masked-display dissociation (A4) and the
history-coloured appraisal (B3) must EMERGE from the substrates and the seeded rolls — if any of this becomes a
rule for B's response, stop; that's the honesty wall.**

---

## BUILD ORDER & CLAIM
1. **Change A** at `appraisal_from_act`: fold A's displayed-valence scalar onto the existing dimensions (A1/A2),
   same seam as the act band (A3), with a **separate** affect-mask roll (A4).
2. **Change B** in `perceive` (+ minimal `converse` plumbing): pass the `Relationship` in (B1), read from `rel`
   (B2), map affect→`social_valence` additively and trust→`threat` per the existing precedent (B3).
3. **Test the P1 claim** (unchanged): feeling crosses (incl. masked display moving B differently by the affect
   roll), AND history shapes the read (same encounter, warm vs harsh `rel` → different appraisal) — both
   emergent. **When both hold, HOLD and report. Do not open P2.**

**Two register notes:** the work order's `IN-CONSPEC`/`perceive` framing was corrected to the real seam
(`appraisal_from_act` for the act/affect band; `perceive` for the situational/record read) — a map-vs-code
correction, logged so the architecture doc's abstraction isn't mistaken for the seam. And the affect band's
separate roll is the CU-relevant dissociation, flagged for the study.

**Build Change A then Change B. Keep every response emergent. The loop starts carrying feeling and reading
history — the first honest turn of the crank.**

# Expression — diagnostic ruling
**Reviewer verification against `origin/main` + rulings. One phase is the researcher's call; do not start it.**

---

## 1. VERIFIED — the diagnostic is confirmed, and the headline is right

Re-derived independently against the remote (v14 seed, 83 circuits / 214 connections):

| circuit | in | out | |
|---|---|---|---|
| `PAG` | **6** | **0** | dead end |
| `PAG-PANIC` | **5** | **0** | dead end |
| `NuAmb` | **2** | **0** | dead end |
| `SympOut` | **1** | **0** | dead end |

`PAG → NuAmb` **absent**, confirmed. `PAG` drives **nothing**. `NuAmb` is driven only by `PVN`/`NTS`. `M1`,
premotor, SMA, facial nucleus **absent** (only `preSMA`). `dACC → PAG-PANIC` confirmed — and note it is
`default_weight_basis: "assumption"`, so the single cortical→expression link is **not even grounded**.

**The headline stands and it is the important finding: the emotional motor system is UNEFFERENTED.** Not a
missing read-out — a missing **output**. This is the **third instance of one systemic pattern**: `PVN-OT`
unafferented → `LC` unafferented → the emotional motor system **unefferented**. **A hub gets wired in one
direction, and the missing direction is invisible until something exercises it.** Standing check from here:
**every hub, both directions.**

**Two corrections to the diagnostic** (both matter for the build):

**(a) `PAG-PANIC` has 5 afferents, not 4** — `MPOA`, `IN-INTERO:contact_loss`, `PVN-OT`, `dACC`, `SEPT`.
Minor, but the afferent set is the point: contact-loss drives it, `MPOA`/`SEPT` (GABA-A) damp it. **The cry
circuit's afferents are already coherent.** It needs an efferent, nothing else.

**(b) `NuAmb` is NOT the vocal effector in this model — and this would have mis-built the limb.** Its seeded
`function` reads: *"Parasympathetic **CARDIAC** outflow (rapid vagal brake on heart rate)."* Wiring
`PAG → NuAmb` as specced would connect the expression hub to the **heart-rate brake**. The real nucleus
ambiguus is genuinely both — the **compact/semicompact formation** is laryngeal/pharyngeal (the common
effector for voluntary *and* involuntary vocalisation) while the **loose/external formation** carries cardiac
vagal preganglionics. **So `NuAmb` is lumped, and the vocal limb does not exist at all.**

---

## 2. Q1 RESOLVED — it is not a sign question. It is a GRAIN question.

**`PAG`'s own `function` field reads: *"Defensive output: freeze (**vlPAG**) / flight (**dPAG**)."***

**The seed documents its own lumping.** Two functionally opposite columns (Bandler & Keay: vlPAG = passive
coping/freezing/quiescence; dl-/lPAG = active coping/fight-flight) are one node — which is precisely what §9
forbade for the amygdala: *"the amygdala subnuclei are kept separate rather than lumped as 'amygdala,'
because the learning site, the output hub, and the inhibitory extinction gate develop and behave
differently."* **PAG fails that rule on its own description.**

**And the edge cites the paper that resolves it.** `CeA → PAG` carries `source: "innate defensive backbone;
Tovote et al. 2016"` — and **Tovote et al. 2016 is the paper establishing that CeA's GABAergic projection
targets vlPAG *GABAergic interneurons*, which disinhibit the vlPAG glutamatergic output → freezing.** So the
net effect on vlPAG **output** is **excitatory, by disinhibition**, through an inhibitory synapse onto an
inhibitory cell. **The edge cites the resolving mechanism and does not implement it.** It is on the
transmitter fallback with no `dominant_receptor`.

**So the tension dissolves — both halves are true:**
- **`CeA → PAG` is inhibitory** *as a synapse* (CeA is GABAergic — correct, keep).
- **The amygdala is among PAG's excitatory controls** *as a net effect on output* (the PLC/Holstege
  account — correct).
- **They are only contradictory while one node stands for two columns and the target cell is unrepresented.**

**This is the same shape as `PVN-OT → CeA` (§3.7a) and `CeA → LC` (§3.7c) — the third instance. The
recurring failure mode of this substrate is LUMPING**, and it is worth saying plainly ahead of the 209-edge
audit: **the audit's WRONG-TARGET and MISSING-ELEMENT categories will be dominated by lumped nodes, not by
wrong signs.** This one is an audit finding arriving early because expression cannot be built on top of it.

---

## 3. The keystone is NOT a blocker — it is a state pin, and it is re-expressible

`test_cea_to_attack_effectors_still_inhibitory_and_unchanged` asserts exactly two things:
1. `_MODEL.circuits["CeA"].sign == -1.0` — **CeA is GABAergic. TRUE, grounded, KEEP.**
2. `edge.weight0 == 0.70` for `CeA→PAG` and `CeA→HYPdm` — **a byte-exact pin on current state.**

**It does not assert anything about CeA's net effect on PAG output.** Per principle 11 — *a committed test
that pins current state is not a design guard; re-expressing one must preserve what it actually protected,
not merely what it literally asserted* — what it protects is: **CeA is GABAergic, and the CeA→defensive-
effector drive has not been silently altered.** A split preserves both: **the sign stays −1.0, the weight
stays 0.70; only the target cell becomes explicit.**

**But the behavioural keystone is a separate matter and must be re-proven, not asserted.** The v9 **neutral
floor** (no provocation → no aggression) and the finding that **damping CeA disinhibits attack** (which
falsified the A+B fix with clean data) are *behavioural* results. A correct split routes `VMHvl → dlPAG`
(attack — untouched) and `CeA → vlPAG-GABA` (freezing). **Re-run the floor and the phenomena battery and
report what happens. If the split flips a prior behavioural finding, that is a finding, not a failure —
surface it, do not tune around it.**

---

## 4. The construct-validity failure — your deeper reading is right, and it means the fix dissolves it

Confirmed: `AFFECTIVE_EMPATHY = ("LA","BA","CeA","MeA","aIns")` ∩ `_DISTRESS_DISPLAY = ("CeA","PAG","BA")`
= **`CeA`, `BA` — two of the three display nodes.** "CU agents show blunted involuntary expression" is
**true by construction**, and you caught it before it became a finding. That is principle 4 working.

**Your deeper point is the correct one and it is the ruling:** this is not a separate defect to be fixed by
editing the throttle set. **It is a symptom.** We read affect and call it expression, so an affect throttle
"explains" the display *by identity*. **Building the display as a real effector read RESOLVES the tautology
at its source** — the display becomes `f(vocal effector)`, which the throttle does not contain, and the claim
becomes one about *transmission through a real pathway* rather than an identity. **Do not touch the throttle
set to fix this. Fix the display and the overlap goes to zero on its own.**

**And note what this buys:** the *interesting* claim — **involuntary blunted while volitional intact** — is
only testable once both pathways exist, because the throttle acts on the affective route and leaves the
volitional route untouched. **That dissociation is the psychopathy signature, and it emerges or it doesn't.**

---

## 5. The two re-homed branches — CONFIRMED closing here

Chronic-distress invisibility (`CeA`=1.000 → display 0.000 by tick 800) and contagion damping are, exactly as
you say, **artifacts of phasic-differencing a limbic signal to fake a display.** Neither is separately
fixable; both are symptoms of the same wrong construction. **They close when the display reads an effector —
register them against this level and close them out here.**

---

## 6. Phasing — build 0→2. STOP before 3.

**Phase 0 — the grain corrections.** Split `PAG` per its own function field (vlPAG / dl-lPAG, Bandler & Keay)
and `NuAmb` per its formations (semicompact = laryngeal/vocal; loose/external = cardiac vagal). Give
`CeA → vlPAG` its cited target cell (Tovote 2016). Re-express the keystone test to what it protects. **Grounded
structural correction — no new domain. Re-run the neutral floor + battery and report.**

**Phase 1 — the efferent limb.** `vl/lPAG → NuAmb-vocal` (Holstege: PAG lesions → complete mutism), the
respiratory limb, `PAG-PANIC → NuAmb-vocal` (the cry finally outputs). **Completing hubs that already exist —
the PVN-OT/LC precedent exactly. No new circuits beyond the splits.**

**Phase 2 — the honest display.** `_DISTRESS_DISPLAY` reads the **effector**, not the affect. Closes §5,
dissolves §4. **Expect the vicarious route's numbers to move — that is the point; re-measure, do not
preserve them.**

**PHASE 3 — the volitional limb — DO NOT START.** M1 / lateral premotor / facial nucleus; premotor→PAG
suppression; M1→NuFac. **This is the researcher's scope call and it is bigger than it looks — see below.**

**Q7 is the gift: do not build a developmental schedule.** Expression hubs are online at 0.0/flat; every
candidate suppressor comes online 4–8 y on PFC-protracted schedules. **Thompson's trajectory is already
encoded. It needs a pathway to act on, not a new schedule.** If a developmental curve has to be *authored*,
something is wrong — stop and surface it.

---

## 7. Standing rules for this level
- **Nothing about the psychopathy signature may be built.** It emerges from two faithful pathways or it does
  not. The model is a representation, not a theory (principle 5).
- **The two-pathway difference is structural, never a gain** (the vicarious precedent).
- **Display rules, suppression strength, expressivity: LEARNED, never coded.** If a constant appears, a
  mechanism is missing (principle 2).
- **Instability = a missing pathway** (principle 1). Adding an output to four dead-end hubs will change
  dynamics. **Expect it. Do not rebalance.**
- Byte-additive; splits are additions, not cuts. Commit + push each phase and **stop for clearance**.

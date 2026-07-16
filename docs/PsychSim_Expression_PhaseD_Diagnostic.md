# Expression Phase D — diagnostic (NOTHING built; grounding the suppressor surfaced two decisions)

Phase D is the model's first motor output. The volitional PRODUCTION route grounds cleanly and is buildable as
specced. The dev-schedule question is answered (no new curve — no stop). **But grounding the suppressor target,
as ruled, surfaced two things the spec could not have known** — one mild, one a real fork I will not resolve by
symmetry. Surfacing before building.

## 0. What grounds cleanly — the volitional PRODUCTION route (buildable as specced)
Master reference §2, the involuntary/volitional dissociation (pyramidal vs extrapyramidal; the volitional-facial-
paresis lesion double dissociation):

| new node | domain | grounding |
|---|---|---|
| **`M1-face`** | `motor_effector` | primary motor cortex face area; origin of the corticobulbar (pyramidal) tract |
| **`PMC-l`** | `motor_effector` | lateral premotor cortex; the volitional system (production **and** the suppressor) |

| new edge | sign | grounding |
|---|---|---|
| `M1-face → NuFac` | + (AMPA) | the pyramidal/corticobulbar route — **the posed expression** (Kuypers; Morecraft) |
| `M1-face → NuAmb-vocal` | + (AMPA) | the cortico-bulbar route reaches the laryngeal/pharyngeal motoneurons too — **bypassing PAG and NRA**, as ruled |
| `PMC-l → M1-face` | + (AMPA) | premotor → motor, the standard hierarchy — gives the volitional route its drive |
| `vlPFC → PMC-l` | + (AMPA) | §3: vlPFC *"selects appropriate responses and inhibits irrelevant ones"*; dlPFC holds the goal → the regulation goal reaches the motor system |

**This makes the volitional route drivable INDEPENDENTLY of the affective circuits** (executive → `PMC-l` →
`M1-face` → effectors), which is what measurement #3 (throttle `AFFECTIVE_EMPATHY`, is the volitional route
spared?) requires. Good.

## 1. The suppressor target — GROUNDED to `PAG-PANIC`, not distributed (as ruled)
Master reference §2.1, the decisive finding:
> a faciorespiratory coordination centre in the **PAG** is controlled by two pathways: an *emotional* system
> (excitatory) and a *volitional* system descending from *lateral premotor cortices that can suppress laughter
> or crying.* … **Inhibitory onto PAG: lateral premotor / motor cortex.**

The centre is **faciorespiratory / vocalisation**, and our vocalisation column is **`PAG-PANIC`** (its own
function field: *"separation-distress & vocalisation system"*; it is the column that projects `PAG-PANIC → NRA →
NuAmb-vocal`). So the suppressor is **`PMC-l → PAG-PANIC` (inhibitory)** — grounded to the **one** column the
literature names, **NOT** distributed to `vlPAG` (freezing) or `dPAG` (escape). Pathological laughing/crying =
this suppressor lost, which the master reference notes is *precisely our current model's behaviour*.

## 2. ★ Surface (mild) — the cortical suppressor cannot inhibit directly; it forces `PAG-PANIC-GABA`
`PMC-l` is cortical = **glutamatergic** → by the receptor-sign convention a direct `PMC-l → PAG-PANIC` edge is
**+1 (excitatory)** — it would *drive* vocalisation, the opposite of suppression. To **inhibit** `PAG-PANIC`, the
cortical projection must excite a **local GABAergic interneuron** — exactly the precedent already in the model:
`CeA/BNST → vlPAG-GABA`, `DRN → dPAG-GABA` (a forebrain projection made net-inhibitory through the column's own
gate). So the grounded suppressor is:

**`PMC-l → PAG-PANIC-GABA` (AMPA, +) → `PAG-PANIC` (inhibited)**

**This forces `PAG-PANIC-GABA`** — the local GABA gate the registered item *"does `PAG-PANIC` need its own
gate?"* asked about. The suppressor answers it: **yes.** Groundable as a **scaffold** PAG-GABA gate on the
`vlPAG-GABA` precedent (a PAG interneuron with no cited pacemaker rate — not `dPAG-GABA`, which had column-
specific electrophysiology). `structural_element`, scaffold baseline, its sign from GABA-A. **Mild** — the
gate architecture is established; I flag it because it is a second new circuit the spec did not name.

## 3. ★★ Surface (a real fork — will NOT resolve by symmetry) — the FACE has no grounded suppressor
The suppressor the literature grounds is **vocal**: it inhibits `PAG-PANIC`, the vocalisation column. **But the
involuntary FACIAL route does not go through the PAG at all** — it is `BA → dACC (M3) → NuFac` (Phase B). So
`PMC-l → PAG-PANIC` suppresses the **cry** and leaves the **face** untouched. Measurement #2 (expression down
50–70%) and #3 (dual-pathway dissociation) are about **both** limbs, so this matters.

**Why I will not just add `PMC-l → dACC` by symmetry** (the ruling's explicit warning): §2.1 grounds the
inhibitory target as the **PAG** only. For the face, §2.1 says merely that *"SMA and the facial nucleus
participate in both systems — the convergence point"* — a **location**, not a mechanism that **reduces** facial
output. And the mechanism matters: `M1-face` is **excitatory** onto `NuFac`, so the volitional route can **mask**
(pose a different expression over the felt one) but **cannot by itself hold a neutral face** — reducing `NuFac`
below the emotional `dACC → NuFac` drive needs an **inhibitory** element that is **not grounded** in the source.

**The fork (needs a ruling):**
- **(a) Vocal-only suppressor now.** Build `PMC-l → PAG-PANIC-GABA` (grounded); facial suppression is DEFERRED
  as ungrounded. Measurement #2 then shows suppression on the **voice** only, and that is the honest, grounded
  result — reported as such. *(My lean: this is the disciplined option — it builds exactly what §2.1 grounds.)*
- **(b) Facial suppressor too**, via a route the reviewer grounds — e.g. `PMC-l → dACC-GABA` (the brake we just
  built), making the premotor suppress the facial-emotional cortical node through its own interneuron. This is
  *architecturally* symmetric with the vocal suppressor (cortex → the target's GABA gate) and `dACC-GABA`
  already exists — but I have **no citation** that lateral premotor inhibits the facial-emotional route, and
  "it is architecturally symmetric" is the symmetry argument the ruling told me to distrust.

**I will not choose (b) without grounding.** Which fork — and if (b), the citation — is the ruling I need.

## 4. Dev-schedule — answered, no new curve (no stop triggered)
Gross suppression matures school-age (Diamond 1988; PFC-paced, into the early 20s). The existing cortical nodes
already span it (`preSMA` 4.0, `dACC` 5.0, `vlPFC` 5.0, `dlPFC` 6.0) on the existing `pfc_low_early_high_late`
schedule. `M1-face`/`PMC-l` take an `online_age` in [4,8] and **reuse that schedule** — **no curve is authored**,
so the ruling's stop-condition is not triggered. The child→adult and neurotic→suppressor differences then fall
out of maturation × experience × temperament, as §5 requires — never a coded constant.

## 5. Registered (not acted on)
- **`M1-face` lumps the laryngeal motor cortex (LMC).** Human volitional vocalisation has a distinct LMC
  (Brodmann area 4/6 larynx region); `M1-face → NuAmb-vocal` attributes to the face-motor node what the LMC
  carries — a sub-grain lump, same class as `dACC` (M3) and `dPAG` (dl/l). Register, do not split now.
- The facial-suppression gap (§3) travels to the audit if the fork resolves to (a).

## 6. What I build once §3 is ruled
`M1-face`, `PMC-l` (+ `PAG-PANIC-GABA`); `M1-face → NuFac`, `M1-face → NuAmb-vocal`, `PMC-l → M1-face`,
`vlPFC → PMC-l`, `PMC-l → PAG-PANIC-GABA` (the vocal suppressor); **facial suppressor per the §3 ruling.**
`motor_effector` domain for the new effector-limb nodes; regrow; full suite; then measure the three emergent
questions (S22 dissociation under crosstalk; Gross suppression signature; the dual-pathway dissociation) and
report as-found — **expecting smaller honest numbers** (S18/artifacts-inflate). **Nothing built until §3.**

# Phase A — CLEARED (`c3d490d`)
**Verified independently against `origin/main`. The arc is sound and the finding is real. Two things must
land BEFORE Phase B's effectors go live — see §2. Do not start Phase B until they do.**

---

## 1. VERIFIED — what I checked, not what was claimed

| claim | verdict |
|---|---|
| 88 circuits / 218 edges; `PAG`, `NuAmb` gone; `vlPAG`, `dPAG`, `vlPAG-GABA`, `dPAG-GABA`, `NuAmb-vocal`, `NuAmb-cardiac`, `NuFac` present | ✅ |
| `dPAG-GABA` baseline **0.19**, setpoint **0.19 — PAIRED** | ✅ |
| The baseline is **DERIVED, not asserted** | ✅ **The `function` field carries the whole arithmetic and its conditions**: intrinsic rate **under synaptic blockade** 6.2 ± 0.84 Hz, against a stated strong-drive reference 32.2 ± 7.0 Hz → 6.2/32.2 ≈ 0.19. Stempel & Evans named. **This is exactly the LC pacemaker discipline and it is the right way to ground a rate.** |
| The **relational** fact preserved | ✅ gate ≫ output; VGluT2⁺ 0.11 ± 0.068 Hz, 92.8 % below 0.04 Hz — *the excitatory population really is silent at rest*, so a floor of 0.0000 is the grounded prediction, not a fitted one. |
| `CeA → vlPAG-GABA` (GABA-A, Tovote) and `BNST → vlPAG-GABA` (GABA-A, Gray & Magnuson + Hao) — **cited, not fallback** | ✅ |
| DRN flag resolved by target cell: `DRN → dPAG-GABA` **5-HT2A**, `DRN → dPAG` **5-HT1A** | ✅ |
| Suite 536 / 0 | ✅ |

**One check I ran that came back clean against my own suspicion:** `source: None` on the circuit looked like a
missing citation — it is not. **No circuit in the seed carries `source` (0 of 88, LC included)**; circuit
grounding lives in `function` by schema, and Stempel & Evans is named there. My concern, not your gap.

**And the proof is the right proof:** silencing the gate → dPAG 0.0000 → 0.0202. **The gate is demonstrated
load-bearing rather than assumed.** That is what makes this a mechanism and not a coincidence — which is
precisely the failure the arc uncovered. **Your own anti-tuning guard firing on your own change, and being
verified still armed afterwards, is the honesty machinery working unprompted. Noted.**

---

## 2. ⛔ BLOCKING FOR PHASE B — the domain fix moved the hazard; it did not remove it

`core/scan.py`:
```
_THROTTLEABLE_DOMAINS = ("defensive_threat", "affiliation", "interoception_autonomic",
                         "social_cognition", "executive")

def throttleable_circuits(...):
    """... Not a curated list: adding a circuit to the seed in one of these domains
       automatically extends the set."""
    return sorted(cid for cid, c in m.circuits.items() if c.domain in _THROTTLEABLE_DOMAINS)
```

**The throttleable set is DERIVED from domain tags and AUTO-EXTENDS.** That is a good design — it prevents
curation drift — and it is exactly why this bit silently. **Phase A automatically added to the throttle set:**
- **`NuFac`, `NuAmb-vocal`** → `interoception_autonomic` → **throttleable.** *"Low-interoception agents show
  less facial expression"* is **still true by construction.** Same bug, new domain. Five of seven domains are
  throttleable; you moved the effectors from one to another.
- **`dPAG-GABA`** → `defensive_threat` → **throttleable.**

### 2a. This collapses Phase C's justification — so the 8th domain is a **Phase B step 0**, not a Phase D prereq
**Phase C's entire reason for existing** is that the display reads effectors **the throttle does not
contain**, so the tautology dissolves. But `throttleable_circuits()` **contains them automatically, by
domain.** The tautology returns through a different door — **and that door opens itself for every circuit we
add.** Building Phase C on a throttleable effector would dissolve the `AFFECTIVE_EMPATHY` overlap and leave an
identical one behind.

**Build the 8th domain — `motor_effector` — before Phase B's effectors go live**, and **exclude it from
`_THROTTLEABLE_DOMAINS`.** Home: `NuFac`, `NuAmb-vocal`, and the Phase-D cortical motor nodes.
**`NuAmb-cardiac` stays `interoception_autonomic` — it genuinely is autonomic.** Splitting the node was what
made that distinction expressible; make it.

### 2b. `dPAG-GABA` is a STRUCTURAL element — pin it. This is the α2 class.
An autonomous pacemaker whose rate is grounded electrophysiology is **not a reactivity dial**. Throttling it
is **directionally perverse**: threat-down → gate-down → **dPAG disinhibited → MORE escape.** A low-threat
temperament would produce a *weaker escape brake*.

**This is the α2 ruling one level up.** We pinned α2 against *plasticity* because an autoreceptor is a
structural element, not a learned association — the same argument applies verbatim against *throttling*:
**a structural element is not a manipulation surface.** Exclude `dPAG-GABA` from the throttleable set (a
stated, cited exclusion — not a curated one), or give the gate populations their own non-throttleable tag.
**Bring the mechanism to review; the ruling is that it must not be throttled.**

> **The general rule, and it now has two instances: the DOMAIN IS A THROTTLE SURFACE — so domain assignment is
> a construct-validity decision, not a taxonomy decision. And a derived set that auto-extends will silently
> swallow every circuit added after it was written.** This joins the throttle-set audit as the same class.

---

## 3. The ~2× discrepancy — you reported it; here is what it is

*"Directionally wrong — the real network dampens that cell; ours excites it."* **Principle 1: that is a
missing inhibitory afferent, and the same paper names its class.**

> *"Disinhibition of the PAG has been suggested as a mechanism for initiating other instinctive behaviours…
> with **inhibitory long-range projections from forebrain regions inhibiting local GABAergic circuits within
> the PAG**."*

And the measurement: **VGAT⁺ activity transiently DECREASES at escape onset.** So **something inhibits
`dPAG-GABA` to release escape** — the gate is opened by disinhibition, exactly as `CeA → vlPAG-GABA` opens
freezing. **We have the gate but not its release.** That is why our in-network rate sits above intrinsic
instead of below it: nothing is dampening it.

**This is a real gap with a named class and it will matter for escape dynamics.** **REGISTER it — do not
build it now** (it is a defensive-initiation question, not an expression one, and it needs its own grounding
pass on which forebrain source). **But it means the escape circuit is not yet complete, and any escape/flight
claim is provisional until it is.**

---

## 4. Register (do not act)
The new keystone principle (*a passing keystone certifies the outcome, not the mechanism — an artifact can
hold it*); principle 6's extension (*no behavioural characterisation from a partial assembly*); the
domain-throttle hazard + the auto-extension property; the A+B narrowing **and** that it was measured against
an artifact-held floor (re-run when convenient — not now, not on this path); the `SC-Pv → dPAG` 0.50
Point-1 candidate; Hao's feeding context and "anterior vlPAG" as an un-modelled sub-grain.

---

## 5. Then Phase B
`motor_effector` domain first (§2a) · `dPAG-GABA` pinned (§2b) · **then** the vocal limb: `PAG-PANIC →
NuAmb-vocal`, the `vlPAG → NuAmb-vocal` grounding question, `PAG-PANIC`'s own gate (registered — the same
architecture, and the same paper names vocalisation as disinhibition-initiated), the emotional route to the
face, the respiratory limb, and `SympOut`'s efferent.

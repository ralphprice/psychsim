# P2a — the intensity-vs-margin question: RESOLVED toward INTENSITY. The implementation is correct as built.

**The adversarial review surfaced a real ambiguity in my ruling, and it is a mechanism question, not a knob. I
verified the two candidate quantities against the code. The resolution is principled, not a matter of
convenience: the update to the relationship representation should scale with the absolute phasic activation of
the selected action (intensity), which is what is implemented — NOT the margin over the runner-up.**

---

## 1. What the two quantities actually are (verified against `core/substrate/social.py`)

- **`win_drive` (implemented)** = `drives[resp.behaviour]` = the winning action's own **phasic drive
  activation** — computed as `max(b.drives.values())` in `FeltResponse.strength` (`social.py:269`). It is the
  activation level of the affordance that won the **action-selection competition** (the basal-ganglia-style
  race among candidate action drives, `respond_to_substrate`). A substrate quantity in [0, 1].
- **margin (the alternative)** = `d_win − d_second` = the difference between the winning drive and the
  next-strongest competing drive. A measure of how *decisively* the winner was selected relative to its
  competitors.

**The review's observation is factually correct:** an ambivalent near-tie win (`{aggress: 0.60, avoid: 0.58}`)
and an uncontested win (`{aggress: 0.60, rest: 0}`) have **identical intensity (0.60)** but very different
**margins (0.02 vs 0.60)**. Under the current implementation they update the relationship representation
identically. The question is whether that is correct.

---

## 2. The resolution — INTENSITY is correct, on three principled grounds

**This is not "intensity is easier." Intensity is what the mechanism should use, for reasons grounded in how
action selection and its downstream consequences actually work:**

**(a) The quantity that propagates downstream is the selected action's activation, not the competition
margin.** After action selection resolves, the winning action's drive is what reaches the effector and motor
systems and what is expressed in behaviour. The **losing competitors are suppressed by the selection circuitry
and do not propagate** — that is what action selection *is*. So the physiologically available signal at the
point where behaviour is produced (and therefore at the point where a partner experiences it and a
relationship representation could be updated) is the **absolute activation of the selected action**. The margin
is a property of the competition that has already been resolved and gated out; it is not carried forward.

**(b) The partner experiences the executed action, not the internal competition.** The relationship
representation `rel(writer, other)` encodes how the writer engaged the other. What the other is affected by —
and what should therefore drive the update — is the **intensity of the action actually produced**. An intensely
aggressive act delivered ambivalently and an intensely aggressive act delivered without hesitation are, at the
point of delivery, the **same act at the same intensity**; the writer's internal ambivalence is not
transmitted (except insofar as it is separately expressed as displayed affect — which is the P1 affective-
transmission channel, a *different* pathway). Scaling the relationship update by intensity correctly makes the
update reflect **what was done**, at the strength it was done.

**(c) Margin would require reading a quantity the mechanism has already gated out.** To scale by
`d_win − d_second`, the update at `adjudicate` would have to read the **suppressed runner-up drive** — a value
that winner-take-all action selection has specifically resolved *against*. This is not a quantity the
downstream update can biologically access: once selection completes, the competitor activations are not a
signal the rest of the system reads. **Using margin would be reaching back into the pre-selection state to
extract a decisiveness signal that the selected pathway does not carry** — which is exactly the kind of
non-physiological shortcut the honesty discipline exists to prevent.

> **Ruling: the relationship-representation update scales with `win_drive` — the selected action's absolute
> phasic activation. This is correct as implemented. The intensity-vs-margin question is resolved toward
> intensity, on the ground that intensity is the quantity the mechanism actually propagates and the partner
> actually experiences. No change is owed. My original ruling named `max(resp.drives.values())`; that was the
> correct quantity, and the review's flag — while a valid catch of the ambiguity — resolves to confirming the
> implementation.**

*(Note on `resp.steps`: I had named it as a possible secondary decisiveness term. It should NOT be added. It
would reintroduce the same margin-like decisiveness signal by another route, and the same three arguments apply
— the update reflects the intensity of what was done, not how many settling steps the competition took. Leave
it out. P2a adds exactly one factor, `win_drive`, and no other.)*

---

## 3. The `win_drive` / `strength` open dependency — correctly registered, and here is its status

The review flagged that `win_drive` (the `strength` scalar) is **load-bearing for the first time**, and that
`band × win_drive`'s absolute magnitude is only as grounded as `strength`, whose absolute scale is
"flagged-not-tuned."

**This is registered correctly and it is not a wall breach.** The reasoning:
- `win_drive` derives from a substrate quantity in [0, 1] (`_phasic_drive` read-outs resolved by the selection
  race). Nothing is tuned to a target. The update's **sign** is emergent (behaviour-string-keyed, category-
  free) and its **magnitude** now scales with an emergent activation. That satisfies the P2a claim.
- What is *not* established is the **absolute calibration** of `strength` — i.e. whether a drive activation of
  0.6 is physiologically "strong" or "moderate." P2a **reuses** `strength` at its existing scale; it does not
  **ground** it. So the absolute magnitude of a relationship update inherits whatever imprecision `strength`'s
  absolute scale carries.

> **This is the correct and honest position: P2a's mechanism (emergent-signed, intensity-scaled update) is
> sound and testable; its absolute magnitudes are provisional to the extent that the drive-strength scalar's
> absolute calibration is provisional. Registered as an open dependency, drawn down only if a later pass's
> claim turns on the absolute magnitude of relationship updates. It does not block P2a, and P2a should not
> attempt to ground it — that would be scope creep into the substrate's drive-calibration, which is a separate
> question.**

The three review-driven refinements (using the winner's own drive rather than `argmax` to remove the hidden
`winner == argmax` invariant; the `getattr` guard enforcing the documented act contract; the explicit
`min(1.0, …)` clamp enforcing the band bound in code rather than by convention) are all sound — they are
behaviour-preserving hardening, provably identical, and they make implicit invariants explicit. Accepted.

---

## 4. Status and the registered items

**P2a is confirmed closed:** the relationship-representation update is now emergent in both sign and magnitude,
the sign category-free and the magnitude scaled by the selected action's phasic activation, with no new tunable
constant introduced. 564 tests, one authorized failure (the defensive-freezing floor, held by the deferred
cortical-overdrive item) and two expected failures, zero regressions. The mechanism is sound and the
adversarial review found no blocker.

**The registered items stand, all documentation-only, no change to the connectome:**
- **The three-store fragmentation** — `gm.rel` (read by social appraisal), `Society.Tie` (standing/reciprocity/
  strain), and `RelationshipMatrix`/`RelationshipSlot` (the reward-prediction-error partner-value learner, fed
  self-referentially only). An architecture decision owed **before P3**: which store is canonical, and whether
  the reward-prediction-error learner subsumes the others. Not urgent for P2a; must be settled before
  population-scale interaction.
- **The developmental-integration gap (what I had mislabelled "P2b")** — the ontogenetic simulation
  (`develop()`) is environment-only and never invokes the dyadic-interaction machinery; the daily-life
  simulation (`daily.py`) bypasses the relationship representation entirely. Consequently, **partner-specific
  learning never occurs across development** — the relationship representation is written only in explicit
  interaction calls, never over a simulated lifespan. This is the next architectural pass, and it is the one
  that makes developmental divergence-by-history possible. Ruled in principle (development must accumulate
  through the same social-appraisal pathway the interaction uses, never a parallel plasticity channel bolted
  into `develop()`); to be scoped as its own pass with its own diagnosis of co-presence and computational cost.
- **The trust-floor / betrayal-representability grounding question** — whether trust should be permitted to go
  negative (representing betrayal) or floor at zero. A grounding question for its own pass, not a knob.
- **The reply-side asymmetry** — in a single interaction, only the trust variable influences the reply (via
  perceptual vigilance gating); the affect and familiarity variables are inert for the reply because the reply
  runs on the received-act appraisal rather than a fresh situational appraisal. Documented; a design decision
  for later if both parties' histories should colour a single interaction.

---

## 5. Next

**No build is owed on P2a — it is closed and the intensity ruling confirms the implementation.** The next
substantive pass is the **developmental-integration gap** (routing the ontogenetic simulation through the
dyadic-interaction machinery so that partner-specific learning accumulates across the lifespan). That is an
architecture pass and it should be scoped deliberately, beginning — as always — with a diagnosis: how does the
daily-life simulation currently model co-presence and interaction opportunity, and what is the computational
envelope of running the full interaction machinery across a developmental timecourse?

**When you are ready to open it, I will scope it in proper terms with its own claim. For now P2a is closed, the
intensity question is resolved toward the implemented quantity on principled grounds, and the open dependencies
are registered. Holding.**

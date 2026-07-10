# PsychSim — Phase 8 instruction (UI console: clock, day/night, markers, pause bug)

**Scope: cosmetic/UX plus one bug.** This phase does **not** touch the organism, the substrate, the
matrices' mechanics, the observer, or any invariant. Two items raised in first-run feedback are
**deliberately excluded** and escalated (§6, §7) — do not fold them in. A cosmetic phase must never
become the vehicle for a dynamics change made under time pressure.

Companion: `docs/PsychSim_UI_Redesign.md` (Phases 0–7). This is Phase 8.

---

## 1. Sim clock — epoch, date, and elapsed

The sim needs a wall-clock identity. Start the clock at **1 January 2000, 00:00**.

- The epoch is a **server-side constant on the sim clock**, not a client-side offset. The tick↔time
  mapping belongs to the simulation; the UI only formats it.
- Expose on `/state`: `epoch` (ISO), `sim_time` (ISO), `elapsed_hours` (int), `tick`, `speed`, `seed`,
  and the seed `version`. If a tick↔hour ratio already exists in the engine, use it; if it is
  implicit, make it an explicit named constant and record it.
- Render in the telemetry strip, absolute **and** elapsed, both mono:

```
PSYCHSIM  ☀ LIVE   2003-04-17 14:00   +3y 107d 14h   tick 15,204   pop 67   1.00×   v9
```

Elapsed carries equal prominence to the date — it is the number that maps onto developmental age and
the 1/n plasticity schedule. Not a tooltip.

Format `+{y}y {d}d {h}h`, zero-padded nowhere, no relative-time prose ("3 years ago").

## 2. Day / night

- **Derive from the sim clock's hour.** Do not add a separate day/night state.
- Telemetry strip: `☀` (day) / `☾` (night), in `--muted`; `--phosphor` stays reserved for LIVE.
- Town stage: a *very* restrained shift — the ground colour stepping a few points darker at night.
  Nothing else. No gradient sunset, no animated transition, no sky. This is an instrument.
- Respect `prefers-reduced-motion`: the shift is a colour step, not a fade.

**Honesty caveat.** If agent behaviour has **no diurnal coupling** in the substrate, the symbol is a
**clock read-out, not a state indicator** — and the UI must not imply otherwise. Do not add copy or
visuals suggesting agents behave differently at night unless the model actually does. If you find the
substrate *does* couple to the hour, say so and we will render it deliberately.

## 3. Monitored-agent markers

Seeded/monitored characters need to be findable on the town map.

- Render a **small numeric badge** on the person marker: a plain index (`1`, `2`, `3`) in `--warn`
  red, top-right of the face, mono, 10px. Keyed to a list in the rail or the Development Cohort tab.
- **Number them; never name the manipulation.** No `throttled`, `lesioned`, `fearless`, or any
  condition label on the map, in a tooltip, or in the marker's `aria-label`. Use the index plus a
  lookup elsewhere.

> **Why this is not cosmetic.** The study exists because we do *not* know what a manipulation
> produces. A map label announcing what was done to an agent primes every observation made while
> watching them. A neutral index plus a lookup is honest; a condition label on the map is a thumb on
> the observer's scale. This is the map-level form of U1 (the UI names circuits and indices, never
> outcomes).

The badge appears only on monitored agents. Everyone else: no badge.

## 4. Face-only person markers

- Drop the large spot behind the face. **The face is the marker.**
- Keep a **selection ring** (`--trace`) on the selected person only.
- Keep the numeric badge (§3) on monitored agents only.
- **Zoom fallback:** if the face is illegible below a scale threshold, render a simple dot *at that
  zoom level* — do not draw both at all zooms.
- This removes one node per person per frame (67 residents → 67 fewer nodes). Note it as a small perf
  win, not the perf fix (§7).

## 5. BUG — pause does nothing

`▶ Start` works; pause is inert. **Diagnose before changing anything**; do not guess-fix.

Candidate locations, in order:
1. `psychsim_server.py` — does the `pause` command reach a handler, and does it set the flag the sim
   loop reads? (`play` at :186, `pause` at :188.)
2. The sim loop thread — does it *check* the paused flag each iteration, or only at start?
3. `ui/src/hooks/useSim.ts` — is the transport button sending `pause`, or always `play`? Is there
   optimistic local state masking a failed round-trip?
4. `rail/TransportSection.tsx` (Phase 1) — did the extraction drop the toggle's branch?

Add a regression test at whichever layer holds the fault: pause → the tick counter stops advancing
across two consecutive `/state` polls; play → it resumes. Report which layer it was.

---

## 6. ESCALATED — physical endowment and biological sex (do NOT build in this phase)

### 6.1 Physical endowment

The researcher is right that these were specified and never wired. The finding, verified:

- **The v9 seed carries a full `physical_endowment` table (7 attributes):** `PH-ATTRACT`, `PH-SIZE`,
  `PH-MUSCLE`, `PH-AGILITY`, `PH-HEALTH`, `PH-SENSORY`, `PH-TEMPERAMENT` — each with a distribution
  and a stated bias.
- **`core/affective_engine/endowment.py` declares `physical: Dict[str, float]`** — but populates it
  from `getattr(seed, "physical", {})`, which does not exist on `TraitSeed`, so it is **always empty**.
- **Nothing consumes it.** Zero readers in `sim_world/` or `substrate/`.
- The seed itself flags the gap: `PH-ATTRACT` biases *"how OTHERS respond to the agent (feeds the*
  ***future*** *relationship matrix)"*.

So the Inspector isn't failing to display it — **there is nothing to display.** Physical endowment is
declared, unpopulated, and unwired.

**This is an organism change, not a UI change**, and it carries real honesty exposure — so it goes
back to the design session as its own scoped decision, not into Phase 8. Sketch of why it needs care:

- *Drawing* per-agent physical traits from the seed's distributions is legitimate endowment, exactly
  like temperament.
- *How they act* is the hard part. A coded rule (`attractive → tie value +0.3`) would be an authored
  social outcome — the encoded-effect the whole project forbids. The honest form is that a physical
  trait modulates **what another agent perceives** (a stimulus property, like a `Thing`'s stimulus
  dict), and whether that yields stronger affiliation must **emerge** from the perceiver's own
  reward/affiliation circuits.
- But "attractive faces are rewarding" is itself an **innate prior** and would need grounding and a
  citation (there is real literature — infant preference for attractive faces), which means an
  `innate_wiring_catalogue` entry, which means **a v10 seed pass** on its own review.
- `PH-SENSORY` ("quality of input entering each channel") is the cleanest: a gain on input channels,
  structural and meaning-blind. `PH-HEALTH` plausibly enters as interoceptive perturbation.
  `PH-SIZE`/`PH-MUSCLE`/`PH-AGILITY` bear on which acts succeed. Each needs its own grounding.

**Action for this phase: none.** Do not populate, wire, or display physical traits. Do not add an
empty "Physical" card to the Inspector — an empty card implies the data exists. Record the finding and
leave it. The design session will scope it.

### 6.2 Biological sex

**Scope, stated precisely: biological sex only** — chromosomal/gonadal sex and the hormonal systems it
determines. Specifically: **prenatal androgenic organisation** of sexually dimorphic circuits, and the
**activational** hormonal modulation that follows at puberty. **Gender as a social construct is out of
scope and is not to be modelled.** Where sex-differentiated social responding appears at all, it must
**emerge** from the matrices — it is never a coded role.

The finding, verified:

- **Sex does not exist anywhere in the code.** Zero references in `core/` or `extensions/`.
- **But the seed presupposes it, in two places, without defining it:**
  - `PH-SIZE` distribution is `normal(mean_by_age_sex, sd)` — parameterised by a sex variable that
    does not exist.
  - `VMH` is characterised as *"Reproductive/sexual and social behaviour (**gonadal-steroid gated**)"*
    — gated by hormones the model has no representation of.
- **It bears directly on the v9 attack node.** The ventrolateral VMH is the canonical sexually
  dimorphic nucleus: females have more Esr1/ERα-expressing neurons in `VMHvl` than males across many
  species including humans, and the female `VMHvl` contains two anatomically and molecularly distinct
  subdivisions — one for aggression, one for sex (Hashikawa et al. 2017, *Nat. Neurosci.* 20:1580 —
  **already in the v9 citation list**). Our `VMHvl` carries no sex parameterisation at all.

So sex is not merely absent: it is **assumed-but-undefined**, and the circuit most recently added to
the substrate is the one whose defining property in the literature is sexual dimorphism.

**The honesty line — this is why it cannot be rushed.** Sex differences in CU/psychopathy prevalence
are an **observed epidemiological outcome**. They belong on the **output** side. A model in which sex
*raises CU likelihood* by construction has encoded the answer, exactly as coding
environment→divergence would have. The honest form:

- **In:** sex as **biological substrate parameters** — prenatal androgenic organisation of dimorphic
  nuclei (`VMHvl` Esr1 density, `VMH`), gonadal-steroid gating, body-size distribution (`PH-SIZE`),
  activational hormonal modulation.
- **Out:** whether that substrate yields the observed sex ratio in CU traits is **measured**, never
  assumed.

That is not a limitation — it is a target. *"Does a sex-differentiated substrate, with nothing about
outcomes encoded, reproduce the observed sex ratio in CU traits?"* is precisely a
**search-for-match-to-held-out-field-data** objective for the scan controller. A hit is corroboration;
a miss is a real sufficiency finding.

**Genetic markers** (the thesis's epigenetics arm — e.g. `MAOA`, `OXTR` methylation) sit downstream of
this and are likewise **out of scope for Phase 8**. They enter, if at all, as parameters on
substrate/plasticity — never as a marker that assigns an outcome.

**Action for this phase: none.** Do not add a sex field, a sex parameter, a hormonal system, or any
sex display. Do not "temporarily" seed a sex attribute to unblock `PH-SIZE`. Escalated to the design
session **jointly with §6.1** as a single scoped **v10 organism pass** — grounded, cited, reviewed —
since both are declared-or-assumed but unwired, both bear on how others respond, and both need the
same treatment. One seed version, one review.

## 7. ESCALATED — performance (separate task; measure first)

"Runs slowly" is almost certainly **not** the front end.

- Known: `/state` was 980 ms for 52 residents because `read_mind` runs a **25-tick substrate settle
  per resident**; the round-robin cache took it to 131 ms. At 67 residents the cache is working hard,
  and the **sim step itself** runs a full substrate settle per person per act.
- **Measure before optimising.** Time (a) the server-side sim step, (b) the `/state` response, (c) the
  client render. Report the three numbers. The expectation is (a) ≫ (b) > (c) — in which case DOM
  nodes are a rounding error.

**The constraint, and it is not negotiable:** trimming settle ticks is legitimate **only if the
selection race has converged by the reduced count** — verify convergence, exactly as the earlier perf
pass did, and treat any behavioural change in the golden as proof the ticks were load-bearing.
Compressing wall-clock is free; changing the dynamics to gain frames is not.

If the substrate is genuinely too slow at 67 residents, the honest responses are: fewer residents,
background agents with `develop=False` (which the Arena already needs), or accepting the speed. **Not
quietly shortening the settle.**

Do not start this inside Phase 8. Bring the three measurements back first.

---

## 8. Deployment note (not this phase, but before any VPS)

`psychsim_server.py` is a **development server**: no auth, and it exposes `save`, `load`,
`delete_save`, and `matrix_upsert`. Anyone who finds the URL can delete saves and edit the matrices.
Before it goes on a public host, put it behind basic auth or a firewall rule at minimum. It is a
research instrument, not a hardened service — that's fine, just don't leave it open.

---

## 9. Acceptance

- [ ] `/state` exposes `epoch`, `sim_time`, `elapsed_hours`, `tick`, `speed`, `seed`, `version`;
      the epoch is a server-side constant; the tick↔hour ratio is a named constant.
- [ ] Telemetry strip shows date **and** `+{y}y {d}d {h}h` elapsed, both mono.
- [ ] `☀`/`☾` derived from the sim hour; town ground steps darker at night; no animation; reduced-motion
      respected. No copy implies diurnal behaviour the substrate doesn't have.
- [ ] Monitored agents carry a numeric badge. **Grep: no condition word** (`throttled`, `lesioned`,
      `fearless`, `psychopath`, `callous`) appears in any marker label, tooltip, or `aria-label`.
- [ ] Person markers are face-only; selection ring on the selected only; zoom fallback to a dot.
- [ ] **Pause works**, with a regression test asserting the tick counter stops across two polls and
      resumes on play. The report says which layer held the fault.
- [ ] No "Physical" card added anywhere; no sex field, sex parameter, hormonal system, or sex display
      added anywhere (§6).
- [ ] No settle-tick change (§7).
- [ ] Gates: `vitest` green · `tsc --noEmit` 0 · `vite build` 0 · full Python suite green.
- [ ] Honesty grep clean; U1/U2/U4/U5 unchanged.

Sync per the usual cadence, confirmed on `origin/main` (`git fetch` then `git log origin/main`).
Report the three perf measurements (§7) alongside the phase, but do not act on them.

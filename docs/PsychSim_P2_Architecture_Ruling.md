# P2 — the architecture ruling. **SPLIT it: P2a (emergent write) now, P2b (route the life through exchanges)
# as its own pass.** And do NOT wire the RPE store yet.

**This is the most consequential diagnosis since the loop began, because it found that P2-as-I-scoped-it is
partly VACUOUS. I verified the crux: `develop()` is env-only and never sees `rel`; the daily loop calls
`converse`/`adjudicate` ZERO times; three relationship stores exist unreconciled. The build session is right to
hold. Here is the ruling, and it starts by admitting my P2 scope bundled two things that must be split.**

---

## 1. The core problem with my P2 scope: it bundled a small fix and a big architecture decision

I wrote P2 as "the record shapes development." The diagnosis proved that is **two claims wearing one label:**
- **(P2a) make the single-exchange write EMERGENT** — currently the sign is emergent but the magnitude is
  scripted (hardcoded ±0.15/±0.2). Small, local, matches the P1 read already built.
- **(P2b) make development NON-VACUOUS** — currently `rel` is never written over a simulated life, because the
  lifecourse (`develop`/`daily`) never runs the exchanges that write it. **Making "development" real requires
  routing the lifecourse through exchanges — a genuine architecture decision.**

> **Bundling these is the exact mistake this branch keeps catching (the dl/l split stacked on a grounding pass;
> S57 built before the pacemaker table). A small honest fix and a large architectural change must not ride in
> one pass — the large one will either be rushed or will swallow the small one. SPLIT THEM.**

---

## 2. P2a — LOCKED: make the write emergent. Scoped to `gm.rel`. Build this now.

**The sign is already emergent (keyed on the emergent behaviour string, honesty-clean). The magnitude is
scripted. P2a makes the magnitude emergent too, using the substrate's own conviction — no new plumbing.**

**Ruling on the forks the build raised, all accepted as recommended:**
- **Outcome scalar → `max(resp.drives.values())`** — the substrate's own emergent conviction at the moment of
  the act, already computed at the call site. **A decisively-won act moves `rel` more than one that barely
  crossed threshold.** ✓
- **AVOID `intensity`** — correctly flagged: it is an appraisal-category proxy and would smuggle a
  THREAT/REWARD label back into the magnitude. **That is a soft honesty breach and the build session caught it
  before I did.** ✓ `resp.steps` as a secondary shaping term only, if at all.
- **Keep the emergent sign selector** (`is_cohesive_act`/`is_aggressive_act` on the behaviour string) — it is
  category-free and honesty-clean; the migration-#2 claim holds. ✓
- **Edge semantics: keep the writer's-own-act driving `rel(writer, other)`** ("how I engaged you") — correct
  substrate-semantics, not a knob. ✓
- **Honesty guards all ACCEPTED:** derive the delta from a substrate quantity already in [0,1] (`max(drives)`
  qualifies); **if `Society.Tie`'s deltas are a structural twin, inherit them byte-for-byte** (the byte-
  identical-twin anti-tuning pattern — "no knob to tune"); **defer any caught-deception trust penalty**
  (deception doesn't emerge in the category-free baseline yet); **never force symmetry by averaging the two
  directed edges.** ✓ all.

**Ruling on the two substrate-grounding questions (NOT knobs):**
- **Clamp asymmetry / is distrust real** — an outcome-scaled magnitude will push trust toward its 0 floor on a
  strong aggressive outcome. **Lean to KEEPING the floor for P2a** (trust bottoms at 0; betrayal-as-negative-
  trust is a separate representable phenomenon). **If betrayal is meant to be representable, that is a grounded
  substrate decision for its own pass — do not tune the floor to make it happen.** Register it.
- **Reply-side read symmetry** — **accept the asymmetry for P2a** (the reply runs on `heard` by design; only
  `trust` bleeds through via perception-gating, which is correct — that's `_vigilance_of` working). **Document
  that `affect`/`familiarity` are inert in-conversation for the reply.** If we later want both histories to
  colour one exchange, colouring `heard` with `rel(target, actor)` is the least-invasive route — **but that is
  P2b-or-later, not P2a.**

**P2a claim (S35):** after an exchange, `rel` moves by a magnitude that scales with the substrate's emergent
conviction (`max(drives)`), sign still emergent — so a decisive warm act builds more affect/trust than a
marginal one, and a decisive aggressive act erodes more than a marginal one, **with every magnitude traceable
to a substrate quantity and no hardcoded step.** Verify the byte-identical inheritance from `Society.Tie` if
it's a twin. **When it holds, P2a closes.**

---

## 3. P2b — the architecture decision: **route the lifecourse through exchanges. Its own pass, ruled in
## principle, scoped separately.**

**The diagnosis's crux — "development has no path; `develop()` is env-only, the daily loop never runs
exchanges" — is REAL and I verified it. This is the decision you flagged, and it is genuinely architectural.
Here is the ruling in principle, with the build deferred to its own pass:**

> **Development MUST accumulate through the SAME P1 perceive→appraisal read — never a parallel `develop()`
> plasticity channel.** The honesty note is exactly right: bolting `rel` into `develop()` as a plasticity term
> would be a second, hidden developmental pathway that bypasses the loop. **The ONLY honest way for history to
> shape a developing life is for the life to actually RUN the exchanges that write and read `rel`.** So:
- **P2b routes co-present interactions in the lifecourse (`daily`/the life-sim) through
  `adjudicate`/`converse`**, so that over a simulated childhood, `rel` is written by real exchanges and read
  back into appraisal — **and divergence-by-history emerges because the life is lived, not because `develop()`
  gained a knob.**
- **`develop()` stays env-only.** It is the substrate's maturation against the environment; it is NOT where
  relational history lives. **Do not add `rel` to `develop()`.** ✓ (the build's recommendation, ruled correct.)

**But P2b is a real architecture pass** — routing the lifecourse through the exchange engine touches the daily
loop, co-presence, who-meets-whom, and performance (the exchange engine is heavier than the current abstract
daily step). **It is NOT a knob and NOT a quick follow-on to P2a. It is the pass that makes the SimCity
actually a society of interacting minds rather than agents developing in parallel isolation.** It deserves its
own scope, its own diagnosis (how does the daily loop currently model co-presence? what's the performance
envelope?), and its own claim.

**P2b claim (when we scope it):** over a simulated life, an agent's relationships and behaviour diverge as a
function of the exchanges it actually had — traceable entirely to `rel` written by lived exchanges and read by
perception, with `develop()` unchanged. **This is the real "development" claim, and it is the gateway to P3
(population-scale life-histories).**

---

## 4. The three-store fragmentation — REGISTER as an architecture decision owed. Do NOT resolve it in P2a.

**Three unreconciled dyadic stores exist:** `gm.rel` (fixed-step, what P1 reads), `Society.Tie`
(standing/reciprocity/strain), and `RelationshipMatrix`/`RelationshipSlot` (the **RPE learner** via
`ValueLearner` — the genuinely emergent-from-outcome writer, currently fed `self` only, banked-but-unfed for
real others).

> **★ The VTA lesson applies exactly: `RelationshipMatrix` EXISTING is not a reason to wire it this pass.** It
> is the eventual right home for an emergent relationship value (it learns per-other by reward-prediction-
> error, which is what a relationship *is*), **but wiring it to real others is a separate unit with its own
> grounding**, and P2a's job is the minimal emergent write that matches the P1 read already built. **Scope P2a
> to `gm.rel`.**

**RULING: register the three-store fragmentation as an architecture decision owed BEFORE P3** — because you
cannot scale relationships to a population (P3) while three stores disagree about what a relationship is. The
decision: **does `RelationshipMatrix` (RPE) become canonical, with `gm.rel` and `Society.Tie` derived from or
replaced by it?** That is a real design question, it is not urgent for P2a, and it must be settled before P3.
**Flag it; do not rush it.**

---

## 5. BUILD ORDER

1. **P2a NOW:** make `gm.rel`'s magnitude emergent (`max(drives)`, emergent sign kept, honesty guards accepted,
   `Society.Tie` byte-identical inheritance if twin). Test the P2a claim. **Hold and report.**
2. **Then P2b as its own pass:** route the lifecourse through exchanges (diagnose co-presence + performance
   first, as always). This is the real development claim.
3. **Before P3:** resolve the three-store fragmentation (the RPE-store-as-canonical decision).

**Register now (no build):** the three-store fragmentation (architecture decision owed before P3); the
trust-floor/betrayal-representability grounding question; the reply-side affect/familiarity in-conversation
inertia (documented asymmetry); and — carried from P1 — the warmth-display effector (highest-value ARC-3 gap).

> **My P2 scope was too big — it bundled an honest local fix with a society-scale architecture change under one
> label, and the diagnosis caught it. P2a is the fix (emergent write, now). P2b is the architecture (route the
> life through exchanges, its own pass). Splitting them is the discipline. Build P2a; hold P2b and the store
> decision for their own scoping. The write becomes emergent this pass; development becomes real the next.**

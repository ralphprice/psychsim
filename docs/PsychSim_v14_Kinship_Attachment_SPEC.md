# PsychSim — v14 design spec: kinship, attachment & pair-bonding

**Design specification. Status: SPEC ONLY — nothing built. For researcher review; phasing decided at
review.** This reopens the organism track for one grounded, cited seed change (v14), to add the
oxytocin/vasopressin bonding machinery the substrate genuinely lacks — the mechanism by which
parent-child attachment, sibling bonds, pair bonds, and their fractiousness and dissolution can
*emerge*. Revealed as a real omission by the Arena (a household cannot currently be defined because the
bonds that make it a household have no mechanism to form).

---

## 0. The keystone (read first — it is what keeps this honest)

Kinship bonds are **developmental outcomes of neural mechanisms, never spawn-time values.** The
temptation — "parent-child → strong bond," "50% shared DNA → high care" — codes the *outcome* against a
variable the brain **cannot sense**. No organism perceives relatedness directly. It perceives *cues*
and *familiarity*, and infers/acts on kinship from those. So:

> **Relatedness (% shared DNA) is an upstream spawn-time FACT that sets *cue similarity* between agents
> — nothing more. The bond — its strength, its fractiousness, its dissolution — EMERGES from each
> agent's own recognition and reward circuits responding to those cues and to early co-rearing. A bond
> is measured, never set. A household is defined by kinship *facts* + co-rearing arrangement, and the
> bonds that make it a household are *discovered*.**

This is the exact pattern established for physical attractiveness in v10: a trait is a **stimulus the
bearer presents**; the response emerges from the perceiver's circuits. Here the "stimulus" is a
**genetic-fingerprint cue** (the MHC/scent analogue), its *similarity* to the perceiver scaled by
shared DNA — and the bond emerges from phenotype matching + familiarity, never from a coded value.

**Grounding for the keystone** (why relatedness is never a direct input): kin recognition uses
association/familiarity (learned templates from early co-rearing — the Westermarck effect), phenotype
matching (self-referent cue comparison — the "armpit effect"), and chemical/MHC cues — never direct
relatedness detection (Mateo & Johnston 2000, *Proc R Soc B* 267:695; Lieberman, Tooby & Cosmides 2007,
*Nature* 445:727; the human olfactory kin-recognition substrate is insula + dmPFC, operating below
conscious awareness — Lundström et al.). Cross-fostering and adoption produce full bonds to non-kin;
the Westermarck effect produces incest-aversion from co-rearing *regardless of actual relatedness* —
both prove the brain reads familiarity/cues, not DNA.

---

## 1. What the substrate ALREADY has (v14 is smaller than it looks)

An audit of v13 shows the bonding scaffold is **substantially present** — v14 largely activates,
receptor-signs, and completes it, rather than building from scratch:

- **`PVN-OT`** — the oxytocin/vasopressin source, already present, already projecting to **`NAc-shell`
  (the OT→reward pathway — the core bonding mechanism!)**, `MeA`, `SEPT`, `MPOA`, `BNST`, `CeA`,
  `PAG-PANIC`. *But these edges are on the transmitter fallback (`receptor=(tx)`), not receptor-signed.*
- **`MPOA`** — the CARE / parental-nurturance hub, present, projecting to `VTA`, `PAG-PANIC`, `VMH`.
- **`MeA`** — "social/chemosensory processing; social recognition" — the kin-cue processing node.
- **`SEPT`** — separation-distress modulation (OT/AVP-sensitive) — the bond-loss signal.
- **`NAc-shell`/`NAc-core`/`VTA`** — the reward system the bond is built in.
- **`aIns`/`mIns`/`pIns`, `dmPFC`, `OFC`** — the self-referent/recognition substrate (the human
  kin-recognition network is insula + dmPFC).
- **`IN-OLF` and `IN-CONSPEC`** — channels for the genetic-fingerprint/scent cue to enter on.

So the machinery is mostly wired. What is **missing** is: (a) receptor-honest signs on the OT/VP
projections; (b) the perceptual-signature cue itself; (c) the imprinting/familiarity critical-period
mechanism; (d) role-based reproductive priming; (e) pair-bond maintenance/dissolution dynamics; and (f)
the spawn-time kinship structure. Each below.

---

## 2. The five grounded mechanisms

### 2.1 The OT/VP nonapeptide bonding pathway (receptor-sign the existing edges + complete)
The core: oxytocin makes a *specific conspecific's* cues rewarding (OT receptors in NAc/reward →
social cues gain incentive salience), and vasopressin supports pair-maintenance *and* territorial
aggression (the same peptide, opposite-valence depending on target/receptor).

- **Receptor-sign the existing `PVN-OT` projections** (per v12a): `PVN-OT→NAc-shell` via **OTR (Gq →
  excitatory)** — oxytocin *facilitates* reward to social cues. `PVN-OT→CeA`, `→BNST` via their cited
  receptors. Vasopressin projections (via a V1a-bearing target) → pair-maintenance in reward regions
  **and** territorial aggression via the threat system (V1a in `BNST`/lateral septum).
- **Complete the pathway** where the reward-gating requires an edge that isn't present (to be
  enumerated at build against v13 — e.g. OTR modulation of `VTA` DA to social cues).
- Grounding: oxytocin/vasopressin in NAc/VTA reward pathways gate pair-bond and parental behaviour
  (Young & Wang; the prairie-vole OTR/V1a-in-reward literature — *Nat. Neurosci.*/*Science*); the
  formation, maintenance, and expression of pair bonds is regulated by mesolimbic dopamine + OT/VP
  (Walum & Young 2018, *Nat. Rev. Neurosci.*).
- **Honesty:** the bond is not coded — OT/VP *gate whether a conspecific's cues are rewarding*; whether
  a bond forms **emerges** from repeated rewarding interaction with that specific individual.

### 2.2 The perceptual signature + phenotype matching (where relatedness enters — as a CUE)
Each agent presents an innate **genetic-fingerprint cue** — the MHC/scent analogue — a stimulus on
`IN-OLF`/`IN-CONSPEC`. Shared DNA sets how *similar* two agents' signatures are (parent-child ~50%
similar; full sibs ~50%; cousins ~12.5%; unrelated ~0). The perceiver's recognition circuits
(`MeA`→`aIns`/`dmPFC` self-referent matching) respond to *similarity-to-self* — and that perceived
similarity feeds affiliation (nepotism) and, in a mate-choice context, aversion (incest-avoidance).

- **Spawn:** each agent gets a signature vector; relatedness between any two agents sets their
  signature *similarity* (a bearer property — like physical stimulus in v10, sex-neutral, pure bearer).
- **Perception:** `felt_response` presents the bearer's signature; the perceiver's own circuits compute
  similarity-to-self (self-referent matching — grounded in the insula/dmPFC substrate) and the
  affiliative/aversive response **emerges**.
- Grounding: self-referent phenotype matching / the "armpit effect" (Mateo & Johnston 2000); MHC-linked
  odour kin cues (the mouse/frog/human MHC literature); the human architecture of kin detection
  (Lieberman, Tooby & Cosmides 2007 — which identifies *co-residence duration* and *maternal
  perinatal association* as the actual human kinship cues, NOT relatedness detection).
- **Honesty:** relatedness never touches behaviour — it sets signature similarity; nepotism and
  incest-aversion **emerge** from matching. "% shared DNA" is a cue-similarity scalar, never a bond
  value. This is the keystone made concrete.

### 2.3 The imprinting / familiarity critical-period mechanism (the household-bond engine)
The dominant kinship mechanism needs **no relatedness at all**: agents co-located during an early
critical window build a **familiarity template** of each other, and familiar-from-early-life is treated
as kin. This is why adoption/cross-fostering work and why the Westermarck effect produces incest-
aversion from co-rearing regardless of blood.

- **Mechanism:** a developmental critical window (like the existing plasticity schedule, but a
  bonding-specific sensitivity period) during which co-present conspecifics' cues are preferentially
  learned — an OT-gated plasticity on the recognition/reward association for co-located individuals.
- Grounding: Bowlby's attachment critical period (~first 2.5y; Bowlby 1969); Lorenz filial imprinting
  (critical period, first moving figure); the Westermarck effect (co-rearing → incest-aversion —
  Lieberman/Tooby/Cosmides; Rantala & Marcinkowska); the proto-attachment→attachment transition
  (Frontiers 2022, imprinting↔attachment re-evaluation).
- **Honesty:** the bond is not assigned to co-reared agents — co-rearing *opens the plasticity* by
  which their cues become familiar/rewarding; the bond **emerges** from the interactions lived in that
  window. Whoever is present bonds — kin, step-kin, adoptive — by the same mechanism, which is
  biologically correct.

### 2.4 Role-based reproductive priming (the parent/infant asymmetry)
Separate from relatedness-reading: the *reproductive event* primes the parent, and the infant is
innately dependent.

- **Parent priming:** the parturition/lactation event drives an OT/VP surge → `MPOA` care-hub
  readiness + OT-gated reward to the infant's cues. Maternal-biased (gestation/lactation), with
  non-gestational parents bonding via the co-rearing route (2.3).
- **Infant dependency:** an innate high-dependency starting state — distress-signalling +
  proximity-seeking + distress-relief-is-rewarding (the `SEPT` separation-distress system, present).
  The infant becomes attached to whoever *reliably relieves its distress* (the secure-base mechanism).
- Grounding: OT/VP priming of parturition/lactation and maternal care (Pedersen; the MPOA parental
  literature); "infants attach to the individual who most reliably responds to distress" (Bowlby;
  Ainsworth; the HPA-buffering secure-base work — *Trends Cogn Sci* 2018); distress-relief as innate
  reinforcer.
- **Honesty:** priming is tied to the *event/role* (gave birth / lactating / soothes distress), an
  innate starting state — not to a relatedness value. The bond still **emerges** from the caregiving
  interactions; priming sets the readiness, not the outcome.

### 2.5 Pair-bond maintenance & dissolution (fractiousness, separation, the child-link)
Pair bonds form, are *maintained by ongoing rewarding interaction*, and *dissolve* when the maintaining
signal decays — and the dissolution has a measured neural correlate.

- **Maintenance:** the pair bond is an OT/VP-gated reward association with the partner, sustained by
  continued positive interaction (and the nonapeptide plasticity that accompanies bonding).
- **Dissolution:** when positive interaction drops or conflict rises, the maintaining reward signal
  decays and the nonapeptide populations return toward pre-bond baseline — separation/divorce
  **emerges** as the bond falls below the threshold that keeps agents co-located. Grounding: pair bonds
  dissolve and re-form with measured PVN OT-neuron plasticity returning to pre-bond baseline after
  dissolution (Scientific Reports 2023, prairie-vole bond-dissolution).
- **Fractiousness & confinement:** vasopressin drives *both* pair-maintenance and *territorial
  aggression*; in a confined space (few escape affordances — **the Arena's `escape = len(present)`
  already models this**), forced proximity means more unavoidable encounters, and whether each engages
  the bonding or the threat system **emerges**. Confinement doesn't code conflict — fewer escape routes
  → more forced interaction → more opportunity for the threat system to engage.
- **The child-link altering the couple's bond:** shared caregiving to an infant is shared rewarding
  (or stressful) interaction — it **emerges** as a modifier of the pair bond, not a coded rule. A child
  can strengthen (shared positive caregiving) or strain (shared stress in confinement) the pair bond,
  discovered by measurement.
- **Honesty:** divorce/fractiousness are never scripted events — they emerge from the maintaining
  signal decaying and the threat system engaging. This is exactly what lets the model *study* what
  makes bonds break.

### 2.6 Household membership & the relocation framework (structural — the seam v15 expands)
**This is a different KIND of mechanism from 2.1–2.5.** Those are *neural* (bonds that emerge from the
substrate). This is *structural/spatial* — which household an agent belongs to. The honesty discipline
therefore applies differently: a **bond** must emerge (neural, never coded), but **household
membership** is a *fact* (structural — legitimately set and changed, like kinship facts). What must
stay honest is the **trigger**: relocation is *driven by* emergent states, never scheduled by a rule.

v14 adds the **minimal framework** — just enough that its own dissolution mechanism (2.5) has a
consequence. A pair bond that decays but leaves the partners still sharing a home is hollow; divorce
must be able to *mean* something. The full generational/economic relocation model is **v15** (§5);
v14 builds only the seam it plugs into.

- **Household membership as a mutable structural fact:** an agent belongs to a household; membership
  can change. (A household = a co-located set of agents — the thing the Arena and the town spawn.)
- **A relocation primitive:** *agent departs household A → forms or joins household B.* Structural, an
  action/event — not a psychological outcome, so not subject to the emergence rule the way a bond is.
- **CRITICAL — the primitive is GATEABLE by conditions.** The departure is gated on a *condition* the
  caller supplies, so v15 can add economic/resource gates (can the agent afford to leave?) *without
  reworking the primitive*. In v14 the only gate is the dissolution trigger; v15 adds the rest.
- **The v14 dissolution hook (the only trigger v14 wires):** when a pair bond decays below the
  co-location threshold (emergent, from 2.5), the relocation primitive fires → one partner's household
  membership changes (they leave to a new/other household). **Emergent trigger, structural mechanism** —
  the *decision* to leave emerges from the bond decaying; the *act* of moving is structural.
- **Honesty:** relocation is not scripted ("divorce at year 15"). It is *driven* by the emergent
  bond-decay from 2.5. v14 wires exactly one trigger (dissolution → one partner relocates); every other
  trigger is v15.
- **Scope marker:** v14 = the framework + the dissolution hook ONLY. Children-leaving-home, household
  formation/merging on new pair bonds, and the entire economic/resource/housing machinery are **v15**
  (§5). The framework is built so v15 plugs in by adding *gated triggers*, not by reworking membership
  or the primitive.

---

## 3. What is SET at spawn vs. what EMERGES (the honesty ledger)

| SET at spawn (facts / innate mechanisms — legitimate inputs) | EMERGES + is measured (never coded) |
|---|---|
| Kinship *facts*: B is parent/sibling/mate of C | The **bond** (parent-child, sibling, pair): its strength |
| Each agent's **perceptual signature**; relatedness sets signature *similarity* | Nepotism (kin-directed affiliation) + incest-aversion |
| **Co-rearing arrangement** (who shares the household in the critical window) | Which bonds form (co-reared bond; the household) |
| **Reproductive priming** (parturition/lactation primed the parent; infant innately dependent) | The parent-infant attachment (from caregiving interaction) |
| The **OT/VP pathway, imprinting window, distress-relief reinforcer** (innate machinery) | **Fractiousness**, **separation/divorce**, the child-link effect |

The left column is inputs (facts + innate machinery); the right column is discovered. Relatedness sets
cues and priming sets readiness; **no bond, and no bond's breakdown, is ever a coded value.**

---

## 4. The Arena & the main UI (why this was the trigger)

- **The Arena** can then define a **household**: a roster with kinship *facts* (parents, children,
  siblings), signatures, and co-rearing — and the bonds, the fractiousness under confinement, the
  potential separation all **emerge** and are observed at high detail. This is what "properly define a
  household" requires, and it's why the Arena revealed the gap.
- **The main model** gets the same: town families spawn with kinship structure, and family dynamics
  (bonding, conflict, separation) emerge over the life course — the dynamic the researcher correctly
  noted is currently missing everywhere, not just the Arena.
- Neither is a coded relationship system — both consume the emergent bonds from the substrate.

---

## 5. Scope, phasing, and the honest flag on size

This is a **substantial organism pass (v14)** — but, per §1, *smaller than physical-endowment* because
the OT/VP scaffold largely exists. It decomposes into natural phases (phasing decided at review):

- **Phase 1 — the bonding pathway:** receptor-sign the existing OT/VP projections + complete the
  OT→reward gating. *(Parent-child and any bond can now form via co-rearing + OT-gated reward.)*
- **Phase 2 — the signature + phenotype matching:** the genetic-fingerprint cue, relatedness→similarity,
  self-referent matching. *(Nepotism + incest-aversion emerge; relatedness enters honestly.)*
- **Phase 3 — imprinting window + role priming:** the critical-period familiarity plasticity + the
  parent/infant asymmetry. *(The household-bond engine + the parent-child asymmetry.)*
- **Phase 4 — pair-bond maintenance/dissolution + confinement fractiousness:** the maintenance-decay
  dynamics + the child-link. *(Divorce/separation/fractiousness emerge; the Arena household is
  complete.)*
- **Phase 5 — spawn-time kinship structure (both Arena & town) + the relocation framework (2.6) + the
  UI:** who is kin of whom, co-rearing arrangement, household membership as a mutable fact, the
  relocation primitive + the dissolution hook, and the household-definition UI. *(The Arena household is
  complete and can dissolve; divorce has a structural consequence.)*

**The follow-on: v15 — generational relocation & the economic layer (a separate spec).** v14 builds the
relocation *framework* (2.6); v15 builds the *depth*: children-leaving-home, household
formation/merging on new pair bonds, and the **economic/resource/housing machinery** that gates
relocation (can an agent afford to leave? housing cost, the resource/SES model). This is a large,
distinct socio-economic domain — it deserves its own spec, and it plugs into v14's gateable relocation
primitive by adding *gated triggers*, not by reworking the framework. **Honesty flag for v15:** economic
effects enter as **structural constraints and perturbation patterns**, never coded outcomes — "low SES
delays leaving home" would be the same trap as "low SES → worse CU." The honest form: resources are a
structural fact, housing has a cost, and whether/when relocation happens *emerges* from whether
resources meet the threshold — discovered, not scripted. Essential for generational simulations;
specced after v14 lands.

Each phase: byte-additive, receptor-signed, real citations, full re-verification (v9 closure, the
phenomena battery, DA stability, the silence/emergence tests), reviewed before the next. The keystone
(§0) is the acceptance gate for every phase: **grep-clean of any relatedness→bond or kinship→behaviour
coded term; every bond a measured/emergent read-out.**

**Verification unique to v14:** an emergence test analogous to the aggression neutral-floor —
*co-rearing unrelated agents produces a bond* (proves the bond is from co-rearing, not relatedness);
*relatedness without co-rearing does NOT auto-produce a bond* (proves relatedness alone isn't coded to
bond); *incest-aversion emerges between co-reared agents regardless of actual relatedness* (the
Westermarck check). These three are the honesty proof, the way the neutral-floor was for aggression.

---

## 6. Open items for researcher decision (at review)
1. **Phasing** — all five as one pass, or staged (my lean: staged, Phase 1–2 first, since they're the
   core mechanism and the rest builds on them).
2. **Before or after the CU study?** — this reopens the organism; the CU study was gated on complete
   *aggression-regulation* anatomy (now met). Kinship/attachment is a *different* domain — the CU study
   may not need it, OR family structure may be central to the developmental-origins question the CU
   study asks. **Researcher's call whether v14 precedes the study.**
3. **Signature representation** — the dimensionality/form of the genetic-fingerprint cue (a scalar
   similarity, or a vector matched component-wise). To resolve at build against the trigger vocabulary.
4. **Which kinship degrees** — parent-child + sibling + mate cover the household; cousins/aunts/uncles
   fall out of lower signature similarity + actual co-rearing automatically (no extra mechanism), but
   confirm the spawn structure should represent them.

---

## 7. Grounding (verified citations to pin at build)
- Bowlby 1969 *Attachment and Loss* (attachment critical period, secure base); Lorenz 1935 (filial
  imprinting critical period); Ainsworth (Strange Situation, distress-relief bond).
- Mateo & Johnston 2000 *Proc R Soc B* 267:695 (self-referent phenotype matching / armpit effect);
  Lieberman, Tooby & Cosmides 2007 *Nature* 445:727 (human kin-detection architecture: co-residence +
  perinatal association as the cues); the insula/dmPFC olfactory kin-recognition substrate.
- Walum & Young 2018 *Nat Rev Neurosci* (OT/VP in pair-bond formation/maintenance/expression); the
  prairie-vole OTR/V1a-in-reward literature (Young & Wang); Scientific Reports 2023 (PVN OT-neuron
  plasticity in pair-bond dissolution).
- Westermarck 1891 / Rantala & Marcinkowska (co-rearing → incest-aversion); Trivers (parent-offspring
  conflict — for the sibling-competition tension).
- Each edge's `dominant_receptor` cited at build (OTR/V1a/etc.), per the v12a convention.

---

*This spec adds the machinery for kinship, attachment, and pair-bonding to emerge — grounded, cited,
and structurally unable to code a bond. Relatedness sets cues; bonds are discovered. Nothing is built
until the researcher reviews and rules on phasing and study-sequencing.*

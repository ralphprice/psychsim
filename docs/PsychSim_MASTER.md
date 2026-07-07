# PsychSim — Master Design & Build Document

*Single authoritative reference for building the valence/motivation subsystem of PsychSim. This
document consolidates the session's design, code-change map, build instructions, and calibration/
validation plan into one entry point. Point a Claude Code session at this file; **Part III is the
executable plan**, and the invariants in §1 are non-negotiable throughout.*

---

## 0. How to use this document

- **Read §1–§4 first** (this front matter): the invariants, the scope, the architecture overview, and
  the substrate context. They make the rest self-contained.
- **Part I** is the *design* (what to build and why), the authoritative specification of the valence
  engine, state vector, learning, selection, matrices, endowment, development, and the study plugin.
- **Part II** is the *code-change map* (which real files change, and how).
- **Part III** is the *build instructions* — the dependency-ordered, test-gated phases Claude Code
  executes. Work one phase at a time; commit at each acceptance gate.
- **Part IV** is the *calibration and validation plan* (how the scaffold numbers get set and how the
  model is tested — the decisive concordance gate).
- **Part V** is the consolidated reference list and the data-verification summary.

Deeper background that this file references but does not reproduce (kept in `docs/`): the full
neural-substrate design document, the social-valence research memo, and the verified reference
workbook (`PsychSim_source_references_VERIFIED.xlsx`). Claude Code does **not** need them to proceed;
they are for depth.

## 1. Governing discipline and invariants (non-negotiable)

The whole project rests on one rule: **the mechanism must never contain the answer.** Personality and
behaviour must *emerge* from a neutral substrate; no psychological outcome is programmed. Concretely,
in every phase of the build:

1. **Valence is computed, never stipulated.** Value = drive reduction over the interoceptive state
   vector. No literal "warm = +0.6 / harsh = −0.7" anywhere.
2. **No coded arbiter.** Nothing may read a situation and directly output a behaviour, an emotion, or
   a category. Behaviour emerges from competition among circuits; the executive sets *parameters*, not
   outcomes.
3. **Named categories are observer read-outs, not primitives.** "fear", "callousness", "boldness",
   "psychopathy" are computed *over* the agent for reporting and **never fed back**. No seed carries an
   outcome category.
4. **Only the primary-reinforcer set is innate value.** Everything richer is learned by association
   (RPE) or grounded homeostatically. The innate set is small and cited (Part I, App. B).
5. **Cognitive biases and the sophropath/psychopath divergence emerge**, they are not coded — from the
   primal systems' structural asymmetries, evolutionary mismatch, and temperament × environment.
6. **The module contract is sacred.** Do not edit `core/modular/registry.py` or `project.py`. Studies
   stay discovered plugins under `extensions/`.
7. **All new numbers are scaffold.** Every set-point, gain, rate, threshold, and capacity is a
   placeholder, collected in one params module and marked `# SCAFFOLD`, to be set only by the
   calibration plan (Part IV).
8. **Supersede legacy behind stable interfaces, with parity tests, and keep the suite green.** Small,
   reversible commits; never delete a legacy path before the new one reproduces it.

## 2. Scope and honesty

PsychSim is a **functional, illustrative** model of a developing mind — not a biophysically literal
brain, and not a claim to reproduce a human exactly. It reproduces *patterns and directions*
(orderings, dynamics, developmental shapes), **not magnitudes**. Claims are held at that level
throughout, and the calibration/validation plan (Part IV) enforces it: mechanism is calibrated on
physiology and the thesis's studies; emergent phenomena are validated on independent data; nothing is
tuned to produce the psychological result.

The reference base has been **verified**: of 115 neuroscience citations underpinning the substrate,
114 resolve to real, correctly-attributed publications (details and the handful of corrections in
Part V). A verified citation grounds a pathway's *existence and direction* — never the substrate's
assumed weights, time-constants, or plasticity curves, which remain scaffold until calibrated.

## 3. Architecture at a glance

One pass through the whole system, so the parts below have a place to sit:

- A **category-free neural substrate** (nucleus-level circuits) receives sensory, proprioceptive, and
  **interoceptive** input and settles into activity; overlapping circuits compete. Emotion and
  behaviour are *read-outs* of this activity, never primitives (§4).
- The agent carries an **interoceptive state vector** — regulated body/need variables with set-points
  (energy, thermal, pain, arousal, social contact, …). Its distance from set-point is **drive**; the
  **reduction** of drive is **valence** (`r = β·(D_t − D_{t+1})`). This is the one valuation engine,
  and it replaces any stipulated "warm/harsh" value.
- A small, cited set of **innate perturbations** are the only hardwired event→value links (pain,
  taste hedonics, suffocation alarm, affiliative touch/contact, separation, looming/startle).
  Everything else acquires value by **reinforcement learning** — a dopamine reward-prediction-error
  rule that is the substrate's own neuromodulated plasticity — producing **anticipatory value** that
  pulls behaviour before outcomes ("wanting" vs the consummatory "liking").
- Value over classes of things is held in **three matrices** on the one engine: **relationships**
  (people; capacity-limited Dunbar slots, allocated by salience so enemies and ambivalent bonds also
  occupy them), the **environment** (objects, nature, animals, belongings), and **groups** (belonging,
  synchrony/endorphins, status, esteem).
- **Behaviour selection** is basal-ganglia action selection: candidate actions, weighted by
  anticipated value against the current drive, compete via disinhibition and accumulation-to-
  threshold; dopamine sets the gain; the **executive** biases the competition (proactive threshold,
  reactive STN "hold", conflict monitoring) — it never decides.
- Individual difference is **endowment**: the *parameters* of all the above (set-points, weights,
  neuromodulator reactivities, innate-perturbation gains, physical traits) — the only legitimate place
  a seed differs. **Epigenetics** lets early experience shift those parameters within windows.
  **Development** runs it forward: circuits mature on schedules (reward early, prefrontal into the
  mid-20s), so adolescent impulsivity and the like emerge from the maturation gradient.
- A **distilled default disposition** (the substrate's own sediment plus a pooled prior) is the
  generalised character; per-entity matrix entries are specific overrides (internal working models).
- The **observer read-out** is where the output categories legitimately live — measured over the
  agent, never fed back — and it is how the model is validated by having the simulated agent "take the
  same tests" as human participants.
- The **sophropath/psychopath study** is a **plugin** on the neutral platform: it seeds a fearless
  proto-disposition; whether it develops toward the adaptive (sophropath) or antisocial (psychopath)
  attractor **emerges** from temperament × developmental environment — the thesis's childhood-
  divergence claim.

## 4. The neural substrate (context Claude Code needs)

The valence subsystem is built *on top of* the substrate; here is what the substrate is, condensed
(full treatment in the substrate design document in `docs/`):

- **Category-free and nucleus-level.** The substrate is a catalogue of pathways/circuits/networks at
  the grain of anatomical nuclei — not "emotion systems." The reference seed carries **73 nuclei, 159
  directed connections, 19 innate-reinforcer links, across 6 domains** (threat, reward, sensory,
  executive, affiliation, interoception). Vocabulary (from the neural-designer): **circuits** (nuclei)
  → **pathways** (routings/cascades through them) → **networks** (weighted aggregates = read-outs).
- **Why nucleus-level, not functional modules.** Shared nuclei serve many roles (the amygdala does
  appetitive learning too; the NAc carries approach *and* aversion), so **internal conflict emerges
  for free** when incompatible tendencies recruit overlapping circuits and compete for the effector
  bottleneck. Functional modules ("a threat module") would re-import the output categories and force a
  hand-authored arbiter — the encoded effect the discipline forbids.
- **Plasticity is local and meaning-blind.** Connections change by pre × post × neuromodulator (a
  three-factor rule); no synapse "knows" it encodes fear. Development sculpts the weights.
- **The executive** (prefrontal nuclei + the STN brake) provides inhibition/control that matures late;
  it biases competition rather than dictating behaviour.
- **The three matrices** (relationship/environment/group) are the interfaces through which the agent's
  learned value over people, things, and groups is held — all running on the one valence engine
  specified in Part I.

## 5. What this document consolidates

This master document is the **build entry point** and supersedes the separate working files as the
single source of truth for the valence/motivation subsystem. It folds together:

- the **Valence & Motivation design specification** (Part I) — including its Appendices A–F (state
  vector; innate perturbations; RPE learning & anticipatory value; distillation & observer read-out;
  the differential-profile plugin; behaviour selection & competition);
- the **code-change map** (Part II);
- the **Claude Code build instructions** (Part III);
- the **calibration and validation plan** (Part IV);
- a **consolidated reference list and the data-verification summary** (Part V).

The full neural-substrate design document, the social-valence research memo, and the verified
reference workbook remain in `docs/` as deeper references.

---

## Part I — Valence & motivation design (specification)

### PsychSim — Valence & Motivation subsystem: design specification

*Detailed spec for how value/valence is generated in the model. Extends the category-free neural substrate summarised in the front matter (§4) and builds on the companion research memo
(`PsychSim_social_valence_research.md`). Status: design, grounded in current literature; parameters
scaffold/assumed until calibrated. The honesty wall is in force throughout: **the only innate value
is a small, cited primary-reinforcer set; every richer value is computed or learned; nothing is
labelled by the designer.***

---

#### 0. The one principle

There is **one valence engine**, and everything that has value for an agent — people, objects,
nature, animals, belongings, groups — draws its value from it. Value is never stipulated ("warm =
good"); it is **computed** as the reduction of a homeostatic drive, grounded in primary reinforcers,
with rich secondary value **learned** by reward-prediction-error. The three interface matrices
(relationship, environment, group) are not three mechanisms; they are **three domains of acquired
value running on the same engine**, differing only in which primary reinforcers and which learned
associations they engage.

This replaces the current code's stipulated valence (`development.py` hand-sets `social_valence`,
warm/harsh) with an emergent quantity — the change that makes "a punishment for one is a reward for
another" *true* rather than decreed.

---

#### 1. The primary-reinforcer set (expanded, with grounding)

The substrate's innate value must be widened beyond the current 19 links, because the evidence is
that **affiliation is itself partly primary** (not derived from feeding/pain), and value also has
non-social and embodied sources. Three classes:

**1a. Non-social physiological primaries** (homeostatic variables with set-points): tissue
damage/nociception (already present), thermal comfort, energy/nutrition, fatigue/rest, autonomic
arousal. These ground survival value and, via the autonomic/interoceptive system already in the
seed, supply the bodily signal affect is read from.

**1b. Social primaries** (the key expansion): a **social-contact variable with a set-point**
(social homeostasis), plus the innate channels that move it — affiliative **C-tactile touch**,
**caregiver proximity/attachment**, and **separation-distress**. These are grounded, not invented:
- Social contact behaves like a homeostatic need with a detector / set-point / effector loop, and
  isolation is an aversive deficit that motivates reconnection (Matthews & Tye, 2019; Lee, Chen &
  Tye, 2021).
- The **endogenous-opioid** system that handles physical **pain** is co-opted for social bonding
  and separation distress — social rejection shares the pain substrate, and blocking µ-opioids
  (naltrexone) causally reduces felt connection (Machin & Dunbar, 2011; Løseth et al., 2024). This
  is why exclusion should be grounded in the shared pain variable (the group matrix already gestures
  at "exclusion presents separation and pain").
- **Oxytocin** acts as the social-reinforcement *gate*: it enables the plasticity (in NAc core, via
  serotonergic 5-HT1B input) that lets social cues acquire value *in the standard reward circuit*
  (Dölen et al., 2013). Oxytocin does not carry a "social = good" number — it gates learning.

**1c. Innate biases / detectors** (priors on *what* acquires value, not values themselves): looming,
face, biological-motion, and voice orienting (already present); **prepared-fear** biases for
ancestral threats such as snakes/spiders (Öhman & Mineka, 2001; Cook & Mineka, 1990 — both in the
substrate's verified reference set); and **biophilia**, an innate affinity for natural/living
environments (Wilson, 1984). These bias which stimuli the developing system readily attaches value
to; they are not value assignments.

*Design rule:* 1a and 1b are homeostatic variables and their innate channels; 1c are detectors that
weight learning. Individual differences in the **reactivity** of any of these (a low-fear, high-
affiliation newborn vs the reverse) are temperament — endowment, never outcome (§5).

---

#### 2. The valence computation — the process, in full

**2.1 State and drive.** The agent carries an interoceptive/homeostatic **state vector** `H` (the
variables of §1a–1b) with **set-points** `H*`. The **drive** is the weighted distance from
set-point:

> `D = Σ_k w_k · dist(H_k, H*_k)`

where the weights `w_k` are part of the endowment (how much each need matters to *this* agent).

**2.2 Valence = drive reduction.** The valence of any outcome is the drop in drive it produces
(homeostatic reinforcement learning; Keramati & Gutkin, 2011, 2014):

> `r(t+1) = β · ( D(t) − D(t+1) )`

Positive when an outcome moves the internal state toward set-point (relief, satiation, contact,
safety, warmth), negative when it moves away (pain, threat, isolation, loss). This `r` is the
interoceptive read of §4 in the memo — the "felt" value — and it is what gets written to memory. It
is **computed from the agent's own state**, so the same external event yields different `r` in
different agents.

**2.3 Neuromodulatory gates.** Gates mark *domain* and *enable plasticity*, they do not add value:
oxytocin/serotonin gate social-cue value in NAc (Dölen); µ-opioid marks consummatory "liking" and
carries the social/pain overlap; dopamine carries the **reward-prediction error** used for learning
(§2.5). These are the neuromodulators already named on the seed's connections.

**2.4 The interaction loop (relationship case, generalises to all three matrices).**
1. **Perceive** the other/object/group: sensory streams + (for persons/groups) exchanged
   **speech-acts** enter the substrate as stimuli (the speech layer feeds appraisal).
2. **Activate**: the substrate settles — overlapping circuits compete (front-matter §3–§4); a behaviour
   (including a speech-act) is emitted.
3. **Outcome**: the world (often *another agent's* substrate output) responds, changing `H`
   (a warm response raises the social-contact variable and, via opioid, lowers pain/arousal; a
   hostile one raises threat/arousal and the social-pain variable).
4. **Valence**: `r = β·(D_t − D_{t+1})` is computed and tagged to the episode.
5. **Learn**: (a) **use-dependent plasticity** strengthens the connections that fired (the substrate
   sediment); (b) **RPE learning** (§2.5) updates the predictive value of the cues present; (c) the
   **relationship matrix** updates its per-partner value and expectation; (d) the **executive**
   installs/updates monitors from remembered outcomes (reversal learning — already sketched in
   `executive.py`).

**2.5 What is learned (secondary/predictive value).** Neutral cues — a face, a name, a tone, a word,
an object, a place, a group emblem — that predict drive-changing outcomes acquire value through
dopaminergic reward-prediction-error learning (Schultz — verified in the substrate set). This is
where the rich, individual, relationship- and object-specific value lives, and it is what fills the
matrices. Developmentally, the agent must first detect the **contingency** between its own actions
and others' responses — caregiver responsiveness is the teaching signal, and social cues carry
enough innate incentive value to speed this (Vernetti, Smith & Senju, 2017).

**2.6 Why value is not universal.** Variation enters at four honest points, none a designer's label:
innate **set-points**; drive-function **weights** `w_k`; innate **reactivities** of the fear /
opioid / oxytocin / dopamine systems; and **learned** predictive associations. Same outcome →
different ΔD → different valence. This is the mechanism behind "a reward for one is a punishment for
another."

---

#### 3. The three matrices as domains of the one engine

Each matrix is a per-agent ledger of *acquired* value over a class of things, all computed by §2.

**3.1 Relationship matrix — persons.** Engages the social primaries (§1b); per-person learned value
and expectation (the "internal working model" of that person). Capacity-limited and slotted (§4).
Value can be strongly positive, negative, or ambivalent.

**3.2 Environment matrix — objects, nature, animals, belongings.** Same engine, different grounding:
- **Objects / tools / resources**: **instrumental** secondary value — things that reliably produce
  drive reductions (food sources, shelter, tools) acquire value by association (§2.5).
- **Nature**: grounded homeostatically — natural environments reduce autonomic arousal and stress
  (Stress Reduction Theory; Ulrich et al., 1991) and restore depleted attention (Attention
  Restoration Theory; Kaplan & Kaplan, 1989), i.e. they *reduce drive*; biophilia (§1c) is the
  innate prior that biases which features attach value (Wilson, 1984). Honest caveat: effects are
  robust for affect, weaker or mixed for physiological markers.
- **Animals / pets**: route through the **social** primaries — human–animal interaction recruits the
  same oxytocin/attachment substrate as conspecific bonding (mutual gaze raises oxytocin in owner and
  dog alike; Nagasawa et al., 2015 — with the honest caveat that the wolf-comparison sample was
  small). So a pet can legitimately occupy a *relationship* slot (§4).
- **Belongings / possessions**: instrumental value plus **identity value** — the "extended self,"
  where valued possessions become part of self-concept (Belk, 1988 — classic; confirm exact cite).
  Threat to a possession then reads partly as threat to self.

**3.3 Group matrix — groups.** "The same circuitry with additional factors," exactly as intuited.
Group belonging draws value from:
- **Belonging as a need** — the social-homeostasis / opioid machinery scaled to collective inclusion
  (the "need to belong"; Baumeister & Leary, 1995 — classic; confirm exact cite). Exclusion from a
  group engages the social-pain substrate.
- **Synchrony / collective effervescence — the key additional factor.** Coordinated, exertive group
  activity (dance, song, chant, drumming, marching, laughter, group sport) triggers **endogenous-
  opioid (endorphin) release**, measured via raised pain threshold and abolished by naltrexone
  (Tarr, Launay, Cohen & Dunbar, 2015; Tarr, Launay & Dunbar, 2017; Dunbar, 2022). This is why fan
  crowds, congregations, teams, festivals and communities bond — the same opioid channel as one-to-
  one bonding, engaged collectively. It also lets bonding scale past the limits of one-to-one
  grooming/contact.
- **Identity & self-esteem** — group membership feeds self-concept; self-esteem functions as a
  **sociometer** gauging social inclusion (Leary et al., 1995 — classic; confirm exact cite).
- **Status/rank within the group** — attained by **dominance vs prestige** (already in
  `group_matrix.py`, grounded in Henrich & Gil-White). Status is itself rewarding.

A "fan base" (for a performer/influencer) is the *inverse* view of the same mechanism — the
performer occupies group/relationship value for many others, and derives status/belonging value from
being so held.

---

#### 4. The relationship-slot architecture (Dunbar) and the enemy extension

**4.1 Layered capacity.** Relationship maintenance is cognitively and temporally costly, so it is
**capacity-limited and layered** — Dunbar's ego-network layers, each ~3× the last, with intimacy
decreasing outward and contact frequency scaling accordingly: **support clique ~5, sympathy group
~15, affinity group ~50, active network ~150** (with looser bands at ~500, ~1500) (Dunbar, 1992,
1998; Zhou et al., 2005; Hill & Dunbar, 2003). The subject's "~12 close" sits in the inner layers.
In the model: a fixed budget of high-investment inner slots and progressively larger, lower-
investment outer bands; slots **decay without contact** (the "convoy" is fluid); kin ties are
hardier (tolerate less contact before decaying).

**4.2 Slots are allocated by salience, not by positive valence — the enemy extension.** The thing
that earns an inner slot is **behavioural relevance = |salience|**, i.e. how much the other moves the
agent's drives, *regardless of sign*. A strongly **negatively-valenced** person — a rival, an
abuser, an "arch-enemy" — can therefore occupy an inner slot and control behaviour enormously
(vigilance, rumination, avoidance or approach, revenge-planning). This is grounded: **bad is stronger
than good** — negative others/events are more salient, processed more deeply, stickier and more
resistant to disconfirmation (Baumeister et al., 2001; Rozin & Royzman, 2001). Each slot therefore
carries **both** an occupancy (salience) and a **valence sign**.

**4.3 The ambivalent slot — the most behaviourally destructive case.** The worst case is not an
enemy in an enemy-slot; it is **high attachment *and* high threat directed at the *same* person** in
an inner slot (an abusive parent or partner, a betraying friend). Because the substrate is shared
(front-matter §3–§4), this co-activates the attachment and threat systems toward one target, producing
**maximal, chronic approach–avoidance conflict** — the emergent signature of attachment trauma and
coercive relationships, and a powerful driver of behaviour. This is *emergent from co-activation*,
not a coded rule, and it is a natural validation target (does the model reproduce the destructive
pull of the ambivalent bond without being told to?).

---

#### 5. The genetic, epigenetic and temperamental endowment

The valence engine needs initial conditions, and those conditions carry a great deal of what is
"with us from birth."

**5.1 Genetic endowment = the newborn's parameters.** Not behaviours, but the **parameters** of the
engine: homeostatic **set-points**, drive-function **weights** `w_k`, and the innate **reactivities**
of the neuromodulator systems (fear/amygdala, opioid, oxytocin, dopamine), plus the physical traits
(attractiveness, congenital health, dexterity) as initial conditions that change *what the world does
to the agent* (front-matter §3). **This is the only legitimate place a "seed" differs** — e.g. a
sophropath vs psychopath proto-seed would differ in fear-system reactivity, affiliation set-point,
opioid/oxytocin sensitivity, and reward weighting — all as initial conditions, never as encoded
outcomes.

**5.2 Epigenetic layer = experience rewriting the parameters, early and semi-permanently.** Early
experience (especially caregiving and adversity) can shift these parameters within developmental
windows and hold them shifted — the mechanism the thesis's Study 3 targets. Concretely: early
maternal separation / adversity can raise threat-system reactivity and lower oxytocin-system function
(OXTR promoter methylation associated with environmental risk and callous-unemotional traits; Cecil
et al., 2014 — in the thesis reference set). In the model this is a **slow, early-window modifier**
that reads accumulated early experience and adjusts the endowment parameters, after which they
persist. It is how "nature" and "nurture" meet in one variable set, and it connects the substrate
directly to Study 3.

**5.3 Cognitive biases — derived, not coded (the honesty-critical point).** Biases must **emerge**
from the architecture, because hand-coding them would be exactly the encoded psychological effect the
project forbids. Two emergent sources:
- **Structural asymmetries of the primal systems.** Negativity bias / loss aversion emerge from a
  fast, low-threshold, slow-to-extinguish threat system set against a slower reward system (amygdala
  low-road, prepared fears, slow vmPFC extinction). Hyperbolic/steep discounting and impulsivity
  emerge from the competition between fast limbic reward circuits and slow prefrontal control — and,
  crucially, from the **maturation gradient** (§6), which is why they peak in adolescence.
- **Evolutionary mismatch.** The primal systems were calibrated for the ancestral environment; placed
  in a modern one they **misfire** — sugar as a super-normal reinforcer, social-media approval as a
  super-normal social reinforcer, feeds hijacking novelty/SEEKING. The mismatch (and the biases it
  produces) is the *emergent consequence* of wiring the primal systems faithfully and running them in
  a modern environment — not a coded bias. **Reproducing known biases without coding them is a
  validation win, not a modelling shortcut.**

---

#### 6. Development across the life course (infant → child → adolescent → adult)

Everything above is **developmentally dynamic**: the same wiring produces different behaviour at
different ages because circuits come online on schedules and mature at different rates (the seed's
`developmental_online_age` and plasticity schedules already encode this).

- **Critical periods.** Sensory and social-reward learning have windows (experience-expectant
  plasticity; social-reward learning has an oxytocin-gated critical period — Nardou et al., 2019).
  Early experience within windows sets epigenetic parameters (§5.2).
- **The maturation gradient and adolescence.** The reward/socioemotional systems (ventral striatum,
  amygdala, vmPFC) mature **early**; the prefrontal control system matures **late** (into the
  mid-20s). Adolescent impulsivity and risk-taking are the **emergent** product of that imbalance —
  reward-driven motivation outpacing an immature brake — not a coded "adolescent risk" rule (dual-
  systems / maturational-imbalance model; Steinberg, 2010; Casey et al., 2008; Shulman et al., 2016).
  This is already latent in the substrate's onset ages; it needs only to be exercised.
- **The distilled default vs specific overrides.** Across development, the sediment of all valued
  interactions becomes the **distilled default disposition** (the "master copy" — largely the
  substrate's strengthened weights plus a generalised social-expectation prior), while the matrices
  hold **specific overrides** for known persons/objects/groups (Bowlby's internal working models,
  now with a learning mechanism). Novel encounters get the default; known ones get the modulated
  version.

---

#### 7. Implementation implications for PsychSim

- **Add an interoceptive/homeostatic state vector** with set-points to the agent (extend the
  interoception/autonomic system already in the seed), covering the §1a–1b variables.
- **Replace stipulated valence with computed valence.** The hand-set `social_valence`/warm–harsh in
  `development.py` becomes `r = β·(D_t − D_{t+1})` over that vector. *(This is the single most
  important honesty fix in the subsystem.)*
- **Neuromodulators as gates on plasticity**, not values (oxytocin/5-HT gate social-cue learning;
  dopamine carries RPE; µ-opioid marks consummatory value and the social/pain overlap).
- **Add RPE learning** so cues (social, object, place, group) acquire predictive value from the
  agent's own experience — the mechanism that fills all three matrices.
- **Generalise the three matrices onto the one engine**; add to the **relationship matrix** the
  layered-slot capacity with per-slot salience *and* valence sign (enabling the enemy/ambivalent
  cases); add to the **group matrix** the synchrony/endorphin, belonging, sociometer and status
  factors; generalise the **environment matrix** to objects/nature/animals/belongings with their
  respective groundings.
- **Add the endowment layer** (genetic parameters: set-points, weights, reactivities, physical
  traits) and the **epigenetic early-window modifier** driven by early experience.
- **Do not code cognitive biases**; let them emerge from the primal-system asymmetries and the
  modern environment, and treat their emergence as validation.
- **Keep the honesty wall**: local, meaning-blind plasticity; the only innate value is the
  §1 primary-reinforcer set; everything else computed or learned.

---

#### 8. Honesty ledger (what is grounded vs scaffold vs assumed)

- **Well-grounded (mechanism/direction):** affiliation as partly primary; the opioid/pain overlap;
  oxytocin as a social-reinforcement gate; value as homeostatic drive reduction; RPE learning of
  secondary value; synchrony→endorphin group bonding; layered relationship capacity; negativity
  bias; the maturation-gradient account of adolescence; epigenetic tuning of endowment.
- **Scaffold/assumed (quantities):** the set-points, drive-function weights `w_k`, the scaling β,
  learning rates, plasticity schedules, slot budgets and decay rates, and the exact mapping from
  events to ΔH. All are placeholders to be calibrated (to the human studies, Study 2/Study 5),
  confidence-coded, never asserted.
- **Frameworks that are young or normative:** social homeostasis (young; set-point/detector/effector
  partly mapped); homeostatic RL (normative idealisation, laid over the substrate as a functional
  overlay — consistent with our functional-illustrative scope, not a claim the brain runs the
  equation); "biases emerge, not coded" (a hypothesis *and* a validation target).
- **Evidence base:** much of the circuit-level work is rodent (social homeostasis, Dölen, opioid
  bonding) applied to a human model; and several human effects (nature, synchrony) are robust for
  affect but noisier for physiology. Carry the caveat.

---

##### References (verified this session with DOIs unless flagged)

**Verified this session:**
- Baumeister, R. F., Bratslavsky, E., Finkenauer, C., & Vohs, K. D. (2001). Bad is stronger than good. *Review of General Psychology, 5*(4), 323–370. https://doi.org/10.1037/1089-2680.5.4.323
- Dölen, G., Darvishzadeh, A., Huang, K. W., & Malenka, R. C. (2013). Social reward requires coordinated activity of nucleus accumbens oxytocin and serotonin. *Nature, 501,* 179–184. https://doi.org/10.1038/nature12518
- Keramati, M., & Gutkin, B. (2014). Homeostatic reinforcement learning for integrating reward collection and physiological stability. *eLife, 3,* e04811. https://doi.org/10.7554/eLife.04811
- Løseth, G. E., et al. (2024). Endogenous mu-opioid modulation of social connection in humans: a systematic review and meta-analysis. *Translational Psychiatry, 14,* 379. https://doi.org/10.1038/s41398-024-03088-3
- Matthews, G. A., & Tye, K. M. (2019). Neural mechanisms of social homeostasis. *Annals of the New York Academy of Sciences.* https://doi.org/10.1111/nyas.14016
- Nagasawa, M., et al. (2015). Oxytocin-gaze positive loop and the coevolution of human–dog bonds. *Science, 348,* 333–336. https://doi.org/10.1126/science.1261022
- Rozin, P., & Royzman, E. B. (2001). Negativity bias, negativity dominance, and contagion. *Personality and Social Psychology Review, 5*(4), 296–320.
- Steinberg, L. (2010). A dual systems model of adolescent risk-taking. *Developmental Psychobiology, 52,* 216–224. https://doi.org/10.1002/dev.20445
- Strang, N. M., Chein, J. M., & Steinberg, L. (2013). The value of the dual systems model of adolescent risk-taking. *Frontiers in Human Neuroscience, 7,* 223. https://doi.org/10.3389/fnhum.2013.00223
- Tarr, B., Launay, J., Cohen, E., & Dunbar, R. (2015). Synchrony and exertion during dance independently raise pain threshold and encourage social bonding. *Biology Letters, 11,* 20150767. https://doi.org/10.1098/rsbl.2015.0767
- Ulrich, R. S., et al. (1991). Stress recovery during exposure to natural and urban environments. *Journal of Environmental Psychology, 11,* 201–230.
- Vernetti, A., Smith, T. J., & Senju, A. (2017). Gaze-contingent reinforcement learning reveals incentive value of social signals in young children and adults. *Proceedings of the Royal Society B, 284,* 20162747. https://doi.org/10.1098/rspb.2016.2747
- Dunbar, R. I. M. (2022). Laughter and its role in the evolution of human social bonding. *Philosophical Transactions of the Royal Society B, 377,* 20210176. https://doi.org/10.1098/rstb.2021.0176

**Already verified in the substrate's own reference set (earlier work):** Barrett & Simmons (2015); Seth (2013); Craig (2002); Schultz (1997); Öhman & Mineka (2001); Cook & Mineka (1990); Nardou et al. (2019); Cecil et al. (2014, thesis refs).

**Classic / standard, cited from established knowledge — confirm exact citation before thesis use:**
Wilson, E. O. (1984). *Biophilia.* Harvard UP. · Kaplan, R., & Kaplan, S. (1989). *The Experience of Nature.* · Dunbar, R. I. M. (1992). Neocortex size as a constraint on group size in primates. *J. Human Evolution* / (1998) The social brain hypothesis. *Evolutionary Anthropology.* · Zhou, Aleman & Dunbar (2005); Hill & Dunbar (2003). · Baumeister, R. F., & Leary, M. R. (1995). The need to belong. *Psychological Bulletin, 117,* 497–529. · Leary, M. R., et al. (1995). The sociometer hypothesis. *JPSP.* · Belk, R. W. (1988). Possessions and the extended self. *J. Consumer Research, 15,* 139–168. · Bowlby, J. (1969). *Attachment.* · Csibra, G., & Gergely, G. (2009). Natural pedagogy. *TiCS.* · Keramati & Gutkin (2011), *NIPS 24.* · Casey, Jones & Hare (2008), *Ann. NYAS*; Shulman et al. (2016), *Dev. Cogn. Neurosci.*

---

### Appendix A — The interoceptive state vector (concrete specification)

*The object every valence computation reads from (§2). This appendix fixes the actual variables,
their set-points, and the rules for operating on them. Grounded where possible; all numeric
parameters are scaffold until calibrated to the human studies.*

#### A.1 Four design decisions that shape the vector

**(1) Variables vs perturbations — the honesty wall for the vector.** The vector holds only
*regulated body/need states*. Threats, rewards, social outcomes, objects and people are
**perturbations** that move these variables — never variables themselves. There is no "threat
variable" and no "reward variable": a threat raises arousal and pain-anticipation, a warm response
reduces a social or arousal deficit, and valence is the resulting drive change. This keeps the output
categories out of the state, exactly as the substrate does.

**(2) The drive is a vector, and it does two jobs.** From the state we compute (a) a **per-variable
drive** `d_k = w_k · dist(H_k, H*_k)`, which *directs behaviour to the right consummatory action* —
hunger → seek food, loneliness → seek company, cold → seek warmth, uncertainty → explore; and (b) a
**scalar aggregate** `D = Σ_k d_k`, whose change gives the overall valence `r = β·(D_t − D_{t+1})`
used for RPE learning and mood. Both are needed: the scalar says *how good or bad*, the vector says
*what to do about it*. This is why "negative valence" alone is insufficient — hunger and loneliness
are both negative but demand different behaviour.

**(3) Set-points are fixed or allostatic.** Some are near-fixed (thermal, osmolality, blood gases,
tissue integrity). Others are **allostatic** — predictively recalibrated by experience (Sterling &
Eyer, 1988; McEwen, 1998; Sterling, 2012): the arousal/stress baseline, the social-connection
set-point, and the epistemic tolerance all shift with the environment the agent has lived in. This
recalibration is the mechanism by which **development, chronic environment, and epigenetics move the
vector**: a chronically threatening early environment raises the arousal baseline and lowers its
threshold (allostatic load); a socially impoverished one recalibrates the social set-point. It ties
this vector directly to §5.2 (epigenetics), §6 (development) and the thesis's Study 3, and it
explains — at the physiological level — why a situation stressful to one agent is not to another.

**(4) Weights and drive-function shape are endowment + state.** `w_k` (how much each need matters to
this agent) is partly innate temperament and partly state-dependent (a starving agent weights energy
more; a standard homeostatic-RL property). `dist()` may be non-linear (steeper near danger). All are
scaffold parameters. Congenital health (a physical-traits endowment, front-matter §3) enters here as
altered baselines/reactivities — e.g. a chronic-pain condition raises the pain baseline.

#### A.2 The variables

Anatomical afferents are given at the textbook level; they map onto the seed's
`interoception_autonomic` circuits (NTS, parabrachial, insula, hypothalamic PVN/arcuate/preoptic,
and the amygdala CO2/acid detector), not onto invented nodes.

##### I. Physiological survival — homeostatic, innate, near-fixed set-points, online at/near birth

| Variable | Senses (afferent) | Set-point (type) | Deficit / deviation | Principal reducers | Status |
|---|---|---|---|---|---|
| Tissue integrity / nociception | nociceptors → posterior insula | zero damage (floor) | pain | healing, analgesia, endogenous opioid; social soothing (shared opioid) | grounded; innate reinforcer (present in seed) |
| Energy / satiety | glucose, ghrelin/leptin, gut vagal → NTS, arcuate | adequate reserve (fixed-ish) | hunger | feeding (releases opioids) | grounded |
| Hydration / osmolality | osmoreceptors (OVLT/SFO) → hypothalamus | normal osmolality (fixed) | thirst | drinking | grounded |
| Thermal comfort | thermoreceptors → preoptic hypothalamus, PBN | comfort band ~37 °C (fixed) | cold / heat discomfort | thermoregulatory behaviour, contact warmth | grounded |
| Respiratory / chemostasis (CO2/O2/pH) | chemoreceptors; amygdala CO2/acid (ASIC1a) | normal blood gases (fixed) | air hunger / suffocation alarm | breathing (grounds panic/suffocation fear) | grounded (Ziemann et al. 2009, verified) |
| Rest / sleep pressure | adenosine, circadian → hypothalamus/brainstem | rested (Process S) | sleepiness / fatigue | sleep, rest | grounded (two-process model; classic) |

##### II. Autonomic / stress — allostatic set-point; online early, regulation matures

| Variable | Senses | Set-point (type) | Deviation | Principal reducers | Status |
|---|---|---|---|---|---|
| Autonomic arousal / allostatic load | baroreceptors, heart rate/HRV, cortisol → NTS, insula, amygdala, PVN | low baseline (**allostatic**) | acute: physiological stress/anxiety (too high); chronic: allostatic load (slow cost) | safety, soothing, rest; social contact (oxytocin/opioid stress-buffering); nature (stress recovery) | grounded (McEwen 1998; Sterling 2012; Ulrich-Lai & Herman 2009, verified) |

##### III. Social — homeostatic with dynamic/allostatic set-points; attachment at birth, belonging widens

| Variable | Senses | Set-point (type) | Deficit | Principal reducers | Status |
|---|---|---|---|---|---|
| Attachment / proximity security | perceived proximity & availability of attachment figure(s) | felt security (dynamic) | separation distress (PANIC) | proximity, contact, responsive caregiving (opioid/oxytocin) | grounded; dominant in infancy (opioid theory; attachment) |
| Social connection / belonging | perceived inclusion, contact quantity × quality | adequate connection (**allostatic**, dynamic-range) | loneliness | affiliative interaction; group synchrony/endorphins (opioid/oxytocin) | grounded (social homeostasis; need to belong); widens across development |
| Social standing / esteem (sociometer) | perceived regard & rank | maintained standing (**allostatic**) | shame / low self-worth; status loss aversive | acceptance, competence, status gain | **tentative** — may be better modelled as a *derived/learned* value than a primal set-point (flagged) |

##### IV. Epistemic / agentic — extension, grounded in predictive regulation; develops

| Variable | Senses | Set-point (type) | Deviation | Principal reducers | Status |
|---|---|---|---|---|---|
| Uncertainty / predictability (epistemic) | prediction error / surprise about the world | tolerable uncertainty (**allostatic**) | surprise / unresolved uncertainty | exploration, learning, information-gain (curiosity/SEEKING/play) | **extension** — grounds curiosity/novelty/mastery/aesthetic reward that pure physiological homeostasis misses; least settled (allostasis-as-uncertainty-reduction + active inference; information-gap curiosity) |
| Control / agency (competence) | perceived controllability/efficacy of outcomes | sense of predictable control (dynamic) | helplessness | effective action, mastery | **tentative** — overlaps epistemic and the executive; may live at the executive layer rather than in the vector (flagged) |

Core vector = the 10 grounded variables (survival 6 + arousal 1 + attachment + belonging + epistemic).
Esteem, control/agency, and the finer sub-divisions are candidates to include or fold, flagged
above.

#### A.3 What is online when (development)

- **At / near birth:** tissue integrity, thermal, energy, hydration, CO2/suffocation, autonomic
  arousal, attachment/proximity. The newborn's valence world is dominated by physiological deficits
  and the attachment/proximity need.
- **Emerging later:** social *belonging* (as the social world widens beyond the caregiver), *standing/
  esteem* (as status becomes legible), the *epistemic* drive (curiosity elaborates through childhood),
  and *control/agency*. These come online on the seed's `developmental_online_age` schedule, and the
  maturation gradient (§6) governs how their drives are regulated at each age.

#### A.4 Connection to the substrate

The vector is the **formalised read-out of the seed's `interoception_autonomic` circuits**, not a
bolt-on: those circuits (NTS, parabrachial, insula, hypothalamic PVN/arcuate/preoptic, amygdala
CO2/acid) *are* the sensing layer; the set-point comparison is their control-centre function; and the
resulting per-variable deviations are what drive the affective/motivational systems and select
consummatory behaviour. Interoceptive inference (Barrett & Simmons 2015; Seth 2013; Craig 2002 —
already in the substrate set) is the read of these deviations *as felt valence*.

#### A.5 Honesty ledger for the vector

- **Solid physiological axes (survival 6 + arousal):** standard homeostatic physiology — that they
  exist and are regulated is well-established; the set-points, weights and drive-function shapes are
  scaffold.
- **Social axes (attachment, belonging):** grounded as genuine homeostatic needs, but the explicit
  *set-point* formalisation rests on a young framework (social homeostasis).
- **Esteem/standing and control/agency:** tentative — plausibly *derived* or *executive-level* rather
  than primal set-points; included as candidates and flagged, to be resolved by whether they earn
  their place behaviourally.
- **Epistemic/uncertainty:** an extension. Pure physiological homeostasis does not cover curiosity,
  novelty, mastery or aesthetic reward; grounding it in allostasis-as-uncertainty-reduction and
  active inference is defensible but the least settled part of the vector.
- **The whole vector is a functional-illustrative overlay:** a real brain does not carry exactly
  these scalars. It is the right *level* for this model (functional, illustrative), not a claim of
  biophysical literalism.

#### A.6 References added in this appendix

**Verified this session:** McEwen, B. S. (1998). Stress, adaptation, and disease: allostasis and
allostatic load. *Annals of the New York Academy of Sciences, 840,* 33–44.
https://doi.org/10.1111/j.1749-6632.1998.tb09546.x · Sterling, P. (2012). Allostasis: a model of
predictive regulation. *Physiology & Behavior, 106,* 5–15.

**Already verified in the substrate set:** Ziemann et al. (2009); Ulrich-Lai & Herman (2009); Barrett
& Simmons (2015); Seth (2013); Craig (2002).

**Classic / standard — confirm exact citation before thesis use:** Sterling, P., & Eyer, J. (1988).
Allostasis: a new paradigm to explain arousal pathology. · Borbély, A. A. (1982). A two-process model
of sleep regulation. *Human Neurobiology.* · Loewenstein, G. (1994). The psychology of curiosity.
*Psychological Bulletin, 116,* 75–98. · Bowlby, J. (1969). *Attachment.*

---

### Appendix B — The innate-perturbation set (the only hardwired event→value links)

*Which events innately move which state-vector variables. This is the boundary between what is
wired at birth and what must be learned; it is the honesty hinge of the whole subsystem. All
gains are scaffold; the set (which sensor moves which variable, in which direction) is the claim.*

#### B.1 The principle, and the critical distinction

An **innate perturbation** is `(innate sensor fires) → (state variable Δ, direction, innate gain)`,
with no cognition in between. These are the system's **unconditioned stimuli** — the ground truth of
value from which everything else is learned. Every richer value acquires its power by **learned
association** with these primaries (secondary reinforcement, via RPE).

The distinction that must be held — and that is easy to get wrong — is between:

- **(i) unconditioned value-perturbations** — events that *move a value variable* (below); and
- **(ii) attentional / learning-rate priors** — events that bias *what is attended to* and *how fast
  something is learned*, but do **not** themselves move a value variable (§B.3).

**Prepared fears and face-orienting are (ii), not (i).** A snake is not innately aversive; fear of it
is merely *learned very fast*. Coding it as an innate value-perturbation would decree the answer —
the exact error the project forbids. This single distinction protects the honesty wall at the input.

#### B.2 The innate value-perturbations (the hardwired US set)

##### A. Physiological / survival — unconditioned
| Trigger (innate sensor) | Variable moved | Dir. | Grounding |
|---|---|---|---|
| Nociceptor firing / tissue damage | tissue integrity (pain) | ↑ (aversive) | standard; innate reinforcer (present) |
| Sweet taste | energy-anticipation / hedonic | + (appetitive) | innate "liking" reaction, Steiner (verified) |
| Bitter / sour taste | hedonic | − (rejection) | innate gaping/rejection, Steiner (verified) |
| Gastric fill / nutrient sensing | energy deficit | ↓ (relief) | standard; feeding releases opioids |
| Osmolality correction (drinking) | hydration deficit | ↓ (relief) | standard |
| Skin warmth / thermal correction | thermal deviation | ↓ (relief) | standard |
| Cold / heat extreme | thermal deviation | ↑ (aversive) | standard |
| CO2 / hypoxia / acidosis | respiratory (suffocation) | ↑ (aversive, panic) | amygdala ASIC1a, Ziemann (verified) |

##### B. Social — unconditioned (the partly-primary set; the honest consequence of §1b)
| Trigger | Variable moved | Dir. | Grounding |
|---|---|---|---|
| Affiliative / C-tactile touch (stroking) | attachment/belonging ↑; arousal ↓; pain ↓ | +/relief | C-tactile & social touch → opioid (Löken, verified; Machin & Dunbar) |
| Contact / proximity with caregiver | attachment-proximity security | ↑ | opioid/oxytocin bonding |
| Loss of contact / separation from attachment figure | attachment-proximity security ↓; arousal ↑ | aversive (separation distress) | PANIC (Panksepp); opioid theory |
| Being held / rocked / soothed | arousal ↓; attachment ↑ | relief | standard; contact comfort (Harlow) |
| Behavioural synchrony (coordinated exertive activity) — *innate machinery, later onset* | belonging ↑ (endorphin) | + | Tarr, Launay, Cohen & Dunbar (verified) |

##### C. Defensive / arousal triggers — unconditioned responses
| Trigger | Variable moved | Dir. | Grounding |
|---|---|---|---|
| Looming / rapid approach (visual) | arousal ↑ + defensive response | aversive | looming, Schiff (verified) |
| Sudden intense stimulus (loud sound, loss of support) | arousal ↑ (startle) | aversive | acoustic startle, Koch (verified) |

That is the whole hardwired set. It is deliberately small.

#### B.3 What is NOT an innate value-perturbation (priors that bias learning, kept separate)

These are real, powerful, and innate — but they belong in the **learning/attention layer**, not the
value-perturbation set:

- **Attentional priors:** face, eye-gaze, and biological-motion orienting bias *where attention (and
  therefore social learning) is directed* — they do not themselves assign value. (Mutual gaze *may*
  carry a faint innate positive tag; the evidence is weak, so treat innate value ≈ 0 and let it be
  learned.) Grounding: newborn face orienting, Simion et al. (verified).
- **Prepared-learning biases:** snakes, spiders, angry faces, heights, and contamination cues are
  acquired as fears/disgust *far faster* than arbitrary cues — a per-cue **learning-rate multiplier**,
  not an innate value. The stimulus is not innately aversive; the fear is learned in one or few
  trials. Grounding: prepared learning, Öhman & Mineka; Cook & Mineka (both verified).

Coding any of these as innate values would smuggle the answer into the mechanism.

#### B.4 Everything else is learned (secondary)

That a *particular* person/voice/face is rewarding; that a smile, praise, or approval feels good;
that criticism, rejection, or social exclusion hurts *beyond* its primary channel; that objects,
money, status symbols, places, teams, and brands have value; that a specific thing is dangerous — all
of this is built by **RPE association** with the §B.2 primaries, over the agent's own history. This
is where individual value-landscapes diverge.

*Honest subtlety:* many social events have **both** a primary core and a learned overlay. Exclusion
directly engages the separation / social-pain primaries **and** carries a large learned social
meaning; a caregiver's face is a learned predictor **attached to** the primary contact/soothing
channels. The design should let a single event perturb the vector through its innate channel *and*
through learned predictions simultaneously — not force a choice between them.

#### B.5 The gains are scaffold; individual variation lives in them

The **set** (which sensor → which variable → which direction) is the grounded structural claim. The
**gains** (how strongly each moves its variable) are scaffold — and inter-individual variation in
these gains **is temperament**: the innate pain-gain, separation-distress-gain, sweet-liking-gain,
touch-reward-gain, and startle/looming-reactivity vary between agents. This is exactly where a bold /
low-fear vs anxious temperament — or a low-affiliation, low-fear proto-seed of the kind the thesis
studies — is set, always as an initial condition, never as an outcome.

#### B.6 Honesty ledger

- **Grounded (that the link exists):** every entry in §B.2 corresponds to a documented primary
  reinforcer or unconditioned response; the §B.3 priors correspond to documented attentional /
  prepared-learning effects. The value-perturbation vs learning-prior split is the load-bearing
  design commitment and is defensible on the evidence.
- **Scaffold:** all gains, the exact ΔH magnitudes, and the learning-rate multipliers.
- **The claim vs the numbers:** we assert the *wiring diagram* of innate perturbations; we do not
  assert the *strengths*, which await calibration and vary by endowment.

---

### Appendix C — RPE learning and anticipatory value

*How learned (secondary) value is acquired and how it drives behaviour before an outcome occurs.
This is the engine that fills all three matrices. It is built on foundations already grounded: the
reward signal is the drive reduction of Appendix A, and the learning is the neuromodulated
plasticity already in the substrate — so this is not a new cognitive module bolted on, but a
formalisation of what the substrate already does.*

#### C.1 The two things learning must produce

1. **Anticipatory value** — a learned prediction of the future drive-reduction a state/cue/action
   leads to. This is what pulls behaviour *before* any outcome (approach the cue that predicts
   relief, avoid the one that predicts harm). It is distinct from the *consummatory* value of
   Appendices A–B (the outcome as actually felt).
2. **A predicted drive-reduction profile** — not just *how much* value, but *which* drive a cue
   predicts relieving (food-cue → energy; friend → belonging; blanket → warmth). Needed so the agent
   can pick the action that addresses the *currently dominant* deficit.

The consummatory/anticipatory split maps onto a well-established dissociation: **"liking" vs
"wanting"** (Berridge & Robinson). *Liking* is the consummatory hedonic reaction (opioid; the felt
ΔH of Appendices A–B); *wanting* is the anticipatory incentive pull (dopamine; the learned value
here). They are dissociable, which is why our design separates them.

#### C.2 The reward signal (already defined, restated)

The primary reward at each step is the drive reduction from the state vector (Appendix A):

> `r_t = β · ( D(t−1) − D(t) )`

computed, never stipulated. Positive when the internal state moved toward set-point, negative when
away. This is the only reward; all learned value is bootstrapped from it.

#### C.3 The value function and the reward-prediction error

Let `V(s)` be the **anticipatory value** of state `s`: the expected discounted future reward.
Learning uses the temporal-difference **reward-prediction error (RPE)**:

> `δ_t = r_t + γ·V(s_{t+1}) − V(s_t)`      (γ = temporal discount)

- `δ > 0`: things went better than predicted → increase `V(s_t)` and strengthen the cues/actions
  that led here.
- `δ < 0`: worse than predicted → decrease them.
- Update: `V(s_t) ← V(s_t) + α·δ_t` (α = learning rate). Eligibility traces / TD(λ) assign credit
  back to the cues that preceded the outcome.

**Dopamine encodes `δ`** (Schultz — verified). This is the same RPE that shifts, with training, from
the outcome to the earliest predictive cue — i.e. how a neutral cue *becomes* a wanting-signal.

#### C.4 Learning is neuromodulated plasticity (keeps it substrate-consistent)

The RPE rule is not a separate module: it is the **third factor** in the substrate's local plasticity.
Synapses change as a product of pre-activity × post-activity × a neuromodulatory signal — a
**three-factor learning rule** (Frémaux & Gerstner — verified) — where the neuromodulator carrying
`δ` is dopamine. So "the relationship matrix learns that this person is rewarding" *is* dopamine-
gated Hebbian strengthening of the pathways that fired during rewarding interactions with them. The
honesty wall holds: the plasticity is local and meaning-blind; the RPE is a scalar neuromodulator,
not a labelled instruction. Oxytocin/opioid gates (from §2.3) mark *which primary channel* was
engaged and license social-cue plasticity (Dölen — verified); dopamine carries *how much better/
worse than expected*.

#### C.5 The homeostatic twist: value is state-dependent and vectorial

Because reward is drive reduction and drive depends on the *current* internal state, the value of an
outcome is **state-dependent** (Keramati & Gutkin prove this — verified): a food cue is valuable when
hungry, near-worthless when sated. A fully re-evaluating (model-based, §C.6) system therefore reads
anticipated value *against the current drive vector*, which gives **motivational modulation of
behaviour for free** — the agent pursues what its present deficits make valuable.

To support this, learning credits value **per drive variable**, not just as a scalar: each cue
acquires a *predicted drive-reduction profile* (a small vector over the Appendix-A variables). At
choice time the agent weights each cue's profile by its current per-variable drive `d_k`, so the
same cue is pursued when it predicts relief of an *active* need and ignored otherwise. *(This is a
deliberate extension of scalar RL, motivated by the vectorial drive of Appendix A; flagged as a
design choice, grounded loosely in multi-objective RL — the scalar aggregate remains available for
mood and for simple credit.)*

#### C.6 Model-free and model-based value (habit vs goal-directed)

Two learned systems, both real and both needed (Daw; Dolan & Dayan — classic):

- **Model-free (habitual):** cached `V`/`Q` values updated by `δ`. Fast, cheap, *insensitive* to
  current drives once cached. Produces habits, and — with overtraining or in addiction — compulsive
  pursuit that ignores current value.
- **Model-based (goal-directed):** a learned model of transitions, used to *simulate forward* and
  re-evaluate outcomes against the current drive vector (§C.5). Flexible, drive-sensitive,
  expensive.

Behaviour arbitrates between them (roughly, by which is more reliable/economical in context). The
**shift from goal-directed to habitual with repetition** is a real phenomenon and a natural handle on
compulsion/addiction — and, developmentally, on how the maturing executive (which supports model-
based control) changes the balance over the life course.

#### C.7 Anticipatory value drives approach and avoidance

Before any outcome, the agent is pulled toward cues/states with high anticipated value and pushed
from those with negative value — Pavlovian **incentive salience** ("wanting"; dopamine) attaching to
predictors. This is what makes a learned friend *sought out*, a learned threat *avoided*, a learned
addictive cue *craved* — all before the consummatory outcome. Anticipatory value is thus the input to
behaviour selection (the next design piece): it proposes what to approach/avoid; the competition/
arbitration mechanism (deferred substrate decision) then resolves *which* pull wins at the effector
bottleneck when several conflict.

#### C.8 Aversive learning, extinction, and the asymmetries

- **Aversive learning** uses negative RPE (dopamine dips; with contributions from habenula and
  serotonergic systems). Cues predicting drive *increases* (harm, loss, isolation) acquire negative
  anticipatory value and drive avoidance.
- **Asymmetries are built in, not coded.** Threat/aversive learning is faster, higher-gain, and
  slower to extinguish than appetitive learning — which is the mechanistic source of the negativity
  bias (§5.3) and, with the prepared-learning multipliers (§B.3), of one-trial fears. These are
  learning-rate/gain asymmetries in the *same* rule, not separate machinery.
- **Extinction** is new learning that the prediction no longer holds (vmPFC-gated; Milad & Quirk —
  verified), not erasure — so extinguished value can spontaneously recover, matching the persistence
  of learned fears and attachments.

#### C.9 How the three matrices are updated by this

Each entry in the relationship / environment / group matrices is, concretely, a **learned value plus
a predicted drive-reduction profile** for that person/object/group, updated by RPE from every
interaction with it (§2.4 loop, step 5b). A warm interaction with a person yields `δ > 0` and raises
that person's anticipatory value and their belonging/attachment profile; a betrayal yields large
`δ < 0` and writes negative, slow-to-extinguish value (the enemy/ambivalent cases of §4). The
matrices are thus not separate stores of "how I feel" — they are the cached outputs of this one
learning rule, per entity.

#### C.10 Honesty ledger and references

- **Grounded (mechanism):** RPE/TD learning of value with dopamine as `δ` (Schultz); learning as
  neuromodulated three-factor plasticity (Frémaux & Gerstner); state-dependent value under homeostatic
  RL (Keramati & Gutkin); liking/wanting dissociation (Berridge & Robinson); model-free/model-based
  duality (Daw); extinction as new vmPFC-gated learning (Milad & Quirk). All either verified in the
  substrate set or standard.
- **Scaffold:** α, β, γ, λ, the per-cue learning-rate multipliers, the arbitration weights between
  model-free/based, and all gains.
- **Design extensions (flagged):** the *vectorial* predicted-drive-reduction profile (beyond scalar
  RL); the exact arbitration rule for model-free vs model-based; both to be resolved and, where
  possible, kept emergent rather than hand-tuned.

**References added:** Schultz, W. (dopamine reward-prediction error — verified in substrate set);
Frémaux, N., & Gerstner, W. (2016). Neuromodulated STDP and three-factor learning rules (verified);
Keramati & Gutkin (2014, verified); Milad & Quirk (verified). *Classic — confirm exact citation:*
Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction.* · Montague, Dayan &
Sejnowski (1996), *J. Neurosci.* · Berridge, K. C., & Robinson, T. E. (1998/2016), incentive-salience
"liking vs wanting." · Daw, N. D., et al. (2005/2011), model-based vs model-free arbitration. · Niv,
Y. (2007), tonic dopamine and response vigour.

---

### Appendix D — Distillation (the default disposition) and the observer read-out

*Two things that sit at the edges of the engine: how specific learning generalises into a default
character, and how we (not the agent) measure what the agent is doing.*

#### D.1 Distillation — how specifics become a default disposition

The per-entity matrices (Appendix C) hold specific learned values. The **distilled default
disposition** — the "master copy," the way the agent behaves toward a novel or generic other — is the
generalisation across them (Bowlby's internal working models). It has two mechanical homes, and
neither requires a separate "distillation process":

**(1) The substrate weights are the automatic sediment.** Because dopamine-gated plasticity from
*every* interaction modifies the *shared* substrate connections (§C.4), the current weights already
*are* the running aggregate across all interactions. The default relational style is largely just the
settled state of the substrate — it distils itself, continuously, for free.

**(2) A pooled prior for expectations.** For the predictive part, model the relationship between the
default and specific entities as **partial pooling**: the default is a slow-updating,
population-level estimate ("people generally respond to me like *this*"); each entity is a
fast-updating local estimate **initialised at the default** and moved toward entity-specific evidence
with experience. The agent's expectation of a given other is a **precision-weighted blend** of the
two — mostly the default for a stranger or a sparsely-known person, mostly entity-specific for someone
well known. Entity estimates in turn slowly feed the default (it is their running aggregate). No full
Bayes is required: a slow global running average plus fast local estimates blended by how much
entity-specific data exists reproduces the structure.

Three consequences fall out, all as *emergent* phenomena rather than coded rules:

- **Transference / generalisation by similarity.** A new other who resembles a known one inherits some
  of that one's value (a generalisation gradient over features; Shepard). A new authority figure is
  met with the disposition learned toward past authority figures. This grounds transference and
  (uncomfortably but honestly) stereotyping — emergent, not authored.
- **Developmental primacy of early data.** The earliest interactions — dominated by the caregiver and
  occurring in high-plasticity windows — disproportionately shape the default, because they are the
  first/only evidence and land when plasticity is greatest. So the early caregiving relationship
  becomes the template for the default relational style. This is the honest mechanism behind "early
  attachment shapes lifelong relational patterns," and it links to the critical-period/epigenetic
  story (§5.2, §6).
- **Ambivalent defaults.** If early data is itself ambivalent (an attachment figure who is also a
  threat — §4.3), the *default* becomes ambivalent, carrying the approach–avoidance conflict into
  novel relationships. A direct, emergent route from early adversity to a pervasive relational
  signature — and a validation target.

*Status:* the substrate-as-sediment part is grounded in the model's own plasticity; the pooled-prior
and similarity-generalisation parts are standard (partial pooling; Shepard's generalisation) but the
specific blend is a design choice, flagged, to be kept as emergent as possible.

#### D.2 The observer read-out — measuring the agent without touching it

Recall the two-scorings rule (§2, and the memo): the **agent's** valuation is causal and in the
mechanism (everything above); the **observer's** read-out is *ours*, non-causal, and **never fed
back**. Appendix D fixes what the observer read-out is.

**What it is.** A set of **named construct metrics** that *we* compute over (a) the agent's behaviour
(choices, actions, speech in defined situations) and (b) its substrate activity, purely to check
whether the emergent behaviour matches the psychological constructs the thesis studies. This is where
the **output categories legitimately live** — "fear," "aggression," "callousness," "empathy,"
"prosociality," "psychopathy" — as *measurements over* the mechanism, never as *parts of* it. It
completes the substrate design's principle that named systems are read-outs, not primitives.

**How it is computed.**
- *From behaviour:* administer **standardised probes** — the simulated agent "takes the same tests"
  as human participants (defined scenarios, decisions, tasks), and we read the behavioural signature.
  This is what makes comparison to human norms possible.
- *From substrate activity:* patterns of activation stand in for the construct — e.g. a blunted
  threat/amygdala response to another's distress reads as a "low-empathy/callousness" signature; a
  strong ambivalent co-activation reads as approach–avoidance conflict.

**What to measure (operationalised from the thesis's own framework).** The metrics should be built
from the thesis's construct definitions, not reinvented here — but the load-bearing ones for the
sophropath vs psychopath distinction are the standard signatures: the triarchic dimensions
(boldness / meanness / disinhibition), callous-unemotional traits, empathy and guilt/remorse,
**punishment/passive-avoidance learning** (the classic psychopathy deficit — poor learning from
punishment, reward dominance), fearlessness, and **reactive vs instrumental aggression**. The
emergent phenomena we have already named — ambivalent-bond conflict, adolescent risk-taking, the
derived cognitive biases, "a punishment for one is a reward for another" — are also observer
read-outs.

**The validation logic (the decisive point).** The substrate is validated to the extent that these
observer read-outs reproduce known human patterns **without those patterns being coded in**. In
particular, the sophropath–psychopath divergence (and its childhood emergence) must **emerge from the
differential endowment alone** (the plugin, next) — if we had to program the divergence, the model
would prove nothing. The observer read-out is therefore both the measuring instrument *and* the
guard against cheating: it is how we would catch ourselves if a result had been smuggled in.

*Status:* the *architecture* (observer-side, never fed back, probe-administered) is fixed here; the
specific metrics and probes are to be operationalised directly from the thesis's Study 1–4 construct
definitions and the instruments they already use.

#### D.3 References

*Standard / classic — confirm exact citation against the thesis's own reference set:* Bowlby, J.
(1969/1982). *Attachment.* · Bretherton, I. (1992), internal working models. · Shepard, R. N. (1987).
Toward a universal law of generalization. *Science.* · Patrick, C. J., Fowles, D. C., & Krueger, R. F.
(2009), triarchic model of psychopathy. · Frick, P. J., & White, S. F. (2008), callous-unemotional
traits. · Blair, R. J. R. (amygdala/empathy model of psychopathy). · Hare, R. D. (PCL-R). — The
psychopathy/sophropathy constructs are the thesis's own domain; the observer read-out should defer to
its definitions rather than import new ones.

---

### Appendix E — The sophropath/psychopath differential profile (as a plugin module)

*How the study-specific differential slots into the already-built module system, expressed in the
valence-engine parameters of this document. This is a research **plugin**, not core — the platform
stays psychology-free; the psychology lives here.*

#### E.1 How it slots in (the existing contract)

The module system (`core/modular/registry.py`) discovers any package under `extensions/<name>/`
exposing a top-level `MODULE = Module(...)`, with optional hooks — `child_source`, `adult_source`,
`world_content`, `categorise`, `report`. The core names no disposition or study; it only runs the
callables a study supplies. The **`sophropathy` module already exists** and already implements the
right shape:

- `child_source` seeds a `fearless_frac` **minority** as the fearless proto-disposition
  (`shared_root_seed()`), the rest `typical_child_seed()` — *"GIVEN temperament only; the outcome
  emerges."*
- `categorise` (`study_category`) **is the observer read-out of Appendix D** — it reads a settled
  network into the study's categories and is never fed back.
- `report` produces the cohort/subject read-out; `world_content` supplies venues and the caregiving
  world.

Crucially, the engine already exports **three** seeds with exactly our division of labour: a single
child start (`shared_root_seed`), and **two adult attractors** (`sophropathic_seed`,
`psychopathic_seed`) used as *parent/adult* seeds — i.e. the two outcomes the same fearless child can
develop into. The differential profile is therefore not a new mechanism to bolt on; it is (a) the
*content* of these seeds re-expressed in the valence-engine parameters, and (b) one honesty
correction (E.4).

#### E.2 The shared root — one proto-disposition, expressed in the new parameters

Both outcomes start from **one** atypical temperament (the fearless child). In the current code this
lives in `TraitSeed.gains` over the legacy system names (THREAT, ANXIETY, CARE, SOCIAL_LOSS, CONTROL,
SEEKING, …). Re-expressed in the parameters this document defines — the *only* legitimate place a seed
differs (§5.1, §B.5, Appendix A) — the shared root is:

| Parameter (this doc) | Typical child | Fearless / shared-root child | Grounds |
|---|---|---|---|
| Threat-system reactivity (arousal-gain to looming/threat; aversive-RPE gain; fear-extinction rate) | mid | **low gain, fast extinction** | low-fear/boldness (Lykken; triarchic boldness) |
| Affiliation weight `w_belonging`, attachment/separation-distress gain, affiliative-touch reward gain | mid | **reduced** | low affiliation / callousness; reduced social reward |
| Vicarious arousal to others' distress cues | mid | **blunted** | amygdala hyporeactivity to distress (Blair); CU traits |
| Appetitive vs aversive RPE balance (reward dominance; passive-avoidance) | balanced | **reward-dominant, weak punishment learning** | response-modulation/reward dominance (Newman — verified) |
| Executive-control maturation (starting point) | undeveloped (as any child) | **undeveloped** (matures late; see divergence) | dual-systems maturation (§6) |

That is a *temperament*: a region of endowment-parameter space, with the gains scaffold and varying
across individuals (a spectrum, not a type). The `fearless_calculating` variant (`shared_root_
calculating_seed`) is simply a different point in the same space (higher cold-instrumental, lower
reactive), already provided.

#### E.3 The divergence is developmental, not a second seed

The sophropath and psychopath are **not two child seeds**. They are the **two adult attractors** the
same fearless child reaches under different development — which is the thesis's whole claim (childhood
divergence). The differentiating axes *emerge* from temperament × environment:

- **Executive control / disinhibition.** The adaptive outcome (sophropath) develops **good executive
  control** — which channels boldness and low fear into non-offending, often instrumentally
  successful, behaviour; the antisocial outcome (psychopath) remains **disinhibited**. In the
  triarchic frame both share *boldness* (± *meanness*); they diverge on *disinhibition*. And executive
  control is exactly what caregiving **structure/warmth/recognition** builds (the code's
  `parent_to_environment`: warmth ← CARE, structure ← CONTROL, recognition ← both). So the divergence
  is driven by the developmental environment, as the thesis requires.
- **The learned value landscape.** Whether prosocial-instrumental strategies are learned to pay
  (sophropath) or exploitative-antisocial ones are (psychopath) is set by the environment's
  contingencies, learned through the RPE engine (Appendix C).

**Differential susceptibility** is the mechanism that makes this work and it is already in the code's
design: the *fearless* child, lacking the fear that would make a harsh upbringing simply frightening,
is **more susceptible to the environment in both directions** — a good environment yields the
adaptive outcome, an adverse one the antisocial outcome — whereas the *typical* child, with fear
intact, tends toward anxiety/withdrawal under adversity rather than callousness. So the two adult
seeds (`sophropathic_seed`, `psychopathic_seed`) are **descriptions of the attractors**, used as
adult/parent dispositions; no child is born destined for either.

#### E.4 One honesty correction for the migration

The current `TraitSeed.access` carries weights named after **outcome categories** —
`cool_instrumental_boldness`, `callous_exploitation`, `strategic_prosociality`, … — as *seed inputs*.
Under this document's discipline (Appendix D: named categories are **observer read-outs, never
primitives**), seeding an access-weight named `callous_exploitation` is close to encoding the answer.
The migration to the valence engine should therefore **move these from seed inputs to observer
outputs**: the seed carries only *temperament parameters* (E.2), and boldness / callousness /
prosociality / exploitation are **computed by the observer read-out** (`categorise`, Appendix D) from
the emergent behaviour. This tightens the honesty wall relative to the current code and is the one
substantive change the differential profile needs beyond re-parameterisation.

#### E.5 What we predict, and how the plugin reports it

- **Prediction (the thesis's target).** Fearless children start alike; through childhood the
  environment shapes executive control and the learned value landscape; by adolescence/adulthood the
  outcomes are distinguishable on the observer read-outs — **boldness shared**, but the sophropath
  showing intact control, instrumental/prosocial integration and non-offending, the psychopath showing
  disinhibition, exploitation and offending. The typical child under the same adversity diverges a
  third way (internalising).
- **How reported.** The plugin's `categorise`/`report` hooks compute the observer read-outs
  (triarchic dimensions, CU traits, punishment/passive-avoidance learning, reactive vs instrumental
  aggression — operationalised from the thesis's own instruments) over the emergent behaviour, per
  subject and per cohort. The result that matters is that the sophropath/psychopath split **emerges
  from the differential endowment plus environment alone** — if it had to be coded, the model would
  show nothing (Appendix D validation logic).

#### E.6 References

*The psychopathy/sophropathy constructs are the thesis's own domain — defer to its definitions;
confirm exact citations there.* Lykken, D. T. (low-fear hypothesis). · Patrick, Fowles & Krueger
(2009), triarchic model (boldness/meanness/disinhibition). · Newman, J. P., et al. (response
modulation / reward dominance — Newman 1999 is in the substrate's verified set). · Blair, R. J. R.
(amygdala/empathy). · Frick, P. J. (callous-unemotional traits). · Belsky, J., & Pluess, M.
(differential susceptibility). · The "successful/adaptive psychopathy" literature for the non-
offending outcome.

---

### Appendix F — Behaviour selection and the competition mechanism

*The last missing link in the live loop: how the parallel pulls (anticipatory values weighted by
current drives, plus reflexive tendencies) resolve into one executed action — without a
hand-authored arbiter. The answer is a real neural mechanism, basal-ganglia action selection, built
from nucleus-level circuits the substrate already contains, and it produces the conflict/impulsivity
phenomena we promised as emergent rather than coded.*

#### F.1 What selection must do (and the honesty constraint)

At every moment several incompatible action tendencies are active at once — approach a valued cue,
avoid a threat, address the dominant bodily deficit, inhibit a prepotent impulse. Only one behaviour
can reach the effectors. Selection must turn the parallel pulls into a single action **and** it must
do so *without a coded rule* ("if threat and reward are both high, do X"). A coded arbiter would be
the encoded psychological effect the project forbids, and it was the whole reason for choosing
nucleus-level circuits: conflict must **emerge** from shared circuits competing for the bottleneck,
not be decided by an author.

#### F.2 The candidates and their strength

Following the **affordance-competition** view (Cisek), the substrate represents multiple potential
actions in parallel; they compete continuously and are biased toward resolution by value. Each
candidate's input strength is its **anticipated value read against the current drive** — from
Appendix C.5, a candidate's predicted drive-reduction *profile* dotted with the current per-variable
drive vector (Appendix A). So a food-seeking candidate is strong when the energy drive is high, weak
when sated; a company-seeking candidate is strong when lonely. Reflexive/prepotent candidates
(innate perturbations, §B; over-trained habits, §C.6) enter the same competition with their own
strength.

#### F.3 The mechanism: basal-ganglia disinhibition + accumulation to threshold

Selection is the job of the **basal ganglia**, which evolved as a centralised device to resolve
conflicts over access to limited motor/cognitive resources (Redgrave, Prescott & Gurney, 1999). Its
operation, in the terms we need:

- Candidate actions correspond to competing channels through the **striatum → pallidum (GPi/SNr) →
  thalamus → cortex** loop. The default pallidal output is *inhibitory*: everything is held off.
- The **direct ("Go") pathway** *disinhibits* the selected channel's thalamocortical loop (releases
  it), while the **indirect ("NoGo") pathway** and surround inhibition suppress competitors — focused
  selection with surround suppression (Mink; the GPR computational model, Gurney, Prescott & Redgrave,
  2001).
- The **subthalamic nucleus (STN)**, via the hyperdirect pathway, provides a **global "hold"** that
  scales with the number/strength of competing demands, preventing premature or multiple selection
  and buying time in high-conflict cases (Frank, 2006).
- Formally this behaves like **evidence/value accumulation to a threshold**: candidate values
  accumulate until one crosses a bound and is committed — which the basal-ganglia–cortex loop
  approximates to an *optimal* decision between alternatives (Bogacz & Gurney, 2007). Close values →
  slow, effortful, high-conflict decisions; a dominant value → fast commitment.

The winner reaches the effectors; the losers are suppressed. Nothing is arbitrated by fiat — the
outcome is a property of which channel accumulates fastest given its value and the competition's
parameters.

#### F.4 Dopaminergic modulation (the gain on selection)

Dopamine sets the *parameters* of the competition, tying selection to the value system (Appendix C):
**phasic** dopamine (the RPE) updates the values that feed the channels; **tonic** dopamine sets the
overall **Go/NoGo balance, the decision threshold, and behavioural vigour**, and the
exploration/exploitation temperature (Niv; Collins & Frank). High tonic dopamine → more Go, lower
thresholds, faster/more impulsive and vigorous action, more exploration; low → cautious, more NoGo.
The relationship is an inverted-U (too much or too little impairs selection; Cools). This is the
handle by which motivation, reward state, and individual dopaminergic reactivity (an endowment
parameter, §5.1) tune how impulsive or cautious an agent is — emergently.

#### F.5 The executive brake as top-down bias, not dictation

The executive (the substrate's prefrontal nuclei — vlPFC/dlPFC/dACC/preSMA feeding the STN) does
**not** pick the action. It **biases the competition's parameters**:

- **Proactively** — raising the global threshold or pre-loading NoGo for an action that context says
  should be withheld (preparing to stop).
- **Reactively** — firing the STN **global hold** to cancel a prepotent response already underway
  ("hold your horses"); the right IFG → STN stop pathway (Aron & Poldrack, 2006; Aron et al., 2014 —
  both verified).
- **Conflict monitoring** — the dACC detects when candidates are close (high conflict) and recruits
  more control, which is *itself* the signal that raises the threshold and slows the decision.

So control changes *how hard it is for a candidate to win*, not *which candidate wins*. The
competition still resolves itself. This is what keeps the executive an honest modulator rather than a
homunculus deciding outcomes.

#### F.6 Conflict, the behavioural-inhibition system, and the ambivalent bond

Approach–avoidance goal conflict has a dedicated resolver: the **behavioural inhibition system**
(septo-hippocampal; Gray & McNaughton), which detects goal conflict, inhibits ongoing behaviour,
boosts vigilance and arousal, and whose *output is anxiety*. In our terms it is the state in which
the accumulator sits near a tie between a strong approach candidate and a strong avoid candidate.

This is exactly the **ambivalent bond** (§4.3): high attachment *and* high threat toward the same
person propose two strong, incompatible, roughly balanced candidates. The consequences fall out with
nothing authored: **oscillation/vacillation** (the accumulator crosses first one bound then the
other), **slow, effortful, depleting decisions**, and — because the conflict stays unresolved — the
BIS keeps **arousal chronically elevated** (the arousal variable of Appendix A never returns to
set-point), producing sustained anxiety and, over time, allostatic load. So the destructive power of
the ambivalent bond is an emergent property of the selection mechanism plus the state vector, and it
is a direct validation target.

#### F.7 Impulsivity, exploration, and the developmental gradient

- **Impulsivity** is a prepotent high-value candidate (a super-stimulus, an over-trained habit,
  §C.6) winning *before* slower model-based evaluation or the executive brake can suppress it —
  strongest when the brake is weak, immature, or depleted, or when tonic dopamine is high.
- **Exploration** is built in: selection is not purely greedy (softmax-like temperature from tonic
  dopamine/noise), so a developing agent explores rather than exploiting a single cached option — a
  requirement for learning (Appendix C).
- **The developmental gradient** needs no extra machinery: the reward/Go system matures early, the
  prefrontal→STN brake late (§6). Strong Go + weak brake through adolescence → prepotent/rewarding
  candidates win more often → **adolescent impulsivity and risk-taking, emergent** (dual-systems model,
  §6), resolving as the brake matures into the mid-20s.

#### F.8 Why this is not a coded arbiter (honesty)

Selection is a property of the competing circuits and the parameters (values, drives, dopaminergic
gain, executive bias) acting on them — not a rule that reads the situation and outputs a behaviour.
The executive sets parameters, never outcomes. Internal conflict, approach–avoidance paralysis,
impulsivity, and the developmental shift all **emerge**. And the mechanism is nucleus-level and
already substrate-shaped: it runs on the striatum → GPe/GPi/SNr → STN → thalamus → cortex loop, with
dopamine (VTA/SNc) as the gain. *Substrate note:* the seed already carries the executive nuclei,
NAc/VTA and preSMA→STN; the **full motor-selection loop nuclei (dorsal striatum, GPe, GPi/SNr,
motor thalamus)** should be present as the selection substrate — flag for the substrate spec if not
yet explicit.

#### F.9 Honesty ledger and references

- **Grounded (mechanism):** basal-ganglia action selection (Redgrave, Prescott & Gurney; GPR model);
  optimal accumulation (Bogacz & Gurney); STN hold and stopping (Frank; Aron — verified); affordance
  competition (Cisek); dopaminergic gain on selection (Niv; Collins & Frank; Cools inverted-U); goal-
  conflict/anxiety (Gray & McNaughton). All either verified this session or standard.
- **Scaffold:** the decision thresholds, accumulation rates, inhibition strengths, softmax
  temperature, and the mapping from value+drive to channel input — all placeholders, all where
  individual variation (endowment) lives.
- **Design commitment:** selection is emergent from competition; the executive is a parameter-setter,
  not a decider; this is the honesty wall at the effector bottleneck.

**References added — verified this session:** Redgrave, P., Prescott, T. J., & Gurney, K. (1999). The
basal ganglia: a vertebrate solution to the selection problem? *Neuroscience, 89,* 1009–1023. ·
Gurney, K., Prescott, T. J., & Redgrave, P. (2001). A computational model of action selection in the
basal ganglia (I & II). *Biological Cybernetics, 84.* · Frank, M. J. (2006). Hold your horses: a
dynamic computational role for the subthalamic nucleus in decision making. *Neural Networks, 19.* ·
Bogacz, R., & Gurney, K. (2007). The basal ganglia and cortex implement optimal decision making.
*Neural Computation, 19.* · Aron, A. R., & Poldrack, R. A. (2006); Aron et al. (2014) — verified in
the substrate set. **Standard — confirm exact citation:** Mink, J. W. (1996); Cisek, P. (2006),
affordance competition; Niv, Y., et al. (2007), tonic dopamine and vigour; Collins, A. G. E., & Frank,
M. J. (2014); Cools, R., & D'Esposito, M. (2011), dopamine inverted-U; Gray, J. A., & McNaughton, N.
(2000), *The Neuropsychology of Anxiety* (the behavioural inhibition system).

---

## Part II — Code-change map

### PsychSim — Valence/Motivation code-change map

*Companion to Part I. Translates that design (Appendices A–F
plus the endowment/epigenetics sections) into concrete changes against the **real** codebase. It is
the precursor to the Claude Code build instructions (plan step 6). Nothing here changes the module
contract in `core/modular/registry.py` or edits `project.py`.*

Verified layout this maps onto:
- `core/affective_engine/` — `core.py` (Appraisal, Network, **TraitSeed**, seeds `shared_root_seed` /
  `sophropathic_seed` / `psychopathic_seed` / …, `CIRCUITS`), `drives.py` (`System`, `Brain`, `Drive`,
  `imprint`, `window_plasticity`, `brain_from_seed`, `appraisal_to_stimulus`), `development.py`
  (`Environment`, `develop`, `probe`, `classify`, `Outcome`, the response-valence logic),
  `memory.py` (`EpisodicMemory` with a `valence` field), `executive.py`, `agent.py`.
- `core/sim_world/` — the three matrices already exist: **`relations.py`** (relationship),
  **`environment_matrix.py`** (environment), **`group_matrix.py`** (group), plus `person.py`,
  `population.py`, `gamemaster.py`, `world.py`.
- `core/neuraldesigner/` + the seed JSONs — the substrate.
- `extensions/sophropathy/` — the study plugin (`society.py` seeds, `world.py::study_category`,
  `report.py`, `module.py`).

---

#### 1. Summary — files touched

| Design element (doc ref) | Primary file(s) | Kind |
|---|---|---|
| Interoceptive state vector + drive + **computed valence** (App. A/B) | **new** `affective_engine/interocept.py`; edit `development.py`, `memory.py` | ADD + REPLACE |
| Innate-perturbation table (App. B) | `affective_engine/interocept.py` (data); consumers in `development.py` | ADD |
| RPE learning + anticipatory value (App. C) | **new** `affective_engine/learning.py`; edit `drives.py` (plasticity) | ADD + MODIFY |
| Neuromodulators as gates (App. C) | `drives.py` / `learning.py` | MODIFY |
| Relationship matrix: Dunbar slots + salience/enemy/ambivalent (App. 4) | `sim_world/relations.py` | MODIFY (major) |
| Environment matrix onto one engine (nature/animals/belongings) (App. 3.2) | `sim_world/environment_matrix.py` | MODIFY |
| Group matrix: synchrony/endorphin + sociometer (App. 3.3) | `sim_world/group_matrix.py` | MODIFY |
| Distillation / default disposition (App. D.1) | `sim_world/relations.py` (pooled prior) + substrate weights | ADD |
| Observer read-out + **access→read-out honesty fix** (App. D.2 / E.4) | `core.py` (TraitSeed), plugin `world.py`/`report.py`; grep `access` consumers | MIGRATE (honesty-critical) |
| Behaviour selection + competition (App. F) | **new** `affective_engine/selection.py`; refactor `executive.py`; seed JSON nuclei | ADD + MODIFY |
| Endowment re-parameterisation + epigenetics (doc §5) | `core.py` (TraitSeed + seeds); **new** `affective_engine/epigenetics.py` | MODIFY + ADD |
| Differential-profile plugin re-expression (App. E) | `extensions/sophropathy/society.py`, `world.py`, `report.py` | MODIFY |
| Retire two-affect-pathway / legacy primitives | `drives.py`, `core.py`, `agent.py` behind stable interfaces | SUPERSEDE (staged) |

---

#### 2. Per-area change specs

##### 2.1 The valence core — `affective_engine/interocept.py` (NEW) + `development.py`, `memory.py`
- **Add `interocept.py`** defining: `StateVector` (the App. A variables + set-points, with a
  `fixed`/`allostatic` flag per variable), `drive(state) -> (per_variable_vector, scalar_D)`, the
  **innate-perturbation table** (App. B: sensor→variable→direction→gain), and
  `valence(D_prev, D_now) -> r = β·(D_prev − D_now)`.
- **`development.py`:** replace the current **stipulated** valence (the `response_valence` logic and
  the hard-set warm/harsh `social_valence` in the appraisal scenarios) with a call that (a) applies an
  event's perturbations to the state vector and (b) returns the *computed* `valence`. The
  scenario/appraisal definitions change from *"this outcome has valence −0.7"* to *"this event moves
  {threat-arousal ↑, social-contact ↓}"*; the number is then computed. `warm_firm_home` /
  `harsh_inconsistent_home` stay as `Environment`s but specify perturbation patterns, not valences.
- **`memory.py`:** `EpisodicMemory.valence` stays but is now written from the computed value; add an
  optional per-variable `drive_reduction` field so memory records *which* drives moved (feeds C.5).
- **Honesty note:** this is the #1 fix — it is what makes "a punishment for one is a reward for
  another" emergent rather than decreed.

##### 2.2 Learning — `affective_engine/learning.py` (NEW) + `drives.py`
- **Add `learning.py`:** the value function `V` (anticipatory value), the TD/RPE update
  `δ = r + γV' − V`, and the **three-factor plasticity** application (pre × post × dopamine=δ). Provide
  `update(cue, r, ...)` used by the matrices.
- **`drives.py`:** the existing plasticity (`imprint`, `window_plasticity`) becomes the substrate
  application of the three-factor rule; keep the window/critical-period gating, add the δ factor.
  Make the neuromodulators **gates**: oxytocin/opioid license social-cue plasticity (App. C.4),
  dopamine carries δ — not stored "values".
- Anticipatory value from here is the input to selection (2.6).

##### 2.3 The three matrices — `relations.py`, `environment_matrix.py`, `group_matrix.py`
Common change: each per-entity record gains a **learned `value` + `drive_reduction_profile`**, updated
by `learning.update(...)` after each interaction (the App. C.9 pattern). Then:
- **`relations.py` (major):** add the **Dunbar layered capacity** — inner slots (~5), then ~15/~50/~150
  bands — with **decay without contact**; **allocate slots by |salience|**, not positive valence; each
  slot stores `value`, `salience`, and a `valence_sign`, enabling the **enemy** and **ambivalent**
  cases (co-active attachment + threat toward one entity → App. 4.3). Expose the ambivalence to the
  selection/BIS path (2.6, 2.7).
- **`environment_matrix.py`:** route value through the one engine; ground **nature** as arousal/stress
  drive-reduction (+ biophilia prior), **animals** through the social/oxytocin channels (a pet may
  take a `relations.py` slot), **belongings** as instrumental + extended-self.
- **`group_matrix.py`:** keep dominance/prestige status (already present); **add** the
  **synchrony/endorphin belonging** factor (coordinated activity → belonging ↑) and the **sociometer**
  (esteem tracks inclusion). Same value engine.

##### 2.4 Distillation / default disposition — `relations.py` (+ substrate)
- The default is **partly automatic** (the substrate weights are the running sediment — no code
  needed). **Add** a **pooled prior**: a slow global estimate of social-outcome expectation; each new
  entity record is **initialised from it** and blended with entity-specific evidence by a
  precision/count weight (App. D.1); entity estimates slowly update the prior. This gives
  transference, early-caregiver primacy, and ambivalent defaults for free.

##### 2.5 Observer read-out + the honesty migration — `core.py` + plugin
- **Honesty-critical (App. E.4):** `TraitSeed.access` currently carries **outcome-category** weights
  (`callous_exploitation`, `strategic_prosociality`, `cool_instrumental_boldness`, …) as seed
  **inputs**. **Remove these from the seed.** The seed carries only **temperament parameters** (2.8).
  The categories become **observer read-outs** computed in the plugin's `world.py::study_category` /
  `report.py` from *emergent* behaviour and substrate activity. **Grep every consumer of `access`**
  (`core.py`, `drives.py`, `agent.py`, the plugin) and re-point them at the read-out.
- The `categorise`/`report` hooks are the observer layer (App. D.2): computed over behaviour, **never
  fed back**; add the study metrics (triarchic / CU / punishment-learning / aggression-type) here.

##### 2.6 Behaviour selection — `affective_engine/selection.py` (NEW) + `executive.py` + seed JSON
- **Add `selection.py`:** basal-ganglia action selection (App. F). Candidates = affordances with input
  strength = anticipatory value ⋅ current drive (2.1/2.2). Implement **accumulation-to-threshold with
  disinhibition** (direct/Go release + indirect/NoGo + STN global hold) → a winner; **dopamine sets the
  gain** (Go/NoGo balance, threshold, vigour, softmax temperature).
- **`executive.py` (refactor):** recast the executive as a **parameter-setter on selection**, not a
  decider — proactive threshold/NoGo bias, reactive **STN "hold"** (the Aron IFG→STN stop), dACC
  conflict monitoring. Keep the existing "learn inhibitory monitors from memory" (reversal learning),
  but route it as *which candidates to bias*, through `selection.py`.
- **Seed JSON / `neuraldesigner`:** ensure the **full motor-selection loop nuclei** exist — dorsal
  striatum, GPe, GPi/SNr, motor thalamus (the seed already has NAc, VTA, and preSMA→STN). Add if
  absent.
- **BIS hook:** an unresolved approach/avoid near-tie holds arousal elevated (App. F.6) — wire the
  selection conflict state back to the arousal variable in `interocept.py`.

##### 2.7 Endowment + epigenetics — `core.py` (TraitSeed) + `epigenetics.py` (NEW)
- **`core.py::TraitSeed`:** extend to carry the **new endowment parameters** — state-vector set-points,
  drive weights `w_k`, neuromodulator reactivities (fear/opioid/oxytocin/dopamine gains), innate-
  perturbation gains (App. B.5), and physical-trait baselines. (This is the re-parameterisation that
  replaces the legacy `gains`/`access` scheme; `gains` map onto the reactivities, `access` is removed
  per 2.5.)
- **Add `epigenetics.py`:** an early-window modifier — reads accumulated early experience during
  `development.develop(...)` and **shifts the allostatic set-points/reactivities** semi-permanently
  (App. A.1(3), doc §5.2). This is the Study-3 hook (OXTR-type effects).

##### 2.8 The differential-profile plugin — `extensions/sophropathy/`
- **`society.py`:** re-express `typical_child_seed` and `fearless_child_seed` (=`shared_root_seed`) in
  the **new temperament parameters** (App. E.2); drop the `access` category weights. `sophropathic_seed`
  / `psychopathic_seed` stay as the **adult attractors** (parent seeds).
- **`world.py::study_category` + `report.py`:** implement the observer read-outs (App. E.5). No
  outcome is coded — the split must emerge from temperament × environment.
- **`module.py`:** unchanged in shape (`child_source`, `categorise`, `report` already wired).

---

#### 3. What is superseded (staged, not big-bang)

The legacy **two-affect-pathway** engine — `drives.py`'s `System`/`Brain`/`Drive` as *primitive
affect systems* and `core.py`/`agent.py`'s appraisal-as-primitive — is superseded by the **substrate
(neuraldesigner) as the source of activation** + the **valence engine (2.1/2.2) as the source of
value**. Migrate behind stable interfaces: keep `TraitSeed`, `develop`, `probe`, `classify`, the three
matrices, and the plugin contract; swap the *internals* so activation comes from the substrate and
value from the state vector. Validate behaviour parity at each step; do not delete legacy paths until
the substrate path reproduces them.

---

#### 4. Build order (dependencies)

1. **`interocept.py`** (state vector + innate perturbations + computed valence) → rewire
   `development.py`, `memory.py`. *Everything depends on this.*
2. **`learning.py`** (RPE + anticipatory value) → extend `drives.py` plasticity.
3. **Matrices** (`relations.py`, `environment_matrix.py`, `group_matrix.py`) adopt value + profile;
   add slots/enemy/ambivalent to `relations.py`; add group factors.
4. **`selection.py`** + **`executive.py`** refactor + seed nuclei → close the live loop; wire BIS→arousal.
5. **`TraitSeed` re-parameterisation** + **`epigenetics.py`**.
6. **Honesty migration** (2.5): `access` → observer read-out; grep and re-point consumers.
7. **Plugin re-expression** (2.8), depends on 5 + 6.
8. **Distillation** pooled prior (2.4), depends on 3.

---

#### 5. Risks and checks

- **Biggest risk — the legacy migration (§3).** Stage it; keep interfaces; parity-test at each step.
- **The honesty migration (2.5) touches many consumers of `access`** — grep first, migrate atomically,
  re-run the plugin's reports to confirm categories still compute (now as read-outs).
- **No new coded arbiter.** Selection (2.6) and the matrices (2.3) must not contain a rule that reads
  the situation and outputs a behaviour/category — the outcome must emerge (App. F.8 / D.2).
- **All numbers are scaffold** (set-points, gains, β/γ/α/λ, thresholds, slot sizes/decay) — calibrated
  later against the human studies; none asserted.
- **Module contract intact** — no edits to `registry.py` or `project.py`; the plugin stays discovered.

---

#### 6. The three honesty-critical changes (do not lose these)

1. **Computed valence replaces stipulated valence** (`development.py` → `interocept.py`, 2.1).
2. **Outcome-category weights migrate from seed *inputs* to observer *outputs*** (`core.py` + plugin,
   2.5) — the seed carries temperament only.
3. **Selection and biases stay emergent** — the executive is a parameter-setter, biases and the
   sophropath/psychopath split emerge, nothing is decreed (2.6, 2.8).

---

## Part III — Build instructions (Claude Code phases)

### PsychSim — Claude Code build instructions (valence/motivation subsystem)

*Executable plan for building the design in Part I via the
Part II. Written for Claude Code working in the repo. Work **one phase
at a time**, test after each, commit at each acceptance gate, and never break the invariants in §0.*

---

#### 0. Orientation and invariants (read before touching anything)

**First actions:** read Part I (the design) and Part II (the code-change map) above; read `README.md`,
`core/affective_engine/`, `core/sim_world/`, `core/modular/registry.py`, and
`extensions/sophropathy/`. Run the existing suite (`python run_tests.py`) and confirm it is green
before changing anything.

**Invariants — do not violate these in any phase:**
1. **Valence is computed, never stipulated.** No literal "warm = +0.6 / harsh = −0.7" anywhere. Value
   = drive reduction over the state vector.
2. **No coded arbiter.** Nothing may read a situation and directly output a behaviour, an emotion, or
   a category. Behaviour emerges from competition; categories are measured, not set.
3. **Named categories are observer read-outs, not primitives.** "fear", "callousness", "boldness",
   "psychopathy" are computed *over* the agent for reporting and *never fed back*. No seed carries an
   outcome category.
4. **The module contract is sacred.** Do **not** edit `core/modular/registry.py` or `project.py`.
   Studies stay discovered plugins under `extensions/`.
5. **All new numbers are scaffold.** Put every set-point, gain, rate, threshold, and capacity in a
   single discoverable place (a `params` module / clearly-named constants) so calibration can find
   them later. Add a comment `# SCAFFOLD` on each.
6. **Supersede legacy behind stable interfaces, with parity tests.** Keep `TraitSeed`, `develop`,
   `probe`, `classify`, the three matrices, and the plugin contract working at all times. Do **not**
   delete a legacy path until the new path reproduces it. Small, reversible commits.
7. **Keep the suite green.** Every phase adds tests and leaves `run_tests.py` passing.

If a design ambiguity blocks a phase, stop and surface it rather than guessing.

---

#### Phase 0 — Safety net (characterisation baseline)
- Add **characterisation tests** (`tests/test_characterisation_*.py`) that snapshot current outputs of
  `develop`, `probe`, `classify`, and the three matrices for a fixed set of seeds
  (`typical_child_seed`, `shared_root_seed`, `sophropathic_seed`, `psychopathic_seed`) × environments
  (`warm_firm_home`, `harsh_inconsistent_home`) with fixed RNG seeds. These capture *current*
  behaviour so the migration can be parity-checked.
- **Acceptance:** suite green; characterisation snapshots committed. *Commit.*

#### Phase 1 — Valence core (`interocept.py`) + rewire valence  *(honesty-critical #1)*
- Create `core/affective_engine/interocept.py`: `StateVector` (App. A variables + set-points, each
  tagged `fixed`/`allostatic`), `drive(state) -> (per_variable_vec, scalar_D)`, the **innate-
  perturbation table** (App. B: sensor→variable→direction→scaffold gain), `valence(D_prev, D_now) =
  BETA*(D_prev - D_now)`.
- Rewire `development.py`: replace the stipulated response-valence with (a) apply an event's
  perturbations to the state vector, (b) return the **computed** valence. Convert the scenario
  appraisals from *stipulated valences* to *perturbation specs*. `warm_firm_home` /
  `harsh_inconsistent_home` express perturbation patterns.
- `memory.py`: write `EpisodicMemory.valence` from the computed value; add optional per-variable
  `drive_reduction`.
- **Tests:** unit tests for drive/valence/perturbations; a parity test that the *sign and ordering* of
  valence for the canonical warm/harsh scenarios match the old qualitative behaviour (exact numbers
  will differ — that is expected and correct). Update characterisation snapshots with a note.
- **Acceptance:** `interocept` unit tests pass; `develop`/`probe` run; valence is computed. *Commit.*

#### Phase 2 — Learning (`learning.py`) + plasticity in `drives.py`
- Create `core/affective_engine/learning.py`: value function `V` (anticipatory value); TD/RPE
  `delta = r + GAMMA*V_next - V`; three-factor plasticity apply (pre × post × dopamine=delta);
  `update(cue, r, drive_profile, ...)`.
- `drives.py`: route `imprint`/`window_plasticity` through the three-factor rule (keep the window/
  critical-period gating; add the `delta` factor). Make oxytocin/opioid **gates** that license
  social-cue plasticity; dopamine carries `delta`.
- **Tests:** RPE converges on a toy task; a cue paired with drive-reduction acquires positive
  anticipatory value; the prepared-fear multiplier (§B.3) makes a flagged cue acquire aversive value
  faster than an arbitrary cue.
- **Acceptance:** learning tests pass. *Commit.*

#### Phase 3 — Matrices adopt the engine
- `sim_world/relations.py`: per-entity `value` + `drive_reduction_profile` updated via
  `learning.update`; **Dunbar layered capacity** (inner ~5, then ~15/~50/~150; SCAFFOLD sizes) with
  **decay without contact**; **allocate slots by |salience|**; each slot stores `value`, `salience`,
  `valence_sign`; support the **ambivalent** case (co-active attachment + threat toward one entity).
- `sim_world/environment_matrix.py`: value through the one engine; nature = arousal/stress drive-
  reduction (+ biophilia prior); animals via the social/oxytocin channels (a pet may take a
  `relations.py` slot); belongings = instrumental + extended-self.
- `sim_world/group_matrix.py`: keep dominance/prestige; add synchrony/endorphin belonging and the
  sociometer.
- **Tests:** slot capacity + eviction by salience; an **enemy** (negative value, high salience) holds
  an inner slot; an **ambivalent** entity is flagged; environment/group entries update by RPE.
- **Acceptance:** matrix tests pass. *Commit.*

#### Phase 4 — Behaviour selection (`selection.py`) + `executive.py` refactor + seed nuclei
- Create `core/affective_engine/selection.py`: candidates = affordances with input =
  anticipatory-value ⋅ current-drive; **accumulation-to-threshold with disinhibition** (Go release +
  NoGo + STN global hold); dopamine sets the gain (Go/NoGo balance, threshold, vigour, softmax
  temperature). All thresholds/rates SCAFFOLD.
- `executive.py`: refactor into a **parameter-setter on selection** — proactive threshold/NoGo bias,
  reactive **STN "hold"**, dACC conflict monitoring. Keep the existing monitor-learning (reversal
  learning) but route it as *which candidates to bias*, through `selection.py`. It must not pick
  actions directly.
- Seed JSON / `neuraldesigner`: ensure the **motor-selection loop nuclei** (dorsal striatum, GPe,
  GPi/SNr, motor thalamus) exist; add if absent (NAc/VTA/preSMA→STN already present).
- Wire the **BIS hook**: an unresolved approach/avoid near-tie holds the arousal variable elevated
  (feed back into `interocept.py`).
- **Tests:** a dominant-value candidate wins; a near-tie produces slow/oscillating selection **and**
  arousal stays elevated (the ambivalent-bond signature); a weakened/immature brake lets a prepotent
  high-value candidate win (impulsivity); running the maturation schedule reproduces an adolescent
  risk-taking bump that resolves with executive maturation.
- **Acceptance:** selection tests pass; the live loop closes. *Commit.*

#### Phase 5 — Endowment re-parameterisation + epigenetics (`epigenetics.py`)
- `core.py::TraitSeed`: carry the **new endowment parameters** (state-vector set-points, drive weights
  `w_k`, neuromodulator reactivities, innate-perturbation gains, physical-trait baselines). Provide a
  mapping from the legacy `gains` to reactivities so existing seeds still construct.
- Create `core/affective_engine/epigenetics.py`: an early-window modifier that reads accumulated early
  experience during `develop(...)` and **shifts allostatic set-points/reactivities** semi-
  permanently (the Study-3 / OXTR-type hook).
- **Tests:** differential susceptibility — the fearless seed diverges by environment while the typical
  seed internalises under adversity; early adversity shifts the arousal set-point and persists.
- **Acceptance:** endowment tests pass. *Commit.*

#### Phase 6 — The honesty migration: `access` → observer read-out  *(honesty-critical #2)*
- **Grep every consumer** of `TraitSeed.access` (`core.py`, `drives.py`, `agent.py`, the plugin).
- Remove the outcome-category weights (`callous_exploitation`, `strategic_prosociality`,
  `cool_instrumental_boldness`, …) from all seeds. Re-point consumers.
- Implement those categories as **observer read-outs** in `extensions/sophropathy/world.py`
  (`study_category`) and `report.py`, computed from *emergent* behaviour and substrate activity.
- **Tests:** no seed carries an outcome category; the plugin's reports still produce the categories
  (now computed, not seeded); behaviour is unchanged by the removal (they were supposed to be
  outputs).
- **Acceptance:** honesty-critical #2 done; plugin reports parity. *Commit.*

#### Phase 7 — Differential-profile plugin re-expression
- `extensions/sophropathy/society.py`: re-express `typical_child_seed` and `fearless_child_seed`
  (=`shared_root_seed`) in the **new temperament parameters** (App. E.2); `sophropathic_seed` /
  `psychopathic_seed` stay as adult attractors.
- `world.py` / `report.py`: the observer metrics (triarchic / CU / punishment-learning / reactive-vs-
  instrumental aggression), operationalised from the thesis's instruments.
- **Tests:** the sophropath/psychopath split **emerges** from temperament × environment (assert it is
  *not* coded — e.g. the same fearless seed reaches different outcomes under warm-firm vs harsh-
  inconsistent homes); a validation-target run shows the divergence.
- **Acceptance:** plugin runs; divergence emergent. *Commit.*

#### Phase 8 — Distillation + legacy retirement
- `sim_world/relations.py`: add the **pooled prior** (default disposition); initialise each entity
  from it; blend by evidence count (partial pooling); let entity estimates slowly update the prior.
- **Tests:** transference (a new entity resembling a known one inherits value); early-caregiver primacy
  (early interactions dominate the default); an ambivalent early environment yields an ambivalent
  default.
- Retire the legacy **two-affect-pathway** internals now that the substrate + valence engine reproduce
  them — behind the stable interfaces; remove or clearly deprecate dead paths.
- **Acceptance:** distillation tests pass; legacy removed/deprecated; **full suite green**. *Commit.*

---

#### Cross-cutting requirements
- **Testing:** unit + parity/characterisation per phase; keep `run_tests.py` green throughout.
- **Scaffold registry:** collect all SCAFFOLD numbers in one params module; this is the surface the
  calibration plan will target.
- **Validation hooks:** expose the observer read-outs and the named validation-target scenarios
  (ambivalent-bond conflict, adolescent risk-taking, negativity bias, differential susceptibility,
  "punishment for one = reward for another") as runnable probes for the validation phase.
- **Documentation:** update `docs/` and the affected `README.md` files as each subsystem changes.

#### The "never do" list (quick reference)
Edit `registry.py`/`project.py` · add a coded arbiter · seed an outcome category · stipulate a
valence · delete a legacy path before parity holds · leave a scaffold number un-marked · land a phase
with the suite red.

---

## Part IV — Calibration & validation plan

### PsychSim — calibration and validation plan (valence/motivation subsystem)

*How the scaffold numbers get set, and how we test that the model's behaviour concords with the
constructs — the decisive gate the thesis rests on. Companion to the design doc, code-change map, and
build instructions.*

---

#### 1. The central methodological principle (read first)

The model is only worth anything if its psychological results **emerge** rather than being fitted in.
That imposes a hard separation that the rest of this plan protects:

- **Calibration tunes low-level mechanism** — the shape of taste hedonics, a fear-extinction rate, the
  dopamine RPE signature, arousal/HRV dynamics, maturation timings — against physiology, the
  neuroscience literature, and the thesis's own studies.
- **Validation tests high-level emergent phenomena** — adolescent risk-taking curves, the negativity
  bias, approach–avoidance conflict, differential susceptibility, and above all the sophropath/
  psychopath divergence — on data and phenomena the calibration did **not** target.
- **Never tune a parameter to hit a validation target.** If we adjusted the numbers until the
  sophropath/psychopath split came out right, the model would demonstrate nothing. The split, and the
  other targets, must fall out of mechanism calibrated on *other* grounds. This is the single rule
  that separates a result from an artefact.

This mirrors what the codebase already assumes ("Stage 5 calibrates against the human studies…
nothing here is fitted to data") and the thesis's own honesty wall.

---

#### 2. The parameter inventory (what is scaffold)

Everything below is a placeholder to be set by §3, collected in one params module (per the build
instructions):

- **State vector (App. A):** per-variable set-points; `fixed` vs `allostatic` designation; drive-
  function shape/curvature; drive weights `w_k`.
- **Innate perturbations (App. B):** the gain on each hardwired sensor→variable link; the per-cue
  **learning-rate multipliers** for prepared learning.
- **Learning (App. C):** `BETA` (valence scale), `GAMMA` (discount), `ALPHA` (learning rate),
  `LAMBDA` (eligibility); the model-free/model-based arbitration weight.
- **Selection (App. F):** decision thresholds; accumulation rates; Go/NoGo and STN-hold strengths;
  softmax temperature; the tonic-dopamine operating point (inverted-U).
- **Matrices (App. 3/4):** Dunbar slot sizes and decay rates; the salience→slot mapping; the pooled-
  prior blend weight.
- **Development (§6):** circuit onset ages; plasticity/critical-period windows; the executive-
  maturation curve; the epigenetic early-window sensitivity.
- **Endowment (§5):** the *ranges and covariances* of the temperament parameters across the population
  (including the atypical/proto-disposition region — App. E).

---

#### 3. Calibration — sources and procedure

Given the model's **functional-illustrative** scope, calibration is mostly *range- and shape-based*
(getting dynamics and orderings right), not precise point-fitting. Two levels:

**3a. Low-level mechanism → physiology and the neuroscience literature.** Set the mechanistic
parameters so the components behave qualitatively as documented: taste hedonics (innate liking/
rejection), fear acquisition/extinction asymmetry and time-course, the dopamine RPE signature
(shift from outcome to predictor), arousal/HRV stress-recovery dynamics, the maturation gradient
timing (reward early, prefrontal into the mid-20s), and the opioid/oxytocin social-reward gating
(e.g. a naltrexone-analogue manipulation should *reduce* modelled social reward — a check drawn from
Løseth et al. 2024). Use the verified reference set for target behaviours; where only a direction is
known, calibrate to the direction, not a number.

**3b. Developmental mappings → the thesis's own studies.** The parent→environment and
environment→outcome mappings (`parent_to_environment`, the develop loop) are what Study 5 calibrates
against the human data (Studies 2–3). Fit the *shape* of these mappings (e.g. how caregiving warmth/
structure relate to executive-control development) to the study data, holding the mechanism from 3a
fixed.

**Procedure:** calibrate 3a first (component behaviour), then 3b (developmental mappings), then
**freeze**. Record every calibration target and its source. Anything not pinned by 3a/3b is left at a
neutral default and enters the sensitivity analysis (§5).

---

#### 4. Validation — the concordance gate

Validation runs the **observer read-outs** (Appendix D) — the simulated agent "takes the same tests"
as human participants — and compares emergent behaviour to human patterns, on phenomena **not used in
calibration**.

**4a. The validation-target battery** (each a runnable probe from the build instructions):
- the **sophropath/psychopath divergence** and its **childhood emergence** (the primary test) — the
  same proto-disposition reaching adaptive vs antisocial outcomes under warm-firm vs harsh-
  inconsistent development, matching the thesis's documented pattern;
- **differential susceptibility** (fearless child diverges by environment; typical child internalises
  under adversity);
- **adolescent risk-taking** (a curvilinear bump that resolves with executive maturation);
- the **negativity bias** ("bad is stronger than good" in learning and impression formation);
- the **ambivalent-bond** signature (approach–avoidance conflict, sustained arousal, its destructive
  behavioural pull);
- **"a punishment for one is a reward for another"** (the same event, opposite valence across
  endowments).

**4b. Types of validity to establish:**
- *Construct* — do the observer read-outs (triarchic dimensions, CU traits, punishment/passive-
  avoidance learning, aggression type) map onto the human constructs with the expected structure?
- *Predictive* — does the model reproduce patterns **not** used to calibrate it (held-out phenomena)?
- *The emergence requirement* — for each target, confirm the outcome was **not** coded (e.g. show the
  divergence appears only through temperament × environment, disappears if either is neutralised).

**4c. What counts as passing.** A target passes if the *qualitative* pattern and *ordering* match the
human data and emerge without being fitted. Given scaffold numbers, we are testing shapes and
directions, not effect sizes — claiming more would overreach the model's scope.

---

#### 5. Robustness and mechanistic checks

Because the numbers are scaffold, robustness *is* the evidence:

- **Sensitivity analysis / parameter sweeps.** Vary each scaffold parameter across a plausible range
  and check whether the validation-target phenomena **persist**. **Robust emergence** (phenomena hold
  across ranges) is strong support; **knife-edge** phenomena (appear only at one tuning) are suspect
  and must be flagged, not reported as findings.
- **Ablation.** Remove a mechanism and confirm the predicted deficit appears — knock out the opioid
  social channel → social reward collapses; remove the executive brake → impulsivity/ persistence of
  prepotent responses; flatten the maturation gradient → no adolescent bump. This is mechanistic
  validation that the phenomena come from the parts we claim.
- **Dose/manipulation checks.** Analogue manipulations should move behaviour in the documented
  direction (naltrexone→less social reward; higher tonic dopamine→more impulsive selection).

---

#### 6. Methodological guards (against circularity and researcher degrees of freedom)

- **Pre-register** the validation targets, the observer-read-out operationalisations, and the
  **calibrate-on-X / validate-on-Y split** before running validation.
- **No tuning to targets.** Parameters are set only by §3; validation is read-only. If a target fails,
  that is a *result about the model*, not a cue to adjust numbers.
- **Hold-out.** Calibrate on some studies/phenomena, validate on independent ones; never both on the
  same data.
- **Report failures.** Publish where the model does *not* reproduce the human pattern — the honest and
  informative outcome, and a guard against selective reporting.
- **Falsifiability.** State in advance what would disconfirm the model (e.g. if the sophropath/
  psychopath divergence required coding the outcome; if the biases only appeared at a single knife-
  edge tuning; if ablating a claimed mechanism left its phenomenon intact).

---

#### 7. What success and failure look like (honest criteria)

- **Success:** the validation-target phenomena emerge, in the right direction and ordering, from
  mechanism calibrated on independent grounds; they are robust across scaffold-parameter ranges;
  ablations behave as predicted; and the sophropath/psychopath divergence tracks the thesis's
  childhood-divergence data **without the outcome being coded**.
- **Failure (equally informative):** a target requires tuning-to-fit, is knife-edge, survives ablation
  of its claimed mechanism, or contradicts the human data. Any of these is reported as a limitation
  and, where possible, traced to the responsible assumption.

---

#### 8. Honesty ledger and connection to the thesis

- Calibration sets **mechanism**, validation tests **emergence** — kept strictly apart; nothing is
  tuned to produce the psychological result.
- The plan is **range/shape-based**, matching the model's functional-illustrative scope (App. A.5,
  and the substrate review): we claim the model reproduces *patterns*, not *magnitudes*.
- Calibration ties to **Studies 2–3–5** and the developmental mappings the codebase already flags for
  Stage-5 calibration; validation ties to the thesis's construct instruments (Study 1–4).
- Every scaffold number remains labelled until calibrated, and every calibration target is recorded
  with its source — so a reader can see exactly what was fitted and what emerged.

---

## Part V — Consolidated references and data verification

### V.1 Data-verification summary

The 115-reference neuroscience bibliography underpinning the substrate was verified against primary
records (CrossRef + targeted PubMed/publisher checks). **114 of 115 resolve to real, correctly-
attributed publications** — the completed workbook is `PsychSim_source_references_VERIFIED.xlsx`
(in `docs/`), with DOIs, full Harvard references, a `Found?` verdict, and correction notes per row.
Items needing action:

- **#115 Zinner 2002 — could not verify.** No matching publication in the relevant field (the known
  Zinner infant work is 1985). Treat as spurious/mis-dated: verify against the source JSON or remove.
- **#89 Sheehan 2004 — wrong year.** The real paper (medial amygdala → hypothalamus, maternal
  behaviour) is 2001 (*Neuroscience* 106:341–356). Correct the year.
- **#98 Steiner 1987 — ambiguous.** A real 1987 Steiner chapter exists (umami), but the commonly-cited
  "facial expressions … hedonics" chapter is 1977. Confirm which was intended.
- **A few one-year offsets** (Hebb 1949, Maren & Holmes 2016, Floresco 2015) are edition/epub
  artefacts, not errors. The seed JSON's "Vidal-Gonzalez 2004" is a seed slip — the xlsx already has
  the correct 2006.

**The load-bearing caveat:** a verified citation grounds a pathway's *existence and direction*; it
never grounds the substrate's newborn weights, time-constants, or plasticity curves. Those remain
scaffold until calibrated (Part IV).

### V.2 Consolidated reference list

Grouped by area. Marked **[V]** = verified this session with the DOI shown; **[S]** = verified in the
substrate's own reference set (earlier work); **[C]** = standard/classic, cited from established
knowledge — confirm exact citation before thesis use.

**Valuation engine — homeostatic RL, reward-prediction error, value**
- **[V]** Keramati, M., & Gutkin, B. (2014). Homeostatic reinforcement learning for integrating reward collection and physiological stability. *eLife, 3,* e04811. https://doi.org/10.7554/eLife.04811
- **[C]** Keramati, M., & Gutkin, B. (2011). A reinforcement learning theory for homeostatic regulation. *NIPS 24.*
- **[S]** Schultz, W. — dopamine reward-prediction error.
- **[V]** Frémaux, N., & Gerstner, W. (2016). Neuromodulated spike-timing-dependent plasticity, and theory of three-factor learning rules. *Frontiers in Neural Circuits.*
- **[S]** Milad, M. R., & Quirk, G. J. (2002). Neurons in medial prefrontal cortex signal memory for fear extinction. *Nature, 420,* 70–74. https://doi.org/10.1038/nature01138
- **[C]** Berridge, K. C., & Robinson, T. E. (1998/2016). Incentive-salience ("liking" vs "wanting").
- **[C]** Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction.* · Montague, Dayan & Sejnowski (1996), *J. Neurosci.* · Daw, N. D., et al. (2005/2011), model-based/model-free arbitration. · Niv, Y. (2007), tonic dopamine and vigour.

**Interoception, valence, allostasis (the state vector)**
- **[S]** Barrett, L. F., & Simmons, W. K. (2015). Interoceptive predictions in the brain. *Nat. Rev. Neuroscience.*
- **[S]** Seth, A. K. (2013). Interoceptive inference, emotion, and the embodied self. *TiCS.*
- **[S]** Craig, A. D. (2002). Interoception: the sense of the physiological condition of the body. *Nat. Rev. Neuroscience, 3,* 655–666.
- **[V]** McEwen, B. S. (1998). Stress, adaptation, and disease: allostasis and allostatic load. *Ann. NYAS, 840,* 33–44. https://doi.org/10.1111/j.1749-6632.1998.tb09546.x
- **[V]** Sterling, P. (2012). Allostasis: a model of predictive regulation. *Physiology & Behavior, 106,* 5–15.
- **[C]** Sterling, P., & Eyer, J. (1988). Allostasis: a new paradigm to explain arousal pathology.
- **[S]** Ziemann, A. E., et al. (2009). The amygdala is a chemosensor that detects CO2 and acidosis. *Cell.* · Ulrich-Lai, Y. M., & Herman, J. P. (2009). Neural regulation of endocrine and autonomic stress responses. *Nat. Rev. Neuroscience.*
- **[C]** Borbély, A. A. (1982). A two-process model of sleep regulation. · Loewenstein, G. (1994). The psychology of curiosity. *Psychol. Bull., 116,* 75–98.

**Social value — homeostasis, opioids, oxytocin, development**
- **[V]** Matthews, G. A., & Tye, K. M. (2019). Neural mechanisms of social homeostasis. *Ann. NYAS.* https://doi.org/10.1111/nyas.14016
- **[C]** Lee, C. R., Chen, A., & Tye, K. M. (2021). The neural circuitry of social homeostasis. *Cell.* · Matthews, G. A., et al. (2016). DRN dopamine neurons and social isolation. *Cell.*
- **[C]** Machin, A. J., & Dunbar, R. I. M. (2011). The brain opioid theory of social attachment. *Behaviour.*
- **[V]** Løseth, G. E., et al. (2024). Endogenous mu-opioid modulation of social connection in humans: a meta-analysis. *Transl. Psychiatry, 14,* 379. https://doi.org/10.1038/s41398-024-03088-3
- **[V]** Dölen, G., Darvishzadeh, A., Huang, K. W., & Malenka, R. C. (2013). Social reward requires coordinated activity of nucleus accumbens oxytocin and serotonin. *Nature, 501,* 179–184. https://doi.org/10.1038/nature12518
- **[S]** Nardou, R., et al. (2019). Oxytocin-dependent reopening of a social reward learning critical period with MDMA. *Nature.*
- **[V]** Vernetti, A., Smith, T. J., & Senju, A. (2017). Gaze-contingent reinforcement learning reveals incentive value of social signals. *Proc. R. Soc. B, 284,* 20162747. https://doi.org/10.1098/rspb.2016.2747
- **[C]** Csibra, G., & Gergely, G. (2009). Natural pedagogy. *TiCS.*

**Environment matrix — nature, animals, belongings**
- **[V]** Ulrich, R. S., et al. (1991). Stress recovery during exposure to natural and urban environments. *J. Environ. Psychology, 11,* 201–230. (Stress Reduction Theory)
- **[C]** Wilson, E. O. (1984). *Biophilia.* Harvard UP. · Kaplan, R., & Kaplan, S. (1989). *The Experience of Nature.* (Attention Restoration Theory)
- **[V]** Nagasawa, M., et al. (2015). Oxytocin-gaze positive loop and the coevolution of human–dog bonds. *Science, 348,* 333–336. https://doi.org/10.1126/science.1261022
- **[C]** Belk, R. W. (1988). Possessions and the extended self. *J. Consumer Research, 15,* 139–168.

**Group matrix — belonging, synchrony/endorphins, status, esteem**
- **[V]** Tarr, B., Launay, J., Cohen, E., & Dunbar, R. (2015). Synchrony and exertion during dance independently raise pain threshold and encourage social bonding. *Biology Letters, 11,* 20150767. https://doi.org/10.1098/rsbl.2015.0767
- **[V]** Dunbar, R. I. M. (2022). Laughter and its role in the evolution of human social bonding. *Phil. Trans. R. Soc. B, 377,* 20210176. https://doi.org/10.1098/rstb.2021.0176
- **[C]** Tarr, B., Launay, J., & Dunbar, R. (2017). Naltrexone blocks endorphins released when dancing in synchrony. · Baumeister, R. F., & Leary, M. R. (1995). The need to belong. *Psychol. Bull., 117,* 497–529. · Leary, M. R., et al. (1995). Sociometer hypothesis. *JPSP.* · Henrich, J., & Gil-White, F. J. (2001). Dominance vs prestige.

**Relationship layers and negativity (slots and enemies)**
- **[C]** Dunbar, R. I. M. (1992). Neocortex size as a constraint on group size in primates. *J. Human Evolution.* / (1998) The social brain hypothesis. · Zhou, Aleman & Dunbar (2005); Hill & Dunbar (2003) — layered ego networks (5/15/50/150).
- **[V]** Baumeister, R. F., Bratslavsky, E., Finkenauer, C., & Vohs, K. D. (2001). Bad is stronger than good. *Review of General Psychology, 5*(4), 323–370. https://doi.org/10.1037/1089-2680.5.4.323
- **[C]** Rozin, P., & Royzman, E. B. (2001). Negativity bias, negativity dominance, and contagion. *Pers. Soc. Psychol. Review, 5*(4), 296–320.

**Behaviour selection and competition**
- **[V]** Redgrave, P., Prescott, T. J., & Gurney, K. (1999). The basal ganglia: a vertebrate solution to the selection problem? *Neuroscience, 89,* 1009–1023. https://doi.org/10.1016/s0306-4522(98)00319-4
- **[V]** Gurney, K., Prescott, T. J., & Redgrave, P. (2001). A computational model of action selection in the basal ganglia (I & II). *Biological Cybernetics, 84.*
- **[V]** Frank, M. J. (2006). Hold your horses: a dynamic computational role for the subthalamic nucleus in decision making. *Neural Networks, 19.*
- **[V]** Bogacz, R., & Gurney, K. (2007). The basal ganglia and cortex implement optimal decision making. *Neural Computation, 19.*
- **[S]** Aron, A. R., & Poldrack, R. A. (2006); Aron, A. R., Robbins, T. W., & Poldrack, R. A. (2014). Inhibition and the right inferior frontal cortex. *TiCS, 18,* 177–185.
- **[C]** Mink, J. W. (1996); Cisek, P. (2006), affordance competition; Niv, Y. (2007); Collins, A. G. E., & Frank, M. J. (2014); Cools, R., & D'Esposito, M. (2011), dopamine inverted-U; Gray, J. A., & McNaughton, N. (2000). *The Neuropsychology of Anxiety* (behavioural inhibition system).

**Development, endowment, epigenetics, distillation**
- **[V]** Steinberg, L. (2010). A dual systems model of adolescent risk-taking. *Developmental Psychobiology, 52,* 216–224. https://doi.org/10.1002/dev.20445
- **[V]** Strang, N. M., Chein, J. M., & Steinberg, L. (2013). The value of the dual systems model of adolescent risk-taking. *Front. Hum. Neuroscience, 7,* 223. https://doi.org/10.3389/fnhum.2013.00223
- **[C]** Casey, B. J., et al. (2008); Shulman, E. P., et al. (2016) — maturational imbalance. · Cecil, C. A. M., et al. (2014) — OXTR methylation and environmental risk (thesis refs). · Bowlby, J. (1969). *Attachment.* · Bretherton, I. (1992), internal working models. · Shepard, R. N. (1987). Toward a universal law of generalization. *Science.*

**Psychopathy / sophropathy constructs (the thesis's own domain — defer to its definitions)**
- **[S]** Newman, J. P., et al. (1999) — response modulation / reward dominance.
- **[C]** Lykken, D. T. (low-fear hypothesis). · Patrick, C. J., Fowles, D. C., & Krueger, R. F. (2009), triarchic model. · Blair, R. J. R. (amygdala/empathy). · Frick, P. J. (callous-unemotional traits). · Belsky, J., & Pluess, M. (differential susceptibility). · Hare, R. D. (PCL-R).

**Innate perceptual/prepared-learning priors (substrate set)**
- **[S]** Öhman, A., & Mineka, S. (2001) — prepared fear. · Cook, M., & Mineka, S. (1990). · Steiner, J. E. (1973/1977) — innate gustofacial hedonics. · Simion, F., et al. (1998) — newborn face orienting. · Schiff, W. (1965) — looming. · Koch, M. (1999) — startle.

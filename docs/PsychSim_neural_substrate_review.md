# PsychSim — Review of the neural-substrate direction and its data

*Companion to the updated `PsychSim_Design_Document.md`. Two decisions were asked for:
(1) is the proposed category-free neural substrate achievable and a good direction; and
(2) which of the gathered research data is useful, accurate, and verifiable. This memo
answers both, and states plainly what it could and could not check.*

---

## Decision 1 — Is the neural substrate achievable, and a good direction?

**Verdict.** The architectural pivot is right and worth committing to. But the maximalist
framing of it — "a working circuit model of the human brain, in which characters evolve
through childhood *exactly like a human*" — is **not achievable**, by this project or by
the field as it stands today, and taken literally it is the single biggest threat to the
thesis's examinability. The recommendation is therefore split: **adopt the architecture;
retire the maximalist claim; hold the ambition at the functional/illustrative level the
seed's own discipline already implies; and let complexity be *earned* by the behavioural
validation gate rather than pursued for completeness.**

**Why the pivot itself is correct.**

- Retiring Panksepp-as-foundation fixes a genuine error, and for the reason the design
  record already gives: the seven systems are *output categories*, and building the
  mechanism out of them smuggles the answer into the substrate — the one thing Principle 1
  forbids. A category-free substrate whose activity is *read out* as emotion removes that
  problem at the root and, as a bonus, sits neutrally between Panksepp's basic-emotion view
  and Barrett's constructionist view rather than committing to hardwired emotions. For a
  project whose whole credibility rests on "we did not encode the outcome," this is not
  cosmetic — it strengthens the load-bearing wall.
- The embodiment insight — that emotion arises from the interaction of interoceptive,
  proprioceptive and sensory signals with the circuitry that appraises them — is
  well-founded, not a flourish (Damasio's somatic-marker line; Barrett & Simmons on
  interoceptive prediction; Craig and Critchley on the insula). Adding an
  interoceptive–autonomic system and proprioception is principled.
- Development as the sculpting of connection strengths through maturing circuitry is exactly
  the mechanism a life-course study of divergent outcomes needs, and exactly what a
  seven-dial model could not represent. This is the real intellectual payoff.

**Why "exactly like a human brain" is not achievable — and is a trap.**

- There is no validated, runnable, whole-brain circuit model of the human brain. This is one
  of the largest open problems in neuroscience; the largest efforts in the world
  (Blue Brain / Human Brain Project, the Allen atlases, the connectome projects) have not
  produced a runnable brain that generates human emotion and behaviour from first
  principles. A doctorate cannot build what the field has not.
- The seed data itself concedes the gap at every line, and this is to its credit: newborn
  weights are qualitative assumptions (the literature reports *adult* patterns, not birth
  strengths); the dynamics — time constants, plasticity/eligibility/homeostatic timescales,
  structural-plasticity thresholds — are marked **SCAFFOLD**, to be replaced by measured
  values; the evidence base is largely `animal_dominant` or `human+animal` applied to a
  human model; and the confidence tier on the connections sampled is overwhelmingly the
  lowest. The honest description of the artefact is therefore *a functional, mechanistic
  sketch at nucleus grain with mostly-assumed parameters* — which is a legitimate and
  interesting thing to build, but it is categorically not "a working model of the human
  brain."
- There is an irony worth internalising. The reason given for dropping Panksepp is that his
  work was "just observational." But the *more* biophysically faithful you try to be, the
  *more* you depend on precisely that kind of empirical grounding — and the less of it
  exists in runnable, parameterised form. The pivot is right at the level of *architecture*
  (don't build out of the output categories); the *ambition* ("faithful biophysical brain")
  runs in the opposite direction to where the evidence can currently support you. Keeping
  the architecture while holding the ambition at the functional level resolves the tension.

**The practical risk if the maximalist version is pursued.** Every added circuit, connection
and schedule is a free parameter, and most are assumed. Each is a degree of freedom and a
place where the researcher's expectations can leak in. The thesis's decisive gate is
*behavioural concordance* — does the simulation *behave* in accordance with the constructs?
A richer substrate does not automatically improve concordance; it can make it harder to
achieve and much harder to attribute (if the sim produces psychopath-like behaviour, was it
the mechanism, or one of a thousand assumed knobs?), and it makes the "no encoded effect"
audit far more laborious, because you must show that *none* of those knobs encodes the
outcome. Breadth for its own sake buys audit burden without buying evidential weight.

**The achievable, defensible version (recommended).**

1. Keep the category-free architecture and the embodiment layer. This is the novel, sound
   core.
2. Describe it, in the thesis and the docs, as a **functional, illustrative** model — a
   mechanistic sketch at nucleus grain, with parameters confidence-coded and dynamics marked
   scaffold. Make that honesty a *headline*, not a footnote: it is the source of the model's
   credibility. The phrase "evolves exactly like a human" should appear, if at all, as a
   stated *aspiration and direction*, explicitly not as a description of the code.
3. Let complexity be earned. Add a system only where (a) it changes behaviour the validation
   gate can see, and (b) its parameters can be grounded or are honestly flagged. The
   threat / reward / executive triad plus interoception is already enough to test the Study 4
   hypothesis; further breadth is optional scaffolding, not a prerequisite.
4. Physical and genetic endowment (attractiveness, health, dexterity, …) belong in, but only
   as **initial conditions that change what the world does to the agent** — an attractive or
   capable child elicits different responses and attempts different things, and *those
   experiences* drive the plasticity. Wiring "attractive → confident" directly would be the
   encoded outcome the honesty wall forbids. (Note: the *sensory system* you list as a
   coming addition is in fact already substantially designed in the seed; proprioception and
   a fuller interoceptive loop are the genuine near additions.)
5. Keep behavioural concordance as the governing test throughout, and keep calibration to the
   human studies (Study 2, Study 5) named as the step that fixes *inputs*, never the engine's
   responses.

---

## Decision 2 — Which of the data is useful, accurate, and verifiable?

**This is now settled: I verified all 115 references in `PsychSim_source_references_TO_VERIFY.xlsx`
against primary records.** The completed workbook, `PsychSim_source_references_VERIFIED.xlsx`,
has the DOI, the full Harvard reference, a `Found?` verdict, and correction notes filled in for
every row. Method: each reference was resolved against the CrossRef API (author + year +
field-consistent title, returning a DOI), and the residual and ambiguous entries were confirmed
by targeted web search against PubMed / publisher records.

**Headline: 114 of 115 are real, correctly-attributed publications.** This is the important — and
slightly surprising — result. Despite the worksheet's own honest warning that 82 of the citations
were "memory-derived" (written from the model's training knowledge, and so at "higher risk of a
plausible-looking reference that does not exist"), they turned out to be overwhelmingly genuine,
canonical papers: the standard references a well-read neuroscientist would cite. There is no
evidence of wholesale fabrication. The fear that a confused session had produced a 172-item-style
liability is simply not borne out for this list.

**Four things need your action** (all flagged in the workbook):

- **#115 Zinner 2002 — could not verify.** No publication matches this author-year in the relevant
  field; the only known Zinner infant work is 1985. Treat it as spurious or mis-dated — check the
  source JSON or drop it. This is the single entry that behaves like the failure mode you were
  worried about.
- **#89 Sheehan 2004 — wrong year.** The real paper (medial amygdala -> hypothalamus, maternal
  behaviour) is 2001 (Neuroscience, 106, 341-356). Correct the year.
- **#98 Steiner 1987 — ambiguous year.** A real 1987 Steiner chapter exists (on umami), but the
  commonly-cited "facial expressions ... hedonics of food-related chemical stimuli" chapter is
  1977. Confirm which was intended.
- **A handful of one-year offsets** (e.g. Hebb 1949, Maren & Holmes 2016, Floresco 2015) are
  edition or epub-vs-print artefacts, not errors — the cited year is fine.

(Separately: the seed JSON I read earlier cited "Vidal-Gonzalez 2004", but the xlsx already carries
the correct 2006 — so that particular slip lives in the seed data, not in this reference list, and
is worth fixing in the JSON.)

**So which data can you use?** Effectively all of it, as a *bibliography*. The reference base the
substrate rests on is sound, and you now have verified DOIs and full references for the whole list.
Two caveats carry over unchanged, and they matter more than the citation check did:

1. **Evidence base.** Much of the mechanistic detail is rodent / primate work applied to a human
   functional model. That is normal and defensible, but the write-up must say so; the seed's
   `evidence_base` field already does.
2. **A verified citation is not a verified parameter.** This is the point to hold onto. Every one of
   these papers supports the *existence and direction* of a pathway — that the vmPFC is involved in
   extinction, that the right IFG brakes responses. **None of them supplies the newborn connection
   weight, the time constant, or the plasticity curve.** Those are the values marked "assumed" and
   "scaffold", and they stay unmeasured no matter how solid the reference beside them is. A page of
   real, verified citations can create a false impression that the *numbers* are grounded; they are
   not. What the reference base legitimately buys you is the substrate's *shape* — which circuits,
   wired which way, coming online roughly when — not its quantitative dynamics.

## One-paragraph summary

Commit to the category-free substrate — it is the right architecture and it strengthens the
discipline the thesis depends on — but describe it honestly as a functional, illustrative model,
drop the "working human brain, exactly like a human" claim as a literal goal, and add systems only
as the behavioural-concordance gate earns them. On the data: the full 115-reference list has now
been verified — 114 are real, correctly-attributed papers, so the substrate's bibliography is
sound and DOIs are filled in (`PsychSim_source_references_VERIFIED.xlsx`); fix the one unverifiable
entry (Zinner 2002) and the year on Sheehan (2001, not 2004), and confirm Steiner 1987. The single
caveat that matters most is unchanged: these citations justify the substrate's *shape*, never its
*numbers*, which remain assumed until calibrated.

# v14 Phase-2 kinship integration — nepotism wired and proven (ledger)

**Design authority:** `docs/PsychSim_v14_Kinship_Attachment_SPEC.md` + `docs/PsychSim_v14_Phase2_Integration_Handover.md`.
Phase-2 **core** (`signature.py` — the bearer signature + self-referent `signature_match`) was cleared
earlier. This is the Phase-2 **integration**: wire `signature_match` into the substrate so kin-recognition
drives behaviour, and prove **nepotism emerges** (never coded). Depends on the Part-1 PVN-OT afferent
completion (`docs/PsychSim_v14_PVN-OT_afferent_completion.md`) — the OT bonding hub had to be drivable first.

## The route the biology picked: through oxytocin
Oxytocin is the mediator of **both** social *recognition* ([Oettl et al. 2016, *Neuron*](https://pmc.ncbi.nlm.nih.gov/articles/PMC4860033/))
and social *reward* ([Dölen et al. 2013, *Nature*](https://www.nature.com/articles/nature12518); [Hung et al.
2017, *Science*](https://www.science.org/doi/10.1126/science.aan4994) — OT signals the salience of a
*familiar* partner in NAc/VTA). So a kin-recognition signal reaching affiliation runs **through oxytocin**.

The handover's original sketch (kin cue → MeA → affiliation) was **anatomically backwards** and was not built:
`MeA` is GABAergic (sign −1), inhibits its one affiliation target (`MPOA`), and pushes the defensive/attack
side — driving it would produce *aggression*, not nepotism (validated empirically). The biology-picked route
routes the cue to the OT system instead.

## What was built
- **`IN-CONSPEC:kin_signature → PVN-OT`** (input edge, `innate_reinforcer`, moderate-strong; cited Oettl
  2016 / Dölen 2013 / Hung 2017). The kin-recognition cue drives oxytocin → the now-working Phase-1 bonding
  scaffold (`PVN-OT → NAc-shell/MeA/SEPT/MPOA`) → affiliation. One edge; reuses everything Part 1 built.
  Collapses the chemosignal-detection→OT relay into the sensory drive, mirroring `affective_touch → PVN-OT`.
- **Signature at spawn** (`agent.py`): each seeded agent samples `random_signature` from a distinct sub-seed
  (independent of the physical draw, reproducible); `self_signature` is the perceiver-role accessor. Banked
  verbatim (`DevelopedAgent`/snapshot/restore/`grow_adult`) — restored-never-edited, mirroring `physical`.
- **`_add_signature_percept`** (`arena.py`, mirrors `_add_physical_percept`): computes
  `signature_match(bearer.signature, perceiver.self_signature)` and adds it as the `kin_signature` cue; called
  at the same site, before `felt_response`. Trigger `kin_signature → IN-CONSPEC:kin_signature` in `social.py`.
- **`child_signature` is NOT called** — no reproduction-from-parents exists yet, so relatedness→shared-loci
  has no spawn site; every spawned agent is UNRELATED (`random_signature`). Ready for Phase 3.

## The keystone — proven (this is the deliverable)
**"Relatedness enters as a cue, not a behaviour."** The grep-gate is clean: every occurrence of
"relatedness"/"kinship" across the kin path is in comments/docstrings; **no functional code downstream of
spawn takes a relatedness term.** The functions are signature-only: `signature_match(bearer_sig,
perceiver_self_sig)`, `_add_signature_percept(percept, perceiver, bearer)`. Relatedness's only causal role is
upstream at spawn (`child_signature`, a function of parent *signatures*, setting shared loci) — and that isn't
even wired yet. Nepotism emerges from the perceiver's circuits valuing a self-similarity cue (OT → bonding),
never a coded similarity→affiliation coefficient.

## Verification
- **Nepotism emerges, monotonically** (constructed similarity gradient through the real percept path): loci
  overlap 0 → 1 gives affiliation-drive 0.001 → 0.100 → 0.201 → 0.303 → 0.420, PVN-OT 0.075 → 0.775, and the
  affiliative act (`nurture`) **wins** at ≥ 0.75 similarity. Higher kin-similarity → more OT → more affiliation.
- **Self-referent + signature-only**: the cue is `signature_match(bearer, perceiver-self)` (Phase-2 core,
  verified); grep-gate clean.
- **Dormant-but-present in the current sim** (honest): all agents unrelated (`random_signature`) → match ≈ 0
  → the kin cue is ≈ 0 → behaviour barely shifts (characterisation golden unchanged). The mechanism is wired
  and proven; it activates when reproduction creates genuine kin (Phase 3).
- **Intact**: v9 aggression closure, Phase-1 bonding, cue→reward learning, the signature core, the bank
  round-trip (signature banked/restored). Full suite green.

## Deferred (flagged, not dropped)
Whether to represent the **neural substrate** of self-referent recognition as explicit circuitry
(`MeA → aIns/dmPFC` "this matches me") — recorded in the seed's `gaps_register`. Not needed for the kinship
mechanism (recognition is a perceptual match, correctly located in `signature_match`; keystone-clean), but
potentially wanted for anatomical completeness or a future social-cognition/CU study of the recognition
substrate itself. **Not** built now (unmotivated for Part 2; changes neither behaviour nor honesty).

## Net change
+1 grounded cited input edge (`IN-CONSPEC:kin_signature → PVN-OT`); signature spawn+banking wiring;
`_add_signature_percept` + its trigger; a gaps_register flag. No existing edge changed. Phase-2 wires and
proves v14's central claim — nepotism as an emergent consequence of self-similarity valued through oxytocin,
with relatedness a spawn-time cue and never a coded behaviour.

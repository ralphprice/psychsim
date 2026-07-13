# v14 Phase 2 Integration — Claude Code handover

**Design authority: `docs/PsychSim_v14_Kinship_Attachment_SPEC.md`.** This resumes v14 (kinship/attachment)
after the HSO detour landed. Phase 2 **core** is cleared on origin/main (`signature.py` — the bearer
signature vector + self-referent `signature_match`, both honesty checks verified). This handover is the
Phase 2 **integration**: wire the verified `signature_match` into the substrate so kin-recognition
actually drives behaviour, and verify **nepotism emerges** (never coded).

Context: the substrate is post-restoration (622b2a3) — the settled weight philosophy applies. Any new
associative site this phase adds starts at its **band and grows through experience** (§2.11 category 3) —
**no near-zero, no HSO, no setpoints.** Backbone/anatomy edges are grounded at their strength.

---

## 0. What Phase 2 integration IS and IS NOT

- **IS:** feed the perceiver's `signature_match(bearer, self)` into the substrate as a **kin cue**, through
  the SAME percept path physical cues use (`felt_response`), so perceived kin-similarity produces an
  affiliative felt response that feeds the Phase-1 OT/VP bonding circuits — and verify nepotism EMERGES
  (higher similarity → more affiliation, measured).
- **IS NOT:** coding a relatedness→behaviour rule; adding a similarity→affiliation coefficient; making the
  match take relatedness as input; or building Phase 3+ (imprinting, dissolution, extended kin). Just the
  cue→percept→emergence wiring for the signature.

---

## 1. The critical correction from the actual code (read before building)

The kinship SPEC sketched "add `IN-OLF:kin_signature → MeA` edges." **`IN-OLF` and `IN-CONSPEC` are NOT
circuit nodes** — they are **cue channels in the trigger vocabulary** that `felt_response` consumes (the
same way physical cues enter). So the kin-signature does NOT enter at a fictional `IN-OLF` node. It enters
**exactly like a physical percept does** — as a cue fed through `felt_response`, which routes it via the
existing perception edges into the perceiver's OWN circuits. Mirror the v10 precedent precisely:

- **The precedent:** `core/arena.py:256` `_add_physical_percept(percept, perceiver, bearer)` — computes
  `physical_stimulus(bearer_physical)` (a bearer-pure cue dict), adds those cues to the `percept`, and the
  percept is fed through `felt_response` (`core/substrate/social.py:170`) — "the same path Things use,"
  routing the triggers via `IN-CONSPEC` edges into the perceiver's own circuits, which value them. **No
  valuation in the cue; the valuation emerges from the perceiver's wiring.**

So Phase 2 integration adds the *signature analogue* of `_add_physical_percept`.

---

## 2. The build (mirror `_add_physical_percept` exactly)

### 2.1 `_add_signature_percept` (the analogue)
Add a function paralleling `_add_physical_percept`: for a perceiver observing a bearer, compute
`signature_match(bearer.signature, perceiver.self_signature)` (the verified Phase-2-core function) and add
the resulting kin-similarity as a **cue** in the `percept` dict — a bearer-pure cue, exactly as
`physical_stimulus` produces physical cues. Then the existing `felt_response` path routes it into the
perceiver's own circuits.

- **Signature as a bearer property:** the signature vector is set at spawn (`random_signature` /
  `child_signature`, already in `signature.py`); relatedness → shared loci ONLY at spawn. The perceiver
  also carries its own `self_signature` (a bearer fact about itself).
- **The cue is the MATCH, computed by the perceiver:** `signature_match(bearer_sig, perceiver_self_sig)`
  — a function of the two vectors ONLY. Relatedness NEVER enters this computation (it's not a parameter;
  it only set the loci at spawn). **Grep-gate: no relatedness term anywhere in the percept/match path.**
- **Call site:** mirror `arena.py:287` where `_add_physical_percept` is called before `felt_response` —
  add `_add_signature_percept` in the same place, so the kin cue joins the percept the same way the
  physical cue does.

### 2.2 The routing into the perceiver's circuits (the cue's destination)
The kin cue, once in the percept, must route (via `felt_response`'s trigger→circuit mapping) into the
self-referent kin-recognition substrate and thence to affiliation. The nodes exist (`MeA`, `aIns`, `mIns`,
`pIns`, `dmPFC` are all present; `MeA` already receives `PVN-OT→MeA`, `PIR→MeA`, `V-ventral→MeA`). Wire the
kin cue → `MeA` (the vomeronasal/social-cue amygdala) → `aIns`/`dmPFC` (self-referent processing) →
affiliation, **using the felt_response trigger vocabulary + seed edges**:
- If the trigger→`MeA` routing and `MeA→aIns`/`dmPFC`→affiliation edges already exist, reuse them.
- If a routing edge is genuinely absent, add it as a **cited seed edge** (Mateo & Johnston 2000 for
  phenotype-matching kin recognition; the insula/dmPFC self-referent-processing substrate). New associative
  routing edges start at their **band and grow** (settled philosophy — NOT near-zero); the `MeA` social-cue
  routing is grounded anatomy (backbone) at its band.
- **Self-referent is preserved by construction:** the cue IS `signature_match(bearer, perceiver-self)`, so
  it already encodes "similarity to the perceiver's own signature." The routing carries that self-referent
  similarity — it does NOT compare to a family template or averaged-kin signature.

### 2.3 Emergence (the point — nepotism is MEASURED, never coded)
Perceived kin-similarity → (via the perceiver's circuits) an affiliative felt response → feeds the Phase-1
OT/VP bonding circuits (`PVN-OT→NAc-shell` etc.). **Nepotism must EMERGE:** an agent developed among kin
vs. strangers shows higher affiliation toward higher-signature-similarity others — as a *consequence* of
the matching feeding the bonding circuits, NOT a coded similarity→affiliation coefficient. There is NO
"relatedness → more affiliation" term anywhere; there is only "the perceiver's circuits value a cue that
happens to be self-similarity," and nepotism falls out.

---

## 3. Verification

- **Nepotism emerges:** higher `signature_match` → more affiliation (measured across a similarity gradient),
  feeding the OT/VP circuits. Report the gradient (similarity vs. affiliation), not a single point.
- **The two honesty checks (the keystone — verified before, must hold in the percept path now):**
  1. **Match is signature-only:** `_add_signature_percept` computes from `(bearer_sig, perceiver_self_sig)`
     and NEVER takes relatedness. Relatedness appears ONLY at spawn (setting shared loci). **Grep-gate the
     percept/match path — no relatedness term downstream of spawn.**
  2. **Self-referent:** the match is against the perceiver's OWN `self_signature`, not a family template or
     averaged-kin signature (it is, by `signature_match`'s construction — confirm the percept passes
     `perceiver.self_signature`, not something else).
- **Signature is a pure bearer property** (like `physical`) — set at spawn, sex-neutral, no valuation in
  the cue.
- **Byte-additive to structure elsewhere** — only the signature percept + its routing are added; no other
  circuits/edges/signs change. Any new routing edge is cited.
- **Full suite green** — the gate. Behaviour shifts (kin cue now drives affiliation), so the golden
  regenerates and the library regrows. **Green honestly** — nepotism emerging from the wiring, not coded.
- **v9 closure + Phase-1 bonding intact** — the kin cue adds to, doesn't disrupt, the existing circuits.

---

## 4. Honesty + process
- **Settled weight philosophy applies:** new associative routing sites start at band + grow (NOT
  near-zero); grounded anatomy (the MeA social-cue routing) at its band. No HSO, no setpoints, no
  near-zero — that whole direction is shelved.
- **The keystone is the point of this phase:** "relatedness enters as a cue, not a behaviour." The grep-gate
  (no relatedness downstream of spawn) is what proves it. This is where v14 earns its central claim.
- **Full suite is the gate** (not inline checks). Golden regenerates, library regrows.
- **Dual-reviewed:** the reviewer verifies against the remote that (a) the match in the percept path is
  signature-only and self-referent, (b) nepotism EMERGES (gradient measured, not a coded coefficient), (c)
  any new routing edge is cited and at-band (not near-zero), (d) suite green.
- **Commit + push + STOP for reviewer clearance before Phase 3.**

---

## 5. Hand-off note (for the implementation session)

> **v14 Phase 2 integration — wire the verified `signature_match` into the substrate so nepotism emerges.**
> Design authority: `docs/PsychSim_v14_Kinship_Attachment_SPEC.md`. Phase 2 core (`signature.py`,
> self-referent `signature_match(bearer, perceiver-self)`) is cleared on origin/main. Post-restoration
> substrate (622b2a3) — settled weight philosophy: new associative sites start at band + grow, NO
> near-zero/HSO.
>
> **CORRECTION from the code:** `IN-OLF`/`IN-CONSPEC` are NOT nodes — they're cue channels `felt_response`
> consumes. So the kin cue enters EXACTLY like a physical percept: add `_add_signature_percept` mirroring
> `_add_physical_percept` (`arena.py:256`) — compute `signature_match(bearer.sig, perceiver.self_sig)`, add
> it as a bearer-pure CUE in the percept, and `felt_response` (`social.py:170`) routes it into the
> perceiver's OWN circuits (→ `MeA` [present, already receives PVN-OT/PIR/V-ventral] → `aIns`/`dmPFC` →
> affiliation). Reuse existing routing edges; add any genuinely-missing one as a CITED seed edge (Mateo &
> Johnston 2000; insula/dmPFC self-referent substrate) at its band (not near-zero).
>
> **The keystone:** the match is a function of the two signature vectors ONLY — relatedness NEVER enters
> the percept/match path (it set the shared loci at spawn, nothing downstream). Grep-gate it. Self-referent:
> match against the perceiver's OWN self_signature, not a family template. **Nepotism must EMERGE** (higher
> match → more affiliation, MEASURED across a gradient, feeding the Phase-1 OT/VP bonding circuits) — never
> a coded similarity→affiliation coefficient.
>
> **Verify:** nepotism gradient emerges; the two honesty checks hold in the percept path (signature-only,
> self-referent); signature is a pure bearer property; new routing edges cited + at-band; full suite green
> (golden regen, library regrow) HONESTLY; v9 + Phase-1 bonding intact. Process: full suite is the gate;
> dual-reviewed (reviewer verifies signature-only + self-referent + nepotism-emerges + cited-at-band edges +
> green on the remote); commit + push + STOP for clearance before Phase 3.

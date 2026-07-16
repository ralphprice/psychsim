# D6 fix #2 — LC's afferent set: diagnostic (NOTHING built; surface first)

The verdict and the principle-1 root cause hold. This is the Phase-1 diagnosis of `LC`'s real afferent set
against the literature, plus the `PVN-OT` check the spec demanded. **Nothing built.** One correction to the
spec's own numbers, one addition, one hazard the spec did not name.

## 1. `LC`'s current afferent set — and the quantified entailment
```
CeA -> LC   band = moderate (0.50)   receptor = CRF-R1     ← the SOLE external afferent
LC  -> LC   band = moderate           receptor = alpha2     ← the α2 autoreceptor
```
**⟳ Stale-memory correction (read the file): `CeA → LC` is `moderate`, not `moderate-strong`.** The
discipline is unchanged — do not touch it — but the fix must be scoped to the real band.

**The entailment, quantified (Phase-3 baseline):** throttle `AFFECTIVE_EMPATHY` → `LC` collapses **54 % at
rest, 72 % under threat, 73 % under distress** (to a floor of 0.100). Because `CeA` is the sole external
afferent, the affective throttle owns almost all of LC's drive. Principle 1: a minor dendritic input carries
100 % of the teaching signal *only because the majors are absent*.

## 2. `LC`'s real afferent set (Aston-Jones et al. 1986; Van Bockstaele) vs ours
| afferent | literature | in model? | proposed |
|---|---|---|---|
| **`PGi`** (paragigantocellularis) | **major excitatory (glutamatergic); ~73 % of LC neurons driven**; integrates exteroceptive + interoceptive (pain, cardiovascular, respiratory, arousal) | **ABSENT** | **NEW circuit** → `PGi → LC` (AMPA, **strong** — the major drive) |
| **`PrH`** (prepositus hypoglossi) | the other major afferent | **ABSENT** | **NEW circuit** → `PrH → LC` (moderate-strong) |
| PVN dorsal cap | minor | `PVN` exists (interoception_autonomic) | `PVN → LC` (low/low-moderate) |
| spinal lamina X | minor | no spinal circuit | defer (no substrate node) |
| **`CeA`** | **minor, DENDRITIC (shell)** — terminates in peri-LC, reaches LC via extranuclear dendrites (Van Bockstaele CeA-CRF) | present, `moderate`, **as the SOLE afferent** | **untouched** — it becomes minor *by adding the majors*, never by re-banding |

**Adding `PGi`+`PrH` at their grounded bands makes `CeA` the minor input it anatomically is — the entailment
dissolves through anatomy, not through editing a set or a band.**

## 3. Two things the spec did not name

**(a) ★ `PGi` must be afferented, or the fix just moves the incompleteness up one level.** `PGi` is an
*integrator* — if it is added unafferented, LC's drive still comes from one place, and I have rebuilt the exact
defect one synapse rostral. **`PGi`'s own grounded afferents are the nociceptive/interoceptive stream** — and
this is where the registered candidates resolve: **Aston-Jones showed `PBN`/`NTS` do NOT project to LC
directly (they terminate *adjacent*); `PGi` is the integrator that relays them.** So the registered-dormant
`PBN→LC`/`NTS→LC` items are **redirected**: `PBN → PGi`, `NTS → PGi`, `IN-SOMATO:nociception → PGi` → `PGi →
LC`. **`PGi` is what those candidates were waiting for.**

**(b) `preBötC → LC` (Yackle et al. 2017) connects two registers into one circuit.** The novel-environment
arousal signal is driven *exclusively* by Cdh9/Dbx1 pre-Bötzinger neurons. `preBötC` is ABSENT (the registered
respiratory-rhythm item). Building it here would serve **both** the LC-afferent completion **and** the
respiratory register — but it is a larger add (a rhythm generator), so I flag it as a **scope choice**: minimal
LC completion (`PGi`+`PrH`+`PVN`) vs. that plus `preBötC`.

## 4. The domain call — get it right or door 3 gets wider
**`PGi`/`PrH` → `interoception_autonomic`** (the `PBN`/`NTS`/`RVLM` precedent). Verified: `interoception_autonomic`
is **not** in `_TEMPERAMENT_DOMAIN`, so **no temperament dial reaches PGi/PrH** — door 3 is not widened through
the new afferents. If they landed in `defensive_threat` the THREAT dial would reach LC through them and the
artifact would get *worse*. This is load-bearing.

## 5. ⛔ This closes DOOR 1 ONLY — #2 is not resolved by it
- **Door 3** — the THREAT dial scales the `LC` *node* directly; completing the afferents does nothing for it,
  so **a CU agent is still born with a throttled teaching signal**. Needs the per-function temperament model
  (fix #4).
- **Door 2** — the scan's `dissociation_index` still ranges over its own signature. Separate fix.
- **Re-measure after door 1 (Phase 3):** throttle `AFFECTIVE_EMPATHY` → if LC still collapses, the entailment
  survives (a real finding); if the collapse goes marginal, door 1 dissolved through anatomy. Either is honest.

## 6. `PVN-OT` — the partial-completion check (as demanded)
```
IN-SOMATO:affective_touch -> PVN-OT  (moderate-strong)
NTS                       -> PVN-OT  (moderate)
IN-CONSPEC:kin_signature  -> PVN-OT  (moderate-strong)
```
**Less acute than LC: no single afferent carries 100 %** (three inputs share the drive), so there is no
one-afferent entailment of the LC kind. **But the SET-completeness question is the same and is `UNRESOLVED`:**
these are the afferents the *kinship work needed* (touch, visceral, kin cue) — the OT literature adds **`MPOA`,
`SON`, `BNST`, and `MeA`** (the `MeA→PVN-OT` sketch was dropped when it proved GABAergic/backwards). So
`PVN-OT` is **plausibly partial**, on the same failure mode — **"partial completion recorded as completion"** —
but it does not gate a study today. **Its own diagnostic, lower priority than LC's.**

## Proposed build (once ruled) — and the order
`PGi` + `PrH` (+ `PVN → LC` minor); `PGi`'s afferents = `PBN`/`NTS`/nociception (redirecting the registered
candidates through it); `PGi`/`PrH` → `interoception_autonomic`; **`CeA → LC` band untouched**; `preBötC` a
flagged scope choice. Then regrow, full suite, **re-measure the entailment**, and report whether door 1
dissolved it. **Doors 2 and 3 stay open; #2 stays open until all three shut.** Nothing built this pass.

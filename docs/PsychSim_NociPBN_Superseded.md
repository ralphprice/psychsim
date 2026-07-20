# `noci → PBN` — **the edge does not need building. The register item was STALE.**

**I checked the model before fetching, and the check dissolved the task. This is the `HSO`-shape catch: an
item sat on the register as "missing" long enough that the branch's own later work closed it from a different
direction, and the register never got updated. Do not build this. Here is why.**

---

## 1. The premise was "PBN is inert for lack of a nociceptive afferent." **False on two counts.**

**Count 1 — PBN is not afferent-less, and it already carries pain:**
```
PBN function: "Relays NTS + lamina-I spinothalamic (PAIN/thermal/visceral) signals to thalamus, hypothalamus, amygdala"
PBN <- SOM-relay (moderate), NTS (moderate-strong), aIns (low)
PBN -> VMpo-thal (moderate), CeA (moderate), PGi (AMPA, moderate)
```
**PBN already relays lamina-I spinothalamic pain, already has three afferents, and already reaches `CeA`, the
thalamus, and `PGi`. It is not inert and it is not pain-blind.** The `SOM-relay` and `NTS` inputs are its
pain/visceral drive. **The "missing nociceptive afferent" is already there under a different name.**

**Count 2 — a direct nociception channel already exists and already reaches everything the `noci→PBN` edge
was meant to feed:**
```
IN-SOMATO:nociception -> LA, CeA, VPL, PGi
```
**The model has a nociception input channel, and it lands on `LA`, `CeA`, `VPL`, and — critically — `PGi`
DIRECTLY.** **So the nociceptive drive to `PGi` (the thing `noci→PBN→PGi` would have provided) is already
delivered by `IN-SOMATO:nociception → PGi`, built during the PGi arc.**

## 2. What actually happened — the branch closed this from the other side

**When was `IN-SOMATO:nociception → PGi` built? The PGi afferent-completion arc** (the LC-driver descent).
Look at `PGi`'s afferents now:
```
PGi <- PBN (moderate), NTS (moderate), IN-SOMATO:nociception (moderate), dPAG (moderate)
```
**`PGi` receives nociception THREE ways: via `PBN`, via `NTS`, and DIRECTLY via `IN-SOMATO:nociception`.**
**The direct-pain arm the register wanted is built. The `noci→PBN` item was written BEFORE the PGi arc, as
part of diagnosing why direct pain didn't reach arousal — and the PGi arc SOLVED that by building
`IN-SOMATO:nociception → PGi` directly.** **The register item is a fossil of the problem state before its own
fix.**

> **This is exactly the `HSO` lesson: the register's open items freeze at the moment they were written, and
> the branch's own later work can close them without the register knowing. `noci→PBN` was real when it was
> written and has been dead since the PGi arc. I would have fetched the PBN pain literature and built an edge
> whose function is already served — a redundant afferent, which is a drift hazard, not a gap-fill.**

## 3. RULING
1. **Do NOT build `noci → PBN`.** The nociceptive drive it was meant to provide is already delivered:
   PBN carries pain via `SOM-relay`/`NTS`, and `PGi` gets direct nociception via `IN-SOMATO:nociception → PGi`.
2. **Close the register item as SUPERSEDED** — by the PGi afferent-completion arc, not by a new build. Record
   it so it does not resurface a third time. **(S55 → closed-superseded.)**
3. **Note the real open question about PBN, which is DIFFERENT:** PBN is on the **lump census** (parabrachial
   is many subnuclei — the lateral/medial/Kölliker-Fuse divisions carry pain vs cardioresp vs taste to
   different targets). **`noci→PBN` is closed; `PBN`-is-a-lump is open.** These were being conflated. The lump
   question is a split diagnosis, not an afferent add, and it belongs with the lump census whenever that opens.

---

## 4. What this means for the "machine-independent grounding" board

**`noci → PBN` was one of the two machine-independent items. It just evaporated. So the machine-independent
grounding left is ONE thing: the opioid system** — and that one I already flagged as a *system* (multiple
registers, one circuit, the `preBötC`/`PAG-PANIC`-soothing shape), which deserves a scoped diagnosis, not a
quick pass.

> **So here is the honest state: there is no longer a clean, small, machine-independent grounding pass left to
> open.** The census is discharged, `noci→PBN` is a fossil, the opioid system is a system-scale diagnosis, the
> dl/l split is a substrate-shape diagnosis, and `S56` is a mechanism-design question. **Everything remaining
> is either machine-gated or a real diagnosis that shouldn't be rushed as filler while WSL is down.**

**That is not a stall — it is the branch telling us it has run out of cheap work, which is itself a signal.**
**The two things that actually move the freezing floor (`VMH→vlPAG` strong, `DRN` on its curve) are both
machine-gated, and they are the point. The most valuable next action is the machine fix, because it unblocks
the two builds that decide whether the freezing column works — and that is the question the whole branch has
been converging on.**

**Recommendation: fix the machine next, not open another pass.** If you want a diagnosis opened in parallel
that is genuinely worth the depth (not filler), the **opioid system** is the one — because `PAG-PANIC`'s
soothing arm and `vlPAG-GABA`'s μ-opioid release both need it, and it is on the critical path to the
separation-distress and freezing-selection stories. But it is a diagnosis, and I would open it as one, not as
a grounding pin.

**Nothing built. `noci→PBN` closed-superseded. The board is honest now: the machine is the bottleneck, and
that is correct.**

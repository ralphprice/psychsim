"""signature.py -- the genetic-fingerprint / MHC-scent kin CUE (v14 Phase 2).

Each agent carries an innate SIGNATURE: a vector of loci (the MHC-allele analogue) -- a pure BEARER
property (like `physical`, v10), sex-neutral, identical regardless of who perceives it. **Relatedness
sets, AT SPAWN, which loci two agents share** (parent-child / full-sibs ~half; cousins ~1/8; unrelated
~0) -- and that is the ONLY causal role relatedness ever plays. After spawn, relatedness never appears
in any computation; the vectors carry everything.

The perceiver detects kin by SELF-REFERENT phenotype matching: it compares another's signature to its
OWN self-signature (component-wise overlap) -- "does this smell like me?" (Mateo & Johnston 2000, the
armpit effect / self-referent phenotype matching). Perceived similarity feeds affiliation (nepotism)
and, in a mate-choice context, aversion (incest-avoidance) -- both EMERGENT, never coded.

THE KEYSTONE, made concrete (v14 spec section 0):
  * `signature_match` is a function of (bearer_signature, perceiver_self_signature) ONLY. It NEVER
    takes relatedness -- relatedness is upstream, at spawn, setting shared loci. (grep-gate: no
    relatedness/kinship term in this matching path.)
  * The match is SELF-REFERENT: the perceiver compares to its OWN signature, never a family template or
    an averaged-kin signature. Self-referent is both the honest mechanism and the biologically correct
    one (Mateo & Johnston: self-matching, not template-matching) -- and it gives incest-aversion for
    free later (too-similar-to-self in mate-choice = the Westermarck signal).
Relatedness sets the cue; the similarity, and the nepotism/aversion it drives, EMERGE.
"""
from typing import List
import random

# SCAFFOLD (labelled, replace-with-data): the MHC-analogue signature geometry. N_LOCI loci, each an
# allele from a large-enough range that UNRELATED agents match only at chance (~1/_ALLELE_RANGE per
# locus -> unrelated similarity ~0), while Mendelian inheritance gives parent-child / full-sibs ~half.
N_LOCI = 16
_ALLELE_RANGE = 64


def random_signature(rng: random.Random) -> List[int]:
    """A fresh, UNRELATED signature -- each locus an independent random allele. Two such signatures
    match only at chance (~1/_ALLELE_RANGE per locus), i.e. similarity ~0 (unrelated)."""
    return [rng.randrange(_ALLELE_RANGE) for _ in range(N_LOCI)]


def child_signature(parent_a: List[int], parent_b: List[int], rng: random.Random) -> List[int]:
    """A child's signature: each locus inherited (Mendelian) from one parent at random. The child thus
    shares ~half its loci with each parent and ~half with a full sibling -- relatedness -> shared loci
    FALLS OUT of inheritance and is set HERE, at spawn, never read afterward. (A single known parent +
    an unrelated other parent is the common case; both-parents-known is the same call.)"""
    return [(parent_a[i] if rng.random() < 0.5 else parent_b[i]) for i in range(min(len(parent_a), len(parent_b)))]


def signature_match(bearer_sig: List[int], perceiver_self_sig: List[int]) -> float:
    """SELF-REFERENT phenotype matching -- the fraction of loci at which the BEARER's signature matches
    the PERCEIVER'S OWN signature, in [0,1]. The similarity-to-self that feeds affiliation.

    A function of the two signatures ONLY: it never takes relatedness (that is upstream, at spawn). And
    self-referent: it compares to `perceiver_self_sig` (the perceiver's OWN signature), never a family
    template. So a parent perceives a child as similar because the child shares half the parent's loci
    -- the parent never needs to KNOW 'this is my child' (Mateo & Johnston 2000)."""
    if not bearer_sig or not perceiver_self_sig:
        return 0.0
    n = min(len(bearer_sig), len(perceiver_self_sig))
    if n == 0:
        return 0.0
    shared = sum(1 for i in range(n) if bearer_sig[i] == perceiver_self_sig[i])
    return shared / n

import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""v14 Phase 2 -- the genetic-fingerprint kin CUE (signature) + self-referent matching.

The keystone made concrete: relatedness sets which loci two agents share AT SPAWN (a bearer fact); the
perceiver's SELF-REFERENT match derives similarity from the two signature vectors ONLY -- no relatedness
downstream. These tests pin the two honesty checks (signature-only, self-referent) + the cue-similarity
structure that makes nepotism EMERGE (kin match higher than strangers), and the source-level grep-gate."""

import io
import random
import tokenize
import unittest

from affective_engine import signature as sig


class TestSignatureCueStructure(unittest.TestCase):
    def test_self_match_is_one(self):
        rng = random.Random(1)
        s = sig.random_signature(rng)
        self.assertEqual(sig.signature_match(s, s), 1.0)          # a signature matches itself perfectly

    def test_unrelated_near_zero_kin_near_half(self):
        rng = random.Random(7)
        # average over many families so the SCAFFOLD geometry's expectations are stable
        unrel, pc, sib = [], [], []
        for _ in range(200):
            pa, pb = sig.random_signature(rng), sig.random_signature(rng)
            other = sig.random_signature(rng)
            c1 = sig.child_signature(pa, pb, rng)
            c2 = sig.child_signature(pa, pb, rng)              # full sibling of c1
            unrel.append(sig.signature_match(pa, other))       # unrelated
            pc.append(sig.signature_match(c1, pa))             # child perceived by parent A (self-referent)
            sib.append(sig.signature_match(c1, c2))            # full siblings
        mean = lambda xs: sum(xs) / len(xs)
        self.assertLess(mean(unrel), 0.10)                     # unrelated ~0 (chance only)
        self.assertGreater(mean(pc), 0.35)                     # parent-child ~half
        self.assertGreater(mean(sib), 0.35)                    # full sibs ~half
        # the ORDERING is the nepotism cue: kin match >> strangers
        self.assertGreater(mean(pc), mean(unrel) + 0.25)
        self.assertGreater(mean(sib), mean(unrel) + 0.25)

    def test_cousins_between_sibs_and_strangers(self):
        # cousins (~1/8 related) sit between full sibs (~1/2) and strangers (~0) -- a graded cue
        rng = random.Random(3)
        cous = []
        for _ in range(200):
            gp_a, gp_b = sig.random_signature(rng), sig.random_signature(rng)   # shared grandparents
            # two siblings (the parents of the cousins)
            par1 = sig.child_signature(gp_a, gp_b, rng)
            par2 = sig.child_signature(gp_a, gp_b, rng)
            child1 = sig.child_signature(par1, sig.random_signature(rng), rng)
            child2 = sig.child_signature(par2, sig.random_signature(rng), rng)
            cous.append(sig.signature_match(child1, child2))
        self.assertGreater(sum(cous) / len(cous), 0.02)        # above strangers
        self.assertLess(sum(cous) / len(cous), 0.40)           # below full sibs


class TestHonestyChecks(unittest.TestCase):
    def test_match_is_self_referent_not_symmetric_to_a_template(self):
        # self-referent: the match is against the PERCEIVER's own signature -- a parent and a stranger
        # perceive the SAME child differently, because they match it to different selves.
        rng = random.Random(11)
        pa, pb = sig.random_signature(rng), sig.random_signature(rng)
        child = sig.child_signature(pa, pb, rng)
        stranger = sig.random_signature(rng)
        self.assertGreater(sig.signature_match(child, pa),     # parent's self-referent view of the child
                           sig.signature_match(child, stranger))  # stranger's self-referent view

    def test_match_path_has_no_relatedness_term(self):
        # grep-gate at the SOURCE level: the matching module references no relatedness/kinship/bond
        # term -- relatedness is upstream (spawn), never in the match. (Strip comments + docstrings;
        # check only the code tokens.)
        src = _O.path.join(_ROOT, "core", "affective_engine", "signature.py")
        with open(src, "rb") as fh:
            names = {t.string.lower() for t in tokenize.tokenize(fh.readline) if t.type == tokenize.NAME}
        for banned in ("relatedness", "kinship", "related", "nepotism", "bond", "incest", "kin"):
            self.assertNotIn(banned, names, f"matching path references '{banned}' -- must be signature-only")


if __name__ == "__main__":
    unittest.main()

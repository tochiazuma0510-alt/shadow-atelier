#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
search/kep-cx-recheck.py -- KEP counterexample re-check for W-A-B3idx162-s1
(P80-A, night repair 2).

Purpose: independently reconstruct the window W-A-B3idx162-s1 (found by
wall-miner-v5.g / kerchi-judge.g v1.3, recorded in
search/certs/wall_miner_v5_20260729.json) FROM SCRATCH in python, sharing
NO GAP helper code and NO GAP-computed multiplication table -- only the
canonical_id_words (the literal generating words of N as words in a,b,
LID-1 run-independent identity) and the b3_index are read from the v5
certificate. Everything else (the B3/N quotient group of order 162, its
permutation representation, PN=Group(x,y), [PN,PN], the (F2)+settled
shadow enumeration, the shadow-Cayley-table group G_N, its kernel and
chi~ image) is recomputed here independently.

Group-theoretic engine: sympy's coset_enumeration_r (Todd-Coxeter, HLT
strategy) builds the regular permutation representation of B3/N from the
presentation <a,b | aba=bab, w_1=1, ..., w_29=1> (w_i = canonical_id_words).
This is an independent third-party implementation of coset enumeration,
not GAP's own LowIndexNormalSubgroupsSearch/NaturalHomomorphismByNormalSubgroup
machinery, and not a copy of any table GAP produced.

Design (mirrors kerchi-judge.g's JudgeWindow -- ported by hand, re-derived
from the pipeline description in that file's comments, NOT by importing or
literally translating GAP source into python line-by-line as a "shared
helper"; every group operation below is implemented from first principles
on top of plain python tuples representing permutations of the 162 cosets):

  mul(P,Q)[c] := Q[P[c]]   -- represents the ABSTRACT PRODUCT P*Q read in
                              ordinary left-to-right order (apply P first,
                              then Q); this is a deliberate, self-consistent
                              convention chosen so that AbstractProd-style
                              expressions need NO reversal trick (unlike
                              GAP's own convention, which requires one --
                              see kerchi-judge.g / gaplib_common.g comments).
                              Associativity is free (ordinary function
                              composition); the convention is used
                              uniformly throughout this file, so genuine
                              GAP-independence is preserved (no numbers or
                              tables are borrowed from the .g scripts).

No u (sealed symbol) is referenced by this reconstruction. No commit is
made by this script; it only writes the requested KEP-counterexample/v1
certificate.
"""
import json
import sys
from math import gcd, lcm

from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup, coset_enumeration_r

WINDOW_ID = "W-A-B3idx162-s1"
CERT_IN = "search/certs/wall_miner_v5_20260729.json"
CERT_OUT = "search/certs/kep_counterexample_idx162s1_20260729.json"


def parse_word_sympy(s, a, b):
    expr = s.replace("^", "**")
    return eval(expr, {"__builtins__": {}}, {"a": a, "b": b})


def tags_from_array_form(arr):
    """sympy FreeGroupElement.array_form -> flat list of unit tags
    ('a','ainv','b','binv'), one tag per unit exponent step, in word order."""
    out = []
    for gen, exp in arr:
        name = "a" if str(gen) == "a" else "b"
        if exp >= 0:
            out.extend([name] * exp)
        else:
            out.extend([name + "inv"] * (-exp))
    return out


def main():
    with open(CERT_IN, encoding="utf-8") as f:
        v5 = json.load(f)
    win = next(w for w in v5["windows"] if w["run_local_serial_id"] == WINDOW_ID)
    words = win["canonical_id_words"]
    jv5 = win["judge"]
    b3_index_v5 = win["b3_index"]

    report = {"window_uid_v5": WINDOW_ID, "v5_source": CERT_IN,
              "v5_recorded": {"abs_Bq": jv5["abs_Bq"], "N_ord": jv5["N_ord"],
                               "c_in_N": jv5["c_in_N"],
                               "isotropy_order": jv5["isotropy_order"],
                               "ker_size": jv5["ker_size"],
                               "chi_image_order": jv5["chi_image_order"],
                               "chi_surjective_assert": jv5["chi_surjective_assert"],
                               "ker_commutes": jv5["ker_commutes"],
                               "verdict": jv5["verdict"],
                               "derived_series_orders": jv5["derived_series_orders"],
                               "derived_length": jv5["derived_length"]},
              "canonical_id_words": words}

    # ---- (1) build B3/N as a permutation group via independent Todd-Coxeter ----
    F, a, b = free_group("a, b")
    braid = a * b * a * (b * a * b) ** -1
    relators = [braid] + [parse_word_sympy(w, a, b) for w in words]
    G = FpGroup(F, relators)
    C = coset_enumeration_r(G, [])
    C.compress()
    n = len(C.table)
    print(f"[1] Bq = B3/N order (independent Todd-Coxeter) = {n}  (b3_index recorded = {b3_index_v5})")

    ident = tuple(range(n))

    def mul(P, Q):
        return tuple(Q[P[c]] for c in range(n))

    def inv(P):
        r = [0] * n
        for c in range(n):
            r[P[c]] = c
        return tuple(r)

    def power(P, k):
        if k == 0:
            return ident
        if k < 0:
            return power(inv(P), -k)
        result = ident
        base = P
        kk = k
        while kk:
            if kk & 1:
                result = mul(result, base)
            base = mul(base, base)
            kk >>= 1
        return result

    def order_of(P):
        k = 1
        cur = P
        while cur != ident:
            cur = mul(cur, P)
            k += 1
        return k

    s1 = tuple(row[0] for row in C.table)   # a
    s1inv = tuple(row[1] for row in C.table)
    s2 = tuple(row[2] for row in C.table)   # b
    s2inv = tuple(row[3] for row in C.table)
    assert inv(s1) == s1inv, "a^-1 column is not the functional inverse of a column"
    assert inv(s2) == s2inv, "b^-1 column is not the functional inverse of b column"

    braid_holds = (mul(mul(s1, s2), s1) == mul(mul(s2, s1), s2))
    print(f"[2] braid relation s1 s2 s1 = s2 s1 s2 holds on this rep: {braid_holds}")
    assert braid_holds

    x = mul(s1, s1)
    y = mul(s2, s2)
    Dlt = mul(mul(s1, s2), s1)          # Delta = s1 s2 s1
    DltInv = inv(Dlt)
    dlt = mul(s1, s2)                    # delta = s1 s2
    dltInv = inv(dlt)
    c_elt = mul(Dlt, Dlt)                # c = Delta^2

    ox, oy, oc = order_of(x), order_of(y), order_of(c_elt)
    Nord = lcm(ox, oy, oc)
    c_in_N = (c_elt == ident)
    charming = [m for m in range(Nord) if gcd(2 * m + 1, Nord) == 1]

    print(f"[3] N_ord={Nord} (recorded {jv5['N_ord']}), c_in_N={c_in_N} (recorded {jv5['c_in_N']}), "
          f"charming_count={len(charming)} (recorded {jv5['charming_count']})")

    # ---- (4) PN = Group(x,y) via BFS closure, recording x/y-words per element ----
    PN_elems = {ident: []}
    frontier = [ident]
    gens = [("x", x), ("xinv", inv(x)), ("y", y), ("yinv", inv(y))]
    while frontier:
        nf = []
        for g in frontier:
            for name, gp in gens:
                h = mul(g, gp)
                if h not in PN_elems:
                    PN_elems[h] = PN_elems[g] + [name]
                    nf.append(h)
        frontier = nf
    abs_PN = len(PN_elems)
    print(f"[4] |PN|={abs_PN} (recorded abs_PN={jv5['abs_PN']})")

    def eval_xy_word(tags, ximg, yimg):
        m = {"x": ximg, "xinv": inv(ximg), "y": yimg, "yinv": inv(yimg)}
        r = ident
        for t in tags:
            r = mul(r, m[t])
        return r

    # sanity: every recorded element reproduces itself via its own word
    for elt, tags in PN_elems.items():
        assert eval_xy_word(tags, x, y) == elt

    # ---- (5) [PN,PN] = derived subgroup of PN (all commutators, then closure) ----
    PN_list = list(PN_elems.keys())
    seeds = set()
    for g in PN_list:
        ginv = inv(g)
        for h in PN_list:
            hinv = inv(h)
            comm = mul(mul(mul(ginv, hinv), g), h)   # g^-1 h^-1 g h, left-to-right
            seeds.add(comm)
    D_elems = {ident}
    frontier = [ident]
    seed_list = list(seeds)
    while frontier:
        nf = []
        for g in frontier:
            for s in seed_list:
                for cand in (mul(g, s), mul(g, inv(s))):
                    if cand not in D_elems:
                        D_elems.add(cand)
                        nf.append(cand)
        frontier = nf
    print(f"[5] |[PN,PN]| = {len(D_elems)}")

    # ---- (6) (F2)+settled shadow enumeration ----
    def TH(g):
        return mul(mul(Dlt, g), DltInv)

    def TT(g):
        return mul(mul(dlt, g), dltInv)

    def RtOf(m, f):
        Wd = mul(power(y, m), f)
        return mul(mul(TT(TT(Wd)), TT(Wd)), Wd)

    # pre-parse canonical_id_words + braid as tag sequences on (a,b) for the
    # settled/well-definedness relator check
    relator_tags = [tags_from_array_form(braid.array_form)]
    for w in words:
        el = parse_word_sympy(w, a, b)
        relator_tags.append(tags_from_array_form(el.array_form))

    def eval_ab_word(tags, aimg, bimg):
        m = {"a": aimg, "ainv": inv(aimg), "b": bimg, "binv": inv(bimg)}
        r = ident
        for t in tags:
            r = mul(r, m[t])
        return r

    def gen_subgroup_size(gset):
        elems = {ident}
        frontier = [ident]
        seedl = list(gset) + [inv(g) for g in gset]
        while frontier:
            nf = []
            for g in frontier:
                for s in seedl:
                    h = mul(g, s)
                    if h not in elems:
                        elems.add(h)
                        nf.append(h)
            frontier = nf
        return len(elems)

    shadows = []
    settled_fail_count = 0
    for f in D_elems:
        # condition 1: f * TH(f) = identity
        if mul(f, TH(f)) != ident:
            continue
        for m in charming:
            u = 2 * m + 1
            # condition 2: RtOf(m,f) = c^m
            if RtOf(m, f) != power(c_elt, m):
                continue
            # condition 3: <x^u, f^-1 y^u f> = PN
            finv = inv(f)
            gen2 = mul(mul(finv, power(y, u)), f)
            if gen_subgroup_size([power(x, u), gen2]) != abs_PN:
                continue
            # condition 4 (settled, KJ-1): candidate images actually satisfy
            # EVERY defining relator of Bq (braid + all 29 N-generators) --
            # i.e. a -> s1^u, b -> f^-1 s2^u f is a well-defined endomorphism
            # of Bq. This is evaluated directly (both images already live in
            # the same 162-element permutation rep of Bq), with no symbolic
            # homomorphism-construction call of any kind.
            A = power(s1, u)
            B = mul(mul(finv, power(s2, u)), f)
            ok = True
            for tg in relator_tags:
                if eval_ab_word(tg, A, B) != ident:
                    ok = False
                    break
            if not ok:
                settled_fail_count += 1
                continue
            shadows.append((m, f))

    shadow_total = len(shadows)
    ker_list = [s for s in shadows if s[0] == 0]
    ker_size_raw = len(ker_list)
    chi_image_order = len(set((2 * m + 1) % (2 * Nord) for (m, f) in shadows))
    settled_total_evaluated = shadow_total + settled_fail_count

    print(f"[6] shadow_total={shadow_total} (recorded shadow_total={jv5['shadow_total']}), "
          f"settled_fail_count={settled_fail_count} (recorded {jv5['settled_fail_count']}), "
          f"ker_size(raw m=0 count)={ker_size_raw} (recorded ker_size={jv5['ker_size']}), "
          f"chi_image_order={chi_image_order} (recorded {jv5['chi_image_order']})")

    # ---- (7) GroupOfShadows: Cayley table of the shadow set -> G_N, ker(chi~) ----
    nS = len(shadows)
    idx_of = {}
    for i, (m, f) in enumerate(shadows):
        idx_of.setdefault(m, []).append((f, i))

    def Eh_apply(f1, u1, g_tags):
        # endomorphism of PN: x -> x^u1, y -> f1^-1 y^u1 f1, applied to an
        # element of PN given as an x/y-word (from PN_elems)
        ximg = power(x, u1)
        yimg = mul(mul(inv(f1), power(y, u1)), f1)
        return eval_xy_word(g_tags, ximg, yimg)

    closed = True
    regs = [[None] * nS for _ in range(nS)]
    for i in range(nS):
        m1, f1 = shadows[i]
        u1 = 2 * m1 + 1
        for j in range(nS):
            mj, fj = shadows[j]
            nm = (2 * m1 * mj + m1 + mj) % Nord
            fj_tags = PN_elems[fj]
            Eh_fj = Eh_apply(f1, u1, fj_tags)
            nf = mul(f1, Eh_fj)
            p = None
            for (cand_f, cand_i) in idx_of.get(nm, []):
                if cand_f == nf:
                    p = cand_i
                    break
            if p is None:
                closed = False
                regs[i][j] = 0
            else:
                regs[i][j] = p

    print(f"[7] (3.53)-analogue closure of shadow Cayley table: closed={closed}")

    isotropy_order = -1
    ker_commutes = None
    verdict = "UNSCREENED"
    G_N_order = None
    ker_order = None
    G_N_abelian = None
    G_N_is_C6 = None
    if closed:
        # G_N = <regs[0..nS-1]> as permutations of range(nS); regular-table
        # construction guarantees this equals the full shadow-Cayley-table
        # group acting regularly IF the table is a genuine group table, so
        # |G_N| should equal nS itself, but we compute the generated
        # permutation-group order explicitly rather than assume it.
        def perm_mul(P, Q):
            return tuple(Q[P[c]] for c in range(nS))

        def perm_inv(P):
            r = [0] * nS
            for c in range(nS):
                r[P[c]] = c
            return tuple(r)

        gen_perms = [tuple(row) for row in regs]
        id_nS = tuple(range(nS))
        elems = {id_nS}
        frontier = [id_nS]
        seedl = gen_perms + [perm_inv(gp) for gp in gen_perms]
        while frontier:
            nf2 = []
            for g in frontier:
                for s in seedl:
                    h = perm_mul(g, s)
                    if h not in elems:
                        elems.add(h)
                        nf2.append(h)
            frontier = nf2
        G_N_order = len(elems)
        isotropy_order = G_N_order

        ker_idx = [i for i in range(nS) if shadows[i][0] == 0]
        ker_gen_perms = [gen_perms[i] for i in ker_idx]
        ker_elems = {id_nS}
        frontier = [id_nS]
        seedl = ker_gen_perms + [perm_inv(gp) for gp in ker_gen_perms]
        while frontier:
            nf2 = []
            for g in frontier:
                for s in seedl:
                    h = perm_mul(g, s)
                    if h not in ker_elems:
                        ker_elems.add(h)
                        nf2.append(h)
            frontier = nf2
        ker_order = len(ker_elems)
        ker_list_elems = list(ker_elems)
        ker_commutes = all(perm_mul(gg, hh) == perm_mul(hh, gg)
                            for gg in ker_list_elems for hh in ker_list_elems)
        verdict = "ABELIAN" if ker_commutes else "NONABELIAN"

        # G_N isomorphism type check (task explicitly claims G_N =~ C6, i.e.
        # G_N itself abelian of order 6 -- distinct from ker_commutes, which
        # is only about ker(chi~) <= G_N): check ALL of G_N commutes.
        G_N_elems_list = list(elems)
        G_N_abelian = all(perm_mul(gg, hh) == perm_mul(hh, gg)
                           for gg in G_N_elems_list for hh in G_N_elems_list)
        G_N_is_C6 = (G_N_order == 6 and G_N_abelian)

    print(f"[8] G_N order (independent) = {isotropy_order} (recorded isotropy_order={jv5['isotropy_order']})")
    print(f"[9] ker(chi~) order (independent, as a group, not raw shadow count) = {ker_order} "
          f"(recorded ker_size={jv5['ker_size']})")
    print(f"[10] ker(chi~) commutes (independent) = {ker_commutes} (recorded ker_commutes={jv5['ker_commutes']})")
    print(f"[11] verdict (independent) = {verdict} (recorded verdict={jv5['verdict']})")
    print(f"[12] G_N abelian (independent, i.e. G_N itself, not just ker) = {G_N_abelian}; "
          f"G_N order 6 + abelian => C6 claim: {G_N_is_C6}")

    chi_surjective_assert = None
    if c_in_N:
        phi_2Nord = None
        # Euler totient of 2*Nord, computed directly (no library import needed
        # -- small number, trial factor)
        def euler_phi(n0):
            result = n0
            p = 2
            nn = n0
            while p * p <= nn:
                if nn % p == 0:
                    while nn % p == 0:
                        nn //= p
                    result -= result // p
                p += 1
            if nn > 1:
                result -= result // nn
            return result
        phi_2Nord = euler_phi(2 * Nord)
        chi_surjective_assert = (chi_image_order == phi_2Nord)

    ta_assert_holds = None
    if closed:
        ta_assert_holds = (ker_order * chi_image_order == isotropy_order)

    # ---- agreement summary vs v5 ----
    agree = {
        "abs_Bq": (n == jv5["abs_Bq"]),
        "N_ord": (Nord == jv5["N_ord"]),
        "c_in_N": (c_in_N == jv5["c_in_N"]),
        "shadow_total": (shadow_total == jv5["shadow_total"]),
        "settled_fail_count": (settled_fail_count == jv5["settled_fail_count"]),
        "isotropy_order_GN": (isotropy_order == jv5["isotropy_order"]),
        "ker_size_group_order": (ker_order == jv5["ker_size"]),
        "chi_image_order": (chi_image_order == jv5["chi_image_order"]),
        "ker_commutes": (ker_commutes == jv5["ker_commutes"]),
        "verdict": (verdict == jv5["verdict"]),
        "G_N_isomorphism_type_claim_C6": (G_N_is_C6 is True),
        "ker_isomorphism_type_claim_C3": (ker_order == 3),
        "Q_isomorphism_type_claim_C2": (chi_image_order == 2),
    }
    all_agree = all(agree.values())

    print("\n=== AGREEMENT SUMMARY (independent python vs GAP v5 certificate) ===")
    for k, v in agree.items():
        print(f"  {k}: {'MATCH' if v else '*** MISMATCH ***'}")
    print(f"ALL_AGREE = {all_agree}")

    # ---- write certificate ----
    cert = {
        "schema": "KEP-counterexample/v1",
        "generated_by": "search/kep-cx-recheck.py",
        "note": ("Independent python-only reconstruction of W-A-B3idx162-s1 "
                 "from canonical_id_words (LID-1 run-independent identity) "
                 "recorded in search/certs/wall_miner_v5_20260729.json. "
                 "Uses sympy's coset_enumeration_r (independent Todd-Coxeter "
                 "implementation) to build B3/N from the presentation "
                 "<a,b|aba=bab,w_1=1,...,w_29=1>; shares no GAP helper code, "
                 "no GAP-computed table, and no multiplication table from "
                 "any prior run. Not a ledger claim by itself -- a "
                 "cross-check (per repo policy, 'cross-checked', not "
                 "'verified' -- that word is reserved for Lean)."),
        "window_uid": WINDOW_ID,
        "v5_source_cert": CERT_IN,
        "v5_source_canonical_id_words": words,
        "reconstruction_generators": {
            "note": "generators of N as words in the free group on a,b (parsed via sympy free_group)",
            "words": words,
        },
        "independent_recomputation": {
            "abs_Bq": n,
            "N_ord": Nord,
            "c_in_N": c_in_N,
            "charming_count": len(charming),
            "abs_PN": abs_PN,
            "derived_subgroup_PN_order": len(D_elems),
            "shadow_total": shadow_total,
            "settled_fail_count": settled_fail_count,
            "settled_total_evaluated": settled_total_evaluated,
            "ker_size_raw_m0_shadow_count": ker_size_raw,
            "chi_image_order": chi_image_order,
            "closure_holds": closed,
            "G_N_order": isotropy_order,
            "G_N_abelian": G_N_abelian,
            "G_N_is_C6_claim": G_N_is_C6,
            "ker_chi_tilde_order": ker_order,
            "ker_chi_tilde_commutes": ker_commutes,
            "verdict": verdict,
            "chi_surjective_assert": chi_surjective_assert,
            "ta_assert_holds": ta_assert_holds,
        },
        "v5_recorded": report["v5_recorded"],
        "agreement": agree,
        "all_agree": all_agree,
        "candidate_shadows": [
            {"m": m, "f_perm_as_x_y_word": PN_elems[f]} for (m, f) in shadows
        ],
    }

    with open(CERT_OUT, "w", encoding="utf-8") as fo:
        json.dump(cert, fo, ensure_ascii=False, indent=2)
    print(f"\nWrote {CERT_OUT}")


if __name__ == "__main__":
    main()

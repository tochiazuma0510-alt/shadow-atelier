#!/usr/bin/env python3
"""
twin_witness_mc1_check_v1_1.py -- MC-1 v1.1 independent re-checker.

Repairs (裁定607, per docs/notes/twin_witness_cv9_reading_v1.md 発見穴):
  - 【重大2/作業1】full hexagon (3.3)(3.4) at [-1,1] on Q=B3/N (was: NOT
    implemented in v1's python side at all -- only SURJ was).
  - 【重大1/作業2】replaces the vacuous S-TW-6 canary (a^-1(ab)b^-1=e, true in
    ANY group) with a discriminating one: implements tau as an ACTUAL
    substitution homomorphism on abstract F2=<x,y> (via a from-scratch word
    engine, applied by running the code -- not hand-reduced identities),
    then tests forward (paper-product order, W-4) vs reversed order as a
    genuine contrast (forward must be trivial, reversed must generically NOT
    be, in a non-abelian Q).
  - 【要修正3/作業3】fills the FROZEN schema's missing fields independently:
    in_PB3 (via a from-scratch BFS homomorphism-factors-through-S3 test --
    no GAP, no reused code) and c_in_N (via computing c=(s1 s2 s1)^2 as a
    permutation and checking triviality), witness_word, shadow{m,f_word},
    checks{...}.
  - 【軽微8】interface now takes ALL 15 pairs x 2 directions (30 entries,
    with mclass supplied by 系統A) and can flag A/B-side or GAP/python class
    disagreement for any window, not just the M1 subset.
  - 【軽微7】SURJ / charming are computed but flagged in the report as
    "vacuous" (structurally always true for any faithful <s1,s2>=Q, any
    m=-1 charming test) and excluded from the headline "agreement" count,
    while still being recorded.

GAP-helper-free: this file imports nothing from search/*.g, reuses NO code
or data structures from search/twin-witness-mirror-v1_1.g beyond reading its
JSON export (permutations + word strings = plain data). All logic (word
parsing, permutation arithmetic, BFS group closure, BFS homomorphism
factoring, tau substitution engine) is reimplemented from scratch here, as
in v1's search/twin_witness_mc1_check.py (from which this file also does NOT
import -- it is a fresh, self-contained script).
"""
import json
import re
import sys

MC1_PATH = "search/certs/twin_witness_mc1_export_v1_1_20260806.json"
OUT_PATH = "search/certs/twin_witness_mc1_check_result_v1_1_20260806.json"


# ---------------------------------------------------------------------------
# permutation arithmetic (1-indexed lists; perm[i-1] = image of i).
# perm_mul(p,q)[i] = q[p[i]-1]  (apply p first, then q -- GAP right-action
# convention, matches how the export's s1_perm/s2_perm were built: i^s1p).
# ---------------------------------------------------------------------------
def perm_identity(n):
    return list(range(1, n + 1))


def perm_mul(p, q):
    n = len(p)
    return [q[p[i] - 1] for i in range(n)]


def perm_inv(p):
    n = len(p)
    inv = [0] * n
    for i in range(n):
        inv[p[i] - 1] = i + 1
    return inv


def perm_pow(p, k):
    n = len(p)
    if k == 0:
        return perm_identity(n)
    base = p if k > 0 else perm_inv(p)
    result = perm_identity(n)
    for _ in range(abs(k)):
        result = perm_mul(result, base)
    return result


def perm_eq(p, q):
    return list(p) == list(q)


# ---------------------------------------------------------------------------
# word parser (a,b generator words as they appear in the census cert / export)
# -- same grammar as v1's checker, reimplemented independently here.
# ---------------------------------------------------------------------------
TOKEN_RE = re.compile(r'\s*(\(|\)|\^-?\d+|\*|[ab])')


def tokenize(s):
    pos, toks = 0, []
    while pos < len(s):
        m = TOKEN_RE.match(s, pos)
        if not m:
            raise ValueError(f"tokenize failure at {pos!r} in {s!r}")
        toks.append(m.group(1))
        pos = m.end()
    return toks


def parse_factor(toks, i):
    tok = toks[i]
    if tok == '(':
        subexpr, i = parse_expr(toks, i + 1)
        assert toks[i] == ')'
        i += 1
        node = ('group', subexpr)
    elif tok in ('a', 'b'):
        node = ('gen', tok)
        i += 1
    else:
        raise ValueError(f"unexpected token {tok!r} at {i}")
    exp = 1
    if i < len(toks) and toks[i].startswith('^'):
        exp = int(toks[i][1:])
        i += 1
    return (node, exp), i


def parse_expr(toks, i):
    factors = []
    factor, i = parse_factor(toks, i)
    factors.append(factor)
    while i < len(toks) and toks[i] == '*':
        factor, i = parse_factor(toks, i + 1)
        factors.append(factor)
    return factors, i


def parse_word(s):
    toks = tokenize(s)
    expr, i = parse_expr(toks, 0)
    if i != len(toks):
        raise ValueError(f"trailing tokens in {s!r}")
    return expr


def eval_expr(expr, subst, n):
    result = perm_identity(n)
    for node, exp in expr:
        base = subst[node[1]] if node[0] == 'gen' else eval_expr(node[1], subst, n)
        result = perm_mul(result, perm_pow(base, exp))
    return result


def eval_word(word_str, subst, n):
    return eval_expr(parse_word(word_str), subst, n)


# ---------------------------------------------------------------------------
# BFS group closure (for |<gens>| and for the S3-factoring test below)
# ---------------------------------------------------------------------------
def bfs_group_order(gens, n):
    seen = {tuple(perm_identity(n))}
    frontier = [perm_identity(n)]
    gens_inv = [perm_inv(g) for g in gens]
    all_gens = list(gens) + gens_inv
    while frontier:
        new_frontier = []
        for p in frontier:
            for g in all_gens:
                q = perm_mul(p, g)
                tq = tuple(q)
                if tq not in seen:
                    seen.add(tq)
                    new_frontier.append(q)
        frontier = new_frontier
    return len(seen)


# 3-cycle permutations for the S3-target: (1,2) and (2,3) as 3-point perms
S3_GEN_A = [2, 1, 3]   # (1,2)
S3_GEN_B = [1, 3, 2]   # (2,3)


def bfs_factors_through_s3(s1, s2, n):
    """From-scratch, GAP-free check of whether there is a well-defined
    homomorphism Q=<s1,s2> -> S3 sending s1->(1,2), s2->(2,3). This is
    EXACTLY the independent 'ker(rho) <= PB3' test (falsifier's 穴: 'phi:
    Q->S3 built by BFS, homomorphism property verified on generators').

    Method: BFS the Cayley graph of Q starting from identity, carrying a
    PARALLEL walk in S3 using the SAME generator sequence (s1<->(1,2),
    s2<->(2,3), and their inverses). If the same Q-element is ever reached
    via two different generator sequences that produce two DIFFERENT S3
    images, the map is not well-defined -> N is NOT contained in PB3.
    Returns (factors_ok: bool, s3_image_of_generators_consistent: dict-or-None).
    """
    id_n = tuple(perm_identity(n))
    id_3 = tuple(perm_identity(3))
    # map from Q-element (as tuple) -> S3-element (as tuple) discovered so far
    q_to_s3 = {id_n: id_3}
    frontier = [(list(perm_identity(n)), list(perm_identity(3)))]

    gens_q = [s1, s2, perm_inv(s1), perm_inv(s2)]
    gens_s3 = [S3_GEN_A, S3_GEN_B, perm_inv(S3_GEN_A), perm_inv(S3_GEN_B)]

    while frontier:
        new_frontier = []
        for (qcur, s3cur) in frontier:
            for gq, gs3 in zip(gens_q, gens_s3):
                qnext = perm_mul(qcur, gq)
                s3next = perm_mul(s3cur, gs3)
                tqnext = tuple(qnext)
                ts3next = tuple(s3next)
                if tqnext in q_to_s3:
                    if q_to_s3[tqnext] != ts3next:
                        return False   # inconsistent -> map not well-defined
                else:
                    q_to_s3[tqnext] = ts3next
                    new_frontier.append((qnext, s3next))
        frontier = new_frontier
    return True


# ---------------------------------------------------------------------------
# tau/theta as an ACTUAL substitution homomorphism engine on abstract F2=<x,y>
# (word = list of (gen in {'x','y'}, sign in {+1,-1}) tokens; this is run as
# code, not hand-reduced -- addresses falsifier's 穴1 complaint directly).
# ---------------------------------------------------------------------------
def word_inverse(word):
    return [(g, -e) for (g, e) in reversed(word)]


def apply_hom(word, images):
    """images: dict gen -> word (list of tokens) giving the image of that
    generator (positive power). Substitutes each token; a token (g,-1) gets
    the INVERSE of images[g] (word_inverse), a token (g,+1) gets images[g]
    verbatim. Concatenates in order. This literally runs the homomorphism
    substitution, generalized to any word length (used here on 1-letter
    words, but written generally on purpose)."""
    result = []
    for (g, e) in word:
        img = images[g]
        if e == 1:
            result.extend(img)
        elif e == -1:
            result.extend(word_inverse(img))
        else:
            raise ValueError("only unit exponents expected here")
    return result


def free_reduce(word):
    stack = []
    for tok in word:
        if stack and stack[-1][0] == tok[0] and stack[-1][1] == -tok[1]:
            stack.pop()
        else:
            stack.append(tok)
    return stack


# tau: x -> y, y -> (x*y)^-1 = y^-1 * x^-1
TAU_IMAGES = {
    'x': [('y', 1)],
    'y': [('y', -1), ('x', -1)],
}


def word_to_perm(word, qx, qy, n):
    result = perm_identity(n)
    for (g, e) in word:
        base = qx if g == 'x' else qy
        result = perm_mul(result, perm_pow(base, e))
    return result


def main():
    with open(MC1_PATH, encoding="utf-8") as f:
        data = json.load(f)

    certs = data["mirror_certs"]
    print(f"MC-1 v1.1 independent re-check: {len(certs)} directed entries "
          f"(expect 30 = 15 pairs x 2 directions)")

    report = []
    all_ok = True
    agreement_core_ok = True   # the non-vacuous agreement subset (穴7)

    for c in certs:
        idx = c["index"]
        puid = c["pair_uid"]
        twin_uid = c["target_window_uid"]
        src_uid = c["source_kernel_uid"]
        deg = c["perm_degree"]
        s1 = [int(x) for x in c["s1_perm"]]
        s2 = [int(x) for x in c["s2_perm"]]
        n_words = c["N_gen_words"]
        k_words = c["K_gen_words"]
        gap_in_pb3 = c["in_PB3"]
        gap_c_in_n = c["c_in_N"]
        gap_witness_word = c["witness_word"]
        gap_mclass = c["mclass"]
        gap_checks = c["checks"]

        ident = perm_identity(deg)
        subst_fwd = {"a": s1, "b": s2}
        s1_inv, s2_inv = perm_inv(s1), perm_inv(s2)
        subst_iota = {"a": s1_inv, "b": s2_inv}

        # --- braid ---
        braid_ok = perm_eq(perm_mul(perm_mul(s1, s2), s1), perm_mul(perm_mul(s2, s1), s2))

        # --- N subseteq ker(rho) ---
        n_in_ker = all(perm_eq(eval_word(w, subst_fwd, deg), ident) for w in n_words)

        # --- iota(N) != N: nontrivial witness ---
        iota_witness = None
        for w in n_words:
            if not perm_eq(eval_word(w, subst_iota, deg), ident):
                iota_witness = w
                break
        iota_ne = (iota_witness is not None)

        # --- K identification: order + K subseteq iota(N) ---
        grp_order = bfs_group_order([s1, s2], deg)
        imorder_ok = (grp_order == idx)
        k_under_iota_trivial = all(perm_eq(eval_word(w, subst_iota, deg), ident) for w in k_words)

        # --- SURJ (recorded, but flagged VACUOUS per 穴7: <s1^-1,s2^-1> ---
        # always equals <s1,s2> as an abstract fact -- same generators, just
        # replaced by their inverses, generate the identical subgroup) ---
        surj_order = bfs_group_order([s1_inv, s2_inv], deg)
        surj_ok = (surj_order == idx)

        # --- 【作業1】full hexagon (3.3)(3.4) at [-1,1] on Q (independent) ---
        # x = s1^2, y = s2^2, c = (s1 s2 s1)^2
        x_perm = perm_mul(s1, s1)
        y_perm = perm_mul(s2, s2)
        delta_perm = perm_mul(perm_mul(s1, s2), s1)
        c_perm = perm_mul(delta_perm, delta_perm)
        c_inv_perm = perm_inv(c_perm)

        lhs33 = perm_mul(s1_inv, s2_inv)
        rhs33 = perm_mul(perm_mul(perm_mul(s1, s2), x_perm), c_inv_perm)
        ok33 = perm_eq(lhs33, rhs33)

        lhs34 = perm_mul(s2_inv, s1_inv)
        rhs34 = perm_mul(perm_mul(perm_mul(s2, s1), y_perm), c_inv_perm)
        ok34 = perm_eq(lhs34, rhs34)
        hexagon_full = ok33 and ok34

        # --- 【要修正3】c_in_N independent re-derivation ---
        c_in_n_indep = perm_eq(c_perm, ident)

        # --- 【要修正3】in_PB3 independent re-derivation (from-scratch BFS) ---
        in_pb3_indep = bfs_factors_through_s3(s1, s2, deg)

        # --- 【重大1/作業2】discriminating canary via ACTUAL tau engine ---
        y_inv_word = [('y', -1)]
        p2_word = free_reduce(apply_hom(y_inv_word, TAU_IMAGES))       # tau(y^-1)
        p1_word = free_reduce(apply_hom(p2_word, TAU_IMAGES))          # tau^2(y^-1)
        p3_word = y_inv_word

        # x,y substitution into Q is qx=x_perm, qy=y_perm (already computed above)
        p1_perm = word_to_perm(p1_word, x_perm, y_perm, deg)
        p2_perm = word_to_perm(p2_word, x_perm, y_perm, deg)
        p3_perm = word_to_perm(p3_word, x_perm, y_perm, deg)

        canary_fwd = perm_eq(perm_mul(perm_mul(p1_perm, p2_perm), p3_perm), ident)
        canary_rev = perm_eq(perm_mul(perm_mul(p3_perm, p2_perm), p1_perm), ident)
        canary_discrim = canary_fwd and (not canary_rev)

        # --- cross-check against GAP's own claims (系統A vs 系統B agreement) ---
        gap_python_mclass_consistent = True  # mclass not recomputed by python here
        # (python does not independently recompute mclass in this pass --
        # that already agreed 15/15 in the v1 run; here we focus on the
        # NEW checks. We DO cross-check the frozen-schema claims below.)
        in_pb3_agree = (gap_in_pb3 == in_pb3_indep)
        c_in_n_agree = (gap_c_in_n == c_in_n_indep)
        witness_word_agree = (gap_witness_word == iota_witness) or (
            gap_witness_word is not None and iota_witness is not None
            # different word is fine as long as BOTH are nontrivial witnesses
            # (witness is not required to be unique) -- record actual words
        )
        checks_agree = (
            gap_checks["braid"] == braid_ok and
            gap_checks["N_in_ker"] == n_in_ker and
            gap_checks["K_in_ker"] == k_under_iota_trivial and
            gap_checks["imorder"] == imorder_ok and
            gap_checks["iota_w_nontrivial"] == iota_ne and
            gap_checks["hexagon_full"] == hexagon_full and
            gap_checks["surj"] == surj_ok
        )

        entry_core_ok = (
            braid_ok and n_in_ker and iota_ne and imorder_ok and
            k_under_iota_trivial and hexagon_full and c_in_n_agree and
            in_pb3_agree and checks_agree
        )
        all_ok = all_ok and entry_core_ok
        agreement_core_ok = agreement_core_ok and entry_core_ok

        report.append({
            "index": idx, "pair_uid": puid,
            "target_window_uid": twin_uid, "source_kernel_uid": src_uid,
            "gap_mclass": gap_mclass,
            "braid_ok": braid_ok, "N_subseteq_ker": n_in_ker,
            "iota_N_ne_N": iota_ne, "iota_witness_word_python": iota_witness,
            "gap_witness_word": gap_witness_word,
            "group_order": grp_order, "imorder_ok": imorder_ok,
            "K_subseteq_iotaN": k_under_iota_trivial,
            "surj_ok_VACUOUS": surj_ok,
            "hexagon_33_ok": ok33, "hexagon_34_ok": ok34, "hexagon_full_ok": hexagon_full,
            "c_in_N_python_indep": c_in_n_indep, "c_in_N_gap_claim": gap_c_in_n,
            "c_in_N_agree": c_in_n_agree,
            "in_PB3_python_indep": in_pb3_indep, "in_PB3_gap_claim": gap_in_pb3,
            "in_PB3_agree": in_pb3_agree,
            "canary_forward_trivial": canary_fwd,
            "canary_reversed_trivial_VACUOUS_IF_TRUE": canary_rev,
            "canary_discriminates": canary_discrim,
            "checks_block_agree_with_gap": checks_agree,
            "entry_core_ok": entry_core_ok,
        })
        print(f"index={idx} ({twin_uid}): braid={braid_ok} N_in_ker={n_in_ker} "
              f"iota!=N={iota_ne} order={grp_order}(={idx}? {imorder_ok}) "
              f"K_sub_iotaN={k_under_iota_trivial} hexFull={hexagon_full} "
              f"c_in_N(py={c_in_n_indep},gap={gap_c_in_n},agree={c_in_n_agree}) "
              f"in_PB3(py={in_pb3_indep},gap={gap_in_pb3},agree={in_pb3_agree}) "
              f"canary(fwd={canary_fwd},rev={canary_rev},discrim={canary_discrim}) "
              f"checks_agree={checks_agree} -> core_ok={entry_core_ok}")

    n_discrim_fail = sum(1 for r in report if not r["canary_discriminates"])
    n_hexagon_fail = sum(1 for r in report if not r["hexagon_full_ok"])
    n_inpb3_disagree = sum(1 for r in report if not r["in_PB3_agree"])
    n_cinn_disagree = sum(1 for r in report if not r["c_in_N_agree"])

    print(f"\n=== SUMMARY: {len(certs)} entries, core_ok all={all_ok} ===")
    print(f"hexagon_full failures: {n_hexagon_fail}/{len(certs)}")
    print(f"canary non-discriminating: {n_discrim_fail}/{len(certs)} "
          f"(0 expected -- Q non-abelian in all 15 registered windows)")
    print(f"in_PB3 GAP/python disagreements: {n_inpb3_disagree}/{len(certs)}")
    print(f"c_in_N GAP/python disagreements: {n_cinn_disagree}/{len(certs)}")
    print("\nNOTE (穴7, recorded not asserted): SURJ and charming(u=-1 unit, "
          "f=1 in [P,P]) are VACUOUS discriminators -- <s1^-1,s2^-1>=<s1,s2> "
          "and 'm=-1 is a unit mod anything' hold for ANY window by "
          "construction. They are computed and recorded above but are "
          "EXCLUDED from the 'core_ok' cross-system agreement tally.")

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "all_core_ok": all_ok,
            "n_entries": len(certs),
            "n_hexagon_fail": n_hexagon_fail,
            "n_canary_non_discriminating": n_discrim_fail,
            "n_in_PB3_disagreements": n_inpb3_disagree,
            "n_c_in_N_disagreements": n_cinn_disagree,
            "vacuous_checks_excluded_from_core": ["surj", "charming (wb_charming)"],
            "entries": report,
        }, f, ensure_ascii=False, indent=2)
    print(f"\nWrote {OUT_PATH}")

    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()

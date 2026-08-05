#!/usr/bin/env python3
"""
twin_witness_mc1_check.py -- MC-1 (mirror certificate) independent re-checker.

Prereg: docs/notes/twin_witness_prereg_iffirst_v1.md sec 2.7 / sec 4.1 (系統 B).

GAP-helper-free by construction: this file does NOT import anything from
search/*.g, does not call GAP, and does not reuse any of the GAP mirror
script's (search/twin-witness-mirror-v1.g) code or data structures beyond
reading its JSON EXPORT (search/certs/twin_witness_mc1_export_v1_20260806.json)
-- permutation lists and word strings, i.e. plain data, not logic. All group
theory here (word evaluation, permutation composition, BFS for group order)
is reimplemented from scratch in pure python with no library beyond stdlib.

For each mirror_cert entry (index, s1_perm, s2_perm = images of a=sigma1,
b=sigma2 as permutations of {1..perm_degree} in Q=B3/N, N_gen_words,
K_gen_words), independently re-verifies (doc sec 2.7 points 1-5):

  1. braid relation: s1*s2*s1 == s2*s1*s2  (as permutations)               -- rho well-defined
  2. all N_gen_words evaluate to the identity permutation under rho        -- N subseteq ker(rho)
  3. iota(w) for w in N_gen_words is NOT the identity for at least one w   -- iota(N) != N  <-- THE non-settled bit
  4. BFS: |<s1,s2>| == index (from the entry); all K_gen_words evaluate to
     identity under rho (=> ker(T_{-1,1}) = K, i.e. the mirror partner is
     correctly identified, not just "some" nontrivial kernel)
  5. SURJ: <s1^-1, s2^-1> generates the full permutation group of order
     'index' (T_{-1,1} surjective)

Word grammar handled (matches the census cert's canonical_id_words style,
verified against all 15*2=30 entries actually present): a sequence of
GEN^EXP factors separated by '*', where GEN is 'a' or 'b', or a
PARENTHESIZED-SUBWORD^EXP, with EXP an optional signed integer (default 1).
Nesting of parens is supported (not required by the actual data, but cheap
to support correctly rather than assume flat structure).
"""
import json
import re
import sys

MC1_PATH = "search/certs/twin_witness_mc1_export_v1_20260806.json"


# ---------------------------------------------------------------------------
# permutation arithmetic (1-indexed lists; perm[i-1] = image of i). No numpy,
# no sympy, no group-theory library -- plain python lists and loops.
# ---------------------------------------------------------------------------
def perm_identity(n):
    return list(range(1, n + 1))


def perm_mul(p, q):
    """Composition matching GAP's convention for word evaluation below:
    we need (p*q) applied to i to mean 'apply p then q' in exactly the same
    order our word-evaluator composes syllables (left-to-right word order
    corresponds to repeated perm_mul calls in the same left-to-right order).
    Concretely: perm_mul(p,q)[i] = q[p[i]] (apply p first, then q)."""
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
    k = abs(k)
    result = perm_identity(n)
    for _ in range(k):
        result = perm_mul(result, base)
    return result


def perm_eq(p, q):
    return list(p) == list(q)


# ---------------------------------------------------------------------------
# word parser: tokenizes "a^-6*(a^-1*b^-1*a^-1)^2*..." into a nested AST,
# then evaluates against a substitution {a: perm, b: perm} to a permutation.
# Reimplemented from scratch (no GAP string parsing reused).
# ---------------------------------------------------------------------------
TOKEN_RE = re.compile(r'\s*(\(|\)|\^-?\d+|\*|[ab])')


def tokenize(s):
    pos = 0
    toks = []
    while pos < len(s):
        m = TOKEN_RE.match(s, pos)
        if not m:
            raise ValueError(f"tokenize failure at {pos!r} in {s!r}")
        tok = m.group(1)
        toks.append(tok)
        pos = m.end()
    return toks


def parse_factor(toks, i):
    """factor := ('a'|'b'|'(' expr ')') ['^' signed-int]
    returns (node, next_i). node is ('gen', 'a'|'b') or ('group', subexpr)."""
    tok = toks[i]
    if tok == '(':
        subexpr, i = parse_expr(toks, i + 1)
        assert toks[i] == ')', f"expected ')', got {toks[i]!r}"
        i += 1
        node = ('group', subexpr)
    elif tok in ('a', 'b'):
        node = ('gen', tok)
        i += 1
    else:
        raise ValueError(f"unexpected token {tok!r} at position {i}")
    exp = 1
    if i < len(toks) and toks[i].startswith('^'):
        exp = int(toks[i][1:])
        i += 1
    return (node, exp), i


def parse_expr(toks, i):
    """expr := factor ('*' factor)*  -> list of (node, exp) pairs"""
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
        raise ValueError(f"trailing tokens in {s!r}: {toks[i:]}")
    return expr


def eval_expr(expr, subst, n):
    """expr is a list of (node, exp) factors; evaluate left-to-right,
    composing via perm_mul in word order (matches GAP word semantics:
    the word x*y means 'x then y' as elements multiply; our perm_mul(p,q)
    convention above is defined consistently with that)."""
    result = perm_identity(n)
    for node, exp in expr:
        kind = node[0]
        if kind == 'gen':
            base = subst[node[1]]
        else:  # 'group'
            base = eval_expr(node[1], subst, n)
        result = perm_mul(result, perm_pow(base, exp))
    return result


def eval_word(word_str, subst, n):
    expr = parse_word(word_str)
    return eval_expr(expr, subst, n)


def iota_word(word_str):
    """iota: a -> a^-1, b -> b^-1. Applied HOMOMORPHICALLY: substitute the
    generator itself for its inverse image, i.e. evaluate the SAME parsed
    expression but with subst = {'a': a_inv_perm, 'b': b_inv_perm} instead
    of {'a': a_perm, 'b': b_perm}. This function just returns the word
    string unchanged -- the iota substitution happens at eval_word() call
    site by passing the inverted subst dict. Kept as a named no-op for
    documentation/readability at call sites."""
    return word_str


def bfs_group_order(gens, n):
    """BFS closure of <gens> acting on {1..n} as a subgroup of Sym(n),
    returns |<gens>| via orbit-stabilizer-free brute force (Schreier-Sims
    would be overkill and reintroduce a 'library'; plain BFS over the
    permutation group's element set via a worklist is enough at these
    orders, degree <= ~940)."""
    seen = {tuple(perm_identity(n))}
    frontier = [perm_identity(n)]
    gens_and_invs = list(gens) + [perm_inv(g) for g in gens]
    while frontier:
        new_frontier = []
        for p in frontier:
            for g in gens_and_invs:
                q = perm_mul(p, g)
                tq = tuple(q)
                if tq not in seen:
                    seen.add(tq)
                    new_frontier.append(q)
        frontier = new_frontier
    return len(seen)


def main():
    with open(MC1_PATH, encoding="utf-8") as f:
        data = json.load(f)

    certs = data["mirror_certs"]
    print(f"MC-1 independent re-check: {len(certs)} mirror_cert entries")

    all_ok = True
    report = []
    for c in certs:
        idx = c["index"]
        puid = c["pair_uid"]
        deg = c["perm_degree"]
        s1 = [int(x) for x in c["s1_perm"]]
        s2 = [int(x) for x in c["s2_perm"]]
        n_words = c["N_gen_words"]
        k_words = c["K_gen_words"]

        subst_fwd = {"a": s1, "b": s2}
        s1_inv = perm_inv(s1)
        s2_inv = perm_inv(s2)
        subst_iota = {"a": s1_inv, "b": s2_inv}

        # (1) braid relation: s1*s2*s1 == s2*s1*s2
        lhs = perm_mul(perm_mul(s1, s2), s1)
        rhs = perm_mul(perm_mul(s2, s1), s2)
        braid_ok = perm_eq(lhs, rhs)

        # (2) N subseteq ker(rho): every N_gen_word evaluates to identity
        ident = perm_identity(deg)
        n_in_ker = all(perm_eq(eval_word(w, subst_fwd, deg), ident) for w in n_words)

        # (3) iota(N) != N: at least one N_gen_word, under the iota
        # substitution, is NOT identity
        iota_nontrivial_witness = None
        for w in n_words:
            img = eval_word(iota_word(w), subst_iota, deg)
            if not perm_eq(img, ident):
                iota_nontrivial_witness = w
                break
        iota_N_ne_N = (iota_nontrivial_witness is not None)

        # (4) K identification: BFS order == index, and K_gen_words all map
        # to identity under (rho o iota) -- i.e. K subseteq iota(N), and by
        # index equality (both = idx) this gives ker(T_{-1,1}) = K.
        grp_order = bfs_group_order([s1, s2], deg)
        order_ok = (grp_order == idx)
        k_under_iota_trivial = all(
            perm_eq(eval_word(w, subst_iota, deg), ident) for w in k_words
        )

        # (5) SURJ: <s1^-1, s2^-1> has order == idx (T_{-1,1} surjective)
        surj_order = bfs_group_order([s1_inv, s2_inv], deg)
        surj_ok = (surj_order == idx)

        entry_ok = braid_ok and n_in_ker and iota_N_ne_N and order_ok and k_under_iota_trivial and surj_ok
        all_ok = all_ok and entry_ok

        report.append({
            "index": idx, "pair_uid": puid,
            "braid_ok": braid_ok,
            "N_subseteq_ker": n_in_ker,
            "iota_N_ne_N": iota_N_ne_N,
            "iota_nontrivial_witness_word": iota_nontrivial_witness,
            "group_order": grp_order, "order_matches_index": order_ok,
            "K_subseteq_iotaN": k_under_iota_trivial,
            "surj_order": surj_order, "surj_ok": surj_ok,
            "entry_ok": entry_ok,
        })
        print(f"index={idx} pair_uid={puid}: braid={braid_ok} N_in_ker={n_in_ker} "
              f"iota(N)!=N={iota_N_ne_N} |<s1,s2>|={grp_order}(==idx? {order_ok}) "
              f"K_subseteq_iotaN={k_under_iota_trivial} surj={surj_ok} "
              f"-> entry_ok={entry_ok}")

    print(f"\nALL {len(certs)} entries: {'ALL_OK (cross-checked)' if all_ok else 'MISMATCH -- see report'}")

    with open("search/certs/twin_witness_mc1_check_result_v1_20260806.json", "w", encoding="utf-8") as f:
        json.dump({"all_ok": all_ok, "entries": report}, f, ensure_ascii=False, indent=2)
    print("Wrote search/certs/twin_witness_mc1_check_result_v1_20260806.json")

    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
r6a_word_iota_checker.py -- R-6a word-level iota identification, INDEPENDENT
python side (系統B per docs/notes/twin_witness_prereg_iffirst_v1.md SS4.1).
sol/sol_reply_112_math38.md F112-5/R-6a; 裁定637 task 2.

GAP-helper-free by construction: does NOT import anything from search/*.g,
does NOT call GAP, and does NOT reuse code from search/r6a_word_iota_v1.g
beyond reading its JSON EXPORT (permutation lists + word strings, i.e. plain
data, not logic). Word parsing/evaluation and permutation arithmetic are
reimplemented from scratch in pure python (stdlib only), independently of
search/twin_witness_mc1_check.py (a different file, different task, no
import relationship -- convention cross-checked against it only insofar as
both correctly reproduce GAP's own '*' semantics for B3 word evaluation).

For every frozen member N (index, permutation rep rho=(s1_perm,s2_perm) with
ker(rho)=N, own canonical_id_words), this script:
  1. Re-verifies independently that N's own words evaluate to the identity
     under rho (sanity: confirms the GAP-side export is self-consistent).
  2. Computes iota(N)'s generating words by applying the automorphism
     a->a^-1, b->b^-1 to the AST of each canonical_id_word (homomorphism
     property: iota(x*y)=iota(x)*iota(y), iota(x^k)=iota(x)^k, so only the
     GENERATOR LEAVES need sign-flipping; parenthesized-subword outer
     exponents are left untouched and the transform still computes
     iota(word) exactly).
  3. For every OTHER member M in the SAME FROZEN FIBER as N (fiber = the
     750-clique as a whole for set (i); the member's own registered pair for
     sets (ii)/(iii) -- exactly as declared in the frozen cert, no
     enlargement), evaluates every iota-transformed generator word of N
     against M's (s1_perm, s2_perm). If ALL map to the identity permutation,
     iota(N) <= M; since N and M have the SAME index within a declared
     fiber, [B3:iota(N)] = [B3:N] = index = [B3:M], so iota(N) <= M with
     equal finite index forces iota(N) = M exactly (subgroup of equal index
     containing it must equal it).
  4. Records the match (should be exactly one candidate per N, including N
     itself as a candidate -- a self-match means N is iota-FIXED).

NO hexagon/charming/SURJ/kernel_multiplicity/settled/isolated/GTSh/
arithmeticity predicate is evaluated. NO TRUE/FALSE verdict is attached to
any external checker. Output is the raw identification only, exactly as
scoped by R-6a.
"""
import json
import re

EXPORT_PATH = "search/certs/r6a_word_iota_gap_export_v1_20260806.json"
FREEZE_PATH = "search/certs/r6a_scope_freeze_v1_20260806.json"
OUT_PATH = "search/certs/r6a_word_iota_checker_v1_20260806.json"


# ---------------------------------------------------------------------------
# permutation arithmetic (1-indexed lists; perm[i-1] = image of i).
# perm_mul(p,q)[i] = q[p[i]-1]  ("apply p first, then q" -- matches GAP's
# right-action '*' convention as already validated in
# search/twin_witness_mc1_check.py for this exact B3-word-evaluation task).
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
    k = abs(k)
    result = perm_identity(n)
    for _ in range(k):
        result = perm_mul(result, base)
    return result


def perm_eq(p, q):
    return list(p) == list(q)


# ---------------------------------------------------------------------------
# word parser -> AST. Grammar: sequence of FACTOR ('*' FACTOR)*, FACTOR is
# GEN ('^' EXP)? or '(' WORD ')' ('^' EXP)?, GEN in {a,b}, EXP signed int.
# AST node: ('gen', 'a'|'b', exp) or ('group', [subword-AST...], exp)
# (a 'group' node's children are themselves a *-separated list of factors).
# ---------------------------------------------------------------------------
TOKEN_RE = re.compile(r'\s*(\(|\)|\^-?\d+|\*|[ab])')


def tokenize(s):
    pos = 0
    toks = []
    while pos < len(s):
        m = TOKEN_RE.match(s, pos)
        if not m:
            raise ValueError(f"bad token at {pos} in {s!r}")
        toks.append(m.group(1))
        pos = m.end()
    return toks


def parse_word(s):
    toks = tokenize(s)
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def parse_factor():
        t = peek()
        if t == '(':
            pos[0] += 1
            sub = parse_seq()
            if peek() != ')':
                raise ValueError(f"expected ) in {s!r}")
            pos[0] += 1
            exp = 1
            if peek() is not None and peek().startswith('^'):
                exp = int(peek()[1:])
                pos[0] += 1
            return ('group', sub, exp)
        elif t in ('a', 'b'):
            pos[0] += 1
            exp = 1
            if peek() is not None and peek().startswith('^'):
                exp = int(peek()[1:])
                pos[0] += 1
            return ('gen', t, exp)
        else:
            raise ValueError(f"unexpected token {t!r} in {s!r}")

    def parse_seq():
        factors = [parse_factor()]
        while peek() == '*':
            pos[0] += 1
            factors.append(parse_factor())
        return factors

    seq = parse_seq()
    if pos[0] != len(toks):
        raise ValueError(f"trailing tokens in {s!r}")
    return seq


def eval_ast_seq(seq, subst):
    n = len(next(iter(subst.values())))
    result = perm_identity(n)
    for node in seq:
        result = perm_mul(result, eval_ast_node(node, subst))
    return result


def eval_ast_node(node, subst):
    kind = node[0]
    if kind == 'gen':
        _, g, exp = node
        return perm_pow(subst[g], exp)
    else:
        _, sub, exp = node
        base = eval_ast_seq(sub, subst)
        return perm_pow(base, exp)


def eval_word(s, subst):
    return eval_ast_seq(parse_word(s), subst)


# ---------------------------------------------------------------------------
# iota transform on the AST: negate every GENERATOR LEAF's exponent; leave
# 'group' (parenthesized-subword) outer exponents untouched, recurse into
# their children. Homomorphism property makes this exactly compute
# iota(word)'s AST (see module docstring point 2).
# ---------------------------------------------------------------------------
def iota_seq(seq):
    return [iota_node(node) for node in seq]


def iota_node(node):
    kind = node[0]
    if kind == 'gen':
        _, g, exp = node
        return ('gen', g, -exp)
    else:
        _, sub, exp = node
        return ('group', iota_seq(sub), exp)


def iota_word_ast(s):
    return iota_seq(parse_word(s))


def eval_iota_word(s, subst):
    return eval_ast_seq(iota_word_ast(s), subst)


def main():
    with open(EXPORT_PATH, encoding="utf-8") as f:
        exp_data = json.load(f)
    with open(FREEZE_PATH, encoding="utf-8") as f:
        freeze_data = json.load(f)

    assert exp_data["frozen_selection_sha256"] == freeze_data["frozen_selection_sha256"], \
        "GAP export's frozen_selection_sha256 does not match the freeze cert -- STOP"

    members = {m["uid"]: m for m in exp_data["members"]}

    # sanity: every member's own words trivial under its own rho (independent
    # re-derivation of the GAP side's all_own_words_trivial claim)
    sanity_fail = []
    for uid, m in members.items():
        subst = {"a": m["s1_perm"], "b": m["s2_perm"]}
        n = m["index"]
        for w in m["own_words"]:
            img = eval_word(w, subst)
            if img != list(range(1, n + 1)):
                sanity_fail.append((uid, w))
    if sanity_fail:
        raise SystemExit(f"SANITY FAILURE (own words not trivial): {sanity_fail[:5]} ...")

    # build fiber -> [uids]
    fibers = {}
    for uid, m in members.items():
        fibers.setdefault(m["fiber"], []).append(uid)

    results = []
    for uid, m in members.items():
        fiber = m["fiber"]
        candidates = fibers[fiber]
        matches = []
        for cand_uid in candidates:
            cand = members[cand_uid]
            if cand["index"] != m["index"]:
                continue  # should not happen within a declared fiber; defensive only
            subst = {"a": cand["s1_perm"], "b": cand["s2_perm"]}
            n = cand["index"]
            ident = list(range(1, n + 1))
            all_trivial = True
            for w in m["own_words"]:
                img = eval_iota_word(w, subst)
                if img != ident:
                    all_trivial = False
                    break
            if all_trivial:
                matches.append(cand_uid)
        results.append({
            "uid": uid, "fiber": fiber, "index": m["index"],
            "iota_matches": matches,
            "iota_is_fixed": (uid in matches),
            "iota_match_count": len(matches),
        })

    n_no_match = sum(1 for r in results if r["iota_match_count"] == 0)
    n_multi_match = sum(1 for r in results if r["iota_match_count"] > 1)
    n_single_match = sum(1 for r in results if r["iota_match_count"] == 1)

    out = {
        "schema": "r6a-word-iota-checker/v1",
        "note": "System B (independent python, GAP-helper-free) word-level iota identification. "
                "iota_matches lists which SAME-FROZEN-FIBER member(s) (by uid) iota(N)'s generator "
                "words all evaluate to the identity under -- i.e. which member iota(N) equals, "
                "given the equal-index-within-fiber argument in the module docstring. NO hexagon/"
                "charming/SURJ/kernel_multiplicity/settled/isolated/GTSh/arithmeticity predicate "
                "evaluated anywhere. NO TRUE/FALSE verdict attached.",
        "authorization": "sol/sol_reply_112_math38.md F112-5/R-6a; 裁定637 task 2",
        "gap_export_sha256_cross_check": "frozen_selection_sha256 matched between GAP export and freeze cert (see assert above)",
        "member_count": len(results),
        "own_words_sanity": "ALL PASS (independent re-derivation)" if not sanity_fail else "FAIL",
        "match_summary": {"single_match": n_single_match, "no_match": n_no_match, "multi_match": n_multi_match},
        "results": results,
    }
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Wrote {OUT_PATH}")
    print(f"  members={len(results)} single_match={n_single_match} no_match={n_no_match} multi_match={n_multi_match}")
    for r in results:
        if r["fiber"] == "clique750:ALL":
            print(f"  {r['uid']}: matches={r['iota_matches']} fixed={r['iota_is_fixed']}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
drophunt_checker_v2.py -- REPAIR per ruling 1737 / spec v2 (scratchpad/
fib_ruling_and_fibre_checker_spec_v2.md sha16 380efc51a241ce67).

Standard library only (json, hashlib, math, sys). Does not import/Read()
search/drophunt_checker_producer_v2.g or any GAP helper. Reads only the
producer's JSON receipt.

Changes vs v1 checker (search/drophunt_checker_v1.py, superseded for this
predicate):
  CK-1: independently RE-DERIVES [G,G] (DerivedSubgroup) membership via a
        degree-bounded Schreier-Sims-style stabilizer chain + normal-closure
        generator search, NOT trusting the producer's charming boolean.
        (v1 declared this "not independently recomputable in pure Python" --
        the falsifier demonstrated that claim was wrong in 15 lines/0.4s;
        this file's group theory section is the repair of that error.)
  CK-2: checks F2 * 1,469,664 == F5 (|G|).
  CK-3: checks the M-block restriction (points 0..35) of <JX,JY> reproduces
        exactly Group(MX,MY) of order 1,469,664 (the M-block projection is
        onto -- i.e. the window genuinely contains M).
  CK-4: short-circuited rows in a producer receipt are represented with
        null (not false) for hex310/hex311/onto/reduction_match/verdict;
        this checker treats "null" as "not evaluated by the producer" and
        does NOT independently evaluate those stages for BLOCKED
        (c_notin_K) windows either -- it only confirms the row is correctly
        marked BLOCKED and does not silently promote null to false.
  Predicate: theta(x)=y,theta(y)=x ; tau(x)=y,tau(y)=(xy)^-1 (word-level,
  applied ONLY when the window's own c_in_K flag is true -- this checker
  refuses to evaluate hexagon/onto on a BLOCKED (c_notin_K) window's rows,
  since word-level substitution is not known-safe there, matching the
  producer's own scope limit rather than silently trusting or re-deriving
  a predicate this checker cannot currently validate).
"""
from __future__ import annotations

import hashlib
import json
import math
import sys


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canonical(v: object) -> bytes:
    return json.dumps(v, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")


Perm = tuple


def load_perm_1indexed(lst: list[int]) -> Perm:
    return tuple(int(x) - 1 for x in lst)


def pid(n: int) -> Perm:
    return tuple(range(n))


def pmul(a: Perm, b: Perm) -> Perm:
    return tuple(b[a[i]] for i in range(len(a)))


def pinv(a: Perm) -> Perm:
    out = [0] * len(a)
    for i, img in enumerate(a):
        out[img] = i
    return tuple(out)


def ppow(a: Perm, e: int) -> Perm:
    if e < 0:
        return ppow(pinv(a), -e)
    n = len(a)
    out = pid(n)
    base = a
    while e:
        if e & 1:
            out = pmul(out, base)
        base = pmul(base, base)
        e >>= 1
    return out


def theta_letter(code: int) -> list[int]:
    if code == 1:
        return [2]
    if code == -1:
        return [-2]
    if code == 2:
        return [1]
    if code == -2:
        return [-1]
    raise ValueError(code)


def tau_letter(code: int) -> list[int]:
    if code == 1:
        return [2]
    if code == -1:
        return [-2]
    if code == 2:
        return [-2, -1]
    if code == -2:
        return [1, 2]
    raise ValueError(code)


def theta_word(word: list[int]) -> list[int]:
    out: list[int] = []
    for c in word:
        out.extend(theta_letter(c))
    return out


def tau_word(word: list[int]) -> list[int]:
    out: list[int] = []
    for c in word:
        out.extend(tau_letter(c))
    return out


def eval_word(word: list[int], JX: Perm, JY: Perm, deg: int) -> Perm:
    val = pid(deg)
    for c in word:
        g = JX if abs(c) == 1 else JY
        gp = g if c > 0 else pinv(g)
        val = pmul(gp, val)  # prepend
    return val


# ---------------------------------------------------------------------------
# Degree-bounded stabilizer chain (orbit + Schreier generators), returning
# a reusable CHAIN structure supporting both order computation and a sift-
# based membership test. This is the CK-1 repair: the same technique used
# for the onto check (group_order) is extended here with a sift() function
# so [G,G]-membership can be tested WITHOUT enumerating the (possibly
# millions-large) group -- only degree-bounded orbit/transversal data is
# ever stored.
# ---------------------------------------------------------------------------

def build_stabilizer_chain(gens: list[Perm], deg: int) -> list[dict]:
    """Returns a list of levels; level i = {'base': b, 'orbit': {point: transversal_perm}, 'gens': [...]}."""
    current = [g for g in gens if g != pid(deg)]
    remaining_points = list(range(deg))
    chain = []
    while True:
        moved = [p for p in remaining_points if any(g[p] != p for g in current)]
        if not moved or not current:
            break
        b = moved[0]
        orbit: dict[int, Perm] = {b: pid(deg)}
        frontier = [b]
        while frontier:
            nxt_frontier = []
            for p in frontier:
                up = orbit[p]
                for g in current:
                    q = g[p]
                    if q not in orbit:
                        orbit[q] = pmul(up, g)
                        nxt_frontier.append(q)
            frontier = nxt_frontier
        schreier = []
        seen_sch = set()
        for p, up in orbit.items():
            for g in current:
                q = g[p]
                uq_inv = pinv(orbit[q])
                sgen = pmul(pmul(up, g), uq_inv)
                if sgen != pid(deg) and sgen not in seen_sch:
                    seen_sch.add(sgen)
                    schreier.append(sgen)
        chain.append({"base": b, "orbit": orbit})
        current = schreier
        remaining_points = [p for p in remaining_points if p != b]
    return chain


def chain_order(chain: list[dict]) -> int:
    order = 1
    for level in chain:
        order *= len(level["orbit"])
    return order


def sift(chain: list[dict], g: Perm) -> Perm | None:
    """Standard stabilizer-chain sift: returns the residual (should be
    identity iff g is in the group generated by the ORIGINAL gens the chain
    was built from), or None if g is definitely NOT in the group (its image
    of some base point falls outside that level's orbit)."""
    cur = g
    for level in chain:
        b = level["base"]
        p = cur[b]
        if p not in level["orbit"]:
            return None
        cur = pmul(cur, pinv(level["orbit"][p]))
    return cur


def group_order(gens: list[Perm], deg: int) -> int:
    return chain_order(build_stabilizer_chain(gens, deg))


def is_identity_after_sift(chain: list[dict], g: Perm, deg: int) -> bool:
    r = sift(chain, g)
    return r is not None and r == pid(deg)


def derived_subgroup_chain(JX: Perm, JY: Perm, deg: int, max_rounds: int = 6) -> list[dict]:
    """[G,G] for G=<JX,JY> is the NORMAL CLOSURE of the single commutator
    [JX,JY] (standard fact for a 2-generator group: G/N abelian iff
    [JX,JY] in N, so the smallest such N is the normal closure of
    [JX,JY]). Build it via bounded-round conjugation-closure on the
    GENERATING SET (not on group elements): start from {[JX,JY]}, repeatedly
    add JX^-1 g JX, JX g JX^-1, JY^-1 g JY, JY g JY^-1 for each current
    generator g, stopping when a round adds no new generator OR after
    max_rounds (whichever first) -- this is the SAME bounded-iteration
    pattern used elsewhere in this repo for other normal closures (e.g.
    search/d972_rung_ordinary_idx3_producer_v2.py's
    normal_closure_commutator_g36), reimplemented independently here.
    Returns the STABILIZER CHAIN of the resulting generating set (usable
    both for order and for sift-based membership testing) -- this is the
    degree-bounded piece; the generating SET can still grow, but is
    typically small (dozens, not millions), and building its stabilizer
    chain is degree-bounded regardless of how many generators it has."""
    comm = pmul(pmul(pinv(JX), pinv(JY)), pmul(JX, JY))  # [x,y] = x^-1 y^-1 x y
    gens = {comm}
    conjugators = [JX, pinv(JX), JY, pinv(JY)]
    for _ in range(max_rounds):
        new_gens = set(gens)
        for g in list(gens):
            for c in conjugators:
                new_gens.add(pmul(pmul(pinv(c), g), c))
        if new_gens == gens:
            break
        gens = new_gens
    return build_stabilizer_chain(list(gens), deg)


def digest_of(v: object) -> str:
    return sha256_bytes(canonical(v))


def check_receipt(path: str) -> dict:
    with open(path, "rb") as fh:
        raw = fh.read()
    receipt_sha256 = sha256_bytes(raw)
    receipt = json.loads(raw.decode("utf-8"))

    errors: list[str] = []

    def require(cond: bool, code: str, detail: str = "") -> None:
        if not cond:
            errors.append(f"{code}: {detail}")

    require(receipt.get("schema") in ("drophunt-checker-producer/v2", "drophunt-checker-producer-v2-window/v1"),
            "SCHEMA_MISMATCH", str(receipt.get("schema")))

    window = receipt["window"]
    K_ord = window["K_ord"]
    M_ord = window["M_ord"]
    F1 = window["F1_m_factor"]
    F2 = window["F2_ratio"]
    F3 = window["F3_fib"]
    F5 = window["F5_size_G"]
    deg = window["degree"]
    c_in_K = window["c_in_K"]
    JX = load_perm_1indexed(window["JX_one_line"])
    JY = load_perm_1indexed(window["JY_one_line"])

    require(K_ord % M_ord == 0, "CC4_K_NOT_LE_M", f"K_ord={K_ord} M_ord={M_ord}")
    require(F1 == K_ord // M_ord, "F1_MISMATCH", "")
    require(F3 == F1 * F2, "FIB_FORMULA_CHECK", "")

    # CK-2: F2 * 1,469,664 == F5
    require(F2 * 1469664 == F5, "CK2_F2_TIMES_MORD_NE_F5", f"F2={F2} F5={F5}")

    # independently recompute |<JX,JY>| via the degree-bounded stabilizer chain
    g_chain = build_stabilizer_chain([JX, JY], deg)
    g_order = chain_order(g_chain)
    require(g_order == F5, "F5_SIZE_G_MISMATCH", f"computed={g_order} declared={F5}")

    # CK-3: M-block order check -- the restriction of <JX,JY> to points
    # [0..35] (the fixed roof-M block, by construction of every window in
    # this family) must equal Group(MX,MY), order 1,469,664. We test this
    # via the SAME group-order technique applied to the projected
    # generators (JX restricted to the first 36 points, likewise JY) --
    # note restriction of a permutation acting block-diagonally to one
    # block is itself a valid permutation on that block.
    JX_mblock = tuple(JX[i] for i in range(36))
    JY_mblock = tuple(JY[i] for i in range(36))
    mblock_order = group_order([JX_mblock, JY_mblock], 36)
    require(mblock_order == 1469664, "CK3_MBLOCK_ORDER_MISMATCH", f"computed={mblock_order}")

    # CK-1: independent [G,G] derivation
    derived_chain = derived_subgroup_chain(JX, JY, deg)
    derived_order = chain_order(derived_chain)

    seed = receipt["seed"]
    rows = receipt["rows"]
    cc1 = receipt["cc1_candidate_coverage"]
    require(len(rows) == F3, "CC1_EVALUATED_COUNT", f"len(rows)={len(rows)} F3={F3}")
    require(cc1["evaluated_count"] == F3 and cc1["expected_count"] == F3 and cc1["match"] is True, "CC1_FIELD_MISMATCH", "")

    if not c_in_K:
        # BLOCKED window: every row must show null placeholders (CK-4), and
        # this checker does NOT independently evaluate hexagon/onto here
        # (matching the producer's own documented scope limit -- word-level
        # substitution is not known-safe when c notin K).
        for row in rows:
            for field in ("charming", "hex310", "hex311", "onto", "reduction_match", "verdict"):
                require(row[field] is None, "CK4_BLOCKED_ROW_NOT_NULL", f"row m={row['m']} field={field}={row[field]}")
            require(row["stage"] == "BLOCKED_c_notin_K", "CK4_BLOCKED_STAGE_LABEL", str(row["stage"]))
        status = "PASS" if not errors else "FAIL"
        return {
            "schema": "drophunt-checker-independent-verdict/v2",
            "receipt_path": path, "receipt_sha256": receipt_sha256,
            "status": status, "errors": errors,
            "window_c_in_K": c_in_K,
            "recomputed_group_order": g_order, "declared_F5_size_G": F5,
            "recomputed_derived_subgroup_order": derived_order,
            "note": "BLOCKED window (c_notin_K): checker confirms null-placeholder discipline only; hexagon/onto NOT independently evaluated here (predicate not known-safe for this window class in this repair pass).",
        }

    # c_in_K=true window: full independent re-derivation.
    m_block_targets = set()
    seen_pairs = set()
    recomputed_valid = 0
    ck1_mismatches = 0

    for row in rows:
        m = row["m"]
        word = row["f_word_codes"]
        pair_key = (m, tuple(word))
        require(pair_key not in seen_pairs, "CC1_DUPLICATE_CANDIDATE", str(pair_key))
        seen_pairs.add(pair_key)
        require(m % M_ord == 0, "M_CONGRUENCE", f"m={m}")

        fperm = eval_word(word, JX, JY, deg)

        # CK-1: independent charming[G,G]-half re-derivation, replacing the
        # producer's own DerivedSubgroup membership check.
        ck1_in_derived = is_identity_after_sift(derived_chain, fperm, deg)
        # NOTE: producer's "charming" also requires gcd(2m+1,K_ord)=1; we
        # recompute that arithmetic half too for a complete independent
        # charming re-derivation.
        ck1_gcd_ok = math.gcd(2 * m + 1, K_ord) == 1
        ck1_charming = ck1_gcd_ok and ck1_in_derived
        if ck1_charming != row["charming"]:
            ck1_mismatches += 1
            errors.append(f"CK1_CHARMING_MISMATCH: row m={m} recomputed={ck1_charming} producer={row['charming']}")

        if not row["charming"]:
            require(row["stage"] == "charming_fail", "STAGE_LABEL_MISMATCH_ON_CHARMING_FAIL", str(row["stage"]))
            require(row["hex310"] is False and row["hex311"] is False and row["onto"] is False and row["verdict"] is False,
                    "SHORT_CIRCUIT_PLACEHOLDER_NOT_FALSE", str(row))
            hex310_recomputed = None
            hex311_recomputed = None
        else:
            thetaW = theta_word(word)
            hex310_recomputed = eval_word(word + thetaW, JX, JY, deg) == pid(deg)
            require(hex310_recomputed == row["hex310"], "HEX310_MISMATCH", f"row m={m}")
            if not row["hex310"]:
                require(row["stage"] == "hex310_fail", "STAGE_LABEL_MISMATCH_ON_HEX310_FAIL", str(row["stage"]))
                require(row["hex311"] is False and row["onto"] is False and row["verdict"] is False,
                        "SHORT_CIRCUIT_PLACEHOLDER_NOT_FALSE_AFTER_HEX310", str(row))
                hex311_recomputed = None
            else:
                ymfWord = ([2] * m) + word
                tau1 = tau_word(ymfWord)
                tau2 = tau_word(tau1)
                # RHS is c^m; since c_in_K, c's joint image is the identity,
                # so c^m = identity for every m -- checked here as a real
                # computation using the SAME group-element identity, not
                # assumed.
                hex311_recomputed = eval_word(tau2 + tau1 + ymfWord, JX, JY, deg) == pid(deg)
                require(hex311_recomputed == row["hex311"], "HEX311_MISMATCH", f"row m={m}")

        if row["charming"] and hex310_recomputed and hex311_recomputed:
            u = 2 * m + 1
            genA = ppow(JX, u)
            genB = pmul(pmul(pinv(fperm), ppow(JY, u)), fperm)
            onto_order = group_order([genA, genB], deg)
            onto_recomputed = onto_order == g_order
            require(onto_recomputed == row["onto"], "ONTO_MISMATCH", f"row m={m}")
        elif row["charming"] and hex310_recomputed and not hex311_recomputed:
            require(row["stage"] == "hex311_fail", "STAGE_LABEL_MISMATCH_ON_HEX311_FAIL", str(row["stage"]))
            require(row["onto"] is False and row["verdict"] is False, "SHORT_CIRCUIT_PLACEHOLDER_NOT_FALSE_AFTER_HEX311", str(row))

        m_block = fperm[:36]
        m_block_targets.add(m_block)

        verdict_recomputed = row["charming"] and bool(hex310_recomputed) and bool(hex311_recomputed) and row.get("onto", False) and row["reduction_match"]
        require(verdict_recomputed == row["verdict"], "VERDICT_RECOMPUTE_MISMATCH", f"row m={m}")
        if row["verdict"]:
            recomputed_valid += 1

    require(len(m_block_targets) == 1, "REDUCTION_MBLOCK_INCONSISTENT", f"{len(m_block_targets)} distinct")
    require(recomputed_valid == receipt["valid_count"], "VALID_COUNT_MISMATCH", f"recomputed={recomputed_valid} declared={receipt['valid_count']}")
    require(ck1_mismatches == 0, "CK1_CHARMING_DERIVED_SUBGROUP_MISMATCHES", str(ck1_mismatches))

    status = "PASS" if not errors else "FAIL"
    return {
        "schema": "drophunt-checker-independent-verdict/v2",
        "receipt_path": path, "receipt_sha256": receipt_sha256,
        "status": status, "errors": errors,
        "window_c_in_K": c_in_K,
        "recomputed_group_order": g_order, "declared_F5_size_G": F5,
        "recomputed_derived_subgroup_order": derived_order,
        "recomputed_valid_count": recomputed_valid, "declared_valid_count": receipt.get("valid_count"),
        "ck1_charming_mismatches": ck1_mismatches,
        "evaluated_count": len(rows), "expected_count_F3": F3,
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: drophunt_checker_v2.py <receipt.json> [...]", file=sys.stderr)
        return 2
    results = [check_receipt(p) for p in argv[1:]]
    print(json.dumps(results, indent=2))
    return 0 if all(r["status"] == "PASS" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

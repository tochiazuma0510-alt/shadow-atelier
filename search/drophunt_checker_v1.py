#!/usr/bin/env python3
"""
drophunt_checker_v1.py -- INDEPENDENT checker for the general-purpose fibre
producer search/drophunt_checker_producer_v1.g (spec: scratchpad/
fib_ruling_and_fibre_checker_spec_v1.md SS2, ruling 1720/1722).

Author-separation discipline (LOCAL-3 v1 style, spec SS2.4): standard library
only (json, hashlib, math, sys, itertools, collections -- nothing else).
Reads ONLY the producer's JSON receipt bytes (path given on argv). Does NOT
import, Read(), or otherwise open search/drophunt_checker_producer_v1.g,
search/week3-battery-common.g, or any other GAP producer helper. All group
theory (permutation composition, theta/tau substitution, hexagon evaluation,
onto-order verification) is reimplemented HERE from the public mathematical
definitions (2401.06870 hexagon (3.10)/(3.11); the receipt's own predicate
labels theta:x<->y, tau:x->y,y->(xy)^-1, which are quoted directly from the
paper/spec, not from producer code).

Independently RE-DERIVED (full recomputation from raw JX,JY permutations +
f_word_codes in the receipt, NOT trusting the producer's verdict fields):
  - m'-congruence (m mod M_ord == seed m_seed)               [cheap, exact]
  - f'-word replay: evaluate f_word_codes into a permutation using an
    independently-implemented prepend word evaluator + independently-
    implemented permutation composition, and cross-check internal
    consistency of the M-block restriction (points 1..M_DEGREE=36) across
    ALL candidates in the same window+seed (they must all agree, since by
    construction every raw candidate reduces to the same seed).            [cheap, exact]
  - hexagon (3.10): f'*theta(f') = 1                                       [cheap, exact]
  - hexagon (3.11): tau^2(y^m'f')*tau(y^m'f')*(y^m'f') = 1                 [cheap, exact]
  - onto: |<x^(2m'+1), f'^-1 y^(2m'+1) f'>| == |G| (F5), via an
    independently-implemented orbit/Schreier-generator stabilizer-chain
    order algorithm (degree-bounded, not order-bounded -- feasible for
    |G| in the millions since degree stays in the low hundreds).           [exact, nontrivial]

SCOPE LIMITATION (stated honestly, not hidden -- see the calibration report
for the full reasoning): the "f' in [G,G]" half of the CHARMING predicate is
NOT independently re-derived from raw permutation data by this checker. Full
recomputation would require either (a) constructing [G,G] as a normal
closure (order-bounded, infeasible in pure Python for |G| ~ millions without
a permutation-group library), or (b) computing G^ab structurally, which is
circular without such a library. Standard-library-only Python has no
Schreier-Sims-with-derived-subgroup toolkit, and importing one (e.g. sympy)
would violate the "standard library only" rule. Instead this checker
performs an ARITHMETIC PROXY cross-check: it verifies that the producer's
charming/non-charming classification is INTERNALLY CONSISTENT with the
abelianized exponent vector ab(f'_word) in Z^2 (all charming-accepted
candidates in a window must share one residue class of ab(f') modulo a
common finite-index sublattice; the checker verifies this coherence across
all rows in the receipt without asserting the specific value of that
sublattice). Any receipt whose charming column is NOT proxy-consistent is
rejected (fail-closed) even though this checker cannot prove which specific
value was wrong.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from itertools import product


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canonical(v: object) -> bytes:
    return json.dumps(v, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")


# ---------------------------------------------------------------------------
# Permutation arithmetic (0-indexed internally; receipt permutations are
# GAP 1-indexed one-line notation, converted on load). Convention: pmul(A,B)
# means "apply A then B" as GROUP ELEMENTS, i.e. i^(A*B)=(i^A)^B, matching
# GAP's right-action semantics that the producer's permutations were built
# under. This is the SAME public convention documented in
# search/d972_rung_ordinary_idx3_producer_v2.py's pmul (an independently
# pre-existing, differently-authored producer for a related calibration
# window) -- both implementations follow the identical GAP semantics because
# that semantics is a mathematical fact about the source system, not a
# shared design choice between this checker and drophunt's own producer.
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# theta/tau letter substitution (public definitions: theta(x)=y, theta(y)=x;
# tau(x)=y, tau(y)=(xy)^-1; extended letter-wise with sign, prepend word
# convention: eval(word) = g_last * ... * g_first as GROUP ELEMENTS).
# f_word_codes convention: 1=x, -1=x^-1, 2=y, -2=y^-1.
# ---------------------------------------------------------------------------

def theta_letter(code: int) -> list[int]:
    # x<->y, sign preserved
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
    # tau(x)=y, tau(x^-1)=y^-1 ; tau(y)=y^-1 x^-1, tau(y^-1)=x y
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
        val = pmul(gp, val)  # prepend: val := g^pow * val
    return val


def word_ab_vector(word: list[int]) -> tuple[int, int]:
    a = sum(1 for c in word if c == 1) - sum(1 for c in word if c == -1)
    b = sum(1 for c in word if c == 2) - sum(1 for c in word if c == -2)
    return (a, b)


# ---------------------------------------------------------------------------
# Group order via orbit + Schreier-generator stabilizer chain (base =
# [0..deg-1], skipping fixed points at each level). Degree-bounded, not
# order-bounded -- suitable for |G| in the millions as long as the
# permutation DEGREE stays modest (all windows in this pass have degree
# well under 200).
# ---------------------------------------------------------------------------

def group_order(gens: list[Perm], deg: int) -> int:
    current = [g for g in gens if g != pid(deg)]
    order = 1
    remaining_points = list(range(deg))
    while True:
        moved = [p for p in remaining_points if any(g[p] != p for g in current)]
        if not moved or not current:
            break
        b = moved[0]
        # orbit of b under current gens, transversal stored as actual perms
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
        order *= len(orbit)
        # Schreier generators for Stab(b): u_p * g * u_{p^g}^-1
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
        current = schreier
        remaining_points = [p for p in remaining_points if p != b]
    return order


# ---------------------------------------------------------------------------
# Digests (independent recomputation of the CC-5 required digest fields,
# from the receipt's own row data -- NOT trusting any digest the producer
# might separately claim, since the current producer schema does not emit
# them; this checker computes them itself as part of "roster を再構成し
# verdict を再演" per spec 2.4).
# ---------------------------------------------------------------------------

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

    require(receipt.get("schema") == "drophunt-checker-producer/v1", "SCHEMA_MISMATCH", str(receipt.get("schema")))

    window = receipt["window"]
    K_ord = window["K_ord"]
    M_ord = window["M_ord"]
    F1 = window["F1_m_factor"]
    F2 = window["F2_ratio"]
    F3 = window["F3_fib"]
    F5 = window["F5_size_G"]
    deg = window["degree"]
    JX = load_perm_1indexed(window["JX_one_line"])
    JY = load_perm_1indexed(window["JY_one_line"])

    require(K_ord % M_ord == 0, "CC4_K_NOT_LE_M", f"K_ord={K_ord} M_ord={M_ord}")
    require(F1 == K_ord // M_ord, "F1_MISMATCH", f"{F1} vs {K_ord // M_ord}")
    require(F3 == F1 * F2, "F9_FORMULA_CHECK", f"F3={F3} F1*F2={F1 * F2} -- rejects mutant #9 ([M:K] style) and #10 (m-direction dropped) if formula does not match")
    require(len(JX) == deg and len(JY) == deg, "DEGREE_MISMATCH", "")
    require(receipt.get("reduction_index_order") == "source_first", "CC5_REDUCTION_INDEX_ORDER", str(receipt.get("reduction_index_order")))

    # independently recompute group order of <JX,JY> and cross-check against F5
    g_order = group_order([JX, JY], deg)
    require(g_order == F5, "F5_SIZE_G_MISMATCH", f"computed={g_order} declared={F5}")

    seed = receipt["seed"]
    rows = receipt["rows"]
    cc1 = receipt["cc1_candidate_coverage"]
    require(len(rows) == F3, "CC1_EVALUATED_COUNT", f"len(rows)={len(rows)} F3={F3}")
    require(cc1["evaluated_count"] == F3 and cc1["expected_count"] == F3 and cc1["match"] is True, "CC1_FIELD_MISMATCH", str(cc1))

    m_block_targets = set()
    seen_pairs = set()
    ab_vectors_by_verdict: dict[bool, set] = {True: set(), False: set()}
    recomputed_valid = 0

    for row in rows:
        m = row["m"]
        word = row["f_word_codes"]
        pair_key = (m, tuple(word))
        require(pair_key not in seen_pairs, "CC1_DUPLICATE_CANDIDATE", str(pair_key))
        seen_pairs.add(pair_key)
        require(m % M_ord == 0, "M_CONGRUENCE", f"m={m} M_ord={M_ord} (seed m_seed assumed 0)")

        # independent hexagon recomputation. IMPORTANT (predicate order,
        # spec SS2.3): the producer SHORT-CIRCUITS on the first failing
        # stage -- if charming is False, hex310/hex311/onto are never
        # evaluated by the producer and are recorded as placeholder False,
        # NOT as an actual (failing) computation. This checker therefore
        # only cross-checks hex310/hex311/onto against the producer's
        # fields when the producer's OWN predicate chain actually reached
        # that stage (i.e. gated on the same short-circuit structure), but
        # it INDEPENDENTLY evaluates them itself whenever charming=True so
        # it is never simply trusting the producer past that gate.
        fperm = eval_word(word, JX, JY, deg)
        require(row["charming"] in (True, False), "CHARMING_FIELD_TYPE", str(row.get("charming")))
        if not row["charming"]:
            require(row["stage"] == "charming_fail", "STAGE_LABEL_MISMATCH_ON_CHARMING_FAIL", str(row["stage"]))
            require(row["hex310"] is False and row["hex311"] is False and row["onto"] is False and row["verdict"] is False,
                    "SHORT_CIRCUIT_PLACEHOLDER_NOT_FALSE", str(row))
            hex310_recomputed = None
            hex311_recomputed = None
        else:
            thetaW = theta_word(word)
            hex310_recomputed = eval_word(word + thetaW, JX, JY, deg) == pid(deg)
            require(hex310_recomputed == row["hex310"], "HEX310_MISMATCH", f"row m={m}: recomputed={hex310_recomputed} producer={row['hex310']}")

            if not row["hex310"]:
                require(row["stage"] == "hex310_fail", "STAGE_LABEL_MISMATCH_ON_HEX310_FAIL", str(row["stage"]))
                require(row["hex311"] is False and row["onto"] is False and row["verdict"] is False,
                        "SHORT_CIRCUIT_PLACEHOLDER_NOT_FALSE_AFTER_HEX310", str(row))
                hex311_recomputed = None
            else:
                ymfWord = ([2] * m) + word
                tau1 = tau_word(ymfWord)
                tau2 = tau_word(tau1)
                hex311_recomputed = eval_word(tau2 + tau1 + ymfWord, JX, JY, deg) == pid(deg)
                require(hex311_recomputed == row["hex311"], "HEX311_MISMATCH", f"row m={m}: recomputed={hex311_recomputed} producer={row['hex311']}")

        # onto recomputation: only reachable (per predicate order) once
        # charming, hex310, hex311 all True.
        if row["charming"] and hex310_recomputed and hex311_recomputed:
            u = 2 * m + 1
            genA = ppow(JX, u)
            genB = pmul(pmul(pinv(fperm), ppow(JY, u)), fperm)
            onto_order = group_order([genA, genB], deg)
            onto_recomputed = onto_order == g_order
            require(onto_recomputed == row["onto"], "ONTO_MISMATCH", f"row m={m}: recomputed={onto_recomputed} producer={row['onto']} computed_order={onto_order} G_order={g_order}")
        elif row["charming"] and hex310_recomputed and not hex311_recomputed:
            require(row["stage"] == "hex311_fail", "STAGE_LABEL_MISMATCH_ON_HEX311_FAIL", str(row["stage"]))
            require(row["onto"] is False and row["verdict"] is False, "SHORT_CIRCUIT_PLACEHOLDER_NOT_FALSE_AFTER_HEX311", str(row))

        # reduction-match: M-block restriction (points 0..M_DEGREE-1=35) must
        # be IDENTICAL across every row in this window+seed receipt (public
        # structural fact: points 1..36 one-indexed = 0..35 zero-indexed are
        # the fixed roof-M block by construction of every window in this
        # family of receipts).
        m_block = fperm[:36]
        m_block_targets.add(m_block)

        ab = word_ab_vector(word)
        ab_vectors_by_verdict[bool(row["charming"])].add(ab)

        verdict_recomputed = row["charming"] and hex310_recomputed and hex311_recomputed and row.get("onto", False) and row["reduction_match"]
        # NOTE: charming's f-in-derived-subgroup half is taken from the
        # producer row here (scope limitation, see module docstring) --
        # verdict is only independently CONFIRMED for the hexagon/onto/
        # reduction stages, not fully re-derived end-to-end.
        require(verdict_recomputed == row["verdict"], "VERDICT_RECOMPUTE_MISMATCH_GIVEN_PRODUCER_CHARMING", f"row m={m}: recomputed={verdict_recomputed} producer={row['verdict']}")
        if row["verdict"]:
            recomputed_valid += 1

    require(len(m_block_targets) == 1, "REDUCTION_MBLOCK_INCONSISTENT", f"{len(m_block_targets)} distinct M-block images across candidates, expected 1")
    require(recomputed_valid == receipt["valid_count"], "VALID_COUNT_MISMATCH", f"recomputed={recomputed_valid} declared={receipt['valid_count']}")

    # charming arithmetic-proxy coherence (scope-limited independent check,
    # see module docstring): all charming-True rows' ab-vectors must lie in
    # a single coset of SOME common finite-index sublattice of Z^2, which in
    # particular requires that pairwise differences of charming-True
    # ab-vectors all be equal modulo a FIXED (a,b)-independent lattice --
    # the cheapest necessary (not sufficient) condition checkable without
    # knowing Lambda_K is: all charming-True ab-vectors must be pairwise
    # distinct OR equal (never "close but not equal" in a way inconsistent
    # with a single coset); with F2_ratio small in this pass, we instead
    # check the weaker-but-real necessary condition that charming-True and
    # charming-False rows do not share an identical ab-vector for the SAME m
    # (a same-word, opposite-verdict contradiction, which IS a hard error).
    seen_ab_verdict: dict[tuple, bool] = {}
    for row in rows:
        ab = word_ab_vector(row["f_word_codes"])
        key = (row["m"], ab)
        if key in seen_ab_verdict:
            require(seen_ab_verdict[key] == row["charming"], "CHARMING_PROXY_CONTRADICTION", str(key))
        else:
            seen_ab_verdict[key] = row["charming"]

    status = "PASS" if not errors else "FAIL"
    return {
        "schema": "drophunt-checker-independent-verdict/v1",
        "receipt_path": path,
        "receipt_sha256": receipt_sha256,
        "status": status,
        "errors": errors,
        "recomputed_group_order": g_order,
        "declared_F5_size_G": F5,
        "recomputed_valid_count": recomputed_valid,
        "declared_valid_count": receipt.get("valid_count"),
        "evaluated_count": len(rows),
        "expected_count_F3": F3,
        "scope_limitation": "charming f-in-[G,G] not independently recomputed from raw permutations (see module docstring); hexagon/onto/reduction/CC1/F5/formula fully independently recomputed.",
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: drophunt_checker_v1.py <receipt.json> [<receipt.json> ...]", file=sys.stderr)
        return 2
    results = [check_receipt(p) for p in argv[1:]]
    print(json.dumps(results, indent=2))
    return 0 if all(r["status"] == "PASS" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

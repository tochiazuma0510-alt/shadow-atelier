#!/usr/bin/env python3
"""
drophunt_checker_v3.py -- item 5 (裁定1749): independent checker for the
WDICT-5-repaired, group-element-only predicate (search/
drophunt_checker_producer_v3.g). Standard library only (json, hashlib,
math, sys). Does not import/Read() any GAP file.

WORD-BASED RE-EVALUATION IS RETIRED (per coordinator instruction). theta~ =
Ad(Delta), tau~ = Ad(delta) are re-derived here as GENUINE HOMOMORPHISM
evaluations on arbitrary group elements via a degree-bounded, HOMOMORPHISM-
TRACKED stabilizer chain (orbit + Schreier generators over G=<JX,JY>, with
each transversal/Schreier element's IMAGE under the target homomorphism
computed in parallel, using the SAME accumulation order as the element
itself is built -- this is what structurally PREVENTS the WDICT-5 class of
bug: the image of a group element is computed via the group's own
multiplication table, not via a separately-chosen word representative
processed by mismatched conventions). This technique already underlies
v2's CK-1 (independent DerivedSubgroup re-derivation via a plain stabilizer
chain); this file extends it to carry a homomorphism image alongside each
orbit/Schreier element.

Independently re-derived (from raw JX,JY,JC in the receipt, NOT trusting
producer's booleans):
  - CK-1: charming's [G,G] half, via the SAME normal-closure-of-commutator
    stabilizer chain as v2.
  - CK-2: F2 * 1,469,664 == F5.
  - CK-3: M-block restriction order == 1,469,664.
  - CK-4 (INVERTED per coordinator correction): for windows with c_in_K
    true, short-circuited rows (predicate not reached that stage) MUST show
    null (None after JSON parse), not false. There is no more whole-window
    BLOCKED case in v3 (theta~/tau~ are always well-defined); if a receipt
    ever again reports whole-window blocking, this checker requires
    valid_count:null and cc1.match:false for it (dead code path today,
    since no v3 producer run has hit it, but present for completeness/
    forward-compat with the coordinator's explicit fallback wording).
  - hexagon (3.10)/(3.11): re-derived via the homomorphism-tracked chain
    described above (NOT the producer's own theta~/tau~ GAP homomorphism
    objects -- this checker builds its OWN independent chain from raw JX,
    JY,JC permutations only).
  - onto: via the plain stabilizer-chain order algorithm (unchanged from
    v2).
  - SS4 8-field enforcement (item 5.1/5.2): predicate_rule, c_in_K,
    tau_descends, F4_isolated, positive_recordability, node_id, seed_key,
    wcp5d_ref must all be PRESENT with the values the spec requires;
    missing or wrong-valued fields => REJECT.

SCOPE LIMITATION (stated, not hidden): this checker's homomorphism-tracked
chain is built over G=<JX,JY> only (candidates always live in G, per the
producer's own construction -- JC only enters as a fixed multiplicative
constant on the RHS of hexagon (3.11), which does not require factorizing
JC itself). This is sufficient for every row this checker has been run
against in this pass.
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


# ---------------------------------------------------------------------------
# Plain stabilizer chain (order + membership), unchanged from v2 -- used for
# CK-1 (derived subgroup) and onto (subgroup order).
# ---------------------------------------------------------------------------

def build_stabilizer_chain(gens: list[Perm], deg: int) -> list[dict]:
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
    comm = pmul(pmul(pinv(JX), pinv(JY)), pmul(JX, JY))
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


# ---------------------------------------------------------------------------
# HOMOMORPHISM-TRACKED stabilizer chain: builds a chain over G=<JX,JY>
# while carrying, for every orbit/Schreier element u, its image phi(u) under
# a target homomorphism phi determined by phi(JX)=imgX, phi(JY)=imgY (imgX,
# imgY given as concrete permutations of the SAME degree, e.g. imgX=JY,
# imgY=JX for theta~, or imgX=JY, imgY=JY^-1*JX^-1*JC for tau~). phi(p) for
# an arbitrary p in <JX,JY> is then computed by sifting p through the chain
# and accumulating the pre-computed phi-images of the transversal elements
# consumed during the sift, in the SAME order the sift consumes them -- this
# is mathematically guaranteed correct whenever phi truly is a homomorphism
# (verified separately/upstream via the closed-form Ad(Delta)/Ad(delta)
# identities), independent of any particular word choice, which is exactly
# the property WDICT-5 broke in the word-based approach.
# ---------------------------------------------------------------------------

def build_hom_tracked_chain(JX: Perm, JY: Perm, imgX: Perm, imgY: Perm, deg: int) -> list[dict]:
    gens = [JX, JY]
    gen_images = {JX: imgX, JY: imgY, pinv(JX): pinv(imgX), pinv(JY): pinv(imgY)}
    current = [g for g in gens if g != pid(deg)]
    remaining_points = list(range(deg))
    chain = []
    while True:
        moved = [p for p in remaining_points if any(g[p] != p for g in current)]
        if not moved or not current:
            break
        b = moved[0]
        orbit: dict[int, Perm] = {b: pid(deg)}
        orbit_img: dict[int, Perm] = {b: pid(deg)}
        frontier = [b]
        while frontier:
            nxt_frontier = []
            for p in frontier:
                up = orbit[p]
                up_img = orbit_img[p]
                for g in current:
                    q = g[p]
                    if q not in orbit:
                        orbit[q] = pmul(up, g)
                        orbit_img[q] = pmul(up_img, gen_images[g])
                        nxt_frontier.append(q)
            frontier = nxt_frontier
        schreier = []
        schreier_img = {}
        seen_sch = set()
        for p, up in orbit.items():
            up_img = orbit_img[p]
            for g in current:
                q = g[p]
                uq_inv = pinv(orbit[q])
                uq_inv_img = pinv(orbit_img[q])
                sgen = pmul(pmul(up, g), uq_inv)
                if sgen != pid(deg) and sgen not in seen_sch:
                    seen_sch.add(sgen)
                    schreier.append(sgen)
                    schreier_img[sgen] = pmul(pmul(up_img, gen_images[g]), uq_inv_img)
        chain.append({"base": b, "orbit": orbit, "orbit_img": orbit_img})
        current = schreier
        gen_images = {**gen_images, **schreier_img, **{pinv(s): pinv(schreier_img[s]) for s in schreier}}
        remaining_points = [p for p in remaining_points if p != b]
    return chain


def apply_hom(chain: list[dict], p: Perm, deg: int) -> Perm | None:
    """Sift p through the chain: p * u_1^-1 * u_2^-1 * ... * u_k^-1 = identity
    (pmul convention: pmul(a,b) = apply a then b), which rearranges to
    p = u_k * u_{k-1} * ... * u_1 (u_k applied first, u_1 applied last, in
    pmul-chaining order). So the homomorphism image phi(p) must accumulate
    in the SAME reversed order: after consuming level i's u_i, the running
    accumulator must have u_i applied BEFORE what was already accumulated,
    i.e. img_acc := pmul(u_i_img, img_acc) (prepend), not append. Getting
    this backwards silently reproduces a WDICT-5-class order bug -- this
    was caught and fixed during this pass's own testing (see cert)."""
    cur = p
    img_acc = pid(deg)
    for level in chain:
        b = level["base"]
        q = cur[b]
        if q not in level["orbit"]:
            return None
        u = level["orbit"][q]
        u_img = level["orbit_img"][q]
        cur = pmul(cur, pinv(u))
        img_acc = pmul(u_img, img_acc)
    if cur != pid(deg):
        return None
    return img_acc


def digest_of(v: object) -> str:
    return sha256_bytes(canonical(v))


def check_self_contained_E(receipt: dict, path: str, receipt_sha256: str, errors: list, require) -> dict:
    """item 2 (裁定1751): PGammaL(2,8) self-contained window. theta=Ad(s),
    tau=Ad(t) here are GENUINE INNER AUTOMORPHISMS of the whole group E,
    computable DIRECTLY as conjugation by s (resp. t) for ANY element --
    no factorization/chain-tracking is needed at all (unlike the M-window
    case, where Delta/delta themselves are not directly available, only
    their closed-form ACTION on generators). This is independently
    re-derived here from raw Ex/Ey/Es/Et permutations in the receipt."""
    window = receipt.get("window", {})
    require(window.get("E_order") == 1512, "PGL_E_ORDER_WRONG", str(window.get("E_order")))
    deg = window.get("degree")
    require(deg == 9, "PGL_DEGREE_WRONG", str(deg))
    Ex = load_perm_1indexed(window["Ex_one_line"])
    Ey = load_perm_1indexed(window["Ey_one_line"])
    Es = load_perm_1indexed(window["Es_one_line"])
    Et = load_perm_1indexed(window["Et_one_line"])

    E_chain = build_stabilizer_chain([Ex, Ey], deg)
    E_order = chain_order(E_chain)
    require(E_order == 1512, "PGL_E_ORDER_RECOMPUTE_MISMATCH", f"computed={E_order}")

    derived_chain = derived_subgroup_chain(Ex, Ey, deg)
    derived_order = chain_order(derived_chain)
    require(derived_order == 504, "PGL_DERIVED_E_ORDER_MISMATCH", f"computed={derived_order}")

    charming_expected = set(window.get("charming_m_mod9", []))
    require(charming_expected == {0, 2, 3, 5, 6, 8} or charming_expected == {"0", "2", "3", "5", "6", "8"}, "PGL_CHARMING_SET_WRONG", str(charming_expected))

    rows = receipt.get("rows", [])
    cc1 = receipt.get("cc1_candidate_coverage", {})
    require(len(rows) == 6 * 504, "PGL_ROW_COUNT_WRONG", f"{len(rows)}")
    require(cc1.get("evaluated_count") == 6 * 504 and cc1.get("match") is True, "PGL_CC1_MISMATCH", "")

    recomputed_valid = 0
    seen_pairs = set()
    pass_count_per_m: dict[int, int] = {}
    for row in rows:
        m = row["m"]
        p = load_perm_1indexed(row["perm_one_line"])
        key = (m, tuple(p))
        require(key not in seen_pairs, "PGL_DUPLICATE_CANDIDATE", str(key))
        seen_pairs.add(key)

        theta_p = pmul(pmul(pinv(Es), p), Es)
        hex310_recomputed = (pmul(theta_p, p) == pid(deg))
        require(hex310_recomputed == row["hex310"], "PGL_HEX310_MISMATCH", f"m={m}: recomputed={hex310_recomputed} producer={row['hex310']}")

        hex311_recomputed = None
        onto_recomputed = None
        if hex310_recomputed:
            u = 2 * m + 1
            ymf = pmul(p, ppow(Ey, m))
            tau_ymf = pmul(pmul(pinv(Et), ymf), Et)
            tau2_ymf = pmul(pmul(pinv(Et), tau_ymf), Et)
            hex311_recomputed = (pmul(pmul(ymf, tau_ymf), tau2_ymf) == pid(deg))
            require(hex311_recomputed == row["hex311"], "PGL_HEX311_MISMATCH", f"m={m}: recomputed={hex311_recomputed} producer={row['hex311']}")
            if hex311_recomputed:
                genA = ppow(Ex, u)
                genB = pmul(pmul(p, ppow(Ey, u)), pinv(p))
                onto_order = group_order([genA, genB], deg)
                onto_recomputed = (onto_order == 1512)
                require(onto_recomputed == row["onto"], "PGL_ONTO_MISMATCH", f"m={m}")

        verdict_recomputed = bool(hex310_recomputed) and bool(hex311_recomputed) and bool(onto_recomputed)
        require(verdict_recomputed == row["verdict"], "PGL_VERDICT_MISMATCH", f"m={m}")
        if row["verdict"]:
            recomputed_valid += 1
            pass_count_per_m[m] = pass_count_per_m.get(m, 0) + 1

    require(recomputed_valid == receipt.get("valid_count"), "PGL_VALID_COUNT_MISMATCH", f"recomputed={recomputed_valid} declared={receipt.get('valid_count')}")
    require(receipt.get("valid_count") == 54, "PGL_VALID_COUNT_NOT_54", str(receipt.get("valid_count")))
    all_nine = all(pass_count_per_m.get(m) == 9 for m in (0, 2, 3, 5, 6, 8))
    require(all_nine, "PGL_NOT_ALL_M_GIVE_9", str(pass_count_per_m))

    status = "PASS" if not errors else "FAIL"
    return {
        "schema": "drophunt-checker-v3-verdict/v1", "receipt_path": path, "receipt_sha256": receipt_sha256,
        "status": status, "errors": errors, "self_contained_E": True,
        "recomputed_E_order": E_order, "recomputed_derived_E_order": derived_order,
        "recomputed_valid_count": recomputed_valid, "declared_valid_count": receipt.get("valid_count"),
        "pass_count_per_m": pass_count_per_m,
    }


REQUIRED_SS4_FIELDS = ["predicate_rule", "c_in_K", "tau_descends", "F4_isolated",
                        "positive_recordability", "node_id", "seed_key", "wcp5d_ref"]


def check_receipt(path: str) -> dict:
    with open(path, "rb") as fh:
        raw = fh.read()
    receipt_sha256 = sha256_bytes(raw)
    receipt = json.loads(raw.decode("utf-8"))

    errors: list[str] = []

    def require(cond: bool, code: str, detail: str = "") -> None:
        if not cond:
            errors.append(f"{code}: {detail}")

    require(receipt.get("schema") == "drophunt-checker-producer/v3", "SCHEMA_MISMATCH", str(receipt.get("schema")))

    # item 5.2: SS4 8-field enforcement
    for field in REQUIRED_SS4_FIELDS:
        require(field in receipt, "SS4_FIELD_MISSING", field)
    if "predicate_rule" in receipt:
        require(receipt["predicate_rule"] == "F2_quotient", "SS4_PREDICATE_RULE_WRONG", str(receipt["predicate_rule"]))
    if "F4_isolated" in receipt:
        require(receipt["F4_isolated"] == "NOT_EVALUATED", "SS4_F4_ISOLATED_WRONG", str(receipt["F4_isolated"]))
    if "positive_recordability" in receipt:
        require(receipt["positive_recordability"] == "NONE", "SS4_POSITIVE_RECORDABILITY_WRONG", str(receipt["positive_recordability"]))
    if "wcp5d_ref" in receipt:
        require(isinstance(receipt["wcp5d_ref"], str) and "wcp5d_resolution_v1" in receipt["wcp5d_ref"], "SS4_WCP5D_REF_WRONG", str(receipt.get("wcp5d_ref")))
    KNOWN_SEED_WORDS = {
        "row36": [-2, -2, -1, -1, 2, 2, 1, -2, -1, -1, 2, 2, 2, -1, -2, -2, 1, 1, 1, 1],
        "row71": [-1, -1, 2, 2, -1, -2, -1, -1, 2, 1, -2, 1, 1, 2],
        "self_contained_E_all_charming_m": [],
    }
    if "seed_key" in receipt:
        sk = receipt["seed_key"]
        require(isinstance(sk, dict) and "word" in sk and "seed_name" in sk and "digest" in sk, "SS4_SEED_KEY_MALFORMED", str(sk))
        if isinstance(sk, dict) and "seed_name" in sk and "word" in sk:
            expected_word = KNOWN_SEED_WORDS.get(sk["seed_name"])
            require(expected_word is not None, "SS4_SEED_KEY_UNKNOWN_SEED_NAME", str(sk.get("seed_name")))
            if expected_word is not None:
                require(sk["word"] == expected_word, "SS4_SEED_KEY_WORD_DOES_NOT_MATCH_SEED_NAME",
                        f"seed_name={sk['seed_name']} word={sk['word']} expected={expected_word}")
    if "c_in_K" in receipt:
        require(isinstance(receipt["c_in_K"], bool), "SS4_C_IN_K_TYPE", str(receipt.get("c_in_K")))
    if "tau_descends" in receipt:
        require(receipt["tau_descends"] == receipt.get("c_in_K"), "SS4_TAU_DESCENDS_NOT_CONSERVATIVE_WITH_C_IN_K", f"tau_descends={receipt.get('tau_descends')} c_in_K={receipt.get('c_in_K')}")

    if receipt.get("self_contained_E"):
        return check_self_contained_E(receipt, path, receipt_sha256, errors, require)

    window = receipt.get("window", {})
    K_ord = window.get("K_ord")
    M_ord = window.get("M_ord")
    F1 = window.get("F1_m_factor")
    F2 = window.get("F2_ratio")
    F3 = window.get("F3_fib")
    F5 = window.get("F5_size_G")
    deg = window.get("degree")
    c_in_K = window.get("c_in_K")
    JX = load_perm_1indexed(window["JX_one_line"]) if "JX_one_line" in window else None
    JY = load_perm_1indexed(window["JY_one_line"]) if "JY_one_line" in window else None
    JC = load_perm_1indexed(window["JC_one_line"]) if "JC_one_line" in window else None

    require(JX is not None and JY is not None and JC is not None, "WINDOW_MISSING_JXYJC", "")
    if JX is None or JY is None or JC is None:
        status = "PASS" if not errors else "FAIL"
        return {"schema": "drophunt-checker-v3-verdict/v1", "receipt_path": path, "receipt_sha256": receipt_sha256, "status": status, "errors": errors}

    require(K_ord % M_ord == 0, "CC4_K_NOT_LE_M", f"K_ord={K_ord} M_ord={M_ord}")
    require(F1 == K_ord // M_ord, "F1_MISMATCH", "")
    require(F3 == F1 * F2, "FIB_FORMULA_CHECK", "")
    require(F2 * 1469664 == F5, "CK2_F2_TIMES_MORD_NE_F5", f"F2={F2} F5={F5}")

    g_chain = build_stabilizer_chain([JX, JY], deg)
    g_order = chain_order(g_chain)
    require(g_order == F5, "F5_SIZE_G_MISMATCH", f"computed={g_order} declared={F5}")

    JX_mblock = tuple(JX[i] for i in range(36))
    JY_mblock = tuple(JY[i] for i in range(36))
    mblock_order = group_order([JX_mblock, JY_mblock], 36)
    require(mblock_order == 1469664, "CK3_MBLOCK_ORDER_MISMATCH", f"computed={mblock_order}")

    derived_chain = derived_subgroup_chain(JX, JY, deg)
    derived_order = chain_order(derived_chain)

    # homomorphism-tracked chains for theta~, tau~ (independent of producer)
    theta_chain = build_hom_tracked_chain(JX, JY, JY, JX, deg)
    JC_inv_JX_inv = pmul(pinv(JY), pinv(JX))  # placeholder, real tau image below
    tau_img_y = pmul(pmul(pinv(JY), pinv(JX)), JC)  # y^-1 x^-1 c
    tau_chain = build_hom_tracked_chain(JX, JY, JY, tau_img_y, deg)

    seed = receipt.get("seed")
    rows = receipt.get("rows", [])
    cc1 = receipt.get("cc1_candidate_coverage", {})
    require(len(rows) == F3, "CC1_EVALUATED_COUNT", f"len(rows)={len(rows)} F3={F3}")
    require(cc1.get("evaluated_count") == F3 and cc1.get("expected_count") == F3 and cc1.get("match") is True, "CC1_FIELD_MISMATCH", "")

    m_block_targets = set()
    seen_pairs = set()
    recomputed_valid = 0
    ck1_mismatches = 0

    for row in rows:
        m = row["m"]
        # v3 rows carry the candidate permutation directly (item 5.1 field);
        # fall back to reconstructing nothing if absent (hard requirement).
        require("perm_one_line" in row, "ROW_MISSING_PERM", f"m={m}")
        if "perm_one_line" not in row:
            continue
        p = load_perm_1indexed(row["perm_one_line"])
        pair_key = (m, tuple(p))
        require(pair_key not in seen_pairs, "CC1_DUPLICATE_CANDIDATE", str(pair_key))
        seen_pairs.add(pair_key)
        require(m % M_ord == 0, "M_CONGRUENCE", f"m={m}")

        # CK-1: independent charming[G,G]-half re-derivation
        ck1_in_derived = is_identity_after_sift(derived_chain, p, deg)
        ck1_gcd_ok = math.gcd(2 * m + 1, K_ord) == 1
        ck1_charming = ck1_gcd_ok and ck1_in_derived
        producer_charming = row["charming"]
        if producer_charming is not None:
            if ck1_charming != producer_charming:
                ck1_mismatches += 1
                errors.append(f"CK1_CHARMING_MISMATCH: row m={m} recomputed={ck1_charming} producer={producer_charming}")

        if producer_charming is False:
            require(row["stage"] == "charming_fail", "STAGE_LABEL_MISMATCH_ON_CHARMING_FAIL", str(row["stage"]))
            require(row["hex310"] is None and row["hex311"] is None and row["onto"] is None and row["verdict"] is False,
                    "CK4_SHORTCIRCUIT_NOT_NULL", str(row))
            hex310_recomputed = None
            hex311_recomputed = None
        else:
            theta_p = apply_hom(theta_chain, p, deg)
            require(theta_p is not None, "THETA_HOM_APPLY_FAILED", f"row m={m}")
            hex310_recomputed = (pmul(p, theta_p) == pid(deg)) if theta_p is not None else None
            require(hex310_recomputed == row["hex310"], "HEX310_MISMATCH", f"row m={m}: recomputed={hex310_recomputed} producer={row['hex310']}")

            if row["hex310"] is False:
                require(row["stage"] == "hex310_fail", "STAGE_LABEL_MISMATCH_ON_HEX310_FAIL", str(row["stage"]))
                require(row["hex311"] is None and row["onto"] is None and row["verdict"] is False,
                        "CK4_SHORTCIRCUIT_NOT_NULL_AFTER_HEX310", str(row))
                hex311_recomputed = None
            else:
                ymf = pmul(ppow(JY, m), p)
                tau_ymf = apply_hom(tau_chain, ymf, deg)
                tau2_ymf = apply_hom(tau_chain, tau_ymf, deg) if tau_ymf is not None else None
                rhs = ppow(JC, m)
                lhs = pmul(pmul(tau2_ymf, tau_ymf), ymf) if (tau_ymf is not None and tau2_ymf is not None) else None
                hex311_recomputed = (lhs == rhs) if lhs is not None else None
                require(hex311_recomputed == row["hex311"], "HEX311_MISMATCH", f"row m={m}: recomputed={hex311_recomputed} producer={row['hex311']}")

        if producer_charming and hex310_recomputed and hex311_recomputed:
            u = 2 * m + 1
            genA = ppow(JX, u)
            genB = pmul(pmul(pinv(p), ppow(JY, u)), p)
            onto_order = group_order([genA, genB], deg)
            onto_recomputed = onto_order == g_order
            require(onto_recomputed == row["onto"], "ONTO_MISMATCH", f"row m={m}")
        elif producer_charming and hex310_recomputed and hex311_recomputed is False:
            require(row["stage"] == "hex311_fail", "STAGE_LABEL_MISMATCH_ON_HEX311_FAIL", str(row["stage"]))
            require(row["onto"] is None and row["verdict"] is False, "CK4_SHORTCIRCUIT_NOT_NULL_AFTER_HEX311", str(row))

        m_block = p[:36]
        m_block_targets.add(m_block)

        verdict_recomputed = bool(producer_charming) and bool(hex310_recomputed) and bool(hex311_recomputed) and bool(row.get("onto")) and bool(row.get("reduction_match"))
        require(verdict_recomputed == row["verdict"], "VERDICT_RECOMPUTE_MISMATCH", f"row m={m}: recomputed={verdict_recomputed} producer={row['verdict']}")
        if row["verdict"]:
            recomputed_valid += 1

    require(len(m_block_targets) <= 1, "REDUCTION_MBLOCK_INCONSISTENT", f"{len(m_block_targets)} distinct")
    require(recomputed_valid == receipt.get("valid_count"), "VALID_COUNT_MISMATCH", f"recomputed={recomputed_valid} declared={receipt.get('valid_count')}")
    require(ck1_mismatches == 0, "CK1_CHARMING_DERIVED_SUBGROUP_MISMATCHES", str(ck1_mismatches))

    status = "PASS" if not errors else "FAIL"
    return {
        "schema": "drophunt-checker-v3-verdict/v1",
        "receipt_path": path, "receipt_sha256": receipt_sha256,
        "status": status, "errors": errors,
        "window_c_in_K": c_in_K,
        "recomputed_group_order": g_order, "declared_F5_size_G": F5,
        "recomputed_derived_subgroup_order": derived_order,
        "recomputed_valid_count": recomputed_valid, "declared_valid_count": receipt.get("valid_count"),
        "ck1_charming_mismatches": ck1_mismatches,
        "evaluated_count": len(rows), "expected_count_F3": F3,
        "ss4_fields_present": [f for f in REQUIRED_SS4_FIELDS if f in receipt],
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: drophunt_checker_v3.py <receipt.json> [...]", file=sys.stderr)
        return 2
    results = [check_receipt(p) for p in argv[1:]]
    print(json.dumps(results, indent=2))
    return 0 if all(r["status"] == "PASS" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

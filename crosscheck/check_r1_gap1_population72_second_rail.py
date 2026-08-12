#!/usr/bin/env python3
"""crosscheck/check_r1_gap1_population72_second_rail.py

[R1-GAP-1] second-rail recomputation (裁定1092/1093/1094).

Role and honesty disclosure (per CV-9 discipline, 裁定1093/1094):
  This script was written by the SAME implementer who wrote the GAP producer
  (search/r1_gap1_population72_census.g), AFTER reading the mathematician's
  scratchpad scripts (scratchpad/d2gap4_census2.g etc.) and the adjudication
  note's method sections in full. It therefore does NOT satisfy the "blind
  independent design" bar needed to promote the population-72 result to
  cross-checked. A genuinely blind checker was commissioned separately
  (isolated implementer). This script's value is: (a) a second numerical
  rail in a different language (Python) using a different group-order
  algorithm (Schreier-Sims via sympy, vs GAP's internal BSGS) that can catch
  transcription/arithmetic bugs in the GAP producer, and (b) it does NOT
  import search/r1_gap1_population72_census.g or any of its intermediate
  results -- it reads only the producer's *cert* JSON (raw output), for the
  positive-control comparisons explicitly authorized by the coordinator
  (d2_gate_v1 W(P1) mon_order=324, and T18n140 block data from
  r13_p1_0_blocks_v1). It reports raw values only; no verdict language, and
  it does NOT bake in the theoretical target distribution
  {324^3, 972^9, 2916^6} anywhere in code or output (per 裁定1094: fail-closed
  comparison across the three rails -- this script, the GAP producer, and the
  independently-designed blind checker F -- is done by the coordinator).

Mathematical object (as given in r1_declaration_draft_v1.md 【R1-GAP-1】 and
the already-certified passport/target values -- NOT re-derived here):
  Degree-18 covers of P^1_t built as: fixed degree-6 base map E->P^1_t with
  local monodromy qX (at t=0, a 6-cycle) and qY (at t=1, type 2^2 1^2,
  cf. search/certs/w9_k3_p1_0d_check_v1_20260812.json), further covered in
  degree 3 by attaching a local S3 element to each of qX's 6 blocks (block i
  <-> point (i,j), j=0,1,2), subject to: full ramification (3-cycle) at the
  single point over t=0; simple ramification (transposition) at the two
  qY-fixed blocks; no ramification at the two qY-2-cycle block-pairs.
  Resolvent invariant = (sgn of local S3 element at each qY-fixed block).

Output: JSON to search/certs/r1_gap1_population72_second_rail_v1_20260813.json
(raw values only).
"""
import json
import hashlib
from math import gcd
from itertools import product

from sympy.combinatorics import Permutation, PermutationGroup

PRODUCER_CERT_PATH = "search/certs/r1_gap1_population72_v1_20260813.json"
D2GATE_CERT_PATH = "search/certs/d2_gate_v1_20260813.json"
BLOCKS_CERT_PATH = "search/certs/r13_p1_0_blocks_v1_20260812.json"
OUT_PATH = "search/certs/r1_gap1_population72_second_rail_v1_20260813.json"

N = 18


# ---------------------------------------------------------------- S3 as 0-indexed maps on {0,1,2}
ID3 = (0, 1, 2)
THREE = [(1, 2, 0), (2, 0, 1)]                    # 3-cycles
TRANSP = [(0, 2, 1), (2, 1, 0), (1, 0, 2)]        # transpositions
S3ALL = [ID3] + THREE + TRANSP


def s3_inv(p):
    r = [0, 0, 0]
    for i in range(3):
        r[p[i]] = i
    return tuple(r)


def sgn3(p):
    # a permutation of {0,1,2} with a fixed point and a 2-cycle is odd;
    # identity and 3-cycles are even
    return -1 if p in TRANSP else 1


# ---------------------------------------------------------------- generic permutation-array helpers
def compose(a, b):
    """apply a first, then b: result[i] = b[a[i]]"""
    return [b[a[i]] for i in range(len(a))]


def inverse(a):
    inv = [0] * len(a)
    for i, v in enumerate(a):
        inv[v] = i
    return inv


def perm_order(a):
    n = len(a)
    seen = [False] * n
    order = 1
    for i in range(n):
        if not seen[i]:
            j = i
            clen = 0
            while not seen[j]:
                seen[j] = True
                j = a[j]
                clen += 1
            order = order * clen // gcd(order, clen)
    return order


def cycle_type(a):
    n = len(a)
    seen = [False] * n
    lens = []
    for i in range(n):
        if not seen[i]:
            j = i
            clen = 0
            while not seen[j]:
                seen[j] = True
                j = a[j]
                clen += 1
            lens.append(clen)
    return sorted(lens)


def orbit(gens, n, start=0):
    seen = {start}
    frontier = [start]
    while frontier:
        nxt = []
        for x in frontier:
            for g in gens:
                y = g[x]
                if y not in seen:
                    seen.add(y)
                    nxt.append(y)
        frontier = nxt
    return seen


# ---------------------------------------------------------------- degree-6 base data (0-indexed)
# = qX/qY from search/certs/w9_k3_p1_0d_check_v1_20260812.json's underlying
# degree-6 quotient (also independently re-derivable from the passport
# ((18),(2^8 1^2),(18)) itself: single point of full ramification e=6 at
# t=0/t=inf, and at t=1 two points of e=1 (simple branch points of the
# degree-3 layer) plus two points of e=2). Converted here to 0-indexed arrays.
qX = [1, 2, 3, 4, 5, 0]           # 6-cycle (0 1 2 3 4 5)
qY = [0, 3, 4, 1, 2, 5]           # (1 3)(2 4) 0-indexed, fixes 0 and 5


def induce(q, alpha):
    """Build a degree-18 permutation array from base perm q (len 6) and 6
    local S3 elements alpha[0..5] (each a length-3 tuple on {0,1,2}), one per
    block. point index p(i,j) = 3*i+j."""
    out = [0] * N
    for i in range(6):
        for j in range(3):
            out[3 * i + j] = 3 * q[i] + alpha[i][j]
    return out


# ---------------------------------------------------------------- target triple (0-indexed)
# lambda_9's measured (sigma0,sigma1), quoted verbatim from
# search/certs/d2_gate_v1_20260813.json .lambda9_target_reference (1-indexed
# cycle notation there; converted here).
def perm_from_cycles_1idx(cycles, n):
    arr = list(range(n))
    for cyc in cycles:
        for a, b in zip(cyc, cyc[1:] + cyc[:1]):
            arr[a - 1] = b - 1
    return arr


LX_CYC = [[1, 11, 8, 13, 6, 15, 4, 17, 2, 10, 9, 12, 7, 14, 5, 16, 3, 18]]
LY_CYC = [[2, 9], [3, 8], [4, 7], [5, 6], [10, 17], [11, 16], [12, 15], [13, 14]]
LX = perm_from_cycles_1idx(LX_CYC, N)
LY = perm_from_cycles_1idx(LY_CYC, N)


def norm_y(X, Y):
    """Relabel points via X's cycle (X must be an 18-cycle) so X becomes the
    standard cycle (0,1,...,17); return the resulting Y'. Two triples with
    18-cycle X are conjugate respecting X iff their normalised Y's agree up
    to rotation."""
    pts = [0]
    p = 0
    for _ in range(N - 1):
        p = X[p]
        pts.append(p)
    rel = [0] * N
    for k, old in enumerate(pts):
        rel[old] = k
    out = [0] * N
    for i in range(N):
        out[rel[i]] = rel[Y[i]]
    return out


def std_power(k):
    # STD^k as an array: point i -> (i+k) mod N  (since STD sends i -> i+1 mod N)
    return [(i + k) % N for i in range(N)]


LN = norm_y(LX, LY)


def ln_class():
    cls = set()
    for k in range(N):
        s = std_power(k)
        # conjugate LN by s^k in the same sense the GAP script uses (^):
        # result[i] = s_inv(LN(s(i)))  i.e. LN^s meaning point-relabel by s
        s_inv = inverse(s)
        conj = [0] * N
        for i in range(N):
            conj[i] = s_inv[LN[s[i]]]
        cls.add(tuple(conj))
    return cls


LCLASS = ln_class()


# ---------------------------------------------------------------- minimal-block algorithm
# (standard textbook algorithm: union-find seeded by a pair (0,k), closed
# under the generators; distinct from GAP's AllBlocks implementation)
def minimal_block_containing(gens, n, a, b):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    union(a, b)
    queue = [(a, b)]
    while queue:
        x, y = queue.pop()
        for g in gens:
            gx, gy = g[x], g[y]
            if find(gx) != find(gy):
                union(gx, gy)
                queue.append((gx, gy))
    root0 = find(0)
    return frozenset(i for i in range(n) if find(i) == root0)


def all_nontrivial_block_sizes(gens, n):
    seen_blocks = set()
    for k in range(1, n):
        blk = minimal_block_containing(gens, n, 0, k)
        if 1 < len(blk) < n:
            seen_blocks.add(blk)
    sizes = sorted({len(b) for b in seen_blocks})
    return sizes, len(seen_blocks)


# ---------------------------------------------------------------- main census
def main():
    rows = []   # (res_class, mon_order, is_target_match, Xp, Yp)
    n_tot = 0
    for a6 in THREE:
        for b1 in TRANSP:
            for b6 in TRANSP:
                for b2 in S3ALL:
                    for b3 in S3ALL:
                        n_tot += 1
                        alpha = [ID3, ID3, ID3, ID3, ID3, a6]
                        beta = [b1, b2, b3, s3_inv(b2), s3_inv(b3), b6]
                        Xp = induce(qX, alpha)
                        Yp = induce(qY, beta)
                        Zp = inverse(compose(Xp, Yp))
                        if perm_order(Xp) != 18:
                            continue
                        if cycle_type(Yp) != [1, 1, 2, 2, 2, 2, 2, 2, 2, 2]:
                            continue
                        if perm_order(Zp) != 18:
                            continue
                        if len(orbit([Xp, Yp], N)) != N:
                            continue
                        G = PermutationGroup([Permutation(Xp), Permutation(Yp)])
                        mon_order = G.order()
                        is_match = tuple(norm_y(Xp, Yp)) in LCLASS
                        rows.append({
                            "res": (sgn3(b2), sgn3(b3)),
                            "mon_order": mon_order,
                            "is_target_match": is_match,
                            "Xp": Xp, "Yp": Yp,
                        })

    n_conn = len(rows)
    population_total_covers = n_conn // 6

    res_classes = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    res_sizes = {}
    mon_dist_by_class = {}
    for r in res_classes:
        sub = [row for row in rows if row["res"] == r]
        res_sizes[str(list(r))] = len(sub) // 6
        dist = {}
        for row in sub:
            dist[row["mon_order"]] = dist.get(row["mon_order"], 0) + 1
        mon_dist_by_class[str(list(r))] = {str(k): v for k, v in sorted(dist.items())}

    matched = [row for row in rows if row["is_target_match"]]
    target_match = None
    if matched:
        m = matched[0]
        gens = [m["Xp"], m["Yp"]]
        block_sizes, n_block_systems = all_nontrivial_block_sizes(gens, N)
        target_match = {
            "resolvent_class": list(m["res"]),
            "mon_order": m["mon_order"],
            "block_sizes": block_sizes,
            "nontrivial_block_systems_count_lower_bound": n_block_systems,
            "n_assignments_matched": len(matched),
        }

    # ---- positive controls (explicitly authorized: single already-certified values) ----
    d2gate = json.load(open(D2GATE_CERT_PATH, encoding="utf-8"))
    blocks_cert = json.load(open(BLOCKS_CERT_PATH, encoding="utf-8"))
    d2gate_p1_mon = d2gate["P1"]["mon_order"]
    t18n140_block_sizes = sorted(blocks_cert["block_sizes"])

    positive_control = {
        "d2_gate_v1_W_P1_mon_order": d2gate_p1_mon,
        "second_rail_matched_cover_mon_order_equal": (
            target_match is not None and target_match["mon_order"] == d2gate_p1_mon
        ),
        "t18n140_block_sizes_r13_p1_0_blocks_v1": t18n140_block_sizes,
        "second_rail_matched_cover_block_sizes_equal": (
            target_match is not None and target_match["block_sizes"] == t18n140_block_sizes
        ),
    }

    # ---- provenance ----
    script_sha256 = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
    producer_cert_sha256 = hashlib.sha256(open(PRODUCER_CERT_PATH, "rb").read()).hexdigest()

    out = {
        "schema": "d2_census_second_rail/v1",
        "generated_by": {
            "tool": "python3 + sympy (Schreier-Sims group order)",
            "script": "crosscheck/check_r1_gap1_population72_second_rail.py",
            "order": "裁定1092/1093/1094 / docs/notes/r1_declaration_draft_v1.md 【R1-GAP-1】",
            "role": "second rail (same implementer as the GAP producer, written AFTER reading the "
                     "mathematician's method sections -- NOT a blind independent checker; does not "
                     "by itself justify promotion to cross-checked; a separately-commissioned blind "
                     "checker (implementer F) is the independence claim)",
        },
        "raw_assignment_count": n_tot,
        "connected_assignment_count": n_conn,
        "gauge_orbit_size": 6,
        "population_total_covers": population_total_covers,
        "resolvent_class_sizes_covers": res_sizes,
        "mon_order_distribution_by_class": mon_dist_by_class,
        "target_match": target_match,
        "positive_control": positive_control,
        "u_touched": False,
        "c_touched": False,
        "prereg_quantities_computed": False,
        "d_no_interpretation": "machine values only; verdict は司令塔",
        "provenance": {
            "script_sha256": script_sha256,
            "producer_cert_sha256_read": producer_cert_sha256,
        },
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    print("[raw] total gauge assignments tested =", n_tot)
    print("[raw] passport-passing & connected   =", n_conn, " (/6 =", population_total_covers, "covers)")
    print("[raw] resolvent class sizes (covers) =", res_sizes)
    print("[raw] |Mon| distribution by class    =", mon_dist_by_class)
    print("[raw] target_match                   =", target_match)
    print("[raw] positive_control                =", positive_control)
    print("\nwrote", OUT_PATH)
    print("script sha256 =", script_sha256)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C1'(S4)+P5' クロスレビュー — 数学者(Claude)の独立第三系統。

Sol の producer / checker のコードは import しない。sympy も使わない。
置換は 0..8 上の tuple、合成は **左から右**((a*b)[i] = b[a[i]])で
Sol の cert と同じ規約に揃える(cert の explicit_XYZ で数値確認済)。

検査項目
  T1 商 Nielsen 類: passport (3^3,3^3,(9))・第3分岐巡回を固定した全解と生成群位数分布
  T2 生成部分群が位数ごとに何個あるか(集合として)
  T3 S9 全走査による normalizer / centralizer と型 (7,1,1) の有無
  T4 240*168 = 8! の incidence 勘定
  T5 P の 3-推移性(sharply)= PSL(2,8) の独立同定
  T6 固定 Z の W-dessin: 54 解 / <Z>-軌道 6 個 / 対角ちょうど 1 個
  T7 cert の explicit_XYZ が XYZ=1・全て 9-巡回・同一 P-類(=対角)であること
  T8 kernel word 復元 rx=(qb qa)^-1, ry=(qa qb)^-1, rz=(rx ry)^-1 が
     qa:=A, qb:=x^-1 A^-1 の定義から**恒等的に**従うか(=独立情報を持たないか)
"""
import itertools
import json
import sys
from collections import Counter

N = 9
ID = tuple(range(N))


def mul(a, b):
    """左から右: 先に a、次に b。 (a*b)[i] = b[a[i]]"""
    return tuple(b[a[i]] for i in range(N))


def inv(a):
    r = [0] * N
    for i, v in enumerate(a):
        r[v] = i
    return tuple(r)


def conj(a, g):
    """g^-1 a g (左右規約に依らず「g で共役」)"""
    return mul(mul(inv(g), a), g)


def ctype(p):
    seen = set()
    out = []
    for i in range(N):
        if i in seen:
            continue
        j, l = i, 0
        while j not in seen:
            seen.add(j)
            l += 1
            j = p[j]
        out.append(l)
    return tuple(sorted(out, reverse=True))


def closure(gens):
    """生成する部分群を BFS で列挙"""
    G = {ID}
    frontier = [ID]
    while frontier:
        nxt = []
        for a in frontier:
            for g in gens:
                b = mul(a, g)
                if b not in G:
                    G.add(b)
                    nxt.append(b)
        frontier = nxt
    return frozenset(G)


ALL_S9 = None


def all_s9():
    global ALL_S9
    if ALL_S9 is None:
        ALL_S9 = [tuple(p) for p in itertools.permutations(range(N))]
    return ALL_S9


def normalizer_data(gens, G):
    """S9 全走査。gens で判定(g s g^-1 in G for all s)"""
    n_ord = 0
    c_ord = 0
    has711 = False
    for g in all_s9():
        cj = tuple(conj(s, g) for s in gens)
        if all(c in G for c in cj):
            n_ord += 1
            if not has711 and ctype(g) == (7, 1, 1):
                has711 = True
        if cj == tuple(gens):
            c_ord += 1
    return {"order": n_ord, "centralizer_order": c_ord, "contains_cycle_type_7_1_1": has711}


def orbits_under(pairs, z):
    """<z>-共役による軌道分解"""
    pool = set(pairs)
    orbs = []
    zs = [ID]
    for _ in range(8):
        zs.append(mul(zs[-1], z))
    while pool:
        p = next(iter(pool))
        orb = set()
        for g in zs:
            orb.add((conj(p[0], g), conj(p[1], g)))
        pool -= orb
        orbs.append(orb)
    return orbs


def main():
    out = {}

    # ---- 固定 9-巡回 C0 = (0 1 2 3 4 5 6 7 8) ----
    C0 = tuple((i + 1) % N for i in range(N))
    assert ctype(C0) == (9,)

    # ---- T1 商 Nielsen 類 ----
    order3 = [p for p in all_s9() if ctype(p) == (3, 3, 3)]
    C0inv = inv(C0)
    sols = []
    for A in order3:
        B = mul(inv(A), C0inv)          # A*B = C0^-1  <=>  A*B*C0 = 1
        if ctype(B) != (3, 3, 3):
            continue
        G = closure([A, B])
        sols.append((A, B, len(G), G))
    dist = Counter(s[2] for s in sols)
    out["T1_order3_element_count_S9"] = len(order3)
    out["T1_solution_count_fixed_C"] = len(sols)
    out["T1_distribution"] = dict(sorted(dist.items()))

    # ---- T2 位数ごとの相異なる生成部分群 ----
    uniq = {}
    for o in sorted(dist):
        uniq[o] = len({s[3] for s in sols if s[2] == o})
    out["T2_unique_subgroups_by_order"] = uniq

    # ---- T3 normalizer / centralizer ----
    reps = {}
    for o in sorted(dist):
        reps[o] = next(s for s in sols if s[2] == o)
    norm = {}
    for o in sorted(dist):
        A, B, _, G = reps[o]
        norm[o] = normalizer_data([A, B], G)
    out["T3_normalizers_in_S9"] = norm

    P = reps[504][3]
    assert C0 in P

    # ---- T4 incidence 勘定 ----
    fact9 = 362880
    NP = norm[504]["order"]
    copies = fact9 // NP
    ord9_in_P = [g for g in P if ctype(g) == (9,)]
    out["T4"] = {
        "index_S9_over_NP": copies,
        "order9_elements_in_P": len(ord9_in_P),
        "product": copies * len(ord9_in_P),
        "nine_cycles_in_S9_8fact": 40320,
        "incidence_per_nine_cycle": copies * len(ord9_in_P) // 40320,
        "exact": copies * len(ord9_in_P) == 40320,
    }

    # ---- T5 P の sharp 3-transitivity(= PSL(2,8) の独立同定) ----
    triples = set()
    base = (0, 1, 2)
    for g in P:
        triples.add((g[0], g[1], g[2]))
    out["T5"] = {
        "P_order": len(P),
        "distinct_images_of_ordered_triple_012": len(triples),
        "num_ordered_triples_9_8_7": 9 * 8 * 7,
        "sharply_3_transitive": len(triples) == 9 * 8 * 7 == len(P),
    }

    # ---- P-共役類(位数 9)----
    def pclass(g):
        return frozenset(conj(g, h) for h in P)

    classes = []
    for g in ord9_in_P:
        if not any(g in c for c in classes):
            classes.append(pclass(g))
    out["T5_order9_classes"] = {"count": len(classes), "sizes": sorted(len(c) for c in classes)}

    # ---- T6 固定 Z=C0 の W-dessin ----
    wsol = []
    for X in ord9_in_P:
        Y = mul(inv(X), C0inv)          # X*Y*C0 = 1
        if ctype(Y) == (9,) and Y in P and closure([X, Y]) == P:
            wsol.append((X, Y))
    worb = orbits_under(wsol, C0)
    czero = next(c for c in classes if C0 in c)
    diag = [(o and True) for o in
            [all(p in czero for p in (next(iter(sorted(ob)))[0], next(iter(sorted(ob)))[1]))
             for ob in worb]]
    out["T6"] = {
        "fixed_Z_solution_count": len(wsol),
        "orbit_count": len(worb),
        "orbit_sizes": sorted(len(o) for o in worb),
        "diagonal_orbit_count": sum(diag),
    }

    # ---- T7 cert の explicit_XYZ を独立に検算 ----
    cert = json.load(open("search/certs/c1prime_s4_p5prime_v1_20260813.json", encoding="utf-8"))
    X, Y, Z = [tuple(a) for a in cert["window_binding"]["explicit_XYZ_array_form"]]
    Pc = closure([X, Y])
    cz = frozenset(conj(Z, h) for h in Pc)
    out["T7"] = {
        "XYZ_product_is_identity_left_to_right": mul(mul(X, Y), Z) == ID,
        "cycle_types": [ctype(X), ctype(Y), ctype(Z)],
        "group_order": len(Pc),
        "same_class": (X in cz) and (Y in cz) and (Z in cz),
        "class_size_of_Z": len(cz),
        "order9_count": len([g for g in Pc if ctype(g) == (9,)]),
    }

    # ---- T8 kernel word 復元は恒等式か(自由群での形式検査) ----
    # qa := A, qb := x^-1 * A^-1 と置いたとき
    #   qa*qb = A * x^-1 * A^-1
    #   rx := (qb*qa)^-1 = (x^-1 A^-1 A)^-1 = x        <- 恒等的に x
    #   ry := (qa*qb)^-1 = A x A^-1                    <- 定義上 y と置いたもの
    #   rz := (rx ry)^-1 = (x y)^-1 = z  (x y z = 1 より)
    # 自由群で語簡約して検査する(生成元 A, x の自由群)。
    def red(w):
        s = []
        for c in w:
            if s and s[-1][0] == c[0] and s[-1][1] == -c[1]:
                s.pop()
            else:
                s.append(c)
        return tuple(s)

    def winv(w):
        return red(tuple((c[0], -c[1]) for c in reversed(w)))

    def wmul(*ws):
        r = ()
        for w in ws:
            r = red(r + w)
        return r

    A_ = (("A", 1),)
    x_ = (("x", 1),)
    qa = A_
    qb = wmul(winv(x_), winv(A_))
    rx = winv(wmul(qb, qa))
    ry = winv(wmul(qa, qb))
    y_expected = wmul(A_, x_, winv(A_))
    out["T8"] = {
        "rx_equals_x_as_free_word": rx == x_,
        "ry_equals_AxAinv_as_free_word": ry == y_expected,
        "note": "rx, ry は qa,qb の定義から自由群で恒等的に従う(独立情報なし)",
    }

    print(json.dumps(out, ensure_ascii=False, indent=1, default=lambda o: list(o)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

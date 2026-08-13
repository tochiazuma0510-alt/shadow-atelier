#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A/B 判定計器の盲目性判定 — 数学者(Claude)独立計算。

(1) A_arith の Goursat データ: GT(M) = GT(K^(9)) x_U GT(N_S4) の中で
    A_arith は「両因子へ全射・指数 3」= 真の subdirect 部分群。
    ⟹ Goursat の共通商は位数 18。その群を数論側から独立に同定する。
(2) 共通商 Gal(Q(zeta_9, 2^(1/3))/Q) の構造(位数 18・非可換・[Q,Q]=C_3)。
(3) ★ gating: G_l = PB_3/K^(l) が S_3 を商に持つか(非可換 3-橋の可否)。
    G_l は正典 Thm 4.3 の marked dihedral triple 群として 3l 点上に構成。
    hom G_l -> S_3 の存在は「G_l x S_3 内の <(x,a),(y,b)> が graph か」で判定。
"""
import itertools
import json
import math
import sys


# ---------- 一般の置換ユーティリティ(0-origin tuple・左から右) ----------
def mul(a, b):
    return tuple(b[a[i]] for i in range(len(a)))


def inv(a):
    r = [0] * len(a)
    for i, v in enumerate(a):
        r[v] = i
    return tuple(r)


def comm(a, b):
    return mul(mul(inv(a), inv(b)), mul(a, b))


def closure(gens, ident):
    G = {ident}
    fr = [ident]
    while fr:
        nx = []
        for a in fr:
            for g in gens:
                c = mul(a, g)
                if c not in G:
                    G.add(c)
                    nx.append(c)
        fr = nx
    return G


def derived(G, gens, ident):
    """[G,G] = <[g,h] : g,h in G> (生成元との交換子で十分だが安全側で全対の一部を使う)"""
    cs = set()
    Gl = list(G)
    for g in Gl:
        for h in gens:
            cs.add(comm(g, h))
    return closure(list(cs) | {ident} if False else list(cs) + [ident], ident)


# ---------- G_l = PB_3/K^(l) の構成(正典 Thm 4.3 の marked dihedral triple) ----------
def make_gl(n):
    """3n 点上。各ブロックに二面体群 D_n(r=回転, s=反転)を置き
       x = (r, s, s), y = (sr, r, sr) を生成元とする。"""
    tot = 3 * n
    def blk(p, i):
        arr = list(range(tot))
        for j in range(n):
            arr[i * n + j] = i * n + p[j]
        return tuple(arr)
    r = tuple((j + 1) % n for j in range(n))
    s = tuple((-j) % n for j in range(n))
    sr = mul(s, r)
    x = mul(mul(blk(r, 0), blk(s, 1)), blk(s, 2))
    y = mul(mul(blk(sr, 0), blk(r, 1)), blk(sr, 2))
    return x, y, tuple(range(tot))


# ---------- S_3 ----------
S3 = [tuple(p) for p in itertools.permutations(range(3))]
ID3 = (0, 1, 2)


def has_S3_quotient(x, y, ident, Gsize):
    """hom G=<x,y> ->> S_3 が存在するか。
       (x,a),(y,b) が G x S_3 で生成する部分群 H を作り
       |H| = |G| (= graph = well-defined hom) かつ <a,b> = S_3 なら全射 hom。"""
    found = []
    for a in S3:
        for b in S3:
            if len(closure([a, b], ID3)) != 6:
                continue
            gens = [(x, a), (y, b)]
            e = (ident, ID3)
            H = {e}
            fr = [e]
            ok = True
            while fr:
                nx = []
                for u in fr:
                    for g in gens:
                        v = (mul(u[0], g[0]), mul(u[1], g[1]))
                        if v not in H:
                            H.add(v)
                            nx.append(v)
                            if len(H) > Gsize:
                                ok = False
                                break
                    if not ok:
                        break
                if not ok:
                    break
                fr = nx
            if ok and len(H) == Gsize:
                found.append((a, b))
    return found


def main():
    out = {}

    # ---- (2) 共通商 Gal(Q(zeta_9, 2^(1/3))/Q) を置換群として構成し構造を読む ----
    # Gal = C_6 x_{C_2} S_3 (= Gal(Q(zeta_9)/Q) と Gal(Q(zeta_3,2^(1/3))/Q) の
    #        Q(zeta_3) 上のファイバー積)。位数 18。
    # C_6 = <c> を 6 点上、S_3 を 3 点上に置き、両者の C_2 商が一致する対を取る。
    C6 = tuple((j + 1) % 6 for j in range(6))
    def c6_to_c2(k):      # C_6 -> C_2 (mod 2)
        return k % 2
    pairs = []
    C6el = closure([C6], tuple(range(6)))
    # C_6 の元を「べき指数」で持つ
    powers = {}
    cur = tuple(range(6))
    for k in range(6):
        powers[cur] = k
        cur = mul(cur, C6)
    for g in C6el:
        for h in S3:
            sgn = 0 if h in (ID3, (1, 2, 0), (2, 0, 1)) else 1     # A_3 か否か
            if c6_to_c2(powers[g]) == sgn:
                pairs.append((g, h))
    Q = set(pairs)
    # Q の生成元と交換子部分群
    qgens = [g for g in Q]
    def qmul(u, v):
        return (mul(u[0], v[0]), mul(u[1], v[1]))
    qid = (tuple(range(6)), ID3)
    qcomm = set()
    for u in Q:
        for v in Q:
            a = qmul(qmul((inv(u[0]), inv(u[1])), (inv(v[0]), inv(v[1]))), qmul(u, v))
            qcomm.add(a)
    # [Q,Q] の閉包
    D = {qid}
    fr = [qid]
    while fr:
        nx = []
        for a in fr:
            for g in qcomm:
                b = qmul(a, g)
                if b not in D:
                    D.add(b)
                    nx.append(b)
        fr = nx
    abelian = all(qmul(u, v) == qmul(v, u) for u in Q for v in Q)
    out["共通商 Gal(Q(zeta9,2^(1/3))/Q)"] = {
        "|Q|": len(Q),
        "可換か": abelian,
        "|[Q,Q]|": len(D),
        "|Q^ab|": len(Q) // len(D),
        "★ 絡み C_3 は [Q,Q] に住むか": len(D) == 3,
        "Q^ab は U=(Z/18)^x ~ C_6 と同位数か": len(Q) // len(D) == 6,
    }

    # ---- (1) A_arith の Goursat 指数勘定(整数のみ) ----
    gt_k9, gt_s4, u_ord = 108, 54, 6
    gt_m = gt_k9 * gt_s4 // u_ord
    d9, ds4, r = 9, 9, 3
    a_arith = 12 * d9 * ds4 // r
    out["Goursat 勘定"] = {
        "|GT(K^(9))|": gt_k9, "|GT(N_S4)|": gt_s4, "|U|": u_ord, "|GT(M)|": gt_m,
        "|A_arith| = 12 d9 dS4 / r": a_arith,
        "[GT(M):A_arith]": gt_m // a_arith,
        "A_arith -> GT(K^(9)) の像 = 12 d9": 12 * d9,
        "全射か(=|GT(K^(9))|)": 12 * d9 == gt_k9,
        "A_arith -> GT(N_S4) の像 = 6 dS4": 6 * ds4,
        "全射か(=|GT(N_S4)|)": 6 * ds4 == gt_s4,
        "★ A_arith は真の subdirect(両因子全射・指数3)": (12 * d9 == gt_k9) and (6 * ds4 == gt_s4) and gt_m // a_arith == 3,
        "[GT(K^(9)) x GT(N_S4) : A_arith] = 共通商の位数": gt_k9 * gt_s4 // a_arith,
    }

    # ---- (3) ★ gating: G_l が S_3 を商に持つか ----
    levels = [int(v) for v in (sys.argv[1:] or ["9", "36", "45"])]
    tab = {}
    for l in levels:
        x, y, ident = make_gl(l)
        G = closure([x, y], ident)
        n = len(G)
        Dg = derived(G, [x, y], ident)
        gab = n // len(Dg)
        # [D,D]
        dcs = set()
        Dl = list(Dg)
        for g in Dl:
            for h in Dl[: min(len(Dl), 60)]:
                dcs.add(comm(g, h))
        D2 = closure(list(dcs) + [ident], ident)
        dab = len(Dg) // len(D2)
        three = 0
        t = dab
        while t % 3 == 0:
            t //= 3
            three += 1
        homs = has_S3_quotient(x, y, ident, n)
        tab[l] = {
            "|G_l|": n,
            "4l^3 or 4(l/2)^3": 4 * l ** 3 if l % 2 else 4 * (l // 2) ** 3,
            "|G_l^ab|": gab,
            "|[G,G]^ab|": dab,
            "[G,G]^ab の 3-指数": three,
            "★ S_3 商の個数": len(homs),
            "★ S_3 を商に持つか": len(homs) > 0,
        }
    out["gating: G_l ->> S_3"] = tab
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

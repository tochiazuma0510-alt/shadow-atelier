#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A/B 判定計器の盲目性 — 絡み座標の同定(数学者 Claude・独立計算)。

模型(正典 Thm 4.6 / surj_s4_v2 §1 の構造から):
  GT(K^(9)) = Aff(Z/9) x C_2                      位数 108
  GT(N_S4)  = Hol(Z/9) = Aff(Z/9)                 位数  54
  U         = (Z/18)^x = (Z/9)^x = C_6            位数   6
  GT(M)     = GT(K^(9)) x_U GT(N_S4)              位数 972
元 = (t1, t2, u, e),  t_i in Z/9,  u in (Z/9)^x,  e in Z/2
積  (t1,t2,u,e)*(t1',t2',u',e') = (t1+u t1', t2+u t2', u u', e+e')

検査:
 T1 位数・交換子群・可換化
 T2 A_arith の Goursat 勘定(指数 3・両因子全射 ⟹ 共通商の位数 18)
 T3 共通商 Q0 = Gal(Q(zeta_9, 2^(1/3))/Q) の構造(位数 18・非可換・[Q0,Q0]=C_3・Q0^ab=C_6)
 T4 (Z/9)^2 の指数 3 部分群 4 個 = P^1(F_3) の 4 直線。退化 2 / 対角 2
 T5 各直線から作る指数 3 部分群の位数・正規性
 T6 GT(M) ->> S_3 の存在(= 非正規指数 3 部分群の存在)
 T7 絡み座標 delta(t) = k_dih - eps*k_S4 mod 3 の 3 値分布
"""
import itertools
import json

N = 9
UNITS = [u for u in range(1, 9) if u % 3 != 0]      # (Z/9)^x, |U| = 6


def elts():
    for t1 in range(N):
        for t2 in range(N):
            for u in UNITS:
                for e in (0, 1):
                    yield (t1, t2, u, e)


def mul(a, b):
    return ((a[0] + a[2] * b[0]) % N, (a[1] + a[2] * b[1]) % N,
            (a[2] * b[2]) % N, (a[3] + b[3]) % 2)


def inv(a):
    ui = next(v for v in UNITS if (a[2] * v) % N == 1)
    return ((-ui * a[0]) % N, (-ui * a[1]) % N, ui, (-a[3]) % 2)


def comm(a, b):
    return mul(mul(inv(a), inv(b)), mul(a, b))


ID = (0, 0, 1, 0)


def closure(gens):
    G = {ID}
    fr = [ID]
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


def main():
    out = {}
    G = list(elts())
    Gs = set(G)
    out["T1"] = {"|GT(M)|": len(G)}

    # 交換子部分群
    cs = {comm(a, b) for a in G for b in G}
    D = closure(list(cs))
    out["T1"]["|[GT(M),GT(M)]|"] = len(D)
    out["T1"]["|GT(M)^ab|"] = len(G) // len(D)
    out["T1"]["[G,G] は (Z/9)^2 (u=1,e=0 の層) か"] = (
        len(D) == 81 and all(d[2] == 1 and d[3] == 0 for d in D))

    # T2 Goursat 勘定
    gt1, gt2, u_ord = 108, 54, 6
    a_ar = 12 * 9 * 9 // 3
    out["T2"] = {
        "|GT(M)|": gt1 * gt2 // u_ord, "|A_arith|": a_ar,
        "[GT(M):A_arith]": (gt1 * gt2 // u_ord) // a_ar,
        "A_arith->GT(K^(9)) の像 12*d9": 12 * 9, "全射": 12 * 9 == gt1,
        "A_arith->GT(N_S4) の像 6*dS4": 6 * 9, "全射": 6 * 9 == gt2,
        "★ Goursat 共通商の位数 = |GT1||GT2|/|A|": gt1 * gt2 // a_ar,
    }

    # T3 Q0 = Gal(Q(zeta_9, 2^(1/3))/Q) = C_6 x_{C_2} S_3  を (s,u) で実現:
    #    s in Z/3 (Kummer), u in (Z/9)^x, 作用は u mod 3 (= +-1)
    Q = [(s, u) for s in range(3) for u in UNITS]
    def qmul(a, b):
        return ((a[0] + (a[1] % 3) * b[0]) % 3, (a[1] * b[1]) % N)
    def qinv(a):
        ui = next(v for v in UNITS if (a[1] * v) % N == 1)
        return ((-(ui % 3) * a[0]) % 3, ui)
    qid = (0, 1)
    qcs = {qmul(qmul(qinv(a), qinv(b)), qmul(a, b)) for a in Q for b in Q}
    QD = {qid}
    fr = [qid]
    while fr:
        nx = []
        for a in fr:
            for g in qcs:
                c = qmul(a, g)
                if c not in QD:
                    QD.add(c)
                    nx.append(c)
        fr = nx
    out["T3"] = {
        "|Q0|": len(Q),
        "可換か": all(qmul(a, b) == qmul(b, a) for a in Q for b in Q),
        "|[Q0,Q0]|": len(QD),
        "|Q0^ab|": len(Q) // len(QD),
        "★ 絡み C_3 は [Q0,Q0] に住む": len(QD) == 3,
        "★ Q0^ab = U (位数 6)": len(Q) // len(QD) == 6,
    }

    # T4 (Z/9)^2 の指数 3 部分群 = mod 3 の直線 (alpha:beta) in P^1(F_3)
    lines = [(1, 0), (0, 1), (1, 1), (1, 2)]
    out["T4"] = {"直線の個数": len(lines),
                 "退化(一方の座標のみ)": [l for l in lines if 0 in l],
                 "★ 対角(両座標を結合)": [l for l in lines if 0 not in l]}

    # T5 各直線 W から H = {g : alpha*t1 + beta*t2 = 0 mod 3} を作る
    t5 = {}
    for (al, be) in lines:
        H = {g for g in G if (al * g[0] + be * g[1]) % 3 == 0}
        # 部分群か
        issub = all(mul(a, b) in H for a in list(H)[:200] for b in list(H)[:200])
        # 正規性
        isnorm = all(mul(mul(inv(x), h), x) in H for x in G[:400] for h in list(H)[:40])
        t5[f"({al}:{be})"] = {"|H|": len(H), "指数": len(G) // len(H),
                              "部分群(標本検査)": issub, "正規か": isnorm,
                              "型": "退化" if 0 in (al, be) else "★対角"}
    out["T5"] = t5

    # T6 GT(M) ->> S_3 (対角直線の H が非正規 ⟹ 3 剰余類への作用が S_3 を与える)
    S3 = [tuple(p) for p in itertools.permutations(range(3))]
    def s3mul(a, b):
        return tuple(b[a[i]] for i in range(3))
    found = 0
    for (al, be) in lines:
        H = {g for g in G if (al * g[0] + be * g[1]) % 3 == 0}
        cosets = []
        rem = set(G)
        while rem:
            x = next(iter(rem))
            c = frozenset(mul(x, h) for h in H)
            cosets.append(c)
            rem -= c
        if len(cosets) != 3:
            continue
        img = set()
        for g in G:
            perm = []
            for c in cosets:
                y = mul(g, next(iter(c)))
                perm.append(next(i for i, d in enumerate(cosets) if y in d))
            img.add(tuple(perm))
        if len(img) == 6:
            found += 1
    out["T6"] = {"S_3 像を与える直線の個数": found,
                 "★ GT(M) ->> S_3 は存在するか": found > 0}

    # T7 絡み座標 delta の 3 値分布(対角直線 (1:-1) = (1:2))
    for (al, be) in [(1, 2), (1, 1)]:
        dist = {0: 0, 1: 0, 2: 0}
        for g in G:
            dist[(al * g[0] + be * g[1]) % 3] += 1
        out.setdefault("T7", {})[f"delta=({al}:{be})"] = {
            "分布": dist, "0 の個数": dist[0], "= 324 か": dist[0] == 324}

    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

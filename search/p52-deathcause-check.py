#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p52-deathcause-check.py
=======================
P5-2「744 全滅の死因の定理化」の機械突合器。

docs/notes/p52_deathcause_v1.md の補題 L1-L4・定理 D・命題 MIN・命題 MIN0 を
search/certs/ep_sweep744_20260801.json の実測 744 点と、独立な有限探索とで
突合する。

規律
----
* 単系統(python・純 Fraction 演算)。工房の lane A/B のコードは import しない
  (述語は spec v19 §2/§3 と Prop S5-3infty の条文から独立に再実装した)。
  よって本スクリプトの結果は cross-checked ではない — 単系統の突合である。
* 封印非接触: \\hat c_mu は封印 3 量の一つ。本ファイルは \\hat c_mu の値・符号・
  平方類、および f6 の係数を一切出力しない。出すのは真偽値のみ。
  Prop S5-3infty が公開で述べる述語「\\hat c_mu != 0」だけを使う。
* 事前登録: 本スクリプトは探索器ではない。§2/§3 の有限探索は「定理の証明の
  中で現れる有限場合分けの機械確認」であり、N_infty 宇宙の拡大走査ではない
  (窓は Cauchy 根界から導いた証明の一部・下の RIGOROUS WINDOW 参照)。

使い方:  python search/p52-deathcause-check.py
終了コード 0 = 全検査 PASS。
"""
import json
import os
import sys
from collections import Counter
from fractions import Fraction as F

# Windows の cp932 コンソールでも日本語出力が壊れないようにする
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ----------------------------------------------------------------------
# 多項式ユーティリティ(昇冪係数リスト・要素は Fraction)
# ----------------------------------------------------------------------
def trim(u):
    u = list(u)
    while u and u[-1] == 0:
        u.pop()
    return u


def deg(u):
    return len(trim(u)) - 1          # 零多項式は -1


def mul(u, v):
    u, v = trim(u), trim(v)
    if not u or not v:
        return []
    r = [F(0)] * (len(u) + len(v) - 1)
    for i, a in enumerate(u):
        if a == 0:
            continue
        for j, b in enumerate(v):
            r[i + j] += a * b
    return trim(r)


def sub(u, v):
    n = max(len(u), len(v))
    r = [F(0)] * n
    for i, a in enumerate(u):
        r[i] += a
    for i, b in enumerate(v):
        r[i] -= b
    return trim(r)


def scal(u, c):
    return trim([c * a for a in u])


def divmod_poly(u, v):
    u, v = trim(u), trim(v)
    assert v, "division by zero polynomial"
    q = [F(0)] * max(1, len(u) - len(v) + 1)
    r = list(u)
    dv, lv = len(v) - 1, v[-1]
    while trim(r) and len(trim(r)) - 1 >= dv:
        r = trim(r)
        k = len(r) - 1 - dv
        c = r[-1] / lv
        q[k] += c
        r = sub(r, [F(0)] * k + [c * x for x in v])
    return trim(q), trim(r)


def der(u):
    return trim([u[i] * i for i in range(1, len(u))])


def gcd_poly(u, v):
    u, v = trim(u), trim(v)
    while v:
        _, r = divmod_poly(u, v)
        u, v = v, r
    return scal(u, F(1) / u[-1]) if u else u      # monic 正規化


def rootpart(u):
    """u の \\bar Q 上の根の重複度の多重集合(降順 tuple)。"""
    u = trim(u)
    parts, k = [], 1
    g = gcd_poly(u, der(u))
    a, _ = divmod_poly(u, g)
    b = g
    while deg(a) > 0:
        c = gcd_poly(a, b)
        m, _ = divmod_poly(a, c)
        if deg(m) > 0:
            parts += [k] * deg(m)
        b, _ = divmod_poly(b, c)
        a = c
        k += 1
    return tuple(sorted(parts, reverse=True))


def inf_norm(u):
    return max(abs(x) for x in u) if u else F(0)


# ----------------------------------------------------------------------
# stage 1 述語(Prop S5-3infty・searcher の factorCheckNinfty と同じ条文を
# 独立実装。値は返さない — 真偽と理由文字列のみ)
# ----------------------------------------------------------------------
def stage1(A, P, require_depressed=True):
    """A = a/a5 (monic quintic), P = p/p2 (monic quadratic) に対し
    A^2 - f6 P^2 = const != 0 / f6 monic (depressed) squarefree deg6 を検査。"""
    f6, r = divmod_poly(mul(A, A), mul(P, P))
    if deg(f6) != 6 or f6[6] != 1:
        return False, "f6 not monic deg 6"
    if require_depressed and len(f6) > 5 and f6[5] != 0:
        return False, "f6 not depressed (Rule1 M1 gauge)"
    if deg(r) > 0:
        return False, "remainder not constant (Pell fails)"
    if not r or r[0] == 0:
        return False, "c_hat = 0"
    if deg(gcd_poly(f6, der(f6))) > 0:
        return False, "f6 not squarefree"
    return True, "stage1 PASS"


# ======================================================================
# PART 1 : 744 点との突合
# ======================================================================
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERT = os.path.join(ROOT, "search", "certs", "ep_sweep744_20260801.json")

E3_CODE = "precondition/leading-coeff-mismatch"     # reject_priority [4]
T1_CODE = "a-partition-mismatch"                    # reject_priority [8]

fails = []


def check(name, cond, ctx=""):
    if not cond:
        fails.append(f"{name} {ctx}")


def part1():
    cert = json.load(open(CERT, encoding="utf-8"))
    pts = cert["points"]
    check("cert-size", len(pts) == 744, f"got {len(pts)}")

    rp_dist, A4_dist, stat = Counter(), Counter(), Counter()
    cal_bad = 0

    for pt in pts:
        gi = pt["global_index"]
        cd = pt["candidate"]
        a = [F(int(t)) for t in cd["a"]]
        p = [F(int(t)) for t in cd["p"]]
        a5, p2 = a[5], p[2]

        # --- L1 : stage 1 は a5^2 = p2^2 = 1 を強制する -------------------
        check("L1", a5 * a5 == 1 and p2 * p2 == 1, f"@{gi}")

        A = scal(a, F(1) / a5)
        P = scal(p, F(1) / p2)

        # --- 較正: 独立実装の stage1 述語が既知 744 生存者を全採択するか ----
        ok, _ = stage1(A, P, require_depressed=True)
        if not ok:
            cal_bad += 1

        # --- L2 : depressed gauge  ==>  a4/a5 = p1/p2 ---------------------
        check("L2", A[4] == P[1], f"@{gi} A4={A[4]} P1={P[1]}")

        # --- L3 : Pell + c_hat != 0  ==>  p | a' ,  a'/a5 = 5 P Q ---------
        Q, rem = divmod_poly(der(A), P)
        check("L3-div", rem == [], f"@{gi}")
        check("L3-lc", deg(Q) == 2 and Q[2] == 5, f"@{gi}")
        Q = scal(Q, F(1, 5))                       # monic

        # --- L4 : 4 A4 = 5 (P1 + Q1) ,  depressed 下で A4 = P1 = -5 Q1 ----
        check("L4-gen", 4 * A[4] == 5 * (P[1] + Q[1]), f"@{gi}")
        check("L4-dep", A[4] == -5 * Q[1], f"@{gi}")

        # --- T-1 の再定式化: T-1 <=> Q in Z[x] かつ Q^2 | A(+ 非退化)-----
        rp = rootpart(A)
        t1_ok = (rp == (2, 2, 1))
        Q_int = all(x.denominator == 1 for x in Q)
        _, r2 = divmod_poly(A, mul(Q, Q))
        q_sf = deg(gcd_poly(Q, der(Q))) == 0
        if r2 == [] and Q_int and q_sf:
            cof, _ = divmod_poly(A, mul(Q, Q))
            t1_re = deg(gcd_poly(Q, cof)) == 0
        else:
            t1_re = False
        check("T1-reform", t1_re == t1_ok, f"@{gi}")

        # --- reason code の再構成(verdict state machine §5.3)------------
        e3_ok = (a5 == p2)
        pred = E3_CODE if not e3_ok else (T1_CODE if not t1_ok else "ACCEPT")
        cA = pt["lane_A_primary_reason_code"]
        check("concordant", cA == pt["lane_B_primary_reason_code"], f"@{gi}")
        check("code", pred == cA, f"@{gi} pred={pred} got={cA}")

        # --- 定理 D の主張: T-1 は 744 全点で不成立(E-3 の成否に依らず)--
        check("THM-D", not t1_ok, f"@{gi}")
        # --- 定理 D の合同: T-1 通過は 5 | a4/a5 を要する -----------------
        check("THM-cong", (A[4] % 5 == 0) or (not t1_ok), f"@{gi}")

        rp_dist[rp] += 1
        A4_dist[A[4]] += 1
        stat[(cA, e3_ok, t1_ok)] += 1

    # --- 対合 / Klein 群の census --------------------------------------
    neg = lambda t: tuple(str(-int(x)) for x in t)
    S = set((tuple(q["candidate"]["a"]), tuple(q["candidate"]["p"])) for q in pts)
    inv = sum(1 for (ak, pk) in S if (ak, neg(pk)) in S)
    kle = sum(1 for (ak, pk) in S
              if all(k in S for k in [(ak, neg(pk)), (neg(ak), pk), (neg(ak), neg(pk))]))
    orbits = set(frozenset([(ak, pk), (ak, neg(pk)), (neg(ak), pk), (neg(ak), neg(pk))])
                 for (ak, pk) in S)

    print("=" * 74)
    print("PART 1 : 744 点との突合(定理 D・補題 L1-L4・reason code 再構成)")
    print("=" * 74)
    print(f"  points / distinct (a,p)        : {len(pts)} / {len(S)}")
    print(f"  involution p -> -p closed      : {inv}/{len(S)}")
    print(f"  Klein V = {{+-a}}x{{+-p}} closed   : {kle}/{len(S)}")
    print(f"  Klein orbits (= 幾何的対象数)   : {len(orbits)}")
    print(f"  rootpart(a/a5) 分布            : {dict(rp_dist)}")
    print(f"  a4/a5 分布                     : "
          f"{ {int(k): v for k, v in sorted(A4_dist.items())} }")
    print(f"  5 | a4/a5 を満たす点           : "
          f"{sum(v for k, v in A4_dist.items() if k % 5 == 0)}")
    print(f"  較正 stage1 述語 vs 744 生存者  : {744 - cal_bad}/744 採択 "
          f"({'PASS' if cal_bad == 0 else 'FAIL'})")
    print("  (reason_code, E-3 通過, T-1 通過) -> 点数")
    for k in sorted(stat, key=str):
        print(f"      {k}  {stat[k]}")
    check("calibration", cal_bad == 0, f"{cal_bad} rejected")


# ======================================================================
# PART 1b : bound=5 の悉皆走査(委嘱4・run 30289323147)との突合
#           — 定理を導くのに一切使っていない out-of-sample データ
# ======================================================================
def part1b():
    import glob
    pat = os.path.join(ROOT, "certificates", "mb", "actions", "30289323147",
                       "ninfty-b5-*.json")
    files = [f for f in sorted(glob.glob(pat)) if not f.endswith("provenance.json")]
    if not files:
        print("\n  (PART 1b: bound-5 証明書が見つからない — skip)")
        return
    rp_dist, lem, cal_bad, hits, tot = Counter(), Counter(), 0, [], 0
    for fn in files:
        d = json.load(open(fn, encoding="utf-8"))
        for det in d.get("stage1_pass_details", []):
            tot += 1
            a = [F(det["a%d" % i]) for i in range(6)]
            p = [F(det["p%d" % i]) for i in range(3)]
            A, P = scal(a, F(1) / a[5]), scal(p, F(1) / p[2])
            lem["L1"] += (a[5] * a[5] == 1 and p[2] * p[2] == 1)
            ok, _ = stage1(A, P, require_depressed=True)
            cal_bad += (not ok)
            lem["L2"] += (A[4] == P[1])
            Q, rem = divmod_poly(der(A), P)
            lem["L3"] += (rem == [] and deg(Q) == 2 and Q[2] == 5)
            Q = scal(Q, F(1, 5))
            lem["BARY"] += (4 * A[4] == 5 * (P[1] + Q[1]))
            r = rootpart(A)
            rp_dist[r] += 1
            if det.get("stage2", {}).get("ok"):
                hits.append(([int(x) for x in a], [int(x) for x in p], r))
    print()
    print("=" * 74)
    print("PART 1b : bound=5 悉皆走査(委嘱4)との突合 — out-of-sample")
    print("=" * 74)
    print(f"  shard 数 / stage1 生存者          : {len(files)} / {tot}")
    print(f"  較正 stage1 述語の採択            : {tot - cal_bad}/{tot}")
    print(f"  補題 L1/L2/L3/BARY                : {dict(lem)}")
    print(f"  rootpart(a/a5) 分布               : {dict(rp_dist)}")
    print(f"  rootpart = [2,2,1](= T-1 通過)  : {rp_dist[(2, 2, 1)]}   <- 定理 D+ の予測は 0")
    print(f"  探索器 stage2 の hit              : {len(hits)}")
    for a, p, r in hits:
        code = "[7] triple-root-of-a" if max(r) >= 3 else "[8] a-partition-mismatch"
        print(f"      a={a} p={p} rootpart={r}  spec T-1 = FAIL ({code})")
    check("part1b-cal", cal_bad == 0, f"{cal_bad} rejected")
    check("part1b-L", all(v == tot for v in lem.values()), f"{dict(lem)} vs {tot}")
    check("part1b-Dplus", rp_dist[(2, 2, 1)] == 0, "T-1 pass found at bound 5")
    check("part1b-hits-fail-T1", all(r != (2, 2, 1) for _, _, r in hits),
          "a stage2 hit passed T-1")


# ======================================================================
# PART 2 : searcher 正規形(depressed)での最小 bound
# ======================================================================
def build(b, c, d):
    """A = (x^2+bx+c)^2 (x+d)  (monic quintic)."""
    q2 = [F(c * c), F(2 * b * c), F(b * b + 2 * c), F(2 * b), F(1)]
    A = [F(0)] * 6
    for i, v in enumerate(q2):
        A[i] += v * d
        A[i + 1] += v
    return trim(A)


def companion(b, c, d):
    """P = (2 Q' l + Q)/5 = (5x^2 + (4d+3b)x + (2bd+c))/5 。
    補題 L3 により Pell 通過候補ではこれが p/p2 に一致する。"""
    return [F(2 * b * d + c, 5), F(4 * d + 3 * b, 5), F(1)]


def part2(TARGET=40):
    """RIGOROUS WINDOW (depressed 側):
       depressed ==> d = -7b, かつ |a4/a5| = 5|b| <= B , |a0/a5| = 7|b|c^2 <= B。
       ゆえに b != 0 なら |b| <= B/5 かつ c^2 <= B/7、b = 0 なら c^2 = |a1/a5| <= B。
       下の窓はこれを B <= TARGET で満たすように取ってあり、証明の一部である。"""
    print()
    print("=" * 74)
    print(f"PART 2 : depressed 正規形での最小 bound(窓 B <= {TARGET}・厳密)")
    print("=" * 74)
    found = []
    for b in range(-(TARGET // 5), TARGET // 5 + 1):
        if b == 0:
            crange = range(-int(TARGET ** 0.5) - 1, int(TARGET ** 0.5) + 2)
        else:
            m = int((TARGET / (7 * abs(b))) ** 0.5) + 1
            crange = range(-m, m + 1)
        for c in crange:
            d = -7 * b
            if b * b - 4 * c == 0:                       # Q squarefree
                continue
            if d * d - b * d + c == 0:                   # gcd(Q, l) = 1
                continue
            A, P = build(b, c, d), companion(b, c, d)
            if any(x.denominator != 1 for x in P):       # p integral
                continue
            ok, _ = stage1(A, P, require_depressed=True)
            if not ok:
                continue
            check("part2-rootpart", rootpart(A) == (2, 2, 1), f"(b,c)=({b},{c})")
            B = max(inf_norm(A[:5]), inf_norm(P[:2]))
            found.append((int(B), b, c, [int(x) for x in A], [int(x) for x in P]))
    found.sort()
    print(f"  E-1..E-6 + T-1 を全て通過する点 : {len(found)}")
    for B, b, c, A, P in found[:6]:
        print(f"     B = {B}   (b,c,d) = ({b},{c},{-7*b})   a/a5 = {A}   p/p2 = {P}")
    if found:
        print(f"  ==> depressed 正規形の最小 bound B* = {found[0][0]}")
    check("part2-min", bool(found) and found[0][0] == 25,
          f"expected 25, got {found[0][0] if found else None}")


# ======================================================================
# PART 3 : gauge-free(depressed を落とした)有限探索
# ======================================================================
def part3(BMAX=6):
    """RIGOROUS WINDOW (gauge-free 側):
       a/a5 は monic かつ |係数| <= B ゆえ Cauchy 界より全根は |z| <= 1+B。
       根は Q の 2 根(重複)と -d。よって |d| <= 1+B、|b| <= 2(1+B)、
       |c| <= (1+B)^2。この窓は完全であり証明の一部である。"""
    print()
    print("=" * 74)
    print("PART 3 : gauge-free 有限探索(depressed を仮定しない・Cauchy 窓)")
    print("=" * 74)
    first = None
    for B in range(1, BMAX + 1):
        R = 1 + B
        surv = []
        for d in range(-R, R + 1):
            for b in range(-2 * R, 2 * R + 1):
                for c in range(-R * R, R * R + 1):
                    if b * b - 4 * c == 0:
                        continue
                    if d * d - b * d + c == 0:
                        continue
                    A = build(b, c, d)
                    if inf_norm(A[:5]) > B:
                        continue
                    P = companion(b, c, d)
                    if any(x.denominator != 1 for x in P):
                        continue
                    if inf_norm(P[:2]) > B:
                        continue
                    ok, why = stage1(A, P, require_depressed=False)
                    surv.append((b, c, d, [int(x) for x in A],
                                 [int(x) for x in P], ok, why))
        full = [s for s in surv if s[5]]
        print(f"  B = {B} : 窓 |d|<={R}, |b|<={2*R}, |c|<={R*R}   "
              f"[T-1 型 + p|a' + 箱] = {len(surv)} 点 / うち E-1..E-6+T-1 全通過 = {len(full)}")
        for b, c, d, A, P, ok, why in full[:6]:
            print(f"       (b,c,d)=({b:2d},{c:2d},{d:2d})  a/a5 = {A}  p/p2 = {P}  "
                  f"rootpart = {rootpart([F(x) for x in A])}")
        if full and first is None:
            first = B
        if B <= 4:
            check("part3-empty", not surv, f"B={B} had {len(surv)} survivors")
    print(f"  ==> gauge-free の最小 bound = {first}")
    check("part3-min", first == 5, f"expected 5, got {first}")


if __name__ == "__main__":
    part1()
    part1b()
    part2()
    part3()
    print()
    print("=" * 74)
    print("VERDICT:", "ALL CHECKS PASS" if not fails else f"{len(fails)} FAILURES")
    for f_ in fails[:20]:
        print("   FAIL:", f_)
    print("=" * 74)
    sys.exit(0 if not fails else 1)

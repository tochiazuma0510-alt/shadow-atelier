#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
w98_alg_driver.py -- W98-ALG driver
  sol/sol_reply_98_math25.md sec.5, W98-5.1 (採択案) / P98-5.1 (実装・検収ゲート) の
  逐語仕様どおりに実装する CharacterTable("Symmetric",n) 不使用の厳密計数 driver。

対象:
  T_all(rho)  = #{(g,h) in S_n^2 : g^2=1, h^3=1, gh=w_rho},  rho=(ell,1^a), n=ell+a.
  T_trans(rho) = 上記のうち <g,h> が n 点上 推移的なもの(= 二項反転で得る)。

式 (ALG-1) (reply 逐語):
  T_all(rho) = (1/n!) * sum_{lambda |- n}  A2(lambda) A3(lambda) chi^lambda(rho) / f^lambda
  A2(lambda)/n! = s_lambda | p1=p2=1, else 0   (Jacobi-Trudi det, h_k^(2) 使用)
  A3(lambda)/n! = s_lambda | p1=p3=1, else 0   (Jacobi-Trudi det, h_k^(3) 使用)
    k h_k^(2) = h_{k-1}^(2) + h_{k-2}^(2),  h_0^(2)=1
    k h_k^(3) = h_{k-1}^(3) + h_{k-3}^(3),  h_0^(3)=1
  f^lambda = hook length formula.
式 (ALG-2) (reply 逐語、rho=(ell,1^a), a<=8 で局所化):
  chi^lambda(ell,1^a) = sum_{mu |- a, lambda/mu が長さ ell の rim hook} (-1)^{ht(lambda/mu)} f^mu
式 (ALG-3) (reply 逐語、二項反転):
  T_all(ell,1^t)   = sum_{a=0}^t C(t,a) T_trans(ell,1^a)
  T_trans(ell,1^t) = sum_{a=0}^t (-1)^{t-a} C(t,a) T_all(ell,1^a)

P98-5.1 実装ゲート(5条)を満たすことを目的に、以下を実装する。
  1. CharacterTable("Symmetric",n) / ctbllib への依存を一切持たない(GAP 非依存、純 Python)。
  2. route A (全 partition-of-n streaming) と route B (rim-hook 直接生成で非零 lambda のみ)
     を独立二重実装する。両ルートは partition 生成器・hook length 実装・h 数列構成法・
     Jacobi-Trudi 行列式アルゴリズムのいずれも共有しない(関数名の prefix rA_ / rB_ で
     分離し、コードの参照関係を持たせない)。
       - route A: h_k は「k h_k = h_{k-1}+h_{k-gap}」の Fraction 直接漸化式。
                  行列式は素朴な Fraction 分数ピボット Gauss 消去。
                  hook length は共役分割を作ってから arm+leg で計算。
                  partition 生成は accel_asc 型(昇順合成の高速アルゴリズム)を自前実装。
       - route B: h_k は g_k=k! h_k の整数漸化式 g_k=g_{k-1}+(falling factorial)*g_{k-gap}
                  (involution数/3-torsion数の組合せ論的漸化式)を経由し k! で割る。
                  行列式は Bareiss 型(縮小主座小行列子)消去。
                  hook length は各行ごとに下の行を直接スキャンして leg を数える。
                  partition 生成は再帰的な「先頭項の上限を下げていく」構成(mu, a<=8 のみ)。
                  chi は mu ごとに rim hook を「追加」して生成される非零 lambda だけを列挙する
                  (removal ではなく addition のビーズ演算 -- route A の removal 演算とも
                  コードとして別物)。
  3. fail-closed assert: 各 T_all の整数性・非負性、(ALG-1) の分母消去、(ALG-3) の非負性、
     さらに route A と route B の一致(不一致は即 AssertionError で停止 -- CV-13 の精神)。
  4. 較正 4 点: (a) 小 n 直接悉皆(全 permutation 総当たり、route A/B と別コード)、
     (b) (23,1^3) T_trans=173880、(c) (25,1^5) T_trans=378000、
     (d) (37,1^2) の両方の値 T_trans=3,296,573,904 / T_all=10,643,405,866
     (search/certs 相当のソース: scratchpad/lt13a/.../ell37-t2/lt_count_gen_ell37_t2_20260801.json,
      cert schema wac_v1-lt-count-gen-cert/v1, GAP 単系統 ClassMultiplicationCoefficient 由来)。
     >0 だけの較正は禁止 -- 全て厳密な数値一致を assert する。
  5. cert: formula ID・各 a の T_all・寄与 partition 数・contribution stream digest(route A/B
     それぞれ)・script digest(自己 sha256)・完走 marker DRIVER_DONE。

言語: 純 Python 3(fractions.Fraction / int の厳密演算のみ。float 不使用)。GAP 非依存。

宇宙: 本 driver が計算するのは rho=(ell,1^a) 型(1 本の長サイクル + 固定点)のみ。
一般の cycle type への拡張は本 driver の対象外(宇宙を勝手に広げない)。
"""

import sys
import os
import json
import math
import time
import hashlib
import datetime
import itertools
from fractions import Fraction
from collections import defaultdict

SCRIPT_PATH = os.path.abspath(__file__)


# ============================================================================
# ROUTE A -- 全 partition-of-n streaming
# ============================================================================

def rA_partitions(n):
    """n の全分割を非増加 tuple として一つずつ生成する(accel_asc 型、自前実装)。
    メモリは O(n) (partition 1 個分) のみ保持する streaming 生成器。"""
    if n == 0:
        yield ()
        return
    a = [0] * (n + 1)
    k = 1
    y = n - 1
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2 * x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            part = a[:k + 2]
            part.reverse()
            yield tuple(part)
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        part = a[:k + 1]
        part.reverse()
        yield tuple(part)


def rA_conjugate(lam):
    if not lam:
        return []
    maxpart = lam[0]
    return [sum(1 for x in lam if x >= c) for c in range(1, maxpart + 1)]


def rA_hook_product(lam):
    if not lam:
        return 1
    conj = rA_conjugate(lam)
    prod = 1
    for i in range(len(lam)):
        for j in range(lam[i]):
            arm = lam[i] - j - 1
            leg = conj[j] - i - 1
            prod *= (arm + leg + 1)
    return prod


def rA_h_seq(nmax, gap):
    """k h_k = h_{k-1} + h_{k-gap}, h_0=1, h_{<0}=0.  直接 Fraction 漸化式。"""
    h = [Fraction(1)]
    for k in range(1, nmax + 1):
        t1 = h[k - 1]
        t2 = h[k - gap] if k - gap >= 0 else Fraction(0)
        h.append(Fraction(t1 + t2, k))
    return h


def rA_det_fraction(M):
    """素朴な Fraction 部分ピボット Gauss 消去による行列式。"""
    n = len(M)
    if n == 0:
        return Fraction(1)
    A = [row[:] for row in M]
    det = Fraction(1)
    for col in range(n):
        piv = None
        for r in range(col, n):
            if A[r][col] != 0:
                piv = r
                break
        if piv is None:
            return Fraction(0)
        if piv != col:
            A[col], A[piv] = A[piv], A[col]
            det = -det
        pivval = A[col][col]
        det *= pivval
        for r in range(col + 1, n):
            if A[r][col] != 0:
                factor = Fraction(A[r][col], pivval)
                for c in range(col, n):
                    A[r][c] -= factor * A[col][c]
    return det


def rA_jacobi_trudi_det(lam, hseq):
    l = len(lam)
    if l == 0:
        return Fraction(1)
    M = [[Fraction(0)] * l for _ in range(l)]
    for i in range(l):
        for j in range(l):
            k = lam[i] - i + j
            if k == 0:
                M[i][j] = Fraction(1)
            elif 0 < k < len(hseq):
                M[i][j] = hseq[k]
            else:
                M[i][j] = Fraction(0)
    return rA_det_fraction(M)


def rA_chi_ell1a(lam, ell, a):
    """chi^lambda(ell,1^a) を「lambda から長さ ell の rim hook を 1 本除去」する
    ビーズ(beta-set)演算で直接計算する(除去方向、route B の追加方向とは別コード)。"""
    L = len(lam)
    beta = [lam[i] + (L - 1 - i) for i in range(L)]
    betaset = set(beta)
    total = 0
    for idx in range(L):
        b = beta[idx]
        bp = b - ell
        if bp < 0 or bp in betaset:
            continue
        newbeta = beta[:]
        newbeta[idx] = bp
        newbeta.sort(reverse=True)
        mu = [newbeta[i] - (L - 1 - i) for i in range(L)]
        mu = tuple(x for x in mu if x > 0)
        if sum(mu) != a:
            raise AssertionError("route A: beta removal size mismatch (bug)")
        height = sum(1 for y in betaset if bp < y < b)
        f_mu = rA_hook_f(mu, a)
        total += ((-1) ** height) * f_mu
    return total


def rA_hook_f(mu, size):
    if size == 0:
        return 1
    fact = math.factorial(size)
    hp = rA_hook_product(mu)
    assert fact % hp == 0, "route A: hook length does not divide n! (bug)"
    return fact // hp


def route_A_compute(ell, a, timing=None):
    t0 = time.time()
    n = ell + a
    n_fact = math.factorial(n)
    hseq_len = 2 * n + 4
    h2seq = rA_h_seq(hseq_len, 2)
    h3seq = rA_h_seq(hseq_len, 3)
    total = Fraction(0)
    contrib = []
    partitions_scanned = 0
    for lam in rA_partitions(n):
        partitions_scanned += 1
        chi_val = rA_chi_ell1a(lam, ell, a)
        if chi_val == 0:
            continue
        f_lam = rA_hook_f(lam, n)
        d2 = rA_jacobi_trudi_det(lam, h2seq)
        d3 = rA_jacobi_trudi_det(lam, h3seq)
        A2v = n_fact * d2
        A3v = n_fact * d3
        assert A2v.denominator == 1, f"route A: A2 not integer at lambda={lam}"
        assert A3v.denominator == 1, f"route A: A3 not integer at lambda={lam}"
        A2i, A3i = A2v.numerator, A3v.numerator
        term = Fraction(A2i * A3i * chi_val, f_lam)
        total += term
        contrib.append((lam, chi_val, A2i, A3i, f_lam))
    T_all_frac = total / n_fact
    assert T_all_frac.denominator == 1, f"route A: ALG-1 denominator not cleared, ell={ell} a={a}: {T_all_frac}"
    T_all = T_all_frac.numerator
    assert T_all >= 0, f"route A: negative T_all, ell={ell} a={a}: {T_all}"
    elapsed = time.time() - t0
    if timing is not None:
        timing['route_A_seconds'] = elapsed
        timing['route_A_partitions_scanned'] = partitions_scanned
    return T_all, contrib


# ============================================================================
# ROUTE B -- rim-hook 直接生成(非零 lambda のみ)
# ============================================================================

def rB_partitions_of(a):
    """a の全分割を非増加 tuple で列挙する(先頭項上限を下げていく再帰、route A とは
    別アルゴリズム)。a<=8 の小さい対象専用。"""
    def rec(remaining, cap):
        if remaining == 0:
            yield ()
            return
        top = min(remaining, cap)
        for first in range(top, 0, -1):
            for rest in rec(remaining - first, first):
                yield (first,) + rest
    if a == 0:
        yield ()
    else:
        yield from rec(a, a)


def rB_hook_product(lam):
    if not lam:
        return 1
    l = len(lam)
    prod = 1
    for i in range(l):
        for j in range(lam[i]):
            leg = 0
            for i2 in range(i + 1, l):
                if lam[i2] > j:
                    leg += 1
                else:
                    break
            arm = lam[i] - 1 - j
            prod *= (arm + leg + 1)
    return prod


def rB_hook_f(mu, size):
    if size == 0:
        return 1
    fact = math.factorial(size)
    hp = rB_hook_product(mu)
    assert fact % hp == 0, "route B: hook length does not divide n! (bug)"
    return fact // hp


def rB_h_seq(nmax, gap):
    """g_k = k! h_k の整数漸化式(involution 数/3-捩れ元数の組合せ論的漸化式)を経由し、
    最後に k! で割って Fraction 化する。route A の直接 Fraction 漸化式とは別経路。"""
    g = [1]
    for k in range(1, nmax + 1):
        t1 = g[k - 1]
        if k - gap >= 0:
            falling = 1
            for m in range(k - gap + 1, k):
                falling *= m
            t2 = falling * g[k - gap]
        else:
            t2 = 0
        g.append(t1 + t2)
    return [Fraction(g[k], math.factorial(k)) for k in range(nmax + 1)]


def rB_det(M):
    """Bareiss 型(縮小主座小行列子による割り切れる消去)行列式。route A の素朴 Gauss
    消去とは別アルゴリズム。"""
    n = len(M)
    if n == 0:
        return Fraction(1)
    A = [row[:] for row in M]
    sign = 1
    prev_pivot = Fraction(1)
    for k in range(n - 1):
        if A[k][k] == 0:
            swapped = False
            for r in range(k + 1, n):
                if A[r][k] != 0:
                    A[k], A[r] = A[r], A[k]
                    sign = -sign
                    swapped = True
                    break
            if not swapped:
                return Fraction(0)
        pivk = A[k][k]
        for i in range(k + 1, n):
            aik = A[i][k]
            for j in range(k + 1, n):
                A[i][j] = Fraction(A[i][j] * pivk - aik * A[k][j], prev_pivot)
        prev_pivot = pivk
    return sign * A[n - 1][n - 1]


def rB_jacobi_trudi_det(lam, hseq):
    l = len(lam)
    if l == 0:
        return Fraction(1)
    M = [[Fraction(0)] * l for _ in range(l)]
    for i in range(l):
        for j in range(l):
            k = lam[i] - i + j
            if k == 0:
                M[i][j] = Fraction(1)
            elif 0 < k < len(hseq):
                M[i][j] = hseq[k]
            else:
                M[i][j] = Fraction(0)
    return rB_det(M)


def rB_add_rim_hooks(mu, ell):
    """mu (|mu|=a) に長さ ell の rim hook を 1 本「追加」する全ての方法を
    (lambda, height) として列挙する(ビーズを ell だけ上げる add 演算、
    route A の remove 演算とはコード的に独立)。"""
    a = sum(mu)
    L = a + ell
    mu_padded = list(mu) + [0] * (L - len(mu))
    beta = [mu_padded[i] + (L - 1 - i) for i in range(L)]
    betaset = set(beta)
    for idx in range(L):
        b = beta[idx]
        bp = b + ell
        if bp in betaset:
            continue
        newbeta = beta[:]
        newbeta[idx] = bp
        newbeta.sort(reverse=True)
        lam = [newbeta[i] - (L - 1 - i) for i in range(L)]
        lam = tuple(x for x in lam if x > 0)
        if sum(lam) != a + ell:
            raise AssertionError("route B: beta addition size mismatch (bug)")
        height = sum(1 for y in betaset if b < y < bp)
        yield lam, height


def route_B_compute(ell, a, timing=None):
    t0 = time.time()
    n = ell + a
    n_fact = math.factorial(n)
    chi_contrib = defaultdict(int)
    mu_count = 0
    for mu in rB_partitions_of(a):
        mu_count += 1
        f_mu = rB_hook_f(mu, a)
        for lam, height in rB_add_rim_hooks(mu, ell):
            chi_contrib[lam] += ((-1) ** height) * f_mu
    hseq_len = 2 * n + 4
    h2seq = rB_h_seq(hseq_len, 2)
    h3seq = rB_h_seq(hseq_len, 3)
    total = Fraction(0)
    contrib = []
    for lam, chi_val in chi_contrib.items():
        if chi_val == 0:
            continue
        f_lam = rB_hook_f(lam, n)
        d2 = rB_jacobi_trudi_det(lam, h2seq)
        d3 = rB_jacobi_trudi_det(lam, h3seq)
        A2v = n_fact * d2
        A3v = n_fact * d3
        assert A2v.denominator == 1, f"route B: A2 not integer at lambda={lam}"
        assert A3v.denominator == 1, f"route B: A3 not integer at lambda={lam}"
        A2i, A3i = A2v.numerator, A3v.numerator
        term = Fraction(A2i * A3i * chi_val, f_lam)
        total += term
        contrib.append((lam, chi_val, A2i, A3i, f_lam))
    T_all_frac = total / n_fact
    assert T_all_frac.denominator == 1, f"route B: ALG-1 denominator not cleared, ell={ell} a={a}: {T_all_frac}"
    T_all = T_all_frac.numerator
    assert T_all >= 0, f"route B: negative T_all, ell={ell} a={a}: {T_all}"
    elapsed = time.time() - t0
    if timing is not None:
        timing['route_B_seconds'] = elapsed
        timing['route_B_mu_count'] = mu_count
    return T_all, contrib


# ============================================================================
# ALG-3 -- 二項反転(推移的計数)
# ============================================================================

def alg3_t_trans(t, T_all_by_a):
    total = 0
    for a in range(t + 1):
        total += ((-1) ** (t - a)) * math.comb(t, a) * T_all_by_a[a]
    assert total >= 0, f"ALG-3: negative T_trans at t={t}: {total}"
    return total


def alg3_t_all_from_trans(t, T_trans_by_a):
    """逆向き(検算用): T_all(ell,1^t) = sum_a C(t,a) T_trans(ell,1^a)。"""
    total = 0
    for a in range(t + 1):
        total += math.comb(t, a) * T_trans_by_a[a]
    return total


# ============================================================================
# 較正(a) -- 小 n 直接悉皆(全 permutation 総当たり、route A/B とは別コード)
# ============================================================================

def brute_force_T_all(ell, a):
    """S_n 全順列を総当たりし、g^2=h^3=1, gh=w_rho の組を直接数える。
    n<=9 程度の小対象専用(較正の第三経路 -- route A/B のどの関数も呼ばない)。"""
    n = ell + a
    if n > 9:
        raise ValueError("brute force is for small n only (n<=9)")
    ident = tuple(range(n))
    target = list(range(n))
    if ell >= 2:
        for i in range(ell - 1):
            target[i] = i + 1
        target[ell - 1] = 0
    # target[ell..n-1] は既に恒等(固定点)
    target = tuple(target)

    def compose(f, g):
        return tuple(f[g[i]] for i in range(n))

    invols = []
    order3 = []
    for p in itertools.permutations(range(n)):
        p2 = compose(p, p)
        if p2 == ident:
            invols.append(p)
        p3 = compose(p2, p)
        if p3 == ident:
            order3.append(p)
    count = 0
    for g in invols:
        for h in order3:
            if compose(g, h) == target:
                count += 1
    return count


# ============================================================================
# digest / cert 補助
# ============================================================================

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def contrib_digest(contrib):
    """(lambda, chi, A2, A3, f_lambda) のリストを lambda で正規順序化して sha256 する。"""
    recs = sorted(contrib, key=lambda r: r[0])
    lines = []
    for lam, chi_val, A2i, A3i, f_lam in recs:
        lines.append(f"{list(lam)}|{chi_val}|{A2i}|{A3i}|{f_lam}")
    blob = "\n".join(lines).encode("utf-8")
    return sha256_hex(blob), len(recs)


def script_digest():
    with open(SCRIPT_PATH, "rb") as fh:
        return sha256_hex(fh.read())


# ============================================================================
# main
# ============================================================================

def compute_cell(ell, a, log):
    timing = {}
    T_all_A, contrib_A = route_A_compute(ell, a, timing)
    T_all_B, contrib_B = route_B_compute(ell, a, timing)
    assert T_all_A == T_all_B, (
        f"route A/B mismatch at ell={ell} a={a}: A={T_all_A} B={T_all_B}"
    )
    digA, nA = contrib_digest(contrib_A)
    digB, nB = contrib_digest(contrib_B)
    rec = {
        "ell": ell,
        "a": a,
        "n": ell + a,
        "T_all": T_all_A,
        "route_A_contributing_partitions": nA,
        "route_B_contributing_partitions": nB,
        "route_A_contribution_digest_sha256": digA,
        "route_B_contribution_digest_sha256": digB,
        "route_A_seconds": round(timing.get('route_A_seconds', 0.0), 4),
        "route_B_seconds": round(timing.get('route_B_seconds', 0.0), 4),
        "route_A_partitions_scanned": timing.get('route_A_partitions_scanned'),
        "route_B_mu_count": timing.get('route_B_mu_count'),
    }
    log(f"    T_all({ell},1^{a}) [n={ell+a}] = {T_all_A}   "
        f"(A: {nA} contrib / {timing.get('route_A_partitions_scanned')} scanned, "
        f"{rec['route_A_seconds']}s ; B: {nB} contrib, {rec['route_B_seconds']}s)")
    return rec


def main():
    t_start = time.time()
    out = {"log": []}

    def log(msg):
        print(msg)
        out["log"].append(msg)

    log("############ W98-ALG driver (sol/sol_reply_98_math25.md sec.5) ############")
    log(f"start: {datetime.datetime.utcnow().isoformat()}Z")

    report = {
        "schema": "wac_v1-w98-alg-driver-cert/v1",
        "formula_id": "W98-ALG (sol_reply_98_math25.md sec.5, ALG-1/ALG-2/ALG-3)",
        "spec_ref": "sol/sol_reply_98_math25.md W98-5.1 / P98-5.1",
        "no_symmetric_chartable": True,
        "no_ctbllib": True,
        "generated_by": "search/probe/wac_v1/w98_alg_driver.py",
    }

    # ---- 較正(a): 小 n 直接悉皆 ----
    log("\n=== 較正(a): 小 n 直接悉皆(brute force, route A/B とは独立) ===")
    small_cases = [(2, 0), (3, 0), (3, 2), (4, 1), (5, 0), (2, 3), (4, 3), (3, 3)]
    small_results = []
    small_ok = True
    for ell, a in small_cases:
        n = ell + a
        bf = brute_force_T_all(ell, a)
        ra, _ = route_A_compute(ell, a)
        rb, _ = route_B_compute(ell, a)
        ok = (bf == ra == rb)
        small_ok = small_ok and ok
        log(f"  (ell={ell},a={a},n={n}): brute={bf}  routeA={ra}  routeB={rb}  "
            f"{'PASS' if ok else '*** FAIL ***'}")
        small_results.append({"ell": ell, "a": a, "n": n, "brute_force": bf,
                               "route_A": ra, "route_B": rb, "pass": ok})
    assert small_ok, "較正(a) 小 n 直接悉皆に不一致あり -- fail-closed 停止"
    report["calibration_small_n"] = small_results

    # ---- 較正(b): (23,1^3) T_trans=173880 ----
    log("\n=== 較正(b): ell=23, T_trans(23,1^3) = 173880 ===")
    ell = 23
    T_all_23 = {}
    for a in range(4):
        rec = compute_cell(ell, a, log)
        T_all_23[a] = rec["T_all"]
    T_trans_23_3 = alg3_t_trans(3, T_all_23)
    log(f"  T_trans(23,1^3) = {T_trans_23_3}  (期待値 173880)  "
        f"{'PASS' if T_trans_23_3 == 173880 else '*** FAIL ***'}")
    assert T_trans_23_3 == 173880, f"較正(b) 不一致: {T_trans_23_3} != 173880"

    # ---- 較正(c): (25,1^5) T_trans=378000 ----
    log("\n=== 較正(c): ell=25, T_trans(25,1^5) = 378000 ===")
    ell = 25
    T_all_25 = {}
    for a in range(6):
        rec = compute_cell(ell, a, log)
        T_all_25[a] = rec["T_all"]
    T_trans_25_5 = alg3_t_trans(5, T_all_25)
    log(f"  T_trans(25,1^5) = {T_trans_25_5}  (期待値 378000)  "
        f"{'PASS' if T_trans_25_5 == 378000 else '*** FAIL ***'}")
    assert T_trans_25_5 == 378000, f"較正(c) 不一致: {T_trans_25_5} != 378000"

    # ---- 較正(d): (37,1^2) 両方の値 ----
    log("\n=== 較正(d): ell=37, (37,1^2) 両方の値(T_all と T_trans) ===")
    ell = 37
    T_all_37_for_cal = {}
    for a in range(3):
        rec = compute_cell(ell, a, log)
        T_all_37_for_cal[a] = rec["T_all"]
    T_all_37_2 = T_all_37_for_cal[2]
    T_trans_37_2 = alg3_t_trans(2, T_all_37_for_cal)
    log(f"  T_all(37,1^2)   = {T_all_37_2}  (期待値 10643405866)  "
        f"{'PASS' if T_all_37_2 == 10643405866 else '*** FAIL ***'}")
    log(f"  T_trans(37,1^2) = {T_trans_37_2}  (期待値 3296573904)  "
        f"{'PASS' if T_trans_37_2 == 3296573904 else '*** FAIL ***'}")
    assert T_all_37_2 == 10643405866, f"較正(d) T_all 不一致: {T_all_37_2}"
    assert T_trans_37_2 == 3296573904, f"較正(d) T_trans 不一致: {T_trans_37_2}"

    report["calibration_named"] = {
        "ell23_a3_T_trans": {"value": T_trans_23_3, "expected": 173880},
        "ell25_a5_T_trans": {"value": T_trans_25_5, "expected": 378000},
        "ell37_a2_T_all": {"value": T_all_37_2, "expected": 10643405866},
        "ell37_a2_T_trans": {"value": T_trans_37_2, "expected": 3296573904},
        "all_pass": True,
    }
    log("\n*** 較正 4 点 ALL PASS ***")

    # ---- 本走: ell=37,41, a=0..8 の 18 値 ----
    log("\n=== 本走: ell in {37,41}, a=0..8 の 18 値 ===")
    cells = {}
    for ell in (37, 41):
        cells[ell] = {}
        for a in range(9):
            if ell == 37 and a in T_all_37_for_cal:
                # 較正走で既に得た a=0,1,2 は再利用せず、独立性のため再計算する
                # (P98-5.1 は「較正」と「本走」を分けて要求しているため二重に走らせる)
                pass
            rec = compute_cell(ell, a, log)
            cells[ell][a] = rec

    report["cells"] = {
        str(ell): {str(a): cells[ell][a] for a in range(9)} for ell in (37, 41)
    }

    # T_trans も ALG-3 で全て算出して cert に残す(検算: 逆変換で T_all に戻るかも確認)
    log("\n=== ALG-3 二項反転: T_trans(ell,1^t), t=0..8 ===")
    trans_table = {}
    for ell in (37, 41):
        T_all_by_a = {a: cells[ell][a]["T_all"] for a in range(9)}
        trans_table[ell] = {}
        for t in range(9):
            tt = alg3_t_trans(t, T_all_by_a)
            trans_table[ell][t] = tt
            log(f"  T_trans({ell},1^{t}) = {tt}")
        # 検算: T_trans から ALG-3 の逆変換で T_all(ell,1^t) が復元できるか(t=0..8 全て)
        for t in range(9):
            back = alg3_t_all_from_trans(t, trans_table[ell])
            assert back == T_all_by_a[t], (
                f"ALG-3 round-trip mismatch ell={ell} t={t}: back={back} orig={T_all_by_a[t]}"
            )
    report["T_trans"] = {str(ell): {str(t): trans_table[ell][t] for t in range(9)} for ell in (37, 41)}

    # ---- fail-closed 完走確認 ----
    total_elapsed = time.time() - t_start
    report["wall_seconds_total"] = round(total_elapsed, 3)
    report["script_sha256"] = script_digest()
    report["provenance"] = {
        "python_version": sys.version,
        "generated_at_utc": datetime.datetime.utcnow().isoformat() + "Z",
    }
    report["driver_done"] = True
    report["marker"] = "DRIVER_DONE"

    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_PATH))), "certs")
    out_path = os.path.join(out_dir, "w98_alg_driver_cert_20260801.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2, sort_keys=False)
    cert_sha = sha256_hex(open(out_path, "rb").read())

    log(f"\nwall_seconds_total = {report['wall_seconds_total']}")
    log(f"script_sha256 = {report['script_sha256']}")
    log(f"cert written: {out_path}")
    log(f"cert_sha256 = {cert_sha}")
    log("\nDRIVER_DONE")
    return report


if __name__ == "__main__":
    main()

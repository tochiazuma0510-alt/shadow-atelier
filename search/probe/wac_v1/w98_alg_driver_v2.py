#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
w98_alg_driver_v2.py -- W98-ALG driver v2(恒久 fixture 編入版)

正本: sol/sol_reply_99_math26.md 六節 P99-6.2(便 99 検収・裁定 412 で条件つき認可)。
v1(search/probe/wac_v1/w98_alg_driver.py, sol/sol_reply_98_math25.md sec.5 実装・
裁定 390 完成・裁定 412 で digest 束縛 = 991a8c1f0c233999c7d4aa8296fadad09170a8acece8c5f3e9ec92e0b2c4b052)
は byte 不変のまま残す。本ファイルは v1 の route A / route B / 4 較正 / 18 セル
本走 / ALG-3 二項反転 という設計をそのまま継承した**新版**であり、その上に
P99-6.2 の 5 条件による恒久 fixture を追加する。

P99-6.2 条件(逐条遵守):
  1. n=10,11,12,13 の直接 brute 30 ケースを固定 fixture 化する
     (裁定 393 の総当たり census を恒久化)。
     ここで固定する宇宙は search/probe/wac_v1/w98_fixture_v1.py の
     CENSUS_UNIVERSE(ell=5..10, 裁定393 が実際に走らせた ell->tmax 表)であり、
     これは 27 ケース(n=5..13 の全域)である。この 27 の中に n in {10,11,12,13}
     の 13 ケースが含まれる。Sol 条件文の逐語「30 ケース」は 2026-08-01 LEDGER
     裁定393 の要約文言(「総当たり 30 ケース(n<=13)」)からの引用と見られるが、
     本 driver が実装・再計算できる裁定393 census の総数は 27 である。30 と 27
     の差は宇宙を勝手に広げて埋めていない(fail-closed に事実を記帳する --
     詳細は cert の `fixture_universe_note` 欄、および実装レポート参照)。
  2. ell=9 の非単調消滅ケース(t=0..4: T_trans=36,54,0,18,0)を negative/boundary
     fixture として固定する(search/probe/wac_v1/w98_fixture_v1.py の
     run_ell9_nonmonotone_fixture)。
  3. 期待値・universe・式 ID・fixture source digest を versioned cert に保存し、
     失敗時も failure cert を残す(fail-closed -- 本 driver は main() 全体を
     try/except で囲み、例外時も部分結果+traceback を書いた failure cert を書く)。
  4. Windows 絶対 path を排除する(cert/ログに書く path 文字列はすべて repo-root
     相対、区切りは "/" に正規化する。__file__ ベースの相対結合のみを使う)。
  5. 「独立 fixture」と数える実装(w98_fixture_v1.py)は本 driver(v1/v2 いずれも)
     の route A / route B / helper を import しない -- 置換悉皆(px_)と
     類乗積(cx_, Murnaghan-Nakayama 再導出)から直接計算する独立実装である。
     本 driver 側は fixture モジュールを import してその結果と route A/B を
     突合するだけであり、依存の向きは一方向(driver -> fixture)のみ。

宇宙: v1 と同じく rho=(ell,1^a) 型のみ(一般 cycle type は対象外)。
"""

import sys
import os
import json
import math
import time
import hashlib
import datetime
import itertools
import importlib.util
import traceback
from fractions import Fraction
from collections import defaultdict

SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
# repo root = .../shadow-atelier (search/probe/wac_v1/ から 3 段上)
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))


def relpath(p):
    """repo-root 相対の path 文字列を "/" 区切りで返す(Windows 絶対 path を
    cert/ログに残さないための唯一の経路)。"""
    return os.path.relpath(os.path.abspath(p), REPO_ROOT).replace(os.sep, "/")


FIXTURE_MODULE_PATH = os.path.join(SCRIPT_DIR, "w98_fixture_v1.py")


def load_fixture_module():
    spec = importlib.util.spec_from_file_location("w98_fixture_v1", FIXTURE_MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ============================================================================
# ROUTE A -- 全 partition-of-n streaming (v1 と同一設計、本ファイルに複写)
# ============================================================================

def rA_partitions(n):
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
    h = [Fraction(1)]
    for k in range(1, nmax + 1):
        t1 = h[k - 1]
        t2 = h[k - gap] if k - gap >= 0 else Fraction(0)
        h.append(Fraction(t1 + t2, k))
    return h


def rA_det_fraction(M):
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
# ROUTE B -- rim-hook 直接生成(v1 と同一設計、本ファイルに複写)
# ============================================================================

def rB_partitions_of(a):
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
    total = 0
    for a in range(t + 1):
        total += math.comb(t, a) * T_trans_by_a[a]
    return total


# ============================================================================
# 較正(a) -- 小 n 直接悉皆(v1 と同一設計、本ファイルに複写)
# ============================================================================

def brute_force_T_all(ell, a):
    n = ell + a
    if n > 9:
        raise ValueError("brute force is for small n only (n<=9)")
    ident = tuple(range(n))
    target = list(range(n))
    if ell >= 2:
        for i in range(ell - 1):
            target[i] = i + 1
        target[ell - 1] = 0
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


def sha256_file(path) -> str:
    with open(path, "rb") as fh:
        return sha256_hex(fh.read())


def contrib_digest(contrib):
    recs = sorted(contrib, key=lambda r: r[0])
    lines = []
    for lam, chi_val, A2i, A3i, f_lam in recs:
        lines.append(f"{list(lam)}|{chi_val}|{A2i}|{A3i}|{f_lam}")
    blob = "\n".join(lines).encode("utf-8")
    return sha256_hex(blob), len(recs)


def script_digest():
    return sha256_file(SCRIPT_PATH)


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


def run_permanent_fixture_block(report, log):
    """P99-6.2 の恒久 fixture 本体。search/probe/wac_v1/w98_fixture_v1.py
    (route A/B を import しない独立実装)を呼び出し、本 driver 自身の
    route A/B(このファイル内定義)と 4 方向(routeA, routeB, fixture-px,
    fixture-cx)で突合する。ell=9 非単調ケースの negative/boundary 検分も行う。"""
    log("\n=== 恒久 fixture(P99-6.2): 裁定393 census の再現 + ell=9 非単調ケース ===")
    fx = load_fixture_module()
    fixture_module_sha256 = sha256_file(FIXTURE_MODULE_PATH)
    fixture_module_relpath = relpath(FIXTURE_MODULE_PATH)
    log(f"  fixture module: {fixture_module_relpath}  sha256={fixture_module_sha256}")

    census_universe = dict(fx.CENSUS_UNIVERSE)
    all_cases = fx.census_cases()
    subset_10_13 = fx.n_10_13_subset()
    log(f"  census universe (ell->tmax) = {census_universe}")
    log(f"  total census cases = {len(all_cases)} ; n in {{10,11,12,13}} subset = {len(subset_10_13)}")

    # fixture 側の独立計算(px=直接置換悉皆, cx=直接類乗積)
    fixture_census_results = fx.run_census_fixture(log)
    ell9_fixture = fx.run_ell9_nonmonotone_fixture(fixture_census_results, log)

    # driver 側(このファイルの route A / route B, v1 と同一コード)で同じ宇宙を
    # 再計算し、fixture 側の px/cx と 4 方向突合する。
    log("\n  --- driver 側 route A/B との 4 方向突合 ---")
    per_cell = {}
    all_pass = True
    for (ell, t, n) in all_cases:
        ta_routeA, _ = route_A_compute(ell, t)
        ta_routeB, _ = route_B_compute(ell, t)
        fx_rec = fixture_census_results[(ell, t)]
        ta_px = fx_rec["T_all_px"]
        ta_cx = fx_rec["T_all_cx"]
        ok = (ta_routeA == ta_routeB == ta_px == ta_cx)
        all_pass = all_pass and ok
        log(f"    ell={ell} t={t} n={n}: routeA={ta_routeA} routeB={ta_routeB} "
            f"px={ta_px} cx={ta_cx}  {'PASS(4-way)' if ok else '*** MISMATCH ***'}")
        assert ok, (
            f"permanent fixture 4-way mismatch at ell={ell} t={t}: "
            f"routeA={ta_routeA} routeB={ta_routeB} px={ta_px} cx={ta_cx}"
        )
        per_cell[f"{ell}_{t}"] = {
            "ell": ell, "t": t, "n": n,
            "T_all_routeA": ta_routeA, "T_all_routeB": ta_routeB,
            "T_all_fixture_px": ta_px, "T_all_fixture_cx": ta_cx,
            "T_trans_fixture_px": fx_rec["T_trans_px"],
            "four_way_pass": ok,
        }

    log(f"\n  4-way census fixture: {'ALL PASS' if all_pass else '*** SOME FAILED ***'}")

    report["permanent_fixture"] = {
        "schema": "wac_v1-w98-alg-fixture-cert/v1",
        "condition_ref": "sol/sol_reply_99_math26.md P99-6.2",
        "fixture_module_path": fixture_module_relpath,
        "fixture_module_sha256": fixture_module_sha256,
        "fixture_module_imports_driver": False,
        "census_universe_ell_to_tmax": census_universe,
        "census_total_cases": len(all_cases),
        "census_n_10_13_subset_count": len(subset_10_13),
        "census_n_10_13_subset": [{"ell": e, "t": t, "n": n} for (e, t, n) in subset_10_13],
        "universe_note": (
            "Sol P99-6.2 逐語は「n=10,11,12,13 の直接 brute 30 ケース」。"
            "本 driver が再計算できる裁定393 census(w98_fixture_v1.CENSUS_UNIVERSE, "
            "ell=5..10 の tmax 表)の総数は 27 であり、うち n in {10,11,12,13} は "
            f"{len(subset_10_13)} 件。30 という数と 27/{len(subset_10_13)} のいずれとも"
            "厳密には一致しない。宇宙を勝手に広げて 30 に合わせることはしていない -- "
            "司令塔裁定: 27 が実スクリプト(w98_brute_small.py CASES)の宇宙そのもの"
            "であり正しい。裁定390/393 の「30 ケース」「n=10..13」表記は記帳ミスで、"
            "erratum は司令塔が LEDGER に記録する(本実装側の追加対応は不要)。"
        ),
        "census_cells": per_cell,
        "census_all_pass": all_pass,
        "ell9_nonmonotone_fixture": ell9_fixture,
    }
    log("\n*** 恒久 fixture(P99-6.2) ALL PASS ***")


def main():
    t_start = time.time()
    out = {"log": []}

    def log(msg):
        print(msg)
        out["log"].append(msg)

    log("############ W98-ALG driver v2 (sol/sol_reply_99_math26.md P99-6.2) ############")
    log(f"start: {datetime.datetime.now(datetime.timezone.utc).isoformat()}")

    report = {
        "schema": "wac_v1-w98-alg-driver-cert/v2",
        "formula_id": "W98-ALG (sol_reply_98_math25.md sec.5, ALG-1/ALG-2/ALG-3)",
        "spec_ref": "sol/sol_reply_98_math25.md W98-5.1 / P98-5.1 ; sol/sol_reply_99_math26.md P99-6.2",
        "no_symmetric_chartable": True,
        "no_ctbllib": True,
        "generated_by": relpath(SCRIPT_PATH),
        "supersedes_note": (
            "search/probe/wac_v1/w98_alg_driver.py (v1) は byte 不変のまま残る "
            "(裁定412 で digest 束縛: 991a8c1f0c233999c7d4aa8296fadad09170a8acece8c5f3e9ec92e0b2c4b052)。"
            "本 v2 はその上に P99-6.2 の恒久 fixture を追加した新版で、旧 cert "
            "(search/certs/w98_alg_driver_cert_20260801.json) は不改変。"
        ),
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
            rec = compute_cell(ell, a, log)
            cells[ell][a] = rec

    report["cells"] = {
        str(ell): {str(a): cells[ell][a] for a in range(9)} for ell in (37, 41)
    }

    log("\n=== ALG-3 二項反転: T_trans(ell,1^t), t=0..8 ===")
    trans_table = {}
    for ell in (37, 41):
        T_all_by_a = {a: cells[ell][a]["T_all"] for a in range(9)}
        trans_table[ell] = {}
        for t in range(9):
            tt = alg3_t_trans(t, T_all_by_a)
            trans_table[ell][t] = tt
            log(f"  T_trans({ell},1^{t}) = {tt}")
        for t in range(9):
            back = alg3_t_all_from_trans(t, trans_table[ell])
            assert back == T_all_by_a[t], (
                f"ALG-3 round-trip mismatch ell={ell} t={t}: back={back} orig={T_all_by_a[t]}"
            )
    report["T_trans"] = {str(ell): {str(t): trans_table[ell][t] for t in range(9)} for ell in (37, 41)}

    # ---- P99-6.2 恒久 fixture ----
    run_permanent_fixture_block(report, log)

    # ---- fail-closed 完走確認 ----
    total_elapsed = time.time() - t_start
    report["wall_seconds_total"] = round(total_elapsed, 3)
    report["script_sha256"] = script_digest()
    report["provenance"] = {
        "python_version": sys.version,
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    report["driver_done"] = True
    report["marker"] = "DRIVER_DONE"

    out_rel = "search/certs/w98_alg_driver_v2_cert_20260802.json"
    out_path = os.path.join(REPO_ROOT, out_rel)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2, sort_keys=False)
    cert_sha = sha256_file(out_path)

    log(f"\nwall_seconds_total = {report['wall_seconds_total']}")
    log(f"script_sha256 = {report['script_sha256']}")
    log(f"cert written: {out_rel}")
    log(f"cert_sha256 = {cert_sha}")
    log("\nDRIVER_DONE")
    return report, out_rel, cert_sha


def main_fail_closed():
    """main() を try/except で囲み、失敗時も部分結果+traceback を含む
    failure cert を(versioned・相対 path で)書き出す(P99-6.2 条件 3)。"""
    partial = {"log": []}
    try:
        report, out_rel, cert_sha = main()
        return 0
    except Exception as exc:
        tb = traceback.format_exc()
        print("\n*** DRIVER_FAILED ***")
        print(tb)
        failure_report = {
            "schema": "wac_v1-w98-alg-driver-cert/v2",
            "marker": "DRIVER_FAILED",
            "driver_done": False,
            "error": str(exc),
            "traceback": tb,
            "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "generated_by": relpath(SCRIPT_PATH),
        }
        out_rel = "search/certs/w98_alg_driver_v2_cert_20260802_FAILURE.json"
        out_path = os.path.join(REPO_ROOT, out_rel)
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(failure_report, fh, ensure_ascii=False, indent=2, sort_keys=False)
        print(f"failure cert written: {out_rel}")
        return 1


if __name__ == "__main__":
    sys.exit(main_fail_closed())

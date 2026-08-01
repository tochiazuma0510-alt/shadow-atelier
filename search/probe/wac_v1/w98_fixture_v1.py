# -*- coding: utf-8 -*-
"""
w98_fixture_v1.py -- W98-ALG 恒久 fixture: 独立実装(route A/B 非依存)。

Sol P99-6.2(sol/sol_reply_99_math26.md 六節)の条件に基づく:
  1. n=10,11,12,13 を含む 裁定393 の直接 brute 総当たり census を固定 fixture 化する。
  2. ell=9 の非単調消滅ケース(t=0..4 で T_trans が 36,54,0,18,0 と非単調に落ちる)を、
     「落ち方を区別する」negative/boundary fixture として固定する。
  5. この fixture は search/probe/wac_v1/w98_alg_driver.py および
     search/probe/wac_v1/w98_alg_driver_v2.py の route A / route B のコード・関数を
     一切 import しない。ここで実装するのは
       (i)  直接置換(permutation)悉皆: order-3 元 h を全列挙し g=w o h^-1 が
            対合(g^2=1)になる対を数える。
       (ii) 直接類乗積(class multiplication): 共役類サイズと Murnaghan-Nakayama
            指標(この fixture 内で独立に再導出)から類乗積係数を計算する。
     (i)/(ii) は本ファイル内で互いにコード共有せず(prefix px_ / cx_ で分離)、
     どちらも driver 側の route A / route B / v1 のどの関数も呼ばない。

宇宙(事前登録・固定): CENSUS_UNIVERSE = 裁定393(2026-08-01)で実際に走らせた
  ell -> t の上限表(w98_brute_small.py の CASES 定義を恒久化したもの)。
  この宇宙は本 fixture 化に際して勝手に広げても絞ってもいない
  (ell=5..10, t は各 ell の tmax まで)。うち n=ell+t が {10,11,12,13} に入る
  13 ケースが Sol P99-6.2 条件文の "n=10,11,12,13" に直接該当する部分集合。
  Sol 条件文は同時に「30 ケース」とも書くが、裁定393 の LEDGER 記述文言は
  「総当たり 30 ケース(n<=13)」であり、本 fixture が独立に再計算できる
  裁定393 census の総数は 27(この宇宙一杯)である。30 と 27 の差は本ファイルの
  設計判断では埋めない(宇宙を勝手に広げて 30 に合わせることをしない) --
  司令塔への報告事項として実装レポートに明記する。
"""

import sys
import os
import json
import math
import time
import hashlib
import datetime
from fractions import Fraction
from collections import defaultdict

SCRIPT_PATH = os.path.abspath(__file__)

# ============================================================================
# 宇宙(事前登録): 裁定393 の brute census を恒久化した ell -> tmax 表
# ============================================================================

CENSUS_UNIVERSE = {5: 3, 6: 3, 7: 4, 8: 4, 9: 4, 10: 3}


def census_cases():
    """(ell, t, n) の全リスト(裁定393 census 順)。"""
    out = []
    for ell in sorted(CENSUS_UNIVERSE):
        for t in range(CENSUS_UNIVERSE[ell] + 1):
            out.append((ell, t, ell + t))
    return out


def n_10_13_subset():
    return [(ell, t, n) for (ell, t, n) in census_cases() if 10 <= n <= 13]


# ============================================================================
# (i) px_ -- 直接置換悉皆(order-3 元列挙 + 対合判定)
# ============================================================================

def px_order3_elements(n):
    """h^3=1 なる h in S_n を list 表現(h[i]=h(i))として全列挙する。
    固定点 + 互いに素な 3-cycle の集合として再帰構成する。"""
    h = list(range(n))
    used = [False] * n

    def rec(start):
        while start < n and used[start]:
            start += 1
        if start == n:
            yield tuple(h)
            return
        used[start] = True
        yield from rec(start + 1)
        for b in range(start + 1, n):
            if used[b]:
                continue
            used[b] = True
            for c in range(b + 1, n):
                if used[c]:
                    continue
                used[c] = True
                for (x, y, z) in ((b, c, start), (c, start, b)):
                    h[start], h[b], h[c] = x, y, z
                    yield from rec(start + 1)
                h[start], h[b], h[c] = start, b, c
                used[c] = False
            used[b] = False
        used[start] = False

    yield from rec(0)


def px_w_target(ell, t):
    """w = (ell,1^t) を list 表現で返す(n=ell+t 上の一つの長サイクル + 固定点)。"""
    n = ell + t
    w = list(range(n))
    for i in range(ell - 1):
        w[i] = i + 1
    w[ell - 1] = 0
    return w


def px_brute_T_all(ell, t):
    """T_all(ell,1^t) = #{(g,h): g^2=1, h^3=1, g o h = w} を直接悉皆で数える。
    合成規約: (g o h)[i] = g[h[i]]。g o h = w  <=>  g[j] = w[h^{-1}[j]]。"""
    n = ell + t
    w = px_w_target(ell, t)
    cnt = 0
    for h in px_order3_elements(n):
        hinv = [0] * n
        for i in range(n):
            hinv[h[i]] = i
        g = [w[hinv[j]] for j in range(n)]
        ok = True
        for j in range(n):
            if g[g[j]] != j:
                ok = False
                break
        if ok:
            cnt += 1
    return cnt


def px_binom_T_trans(t, T_all_by_a):
    """ALG-3 の二項反転そのもの(公開済み厳密公式・driver からの import ではなく
    ここで直接評価する)。T_trans(ell,1^t) = sum_a (-1)^{t-a} C(t,a) T_all(ell,1^a)。"""
    total = 0
    for a in range(t + 1):
        total += ((-1) ** (t - a)) * math.comb(t, a) * T_all_by_a[a]
    return total


# ============================================================================
# (ii) cx_ -- 直接類乗積(class multiplication, Murnaghan-Nakayama 再導出)
# ============================================================================
#   N(K_2,K_3) = (|K_2||K_3|/n!) * sum_lambda chi^lambda(K_2) chi^lambda(K_3)
#                                              chi^lambda(w) / f^lambda
#   ここでの chi^lambda(rho) は本 fixture 内で独立に beta-set / rim-hook 除去
#   演算として再導出する(driver route A の rA_chi_ell1a, route B の
#   rB_add_rim_hooks, w98_classmult.py の chi_uniform のいずれとも
#   コードを共有しない独立実装)。

def cx_partitions(n, cap=None):
    if cap is None:
        cap = n
    if n == 0:
        yield ()
        return
    top = min(n, cap)
    for first in range(top, 0, -1):
        for rest in cx_partitions(n - first, first):
            yield (first,) + rest


def cx_beta(lam, L):
    padded = list(lam) + [0] * (L - len(lam))
    return tuple(padded[i] + (L - 1 - i) for i in range(L))


def cx_lambda_from_beta(beta):
    b = sorted(beta, reverse=True)
    L = len(b)
    lam = tuple(b[i] - (L - 1 - i) for i in range(L))
    return tuple(x for x in lam if x > 0)


_CX_HOOK_MEMO = {}


def cx_hook_f(lam):
    n = sum(lam)
    if n == 0:
        return 1
    if lam in _CX_HOOK_MEMO:
        return _CX_HOOK_MEMO[lam]
    conj = [0] * (lam[0] if lam else 0)
    for p in lam:
        for j in range(p):
            conj[j] += 1
    prod = 1
    for i, p in enumerate(lam):
        for j in range(p):
            arm = p - 1 - j
            leg = conj[j] - 1 - i
            prod *= (arm + leg + 1)
    fact = math.factorial(n)
    assert fact % prod == 0, "cx_hook_f: hook product does not divide n! (bug)"
    val = fact // prod
    _CX_HOOK_MEMO[lam] = val
    return val


def cx_chi_uniform_plus_ones(lam, block, ones):
    """chi^lambda(block, 1^ones) : 長さ block の rim hook を 1 本剥がして
    残りが全て 1^ones であることを直接検算しつつ計算する。"""
    n = sum(lam)
    assert n == block + ones
    L = len(lam)
    if L == 0:
        return 0
    beta = cx_beta(lam, L)
    bset = set(beta)
    total = 0
    for idx in range(L):
        b = beta[idx]
        bp = b - block
        if bp < 0 or bp in bset:
            continue
        newbeta = list(beta)
        newbeta[idx] = bp
        height = sum(1 for y in bset if bp < y < b)
        mu = cx_lambda_from_beta(newbeta)
        # 残り mu は恒等類 1^ones の上で評価する: chi^mu(1^ones) = f^mu
        # (mu の「形」を all-ones に限定するのは誤り -- 恒等類の指標は次元 f^mu)。
        if sum(mu) != ones:
            continue
        f_mu = cx_hook_f(mu)
        total += ((-1) ** height) * f_mu
    return total


def cx_lambdas_with_hook(block, ones):
    """chi^lambda(block,1^ones) が非零になり得る lambda を mu |- ones に長さ block
    の rim hook を「追加」して生成する(route B とは別コード列)。"""
    out = set()
    for mu in cx_partitions(ones):
        L = max(len(mu), 1) + block + 2
        padded = list(mu) + [0] * (L - len(mu))
        beta = [padded[i] + (L - 1 - i) for i in range(L)]
        bset = set(beta)
        for idx in range(L):
            bp = beta[idx] + block
            if bp in bset:
                continue
            newbeta = list(beta)
            newbeta[idx] = bp
            out.add(cx_lambda_from_beta(newbeta))
    return sorted(out)


def cx_class_size(n, cyc_counts):
    """共役類サイズ n!/z_rho。cyc_counts: {part_length: multiplicity}。"""
    z = 1
    for part, mult in cyc_counts.items():
        z *= (part ** mult) * math.factorial(mult)
    fact = math.factorial(n)
    assert fact % z == 0
    return fact // z


def cx_class_mult_T_all(ell, t):
    """T_all(ell,1^t) を類乗積(class multiplication)から直接計算する。
    K_2 = involution 全体の合併類(すべての 2^k1^{n-2k} をまとめて足す)、
    K_3 = order-3 元全体の合併類(3^k1^{n-3k})とし、
      T_all = sum over involution classes 2^k1^{n-2k}, order3 classes 3^j1^{n-3j}
              of N(class2, class3)
    を N の Murnaghan-Nakayama 直接式で積み上げる(driver の ALG-1/ALG-2 公式
    ではなく、各共役類ペアごとに定義どおりの類乗積を計算して和を取る --
    二項反転にも ALG-3 にも依存しない)。"""
    n = ell + t
    total = 0
    for k2 in range(0, n // 2 + 1):
        m2 = n - 2 * k2
        if m2 < 0:
            continue
        for k3 in range(0, n // 3 + 1):
            m3 = n - 3 * k3
            if m3 < 0:
                continue
            K2 = cx_class_size(n, {2: k2, 1: m2} if m2 else {2: k2})
            K3 = cx_class_size(n, {3: k3, 1: m3} if m3 else {3: k3})
            lambdas = cx_lambdas_with_hook(ell, t)
            s = Fraction(0)
            for lam in lambdas:
                cw = cx_chi_uniform_plus_ones(lam, ell, t)
                if cw == 0:
                    continue
                c2 = cx_chi_removed_2ktail(lam, k2, m2)
                if c2 == 0:
                    continue
                c3 = cx_chi_removed_3ktail(lam, k3, m3)
                if c3 == 0:
                    continue
                s += Fraction(c2 * c3 * cw, cx_hook_f(lam))
            val = Fraction(K2 * K3, math.factorial(n)) * s
            assert val.denominator == 1, f"cx_class_mult_T_all: non-integer at ell={ell} t={t} k2={k2} k3={k3}: {val}"
            total += int(val)
    return total


def cx_chi_removed_2ktail(lam, k2, m2):
    """chi^lambda(2^{k2} 1^{m2}) を k2 本の長さ2 rim hook を順に剥がして計算する。"""
    return _cx_chi_repeated_removed(lam, 2, k2, m2)


def cx_chi_removed_3ktail(lam, k3, m3):
    """chi^lambda(3^{k3} 1^{m3}) を k3 本の長さ3 rim hook を順に剥がして計算する。"""
    return _cx_chi_repeated_removed(lam, 3, k3, m3)


_CX_REP_MEMO = {}


def _cx_chi_repeated_removed(lam, r, k, m):
    """chi^lambda(r^k 1^m) を r-rim hook を k 本剥がし切って計算する(再帰、
    残り |lam|=m になった時点で f^lam を返す)。"""
    key = (lam, r, k, m)
    if key in _CX_REP_MEMO:
        return _CX_REP_MEMO[key]
    if k == 0:
        # 残り 0 本 = 恒等類 1^m。chi^lambda(1^m) = f^lambda(次元そのもの、
        # lambda の形に依らない)。
        val = cx_hook_f(lam) if sum(lam) == m else 0
        _CX_REP_MEMO[key] = val
        return val
    L = len(lam)
    if L == 0:
        _CX_REP_MEMO[key] = 0
        return 0
    beta = cx_beta(lam, L)
    bset = set(beta)
    total = 0
    for idx in range(L):
        b = beta[idx]
        bp = b - r
        if bp < 0 or bp in bset:
            continue
        newbeta = list(beta)
        newbeta[idx] = bp
        height = sum(1 for y in bset if bp < y < b)
        mu = cx_lambda_from_beta(newbeta)
        total += ((-1) ** height) * _cx_chi_repeated_removed(mu, r, k - 1, m)
    _CX_REP_MEMO[key] = total
    return total


# ============================================================================
# passport (Riemann-Hurwitz) の独立再導出(非単調ケースの「なぜ 0 か」を分離する)
# ============================================================================

def rh_passports(ell, t):
    """3 f2 + 4 f3 = ell + 6 - 5t - 12 gamma を満たす (f2,f3,gamma) を列挙する。
    空なら RH により T_trans=0 が強制される。空でないのに 0 になるのは別途
    数値的にしか確認できない偶然/構造("非単調"の正体そのもの)。"""
    n = ell + t
    out = []
    gamma = 0
    while True:
        rhs = ell + 6 - 5 * t - 12 * gamma
        if rhs < 0:
            break
        for f2 in range(0, n + 1):
            if (n - f2) % 2 or 3 * f2 > rhs:
                continue
            r = rhs - 3 * f2
            if r % 4:
                continue
            f3 = r // 4
            if f3 <= n and (n - f3) % 3 == 0:
                out.append((f2, f3, gamma))
        gamma += 1
    return out


# ============================================================================
# digest 補助
# ============================================================================

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def script_digest():
    with open(SCRIPT_PATH, "rb") as fh:
        return sha256_hex(fh.read())


# ============================================================================
# fixture 実行本体 -- 呼び出し側(v2 driver または単体実行)が使う API
# ============================================================================

def run_census_fixture(log=print):
    """裁定393 census(ell=5..10)を px_(直接置換)と cx_(直接類乗積)の両方で
    独立に計算し、相互に一致するかを assert する。fail-closed: 不一致は例外。
    戻り値: {(ell,t): {"n":..,"T_all_px":..,"T_all_cx":..,"T_trans_px":..,"pass":True/False}}"""
    results = {}
    for ell in sorted(CENSUS_UNIVERSE):
        tmax = CENSUS_UNIVERSE[ell]
        T_all_px_by_t = {}
        for t in range(tmax + 1):
            n = ell + t
            t0 = time.time()
            ta_px = px_brute_T_all(ell, t)
            ta_cx = cx_class_mult_T_all(ell, t)
            elapsed = time.time() - t0
            T_all_px_by_t[t] = ta_px
            tt_px = px_binom_T_trans(t, T_all_px_by_t)
            ok = (ta_px == ta_cx)
            results[(ell, t)] = {
                "n": n,
                "T_all_px": ta_px,
                "T_all_cx": ta_cx,
                "T_trans_px": tt_px,
                "pass": ok,
                "seconds": round(elapsed, 3),
            }
            log(f"  [census] ell={ell} t={t} n={n}: T_all(px)={ta_px} T_all(cx)={ta_cx} "
                f"T_trans(px)={tt_px}  {'PASS' if ok else '*** MISMATCH ***'}  ({elapsed:.2f}s)")
            assert ok, f"census fixture px/cx mismatch at ell={ell} t={t}: px={ta_px} cx={ta_cx}"
    return results


def run_ell9_nonmonotone_fixture(census_results, log=print):
    """ell=9 の非単調消滅ケース(negative/boundary fixture)。
    期待される「落ち方」: t=0..4 の T_trans(px) は 36,54,0,18,0 で、
      - t=2 は RH passport が空(数値的に理由が説明できる「構造的ゼロ」)
      - t=3 は t=2 が 0 の直後にもかかわらず非零(passport が再び開く)
      - t=4 は再び 0(この後は passport 空 = 恒久ゼロ側の入口)
    という非単調パターンを厳密数値で固定する。
    合わせて、「一度 0 を観測したら以降単調非増加」という誤った正規化仮定
    (naive monotone-envelope 仮定)がこのデータに対して破綻することを
    明示的に実演する(= 正規化バグの検出力の実演)。"""
    ell = 9
    tt_seq = [census_results[(ell, t)]["T_trans_px"] for t in range(5)]
    expected_seq = [36, 54, 0, 18, 0]
    log(f"  [ell=9 non-monotone] T_trans(px) t=0..4 = {tt_seq}  (期待 {expected_seq})")
    assert tt_seq == expected_seq, (
        f"ell=9 non-monotone fixture: sequence mismatch {tt_seq} != {expected_seq}"
    )

    passports_by_t = {t: rh_passports(ell, t) for t in range(5)}
    forced_zero = {t: (len(passports_by_t[t]) == 0) for t in range(5)}
    log(f"  [ell=9 non-monotone] RH passport 有無(空=強制ゼロ) t=0..4 = "
        f"{[not forced_zero[t] for t in range(5)]}")
    # t=0,1,3 は passport あり(非零になり得る)、t=2,4 は passport 空(強制ゼロ)
    expected_forced = {0: False, 1: False, 2: True, 3: False, 4: True}
    for t in range(5):
        assert forced_zero[t] == expected_forced[t], (
            f"ell=9 passport-forced-zero classification mismatch at t={t}: "
            f"got {forced_zero[t]} expected {expected_forced[t]}"
        )
        if forced_zero[t]:
            assert tt_seq[t] == 0, f"ell=9 t={t}: passport forced zero but T_trans={tt_seq[t]}"
        else:
            assert tt_seq[t] != 0, f"ell=9 t={t}: passport allows nonzero but T_trans=0"

    # 「一度 0 を見たら以後単調非増加(=恒久的に 0 以下)」という誤った正規化仮定を
    # このデータに適用すると破綻することを明示的に実演する(検出力の実演)。
    naive_monotone_would_predict_t3_zero = (tt_seq[2] == 0)
    actual_t3_nonzero = (tt_seq[3] != 0)
    monotone_bug_would_be_caught = naive_monotone_would_predict_t3_zero and actual_t3_nonzero
    log(f"  [ell=9 non-monotone] naive monotone-envelope 仮定は t=3 で破綻するか: "
        f"{monotone_bug_would_be_caught}")
    assert monotone_bug_would_be_caught, (
        "ell=9 non-monotone fixture: 期待していた「単調仮定が破綻する」性質が"
        "このデータで確認できない -- fixture 設計そのものの前提が崩れている(fail-closed)"
    )

    return {
        "ell": ell,
        "T_trans_px_seq_t0_4": tt_seq,
        "expected_seq": expected_seq,
        "passport_counts_t0_4": [len(passports_by_t[t]) for t in range(5)],
        "forced_zero_t0_4": [forced_zero[t] for t in range(5)],
        "monotone_bug_detector_fires": monotone_bug_would_be_caught,
    }


def main():
    out = {"log": []}

    def log(msg):
        print(msg)
        out["log"].append(msg)

    log("############ w98_fixture_v1.py -- 独立 fixture 単体実行 ############")
    log(f"start: {datetime.datetime.now(datetime.timezone.utc).isoformat()}")

    all_cases = census_cases()
    subset_10_13 = n_10_13_subset()
    log(f"census universe: {CENSUS_UNIVERSE}  (total cases = {len(all_cases)}, "
        f"n in 10..13 subset = {len(subset_10_13)})")

    census_results = run_census_fixture(log)
    ell9 = run_ell9_nonmonotone_fixture(census_results, log)

    out["census_universe"] = CENSUS_UNIVERSE
    out["census_total_cases"] = len(all_cases)
    out["n_10_13_subset_cases"] = [{"ell": e, "t": t, "n": n} for (e, t, n) in subset_10_13]
    out["census_results"] = {
        f"{ell}_{t}": census_results[(ell, t)] for (ell, t, n) in all_cases
    }
    out["ell9_nonmonotone_fixture"] = ell9
    out["script_sha256"] = script_digest()
    out["marker"] = "FIXTURE_DONE"
    log("\nFIXTURE_DONE")
    return out


if __name__ == "__main__":
    main()

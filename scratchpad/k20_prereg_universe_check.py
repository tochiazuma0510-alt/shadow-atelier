#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
K^(20) 事前登録票のための宇宙チェック(整数演算のみ・hexagon 走査ゼロ)

やること:
  (1) 正典 2405 Thm 4.3 (4.12) の閉じた式から |GT(K^(n))| を計算する関数を書き、
      既存証明書 K4/K8/K12/K16(4|n 枝)と K3/K5/K9/K15(奇枝)で照合する。
      -> 式の読み(4|n 追加条件 k = kappa(m)/2 mod 2、k は mod n/2)が正しいことの検証。
  (2) その式を n=20 に適用して列挙範囲(|X_20|, |GT(K^(20))|)を出す。
  (3) ★ m~=0 の項で phi_1 の持上げが存在するか(= 障害類が 0 か)を
      正典 Thm 4.3 の閉じた式だけから判定する。

注意: Im R の「実測」(hexagon 走査)は 1 行も含まない。すべて正典の閉じた式である。
"""
import json, os, sys

REPO = r"C:\Users\81905\Desktop\shadow-atelier"

FAILS = []
def check(name, got, want):
    ok = (got == want)
    if not ok:
        FAILS.append((name, got, want))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got={got} want={want}")
    return ok

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def K_ord(n):
    """定義ノート: K_ord^(n) = n (n 偶) / 2n (n 奇)"""
    return n if n % 2 == 0 else 2 * n

def kappa(m):
    """(4.9): kappa(m) = m+1 (m 奇) / -m (m 偶)"""
    return m + 1 if m % 2 == 1 else -m

def X(n):
    """charming set X_n = {m in Z/K_ord : gcd(2m+1, K_ord)=1}"""
    ko = K_ord(n)
    return [m for m in range(ko) if gcd(2 * m + 1, ko) == 1]

def GT_pairs(n):
    """Thm 4.3 (4.12): {(m, k)} ; k は mod ord(r^2)=n1 ; 4|n のとき k = kappa(m)/2 mod 2"""
    ko = K_ord(n)
    n1 = n // 2 if n % 2 == 0 else n   # ord(r^2): n 偶なら n/2、n 奇なら n
    out = []
    for m in X(n):
        for k in range(n1):
            if n % 4 == 0:
                km = kappa(m)
                assert km % 2 == 0, (n, m, km)
                if (k - km // 2) % 2 != 0:
                    continue
            out.append((m, k))
    return out

print("=" * 72)
print("Part A: Thm 4.3 (4.12) の読みを既存証明書で較正")
print("=" * 72)
for n in [3, 4, 5, 8, 9, 12, 15, 16]:
    path = os.path.join(REPO, "certificates", f"K{n}.v1.json")
    if not os.path.exists(path):
        print(f"  (skip) K{n}.v1.json なし")
        continue
    with open(path, encoding="utf-8") as fh:
        cert = json.load(fh)
    # shadow 数の欄をいくつか探す
    cand = None
    for key in ("shadows", "gt_shadows", "elements"):
        if isinstance(cert.get(key), list):
            cand = len(cert[key]); break
    if cand is None:
        for key in ("gt_count", "gt_order", "thm46_expected_order", "count"):
            if isinstance(cert.get(key), int):
                cand = cert[key]; break
    if cand is None:
        # ネストを一段だけ探す
        for k, v in cert.items():
            if isinstance(v, dict):
                for kk in ("gt_count", "gt_order", "count", "thm46_expected_order"):
                    if isinstance(v.get(kk), int):
                        cand = v[kk]; break
            if cand is not None:
                break
    pred = len(GT_pairs(n))
    check(f"|GT(K^({n}))| 式 vs cert", cand, pred)

print()
print("=" * 72)
print("Part B: n=20 の列挙範囲(事前登録の凍結値)")
print("=" * 72)
X20 = X(20)
G20 = GT_pairs(20)
print(f"  K_ord(20) = {K_ord(20)}")
print(f"  |X_20| = {len(X20)}   X_20 = {X20}")
print(f"  ord(r^2) in D_20 = {20//2}")
print(f"  |GT(K^(20))| = {len(G20)}")
check("|X_20| = 16 (campaign 3.7 W-3 行)", len(X20), 16)
check("K_ord(20) = 20 (campaign 3.7 W-3 行)", K_ord(20), 20)

# 参考: K^(5) 側
X5 = X(5)
G5 = GT_pairs(5)
check("|X_5| = 8", len(X5), 8)
check("|GT(K^(5))| = 40", len(G5), 40)

print()
print("=" * 72)
print("Part C: ★ m~ = 0 の項で phi_1 が持ち上がるか(障害類 = 0 か)")
print("=" * 72)
# phi_1 = [0, (rbar^2, rbar^-2, 1)] in GT(K^(5)) ; Theta_5 座標 k = 1
# 還元 R: (m~, k~) |-> (m~ mod K_ord(5)=10, f~ mod K^(5))
#   f-部: D_20 ->> D_5 は r |-> rbar (rbar^5=1) ゆえ第 1 成分 r^{2k~} |-> rbar^{2 k~ mod 5}
#   phi_1 の第 1 成分は rbar^2 ゆえ 2k~ = 2 (mod 5) <=> k~ = 1 (mod 5)
#   第 3 成分 r^{kappa(m~)} |-> rbar^{kappa(m~) mod 5}; phi_1 の第 3 成分は 1 ゆえ kappa(m~) = 0 (mod 5)
def reduces_to_phi1(m_t, k_t):
    if m_t % 10 != 0:
        return False
    if (2 * k_t - 2) % 5 != 0:
        return False
    if kappa(m_t) % 5 != 0:
        return False
    return True

lifts = [(m, k) for (m, k) in G20 if reduces_to_phi1(m, k)]
lifts_m0 = [(m, k) for (m, k) in lifts if m == 0]
lifts_m10 = [(m, k) for (m, k) in lifts if m == 10]
print(f"  phi_1 の持上げ全体            : {lifts}")
print(f"  そのうち m~ = 0  の項         : {lifts_m0}   <- 障害類が支配する項")
print(f"  そのうち m~ = 10 の項         : {lifts_m10}")
check("m~=0 の項に持上げが在る(=> 障害類 = 0)", len(lifts_m0) > 0, True)
check("m~=0 の持上げは k~=6 のちょうど 1 個", lifts_m0, [(0, 6)])
# 整合確認: m~=0 では 4|n 条件が k~ 偶を要求、k~=1 (mod 5) と合わせて k~=6
check("m~=0 で 4|n 条件は k~ 偶を要求", kappa(0) // 2 % 2, 0)
check("k~=6 は Z/10 で偶かつ 1 mod 5", (6 % 2, 6 % 5), (0, 1))

print()
print("=" * 72)
print(f"FAILS = {len(FAILS)}")
for f in FAILS:
    print("   ", f)
print("RESULT:", "ALL PASS" if not FAILS else "HAS FAILURES")

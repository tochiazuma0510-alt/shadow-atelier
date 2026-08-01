# -*- coding: utf-8 -*-
"""W98-ALG T_trans(37,1^6->1^7) の 1/10 段差 検分 (数学者独立検算)
 (1) cert の T_all から自前の二項反転で T_trans を再計算し cert 値と突合
 (2) Riemann-Hurwitz(種数 >= 0)による passport 必要条件を独立に列挙
 (3) T_trans / |C_{S_n}(w)| = T_trans/(ell * t!) = 重み付き dessin 数 の整数性
 (4) 消滅予測から T_all(ell,1^9) を予言(driver 再走で突合するため)
"""
import json, math, itertools, os

CERT = r"C:\Users\81905\Desktop\shadow-atelier\search\certs\w98_alg_driver_cert_20260801.json"
c = json.load(open(CERT, encoding="utf-8"))
Tall = {int(l): {int(a): v["T_all"] for a, v in d.items()} for l, d in c["cells"].items()}
Tcert = {int(l): {int(t): v for t, v in d.items()} for l, d in c["T_trans"].items()}

print("="*78)
print("(1) 独立二項反転  T_trans(l,1^t) = sum_a (-1)^(t-a) C(t,a) T_all(l,1^a)")
print("="*78)
mine = {}
for ell in (37, 41):
    mine[ell] = {}
    for t in range(9):
        s = sum((-1)**(t-a) * math.comb(t, a) * Tall[ell][a] for a in range(t+1))
        mine[ell][t] = s
        ok = "OK " if s == Tcert[ell][t] else "*** MISMATCH ***"
        print(f"  l={ell} t={t}: mine={s:>16d}  cert={Tcert[ell][t]:>16d}  {ok}")

print()
print("="*78)
print("(2) 種数 >= 0 の必要条件 (RH): 3*f2 + 4*f3 = ell + 6 - 5t - 12*gamma")
print("    f2=#fix(g) (g^2=1), f3=#fix(h) (h^3=1), n=ell+t, f2=n mod 2, f3=n mod 3")
print("="*78)
def passports(ell, t):
    n = ell + t
    out = []
    g = 0
    while True:
        rhs = ell + 6 - 5*t - 12*g
        if rhs < 0:
            break
        for f2 in range(0, n+1):
            if (n - f2) % 2 or 3*f2 > rhs:
                continue
            r = rhs - 3*f2
            if r % 4:
                continue
            f3 = r // 4
            if f3 > n or (n - f3) % 3:
                continue
            out.append((f2, f3, g))
        g += 1
    return out

for ell in (37, 41):
    print(f"  --- ell={ell} ---")
    for t in range(0, 12):
        ps = passports(ell, t)
        obs = Tcert[ell].get(t)
        obss = f"T_trans={obs}" if obs is not None else "T_trans=(未計算)"
        pred = "MUST BE 0" if not ps else f"{len(ps)} passports {ps[:6]}"
        print(f"    t={t:>2} n={ell+t:>2}: {pred:<62} {obss}")

print()
print("="*78)
print("(3) 正規化 D(t) = T_trans(l,1^t) / (ell * t!)   ( |C_{S_n}(w)| = ell*t! )")
print("="*78)
for ell in (37, 41):
    print(f"  --- ell={ell} ---")
    prev = None
    for t in range(9):
        cen = ell * math.factorial(t)
        v = Tcert[ell][t]
        q, r = divmod(v, cen)
        fac = []
        m = q
        d = 2
        while d*d <= m:
            while m % d == 0:
                fac.append(d); m //= d
            d += 1
        if m > 1: fac.append(m)
        ratio = ""
        if prev is not None and q:
            ratio = f"  D(t-1)/D(t)={prev/q:.6g}"
        print(f"    t={t}: D={q:<12d} rem={r}  factors={fac}{ratio}")
        prev = q

print()
print("="*78)
print("(4) 消滅予測からの T_all(l,1^t) 予言 (t>=9)")
print("    T_trans(l,1^t)=0 for t>=9 => T_all(l,1^t) = sum_{a<=8} C(t,a) T_trans(l,1^a)")
print("="*78)
for ell in (37, 41):
    for t in (9, 10):
        p = sum(math.comb(t, a) * Tcert[ell][a] for a in range(9))
        print(f"  predict T_all({ell},1^{t})  [n={ell+t}] = {p}")

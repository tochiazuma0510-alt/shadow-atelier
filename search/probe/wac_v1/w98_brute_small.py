# -*- coding: utf-8 -*-
"""小 ell 独立検証(指標理論を一切使わない第三ルート)
   T_all(ell,1^t) = #{(g,h): g^2=h^3=1, g o h = w} を h の直接列挙で数える
   -> 自前二項反転で T_trans -> RH passport 予測(特に消滅)と突合
   -> 同時に driver の route A / route B とも突合(n<=12 まで、cert の brute は n<=7 のみ)
"""
import sys, math, time, importlib.util
sys.setrecursionlimit(20000)

spec = importlib.util.spec_from_file_location(
    "drv", r"C:\Users\81905\Desktop\shadow-atelier\search\probe\wac_v1\w98_alg_driver.py")
drv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drv)


def order3_elements(n):
    """h^3 = 1 なる h を全列挙(互いに素な 3-cycle の集合)。yield: list h[i]=h(i)"""
    h = list(range(n))
    used = [False]*n

    def rec(start):
        while start < n and used[start]:
            start += 1
        if start == n:
            yield tuple(h)
            return
        used[start] = True
        # 固定点
        yield from rec(start+1)
        # 3-cycle (start, b, c)
        for b in range(start+1, n):
            if used[b]:
                continue
            used[b] = True
            for c in range(b+1, n):
                if used[c]:
                    continue
                used[c] = True
                for (x, y, z) in ((b, c, start), (c, start, b)):
                    h[start], h[b], h[c] = x, y, z
                    yield from rec(start+1)
                h[start], h[b], h[c] = start, b, c
                used[c] = False
            used[b] = False
        used[start] = False
    yield from rec(0)


def brute_T_all(ell, t):
    """driver と同じ合成規約: compose(g,h)[i] = g[h[i]] == w[i]  =>  g[j] = w[hinv[j]]"""
    n = ell + t
    w = list(range(n))
    for i in range(ell-1):
        w[i] = i+1
    w[ell-1] = 0
    cnt = 0
    rng = range(n)
    for h in order3_elements(n):
        hinv = [0]*n
        for i in rng:
            hinv[h[i]] = i
        g = [w[hinv[j]] for j in rng]
        ok = True
        for j in rng:
            if g[g[j]] != j:
                ok = False
                break
        if ok:
            cnt += 1
    return cnt


def passports(ell, t):
    n = ell + t
    out, gg = [], 0
    while True:
        rhs = ell + 6 - 5*t - 12*gg
        if rhs < 0:
            break
        for f2 in range(0, n+1):
            if (n-f2) % 2 or 3*f2 > rhs:
                continue
            r = rhs - 3*f2
            if r % 4:
                continue
            f3 = r//4
            if f3 <= n and (n-f3) % 3 == 0:
                out.append((f2, f3, gg))
        gg += 1
    return out


CASES = {5: 3, 6: 3, 7: 4, 8: 4, 9: 4, 10: 3}   # ell -> t の上限
print("ell  t   n   brute_T_all      routeA         routeB       | T_trans(自前反転)   RH予測    判定")
print("-"*118)
allok = True
for ell in sorted(CASES):
    tmax = CASES[ell]
    Ta = []
    for t in range(tmax+1):
        n = ell+t
        t0 = time.time()
        bf = brute_T_all(ell, t)
        rA, _ = drv.route_A_compute(ell, t)
        rB, _ = drv.route_B_compute(ell, t)
        Ta.append(bf)
        tt = sum((-1)**(t-a)*math.comb(t, a)*Ta[a] for a in range(t+1))
        ps = passports(ell, t)
        pred = "=0 (RHで強制)" if not ps else f"!=0可 ({len(ps)}pp)"
        ok = (bf == rA == rB) and ((tt == 0) if not ps else True)
        if not ok:
            allok = False
        print(f"{ell:>3} {t:>2} {n:>3}  {bf:>13d}  {rA:>13d}  {rB:>13d} | {tt:>15d}  {pred:<14} "
              f"{'OK' if ok else '*** FAIL ***'}  ({time.time()-t0:.1f}s)")
    print()
print("ALL CONSISTENT" if allok else "*** SOME FAILED ***")
print("BRUTE_DONE")

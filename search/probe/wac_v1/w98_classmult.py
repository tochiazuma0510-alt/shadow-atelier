# -*- coding: utf-8 -*-
"""ALG-3 非依存ルート: T_trans(37,1^t) を「類乗積定数」として直接計算する。
   RH により t=6,7,8 では許容 passport が唯一:
     t=6: (f2,f3)=(3,1) -> types (2^20 1^3, 3^14 1^1)
     t=7: (f2,f3)=(0,2) -> types (2^22,     3^14 1^2)   [f2=0 => 非推移対は存在しない]
     t=8: (f2,f3)=(1,0) -> types (2^22 1^1, 3^15)       [f3=0 => 非推移対は存在しない]
   類乗積: N(K2,K3) = (|K2||K3|/n!) * sum_lam chi(K2)chi(K3)chi(w)/f_lam
   二項反転も T_all も使わない。まず小 ell で brute force と突合して実装を較正する。
"""
import sys, math, time
from functools import lru_cache
sys.setrecursionlimit(100000)

# ---------- 分割 <-> beta 集合 / MN 則 ----------
def beta_of(lam):
    L = len(lam)
    return tuple(lam[i] + (L - 1 - i) for i in range(L))

def lam_of_beta(beta):
    b = sorted(beta, reverse=True)
    L = len(b)
    out = tuple(b[i] - (L - 1 - i) for i in range(L))
    return tuple(x for x in out if x > 0)

_hookmemo = {}
def f_lam(lam):
    n = sum(lam)
    if n == 0:
        return 1
    if lam in _hookmemo:
        return _hookmemo[lam]
    conj = [0] * (lam[0])
    for p in lam:
        for j in range(p):
            conj[j] += 1
    prod = 1
    for i, p in enumerate(lam):
        for j in range(p):
            prod *= (p - j) + (conj[j] - i) - 1
    assert math.factorial(n) % prod == 0
    v = math.factorial(n) // prod
    _hookmemo[lam] = v
    return v

_chimemo = {}
def chi_uniform(lam, r, tail):
    """chi^lam(r^k ∪ tail) を rim hook 長 r を剥がし切って計算(|lam| = r*k + |tail|)。
       tail は 1^m のみを想定(m=|lam| mod r 相当)。"""
    key = (lam, r, tail)
    v = _chimemo.get(key)
    if v is not None:
        return v
    n = sum(lam)
    if n == sum(tail):
        v = f_lam(lam) if all(x == 1 for x in tail) else None
        assert v is not None
        _chimemo[key] = v
        return v
    beta = beta_of(lam)
    bs = set(beta)
    total = 0
    for idx in range(len(beta)):
        b = beta[idx]
        bp = b - r
        if bp < 0 or bp in bs:
            continue
        nb = list(beta)
        nb[idx] = bp
        ht = sum(1 for y in bs if bp < y < b)
        total += ((-1) ** ht) * chi_uniform(lam_of_beta(nb), r, tail)
    _chimemo[key] = total
    return total

def chi_long_plus_ones(lam, ell, a):
    """chi^lam(ell, 1^a): 長さ ell の rim hook を 1 本剥がして f^mu を足す。"""
    beta = beta_of(lam)
    bs = set(beta)
    total = 0
    for idx in range(len(beta)):
        b = beta[idx]
        bp = b - ell
        if bp < 0 or bp in bs:
            continue
        nb = list(beta)
        nb[idx] = bp
        ht = sum(1 for y in bs if bp < y < b)
        mu = lam_of_beta(nb)
        assert sum(mu) == a
        total += ((-1) ** ht) * f_lam(mu)
    return total

def partitions(n, cap=None):
    if cap is None:
        cap = n
    if n == 0:
        yield ()
        return
    for first in range(min(n, cap), 0, -1):
        for rest in partitions(n - first, first):
            yield (first,) + rest

def lambdas_with_long_hook(ell, a):
    """chi^lam(ell,1^a) != 0 になり得る lam を mu |- a に ell-rim hook を足して直接生成。"""
    out = set()
    for mu in partitions(a):
        L = max(len(mu), 1) + ell + 2
        m = list(mu) + [0] * (L - len(mu))
        beta = [m[i] + (L - 1 - i) for i in range(L)]
        bs = set(beta)
        for idx in range(L):
            bp = beta[idx] + ell
            if bp in bs:
                continue
            nb = list(beta)
            nb[idx] = bp
            out.add(lam_of_beta(nb))
    return sorted(out)

def class_size(n, rho):
    """cycle type rho (list) の共役類の大きさ = n!/z_rho"""
    z = 1
    from collections import Counter
    cnt = Counter(rho)
    for part, mult in cnt.items():
        z *= (part ** mult) * math.factorial(mult)
    assert math.factorial(n) % z == 0
    return math.factorial(n) // z

def class_mult_count(ell, t, k2, m2, k3, m3):
    """w=(ell,1^t) 固定。g の型 = 2^k2 1^m2、h の型 = 3^k3 1^m3 の対の個数。"""
    n = ell + t
    assert 2*k2 + m2 == n and 3*k3 + m3 == n
    K2 = class_size(n, [2]*k2 + [1]*m2)
    K3 = class_size(n, [3]*k3 + [1]*m3)
    lams = lambdas_with_long_hook(ell, t)
    from fractions import Fraction
    s = Fraction(0)
    for lam in lams:
        cw = chi_long_plus_ones(lam, ell, t)
        if cw == 0:
            continue
        c2 = chi_uniform(lam, 2, tuple([1]*m2))
        if c2 == 0:
            continue
        c3 = chi_uniform(lam, 3, tuple([1]*m3))
        if c3 == 0:
            continue
        s += Fraction(c2 * c3 * cw, f_lam(lam))
    val = Fraction(K2 * K3, math.factorial(n)) * s
    assert val.denominator == 1, f"class mult not integer: {val}"
    return int(val)

# ---------- 較正: 小 ell を brute force と突合 ----------
def brute_class_count(ell, t, k2, m2, k3, m3):
    n = ell + t
    w = list(range(n))
    for i in range(ell-1):
        w[i] = i+1
    w[ell-1] = 0
    def cyc_type(p):
        seen = [False]*n
        ct = []
        for i in range(n):
            if not seen[i]:
                c = 0
                j = i
                while not seen[j]:
                    seen[j] = True
                    j = p[j]
                    c += 1
                ct.append(c)
        return tuple(sorted(ct, reverse=True))
    tgt2 = tuple(sorted([2]*k2 + [1]*m2, reverse=True))
    tgt3 = tuple(sorted([3]*k3 + [1]*m3, reverse=True))
    import itertools
    cnt = 0
    for h in itertools.permutations(range(n)):
        hh = tuple(h[h[i]] for i in range(n))
        if tuple(h[hh[i]] for i in range(n)) != tuple(range(n)):
            continue
        if cyc_type(h) != tgt3:
            continue
        hinv = [0]*n
        for i in range(n):
            hinv[h[i]] = i
        g = [w[hinv[j]] for j in range(n)]
        if any(g[g[j]] != j for j in range(n)):
            continue
        if cyc_type(g) != tgt2:
            continue
        cnt += 1
    return cnt

print("=== 較正: class_mult_count vs brute force (小 ell) ===")
CAL = [(5,1,3,0,2,0),(6,1,2,3,2,1),(7,2,4,1,3,0),(7,1,4,0,2,2),(8,2,5,0,3,1),(9,1,5,0,3,1)]
for (ell,t,k2,m2,k3,m3) in CAL:
    n = ell+t
    if 2*k2+m2 != n or 3*k3+m3 != n:
        print(f"  skip ell={ell} t={t} (型が n={n} に合わない)"); continue
    a = class_mult_count(ell,t,k2,m2,k3,m3)
    b = brute_class_count(ell,t,k2,m2,k3,m3)
    print(f"  ell={ell} t={t} n={n} g=2^{k2}1^{m2} h=3^{k3}1^{m3}: formula={a} brute={b} "
          f"{'OK' if a==b else '*** FAIL ***'}")

print()
print("=== ALG-3 非依存の T_trans(37,1^t), t=6,7,8 ===")
CERT = {6: 3199996800, 7: 319999680, 8: 639999360}
t0 = time.time()
# t=7: n=44, g=2^22, h=3^14 1^2  (f2=0 => 全て推移的)
v7 = class_mult_count(37, 7, 22, 0, 14, 2)
print(f"  t=7: N(2^22, 3^14 1^2) = {v7}   cert T_trans={CERT[7]}   "
      f"{'MATCH' if v7==CERT[7] else '*** MISMATCH ***'}   ({time.time()-t0:.1f}s)")
sys.stdout.flush()
t0 = time.time()
# t=8: n=45, g=2^22 1^1, h=3^15  (f3=0 => 全て推移的)
v8 = class_mult_count(37, 8, 22, 1, 15, 0)
print(f"  t=8: N(2^22 1, 3^15)   = {v8}   cert T_trans={CERT[8]}   "
      f"{'MATCH' if v8==CERT[8] else '*** MISMATCH ***'}   ({time.time()-t0:.1f}s)")
sys.stdout.flush()
t0 = time.time()
# t=6: n=43, g=2^20 1^3, h=3^14 1^1。非推移対は「1 点だけ singleton」型のみ可能:
#      6 通りの選び方 x (n=42, w=(37,1^5), g=2^20 1^2, h=3^14) の推移対
v6raw = class_mult_count(37, 6, 20, 3, 14, 1)
v6sub = class_mult_count(37, 5, 20, 2, 14, 0)
v6 = v6raw - 6 * v6sub
print(f"  t=6: N(2^20 1^3, 3^14 1) = {v6raw} ; 非推移補正 6*N_42(2^20 1^2,3^14)=6*{v6sub}")
print(f"       => T_trans = {v6}   cert T_trans={CERT[6]}   "
      f"{'MATCH' if v6==CERT[6] else '*** MISMATCH ***'}   ({time.time()-t0:.1f}s)")
print()
print(f"  段差比 t=6 -> t=7 (ALG-3 非依存値): {v6} / {v7} = {v6/v7}")
print("CLASSMULT_DONE")

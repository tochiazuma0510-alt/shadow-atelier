"""W-Exist 検証用: 算術入力(S5 / S4 の Q 上実現)と可解性の検算.
整数演算のみ. 外部ライブラリなし."""
from itertools import permutations, product

# ---------- 1. x^5 - x - 1 : disc = 256a^5 + 3125b^4 with a=b=-1 ----------
a, b = -1, -1
disc5 = 256 * a**5 + 3125 * b**4
def isqrt_exact(n):
    if n < 0: return None
    r = int(n**0.5)
    while r*r > n: r -= 1
    while (r+1)*(r+1) <= n: r += 1
    return r if r*r == n else None
def factor(n):
    n = abs(n); fs = []; d = 2
    while d*d <= n:
        while n % d == 0: fs.append(d); n //= d
        d += 1
    if n > 1: fs.append(n)
    return fs
print("[1] disc(x^5-x-1) =", disc5, "factors", factor(disc5),
      "perfect square?", isqrt_exact(disc5) is not None, " odd?", disc5 % 2 == 1)

# ---------- 2. mod 2 factorization (x^2+x+1)(x^3+x^2+1) = x^5+x+1 ----------
def polymul_F2(p, q):
    r = [0]*(len(p)+len(q)-1)
    for i, pi in enumerate(p):
        for j, qj in enumerate(q):
            r[i+j] ^= (pi & qj)
    return r
p2 = [1,1,1]        # 1 + x + x^2
p3 = [1,0,1,1]      # 1 + x^2 + x^3
prod = polymul_F2(p2, p3)
target = [1,1,0,0,0,1]  # 1 + x + x^5  ==  x^5 - x - 1 mod 2
print("[2] (x^2+x+1)(x^3+x^2+1) =", prod, " == x^5+x+1 ?", prod == target)
# irreducibility of the two factors over F2 (no roots; degrees 2,3)
ev = lambda c, t: sum(ci*(t**i) for i, ci in enumerate(c)) % 2
print("    x^2+x+1 roots in F2:", [t for t in (0,1) if ev(p2,t)==0],
      "| x^3+x^2+1 roots in F2:", [t for t in (0,1) if ev(p3,t)==0])

# ---------- 3. x^5-x-1 irreducible over Z (rational roots + deg2*deg3 over Z) ----------
def has_int_root(coeffs):  # coeffs low->high, monic, constant c0 -> divisors of c0
    c0 = coeffs[0]
    cands = set()
    for d in range(1, abs(c0)+1):
        if c0 % d == 0: cands |= {d, -d}
    return [t for t in cands if sum(c*(t**i) for i, c in enumerate(coeffs)) == 0]
f5 = [-1,-1,0,0,0,1]
print("[3] rational roots of x^5-x-1:", has_int_root(f5))
# (x^2+ax+b)(x^3+cx^2+dx+e) = x^5-x-1 over Z ; b*e = -1 so (b,e) in {(1,-1),(-1,1)}
sols = []
for bb, ee in ((1,-1), (-1,1)):
    for aa in range(-6, 7):
        for cc in range(-6, 7):
            for dd in range(-6, 7):
                g = polymul_int([1, aa, bb][::-1], [1, cc, dd, ee][::-1]) if False else None
                # expand manually: (x^2+aa x+bb)(x^3+cc x^2+dd x+ee)
                co = [bb*ee, bb*dd + aa*ee, bb*cc + aa*dd + ee, bb + aa*cc + dd, aa + cc, 1]
                if co == f5: sols.append((aa,bb,cc,dd,ee))
print("    Z-factorizations deg2*deg3 found:", sols)

# ---------- 4. x^4-x-1 : disc = -27p^4+256q^3, resolvent cubic x^3-4qx-p^2 ----------
p, q = -1, -1
disc4 = -27*p**4 + 256*q**3
print("[4] disc(x^4-x-1) =", disc4, " perfect square?", isqrt_exact(disc4) is not None)
res = [-p*p, -4*q, 0, 1]   # x^3 - 4q x - p^2 = x^3 + 4x - 1
print("    resolvent cubic x^3+4x-1 rational roots:", has_int_root(res))
f4 = [-1,-1,0,0,1]
print("    rational roots of x^4-x-1:", has_int_root(f4))
sols4 = []
for bb, ee in ((1,-1), (-1,1)):
    for aa in range(-6,7):
        for cc in range(-6,7):
            co = [bb*ee, bb*cc + aa*ee, bb + aa*cc + ee, aa + cc, 1]
            if co == f4: sols4.append((aa,bb,cc,ee))
print("    Z-factorizations deg2*deg2:", sols4)

# ---------- 5. derived series of S4, S5 (brute force) ----------
def mul(p_, q_): return tuple(p_[q_[i]] for i in range(len(q_)))
def gen_group(gens, n):
    G = {tuple(range(n))}
    frontier = [tuple(range(n))]
    while frontier:
        new = []
        for g in frontier:
            for s in gens:
                h = mul(g, s)
                if h not in G: G.add(h); new.append(h)
        frontier = new
    return G
def inv(p_):
    r = [0]*len(p_)
    for i, v in enumerate(p_): r[v] = i
    return tuple(r)
def derived(G, n):
    comms = set()
    for g in G:
        for h in G:
            comms.add(mul(mul(g, h), mul(inv(g), inv(h))))
    return gen_group(list(comms), n)
def derived_length(G, n):
    d = 0; cur = G
    while len(cur) > 1:
        nxt = derived(cur, n)
        if len(nxt) == len(cur): return None      # perfect core -> non-solvable
        cur = nxt; d += 1
    return d
for n in (4, 5):
    Sn = set(permutations(range(n)))
    dl = derived_length(Sn, n)
    print(f"[5] |S{n}| = {len(Sn)}  derived length =", dl if dl is not None else "INFINITE (non-solvable)")

# ---------- 6. the C2F-style corollary check on a toy: G/ker abelian & ker solvable => G solvable ----------
print("[6] (checked on paper: 1->ker->G->abelian->1 with ker solvable => G solvable)")

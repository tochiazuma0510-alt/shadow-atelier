# TW probe v3: orientation / twist-rigidity mechanism.  Pure finite groups, integers only.
# (O1) Is H conjugate to XHX^{-1} inside AH?   (expected NO, because N_G(H)=H)
# (O2) rotation ratio r_inf/r_0 read on block 1 vs block 2 (expected: r and -r)
# (O3) does the AH-block system get swapped by X?  (expected YES)
import sys
sys.path.insert(0, ".")
from tw_blocks import QTAB

def run(n, alpha):
    def enc(v, q): return ((v[0]*n + v[1])*n + v[2])*4 + q
    def dec(x):
        q = x % 4; x //= 4
        c = x % n; x //= n
        return (x // n, x % n, c), q
    def act(q, v):
        if q == 0: return v
        return tuple(v[j] if (j+1) == q else (-v[j]) % n for j in range(3))
    def mul(x, y):
        v, q = dec(x); w, r = dec(y); aw = act(q, w)
        return enc(tuple((v[j]+aw[j]) % n for j in range(3)), QTAB[q][r])
    def inv(x):
        v, q = dec(x); return enc(act(q, tuple((-t) % n for t in v)), q)

    G = list(range(4*n**3))
    U = [((alpha*t) % n, s % n, t % n) for s in range(n) for t in range(n)]
    H = [enc(v, q) for v in U for q in (0, 2)]
    Hset = set(H)
    AH = [enc((a,b,c), q) for a in range(n) for b in range(n) for c in range(n) for q in (0,2)]

    X  = enc((1,0,0), 1)
    Y  = enc((1,1,1), 2)
    XY = mul(X, Y)
    Z  = inv(XY)
    X2 = mul(X, X); Z2 = mul(Z, Z)

    # (O1)
    XHX = set(mul(mul(X, h), inv(X)) for h in H)
    conj_in_AH = any(set(mul(mul(g, h), inv(g)) for h in XHX) == Hset for g in AH)

    # cosets
    def coset(g): return min(mul(g, h) for h in H)
    cid = {}; reps = []
    canon = {}
    for g in G:
        c = coset(g)
        if c not in cid:
            cid[c] = len(reps); reps.append(c)
        canon[g] = cid[c]
    L = len(reps)
    def app(g, k): return canon[mul(g, reps[k])]

    # blocks
    seen = [-1]*L; nb = 0
    for k in range(L):
        if seen[k] != -1: continue
        st=[k]; seen[k]=nb
        while st:
            x = st.pop()
            for g in AH:
                y = app(g, x)
                if seen[y] == -1: seen[y]=nb; st.append(y)
        nb += 1
    blocks = [[k for k in range(L) if seen[k]==b] for b in range(nb)]

    # (O3)
    X_swaps = (seen[app(X, blocks[0][0])] != 0)

    # (O2) ratio on each block
    ratios = []
    for b in blocks:
        p = b[0]
        phi = {}; x = p
        for j in range(n):
            phi[x] = j; x = app(X2, x)
        assert x == p and len(phi) == n, "X^2 not an n-cycle on the block"
        r = phi[app(Z2, p)]
        # consistency: Z^2 must act as the same translation from every point
        ok = all((phi[app(Z2, y)] - phi[y]) % n == r for y in b)
        ratios.append((r, ok))
    print({"n": n, "alpha": alpha,
           "H~XHX^-1 in AH": conj_in_AH,
           "X swaps blocks": X_swaps,
           "ratio r_inf/r_0 per block": [r for r, _ in ratios],
           "translation-consistent": [o for _, o in ratios],
           "sum of the two ratios mod n": (ratios[0][0] + ratios[1][0]) % n},
          flush=True)

if __name__ == "__main__":
    for n in (3, 7, 9, 11, 13):          # n=5 skipped (freeze U7-NO5)
        for a in range(1, (n-1)//2 + 1):
            run(n, a)

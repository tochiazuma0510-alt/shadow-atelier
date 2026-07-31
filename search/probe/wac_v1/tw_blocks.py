# TW probe v2 (fast): pure finite-group check, integers only.
# NO contact with curves, lambda, u, valuations. n=5 deliberately skipped (freeze U7-NO5).
import sys

QTAB = [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]]

def run(n, alpha):
    N4 = 4
    def enc(v, q): return ((v[0]*n + v[1])*n + v[2])*4 + q
    def dec(x):
        q = x % 4; x //= 4
        c = x % n; x //= n
        b = x % n; a = x // n
        return (a, b, c), q
    def act(q, v):
        if q == 0: return v
        return tuple(v[j] if (j+1) == q else (-v[j]) % n for j in range(3))
    def mul(x, y):
        v, q = dec(x); w, r = dec(y)
        aw = act(q, w)
        return enc(tuple((v[j]+aw[j]) % n for j in range(3)), QTAB[q][r])
    def inv(x):
        v, q = dec(x)
        return enc(act(q, tuple((-t) % n for t in v)), q)

    G = list(range(4*n**3))
    U = [((alpha*t) % n, s % n, t % n) for s in range(n) for t in range(n)]
    H = [enc(v, q) for v in U for q in (0, 2)]
    Hset = set(H)
    AH = set(enc((a,b,c), q) for a in range(n) for b in range(n) for c in range(n) for q in (0,2))

    # canonical rep of left coset gH
    def coset(g): return min(mul(g, h) for h in H)
    canon = {}
    reps = []
    cid = {}
    for g in G:
        c = coset(g)
        if c not in cid:
            cid[c] = len(reps); reps.append(c)
        canon[g] = cid[c]
    L = len(reps)
    def perm(g): return [canon[mul(g, reps[k])] for k in range(L)]

    e1 = enc((1,0,0), 1)            # X = a1 q1
    Yg = enc((1,1,1), 2)            # Y = a1 a2 a3 q2
    pX, pY = perm(e1), perm(Yg)

    NG = set(g for g in G if all(mul(mul(g, h), inv(g)) in Hset for h in H))
    core = set(Hset)
    for g in G:
        core &= set(mul(mul(g, h), inv(g)) for h in H)
    a2 = set(enc((0, s, 0), 0) for s in range(n))

    # blocks = AH-orbits on Lambda
    seen = [-1]*L; nb = 0
    for k in range(L):
        if seen[k] != -1: continue
        stack=[k]; seen[k]=nb
        while stack:
            x = stack.pop()
            for g in AH:
                y = canon[mul(g, reps[x])]
                if seen[y] == -1:
                    seen[y] = nb; stack.append(y)
        nb += 1
    blocks = [[k for k in range(L) if seen[k]==b] for b in range(nb)]

    def ctype(p, dom):
        dom = set(dom); typ=[]
        while dom:
            s = dom.pop(); c=1; x=p[s]
            while x != s:
                dom.discard(x); x=p[x]; c+=1
            typ.append(c)
        return tuple(sorted(typ, reverse=True))

    res = dict(
        n=n, alpha=alpha, sizeG=len(G), sizeH=len(H), L=L,
        N_eq_H=(NG == Hset), core_is_a2=(core == a2), sizeM=len(G)//len(core),
        blocks=[len(b) for b in blocks],
        X_swaps=(seen[pX[0]] != seen[0]),
        Y_keeps=all(seen[pY[k]] == seen[k] for k in range(L)),
        typeY=ctype(pY, range(L)),
        fixY_per_block=[sum(1 for k in b if pY[k]==k) for b in blocks],
        typeY_per_block=[ctype(pY, b) for b in blocks],
    )
    print(res, flush=True)
    return res

if __name__ == "__main__":
    ok = True
    for n in (3, 7, 9, 11, 13):
        for alpha in range(1, (n-1)//2 + 1):
            r = run(n, alpha)
            if r["core_is_a2"]:
                # for alpha a unit the design predicts: 2 blocks of size n, one Y-fixed pt each
                if r["blocks"] != [n, n] or r["fixY_per_block"] != [1, 1]:
                    ok = False; print("  *** MISMATCH ***", flush=True)
    print("ALL-CONSISTENT" if ok else "SOME-MISMATCH", flush=True)

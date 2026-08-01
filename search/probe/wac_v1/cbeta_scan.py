# C-beta stage-5 dispute diagnostic (裁定 306).
#  (A) convention scan : standard / inverted / reversed / inv+rev  (= right-action opposite)
#  (B) chi_P criterion  : exact equality  vs  full conjugacy class  vs  "same line"
# Integer arithmetic only.  Run from search/probe/wac_v1.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cbeta_nielsen import build as ab, pmul, pinv
from cbeta_model import model_group
from cbeta_recheck import conj_explicit, model_triples

N = 7

def conventions():
    out = {}
    for ap in (1, 2, 3):
        La, X, Y, Z, M = ab(N, ap)
        out[ap] = {"standard": (X, Y, Z),
                   "inverted": (pinv(X), pinv(Y), pinv(Z)),
                   "reversed": (Z, Y, X),
                   "inv+rev":  (pinv(Z), pinv(Y), pinv(X))}
    return out

def scanA():
    absd = conventions()
    print("=== (A) convention scan : which abstract alpha' does model(alpha) match ? ===")
    for a in (1, 2, 3):
        tri, n0, n1, ni, L = model_triples(a)
        row = {c: [ap for ap in (1, 2, 3) if any(conj_explicit(absd[ap][c], T, L) for T in tri)]
               for c in ("standard", "inverted", "reversed", "inv+rev")}
        print(f"  model alpha={a}: " + "  ".join(f"{c}->{row[c]}" for c in row), flush=True)

def scanB():
    print("=== (B) chi_P criterion : exact / full class / line ===")
    for a in (1, 2, 3):
        els, mul, inv, perm, L, Hm = model_group(N, a)
        M = sorted({perm(g) for g in els}); ID = tuple(range(L))
        def sq(el): return mul(el, el)[0]
        chi0 = (1 % N, 0); chiI = ((-a) % N, (-1) % N)
        C1 = [perm(g) for g in els if g[1] == 1]
        def cls(el):
            p = perm(el); return frozenset(pmul(pmul(c, p), pinv(c)) for c in M)
        variants = {
          "exact":      ([perm(g) for g in els if g[1] == 3 and sq(g) == chi0],
                         set(perm(g) for g in els if g[1] == 2 and sq(g) == chiI)),
          "full class": (list(cls([g for g in els if g[1]==3 and sq(g)==chi0][0])),
                         cls([g for g in els if g[1]==2 and sq(g)==chiI][0])),
          "line":       ([perm(g) for g in els if g[1]==3 and sq(g) in {((t)%N,0) for t in range(1,N)}],
                         set(perm(g) for g in els if g[1]==2 and
                             sq(g) in {((-t*a)%N,(-t)%N) for t in range(1,N)})),
        }
        for tag, (S0, SI) in variants.items():
            tri = []
            for g0 in S0:
                for g1 in C1:
                    gi = pinv(pmul(g0, g1))
                    if gi in SI:
                        gen = {ID}; fr = [ID]
                        while fr:
                            x = fr.pop()
                            for s in (g0, g1, pinv(g0), pinv(g1)):
                                y = pmul(x, s)
                                if y not in gen: gen.add(y); fr.append(y)
                        if len(gen) == len(M): tri.append((g0, g1, gi))
            seen = set(); orb = []
            for t in tri:
                if t in seen: continue
                o = {tuple(pmul(pmul(c, x), pinv(c)) for x in t) for c in M}
                seen |= o; orb.append(o)
            m = [ap for ap in (1, 2, 3)
                 if any(conj_explicit(ab(N, ap)[1:4], T, L) for T in tri)]
            print(f"  alpha={a} {tag:11s}: |S0|={len(S0):3d} |Sinf|={len(SI):3d} "
                  f"triples={len(tri):5d} orbits={len(orb)} matches={m}", flush=True)

if __name__ == "__main__":
    scanA(); print(); scanB()

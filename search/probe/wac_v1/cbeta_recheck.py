# DECISIVE RE-CHECK for 裁定 306 dispute.
#  - chi_P filtering = EXACT equality  g^2 == chi_P   (as the implementer used)
#  - stage-5 conjugacy tested by TWO independent methods
#  - FULL CROSS TABLE model(alpha) x abstract(alpha')  -- this is what settles it
import sys
sys.path.insert(0, ".")
from cbeta_nielsen import build as abstract_build, pmul, pinv, ctype
from cbeta_model import model_group, canon_form
N = 7

def model_triples(a):
    els, mul, inv, perm, L, Hm = model_group(N, a)
    M = sorted({perm(g) for g in els}); ID = tuple(range(L))
    chi0 = (1 % N, 0)                    # k=i   over lambda=0 : (v(h),v(g))=(1,0)
    chiI = ((-a) % N, (-1) % N)          # k=1   over lambda=inf: (v(h),v(g))=(-a,-1)
    def sq(el): return mul(el, el)[0]
    C0 = [perm(g) for g in els if g[1] == 3 and sq(g) == chi0]
    CI = set(perm(g) for g in els if g[1] == 2 and sq(g) == chiI)
    C1 = [perm(g) for g in els if g[1] == 1]
    tri = []
    for g0 in C0:
        for g1 in C1:
            gi = pinv(pmul(g0, g1))
            if gi in CI:
                gen = {ID}; fr = [ID]
                while fr:
                    x = fr.pop()
                    for s in (g0, g1, pinv(g0), pinv(g1)):
                        y = pmul(x, s)
                        if y not in gen: gen.add(y); fr.append(y)
                if len(gen) == len(M): tri.append((g0, g1, gi))
    return tri, len(C0), len(C1), len(CI), L

# --- conjugacy test 1: BFS canonical form ---
def conj_canon(A, B, L):
    cf = canon_form(A[0], A[1], 0)
    return any(canon_form(B[0], B[1], s) == cf for s in range(L))

# --- conjugacy test 2: explicit construction of the conjugator, independent code path ---
def conj_explicit(A, B, L):
    """find c in Sym(L) with c A_i c^{-1} = B_i for i=0,1  (c(A(x)) = B(c(x)))"""
    a0, a1 = A[0], A[1]; b0, b1 = B[0], B[1]
    for s in range(L):
        c = {0: s}; stack = [0]; ok = True
        while stack and ok:
            x = stack.pop()
            for ga, gb in ((a0, b0), (a1, b1)):
                y = ga[x]; ty = gb[c[x]]
                if y in c:
                    if c[y] != ty: ok = False; break
                else:
                    c[y] = ty; stack.append(y)
        if ok and len(c) == L and len(set(c.values())) == L:
            # verify on all three generators
            cc = tuple(c[i] for i in range(L))
            ok2 = all(all(cc[A[j][x]] == B[j][cc[x]] for x in range(L)) for j in range(3))
            if ok2: return True
    return False

if __name__ == "__main__":
    abstracts = {}
    for ap in (1, 2, 3):
        La, X, Y, Z, Mabs = abstract_build(N, ap)
        abstracts[ap] = ((X, Y, Z), La)
    for a in (1, 2, 3):
        tri, n0, n1, ni, L = model_triples(a)
        print(f"model alpha={a}: |C0|={n0} |C1|={n1} |Cinf|={ni} triples={len(tri)}", flush=True)
        for ap in (1, 2, 3):
            A, La = abstracts[ap]
            m1 = any(conj_canon(A, T, L) for T in tri)
            m2 = any(conj_explicit(A, T, L) for T in tri)
            print(f"    vs abstract alpha'={ap}:  canon={m1}   explicit={m2}"
                  + ("   <-- MATCH" if m1 else ""), flush=True)

"""m2_symbolic_ext.py -- extension of cbeta_symbolic_check.py to alpha = 1..8.

SPEC HEADER
  purpose : the four transformation laws used by the (M2) family note are claimed to be
            EXACT rational-function identities in k, with NO dependence on n.  This script
            re-verifies them symbolically for alpha = 1..8 (the paper proof is uniform in
            alpha; this is the machine confirmation of the hand computation).
  claims  :  h(k) = (k-i)/(k+i) * ((k+1)/(k-1))^alpha ,  g(k) = (k+1)/(k-1)
             h(-k)  == h(k)^{-1}
             g(-k)  == g(k)^{-1}
             g(1/k) == -g(k)
             h(1/k) == (-1)^{alpha+1} h(k)^{-1} g(k)^{2 alpha}
  note    : n enters ONLY through "reduce mod n-th powers" and through the two parity
            facts (-1)^{alpha+1} has an n-th root in {+-1} for n odd, and (-u)^n = -u^n.
            Neither appears in the identities above.
"""
import sympy as sp

k = sp.symbols('k'); i = sp.I


def h_of(x, a): return (x - i) / (x + i) * ((x + 1) / (x - 1)) ** a
def g_of(x): return (x + 1) / (x - 1)


ok = True
for a in range(1, 9):
    h = h_of(k, a); g = g_of(k)
    r = dict(alpha=a,
             h_sigma=(sp.simplify(h_of(-k, a) - h ** -1) == 0),
             g_sigma=(sp.simplify(g_of(-k) - g ** -1) == 0),
             g_theta=(sp.simplify(g_of(1 / k) + g) == 0),
             h_theta=(sp.simplify(sp.simplify(h_of(1 / k, a))
                                  - sp.simplify((-1) ** (a + 1) * h ** -1 * g ** (2 * a))) == 0))
    print(r, flush=True)
    ok = ok and all(v is True for key, v in r.items() if key != "alpha")
print("ALL_IDENTITIES_HOLD(alpha=1..8) =", ok)

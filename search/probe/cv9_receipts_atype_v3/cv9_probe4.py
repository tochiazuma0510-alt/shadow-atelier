"""Independent LINEAR-TIME evaluator for the word-level 5-coface predicate.

Key: push_i o tau0^k is itself a homomorphism F2 -> e4, so the predicate can be
evaluated with O(|w|) group multiplications instead of building the giant words
and calling push_through_coface_letters (which is O(n^2)).
tau0: x->y, y->(xy)^-1  (order 3):
  tau0^0 = (x, y);  tau0^1 = (y, (xy)^-1);  tau0^2 = ((xy)^-1, x)
"""
import sys, time, importlib.util
from pathlib import Path
ROOT = Path(r"C:\Users\81905\Desktop\shadow-atelier")
spec = importlib.util.spec_from_file_location("p31", str(ROOT / "scratchpad" / "d972_atype_v3_1_production.py"))
P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
core = P.core
eng = P.Engine(); e4 = eng.e4; K = 18
W = P.W_WORD
m_fpp, f_pp = P.build_f_double_prime(eng)
bases = {1: (0, []), 17: (17, []), 7: (3, W), 11: (14, W), 13: (6, f_pp), 5: (11, f_pp)}

MUL = e4.mul; ONE = e4.identity


def INV(a):
    """e4.inverse only handles MARKED GENERATORS (IndependentPc._inv_gen lookup
    raises IndexError on a general element) -- invert via the element's order."""
    cur = a
    for k in range(1, 401):
        if cur == ONE:
            v = ONE
            for _ in range(k - 1):
                v = MUL(v, a)
            return v
        cur = MUL(cur, a)
    raise RuntimeError("order > 400")


_ICACHE = {}


def evalw(w, A, B):
    key = (A, B)
    if key not in _ICACHE:
        _ICACHE[key] = (INV(A), INV(B))
    Ai, Bi = _ICACHE[key]
    v = ONE
    for L in w:
        v = MUL(v, A if L == 1 else Ai if L == -1 else B if L == 2 else Bi)
    return v


def powe(a, k):
    v = ONE
    for _ in range(k):
        v = MUL(v, a)
    return v


TOWER = {}
for i in range(5):
    X = e4.eval(eng.cofaces[i][0]); Y = e4.eval(eng.cofaces[i][2])
    XY = MUL(X, Y)
    TOWER[i] = [(X, Y), (Y, INV(XY)), (INV(XY), X)]


def fast_slot(f, m, i):
    (X0, Y0), (X1, Y1), (X2, Y2) = TOWER[i]
    a_ok = MUL(evalw(f, X0, Y0), evalw(f, Y0, X0)) == ONE      # f . theta0(f) = 1
    g0 = MUL(powe(Y0, m), evalw(f, X0, Y0))
    g1 = MUL(powe(Y1, m), evalw(f, X1, Y1))
    g2 = MUL(powe(Y2, m), evalw(f, X2, Y2))
    b_ok = MUL(MUL(g2, g1), g0) == ONE                          # tau^2(g).tau(g).g = 1
    return a_ok, b_ok


fast_all5 = lambda f, m: all(all(fast_slot(f, m, i)) for i in range(5))

print("\n=== V0. VALIDATE the fast evaluator against the production predicate ===")
bad = 0; n = 0
for f in ([], [2, -1], W, f_pp, [1, 2, -1, -2], [1, 1, 2]):
    for m in range(K):
        for i in range(5):
            n += 1
            if fast_slot(f, m, i) != eng.predB_slot(f, m, i):
                bad += 1
print(f"  {n} (f,m,slot) cells compared against Engine.predB_slot -- disagreements: {bad}")
assert bad == 0, "fast evaluator does not reproduce the production predicate"
print("  fast evaluator VALIDATED (exact agreement).")

print("\n=== D1. anatomy of the 36-cell gate4 grid (code cap = len(f) < 1500) ===")
rows = []
for l1 in sorted(bases):
    for l2 in sorted(bases):
        m, f = eng.compose(bases[l1], bases[l2])
        rows.append((l1, l2, m, (2 * m + 1) % K, len(f), not (len(f) < 1500), eng.charming_gate(f), (l1 * l2) % K, f))
capped = [r for r in rows if r[5]]
print(f"  lambda multiplicativity (lam == lam1*lam2 mod 18) over all 36: {all(r[3] == r[7] for r in rows)}")
print(f"  non-charming composites among all 36: {[(r[0], r[1]) for r in rows if not r[6]]}")
print(f"  cells with len(f) >= 1500 -> SILENTLY marked 'not closed': {len(capped)}/36")
print(f"  max len(f) among the 28 uncapped cells: {max(r[4] for r in rows if not r[5])}")

print("\n=== D2. DECISIVE: evaluate the capped cells with NO cap (linear-time) ===")
for r in capped:
    l1, l2, m, lam, ln, _, ch, prod, f = r
    t0 = time.time()
    per = [fast_slot(f, m, i) for i in range(5)]
    ok = all(a and b for a, b in per)
    print(f"    lam1={l1:2d} lam2={l2:2d} -> m={m:2d} lam={lam:2d}(=lam1*lam2:{lam == prod}) "
          f"len={ln:6d} charming={ch} ALL5={ok} per-slot={per} [{time.time()-t0:.1f}s]")
n_closed_true = sum(1 for r in rows if fast_all5(r[8], r[2]) and r[6])
print(f"  >>> TRUE closure count with the cap removed: {n_closed_true}/36")

print("\n=== D3. naive-product negative control: which cells leak ===")
leak = []
for l1 in sorted(bases):
    for l2 in sorted(bases):
        p1, p2 = bases[l1], bases[l2]
        nf = core.reduce_word(p1[1] + p2[1]); nm = (p1[0] + p2[0]) % K
        if eng.charming_gate(nf) and fast_all5(nf, nm):
            leak.append((l1, l2, nm, len(nf), p1[1] == [], p2[1] == []))
print(f"  naive-product cells that still CLOSE (control leaks): {len(leak)}/36")
for r in leak:
    print(f"    lam1={r[0]:2d} lam2={r[1]:2d} naive_m={r[2]:2d} len={r[3]:3d} "
          f"f1=identity:{r[4]} f2=identity:{r[5]}")

print("\n=== D4. (3.53)-order loop growth (w_verification_series item (iv), range(40)) ===")
p = (3, W); cur = p
for k in range(1, 11):
    cur = eng.compose(cur, p)
    print(f"    step {k:2d}: m={cur[0]:2d} len(f)={len(cur[1]):,}  cur==p ? {cur == p}")
    if len(cur[1]) > 400_000:
        print("    growth ~9x/step; 40 steps is unreachable (free-word representative never "
              "returns to p). ABORTING probe.")
        break

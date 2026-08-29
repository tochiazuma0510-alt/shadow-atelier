#!/usr/bin/env python3
"""Independent checker for the PILOT-2 ben4 L6' certificate.

Second implementation, second language: this reads ONLY
  * the certificate  search/certs/pilot2_ben4_L6_v1_20260829.json   (Q and C)
  * the exported basis scratchpad/pilot2_ben4_a_basis_k2N717_out.json (btilde_n, rho)
and recomputes, in Python/mpmath at 256 bits, on sample points that appear in NEITHER the
fit shells (0.42, 0.55, 0.68 rho) NOR the held-out shell (0.72 rho) NOR the wide shells:

  1. Q vanishes on the canonical image of X
  2. C vanishes on it
  3. the four cubics X_l * Q vanish on it (independent re-derivation of the containment)
  4. rank of Q's 4x4 symmetric matrix
  5. the iota parity of the basis (f_1, f_3 even; f_2, f_4 odd)
  6. the exact linear conditions q11 = q12 = 0, q13 + q22 = 0, q14 + q23 = 0
  7. the four iota-odd quadratic and ten iota-odd cubic monomials vanish

The Julia producer is never consulted; only its published numbers are.
"""
import json, os, sys
from mpmath import mp, mpf, mpc, sqrt, exp, pi, log10

mp.prec = 256
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cert = json.load(open(os.path.join(ROOT, "search/certs/pilot2_ben4_L6_v1_20260829.json"), encoding="utf-8"))
bas  = json.load(open(os.path.join(ROOT, "scratchpad/pilot2_ben4_a_basis_k2N717_out.json"), encoding="utf-8"))

RHO = mpf(bas["rho"])
BT  = [[mpc(mpf(re), mpf(im)) for re, im in zip(r, i)]
       for r, i in zip(bas["basis_btilde_re"], bas["basis_btilde_im"])]
N   = bas["N"]
D   = cert["FINAL_VERDICT"]["attained_D_digits"]
assert len(BT) == 4 and all(len(b) == N + 1 for b in BT)

s2 = cert["part_L6_step1_Sym2"]; s3 = cert["part_L6_step3_Sym3_and_C"]
MON2 = [(i, j) for i in range(1, 5) for j in range(i, 5)]
MON3 = [(i, j, k) for i in range(1, 5) for j in range(i, 5) for k in range(j, 5)]
assert s2["Q_monomials"] == ["".join("X%d" % i for i in t) for t in MON2]
assert s3["C_monomials"] == ["".join("X%d" % i for i in t) for t in MON3]
Q = [mpc(mpf(a), mpf(b)) for a, b in zip(s2["Q_re"], s2["Q_im"])]
C = [mpc(mpf(a), mpf(b)) for a, b in zip(s3["C_re"], s3["C_im"])]

def P(u):
    """(f_1,...,f_4) at w = u*rho, by Horner on the rescaled series"""
    out = []
    for b in BT:
        s = mpc(0)
        for j in range(len(b) - 1, -1, -1):
            s = s * u + b[j]
        out.append(s)
    return out

def evalform(coef, mons, p):
    num, den = mpc(0), mpf(0)
    for c, t in zip(coef, mons):
        z = c
        for i in t:
            z *= p[i - 1]
        num += z
        den = max(den, abs(z))
    return abs(num) / den

# ---- fresh sample points: radii and offsets used by no shell in the producer -------------
PTS = [mpf(r) * exp(mpc(0, 1) * 2 * pi * (mpf(m) + mpf(off)) / q)
       for r, off, q in (("0.31", "0.0517", 29), ("0.47", "0.6183", 31), ("0.61", "0.8090", 23))
       for m in range(q)]
rQ = max(evalform(Q, MON2, P(u)) for u in PTS)
rC = max(evalform(C, MON3, P(u)) for u in PTS)
# X_l * Q as cubics
idx3 = {t: c for c, t in enumerate(MON3)}
rLQ = mpf(0)
for l in range(1, 5):
    v = [mpc(0)] * 20
    for c, (i, j) in enumerate(MON2):
        v[idx3[tuple(sorted((i, j, l)))]] += Q[c]
    rLQ = max(rLQ, max(evalform(v, MON3, P(u)) for u in PTS))

# ---- rank of Q -------------------------------------------------------------------------
MQ = [[mpc(0)] * 4 for _ in range(4)]
for c, (i, j) in enumerate(MON2):
    if i == j:
        MQ[i - 1][i - 1] = Q[c]
    else:
        MQ[i - 1][j - 1] = Q[c] / 2
        MQ[j - 1][i - 1] = Q[c] / 2
fro = sqrt(sum(abs(MQ[i][j]) ** 2 for i in range(4) for j in range(4)))
MQn = [[MQ[i][j] / fro for j in range(4)] for i in range(4)]
def det4(M):
    from itertools import permutations
    s = mpc(0)
    for p in permutations(range(4)):
        sg = 1
        for a in range(4):
            for b in range(a + 1, 4):
                if p[a] > p[b]:
                    sg = -sg
        t = mpc(sg)
        for a in range(4):
            t *= M[a][p[a]]
        s += t
    return s
detQ = det4(MQn)
# singular values via the eigenvalues of MQn^H MQn (4x4 Hermitian; power/deflation-free:
# use the characteristic polynomial through mpmath's eigensolver)
from mpmath import polyroots
# H = MQn^H MQn  (4x4 Hermitian positive semidefinite); its eigenvalues are the squared
# singular values.  Characteristic polynomial by Faddeev-LeVerrier, then mpmath polyroots --
# no dependence on any external eigensolver.
H = [[sum(MQn[k][i].conjugate() * MQn[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
def matmul(A, B): return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
def trace(A):     return sum(A[i][i] for i in range(4))
Mk = [[mpc(1) if i == j else mpc(0) for j in range(4)] for i in range(4)]
coeff = [mpc(1)]                                    # char poly  x^4 + c1 x^3 + c2 x^2 + ...
Ak = H
for k in range(1, 5):
    ck = -trace(Ak) / k
    coeff.append(ck)
    Ak = matmul(H, [[Ak[i][j] + (ck if i == j else mpc(0)) for j in range(4)] for i in range(4)])
ev = sorted([abs(r) for r in polyroots([c.real for c in coeff], maxsteps=200, extraprec=200)], reverse=True)
sv = [sqrt(x) for x in ev]

# ---- structure -------------------------------------------------------------------------
pos2 = {t: c for c, t in enumerate(MON2)}
qq = lambda i, j: Q[pos2[(min(i, j), max(i, j))]]
par = [max(abs(BT[i][n]) for n in range(0, min(200, N) + 1) if n % 2 != i % 2) for i in range(4)]
iota_odd2 = max(abs(qq(*t)) for t in ((1, 2), (1, 4), (2, 3), (3, 4)))
sign3 = lambda t: (-1) ** sum(1 for i in t if i in (1, 3))
iota_odd3 = max(abs(C[c]) for c, t in enumerate(MON3) if sign3(t) == -1)
iota_even3 = max(abs(C[c]) for c, t in enumerate(MON3) if sign3(t) == 1)

FLOOR = mpf(10) ** (-mpf(D) / 2)
res = {
 "checker": "crosscheck/check_pilot2_ben4_L6_v1.py (Python/mpmath 256-bit; independent of the Julia producer)",
 "cert": "search/certs/pilot2_ben4_L6_v1_20260829.json",
 "sample_points": "83 points on radii 0.31, 0.47, 0.61 rho with fresh angular offsets -- disjoint from every shell used by the producer",
 "Q_max_relative_residual_on_X": float(rQ),
 "C_max_relative_residual_on_X": float(rC),
 "Xl_Q_max_relative_residual_on_X": float(rLQ),
 "abs_det_of_normalised_Q_matrix": float(abs(detQ)),
 "singular_values_of_normalised_Q_matrix": [float(x) for x in sv] if sv else None,
 "rank_Q_by_absolute_floor": (sum(1 for x in sv if x >= sv[0] * FLOOR) if sv else None),
 "rank_Q_in_cert": cert["part_L6_step2_rank_of_Q"]["rank"],
 "iota_parity_basis_wrong_parity_max": [float(x) for x in par],
 "q11": float(abs(qq(1, 1))), "q12": float(abs(qq(1, 2))),
 "q13_plus_q22": float(abs(qq(1, 3) + qq(2, 2))), "q14_plus_q23": float(abs(qq(1, 4) + qq(2, 3))),
 "q24_minus_q33": float(abs(qq(2, 4) - qq(3, 3))),
 "iota_odd_quadratic_monomials_max": float(iota_odd2),
 "iota_odd_cubic_monomials_max": float(iota_odd3),
 "iota_even_cubic_monomials_max": float(iota_even3),
 "absolute_floor": float(FLOOR),
}
res["VERDICT"] = ("AGREES" if (rQ < FLOOR and rC < FLOOR and rLQ < FLOOR
                               and res["rank_Q_by_absolute_floor"] == res["rank_Q_in_cert"]
                               and iota_odd2 < FLOOR and iota_odd3 < FLOOR) else "DISAGREES")
print(json.dumps(res, indent=1))
out = os.path.join(ROOT, "crosscheck", "verdicts", "pilot2_ben4_L6_crosscheck_v1_20260829.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(res, open(out, "w", encoding="utf-8"), indent=1)
print("WROTE", out)
sys.exit(0 if res["VERDICT"] == "AGREES" else 1)

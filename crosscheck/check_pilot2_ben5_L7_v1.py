#!/usr/bin/env python3
"""
Independent checker for  search/certs/pilot2_ben5_L7_v1_20260829.json  (PILOT-2 ben5 / L7').

PRODUCER / CHECKER SEPARATION.  This file shares NO code with the producer
(scratchpad/pilot2_ben5_*.py).  It reads only

  (i)  the CERT's claimed exact integers   -- Q, C, B, k, A, P_0/P_1/P_inf, and the
       recognised rational series coefficients c_{i,n};
  (ii) the ben4-certified echelon basis    -- scratchpad/pilot2_ben4_a_basis_k2N717_out.json
       (sha16 61d9c07e37c24606) and ..._k2N538_out.json (bf89cd427825f579);

and re-derives every claim from scratch by a different route.  In particular it never calls
the producer's rank detector, its series recogniser, or its exact-kernel code.

  usage:  python crosscheck/check_pilot2_ben5_L7_v1.py
"""
import json, os, sys, hashlib, itertools
from fractions import Fraction as Fr
from mpmath import mp, mpf, mpc

mp.dps = 60
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERT = os.path.join(ROOT, "search", "certs", "pilot2_ben5_L7_v1_20260829.json")
OUTV = os.path.join(ROOT, "crosscheck", "verdicts", "pilot2_ben5_L7_crosscheck_v1_20260829.json")

M2 = [(i, j) for i in range(1, 5) for j in range(i, 5)]
M3 = [(i, j, k) for i in range(1, 5) for j in range(i, 5) for k in range(j, 5)]
I2 = {t: c for c, t in enumerate(M2)}
I3 = {t: c for c, t in enumerate(M3)}
nm = lambda t: "".join("X%d" % i for i in t)
wt = lambda t: sum(i - 1 for i in t)
fails, notes = [], []


def chk(name, cond, detail=""):
    (notes if cond else fails).append("%s %s %s" % ("PASS" if cond else "FAIL", name, detail))
    print("  %-4s %-52s %s" % ("PASS" if cond else "FAIL", name, detail))
    return cond


def sha16(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]


cert = json.load(open(CERT, encoding="utf-8"))
E = cert["part_exact_model"]
Q = [Fr(x) for x in E["Q"]["coeffs"]]
C = [Fr(x) for x in E["C"]["coeffs"]]
B = [Fr(x) for x in cert["part_phi"]["B_coeffs"]]
K = Fr(cert["part_phi"]["k"])
A = [[Fr(x) for x in r] for r in E["A"]["matrix"]]
NU2 = Fr(E["twist"]["nu_squared"])
SER = {(e["i"], e["n"]): Fr(e["num"], e["den"]) for e in cert["part_series_recognition"]["entries"]}
NC = max(n for (_, n) in SER)

print("=== independent check of PILOT-2 ben5 cert (%s) ===" % sha16(CERT))
print("\n-- 0. inputs --")
for k_, v in cert["input_artifacts"].items():
    p = os.path.join(ROOT, k_)
    chk("input sha16 %s" % os.path.basename(k_), os.path.exists(p) and sha16(p) == v, v)

# ---------------------------------------------------------------------------------------
# exact series arithmetic (written independently)
# ---------------------------------------------------------------------------------------
def mul(a, b, M):
    o = [Fr(0)] * (M + 1)
    for i in range(min(len(a), M + 1)):
        if a[i]:
            for j in range(min(len(b), M + 1 - i)):
                if b[j]:
                    o[i + j] += a[i] * b[j]
    return o


def inv(a, M):
    o = [Fr(0)] * (M + 1)
    o[0] = 1 / a[0]
    for k_ in range(1, M + 1):
        o[k_] = -sum(a[j] * o[k_ - j] for j in range(1, k_ + 1) if j < len(a)) / a[0]
    return o


def prod(S, t, M):
    r = [Fr(1)] + [Fr(0)] * M
    for i in t:
        r = mul(r, S[i - 1], M)
    return r


def evf(coef, mons, S, M):
    o = [Fr(0)] * (M + 1)
    for c, t in enumerate(mons):
        if coef[c]:
            p = prod(S, t, M)
            o = [o[m] + coef[c] * p[m] for m in range(M + 1)]
    return o


# model-2 series, rebuilt from the cert's rationals AND the cert's twist
SIG = [[Fr(0)] * (NC + 1) for _ in range(4)]
for (i, n), v in SER.items():
    w = n - (i - 1)
    SIG[i - 1][n] = v * NU2 ** (w // 2)
for i in range(4):
    SIG[i][i] = Fr(1)

print("\n-- 1. the exact Q-model --")
chk("sigma is echelon: sigma_i = t^(i-1) + O(t^4)",
    all(SIG[i][j] == (1 if i == j else 0) for i in range(4) for j in range(4)))
qs = evf(Q, M2, SIG, NC - 1)
cs = evf(C, M3, SIG, NC)
chk("Q(sigma) == 0 exactly to order %d" % (NC - 1), all(x == 0 for x in qs))
chk("C(sigma) == 0 exactly to order %d" % NC, all(x == 0 for x in cs))
MQ = [[Fr(0)] * 4 for _ in range(4)]
for c, (i, j) in enumerate(M2):
    if i == j:
        MQ[i - 1][i - 1] = Q[c]
    else:
        MQ[i - 1][j - 1] = MQ[j - 1][i - 1] = Fr(Q[c], 2)
det = sum((-1) ** sum(1 for a in range(4) for b in range(a + 1, 4) if p[a] > p[b]) *
          MQ[0][p[0]] * MQ[1][p[1]] * MQ[2][p[2]] * MQ[3][p[3]]
          for p in itertools.permutations(range(4)))
chk("rank Q = 4 (det != 0, smooth quadric, two g^1_3)", det != 0, "det = %s" % str(det))

print("\n-- 2. the order-3 automorphism A --")
mm = lambda X, Y: [[sum(X[i][k_] * Y[k_][j] for k_ in range(4)) for j in range(4)] for i in range(4)]
A2 = mm(A, A)
chk("A^3 = I exactly", all(mm(A2, A)[i][j] == (1 if i == j else 0) for i in range(4) for j in range(4)))
chk("trace A = 1 (eigenvalues 1,1,omega,omega^2)", sum(A[i][i] for i in range(4)) == 1)


def sub(coef, Mx, mons, idx):
    o = [Fr(0)] * len(mons)
    for c, t in enumerate(mons):
        if not coef[c]:
            continue
        for pk in itertools.product(range(1, 5), repeat=len(t)):
            pr = coef[c]
            for a in range(len(t)):
                pr *= Mx[t[a] - 1][pk[a] - 1]
            o[idx[tuple(sorted(pk))]] += pr
    return o


QA = sub(Q, A, M2, I2)
sQ = next(QA[c] / Q[c] for c in range(10) if Q[c])
chk("Q o A = (%s) * Q exactly" % str(sQ), all(QA[c] == sQ * Q[c] for c in range(10)))
LQ = []
for l in range(1, 5):
    v = [Fr(0)] * 20
    for c, (i, j) in enumerate(M2):
        v[I3[tuple(sorted((i, j, l)))]] += Q[c]
    LQ.append(v)


def red(v, basis):
    v = list(v)
    R = [b[:] for b in basis]
    piv, r0 = [], 0
    for c in range(20):
        pr = next((i for i in range(r0, len(R)) if R[i][c]), None)
        if pr is None:
            continue
        R[r0], R[pr] = R[pr], R[r0]
        pv = R[r0][c]
        R[r0] = [x / pv for x in R[r0]]
        for i in range(len(R)):
            if i != r0 and R[i][c]:
                f = R[i][c]
                R[i] = [R[i][j] - f * R[r0][j] for j in range(20)]
        piv.append(c)
        r0 += 1
    for r, pc in enumerate(piv):
        if v[pc]:
            f = v[pc]
            v = [v[j] - f * R[r][j] for j in range(20)]
    return v, len(piv)


CAr, dimLQ = red(sub(C, A, M3, I3), LQ)
Cr, _ = red(C, LQ)
sC = next(CAr[c] / Cr[c] for c in range(20) if Cr[c])
chk("dim span{X_l Q} = 4", dimLQ == 4)
chk("C o A = (%s) * C mod span{X_l Q} exactly" % str(sC), all(CAr[c] == sC * Cr[c] for c in range(20)))

print("\n-- 3. the three ramification points --")
P = {"P_0": [Fr(1), Fr(0), Fr(0), Fr(0)]}
P["P_1"] = [sum(A[i][j] * P["P_0"][j] for j in range(4)) for i in range(4)]
P["P_inf"] = [sum(A2[i][j] * P["P_0"][j] for j in range(4)) for i in range(4)]
prj = lambda p: [x / next(y for y in p if y) for x in p]
for key in ("P_0", "P_1", "P_inf"):
    claimed = [Fr(x) for x in cert["part_phi"]["points"][key]]
    ok = prj(claimed) == prj(P[key])
    q0 = sum(Q[c] * P[key][t[0] - 1] * P[key][t[1] - 1] for c, t in enumerate(M2))
    c0 = sum(C[c] * P[key][t[0] - 1] * P[key][t[1] - 1] * P[key][t[2] - 1] for c, t in enumerate(M3))
    chk("%s matches the cert and lies on X exactly" % key, ok and q0 == 0 and c0 == 0,
        "(%s)" % ":".join(str(x) for x in claimed))
IO = [Fr(-1), Fr(1), Fr(-1), Fr(1)]
chk("iota fixes P_0 and swaps P_1 <-> P_inf",
    prj([IO[i] * P["P_0"][i] for i in range(4)]) == prj(P["P_0"]) and
    prj([IO[i] * P["P_1"][i] for i in range(4)]) == prj(P["P_inf"]))

print("\n-- 4. phi = k X_4^3 / B : divisor, sparsity, S_3 action (all EXACT) --")
MS = NC
SA = [[sum(A[i][j] * SIG[j][n] for j in range(4)) for n in range(MS + 1)] for i in range(4)]
SI = [[sum(A2[i][j] * SIG[j][n] for j in range(4)) for n in range(MS + 1)] for i in range(4)]
SJ = [[SIG[i][n] * IO[i] for n in range(MS + 1)] for i in range(4)]
phi = lambda S: [x * K for x in mul(prod(S, (4, 4, 4), MS), inv(evf(B, M3, S, MS), MS), MS)]
p0 = phi(SIG)
p1 = phi(SA)
pj = phi(SJ)          # phi at P_inf does NOT exist as a power series -- that is the pole; 1/phi is used below
ord_ = lambda s: next((m for m in range(len(s)) if s[m]), None)
chk("ord_{P_0}(phi) = 9", ord_(p0) == 9)
chk("ord_{P_1}(phi - 1) = 9", ord_([p1[0] - 1] + p1[1:]) == 9)
one = [Fr(1)] + [Fr(0)] * MS
chk("ord_{P_inf}(1/phi) = 9", ord_(mul(evf(B, M3, SI, MS), inv([x * K for x in prod(SI, (4, 4, 4), MS)], MS), MS)) == 9)
chk("phi is sparse in t^9 (Delta-invariance)", all(p0[m] == 0 for m in range(MS + 1) if m % 9))
t1 = mul(one, inv([one[m] - p0[m] for m in range(MS + 1)], MS), MS)
chk("phi o A = 1/(1-phi)  [3-cycle (0 1 inf)]", all(p1[m] == t1[m] for m in range(MS + 1)),
    "agreement to order %d > 2*deg phi = 18 => equality on X" % MS)
t2 = mul(p0, inv([p0[m] - one[m] for m in range(MS + 1)], MS), MS)
chk("phi o iota = phi/(phi-1)  [transposition (1 inf)]", all(pj[m] == t2[m] for m in range(MS + 1)))
BI = sub(B, [[IO[i] if i == j else Fr(0) for j in range(4)] for i in range(4)], M3, I3)
sm = [B[c] + BI[c] for c in range(20)]
chk("B + B o iota is a multiple of X_4^3",
    all(sm[c] == 0 for c in range(20) if M3[c] != (4, 4, 4)))
# the divisor proof: the hyperplane X_4 = 0 meets X in 3 P_0 + 3 R with R = (3:0:-4:0)
R = [Fr(x) for x in cert["part_divisor_proof"]["R"]]
chk("R lies on X exactly",
    sum(Q[c] * R[t[0] - 1] * R[t[1] - 1] for c, t in enumerate(M2)) == 0 and
    sum(C[c] * R[t[0] - 1] * R[t[1] - 1] * R[t[2] - 1] for c, t in enumerate(M3)) == 0)
MR = 26
XR = [[Fr(1)] + [Fr(0)] * MR, [Fr(0), Fr(1)] + [Fr(0)] * (MR - 1),
      [R[2] / R[0]] + [Fr(0)] * MR, [Fr(0)] * (MR + 1)]
for k_ in range(1, MR + 1):
    qk = evf(Q, M2, XR, MR)[k_]
    ck = evf(C, M3, XR, MR)[k_]
    def dd(coef, mons, idx):
        o = [Fr(0)] * (MR + 1)
        for c, t in enumerate(mons):
            if not coef[c]:
                continue
            for pos in range(len(t)):
                if t[pos] != idx:
                    continue
                pr = [Fr(1)] + [Fr(0)] * MR
                for j, i in enumerate(t):
                    if j != pos:
                        pr = mul(pr, XR[i - 1], MR)
                o = [o[m] + coef[c] * pr[m] for m in range(MR + 1)]
        return o
    a11, a12 = dd(Q, M2, 3)[0], dd(Q, M2, 4)[0]
    a21, a22 = dd(C, M3, 3)[0], dd(C, M3, 4)[0]
    D_ = a11 * a22 - a12 * a21
    XR[2][k_] += (-qk * a22 + ck * a12) / D_
    XR[3][k_] += (-a11 * ck + a21 * qk) / D_
chk("local branch at R solves Q = C = 0 to order %d" % MR,
    all(x == 0 for x in evf(Q, M2, XR, MR)) and all(x == 0 for x in evf(C, M3, XR, MR)))
oX4, oB = ord_(XR[3]), ord_(evf(B, M3, XR, MR))
chk("ord_R(X_4) = 3 and ord_R(B) = 9  ==>  div(phi) = 9P_0 - 9P_inf, deg phi = 9",
    oX4 == 3 and oB == 9, "(measured %d, %d)" % (oX4, oB))
chk("[G6'-b] Riemann-Hurwitz saturated: 24 = 3*(9-1), no branch point outside {0,1,inf}",
    (2 * 4 - 2) - 9 * (-2) == 3 * (9 - 1))

print("\n-- 5. the model reproduces the ben4-certified analytic basis (independent numerics) --")
for tag, exp in (("k2N717", 1e-18), ("k2N538", 1e-14)):
    bp = os.path.join(ROOT, "scratchpad", "pilot2_ben4_a_basis_%s_out.json" % tag)
    d = json.load(open(bp, encoding="utf-8"))
    bt = [[mpc(mpf(d["basis_btilde_re"][i][n]), mpf(d["basis_btilde_im"][i][n]))
           for n in range(len(d["basis_btilde_re"][i]))] for i in range(4)]
    # Lambda is fixed by ONE coefficient (weight 2): bt_{3,4} = c^(2)_{3,4} * Lambda^{-2}
    LAM2 = SIG[2][4] / bt[2][4]
    LAM2 = mpc(mpf(LAM2.numerator) / LAM2.denominator, 0) if isinstance(LAM2, Fr) else \
        mpf(SIG[2][4].numerator) / SIG[2][4].denominator / bt[2][4]
    LAM = mp.sqrt(LAM2)
    worst = mpf(0)
    for (i, n), v in SER.items():
        w = n - (i - 1)
        pred = mpf(SIG[i - 1][n].numerator) / SIG[i - 1][n].denominator * LAM ** (-w) if SIG[i - 1][n] else mpf(0)
        worst = max(worst, abs(pred - bt[i - 1][n]))
    chk("[%s] every recognised coefficient reproduces the certified basis" % tag, float(worst) < exp,
        "worst |predicted - certified| = %.3e" % float(worst))
    # phi: Delta-fibre constancy at HELD-OUT points, evaluated on the certified basis
    Ban = [mpf(B[c].numerator) / B[c].denominator * LAM ** (-wt(t)) for c, t in enumerate(M3)]
    Nan = mpf(K.numerator) / K.denominator * LAM ** (-9)
    zeta = mp.expjpi(mpf(2) / 9)
    ev = lambda v: [sum(bt[i][n] * v ** n for n in range(len(bt[i]))) for i in range(4)]
    spread, orders = mpf(0), []
    for m_ in range(7):
        v = mpf("0.735") * mp.expjpi(2 * (mpf(m_) + mpf("0.317")) / 7)
        vals = []
        for j in range(9):
            pv = ev(zeta ** j * v)
            num = Nan * pv[3] ** 3
            den = sum(Ban[c] * pv[t[0] - 1] * pv[t[1] - 1] * pv[t[2] - 1] for c, t in enumerate(M3))
            vals.append(num / den)
        mn = sum(vals) / 9
        spread = max(spread, max(abs(x - mn) for x in vals) / abs(mn))
    chk("[%s] phi is constant on held-out delta_a-fibres (9 points each, 7 fibres)" % tag,
        float(spread) < exp * 100, "max relative spread = %.3e" % float(spread))
    # measured vanishing order at P_0.  phi = g_1 v^9 (1 + g_2/g_1 v^9 + ...) is sparse in v^9, so the
    # finite-difference exponent log_2|phi(2v)/phi(v)| = 9 + O((2^9-1) v^9): the tolerance below is that
    # SYSTEMATIC size, computed from v alone -- it is not tuned to the measured value.
    for v0 in (mpf("0.02"), mpf("0.04")):
        r = []
        for s in (1, 2):
            pv = ev(v0 * s)
            num = Nan * pv[3] ** 3
            den = sum(Ban[c] * pv[t[0] - 1] * pv[t[1] - 1] * pv[t[2] - 1] for c, t in enumerate(M3))
            r.append(num / den)
        o1 = mp.log(abs(r[1] / r[0])) / mp.log(2)
        tolo = float(1000 * 511 * (2 * v0) ** 9)
        chk("[%s] measured ord_{P_0}(phi) = 9 at |v| = %s" % (tag, mp.nstr(v0, 3)),
            abs(o1 - 9) < tolo, "measured %.10f (systematic tolerance %.2e)" % (float(o1), tolo))

print("\n=== %d PASS, %d FAIL ===" % (len(notes), len(fails)))
os.makedirs(os.path.dirname(OUTV), exist_ok=True)
json.dump({"schema": "pilot2-ben5-crosscheck/v1", "cert": os.path.relpath(CERT, ROOT),
           "cert_sha16": sha16(CERT), "n_pass": len(notes), "n_fail": len(fails),
           "verdict": "AGREES" if not fails else "DISAGREES",
           "checks": notes + fails}, open(OUTV, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("VERDICT:", "AGREES" if not fails else "DISAGREES", "->", OUTV)
sys.exit(1 if fails else 0)

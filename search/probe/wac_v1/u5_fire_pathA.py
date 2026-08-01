# u5 FIRE - path A: explicit K^(n) tower model from KUM-n, exact arithmetic over Q(i).
# Ported verbatim from u7_fire_pathA.py (裁定 300 firing design); model code is n-generic
# and untouched.  Exact rationals only; no floating point.
#
# n=5 DISCIPLINE:
#   ALLOWED_N below intentionally contains 5.  This is a *versioned release*, scoped to
#   this script only, under 裁定 396 (2026-08-01 研究者一括認可 (2) n=5 開封).  No other
#   probe's ALLOWED_N (m2_family_check.py / m2_desc_check.py / m2_crosstable_gap_v1.g /
#   tw_blocks.py / tw_orient.py / u7_fire_path{A,B}.py) is touched or reinterpreted by
#   this release; freeze U7-NO5 remains in force everywhere else.
#
# CV-13 calibration (this script's __main__): before touching n=5, path A first
# re-derives n=7 (alpha=1,2,3) and n=3 (alpha=1, CAL-3) and hard-asserts bit-for-bit
# reproduction of search/certs/u7_fire_20260801.json ("all_windows_alpha" + CAL-3
# fields).  Only after that gate passes does it evaluate n=5.
#
# Model (alpha = window label, r_0 = 1, r_inf = -alpha):
#   B_0 = P^1_k ; kappa_{1,2} = +-i (over m_0 = 0) ; kappa_{3,4} = +-1 (over m_0 = inf)
#   h(k) = (k-i)^{1}(k+i)^{-1}(k-1)^{-alpha}(k+1)^{alpha}
#   Wtilde_0 : y^n = h(k) ;  iota(k,y) = (-k, 1/y)  [checked: h(-k) = h(k)^{-1}]
#   W_0 = Wtilde_0 / <iota> ;  m_0 = (1+k^2)/(1-k^2) ;  lambda = m_0^2   (gamma = 1)
# Local expansion at the cusp: t := k - i is a local param on B_0 at kappa_1 = i,
#   y is a uniformizer of Wtilde_0 at Q_+ = (k=i, y=0)  [v(y) = 1 since v(h) = n there],
#   and Wtilde_0 -> W_0 is unramified at Q_+ (iota swaps Q_+ and Q_-),
#   so O^_{W_0,P_0} = O^_{Wtilde_0,Q_+} and u_n is read off there.
import json
import os
from fractions import Fraction as Fr

ALLOWED_N = (5,)   # 裁定396 (2026-08-01) による n=5 の versioned 解除。この script 限定。


class QI:                       # Gaussian rationals a + b i
    __slots__ = ("a", "b")
    def __init__(self, a=0, b=0): self.a = Fr(a); self.b = Fr(b)
    def __add__(s, o): return QI(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return QI(s.a - o.a, s.b - o.b)
    def __mul__(s, o): return QI(s.a*o.a - s.b*o.b, s.a*o.b + s.b*o.a)
    def inv(s):
        d = s.a*s.a + s.b*s.b
        assert d != 0, "division by zero in Q(i)"
        return QI(s.a/d, -s.b/d)
    def __truediv__(s, o): return s * o.inv()
    def __pow__(s, e):
        if e < 0: return s.inv() ** (-e)
        r = QI(1, 0)
        for _ in range(e): r = r * s
        return r
    def __eq__(s, o): return s.a == o.a and s.b == o.b
    def __repr__(s):
        if s.b == 0: return str(s.a)
        return f"{s.a}{'+' if s.b>0 else '-'}{abs(s.b)}i"

I  = QI(0, 1)
ONE = QI(1, 0)

def run(n, alpha):
    k_at_kappa1 = I
    # h1 = lim_{t->0} h(i+t)/t = (k+1)^alpha / ( (k+i) * (k-1)^alpha ) at k = i
    h1 = (I + ONE)**alpha / ((I + I) * (I - ONE)**alpha)
    # leading coeff of m_0 at t=0:  m_0 = t(2i+t)/(2-2it-t^2)  ->  (2i)/2 = i
    m1 = (I + I) / QI(2, 0)
    assert m1 == I
    # lambda = m_0^2 = (m1 t)^2 (1+...) = -t^2(1+...);  t = y^n/h1 (1+...)
    L0 = m1 * m1                                  # = -1
    u  = L0 / (h1 * h1)                           # u_n  (leading coeff of lambda in y^{2n})
    # fibre over lambda = 1 : the two unramified points R_+ (k=0) and R_- (k=inf)
    h_at_0   = (QI(0,0) - I) * (ONE)**alpha / (I * (QI(0,0) - ONE)**alpha)   # h(0)
    h_at_inf = ONE                                                          # deg num = deg den
    # iota-fixed point in each fibre solves y = 1/y and y^n = h  =>  y = +-1 with y^n = h
    def fixed_y(hval):
        for cand in (ONE, QI(-1, 0)):
            if cand**n == hval: return cand
        return None
    R_plus, R_minus = fixed_y(h_at_0), fixed_y(h_at_inf)
    # h(-k) = h(k)^{-1} sanity at a random rational point k = 3
    k = QI(3, 0)
    hk  = (k-I)*(k+ONE)**alpha / ((k+I)*(k-ONE)**alpha)
    mk  = QI(-3, 0)
    hmk = (mk-I)*(mk+ONE)**alpha / ((mk+I)*(mk-ONE)**alpha)
    out = dict(n=n, alpha=alpha, h1=str(h1), u=str(u), u_is_rational=(u.b == 0),
               u_value=(str(u.a) if u.b == 0 else None),
               h_at_0=str(h_at_0), h_at_inf=str(h_at_inf),
               R_plus_y=str(R_plus), R_minus_y=str(R_minus),
               both_R_rational=(R_plus is not None and R_minus is not None),
               iota_ok=(hmk == hk.inv()))
    print(out, flush=True)
    return out


def _load_u7_cert():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, "..", "..", ".."))
    with open(os.path.join(root, "search", "certs", "u7_fire_20260801.json"), encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    # ---- CV-13 anchor: n=7 (and n=3 CAL-3) must bit-reproduce the frozen u7 cert ----
    cert = _load_u7_cert()
    anchor_fail = []

    r3 = run(3, 1)
    if r3["u_value"] != cert["calibration_CAL3"]["u_3_computed"]:
        anchor_fail.append(f"CAL-3 n=3: got {r3['u_value']!r}, cert {cert['calibration_CAL3']['u_3_computed']!r}")

    anchor7 = {}
    for a in (1, 2, 3):
        r = run(7, a)
        anchor7[f"n7_a{a}"] = r
        cert_val = cert["path_A"]["all_windows_alpha"][f"n7_a{a}"]
        if r["u_value"] != cert_val:
            anchor_fail.append(f"n=7 alpha={a}: got {r['u_value']!r}, cert {cert_val!r}")

    r7a1 = anchor7["n7_a1"]
    if r7a1["h1"] != cert["path_A"]["leading_coeff_h1"]:
        anchor_fail.append(f"n=7 a=1 h1: got {r7a1['h1']!r}, cert {cert['path_A']['leading_coeff_h1']!r}")
    if r7a1["R_plus_y"] != cert["path_A"]["R_plus_y"]:
        anchor_fail.append(f"n=7 a=1 R_plus_y: got {r7a1['R_plus_y']!r}, cert {cert['path_A']['R_plus_y']!r}")
    if r7a1["R_minus_y"] != cert["path_A"]["R_minus_y"]:
        anchor_fail.append(f"n=7 a=1 R_minus_y: got {r7a1['R_minus_y']!r}, cert {cert['path_A']['R_minus_y']!r}")
    if r7a1["iota_ok"] != cert["path_A"]["iota_involution_check"]:
        anchor_fail.append(f"n=7 a=1 iota_ok: got {r7a1['iota_ok']!r}, cert {cert['path_A']['iota_involution_check']!r}")

    print("CV-13 ANCHOR:", "PASS" if not anchor_fail else "FAIL", flush=True)
    for msg in anchor_fail:
        print("  MISMATCH:", msg, flush=True)
    assert not anchor_fail, "CV-13 anchor (n=7 bit reproduction of u7_fire_20260801.json) failed"

    # ---- n=5 measurement (post-anchor; ALLOWED_N release scoped to this run) ----
    res5 = []
    for n in ALLOWED_N:           # = (5,)  -- 裁定396 versioned release
        for a in range(1, (n-1)//2 + 1):
            res5.append(run(n, a))

    print("n=5 all u rational:", all(r["u_is_rational"] for r in res5), flush=True)
    print("n=5 all R_+,R_- individually rational:", all(r["both_R_rational"] for r in res5), flush=True)
    print("n=5 all iota involution checks:", all(r["iota_ok"] for r in res5), flush=True)

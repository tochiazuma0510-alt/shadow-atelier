# -*- coding: utf-8 -*-
# CR-1 導出値: Brown 1301.3053v2 Definition 8.1 / Remark 8.2 (8.6) + Example 8.4 f12
# から ē₁₂ の全項を再構成する。根拠式: (8.6) p.22(画像照合済), f12 = [x1^8,x2^2]-3[x1^6,x2^4] p.24(画像照合済)
# 照合アンカー(p.24 逐語): coeff(x3^7 x4)=1, coeff(x1^3 x2^2 x3^2 x4)=-116, coeff(x1^2 x2^5 x4)=-57, 全118項
import json
from sympy import symbols, Poly, expand, factor, gcd_list, simplify, div

x, y = symbols('x y')
x1, x2, x3, x4 = symbols('x1 x2 x3 x4')

# f12 (Example 8.4, p.24): [x1^8,x2^2] - 3[x1^6,x2^4],  [a,b] = x^a y^b - x^b y^a
f = x**8*y**2 - x**2*y**8 - 3*(x**6*y**4 - x**4*y**6)

# s12 (Example 7.2, p.21) との一致確認
s12 = expand(x**2*y**2*(x-y)**3*(x+y)**3)
assert expand(f - s12) == 0, "f12 != s12"

# f = x y (x-y) f0  (§8.2, p.22)
q, r = div(Poly(f, x, y), Poly(x*y*(x-y), x, y))
assert r.is_zero
f0 = q.as_expr()
# f0 の性質確認: 対称・(8.4) 3-term
assert expand(f0 - f0.subs({x: y, y: x}, simultaneous=True)) == 0, "f0 not symmetric"
t3 = expand(f0 + f0.subs({x: y-x, y: -x}, simultaneous=True) + f0.subs({x: -y, y: x-y}, simultaneous=True))
assert t3 == 0, "3-term (8.4) fails"

f1 = expand((x-y)*f0)
def F1(a, b): return f1.subs({x: a, y: b}, simultaneous=True)
def F0(a, b): return f0.subs({x: a, y: b}, simultaneous=True)

# (8.6) p.22 逐語どおり
e12 = expand(
    F1(x4-x3, x2-x1) + F1(-x4, x3-x2) + F1(x1, x4-x3) + F1(x2-x1, -x4) + F1(x3-x2, x1)
    - x1*F0(x2-x3, x4-x3) + (x1-x2)*F0(x3-x4, -x4) + (x2-x3)*F0(x4, x1)
    + (x3-x4)*F0(-x1, x2-x1) + x4*F0(x1-x2, x3-x2)
)

P = Poly(e12, x1, x2, x3, x4)
terms = P.terms()  # [((a1,a2,a3,a4), coeff), ...]

# --- 検査 ---
n_terms = len(terms)
coeffs = [int(c) for (_, c) in terms]  # 整数でなければここで例外
anchors = {
    (0,0,7,1): 1,      # x3^7 x4
    (3,2,2,1): -116,   # x1^3 x2^2 x3^2 x4
    (2,5,0,1): -57,    # x1^2 x2^5 x4
}
anchor_result = {}
d = dict(P.terms())
for mono, expected in anchors.items():
    got = int(d.get(mono, 0))
    anchor_result[str(mono)] = {"expected": expected, "got": got, "ok": got == expected}

# (8.7): e12(x,y,0,0) = f1(x,y)
lhs87 = expand(e12.subs({x1: x, x2: y, x3: 0, x4: 0}, simultaneous=True))
ok87 = expand(lhs87 - f1) == 0

# 線形化二重シャッフル (8.2)(8.3) の 4 本(p.22 逐語)
def sub4(g, a, b, c, dd):
    return g.subs({x1: a, x2: b, x3: c, x4: dd}, simultaneous=True)
V = (x1, x2, x3, x4)
def perm(g, p):  # p = tuple of indices (1-based) meaning f(x_{p1},x_{p2},x_{p3},x_{p4})
    return sub4(g, *[V[i-1] for i in p])
sh1 = [(1,2,3,4),(2,1,3,4),(2,3,1,4),(2,3,4,1)]                     # 1 sha 234
sh2 = [(1,2,3,4),(1,3,2,4),(1,3,4,2),(3,1,2,4),(3,1,4,2),(3,4,1,2)] # 12 sha 34
eq82a = expand(sum(perm(e12, p) for p in sh1))
eq82b = expand(sum(perm(e12, p) for p in sh2))
def sharp(g, p):
    a = V[p[0]-1]; b = a + V[p[1]-1]; c = b + V[p[2]-1]; dd = c + V[p[3]-1]
    return sub4(g, a, b, c, dd)
eq83a = expand(sum(sharp(e12, p) for p in sh1))
eq83b = expand(sum(sharp(e12, p) for p in sh2))

from math import gcd
g_all = 0
for c in coeffs: g_all = gcd(g_all, abs(c))

out = {
    "n_terms": n_terms,
    "all_coeffs_integer": True,  # int() cast above would have raised otherwise
    "gcd_abs_coeffs": g_all,
    "coeff_min": min(coeffs), "coeff_max": max(coeffs),
    "anchors": anchor_result,
    "eq_8_7_holds": bool(ok87),
    "lds_8_2a_zero": eq82a == 0, "lds_8_2b_zero": eq82b == 0,
    "lds_8_3a_zero": eq83a == 0, "lds_8_3b_zero": eq83b == 0,
    "f0": str(factor(f0)), "f1": str(factor(f1)),
    "homogeneous_degree": P.total_degree(),
}
print(json.dumps(out, indent=1))

# 全項リスト(grlex 降順: sympy Poly.terms() の既定順のまま)
rows = [{"exp": list(m), "mono": "*".join(f"x{i+1}^{e}" for i, e in enumerate(m) if e) or "1",
         "coeff": int(c)} for (m, c) in terms]
with open(r"C:\Users\81905\AppData\Local\Temp\claude\C--Users-81905-Desktop-shadow-atelier\d2b80bbe-2be7-426c-9dbe-a39ba301883a\scratchpad\e12_terms.json", "w", encoding="utf-8") as fh:
    json.dump(rows, fh, indent=0)
print("terms written:", len(rows))

# Symbolic check of the uniform (leaf-rooted) derivation of Theorem T3-N0.
#   W = s + W^2,  s = u+z+lam,   Y = W - lam
#   R_comb := (u+z)*Y + lam*W^2        (root = any leaf; black leaf -> Y, leg -> W^2)
#   claim:  R_comb = s*W - 2*lam*(u+z) - lam^2      (exact identity)
#   claim:  [u^t z^f3 lam^f2] R_comb / (m+1) = Cat(m-1)*m!/(t! f2! f3!),  m = t+f2+f3-1 >= 2
from sympy import symbols, Poly, expand, binomial, factorial, Rational, simplify

u, z, lam = symbols('u z lam')
s = u + z + lam
DEG = 8

def trunc(p):
    p = expand(p)
    out = 0
    for mon, c in Poly(p, u, z, lam).terms():
        if sum(mon) <= DEG:
            out += c * u**mon[0] * z**mon[1] * lam**mon[2]
    return expand(out)

# W = s + W^2 by iteration
W = 0
for _ in range(DEG + 2):
    W = trunc(s + W*W)
Y = expand(W - lam)
R = trunc(expand((u + z)*Y + lam*W*W))
lhs = trunc(expand(R + 2*lam*(u + z) + lam**2))
rhs = trunc(expand(s*W))
print("identity R = s*W - 2*lam*(u+z) - lam^2  :", expand(lhs - rhs) == 0)

def cat(i):
    return binomial(2*i, i) // (i + 1)

bad = 0; checked = 0
Rp = Poly(R, u, z, lam)
for (t, f3, f2), c in Rp.terms():
    m = t + f2 + f3 - 1
    if m < 2:
        continue
    pred = Rational(cat(m-1) * factorial(m), factorial(t)*factorial(f2)*factorial(f3))
    got = Rational(c, m + 1)
    checked += 1
    if got != pred:
        bad += 1
        print(f"  MISMATCH t={t} f2={f2} f3={f3} m={m}: rooted={c} /(m+1)={got} vs {pred}")
print(f"coefficient check (m>=2, deg<= {DEG}): checked={checked} mismatches={bad}")

# also: the OLD derivation (root at a looped black leaf, divide by t) must agree where t>=1
Rold = trunc(expand(u*Y))
bad2 = 0; checked2 = 0
for (t, f3, f2), c in Poly(Rold, u, z, lam).terms():
    m = t + f2 + f3 - 1
    if m < 2 or t < 1:
        continue
    pred = Rational(cat(m-1)*factorial(m), factorial(t)*factorial(f2)*factorial(f3))
    got = Rational(c, t)
    checked2 += 1
    if got != pred:
        bad2 += 1
        print(f"  OLD MISMATCH t={t} f2={f2} f3={f3} m={m}: {got} vs {pred}")
print(f"old derivation cross-check (t>=1): checked={checked2} mismatches={bad2}")

# how many passports have t = f3 = 0 (only leg-rooting available)?
only_leg = [(t, f2, f3) for (t, f3, f2), c in Rp.terms()
            if t == 0 and f3 == 0 and t + f2 + f3 - 1 >= 2]
print("passports with t=f3=0 (old rooting impossible):", sorted(only_leg))

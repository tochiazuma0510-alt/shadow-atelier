# Lemma C-DEG check: linking numbers (= PB_3 abelianization) of the hexagon
# defects (2.18)/(2.19) of Dolgushev-Le-Lorenz 2008.00066.
#
#   D1 = [s1^L f^-1 s2^L f] * [f^-1 s1 s2 (x13 x23)^m]^-1
#   D2 = [f^-1 s2^L f s1^L] * [s2 s1 (x12 x13)^m f]^-1        (L = 2m+1)
#
# claim (hand computation):
#   lk(D1) = ( r , p+q-r , r ),   lk(D2) = ( r-p-q , -r , -r )
# in coordinates (lk12, lk23, lk13), where (p,q,r) = lk(f).
# In particular deg_c(D1) = lk13(D1) = r = deg_c(f)  and  deg_c(D2) = -r,
# because deg_c = lk13 for PB_3 = <x12,x23> x <c>, c = x12 x13 x23.
import random
from fractions import Fraction

# braid letters: +i = sigma_i, -i = sigma_i^{-1}   (i in {1,2}; positions 1..3)
def lk_of(word, nstr=3):
    """signed crossing counts / 2, by unordered pair of STRAND labels."""
    pos = list(range(nstr))            # pos[k] = strand sitting at position k
    cnt = {}
    for L in word:
        i, s = abs(L) - 1, (1 if L > 0 else -1)
        a, b = pos[i], pos[i+1]
        key = (min(a, b), max(a, b))
        cnt[key] = cnt.get(key, 0) + s
        pos[i], pos[i+1] = pos[i+1], pos[i]
    assert pos == list(range(nstr)), f"not a pure braid: {pos}"
    return {k: Fraction(v, 2) for k, v in cnt.items()}

def inv(w):  return [-L for L in reversed(w)]
def pw(w, n):
    return w*n if n >= 0 else inv(w)*(-n)

s1, s2 = [1], [2]
x12 = pw(s1, 2)
x23 = pw(s2, 2)
x13 = inv(s1) + x23 + s1          # = s1^-1 s2^2 s1  (C1 (A.4) form)
c   = x12 + x13 + x23             # (A.5)

def vec(d):  # (lk12, lk23, lk13) with strands 0,1,2 == 1,2,3
    return (d.get((0,1), 0), d.get((1,2), 0), d.get((0,2), 0))

print("lk(x12) =", vec(lk_of(x12)), " lk(x23) =", vec(lk_of(x23)),
      " lk(x13) =", vec(lk_of(x13)), " lk(c) =", vec(lk_of(c)))

def rand_f(nlet, with_c=True):
    gens = [x12, x23, x13] + ([c] if with_c else [])
    w = []
    for _ in range(nlet):
        g = random.choice(gens)
        w += g if random.random() < .5 else inv(g)
    return w

bad = 0; checked = 0
random.seed(20260731)
for trial in range(400):
    m = random.choice([-3, -1, 0, 1, 2, 3, 4])
    L = 2*m + 1
    f = rand_f(random.randint(0, 5))
    p, q, r = vec(lk_of(f))
    lhs1 = pw(s1, L) + inv(f) + pw(s2, L) + f
    rhs1 = inv(f) + s1 + s2 + pw(x13 + x23, m)
    D1 = lhs1 + inv(rhs1)
    lhs2 = inv(f) + pw(s2, L) + f + pw(s1, L)
    rhs2 = s2 + s1 + pw(x12 + x13, m) + f
    D2 = lhs2 + inv(rhs2)
    got1, got2 = vec(lk_of(D1)), vec(lk_of(D2))
    exp1, exp2 = (r, p+q-r, r), (r-p-q, -r, -r)
    checked += 1
    if got1 != exp1 or got2 != exp2:
        bad += 1
        print(f"  MISMATCH m={m} lk(f)={(p,q,r)}: D1 {got1} vs {exp1}; D2 {got2} vs {exp2}")

print(f"random trials: checked={checked} mismatches={bad}")

# central-shift check: f -> f*c^k must send D1 -> D1*c^k and D2 -> D2*c^-k
bad2 = 0
for trial in range(100):
    m = random.choice([0, 1, 2, 3, 4]); L = 2*m+1
    f = rand_f(random.randint(0, 4), with_c=False)
    k = random.randint(-3, 3)
    fk = f + pw(c, k)
    def D(ff):
        d1 = pw(s1,L)+inv(ff)+pw(s2,L)+ff + inv(inv(ff)+s1+s2+pw(x13+x23,m))
        d2 = inv(ff)+pw(s2,L)+ff+pw(s1,L) + inv(s2+s1+pw(x12+x13,m)+ff)
        return vec(lk_of(d1)), vec(lk_of(d2))
    a1, a2 = D(f); b1, b2 = D(fk)
    ck = vec(lk_of(pw(c, k)))
    if b1 != tuple(x+y for x, y in zip(a1, ck)) or b2 != tuple(x-y for x, y in zip(a2, ck)):
        bad2 += 1
        print("  CENTRAL-SHIFT MISMATCH", m, k, a1, b1, a2, b2)
print(f"central shift f->f*c^k: mismatches={bad2}")

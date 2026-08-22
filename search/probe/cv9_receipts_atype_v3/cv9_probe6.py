"""Stress the ONE new unasserted premise in v3.2: safe_e4_inverse() assumes the
pc group has EXPONENT 3 (p^-1 == p^2 for EVERY p).  core.py only guarantees
relative_orders == 3 for the GENERATORS (x_i^3=1), which does NOT imply the
group has exponent 3 -- a polycyclic 3-group of class >= 3 can have elements of
order 9.  Adversarial sample: deep commutators / long words, where order 9 would
first appear."""
import sys, random, json
from pathlib import Path
ROOT = Path(r"C:\Users\81905\Desktop\shadow-atelier")
sys.path.insert(0, str(ROOT / "search"))
import koubou158_L3_core_v1_1 as core

q3 = json.loads((ROOT / core.Q3_CHIEF).read_text(encoding="utf-8"))
pc = core.IndependentPc(q3["groups"]["PB4"])
ONE = pc.one()
print("pc: n =", pc.n, " |pc| = 3^n =", 3 ** pc.n)

gens = [pc.collect([i]) for i in range(1, pc.n + 1)]
inv_coords = [row["inverse_coords"] for row in q3["groups"]["PB4"]["marked_generators"]]
print("marked_generators inverse_coords (first 6 gens):", inv_coords)


def cube_ok(p):
    return pc.mul(p, pc.mul(p, p)) == ONE


random.seed(11)
bad = []
n = 0

# (1) random words
for _ in range(3000):
    w = [random.choice(range(1, pc.n + 1)) for _ in range(random.randint(1, 40))]
    p = pc.collect(w); n += 1
    if not cube_ok(p): bad.append(("randword", w))

# (2) deep commutators -- where exponent 9 shows up first if class >= 3
def comm(a, b):
    return pc.mul(pc.mul(a, b), pc.mul(pc.mul(a, pc.mul(a, a)) if False else inv(a), inv(b)))
def inv(p):
    return pc.mul(p, p)  # ONLY valid if exponent 3 -- use cautiously; verified below per element
# safer: build inverses by brute order
def true_inv(p):
    cur = p
    for k in range(1, 30):
        if cur == ONE:
            v = ONE
            for _ in range(k - 1): v = pc.mul(v, p)
            return v, k
        cur = pc.mul(cur, p)
    raise RuntimeError("order > 30")

orders = {}
sample = []
for _ in range(400):
    w = [random.choice(range(1, pc.n + 1)) for _ in range(random.randint(1, 30))]
    sample.append(pc.collect(w))
for i in range(0, len(sample) - 1, 2):
    a, b = sample[i], sample[i + 1]
    ai, _ = true_inv(a); bi, _ = true_inv(b)
    c1 = pc.mul(pc.mul(a, b), pc.mul(ai, bi))
    c2 = pc.mul(pc.mul(a, c1), pc.mul(ai, true_inv(c1)[0]))
    c3 = pc.mul(pc.mul(b, c2), pc.mul(bi, true_inv(c2)[0]))
    for p in (c1, c2, c3):
        n += 1
        _, o = true_inv(p)
        orders[o] = orders.get(o, 0) + 1
        if not cube_ok(p): bad.append(("deepcomm", None))

# (3) all products of <= 3 generators
for i in range(1, pc.n + 1):
    for j in range(1, pc.n + 1):
        for k in range(1, pc.n + 1):
            p = pc.collect([i, j, k]); n += 1
            if not cube_ok(p): bad.append(("triple", (i, j, k)))

print(f"\nelements tested for p^3 == 1: {n}")
print(f"VIOLATIONS (element of order 9 or more): {len(bad)}")
print(f"observed element orders among deep commutators: {orders}")
print("VERDICT:", "exponent-3 premise HOLDS on this adversarial sample"
      if not bad else f"EXPONENT-3 PREMISE FALSIFIED -- examples: {bad[:3]}")

import sys, importlib.util
from pathlib import Path
ROOT = Path(r"C:\Users\81905\Desktop\shadow-atelier")
spec = importlib.util.spec_from_file_location("prod", str(ROOT / "scratchpad" / "d972_atype_v3_production.py"))
prod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prod)
core = prod.core
p0v4 = prod.p0v4

eng = prod.Engine()
E = eng.e4
K = eng.KAPPA

print("\n=== P1. ord(c) / CPOW integrity ===")
print("len(CPOW) =", len(eng.CPOW), "(must be 18 for c^m to be an injective label)")
cur = E.identity; order = None
for k in range(1, 200):
    cur = E.mul(cur, eng.c_val)
    if cur == E.identity:
        order = k; break
print("actual ord(c) in e4 =", order)
# ord of x,y images per slot
for i in range(5):
    ox = oy = None
    v = E.identity
    for k in range(1, 200):
        v = E.mul(v, E.eval(eng.push([1], i)))
        if v == E.identity: ox = k; break
    v = E.identity
    for k in range(1, 200):
        v = E.mul(v, E.eval(eng.push([2], i)))
        if v == E.identity: oy = k; break
    print(f"  slot{i}: ord(x)={ox} ord(y)={oy}")

print("\n=== P2. the 72 agreement cells: TRUTH DISTRIBUTION ===")
cases = [[], [2, -1], [2, 2, -1, -1], eng.W]
from collections import Counter
cnt = Counter(); trues = []
for w in cases:
    for m in range(K):
        a1 = eng.hexA_ad(w, 0)
        b1 = eng.hexB_ad_klog(w, m, 0) == m % K
        cnt[(a1, b1)] += 1
        if a1 and b1: trues.append((w, m))
print("distribution of (thetaGate, hexGate) over 72 cells:", dict(cnt))
print("cells where BOTH hold:", trues)

print("\n=== P3. HYBRID-DEFECT DETECTOR (erratum (a): Ad-LHS vs RHS=1) ===")
# defective predicate = Ad-form LHS compared to identity (RHS=1)
diffs = []
for w in cases:
    for m in range(K):
        correct = eng.hexB_ad_klog(w, m, 0) == m % K
        hybrid = eng.hexB_ad_klog(w, m, 0) == 0
        if correct != hybrid:
            diffs.append((w, m, correct, hybrid))
print(f"self-test case set: cells where correct(RHS=c^m) != hybrid(RHS=1): {len(diffs)}/72")
for d in diffs[:10]: print("   ", d)

print("\n=== P4. spec 4.3 witness table reproduction (the identity test) ===")
f_pp = eng.compose((3, eng.W), (3, eng.W))
print("compose((3,W),(3,W)) -> m=", f_pp[0], " len(f'')=", len(f_pp[1]))
witness = {
    "f=1  (lam=1)  m=0":  ([], 0),
    "f=1  (lam=1)  m=9":  ([], 9),
    "f=1  (lam=17) m=8":  ([], 8),
    "f=1  (lam=17) m=17": ([], 17),
    "f=W  (lam=7)  m=3":  (eng.W, 3),
    "f=W  (lam=7)  m=12": (eng.W, 12),
    "f=W  (lam=11) m=5":  (eng.W, 5),
    "f=W  (lam=11) m=14": (eng.W, 14),
    "f=f''(lam=13) m=6":  (f_pp[1], 6),
    "f=f''(lam=13) m=15": (f_pp[1], 15),
    "f=f''(lam=5)  m=2":  (f_pp[1], 2),
    "f=f''(lam=5)  m=11": (f_pp[1], 11),
}
for label, (w, m) in witness.items():
    s0 = eng.is_gtpair_slot(w, m, 0)
    a5 = eng.is_gtpair_all5(w, m)
    ch = eng.charming_gate(w)
    print(f"  {label:22s} slot0={str(s0):5s} all5={str(a5):5s} charming={ch}")

print("\n=== P5. full m-scan of the three witness f's (which m pass?) ===")
for name, w in (("f=1", []), ("f=W", eng.W), ("f=f''", f_pp[1])):
    ok0 = [m for m in range(K) if eng.is_gtpair_slot(w, m, 0)]
    ok5 = [m for m in range(K) if eng.is_gtpair_all5(w, m)]
    print(f"  {name}: slot0 pass m={ok0}")
    print(f"  {name}: all5  pass m={ok5}")

print("\n=== P6. is gate 3 (5 cofaces) non-vacuous? per-slot verdicts ===")
for name, w in (("f=1", []), ("f=W", eng.W), ("f=f''", f_pp[1])):
    for m in range(K):
        v = [eng.is_gtpair_slot(w, m, i) for i in range(5)]
        if len(set(v)) > 1:
            print(f"  SLOT-DEPENDENT: {name} m={m} -> {v}")
print("  (no line above = all 5 slots always agree => gate 3 never rejects anything)")

print("\n=== P7. destructive control: does the instrument ever say NO? ===")
neg = [[1], [1, 2], [1, -2], [1, 1, 2, -1, -2, -1], [2, 1, -2, -1]]
for w in neg:
    res = [(m, eng.is_gtpair_slot(w, m, 0)) for m in range(K)]
    yes = [m for m, r in res if r]
    print(f"  w={w}: theta gate={eng.hexA_ad(w,0)}  m passing (3.11)={yes}  charming={eng.charming_gate(w)}")

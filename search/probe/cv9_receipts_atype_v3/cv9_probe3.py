import sys, importlib.util
from pathlib import Path
ROOT = Path(r"C:\Users\81905\Desktop\shadow-atelier")
spec = importlib.util.spec_from_file_location("p31", str(ROOT / "scratchpad" / "d972_atype_v3_1_production.py"))
P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
core = P.core
eng = P.Engine(); K = 18
W = P.W_WORD
m_fpp, f_pp = P.build_f_double_prime(eng)
bases = {1: (0, []), 17: (17, []), 7: (3, W), 11: (14, W), 13: (6, f_pp), 5: (11, f_pp)}

print("\n=== D1. anatomy of the 36-cell gate4 grid (cap in code = len(f) < 1500) ===")
rows = []
for l1, p1 in sorted(bases.items()):
    for l2, p2 in sorted(bases.items()):
        m, f = eng.compose(p1, p2)
        capped = not (len(f) < 1500)
        rows.append((l1, l2, m, (2*m+1) % K, len(f), capped, eng.charming_gate(f), l1*l2 % K))
fails = [r for r in rows if r[5]]
print(f"  cells with len(f) >= 1500 (silently marked NOT closed): {len(fails)}/36")
for r in fails:
    print(f"    lam1={r[0]:2d} lam2={r[1]:2d} -> m={r[2]:2d} lam={r[3]:2d} (lam1*lam2={r[7]:2d}) len(f)={r[4]:6d} charming={r[6]}")
print(f"  lambda multiplicativity (lam == lam1*lam2 mod 18) over all 36: "
      f"{all(r[3] == r[7] for r in rows)}")
print(f"  non-charming composites among all 36: {[ (r[0],r[1]) for r in rows if not r[6] ]}")
print(f"  max len(f) among UNCAPPED cells: {max(r[4] for r in rows if not r[5])}")

print("\n=== D2. re-evaluate the 8 capped cells with NO cap (the decisive test) ===")
import time
for l1, p1 in sorted(bases.items()):
    for l2, p2 in sorted(bases.items()):
        m, f = eng.compose(p1, p2)
        if len(f) < 1500:
            continue
        t0 = time.time()
        ch = eng.charming_gate(f)
        gp = eng.is_gtpair_all5(f, m)
        per = [eng.gtpair_B_slot(f, m, i) for i in range(5)]
        print(f"    lam1={l1:2d} lam2={l2:2d} m={m:2d} len={len(f):6d} charming={ch} "
              f"ALL5={gp} per-slot={per}  [{time.time()-t0:.1f}s]")

print("\n=== D3. naive-product negative control: which 11 cells 'pass' and why ===")
ok = []
for l1, p1 in sorted(bases.items()):
    for l2, p2 in sorted(bases.items()):
        nf = core.reduce_word(p1[1] + p2[1]); nm = (p1[0] + p2[0]) % K
        v = eng.verdict(nf, nm) if len(nf) < 1500 else {"charming": None, "gtpair_all5": None}
        if bool(v.get("gtpair_all5")):
            ok.append((l1, l2, nm, len(nf), p1[1] == [] or p2[1] == []))
print(f"  naive control cells that CLOSE (control leaks): {len(ok)}/36")
for r in ok:
    print(f"    lam1={r[0]:2d} lam2={r[1]:2d} naive_m={r[2]:2d} len={r[3]:3d} one_operand_is_identity={r[4]}")

print("\n=== D4. (3.53)-order loop blow-up (w_verification_series item iv) ===")
p = (3, W); cur = p
for k in range(1, 13):
    cur = eng.compose(cur, p)
    print(f"    step {k:2d}: m={cur[0]:2d} len(f)={len(cur[1]):,}   equals-p? {cur == p}")
    if len(cur[1]) > 3_000_000:
        print("    ... growth ~9x/step; loop range is 40 -> unreachable (memory blow-up). ABORTING probe.")
        break

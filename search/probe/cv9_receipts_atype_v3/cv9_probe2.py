import sys, json, random, importlib.util
from pathlib import Path
ROOT = Path(r"C:\Users\81905\Desktop\shadow-atelier")
sys.path.insert(0, str(ROOT / "search")); sys.path.insert(0, str(ROOT / "scratchpad"))
import koubou158_L3_core_v1_1 as core
import audit_P0_naive_judge_v4 as A
spec = importlib.util.spec_from_file_location("prod", str(ROOT / "scratchpad" / "d972_atype_v3_production.py"))
prod = importlib.util.module_from_spec(spec); spec.loader.exec_module(prod)

eng = prod.Engine(); e4 = eng.e4; K = 18
q3 = A.load_q3(); cofaces = q3["formulas"]["cofaces_3_4"]
TAU_X, TAU_Y = [2], [-2, -1]; TH_X, TH_Y = [2], [1]
tau0 = lambda w: A.reduce_word(core.substitute2(w, TAU_X, TAU_Y))
th0 = lambda w: A.reduce_word(core.substitute2(w, TH_X, TH_Y))
def predB(w, m, i):
    g = A.reduce_word([2]*m + w)
    lhs = A.reduce_word(tau0(tau0(g)) + tau0(g) + g)
    a = e4.eval(A.push_through_coface_letters(A.reduce_word(w + th0(w)), cofaces[i])) == e4.identity
    b = e4.eval(A.push_through_coface_letters(lhs, cofaces[i])) == e4.identity
    return a, b
refAll5 = lambda w, m: all(a and b for a, b in (predB(w, m, i) for i in range(5)))

print("=== Q1. structure of the 1170-cell A/B disagreements (spec claims CONJUNCTION agrees) ===")
random.seed(2)
cases = [[], [2,-1], [2,2,-1,-1], eng.W, A.FIXED_WORD]
cases += [A.reduce_word([random.choice([1,-1,2,-2]) for _ in range(random.randint(1,14))]) for _ in range(60)]
tup_dis = conj_dis = 0; bad = []
for w in cases:
    for m in range(K):
        a1 = eng.hexA_ad(w,0); b1 = (eng.hexB_ad_klog(w,m,0) == m % K)
        a2, b2 = predB(w, m, 0)
        if (a1,b1) != (a2,b2):
            tup_dis += 1
            if (a1 and b1) != (a2 and b2):
                conj_dis += 1; bad.append((w,m,(a1,b1),(a2,b2)))
print(f"  cells={len(cases)*K}  TUPLE-level disagreements={tup_dis}   CONJUNCTION-level disagreements={conj_dis}")
print(f"  -> spec claim ('judgment/conjunction agrees on 1170 cells') = {'HOLDS' if conj_dis==0 else 'FAILS'}")
if bad: print("   examples:", bad[:5])
print("  NOTE: production self_test_predicate_agreement compares TUPLES and core.require-aborts on any mismatch.")

print("\n=== Q2. production is_gtpair_all5  vs  reference word-level all-5 ===")
f_pp = eng.compose((3, eng.W), (3, eng.W))
tbl = [("f=1", []), ("y x^-1", [2,-1]), ("y^4x^-4", [2]*4+[-1]*4),
       ("W", eng.W), ("f''", f_pp[1]), ("FIXED_WORD", A.FIXED_WORD)]
for nm, w in tbl:
    p5 = [m for m in range(K) if eng.is_gtpair_all5(w, m)]
    r5 = [m for m in range(K) if refAll5(w, m)]
    ps0 = [m for m in range(K) if eng.is_gtpair_slot(w, m, 0)]
    rs0 = [m for m in range(K) if all(predB(w, m, 0))]
    flag = "  <<< DIVERGENT" if p5 != r5 else ""
    print(f"  {nm:11s} slot0 prod={ps0} ref={rs0} | ALL5 prod={p5} ref={r5}{flag}")

print("\n=== Q3. frame hypothesis: slot i's own local-B3 frame (only slots 0 and 4 have one) ===")
tab = eng.table
frames = {0: ([2,3],[2,3,2],[4,5,6]), 4: ([1,2],[1,2,1],[1,2,3])}
for i,(dw,hw,cw) in frames.items():
    imd = A.aij_automorphism_images(dw, tab); imd2 = A.aij_automorphism_images(dw*2, tab)
    imh = A.aij_automorphism_images(hw, tab); cv = e4.eval(cw)
    cp = {}; cur = e4.identity
    for k in range(K): cp[cur] = k; cur = e4.mul(cur, cv)
    def nat(w, m, imd=imd, imd2=imd2, imh=imh, cp=cp, i=i):
        fp = A.push_through_coface_letters(w, cofaces[i])
        if e4.eval(fp + A.apply_automorphism(fp, imh)) != e4.identity: return False
        g = A.reduce_word(A.push_through_coface_letters([2]*m, cofaces[i]) + fp)
        return cp.get(e4.eval(A.apply_automorphism(g, imd2) + A.apply_automorphism(g, imd) + g)) == m % K
    for nm, w in (("f=1", []), ("W", eng.W)):
        native = [m for m in range(K) if nat(w, m)]
        frozen = [m for m in range(K) if eng.is_gtpair_slot(w, m, i)]
        ref = [m for m in range(K) if all(predB(w, m, i))]
        print(f"  slot{i} {nm:4s}: NATIVE-frame Ad-form={native}  PRODUCTION(frozen slot0 frame)={frozen}  word-level ref={ref}")

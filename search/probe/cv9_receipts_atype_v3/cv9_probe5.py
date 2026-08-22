import sys, time, importlib.util
from pathlib import Path
ROOT = Path(r"C:\Users\81905\Desktop\shadow-atelier")
s = importlib.util.spec_from_file_location("p32", str(ROOT / "scratchpad" / "d972_atype_v3_2_production.py"))
P = importlib.util.module_from_spec(s); s.loader.exec_module(P)
core = P.core
eng = P.Engine(); e4 = eng.e4; K = 18; W = P.W_WORD
MUL = e4.mul; ONE = e4.identity

print("\n=== S1. safe_e4_inverse() correctness (v3.2's home-made inverse -- highest-risk new code) ===")
import random
random.seed(5)
els = [e4.eval([random.choice([1,-1,2,3,-3,4,5,6,-6]) for _ in range(random.randint(1,25))]) for _ in range(400)]
els += [e4.eval(eng.cofaces[i][j]) for i in range(5) for j in range(3)]
bad = [v for v in els if MUL(v, P.safe_e4_inverse(e4, v)) != ONE or MUL(P.safe_e4_inverse(e4, v), v) != ONE]
print(f"  {len(els)} elements tested: two-sided-inverse failures = {len(bad)}")
pc_bad = [v for v in els if e4.pc.mul(v[1], e4.pc.mul(v[1], v[1])) != e4.pc.one()]
print(f"  pc exponent-3 claim (p^3 == 1) violations: {len(pc_bad)}")
assert not bad and not pc_bad
print("  safe_e4_inverse VALIDATED (exponent-3 premise holds on this sample).")

# ---------- independent linear evaluator (mine, from probe4) ----------
_IC = {}
def INV(a):
    if a in _IC: return _IC[a]
    cur = a
    for k in range(1, 401):
        if cur == ONE:
            v = ONE
            for _ in range(k-1): v = MUL(v, a)
            _IC[a] = v; return v
        cur = MUL(cur, a)
    raise RuntimeError
def evalw(w, A, B):
    Ai, Bi = INV(A), INV(B); v = ONE
    for L in w: v = MUL(v, A if L==1 else Ai if L==-1 else B if L==2 else Bi)
    return v
def powe(a,k):
    v = ONE
    for _ in range(k): v = MUL(v,a)
    return v
TOW = {}
for i in range(5):
    X = e4.eval(eng.cofaces[i][0]); Y = e4.eval(eng.cofaces[i][2]); XY = MUL(X,Y)
    TOW[i] = [(X,Y),(Y,INV(XY)),(INV(XY),X)]
def myslot(f,m,i):
    (X0,Y0),(X1,Y1),(X2,Y2) = TOW[i]
    a = MUL(evalw(f,X0,Y0), evalw(f,Y0,X0)) == ONE
    b = MUL(MUL(MUL(powe(Y2,m),evalw(f,X2,Y2)), MUL(powe(Y1,m),evalw(f,X1,Y1))),
            MUL(powe(Y0,m),evalw(f,X0,Y0))) == ONE
    return a,b
myall5 = lambda f,m: all(all(myslot(f,m,i)) for i in range(5))

print("\n=== S2. my independent evaluator vs v3.2 predB_fast ===")
m_fpp, f_pp = P.build_f_double_prime(eng)
n=bad2=0
for f in ([], [2,-1], W, f_pp, P.theta_false_charming_word(), [1,2,-1,-2]):
    for m in range(K):
        for i in range(5):
            n+=1
            if myslot(f,m,i) != eng.predB_fast(f,m,i): bad2+=1
print(f"  {n} cells compared: disagreements={bad2}")
assert bad2==0
print("  v3.2 linear evaluator VALIDATED against an independent implementation.")

# ---------- fast free-group substitution (single final reduction) ----------
def subst_fast(w, xw, yw):
    xi, yi = core.inv_word(xw), core.inv_word(yw)
    out=[]
    for L in w: out.extend(xw if L==1 else xi if L==-1 else yw if L==2 else yi)
    return core.reduce_word(out)
def E_fast(m,f,w):
    lr = (2*m+1)%K; lam = lr if lr<=9 else lr-K
    xw = [1]*lam if lam>=0 else [-1]*(-lam)
    yp = [2]*lam if lam>=0 else [-2]*(-lam)
    return subst_fast(w, xw, core.reduce_word(core.inv_word(f)+yp+f))
def comp_fast(p1,p2):
    (m1,f1),(m2,f2)=p1,p2
    return ((2*m1*m2+m1+m2)%K, core.reduce_word(f1+E_fast(m1,f1,f2)))
print("\n=== S3. validate comp_fast against Engine.compose ===")
for p1 in [(3,W),(14,W),(6,f_pp),(11,f_pp),(17,[]),(0,[])]:
    for p2 in [(3,W),(6,f_pp),(0,[])]:
        assert comp_fast(p1,p2) == eng.compose(p1,p2), (p1[0],p2[0])
print("  comp_fast == Engine.compose on 18 pairs. VALIDATED.")

print("\n=== S4. IDENTIFY f12 and f5 inside v3.2's OWN gate4 grid ===")
f12_m, f12 = comp_fast((11,f_pp),(11,f_pp))   # lambda 5 x 5 = 25 = 7
f5_m,  f5  = comp_fast((6,f_pp),(11,f_pp))    # lambda 13 x 5 = 65 = 11
for nm,(m,f) in (("f12",(f12_m,f12)),("f5",(f5_m,f5))):
    t0=time.time(); ok = myall5(f,m); ch = eng.charming_gate(f)
    print(f"  {nm}: m={m} len={len(f)} charming={ch} ALL5={ok}  [{time.time()-t0:.1f}s]")

print("\n=== S5. close m=15 and m=2 ===")
for nm, p2 in (("m15", (f12_m, f12)), ("m2", (f5_m, f5))):
    t0=time.time()
    m,f = comp_fast((3,W), p2)
    ok = myall5(f,m); ch = eng.charming_gate(f)
    print(f"  {nm}: route compose((3,W),({p2[0]},{'f12' if nm=='m15' else 'f5'})) -> "
          f"m={m} lambda={(2*m+1)%K} len={len(f)} charming={ch} ALL5={ok}  [{time.time()-t0:.1f}s]")

# S4 diagonal labelling that reproduces the canon labels (1,2)/(1,3,4) in the
# MakeGn block basis (which differs from the canon (4.7)/(4.8) basis by diag(1,1,-1)).
from itertools import product
P=5
def mv(M,v): return tuple(sum(M[i][k]*v[k] for k in range(3))%P for i in range(3))
def mm(M,N): return tuple(tuple(sum(M[i][k]*N[k][j] for k in range(3))%P for j in range(3)) for i in range(3))
TH_c=((0,1,0),(1,0,0),(0,0,4)); TA_c=((0,0,1),(1,0,0),(0,1,0))          # canon basis
TH_p=((0,1,0),(1,0,0),(0,0,4)); TA_p=((0,0,4),(1,0,0),(0,4,0))          # MakeGn block basis (measured)
d=((1,0,0),(0,1,0),(0,0,4))
print("basis change check: d*TA_p*d == TA_c :", mm(mm(d,TA_p),d)==TA_c,
      "   d*TH_p*d == TH_c :", mm(mm(d,TH_p),d)==TH_c)
def norm(v):
    v=tuple(x%P for x in v); a=tuple((-x)%P for x in v); return min(v,a)
def labels(diag, TH, TA, extra=()):
    lab={norm(tuple(x%P for x in dv)):k for k,dv in diag.items()}
    def perm_of(M): return tuple(lab[norm(mv(M,tuple(x%P for x in diag[k])))] for k in (1,2,3,4))
    def cyc(p):
        seen,out=set(),[]
        for st in range(1,5):
            if st in seen: continue
            c,cur=[],st
            while cur not in seen: seen.add(cur); c.append(cur); cur=p[cur-1]
            if len(c)>1: out.append(tuple(c))
        return out or "id"
    return [(nm,cyc(perm_of(M))) for nm,M in (("Delta",TH),("delta",TA))+extra]
DIAG_c={1:(1,1,-1),2:(1,1,1),3:(-1,1,1),4:(1,-1,1)}
DIAG_p={1:(1,1,1), 2:(1,1,-1),3:(-1,1,-1),4:(1,-1,-1)}   # = d.DIAG_c
print("canon basis, l = ", DIAG_c, "->", labels(DIAG_c,TH_c,TA_c,
      (("sigma1",mm(mm(TA_c,TA_c),TH_c)),("sigma2",mm(TH_c,mm(TA_c,TA_c))))))
print("MakeGn basis, l'= ", DIAG_p, "->", labels(DIAG_p,TH_p,TA_p,
      (("sigma1",mm(mm(TA_p,TA_p),TH_p)),("sigma2",mm(TH_p,mm(TA_p,TA_p))))))

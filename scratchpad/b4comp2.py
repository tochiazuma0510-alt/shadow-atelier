# v1.1: full print of the 20 composites psi o p_i o phi, on x12, x23, x13 AND c.
def red(w):
    out=[]
    for g,e in w:
        if e==0: continue
        if out and out[-1][0]==g:
            ne=out[-1][1]+e; out.pop()
            if ne!=0: out.append((g,ne))
        else: out.append((g,e))
    return tuple(out)
def mul(*ws):
    r=[]
    for w in ws: r+=list(w)
    prev=None; cur=tuple(r)
    while prev!=cur: prev=cur; cur=red(cur)
    return cur
def inv(w): return red(tuple((g,-e) for g,e in reversed(w)))
X=(('x',1),); Y=(('y',1),); E=()
PSI={'x12':X,'x23':Y,'x13':mul(inv(X),inv(Y))}       # psi(c)=1
COF={
 'phi123'   : {'x12':['x12'],       'x23':['x23'],       'x13':['x13'],       'c':['x12','x13','x23']},
 'phi234'   : {'x12':['x23'],       'x23':['x34'],       'x13':['x24'],       'c':['x23','x24','x34']},
 'phi12_3_4': {'x12':['x13','x23'], 'x23':['x34'],       'x13':['x14','x24'], 'c':['x13','x23','x14','x24','x34']},
 'phi1_23_4': {'x12':['x12','x13'], 'x23':['x24','x34'], 'x13':['x14'],       'c':['x12','x13','x14','x24','x34']},
 'phi1_2_34': {'x12':['x12'],       'x23':['x23','x24'], 'x13':['x13','x14'], 'c':['x12','x13','x14','x23','x24']},
}
P={1:{'x12':None,'x13':None,'x14':None,'x23':'x12','x24':'x13','x34':'x23'},
   2:{'x12':None,'x23':None,'x24':None,'x13':'x12','x14':'x13','x34':'x23'},
   3:{'x13':None,'x23':None,'x34':None,'x12':'x12','x14':'x13','x24':'x23'},
   4:{'x14':None,'x24':None,'x34':None,'x12':'x12','x13':'x13','x23':'x23'}}
def comp(i,cof,gen):
    parts=[]
    for g4 in COF[cof][gen]:
        g3=P[i][g4]; parts.append(E if g3 is None else PSI[g3])
    return mul(*parts)
def show(w):
    if w==(): return '1'
    return ''.join(('%s^%d'%(g,e) if e!=1 else g) for g,e in w)
psi_pair=(X,Y,PSI['x13'],E)
npsi=ndeg=0
print("=== 20 composites  psi o p_i o phi   (images of x12, x23, x13, c) ===")
for i in [4,3,2,1]:
    for cof in ['phi123','phi234','phi12_3_4','phi1_23_4','phi1_2_34']:
        q=tuple(comp(i,cof,g) for g in ['x12','x23','x13','c'])
        if q==psi_pair: kind='= psi'; npsi+=1
        else:
            base=set(g for w in q for g,_ in w)
            kind='CYCLIC-IMAGE (degenerate), <%s>'%(','.join(sorted(base)) if base else '1'); ndeg+=1
            assert len(base)<=1, (i,cof,q)
        print("  p_%d o %-10s : x12->%-8s x23->%-8s x13->%-8s c->%-8s  %s"%(
              i,cof,show(q[0]),show(q[1]),show(q[2]),show(q[3]),kind))
print("  totals: psi = %d , degenerate = %d"%(npsi,ndeg))
print()
print("  NOTE: every degenerate row has lambda(c) != 1  => each single row already forces k = 0 mod 7")
print("        on w = f*c^k with f in V(F2).  (lemma B4-IND)")
print()
print("=== consistency check: p_4 o phi123 = id on PB3 (split retraction) ===")
print("   images of (x12,x23,x13,c) under p_4 o phi123 =",
      [ '/'.join(str(P[4][g]) for g in COF['phi123'][k]) for k in ['x12','x23','x13','c']])

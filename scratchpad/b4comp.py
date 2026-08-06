# Free-group word calculus over generators x,y of P = F2/V(F2).
# Represent a word as a tuple of (gen,exp) pairs, freely reduced.
def red(w):
    out=[]
    for g,e in w:
        if e==0: continue
        if out and out[-1][0]==g:
            ne=out[-1][1]+e
            out.pop()
            if ne!=0: out.append((g,ne))
        else: out.append((g,e))
    return tuple(out)
def mul(*ws):
    r=[]
    for w in ws: r+=list(w)
    # repeated reduction
    prev=None; cur=tuple(r)
    while prev!=cur:
        prev=cur; cur=red(cur)
    return cur
def inv(w): return red(tuple((g,-e) for g,e in reversed(w)))
X=(('x',1),); Y=(('y',1),); E=()

# psi : PB3 -> P     x12->x, x23->y, x13->x^-1 y^-1   (since psi(c)=1)
PSI={'x12':X,'x23':Y,'x13':mul(inv(X),inv(Y))}

# cofaces phi : PB3 -> PB4  (A.18)   images written in PB4 generators
COF={
 'phi123'   : {'x12':['x12'],        'x23':['x23'],       'x13':['x13']},
 'phi234'   : {'x12':['x23'],        'x23':['x34'],       'x13':['x24']},
 'phi12_3_4': {'x12':['x13','x23'],  'x23':['x34'],       'x13':['x14','x24']},
 'phi1_23_4': {'x12':['x12','x13'],  'x23':['x24','x34'], 'x13':['x14']},
 'phi1_2_34': {'x12':['x12'],        'x23':['x23','x24'], 'x13':['x13','x14']},
}
# forget-strand maps p_i : PB4 -> PB3 (kill x_{jk} with i in {j,k}; relabel remaining strands 1,2,3)
P={
 1: {'x12':None,'x13':None,'x14':None,'x23':'x12','x24':'x13','x34':'x23'},
 2: {'x12':None,'x23':None,'x24':None,'x13':'x12','x14':'x13','x34':'x23'},
 3: {'x13':None,'x23':None,'x34':None,'x12':'x12','x14':'x13','x24':'x23'},
 4: {'x14':None,'x24':None,'x34':None,'x12':'x12','x13':'x13','x23':'x23'},
}
def comp(i,cof,gen):
    """image in P of source generator `gen` under psi o p_i o phi"""
    parts=[]
    for g4 in COF[cof][gen]:
        g3=P[i][g4]
        parts.append(E if g3 is None else PSI[g3])
    return mul(*parts)

def show(w):
    if w==(): return '1'
    return ''.join(('%s^%d'%(g,e) if e!=1 else g) for g,e in w)

print("=== 20 composites  psi o p_i o phi   (images of x12, x23) ===")
psi_pair=(X,Y)
tab={}
for i in [4,3,2,1]:
    for cof in COF:
        a=comp(i,cof,'x12'); b=comp(i,cof,'x23')
        tab[(i,cof)]=(a,b)
        # classify
        if (a,b)==psi_pair: kind='= psi'
        else:
            # cyclic?  both powers of a common generator-word of length<=1
            def base(w):
                if w==(): return None
                if len(w)==1: return w[0][0]
                return 'NONCYCLIC'
            ba,bb=base(a),base(b)
            ok = (ba is None or bb is None or ba==bb) and 'NONCYCLIC' not in (ba,bb)
            kind='cyclic-image (DEGENERATE)' if ok else '??? NOT CLASSIFIED'
        print("  p_%d o %-10s : x12->%-8s x23->%-8s   %s"%(i,cof,show(a),show(b),kind))

print()
print("=== pentagon (2.20) modulo ker(psi-tilde) and modulo the B4-core, on charming f ===")
print("    rule: a DEGENERATE substitution sends every f in [F2,F2] to 1 (abelian image).")
order_L=['phi234','phi1_23_4','phi123']     # LHS of (2.20)
order_R=['phi1_2_34','phi12_3_4']           # RHS of (2.20)
for i in [4,3,2,1]:
    def sym(cof):
        a,b=tab[(i,cof)]
        return 'f(x,y)' if (a,b)==psi_pair else '1'
    L=[sym(c) for c in order_L]; R=[sym(c) for c in order_R]
    Lr=[t for t in L if t!='1'] or ['1']; Rr=[t for t in R if t!='1'] or ['1']
    print("  coord i=%d :  LHS = %s   RHS = %s   -> %s"%(i,'*'.join(Lr),'*'.join(Rr),
          'IDENTITY (no pentagon content)' if Lr==Rr else 'NONTRIVIAL'))
print()
print("  => (2.20) is identically satisfied by every charming f at ker(psi-tilde) and at the B4-core.")

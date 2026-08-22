import itertools, sys
# free assoc algebra on X=0,Y=1 ; words of length w indexed by tuples
def words(w): return list(itertools.product([0,1],repeat=w))

def dynkin_basis(w, p):
    # pi_w(a1...aw) = [...[[a1,a2],a3],...,aw]  as element of A_w
    W = words(w); idx = {u:i for i,u in enumerate(W)}
    rows=[]
    for u in W:
        # build iteratively as dict word->coeff
        cur = {(u[0],):1}
        for k in range(1,w):
            a=u[k]; new={}
            for v,c in cur.items():
                t=v+(a,)
                new[t]=(new.get(t,0)+c)%p
                t2=(a,)+v
                new[t2]=(new.get(t2,0)-c)%p
            cur={k2:v2 for k2,v2 in new.items() if v2%p}
        r=[0]*len(W)
        for v,c in cur.items(): r[idx[v]]=c%p
        rows.append(r)
    return rows, W, idx

def rref(M,p):
    M=[row[:] for row in M]; rows=len(M); cols=len(M[0]) if rows else 0
    piv=[]; r=0
    for c in range(cols):
        pr=None
        for i in range(r,rows):
            if M[i][c]%p: pr=i;break
        if pr is None: continue
        M[r],M[pr]=M[pr],M[r]
        inv=pow(M[r][c],p-2,p)
        M[r]=[(v*inv)%p for v in M[r]]
        for i in range(rows):
            if i!=r and M[i][c]%p:
                f=M[i][c]
                M[i]=[(M[i][j]-f*M[r][j])%p for j in range(cols)]
        piv.append(c); r+=1
        if r==rows: break
    return M[:r],piv

def subst(poly, images, p, w):
    # poly: dict word->coeff ; images: list of dicts letter->(dict of words of length1 -> coeff)
    out={}
    for u,c in poly.items():
        cur={():c}
        for a in u:
            new={}
            for v,cv in cur.items():
                for lw,cl in images[a].items():
                    t=v+lw
                    new[t]=(new.get(t,0)+cv*cl)%p
            cur=new
        for v,cv in cur.items():
            if cv%p: out[v]=(out.get(v,0)+cv)%p
    return {k:v for k,v in out.items() if v%p}

def run(w,p,verbose=False):
    rows,W,idx = dynkin_basis(w,p)
    B,piv = rref(rows,p)     # basis of L_w as vectors in A_w
    d=len(B)
    # substitutions
    X={(0,):1}; Y={(1,):1}; Z={(0,):p-1,(1,):p-1}
    S_swap=[Y,X]          # X->Y, Y->X
    S1=[Y,Z]              # X->Y, Y->Z
    S2=[Z,X]              # X->Z, Y->X
    eqs=[]
    for bvec in B:
        poly={W[i]:bvec[i] for i in range(len(W)) if bvec[i]%p}
        r1=subst(poly,S_swap,p,w)     # psi(Y,X)
        e1={}
        for k,v in poly.items(): e1[k]=(e1.get(k,0)+v)%p
        for k,v in r1.items(): e1[k]=(e1.get(k,0)+v)%p
        a=subst(poly,S1,p,w); b=subst(poly,S2,p,w)
        e2={}
        for src in (poly,a,b):
            for k,v in src.items(): e2[k]=(e2.get(k,0)+v)%p
        eqs.append(([e1.get(u,0)%p for u in W],[e2.get(u,0)%p for u in W]))
    # columns = coefficients c_i of psi = sum c_i B_i ; rows = equations
    M=[]
    for j in range(len(W)):
        M.append([eqs[i][0][j] for i in range(d)])
    for j in range(len(W)):
        M.append([eqs[i][1][j] for i in range(d)])
    R,pv=rref(M,p)
    return d, d-len(pv)

for w in range(1,13):
    r1=run(w,2147483647); r2=run(w,998244353)
    print("w=%2d  dim Lie_w=%4d   dim grt^hex_w = %d (p1) / %d (p2)"%(w,r1[0],r1[1],r2[1]))
    sys.stdout.flush()

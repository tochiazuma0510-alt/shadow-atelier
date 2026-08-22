#!/usr/bin/env python3
"""WO-155-1: independent full-48 A2 checker (pure Python, no producer import).

The only runtime judgment inputs are the two frozen witness exports named
below.  The registered DEEP15 source contributes an embedded extraction
payload and provenance SHA; the source file is never read at runtime.  All
group, Fox, and finite-field calculations in this file are local.
"""
import base64, hashlib, json, os, re, sys, zlib
from collections import deque, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P3 = "search/certs/koubou83_A2_48sweep_v2_witness_export_20260822.json"
P2 = "search/certs/koubou83_A2_48sweep_v3_p2_witness_export_20260822.json"
DEEP = "search/iso_census83_deep15_data.g"
PIN = {
    P3: "25f902e0e8bbbe7dd8c9c60113eb239cb3b0a8a6d9a9c37491e06f6bfa1f6511",
    P2: "2f665114d8ffcd35383d36a5a3d9a9c3d0dbb36e932cfd52d399913c34ced3e1",
    DEEP: "75905c604b83058ff6406f5c115bfa3325fd4424c98125750e49c2b76bbd35ec",
}
EXPORT_META={P3:{"cert_schema":"koubou83-A2-48sweep-v2-witness-export/1","witness_jsonl_source":"search/certs/koubou83_A2_48sweep_v2_20260822_witness.jsonl","witness_jsonl_sha256":"79f253c30f81a763fc81399a889f98db575cbc37b7c04cf04886380795e091ea","p":(2,3)},P2:{"cert_schema":"koubou83-A2-48sweep-v3-p2-witness-export/1","witness_jsonl_source":"search/certs/koubou83_A2_48sweep_v3_p2_20260822_witness.jsonl","witness_jsonl_sha256":"b588f84c3dc5ff2550a421a4c0029f9bddb26f9df71aaf41712f77c090d4dfc4","p":(2,)}}
WINDOWS = ((1152, 154161), (1152, 154163))
EMBEDDED_DEEP15 = {
154161: "eNqNVruO3DAM/BdXjrBXiPJucb8SnAEbm+KaBEiKBAjy77EkUhxSWu9WtkiJHD6G0t/p8/v925/pPcYrXabP+/T+tfzG6xJv8eMy/f7x8/7rkE7ztr6lsIfjE7+sNF2KhKqEVBKrJLGkLBZZrAue3/PubV3MMuxwODsoElJJqhIwchitiy2ov+KIZerWSNGdVYBXqwDnTbG+XQ/ZDdZJ1knWEmtOWHecZPtS17EHhwoDDhUG3KHY16u6zIkusuLpVn7ziWO9C1AaZYVA5fKCKpeZWg7jQiLmTuJ9XLkSQ22fbGFfE9cSDXLHVUFqJ0ewjcrCbv4cutausSIoZ0kFuENQEqKUHQVL1SsAXseWBYUczd443luQO3IkkbUsplGZpLhdNWpOGUKqLgdwyRPmFDAhixRyxyNFbqjATbCSTTBBtXNzZLZgwyjZjhBaTVJTRh1PRdzVFtqCKyyeA+xsVkwfqLLX9T2CnjS4wKxQ9puZyiRgmwGAutGAGXfDATOe+W+iuwWtL+hjeAxgsKcqHY0Ms7h0iKgamucuoS1QqOGgtmTkpCaChOjgDkvrPaj5WgiHJQwR10geGAccuSmgHfvT4xkkVsRE3z1CfbhfmaqFpBtUuQIpq1nnhetAPgu7Z5gYjfg1b3wowUVARgO3X0B0kUNq0MIQPNhCF5w5bN/goJLQCUkSJW4zwJqts/yJJZ8Md3Z0CWxmtEvuTwcwDHCAVaNPlm9tItB4BLsr2w5hvrSf8F52PScsXwUDyib09JAx+KZjRyOnLZXPqAf3nQ09zP2zLrzODdL9LxWe9BXka4fXXOO+H6vJXyDn0wJfPP3QUITu9Wkaf7ZPy60CetoBo849z017MrvYrsG/EVs39+KQn/z+FsIXghvl3YWxJjBPL2FJ7jH6MH1Hoj/+/Qeg8FRq",
154163: "eNqNVU1vwyAM/S+cKGoPmLSH/pWpkYi6Qy+btB02adp/X7CxjQnLdkmIPx7w/Ox8ucfL/fnTXWM8w9E97u76hMt4nuIl3Y7u4/Xt/r5aXZ5PMfgl5BnCclgfxeCOZF/KAz20OOFKYpZqqiHFDsX8e1Zx5z3YVLcGeqfVcWnswN8T7kMpcoAU8mr2uFgxDnOiz7IJ7kCWHNoQuXDoItnhcV9PhDBDhxn4RI2nwCKXGNACxA4ABCDuA5Qob3MT5e6mJQHvL4V4ZKRUwdPIyB6ukhJpU0FTQYwTZ6nLZjF7YXCQYTm25+nDtscyQvbCThqoPNSXZ0GbInttkaECosQrAAeJy5ZjdNqm5wxfudTWsBA1+Dd2ayO0Gp+CVgl7128lLVQ04h0wB8ZurqsTwWT3uu/2CcPTkHqkwdhcEf7knKMUOTXIVAchNil9pkGSMjrDtnXI0w80mYGhrfbMU07q0ys86+WkZwWk0UCWKNBdfQ6mC6NOY9hc1PZsJpKhFZmmMpZGNp2PhnEXi3unQev/4B9alIGxUSOP9EZoIzhU5O37ByhYvvU="
}

def sha(path):
    h = hashlib.sha256()
    with open(os.path.join(ROOT, path), "rb") as f:
        for b in iter(lambda: f.read(1 << 16), b""): h.update(b)
    return h.hexdigest()

def inv(w): return [-x for x in w[::-1]]
def power(w, n): return [] if n == 0 else (inv(w) * (-n) if n < 0 else list(w) * n)
def red(a, b):
    z = list(a)
    for t in b:
        if z and z[-1] == -t: z.pop()
        else: z.append(t)
    return z

def tokenize(s):
    out=[]; i=0
    while i<len(s):
        c=s[i]
        if c in "()*": out.append(c); i+=1
        elif c in "ab": out.append(c); i+=1
        elif c=="^":
            j=i+1; k=j
            if s[j]=="-": j+=1
            while j<len(s) and s[j].isdigit(): j+=1
            out.append(("e",int(s[k:j]))); i=j
        else: raise ValueError("bad word token")
    return out
def parse(s):
    t=tokenize(s); p=[0]
    def expr():
        z=term()
        while p[0]<len(t) and t[p[0]]=="*": p[0]+=1; z+=term()
        return z
    def term():
        q=t[p[0]]
        if q=="(": p[0]+=1; z=expr(); assert t[p[0]]==")"; p[0]+=1
        elif q in ("a","b"): p[0]+=1; z=[1 if q=="a" else 2]
        else: raise ValueError("bad term")
        e=1
        if p[0]<len(t) and isinstance(t[p[0]],tuple): e=t[p[0]][1]; p[0]+=1
        return power(z,e)
    z=expr(); assert p[0]==len(t); return z

FORWARD={(1,1):(2,[],0),(1,2):(3,[],0),(2,1):(1,[1],0),(2,2):(4,[],0),
 (3,1):(5,[],0),(3,2):(1,[2],0),(4,1):(6,[],0),(4,2):(2,[-2,-1],1),
 (5,1):(3,[-1,-2],1),(5,2):(6,[],0),(6,1):(4,[2],0),(6,2):(5,[1],0)}
REVERSE={(b,g):(a,w,k) for (a,g),(b,w,k) in FORWARD.items()}
def pb(w):
    s=1; z=[]; k=0
    for t in w:
        if t>0: s2,q,d=FORWARD[(s,t)]; z=red(z,q); k+=d; s=s2
        else: s2,q,d=REVERSE[(s,-t)]; z=red(z,inv(q)); k-=d; s=s2
    if s!=1: raise ValueError("word is not PB3")
    return z,k

GI={1:0,-1:1,2:2,-2:3}; IV=(1,0,3,2)
class TC:
    def __init__(self, rs): self.rs=rs; self.tab=[[None]*4]; self.par=[0]
    def find(self,x):
        while self.par[x]!=x: self.par[x]=self.par[self.par[x]]; x=self.par[x]
        return x
    def new(self): self.tab.append([None]*4); self.par.append(len(self.par)); return len(self.par)-1
    def merge(self,a,b):
        q=[(a,b)]
        while q:
            a,b=q.pop(); a=self.find(a); b=self.find(b)
            if a==b: continue
            if a>b: a,b=b,a
            self.par[b]=a
            for g in range(4):
                u,v=self.tab[a][g],self.tab[b][g]
                if u is None and v is not None:
                    self.tab[a][g]=v; ii=IV[g]
                    if self.tab[v][ii] is None:self.tab[v][ii]=a
                    elif self.find(self.tab[v][ii])!=a:q.append((self.tab[v][ii],a))
                elif u is not None and v is not None and self.find(u)!=self.find(v):q.append((u,v))
    def link(self,a,g,b):
        a=self.find(a);b=self.find(b); u=self.tab[a][g]
        if u is None:
            self.tab[a][g]=b; ii=IV[g]
            if self.tab[b][ii] is None:self.tab[b][ii]=a
            elif self.find(self.tab[b][ii])!=a:self.merge(self.tab[b][ii],a)
        elif self.find(u)!=b:self.merge(u,b)
    def scan(self,c,r):
        a=b=self.find(c); i=0;j=len(r)
        while i<j and self.tab[self.find(a)][GI[r[i]]] is not None:a=self.tab[self.find(a)][GI[r[i]]];i+=1
        while j>i and self.tab[self.find(b)][GI[-r[j-1]]] is not None:b=self.tab[self.find(b)][GI[-r[j-1]]];j-=1
        if i==j:
            if self.find(a)!=self.find(b):self.merge(a,b)
        elif i==j-1:self.link(a,GI[r[i]],b)
        else:
            a=self.find(a); g=GI[r[i]]
            if self.tab[a][g] is None:
                u=self.new(); self.tab[a][g]=u; self.tab[u][IV[g]]=a
            return False
        return True
    def run(self):
        c=0
        while c<len(self.tab):
            if self.find(c)==c:
                for r in self.rs:
                    tries=0
                    while not self.scan(c,r):
                        tries+=1
                        if tries>4*(len(r)+2): raise RuntimeError("coset enumeration did not close")
            c+=1
        live=[i for i in range(len(self.tab)) if self.find(i)==i]; mp={x:i for i,x in enumerate(live)}
        self.tab=[[mp[self.find(v)] if v is not None else None for v in self.tab[x]] for x in live]
        if any(v is None for r in self.tab for v in r): raise RuntimeError("incomplete coset table")
        return self.tab

def ev(w,tab,start=0):
    c=start
    for t in w:c=tab[c][GI[t]]
    return c
def source_records():
    got={}
    for key,blob in EMBEDDED_DEEP15.items():
        q=json.loads(zlib.decompress(base64.b64decode(blob)))
        assert q["id"]==[1152,key] and len(q["words"])==(109 if key==154161 else 59)
        assert key!=154163 or not q["words"][0].startswith("a^-6")
        got[key]=(q["index"],q["words"])
    return got
def load_export(path):
    d=json.load(open(os.path.join(ROOT,path),encoding="utf-8")); m=EXPORT_META[path]
    assert isinstance(d,dict) and d.get("cert_schema")==m["cert_schema"] and isinstance(d.get("generated"),str) and isinstance(d.get("purpose"),str)
    assert d.get("provenance")=={"witness_jsonl_source":m["witness_jsonl_source"],"witness_jsonl_sha256":m["witness_jsonl_sha256"]}
    ws=d.get("witnesses"); assert isinstance(ws,list)
    for r in ws:
        assert isinstance(r,dict) and set(r)=={"window","shadow_idx","m","f_xyword","p","witness_sigma_word"}
        assert isinstance(r["window"],list) and len(r["window"])==2 and all(isinstance(x,int) for x in r["window"])
        assert isinstance(r["shadow_idx"],int) and isinstance(r["m"],int) and r["p"] in m["p"]
        assert isinstance(r["f_xyword"],list) and isinstance(r["witness_sigma_word"],list)
        assert all(isinstance(x,int) and abs(x) in (1,2) for x in r["f_xyword"]+r["witness_sigma_word"])
    return d,m

def build(id2,p):
    rec=source_records()[id2][1]; m0=power([1],-6) if id2==154161 else power([-1,-2],3)
    rs=[]; defining_mwords=[]
    for s in rec:
        w,k=pb(parse(s)); q=w+power(m0,-k); rs.append(q); defining_mwords.append(q)
    tab=TC(rs).run(); n=len(tab); assert n==192
    X=[r[0] for r in tab]; Xi=[r[1] for r in tab]; Y=[r[2] for r in tab]; Yi=[r[3] for r in tab]
    def fox(w):
        v=[0]*(2*n); c=0
        for t in w:
            if t==1:v[c]=(v[c]+1)%p;c=X[c]
            elif t==-1:c=Xi[c];v[c]=(v[c]-1)%p
            elif t==2:v[n+c]=(v[n+c]+1)%p;c=Y[c]
            else:c=Yi[c];v[n+c]=(v[n+c]-1)%p
        return v,c
    cols=[]
    for arr,off in ((X,0),(Y,n)):
        for i in range(n):
            z=[0]*n; z[i]=(z[i]-1)%p; z[arr[i]]=(z[arr[i]]+1)%p; cols.append(z)
    def apply_D(v):
        return [sum(cols[j][i]*v[j] for j in range(2*n))%p for i in range(n)]
    def fox_identity_ok(w):
        v,e=fox(w); want=[0]*n; want[e]=(want[e]+1)%p; want[0]=(want[0]-1)%p
        return apply_D(v)==want
    fox_fixtures=([1,2,-1,2,1,-2],[1,1,2,-1],[2,-1,2,-1],[1,2,1,2])
    defining_eval=all(ev(q,tab)==0 for q in defining_mwords)
    fox_checks=all(fox_identity_ok(q) for q in defining_mwords+list(fox_fixtures))
    assert defining_eval and fox_checks
    M=[[cols[j][i] for j in range(2*n)] for i in range(n)]; piv=[]; rr=0
    for c in range(2*n):
        q=next((i for i in range(rr,n) if M[i][c]),None)
        if q is None:continue
        M[rr],M[q]=M[q],M[rr]; iv=pow(M[rr][c],-1,p); M[rr]=[(x*iv)%p for x in M[rr]]
        for i in range(n):
            if i!=rr and M[i][c]:
                z=M[i][c];M[i]=[(a-z*b)%p for a,b in zip(M[i],M[rr])]
        piv.append(c);rr+=1
    ker=[]
    for f in [i for i in range(2*n) if i not in piv]:
        v=[0]*(2*n);v[f]=1
        for i,c in enumerate(piv):v[c]=(-M[i][f])%p
        ker.append(v)
    wo=[None]*n;wo[0]=[]; dq=deque([0])
    while dq:
        c=dq.popleft()
        for arr,t in ((X,1),(Xi,-1),(Y,2),(Yi,-2)):
            q=arr[c]
            if wo[q] is None:wo[q]=wo[c]+[t];dq.append(q)
    cb=ev(m0,tab); perm=[ev(wo[g],tab,cb) for g in range(n)]
    def phi(v):return [v[perm[i]] for i in range(n)]+[v[n+perm[i]] for i in range(n)]
    def add(v,P):
        v=v[:]
        for j in sorted(P):
            if v[j]:
                z=v[j]*pow(P[j][j],-1,p)%p; b=P[j];v=[(a-z*x)%p for a,x in zip(v,b)]
        j=next((i for i,x in enumerate(v) if x),None)
        if j is None:return False
        iv=pow(v[j],-1,p);P[j]=[(x*iv)%p for x in v];return True
    U={}
    for v in ker:add([(a-b)%p for a,b in zip(phi(v),v)],U)
    T={}
    for v in U.values():add(v+[0],T)
    def Phi_parts(sw):
        w,k=pb(sw);v,e=fox(w+power(m0,-k));return v+[k%p],e
    basis_vectors=[]
    for s in rec:
        q=Phi_parts(parse(s))[0]
        if add(q,T):basis_vectors.append(q)
    # A second tracker carries the actual V-basis coefficients.  Its U seeds
    # have zero coefficient; each accepted defining word gets one unit slot.
    C={}; zc=[0]*len(basis_vectors)
    def add_coeff(v,co):
        v=v[:];co=co[:]
        for j in sorted(C):
            if v[j]:
                b,bc=C[j];q=v[j]*pow(b[j],-1,p)%p
                v=[(a-q*x)%p for a,x in zip(v,b)]
                co=[(a-q*x)%p for a,x in zip(co,bc)]
        j=next((i for i,x in enumerate(v) if x),None)
        if j is None:return False
        q=pow(v[j],-1,p);C[j]=([(x*q)%p for x in v],[(x*q)%p for x in co]);return True
    for v in U.values():add_coeff(v+[0],zc)
    for i,v in enumerate(basis_vectors):
        co=[0]*len(basis_vectors);co[i]=1;assert add_coeff(v,co)
    def detail(sw):
        try:v,e=Phi_parts(sw)
        except Exception:return {"evaluation_identity":False,"tracker_remainder_zero":False,"v_coefficient_zero":False,"v_coefficients":[]}
        co=[0]*len(basis_vectors)
        for j in sorted(C):
            if v[j]:
                b,bc=C[j];q=v[j]*pow(b[j],-1,p)%p
                v=[(a-q*x)%p for a,x in zip(v,b)]
                co=[(a-q*x)%p for a,x in zip(co,bc)]
        return {"evaluation_identity":e==0,"tracker_remainder_zero":not any(v),"v_coefficient_zero":not any(co),"v_coefficients":co}
    def member(sw):
        d=detail(sw);return d["evaluation_identity"] and d["tracker_remainder_zero"] and d["v_coefficient_zero"]
    def n_member(sw):
        try:return Phi_parts(sw)[1]==0
        except Exception:return False
    return {"member":member,"n_member":n_member,"detail":detail,"fox":fox,"tab":tab,"rankD":len(piv),"dimKer":len(ker),"rankU":len(U),"dimV":len(T)-len(U),"rankFull":len(T),"kappa":next(k for k in range(1,5001) if ev(power(m0,k),tab)==0),"record_count":len(rec),"basis_count":len(basis_vectors),"defining_evaluation_identity":defining_eval,"fox_identity_self_check":fox_checks,"fox_identity_checked_words":len(defining_mwords)+len(fox_fixtures)}

def expand_xy(w):
    z=[]
    for t in w:
        q=[1,1] if abs(t)==1 else [2,2]; z+=q if t>0 else inv(q)
    return z
def strand_abgamma(w):
    labels=[1,2,3]; c={(1,2):0,(1,3):0,(2,3):0}
    for t in w:
        i=abs(t)-1; pair=tuple(sorted((labels[i],labels[i+1]))); c[pair]+=1 if t>0 else -1
        labels[i],labels[i+1]=labels[i+1],labels[i]
    raw=(c[(1,2)],c[(1,3)],c[(2,3)])
    assert labels==[1,2,3] and all(v%2==0 for v in raw)
    return {"raw":raw,"coords":((raw[0]-raw[1])//2,(raw[2]-raw[1])//2,raw[1]//2)}
def raw_crossings(w): return strand_abgamma(w)["raw"]
def strand_coords(w): return tuple(strand_abgamma(w)["coords"])
def coords(w):
    z,k=pb(w); return (sum(t==1 for t in z)-sum(t==-1 for t in z),sum(t==2 for t in z)-sum(t==-2 for t in z),k)
def Rwords(F,m):
    u=2*m+1;c=[1,2,1,1,2,1];x=[1,1];y=[2,2]
    return (power([1],u)+inv(F)+power([2],u)+F+power(c,-m)+power(x,m)+[-2,-1]+F,
            inv(F)+power([2],u)+F+power([1],u)+inv(F)+power(c,-m)+power(y,m)+[-1,-2])
def row_manifest(r):
    q={"window":r["window"],"shadow_idx":r["shadow_idx"],"p":r["p"],"m":r["m"],"f_xyword":r["f_xyword"],"witness_sigma_word":r["witness_sigma_word"]}
    b=json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode();
    return {"key":[*r["window"],r["shadow_idx"],r["p"]],"row_sha256":hashlib.sha256(b).hexdigest(),"f_xyword_sha256":hashlib.sha256(json.dumps(r["f_xyword"],separators=(",",":")).encode()).hexdigest(),"witness_sigma_word_sha256":hashlib.sha256(json.dumps(r["witness_sigma_word"],separators=(",",":")).encode()).hexdigest(),"m":r["m"]}

def main():
    assert sha(P2)==PIN[P2] and sha(P3)==PIN[P3]
    e2,m2=load_export(P2); e3,m3=load_export(P3); d2=e2["witnesses"]; d3=e3["witnesses"]
    rows=[r for r in d2 if r["p"]==2]+[r for r in d3 if r["p"]==3]
    assert len(rows)==192
    keys=[(r["window"][0],r["window"][1],r["shadow_idx"],r["p"]) for r in rows]
    assert len(set(keys))==192 and set(keys)==set((1152,w,i,p) for w in (154161,154163) for i in range(1,49) for p in (2,3))
    by={(r["window"][0],r["window"][1],r["shadow_idx"],r["p"]):r for r in rows}
    for w in (154161,154163):
        for i in range(1,49):
            a,b=by[(1152,w,i,2)],by[(1152,w,i,3)]
            assert a["m"]==b["m"] and a["f_xyword"]==b["f_xyword"]
    env={}; engines={}
    pin_ab={"sigma1_squared":list(strand_coords([1,1])),"sigma2_squared":list(strand_coords([2,2])),"delta_squared":list(strand_coords([1,2,1,1,2,1])),"delta_squared_raw_crossings":list(raw_crossings([1,2,1,1,2,1]))}
    assert pin_ab=={"sigma1_squared":[1,0,0],"sigma2_squared":[0,1,0],"delta_squared":[0,0,1],"delta_squared_raw_crossings":[2,2,2]}
    for w in (154161,154163):
        env[str(w)]={}
        for p in (2,3):
            engines[(w,p)]=build(w,p); e=engines[(w,p)]
            expected={"record_count":109,"kappa":2,"rankD":191,"dimKer":193,"rankU":96,"dimV":98} if w==154161 else {"record_count":59,"kappa":4,"rankD":191,"dimKer":193,"rankU":144,"dimV":50}
            assert {k:e[k] for k in expected}==expected and e["rankFull"]==e["rankU"]+e["dimV"]==e["dimKer"]+1 and e["defining_evaluation_identity"] and e["fox_identity_self_check"]
            env[str(w)][str(p)]={k:e[k] for k in ("record_count","kappa","rankD","dimKer","rankU","dimV","rankFull","defining_evaluation_identity","fox_identity_self_check","fox_identity_checked_words")}
    outcomes=[]; direct=0; legal=0; n_membership=0; charming=0; v_coeff=0
    for r in sorted(rows,key=lambda q:(q["window"][1],q["shadow_idx"],q["p"])):
        w,p=r["window"][1],r["p"]; F=expand_xy(r["f_xyword"])+r["witness_sigma_word"]; z,g=pb(r["witness_sigma_word"]); zF,gF=pb(F)
        sg=strand_abgamma(r["witness_sigma_word"])["coords"][2]; sF=strand_abgamma(F)["coords"][2]; assert sg==g and sF==gF
        a,b,gg=strand_coords(F); strand_match=(coords(F)==(a,b,gg)); correction_N=engines[(w,p)]["n_member"](r["witness_sigma_word"]); legal_ok=(p and sg%p==0 and sF%p==0 and correction_N); charm_ok=(a%p==0 and b%p==0 and ((a+b)//p)%3==0)
        rr=Rwords(F,r["m"]); d1=engines[(w,p)]["detail"](rr[0]);d2=engines[(w,p)]["detail"](rr[1]); direct_ok=all(d1[k] and d2[k] for k in ("evaluation_identity","tracker_remainder_zero","v_coefficient_zero"))
        legal+=legal_ok; n_membership+=correction_N; charming+=charm_ok; direct+=direct_ok; v_coeff+=d1["v_coefficient_zero"] and d2["v_coefficient_zero"]
        outcomes.append({"key":[1152,w,r["shadow_idx"],p],"legal":legal_ok,"correction_N_membership":correction_N,"charming":charm_ok,"direct_R_membership":direct_ok,"R1_evaluation_identity":d1["evaluation_identity"],"R2_evaluation_identity":d2["evaluation_identity"],"R1_tracker_remainder_zero":d1["tracker_remainder_zero"],"R2_tracker_remainder_zero":d2["tracker_remainder_zero"],"R1_v_coefficient_zero":d1["v_coefficient_zero"],"R2_v_coefficient_zero":d2["v_coefficient_zero"],"coords":[a,b,gg],"pb_coords_match_strand_tracker":strand_match,"pb_strand_gamma_match":sg==g and sF==gF,"witness_gamma":sg,"R_lengths":[len(rr[0]),len(rr[1])]})
    assert legal==192 and charming==192 and direct==192
    positives=[]
    for w in (154161,154163):
        for m in (0,11):
            cands=[r for r in rows if r["window"]==[1152,w] and r["p"] in (2,3) and r["m"]==m and r["f_xyword"]==[]]
            assert len(cands)==2 and {r["p"] for r in cands}=={2,3}
            checks=[]
            for r0 in cands:
                F0=expand_xy(r0["f_xyword"])+r0["witness_sigma_word"]; z,g=pb(r0["witness_sigma_word"]); _,gF=pb(F0); sg=strand_abgamma(r0["witness_sigma_word"])["coords"][2];sF=strand_abgamma(F0)["coords"][2];assert sg==g and sF==gF; a,b,_=strand_coords(F0); eng=engines[(w,r0["p"])]
                rr=Rwords(F0,m);d1=eng["detail"](rr[0]);d2=eng["detail"](rr[1]); legal0=(sg%r0["p"]==0 and sF%r0["p"]==0 and eng["n_member"](r0["witness_sigma_word"])); charming0=(a%r0["p"]==0 and b%r0["p"]==0 and ((a+b)//r0["p"])%3==0); direct0=all(d1[k] and d2[k] for k in ("evaluation_identity","tracker_remainder_zero","v_coefficient_zero")); checks.append({"p":r0["p"],"key":[1152,w,r0["shadow_idx"],r0["p"]],"legal":legal0,"charming":charming0,"direct":direct0,"pb_strand_gamma_match":sg==g and sF==gF,"R_lengths":[len(rr[0]),len(rr[1])]})
            positives.append({"window":w,"m":m,"semantic_rows":checks,"control_pass":all(x["legal"] and x["charming"] and x["direct"] for x in checks)})
    def variant(r, suffix, full=False):
        w,p=r["window"][1],r["p"]; eng=engines[(w,p)]; ww=suffix if full else r["witness_sigma_word"]+suffix; Fv=expand_xy(r["f_xyword"])+ww; z,g=pb(ww); _,gF=pb(Fv); sg=strand_abgamma(ww)["coords"][2];sF=strand_abgamma(Fv)["coords"][2];assert sg==g and sF==gF;a,b,_=strand_coords(Fv)
        rr=Rwords(Fv,r["m"]); d1=eng["detail"](rr[0]);d2=eng["detail"](rr[1]); direct_v=all(d1[k] and d2[k] for k in ("evaluation_identity","tracker_remainder_zero","v_coefficient_zero"))
        legal_v=(p and sg%p==0 and sF%p==0 and eng["n_member"](ww)); charming_v=(a%p==0 and b%p==0 and ((a+b)//p)%3==0)
        return {"legal":legal_v,"charming":charming_v,"direct":direct_v,"N_membership":eng["n_member"](ww),"pb_strand_gamma_match":sg==g and sF==gF,"witness_nonempty":bool(r["witness_sigma_word"]),"R_details":[d1,d2]}
    x2=[variant(r,[1,1]) for r in rows]; destructive_x=sum(not (q["legal"] and q["charming"] and q["direct"]) for q in x2); destructive_x_direct=sum(not q["direct"] for q in x2)
    conj_suffix=[1,1]; conjugations=[]
    for r in rows:
        x=conj_suffix; w0=r["witness_sigma_word"]; conjugations.append(variant(r,x+w0+inv(x),True))
    destructive_conj_nonempty=sum(not q["direct"] for q in conjugations if q["witness_nonempty"]); destructive_conj_empty=sum(not q["direct"] for q in conjugations if not q["witness_nonempty"])
    conj_cells={}
    for w in (154161,154163):
        z=[q for r,q in zip(rows,conjugations) if r["window"][1]==w and r["witness_sigma_word"]]
        e=[q for r,q in zip(rows,conjugations) if r["window"][1]==w and not r["witness_sigma_word"]]
        conj_cells[str(w)]={"nonempty_rows":len(z),"nonempty_direct_failures":sum(not q["direct"] for q in z),"empty_rows":len(e),"empty_direct_failures":sum(not q["direct"] for q in e),"legal_preserved":all(q["legal"] for q in z+e),"charming_preserved":all(q["charming"] for q in z+e),"N_membership_maintained":all(q["N_membership"] for q in z+e)}
    claim_digest=hashlib.sha256(json.dumps(sorted(keys),separators=(",",":")).encode()).hexdigest()
    coverage_exact=len(rows)==192 and set(keys)==set((1152,w,i,p) for w in (154161,154163) for i in range(1,49) for p in (2,3))
    contract_exact=coverage_exact and all(by[(1152,w,i,2)]["m"]==by[(1152,w,i,3)]["m"] and by[(1152,w,i,2)]["f_xyword"]==by[(1152,w,i,3)]["f_xyword"] for w in (154161,154163) for i in range(1,49))
    strand_match=sum(o["pb_coords_match_strand_tracker"] for o in outcomes)
    env_ok=all(e["defining_evaluation_identity"] and e["fox_identity_self_check"] and e["rankFull"]==e["rankU"]+e["dimV"]==e["dimKer"]+1 for c in env.values() for e in c.values())
    pin_ok=sha(P2)==PIN[P2] and sha(P3)==PIN[P3] and pin_ab=={"sigma1_squared":[1,0,0],"sigma2_squared":[0,1,0],"delta_squared":[0,0,1],"delta_squared_raw_crossings":[2,2,2]}
    positive_ok=all(x["control_pass"] for x in positives)
    gamma_variant_ok=all(q["pb_strand_gamma_match"] for q in x2+conjugations)
    out={"schema":"shadow-atelier/koubou83-A2-full48-crosscheck/v1","predicate_version":"WO-155-1/CLAIM-COVER-1/PIN-AB-1/Kp-direct-v1","claim_universe_digest_sha256":claim_digest,"generated_by":"crosscheck/check_koubou83_A2_full48_v1.py (pure Python, independent)","contract":"cross-checked candidate","input_sha256":{P2:sha(P2),P3:sha(P3)},"export_pins":{P2:{"cert_schema":e2["cert_schema"],"generated":e2["generated"],"purpose":e2["purpose"],"provenance":e2["provenance"]},P3:{"cert_schema":e3["cert_schema"],"generated":e3["generated"],"purpose":e3["purpose"],"provenance":e3["provenance"]}},"source_extraction_provenance":{"path":DEEP,"source_extraction_sha256":PIN[DEEP],"embedded_records":{"154161":{"index":source_records()[154161][0],"word_count":109},"154163":{"index":source_records()[154163][0],"word_count":59}},"selection_rule":"id [1152,154161] and id [1152,154163] record whose first word is not a^-6","runtime_source_read":False},"pin_ab":pin_ab,"environment_canaries":env,"coverage":{"selected":len(rows),"expected":192,"exact":coverage_exact,"cells":{"154161_p2":48,"154161_p3":48,"154163_p2":48,"154163_p3":48},"p_counts":{"2":96,"3":96}},"producer_contract":{"semantic_key_exact":contract_exact,"paired_m_f_exact":contract_exact,"row_manifest":sorted([row_manifest(r) for r in rows],key=lambda x:x["key"])},"outcomes":outcomes,"controls":{"positive":positives,"destructive_append_x2_suffix":[1,1],"destructive_append_x2_direct_failures":destructive_x_direct,"destructive_append_x2_overall_failures":destructive_x,"structure_sensitive":"w -> x*w*x^-1","structure_sensitive_x":[1,1],"structure_sensitive_nonempty_failures":destructive_conj_nonempty,"structure_sensitive_empty_failures":destructive_conj_empty,"structure_sensitive_cells":conj_cells},"summary":{"selected_192_192":len(rows)==192,"cell_48_48":coverage_exact,"coverage_exact":coverage_exact,"producer_contract_exact":contract_exact,"legal_192_192":legal==192,"correction_N_membership_192_192":n_membership==192,"charming_192_192":charming==192,"direct_R_192_192":direct==192,"R_tracker_v_coefficient_zero_192_192":v_coeff==192,"strand_tracker_pb_coords_match_192_192":strand_match==192,"variant_pb_strand_gamma_match":gamma_variant_ok,"pin_ab_pass":pin_ok,"environment_fox_tracker_pass":env_ok,"positive_controls_pass":positive_ok,"destructive_x2_overall_gate_fail_192_192":destructive_x==192,"structure_sensitive_nonempty_direct_failure":destructive_conj_nonempty>0,"structure_sensitive_legal_preserved":all(q["legal_preserved"] for q in conj_cells.values()),"structure_sensitive_charming_preserved":all(q["charming_preserved"] for q in conj_cells.values()),"structure_sensitive_N_preserved":all(q["N_membership_maintained"] for q in conj_cells.values()),"destructive_controls_pass":destructive_x==192 and destructive_conj_nonempty>0,"overall":"PASS" if coverage_exact and contract_exact and legal==charming==n_membership==direct==v_coeff==strand_match==192 and gamma_variant_ok and pin_ok and env_ok and positive_ok and destructive_x==192 and destructive_conj_nonempty>0 and all(q["legal_preserved"] and q["charming_preserved"] and q["N_membership_maintained"] for q in conj_cells.values()) else "FAIL"}}
    out["checker_source_sha256"]=sha("crosscheck/check_koubou83_A2_full48_v1.py")
    path=os.path.join(ROOT,"crosscheck/verdicts/koubou83_A2_full48_crosscheck_v1_20260822.json")
    with open(path,"w",encoding="utf-8",newline="\n") as f:json.dump(out,f,ensure_ascii=False,sort_keys=True,indent=2);f.write("\n")
    print(json.dumps(out["summary"],sort_keys=True)); return 0 if out["summary"]["overall"]=="PASS" else 1
if __name__=="__main__":sys.exit(main())

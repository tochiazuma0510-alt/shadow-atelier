#!/usr/bin/env python3
"""Independent checker for explicit-block direct-v4; no GAP helper import."""
from __future__ import annotations
import argparse,json,math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DEFAULT=ROOT/"ci"/"out"/"d972_b4_marity_phaseb1_direct_v4.json"
MOD=0b1011
LINES=tuple([(1,i) for i in range(8)]+[(0,1)])
P=tuple[int,...]
def comp(a:P,b:P)->P:return tuple(b[a[i]] for i in range(len(a)))
def inv(a:P)->P:
 r=[0]*len(a)
 for i,j in enumerate(a):r[j]=i
 return tuple(r)
def pw(a:P,n:int)->P:
 if n<0:return pw(inv(a),-n)
 r=tuple(range(len(a)))
 while n:
  if n&1:r=comp(r,a)
  a=comp(a,a);n//=2
 return r
def order(a:P)->int:
 seen=set();z=1
 for i in range(len(a)):
  if i not in seen:
   j=i;n=0
   while j not in seen:seen.add(j);j=a[j];n+=1
   z=math.lcm(z,n)
 return z
def gf(a:int,b:int)->int:
 r=0
 while b:
  if b&1:r^=a
  b>>=1;a<<=1
  if a&8:a^=MOD
 return r&7
def mat(m):
 out=[]
 for a,b in LINES:
  x=gf(a,m[0][0])^gf(b,m[1][0]);y=gf(a,m[0][1])^gf(b,m[1][1])
  out.append(LINES.index((1,gf(y,next(i for i in range(1,8) if gf(x,i)==1))) if x else (0,1)))
 return tuple(out)
def shift(p:P,off:int,total:int)->P:return tuple((off+p[i-off]) if off<=i<off+len(p) else i for i in range(total))
def block(ps):
 out=[];off=0
 for p in ps:out.extend(off+x for x in p);off+=len(p)
 return tuple(out)
def gn(n:int):
 r=tuple((i+1)%n for i in range(n));s=tuple((-i)%n for i in range(n))
 tr=lambda p,k:shift(p,k*n,3*n)
 x=comp(comp(tr(r,0),tr(s,1)),tr(s,2));sr=comp(s,r);y=comp(comp(tr(sr,0),tr(r,1)),tr(sr,2))
 return x,y
def evalw(w,imgs):
 z=tuple(range(len(imgs[0])))
 for k in w:z=comp(z,imgs[abs(k)-1] if k>0 else inv(imgs[-k-1]))
 return z
def expected():
 gx,gy=gn(9);s=mat(((1,0),(1,1)));t=mat(((4,3),(1,5)));x=pw(comp(s,inv(t)),2);y=comp(comp(inv(s),x),s)
 xm=block((gx,x));ym=block((gy,y));m=(xm,comp(inv(xm),inv(ym)),ym)
 rows=(((),(),(),(1,),(2,),(3,)),((),(1,),(2,),(),(),(3,)),((1,),(),(2,),(),(3,),()),((1,),(2,),(),(3,),(),()))
 dels=[tuple(evalw(w,m) for w in row) for row in rows]
 cfs=(((1,),(2,),(4,)),((4,),(5,),(6,)),((2,4),(3,5),(6,)),((1,2),(3,),(5,6)),((1,),(2,3),(4,5)))
 blocks=[];ids=[]
 for k,cf in enumerate(cfs,1):
  for i,row in enumerate(dels,1):
   b=tuple(evalw(w,row) for w in cf);blocks.append(b)
   if b==m:ids.append([k,i])
 gens=[block(tuple(b[j] for b in blocks)) for j in range(3)]
 center=evalw((1,2,3),gens)
 from sympy.combinatorics import Permutation,PermutationGroup
 go=lambda xs:int(PermutationGroup(*[Permutation(list(x),size=720) for x in xs]).order())
 full=go(gens);f2=go((gens[0],gens[2]));co=order(center)
 return {"generator_arrays":[[x+1 for x in g] for g in gens],"center_image":[x+1 for x in center],"center_order":co,"N_ord":math.lcm(order(gens[0]),order(gens[2]),co),"identity_coordinates":ids,"full":full,"f2":f2,"split":{"status":"CONDITIONAL_SPLIT_NUMERIC_GATE" if full==1469664*18 and f2==1469664 and co==18 else "NOT_ESTABLISHED","required_quotient_order":26453952,"required_F2_order":1469664,"required_center_order":18}}
def check(path:Path):
 o=json.loads(path.read_text(encoding="utf-8"));e=expected()
 if o.get("schema")!="d972-b4-marity-phaseb1-direct/v4" or o.get("status")!="DIRECT_20_BLOCK_TYPED":raise ValueError("schema/status")
 if o.get("explicit_blocks") is not True or o.get("degree")!=720 or o.get("block_count")!=20 or o.get("block_degree")!=36:raise ValueError("explicit block shape")
 if o.get("source_marking")!=["x12","x13","x23"] or o.get("target_marking")!=["X","X^-1Y^-1","Y"]:raise ValueError("marking")
 if o.get("generator_arrays")!=e["generator_arrays"]:raise ValueError("independent generator replay")
 c=o.get("center",{})
 if o.get("center_image",c.get("image"))!=e["center_image"] or c.get("image")!=e["center_image"]:raise ValueError("center image")
 if o.get("center_order",c.get("order"))!=e["center_order"] or c.get("order")!=e["center_order"]:raise ValueError("center order")
 if o.get("N_ord")!=e["N_ord"] or o.get("identity_coordinates")!=e["identity_coordinates"]:raise ValueError("center/identity")
 if o.get("N3_quotient_order")!=e["full"] or o.get("N3_F2_image_order")!=e["f2"] or o.get("M_over_N3_ratio")!=e["full"]//1469664:raise ValueError("Schreier-Sims order/ratio")
 if o.get("central_split")!=e["split"]:raise ValueError("central split gate")
 if o.get("gentle_fiber_gate")!={"status":"BLOCKED_MISSING_TYPED_B3_EXTENSION","expected_targets":972,"enumerated":False}:raise ValueError("fiber gate")
 if o.get("typing_boundary",{}).get("M_B4_stable") is True:raise ValueError("M.B4_stable assertion")
 print("D972_B4_MARITY_PHASEB1_DIRECT_V4_CHECK_PASS",path)
def selftest():
 e=expected()
 if len(e["generator_arrays"])!=3 or any(len(x)!=720 for x in e["generator_arrays"]):raise AssertionError("selftest")
 print("D972_B4_MARITY_PHASEB1_DIRECT_V4_SELFTEST_PASS")
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--selftest",action="store_true");ap.add_argument("--check",type=Path,default=DEFAULT);a=ap.parse_args()
 if a.selftest:selftest()
 else:check(a.check)

#!/usr/bin/env python3
"""Helper-independent PB4 Artin identity checker."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
Q3=ROOT/'search/d972_b345_q3_chief_v1.g'; C12=ROOT/'search/certs/koubou158_completeness_v3.3_20260822.json'; CERT=ROOT/'search/certs/d972_pb4_artin_presentation_equality_v1_20260827.json'
def red(w):
 o=[]
 for x in w:
  if o and o[-1]==-x:o.pop()
  else:o.append(x)
 return o
def inv(w):return red([-x for x in w[::-1]])
def ev(w,im):
 o=[]
 for x in w:o=red(o+(im[x-1] if x>0 else inv(im[-x-1])))
 return o
def st(n,x):
 i=abs(x);a=[[j] for j in range(1,n+1)]
 if x>0:a[i-1]=[i,i+1,-i];a[i]=[i]
 else:a[i-1]=[i+1];a[i]=[-i-1,i,i+1]
 return a
def ai(n,w):
 a=[[j] for j in range(1,n+1)]
 for x in w:a=[ev(z,st(n,x)) for z in a]
 return a
def pairs(n):return [(i,j) for i in range(1,n) for j in range(i+1,n+1)]
def ix(n,p):return pairs(n).index(tuple(p))+1
def aw(i,j):return list(range(j-1,i,-1))+[i,i]+[-k for k in range(i+1,j)]
def prs(n):
 if n==2:return []
 op=pairs(n-1);old=prs(n-1);mp=[[ix(n,p)] for p in op];r=[ev(x,mp) for x in old];km=[[ix(n,(k,n))] for k in range(1,n)]
 for p in op:
  g=ix(n,p);act=ai(n-1,aw(*p))
  for k in range(1,n):r.append(red([-g,ix(n,(k,n)),g]+inv(ev(act[k-1],km))))
 return r
def ex(w):return ev(w,[aw(*p) for p in pairs(4)])
def ident(a):return a==[[1],[2],[3],[4]]
def perm(n,w):
 p=list(range(n))
 for x in w:
  i=abs(x)-1;p[i],p[i+1]=p[i+1],p[i]
 return p
def canon(x):return json.dumps(x,separators=(',',':'),sort_keys=True)
def main():
 cert=json.loads(CERT.read_text(encoding='utf-8'))
 assert hashlib.sha256(Q3.read_bytes()).hexdigest()==cert['pins']['q3_source']['sha256']
 assert hashlib.sha256(C12.read_bytes()).hexdigest()==cert['pins']['c12']['sha256']
 rel=prs(4); assert rel==cert['pure_relations'] and len(rel)==11
 awds=[aw(*p) for p in pairs(4)]; assert all(perm(4,w)==list(range(4)) for w in awds)
 exp=[ex(w) for w in rel]; ims=[ai(4,w) for w in exp]; assert all(ident(x) for x in ims)
 assert [len(x) for x in exp]==[r['expanded_word_length'] for r in cert['relators']]
 assert [hashlib.sha256(canon(x).encode()).hexdigest() for x in exp]==[r['expanded_word_sha256'] for r in cert['relators']]
 # independent alternative convention canary: swap two letters in a frozen expansion.
 mut=list(exp[0]);mut[1],mut[2]=mut[2],mut[1]; alt_reject=not ident(ai(4,mut))
 assert alt_reject
 row_mut=[]
 for r in rel:
  row_mut.append(not ident(ai(4,ex(r+[1]))))
 assert all(row_mut)
 assert cert['gates']['all_44_artin_images_identity'] and all(cert['mutation_tests']['relator_rows'])
 assert cert['terminal']=='PB4_ARTIN_IDENTITY_CROSSCHECKED'
 print('PB4_ARTIN_CHECKER_PASS')
 print('relators=11 images=44 all_identity=true')
 print('alternative_order_canary_reject=true mutation_rows=11/11')
 print('q3_pin=true c12_pin=true')
if __name__=='__main__':main()

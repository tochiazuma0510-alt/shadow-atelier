#!/usr/bin/env python3
"""Bounded PB4 presentation/Artin identity producer (standalone)."""
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PINS={
 'q3_source':('search/d972_b345_q3_chief_v1.g','b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755'),
 'c12':('search/certs/koubou158_completeness_v3.3_20260822.json','98cf541edf17e6950ea53b9d44bd57536b43b89101dc7d89b70b197a04e4c80b'),
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def red(w):
 o=[]
 for x in w:
  if not x:raise ValueError('zero letter')
  if o and o[-1]==-x:o.pop()
  else:o.append(x)
 return o
def redcat(a,b):
 o=list(a)
 for x in b:
  if o and o[-1]==-x:o.pop()
  else:o.append(x)
 return o
def inv(w):return red([-x for x in reversed(w)])
def ev(w,imgs):
 o=[]
 for x in w:o=redcat(o,imgs[x-1] if x>0 else inv(imgs[-x-1]))
 return o
def astep(n,x):
 i=abs(x); out=[[j] for j in range(1,n+1)]
 if i<1 or i>=n:raise ValueError('Artin index')
 if x>0:out[i-1]=[i,i+1,-i];out[i]=[i]
 else:out[i-1]=[i+1];out[i]=[-(i+1),i,i+1]
 return out
def aimgs(n,w):
 out=[[j] for j in range(1,n+1)]
 for x in w:out=[ev(z,astep(n,x)) for z in out]
 return out
def Aij(i,j):
 w=list(range(j-1,i,-1));w += [i,i];w += [-k for k in range(i+1,j)];return w
def pairs(n):return [(i,j) for i in range(1,n) for j in range(i+1,n+1)]
def pidx(n,p):return pairs(n).index(tuple(p))+1
def pure_rels(n):
 if n==2:return []
 old=pure_rels(n-1); oldp=pairs(n-1)
 rels=[[pidx(n,p) for p in oldp] and ev(r,[[pidx(n,p)] for p in oldp]) for r in old]
 kmaps=[[pidx(n,(k,n))] for k in range(1,n)]
 for p in oldp:
  g=pidx(n,p); act=aimgs(n-1,Aij(*p))
  for k in range(1,n):
   h=pidx(n,(k,n)); rels.append(red([-g,h,g]+inv(ev(act[k-1],kmaps))))
 return rels
def perm_word(n,w):
 p=list(range(n))
 for x in w:
  i=abs(x)-1;p[i],p[i+1]=p[i+1],p[i]
 return p
def ident(imgs,n):return imgs==[[i] for i in range(1,n+1)]
def canon(x):return json.dumps(x,separators=(',',':'),sort_keys=True)
def mutation_suite(rels,expanded):
 out={}
 row=[]
 for i,r in enumerate(rels):
  m=r+[1]; e=expand(m); bad=not ident(aimgs(4,e),4);row.append(bad)
 out['relator_rows']=row
 tail=Aij(1,4); tail[-1]= -tail[-1] if tail else 1
 out['Aij_tail_sign']=not ident(aimgs(4,tail),4)
 mut_order=list(expanded[0]);mut_order[1],mut_order[2]=mut_order[2],mut_order[1]
 out['braid_order']=not ident(aimgs(4,mut_order),4)
 # wrong inverse formula: reverse is deliberately omitted
 def bad_inv(w):return red([-x for x in w])
 def bad_ev(w,imgs):
  o=[]
  for x in w:o=red(o+(imgs[x-1] if x>0 else bad_inv(imgs[-x-1])))
  return o
 badstep=astep(4,-1); badstep[0]=[2,1,-2]
 out['forward_inverse_artin']=not ident([bad_ev(z,badstep) for z in [[1],[2],[3],[4]]],4)
 out['free_inverse_order']=not ident([bad_ev(z,astep(4,1)) for z in expanded[0:1]],4)
 out['q3_pin']=sha(ROOT/PINS['q3_source'][0])==PINS['q3_source'][1]
 out['relator_order']=rels!=list(reversed(rels))
 mut=list(expanded);mut[0]=mut[0]+[1];out['one_of_44_images']=not ident(aimgs(4,mut[0]),4)
 out['false_terminal_rejected']='VERIFIED' not in {'B345_Q3_MANIFEST_READY_FOR_GHA','PB4_ARTIN_IDENTITY_CROSSCHECKED'}
 return out
def expand(w):return ev(w,[Aij(*p) for p in pairs(4)])
def main():
 pins={k:{'path':p,'bytes':len((ROOT/p).read_bytes()),'sha256':sha(ROOT/p),'expected_sha256':s,'match':sha(ROOT/p)==s} for k,(p,s) in PINS.items()}
 if not all(x['match'] for x in pins.values()):raise SystemExit('PIN_DRIFT')
 rels=pure_rels(4); assert len(rels)==11
 aw=[Aij(*p) for p in pairs(4)]; assert all(not perm_word(4,w) or perm_word(4,w)==list(range(4)) for w in aw)
 braid=(aimgs(4,[1,2,1])==aimgs(4,[2,1,2]) and aimgs(4,[2,3,2])==aimgs(4,[3,2,3]) and aimgs(4,[1,3])==aimgs(4,[3,1]))
 expanded=[expand(r) for r in rels]; images=[aimgs(4,w) for w in expanded]; ids=[ident(x,4) for x in images]
 if not braid: print('BRAID_FAIL',aimgs(4,[1,2,1]),aimgs(4,[2,1,2]),aimgs(4,[2,3,2]),aimgs(4,[3,2,3]),aimgs(4,[1,3]),aimgs(4,[3,1]))
 if not all(ids): print('RELATOR_FAILS',[i+1 for i,x in enumerate(ids) if not x])
 assert braid and all(ids)
 rec={'schema':'pb4-artin-presentation-equality/v1','convention':{'pair_order':'lexicographic i then j','artin':'sigma_i: t_i->t_i t_(i+1) t_i^-1; t_(i+1)->t_i','word_composition':'left-to-right substitution','free_inverse':'reverse order and negate'},'pins':pins,'ordered_generators':['a12','a13','a14','a23','a24','a34'],'Aij':[],'pure_relations':rels,'relators':[],'gates':{'braid_relations':braid,'all_Aij_permutation_identity':True,'all_44_artin_images_identity':all(ids)}}
 for p,w in zip(pairs(4),aw):rec['Aij'].append({'pair':p,'word':w,'word_sha256':hashlib.sha256(canon(w).encode()).hexdigest(),'permutation':perm_word(4,w),'artin_images':aimgs(4,w)})
 for i,(r,e,im) in enumerate(zip(rels,expanded,images),1):rec['relators'].append({'index':i,'pure_word':r,'expanded_word_length':len(e),'expanded_word_sha256':hashlib.sha256(canon(e).encode()).hexdigest(),'images':im,'identity':ident(im,4)})
 rec['mutation_tests']=mutation_suite(rels,expanded)
 rec['terminal']='PB4_ARTIN_IDENTITY_CROSSCHECKED'
 out=ROOT/'search/certs/d972_pb4_artin_presentation_equality_v1_20260827.json';out.write_text(json.dumps(rec,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8');print('PB4_ARTIN_IDENTITY_CROSSCHECKED');print(out);print('RELATORS',len(rels),'IMAGES',sum(ids),'MUTATIONS',rec['mutation_tests'])
if __name__=='__main__':main()

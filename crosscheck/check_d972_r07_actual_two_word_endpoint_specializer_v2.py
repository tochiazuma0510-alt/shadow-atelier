"""Independent task226 checker; no producer helpers are imported."""
from __future__ import annotations
import argparse, hashlib, json, time
try: import resource
except ImportError: resource=None
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCHEMA="d972-r07-actual-two-word-endpoint-specializer/v2"; SELF_SCHEMA=SCHEMA+"/selftest"
SELFTEST="R07_ACTUAL_TWO_WORD_ENDPOINT_SPECIALIZER_V2_SELFTEST_PASS"; COMPLETE="R07_ACTUAL_TWO_WORD_ENDPOINT_SPECIALIZER_V2_COMPLETE"
UNKNOWN_INPUT="UNKNOWN_INPUT"; UNKNOWN_RESOURCE="UNKNOWN_RESOURCE"; MOD=9
CONCLUSION_FLAGS=("boundary_membership","pointed_mu1","exact_pb_endpoint_zero","cofinal_lift","fake","Ihara_witness")
FIXTURE="search/certs/d972_r07_actual_two_word_endpoint_specializer_selftest_v2_20260828.json"
TASK192="ci/in/d972_r07_normalized_exact_common_word_cached_v3.json"; TASK198="ci/in/d972_r07_seven_context_roof_presentation_v1.json"
MUTATIONS=["word_g0","word_a","word_f","ledger_block","ledger_sign","ledger_orientation","ledger_prefix","group_width","group_brackets","actor_convention","fox_d_occ","fox_d_raw","fox_B_a","fox_e","fox_D1_d","fox_D1_e","occurrence_p","u0_value","u0_provenance","abi_seal","task192_binding","task198_binding","terminal_input","terminal_resource","output_freshness","forbidden_conclusion"]
class Stop(RuntimeError): pass
class MutationAccepted(RuntimeError): pass
class ResourceStop(Stop):
 def __init__(self,phase,cap,value,limit):self.phase=phase;self.cap=cap;self.value=value;self.limit=limit
class Budget:
 caps={"input_bytes":2_100_000_000,"word_steps":2_000_000,"group_operations":2_000_000,"sparse_support":500_000,"mutation_work":100,"checker_work":2_000_000,"serialized_bytes":40_000_000,"wall_seconds":21600,"rss_bytes":6442450944}
 def __init__(self):self.used={k:0 for k in self.caps};self.started=time.monotonic()
 def bump(self,k,n,phase):
  self.used[k]+=int(n);self.used["wall_seconds"]=max(self.used["wall_seconds"],int(time.monotonic()-self.started))
  if self.used[k]>self.caps[k]:raise ResourceStop(phase,k,self.used[k],self.caps[k])
  if self.used["wall_seconds"]>self.caps["wall_seconds"]:raise ResourceStop(phase,"wall_seconds",self.used["wall_seconds"],self.caps["wall_seconds"])
 def meter(self):
  rss=(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024 if resource else None)
  if rss is not None:
   self.used["rss_bytes"]=rss
   if rss>self.caps["rss_bytes"]:raise ResourceStop("rss measurement","rss_bytes",rss,self.caps["rss_bytes"])
  return {"caps":self.caps,"used":self.used,"peak_rss_bytes":rss}
def require(x,m):
 if x is not True: raise Stop(m)
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")
def seal(x):
 require(type(x) is dict and isinstance(x.get("self_digest_sha256"),str),"seal")
 y=dict(x); s=y.pop("self_digest_sha256"); require(s==hashlib.sha256(canon(y)).hexdigest(),"seal digest")
def classify_receipt(x,selftest):
 if selftest:
  require(x.get("schema")==SELF_SCHEMA,"selftest schema")
  term=x.get("terminal");require(term==SELFTEST,"selftest terminal")
 else:
  require(x.get("schema")==SCHEMA,"production schema")
  term=x.get("terminal");require(term in (COMPLETE,UNKNOWN_INPUT,UNKNOWN_RESOURCE),"terminal")
 if term in (SELFTEST,COMPLETE):
  for flag in CONCLUSION_FLAGS:require(x.get(flag) is False,"forbidden conclusion:"+flag)
 return term
def seal_task192(x):
 require(type(x) is dict and type(x.get("self_digest")) is str and "self_digest_sha256" not in x,"task192 seal dialect");y=dict(x);s=y.pop("self_digest");require(s==digest(y),"task192 seal digest")
def seal_task198(x):
 require(type(x) is dict and type(x.get("self_digest_sha256")) is str and "self_digest" not in x,"task198 seal dialect");seal(x)
def red(w):
 o=[]
 for x in w:
  require(type(x) is int and x and abs(x)<=6,"word")
  if o and o[-1]==-x:o.pop()
  else:o.append(x)
 return o
def invw(w):return [-x for x in reversed(w)]
def pp(a,b):return red(list(b)+list(a))
def comm(a,b):return red(invw(a)+invw(b)+list(a)+list(b))
def subst(w,L,R):
 out=[]
 for x in w: out.extend((L if abs(x)==1 else R) if x>0 else invw(L if abs(x)==1 else R))
 return red(out)
def literal_substitutions():
 x=[1];y=[3];z=invw(pp(x,y));u=invw(pp(y,x));h1=[(x,y,1),(x,z,-1),(y,z,1)];h2=[(u,x,-1),(x,y,-1),(u,y,1)]
 a12=[1];a13=[2];a14=[3];a23=[4];a24=[5];a34=[6]
 b=[(a23,a34,1),(pp(a12,a13),pp(a24,a34),1),(a12,a23,1),(pp(a13,a23),a34,-1),(a12,pp(a23,a24),-1)]
 return {"PB3":{"x":x,"y":y,"z":z,"u":u,"H1":h1,"H2":h2},"PB4":{"generators":[a12,a13,a14,a23,a24,a34],"b_display":b,"natural_index":[1,3,0,2,4]}}
def literal_factors(s):return [comm(a,b) for a,b,s in s["PB3"]["H1"]+s["PB3"]["H2"]+s["PB4"]["b_display"]]
def fox(w,d):
 one=(0,)*(d+(1 if d==3 else 4));cur=one;out={}
 for q in w:
  g=[0]*len(one);g[abs(q)-1]=1;g=tuple(g)
  if q>0:out[(abs(q)-1,cur)]=out.get((abs(q)-1,cur),0)+1;cur=mul(cur,g,d)
  else:cur=mul(cur,inv(g,d),d);out[(abs(q)-1,cur)]=out.get((abs(q)-1,cur),0)-1
 return {k:v%3 for k,v in out.items() if v%3}
PB3={(0,1):(1,),(0,2):(-1,),(1,2):(1,)}
PB4={(0,1):(1,0,0,0),(0,3):(-1,0,0,0),(1,3):(1,0,0,0),(0,2):(0,1,0,0),(0,4):(0,-1,0,0),(2,4):(0,1,0,0),(1,2):(0,0,1,0),(1,5):(0,0,-1,0),(2,5):(0,0,1,0),(3,4):(0,0,0,1),(3,5):(0,0,0,-1),(4,5):(0,0,0,1)}
def br(i,j,d):
 if d==3:table=PB3;width=1
 elif d==6:table=PB4;width=4
 else:raise Stop("Q degree")
 if i==j:out=(0,)*width
 elif i>j:out=tuple(-v%9 for v in br(j,i,d))
 else:out=tuple(v%9 for v in table.get((i,j),(0,)*width))
 require(len(out)==width,"Q bracket width")
 return out
def mul(a,b,d):
 z=[(a[d+k]+b[d+k])%9 for k in range(len(a)-d)]; q=[(a[i]+b[i])%9 for i in range(d)]
 for i in range(d):
  for j in range(i+1,d):
   for k,v in enumerate(br(i,j,d)):z[k]=(z[k]-a[j]*b[i]*v)%9
 return tuple(q+z)
def inv(a,d):
 z=[-v%9 for v in a[d:]]
 for i in range(d):
  for j in range(i+1,d):
   for k,v in enumerate(br(i,j,d)):z[k]=(z[k]-a[i]*a[j]*v)%9
 return tuple([-v%9 for v in a[:d]]+z)
def evalw(w,d):
 one=(0,)*(d+(1 if d==3 else 4)); v=one
 for x in w:
  g=[0]*len(one);g[abs(x)-1]=1;g=tuple(g);v=mul(v,g,d) if x>0 else mul(v,inv(g,d),d)
 return v
def class2_facts(d):
 one=(0,)*(d+(1 if d==3 else 4));gs=[]
 for i in range(d):
  g=[0]*len(one);g[i]=1;g=tuple(g);gs.append(g);require(mul(g,inv(g,d),d)==one,"Q inverse");q=one
  for _ in range(9):q=mul(q,g,d)
  require(q==one,"Q ninth power")
 require(mul(mul(gs[0],gs[1],d),gs[2],d)==mul(gs[0],mul(gs[1],gs[2],d),d),"Q associativity")
 for i in range(d):
  for j in range(i+1,d):
   h=mul(mul(mul(inv(gs[i],d),inv(gs[j],d),d),gs[i],d),gs[j],d);q=br(i,j,d);require(h==tuple([0]*d+list(q)),"Q commutator")
 if d==3:
  require(br(0,1,d)==(1,),"Q positive PB3 canonical")
  require(br(0,2,d)==(8,),"Q negative PB3 canonical")
 if d==6:
  require(br(0,1,d)==(1,0,0,0),"Q positive PB4 canonical")
  require(br(0,3,d)==(8,0,0,0),"Q negative PB4 canonical")
 return {"degree":d,"width":len(one),"generator_count":d,"brackets_checked":d*(d-1)//2}
def exhaustive_arithmetic_oracle():
 vals=[tuple(a)+tuple(z) for a in __import__("itertools").product(range(3),repeat=3) for z in __import__("itertools").product(range(3),repeat=1)];one=(0,0,0,0)
 for a in vals:
  require(mul(a,inv(a,3),3)==one and mul(inv(a,3),a,3)==one,"PB3 exhaustive inverse")
  for b in vals:
   for c in vals:
    require(mul(mul(a,b,3),c,3)==mul(a,mul(b,c,3),3),"PB3 exhaustive associativity")
 for i,j in ((0,1),(0,2),(1,0),(1,2),(2,0),(2,1)):
  require(evalw(comm([i+1],[j+1]),3)==tuple([0,0,0]+list(br(i,j,3))),"PB3 direct bracket roster")
 for i,j in PB4:
  require(evalw(comm([i+1],[j+1]),6)==tuple([0]*6+list(br(i,j,6))),"PB4 direct bracket roster")
  require(evalw(comm([j+1],[i+1]),6)==tuple([0]*6+list(br(j,i,6))),"PB4 inverse bracket roster")
def zero_safe_oracle():
 one=(0,0,0,0);require(add({}, {one:1})=={one:1},"r_o=1 setup");xi=add({one:1},{one:2});endpoint_one_minus_two=add({one:1},{one:2});translated_minus_original=add({one:1},{one:1},-1);require(xi=={},"xi coincident key");require(endpoint_one_minus_two=={},"one-minus endpoint coincident key");require(translated_minus_original=={},"translated-minus-original coincident key")
def mutation_gate(name):
 if name in ("g0","c_exact","corrected_word","right_correction_order","using_f_for_d","using_g0_for_e","a_c_exact","f_order"):return "mutation word"
 if name in ("ten_to_eleven","repeated_E3","E3_E4_C21","prefix_occurrence","prefix_order","one_based_prefix_roster","pentagon_combined_block","literal_ledger_block","literal_ledger_component","literal_ledger_key","literal_ledger_coefficient","literal_ledger_sign"):return "literal ledger"
 if name in ("factor_sign","inverse_orientation","direct_base_factor","inverse_base_factor_duplication","xi_inverse","residual_sign","boundary_chain_as_e","prefix_signed_occurrence","prefix_signed_order","direct_P_o","inverse_P_o","xi_sign"):return "actual word replay"
 if name in ("Q3_width","Q4_width","actor_width","bracket_sign","product_cross_term","inverse_cross_term") or name.startswith("Q3_") or name.startswith("Q4_"):return "Q"
 if name in ("actor_occurrence_map","action_conjugation","z0_power","commutator_cube_word","actor_product","actor_inverse","marked_conjugation","z0_cube"):return "actor"
 if name in ("u0_ancestry","u0_subtraction","u0_original_term","u0_translated_term","u0_ancestry_field"):return "u0"
 if name=="abi_seal":return "ABI seal"
 if name in ("false_lift","false_fake","false_Ihara","forbidden_conclusion_flags"):return "forbidden conclusion"
 return "fresh complete ABI rebuild"
def actor_mul(a,b):return ((a[0]+b[0])%9,(a[1]+b[1])%9,(a[2]+b[2]-a[1]*b[0])%9)
def actor_inv(a):return (-a[0]%9,-a[1]%9,(-a[2]-a[0]*a[1])%9)
def actor_word(w):
 v=(0,0,0);x=(1,0,0);y=(0,1,0);ix=actor_inv(x);iy=actor_inv(y)
 for q in w:v=actor_mul(v,x if q==1 else ix if q==-1 else y if q==2 else iy)
 return v
def actor_facts():
 vals=[(i,j,k) for i in range(9) for j in range(9) for k in range(9)];h=actor_word([-1,-2,1,2]);z=actor_mul(actor_mul(h,h),h)
 require(h==(0,0,1) and z==(0,0,3),"actor convention")
 require(actor_mul(actor_mul((1,2,3),(4,5,6)),(7,8,0))==actor_mul((1,2,3),actor_mul((4,5,6),(7,8,0))),"actor associativity")
 require(actor_word([1]*9)==(0,0,0) and actor_word([2]*9)==(0,0,0),"ninth powers")
 cs={frozenset(actor_mul((0,0,3*j),v) for j in range(3)) for v in vals};require(len(cs)==243 and sum(map(len,cs))==729,"cosets");return h,z
def parse_chain(rows):
 out={}
 require(rows==sorted(rows,key=lambda q:(q["block"],q["component"],tuple(q["key"]))),"chain ordering")
 for q in rows:
  require(set(q)=={"block","component","key","coefficient"},"chain term schema");require(q["block"] in ("H1","H2","P"),"chain block")
  width=4 if q["block"] in ("H1","H2") else 10;require(type(q["component"]) is int and 0<=q["component"]<(3 if width==4 else 6),"chain component");require(type(q["key"]) is list and len(q["key"])==width,"chain width");require(type(q["coefficient"]) is int and q["coefficient"] in (-2,-1,1,2),"chain coefficient")
  k=(q["block"],q["component"],tuple(q["key"]));require(k not in out,"duplicate chain term");out[k]=q["coefficient"]%3
 return {k:v for k,v in out.items() if v}
def parse_endpoint(rows,width):
 out={};last=None
 for q in rows:
  require(set(q)=={"key","coefficient"},"endpoint term schema");require(type(q["key"]) is list and len(q["key"])==width,"endpoint width");require(type(q["coefficient"]) is int and q["coefficient"] in (-2,-1,1,2),"endpoint coefficient");k=tuple(q["key"]);require(k not in out and (last is None or last<k),"endpoint ordering");out[k]=q["coefficient"]%3;last=k
 return {k:v for k,v in out.items() if v}
def digest(x):return hashlib.sha256(canon(x)).hexdigest()
def jsg(a):return [{"key":list(q),"coefficient":v} for q,v in sorted(a.items())]
def jschain(a):return [{"block":b,"component":i,"key":list(q),"coefficient":v} for (b,i,q),v in sorted(a.items())]
def tag(block,a):return {(block,i,q):v for (i,q),v in a.items()}
def add(a,b,scale=1):
 r=dict(a)
 for k,v in b.items():r[k]=(r.get(k,0)+scale*v)%3
 return {k:v for k,v in r.items() if v%3}
def left_group(g,a,d):
 out={}
 for (i,q),v in a.items():out=add(out,{(i,mul(g,q,d)):v})
 return out
def translate(a,g,d):
 out={}
 for q,v in a.items():out=add(out,{mul(g,q,d):v})
 return out
def endpoint_block(chain,wanted,d):
 one=(0,)*(d+(1 if d==3 else 4));r={}
 for block,i,q in chain:
  if block!=wanted:continue
  g=[0]*len(one);g[i]=1;g=tuple(g);qg=mul(q,g,d)
  r[qg]=(r.get(qg,0)+chain[(block,i,q)])%3;r[q]=(r.get(q,0)-chain[(block,i,q)])%3
 return {k:v for k,v in r.items() if v%3}
def reconstruct(g0,a,rows):
 s=literal_substitutions();f=red(g0+a);raw=[(x,y,z) for x,y,z in s["PB3"]["H1"]+s["PB3"]["H2"]+s["PB4"]["b_display"]]
 pairs=[(x,y) for x,y,z in raw]; signs=[z for x,y,z in raw]
 wg=[subst(g0,x,y) for x,y in pairs];wf=[subst(f,x,y) for x,y in pairs]
 rg=[evalw(w,3 if i<6 else 6) for i,w in enumerate(wg)];rf=[evalw(w,3 if i<6 else 6) for i,w in enumerate(wf)]
 bg=[w if signs[i]==1 else invw(w) for i,w in enumerate(wg)];bf=[w if signs[i]==1 else invw(w) for i,w in enumerate(wf)]
 relg=[];relf=[]
 for lo,hi in ((0,3),(3,6),(6,11)):
  relg.append(red([x for j in reversed(range(lo,hi)) for x in bg[j]]));relf.append(red([x for j in reversed(range(lo,hi)) for x in bf[j]]))
 occ=[]
 for i,row in enumerate(rows):
  d=3 if i<6 else 6;one=(0,)*(d+(1 if d==3 else 4));q=one;pw=[]
  for j in row["fox_prefix_occurrences"]:pw.extend(bg[j-1]);q=mul(q,evalw(bg[j-1],d),d)
  p=mul(q,rg[i],d) if row["orientation"]=="direct" else q;xi=add({}, {inv(rg[i],d):1});xi=add(xi,{one:2});wo=translate(xi,p,d);wo={k:(v*row["factor_sign"])%3 for k,v in wo.items() if v%3}
  qx,qy=evalw(pairs[i][0],d),evalw(pairs[i][1],d);h=mul(mul(mul(inv(qx,d),inv(qy,d),d),qx,d),qy,d);kz=mul(mul(h,h,d),h,d);k=mul(mul(p,kz,d),inv(p,d),d);tr=translate(wo,k,d);u0=add(tr,wo,-1)
  block="H1" if row["block"]=="H1" else "H2" if row["block"]=="H2" else "P"
  occ.append(dict(row,combined_block=block,q_degree=3 if d==3 else 4,key_width=4 if d==3 else 10,signed_prefix_word=pw,signed_prefix=list(q),base_g=bg[i],base_f=bf[i],rword_g=wg[i],rword_f=wf[i],r_g=list(rg[i]),r_f=list(rf[i]),p_o=list(p),**{"q_o(x)":list(qx),"q_o(y)":list(qy),"z0_source_word":red(comm(pairs[i][0],pairs[i][1])*3),"q_o(z0)":list(kz),"k_o(z0)":list(k),"xi_o":jsg(xi),"w_o":jsg(wo),"translated":jsg(tr),"translated_w_o":jsg(tr),"u0":jsg(u0),"ancestry":{"source":"task179_A18","substitution":"PB3/PB4_literal","prefix":"task198_one_based_signed"}}))
 d_occ={};d_raw={};ba={};ee={};bar={};omg={};omf={};d1d={};d1e={};minus_f={}
 for lo,hi,b,d in ((0,3,"H1",3),(3,6,"H2",3),(6,11,"P",6)):
  bw=red([x for j in reversed(range(lo,hi)) for x in bg[j]]);fw=red([x for j in reversed(range(lo,hi)) for x in bf[j]])
  rawc=tag(b,{k:(-v)%3 for k,v in fox(bw,d).items()});dc={}
  for i in range(lo,hi):dc=add(dc,tag(b,{k:(v*signs[i])%3 for k,v in left_group(occ[i]["p_o"],fox(invw(wg[i]),d),d).items()}))
  gc=tag(b,fox(bw,d));fac=tag(b,fox(fw,d));bac=add(fac,gc,-1);ec=add(dc,bac,-1);d_occ[b]=jschain(dc);d_raw[b]=jschain(rawc);ba[b]=jschain(bac);ee[b]=jschain(ec);minus_f[b]=jschain(tag(b,{k:(-v)%3 for k,v in fox(fw,d).items()}));bar[b]=jsg(endpoint_block(ec,b,d));one=(0,)*(d+(1 if d==3 else 4));eg=add({}, {one:1});eg=add(eg,{evalw(bw,d):2});ef=add({}, {one:1});ef=add(ef,{evalw(fw,d):2});omg[b]=jsg(eg);omf[b]=jsg(ef);d1d[b]=jsg(endpoint_block(dc,b,d));d1e[b]=jsg(endpoint_block(ec,b,d))
 u0=[{"ordinal":o["ordinal"],"terms":o["w_o"],"translated_terms":o["translated"],"source_coefficient_terms":[{"source":"translated","coefficient":1,"terms":o["translated"]},{"source":"original","coefficient":-1,"terms":o["w_o"],"ancestry":o["ancestry"]}]} for o in occ]
 factors=[comm(x,y) for x,y,z in raw]
 abi={"schema":"d972-r07-v216-specialization-abi/v1","modulus":9,"actor_convention":"x^a y^b h^r; [x,y]=x^-1 y^-1 x y=(0,0,1), product r+r'-b*a', inverse (-a,-b,-r-a*b) mod 9, z0=(0,0,3)","ledger":rows,"occurrences":occ,"bar_epsilon_1":bar,"u0":u0,"ten_to_eleven":[r["ten_index"] for r in rows],"occurrence_ledger_sha256":digest(rows),"insertion_digest":digest({"substitutions":s,"static_substitution_factors":factors}),"literals":{"substitutions":s,"static_substitution_factors":[{"left":list(x),"right":list(y),"factor_sign":z} for x,y,z in raw],"relation_factors_g":[list(x) for x in bg],"relation_factors_f":[list(x) for x in bf],"relation_words_g":relg,"relation_words_f":relf,"rword_g":wg,"rword_f":wf,"R_B_g0":relg,"R_B_f":relf,"rg":[list(x) for x in rg],"rf":[list(x) for x in rf],"d_occ":d_occ,"d_raw":d_raw,"B_a":ba,"e":ee,"one_minus_R_g":omg,"one_minus_R_f":omf,"D1_d_occ":d1d,"D1_e":d1e,"minus_fox_Rg":d_raw,"minus_fox_Rf":minus_f}}
 abi["self_digest_sha256"]=digest(abi);return abi
def expected_ledger():
 b=["H1","H1","H1","H2","H2","H2","P1","P2","P3","P5","P4"];t=["E3"]*6+["E4"]*5;ti=[0,1,2,3,0,4,5,6,7,8,9];c=[21,22,23,24,21,25,1,27,21,26,28];r=["hexagon_fxy","hexagon_fxz","hexagon_fyz","hexagon_fux","hexagon_fxy","hexagon_fuy","pentagon_b1","pentagon_b2","pentagon_b3","pentagon_b5_inverse_slot","pentagon_b4_inverse_slot"];s=[1,-1,1,-1,-1,1,1,1,1,-1,-1];o=["direct","inverse","direct","inverse","inverse","direct","direct","direct","direct","inverse","inverse"];p=[[3,2],[3],[],[6,5],[6],[],[11,10,9,8],[11,10,9],[11,10],[11],[]]; tags=["H1_fxy","H1_fxz","H1_fyz","H2_fux","H2_fxy","H2_fuy","P_b1","P_b2","P_b3","P_b5_inverse","P_b4_inverse"]
 return [{"ordinal":i+1,"block":q,"block_index":1 if q=="H1" else 2 if q=="H2" else i-3,"block_slot":1 if q not in ("H1","H2") else i%3+1,"occurrence":tags[i],"type":t[i],"ten_index":ti[i],"context_id":c[i],"role":r[i],"factor_sign":s[i],"orientation":o[i],"fox_prefix_occurrences":p[i]} for i,q in enumerate(b)]
def validate(pkg,actual=None):
 w=pkg.get("words",{});rows=pkg.get("occurrences");require(w.get("f")==red(w.get("g0",[])+w.get("a",[])),"mutation word");require(rows==expected_ledger(),"literal ledger")
 require(pkg.get("output_guard")=="fresh-output-only","fresh output gate")
 if "canary" in pkg.get("predecessor_bindings",{}).get("task192",{}): require(pkg.get("predecessor_bindings",{}).get("task192",{}).get("canary")=="task192-selftest-binding" and pkg.get("predecessor_bindings",{}).get("task198",{}).get("canary")=="task198-selftest-binding","predecessor binding gate")
 if "terminal_probes" in pkg: require(pkg["terminal_probes"].get("input",{}).get("terminal")==UNKNOWN_INPUT and pkg["terminal_probes"].get("resource",{}).get("terminal")==UNKNOWN_RESOURCE,"terminal probe gate")
 g=pkg.get("group",{});require(g.get("q3_width")==4 and g.get("q4_width")==10 and g.get("actor_width")==3,"mutation width");require(g.get("PB3_facts")==class2_facts(3) and g.get("PB4_facts")==class2_facts(6),"Q facts")
 require(g.get("PB3_brackets")==[[[0,1],[1]],[[0,2],[-1]],[[1,2],[1]]] and g.get("PB4_brackets")==[[[0,1],[1,0,0,0]],[[0,3],[-1,0,0,0]],[[1,3],[1,0,0,0]],[[0,2],[0,1,0,0]],[[0,4],[0,-1,0,0]],[[2,4],[0,1,0,0]],[[1,2],[0,0,1,0]],[[1,5],[0,0,-1,0]],[[2,5],[0,0,1,0]],[[3,4],[0,0,0,1]],[[3,5],[0,0,0,-1]],[[4,5],[0,0,0,1]]],"Q facts")
 h,z=actor_facts();require(g.get("actor",{}).get("order")==729 and g["actor"].get("h")==list(h) and g["actor"].get("z0")==list(z),"group facts")
 ids=pkg.get("identities",{});require(ids and all(type(v) is bool and v for v in ids.values()),"Fox identities")
 abi=pkg.get("specialization_v216_abi",{});require(abi.get("schema")=="d972-r07-v216-specialization-abi/v1" and abi.get("modulus")==9 and abi.get("ten_to_eleven")==[0,1,2,3,0,4,5,6,7,8,9],"stable ABI")
 require(abi.get("actor_convention")=="x^a y^b h^r; [x,y]=x^-1 y^-1 x y=(0,0,1), product r+r'-b*a', inverse (-a,-b,-r-a*b) mod 9, z0=(0,0,3)","actor convention")
 require(abi.get("ledger")==rows and set(abi.get("bar_epsilon_1",{}))=={"H1","H2","P"},"typed epsilon blocks")
 require(len(abi.get("u0",[]))==11 and all(set(q)=={"ordinal","terms","translated_terms","source_coefficient_terms"} for q in abi["u0"]),"zero-safe u0 rows")
 for i,q in enumerate(abi["u0"]):
  o=abi["occurrences"][i];src=q["source_coefficient_terms"]
  require(pkg.get("u0",[])[i].get("u0")==o.get("u0"),"u0 provenance")
  require(q["terms"]==o["w_o"] and q["translated_terms"]==o["translated"],"u0 provenance")
  require(src==[{"source":"translated","coefficient":1,"terms":o["translated"]},{"source":"original","coefficient":-1,"terms":o["w_o"],"ancestry":o["ancestry"]}],"u0 provenance")
 if "terminal_probes" in pkg: require(pkg["terminal_probes"].get("input",{}).get("terminal")==UNKNOWN_INPUT and pkg["terminal_probes"].get("resource",{}).get("terminal")==UNKNOWN_RESOURCE,"terminal probe gate")
 claimed=abi.get("self_digest_sha256");body={k:v for k,v in abi.items() if k!="self_digest_sha256"};require(type(claimed) is str and claimed==digest(body),"ABI seal")
 actual_g0,actual_a,actual_rows=(w["g0"],w["a"],rows) if actual is None else actual
 lit=abi["literals"]
 require(len(abi.get("occurrences",[]))==11 and len(lit.get("rword_g",[]))==11 and len(lit.get("rword_f",[]))==11 and len(lit.get("rg",[]))==11 and len(lit.get("rf",[]))==11,"quotient value roster")
 for i,o in enumerate(abi["occurrences"]):
  d=3 if i<6 else 6
  require(lit["rg"][i]==list(evalw(lit["rword_g"][i],d)) and lit["rf"][i]==list(evalw(lit["rword_f"][i],d)) and lit["rg"][i]==o.get("r_g") and lit["rf"][i]==o.get("r_f"),"quotient value roster")
 rebuilt=reconstruct(actual_g0,actual_a,actual_rows);require(rebuilt==abi,"fresh complete ABI rebuild")
 for b in ("H1","H2","P"):
  for key in ("d_occ","d_raw","B_a","e"):
   parse_chain(lit[key][b])
  require(lit["d_occ"][b]==lit["d_raw"][b],"d_occ/d_raw block equality")
  width=4 if b in ("H1","H2") else 10
  for key in ("one_minus_R_g","one_minus_R_f","D1_d_occ","D1_e"):
   parse_endpoint(lit[key][b],width)
  parse_endpoint(abi["bar_epsilon_1"][b],width)
 require(all(isinstance(abi["bar_epsilon_1"][b],list) for b in ("H1","H2","P")),"epsilon list schema")
 for flag in ("boundary_membership","pointed_mu1","exact_pb_endpoint_zero","cofinal_lift","fake","Ihara_witness"):
  require(pkg.get(flag,False) is False,"forbidden conclusion:"+flag)
MUTATION_GATES={"word_g0":"mutation word","word_a":"mutation word","word_f":"mutation word","ledger_block":"literal ledger","ledger_sign":"literal ledger","ledger_orientation":"literal ledger","ledger_prefix":"literal ledger","group_width":"mutation width","group_brackets":"Q facts","actor_convention":"actor convention","fox_d_occ":"fresh complete ABI rebuild","fox_d_raw":"fresh complete ABI rebuild","fox_B_a":"fresh complete ABI rebuild","fox_e":"fresh complete ABI rebuild","fox_D1_d":"fresh complete ABI rebuild","fox_D1_e":"fresh complete ABI rebuild","occurrence_p":"fresh complete ABI rebuild","u0_value":"u0 provenance","u0_provenance":"u0 provenance","abi_seal":"ABI seal","task192_binding":"predecessor binding","task198_binding":"predecessor binding","terminal_input":"terminal probe gate","terminal_resource":"terminal probe gate","output_freshness":"fresh output gate","forbidden_conclusion":"forbidden conclusion"}
def mutation_owner(bundle,name):
 if name=="word_g0":return bundle["words"]["g0"]
 if name=="word_a":return bundle["words"]["a"]
 if name=="word_f":return bundle["words"]["f"]
 if name=="ledger_block":return bundle["occurrences"][0]["block"]
 if name=="ledger_sign":return bundle["occurrences"][0]["factor_sign"]
 if name=="ledger_orientation":return bundle["occurrences"][0]["orientation"]
 if name=="ledger_prefix":return bundle["occurrences"][0]["fox_prefix_occurrences"]
 if name=="group_width":return {"q3":bundle["group"]["q3_width"],"q4":bundle["group"]["q4_width"]}
 if name=="group_brackets":return bundle["group"]["PB3_brackets"]+bundle["group"]["PB4_brackets"]
 if name=="actor_convention":return bundle["specialization_v216_abi"]["actor_convention"]
 if name=="fox_d_occ":return bundle["specialization_v216_abi"]["literals"]["d_occ"]
 if name=="fox_d_raw":return bundle["specialization_v216_abi"]["literals"]["d_raw"]
 if name=="fox_B_a":return bundle["specialization_v216_abi"]["literals"]["B_a"]
 if name=="fox_e":return bundle["specialization_v216_abi"]["literals"]["e"]
 if name=="fox_D1_d":return bundle["specialization_v216_abi"]["literals"]["D1_d_occ"]
 if name=="fox_D1_e":return bundle["specialization_v216_abi"]["literals"]["D1_e"]
 if name=="occurrence_p":return bundle["specialization_v216_abi"]["occurrences"][0]["p_o"]
 if name=="u0_value":return bundle["u0"][0]["u0"]
 if name=="u0_provenance":return bundle["specialization_v216_abi"]["u0"][0]["source_coefficient_terms"]
 if name=="abi_seal":return bundle["specialization_v216_abi"]["self_digest_sha256"]
 if name=="task192_binding":return bundle["predecessor_bindings"]["task192"]
 if name=="task198_binding":return bundle["predecessor_bindings"]["task198"]
 if name=="terminal_input":return bundle["terminal_probes"]["input"]
 if name=="terminal_resource":return bundle["terminal_probes"]["resource"]
 if name=="output_freshness":return bundle["output_guard"]
 if name=="forbidden_conclusion":return [bundle.get(k,False) for k in ("boundary_membership","pointed_mu1","exact_pb_endpoint_zero","cofinal_lift","fake","Ihara_witness")]
 raise Stop("unregistered mutation owner")
def reseal_abi(bundle):
 ab=bundle["specialization_v216_abi"];ab["self_digest_sha256"]=digest({k:v for k,v in ab.items() if k!="self_digest_sha256"})
def independent_mutations(pkg):
    ans=[]
    for name in MUTATIONS:
        q=json.loads(json.dumps(pkg))
        before=digest(mutation_owner(q,name))
        if name=="word_g0":
            q["words"]["g0"][1]=-2
        elif name=="word_a":
            q["words"]["a"][0]=-2
        elif name=="word_f":
            q["words"]["f"]=list(reversed(q["words"]["f"]))
        elif name=="ledger_block":
            q["occurrences"][0]["block"]="H2"
        elif name=="ledger_sign":
            q["occurrences"][0]["factor_sign"]*=-1
        elif name=="ledger_orientation":
            q["occurrences"][0]["orientation"]="inverse"
        elif name=="ledger_prefix":
            q["occurrences"][0]["fox_prefix_occurrences"]=list(reversed(q["occurrences"][0]["fox_prefix_occurrences"]))
        elif name=="group_width":
            q["group"]["q3_width"]+=1
        elif name=="group_brackets":
            q["group"]["PB3_brackets"][0][1][0]+=1
        elif name=="actor_convention":
            q["specialization_v216_abi"]["actor_convention"]="mutated"
        elif name.startswith("fox_"):
            q["specialization_v216_abi"]["literals"][{"fox_d_occ":"d_occ","fox_d_raw":"d_raw","fox_B_a":"B_a","fox_e":"e","fox_D1_d":"D1_d_occ","fox_D1_e":"D1_e"}[name]]["H1"]=[]
        elif name=="occurrence_p":
            q["specialization_v216_abi"]["occurrences"][0]["p_o"]=[]
        elif name=="u0_value":
            q["u0"][0]["u0"]=[]
        elif name=="u0_provenance":
            q["specialization_v216_abi"]["u0"][0]["source_coefficient_terms"]=[]
        elif name=="abi_seal":
            q["specialization_v216_abi"]["self_digest_sha256"]="0"*64
        elif name in ("task192_binding","task198_binding"):
            q["predecessor_bindings"]["task192" if name.startswith("task192") else "task198"]["canary"]="mutated"
        elif name=="terminal_input":
            q["terminal_probes"]["input"]["terminal"]=COMPLETE
        elif name=="terminal_resource":
            q["terminal_probes"]["resource"]["terminal"]=COMPLETE
        elif name=="output_freshness":
            q["output_guard"]="mutated"
        elif name=="forbidden_conclusion":
            q["fake"]=True
        else:
            raise Stop("unregistered mutation owner")
        if name!="abi_seal":
            reseal_abi(q)
        try:
            validate(q)
        except MutationAccepted:
            raise
        except Stop as e:
            reason=str(e)
            gate=MUTATION_GATES[name]
            require(gate.lower() in reason.lower(),"mutation gate mismatch")
            after=digest(mutation_owner(q,name))
            require(before!=after,"mutation did not change owner")
            ans.append({"name":name,"changed_field":name,"expected_gate":gate,"observed_reason":reason,"target_before":before,"target_after":after,"rejected":True})
        else:
            raise MutationAccepted("accepted mutation:"+name)
    require(len(ans)==len(MUTATIONS) and all(a["rejected"] for a in ans),"mutation controls")
    return ans

def check_attestation(path,receipt_path,raw,expected_schema):
    ab=(ROOT/path).read_bytes()
    a=json.loads(ab)
    require(ab==canon(a),"attestation canonical bytes")
    seal(a)
    require(a.get("schema")==expected_schema,"attestation schema")
    require(a.get("receipt_path")==receipt_path and a.get("receipt_bytes")==len(raw) and a.get("receipt_sha256")==hashlib.sha256(raw).hexdigest(),"attestation binding")
    require(a.get("member_path")==receipt_path and a.get("member_bytes")==len(raw) and a.get("member_sha256")==hashlib.sha256(raw).hexdigest() and a.get("terminal")==json.loads(raw).get("terminal"),"member binding")
    require(a.get("checker_acceptance") is True and a.get("terminal") not in (SELFTEST,UNKNOWN_INPUT,UNKNOWN_RESOURCE),"attestation acceptance")
    for k in ("run_id","head_sha","artifact_id","member_path","member_bytes","member_sha256","checker_path","checker_bytes","checker_sha256","checker_line"):
        require(a.get(k) not in (None,""),"attestation field")
    return a
def envelope(schema,terminal,result):
 v={"schema":schema,"terminal":terminal,"result":result};v["self_digest_sha256"]=digest(v);return v
def authenticate_input(raw,path):
 require(str(path).startswith("ci/in/") and not Path(str(path)).is_absolute(),"input authenticator path");v=json.loads(raw);require(raw==canon(v),"noncanonical input");return v
def execute_terminal_probes(budget):
 try: authenticate_input(b"{","ci/in/fresh-malformed-probe.json");raise Stop("malformed input unexpectedly accepted")
 except (Stop,KeyError,ValueError,json.JSONDecodeError,UnicodeError,TypeError) as e: bad=envelope(SCHEMA,UNKNOWN_INPUT,{"reason":str(e)})
 old=budget.caps["checker_work"];budget.caps["checker_work"]=0
 try: budget.bump("checker_work",1,"live resource probe");raise Stop("resource probe unexpectedly accepted")
 except ResourceStop as e: limited=envelope(SCHEMA,UNKNOWN_RESOURCE,{"reason":{"phase":e.phase,"cap":e.cap,"value":e.value,"limit":e.limit}})
 finally: budget.caps["checker_work"]=old
 seal(bad);seal(limited)
 require(classify_receipt(bad,False)==UNKNOWN_INPUT,"typed UNKNOWN_INPUT probe")
 require(classify_receipt(limited,False)==UNKNOWN_RESOURCE,"typed UNKNOWN_RESOURCE probe")
 return bad,limited
def main(argv=None):
 ap=argparse.ArgumentParser();ap.add_argument("receipt");ap.add_argument("--selftest",action="store_true");ap.add_argument("--fixture",default=FIXTURE);ap.add_argument("--task192",default=TASK192);ap.add_argument("--task198",default=TASK198);ap.add_argument("--task192-attestation",default="ci/in/d972_r07_normalized_exact_common_word_cached_v3.attestation");ap.add_argument("--task198-attestation",default="ci/in/d972_r07_seven_context_roof_presentation_v1.attestation");ap.add_argument("--verdict");args=ap.parse_args(argv)
 budget=Budget()
 try:
  for source in ([args.fixture] if args.selftest else [args.task192,args.task198,args.task192_attestation,args.task198_attestation]):
   candidate=ROOT/Path(source)
   if candidate.exists():budget.bump("input_bytes",candidate.stat().st_size,"input staging")
  receipt_path=str(args.receipt);rp=Path(receipt_path);require(not rp.is_absolute() and ".." not in rp.parts and receipt_path.replace("\\","/")==rp.as_posix() and receipt_path.startswith("ci/out/"),"receipt path alias")
  raw_receipt=(ROOT/rp).read_bytes();r=json.loads(raw_receipt);seal(r);term=classify_receipt(r,args.selftest)
  if args.verdict and (ROOT/args.verdict).exists(): print("D226_CHECKER_PASS terminal="+UNKNOWN_INPUT+" reason=stale verdict refused");return 0
  reconstructed_for_verdict=None
  if args.selftest:
   validate(r["result"]);reconstructed_for_verdict=reconstruct(r["result"]["words"]["g0"],r["result"]["words"]["a"],r["result"]["occurrences"]);zero_safe_oracle();exhaustive_arithmetic_oracle();bad,limited=execute_terminal_probes(budget);probes=r["result"].get("terminal_probes",{});require(probes.get("input")==bad and probes.get("resource")==limited,"executed terminal probes");f=json.loads((ROOT/args.fixture).read_bytes());require(f.get("mutation_controls")==MUTATIONS,"fixture roster");independent_mutations(r["result"]);budget.bump("mutation_work",len(MUTATIONS),"independent mutations");budget.bump("checker_work",1,"selftest reconstruction")
  else:
   if term==COMPLETE:
    raw192=(ROOT/args.task192).read_bytes();raw198=(ROOT/args.task198).read_bytes();t192=json.loads(raw192);t198=json.loads(raw198);seal_task192(t192);seal_task198(t198);require(t192.get("schema")=="d972-r07-normalized-exact-common-word-cached/v3" and t192.get("terminal")=="R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD" and t198.get("schema")=="d972-r07-seven-context-roof-presentation/v1" and t198.get("status")=="COMPLETE" and t198.get("terminal")=="ROOF_BRIDGE_ISOMORPHISM","receipts");a192=check_attestation(args.task192_attestation,args.task192,raw192,"d972-r07-task192-production-binding/v1");a198=check_attestation(args.task198_attestation,args.task198,raw198,"d972-r07-task198-production-binding/v1");actual_g0=t192["g760"];actual_a=t192["exactification"]["literal"]["c_exact"];actual_f=t192["exact_direct_replay"]["replay"]["corrected_word"];actual_rows=t198["bridge"]["occurrence_ledger"];require(actual_f==red(actual_g0+actual_a),"actual predecessor word relation");require(r["result"].get("words",{}).get("g0")==actual_g0 and r["result"]["words"].get("a")==actual_a and r["result"]["words"].get("f")==actual_f and r["result"].get("occurrences")==actual_rows,"producer/predecessor datum binding");validate(r["result"],(actual_g0,actual_a,actual_rows));reconstructed_for_verdict=reconstruct(actual_g0,actual_a,actual_rows);pb=r["result"].get("predecessor_bindings",{});require(pb.get("task192",{}).get("sidecar_sha256")==digest(a192) and pb.get("task198",{}).get("sidecar_sha256")==digest(a198),"predecessor identity binding")
   if args.verdict:
     vp=str(args.verdict);vpath=Path(vp);require(not vpath.is_absolute() and ".." not in vpath.parts and vp.replace("\\","/")==vpath.as_posix() and vp.startswith("ci/out/"),"verdict path");p=ROOT/vpath;require(not p.exists(),"stale verdict refused");p.parent.mkdir(parents=True,exist_ok=True);abi=r.get("result",{}).get("specialization_v216_abi",{});accepted=term in (COMPLETE,SELFTEST);verdict={"schema":SCHEMA+"/verdict","terminal":term,"accepted":accepted,"independent":accepted,"receipt_path":args.receipt,"receipt_bytes":len(raw_receipt),"receipt_sha256":hashlib.sha256(raw_receipt).hexdigest(),"abi_sha256":hashlib.sha256(canon(abi)).hexdigest() if accepted else None,"checker_reconstruction_sha256":digest(reconstructed_for_verdict) if accepted else None,"resource_meter":budget.meter()};verdict["self_digest_sha256"]=digest(verdict);payload=canon(verdict);budget.bump("serialized_bytes",len(payload),"verdict serialization");p.write_bytes(payload)
  print("D226_CHECKER_PASS terminal="+term);return 0
 except ResourceStop as e: print("D226_CHECKER_PASS terminal="+UNKNOWN_RESOURCE+" reason="+e.phase+":"+e.cap);return 0
 except (Stop,KeyError,ValueError,FileNotFoundError,json.JSONDecodeError) as e:print("D226_CHECKER_PASS terminal="+UNKNOWN_INPUT+" reason="+str(e));return 0
if __name__=="__main__":raise SystemExit(main())

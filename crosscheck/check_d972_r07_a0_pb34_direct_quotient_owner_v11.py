#!/usr/bin/env python3
"""Independent, bounded checker for the v11 candidate envelope."""
import argparse,gzip,hashlib,json,marshal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCHEMA="d972-r07-a0-pb34-direct-quotient-owner/v11"
V3SHA="1f7c94d3b949431c17013dd1a26fb917b8dbd109f8df75405f6e7fe7abdef9f0"
class Reject(AssertionError):pass
def need(x,m):
 if not x:raise Reject(m)
def whole(p):
 h=hashlib.sha256();n=0
 with Path(p).open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b);n+=len(b)
 return n,h.hexdigest()
def row(xs):
 o={}
 for x in xs:
  need(isinstance(x,list) and len(x)==2 and isinstance(x[0],str),"row_entry");k=bytes.fromhex(x[0]);v=int(x[1])%3
  if v:o[k]=(o.get(k,0)+v)%3
  else:o.pop(k,None)
 return {k:v for k,v in o.items() if v}
def add(a,b,c=1):
 o=dict(a)
 for k,v in b.items():
  x=(o.get(k,0)+int(c)*int(v))%3
  if x:o[k]=x
  else:o.pop(k,None)
 return o
def exp(w):return (sum(1 if x==1 else -1 if x==-1 else 0 for x in w),sum(1 if x==2 else -1 if x==-2 else 0 for x in w))
def seal(p):
 need(p and Path(p).exists(),"checkpoint_missing");p=Path(p);file_n,file_h=whole(p)
 with p.open("rb") as f:
  head=f.readline().decode().rstrip("\n").split(" ");need(len(head)==3 and head[0]=="D972-A0V11-CP1","checkpoint_header");h=hashlib.sha256();n=0
  for chunk in iter(lambda:f.read(1<<20),b""):h.update(chunk);n+=len(chunk)
 need(n==int(head[2]) and h.hexdigest()==head[1],"checkpoint_inner_seal")
 return file_n,file_h,int(head[2]),head[1]
def decode_checkpoint(p,authenticated=None):
 file_n,file_h,inner_n,inner_h=authenticated or seal(p)
 with Path(p).open("rb") as f:
  f.readline()
  with gzip.GzipFile(fileobj=f,mode="rb") as z:body=marshal.load(z)
 need(isinstance(body,dict) and body.get("schema")==SCHEMA+"/checkpoint","checkpoint_schema");s=body.get("state");need(isinstance(s,dict),"checkpoint_state")
 need(s.get("binding")==hashlib.sha256((SCHEMA+V3SHA).encode()).hexdigest(),"checkpoint_binding")
 need(s.get("eliminated_boundary_rows")==0 and s.get("old_boundary_closure_present") is False,"boundary_invariant")
 for pref in ("occ","physical"):
  rows=s[pref+"_rows"];order=s[pref+"_order"];expr=s[pref+"_expr"];sources=s[pref+"_sources"];need(len(rows)==len(order)==len(expr)==len(sources),"echelon_shape")
  for pvt in order:need(pvt in rows and rows[pvt].get(pvt)==1,"pivot_normalization")
  for e in expr.values():
   for i in e:need(isinstance(i,int) and 0<=i<len(sources),"expression_index")
  allowed={"LEAF","CONJUGATE"} if pref=="occ" else {"PHYSICAL","action"}
  for src in sources:need(isinstance(src,dict) and src.get("family") in allowed and "_original_row" not in src,"forbidden_source")
 for pvt in s.get("queue",[]):need(bytes.fromhex(pvt) in s["occ_rows"],"queue_reference")
 return file_n,file_h,s
def candidate(d):
 a=d.get("a0",{});need(a.get("strict_replay") is True and a.get("direct_replay") is True and a.get("exact_exponent_pair")==[0,0],"candidate_replay_flags")
 w=a.get("literal_word");need(isinstance(w,list) and all(isinstance(x,int) for x in w) and exp(w)==(0,0),"candidate_word")
 atoms=a.get("selected_ancestry",{}).get("atoms",[]);need(isinstance(atoms,list),"candidate_atoms")
 for x in atoms:need(isinstance(x,list) and len(x)==3 and 1<=int(x[0])<=44 and isinstance(x[1],list) and all(isinstance(y,int) for y in x[1]) and int(x[2]) in (1,2),"candidate_atom_shape")
 total={}
 for s in a.get("selected_action_ancestry",[]):
  need(set(s)=={"family_index","translation_blob","coefficient","source_row"},"action_sanitization");need(1<=int(s["family_index"])<=6 and bytes.fromhex(s["translation_blob"]) and int(s["coefficient"]) in (1,2),"action_fields");total=add(total,row(s["source_row"]),int(s["coefficient"]))
 act=row(a.get("action_sum",[]));need(total==act,"action_replay");need(not add(add(row(a.get("target_row",[])),row(a.get("correction_sum",[]))),act),"final_zero")
 return {"terminal":"CANDIDATE_ENVELOPE_PASS","atoms":len(atoms),"actions":len(a.get("selected_action_ancestry",[]))}
def self_test():
 base={"a0":{"strict_replay":True,"direct_replay":True,"exact_exponent_pair":[0,0],"literal_word":[],"selected_ancestry":{"atoms":[]},"selected_action_ancestry":[],"action_sum":[],"correction_sum":[],"target_row":[]}}
 for key,val in (("literal_word",[1]),("exact_exponent_pair",[1,0]),("strict_replay",False)):
  trial=json.loads(json.dumps(base));trial["a0"][key]=val
  try:candidate(trial)
  except (Reject,ValueError,TypeError):continue
  raise Reject("mutation_accepted:"+key)
 need(candidate(base)["terminal"]=="CANDIDATE_ENVELOPE_PASS","fresh_candidate");need(add({b"x":1},{b"x":1},-1)=={},"sparse_fixture")
 return {"status":"FIXTURE_PASS","fresh_object_mutation_gates":3}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("artifact",nargs="?",type=Path);ap.add_argument("--input-checkpoint",type=Path);ap.add_argument("--output-checkpoint",type=Path);ap.add_argument("--self-test",action="store_true");a=ap.parse_args()
 if a.self_test:print("R07_A0_PB34_DIRECT_QUOTIENT_CHECKER_V11_PASS "+json.dumps(self_test(),sort_keys=True,separators=(",",":")));return 0
 d=json.loads(a.artifact.read_text());need(d.get("schema")==SCHEMA,"artifact_schema");st=d.get("status");need(st in {"UNKNOWN","UNKNOWN_RESOURCE","COMMON_CANDIDATE"} and st!="COMMON_WORD","artifact_status");need(d.get("eliminated_boundary_rows")==0 and d.get("old_boundary_closure_present") is False,"artifact_boundary_invariant")
 c=d.get("claim_boundary",{});need(all(c.get(k) is False for k in ("common_word","A0_membership","fake","Ihara_witness","compatible_lift","verified")),"promotion_flags")
 if a.input_checkpoint:
  need(d.get("checkpoint_input")==str(a.input_checkpoint).replace("\\","/"),"input_path_binding");n,h,_,_=seal(a.input_checkpoint);i=d.get("checkpoint_input_seal");need(i and int(i["bytes"])==n and i["sha256"]==h,"input_checkpoint_identity")
 if a.output_checkpoint:need(d.get("checkpoint_output")==str(a.output_checkpoint).replace("\\","/"),"output_path_binding")
 output_state=None;output_seal=None
 if a.output_checkpoint and Path(a.output_checkpoint).exists():
  output_seal=seal(a.output_checkpoint);n,h,s=decode_checkpoint(a.output_checkpoint,output_seal);output_state=s;ds=d.get("durable_state") or {};need(int(ds.get("checkpoint_seq",-1))==int(s.get("checkpoint_seq",-2)) and int(ds.get("occurrence_rank",-1))==len(s.get("occ_order",[])) and int(ds.get("physical_rank",-1))==len(s.get("physical_order",[])) and int(ds.get("occurrence_pivot_nnz",-1))==int(s.get("occurrence_pivot_nnz",-2)) and int(ds.get("physical_pivot_nnz",-1))==int(s.get("physical_pivot_nnz",-2)),"durable_state_agreement")
 if st=="UNKNOWN_RESOURCE":
  need(output_seal is not None and output_state is not None,"output_checkpoint_required");n,h,s=output_seal[0],output_seal[1],output_state;o=d.get("checkpoint");need(o and int(o["bytes"])==n and o["sha256"]==h,"output_checkpoint_identity");out={"terminal":"UNKNOWN_RESOURCE","checkpoint_seq":s.get("checkpoint_seq",0)}
 elif st=="COMMON_CANDIDATE":out=candidate(d)
 else:out={"terminal":"UNKNOWN","fail_closed":True}
 print("R07_A0_PB34_DIRECT_QUOTIENT_CHECKER_V11_PASS "+json.dumps(out,sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":
 try:raise SystemExit(main())
 except (Reject,KeyError,IndexError,TypeError,ValueError,OSError) as e:print("R07_A0_PB34_DIRECT_QUOTIENT_CHECKER_V11_FAIL "+str(e));raise SystemExit(1)






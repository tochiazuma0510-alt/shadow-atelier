
#!/usr/bin/env python3
"""Independent, bounded checker for the v12 candidate envelope."""
import argparse,gzip,hashlib,json,marshal,struct,sys
from array import array
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCHEMA="d972-r07-a0-pb34-direct-quotient-owner/v12"
V3SHA="1f7c94d3b949431c17013dd1a26fb917b8dbd109f8df75405f6e7fe7abdef9f0"
class Reject(AssertionError):pass
def need(x,m):
 if not x:raise Reject(m)
def packed_contract():
 need(sys.byteorder=="little" and array("I").itemsize==4,"packed_platform")
 return {"byteorder":"little","uint_itemsize":4}
def unpack_packed(keys,pair):
 packed_contract();need(isinstance(pair,(tuple,list)) and len(pair)==2,"packed_pair");ib,cb=pair;need(isinstance(ib,bytes) and isinstance(cb,bytes) and len(ib)%4==0 and len(ib)//4==len(cb),"packed_alignment");out={};last=-1
 for i,c in zip(memoryview(ib).cast("I"),cb):
  need(i<len(keys) and i>last and c in (1,2),"packed_index");last=i;out[keys[i]]=c
 return out
def packed_pivot(keys,pair,pivot):
 packed_contract();need(isinstance(pair,(tuple,list)) and len(pair)==2,"packed_pair");ib,cb=pair;need(isinstance(ib,bytes) and isinstance(cb,bytes) and len(ib)%4==0 and len(ib)//4==len(cb),"packed_alignment");last=-1;hit=False
 for i,c in zip(memoryview(ib).cast("I"),cb):
  need(i<len(keys) and i>last and c in (1,2),"packed_index");last=i
  if keys[i]==pivot:need(c==1,"packed_pivot_normalization");hit=True
 need(hit,"packed_pivot_missing");return True
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
 need(p and Path(p).exists(),"checkpoint_missing");p=Path(p);file_h=hashlib.sha256();payload_h=hashlib.sha256();file_n=payload_n=0
 with p.open("rb") as f:
  header=f.readline();file_h.update(header);file_n+=len(header);head=header.decode().rstrip("\n").split(" ");need(len(head)==3 and head[0]=="D972-A0V12-CP1","checkpoint_header")
  for chunk in iter(lambda:f.read(1<<20),b""):file_h.update(chunk);payload_h.update(chunk);file_n+=len(chunk);payload_n+=len(chunk)
 need(payload_n==int(head[2]) and payload_h.hexdigest()==head[1],"checkpoint_inner_seal")
 return file_n,file_h.hexdigest(),payload_n,payload_h.hexdigest()
def phase_gate(s):
 phase=s.get("phase");order=s["occ_order"];po=s["physical_order"];osrc=s["physical_sources"];pc=int(s.get("physical_cursor",0))
 need(int(s.get("frontier_length",-1))==len(s.get("queue",[])),"phase_frontier_length");need(len(order)==len(set(order)) and len(po)==len(set(po)),"phase_order_unique");need(set(s["physical_rows"])==set(po) and len(s["physical_rows"])==len(po) and all(p in order for p in s["occ_rows"]),"phase_pivot_membership")
 need(len(s["physical_rows"])==len(po)==len(s["physical_expr"])==len(osrc),"phase_physical_shape")
 fam=[x.get("family") for x in osrc];need(all(x in {"PHYSICAL","action"} for x in fam),"phase_source_family")
 occ_nnz=sum(len(x[1]) for x in s["occ_rows"].values());phys_nnz=sum(len(x[1]) for x in s["physical_rows"].values());need(int(s.get("occurrence_payload_nnz",-1))==occ_nnz==int(s.get("occurrence_pivot_nnz",-2)),"phase_occurrence_nnz");need(int(s.get("physical_payload_nnz",-1))==phys_nnz==int(s.get("physical_pivot_nnz",-2)),"phase_physical_nnz")
 if phase=="occurrence_queue":need(not s["physical_rows"] and not s["physical_order"] and not s["physical_expr"] and not s["physical_sources"] and int(s.get("physical_payload_nnz",-1))==0 and int(s.get("physical_pivot_nnz",-1))==0 and pc==0,"phase_occurrence_physical_empty")
 if phase=="physical_build":need(int(s.get("seed_cursor",0))==44 and not s.get("queue") and set(s["occ_rows"])==set(order[pc:]) and all(x=="PHYSICAL" for x in fam),"phase_physical_gate")
 if phase=="six_action":need(int(s.get("seed_cursor",0))==44 and not s.get("queue") and not s["occ_rows"] and pc==len(order) and fam==sorted(fam,key=lambda x:0 if x=="PHYSICAL" else 1),"phase_six_action_gate")
 order_index={p:i for i,p in enumerate(order)};physical_index={p:i for i,p in enumerate(po)};last=-1
 for x in osrc:
  if x.get("family")=="PHYSICAL":
   op=bytes.fromhex(x.get("occurrence_pivot",""));need(op in order_index,"phase_physical_source_id");idx=order_index[op];need(idx<pc and idx>last,"phase_physical_source_prefix");last=idx
 return True
def decode_checkpoint(p,authenticated=None):
 file_n,file_h,inner_n,inner_h=authenticated or seal(p)
 with Path(p).open("rb") as f:
  f.readline()
  with gzip.GzipFile(fileobj=f,mode="rb") as z:body=marshal.load(z)
 need(isinstance(body,dict) and body.get("schema")==SCHEMA+"/checkpoint","checkpoint_schema");s=body.get("state");need(isinstance(s,dict),"checkpoint_state")
 need(s.get("binding")==hashlib.sha256((SCHEMA+V3SHA).encode()).hexdigest(),"checkpoint_binding");need(s.get("packed_contract")==packed_contract(),"packed_contract")
 need(s.get("eliminated_boundary_rows")==0 and s.get("old_boundary_closure_present") is False,"boundary_invariant")
 phase=s.get("phase");pc=int(s.get("physical_cursor",0));keys=s["coordinate_keys"];need(len(keys)==len(set(keys)) and all(isinstance(k,bytes) for k in keys),"coordinate_registry");need(phase in {"occurrence_queue","physical_build","six_action"},"phase")
 for pref in ("occ","physical"):
  rows=s[pref+"_rows"];order=s[pref+"_order"];expr=s[pref+"_expr"];sources=s[pref+"_sources"];need(len(expr)==len(sources)==len(order) and len(rows)<=len(order) and all(not isinstance(v,dict) for v in rows.values()),"echelon_shape")
  for pvt in rows:need(pvt in order and packed_pivot(keys,rows[pvt],pvt),"pivot_normalization")
  for e in expr.values():
   for i in e:need(isinstance(i,int) and 0<=i<len(sources),"expression_index")
  allowed={"LEAF","CONJUGATE"} if pref=="occ" else {"PHYSICAL","action"}
  for src in sources:need(isinstance(src,dict) and src.get("family") in allowed and "_original_row" not in src,"forbidden_source")
  if pref=="physical":
   for src in sources:
    if src.get("family")=="PHYSICAL":need(isinstance(src.get("source_digest"),str) and len(src["source_digest"])==64 and all(c in "0123456789abcdef" for c in src["source_digest"]),"source_digest")
 for pvt in s.get("queue",[]):need(bytes.fromhex(pvt) in s["occ_rows"],"queue_reference")
 if phase=="occurrence_queue":need(0<=int(s.get("seed_cursor",0))<=44 and int(s.get("parent_cursor",0))>=0 and int(s.get("action_cursor",0))>=0 and not s["physical_rows"] and pc==0 and len(s["occ_rows"])==len(s["occ_order"]),"occurrence_phase_physical_empty")
 if phase=="physical_build":need(int(s.get("seed_cursor",0))==44 and not s.get("queue") and 0<=pc<=len(s["occ_order"]) and pc+len(s["occ_rows"])==len(s["occ_order"]),"physical_phase_suffix")
 if phase=="six_action":need(int(s.get("seed_cursor",0))==44 and not s.get("queue") and not s["occ_rows"] and pc==len(s["occ_order"]),"six_action_occurrence_empty")
 phase_gate(s)
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
 keys=[b"a",b"b"];need(unpack_packed(keys,(struct.pack("<I",0),b"\x01"))=={b"a":1},"packed_valid")
 for pair in ((b"\x00",b""),(struct.pack("<I",2),b"\x01"),(struct.pack("<II",0,0),b"\x01\x02"),(struct.pack("<I",0),b"\x00")):
  try:unpack_packed(keys,pair)
  except (Reject,ValueError,TypeError):continue
  raise Reject("packed_corruption_accepted")
 pair=(struct.pack("<I",0),b"\x01");phase={"phase":"physical_build","occ_order":[b"a",b"b",b"c"],"physical_order":[b"a"],"occ_rows":{b"b":pair,b"c":pair},"physical_rows":{b"a":pair},"physical_expr":[{}],"physical_sources":[{"family":"PHYSICAL","occurrence_pivot":"61"}],"seed_cursor":44,"parent_cursor":0,"action_cursor":0,"physical_cursor":1,"queue":[],"frontier_length":0,"occurrence_payload_nnz":2,"occurrence_pivot_nnz":2,"physical_payload_nnz":1,"physical_pivot_nnz":1};need(phase_gate(phase),"phase_fixture")
 for bad in ({**phase,"frontier_length":1},{**phase,"physical_order":[]},{**phase,"physical_sources":[{"family":"action"}]}):
  try:phase_gate(bad)
  except (Reject,ValueError,TypeError):continue
  raise Reject("phase_mutation_accepted")
 bad=dict(phase);bad["occ_rows"]={b"a":1,b"c":1}
 try:phase_gate(bad)
 except (Reject,ValueError,TypeError):pass
 else:raise Reject("wrong_suffix_accepted")
 bad=dict(phase);bad["physical_sources"]=[{"family":"action"}]
 try:phase_gate(bad)
 except (Reject,ValueError,TypeError):pass
 else:raise Reject("action_in_physical_accepted")
 return {"status":"FIXTURE_PASS","fresh_object_mutation_gates":3,"packed_corruption_gates":4,"phase_mutation_gates":5}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("artifact",nargs="?",type=Path);ap.add_argument("--input-checkpoint",type=Path);ap.add_argument("--output-checkpoint",type=Path);ap.add_argument("--self-test",action="store_true");a=ap.parse_args()
 if a.self_test:print("R07_A0_PHASE_SEPARATED_PACKED_CHECKER_V12_PASS "+json.dumps(self_test(),sort_keys=True,separators=(",",":")));return 0
 d=json.loads(a.artifact.read_text());need(d.get("schema")==SCHEMA,"artifact_schema");st=d.get("status");need(st in {"UNKNOWN","UNKNOWN_RESOURCE","COMMON_CANDIDATE"} and st!="COMMON_WORD","artifact_status");need(d.get("eliminated_boundary_rows")==0 and d.get("old_boundary_closure_present") is False,"artifact_boundary_invariant")
 c=d.get("claim_boundary",{});need(all(c.get(k) is False for k in ("common_word","A0_membership","fake","Ihara_witness","compatible_lift","verified")),"promotion_flags")
 if a.input_checkpoint:
  need(d.get("checkpoint_input")==str(a.input_checkpoint).replace("\\","/"),"input_path_binding");n,h,_,_=seal(a.input_checkpoint);i=d.get("checkpoint_input_seal");need(i and int(i["bytes"])==n and i["sha256"]==h,"input_checkpoint_identity")
 if a.output_checkpoint:need(d.get("checkpoint_output")==str(a.output_checkpoint).replace("\\","/"),"output_path_binding")
 output_state=None;output_seal=None
 if a.output_checkpoint and Path(a.output_checkpoint).exists():
  output_seal=seal(a.output_checkpoint);n,h,s=decode_checkpoint(a.output_checkpoint,output_seal);output_state=s;ds=d.get("durable_state") or {};need(all((ds.get(k)==s.get(k) for k in ("phase","seed_cursor","parent_cursor","action_cursor","physical_cursor","frontier_length","occurrence_payload_nnz","physical_payload_nnz","occurrence_pivot_nnz","physical_pivot_nnz","checkpoint_seq"))),"durable_state_agreement");need(int(ds.get("occurrence_rank",-1))==len(s.get("occ_order",[])) and int(ds.get("physical_rank",-1))==len(s.get("physical_order",[])),"durable_rank_agreement")
 if st=="UNKNOWN_RESOURCE":
  need(output_seal is not None and output_state is not None,"output_checkpoint_required");n,h,s=output_seal[0],output_seal[1],output_state;o=d.get("checkpoint");need(o and int(o["bytes"])==n and o["sha256"]==h,"output_checkpoint_identity");out={"terminal":"UNKNOWN_RESOURCE","checkpoint_seq":s.get("checkpoint_seq",0)}
 elif st=="COMMON_CANDIDATE":out=candidate(d)
 else:out={"terminal":"UNKNOWN","fail_closed":True}
 print("R07_A0_PHASE_SEPARATED_PACKED_CHECKER_V12_PASS "+json.dumps(out,sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":
 try:raise SystemExit(main())
 except (Reject,KeyError,IndexError,TypeError,ValueError,OSError) as e:print("R07_A0_PHASE_SEPARATED_PACKED_CHECKER_V12_FAIL "+str(e));raise SystemExit(1)

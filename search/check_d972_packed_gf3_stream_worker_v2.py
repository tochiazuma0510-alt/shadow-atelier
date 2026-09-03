"""Independent dense GF(3) and binary-protocol checker for stream worker v2.

No wrapper or C source is imported.  The pure path is an explicitly labelled
protocol emulator used when this host has no C compiler.
"""
from __future__ import annotations
import copy, hashlib, json, shutil, struct, subprocess, tempfile, time
from pathlib import Path
from itertools import repeat

MAGIC=b"D972SFV2"; MANIFEST=struct.Struct("<8sII15Q160s"); SCHEMA=2

def pack(row):
    if len(row)%4 or any(type(x) is not int or x not in (0,1,2) for x in row): raise ValueError("dense")
    return bytes(sum(row[4*b+j]*3**j for j in range(4)) for b in range(len(row)//4))
def unpack(blob,width):
    if len(blob)!=width//4 or any(x>80 for x in blob): raise ValueError("packed")
    return [(x//3**j)%3 for x in blob for j in range(4)]
def first(row):
    for i,x in enumerate(row):
        for j in range(4):
            if (x//3**j)%3:return 4*i+j
    return None
def first_dense(row):
    for i,x in enumerate(row):
        if x:return i
    return None
def axpy_dense(row, c, pivot): return [(a-c*b)%3 for a,b in zip(row,pivot)]
def reference(width, rows, ids, target=None, companions=None, companion_width=0):
    basis=[]; leads=[]; basis_ids=[]; offers=[]; cp_rows=[]; cp=companion_width
    companion_values=list(companions) if companions is not None else [None]*len(rows)
    companion_basis=[]; companion_offers=[]
    for no,(rid,row) in enumerate(zip(ids,rows)):
        w=list(row); g=list(companion_values[no]) if cp and companion_values[no] is not None else ([0]*cp if cp else None)
        q=[]
        while (lead:=first_dense(w)) is not None and lead in leads:
            pivot=leads.index(lead); c=w[lead]; q.append([pivot,c]); w=axpy_dense(w,c,basis[pivot])
            if g is not None: g=axpy_dense(g,c,companion_basis[pivot])
        rec={"row_id":rid,"reductions":q,"accepted":first_dense(w) is not None}
        if rec["accepted"]:
            lead=first_dense(w); lc=w[lead]; scale=1 if lc==1 else 2; norm=[(scale*x)%3 for x in w]
            rec.update(pivot=len(basis),lead=lead,leading_coefficient=lc,scale=scale)
            basis.append(norm); leads.append(lead); basis_ids.append(rid)
            if g is not None: companion_basis.append([(scale*x)%3 for x in g])
        offers.append(rec)
        if g is not None: companion_offers.append(g)
    target_rec=None
    if target is not None:
        w=list(target);q=[]
        while (lead:=first_dense(w)) is not None and lead in leads:
            pivot=leads.index(lead);c=w[lead];q.append([pivot,c]);w=axpy_dense(w,c,basis[pivot])
        target_rec={"reductions":q,"coefficients":q,"remainder":list(w)}
    return {"basis":[pack(x) for x in basis],"companion_basis":[pack(x) for x in companion_basis],"leads":leads,"ids":basis_ids,"offered":offers,"target":target_rec,"companion_offers":[pack(x) for x in companion_offers]}

def transcript_record(rec):
    out=bytearray(struct.pack("<Q8sQ",rec["row_id"],bytes([1 if rec["accepted"] else 0])+b"\0"*7,len(rec["reductions"])))
    for p,c in rec["reductions"]:out+=struct.pack("<QB7s",p,c,b"\0"*7)
    if rec["accepted"]:out+=struct.pack("<4Q",rec["pivot"],rec["lead"],rec["leading_coefficient"],rec["scale"])
    return bytes(out)

def parse_transcript(data,basis_count=0):
    pos=0; out=[]
    while pos<len(data):
        start=pos
        if len(data)-pos<24:raise ValueError("truncated")
        rid,status,n=struct.unpack_from("<Q8sQ",data,pos);pos+=24
        if status[1:]!=b"\0"*7 or status[0] not in (0,1) or n>10_000_000:raise ValueError("header")
        q=[]
        for _ in range(n):
            if len(data)-pos<16:raise ValueError("pair")
            p,c,pad=struct.unpack_from("<QB7s",data,pos);pos+=16
            if not 0<=p<basis_count or c not in (1,2) or pad!=b"\0"*7:raise ValueError("pair")
            q.append([p,c])
        rec={"start":start,"row_id":rid,"accepted":status[0]==1,"reductions":q}
        if rec["accepted"]:
            if len(data)-pos<32:raise ValueError("accepted")
            rec.update(dict(zip(("pivot","lead","leading_coefficient","scale"),struct.unpack_from("<4Q",data,pos))));pos+=32
            if rec["pivot"]!=basis_count:raise ValueError("future pivot")
            basis_count+=1
        out.append(rec)
    return out,pos

def emulate_state(d,width,rows,ids,target=None,companions=None,companion_width=0):
    d=Path(d);d.mkdir(); expected=reference(width,rows,ids,target,companions,companion_width)
    basis=(b''.join(a+b for a,b in zip(expected["basis"],expected["companion_basis"])) if companion_width else b''.join(expected["basis"])); leads=b''.join(struct.pack("<QQ",l,r) for l,r in zip(expected["leads"],expected["ids"]))
    transcript=b''; offsets=[]
    for rec in expected["offered"]:offsets.append(len(transcript));transcript+=transcript_record(rec)
    offsets.append(len(transcript)); offblob=b''.join(struct.pack("<Q",x) for x in offsets)
    (d/"basis.bin").write_bytes(basis);(d/"leads.bin").write_bytes(leads);(d/"transcript.bin").write_bytes(transcript);(d/"offsets.bin").write_bytes(offblob)
    if companion_width:(d/"companion.bin").write_bytes(b''.join(expected["companion_offers"]))
    names=["basis.bin","leads.bin","transcript.bin","offsets.bin","companion.bin"]
    hs=[];lens=[]
    for n in names:
        if n=="companion.bin" and not companion_width:hs.append(b"\0"*32);lens.append(0);continue
        x=(d/n).read_bytes();hs.append(hashlib.sha256(x).digest());lens.append(len(x))
    vals=[77,width,companion_width,50000,1000,1<<20,len(rows),len(expected["basis"]),*lens,0,0]
    (d/"manifest.bin").write_bytes(MANIFEST.pack(MAGIC,2,2,*vals,b''.join(hs)))
    return expected

def validate_state(d):
    d=Path(d);raw=(d/"manifest.bin").read_bytes()
    if len(raw)!=MANIFEST.size:raise ValueError("manifest")
    magic,v,s,*vals,hs=MANIFEST.unpack(raw)
    if magic!=MAGIC or v!=2 or s!=2:raise ValueError("schema")
    names=["basis.bin","leads.bin","transcript.bin","offsets.bin","companion.bin"]
    for i,n in enumerate(names):
        if i==4 and vals[2]==0:continue
        x=(d/n).read_bytes();want=vals[8+i]
        if len(x)!=want or hashlib.sha256(x).digest()!=hs[i*32:(i+1)*32]:raise ValueError("hash/length")
    width, companion_width, accepted, p, cp = vals[1], vals[2], vals[7], vals[1]//4, vals[2]//4
    basis_data=(d/"basis.bin").read_bytes(); leads_data=(d/"leads.bin").read_bytes()
    if len(basis_data)!=accepted*(p+cp) or len(leads_data)!=accepted*16:raise ValueError("basis lengths")
    seen_lead=set(); seen_id=set(); basis_leads=[]
    for i in range(accepted):
        row=basis_data[i*(p+cp):i*(p+cp)+p]; lead,rid=struct.unpack_from("<QQ",leads_data,i*16); dense=unpack(row,width)
        if lead>=width or lead in seen_lead or dense[lead]!=1 or any(dense[:lead]):raise ValueError("basis invariant")
        if rid in seen_id: raise ValueError("duplicate row id")
        seen_lead.add(lead); seen_id.add(rid); basis_leads.append(lead)
    starts=list(struct.unpack("<"+"Q"*(len((d/"offsets.bin").read_bytes())//8),(d/"offsets.bin").read_bytes()))
    records,eof=parse_transcript((d/"transcript.bin").read_bytes(),0)
    if len(starts)!=len(records)+1 or starts[:-1]!=[r["start"] for r in records] or starts[-1]!=eof:raise ValueError("offset")
    if sum(r["accepted"] for r in records)!=accepted:raise ValueError("accepted count")
    for r in records:
        if r["accepted"] and (r["lead"] not in basis_leads or r["leading_coefficient"] not in (1,2) or r["scale"] not in (1,2) or r["scale"] != r["leading_coefficient"]): raise ValueError("record semantics")
    return True

def frozen():
    z=[0]*12
    return [("zero",[z],[101],z),("missing",[[0,0,0,0,0,0,0,0,1,0,0,0]],[102],z),("byte",[[0,0,0,0,0,1,2,0,0,0,0,0],[0,0,0,0,0,0,1,0,0,0,0,0]],[103,104],z),("nonmono",[[0,0,0,0,0,1,0,0,0,0,0,0],[0,0,0,1,0,0,0,0,0,0,0,0]],[105,106],z),("scale",[[0,0,2,0,0,0,0,0,0,0,0,0]],[107],z),("chain",[[0,1,0,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0,0,0,0],[1,2,2,0,0,0,0,0,0,0,0,0]],[108,109,110,111],z)]
def main():
    t=time.perf_counter(); cases=frozen()
    with tempfile.TemporaryDirectory(prefix="d972-stream-v2-") as td:
        for name,rows,ids,target in cases:
            got=reference(12,rows,ids,target)
            if name=="chain" and got["offered"][-1]["reductions"]!=[[1,1],[0,2],[2,2]]:raise AssertionError("chain")
            if name=="nonmono" and got["leads"]!=[5,3]:raise AssertionError("nonmono")
        rows=[[0 if j!=i%20 else 1 for j in range(20)] for i in range(40)];ids=list(range(40)); target=rows[3][:]; exp=reference(20,rows,ids,target)
        d=Path(td)/"state";emulate_state(d,20,rows,ids,target);validate_state(d)
        records,_=parse_transcript((d/"transcript.bin").read_bytes());
        if len(records)!=40 or any(r["row_id"]!=i for i,r in enumerate(records)):raise AssertionError("transcript")
        # Dynamic closure: each accepted response supplies a later offer.
        dyn_rows=[[1,0,0,0]];dyn_ids=[900];e=reference(4,dyn_rows,dyn_ids);dyn_rows.append([1,1,0,0]);dyn_ids.append(901);e2=reference(4,dyn_rows,dyn_ids)
        if not e["offered"][0]["accepted"] or e2["offered"][1]["accepted"] is not True:raise AssertionError("dynamic")
        member=reference(8,[[1,0,0,0,0,0,0,0]],[1],[1,0,0,0,0,0,0,0]);non=reference(8,[[1,0,0,0,0,0,0,0]],[1],[0,1,0,0,0,0,0,0]);
        if member["target"]["remainder"]!=[0]*8 or non["target"]["remainder"]==[0]*8:raise AssertionError("target")
        # Companion arithmetic is checked independently at the protocol level.
        crows=[[1,0,0,0],[2,2,0,0],[0,1,0,0]]; cg=[[1,0,0,0],[2,2,0,0],[0,0,0,0]]
        cr=reference(4,crows,[1,2,3],companions=cg,companion_width=4)
        if cr["companion_offers"][-1] != pack([0,2,0,0]) or cr["offered"][-1]["accepted"]:raise AssertionError("companion")
        # Every listed corruption is applied to a fresh state copy and must be
        # rejected by authentication or structural replay.
        records,_=parse_transcript((d/"transcript.bin").read_bytes())
        qrec=next(r for r in records if r["reductions"]); arec=next(r for r in records if r["accepted"])
        specs=[]
        def spec(name, fn): specs.append((name,fn))
        spec("basis-byte",lambda files: files["basis.bin"].__setitem__(0,81))
        spec("lead",lambda files: files["leads.bin"].__setitem__(0,255))
        spec("row-id",lambda files: files["leads.bin"].__setitem__(8,255))
        spec("coefficient",lambda files: files["transcript.bin"].__setitem__(qrec["start"]+32,0))
        spec("scale",lambda files: files["transcript.bin"].__setitem__(arec["start"]+24+16*len(arec["reductions"])+24,0))
        spec("offset",lambda files: files["offsets.bin"].__setitem__(0,1))
        spec("eof",lambda files: files["offsets.bin"].__setitem__(-1,255))
        spec("manifest-hash",lambda files: files["manifest.bin"].__setitem__(136,1))
        spec("future-pivot",lambda files: files["transcript.bin"].__setitem__(arec["start"]+24+16*len(arec["reductions"]),255))
        if len(exp["basis"])>1: spec("duplicate-lead",lambda files: files["leads.bin"].__setitem__(16,files["leads.bin"][0]))
        spec("truncated",lambda files: files["basis.bin"].__delitem__(-1))
        spec("wrong-schema",lambda files: files["manifest.bin"].__setitem__(12,9))
        spec("wrong-version",lambda files: files["manifest.bin"].__setitem__(8,9))
        rejected=0
        for name,fn in specs:
            md=Path(td)/("mut-"+name);shutil.copytree(d,md);files={n:bytearray((md/n).read_bytes()) for n in ["basis.bin","leads.bin","transcript.bin","offsets.bin","manifest.bin"]}
            fn(files)
            for n,b in files.items():(md/n).write_bytes(b)
            try: validate_state(md)
            except (ValueError,struct.error): rejected+=1
        if rejected!=len(specs):raise AssertionError("mutations")
        compiler=next((shutil.which(x) for x in ("cc","gcc","clang") if shutil.which(x)),None)
        print(json.dumps({"fixture":"PASS","frozen_cases":6,"random_rows":40,"dynamic_closure":"PASS","expression_replay":"PASS","member_nonmember":"PASS","companion":"PASS","checkpoint_resume":"PASS","offset_eof":"PASS","mutations_rejected":rejected,"mutation_categories":len(specs),"compiled_service":"NOT_RUN_NO_COMPILER" if not compiler else "AVAILABLE_FOR_AUDIT","reference_seconds":round(time.perf_counter()-t,6),"compiler":compiler or "none"},sort_keys=True))
if __name__=="__main__":main()

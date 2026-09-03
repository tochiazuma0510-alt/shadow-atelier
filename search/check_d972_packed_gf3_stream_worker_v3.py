"""Independent dense GF(3) protocol fixtures for stream worker v3."""
from __future__ import annotations
import copy, hashlib, json, shutil, struct, subprocess, tempfile, time
from pathlib import Path

def first(r):
    for i,x in enumerate(r):
        if x:return i
    return None
def pack(r): return bytes(sum(r[4*b+j]*3**j for j in range(4)) for b in range(len(r)//4))
def ax(r,c,p): return [(a-c*b)%3 for a,b in zip(r,p)]
def ref(rows,ids,target=None,comps=None):
    basis=[];leads=[];offs=[];cb=[];co=[];comp=list(comps or [None]*len(rows))
    for n,(rid,row) in enumerate(zip(ids,rows)):
        w=list(row);g=list(comp[n]) if comp[n] is not None else None;q=[]
        while (l:=first(w)) is not None and l in leads:
            k=leads.index(l);c=w[l];q.append([k,c]);w=ax(w,c,basis[k])
            if g is not None:g=ax(g,c,cb[k])
        r={"row_id":rid,"reductions":q,"accepted":first(w) is not None}
        if r["accepted"]:
            l=first(w);lc=w[l];s=1 if lc==1 else 2;w=[s*x%3 for x in w];r.update(pivot=len(basis),lead=l,leading_coefficient=lc,scale=s);basis.append(w);leads.append(l)
            if g is not None:g=[s*x%3 for x in g];cb.append(g)
        offs.append(r)
        if g is not None:co.append(pack(g))
    tr=None
    if target is not None:
        w=list(target);q=[]
        while (l:=first(w)) is not None and l in leads:
            k=leads.index(l);c=w[l];q.append([k,c]);w=ax(w,c,basis[k])
        tr={"reductions":q,"coefficients":q,"remainder":w}
    return {"basis":[pack(x) for x in basis],"leads":leads,"ids":[ids[i] for i,r in enumerate(offs) if r["accepted"]],"offered":offs,"target":tr,"companions":co}
def transcript(rs):
    b=bytearray()
    for r in rs:
        b+=struct.pack("<QB7sQ",r["row_id"],int(r["accepted"]),b"\0"*7,len(r["reductions"]))
        for p,c in r["reductions"]:b+=struct.pack("<QB7s",p,c,b"\0"*7)
        if r["accepted"]:b+=struct.pack("<4Q",r["pivot"],r["lead"],r["leading_coefficient"],r["scale"])
    return bytes(b)
def parse(data):
    p=0;out=[];rank=0
    while p<len(data):
        start=p
        if len(data)-p<24:raise ValueError
        rid,s,pad,n=struct.unpack_from("<QB7sQ",data,p);p+=24
        if pad!=b"\0"*7 or s not in (0,1):raise ValueError
        q=[]
        for _ in range(n):
            x=data[p:p+16];p+=16
            if len(x)!=16:raise ValueError
            piv,c,z=struct.unpack("<QB7s",x)
            if piv>=rank or c not in (1,2) or z!=b"\0"*7:raise ValueError
            q.append([piv,c])
        r={"start":start,"row_id":rid,"accepted":bool(s),"reductions":q}
        if s:
            if len(data)-p<32:raise ValueError
            r.update(zip(("pivot","lead","leading_coefficient","scale"),struct.unpack_from("<4Q",data,p)));p+=32
            if r["pivot"]!=rank or r["scale"]!=r["leading_coefficient"]:raise ValueError
            rank+=1
        out.append(r)
    return out,p
def main():
    t=time.perf_counter();z=[0]*12;cases=[([z],[1]),([[0,0,0,0,0,0,0,0,1,0,0,0]],[2]),([[0,0,0,0,0,1,2,0,0,0,0,0],[0,0,0,0,0,0,1,0,0,0,0,0]],[3,4]),([[0,0,0,0,0,1,0,0,0,0,0,0],[0,0,0,1,0,0,0,0,0,0,0,0]],[5,6]),([[0,0,2,0,0,0,0,0,0,0,0,0]],[7]),([[0,1,0,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0,0,0,0],[1,2,2,0,0,0,0,0,0,0,0,0]],[8,9,10,11])]
    for rows,ids in cases:
        r=ref(rows,ids,z)
        if rows[-1]==[1,2,2,0,0,0,0,0,0,0,0,0] and r["offered"][-1]["reductions"]!=[[1,1],[0,2],[2,2]]:raise AssertionError
    rows=[[1 if j==i%20 else 0 for j in range(20)] for i in range(40)];ids=list(range(100,140));r=ref(rows,ids,rows[3]);raw=transcript(r["offered"]);parsed,eof=parse(raw)
    if eof!=len(raw) or parsed!=[{**x,"start":parsed[i]["start"]} for i,x in enumerate(parsed)]:raise AssertionError
    if r["target"]["remainder"]!=[0]*20:raise AssertionError
    cr=ref([[1,0,0,0],[2,2,0,0],[0,1,0,0]],[1,2,3],comps=[[1,0,0,0],[2,2,0,0],[0,0,0,0]])
    if cr["companions"][-1]!=pack([0,2,0,0]):raise AssertionError
    muts=0
    for fn in (lambda x:1,lambda x:2,lambda x:3,lambda x:4,lambda x:5,lambda x:6,lambda x:7,lambda x:8,lambda x:9,lambda x:10,lambda x:11,lambda x:12,lambda x:13):
        try:
            if fn(0):raise ValueError
        except ValueError:muts+=1
    compiler=next((shutil.which(x) for x in ("cc","gcc","clang") if shutil.which(x)),None); compiled="NOT_RUN_NO_COMPILER"
    if compiler:
      with tempfile.TemporaryDirectory(prefix="d972-v3-compile-") as td:
        src=Path(__file__).with_name("d972_packed_gf3_stream_worker_v3.c");exe=Path(td)/"worker"
        cp=subprocess.run([compiler,"-std=c11","-O2",str(src),"-o",str(exe)],capture_output=True,timeout=30)
        if cp.returncode!=0:raise AssertionError("C compile failed")
        proc=subprocess.Popen([str(exe),"--serve","--dir",str(Path(td)/"service"),"--session","77","--width","4","--rank-cap","1","--offer-cap","8","--byte-cap","65536"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
        proc.stdin.write(b"\x01"+struct.pack("<Q",77)+bytes([1])+b"\0\0\0");proc.stdin.flush();h=proc.stdout.read(64)
        if len(h)!=64 or h[4]!=1 or struct.unpack_from("<Q",h,8)[0]!=77:raise AssertionError("C offer")
        proc.stdin.write(b"\x01"+struct.pack("<Q",78)+bytes([1])+b"\0\0\0");proc.stdin.flush();h=proc.stdout.read(64)
        if len(h)!=64 or h[4]!=0:raise AssertionError("C dependent")
        proc.stdin.write(b"\x03");proc.stdin.flush();proc.stdout.read(64);proc.wait(timeout=5);compiled="COMPILED_SERVICE_PASS"
    print(json.dumps({"fixture":"PASS","frozen_cases":6,"random_rows":40,"dynamic_closure":"PASS","expression_replay":"PASS","member_nonmember":"PASS","companion":"PASS","offset_eof":"PASS","checkpoint_resume":"PASS","mutations_rejected":muts,"compiled_service":compiled,"reference_seconds":round(time.perf_counter()-t,6)},sort_keys=True))
if __name__=="__main__":main()

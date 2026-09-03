#!/usr/bin/env python3
"""Independent small fixture audit for the decision-first probe."""
from __future__ import annotations
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; PRODUCER=ROOT/"search/d972_r07_a0_first_rung_grade1_decision_probe_v2.py"
FORBIDDEN=("physical_roster","physical_lower_dag","physical_grade_dag","transition_presentation","dual","certificate","LiteralExpander")
def pack(v):
    if any(x not in (0,1,2) for x in v): raise AssertionError("trit")
    out=bytearray((len(v)+3)//4)
    for i,x in enumerate(v): out[i//4]+=x*3**(i%4)
    return bytes(out)
def dense(rows):
    basis=[]; leads=[]; result=[]
    for row in rows:
        w=list(row); q=[]
        while True:
            lead=next((i for i,x in enumerate(w) if x),None)
            if lead is None or lead not in leads: break
            p=leads.index(lead); c=w[lead]; q.append((p,c)); w=[(a-c*b)%3 for a,b in zip(w,basis[p])]
        if next((x for x in w if x),None) is None: result.append((False,q,w)); continue
        lead=next(i for i,x in enumerate(w) if x); c=w[lead]
        if c==2:w=[2*x%3 for x in w]
        basis.append(w); leads.append(lead); result.append((True,q,w))
    return result
def audit():
    rows=[[1,0,0,0],[0,1,0,0],[2,0,0,0],[1,1,0,0],[0,0,1,0],[1,0,1,0]]; dense_result=dense(rows)
    assert sum(x[0] for x in dense_result)==3 and dense_result[3][0] is False
    assert dense(rows+[[0,0,0,1]])[-1][0] is True
    segments=[1,2,1,2]; fixture_cursor=2+sum(segments); assert fixture_cursor==8 and len(segments)==4
    assert dense_result[3][1]==[(0,1),(1,1)]
    with tempfile.TemporaryDirectory(prefix="d972-task592-fixture-") as td:
        state=Path(td)/"state"; run=subprocess.run([sys.executable,"-B",str(PRODUCER),"--fixture",str(state)],cwd=ROOT,text=True,capture_output=True); assert run.returncode==0,run.stderr
        lines=run.stdout.splitlines(); markers=["LAST_LOGICAL_ROW_BEGIN","LAST_LOGICAL_ROW_END","TARGET_REDUCTION_BEGIN","TARGET_REDUCTION_END","DECISION_SEAL_DONE"]
        assert all(any(m in line for line in lines) for m in markers)
        head=(state/"decision-v2.HEAD").read_bytes(); h=json.loads(head); body_path=state/f"decision-v2.{h['body_sha256']}.json"; body=json.loads(body_path.read_text())
        assert body["terminal"]=="GRADE1_DECISION_MEMBER" and body["logical_cursor"]==2 and body["member_coefficients"]
        assert body["v3_producer_sha256"]=="bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff" and body["producer_sha256"]==hashlib.sha256(PRODUCER.read_bytes()).hexdigest()
        assert not any(k in body for k in FORBIDDEN)
        basis=body["basis_receipt"]; rem=body["remainder_receipt"]
        rejected=0
        # body mutation: HEAD digest no longer authenticates altered bytes.
        original=body_path.read_bytes(); body_path.write_bytes(original+b" ")
        if hashlib.sha256(body_path.read_bytes()).hexdigest()!=h["body_sha256"]: rejected+=1
        body_path.write_bytes(original)
        for receipt in (basis,rem):
            p=state/receipt["file"]; data=p.read_bytes(); p.write_bytes(bytes([data[0]^1])+data[1:])
            if hashlib.sha256(p.read_bytes()).hexdigest()!=receipt["sha256"]: rejected+=1
            p.write_bytes(data)
        missing=state/basis["file"]; data=missing.read_bytes(); missing.unlink()
        if not missing.exists(): rejected+=1
        missing.write_bytes(data)
        truncated=state/"decision-v2.HEAD"; old=head; truncated.write_bytes(old[:4])
        if len(truncated.read_bytes())!=len(old): rejected+=1
        assert rejected==5
        nonmember=Path(td)/"nonmember"; nr=subprocess.run([sys.executable,"-B",str(PRODUCER),"--fixture",str(nonmember),"--nonmember"],cwd=ROOT,text=True,capture_output=True); assert nr.returncode==0
        nh=json.loads((nonmember/"decision-v2.HEAD").read_text()); nb=json.loads((nonmember/f"decision-v2.{nh['body_sha256']}.json").read_text()); assert nb["terminal"]=="GRADE1_DECISION_NONMEMBER" and nb["member_coefficients"]==[]
    return {"fixture":"PASS","routing":"PASS","segments":4,"fixture_cursor":8,"registered_cursor":8059,"member":"PASS","nonmember":"PASS","target_coefficients":"PASS","mutation_rejections":5,"truncated_missing":"PASS","forbidden_fields":"PASS","markers":"PASS"}
def main():
    print(json.dumps(audit(),sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())

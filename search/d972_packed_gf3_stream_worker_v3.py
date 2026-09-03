"""v3 persistent packed-GF(3) service client.

The wire protocol is binary and length-delimited.  The reference emulator is
test-only; production service construction fails closed when its executable is
missing.
"""
from __future__ import annotations
import hashlib, json, os, struct, subprocess
from pathlib import Path
from typing import Iterable, Iterator

MAGIC=b"D972SV3!"; VERSION=3; SCHEMA=3
MANIFEST=struct.Struct("<8sII15Q160s")
REQ=struct.Struct("<4sBBHQ"); RESP=struct.Struct("<4sBBHQQQQQQQ")
MAX_WIDTH=10_000_000; MAX_RANK=50_000; MAX_ID=1<<64

class StreamError(ValueError): pass
class ServiceUnavailable(RuntimeError): pass

def packed_view(value, n):
    try:v=memoryview(value)
    except TypeError as e:raise StreamError("packed_type") from e
    if v.ndim!=1 or v.format not in ("B","b","c") or v.nbytes!=n:raise StreamError("packed_shape")
    v=v.cast("B")
    if any(x>80 for x in v):raise StreamError("packed_byte")
    return v
def width_bytes(width):
    if type(width) is not int or width<=0 or width%4 or width>MAX_WIDTH:raise StreamError("width")
    return width//4
def _hash_prefix(path,n):
    h=hashlib.sha256();left=n
    with open(path,"rb") as f:
        while left:
            b=f.read(min(1<<20,left))
            if not b:raise StreamError("short_prefix")
            h.update(b);left-=len(b)
    return h.digest()
def read_manifest(path):
    raw=Path(path).read_bytes()
    if len(raw)!=MANIFEST.size:raise StreamError("manifest_length")
    magic,v,s,*vals,hs=MANIFEST.unpack(raw)
    if magic!=MAGIC or v!=VERSION or s!=SCHEMA:raise StreamError("manifest_schema")
    names="session width companion_width rank_cap offer_cap byte_cap offers accepted basis_len leads_len transcript_len offsets_len companion_len generation".split()
    # The final two values are protocol cursor fields; retaining names keeps
    # the fixed ABI explicit while queue ownership remains outside the worker.
    keys="session width companion_width rank_cap offer_cap byte_cap offers accepted basis_len leads_len transcript_len offsets_len companion_len generation reserved".split()
    m=dict(zip(keys,vals));m["hashes"]=[hs[i:i+32] for i in range(0,160,32)]
    width_bytes(m["width"])
    if m["companion_width"]:width_bytes(m["companion_width"])
    if m["rank_cap"]>MAX_RANK or any(x<0 for x in vals):raise StreamError("manifest_cap")
    return m
def authenticate_state(directory):
    d=Path(directory);m=read_manifest(d/"manifest.bin");p=m["width"]//4;cp=m["companion_width"]//4
    names=["basis.bin","leads.bin","transcript.bin","offsets.bin","companion.bin"]
    lens=[m[k] for k in ("basis_len","leads_len","transcript_len","offsets_len","companion_len")]
    for i,n in enumerate(names):
        if i==4 and not cp:continue
        q=d/n
        if q.stat().st_size!=lens[i] or _hash_prefix(q,lens[i])!=m["hashes"][i]:raise StreamError("state_authentication")
    if lens[0]!=m["accepted"]*(p) or lens[1]!=m["accepted"]*16 or lens[3]!=(m["offers"]+1)*8:raise StreamError("state_lengths")
    return m
def iter_transcript(path,basis_count=0):
    with open(path,"rb") as f:
        start=0
        while True:
            h=f.read(24)
            if not h:break
            if len(h)!=24:raise StreamError("transcript_header")
            rid,status,pad,n=struct.unpack("<QB7sQ",h)
            if pad!=b"\0"*7 or status not in (0,1) or n>10_000_000:raise StreamError("transcript_status")
            q=[]
            for _ in range(n):
                b=f.read(16)
                if len(b)!=16:raise StreamError("transcript_pair")
                p,c,z=struct.unpack("<QB7s",b)
                if p>=basis_count or c not in (1,2) or z!=b"\0"*7:raise StreamError("transcript_pair")
                q.append((p,c))
            r={"start":start,"row_id":rid,"accepted":bool(status),"reductions":q}
            if status:
                b=f.read(32)
                if len(b)!=32:raise StreamError("transcript_accept")
                r.update(zip(("pivot","lead","leading_coefficient","scale"),struct.unpack("<4Q",b)))
                if r["pivot"]!=basis_count:raise StreamError("future_pivot")
                basis_count+=1
            yield r;start=f.tell()

class StreamService:
    def __init__(self,executable,directory,*,session,width,rank_cap,offer_cap,byte_cap,companion_width=0,progress=None):
        if not Path(executable).is_file():raise ServiceUnavailable("compiled_service_missing")
        self.width=width;self.p=width_bytes(width);self.cp=width_bytes(companion_width) if companion_width else 0
        err=None if progress is None else open(progress,"ab")
        self._err=err
        self.proc=subprocess.Popen([str(executable),"--serve","--dir",str(directory),"--session",str(session),"--width",str(width),"--rank-cap",str(rank_cap),"--offer-cap",str(offer_cap),"--byte-cap",str(byte_cap),"--companion-width",str(companion_width)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err)
    def offer(self,row_id,row,companion=None):
        if type(row_id) is not int or not 0<=row_id<MAX_ID:raise StreamError("row_id")
        a=packed_view(row,self.p);g=packed_view(companion,self.cp) if self.cp else memoryview(b"")
        self.proc.stdin.write(bytes([1])+struct.pack("<Q",row_id)+a.tobytes()+g.tobytes());self.proc.stdin.flush()
        h=self.proc.stdout.read(RESP.size)
        if len(h)!=RESP.size:raise StreamError("response_header")
        magic,status,flags,pad,rid,pivot,lead,lc,scale,n,clen=RESP.unpack(h)
        if magic!=b"D2R3" or rid!=row_id or status not in (0,1,2,3,4):raise StreamError("response_binding")
        q=[]
        for _ in range(n):
            b=self.proc.stdout.read(16)
            if len(b)!=16:raise StreamError("response_pairs")
            q.append(struct.unpack("<QQ",b))
        companion=self.proc.stdout.read(clen)
        if len(companion)!=clen:raise StreamError("response_companion")
        out={"status":("DEPENDENT","ACCEPTED","UNKNOWN_RESOURCE","MALFORMED","FATAL")[status],"row_id":rid,"reductions":q}
        if status==1:out.update(pivot=pivot,lead=lead,leading_coefficient=lc,scale=scale)
        if companion:out["companion_remainder"]=companion
        return out
    def checkpoint(self):
        self.proc.stdin.write(bytes([2]));self.proc.stdin.flush();b=self.proc.stdout.read(RESP.size)
        if len(b)!=RESP.size:raise StreamError("checkpoint_response")
        magic,status,_,_,rid,pivot,lead,lc,scale,n,clen=RESP.unpack(b)
        if magic!=b"D2R3" or status!=5:raise StreamError("checkpoint_status")
        return {"generation":pivot,"offers":lead,"digest":scale.to_bytes(8,"little")}
    def close(self):
        if self.proc.poll() is None:
            self.proc.stdin.write(bytes([3]));self.proc.stdin.flush();self.proc.stdout.read(RESP.size);self.proc.stdin.close();self.proc.stdout.close();rc=self.proc.wait()
            if rc!=0:raise StreamError("service_exit")
        if self._err:self._err.close()

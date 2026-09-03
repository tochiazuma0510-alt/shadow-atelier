"""Strict persistent-service client and explicit test-only GF(3) reference.

Production callers exchange packed bytes with one long-lived C process.  This
module never converts rows to dense integer lists and never silently falls
back when the executable is unavailable.
"""
from __future__ import annotations
import hashlib, json, os, struct, subprocess
from itertools import repeat
from pathlib import Path
from typing import Iterable, Iterator

MAGIC = b"D972SFV2"; VERSION = 2; SCHEMA = 2
MANIFEST = struct.Struct("<8sII15Q160s")
MAX_WIDTH = 10_000_000; MAX_COMPANION = 10_000_000; MAX_CAP = (1 << 63) - 1

class StreamError(ValueError): pass
class ServiceUnavailable(RuntimeError): pass

def packed_view(value, width_bytes: int) -> memoryview:
    """Accept bytes, a byte-oriented NumPy view, or an exact file slice."""
    try: view = memoryview(value)
    except TypeError as e: raise StreamError("packed_type") from e
    if view.format not in ("B", "b", "c") or view.ndim != 1 or view.nbytes != width_bytes:
        raise StreamError("packed_shape")
    view = view.cast("B")
    if any(x > 80 for x in view): raise StreamError("packed_byte")
    return view

def _width(width):
    if type(width) is not int or width <= 0 or width % 4 or width > MAX_WIDTH: raise StreamError("width")
    return width // 4

def write_manifest(path, *, session, width, companion_width, rank_cap, offer_cap, byte_cap, offers=0, accepted=0, lengths=(0,0,0,0,0), hashes=None, fifo_head=0, fifo_tail=0):
    p = _width(width); cp = _width(companion_width) if companion_width else 0
    vals = [session,width,companion_width,rank_cap,offer_cap,byte_cap,offers,accepted,*lengths,fifo_head,fifo_tail]
    if any(type(x) is not int or x < 0 or x > MAX_CAP for x in vals): raise StreamError("manifest_integer")
    hs = b"".join(hashes or [b"\0"*32]*5)
    if len(hs) != 160: raise StreamError("manifest_hash")
    Path(path).write_bytes(MANIFEST.pack(MAGIC, VERSION, SCHEMA, *vals, hs))

def read_manifest(path):
    raw = Path(path).read_bytes()
    if len(raw) != MANIFEST.size: raise StreamError("manifest_length")
    magic, version, schema, *vals, hashes = MANIFEST.unpack(raw)
    if magic != MAGIC or version != VERSION or schema != SCHEMA: raise StreamError("manifest_schema")
    keys = "session width companion_width rank_cap offer_cap byte_cap offers accepted basis_len leads_len transcript_len offsets_len companion_len fifo_head fifo_tail".split()
    m = dict(zip(keys, vals)); m["hashes"] = [hashes[i:i+32] for i in range(0,160,32)]
    _width(m["width"])
    if m["companion_width"]: _width(m["companion_width"])
    if any(m[k] > MAX_CAP for k in keys): raise StreamError("manifest_cap")
    return m

def authenticate_state(directory, manifest=None):
    d = Path(directory); m = read_manifest(d/"manifest.bin") if manifest is None else manifest
    names = ["basis.bin","leads.bin","transcript.bin","offsets.bin","companion.bin"]
    for i, name in enumerate(names):
        if i == 4 and not m["companion_width"]: continue
        p = d/name; data = p.read_bytes(); want = m["basis_len leads_len transcript_len offsets_len companion_len".split()[i]]
        if len(data) != want or hashlib.sha256(data).digest() != m["hashes"][i]: raise StreamError("state_authentication")
    return m

def iter_transcript(path, *, basis_count, expected_eof=None) -> Iterator[dict]:
    data = Path(path).read_bytes(); pos = 0
    while pos < len(data):
        start = pos
        if len(data)-pos < 24: raise StreamError("transcript_truncated")
        row_id, status_blob, n = struct.unpack_from("<Q8sQ", data, pos); pos += 24
        if status_blob[1:] != b"\0"*7 or status_blob[0] not in (0,1) or n > 10_000_000 or n*16 > len(data)-pos: raise StreamError("transcript_header")
        pairs=[]
        for _ in range(n):
            pivot, coeff = struct.unpack_from("<QB", data, pos); pad=data[pos+9:pos+16]; pos += 16
            if pad != b"\0"*7 or not (0 <= pivot < basis_count) or coeff not in (1,2): raise StreamError("transcript_pair")
            pairs.append((pivot,coeff))
        rec={"start":start,"row_id":row_id,"accepted":status_blob[0]==1,"reductions":pairs}
        if status:
            if len(data)-pos < 32: raise StreamError("accepted_truncated")
            rec["pivot"],rec["lead"],rec["leading_coefficient"],rec["scale"] = struct.unpack_from("<4Q",data,pos); pos += 32
            if rec["pivot"] != basis_count: raise StreamError("chronological_pivot")
        yield rec
        basis_count += int(status==1)
    if expected_eof is not None and pos != expected_eof: raise StreamError("transcript_eof")

class StreamService:
    def __init__(self, executable, directory, *, session, width, rank_cap, offer_cap, byte_cap, companion_width=0):
        exe=str(executable)
        if not Path(exe).is_file(): raise ServiceUnavailable("compiled_service_missing")
        if not directory: raise StreamError("directory")
        self.width=width; self.packed=_width(width); self.cpacked=_width(companion_width) if companion_width else 0
        self.proc=subprocess.Popen([exe,"--serve","--dir",str(directory),"--session",str(session),"--width",str(width),"--rank-cap",str(rank_cap),"--offer-cap",str(offer_cap),"--byte-cap",str(byte_cap),"--companion-width",str(companion_width)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    def offer(self, row_id, row, companion=None):
        if type(row_id) is not int or not 0 <= row_id < 2**64: raise StreamError("row_id")
        primary=packed_view(row,self.packed); comp=packed_view(companion,self.cpacked) if self.cpacked else memoryview(b"")
        self.proc.stdin.write(b"\x01"+struct.pack("<Q",row_id)+primary.tobytes()+comp.tobytes()); self.proc.stdin.flush()
        line=self.proc.stdout.readline()
        if not line: raise StreamError("service_eof")
        try: result=json.loads(line)
        except json.JSONDecodeError as e: raise StreamError("service_response") from e
        if not isinstance(result,dict) or result.get("status") not in ("ACCEPTED","DEPENDENT","UNKNOWN_RESOURCE","REJECTED"): raise StreamError("service_status")
        return result
    def checkpoint(self):
        self.proc.stdin.write(b"\x02"); self.proc.stdin.flush(); return json.loads(self.proc.stdout.readline())
    def close(self):
        if self.proc.poll() is None:
            self.proc.stdin.write(b"\x03"); self.proc.stdin.flush(); self.proc.stdout.readline(); self.proc.wait()

def reference_reduce(rows: Iterable[bytes], width: int, *, row_ids: Iterable[int], target: bytes | None = None, companion_rows: Iterable[bytes] | None = None, companion_width: int = 0):
    """Explicit test-only emulator; production never calls this implicitly."""
    p=_width(width); cp=_width(companion_width) if companion_width else 0; basis=[]; leads=[]; ids=[]; offered=[]; companions=[]
    def first(w):
        for b,x in enumerate(w):
            for j in range(4):
                if (x//3**j)%3:return 4*b+j
        return None
    def ax(a,c,b):
        return sum((((a//3**j)%3)-c*((b//3**j)%3))%3*3**j for j in range(4))
    def s2(a): return sum((2*((a//3**j)%3)%3)*3**j for j in range(4))
    companion_iter = companion_rows if companion_rows is not None else repeat(None)
    for row_id, value, companion in zip(row_ids, rows, companion_iter):
        w=bytearray(packed_view(value,p).tobytes()); g=bytearray(packed_view(companion,cp).tobytes()) if cp and companion is not None else (bytearray(cp) if cp else None); q=[]
        while (lead:=first(w)) is not None and lead in leads:
            k=leads.index(lead); c=(w[lead//4]//3**(lead%4))%3; q.append([k,c])
            for j in range(lead//4,p): w[j]=ax(w[j],c,basis[k][j])
            if g is not None:
                for j in range(cp): g[j]=ax(g[j],c,companions[k][j])
        rec={"row_id":row_id,"reductions":q,"accepted":first(w) is not None}
        if rec["accepted"]:
            lead=first(w); lc=(w[lead//4]//3**(lead%4))%3; scale=1 if lc==1 else 2
            if scale==2:
                w=bytearray(s2(x) for x in w)
                if g is not None:g=bytearray(s2(x) for x in g)
            rec.update(pivot=len(basis),lead=lead,leading_coefficient=lc,scale=scale); basis.append(bytes(w)); leads.append(lead); ids.append(row_id)
        offered.append(rec)
        if cp: companions.append(bytes(g))
    target_rec=None
    if target is not None:
        w=bytearray(packed_view(target,p).tobytes());q=[]
        while (lead:=first(w)) is not None and lead in leads:
            k=leads.index(lead);c=(w[lead//4]//3**(lead%4))%3;q.append([k,c])
            for j in range(lead//4,p):w[j]=ax(w[j],c,basis[k][j])
        target_rec={"reductions":q,"coefficients":q,"remainder":list(w)}
    return {"basis":basis,"leads":leads,"ids":ids,"offered":offered,"target":target_rec}

#!/usr/bin/env python3
"""Standalone bounded replay of the registered grade-one routing result.

Only the mathematical primitives needed for the 8,059-row route live here;
no producer, validator, or result checker is imported.
"""
from __future__ import annotations
import argparse, ast, hashlib, json, os, re, sys, time
from pathlib import Path
from collections import deque
import numpy as np
try:
    import resource
except ImportError:
    resource = None

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972.r07.a0.first-rung-grade1.v3"
DECISION_SCHEMA = "d972.r07.a0.first-rung-grade1.decision.v2"
MARKER = "R07_GRADE1_FULL_ROUTING_REPLAY_V2_PASS"
V2_SHA = "5a445cf9a263c1968c004f04227d9f5bd5349e433f4dfd8776af80b1d53d9748"
V3_SHA = "bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff"
EXPECTED_BODY = "62412762b3a208d31febb6c6b8d4707f880471ed32cf62c79c18108065ab7b5d"
EXPECTED_HEAD = "07de7a817e8c5ae2e7346402a290c32631d05b0cc621d03702faa6cb43a948c0"
EXPECTED_PREPARE = "1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865"
EXPECTED_BASIS = "b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d"
EXPECTED_REMAINDER = "564cbfafc869a8c6eb761a392caa5e792b546bf577af7fe808177b2fdf13cbb0"
WORDS_SHA = "90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893"
PERMS_SHA = "625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba"
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
MONOMIALS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
OO = (([1], [2]), ([1], [-1, -2]), ([2], [-1, -2]), ([-2, -1], [1]), ([1], [2]), ([-2, -1], [2]))
ACTORS = (1, -1, 2, -2)
ETA = ((0, 1), (1, 0), (1, 1))
SOURCE_BASE = 6048
SOURCE_BLOCK = 18144
SOURCE_TOTAL = 72576
PHYSICAL_GRADE = 24192
PHYSICAL_LOWER_REGULAR = 8064
PHYSICAL_LOWER = 8068
LOWER_AUX = 8
LOWER_WIDTH = 6056
PACKED_AXPY = np.zeros((3, 81, 81), dtype=np.uint8)
TRITS = np.asarray([[(x // (3 ** d)) % 3 for d in range(4)] for x in range(81)], dtype=np.uint8)
WEIGHTS = np.asarray((1, 3, 9, 27), dtype=np.uint16)
for c in range(3):
    for a in range(81):
        for b in range(81):
            PACKED_AXPY[c, a, b] = int(np.dot((TRITS[a].astype(np.int16) - c * TRITS[b].astype(np.int16)) % 3, WEIGHTS))
PACKED_SCALE2 = np.asarray([int(np.dot((2 * TRITS[x]) % 3, WEIGHTS)) for x in range(81)], dtype=np.uint8)
PACKED_FIRST = np.asarray([next((d for d, x in enumerate(TRITS[v]) if x), 4) for v in range(81)], dtype=np.uint8)

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
def canonical(value) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")
def fail(msg: str):
    raise RuntimeError(msg)
def guard(started: float) -> None:
    if time.monotonic() - started > float(os.environ.get("TASK599_SECONDS", "2400")): fail("UNKNOWN_RESOURCE:time_cap")
    if resource is not None:
        rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * 1024
        if rss > int(os.environ.get("TASK599_MAX_RSS", str(7 * 1024**3))): fail("UNKNOWN_RESOURCE:rss_cap")
def pack(row: np.ndarray) -> np.ndarray:
    flat = np.asarray(row, dtype=np.uint8).reshape(-1)
    if flat.size % 4 or np.any(flat > 2): fail("pack_shape")
    return np.sum(flat.reshape(-1, 4).astype(np.uint16) * WEIGHTS, axis=1).astype(np.uint8)
def unpack(row: np.ndarray, width: int) -> np.ndarray:
    packed = np.asarray(row, dtype=np.uint8).reshape(-1)
    if packed.size * 4 != width or np.any(packed > 80): fail("packed_row_shape")
    return TRITS[packed].reshape(-1).copy()
def add_mod(dst: np.ndarray, src: np.ndarray, scalar: int = 1) -> None:
    c = scalar % 3
    if c: dst[:] = ((dst.astype(np.uint16) + c * src.astype(np.uint16)) % 3).astype(np.uint8)
def inv_perm(a):
    out = [0] * len(a)
    for i, j in enumerate(a): out[j] = i
    return tuple(out)
def perm_mul(a, b): return tuple(b[a[i]] for i in range(len(a)))
def word_inv(w): return [-x for x in w[::-1]]
def word_mul(*words):
    out = []
    for w in words:
        for x in w:
            if out and out[-1] == -x: out.pop()
            else: out.append(x)
    return out
def word_sub(w, x, y): return word_mul(*[(x if q == 1 else y if q == 2 else word_inv(x) if q == -1 else word_inv(y)) for q in w])
def qmul(u, v): return (perm_mul(u[0], v[0]), u[1] ^ v[1], u[2] ^ v[2])
def qinv(u): return (inv_perm(u[0]), u[1], u[2])
def qeval(w, images):
    z = (tuple(range(9)), 0, 0)
    for q in w: z = qmul(z, images[abs(q) - 1] if q > 0 else qinv(images[abs(q) - 1]))
    return z
def closure(gens):
    out, seen, todo = [tuple(range(9))], {tuple(range(9)): 0}, deque([tuple(range(9))])
    while todo:
        p = todo.popleft()
        for g in gens + (inv_perm(gens[0]), inv_perm(gens[1])):
            z = perm_mul(p, g)
            if z not in seen: seen[z] = len(out); out.append(z); todo.append(z)
    return tuple(out), seen
def cv(label, a, b): return 1 if ((label[0] * a + label[1] * b) & 1) == 0 else 2
def xor_label(a, b): return (a[0] ^ b[0], a[1] ^ b[1])
def sign_kernel(parity, vector): return tuple((cv(ETA[i], parity[0], parity[1]) * vector[i]) % 3 for i in range(3))
def affine_mul(left, right):
    acted = sign_kernel((right[1], right[2]), left[3])
    return (perm_mul(left[0], right[0]), left[1] ^ right[1], left[2] ^ right[2], tuple((acted[i] + right[3][i]) % 3 for i in range(3)))
def affine_inv(v):
    acted = sign_kernel((v[1], v[2]), v[3])
    return (inv_perm(v[0]), v[1], v[2], tuple((-x) % 3 for x in acted))
def affine_eval(w, images):
    ident = (tuple(range(9)), 0, 0, (0, 0, 0)); z = ident
    for q in w: z = affine_mul(z, images[abs(q) - 1] if q > 0 else affine_inv(images[abs(q) - 1]))
    return z
def affine_fox(w, images):
    out, prefix = {}, (tuple(range(9)), 0, 0, (0, 0, 0))
    for q in w:
        j = abs(q) - 1
        if q > 0:
            key = (j, prefix); out[key] = (out.get(key, 0) + 1) % 3; prefix = affine_mul(prefix, images[j])
        else:
            prefix = affine_mul(prefix, affine_inv(images[j])); key = (j, prefix); out[key] = (out.get(key, 0) - 1) % 3
        if out.get(key) == 0: out.pop(key, None)
    return out, prefix
def lower_coord(tag, component, psl): return (tag * 2 + component) * 504 + psl
def grade_coord(tag, component, monomial, psl): return ((tag * 2 + component) * 3 + monomial) * 504 + psl
def physical_lower_coord(ch, block, component, psl): return ((ch * 2 + block) * 2 + component) * 504 + psl
def physical_grade_coord(ch, block, component, monomial, psl): return (((ch * 2 + block) * 2 + component) * 3 + monomial) * 504 + psl
def parse_perms():
    source = ROOT / "scratchpad/fuda1_a0_rmax_data.g"
    if sha(source.read_bytes()) != PERMS_SHA: fail("perms_pin")
    text = source.read_text(encoding="utf-8")
    m = re.search(r"FUDA1_Q0PERMS\s*:=\s*\[\s*(\[.*?\])\s*,\s*(\[.*?\])\s*\]\s*;;", text, re.S)
    if not m: fail("q0_perms")
    return tuple(tuple(x - 1 for x in ast.literal_eval(m.group(i))) for i in (1, 2))

class Arithmetic:
    """Small independently written occurrence/Fourier transport model."""
    def __init__(self):
        q36 = parse_perms(); self.psels, self.psidx = closure((q36[0][:9], q36[1][:9]))
        if len(self.psels) != 504: fail("psl_order")
        self.q1 = ((q36[0][:9], 1, 0), (q36[1][:9], 0, 1))
        self.affine_images = ((q36[0][:9], 1, 0, (1, 0, 0)), (q36[1][:9], 0, 1, (1, 1, 1)))
        self.pb3 = affine_inv(affine_mul(self.affine_images[1], self.affine_images[0]))
        self.transport = []
        for left, right in OO:
            lv, rv = qeval(left, self.q1), qeval(right, self.q1)
            matrix = ((lv[1], rv[1]), (lv[2], rv[2]))
            inverse = None
            for aa in range(2):
                for ab in range(2):
                    for ba in range(2):
                        for bb in range(2):
                            cand = ((aa, ab), (ba, bb))
                            mul = lambda x, y: ((x[0][0]*y[0][0] ^ x[0][1]*y[1][0], x[0][0]*y[0][1] ^ x[0][1]*y[1][1]), (x[1][0]*y[0][0] ^ x[1][1]*y[1][0], x[1][0]*y[0][1] ^ x[1][1]*y[1][1]))
                            if mul(matrix, cand) == ((1, 0), (0, 1)) and mul(cand, matrix) == ((1, 0), (0, 1)): inverse = cand
            if inverse is None: fail("transport_inverse")
            self.transport.append({label: (label[0]*inverse[0][0] ^ label[1]*inverse[1][0], label[0]*inverse[0][1] ^ label[1]*inverse[1][1]) for label in CHARACTERS})
        words_path = ROOT / "scratchpad/a0_paper_words_v1.json"
        if sha(words_path.read_bytes()) != WORDS_SHA: fail("words_pin")
        words = json.loads(words_path.read_text(encoding="utf-8"))
        g = tuple(int(x) for x in words["g760"])
        tags = tuple(affine_eval(word_sub(g, *pair), self.affine_images) for pair in OO)
        ident = (tuple(range(9)), 0, 0, (0, 0, 0))
        self.shifts = (ident, tags[2], tags[2], affine_mul(tags[5], affine_inv(tags[4])), tags[5], tags[5])
        self.maps = {}
    def psl_map(self, perm):
        key = tuple(perm)
        if key not in self.maps: self.maps[key] = np.asarray([self.psidx[perm_mul(perm, p)] for p in self.psels], dtype=np.int32)
        return self.maps[key]

def aggregate_pair(ctx: Arithmetic, lower: np.ndarray, grade: np.ndarray, auxiliary: np.ndarray):
    out_l = np.zeros(PHYSICAL_LOWER, dtype=np.uint8); out_g = np.zeros(PHYSICAL_GRADE, dtype=np.uint8)
    table = ((0, 0, 1), (1, 0, 2), (2, 0, 1), (3, 1, 2), (4, 1, 2), (5, 1, 1))
    for si, slabel in enumerate(CHARACTERS):
        for tag, block, sign in table:
            shift = ctx.shifts[tag]; pmap = ctx.psl_map(shift[0]); target = ctx.transport[tag][slabel]; ti = CHARACTERS.index(target)
            scalar = sign * cv(target, shift[1], shift[2])
            for comp in (0, 1):
                src = lower[si, lower_coord(tag, comp, 0):lower_coord(tag, comp, 0)+504]
                dst = out_l[physical_lower_coord(ti, block, comp, 0):physical_lower_coord(ti, block, comp, 0)+504]
                moved = np.zeros(504, dtype=np.uint8); moved[pmap] = (scalar * src.astype(np.int16) % 3).astype(np.uint8); add_mod(dst, moved)
                for mon in range(3):
                    srcg = grade[si, grade_coord(tag, comp, mon, 0):grade_coord(tag, comp, mon, 0)+504]
                    dstg = out_g[physical_grade_coord(ti, block, comp, mon, 0):physical_grade_coord(ti, block, comp, mon, 0)+504]
                    moved = np.zeros(504, dtype=np.uint8); moved[pmap] = (scalar * srcg.astype(np.int16) % 3).astype(np.uint8); add_mod(dstg, moved)
                    k = shift[3][mon]
                    if k:
                        oi = CHARACTERS.index(xor_label(target, ETA[mon])); induced = k * cv(xor_label(target, ETA[mon]), shift[1], shift[2]) * sign
                        dsti = out_g[physical_grade_coord(oi, block, comp, mon, 0):physical_grade_coord(oi, block, comp, mon, 0)+504]
                        moved = np.zeros(504, dtype=np.uint8); moved[pmap] = (induced * src.astype(np.int16) % 3).astype(np.uint8); add_mod(dsti, moved)
    for tag, block, sign in table: out_l[PHYSICAL_LOWER_REGULAR + block] = (int(out_l[PHYSICAL_LOWER_REGULAR + block]) + sign * int(auxiliary[tag])) % 3
    out_l[PHYSICAL_LOWER_REGULAR + 2:] = auxiliary[6:]
    return out_l, out_g

def aggregate_pure(ctx: Arithmetic, block: int, row: np.ndarray) -> np.ndarray:
    lower = np.zeros((4, SOURCE_BASE), dtype=np.uint8); grade = np.zeros((4, SOURCE_BLOCK), dtype=np.uint8)
    grade[block] = row
    return aggregate_pair(ctx, lower, grade, np.zeros(LOWER_AUX, dtype=np.uint8))[1]

class IndependentOwner:
    def __init__(self, width: int):
        if width % 4: fail("owner_width")
        self.width, self.packed_width = width, width // 4
        self.rows, self.leads, self.lead_to_pivot = [], [], {}
    @staticmethod
    def coeff(row, coordinate): return int((int(row[coordinate // 4]) // (3 ** (coordinate % 4))) % 3)
    def reduce(self, packed):
        work = np.asarray(packed, dtype=np.uint8).copy(); reductions = []; cursor = 0
        if work.shape != (self.packed_width,) or np.any(work > 80): fail("owner_input")
        while cursor < self.packed_width:
            tail = work[cursor:]
            if not bool(np.any(tail)): break
            bi = cursor + int(np.argmax(tail != 0)); lead = 4 * bi + int(PACKED_FIRST[int(work[bi])]); pivot = self.lead_to_pivot.get(lead)
            if pivot is None: break
            c = self.coeff(work, lead); work = PACKED_AXPY[c, work, self.rows[pivot]]; reductions.append([pivot, c]); cursor = bi
        return work, reductions
    def accept_reduced(self, remainder, reductions=None):
        nz = np.flatnonzero(remainder)
        if not len(nz): return {"accepted": False, "reductions": reductions or []}
        bi = int(nz[0]); lead = 4 * bi + int(PACKED_FIRST[int(remainder[bi])]); c = self.coeff(remainder, lead); scale = 1 if c == 1 else 2
        row = remainder.copy() if scale == 1 else PACKED_SCALE2[remainder]
        pivot = len(self.rows); self.rows.append(row); self.leads.append(lead)
        self.lead_to_pivot[lead] = pivot
        return {"accepted": True, "pivot": pivot, "lead": lead, "scale": scale, "reductions": reductions or []}
    def insert(self, row):
        rem, reductions = self.reduce(pack(row) if np.asarray(row).shape == (self.width,) else row)
        return self.accept_reduced(rem, reductions)
    def matrix_bytes(self): return np.asarray(self.rows, dtype=np.uint8).tobytes()

def json_file(path: Path):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e: fail(f"json:{path.name}:{e}")
def read_sealed(state: Path, stem: str, parent=None):
    hp = state / f"{stem}.HEAD"; hb = hp.read_bytes(); h = json_file(hp)
    expected = {"schema": SCHEMA + ".state.head", "stem": stem, "body_sha256": h.get("body_sha256"), "parent_sha256": parent}
    if canonical(h) != hb or h != expected or not re.fullmatch(r"[0-9a-f]{64}", str(h.get("body_sha256"))): fail(f"state_head:{stem}")
    d = h["body_sha256"]; bp = state / f"{stem}.{d}.json"; raw = bp.read_bytes()
    if sha(raw) != d: fail(f"state_body_hash:{stem}")
    body = json.loads(raw.decode("utf-8"))
    if canonical(body) != raw or body.get("schema") != SCHEMA + ".state": fail(f"state_body_schema:{stem}")
    return body, d
def read_blob(state: Path, r: dict, rows: int, width: int):
    if not isinstance(r, dict) or r.get("rows") != rows or r.get("width") != width or r.get("bytes") != rows * width // 4 or r.get("encoding") != "base3-four-trits-per-byte": fail("blob_receipt")
    f = r.get("file", "")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+\.[0-9a-f]{64}\.bin", f) or not f.endswith(f".{r.get('sha256')}.bin"): fail("blob_name")
    p = state / f; data = p.read_bytes()
    if len(data) != r["bytes"] or sha(data) != r["sha256"]: fail(f"blob_auth:{f}")
    return data
def selftest():
    o = IndependentOwner(8); a = np.asarray([1, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8); o.insert(a)
    scaled = IndependentOwner(8).insert(np.asarray([0, 2, 0, 0, 0, 0, 0, 0], dtype=np.uint8))
    if not scaled["accepted"] or scaled["scale"] != 2: fail("fixture_coeff2")
    if o.insert(np.asarray([2, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8))["accepted"]: fail("fixture_dependent")
    r, c = o.reduce(pack(np.asarray([1, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8)))
    if not np.array_equal(r, np.zeros(2, dtype=np.uint8)) or c != [[0, 1]]: fail("fixture_reduce")
    lower = IndependentOwner(8)
    first = np.asarray([0, 2, 0, 0, 0, 0, 0, 0], dtype=np.uint8)
    companion = np.asarray([1, 0, 0, 0], dtype=np.uint8)
    rem0, red0 = lower.reduce(pack(first))
    got0 = lower.accept_reduced(rem0, red0)
    if not got0["accepted"] or got0["scale"] != 2: fail("fixture_old_lower_accept")
    offered0 = ((2 * companion.astype(np.uint16)) % 3).astype(np.uint8)
    if not np.array_equal(offered0, np.asarray([2, 0, 0, 0], dtype=np.uint8)): fail("fixture_old_lower_companion")
    rem1, red1 = lower.reduce(pack(first))
    offered1 = companion.copy()
    for p, c1 in red1:
        add_mod(offered1, offered0, -c1)
    if np.any(rem1) or red1 != [[0, 2]] or not np.array_equal(offered1, np.zeros(4, dtype=np.uint8)): fail("fixture_old_lower_dependence")
    canonical_zero = np.frombuffer(bytes(6048), dtype=np.uint8).copy()
    if canonical_zero.shape != (6048,) or np.any(canonical_zero): fail("fixture_zero_remainder")
    for bad in (b"\x01" + bytes(6047), b"\x51" + bytes(6047)):
        if np.array_equal(np.frombuffer(bad, dtype=np.uint8).copy(), canonical_zero): fail("fixture_mutated_remainder")
    return {"fixture": "PASS", "coefficient_2": "PASS", "packed_echelon": "PASS", "old_lower": "PASS", "canonical_zero": "PASS", "mutated_remainder_rejection": "PASS", "nonzero_remainder_rejection": "PASS"}

def candidate_files(candidate: Path):
    names = sorted(p.name for p in candidate.iterdir() if p.is_file())
    if len(names) != 4 or "decision-v2.HEAD" not in names: fail("candidate_four_files")
    head_raw = (candidate / "decision-v2.HEAD").read_bytes(); head = json.loads(head_raw)
    if canonical(head) != head_raw or sha(head_raw) != EXPECTED_HEAD or head.get("schema") != DECISION_SCHEMA + ".head" or head.get("stem") != "decision-v2": fail("candidate_head")
    body_digest = head.get("body_sha256")
    if body_digest != EXPECTED_BODY: fail("candidate_body_digest")
    body_path = candidate / f"decision-v2.{body_digest}.json"; body_raw = body_path.read_bytes()
    if sha(body_raw) != body_digest: fail("candidate_body_hash")
    body = json.loads(body_raw)
    if canonical(body) != body_raw or body.get("schema") != DECISION_SCHEMA or body.get("terminal") != "GRADE1_DECISION_MEMBER": fail("candidate_body_schema")
    if body.get("prepare_sha256") != EXPECTED_PREPARE or body.get("producer_sha256") != V2_SHA or body.get("v3_producer_sha256") != V3_SHA: fail("candidate_pins")
    if body.get("logical_cursor") != 8059 or body.get("old_ranks") != [505, 503, 503, 503] or body.get("block_ranks") != [1509, 1512, 1512, 1512]: fail("candidate_counts")
    if body.get("old_logical_count") != 2014 or body.get("block_logical_count") != 6045 or body.get("lower_offer_count") != 2014 or body.get("lower_rank") != 1661 or body.get("grade_offer_count") != 6398 or body.get("grade_rank") != 5044: fail("candidate_ranks")
    bs = body.get("basis_receipt"); rs = body.get("remainder_receipt")
    if not isinstance(bs, dict) or bs.get("sha256") != EXPECTED_BASIS or bs.get("rows") != 5044 or bs.get("width") != PHYSICAL_GRADE or bs.get("bytes") != 5044 * (PHYSICAL_GRADE // 4): fail("candidate_basis_receipt")
    if not isinstance(rs, dict) or rs.get("sha256") != EXPECTED_REMAINDER or rs.get("rows") != 1 or rs.get("width") != PHYSICAL_GRADE or rs.get("bytes") != PHYSICAL_GRADE // 4: fail("candidate_remainder_receipt")
    for r in (bs, rs):
        if r.get("encoding") != "base3-four-trits-per-byte" or not re.fullmatch(r"[A-Za-z0-9_.-]+\.[0-9a-f]{64}\.bin", str(r.get("file"))) or not str(r["file"]).endswith(f".{r['sha256']}.bin"): fail("candidate_receipt_semantics")
    if body.get("block_sha256") is None or len(body["block_sha256"]) != 4 or any(not re.fullmatch(r"[0-9a-f]{64}", str(x)) for x in body["block_sha256"]): fail("candidate_block_digests")
    if not isinstance(body.get("member_coefficients"), list) or len(body["member_coefficients"]) != 3317: fail("candidate_coefficients")
    basis_path = candidate / bs["file"]; remainder_path = candidate / rs["file"]
    basis, remainder = basis_path.read_bytes(), remainder_path.read_bytes()
    if sha(basis) != EXPECTED_BASIS or sha(remainder) != EXPECTED_REMAINDER: fail("candidate_blob_hash")
    if len(basis) != bs["bytes"] or len(remainder) != rs["bytes"]: fail("candidate_blob_size")
    return body, basis, remainder

def validate_rows(packed: np.ndarray, leads, width: int, label: str):
    rows, row_bytes = len(leads), width // 4
    if packed.size != rows * row_bytes: fail(f"{label}_size")
    seen = set()
    for i, lead in enumerate(leads):
        if not isinstance(lead, int) or not 0 <= lead < width or lead in seen: fail(f"{label}_lead")
        seen.add(lead); row = packed[i * row_bytes:(i + 1) * row_bytes]; nz = np.flatnonzero(row)
        if not len(nz) or 4 * int(nz[0]) + int(PACKED_FIRST[int(row[int(nz[0])])]) != lead: fail(f"{label}_actual_lead")
        if IndependentOwner.coeff(row, lead) != 1: fail(f"{label}_normalization")

def load_source(state: Path):
    prepare, prepare_digest = read_sealed(state, "prepare")
    if prepare.get("phase") != "prepare" or prepare.get("fixture") is not False: fail("prepare_semantics")
    old = prepare.get("old_blocks"); packets = prepare.get("packets")
    if not isinstance(old, list) or len(old) != 4 or not isinstance(packets, list) or len(packets) != 4: fail("prepare_roster")
    residual_receipt = prepare.get("residual_blob")
    residual = read_blob(state, residual_receipt, 1, PHYSICAL_GRADE)
    old_rows = []
    for i, item in enumerate(old):
        rank = item.get("rank")
        if rank != [505, 503, 503, 503][i] or item.get("character_index") != i: fail("old_rank")
        low = read_blob(state, item.get("lower_basis_blob"), rank, LOWER_WIDTH)
        lift = read_blob(state, item.get("lifted_grade_blob"), rank, SOURCE_TOTAL)
        old_rows.append((rank, np.frombuffer(low, dtype=np.uint8).copy(), np.frombuffer(lift, dtype=np.uint8).copy(), i))
    blocks = []
    for i, expected_rank in enumerate((1509, 1512, 1512, 1512)):
        b, d = read_sealed(state, f"block-{i}", prepare_digest)
        if b.get("phase") != "block" or b.get("character_index") != i or b.get("parent_sha256") != prepare_digest or b.get("rank") != expected_rank or b.get("queue_exhausted") is not True: fail("block_semantics")
        leads = b.get("pivot_leads")
        if not isinstance(leads, list) or len(leads) != expected_rank: fail("block_leads")
        raw = read_blob(state, b.get("basis_blob"), expected_rank, SOURCE_BLOCK)
        mat = np.frombuffer(raw, dtype=np.uint8).copy(); validate_rows(mat, leads, SOURCE_BLOCK, f"block{i}")
        blocks.append((b, d, mat, leads))
    return prepare, prepare_digest, residual_receipt, residual, old_rows, blocks

def route(state: Path, candidate: Path, out: Path):
    started = time.monotonic()
    body, candidate_basis, candidate_remainder = candidate_files(candidate)
    prepare, prepare_digest, residual_receipt, residual, old_rows, blocks = load_source(state)
    if prepare_digest != EXPECTED_PREPARE: fail("prepare_digest")
    if body.get("block_sha256") != [x[1] for x in blocks]: fail("block_digest_binding")
    if body.get("residual_receipt") != residual_receipt: fail("residual_receipt_binding")
    if body.get("residual_sha256") != sha(unpack(np.frombuffer(residual, dtype=np.uint8), PHYSICAL_GRADE).tobytes()): fail("residual_hash_binding")
    ctx = Arithmetic(); lower = IndependentOwner(PHYSICAL_LOWER); grade = IndependentOwner(PHYSICAL_GRADE); companions = []
    logical = lower_offers = grade_offers = 0
    for rank, low_raw, lift_raw, character in old_rows:
        low_mat = low_raw.reshape(rank, LOWER_WIDTH // 4); lift_mat = lift_raw.reshape(rank, SOURCE_TOTAL // 4)
        for pivot in range(rank):
            lower_row = unpack(low_mat[pivot], LOWER_WIDTH); occurrence_lower = np.zeros((4, SOURCE_BASE), dtype=np.uint8); occurrence_lower[character] = lower_row[:SOURCE_BASE]
            occurrence_grade = unpack(lift_mat[pivot], SOURCE_TOTAL).reshape(4, SOURCE_BLOCK)
            physical_lower, physical_grade = aggregate_pair(ctx, occurrence_lower, occurrence_grade, lower_row[SOURCE_BASE:])
            lower_offers += 1; remainder, reductions = lower.reduce(pack(physical_lower)); companion = physical_grade.copy()
            for p, c in reductions: add_mod(companion, companions[p], -c)
            if np.any(remainder):
                accepted = lower.accept_reduced(remainder, reductions)
                if not accepted["accepted"] or accepted["reductions"] != reductions: fail("lower_accept")
                if accepted["scale"] == 2: companion = ((2 * companion.astype(np.uint16)) % 3).astype(np.uint8)
                companions.append(companion)
            else:
                grade_offers += 1; grade.insert(companion)
            logical += 1
            if logical % 256 == 0: guard(started); print(json.dumps({"progress": logical, "lower_rank": len(lower.rows), "grade_rank": len(grade.rows)}), flush=True)
    if logical != 2014 or len(lower.rows) != 1661: fail("old_route_counts")
    for block_index, (block_body, block_digest, raw, leads) in enumerate(blocks):
        rank = len(leads); mat = raw.reshape(rank, SOURCE_BLOCK // 4)
        for pivot in range(rank):
            grade_offers += 1; grade.insert(aggregate_pure(ctx, block_index, unpack(mat[pivot], SOURCE_BLOCK))); logical += 1
            if logical % 256 == 0: guard(started); print(json.dumps({"progress": logical, "lower_rank": len(lower.rows), "grade_rank": len(grade.rows)}), flush=True)
    if logical != 8059 or grade_offers != 6398 or len(grade.rows) != 5044: fail("route_counts")
    guard(started)
    routed_basis = grade.matrix_bytes()
    if sha(routed_basis) != EXPECTED_BASIS or routed_basis != candidate_basis or grade.leads != body.get("grade_pivot_leads"): fail("candidate_basis_mismatch")
    target = np.frombuffer(residual, dtype=np.uint8).copy(); remainder, coefficients = grade.reduce(target); candidate_remainder = np.frombuffer(candidate_remainder, dtype=np.uint8).copy()
    if np.any(remainder) or not np.array_equal(remainder, candidate_remainder) or coefficients != body.get("member_coefficients"): fail("target_reduction")
    reconstructed = np.zeros(PHYSICAL_GRADE // 4, dtype=np.uint8)
    for pivot, coefficient in coefficients: reconstructed = PACKED_AXPY[(3 - coefficient) % 3, reconstructed, grade.rows[pivot]]
    if not np.array_equal(reconstructed, target): fail("target_reconstruction")
    target_dense = unpack(target, PHYSICAL_GRADE)
    if sha(target) != residual_receipt["sha256"] or sha(target_dense.tobytes()) != body["residual_sha256"]: fail("target_hashes")
    if sha(candidate_remainder) != EXPECTED_REMAINDER or sha(candidate_remainder) != body["remainder_receipt"]["sha256"]: fail("remainder_hash")
    if out:
        verdict = {"basis_sha256": sha(routed_basis), "block_sha256": [x[1] for x in blocks], "candidate_body_sha256": EXPECTED_BODY, "candidate_remainder_sha256": sha(candidate_remainder), "coefficient_count": len(coefficients), "coefficient_sha256": sha(canonical(coefficients)), "cross_checked": False, "cursor": logical, "elapsed_seconds": time.monotonic() - started, "grade_offer_count": grade_offers, "grade_rank": len(grade.rows), "lead_sha256": sha(canonical(grade.leads)), "lower_offer_count": lower_offers, "lower_rank": len(lower.rows), "marker": MARKER, "prepare_sha256": prepare_digest, "remainder_sha256": sha(candidate_remainder), "residual_packed_sha256": sha(target), "residual_sha256": sha(target_dense.tobytes()), "verified": False}
        guard(started)
        out.write_bytes(canonical(verdict)); print(json.dumps(verdict, sort_keys=True), flush=True)
    return 0

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--state"); ap.add_argument("--candidate"); ap.add_argument("--out"); ap.add_argument("--selftest", action="store_true"); args = ap.parse_args()
    try:
        if args.selftest:
            print(json.dumps(selftest(), sort_keys=True)); return 0
        if not args.state or not args.candidate or not args.out: fail("usage")
        return route(Path(args.state), Path(args.candidate), Path(args.out))
    except Exception as exc:
        print(json.dumps({"status": "REJECTED", "error": str(exc)}), file=sys.stderr, flush=True); return 1
if __name__ == "__main__": raise SystemExit(main())

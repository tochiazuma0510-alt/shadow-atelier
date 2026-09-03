#!/usr/bin/env python3
"""Third-leg bounded check of the Task595 grade-one decision candidate.

Workshop-authored (falsifier).  Imports nothing from search/ or crosscheck/.
Format knowledge was taken by *reading* the checker's candidate_files/read_blob:
  basis blob   : rows x (width/4) bytes, each byte in [0,80], four base-3 trits
                 per byte, trit d of byte b = (b // 3**d) % 3, coordinate 4b+d
  remainder    : one packed row of 6048 bytes
  body JSON    : member_coefficients = ordered [[pivot, coeff], ...]
                 grade_pivot_leads   = [lead, ...] in insertion order
                 residual_receipt.sha256 = sha256 of the packed residual bytes
                 residual_sha256          = sha256 of the dense uint8 trit row
All arithmetic is integer (GF(3) by explicit % 3).
"""
import hashlib, json, sys, time
from pathlib import Path
import numpy as np

CAND = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "cand"
WIDTH = 24192
EXP = {
    "head": "07de7a817e8c5ae2e7346402a290c32631d05b0cc621d03702faa6cb43a948c0",
    "body": "62412762b3a208d31febb6c6b8d4707f880471ed32cf62c79c18108065ab7b5d",
    "basis": "b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d",
    "remainder": "564cbfafc869a8c6eb761a392caa5e792b546bf577af7fe808177b2fdf13cbb0",
    "residual_packed": "648696895595f479b6e2ccb65332589cf8a1a3bf4cf3f92be37e7910f72b79e6",
    "residual_dense": "5503afc98809a92f5734e8b1ac198b60eef33d9c4751658c79ad6c3927884134",
}
def sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def say(*a):
    print(*a, flush=True)

t0 = time.monotonic()
files = sorted(p for p in CAND.iterdir() if p.is_file())
say("files:", [p.name for p in files])
head_p = CAND / "decision-v2.HEAD"
head_raw = head_p.read_bytes(); head = json.loads(head_raw)
body_p = CAND / f"decision-v2.{head['body_sha256']}.json"
body_raw = body_p.read_bytes(); body = json.loads(body_raw)
basis_p = CAND / body["basis_receipt"]["file"]
rem_p = CAND / body["remainder_receipt"]["file"]
basis_raw = basis_p.read_bytes(); rem_raw = rem_p.read_bytes()

# ---------- (i) hashes ----------
got = {"head": sha(head_raw), "body": sha(body_raw), "basis": sha(basis_raw), "remainder": sha(rem_raw)}
for k in ("head", "body", "basis", "remainder"):
    say(f"(i) sha256 {k:9s} = {got[k]}  expected={EXP[k]}  match={got[k]==EXP[k]}")
say(f"(i) head.body_sha256 == body sha: {head['body_sha256']==got['body']}")
say(f"(i) sizes: body={len(body_raw)} basis={len(basis_raw)} remainder={len(rem_raw)}")
say(f"(i) body.terminal={body['terminal']} grade_rank={body['grade_rank']} lower_rank={body['lower_rank']} cursor={body['logical_cursor']}")
say(f"(i) body.residual_receipt.sha256={body['residual_receipt']['sha256']}  body.residual_sha256={body['residual_sha256']}")
say(f"(i) body.prepare_sha256={body['prepare_sha256']}")
say(f"(i) body.block_sha256={body['block_sha256']}")

# ---------- (ii) decode + rank ----------
rows = int(body["basis_receipt"]["rows"]); assert body["basis_receipt"]["width"] == WIDTH
assert len(basis_raw) == rows * WIDTH // 4, "basis size"
packed = np.frombuffer(basis_raw, dtype=np.uint8).reshape(rows, WIDTH // 4)
assert int(packed.max()) <= 80, "packed byte > 80"
TRITS = np.asarray([[(x // 3**d) % 3 for d in range(4)] for x in range(81)], dtype=np.uint8)
B = TRITS[packed].reshape(rows, WIDTH)          # dense trits, coordinate 4b+d
del packed
say(f"(ii) B shape={B.shape} dtype={B.dtype} nonzero={int(np.count_nonzero(B))} max={int(B.max())}")
nz_rows = (B != 0).any(axis=1)
assert bool(nz_rows.all()), "zero row in basis"
leads = np.argmax(B != 0, axis=1).astype(np.int64)
lead_vals = B[np.arange(rows), leads]
say(f"(ii) my leads: distinct={len(set(leads.tolist()))==rows} min={int(leads.min())} max={int(leads.max())} all_leading_coeff_1={bool((lead_vals==1).all())}")
say(f"(ii) my leads == body.grade_pivot_leads: {leads.tolist()==list(body['grade_pivot_leads'])}")
# echelon property: row j is zero at every lead strictly smaller than its own lead
order = np.argsort(leads, kind="stable")
S = B[order][:, leads[order]].astype(np.int16)   # rows sorted by lead, columns = sorted leads
below = np.tril(S, -1)
say(f"(ii) S=B[sorted rows][:, sorted leads] : unit diagonal={bool((np.diag(S)==1).all())} strictly-lower zero={int(np.count_nonzero(below))==0} upper nonzeros={int(np.count_nonzero(np.triu(S,1)))}")
# own forward GF(3) elimination on S (generic; no use of the triangular structure)
def gf3_forward_rank(M: np.ndarray) -> int:
    M = M.copy() % 3; r = 0; n, m = M.shape
    for c in range(m):
        if r == n: break
        col = M[r:, c]; nz = np.flatnonzero(col)
        if len(nz) == 0: continue
        p = r + int(nz[0])
        if p != r: M[[r, p]] = M[[p, r]]
        if M[r, c] == 2: M[r] = (2 * M[r]) % 3
        rest = nz[1:] + r
        if len(rest): M[rest] = (M[rest] - np.outer(M[rest, c], M[r])) % 3
        r += 1
    return r
t1 = time.monotonic(); rk = gf3_forward_rank(S); t2 = time.monotonic()
say(f"(ii) own GF(3) forward elimination on lead-column minor: rank={rk} of {rows} ({t2-t1:.1f}s) -> rank(B)>=rank(minor)={rk}, rank(B)<=rows={rows} => rank(B)={rk if rk==rows else 'UNDETERMINED'}")
# (a random full-width projection witness was removed: integer matmul is too slow here and the minor argument is already rigorous)

# ---------- (iii) sum of coefficients reconstructs the sealed residual ----------
co = body["member_coefficients"]
piv = np.asarray([c[0] for c in co], dtype=np.int64); cf = np.asarray([c[1] for c in co], dtype=np.int64)
say(f"(iii) coefficient list: n={len(co)} pivots distinct={len(set(piv.tolist()))==len(co)} in range={bool((piv>=0).all() and (piv<rows).all())} coeffs in {{1,2}}={bool(np.isin(cf,[1,2]).all())}")
lead_order_ok = bool(np.all(np.diff(leads[piv]) > 0))
say(f"(iii) coefficient list ordered by strictly increasing lead: {lead_order_ok}")
acc = (B[piv].astype(np.int64) * cf[:, None]).sum(axis=0) % 3
acc = acc.astype(np.uint8)
WEIGHTS = np.asarray((1, 3, 9, 27), dtype=np.int64)
acc_packed = (acc.reshape(-1, 4).astype(np.int64) * WEIGHTS).sum(axis=1).astype(np.uint8)
sp = sha(acc_packed.tobytes()); sd = sha(acc.tobytes())
say(f"(iii) sum_i c_i*B[i] : support={int(np.count_nonzero(acc))}")
say(f"(iii) packed sha256 = {sp}  expected residual_receipt.sha256={EXP['residual_packed']}  match={sp==EXP['residual_packed']}  (body says {body['residual_receipt']['sha256']==EXP['residual_packed']})")
say(f"(iii) dense  sha256 = {sd}  expected residual_sha256={EXP['residual_dense']}  match={sd==EXP['residual_dense']}  (body says {body['residual_sha256']==EXP['residual_dense']})")
# own reduction of the reconstructed target by B (increasing-lead scan) must return zero and the same ordered list
lead_to_row = {int(l): i for i, l in enumerate(leads.tolist())}
w = acc.astype(np.int64).copy(); mine = []; pos = 0
while True:
    nzw = np.flatnonzero(w[pos:])
    if len(nzw) == 0: break
    lead = pos + int(nzw[0]); i = lead_to_row.get(lead)
    if i is None: break
    c = int(w[lead]); w = (w - c * B[i].astype(np.int64)) % 3; mine.append([i, c]); pos = lead
say(f"(iii) own reduction: remainder support={int(np.count_nonzero(w))} n_coeffs={len(mine)} same ordered list as body={mine==co}")

# ---------- (iv) remainder blob ----------
rem = np.frombuffer(rem_raw, dtype=np.uint8)
say(f"(iv) remainder blob: bytes={len(rem_raw)} all_zero={not bool(rem.any())} body.remainder_support={body['remainder_support']} body.remainder_packed_support={body['remainder_packed_support']}")
say(f"(iv) sha256(zero 6048 bytes) = {sha(bytes(6048))}  == expected remainder sha: {sha(bytes(6048))==EXP['remainder']}")

say(f"elapsed {time.monotonic()-t0:.1f}s")
ok = all([got[k]==EXP[k] for k in ("head","body","basis","remainder")]) and rk==rows and sp==EXP['residual_packed'] and sd==EXP['residual_dense'] and not bool(rem.any()) and mine==co
say("THIRD_LEG_RESULT:", "AGREE" if ok else "DISAGREE")

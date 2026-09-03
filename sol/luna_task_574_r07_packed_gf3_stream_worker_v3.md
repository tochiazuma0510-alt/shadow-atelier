# Luna Task 574 — packed GF(3) stream worker v3, one bounded repair

Author: Sol / 2026-09-03

## 0. Role and hard scope

Implement one versioned v3 repair of Task572, using the complete independent
verdict `sol/sol_reply_573_audit_r07_packed_gf3_stream_worker_v2.md` as the
defect list.  This is a finite primitive/protocol repair.  Do not integrate it
into Task565, do not edit a workflow, do not dispatch GHA, and do not refactor
unrelated mathematics.

Write only:

1. `search/d972_packed_gf3_stream_worker_v3.c`
2. `search/d972_packed_gf3_stream_worker_v3.py`
3. `search/check_d972_packed_gf3_stream_worker_v3.py`
4. `sol/luna_reply_574_r07_packed_gf3_stream_worker_v3.md`

The v2 files remain frozen evidence.  No production result is claimed in
this task.

## 1. Production envelope is now smaller

The conditional paper cap in
`sol/proof_r07_associated_grade_cayley_fox_rank_cap_v454.md` reduces the
grade-two source envelope to:

```text
origins per character                 32,280
rank cap, trivial character            3,027
rank cap, each nontrivial character     3,025
offer cap, trivial                     44,388
offer cap, nontrivial                  44,380
primary width                          36,288 trits
companion width                        48,384 trits
```

Keep the worker generic and argument-bound, but include fixtures at these
shapes or scaled structural analogues.  Do not allocate against the obsolete
36,288-rank bound.  Treat v454 as conditional until independent audit; the
worker must still reject a caller-supplied rank cap larger than its safe
configured maximum.

## 2. Preserve the accepted algebraic core

Retain v2's packed four-trit GF(3) arithmetic, v4 reduction order, pivot
normalization, and positive coefficient convention:

```text
dependent: input = sum(q_i * basis_i)
accepted:  input = sum(q_i * basis_i) + scale * new_basis
```

Fix the live-service failure: before acknowledging an accepted row, install
its primary row, lead, opaque ID, and lead-map entry in memory.  In companion
mode install the companion row normalized by the same scale in a separate
accepted-pivot array.  Validate a pivot invariant once on acceptance or load,
not on every reduction edge.

Reduction happens before the rank-cap decision.  At full rank, dependent and
zero offers remain legal; only a genuinely new pivot returns
`UNKNOWN_RESOURCE`.

## 3. Use a fixed binary protocol, not ad-hoc JSON

Use checked little-endian fixed headers and length-delimited payloads for
stdin/stdout.  Every response must echo the input opaque `uint64` ID and give
one typed status:

```text
DEPENDENT | ACCEPTED | UNKNOWN_RESOURCE | MALFORMED | FATAL
```

For a dependent primary row return its ordered reduction pairs.  In companion
mode also return the exact dependent companion remainder.  For an accepted
row return lead, scale and pivot number, plus any reduction pairs.  The Python
wrapper must bind the echoed ID before exposing a result.  It must provide a
bounded iterator/accessor for returned companion bytes.

Malformed framing, short reads, invalid trits, duplicate live leads and I/O
errors are fail-closed; none may fall through with exit status zero.

## 4. Explicit checkpoint boundary

Per-offer fsync and whole-file rehash are forbidden.  Add an explicit
`CHECKPOINT` request.  Offers since the last checkpoint are provisional from
the durability point of view; the wrapper/outer driver may act on them in
memory but persists its queue only after the checkpoint acknowledgement.

At checkpoint:

1. flush/fsync changed data files;
2. publish a manifest temp file atomically;
3. fsync the containing directory on POSIX (and use the corresponding
   write-through publication on Windows where available); and
4. return checkpoint generation, committed offer count and manifest digest.

Maintain incremental SHA-256 contexts while the process is live; finalize a
copy at checkpoint.  On resume, scan each committed prefix once to authenticate
and rebuild the live contexts.  Never rescan every historical byte at every
offer or checkpoint.

Progress goes to inherited stderr, a caller-supplied log file, or a drained
reader.  Print only at a bounded cadence (default at least 256 offers or 15
seconds), never once per offer.  The wrapper must not create an unread pipe.

## 5. Exact persistent layout and resume

Use these invariants, or a byte-equivalent documented layout:

```text
basis.bin       = accepted primary rows only
companion.bin   = accepted companion rows only (absent outside companion mode)
leads.bin       = one {lead, opaque_id} record per accepted pivot
transcript.bin  = one response record per offered row
offsets.bin     = n+1 uint64 offsets for n transcript records
```

A fresh offsets file contains one zero EOF offset.  For one new transcript
record, use the old EOF as its start and append exactly one new EOF.  Thus the
sequences are `[0]`, `[0,E1]`, `[0,E1,E2]`, not two offsets per offer.

On resume:

- distinguish absent manifest (fresh allowed) from any present invalid,
  truncated, wrong-version or wrong-session manifest (fatal; never reset);
- require all count/cap/length equalities, including
  `basis_len=accepted*primary_row_bytes`, accepted lead/ID count, companion
  length, `offset_count=offers+1`, final offset equal transcript length, and
  counts within caps;
- hash exactly each committed prefix and compare it before truncating an
  uncommitted suffix; then durably truncate;
- rebuild primary and companion accepted bases, the lead map, accepted IDs,
  offer count and incremental hash contexts from committed state;
- seek every append stream to the authenticated committed end; and
- cross-bind each accepted transcript record to the same pivot's lead, ID,
  scale and basis row.

Do not keep fake `fifo_head/fifo_tail` fields in the service manifest.  Queue
ownership is in the outer deterministic driver.  A committed opaque ID must
be queryable so the driver can rebuild pending actor offers without replaying
committed work.  Replaying an uncommitted post-checkpoint offer is allowed;
replaying a committed offer is not required.

## 6. Transactional caps and portable C

Predict transcript, offset, basis, lead and companion byte consumption before
any write.  If a resource cap would be crossed, return `UNKNOWN_RESOURCE`
without changing live state or leaving a suffix.  Allocation failure is a
resource result; malformed input is not.  Any partial write must roll back to
the last in-memory offer boundary, or terminate fatally so resume truncates it
to the last committed checkpoint.

Fix all Task573 portability findings:

- native POSIX/Windows path joining inside the requested state directory;
- binary stdin/stdout on Windows;
- checked 64-bit file positions and truncation;
- explicit serialization of every manifest field, never pointer-walking
  across scalar struct members;
- checked numeric conversion with no ignored tail;
- every read/write/flush/checkpoint/close result checked; and
- atomic manifest publication with typed failure.

Linux GHA is the production platform.  Windows support need not be optimized,
but its binary and file-position behavior must not silently corrupt data.

## 7. Python wrapper

The wrapper must:

- use byte-oriented views without copying whole matrices;
- have no production timeout and no Python fallback;
- stream transcript authentication/iteration instead of `read_bytes()`;
- bind session, widths, caps, mode, generation, counts and echoed offer IDs;
- expose `checkpoint()` and validate its acknowledgement;
- drain/redirect/inherit progress output;
- expose dependent companion remainders; and
- make `close()` bounded by protocol EOF/process exit checks, reporting a
  fatal protocol error rather than hanging silently.

Fix v2's undefined `status` iterator path.  The dense reference helper must
index companion rows by accepted pivot, not offer position.

## 8. Independent checker and honest fixtures

The checker remains independent: dense GF(3), no import of the wrapper or C
implementation, no shared row helper.  If a C compiler is available, it must
actually compile and invoke v3.  If none is available, report
`COMPILED_SERVICE_NOT_RUN_NO_COMPILER`; do not print PASS for compiled paths.

When compiled execution is available, cover at minimum:

1. fresh two identical rows: first ACCEPTED, second DEPENDENT with the first
   pivot coefficient;
2. zero/one/two/many transcript offset boundaries;
3. a nonempty reduction response and opaque-ID echo;
4. dependent rows after the rank cap is full;
5. primary and companion accepted/dependent semantics;
6. explicit checkpoint, kill after committed offers, append a corrupt or
   incomplete uncommitted suffix, resume without replaying committed offers,
   and equality with one uninterrupted dense reference;
7. companion resume using an old pivot;
8. invalid present manifest rejected without modifying any state file;
9. committed-prefix corruption plus a longer suffix rejected;
10. predicted byte-cap rejection before mutation;
11. Linux state paths remain inside the state directory; and
12. bounded progress with no unread-stderr deadlock.

Apply rehashed semantic mutations, not only stale-hash mutations: transcript
opaque ID versus accepted ID, offer count, pivot/lead/scale, offset EOF,
companion accepted-row content, lengths/caps, and a valid-hash wrong session.
The checker must compare transcript record count with manifest offer count and
replay every fixture offer densely from the fixture's supplied input rows.

Also retain v2's six frozen arithmetic cases, deterministic random dense
cases, primary MEMBER/NONMEMBER and companion agreement.

## 9. Stop rule and report

Do not add SIMD, compression, SAT, alternate sparse formats, style cleanup or
Task565 integration.  The goal is the smallest correct persistent transducer
that closes Task573's finite failures under the smaller v454 envelope.

Run `py_compile` and every available bounded fixture.  Report exact commands,
wall time, compiler status, test counts, mutation counts, peak measured RSS
if compiled execution exists, file hashes and byte sizes.  End with exactly
one of:

```text
PACKED_GF3_STREAM_WORKER_V3_CANDIDATE_AUDIT_REQUIRED
PACKED_GF3_STREAM_WORKER_V3_NOT_READY
```

No grade-two production, A0, COMMON, cofinal-lift, fake or Ihara claim.

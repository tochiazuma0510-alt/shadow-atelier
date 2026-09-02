# Luna Task 572: persistent packed-GF(3) stream worker (v2)

Author: Sol / 2026-09-03

## 1. Role and objective

You are Luna, implementation support.  Replace the rejected Task567 one-shot
candidate by a new versioned v2 primitive which implements the exact streamed
transducer of repaired v452.  Read Task567, the complete Task569 failure
report, v452 at SHA-256
`754c5ae214ee48ad530948feb734a50395386e5bb1d8fe25daf0cedc6c3313c1`,
and Task570's complete audit before coding.

This task implements and exercises a bounded primitive only.  Do not modify or
wire Task565, v3/v4, any running workflow, certificate, v220 or provenance; do
not launch a real phase or GHA run.

## 2. Allowed outputs

Write only:

1. `search/d972_packed_gf3_stream_worker_v2.c`;
2. `search/d972_packed_gf3_stream_worker_v2.py`;
3. `search/check_d972_packed_gf3_stream_worker_v2.py`;
4. `sol/luna_reply_572_r07_packed_gf3_stream_worker_v2.md`.

Temporary states/builds/pycache belong outside the repository.  No git,
workflow edit, dispatch or local parallel Python.

## 3. Algebra and dynamic service contract

Use the frozen four-trits-per-byte encoding and exactly the v4 first-lead,
insertion-order pivot policy.  The C11 worker must be one persistent process
or a genuinely resumable append process: the caller offers a packed row, gets
its acceptance information before offering the next row, and may therefore
generate the four actor children of an accepted pivot dynamically.  Starting
a new process per row, replaying every prior row, or requiring a closed static
matrix is forbidden.

Each offer has a uint64 opaque ID.  Return or expose the complete ordered
reduction list, dependent/accepted status and, when accepted, pivot, lead,
leading coefficient and normalization scale.  The full expression is

```text
dependent: q
accepted:  q followed by (new_pivot, scale)
```

as in v452 (2.4).  Multiple nonzero trits in one byte, coefficient two, and
nonmonotone leads must exactly match v4.  Avoid the v1 aliased `memcpy`; all C
operations must have defined C11 behavior and checked integer/allocation/file
bounds.

## 4. File-backed binary transcript and memory

The production path retains only the accepted packed basis, lead map, one
work row, the current row's reductions, and bounded protocol buffers.  It must
not retain all offered rows or all historical reductions in memory.

Use versioned fixed-endian binary files for:

- normalized accepted rows in pivot order;
- leads and opaque accepted-row IDs;
- variable-length offer records;
- all record starts plus one EOF offset; and
- optional synchronized companion rows described below.

The small canonical manifest binds schema/version, field widths, parent/session
ID, ambient width, caps, accepted/offer counts, exact file lengths and SHA-256
values.  A checker must sequentially parse the transcript, recompute every
offset including EOF, enforce the exact opaque-ID order supplied by the caller,
and check chronological pivot references, coefficients and scales.  Decimal
arrays of basis bytes or coefficient pairs in JSON are forbidden.

Make rank, offers and transcript-byte caps explicit 64-bit inputs.  They must
accept at least the Task565 source envelope `(width=36288, rank=36288,
offers=177432, packed basis=329204736 bytes)` and physical envelope
`(width=48384, rank=48384, offers=153211)` without a static-input-size gate.
Cap exhaustion returns typed `UNKNOWN_RESOURCE`, never a mathematical
NONMEMBER.

## 5. Atomic checkpoint and real resume

Checkpoint only between offers.  It records committed basis/transcript/offset
prefix lengths, offer count, accepted count and caller FIFO cursor fields.  On
resume:

1. authenticate the manifest and every committed prefix;
2. reject or discard only an uncommitted suffix beyond the recorded lengths;
3. parse the complete committed transcript/offset structure;
4. validate every normalized accepted row/unique lead once and rebuild the
   lead-to-pivot map; and
5. continue from the next offer without replaying committed input rows.

Write the manifest through temp-file, flush/fsync and atomic rename.  A partial
receipt must never masquerade as a checkpoint.  Provide monotonically printed
progress suitable for unbuffered GHA logs.  The wrapper must not impose a
30-second production timeout and must never silently fall back to Python.

## 6. Synchronized companion mode

Support an optional packed companion width.  For an offered pair `(L,g)`, if
primary reduction records `(pivot,a)`, update both

```text
L <- L - a*L_pivot
g <- g - a*g_pivot.
```

When `L` is accepted, normalize and store both rows by the same primary scale.
When `L` is dependent, return/expose the resulting unscaled companion so a
caller can offer it to a second grade worker.  Bind both files and a shared
physical-offer ID.  This is the exact lower-first operation of v452 section 6;
do not decide what the caller does with the dependent companion.

## 7. Independent wrapper and checker

The wrapper accepts already-packed bytes, NumPy uint8 views, file slices or a
streaming iterator; it must not require dense Python integer lists.  It
authenticates small manifests and exposes one-record-at-a-time transcript
parsing.  Test-only reference code must be explicitly selected; production
must fail closed when the C executable is unavailable.

The checker must not import the wrapper/C or share packed algebra helpers.
Implement its expected linear algebra with genuinely dense GF(3) coordinates,
using packing only at the I/O boundary.  It independently checks complete
receipts, rows, expressions, chronological DAG semantics, offsets/EOF,
checkpoint prefixes and companion updates.

## 8. Mandatory bounded serial fixtures

Cover all of the following on the actual wrapper/service path when a compiler
is available, and on an explicitly labelled pure protocol/reference emulator
otherwise:

1. all six v4 frozen reducer cases and the chained three-row trace;
2. deterministic random matrices, zero/dependent rows, scale two, multiple
   trits in one byte and nonmonotone leads;
3. complete expression replay for every offered row and MEMBER/NONMEMBER-style
   target remainders (without making a membership claim);
4. dynamic closure: an accepted response is used to create later offers;
5. checkpoint after a nontrivial prefix, injected uncommitted tails, resume,
   and byte-identical equivalence with uninterrupted execution;
6. companion reduction, acceptance scaling and dependent companion handoff;
7. rejection of mutated basis byte, lead, row ID, coefficient, scale, offset,
   EOF, manifest hash, future pivot, duplicate lead, truncated files and wrong
   schema/version; and
8. bounded RSS/file-size and elapsed-time reporting.

If no compiler is present, run serial `py_compile` and all independent pure
protocol/parser fixtures, state `COMPILED_SERVICE_NOT_RUN_NO_COMPILER`, and do
not invent a speedup.  A later independent audit and GHA compiled calibration
remain mandatory.

## 9. Reply boundary

Record exact files, bytes, SHA-256, commands, runtimes, fixture counts, caps and
limitations.  End with exactly one verdict:

```text
PACKED_GF3_STREAM_WORKER_V2_CANDIDATE_AUDIT_REQUIRED
PACKED_GF3_STREAM_WORKER_V2_BLOCKED
```

State explicitly:

```text
TASK565 INTEGRATION: not performed
CURRENT GRADE-ONE RUNS: unchanged
GRADE-TWO PRODUCTION: not launched
MATHEMATICAL TERMINAL: none
verified=false
```


# Luna Task 577 — external-owner packed GF(3) worker v4

Author: Sol / 2026-09-03

## 0. Role, objective, and stop rule

You are Luna implementation support.  Implement the simpler split-owner
protocol proved in `sol/proof_r07_cap_bounded_external_owner_v455.md`.  Read
the complete Task576 audit first.  Do **not** patch the rejected v3 persistence
code: v4 has a deliberately different ownership boundary.

This is one bounded primitive implementation.  Do not integrate Task565, edit
a workflow, dispatch GHA, run a real grade, or modify v220/provenance.  If the
actual production path cannot be implemented within this task, return
`NOT_READY`; never substitute a reference emulator or hard-coded PASS label.

Write only:

1. `search/d972_external_owner_gf3_worker_v4.c`
2. `search/d972_external_owner_gf3_worker_v4.py`
3. `search/check_d972_external_owner_gf3_worker_v4.py`
4. `sol/luna_reply_577_r07_external_owner_stream_worker_v4.md`

Temporary builds/states/pycache go outside the repository.  No git operation
and no local parallel Python.

## 1. Frozen mathematical semantics and envelope

Use base-3 four-trits-per-byte encoding and the exact v4 first-lead,
insertion-order pivot policy.  Positive reduction coefficients satisfy

```text
dependent: input = sum(q_i * basis_i)
accepted:  input = sum(q_i * basis_i) + scale * new_basis
```

with `scale` equal to the original leading coefficient in `{1,2}`.  The
Task575-accepted first-rung cap is generic `rank_cap < 4096`; real grade two
uses:

```text
primary width             36,288 trits
companion width           48,384 trits
rank cap                  3,027 (trivial) / 3,025 (nontrivial)
offer cap                44,388 / 44,380
accepted matrices max    64,075,536 bytes together
```

Encode one reduction as little-endian uint16 `2*pivot + (coefficient-1)`.
Reject `rank_cap >= 4096`, a decoded future pivot, or a noncanonical value.

## 2. Hard ownership split

The C process owns **no durable write path**.  It must never append, hash,
fsync, rename, truncate, or authenticate state.  It owns only:

- normalized primary accepted rows;
- optional normalized companion accepted rows;
- unique leads and a lead-to-pivot map;
- accepted opaque IDs;
- one work row pair and one current reduction ledger; and
- logical offer/rank/byte counters needed for transactional caps.

The Python wrapper owns all durable state and checkpoint publication.  This
separation is load-bearing.  Do not recreate v3's mixed C/Python persistence.

On fresh startup C receives zero accepted rows.  On resume, after Python has
authenticated/truncated the state, C receives read-only paths plus exact
committed lengths/counts and loads the normalized basis, optional companion,
and `{lead,opaque_id}` records once.  It validates canonical packed bytes,
normalization, unique leads, row sizes, IDs, counts and caps and rebuilds the
map.  It reads no manifest itself and writes none of these files.

## 3. Fixed service protocol

Use checked fixed-endian binary request/response headers with magic, version,
op/status, echoed uint64 opaque ID, lengths and counters.  Support:

```text
OFFER
STATS
CLOSE
```

For each `OFFER`, read exactly one packed primary row and optional companion.
Reject short/extra/malformed framing and bytes above 80.  Reduce the primary;
apply exactly the same coefficients to the companion.

Before mutating the live basis, compute the exact logical durable-byte charge
for this response under Section 4.  Enforce rank, offer and total-byte caps
transactionally.  At full rank a row is reduced first: dependent remains a
valid `DEPENDENT`; only a genuinely new pivot is `UNKNOWN_RESOURCE`.  A cap
result changes no live row, map, counter, or durable file.

Return exactly one typed result:

- `DEPENDENT`: ordered compact reductions and the unscaled companion
  remainder when enabled;
- `ACCEPTED`: reductions, new pivot, lead, leading coefficient, scale, and
  the normalized primary and normalized companion rows;
- `UNKNOWN_RESOURCE`, `MALFORMED`, or `FATAL`: no mathematical terminal.

Install an accepted row, companion, lead and ID in memory **before** replying.
All allocation and arithmetic bounds must be checked.  Use defined C11
operations, binary stdin/stdout on Windows, strict integer parsing, and
bounded progress to inherited/redirected stderr (not per offer).  Response
writes and close must be checked; a broken pipe exits nonzero.

## 4. Python-owned durable format

The wrapper creates and exclusively writes:

```text
basis.bin       accepted normalized primary rows only
companion.bin   accepted normalized companion rows only, if enabled
leads.bin       one fixed {lead,opaque_id} per accepted pivot
transcript.bin  one versioned response record per successful offered row
offsets.bin     [0,E1,...,En], exactly n+1 uint64 values
manifest        one small versioned atomic commit record
```

The transcript uses the compact uint16 reductions, status-specific metadata,
and the opaque ID.  It does not duplicate accepted row bytes.  Decimal basis
or reduction arrays in JSON are forbidden; a scalar-only canonical JSON
manifest is allowed, though a fixed binary manifest is preferable.

For one successful response, validate the echo, status fields, pair ancestry,
lengths and normalized accepted rows before appending exactly one provisional
record/EOF and any accepted row.  Maintain incremental SHA-256 contexts while
live.  Do not reread/hash whole files per offer or per checkpoint.

`checkpoint()` is Python-only and occurs between offers:

1. compare wrapper counts with a C `STATS` response;
2. flush/fsync the five data files;
3. copy the incremental digests and write session/parent/input identities,
   encoding, widths/caps, generation, offers, accepted, last ID, exact lengths
   and digests to a temporary manifest;
4. fsync and atomically replace the manifest, with directory fsync on POSIX;
5. return the committed generation/count/digest.

On resume, distinguish no manifest (fresh) from an invalid present manifest
(fatal).  Bind all caller parameters.  Hash each committed prefix once,
reject corruption within it, then truncate only an uncommitted suffix.  Parse
the entire transcript and offsets sequentially; require one initial zero, one
EOF per offer, final EOF equal to transcript length, chronological pivots,
accepted rows/counts/leads/IDs/scales cross-bound, and exact file lengths.
Rebuild incremental hash contexts and the deterministic origins-first/FIFO
cursor from records, then start C on the authenticated accepted files.  No
committed offered row may be re-eliminated.

The wrapper has no production timeout, Python fallback, unread stderr pipe,
or whole-matrix copy.  `close()` checks the response, EOF and bounded process
exit.  A test-only dense reference must be explicitly named as such.

## 5. Deterministic cursor API

The durable layer need not store a second FIFO file.  Expose a streaming scan
which, given `origin_count` and actor order `(0,1,2,3)`, reconstructs:

- accepted pivot IDs in order;
- whether the origin phase is complete;
- the next FIFO pivot and actor index; and
- the unique expected next opaque offer ID.

Require at finalization

```text
offers = origin_count + 4*accepted
origin phase complete
FIFO exhausted
```

Do not claim v444/v451 completion merely on rank saturation; Task575 requires
all origin and four-per-pivot transition reductions for next-grade use.

## 6. Independent checker and honest fixtures

The checker must not import the wrapper/C or share algebra/state helpers.  Its
expected elimination is dense GF(3); packing is only at I/O boundaries.  When
a compiler is present it compiles and drives the **actual C + wrapper durable
path**.  When absent, print `COMPILED_SERVICE_NOT_RUN_NO_COMPILER`; pure
reference/parser tests must have separate labels and cannot imply compiled,
resume, RSS or persistence PASS.

Mandatory actual compiled-path cases:

1. all six frozen v4 reducer cases, coefficient two, multi-trit bytes,
   nonmonotone leads, zero/dependent, and deterministic random rows;
2. dynamic closure where an accepted row forms a later offer;
3. companion accept scaling and dependent handoff;
4. offsets after 0/1/2/many rows and complete expression replay;
5. checkpoint after a nontrivial prefix, hard-kill, append uncommitted suffixes,
   resume from the manifest without reoffering committed rows, and equality
   with uninterrupted dense reference;
6. committed basis/transcript/offset/companion/lead corruption rejected even
   with longer suffix, and invalid present manifest rejected without mutation;
7. rehashed semantic mutations of ID, lead, scale, coefficient, offset EOF,
   counts, valid-hash wrong session/config, future pivot and duplicate lead;
8. rank-cap dependent acceptance, offer cap and predicted byte-cap rejection
   before live or file mutation;
9. actual state lengths/digests and deterministic cursor/final equation; and
10. elapsed time, file sizes, peak RSS, bounded progress and clean close.

Never implement a mutation count using lambdas that deliberately throw, and
never print a PASS key for a path not executed.  The compiled fixture must
create its state directory and use exactly framed rows.

## 7. Bounded execution and reply

Run serial `py_compile` and all available seconds-scale fixtures.  Do not run
real-width elimination locally.  Report exact commands, measured runtimes,
compiler status, cases genuinely exercised, mutations genuinely rejected,
file sizes/hashes and remaining limitations.  End with exactly one verdict:

```text
EXTERNAL_OWNER_GF3_WORKER_V4_CANDIDATE_AUDIT_REQUIRED
EXTERNAL_OWNER_GF3_WORKER_V4_NOT_READY
```

Also state:

```text
TASK565 INTEGRATION: not performed
GRADE-TWO PRODUCTION: not launched
CURRENT GRADE-ONE GHA: unchanged
MATHEMATICAL TERMINAL: none
verified=false
```

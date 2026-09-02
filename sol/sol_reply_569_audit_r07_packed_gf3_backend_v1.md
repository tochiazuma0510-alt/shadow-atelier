PACKED_GF3_BACKEND_V1_AUDIT_FAIL

# Sol Reply 569 — independent audit of packed GF(3) backend v1

I read Task567 in full before inspecting its outputs and audited only the
bounded backend, wrapper, checker, and Task565 integration boundary requested
by Task569.  I did not inspect or run row 36/648, alter candidate code, run a
production computation, use git/GHA, or create a certificate.  The algebraic
kernel is sound modulo one portable-C defect, but the package is not a release
candidate: it has no real resume/incremental ABI, rejects the preregistered
Task565 scale, and its wrapper/checker do not fail closed on complete receipt
semantics.

## 1. Independently measured inputs

| input | bytes | SHA-256 |
|---|---:|---|
| `sol/luna_task_567_r07_packed_gf3_compiled_backend_v1.md` | 5,557 | `03af7296a894d4b768887fc67c059704801aa3bae90865393dc6aab370b5790e` |
| `search/d972_packed_gf3_echelon_backend_v1.c` | 10,593 | `5584c0de34e348935c64f641436bc8b43239b9da7ecdc21abf09f12ee3a511fd` |
| `search/d972_packed_gf3_echelon_backend_v1.py` | 10,645 | `53165193a3087e24e2d5eba3ea474d3aa58a7ab5df48fe08f3b9b8c658b14b51` |
| `search/check_d972_packed_gf3_echelon_backend_v1.py` | 14,120 | `161912fd2fe7ee4f071079a92f16609d072a2c4de31d33faf93d7258be54ad8c` |
| `sol/luna_reply_567_r07_packed_gf3_compiled_backend_v1.md` | 3,389 | `6e132d0736069d91b462b88cd3547f7caf15089c714c690ffe93f4643e0fc009` |

The three code-file measurements agree with Luna's report.  The closed reply's
previously unreported digest is recorded above.

## 2. Exact algebra and receipts

### 2.1 Algebraic core: conditional PASS; portable C execution: FAIL

The intended operation is exactly the v4 operation:

- C `trit`, `pack4`, and `axpy_byte` (lines 44--51) implement weights
  `(1,3,9,27)` and `a-cb` over GF(3), matching v4's tables at lines 617--634.
- `reduce` (C lines 72--85) selects the least nonzero trit, looks up its stored
  lead, appends the insertion-order pivot ID and actual coefficient, subtracts
  that pivot, and revisits the same byte.  Thus multiple live trits in one byte
  and nonmonotone pivot IDs follow v4 lines 684--703.
- `normalize` (C lines 88--95) records the pre-normalization leading
  coefficient and multiplies by two exactly when it is two, matching v4 lines
  705--731.  New pivot IDs are `accepted` in insertion order (C lines 139--141),
  independent of lead order.
- The receipt relation has v4's positive expression convention:
  `input = sum(coefficient * earlier_basis) + leading_coefficient * new_basis`
  for an accepted row, and omits the final term for a dependent row.  The target
  relation is `target = remainder + sum(coefficient * basis)`.  C lines 147--151
  expose the normalized basis, every ordered reduction, acceptance fields, and
  target remainder.

An independent dense-coordinate audit (no packed helper in the expected
calculation) agreed with the Python reference on every ordered pair of rows in
`F3^4` (6,561 cases), 250 deterministic cases at widths 4, 8, 12, 20, and 32,
and the exact chained Task562-style trace
`[[1,1],[0,2],[2,2]]`.  This supports the mathematics, but it does not execute
the C file.

There is a load-bearing portable-C defect at C line 74.  Both production call
sites pass identical pointers, `reduce(work, work, ...)` at line 136 and
`reduce(target, target, ...)` at line 145, after which line 74 calls
`memcpy(work,input,packed)`.  C11 7.24.2.1p2 `memcpy` has undefined behavior
for overlapping source and destination objects; identical nonempty ranges overlap.
The minimal execution witness is width 4 with one offered row: it reaches
`memcpy(p,p,1)` before any elimination.  A one-line guard or a distinct input
buffer is a local repair, but because every compiled row reaches it, it is a
correctness release blocker until repaired and compiled.

### 2.2 Suffix update: mathematical PASS

`row_invariant` (C lines 54--59) checks leading coefficient one and every
earlier trit zero.  It is enforced at insertion (line 138) and again before
each suffix AXPY (lines 82--84).  At a loop head, `cursor` is the least nonzero
byte of `work` (lines 75--79).  Therefore all work bytes before `cursor` are
zero, while the pivot invariant makes all pivot bytes before `cursor` zero.
The omitted full-row AXPY bytes are consequently `0-c*0=0`; starting at
`cursor` is byte-for-byte equal to the v4 full-row update.  Leaving `cursor`
unchanged after line 84 also proves the required repeated visit.

This proof applies to the only bases this v1 worker can possess: rows it has
just reduced, normalized, and checked.  There is no state-load path to which
the invariant would have to be extended.  Checker lines 193--211 provide a
packed suffix/full comparison, but not an independent dense proof.

### 2.3 Determinism and opaque IDs: single-run PASS; resume FAIL

Within a fresh run, C lines 132--142 consume rows in file order; lines 139--141
assign pivot IDs in acceptance order; and lines 148--151 emit bases, offered
records, and reduction pairs in deterministic order.  The uint64 row ID read at
line 135 is reproduced in both the offered record and, when accepted, the basis
record (lines 140, 148, 150).  Duplicate opaque IDs are preserved rather than
silently renumbered.

There is no resume boundary.  The CLI accepts only input/output/version/schema
(C lines 112--119), then always allocates an empty lead map (lines 127--128) and
rebuilds from row zero.  It cannot load a basis, lead map, ledger cursor, or
next-row boundary, and it emits no receipt until EOF.  The purported checker
gate at lines 230--236 merely copies a Python reference object's three lists.
Moreover, line 235 substitutes only `accepted_basis` into a newly recomputed
uninterrupted receipt; it does not compare the resumed second-half offered
records or a target reduced by `right`.  This is a load-bearing protocol
failure, not a cosmetic checkpoint omission.

### 2.4 Structural failure closure: C mostly PASS; wrapper FAIL

The C input side correctly checks CLI schema/version (line 119), magic and
header (lines 121--123), width/row and allocation products (lines 123--126),
packed bytes (lines 135 and 143), short reads, and trailing bytes (lines
134--145).  Lead indices are internally derived, duplicate leads are rejected
at line 138, and ledger reallocations/counters are bounded at lines 60--70.

Two local C robustness repairs remain.  Line 126 checks arithmetic for the
declared payload but, contrary to its comment, does not establish the actual
file length before allocation and processing.  Lines 146--152 write directly
to the final pathname; although `fclose` is checked, there is no temporary-file,
durability, and atomic-rename commit protocol, so interruption leaves a partial
receipt.  Data-processing failures also share exit code 2 and no diagnostic or
progress record.

The production wrapper is materially fail-open on receipt meaning:

- `_pairs` (Python lines 193--196) checks only nonnegative integers.  Offered
  pairs later receive a range check (lines 225--230), but target pairs do not
  (lines 236--238).
- Accepted records are not tied to the corresponding basis record or
  chronological accepted count; pivot, lead, leading coefficient, and scale
  are checked only for membership in broad ranges (lines 225--235).  It does
  not enforce `pivot == next accepted pivot`, matching row IDs/leads,
  `scale == inverse(leading_coefficient)`, or that reductions reference only
  earlier pivots.
- It does not bind offered count/order or any receipt content to the input
  file, and it does not replay rows or the target.  Any valid packed remainder
  is accepted (lines 239--241).
- `parse_receipt` reads and decodes the entire file before applying any size,
  basis-count, or total-ledger cap (lines 199--213).

On one valid four-row receipt, the wrapper accepted all eight independently
mutated false receipts: target pivot `999999`; wrong accepted pivot; wrong
accepted lead; scale 1 with leading coefficient 2; an accepted flag changed to
false; a first row reduced by a future pivot; a changed target remainder; and
deletion of an offered record.  Each is a small counterexample to the claimed
fail-closed complete parser.  These are load-bearing receipt/replay repairs.

### 2.5 Claim discipline: PASS

The C file claims only an echelon operation.  Wrapper lines 1--5 and 84--98
make the slow reference explicit and never silently fall back.  The Task567
reply also keeps source closure, PB gates, ancestry, MEMBER/NONMEMBER, and all
mathematical terminals outside this primitive.  That boundary is correct:
even after repair, MEMBER requires caller replay of every coefficient against
original rows, while NONMEMBER additionally requires a separately checked dual
annihilating the complete original roster and pairing nontrivially with the
target.

## 3. Independent checker audit and bounded rerun

The checker has no wrapper/C import: its imports at lines 7--18 are standard
library only.  That narrow independence gate passes.  The stronger required
gate does not.  `DenseReference` is not dense: it stores packed byte rows and
uses the same `pack`, packed `first`, packed-byte `axpy`, and `scale2` design at
lines 26--91.  The full-row comparison also shares that `axpy` helper.  Thus it
is a separately typed packed implementation, not a dense GF(3) reconstruction.

Other checker defects are concrete:

- `six_cases` (lines 168--177) resets the owner for six simplified cases; it
  does not replay Task562's one chained owner and exact stored matrices.
- With no compiler, lines 218--257 compare and mutate only objects made by the
  checker itself.  They do not exercise C or the production wrapper.
- Even if a compiler exists, lines 265--269 execute only the 32-by-20 random
  input, not all frozen/random/member/nonmember/resume/malformed gates.  A
  compiler found but returning a compile error is silently treated as
  `compiled=false` because line 263 has no failing `else`.
- The “resume” comparison is incomplete as described in section 2.3.
- Its validator accepted seven semantic mutations from the list above (all
  except the target out-of-range pivot), so its five chosen receipt mutations
  do not establish complete reconstruction.
- The alleged benchmark is only the Python construction of 32 width-20 rows
  (line 223).  The compiled branch records neither compiled elapsed time nor a
  speedup.  It therefore cannot satisfy the compiled benchmark gate later.

The prescribed bounded commands were rerun serially with bytecode outside the
repository:

```text
python -m py_compile search/d972_packed_gf3_echelon_backend_v1.py search/check_d972_packed_gf3_echelon_backend_v1.py
exit 0; outer wall 0.298661 s

python -B -u search/check_d972_packed_gf3_echelon_backend_v1.py
exit 0; outer wall 0.166609 s
```

Its exact result was:

```json
{"compiled": false, "compiled_status": "COMPILED_FIXTURE_NOT_RUN_NO_COMPILER", "compiler": "none", "elapsed_seconds": 0.053587, "fixture": "PASS", "frozen_cases": 6, "member_target": "PASS", "mutations_rejected": 7, "nonmember_remainder": "PASS", "random_rows": 32, "reference_benchmark_seconds": 0.003508, "resume_boundary": "PASS", "suffix_full": "PASS"}
```

`Get-Command` found none of `clang`, `clang-cl`, `gcc`, `cc`, `cl`, `zig`, or
`tcc`; `vswhere` found no x64 MSVC tool, and the checked common LLVM/MSYS2
paths were absent.  Hence no compiled execution or timing is reported.  The
compiled gate remains in addition to, not instead of, the static failures.

## 4. Memory, time, and Task565 viability

The C process has one positive memory property: it streams offered row bytes
(lines 132--142), retains only accepted packed basis rows, one work row, one
target, and receipts, and does not duplicate a full input matrix.  It invokes
one process per batch, not one process per pivot.

Its ABI bounds nevertheless exclude the intended job.  Task565 fixes packed
widths 9,072 and 12,096 bytes, per-character attempts at most 177,432, and
joint physical inputs at most 153,211.  C rejects more than 100,000 rows at
line 123.  More strongly, line 126 applies the 512 MiB cap to
`nrows*packed`, despite not retaining those input rows.  It therefore permits
at most 59,178 character rows or 44,384 physical rows.  The preregistered
ceilings are 1,609,663,104 and 1,853,240,256 input bytes respectively, both
rejected before processing.

The 10,000,000-entry ledger cap is also below the ABI worst cases
`177432*36288 = 6,438,652,416` and
`153211*48384 = 7,412,961,024`.  It is exhausted at averages of only 56.360
and 65.269 reductions per offered row.  C retains all reduction arrays until
the end (lines 60--70, 103, 149--151); on a conventional 64-bit ABI the logical
ledger alone is 160 MB, and geometric capacities have the safe bound
`< 2*ledger + 8*nonempty_rows` slots, about 333 MB at the stated caps.  Together
with at most 512 MiB of basis bytes and an 80 MB lead map, C itself is bounded
well below 8 GiB, but only by terminating before the Task565 envelope.

The Python boundary reintroduces the memory/time hazards:

- `write_input` requires a sized collection of dense built-in Python integers,
  validates all rows before packing, and has no streamed iterator/packed-row
  path (lines 33--81).  A four-trit `numpy.uint8` row—the native Task565 type—is
  already rejected with `BackendError:dense_row` because lines 39 and 54 insist
  on `type(x) is int`.
- `parse_receipt` simultaneously creates raw JSON bytes, a decoded string, and
  nested Python lists.  A 512 MiB packed basis alone needs roughly 4.29 GB of
  list slots, plus at least about 1.07 GB each for minimal one-digit/comma JSON
  bytes and its decoded string; ledger pair objects and caller state make an
  8-GiB peak likely.  There is no pre-parse cap or streaming parser.
- `run_compiled` has a fixed 30-second timeout (line 93), incompatible with a
  six-hour production phase.  C emits neither progress nor checkpoint, and its
  repeated `row_invariant` scan traverses every coordinate before each pivot
  AXPY (lines 54--57 and 83), adding another full-prefix scalar pass per
  reduction.

These are likely 8-GiB/6-hour blockers, not requested cosmetic work.  After
they are repaired, lookup tables for `first_trit`/AXPY and less verbose receipt
encoding would be optional optimizations subject to calibration; they are not
substitutes for correctness and streaming.

Task565 cannot call this backend once per streamed closure phase without
changing its row order or ancestry.  In Task565 lines 2262--2304, each accepted
pivot is queued and its four actor children are generated only after its
normalized row and pivot ID are known.  This worker consumes a closed file and
returns acceptance only after EOF, so the caller cannot construct that file.
Per-row processes would discard the basis; repeated prefix batches would be
quadratic and there is no resume import.  The lower-first merge at Task565
lines 2481--2505 likewise needs lower reductions before forming the paired
grade remainder.

The smallest viable integration is therefore a repaired v2 persistent
worker/library ABI, not a caller-only wiring change:

1. remove the aliased `memcpy`; add authenticated basis/lead/ledger state load
   and append, or an interactive persistent process that returns each offered
   record before accepting the next row;
2. accept streamed packed NumPy/file rows, use production-compatible caps, and
   write bounded binary/streamed ledgers with progress plus atomic checkpoints;
3. bind receipts to input/order and make the wrapper/checker replay every row,
   scale, chronological pivot reference, target remainder, and resumed state
   with an actually dense independent implementation;
4. have the Task565 adapter preserve the current origin-first then FIFO
   pivot/actor order via opaque attempt IDs, and run the lower owner before the
   grade owner while retaining the existing companion scaling; and
5. run all C fixtures and malformed-input gates, then a separate bounded GHA
   calibration.  Source closure, PB gates, final replay, and dual construction
   remain caller responsibilities.

No production or mathematical terminal follows from this audit.

CURRENT GRADE-ONE RUNS: unchanged

GRADE-TWO PRODUCTION: not launched

MATHEMATICAL TERMINAL: none

verified=false

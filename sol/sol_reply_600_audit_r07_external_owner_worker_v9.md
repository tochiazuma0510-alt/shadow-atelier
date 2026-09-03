# Task 600 - independent audit of external-owner worker v9

## Verdict

`PASS_AFTER_REPAIR`

The ownership/protocol design remains usable, but the frozen v9 trio is
**not statically ready** and must not be sent to a compiler/interop campaign in
its present form.  This is not a compiler-availability ruling.  The C worker
has a deterministic coefficient-one arithmetic error and frees its
session-owned ledger on both resource-cap paths.  The Python lifetime pump can
wait for 65,536 bytes or EOF before exposing an 88-byte response.  Independently,
the checker asserts that a request including its payload is exactly 88 bytes,
so every compiled direct/cap campaign stops before its first offer.

All four defects are finite local repairs; no worker redesign is needed.
Accordingly the conditional verdict is `PASS_AFTER_REPAIR`, while the status of
these exact v9 files is `NOT_READY`.

Current authorization boundary:

- compiler/interop evidence for v9: **NOT RUN**;
- GHA compiler/interop campaign for these hashes: **do not dispatch**;
- production integration or production run: **not authorized**.

## Frozen receipt

I read every numbered input in full.  The audited bytes are:

| file | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `sol/sol_task_600_audit_r07_external_owner_worker_v9.md` | 1,536 | 29 | `d0ca5c33a7f2f6a2ae4ef67ec7c750af8c50e729c573abf5b8e18c28ea5d457e` |
| `sol/sol_reply_591_audit_r07_external_owner_worker_v8.md` | 18,436 | 306 | `c9d9a1c482c93d1bc6570f448b1f1b69dd9b250c5c8380f0f2ef72a0e0f09844` |
| `sol/luna_task_596_r07_external_owner_worker_v9.md` | 2,890 | 55 | `3c38f21ff8035d7e66a194d399e9dc2685490565963311bf443cf2d4029d635f` |
| `search/d972_external_owner_gf3_worker_v9.c` | 14,515 | 236 | `628a939313cb6c48a3f46ffa8b0c930cd989b2da6f1d289cd931858cbc9a9b60` |
| `search/d972_external_owner_gf3_worker_v9.py` | 23,734 | 304 | `688787067c35b33ccc7d48dbb60bb2e418b5d1d75c394e686bea29b0d8d403b2` |
| `search/check_d972_external_owner_gf3_worker_v9.py` | 12,998 | 156 | `02f9a3eaf8f625c83ef19e4e4b19ff66b331cf8be9ffd80be0797e0b7a4d1a3c` |
| `sol/luna_reply_596_r07_external_owner_worker_v9.md` | 2,337 | 23 | `7a6aab402d5667e989244dc06800854370577d24595cb63fb4b5d79fdd7df638` |
| `sol/proof_r07_grade1_finite_roster_external_owner_cap_v462.md` | 6,669 | 160 | `cc51a9c25676565b31d63b691c77c50112501450eb2dfbf36104c79fb01fa5a5` |

## F1 - the packed C kernel is not GF(3) elimination

`init_tables` line 24 has three nested loops, but its coefficient-one entry is
computed from outer `a` and inner `b`, then stored at `SUB[1][b][c]`.  The
right operand `c` does not enter that computation, and every entry is
overwritten for all 81 values of outer `a`.  After initialization,

```text
SUB[1][left][right] = pack4( digits(80) - digits(left) ),
```

independently of `right`.  A direct witness is

```text
installed SUB[1][1][1] = 79
required  SUB[1][1][1] = 0.
```

Thus subtracting an identical pivot with coefficient one does not cancel its
lead.  The next pass can exhaust the rank-bounded ledger and return `FATAL`.
This is a semantic failure, not a performance concern and not something a
compiler can repair.

The exact repair is to index the table directly by
`coefficient,left,right`, computing
`SUB[1][left][right]=left-right` and
`SUB[2][left][right]=left-2*right` digitwise over GF(3).  Preserve the working
`SCALE2`, `FIRST`, packed-byte loop, monotone byte cursor, pivot order, and
companion update.  The repaired compiled campaign must include the existing
coefficient-one cancellation witness.

## F2 - cap handling still has the specified UAF/double-free

The one-ledger design is present: `LEDGER` is allocated once at lines 177--179
and each offer sets `q=LEDGER` at line 184.  Nevertheless, both unchanged-state
resource branches execute `free(q)` at lines 216 and 223 and then `continue`.
The next offer rebinds `q` to the freed global buffer and writes reduction pairs
through it.  Either cleanup at lines 232--235 frees `LEDGER` a second time.
Even `UNKNOWN_RESOURCE`, followed only by `STATS` and `CLOSE`, reaches the
double free on close.

Persistent counters, map, and basis are otherwise not changed on those cap
edges, and the immediate `continue` is correct.  The exact repair is therefore
small: a resource-cap branch must never free the session-owned ledger.  Emit
one zero-body, unchanged-counter `UNKNOWN_RESOURCE` and continue; free
`LEDGER` exactly once in the common service cleanup.

`write_full` at line 35 is also still one `fwrite`, not a full-write loop.
A short successful write leaves a frame prefix and returns failure.  Loop over
the remaining bytes until complete or a hard stream error.  This remains one
logical header write and one logical response-body write; it does not restore
per-pair writes.

Finally, the requested strict-warning cleanup was not performed: helpers at
lines 81, 84, and 87 retain `if (...) return 0; *z=...` on one line.  Split and
brace those conditionals before the strict build.  Compiler absence today is
not itself a defect, but known warning-prone source should not be delegated to
the first GHA result.

## F3 - owner transport and durable replay remain incomplete

The new queue and sole reader are the right shape, but the pump at line 177
calls `self.proc.stdout.read(65536)` on a buffered pipe.  Such a read may wait
to fill the requested size or see EOF.  The service flushes an 88-byte response
and remains alive, so construction can hang in its initial `STATS`.  A bounded
pipe witness on this host wrote and flushed 88 bytes while keeping the child
alive; after 0.5 seconds the `read(65536)` had returned no item, and it returned
the 88 bytes only after the child was killed.

Use `read1`, `os.read`, or an equivalent platform-safe partial pipe read in the
single lifetime pump.  In addition:

- `_request` lines 206 and 215 always use the default `deadline=None`; there is
  no session/request setting by which the checker can supply a deadline.  Add
  one optional checker deadline, pass the same absolute response deadline
  through header and body reads, and retain `None` as the production default.
- `_poison` sets a flag but `_request` never rejects a poisoned session.  It
  kills without a checked `wait`, does not close stdout or durable handles, and
  returns after a two-second join even if the sole reader is still alive.
  Timeout/error cleanup must kill and reap the worker, close both pipe ends and
  owner streams, join the sole reader, and make every later request fail before
  returning control.
- `_write` loops over reported file writes and advances digest/length only
  after its flush, which is good, but a zero/exceptional append merely raises.
  A partially appended five-stream transaction must poison/terminate the
  session.  `finalize` likewise needs a common success/error cleanup so an
  incomplete gate, malformed response, EOF error, or wait timeout cannot leak
  its process, pump, or durable files.

The offset vectors are now streamed with `previous/current` scalars and no
offer-sized list is retained.  However, `_parse_prefix` opens only transcript
and offsets once; lines 152--160 reopen and seek basis, companion, and leads
for every accepted record.  It also never rejects a primary byte above 80
before applying `first_lead`.  Open the present four/five streams once,
consume accepted rows and lead records sequentially in transcript/offset
lockstep, require exact EOFs, and check canonical primary and companion bytes,
normalized first lead, and lead/ID binding in that pass.

The remaining avoidable Python hot scan is `first_lead` lines 40--43, which
visits individual trits with division/exponentiation for every live and resumed
accepted row.  Use the same 81-entry packed-byte first-trit table as the C
worker (and a bulk/compiled canonical-byte test rather than generator work in
the live large-row path).  No dense row conversion, matrix copy, alternate
pivot order, or new data structure is needed.

The positive live-ID check, exact returned first-lead/lc/scale check, monotone
resume IDs, rank-bounded accepted-ID list, suffix resume from ID 5, immediate
kill return, exhausted `None` cursor fields, manifest replacement, and the
intended `CLOSE`/`CLOSED` field checks are present and should be preserved.

## F4 - the compiled checker path cannot run and does not prove Task591

The first compiled offer cannot pass checker line 56.  `WIRE.size` is 88, but
`data` already includes primary and companion payloads.  The direct fixture has
length `88+2+2=92`, and the cap fixture has length `88+3=91`; both are asserted
equal to 88.  Assert the header length separately and the complete frame as
`88+pn+cn`.

After that immediate defect, the following Task591 gates are still absent:

1. `exact` uses `select` followed by the same potentially filling buffered
   `read(n)`, and `select` on a Windows anonymous pipe is not portable.  Replace
   it with a lifetime/nonblocking exact reader.  Add a real timeout to
   `compile_worker`; for MSVC add strict warning-as-error flags rather than only
   `/std:c11`.
2. `direct_campaign` ignores its `campaign` argument and regenerates
   `campaign_rows`.  `parse_state` does not independently construct or
   whole-byte compare all five expected streams: accepted record
   pivot/lead/lc/scale are not compared with dense expectations, and record
   lead is only cross-bound to the equally mutable leads stream.  Decode the
   exact campaign bytes once, run an independent dense pass, construct exact
   transcript/offset/basis/companion/leads bytes, and compare each complete
   stream.
3. `cap_gate` checks only status and then kills the worker.  It never checks
   unchanged returned counters, sends `STATS`, or closes cleanly; consequently
   it hides the ledger double free.  Its offer-cap third row is `[1,1]`, already
   dependent on the first two pivots, rather than a genuinely new row.  Use a
   new lead, require literal `UNKNOWN_RESOURCE`, then literal `STATS`, exact
   unchanged state, `CLOSED`, stdout EOF, and exit zero for every cap case.
   `direct_campaign` also fails to assert literal `STATS` and `CLOSED` and does
   not check stdout EOF.
4. The four mutation loops run no clean-resume control and only count nonzero
   exits, without attributing the invariant.  The future pair is found by a raw
   scan rather than authenticated offsets; the lead-ID mutation flips ID 1 to
   zero rather than swapping two existing nonzero accepted IDs; and the basis
   byte mutation is not the requested coordinated record/leads lead change
   with the canonical basis row left unchanged.  Restore the four isolated
   mutations exactly as commissioned and assert each named rejection.
5. There are no raw partial-header, terminal malformed/noncanonical,
   compile-time test-only allocation-`FATAL`, fragmented-success,
   stalled-response, or short-response tests.  The production binary must not
   contain the allocation failpoint.  The hard-kill gate should also parse and
   identify the physical provisional offset/transcript records 5--6, rather
   than merely check that transcript length exceeds the committed fourth
   offset.

These are required evidence gates, not requests for broader fuzzing or a new
protocol.

## Exact bounded successor

Freeze v9 and make one v10 copy containing only F1--F4.  First perform a fresh
static audit.  If it passes, run one finite strict compiler/interop campaign on
GHA, with every compiled, raw-wire, durable, cap, mutation, close, cursor, and
hard-kill field reported honestly.  Compiler absence locally remains
`NOT_RUN_NO_COMPILER`; the dense-reference-only marker is not compiled or
interoperability evidence.

The v462 grade-one theorem does not alter this repair.  `MAX_RANK=4095` is the
narrower later-grade service contract audited here.  A distinct future
grade-one interface must admit the pinned rank cap 8,059 and use the finite
roster/two-owner schedule; that adapter is explicitly not implemented by v9
and must not be smuggled into this worker patch.

No A0, COMMON, cofinality, grade-one MEMBER/NONMEMBER, fake, or Ihara claim
follows.  `verified=false`.

```text
TASK600_EXTERNAL_OWNER_V9_STATIC: PASS_AFTER_REPAIR
FROZEN_V9_READY: NO
COMPILER_INTEROP: NOT_RUN_NO_COMPILER
NEXT: VERSIONED_V10_F1_F4_THEN_FRESH_STATIC_AUDIT
PRODUCTION: NOT_AUTHORIZED
```

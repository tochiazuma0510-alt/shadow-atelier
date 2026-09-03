# Task 610 - fresh static audit of external-owner worker v10

## Verdict

`PASS`

The exact v10 trio in the receipt below is statically ready for one bounded
GHA strict-compile/interop campaign.  I found no remaining Task600 F1--F4
blocker.  This is only a source/code-path ruling: the Task603 host had no C
compiler, I did not compile or execute the checker in this audit, and no
compiled or interoperability result exists yet for these hashes.

Authorization remains narrow:

- one compiler-present GHA campaign for the exact audited hashes: **ready**;
- production integration or a production calculation: **not authorized**;
- grade-one rank 8,059 adapter: **not implemented and out of scope**.

## Frozen receipt

I read the kickoff and every numbered input in full.  The three v10 source
hashes agree exactly with the Task603 receipt.

| file | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `sol/sol_task_610_audit_r07_external_owner_worker_v10.md` | 1,814 | 37 | `5e78ce92e71e465f8db556adcc1f538e57a6d5c9efc02159f3e15a2c9670d915` |
| `sol/sol_reply_600_audit_r07_external_owner_worker_v9.md` | 12,345 | 224 | `345b0cec56f692802108727c472a36dc43d1f3da794c87d5d75232251f01ae55` |
| `sol/luna_task_603_r07_external_owner_worker_v10.md` | 2,613 | 46 | `eb682db3406dbb9058e38ffa5662930187dc99d56c95387a0aeb27dfb2613def` |
| `search/d972_external_owner_gf3_worker_v10.c` | 22,449 | 763 | `8938bcdad693553266aeb08cfe023548fcb8d5965683157e60df564ea16681bd` |
| `search/d972_external_owner_gf3_worker_v10.py` | 38,121 | 1,026 | `3b6441063348987d101a9dc8ac019b2dcc85dee983f77342b821db710c00a16c` |
| `search/check_d972_external_owner_gf3_worker_v10.py` | 44,071 | 1,256 | `34016ce93096cfdc1e28735468a624016c6e53be6b39a1002adc1f07b9d44f63` |
| `sol/luna_reply_603_r07_external_owner_worker_v10.md` | 5,688 | 111 | `4497fa9db7f281c0f573f3756f08ee5543558f8ab2d019c089f8257084df33e1` |
| `sol/proof_r07_grade1_finite_roster_external_owner_cap_v462.md` | 6,669 | 160 | `cc51a9c25676565b31d63b691c77c50112501450eb2dfbf36104c79fb01fa5a5` |

## F1 - packed GF(3) arithmetic: closed

`init_tables` now constructs
`SUB[coefficient][left][right]` directly.  For coefficients 1 and 2 it
subtracts the corresponding right digit from each left digit modulo 3; the
coefficient-zero slice is the identity.  In particular the previous decisive
counterexample is repaired: `SUB[1][1][1]=0`.  `SCALE2` and the 81-entry
first-nonzero-trit table are separately and correctly populated.

The live reducer remains a packed-byte loop.  Its monotone byte cursor is
sound because an echelon pivot has no nonzero trit before its registered lead,
so subtracting that pivot cannot introduce an earlier lead.  Reduction-pair
codes remain lossless under the pinned `MAX_RANK=4095`, and primary and
companion rows use the same coefficient and normalization scale.

The checker has both required finite witnesses: its dense campaign makes ID 5
dependent after coefficient-one reductions, and the compiled one-byte gate
offers the identical packed row twice and requires the second response to be
`DEPENDENT` with exactly `[(0,1)]`.  Thus the decisive Task600 arithmetic
regression is no longer hidden behind the larger campaign.

## F2 - ledger, full writes, and cap state: closed

There is one session allocation of `LEDGER`; every offer merely aliases it as
`q`.  Neither the dependent nor independent `UNKNOWN_RESOURCE` edge frees it,
and both edges return immediately without changing offers, accepted rank,
logical bytes, map, or basis.  Each terminal cleanup path frees the ledger
once.  I found no remaining use-after-free or double-free path.

Both C response writes and Python durable writes advance in full-write loops.
Digest and declared length advance only after a complete durable append and
flush.  The previously warning-prone compact C conditionals are split, and
the checker requests warning-as-error compilation.

The three cap fixtures are load-bearing rather than cosmetic:

- rank cap: the rejected row has a genuinely new lead;
- offer cap: the rejected row is again genuinely new;
- byte cap after a pair: after accepting `e0`, `e0+e1` performs the
  coefficient-one pivot reduction and still has the new `e1` lead.  With the
  fixture's initial 8 bytes, the first accepted transaction reaches 91 bytes
  and the second would reach 176, exceeding its exact cap 175.

Every case requires literal `UNKNOWN_RESOURCE`, unchanged `(offers,accepted)
=(1,1)`, then literal `STATS`, literal `CLOSED`, stdout EOF, and exit zero.
Clean close therefore exercises the ledger lifetime that v9's kill-only cap
test concealed.

## F3 - transport, transactions, replay, and cursor: closed

The owner has one lifetime stdout pump.  It uses `read1(65536)` when available
and `os.read` otherwise; neither asks a buffered stream to fill 65,536 bytes
before publishing a short response.  A request computes one absolute response
deadline and passes that same value to both the 88-byte header read and the
body read.  The production default remains `None`, while the checker supplies
finite deadlines.

Poison is terminal.  Subsequent use is rejected, and forced shutdown kills
and reaps the child, closes both pipe ends, closes durable streams, and joins
the sole reader.  `_append_record` catches failure anywhere in its ordered
multi-stream append and poisons the session, so a partial physical transaction
cannot be reused as committed state.  The old manifest remains the commit
point and a later resume authenticates its prefixes before truncating any
provisional suffix.  `finalize` has a `finally` cleanup covering success and
every error edge.

Committed replay opens transcript, offsets, basis, optional companion, and
leads once in an `ExitStack` and consumes them sequentially in transcript/
offset lockstep.  It checks the declared end of every stream, canonical packed
bytes, normalized primary lead, coefficient one at that lead, record/lead
agreement, and opaque-ID binding.  The separate prefix-hash pass is required
authentication, not a per-record reopen.  Live and replay lead discovery use
the 81-entry packed-byte table; there is no per-trit Python lead scan.

The preserved protocol facts are all still present: positive and monotone
offer IDs, exact returned pivot/lead/lc/scale, rank-bounded accepted-ID state,
manifest replacement, suffix regeneration beginning at ID 5, exhausted cursor
fields all `None`, and exact `STATS`/`CLOSED` control fields.  The hard-kill
gate authenticates the committed four-offer manifest, parses physical offset
entries through offer 6, identifies provisional transcript records 5 and 6,
then requires resumed state to be whole-byte identical to a clean run.

## F4 - finite checker evidence: statically complete

Request construction now distinguishes the exact 88-byte header from the
complete `88+pn+cn` frame.  Both checker and owner use portable pump-backed
exact reads.  C compilation has a 60-second timeout and uses either
`-std=c11 -O2 -Wall -Wextra -Werror -pedantic` or
`/std:c11 /W4 /WX /TC`.

The supplied campaign bytes, rather than regenerated rows, feed an independent
dense GF(3) pass.  That pass constructs expected response metadata and exact
transcript, offsets, basis, companion, and leads images.  The compiled direct
campaign compares every response field, while durable execution compares all
five complete streams and their manifest lengths and hashes byte for byte.

Exactly the commissioned four semantic mutations are present, each with its
own clean-resume control and named rejection:

| isolated mutation | required rejection |
|---|---|
| authenticated-record reduction changed to the current/future pivot | `future_pivot` |
| two existing nonzero accepted IDs swapped in leads | `lead_binding` |
| one authenticated offset interval changed | `record_offset_binding` |
| accepted record and leads lead changed together, canonical basis left unchanged | `basis_binding` |

The remaining finite gates are also present: all 1--87 byte request-header
prefixes terminate with exit 6; malformed operation and noncanonical packed
byte 81 return terminal `MALFORMED`; a separately compiled test binary returns
terminal `FATAL` on accepted-row allocation; one complete 89-byte request is
sent in 89 one-byte fragments and succeeds; fragmented, stalled, and short
response fixtures exercise partial delivery, one-deadline poison cleanup, and
EOF poison cleanup.  The failpoint branch is preprocessor-guarded, the
production compile command has no failpoint define, and normal production
campaigns must accept rows; the special define occurs only in the test-binary
command.

## Performance audit

No Task600 repair reintroduces a material later-grade hot-path regression.
Elimination and normalization stay in the packed C kernel.  The owner makes
only a fixed number of one-row-sized immutable/wire copies per offer; it does
not convert live rows to dense trit lists, copy a basis or matrix, or perform
Python work per pivot trit.  Resume uses sequential open streams rather than
per-record reopen, and offset state is scalar while accepted IDs are
rank-bounded.  The C-level canonical-byte translation is a linear packed-byte
check, not a per-trit generator.  The only dense oracle is the fixed
16-offer, width-8 checker fixture.  The raw and mutation campaigns are exactly
the commissioned finite cases, not a fuzzing expansion.

## Exact bounded GHA gate

One workflow job may now run the following campaign, and only for the frozen
hashes above.  Give the job a finite outer timeout (15 minutes is sufficient
for the checker's stricter inner bounds), use a runner on which one supported C
compiler is definitely on `PATH`, and execute:

```text
python -B search/check_d972_external_owner_gf3_worker_v10.py
```

Exit zero alone is insufficient because the checker honestly exits zero with
`compiler=NONE`.  The workflow must parse the single JSON report and require:

1. `compiler != "NONE"`; both production and allocation-test strict compiles
   finish within their 60-second bounds.  The production command contains no
   `EOW_TEST_FAIL_ACCEPT_ALLOC`, the test command contains it exactly once,
   and `production_failpoint_define="ABSENT"`.
2. `version=10`, `wire_header_bytes=88`, `record_header_bytes=56`,
   `rank_contract=4095`, `grade1_rank_8059_adapter="OUT_OF_SCOPE"`,
   `production=false`, and `verified=false`.
3. `static_source="PASS"`, `dense_reference="PASS"`, `offers=16`,
   `accepted_reference=3`, and
   `dense_coefficient_one_witness="ID5_DEPENDENT_AFTER_C1_C1"`.
4. The expected five-stream SHA-256 values are exactly:

   ```text
   basis.bin      29cb9adc78f3170a94efdf7d017a6e171929186d761281b99005473f4790ac12
   companion.bin  351ea4ae333c69e88e860823d5bbc4df2e165020fc47f755d318b3a6ddab9f7a
   transcript.bin e668ea9177aca442e3adf6be177246d5581fbea0737912ea52172dc473f1c1ab
   offsets.bin    5d9363ec924b847008bdd68a724b3bd7a1980c2439938219d2b898513a5e3d30
   leads.bin      0c63c9bdd21f44653a6c359796aafab772898febbadb5413a0f22738d6c39a30
   ```

5. The compiled direct campaign reports 16 offers, 3 accepted, exact `STATS`,
   and `CLOSED`/EOF/exit-zero; the separate coefficient-one cancellation gate
   reports `CANCELS_TO_ZERO`; `five_stream_image`,
   `literal_stats_closed_eof`, and `cursor_finalize` are `PASS`.
6. All three cap entries are
   `UNKNOWN_UNCHANGED_STATS_CLOSED_EOF_EXIT0`; partial-header evidence says
   `cases=87`, range `[1,87]`, and exit 6; malformed and noncanonical entries
   are `MALFORMED_EOF_EXIT6`; allocation failure is
   `TEST_ONLY_FATAL_EOF_EXIT6`; fragmented request reports 89 frame bytes, 89
   fragments, and `ACCEPTED_CLOSED`.
7. Owner transport fixtures report the exact 81-entry table pass,
   fragmented-response pass, stalled-response
   `DEADLINE_POISON_REAP_CLOSE_JOIN`, short-response
   `EOF_POISON_REAP_CLOSE_JOIN`, and poisoned-session reuse `REJECTED`.
8. Hard-kill evidence reports committed offers 4, physical provisional IDs
   `[5,6]`, and 7 physical offsets; suffix resume is `PASS`.  Mutation evidence
   reports four clean controls and exactly the four named rejection reasons in
   the table above.
9. Every compiled/interop field is populated--none may be
   `NOT_RUN_NO_COMPILER`--and the terminal field is `interoperability="PASS"`.

The workflow receipt should record the run ID and exact commit SHA.  A failed
field is evidence for a new versioned repair, not permission to weaken or skip
the gate.

The v462 finite-roster theorem does not enlarge this ruling.  Its rank-8,059
two-owner schedule remains a separate future interface; v10 deliberately
retains the later-grade rank-4,095 contract.  No grade membership, A0, COMMON,
cofinality, fake, or Ihara claim follows.

```text
TASK610_EXTERNAL_OWNER_V10_STATIC: PASS
EXACT_V10_READY_FOR_ONE_BOUNDED_GHA_CAMPAIGN: YES
STRICT_COMPILE_AND_INTEROP: NOT_RUN
PRODUCTION: NOT_AUTHORIZED
verified=false
```

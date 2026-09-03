# Sol(max) Task750: P1 checker state-head v4 hostile audit

## Decision

All six requested finite release checks pass.  Checker v4 makes the exact
state-head schema repair diagnosed from run/attempt `33814881435/1`, exercises
it with an independently spelled positive fixture and an old-schema negative
fixture, and leaves the producer binding, body schema, replay arithmetic,
receipt validation, and CLI unchanged.  It is safe to run the checker alone
against the original six producer receipts and five immutable Task554 parent
roots.

This is a code-release ruling only.  I did not rerun any large parent, inspect
row-36/nonarithmetic typing, reopen the accepted P1 mathematics, run GHA, use
git, or edit implementation/workflow files.

## Exact audited bytes

All listed files have zero CR bytes, are LF-only, and end in byte `0a`.

| path | bytes | LF bytes | final LF | SHA-256 |
|---|---:|---:|:---:|---|
| `sol/sol_task_750_audit_r07_p1_checker_state_head_v4.txt` | 2,002 | 47 | yes | `43be397f7d3ad8e20f1dc15bb57c7db4b09a7ef0138f290bb3cdc90f0cb4deb0` |
| `sol/proof_r07_p1_checker_state_head_schema_repair_v493.md` | 2,414 | 80 | yes | `2feb9f83135cc4af234dfc7110128b2636fb12bd82e920ce3bdab19b02fddf5b` |
| `sol/luna_task_749_r07_p1_checker_state_head_v4.md` | 2,563 | 62 | yes | `c114c98fb9994c59977683ed19d043ad48a1007325cd7e67d8804f2d1f92459f` |
| `sol/luna_reply_749_r07_p1_checker_state_head_v4.md` | 3,340 | 71 | yes | `2d93e8e576633d5b8d5bfc9434c266266054c89ff0a808dec782493bb8b0a316` |
| `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v3.py` | 130,683 | 2,689 | yes | `3cfdbe0485711b9b4a08db2d664ded7719a126e3a499724d33cd122a101e774e` |
| `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v4.py` | 132,129 | 2,719 | yes | `cc9a27e8ab447ecd6e4fbebbd1240195e442d6c5eb14241a5f9d7c669154ee19` |
| `search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py` | 41,619 | 382 | yes | `dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf` |

The measured checker-v4 size, newline count, final LF, and SHA-256 exactly
match Luna's release receipt.

## F750-1: complete v3-to-v4 executable diff — PASS

The complete direct unified source diff has exactly three hunks:

1. add the sole top-level assignment
   `SEALED_HEAD_SCHEMA = "d972.r07.a0.first-rung-grade1.v3.state.head"`;
2. in `read_sealed`, replace only
   `"schema": STATE_SCHEMA + ".head"` by
   `"schema": SEALED_HEAD_SCHEMA`;
3. extend only `selftest`: create a dedicated `sealed` temporary subdirectory,
   define `write_fixture_head`, positively read one prepare and four block
   heads, mutate prepare to the old `...v3.head` schema and require rejection,
   record one live-kernel/acceptance item, and move the pre-existing safe-root
   toy file into its own `toy` subdirectory so its exact roster stays isolated.

An independent AST comparison gives:

```text
function roster:                         identical
changed functions:                       read_sealed, selftest
all other function ASTs:                 identical
added top-level assignments:             SEALED_HEAD_SCHEMA only
removed top-level assignments:           none
changed common top-level assignments:    none
import roster:                            identical
```

Thus the above is the complete executable delta; there is no unreported
release change.

## F750-2: head/body schema separation and all five routes — PASS

The corrected literal occurs in checker v4 exactly twice: once as the
production `SEALED_HEAD_SCHEMA` value and once as the independently spelled
positive fixture literal.  `read_sealed` constructs its exact four-key head
object with `SEALED_HEAD_SCHEMA`; the old `STATE_SCHEMA + ".head"` expression
does not remain anywhere.

The production call graph remains:

```text
authenticate_prepare
  -> read_sealed(safe, "prepare", PREPARE_DIGEST, None)

run_actual_check, for each index 0,1,2,3
  -> replay_block
     -> authenticate_block
        -> read_sealed(safe, f"block-{index}", PARENTS[index], PREPARE_DIGEST)
```

These are the only production `read_sealed` call sites.  Therefore prepare and
all four blocks use the corrected literal through one exact gate.

`STATE_SCHEMA` itself is byte-for-byte unchanged at
`d972.r07.a0.first-rung-grade1.v3`.  The unchanged `validate_prepare_body` and
`validate_block_body` functions still require `body["schema"] == STATE_SCHEMA`.
The rest of `read_sealed` is also unchanged: canonical bytes, exact head key
set and value equality, body filename, body canonicality, and body SHA-256 all
remain mandatory.  Safe-root and exact-roster production checks are unchanged.

## F750-3: independent positive fixture and old-schema rejection — PASS

The entire v4 `selftest` source contains zero references to
`SEALED_HEAD_SCHEMA`.  Its writer instead spells the authenticated literal
`d972.r07.a0.first-rung-grade1.v3.state.head` directly.  It writes canonical
head/body pairs and calls the live `read_sealed` once for prepare and once in
each iteration of `range(4)` for block 0 through block 3.  Thus a mistake in
the production expression cannot automatically make the positive fixture
agree.

The same fixture then changes only prepare's schema to the independently
spelled old value `d972.r07.a0.first-rung-grade1.v3.head`, rewrites canonical
JSON, and passes it back to live `read_sealed` under `expect_reject`.

Besides reading the source, I ran a separate bounded probe whose serializer,
literal, and SHA calculation were defined outside the checker.  It obtained:

```text
positive heads accepted: prepare, block-0, block-1, block-2, block-3
positive_count=5
old schema result=REJECT
old schema exact reason=sealed_head:prepare
```

This independently confirms both directions and the shared prepare/block
production gate.

## F750-4: noninterference and production cost — PASS

The imports are unchanged standard-library modules plus NumPy; there is no
producer import, `importlib`, module loader, `__import__`, `exec`, `eval`, or
`runpy` call in checker v4.  `PRODUCER_V5_SOURCE` and `PRODUCER_V5_SHA` are
AST-identical to v3, and the pinned value
`dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf`
equals the measured producer-v5 bytes.  The producer is still read only as
bytes for provenance.

In particular, the following v3/v4 function ASTs are identical:

```text
validate_prepare_body, validate_block_body
authenticate_prepare, authenticate_block
replay_prepare, replay_block_kernel, replay_block
validate_peer_prepare, validate_peer_block, validate_join_receipt
compare_semantic_receipts, validate_obligation_totals, validate_producer_chain
run_actual_check, parse_args, validate_cli, main
```

This covers the arithmetic, equality-LF route, projector, packet/DAG replay,
six-receipt validation, claim flags, resource caps, result construction, and
all CLI branches.  There is no weakened check or new shared oracle: production
uses the new constant while the fixture deliberately uses its own literal.

No added source line contains a NumPy dense allocation or any thread, process,
executor, concurrency, retry, wait, or sleep mechanism.  All file creation and
extra reads are confined to `--selftest` and use tiny temporary JSON objects.
The only production operation change is replacing a short string concatenation
with a constant lookup.  No resident copy, parallel local work, or slower
production path was introduced, and no unrelated hardening is requested.

## F750-5: bounded compile and selftest — PASS

Bytecode was directed outside the repository to
`C:\Users\81905\AppData\Local\Temp\task750-pycache-ffa7e0b19634421f9e1e7d702890ec3a`.
The exact commands were:

```powershell
$env:PYTHONPYCACHEPREFIX = 'C:\Users\81905\AppData\Local\Temp\task750-pycache-ffa7e0b19634421f9e1e7d702890ec3a'
python -m py_compile crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v4.py
python -B crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v4.py --selftest
```

Results:

```text
py_compile exit=0
selftest exit=0
status=PASS
fixture_accept=7
rejections=42
live_kernels includes sealed_head_schema
actual_five_artifact_check=DEFERRED_TO_GHA
verified=false
```

All 38 named `rejection_table` entries are `REJECT`; the new head-schema
rejection is counted separately, explaining the v3-to-v4 total increase from
41 to 42.  No checker `--check` mode or real parent was run locally.

## F750-6: checker-only GHA reuse — PASS

No precise dependency requires rebuilding the successful producer phases.
Checker v4 retains the exact producer-v5 path/SHA pin, Task554 source ancestry,
five parent digests, basis pins, receipt schemas, phase counts, join schema,
and CLI.  Its repaired head gate consumes the existing immutable state heads;
it does not alter or request new parent or producer bytes.

The unchanged actual route accepts five parent roots plus the original prepare,
four block, and join receipt paths.  It authenticates producer v5, independently
replays the five parents, validates all six producer receipts, compares the
semantic families, and records SHA-256 of each raw receipt before emitting its
atomic result.  Hence a checker-only job may stage the five immutable Task554
parents and the six exact receipts from `33814881435/1` and invoke checker v4.

The new workflow/result envelope must, as stated in v493, bind the original
run/attempt/current-head evidence and checker-v4 source hash.  That is dispatch
provenance, not a reason to regenerate the producer receipts.  This audit did
not inspect or authorize any workflow-file modification.

Until that actual checker-only run succeeds, P1 has producer success but not an
independently cross-checked semantic terminal.  No downstream claim is promoted.

```text
REAL_FIVE_ARTIFACT_CHECKER=NOT_RUN
P1_PRODUCER_SIX_PHASES=ACTUAL_SUCCESS
P1_SEMANTIC_REPLAY=PRODUCER_SUCCESS_CHECKER_PENDING
P1_SEMANTICS_CROSS_CHECKED=NO
A0/COMMON/COFINAL/FAKE/IHARA=NOT_DECLARED
verified=false
```

VERDICT=PASS_P1_CHECKER_STATE_HEAD_V4_SAFE_FOR_GHA
SAFE_TO_DISPATCH_CHECKER_ONLY_GHA=yes

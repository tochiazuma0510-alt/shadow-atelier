# Sol Task776 — hostile audit of canonical P1 lift v6 runtime repair

## Ruling

**PASS for dispatch, with the proposed root-cause attribution rejected.**
V6 is an arithmetic-neutral diagnostic/hardening revision and workflow v3 is
internally consistent.  It is safe to dispatch because another ordinary
production exception will carry both a retained build phase and a bounded
traceback tail.  It is **not** established that the packet-row conversion
caused run `33824881796/1`; the observed causal timeline excludes that line.

I read every commissioned input, both producers, both workflows, and every
file in the extracted log directory.  I did not read a production parent,
run the full lift, use GHA/network/delegation, or perform a high-memory replay.

## 1. Exact byte boundary and differential result

All four files have zero CR and NUL bytes and end in LF.

| file | bytes | LF | SHA-256 |
|---|---:|---:|---|
| producer v5 | 104,788 | 2,231 | `32ee4c536e0f5289a13bcd71723bfc6cfc8bd52f074008b78ba2acaca7d6466b` |
| producer v6 | 105,983 | 2,257 | `e83f6fca9643905b935b73b8dcaea51effbe08f6a9549523478227d3ec85bc62` |
| workflow v2 | 27,574 | 497 | `be01039bf16bdb917d717979b4b309d3bebb1a6f60b9ccf95a5e17b8a1715d20` |
| workflow v3 | 27,574 | 497 | `ac5d47c2e8b709af96b2ebc3e9fef60d4844f3014efef26806b69c06b14c40c1` |

The producer text delta is exactly 34 inserted and 8 deleted lines, with
2,223 unchanged lines.  At top-level AST granularity it adds only the
`runtime_phase` function and changes exactly `validate_launch_manifest`,
`build`, `fixture_receipt_validation`, and `main`.  Imports differ only by
adding `traceback`; module assignments are AST-identical except for the new
`RUNTIME_PHASE` state.

All arithmetic and storage definitions inspected below are byte-for-byte AST
equal between v5 and v6:

- `validate_node`, `validate_expression`, `validate_actor_order`,
  `validate_defect_origins`, and `validate_authenticated_dag`;
- `add_full`, `scale_full`, `flatten_p1`, `full_from`, `expected_p1`,
  `recurse_node`, `projected_seed`, `compile_packet_v486`, and
  `compile_old_defect`;
- `raw_component_digest`, `full_row_digest`, `reduction_digests`, and
  `make_instruction`;
- `PackedCache`, `InstructionSink`, `LazyP1`, and `instruction_receipt`.

After removing the nine phase-label calls and normalizing only the launch and
candidate schema versions, the producer executable key, and the single
packet-byte spelling, the complete `build` ASTs are equal.  Thus row counts
and order, the four old/new loops, DAG origins, ordered reductions, scale,
P1 gate, packed cache, checkpoints, resource enforcement, authentication,
and all false claim flags are unchanged.  The schema/key substitutions are
the necessary `launch.v4 -> launch.v5`, candidate `v4 -> v5`, and
`producer_v5 -> producer_v6` provenance changes.

`ARITHMETIC_AST_UNCHANGED=yes`.

## 2. The actual causal timeline refutes the Luna diagnosis

The changed expression is inside a defect-origin branch of the **new-row**
loop.  Control cannot reach it until all four old blocks, totalling 2,014
rows, have completed.  Each successful old row appends exactly once, then
writes its instruction, and the unchanged code calls `checkpoint` whenever
the cursor is divisible by 128.  Reaching the new-row loop therefore implies
that the fifteen old checkpoints at cursors

```text
128, 256, ..., 1920
```

have already executed.  Each checkpoint prints with `flush=True`.  Workflow
v2 additionally used Python `-u`, `stdbuf`, and `tee`, with stdout and stderr
merged into the preserved `build.log`.

The extracted `build.log` is exactly 91 bytes, one LF, and contains only:

```json
{"status":"REJECTED","error":"object supporting the buffer API required","verified":false}
```

There is no checkpoint line to reconcile with reaching the packet branch.
Deleting the temporary candidate in `finally` cannot delete a line already
written through `tee`.  Consequently the modified packet expression did not
cause the recorded failure.  A failure during authentication, lazy-P1
opening, an early old row's surrounding receipt/cache work, or the first
checkpoint remains possible; the old one-line terminal cannot distinguish
these.

Root's actual-data replay of character-0 rows 0 through 127 in 15.452 s
further excludes a deterministic failure of those old DAG arithmetic/P1
steps.  It does not by itself replay every authentication, instruction,
cache-sync, and cleanup operation, so it does not prove an alternative root
cause.

There is also no type argument supporting Luna's claimed call site.  V5 calls
`sha(bytes(packet[...]))`; if `sha` is reached, its argument is already a
built-in `bytes` object.  In an independent bounded control under Python
3.13.14 and the workflow-pinned NumPy 2.5.1, a C-contiguous `uint8` memmap row
of the actual packed-row width 4,536 gave

```text
bytes(row) == row.tobytes(order="C")
len = 4536
SHA-256 digests equal
```

The v6 spelling is therefore harmless, deterministic hardening of a single
row receipt and adds no semantic change, but its comment about a
runtime-dependent old conversion is not a demonstrated diagnosis of this
run.  `ROOT_CAUSE_PROVED=no`.

## 3. Exception observability and cleanup masking

V6 sets a string phase before authentication, words, context, lazy-P1
opening, every old row, every packet open and new row, the stream terminal,
and final receipts.  The general `except Exception` formats the fully unwound
exception, retains its final 8,192 characters, and emits only JSON-native
values: strings plus `verified=false`.  `json.dumps` therefore cannot reject
the payload on the audited path; its default ASCII escaping also makes
non-ASCII exception text safe for stderr.

The stream cleanup can replace a primary exception with the first exception
from instruction, cache, or P1-store close.  This does not reintroduce the
opaque failure:

- no cleanup operation resets `RUNTIME_PHASE`, so the exact character/row (or
  the preceding named build phase) remains available;
- raising the saved close exception while the primary exception is active
  preserves the primary exception as Python traceback context;
- the outer `main` handler runs only after all `build` cleanup has unwound, so
  it observes the replacement and its context;
- `shutil.rmtree(..., ignore_errors=True)` cannot replace that exception.

A bounded injected control with primary `ValueError("primary-buffer-site")`
and masking `OSError("cleanup-close-site")` returned exit 1 and valid JSON.
It retained phase `build.old[3].row[502]`, both exception texts in a
427-character traceback, the masking error in `error`, and
`verified=false`.

A 20,000-character ordinary `RuntimeError` also returned parseable JSON with
an exactly 8,192-character `traceback_tail`.  The 8,192 limit is a character
limit on that field, not a limit on the complete serialized record: `error`
is intentionally still untruncated, and ASCII escaping can expand serialized
bytes.  This distinction does not make the result opaque or defeat the
commissioned traceback bound.  The real CLI `--build` missing-argument
control likewise returned exit 1 with phase `startup`, traceback call sites,
`error="build_arguments"`, and `verified=false`.

`ResourceStop` and `KeyboardInterrupt` remain deliberately separate
`UNKNOWN_RESOURCE` exits.  Every `ResourceStop` construction in this build
has an explicit fixed resource reason (and old/new/terminal where relevant),
so it is not the opaque ordinary `REJECTED` class at issue.  For ordinary
exceptions on the actual build path, a second one-line message without a
phase/call site is prevented.

`SECOND_OPAQUE_FAILURE_PREVENTED=yes`.

## 4. Workflow v3

The workflow delta is exactly 16 insertions and 16 deletions.  Reversing the
mechanical v3 identifiers, producer path/hash/size/LF, launch and candidate
schemas, executable key, fire token, and artifact names makes workflow v3
byte-for-byte equal to v2.

- There is one job, 17 sequential steps, no matrix or strategy, and no retry
  or parallel lift producer.
- The fire token
  `[fire-r07-canonical-p1-degree2-lift-v3]` occurs exactly once; the v2 token
  is absent.
- All ten action uses have full 40-hex pins.  All eight local source
  path/hash/byte/LF pins match the current exact files.
- Producer v6, launch schema `...launch.v5`, executable key `producer_v6`,
  final manifest schema `...lift.v5`, and the candidate gate agree.  No v5
  producer path or key remains.
- Checker-v5 result/workflow receipt/success-artifact pins and the six exact
  producer receipt hashes are unchanged.  The source run and all five parent
  artifact identities are unchanged and still authenticated before use.
- All four inline Python programs parse.  The staged checker roster remains
  exact and canonical; the launch manifest preserves checker and raw-parent
  provenance.
- The internal cap remains 2,220 seconds, the producer wrapper remains 38
  minutes, the job remains 45 minutes, and
  `D972_LIFT_MAX_RSS=7516192768` remains the 7-GiB gate under the unchanged
  `ulimit -v 8388608` KiB process ceiling.
- The candidate artifact remains `if: success()` and logs remain
  `if: always()`.

## 5. Bounded controls, performance, and claim boundary

All generated test material was outside the repository under `%TEMP%`.

| control | result |
|---|---|
| external-pycache `py_compile` of v6 | exit 0; 0.228 s |
| v6 `--selftest` | exit 0; 1.190 s; `fixture_accept=6`, `rejections=50`, forbidden calls empty |
| v5/v6 top-level, critical-function, and normalized-build AST comparison | PASS |
| memmap old/new conversion at actual row width | equal bytes and digest |
| masking-exception, long-traceback, and CLI-error controls | all valid fail-closed JSON as detailed above |
| workflow normalization, BaseLoader parse, four inline ASTs, action/local pins, seriality and gates | PASS |

The production-path additions allocate only short phase strings and, on
failure, traceback text.  The changed packet operation materializes the same
single 4,536-byte row that `bytes(...)` already materialized.  There is no new
dense owner, matrix copy, duplicate parse, full-file pass, parent replay, or
heavy selftest.  The selftest still says
`"actual_replay":"DEFERRED_TO_GHA"` and `"verified":false`.

This ruling authorizes only a fresh candidate-producing dispatch with better
failure evidence.  It neither treats the v2 runtime failure as repaired nor
claims an 8,059-row result, canonical P1 lift, A0/common/cofinal conclusion,
fake/Ihara conclusion, or Lean verification.

```text
VERDICT=PASS_CANONICAL_P1_LIFT_V6_RUNTIME_REPAIR
SAFE_TO_DISPATCH_GHA=yes
ARITHMETIC_AST_UNCHANGED=yes
ROOT_CAUSE_PROVED=no
SECOND_OPAQUE_FAILURE_PREVENTED=yes
CANONICAL_P1_LIFT=NOT_CLAIMED
FAKE_IHARA=NOT_CLAIMED
verified=false
```

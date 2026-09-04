# Sol Task769 — narrow hostile re-audit of the canonical P1 lift v5 clock repair

## Ruling

**PASS.**  The sole Task764 release blocker is closed.  The fixed historical
receipt is not rewritten: workflow v2 stages its exact 2,310 bytes at SHA-256
`323ca2603b9ff7c42449fc0e2421c190eedcd7cd62471b695dee991fb1b728eb`,
and v5 admits its one-field
`checker_process.elapsed_wall_clock="03.76"` through the same production
`validate_checker_workflow_receipt` call that precedes cache allocation.

The v4-to-v5 executable delta contains only that clock admission, bounded
fixtures, and the mechanically necessary version/provenance plumbing.  There
is no arithmetic, cache, instruction, resource, parent-pin, or claim-boundary
drift.  Workflow v2 is internally consistent and dispatchable.

I read all eight commissioned inputs completely and processed all six audit
obligations.  I did not run GHA, read a real parent or artifact, run the
8,059-row lift, use git/es7ops, or invoke another agent.

## 1. Exact byte boundary

Every file below has zero CR bytes and a final LF.

| file | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `sol/sol_task_769_reaudit_r07_canonical_p1_lift_v5_clock_repair.txt` | 2,426 | 50 | `64d4542a26c5e157f36378a02268c559bba4a39238f3975aa3876c61326ddde4` |
| `sol/sol_task_764_audit_r07_canonical_p1_degree2_lift_v4_workflow_v1.txt` | 4,619 | 88 | `e58dce44cd666f840ad762601aa4b3c068fca0c1d5c2c493f69ba3b22d5f4e99` |
| `sol/sol_reply_764_audit_r07_canonical_p1_degree2_lift_v4_workflow_v1.md` | 15,532 | 329 | `478c2b171973b0f6b21a4378b03b41a8fbcefd2a8947a0afe911ff117956762c` |
| `sol/luna_task_767_r07_canonical_p1_lift_elapsed_clock_repair_v1.md` | 3,013 | 72 | `0ccaf72a842b617f0793050d90bcc37fa116a700c1bb6f66b436e2cb2819bd08` |
| `sol/luna_reply_767_r07_canonical_p1_lift_elapsed_clock_repair_v1.md` | 6,417 | 156 | `4f75c285d9228345d69e433e7e3cb2230a8cc2329f28e558642813baafb9f256` |
| `search/d972_r07_canonical_p1_dag_degree2_lift_v4.py` | 104,313 | 2,222 | `68c690f18a495793b295c35f8bd9a9286485b8bd141fb3a31d2ed9de36591b8b` |
| `search/d972_r07_canonical_p1_dag_degree2_lift_v5.py` | 104,788 | 2,231 | `32ee4c536e0f5289a13bcd71723bfc6cfc8bd52f074008b78ba2acaca7d6466b` |
| `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v1.yml` | 27,574 | 497 | `80d36642a162b329a4b9d1288e4840ef6e8f736d087fa0a0909bd6af51a16c21` |
| `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v2.yml` | 27,574 | 497 | `be01039bf16bdb917d717979b4b309d3bebb1a6f60b9ccf95a5e17b8a1715d20` |

## 2. Exact historical receipt reaches the production gate

The reachability chain is exact and contains no normalization step:

1. Workflow v2 ties the checker download to run `33819301663`, artifact
   `9918207444`, its exact name, 24,694 API bytes, digest, successful run, and
   head SHA.  Its recursive staging code permits exactly eight regular files.
2. For `workflow-receipt.json`, staging requires exactly 2,310 bytes and the
   accepted raw SHA above, checks canonical ASCII JSON plus final LF, and
   copies the unchanged raw bytes.
3. `authenticate_inputs` calls `canonical_file`, recomputes that raw SHA, and
   requires `CHECKER_WORKFLOW_RECEIPT_SHA` before calling
   `validate_checker_workflow_receipt` at v5 line 1231.
4. `build` calls `authenticate_inputs` at line 1428.  The `PackedCache`
   constructor is not reached until line 1447.  Thus the clock gate is on the
   actual production path and is completed before allocating the
   292,444,992-byte cache.

The differential proof is decisive.  Task764's exact accepted receipt reached
this validator and failed at only
`checker_process_elapsed_shape`.  Between v4 and v5, the ASTs of both
`authenticate_inputs` and `validate_checker_workflow_receipt` are exactly
equal; the called parser changes only

```python
len(fields) in (2, 3)
```

to

```python
len(fields) in (1, 2, 3)
```

All receipt pins and all checks following the clock call are unchanged.  An
independent executable trace of `fixture_receipt_validation` recorded its
first clock call as

```text
('03.76', 'validate_checker_workflow_receipt')
```

and returned `accepted=3, rejected=33`.  Direct comparison gives

```text
v4 validate_elapsed_clock("03.76")  REJECT checker_process_elapsed_shape
v5 validate_elapsed_clock("03.76")  ACCEPT
```

This closes the actual Task764 path; it is not merely an isolated parser test
or a regenerated receipt test.

## 3. Clock grammar and negative cases

V5 implements the retained numeric grammar correctly:

- one field is seconds, two fields are an unrestricted nonnegative integral
  minute field plus seconds, and three fields are nonnegative integral hours,
  a minute field below 60, and seconds;
- in every shape, seconds must be finite and satisfy `0 <= seconds < 60`;
- `03.76`, `0`, `59.999`, `0:00.01`, `12:59.5`, `1:02:03.50`, and
  `0:59:59.999` all passed;
- non-string values, empty, `not-a-number`, `nan`, `NaN`, `inf`, and `-inf`
  were rejected;
- `-0.01` was rejected as negative;
- `60`, `60.0`, `0:60`, `0:60.0`, and `0:00:60` were rejected by the seconds
  range, while `0:60:00` was rejected by the three-field minute range;
- `0::01` and `0:x:01` were rejected as malformed fields, and
  `0:00:00:01` was rejected as a four-field shape.

The accepted receipt is raw-SHA pinned, so no broader spelling can be
substituted into this release path.  No grammar redesign is warranted.

## 4. Exact v4-to-v5 AST delta

The textual delta is exactly 18 insertions and 9 deletions.  Top-level AST
comparison found no added or removed function or class, no changed class, no
changed module assignment, and identical imports.  Exactly five functions
change:

- `load_dependencies`: only the collision-avoidance module name advances from
  `task761_checker_v5` to `task767_checker_v5`; checker bytes remain pinned;
- `validate_elapsed_clock`: only the one-field admission above;
- `validate_launch_manifest`: launch schema `v3 -> v4` and executable key
  `producer_v4 -> producer_v5`;
- `build`: final schema `v3 -> v4` and the same executable-key advance;
- `fixture_receipt_validation`: exact `03.76` full-validator witness, retained
  two/three-field positives, clock negatives, and matching fixture versions.

All four loops in `build` are AST-identical.  The full ASTs of
`validate_node`, `validate_expression`, `validate_actor_order`,
`validate_defect_origins`, `validate_authenticated_dag`, `add_full`,
`scale_full`, `flatten_p1`, `full_from`, `recurse_node`, `projected_seed`,
`compile_packet_v486`, `compile_old_defect`, `reduction_digests`,
`make_instruction`, and `instruction_receipt` are equal.  Every class,
including `PackedCache`, `InstructionSink`, and `LazyP1`, is equal.

Module assignments are AST-identical, so the following are unchanged:

```text
rows/order       8059; 0,505,1008,1511,2014,3523,5035,6547,8059
characters       (0,0),(0,1),(1,0),(1,1)
actors           1,-1,2,-2
row bytes/cache  36288; 292444992
```

The six degree-two monomials, old/new ranks, packet projection, ordered
reduction recurrence, packed-cache format, instruction ancestry/output,
accepted checker/result/receipt and parent/artifact pins, forbidden-call set,
and all false claim flags are likewise unchanged.  The Task764 raw-body
retention remains exactly as before and is explicitly nonblocking here.

`ARITHMETIC_AST_UNCHANGED=yes`.

## 5. Workflow v2

BaseLoader YAML parsing succeeded.  All four inline Python heredocs parse as
Python.  V1-to-v2 is an exact 16-insertion/16-deletion mechanical diff: only
the workflow/fire/executable versions, v5 local pin, launch/final schemas,
producer key, and output artifact names change.

- The exact fire token
  `[fire-r07-canonical-p1-degree2-lift-v2]` occurs once; the v1 token is absent.
- There is one job and 17 sequential steps, with no matrix, strategy,
  concurrency, retry, added lift-checker execution, or connection pass.
- All 10 action uses have complete 40-hex pins.
- All eight locally authenticated source pins match live bytes:

| source | bytes | LF | SHA-256 |
|---|---:|---:|---|
| producer v5 | 104,788 | 2,231 | `32ee4c536e0f5289a13bcd71723bfc6cfc8bd52f074008b78ba2acaca7d6466b` |
| checker v5 | 133,318 | 2,740 | `bc60882b3ee22aa449c51cc280491b3d66df384a814a7033e418454f66900f97` |
| grade1 v4 | 144,552 | 3,326 | `1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4` |
| prebuild v1 | 145,917 | 3,499 | `acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8` |
| semantic v5 | 41,619 | 382 | `dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf` |
| structural v1 | 47,995 | 545 | `38fcbe3757d1b14fd19f4f557f763c1f5f6a2e8da47e0e061707cf28c5064d73` |
| floor v1 | 26,235 | 508 | `6201ae0b5c1d648529ac648a574c5096b8088fe341423724556860d9d3f23fba` |
| words JSON | 115,928 | 0 | `90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893` |

The staging roster is exactly `independent-result.json`,
`workflow-receipt.json`, prepare, four blocks, and join.  It recursively
rejects symlinks, extra/missing files, duplicate basenames, wrong raw hashes,
wrong fixed sizes, and noncanonical JSON.

Workflow launch schema `...launch.v4`, v5's launch validator, final manifest
schema `...lift.v4`, and the workflow's final gate agree.  Checker
`CHECKER_SCHEMA`/`MARKER`, the independent terminal, and the candidate status
gate are unchanged and remain tied to the exact checker-v5 hash.  The
human-readable launch step name still contains `v3`; its executable schema
literal is `v4`, so the label has no release semantics and is not a blocker.

The caps are unchanged and coherent: `D972_LIFT_SECONDS=2220` (37 minutes), a
38-minute outer timeout, a 45-minute job timeout, `ulimit -v 8388608` KiB
(8 GiB), and `D972_LIFT_MAX_RSS=7516192768` bytes (7 GiB).  The success
artifact remains success-only and diagnostics remain `always()` uploaded.

## 6. Bounded checks and claim boundary

All test-generated material was outside the repository under
`C:\Users\81905\AppData\Local\Temp\sol-task769-audit-a0d1f8d6c39e49529438bab4f07190b6`.
No audit process was left running.

| check | result | elapsed |
|---|---|---:|
| external-pycache `py_compile` | exit 0 | 0.265397 s |
| v5 `--selftest` | exit 0; `fixture_accept=6`, `rejections=50`, forbidden calls empty | 3.020019 s |
| direct grammar plus full-validator caller trace | all expected outcomes; exact `03.76` caller witnessed | 0.462933 s |
| v4/v5 text, top-level AST, critical arithmetic AST, and four-loop comparison | PASS | 0.108087 s |
| workflow YAML, four inline ASTs, source/action pins, roster, seriality, and caps | PASS | 0.044426 s |

The selftest terminal retains
`"actual_replay":"DEFERRED_TO_GHA"` and `"verified":false`.  This audit
authorizes only dispatch of the candidate-producing workflow.  It makes no
actual lift, connection, grade-two terminal, A0/COMMON/cofinal/fake/Ihara, or
Lean-verification claim.

VERDICT=PASS_CANONICAL_P1_LIFT_V5_CLOCK_REPAIR
SAFE_TO_DISPATCH_GHA=yes
ARITHMETIC_AST_UNCHANGED=yes
ACTUAL_8059_ROW_LIFT_REPLAY=NOT_RUN
verified=false

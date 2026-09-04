# Luna Task767 - canonical P1 lift elapsed-clock repair

## Result

The single Task764 reachability defect is repaired in a versioned producer and
workflow.  The exact accepted raw receipt remains unchanged at 2,310 bytes,
SHA-256
`323ca2603b9ff7c42449fc0e2421c190eedcd7cd62471b695dee991fb1b728eb`.
Its historical `checker_process.elapsed_wall_clock="03.76"` now reaches and
passes the same `validate_checker_workflow_receipt` production validator used
before cache allocation.

Only the three commissioned outputs were created:

- `search/d972_r07_canonical_p1_dag_degree2_lift_v5.py`
- `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v2.yml`
- `sol/luna_reply_767_r07_canonical_p1_lift_elapsed_clock_repair_v1.md`

No real parent or accepted artifact was read, no 8,059-row replay was run, no
GHA workflow was dispatched, and no git/es7ops/agent operation was used.

## Exact byte boundary

Every measured file below has zero CR bytes and a final LF.

| path | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_canonical_p1_dag_degree2_lift_v4.py` | 104,313 | 2,222 | `68c690f18a495793b295c35f8bd9a9286485b8bd141fb3a31d2ed9de36591b8b` |
| `search/d972_r07_canonical_p1_dag_degree2_lift_v5.py` | 104,788 | 2,231 | `32ee4c536e0f5289a13bcd71723bfc6cfc8bd52f074008b78ba2acaca7d6466b` |
| `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v1.yml` | 27,574 | 497 | `80d36642a162b329a4b9d1288e4840ef6e8f736d087fa0a0909bd6af51a16c21` |
| `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v2.yml` | 27,574 | 497 | `be01039bf16bdb917d717979b4b309d3bebb1a6f60b9ccf95a5e17b8a1715d20` |

The v4-to-v5 textual delta is 18 insertions and 9 deletions.  The workflow
v1-to-v2 delta is 16 insertions and 16 deletions.

## One-function repair

`validate_elapsed_clock` now accepts one, two, or three colon-separated fields.
The existing numeric conversion and range gates are unchanged: all leading
fields must be nonnegative integers, seconds must be finite and satisfy
`0 <= seconds < 60`, and the middle minute field in the three-field form must
be below 60.  Thus `03.76` is accepted without rewriting or normalizing the
fixed receipt, while the established `0:00.01` and `1:02:03.50` forms remain
accepted.

The bounded fixture puts `03.76` inside the complete synthetic checker
workflow receipt and calls `validate_checker_workflow_receipt`.  Separate
negative fixtures reject:

- empty and nonnumeric strings;
- `nan` and `inf`;
- a negative seconds value;
- one-field and colon-form seconds at 60;
- a three-field minute value at 60;
- an empty middle field; and
- a four-field spelling.

The only other producer edits are version plumbing:

- the checker module namespace advances from `task761_checker_v5` to
  `task767_checker_v5` without changing the checker bytes;
- launch schema advances to
  `d972.r07.canonical-p1-dag-degree2-lift.launch.v4`;
- final manifest schema advances to
  `d972.r07.canonical-p1-dag-degree2-lift.v4`; and
- the executable key advances from `producer_v4` to `producer_v5` in the
  launch fixture, production launch gate, and final manifest.

The accepted result, workflow receipt, checker, runs, artifacts, six receipts,
five parent-body pins, source ancestry, import hashes, false claims, and
resource behavior are unchanged.

## Arithmetic invariance

The exact top-level AST comparison reports only these changed functions:

```text
build
fixture_receipt_validation
load_dependencies
validate_elapsed_clock
validate_launch_manifest
```

No function or class was added or removed.  The ASTs of all classes are equal.
The four loops in `build` are individually AST-identical.  The complete ASTs
of `add_full`, `scale_full`, `flatten_p1`, `full_from`, `recurse_node`,
`projected_seed`, `compile_packet_v486`, `compile_old_defect`,
`reduction_digests`, `make_instruction`, and `instruction_receipt` are equal.
Consequently the 8,059-row recurrence, character/actor order, packet
projection, packed-cache format, instruction generation, and resource paths
have no AST delta.

## Workflow v2

Workflow v2 is a mechanical successor of v1.  It uses the exact fire token
`[fire-r07-canonical-p1-degree2-lift-v2]` and pins producer v5 at 104,788
bytes, 2,231 LF, SHA-256
`32ee4c536e0f5289a13bcd71723bfc6cfc8bd52f074008b78ba2acaca7d6466b`.
Compile, selftest, launch construction, real invocation, and final manifest
checks all reference v5.  Launch/final schema gates and the executable key are
advanced consistently, and success/log artifact names are versioned to v2.

All other workflow structure remains unchanged: 17 serial steps, exact-event
checkout, Python 3.13, NumPy 2.5.1, all accepted metadata/hash gates, recursive
eight-file staging, canonical launch construction, success-only candidate
upload, and always-uploaded diagnostics.  The 2,220-second internal cap,
38-minute command cap, 45-minute job cap, `ulimit -v 8388608`, 7-GiB RSS gate,
and single-threaded BLAS environment are unchanged.  No checker, connection
pass, retry, resume, concurrency, or heavy test was added.

## Sequential bounded checks

All bytecode output was directed to `%TEMP%`.  The checks were run
sequentially and exited successfully:

```text
py_compile
  exit=0 elapsed_seconds=0.228073

producer --selftest
  exit=0 elapsed_seconds=0.774115
  fixture_accept=6
  rejections=50
  forbidden_calls=[]
  actual_replay=DEFERRED_TO_GHA

exact 03.76 production workflow-receipt witness
  accepted=3 fixture_rejections=33 elapsed_seconds=0.624634

v4/v5 top-level and arithmetic AST comparison
  PASS arithmetic_delta=none class_delta=none elapsed_seconds=0.098981

build-loop AST comparison
  PASS loops=4 elapsed_seconds=0.058211

workflow YAML + four inline-Python AST comparison
  PASS steps=17 heredocs=4 elapsed_seconds=0.022219

workflow eight local file pins + ten action pins
  PASS elapsed_seconds=0.023817
```

The selftest terminal was:

```json
{"actual_replay":"DEFERRED_TO_GHA","all_four_actor_slots":true,"fixture_accept":6,"forbidden_calls":[],"full_projector_nonzero_p1":true,"rejections":50,"scale_two":true,"selftest":"PASS","semantic_checker_launch_validation":true,"verified":false}
```

This is an implementation candidate for the narrow Task764 re-audit.  It does
not promote a lift or any downstream arithmetic claim.

CANONICAL_P1_LIFT_V5_CLOCK_REPAIR=IMPLEMENTED_CANDIDATE
SAFE_FOR_NARROW_REAUDIT=yes
ACTUAL_8059_ROW_LIFT_REPLAY=NOT_RUN
verified=false

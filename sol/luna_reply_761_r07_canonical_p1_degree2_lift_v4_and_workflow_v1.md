# Luna Task761 - canonical P1-DAG degree-two lift v4 and workflow v1

```text
RESULT=COMPLETE
SAFE_FOR_INDEPENDENT_AUDIT=yes
REAL_PARENT_REPLAY=NOT_RUN
GHA_DISPATCH=NOT_RUN
```

Created exactly the three commissioned files:

- `search/d972_r07_canonical_p1_dag_degree2_lift_v4.py`
- `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v1.yml`
- `sol/luna_reply_761_r07_canonical_p1_degree2_lift_v4_and_workflow_v1.md`

No real parent was read, no 292 MB cache or lift candidate was built, and no
GHA workflow was dispatched.  No checkout, add, commit, push, or workflow API
operation was performed.  One read-only `git diff --no-index` invocation was
used solely to inspect/count the v3-to-v4 file delta; it did not read or alter
the repository index, refs, worktree metadata, credentials, or remote state.

## Exact file boundary

All measured files below contain zero CR bytes and end in LF.

| path | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_canonical_p1_dag_degree2_lift_v3.py` (source) | 89,095 | 1,932 | `fc1b7f58478365546fbc80f11b05add6f0478c662d32c9c09f49593343ea3ef0` |
| `search/d972_r07_canonical_p1_dag_degree2_lift_v4.py` | 104,313 | 2,222 | `68c690f18a495793b295c35f8bd9a9286485b8bd141fb3a31d2ed9de36591b8b` |
| `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v1.yml` | 27,574 | 497 | `80d36642a162b329a4b9d1288e4840ef6e8f736d087fa0a0909bd6af51a16c21` |

The textual v3-to-v4 delta is 324 inserted and 34 deleted lines.  Its
top-level AST delta adds only these three functions:

```text
validate_artifact_identity
validate_checker_workflow_receipt
validate_elapsed_clock
```

The only changed existing functions are `load_dependencies`,
`validate_launch_manifest`, `validate_checker_result`, `authenticate_inputs`,
`build`, `fixture_receipt_validation`, `parser`, and `validate_cli`.  All
recurrence, character/actor, packet projection, packed-cache, instruction,
and 8,059-row generation functions are AST-identical to v3.  No top-level
function or class was removed.

## Finite provenance repair

The v4 producer now pins and loads checker-v5 at
`bc60882b3ee22aa449c51cc280491b3d66df384a814a7033e418454f66900f97`.
Every semantic/executable key, module name, launch field, final source recheck,
and final manifest field uses the honest `checker_v5` identity; no
`checker_v4` spelling remains.

The new required CLI input is
`--semantic-checker-workflow-receipt`.  Before output-cache allocation, v4
canonically reads and registers both accepted files and fixes their raw bytes:

```text
independent-result.json
  sha256 405e1b26f971f67cb73129071a77346b126d0228c84219c2c3b0d879c63c99d5
workflow-receipt.json
  sha256 323ca2603b9ff7c42449fc0e2421c190eedcd7cd62471b695dee991fb1b728eb
```

The workflow-receipt validator enforces its exact key set/schema and plain
types; checker run `33819301663/1` and head
`e8a4de593700a81fb2a026366e349b89b640a6e8`; checker success artifact
`9918207444`; producer run `33814881435/1`, head
`15778e83c52941040ef9d4289ab76d897ee30ebc`, failed terminal, and exact eight
job records; producer six-receipt artifact `9916479231`; the exact six receipt
SHA values; linked checker/result/receipt hashes; finite nonnegative telemetry;
all false claim flags; `independent_checker=true`; and `verified=false`.

Launch schema
`d972.r07.canonical-p1-dag-degree2-lift.launch.v3` binds the raw checker result
SHA, raw workflow-receipt SHA, accepted checker artifact identity, exact root
identities, exact six receipts, source ancestry, and executable/import hashes.
Final schema `d972.r07.canonical-p1-dag-degree2-lift.v3` preserves those links
in the manifest and `source_ancestry`.  The coordinated opaque-manifest hole is
closed by comparing checker prepare `input_manifest_sha256` to the manifest
recomputed from the authenticated raw prepare root.

No checker arithmetic is rerun by v4.  The accepted raw checker result plus
its authenticated workflow receipt remain the arithmetic authority.

## Workflow v1

The workflow has 17 steps and supports manual dispatch or the exact push token
`[fire-r07-canonical-p1-degree2-lift-v1]`.  It checks out the exact event SHA,
uses Python 3.13 and NumPy 2.5.1, and authenticates before the real invocation:

- the exact v4 producer, checker-v5, and five unchanged imports plus words;
- checker run/artifact `33819301663/9918207444`;
- producer run, all eight exact jobs, and six-receipt artifact
  `33814881435/9916479231`; and
- the five original raw artifacts from `33677346616/1` at
  `22c6dddb43d107c05e65f53ad898823ae8ebe276`, using the checker-only-v3
  artifact metadata gates unchanged.

Compile and selftest run before downloads.  The accepted checker success
artifact is then downloaded.  Its directory layout is not trusted: exactly
eight regular files are located recursively, every basename must be unique,
every JSON byte stream must be canonical, and the result, workflow receipt,
and all six receipt hashes must match their fixed values before copying into a
canonical staging directory.

The launch builder hashes the five fixed body files and records their live
stable identities, hashes all accepted receipts again, and writes canonical
ASCII JSON into the always-uploaded log directory.  It contains no 8,059-row
arithmetic.

The actual producer command is serial and fixed to
`PYTHONHASHSEED=0`, `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, and
`MKL_NUM_THREADS=1`.  The job timeout is 45 minutes, the producer has a
37-minute internal deadline and a 38-minute outer `timeout`, and the shell
sets an exact 8 GiB virtual-memory cap (`ulimit -v 8388608`).  Both Python and
`tee` are line-buffered.  There is no retry, resume, connection pass,
independent lift checker, or full-matrix reconstruction.

Candidate upload is reachable only after exit zero, the exact final stdout
terminal, an exact three-file roster, canonical manifest, 292,444,992-byte
cache plus streaming hash, and 8,059-line instruction stream plus streaming
hash/EOF checks.  Logs and the canonical launch manifest use an `always()`
upload step.

## Bounded checks

`py_compile` used an external `%TEMP%` bytecode directory and passed.  The
producer selftest passed with the following terminal:

```json
{"actual_replay":"DEFERRED_TO_GHA","all_four_actor_slots":true,"fixture_accept":6,"forbidden_calls":[],"full_projector_nonzero_p1":true,"rejections":39,"scale_two":true,"selftest":"PASS","semantic_checker_launch_validation":true,"verified":false}
```

The 39 production-validator rejections include mutations of checker-v5 SHA,
checker-result SHA linkage, workflow run/head, each checker artifact field,
producer receipt linkage, false flags, independent flag, nested input-manifest
digest, and launch receipt/executable provenance.  Existing checker-result,
recurrence, actor, cache, and instruction mutations remain active.

Additional bounded results:

```text
PY_COMPILE_OK
YAML_PARSE_AND_INLINE_AST_PASS steps=17 heredocs=4 timeout_minutes=45
ACTION_PINS_OK=10
SOURCE_HASH_SIZE_LF_PINS_OK=8
FORBIDDEN_CALLABLES=[]
RECURRENCE_AST_DELTA=none
```

The actual parents and accepted checker artifact were not available to this
bounded local run, so all numerical promotion remains deferred to the parent
GHA execution and its subsequent independent audit.

```text
SAFE_FOR_INDEPENDENT_AUDIT=yes
ACTUAL_8059_ROW_LIFT_REPLAY=NOT_RUN
CONNECTION_EOF=NOT_RUN
CROSS_CHECKED=no
verified=false
```

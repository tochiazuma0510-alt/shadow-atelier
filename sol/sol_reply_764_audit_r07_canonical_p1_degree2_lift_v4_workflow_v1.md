# Sol Task764 — hostile finite audit of canonical P1 degree-two lift v4/workflow v1

## Ruling

The arithmetic successor is unchanged and the new provenance chain is honest,
but the submitted pair is **not dispatch-safe**.  There is one deterministic
production-reachability blocker.

The accepted 2,310-byte `workflow-receipt.json` contains

```json
"checker_process":{"elapsed_wall_clock":"03.76",...}
```

whereas v4 `validate_elapsed_clock` splits on `:` and requires two or three
fields.  The exact accepted one-field value therefore raises
`checker_process_elapsed_shape`.  The workflow stages that exact receipt and
passes it to v4, so the real command exits rejected in `authenticate_inputs`,
before cache allocation and before any of the 8,059-row recursion.  The
selftest misses this because its synthetic positive receipt uses
`"0:00.01"`.

I processed all seven numbered Task764 sections in order and read every file
listed in section 1 completely.  I did not download an artifact, read a real
parent, construct the 292 MB cache, dispatch GHA, use git/es7ops, or run an
8,059-row lift.

## 1. Exact byte boundary

`LF` is the count of byte `0a`.  Every row below has zero CR bytes and a final
LF.

| file | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `sol/sol_task_764_audit_r07_canonical_p1_degree2_lift_v4_workflow_v1.txt` | 4,619 | 88 | `e58dce44cd666f840ad762601aa4b3c068fca0c1d5c2c493f69ba3b22d5f4e99` |
| `sol/sol_reply_758_audit_r07_canonical_p1_degree2_lift_v3.md` | 19,191 | 361 | `9f577293fda04399f7a8e595c7d1695b35c8492836cc49ce1660e3fdfa3aad2c` |
| `sol/luna_task_761_r07_canonical_p1_degree2_lift_v4_and_workflow_v1.md` | 7,259 | 159 | `4bb1e0c7b80ca56c04daec21802e02391823a4d02431704eab1bc980639342fc` |
| `sol/luna_reply_761_r07_canonical_p1_degree2_lift_v4_and_workflow_v1.md` | 7,400 | 164 | `bc05732f61f95c2dce689f9be57b0e576c9a40ea56425df7dbf9f1c6d409e396` |
| `sol/proof_r07_canonical_lift_finite_release_normal_form_v491.md` | 4,174 | 94 | `56b9851b3ff67138419793514494d3737017dd1680cdccb1e15d92eb85090181` |
| `sol/proof_r07_canonical_lift_checker_v4_input_amendment_v494.md` | 1,188 | 31 | `6cfc1e67667b769345f5a62c22760c8d3020d2629e93f2ab7c2853e11ff10042` |
| `search/d972_r07_canonical_p1_dag_degree2_lift_v3.py` | 89,095 | 1,932 | `fc1b7f58478365546fbc80f11b05add6f0478c662d32c9c09f49593343ea3ef0` |
| `search/d972_r07_canonical_p1_dag_degree2_lift_v4.py` | 104,313 | 2,222 | `68c690f18a495793b295c35f8bd9a9286485b8bd141fb3a31d2ed9de36591b8b` |
| `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v1.yml` | 27,574 | 497 | `80d36642a162b329a4b9d1288e4840ef6e8f736d087fa0a0909bd6af51a16c21` |

The workflow's SHA/byte/LF pins match the live bytes of all eight local inputs:
v4, checker-v5, grade1-v4, prebuild-v1, semantic-v5, structural-v1,
floor-v1, and the words JSON.  The seven source files end in LF; the words
JSON has zero LF and ends in `}` as declared.

## 2. V3-to-v4 delta and arithmetic invariance

A `difflib.SequenceMatcher(..., autojunk=False)` comparison gives exactly 324
inserted and 34 deleted lines.  Top-level AST comparison gives:

- new functions: `validate_artifact_identity`,
  `validate_checker_workflow_receipt`, `validate_elapsed_clock`;
- changed existing functions: `load_dependencies`,
  `validate_launch_manifest`, `validate_checker_result`,
  `authenticate_inputs`, `build`, `fixture_receipt_validation`, `parser`, and
  `validate_cli`;
- no removed function and no changed class.

The ASTs of all numerical/replay functions are exactly equal between v3 and
v4: node/expression/DAG validation, component and row hashing, addition and
scaling, P1 flattening and reconstruction, `recurse_node`, projected seeds,
the v486 packet projection, old-defect compilation, lazy P1 access,
reduction-digest generation, and instruction generation.  The complete class
ASTs of `PackedCache`, `InstructionSink`, and `LazyP1` are also equal.  All four
explicit loops inside `build` have equal ASTs.

The constants `OLD_RANKS`, `NEW_RANKS`, `ORDER`, `OLD_ORIGIN_RANGES`,
`CHARACTERS`, `ACTORS`, `MONOMIALS`, all source widths, `D2_WIDTH`,
`ROW_BYTES`, `ROWS`, `CACHE_BYTES`, the claim flags, import hashes, and
forbidden-call set are AST-identical.  In particular:

```text
old ranks       505,503,503,503
new ranks       1509,1512,1512,1512
global order    0,505,1008,1511,2014,3523,5035,6547,8059
characters      (0,0),(0,1),(1,0),(1,1)
actors          1,-1,2,-2
row recurrence  scale * (raw - ordered prior reductions)
```

Packet selection, all six degree-two monomials, packed row format, the
292,444,992-byte cache, rolling ancestry, and streaming instruction receipt
are unchanged.  A case-insensitive static scan finds no `checker_v4`, old
checker path/SHA, or old checker key anywhere in v4 or workflow v1.  Thus the
only intended semantic delta is the Task758 provenance amendment; the new
elapsed-clock gate is within that amendment, but is over-restrictive.

`ARITHMETIC_AST_UNCHANGED=yes`.

## 3. Actual provenance chain

The constants in v4 and the workflow agree exactly with the accepted facts:

- checker run/attempt/head `33819301663/1` at
  `e8a4de593700a81fb2a026366e349b89b640a6e8`;
- success artifact `9918207444`, name
  `task757-p1-semantic-checker-only-v3-success-33819301663-1`, API bytes
  `24694`, digest
  `sha256:f99fd6ce1172cc349b249ead8dbb8e75c8c8bd8a1b8a0493dfd4596aee5fbf0c`;
- result bytes/SHA `13336` /
  `405e1b26f971f67cb73129071a77346b126d0228c84219c2c3b0d879c63c99d5`;
- workflow-receipt bytes/SHA `2310` /
  `323ca2603b9ff7c42449fc0e2421c190eedcd7cd62471b695dee991fb1b728eb`;
- checker-v5 SHA
  `bc60882b3ee22aa449c51cc280491b3d66df384a814a7033e418454f66900f97`;
- producer run/attempt/head `33814881435/1` at
  `15778e83c52941040ef9d4289ab76d897ee30ebc`, and artifact
  `9916479231`, 8,412 bytes, digest
  `sha256:91281261a272e6ff48104a579a86e9cb300fc1543eaad1321b609e6d83564245`;
- the prepare, four block, and join receipt hashes exactly equal the six
  Task764 values.

Static extraction of the checker-only-v3 workflow receipt builder finds the
same 21 top-level keys as `CHECKER_WORKFLOW_RECEIPT_KEYS`, and its ordered
eight-job tuple equals `PRODUCER_JOBS`: seven successes through join and the
named old `independent-check` failure.  V4 checks plain types, exact artifact
objects, fixed run identities, exact receipt map, checker/result linkage,
finite nonnegative numerical telemetry, exact false claim flags,
`independent_checker=true`, and `verified=false`.

The checker-result gate retains the exact outer/prepare/block schemas and
counts.  Its added comparison

```text
result.prepare.input_manifest_sha256 == sha256(canonical(input_manifest))
```

closes Task758's coordinated opaque-manifest mutation.  The six raw receipt
hashes are recomputed from the inputs; the exact checker result and workflow
receipt are both raw-SHA pinned and entered in `FileRegistry`; the launch is
compared with recomputed raw-root identities; and the final manifest records
the two hashes and success-artifact identity both directly and in source
ancestry.  A coordinated self-written launch therefore cannot substitute an
unaccepted result or receipt.

The chain is nevertheless unusable because of the exact historical clock
string.  The source checker workflow used the greedy extraction

```python
re.search(r"Elapsed \(wall clock\) time.*:\s*(.+)", timing)
```

so a line ending in `0:03.76` yields `03.76`.  A direct call to the production
validator gave:

```text
validate_elapsed_clock("03.76")    REJECT checker_process_elapsed_shape
validate_elapsed_clock("0:00.01")  ACCEPT
```

This is fail-closed, not a provenance bypass.  The accepted receipt's raw SHA
and every substantive ancestry link remain honest.

```text
PROVENANCE_HONEST=yes
ACTUAL_ACCEPTED_RECEIPT_CONSUMABLE=no
```

## 4. Workflow reachability and acquisition

Workflow v1 parses as YAML and has 17 serial steps.  It has manual dispatch
and one push gate containing the fire token exactly once:

```text
[fire-r07-canonical-p1-degree2-lift-v1]
```

Checkout is pinned and uses `${{ github.sha }}`.  Python is 3.13, NumPy is
2.5.1, and all 10 action uses are full 40-hex pins.  Before the producer it
checks the local source bytes and API metadata for the checker run/artifact,
producer run/all eight jobs/six-receipt artifact, and all five source-run
artifacts.  The checker-success download is tied to the accepted run and
name.  Its recursive staging gate permits exactly eight regular files with
unique basenames, rejects symlinks, checks both fixed sizes where specified,
checks every raw SHA, and requires canonical ASCII JSON with final LF.

The launch builder contains no lift arithmetic.  It rehashes the five root
bodies, six receipts, result and workflow receipt, and records stable body
identities plus the accepted executable/import/artifact data.  The actual CLI
passes all five roots, six receipts, the result, workflow receipt, launch, and
fresh external output directory exactly once.

After a zero producer exit, workflow v1 requires the exact producer terminal,
the exact three-file candidate roster, canonical manifest, a
292,444,992-byte cache whose digest matches the manifest, and an 8,059-line
instruction stream with matching byte count/digest/final LF/EOF.  Candidate
upload is success-only; diagnostic upload is `always()`.  There is no
independent lift checker, connection pass, retry, resume, concurrency key, or
unrelated global-matrix reconstruction.

Those gates are sound but unreachable with the accepted receipt: the real
command fails at the clock validator before reaching the row loop.  Dispatch
would therefore only consume runner time and upload failure diagnostics.

## 5. Resource and avoidable-work audit

The numerical cache is still file-backed:

```text
8059 * 36288 = 292444992 bytes on disk.
```

There is no resident cache copy or decoded all-row matrix.  The fixed P1 maps
total 67,011,332 bytes, and only one 37,340,352-byte packet map is open at a
time, for at most 104,351,684 mapped input/packet bytes.  A complete unpacked
row is 241,928 bytes.  The recurrence retains only a bounded handful of rows;
the 8,059 cached row hashes are under roughly 1 MiB.  Each numerical reduction
parent is decoded once for subtraction, while `make_instruction` obtains its
receipt by O(1) `row_sha`; actor/transition parents are hashed while already
resident.  Instruction verification reads one bounded line at a time.

No dense global matrix, 44/176 full-row cache, ancestry tree, cache copy,
whole instruction read, repeated parent replay, unbounded JSON ancestry,
parallel numerical job, or hidden retry is present.  The exact authenticated
JSON bodies are bounded inputs.  Peak usage is therefore the interpreter and
parsed fixed bodies, at most 104,351,684 mapped bytes, a small row working set,
and streaming buffers, comfortably structurally below 8 GiB.

The caps are nested as declared: 2,220 seconds internal, 38 minutes outer,
45 minutes job, `ulimit -v 8388608`, and a 7 GiB producer RSS threshold.  The
outer command has one minute beyond the internal row timer for authentication
and final streaming checks, and the job has seven minutes beyond the outer
command for setup/download/upload.  No code path forces the caps to contradict
one another.  Their empirical wall-clock margin remains unmeasured because
the prohibited real build was not run.

One minor avoidable retention from Task758 remains: `authenticate_inputs`
returns `prepare_raw` and four `block_raws`, so those five raw byte strings stay
reachable through the build although only their registered identities are
needed.  This is not a dense or release-blocking path, but it is an honest
small cleanup opportunity.

```text
PROHIBITED_SLOW_OR_MEMORY_HEAVY_PATH_REMAINS=no
MINOR_AVOIDABLE_RAW_BODY_RETENTION_REMAINS=yes
```

## 6. Bounded sequential checks

All generated test material was outside the repository under
`C:\Users\81905\AppData\Local\Temp\sol-task764-audit-764`.  The external
pycache was
`C:\Users\81905\AppData\Local\Temp\sol-task764-audit-764\pycache`; the two
bounded selftest invocations used
`...\task755-selftest-rgb98tyk` and
`...\task755-selftest-o725chgr`.  The selftest's temporary
`task746-source-pin-*` directories removed themselves.  The audit processes
all exited; none was left running.  Peak RSS was unavailable from the Windows
process interface used here (reported null), so no invented value is given.
The external audit root remains outside the repository.

Commands and results:

```text
PYTHONPYCACHEPREFIX=<external-pycache>
python -B -m py_compile search/d972_r07_canonical_p1_dag_degree2_lift_v4.py
  exit 0; 0.558 s; stdout/stderr empty

TEMP=<external-root>; TMP=<external-root>
python -B search/d972_r07_canonical_p1_dag_degree2_lift_v4.py --selftest
  exit 0; 2.389 s
  {"actual_replay":"DEFERRED_TO_GHA","all_four_actor_slots":true,
   "fixture_accept":6,"forbidden_calls":[],
   "full_projector_nonzero_p1":true,"rejections":39,"scale_two":true,
   "selftest":"PASS","semantic_checker_launch_validation":true,
   "verified":false}

python -B - <YAML/BaseLoader + four-heredoc AST audit>
  PASS; 0.022023 s; steps=17; inline Python blocks=4; pinned actions=10

python -B - <v3/v4 AST and static-diff audit>
  PASS; 0.111551 s; inserted=324; deleted=34;
  critical arithmetic AST delta=none; build loop AST delta=none

python -B - <production elapsed-clock witness>
  0.000045 s; "03.76" rejected; synthetic "0:00.01" accepted

python -B - <one-field finite-clock repair probe>
  0.000040 s; "03.76" accepted; empty/nan/negative/>=60-second and
  four-field mutations rejected
```

The ordinary v4 selftest therefore passes but is not a witness that the exact
accepted receipt passes; its positive fixture differs at the decisive field.

## 7. Smallest finite repair and claim boundary

There is one substantive repair:

1. In a versioned producer successor, make `validate_elapsed_clock` accept the
   historical one-field finite nonnegative seconds spelling.  The minimal
   safe shape change is `len(fields) in (1, 2, 3)`, retaining the existing
   finite and `0 <= seconds < 60` check; equivalently, because the whole raw
   receipt is SHA-pinned, an exact positive case for `"03.76"` is sufficient.
   Add the exact one-field spelling to the production-validator selftest, not
   just a normalized synthetic clock.
2. Mechanically re-pin the versioned producer bytes/SHA/LF in its versioned
   workflow and rename/version the producer executable and launch/final
   manifest keys where needed for honest ancestry.  Do not alter any
   recurrence, packet, cache, or instruction AST.  One bounded selftest plus
   YAML/AST check is sufficient before a fresh audit; no parent replay or
   extra heavy test is needed to close this defect.

The second item is only the inevitable provenance consequence of changing
producer bytes, not a second defect.  The accepted checker result and receipt
must not be regenerated or normalized; they are the fixed historical inputs.

No actual lift, connection, grade-two terminal, A0/COMMON, compatible/cofinal
lift, fake witness, or Ihara witness follows from this audit.

```text
ARITHMETIC_AST_UNCHANGED=yes
PROVENANCE_HONEST=yes
ACTUAL_ACCEPTED_RECEIPT_CONSUMABLE=no
UNNECESSARY_SLOW_PATH_REMAINS=no
UNNECESSARY_MEMORY_RETENTION_REMAINS=yes_nonblocking_raw_bodies_only
ACTUAL_8059_ROW_LIFT_REPLAY=NOT_RUN
CONNECTION_EOF=NOT_RUN
GRADE_TWO_TERMINAL=NOT_RUN
CROSS_CHECKED=no
verified=false
SAFE_TO_DISPATCH_GHA=no
```

VERDICT=FAIL_CANONICAL_P1_LIFT_V4

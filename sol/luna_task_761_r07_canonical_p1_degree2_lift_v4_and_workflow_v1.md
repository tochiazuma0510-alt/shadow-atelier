# Luna Task 761 — canonical P1-DAG degree-two lift v4 + first GHA workflow

## 0. Role and exact write boundary

You are Luna.  Implement the single finite provenance repair isolated by
Sol(max) Task758, then make the first bounded GHA producer workflow.  Create
only:

- `search/d972_r07_canonical_p1_dag_degree2_lift_v4.py`
- `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v1.yml`
- `sol/luna_reply_761_r07_canonical_p1_degree2_lift_v4_and_workflow_v1.md`

Use v3 as the source.  Do not change its 8,059-row recurrence, character or
actor order, packet projection, packed-cache format, instruction stream, or
claim boundary.  Do not run real parents, GHA, git, or build a new checker.

Read completely:

- `sol/sol_reply_758_audit_r07_canonical_p1_degree2_lift_v3.md`
- `search/d972_r07_canonical_p1_dag_degree2_lift_v3.py`
- `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v5.py`
- `.github/workflows/d972-r07-p1-semantic-checker-only-v3.yml`
- `sol/proof_r07_canonical_lift_finite_release_normal_form_v491.md`
- `sol/proof_r07_p1_checker_body_schema_repair_v497.md`

## 1. Accepted checker-v5 boundary

The actual accepted checker-only result is fixed as follows.

```text
checker executable sha256:
bc60882b3ee22aa449c51cc280491b3d66df384a814a7033e418454f66900f97

checker workflow run/attempt/head:
33819301663 / 1 / e8a4de593700a81fb2a026366e349b89b640a6e8

checker success artifact:
id       9918207444
name     task757-p1-semantic-checker-only-v3-success-33819301663-1
bytes    24694
digest   sha256:f99fd6ce1172cc349b249ead8dbb8e75c8c8bd8a1b8a0493dfd4596aee5fbf0c

independent-result.json:
bytes    13336
sha256   405e1b26f971f67cb73129071a77346b126d0228c84219c2c3b0d879c63c99d5
marker   R07_GRADE2_P1_COMPONENTWISE_INDEPENDENT_CHECKER_V1_PASS

workflow-receipt.json:
bytes    2310
sha256   323ca2603b9ff7c42449fc0e2421c190eedcd7cd62471b695dee991fb1b728eb
schema   d972.r07.p1.componentwise.checker-only.v3.workflow-receipt
```

Its producer parent is also fixed:

```text
run/attempt/head 33814881435 / 1 / 15778e83c52941040ef9d4289ab76d897ee30ebc
six-receipt artifact id/name/bytes/digest
9916479231
task729-p1-semantic-six-receipts-33814881435-1
8412
sha256:91281261a272e6ff48104a579a86e9cb300fc1543eaad1321b609e6d83564245
```

The six canonical receipt SHA256 values are:

```text
prepare 9caf8cbf04742b1400c5c63d765508308af72ef773050af5562221a082fd159a
block0  e9271d20739aee299620ef6e8d53dd940ea10ed1ab688bd61b69c7fb0ff4afc8
block1  7f34bb964665078727c7ed2b5e5165c50b1763003d573789d7406a6b06445eca
block2  6d8ebdf7b9495608c89779ecfd7ca8f3c1a84790fc8e2b6b6fc5dd292c530e6a
block3  a558c466862bf050bf8c850aaf47be633ae1f0bce9785f18b410cb0eff9f6d9d
join    a3479e7ebc010fbfde4d42c95eebd8cf81cc5eeab9ef37ab77ba2284fb8b27c8
```

## 2. Minimal v4 producer repair

Perform exactly the Task758 Section 4 amendment.

1. Pin/load checker-v5, replace every `checker_v4` semantic/executable key,
   module name, launch entry, final source recheck, and manifest field by the
   honest `checker_v5` entry.  Preserve the checker result schema/marker and
   arithmetic validator.
2. Add one CLI input `--semantic-checker-workflow-receipt`.  Canonically read
   it before allocation and validate its **exact** key set, schema, plain
   integer/string/bool types, false claim flags, independent-checker flag,
   finite nonnegative telemetry, and the exact values above.
3. Link its `checker_sha256` to the v5 pin,
   `independent_result_sha256` to the raw checker-result bytes, and every
   producer receipt SHA to the same six canonical receipt inputs.  Require its
   producer run/attempt/head/artifact and checker run/attempt/commit values to
   equal the fixed actual values above.  The producer run conclusion may be
   `failure` because only its obsolete embedded checker job failed; require
   every listed producer phase through join to be success and the named old
   independent-check job to be failure exactly as the receipt records.
4. Register the workflow-receipt raw bytes and bind their SHA and the accepted
   checker success artifact identity in a versioned launch schema and final
   manifest/source ancestry.  Use a new honest v4/v3 schema name where the old
   v2 launch/manifests would misdescribe inputs.
5. Close Task758's coordinated opaque-manifest mutation: compare the nested
   checker prepare `input_manifest_sha256` with the `expected_manifest`
   already computed from the authenticated raw prepare input.
6. Extend bounded selftest through production validators.  Positive v5
   result+workflow receipt passes.  Mutations of checker-v5 SHA, checker
   result SHA, workflow run/head, artifact id/digest/bytes/name, producer
   receipt linkage, false flags, independent flag, nested input-manifest
   digest, and launch provenance must be rejected.

Do not rerun checker arithmetic inside v4.  The raw accepted checker result
and authenticated workflow receipt are the arithmetic authority.

## 3. First producer workflow

Create one workflow derived from the immutable-parent download/authentication
style of the checker-only-v3 workflow.  Requirements:

- triggers: `workflow_dispatch` and push commit token
  `[fire-r07-canonical-p1-degree2-lift-v1]`;
- exact event SHA checkout; Python 3.13 and the already pinned NumPy version;
- authenticate v4 source bytes, checker-v5 bytes, actual checker run/artifact,
  actual producer run/six-receipt artifact, and the original five raw semantic
  roots from source run `33677346616/1` head
  `22c6dddb43d107c05e65f53ad898823ae8ebe276` before invoking v4;
- reuse the existing checker-only-v3 artifact names and metadata gates for the
  original prepare/block roots.  Download the accepted checker success
  artifact for `independent-result.json`, `workflow-receipt.json`, and the six
  receipts; do not trust filenames without hashes;
- construct the new launch manifest canonically from the five authenticated
  root identities, six receipt hashes, checker result/workflow receipt hashes,
  fixed source ancestry, executable/import hashes, and checker success
  artifact identity, then let v4 validate it;
- run compile+selftest before downloads; real build is serial with
  `PYTHONHASHSEED=0`, `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`,
  `MKL_NUM_THREADS=1`, an 8 GiB virtual-memory cap, `timeout` no greater than
  45 minutes, and line-buffered tee to a log;
- upload the candidate directory only after the producer terminal and exact
  manifest/cache/instruction presence checks; upload logs always;
- no in-workflow independent lift checker, no connection pass, no retry or
  resume framework, and no unrelated full-matrix reconstruction.

The workflow must use v4's actual SHA/byte count and the unchanged imported
file pins.  It may use a short inline canonical-JSON launch builder, but it
must not duplicate the 8,059-row arithmetic.

## 4. Bounded checks and reply

Run `py_compile`, producer selftest, YAML parse, exact source diff/call-graph
checks, and bounded launch/workflow-receipt mutation tests.  Report exact
bytes/LF/SHA, the v3-to-v4 delta, workflow steps and resource policy.

Required terminal:

```text
SAFE_FOR_INDEPENDENT_AUDIT=yes|no
ACTUAL_8059_ROW_LIFT_REPLAY=NOT_RUN
CONNECTION_EOF=NOT_RUN
CROSS_CHECKED=no
verified=false
```

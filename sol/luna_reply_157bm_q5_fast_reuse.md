# Luna reply 157bm — q5 fast lane from pinned calibrations

## Implementation

Added exactly one implementation file:

```text
.github/workflows/d972-burau-tuple-q5-fast-v1.yml
```

The workflow supports manual dispatch and a branch/path-limited `push`
trigger.  The push trigger is restricted to branch
`sol/d972-dmtcp-provision-v420` and exactly these four paths:
`.github/workflows/d972-burau-tuple-q5-fast-v1.yml`,
`search/d972_b4_burau_fiber_v4.py`,
`search/check_d972_b4_burau_fiber_v4.py`, and
`search/certs/d972_b4_word_key_artifact_v1_20260816.json`.  This makes the
first matching branch push start the workflow even before the workflow file
is present on the default branch, while unrelated pushes do not start it.
It uses minimal `actions: read` and `contents: read` permissions, and runs a matrix with `a=2` and `a=4` and
`fail-fast: false`.  It leaves the existing producer and checker unchanged.
Each matrix job:

1. queries the GitHub API for the pinned run and artifact IDs;
2. hard-fails on missing, expired, renamed, resized, or wrong-run artifacts;
3. downloads the exact q3/q4 artifact names from run `32051744038`;
4. verifies the downloaded JSON SHA-256 and internal q/a/status/source,
   row-count, order, and calibration metadata;
5. independently rechecks both calibration receipts;
6. runs the unchanged q5 producer with the existing 12 GB virtual-memory
   limit and 360-minute timeout;
7. enforces the exact candidate/all-pass marker count and runs the current
   independent checker; and
8. uploads the complete q5 logs, receipt, and downloaded calibration inputs.

The step summary reports the q5 status and the number of zero
identity-defect rows.  It emits no theorem/terminal token.  An all-pass
receipt remains UNKNOWN; only a checker-PASS candidate with a zero row is
usable by the direct-obstruction route.

## Pinned calibration artifacts

The GitHub API confirmed both artifacts are unexpired, belong to run
`32051744038`, and have the same source head
`983bd8b960c5d71ef686ee0d8a590728913f61d7`:

| q | artifact ID | exact name | size | downloaded JSON SHA-256 |
|---:|---:|---|---:|---|
| 3 | `9296644565` | `d972-burau-tuple-v4-calibration-q3-attempt1` | 95607 | `0813a151cd47a56f29aab629ebfc35a0293a8ce84d98c24f3a3ac3e0601ad8e2` |
| 4 | `9297445824` | `d972-burau-tuple-v4-calibration-q4-attempt1` | 95523 | `414c13fe680c2eeb6f3f75c7f6a7206a707c18a426da619543232e1a98855de2` |

I downloaded both artifacts to `%TEMP%` outside the repository and verified
the byte hashes and JSON metadata.  Both contain 972 rows and have status
`UNKNOWN_BURAU_SPECIALIZATION_ALLPASS`; q3 has `(q,a)=(3,-1)` and q4 has
`(q,a)=(4,2)`.

The fast workflow pins the full current source hashes:

```text
producer search/d972_b4_burau_fiber_v4.py
aa8726570c58840a000b4b247b34eccd39a958f97087e6745216e2055b578cec

checker search/check_d972_b4_burau_fiber_v4.py
bb398fe265bb81d5dc36312b4468238b8420fc866cc6a8cae7ad1eacee5ab2c7
```

The newly added workflow SHA-256 is:

```text
.github/workflows/d972-burau-tuple-q5-fast-v1.yml
f6e5a635d734477f9a0a225e31187a94aa88280539db51a9ea6a22306926f38d
```

## Validation performed

```text
gh api .../actions/runs/32051744038/artifacts?per_page=100
  PASS: exact IDs, names, sizes, unexpired state, run binding

gh run download 32051744038 --name <q3/q4 exact name> --dir %TEMP%\d972-q5-fast-157bm
  PASS: both artifacts downloaded

downloaded JSON SHA/source/q-a/status/972-row metadata check
  PASS: q3 and q4

PyYAML workflow parse
  YAML_PARSE_PASS

post-patch YAML and branch/path trigger static contract check
  POST_PATCH_YAML_STATIC_PASS

embedded workflow Python compilation
  EMBEDDED_PYTHON_COMPILE_PASS (3 blocks)

python search/d972_b4_burau_fiber_v4.py --self-test
  D972_B4_BURAU_FIBER_V4_SELFTEST_PASS

python search/check_d972_b4_burau_fiber_v4.py --self-test
  D972_B4_BURAU_FIBER_V4_CHECKER_SELFTEST_PASS
  D972_B4_BURAU_FIBER_V4_CHECKER_FINAL_MARKER status=PASS
```

`actionlint` and a native bash syntax checker are not installed in this
Windows workspace; YAML parsing, embedded-Python compilation, and both
lightweight project selftests passed.  No local GAP, heavy producer, Git
commit, push, or workflow dispatch was performed.

## Risks and handoff

The parent must commit/push the new workflow on
`sol/d972-dmtcp-provision-v420`; that matching push triggers the run once.
Manual dispatch remains available.  The workflow intentionally fails closed if the old artifacts expire or drift,
if the producer/checker source hashes change, if either q3/q4 checker fails,
or if q5 returns `UNKNOWN_RESOURCE`.  The two q5 matrix jobs each retain the
existing 360-minute timeout and 12 GB virtual-memory limit, so the fast lane
avoids recomputing q3/q4 but still has the expected q5 cost.

Only the workflow and this specified reply were changed.  The user's dirty
matrix files and all production mathematical code were preserved.

READY_TO_COMMIT_AND_DISPATCH

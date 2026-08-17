# Luna reply 157ci: q5 sealed-calibration fast start

## Verdict

Q5_SEALED_FASTSTART_READY

I built only the new workflow

    .github/workflows/d972-burau-accel-v2.yml

and this reply.  The audited 157by producer/checker and the old workflow were
not edited.  No Git, GHA dispatch/execution, GAP, or heavy local enumeration
was run.

## Immutable calibration pins

The workflow pins the calibration run, source revision, and attempt:

    run       32072654277
    head      303778b34e173acf6a35ad09297cf37f18dfce53
    attempt   1

The two artifact records are pinned as follows:

    q3  id 9303461247
        name   d972-burau-q5-parallel-v1-calibration-q3-attempt1
        size   95914 bytes
        digest sha256:24bf1fc9fcb7505a7fe83e7521bcc7c65a32b58947ce04edb471013e4720df24
        receipt 0813a151cd47a56f29aab629ebfc35a0293a8ce84d98c24f3a3ac3e0601ad8e2

    q4  id 9303700869
        name   d972-burau-q5-parallel-v1-calibration-q4-attempt1
        size   95831 bytes
        digest sha256:38be12c17437dba07b3b1b33c82d558ba38478a059dbcbe6641fdfc0146ccf62
        receipt 414c13fe680c2eeb6f3f75c7f6a7206a707c18a426da619543232e1a98855de2

The API gate checks run id, head SHA, run attempt, artifact id/name/size,
archive digest, nonexpired state, artifact run id, artifact head SHA, and
unique artifact names (workflow lines 60--120).  The downloads use the exact
names and run id (lines 123--139); the archive digest therefore authenticates
the complete evidence bundle, not only its receipt.

## Sealed evidence authentication

Each downloaded bundle is required to contain exactly one discoverable copy
of the receipt, calibration seal, checker log, and checker-status file.  The
gate at lines 141--262 checks:

* receipt SHA, v4 schema/final marker, all-pass status, q/a, 972 rows and
  row indices, fiber size/counts, frozen word/artifact/target/tuple hashes,
  roof and H'/H/kernel orders;
* seal schema `d972-burau-q5-parallel/calibration-seal/v1`, `complete=true`,
  run/attempt/artifact ids, name and size, q/a, receipt SHA, 972 rows,
  legacy producer/checker hashes, checker exit 0, and receipt status/marker;
* checker-status exactly `0` and exactly one
  `D972_B4_BURAU_FIBER_V4_CHECK_PASS ` line in each sealed checker log.

The current source/artifact hashes are also checked before any q5 work:

    q5 producer    fe9ee097c50a54ffc69ce9bcb820e7ac09847581eb82a3dd2d83962aab69e2dc
    q5 checker     e36405fafb75ea3eaf096e507920b9d2ebe683e867a49a35c8f1bdcb708a0c7a
    legacy producer aa8726570c58840a000b4b247b34eccd39a958f97087e6745216e2055b578cec
    legacy checker  e0b4cb923c1bd73b9afdc7f47de739f91c8aa3c0d7764c239e1df76d74fbce14
    words          564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9

## Unchanged deep q5 contract

The q5 producer receives the same two receipt paths discovered from the
sealed bundles (`--calibration-q3` and `--calibration-q4`, lines 275--296).
Its own `calibration_ok` path therefore deep-validates both complete 972-row
receipts before the q5 computation.  The workflow does not replace that
check with seal metadata.

The q5 receipt gate retains the v1 candidate/all-pass rules (lines 300--340):

* candidate status requires a contiguous prefix ending in exactly one zero
  fiber with `row_scan_complete=false` and the terminal index equal to the
  prefix length;
* all-pass status requires all 972 rows, no zero fiber,
  `row_scan_complete=true`, and no terminal index;
* the receipt must bind the q5 source hash, exact-kernel witness method,
  q=5/a, and the exact q3/q4 receipt SHAs in `calibration_gate`.

The independent q5 checker receives those same two sealed receipt paths and
the q5 receipt (lines 342--358).  It must exit zero and emit exactly one
`D972_B4_BURAU_ACCEL_CHECK_PASS ` marker.  No legacy calibration checker
command occurs in the workflow: the immutable sealed evidence already
contains the completed legacy checker result, while the unchanged q5
producer/checker revalidate the full calibration receipts and q5 fibers.
This is exact reuse of independently checked, hash-bound evidence rather
than trust in an unchecked aggregate.

## Matrix, failure handling, and static checks

The q5 matrix remains exactly `a=2` and `a=4`, with `fail-fast: false` and a
360-minute cap (lines 41--50).  Both producer/checker selftests run before
the expensive q5 producer (lines 264--273).  All evidence under `ci/out/`
and `ci/in/` is uploaded with `if: always()` (lines 360--368), including
failure logs, status files, sealed bundles, and q5 receipts.

Static checks passed:

    YAML_PARSE_PASS
    EMBEDDED_PY_COMPILE_PASS (3 here-documents)
    STATIC_BINDINGS_PASS

The q5 producer and checker selftests passed with their expected final and
negative-fixture markers.  The Windows audit environment has no `bash`, so
`bash -n` was unavailable; shell quoting, `set -euo pipefail`, PIPESTATUS,
marker cardinality, and failure paths were inspected manually.

Current workflow SHA-256:

    5543dc8666aa2f8fdd25975dfeeb174b8ff397a72007ba005a587d184f64cf2f

Q5_SEALED_FASTSTART_READY

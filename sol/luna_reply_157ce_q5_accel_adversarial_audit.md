# Luna reply 157ce: adversarial audit of q5 accelerator bundle

## Verdict

Q5_ACCEL_AUDIT_PASS

I audited the complete 157by instruction/reply and the three versioned files:

    search/d972_b4_burau_accel_v1.py
    search/check_d972_b4_burau_accel_v1.py
    .github/workflows/d972-burau-accel-v1.yml

No GAP, heavy enumeration, Git, or GHA was run, and no bundle file was
modified. The production workflow is fail-closed on the requested
candidate/all-pass boundary. The only production matrix entries are q=5,
a=2 and q=5, a=4.

## Lightweight checks

These passed:

    AST_PARSE_PASS
      d972_b4_burau_accel_v1.py
      check_d972_b4_burau_accel_v1.py

    YAML_PARSE_PASS
      d972-burau-accel-v1.yml

    EMBEDDED_PY_COMPILE_PASS (3 here-doc blocks)

    D972_B4_BURAU_ACCEL_V1_SELFTEST_PASS
    D972_B4_BURAU_ACCEL_PARTIAL_ALLPASS_NEGATIVE_PASS
    D972_B4_BURAU_ACCEL_CHECKER_SELFTEST_PASS
    D972_B4_BURAU_ACCEL_CHECKER_FINAL_MARKER status=PASS

The Windows audit environment has no bash executable, so bash -n could not
be invoked. The run blocks were inspected for quoting and control-flow
errors; the YAML and all embedded Python blocks parse successfully.

The four pinned source hashes in the workflow match the working-tree bytes:

    producer  fe9ee097c50a54ffc69ce9bcb820e7ac09847581eb82a3dd2d83962aab69e2dc
    checker   e36405fafb75ea3eaf096e507920b9d2ebe683e867a49a35c8f1bdcb708a0c7a
    cal-prod  aa8726570c58840a000b4b247b34eccd39a958f97087e6745216e2055b578cec
    cal-check e0b4cb923c1bd73b9afdc7f47de739f91c8aa3c0d7764c239e1df76d74fbce14

The current workflow bytes (including the q4-path correction) have SHA-256

    aad5feadd26687be0d84ac85ab9cacfc6ae211b5bec74f83f2029888a1bab1e9

The q4 download now lands at ci/in/q4 (lines 100--107), and the same path
is used by the q4 artifact gate, legacy calibration check, producer, and
active checker (lines 140, 173, 185--188, and 250). No q4 path mismatch
remains.

## Exact kernel and discovery witnesses

The producer's exact path is:

* complete_hprime (lines 486--514) repeatedly rebuilds the complete
  projected section, Schreier relators, and finite kernel. It rejects a
  projection larger than the frozen P' order and rejects termination before
  the complete projected order 367416.
* enumerate_kernel_with_witness (lines 449--467) exhausts the signed
  Schreier-generator BFS until the queue is empty. It has no depth, sample,
  timeout, Bloom, or word-length cutoff. Every discovered edge label is
  retained in witness.
* run_full (lines 753--778) checks that every returned kernel element has
  identity roof block and reconstructs every cited fiber as the full h0*K
  set.

The witness-generating claim is sound: by induction on BFS discovery time,
every visited vertex is a product of recorded discovery labels, while every
recorded label is a Schreier relator. Thus the recorded labels generate the
same finite K as the exhaustive BFS. The bounded regression at producer lines
863--883 checks both closure equality and failure after deleting a witness.

The active checker is the standalone v4 entry point at lines 1082--1097.
It reimplements the section/relator closure in v4_complete (lines
840--855), decodes and compares the complete serialized kernel (lines
967--975), and independently closes the supplied witness list (lines
976--980). It then reconstructs every cited fiber and recomputes every
defect (lines 993--1010). It does not import the producer.

There is an unused legacy checker block at the beginning of the checker
file (the SCHEMA/FINAL values at lines 28--29 and main around
613--624). It is not the executed path: the final if __name__ calls
main_v4 at lines 1082--1097, which uses V4_SCHEMA, V4_FINAL, and the
accelerator markers. This is a non-blocking maintainability caveat, not a
production gate bypass.

## Pentagon and A.18 convention

I checked the primary paper page images:

* PDF p.13, equation (2.20), displays
  phi234(f) phi1,23,4(f) phi123(f) =
  phi1,2,34(f) phi12,3,4(f).
* PDF p.49, equation (A.18), gives the five coface generator maps.

The producer's A18_NAMES and a18_pairs (lines 45--46 and 362--368)
match the p.49 order:

    123, 234, 12,3,4, 1,23,4, 1,2,34.

With the explicit paper_prod reverse-action convention, matrix_defect
(lines 371--374) is the right-side inverse times the left side of (2.20).
The independent checker repeats this as v4_defect (lines 765--777).
The mutation test at checker lines 541--555 rejects the swapped product
and swapped leading A.18 order. No convention drift was found.

## Candidate-only scan semantics

The producer scans all elements of each finite fiber before deciding whether
that row has zero identity defects (lines 774--785). For q=5, after such a
complete zero fiber it stops and writes a contiguous prefix with
row_scan_complete=false and terminal_zero_row_index equal to the last
cited row (lines 786--802).

The active checker accepts a partial prefix only for the candidate status:
scan_metadata_ok (lines 643--653) requires the terminal index to equal the
prefix length. Its row loop recomputes the complete cited fibers and all
defects. It then requires exactly one zero row and requires it to be the
last cited row (lines 1016--1019). For all-pass status it requires
row_scan_complete=true, 972 rows, no zero, and no terminal index
(lines 1020--1022). The workflow duplicates these gates in its receipt
Python block (lines 212--238).

Therefore:

* partial all-pass is rejected;
* a candidate with a missing or non-last zero row is rejected;
* a claimed zero cannot be obtained by sampling a fiber;
* a complete fiber with a nonzero kernel element omitted is rejected by the
  recomputed fiber size/digest and defect scan.

An empty witness list is rejected for every nontrivial kernel by checker
line 978. It is allowed only when the independently reconstructed kernel is
trivial, which is the correct exception.

## Frozen artifact and calibration bindings

The producer validates the frozen 972-word artifact, all 972 rows, canonical
row digest, target digest, tuple digest, and duplicate-free keys in
load_words (lines 203--221). The active checker repeats the source replay
and key binding independently.

For q5, the producer requires both q3 and q4 files to have their pinned
SHA-256 values and the v4 calibration schema/marker and complete 972-row
metadata (lines 729--743). The workflow additionally binds:

* calibration run ID, artifact IDs, names, and sizes (lines 19--29 and
  49--89);
* downloaded artifact paths and file SHA-256 values (lines 91--107 and
  138--153);
* legacy producer and checker source hashes (lines 129--137);
* an independent legacy checker pass for both q3 and q4 (lines 167--175).

The active q5 checker repeats the q3/q4 file hashes and calibration
contracts at lines 1023--1036. A substitute calibration, source drift, or
schema/marker drift therefore stops before a q5 receipt can pass.

## Workflow gates and failure behavior

The workflow matrix is exactly a: ["2", "4"] under the single q5 job
(lines 31--39). q3/q4 are calibration inputs only; q7 and other registered
self-test parameters are not production matrix entries.

The producer step uses set -euo pipefail, captures the producer status
through PIPESTATUS, requires exactly one recognized final status marker,
and validates the receipt metadata (lines 177--242). The checker step also
uses pipefail and requires the active D972_B4_BURAU_ACCEL_CHECK_PASS
marker (lines 244--252). Thus a status/marker disagreement fails the job.

The upload step has if: always() and uploads both ci/out/ and ci/in/
(lines 254--262), so logs and receipts are retained after producer, checker,
or gate failure. There is no continue-on-error on the producer/checker
steps, and no failure is converted to all-pass.

## Fail-open mutation audit

The following mutations were checked in code and selftests:

    partial all-pass                 rejected by scan_metadata_ok
    missing/non-last terminal zero   rejected by candidate metadata/count gates
    incomplete K                     rejected by exact kernel equality and orders
    incomplete witness list          rejected by independent closure
    empty witnesses                  rejected unless |K|=1
    status disagreement              rejected by receipt and workflow marker gates
    q3/q4 substitution               rejected by run/id/name/size/SHA/source gates
    source/hash/schema drift         rejected by workflow and active checker
    sampled/timeout/Bloom result     no such acceptance path exists

The accelerator is therefore permission-ready for the parent to
commit/dispatch. This is only a bundle audit; it is not an A/B result.

Q5_ACCEL_AUDIT_PASS

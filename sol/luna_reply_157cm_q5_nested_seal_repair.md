# Luna reply 157cm — q5 nested-seal fail-closed repair

## Verdict

The versioned repair is ready.  I changed only

    .github/workflows/d972-burau-accel-v3.yml
    sol/luna_reply_157cm_q5_nested_seal_repair.md

I did not run GAP, Git, a GHA workflow/dispatch, or q5 production.

## Repaired provenance model

The workflow now treats the downloaded archive and its embedded source seal as
two distinct immutable layers.

Outer wrapper run:

    run       32072654277
    head      303778b34e173acf6a35ad09297cf37f18dfce53
    attempt   1
    q3        id 9303461247, size 95914
              d972-burau-q5-parallel-v1-calibration-q3-attempt1
              sha256:24bf1fc9fcb7505a7fe83e7521bcc7c65a32b58947ce04edb471013e4720df24
    q4        id 9303700869, size 95831
              d972-burau-q5-parallel-v1-calibration-q4-attempt1
              sha256:38be12c17437dba07b3b1b33c82d558ba38478a059dbcbe6641fdfc0146ccf62

Inner source run:

    run       32051744038
    head      983bd8b960c5d71ef686ee0d8a590728913f61d7
    attempt   1
    q3        id 9296644565, size 95607
              d972-burau-tuple-v4-calibration-q3-attempt1
              sha256:73c561bdddcb777c83bd5e1a8e4464ed148ab074ab7f3e85d840effbb9a3f611
    q4        id 9297445824, size 95523
              d972-burau-tuple-v4-calibration-q4-attempt1
              sha256:0088f0027ea2ec3edc8e5cef853e8e2b756401ace3527785b96e92129c49510c

For each run, the API gate checks id, head SHA, run attempt, complete paginated
artifact coverage, unique id and name, size, archive digest, nonexpired state,
and the artifact's run/head backlink.  It intentionally does not require the
inner run's overall conclusion to be successful: that run failed in unrelated
lanes, while the two named artifacts are authenticated independently.

The two downloads remain the exact outer q3/q4 wrapper names from outer run
32072654277.  Their seals are now compared, with exact key equality, against
the corresponding inner run/artifact identity rather than the wrapper
identity.  Receipt SHA, q/a, all 972 ordered rows, fiber counts, unique target
keys, frozen producer/checker/word hashes, group-order fields, checker marker
cardinality, and checker exit 0 remain mandatory.

The API step writes `nested-api-binding-v3.json`; the evidence step requires
that ledger to equal a freshly reconstructed outer/inner/tag mapping and emits
one binding receipt per tag containing both layers plus the actual receipt,
seal, checker-log, and checker-status hashes.  Thus q3/q4, outer/inner run,
artifact id/name/size/digest, receipt, and seal cannot be recombined
independently.

## Hostile fixture and q5 preservation

After accepting the real downloaded q3 and q4 bundles, the workflow applies
19 bounded mutations to the same validation functions.  They cover replacing
each inner seal identity field by its outer value, both directions of q3/q4
seal and receipt exchange, a seal receipt-hash exchange, outer/inner run
exchange, q3/q4 outer and inner artifact exchange, and API-ledger receipt
exchange.  Every mutation must raise the fail-closed gate; otherwise the job
stops before q5.  No fixture invokes the q5 producer.

An offline exact-provenance object fixture using the pinned real identities and
seal schema also passed its positive case and 12 representative mutations:

    LOCAL_EXACT_NESTED_PROVENANCE_FIXTURE_PASS 12

The q5 matrix is unchanged at a=2 and a=4, `fail-fast: false`, 360 minutes,
and a 12 GB virtual-memory limit.  The producer still distinguishes an early
zero-fiber candidate from a complete 972-row all-pass receipt, binds the two
calibration receipt hashes, and is followed by the independent checker.  The
final artifact upload remains `if: always()` and includes both input bundles,
API/binding receipts, logs, status files, selftests, and any q5 receipt.

All five actions are pinned to immutable 40-hex commits.  The workflow's push
path names v3, and its uploaded artifact name is also versioned v3.

## Static and bounded audit

    YAML_PARSE_PASS
    EMBEDDED_PY_COMPILE_PASS 3
    STATIC_NESTED_BINDINGS_PASS
    IMMUTABLE_ACTION_PINS_PASS 5

Both current q5 acceleration selftests passed, including their negative
fixtures:

    D972_B4_BURAU_ACCEL_V1_SELFTEST_PASS
    D972_B4_BURAU_ACCEL_PARTIAL_ALLPASS_NEGATIVE_PASS
    D972_B4_BURAU_ACCEL_CHECKER_FINAL_MARKER status=PASS

The legacy calibration producer/checker selftests also passed:

    D972_B4_BURAU_FIBER_V4_SELFTEST_PASS
    D972_B4_BURAU_FIBER_V4_CHECKER_FINAL_MARKER status=PASS

Pinned current file hashes were rechecked:

    q5 producer       fe9ee097c50a54ffc69ce9bcb820e7ac09847581eb82a3dd2d83962aab69e2dc
    q5 checker        e36405fafb75ea3eaf096e507920b9d2ebe683e867a49a35c8f1bdcb708a0c7a
    calibration prod  aa8726570c58840a000b4b247b34eccd39a958f97087e6745216e2055b578cec
    calibration check e0b4cb923c1bd73b9afdc7f47de739f91c8aa3c0d7764c239e1df76d74fbce14
    frozen words      564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9
    workflow v3       9b88456531ba65365f06f9200ee375e41b7d183bac323ad6cbfdd1548b633c77

`bash` is unavailable in this Windows audit environment, so no `bash -n` was
run; YAML, every Python here-document, shell quoting, `PIPESTATUS`, marker
cardinality, and `always()` failure collection were inspected directly.

Q5_NESTED_SEAL_REPAIR_READY

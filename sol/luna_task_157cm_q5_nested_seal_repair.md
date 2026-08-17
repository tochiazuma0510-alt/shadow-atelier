# Luna task 157cm — q5 faststart nested-seal repair

## Role

You are Luna, implementing and hostile-auditing a small fail-closed GHA repair.
Do not run local GAP, Git, or GHA.  Modify only the new versioned workflow and
reply listed below.

## Observed failure

Run `32080494862`, job `95542402003` (`q5-a2`), failed in 30 seconds at
`Install dependencies and authenticate sealed evidence`.  The outer artifact
API authentication passed and the downloaded receipt hashes/source hashes all
match.  The error is a nested-provenance mismatch:

- outer wrapper run: `32072654277`, head
  `303778b34e173acf6a35ad09297cf37f18dfce53`, attempt 1;
- outer wrapper artifacts:
  - q3 id `9303461247`, name
    `d972-burau-q5-parallel-v1-calibration-q3-attempt1`, size `95914`, archive
    digest `sha256:24bf1fc9fcb7505a7fe83e7521bcc7c65a32b58947ce04edb471013e4720df24`;
  - q4 id `9303700869`, name
    `d972-burau-q5-parallel-v1-calibration-q4-attempt1`, size `95831`, archive
    digest `sha256:38be12c17437dba07b3b1b33c82d558ba38478a059dbcbe6641fdfc0146ccf62`.

Those wrapper artifacts intentionally contain seals for the original source
calibration run, not for the wrapper run:

- inner source run: `32051744038`, head
  `983bd8b960c5d71ef686ee0d8a590728913f61d7`, attempt 1;
- q3 inner artifact id `9296644565`, name
  `d972-burau-tuple-v4-calibration-q3-attempt1`, size `95607`, archive digest
  `sha256:73c561bdddcb777c83bd5e1a8e4464ed148ab074ab7f3e85d840effbb9a3f611`;
- q4 inner artifact id `9297445824`, name
  `d972-burau-tuple-v4-calibration-q4-attempt1`, size `95523`, archive digest
  `sha256:0088f0027ea2ec3edc8e5cef853e8e2b756401ace3527785b96e92129c49510c`.

The v2 workflow incorrectly requires the internal seal's `run_id`,
`artifact_id`, `artifact_name`, and `artifact_size` to equal the outer wrapper
provenance.  The actual internal seals correctly record the inner provenance.

## Required implementation

Create, do not overwrite:

- `.github/workflows/d972-burau-accel-v3.yml`
- `sol/luna_reply_157cm_q5_nested_seal_repair.md`

Base the workflow on v2 but separate `OUTER_*` and `INNER_*` constants.

1. Authenticate the exact outer run and exact two wrapper artifacts, including
   id/name/size/archive digest/nonexpired/run/head/attempt and uniqueness.
2. Authenticate the exact inner run and exact two source artifacts with the
   corresponding complete identity fields above.  The inner run overall may
   have failed in unrelated lanes; accept only the two pinned artifacts and
   their lossless checker evidence.
3. Download the exact outer wrapper artifacts and require their embedded
   seals to match the **inner** provenance.  Continue to require exact receipt
   SHA, source SHA, checker SHA, row coverage, checker log/exit, q/a, and every
   v2 semantic field.
4. Cross-bind the outer wrapper artifact to its inner seal and receipt: reject
   any mix-and-match between q3/q4, wrapper/source run, artifact id, receipt,
   or seal.  Do not merely weaken/delete the failed checks.
5. Preserve q5 a=2/a=4 producer/checker semantics, resource limits, candidate
   versus all-pass distinction, and always-upload failure evidence.
6. Pin all actions by immutable commit SHA.  Parse YAML and every embedded
   Python block; run existing producer/checker selftests.  Add a bounded local
   fixture test (no q5 production) showing the real nested bundle accepts and
   mutations swapping outer/inner fields reject.

The parent will commit, push, and run it.  Do not do those actions yourself.

## Output verdict

End the reply with exactly one token:

- `Q5_NESTED_SEAL_REPAIR_READY`
- `Q5_NESTED_SEAL_REPAIR_BLOCKED`

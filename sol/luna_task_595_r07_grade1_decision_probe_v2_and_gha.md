# Luna Task595: grade-one decision probe v2 plus bounded recovery workflow

## Authority and allowed writes

The researcher has repeatedly directed that heavy calculation use GHA and
that runnable work be launched without delay.  This is the narrow versioned
workflow implementation for that already authorized calculation.  Luna may
write only:

1. `search/d972_r07_a0_first_rung_grade1_decision_probe_v2.py`
2. `search/check_d972_r07_a0_first_rung_grade1_decision_probe_v2.py`
3. `.github/workflows/d972-r07-a0-first-rung-grade1-decision-v2-recovery.yml`
4. `sol/luna_reply_595_r07_grade1_decision_probe_v2_and_gha.md`

Do not modify v1/v3/v4, any certificate, proof, v220 or other workflow.  Do
not commit, push, dispatch or run the real roster; root alone is the broker.

## V2 repairs; keep the v1 scope small

Start from Task592 v1, but keep the v3 vectorized reducer and the immediate
decision-only stop.  Apply exactly these repairs:

1. Bind SHA-256 of the imported v3 producer in both the decision body and
   workflow.  The frozen value at commission is
   `bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff`.
2. Assert and record old ranks `[505,503,503,503]`, block ranks
   `[1509,1512,1512,1512]`, old logical count 2,014, block logical count
   6,045 and total cursor 8,059.
3. Do not reduce an accepted lower row twice.  Add a small local
   accept-already-reduced helper with semantics byte-for-byte equivalent to
   v3 `_accept` logic, and cover equivalence including coefficient two and a
   dependent row in the bounded fixture.  Do not adopt v4's bytewise scan.
4. The fixture producer/checker must emit and authenticate both an actual
   MEMBER decision and an actual NONMEMBER decision body.  `REFERENCE_PASS`
   alone is insufficient.  The checker remains honestly fixture-only; it
   must not call itself an independent real replay.
5. Reject an existing decision HEAD rather than silently replacing it.
   Remove a temporary file on atomic-write failure where safely possible.
6. Preserve all Task592 exclusions: no dual, ancestry/DAG, transition
   presentation, LiteralExpander, degree-two replay or repository
   certificate.

Run only py_compile and bounded fixtures locally.

## Recovery workflow

The new workflow is one production **candidate-decision** job, not a full
terminal/checker job.  It must:

- trigger by `workflow_dispatch` and by push on branch
  `sol/r07-explicit-lift-20260825` only when the commit message contains
  `[fire-grade1-decision-v2]`;
- checkout the exact pushed SHA, use Python 3.13 and pin `numpy==2.5.1`;
- authenticate the v2 producer/checker hashes, the frozen v3 hash above and
  the Task595 reply marker before any large input download;
- run py_compile plus both bounded fixtures;
- download exactly source run `33677346616`, attempt 1, prepare artifact
  `task554-grade1-v3-prepare-33677346616-1` and pattern
  `task554-grade1-v3-state-block-*-33677346616-1` with the pinned download
  action already used by the v4 recovery;
- assemble them into a fresh runner-temp directory, require the one prepare
  and four block HEADs, require no decision-v2 HEAD, and run v2 under
  `ulimit -v 8388608`, internal `TASK595_SECONDS=2400`, and outer timeout 45
  minutes;
- on success require `decision-v2.HEAD`, exactly one decision body, grade
  basis blob and remainder blob, and stage only those four files;
- upload the candidate decision state with compression level 0 and 90-day
  retention; upload all logs under `if: always()`;
- make every path and action SHA pinned, use only read permissions, and do no
  checkout mutation, commit, release upload or checker promotion.

The workflow step/log names must say candidate decision, not terminal,
cross-checked or verified.  Report exact file hashes/bytes and an honest
READY/NOT_READY verdict.  Root will review, commit, push and allow the push
trigger only after the reply is complete.


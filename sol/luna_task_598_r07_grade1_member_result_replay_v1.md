# Luna Task 598 — independent result replay for the grade-one MEMBER candidate

Role: Luna implementation.  This is a small result checker, not another
discovery engine.  Add only:

1. `crosscheck/check_d972_r07_a0_first_rung_grade1_decision_result_v1.mjs`
2. `sol/luna_reply_598_r07_grade1_member_result_replay_v1.md`

Do not modify the producer, v3/v4, workflows, proofs, v220 or existing
receipts.  Do not commit, push, dispatch GHA or run another production route.

## Exact input and independence contract

The checker accepts either:

    node <checker> --candidate <decision-artifact-dir>
    node <checker> --candidate <decision-artifact-dir> --residual <exact-residual-bin>

Use Node standard-library code only.  Do not import or copy a reducer,
packing table, JSON helper or validation helper from any repository producer.
The candidate directory has exactly the four Task595 decision files.  The
optional residual is the 6,048-byte file named by the body's
`residual_receipt` and comes from the exact sealed prepare artifact.

Authenticate and enforce:

- HEAD -> body SHA-256, then the basis and remainder receipt SHA/size;
- schema/terminal, frozen v2 and v3 producer hashes, prepare and four block
  parent digests, cursor `8059`, ranks `[505,503,503,503]` and
  `[1509,1512,1512,1512]`, old/block counts `2014+6045`, lower offers/rank
  `2014/1661`, grade offers/rank `6398/5044`, width `24192` and packed row
  length `6048`;
- when supplied, the separate residual SHA/size against `residual_receipt`
  and `residual_sha256`.

Independently decode the base-3 four-trits-per-byte format.  Reject any byte
above 80.  Check that all 5,044 basis leads are in range and unique, that the
declared lead of each row is its actual first nonzero trit, and that its lead
coefficient is normalized to one.  Check every selected coefficient has a
distinct in-range pivot and coefficient 1 or 2.

Independently sum each selected coefficient times its referenced packed basis
row over F3, in the recorded coefficient order.  The reconstructed target's
SHA-256 must equal both the authenticated `residual_receipt.sha256` and
`residual_sha256`; this gives a bounded digest-bound replay without downloading
the large prepare artifact.  When the exact residual file is supplied, also
require byte-for-byte equality, subtract the same selected combination, and
require the result to equal the emitted remainder byte-for-byte.  Recompute
trit support, packed-byte support and all hashes.
For `GRADE1_DECISION_MEMBER`, require the result to be identically zero and
the selected coefficient list nonempty.  Emit one compact JSON verdict with
all fixed counts and digests and the marker
`R07_GRADE1_MEMBER_RESULT_REPLAY_V1_PASS`.

Distinguish `DIGEST_BOUND_PASS` from the stronger `EXACT_FILE_PASS` in the
JSON, while using the requested overall PASS marker for either.  Add only a
tiny bounded selftest for coefficient 2, zero/nonzero remainder and
one mutated byte/hash rejection; no large synthetic campaign or optional
hardening.  Run syntax/selftest locally.  If the exact residual is already
available outside the repository, the reply may also record an actual replay,
but never copy artifacts into the repository.  This checker validates the
reported linear MEMBER witness against the emitted basis; it does not claim
to independently regenerate the 8,059 physical rows or prove a cofinal lift.

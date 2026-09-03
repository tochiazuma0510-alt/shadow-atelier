# Luna Task 599 — independent 8,059-row grade-one routing replay

Role: Luna implementation.  This is the one remaining replay named by
Sol(max) Task597 before the Task595 MEMBER result can be called cross-checked.
Implement only:

1. `crosscheck/check_d972_r07_a0_first_rung_grade1_full_routing_v1.py`
2. `.github/workflows/d972-r07-a0-grade1-independent-routing-v1.yml`
3. `sol/luna_reply_599_r07_grade1_independent_full_routing_v1.md`

Do not modify v2/v3/v4, Task595 artifacts, proofs, v220 or other workflows.
Do not commit, push, dispatch or run production; root is the sole broker.
The researcher's standing instruction to place heavy computation on GHA is
the narrow commander preapproval for this candidate workflow only.

## 1. Independence and exact inputs

Read Task597's reply in full.  The checker must be standalone.  It must not
import the Task595 producer, the frozen v3/v4 producer, their validators,
packing/reducer/aggregation helpers, or the Task598 result checker.  The
existing `search/check_d972_r07_a0_first_rung_grade1_v3.py` may be used as the
already independent mathematical reference for free-word/affine/occurrence
arithmetic, but the new file must contain and pin its own required code and
must not import it.  Keep only what this replay needs.

CLI:

    python -B <checker> --state <prepare-plus-four-block-dir> \
      --candidate <Task595-four-file-dir> --out <verdict.json>

Authenticate independently, using exact canonical JSON and SHA/size checks:

- source run `33677346616`, attempt 1: prepare HEAD/body/blobs and block
  0--3 HEAD/body/basis blobs, including their parent digests and ranks;
- candidate run `33707397894`, attempt 1, commit
  `93f746ad1b649796e1bc28e00ff34993498929ee`: decision HEAD/body, basis and
  remainder blobs;
- candidate body digest
  `62412762b3a208d31febb6c6b8d4707f880471ed32cf62c79c18108065ab7b5d`,
  prepare digest
  `1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865`,
  and its four block digests exactly as recorded in the body.

## 2. Independent reroute

Implement base-3 four-trits-per-byte tables and the streaming echelon owner
inside the checker.  Do not text-copy the producer's PackedEchelon.  Preserve
insertion pivot ids and a lead-to-pivot map.  Use vectorized NumPy packed AXPY
and NumPy nonzero-byte search; do not introduce Python bytewise scans, dense
full-row closure, ancestry, duals or degree-two work.

Using independently defined affine/Fourier occurrence arithmetic and physical
aggregation, route in the exact registered order:

1. the four old paired bases, ranks `[505,503,503,503]`, lower-first;
2. the four exhausted block bases, ranks `[1509,1512,1512,1512]`.

For an old row, reduce its 8,068-trit physical lower part, apply exactly those
coefficients to its 24,192-trit grade companion, normalize the companion when
a new lower pivot has leading coefficient 2, and otherwise offer the
lower-zero companion to the grade owner.  Maintain a grade companion for each
insertion-ordered lower pivot.  For a block row, independently aggregate the
18,144-trit source grade row and offer it directly to the grade owner.

Assert cursor 2,014 before the block loop and 8,059 at its end.  Emit progress
at least every 256 logical rows.  The full replay must obtain:

    lower offers/rank = 2014 / 1661
    grade offers/rank = 6398 / 5044

Require byte-for-byte equality of the independently routed packed grade basis
and exact lead list to the candidate basis
`b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d`.
Then load the authenticated prepare residual, independently reduce it, and
require zero remainder, the exact candidate remainder bytes, and the exact
3,317-pair coefficient list.  Reconstruct the residual from those coefficients
and match both candidate residual hashes.

## 3. Output and limits

The verdict is a small canonical JSON containing all input digests, cursor,
offer/rank counts, basis/lead/residual/remainder/coefficient digests, elapsed
seconds, `verified:false`, `cross_checked:false`, and marker
`R07_GRADE1_FULL_ROUTING_REPLAY_V1_PASS`.  The false cross_checked flag is
intentional: root promotes only after inspecting the independent receipt.
On mismatch or resource exhaustion, exit nonzero and emit no PASS verdict.

Add only bounded pack/echelon/old-lower coefficient-2 fixtures.  No synthetic
campaign, optional schema framework, checkpoint system, ancestry or dual.

The workflow must:

- trigger by workflow_dispatch or a push on the working branch whose commit
  message contains `[fire-grade1-independent-routing-v1]`;
- exact-SHA checkout, Python 3.13, NumPy 2.5.1 and commit-pinned actions;
- authenticate checker/reply hashes before downloads;
- download the exact source prepare/four block artifacts and exact Task595
  candidate artifact by run id/attempt-qualified names;
- run selftest, then one 40-minute internal / 45-minute outer replay under a
  7-GiB internal RSS and 8-GiB virtual-memory cap, with a 60-minute job cap;
- upload only the small verdict on success and logs under always().

Report exact bytes/SHA values, bounded test commands, expected artifact names,
and readiness.  Production output remains candidate and verified is reserved
for Lean.

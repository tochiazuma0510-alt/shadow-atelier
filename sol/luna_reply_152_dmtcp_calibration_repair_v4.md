# Luna reply 152 — direct-BQ calibration and candidate repair v4

## 判定

The v2 mainline is repaired in place and remains fail-closed. The raw
`FQ/<q_relators>` construction, `Size(Q)`, and `IsBijective(qToBase)` gates are
gone from both independent routes. No GAP was run locally. Python static tests
pass; this is not an A result by itself.

## v4 calibration route

`search/check_d972_dovetail_v2.py` now reconstructs the explicit permutation
`BQ` of order `8,817,984` from the frozen G9/P4 six-coset markings. Producer
`q_relators` are evaluated under the free-generator map
`FQ -> BQ`, and every relator must evaluate to 1. The relator list is retained
only as a digest-bound one-way consistency gate; no quotient group is built and
no quotient order or bijection is inferred.

The k=1 and k=2 scan and its 972 fiber receipts are otherwise unchanged. The
receipt schema is `d972-independent-calibration/v4-direct-bq`, with explicit
`calibration_route`, `bq_order`, and `q_relators_checked_in_bq` fields. Failure
receipts are versioned as `d972-independent-calibration-failure-v4.json` and
remain bounded, hashed, and fail-closed.

## v4 candidate route

`search/check_d972_dovetail_v1.py` now builds each finite candidate
presentation `P` independently, constructs the same explicit BQ, and directly
forms

\[
  \rho:P\longrightarrow BQ,
  \qquad (h_1,\ldots,h_{k-1},s_1,s_2)\mapsto
  (1,\ldots,1,b_1,b_2).
\]

The exact gates are: BQ order, all producer q-relators evaluate to 1 in BQ,
rho is onto, `|ker rho|=k`, the marked images are `(bs1,bs2)`, the braid
relation holds, and `|P|=k*|BQ|`. The candidate's permutation reconstruction
uses the same direct P-to-BQ map. A q-relator list that is incomplete can cause
an eligible candidate to be missed, but cannot create a false A witness,
because every accepted candidate is still checked against its finite P and
direct BQ map.

The checker summary and final-v2 seal now bind
`candidate_validation_mode=direct-explicit-permutation-BQ` and BQ order, so a
candidate accepted through an obsolete quotient route cannot produce A. Each
candidate backend also records and checks the canonical q-relator SHA-256.

## k-prefix policy

The v1 seed manifest and v2 manifest now start the active cursor at `k=8`.
The frozen `k=3..7` all-pass result is anchored to
`sol/sol_reply_151_finish.md` SHA-256
`36460bb959ec8f81efc5989e722ec2a3d1490c71a8a67f92cc18488cd3c09c2c`.
This skip has no effect on A soundness: one exact isolated zero-fiber witness
is sufficient. It grants no B or completeness authority; all k=3..7 rows are
declared `FROZEN_ALL_PASS_NOT_RECHECKED`, not freshly enumerated by v4.

The v2 manifest's DMTCP contract now records the direct-BQ route and has
contract SHA-256
`f4eb427c13561354992ff5dbed2b98d53e6dce318fa586f1afe12b616fe4b741`.
The v1 state schema's `start_k` constant is correspondingly 8 (schema SHA-256
`b4ae916cd3d7897bdb8c3d9b3be49a574451034a794039039ee985a97fb01dcf`), so an
old k=3 seed or resume state is rejected rather than silently mixed with the
new prefix policy.

## Static verification

Executed without GAP:

```text
python -B -m py_compile search/check_d972_dovetail_v1.py search/check_d972_dovetail_v2.py search/d972_dovetail_producer_v1.py search/d972_dovetail_producer_v2.py
python search/check_d972_dovetail_v1.py --self-test
python search/check_d972_dovetail_v2.py --self-test
python search/d972_dovetail_producer_v2.py --self-test
python search/check_d972_dovetail_v3.py --self-test
```

All returned exit code 0. v2 reports three calibration tamper negatives,
including direct-route tampering. No workflow YAML, dispatch, commit, or push
was performed. A future GHA run must use the existing workflow's normal
DMTCP inputs; this repair changes the referenced source files and manifest,
not the workflow contract.

**Final status:** static repair PASS; mathematical A remains pending an actual
GHA-produced direct-BQ candidate with a zero fiber and final postcheck seal.

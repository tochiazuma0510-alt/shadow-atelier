# Luna Task791 implementation receipt

## Verdict

`READY_FOR_HOSTILE_AUDIT`

The finite v512 repair is implemented in the commissioned v9/v7/v15
successors.  This is an implementation and bounded-fixture receipt only.
No GHA dispatch, production run, commit/push, or large local computation was
performed.  The actual-parent value `S=23` below is inherited from the
authenticated v14 resource result; this task did not run that resource-sized
input.

## Exact receipts

All three implementation files are LF-only and contain no NUL bytes.  The
reply file is the receipt itself and is omitted from the table because a
self-referential SHA-256 would not be stable.

| file | bytes | LF | CR | NUL | SHA-256 |
|---|---:|---:|---:|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py` | 70945 | 1272 | 0 | 0 | `1422bec44e1367c0ea22043cb7b5e844ba8e7df69e3da763bd08e372d5dc8046` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v7.py` | 109876 | 1894 | 0 | 0 | `0599759e2c2311e771439cf7bce10fd3fb0ce99f498e60a62827aa12a1a460c4` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v15.yml` | 13249 | 198 | 0 | 0 | `6710ae309ef24409e01f4e28bf2d219342b75c2ff6b49d7b6125c4014caf4f84` |

The exact newly pinned input receipts are:

| file | bytes | SHA-256 |
|---|---:|---|
| `sol/proof_r07_all_path_direct_canary_induction_repair_v512.md` | 6151 | `33997289c63c66392849ebdc81f4668172272f72057d54e383e50523059b2011` |
| `sol/sol_reply_789_audit_r07_all_path_direct_canary_induction_v509.md` | 16116 | `a862524927f04547390114f7fa2425e9760d184a30c2c236c2ecf01fe5d71d61` |

For the mechanical-successor comparison, the audited predecessor receipts
were v8 producer `59749` bytes / `1037` LF /
`9acb4edcbbfcb4b1e8815918ee39215298d8c97811e99467bb713d9b41a2875c`, v6
checker `98228` bytes / `1654` LF /
`8b3bcc7120dec651debb0d4af775c5f2429ea30481c336139252e44e5db73652`, and
v14 workflow `12320` bytes / `187` LF /
`6ce08d351d8db84448bcb4657ecbc13ba39dea7c0ddd7882b1a35265b486ada2`.

## Bounded commands and results

Only the commissioned three bounded commands were run locally:

```text
python -B -m py_compile search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v7.py
python -B search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py --selftest
python -B search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v7.py --selftest
```

`py_compile`: exit `0`, no output.

Producer v9 selftest: exit `0`, `fixture=PASS`,
`direct_schedule=S`, `direct_replay_label=reached-seed-base-plus-four-actor-v1`,
`base_canary_direct_calls=2`, `base_canary_completion=2`,
`full_prefix_generic_comparisons=0`, `actor_atom_generic_evaluations=4`,
`occurrence_components=11`, `E4_split_buckets=2`,
`noncommuting_recurrence_cases=4`, `bucket_mutation_rejections=6`, and
`generic_builders_called=false`.

Checker v7 selftest: exit `0`, `fixture=PASS`,
`direct_schedule=S`, `direct_replay_label=reached-seed-base-plus-four-actor-v1`,
`base_canary_direct_calls=2`, `base_canary_completion=2`,
`precision2_schedule=G`, `full_prefix_generic_comparisons=0`,
`actor_atom_generic_evaluations=4`, `occurrence_components=11`,
`mutation_count=55`, and `E4_split_buckets=2`.

The fixture has two reached seeds, so each side makes exactly two
`direct_column((), relators[s-1])` calls, records two complete rows, and
accepts only completion `2` with EOF.  The authenticated live-parent roster
has `S=23`; the implementation derives and compares that count from the raw
roster rather than hard-coding a universal ceiling.

## v9 producer change summary against v8

The source-universe construction, exact source keys, eleven-slot typed
signature collection, trie, full signature buckets, lower/top packing and
existing false-claim gates are retained.  The old generic
`replay_bucket_direct` production path is replaced by
`replay_reached_seed_base`: it sorts the raw reached roster before
coefficient cancellation, invokes the unchanged generic empty-path
`direct_column` once per seed, canonicalizes each complete sparse row, records
`(seed, nnz, canonical_sparse_row_sha256)`, and requires exact completion and
EOF.

The producer now also serializes and validates the four typed atom
signatures in order `(-2,-1,1,2)`, both inverse equalities, one independently
evaluated noncommuting parent*atom order anchor, and the exact v512
g-dependent eleven-prefix contract.  A rolling digest starts from 32 zero
bytes and hashes each canonical base-row record in sorted-seed order.  The
manifest has the new canary and precision2 completion fields.  The existing
full loop remains over every nonzero bucket in canonical order, with an
`aggregation_done == aggregation_total` gate; no bucket merging, sampling or
negative inference was added.

## v7 checker change summary against v6

The checker does not import v9 or any producer helper.  Its local
`IndependentAllSeven`, sparse-row canonicalizer, atom signature code, inverse
checks, order anchor, occurrence-prefix contract and rolling digest
independently recompute the reached roster/base receipt and exact-compare it
with the producer manifest.  It rejects the predecessor marker/schema and
requires the new producer marker.  Its independent replay still traverses
every full signature bucket and every coefficient-1/2 precision2 action, with
an explicit completion-count gate, before the existing payload-coordinate and
target gates.

The minimum live fixture reaches the new receipt validators and rejects the
parent*atom order swap, slot-10 inverse-sign/prefix mutations, literal
pentagon-order mutation, E4-to-E3 typed-slot mutation, base-row digest/count/
EOF mutations, and a skipped precision2 completion.  It does not add a broad
mutation farm, retry matrix, benchmark, or production-sized fixture.

## v15 workflow change summary against v14

This is a mechanical v14 successor.  It updates only the workflow/path/fire
token, v9/v7 marker/hash/size pins, v512 and Task789 audit byte/SHA pins, and
v15 artifact names.  Exact event-SHA checkout, read-only permissions,
immutable Task625/Task554/Task595 parent gates, pinned actions, Python and
NumPy versions, serial BLAS variables, memory/time limits, success-only
residual upload and always-run log upload remain unchanged.  A non-fire push
does not enter production; manual dispatch remains available for a later root
decision.  The workflow was not dispatched.

## New schemas, markers and scope

```text
producer schema       = d972.r07.a0.fresh-precision2-endpoint-signature.v9
producer marker       = R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V9_CANDIDATE
checker schema        = d972.r07.a0.fresh-precision2-endpoint-signature.v7.checker
checker marker        = R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V7_CHECKER_PASS
direct canary schema  = d972.r07.a0.reached-seed-direct-canary.v1
runtime profile       = endpoint-minimal-reached-seed-canary-v1
direct replay label   = reached-seed-base-plus-four-actor-v1
prefix-table schema   = r07.v512.actual-g-dependent-prefix-table.v1
```

The honest generic scope recorded in the canary is:

```text
31-context joint direct_column at empty path per reached seed; all-path propagation by conjugacy
```

The eleven occurrence contract is fixed as follows; the first six rows are
E3 and the final five are E4, with the actual g-dependent `prefix_hex` bound
by the producer and independently recomputed by the checker.

```text
ordinal label             block sign coordinate
1       H1_fxy            1     +1   0
2       H1_fxz            1     -1   1
3       H1_fyz            1     +1   2
4       H2_fux            2     -1   3
5       H2_fxy            2     -1   0
6       H2_fuy            2     +1   4
7       P_b1              3     +1   5
8       P_b2              3     +1   6
9       P_b3              3     +1   7
10      P_b5_inverse      3     -1   8
11      P_b4_inverse      3     -1   9
```

## Schedule and status boundary

The reduced direct schedule is `S` (one empty-path base call per reached
seed); the full precision2 schedule remains `G` with the authenticated
parent's `G=21,287` nonzero full-signature buckets.  The inherited parent
resource result was `L=21,608`, `U=13,043`, `G=21,287`, `S=23`; those values
are recorded as provenance, not as a new production claim.  No generic rows
are retained after their base digests are formed, and no dense copy or local
parallel replay was introduced.

This receipt makes no claim about rho2, A0, COMMON, a compatible lift, fake,
Ihara, or Lean verification.  The payload's `verified=false` (and related
claim gates remain false); the verdict only means the bounded implementation
is ready for the separately commissioned hostile audit.

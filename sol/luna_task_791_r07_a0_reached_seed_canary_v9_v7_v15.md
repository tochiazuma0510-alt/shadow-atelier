# Luna Task791: implement the audited A0 reached-seed canary successor

Reply only to sol/luna_reply_791_r07_a0_reached_seed_canary_v9_v7_v15.md.
Create or edit only the four files named in Section 7. Do not dispatch GHA,
run production, perform git operations, or do a large local computation.
Read every numbered section, first to last.

## 1. Authority and exact objective

Read completely:

1. sol/proof_r07_all_path_direct_canary_induction_v509.md;
2. sol/sol_reply_789_audit_r07_all_path_direct_canary_induction_v509.md;
3. sol/proof_r07_all_path_direct_canary_induction_repair_v512.md;
4. the current producer v8, checker v6 and workflow v14;
5. sol/sol_reply_779_reaudit_r07_a0_checker_two_anchor_repair_v1.md;
6. sol/sol_reply_788_root_r07_a0_v14_resource_result.md.

Implement only the finite Task789/v512 repair. On the actual parent it
replaces the expensive generic printed-equation calls 21,287 -> 23 per side.
It must leave the exact source universe, full eleven-slot signature buckets
and all 21,287 precision-two bucket aggregations unchanged.

## 2. Producer v9

Start from v8 and preserve every authentication, exact-key, endpoint, trie,
bucket, precision-two, target, lower/top, packing, receipt, resource and
false-claim gate unless this task explicitly changes it.

Replace only replay_bucket_direct and its production call by a reached-seed
base canary:

1. take the sorted raw reached-seed set before any coefficient cancellation;
2. call the unchanged generic direct_column((), relators[s-1]) exactly once
   for every reached seed;
3. canonicalize its complete sparse row and record
   (seed, nnz, canonical_sparse_row_sha256);
4. require exact completion count and EOF;
5. retain and serialize the four typed atom signatures in fixed order
   (-2,-1,1,2), both inverse equalities, and one independently evaluated
   noncommuting two-letter parent*atom order anchor;
6. bind the exact eleven labels/signs and v512 actual g-dependent prefix
   table contract; and
7. place the canonical receipt plus rolling digest in the payload manifest.

The actual count is result-derived but must be 23 for the immutable current
parent. Do not hard-code 23 as a mathematical universal ceiling; compare the
completed count to the authenticated reached roster and also record it. The
existing generic call establishes its stronger 31-context joint guard;
record that scope honestly.

Bump the payload marker/schema and runtime profile so a v8 payload cannot
masquerade as v9. Use a new direct-replay label such as
reached-seed-base-plus-four-actor-v1. Keep the existing seven payload files;
the finite canary receipt may be canonical manifest data and need not create
another large file.

## 3. Full precision-two work must remain

After the base canary, preserve the current loop over every nonzero full
signature bucket. In particular:

- compute the seed precision-two cache;
- traverse all G buckets in canonical order;
- apply each exact representative path and coefficient 1 or 2;
- form the complete lower/auxiliary and top residual;
- emit path-signatures.json and signature-buckets.json unchanged in
  mathematical content; and
- keep progress output for base-canary completion and full aggregation
  completion separately.

No signature merging beyond the current exact full signature, monomial
split, bucket sampling, early target exit, or negative inference is allowed.

## 4. Independent checker v7

Start from checker v6. Do not import producer v9 or any shared helper.
Recompute independently:

- the sorted raw reached-seed roster;
- the generic empty-path direct row for every reached seed using
  IndependentAllSeven;
- every canonical sparse row hash/count;
- the four typed atom signatures, inverse identities, noncommuting order
  anchor, labels/signs and v512 prefix-table contract; and
- the receipt canonical digest and EOF.

Compare these values exactly with the producer manifest. Then retain the
complete independent precision-two replay over all G buckets and every
existing payload-coordinate gate. Bump the checker schema/marker and require
only the new producer marker; reject a v8/v6 payload/verdict.

The live bounded fixtures must reject at least:

1. parent*atom -> atom*parent;
2. slot 10 P_b5_inverse sign - -> + or prefix G_4^-1 -> 1;
3. the existing literal pentagon-order mutation;
4. an E4-to-E3 typed-slot mutation;
5. a base-row digest/count/EOF mutation; and
6. any attempt to skip the retained full precision-two bucket loop.

Use the existing bounded anchors. Add only the minimum fixture needed to
reach the new live receipt validators; do not add a broad SELFTEST, mutation
farm, retry matrix, benchmark, or production-sized fixture.

## 5. Workflow v15

Create a mechanical successor of v14. Keep exact event-SHA checkout,
read-only permissions, immutable Task625/Task554/Task595 parents, pinned
actions, Python/NumPy versions, serial BLAS variables, memory limits,
producer/checker timeouts, success-only residual upload and always-run log
upload.

Update only the workflow/path/fire token, v9/v7 file/hash/size pins, new
producer/checker markers and v15 artifact names. Add exact byte/SHA pins for
v512 and the Task789 audit. A push without
[fire-fresh-precision2-endpoint-v15] must not run production; manual workflow
dispatch remains possible only after root later audit decision. Do not
dispatch it.

## 6. Speed and memory discipline

This repair is a loop-bound/schema change, not a rewrite. Do not rebuild the
source graph, change the 21,287-bucket precision-two arithmetic, retain
generic rows after their 23 digests are formed, introduce parallel local
Python, or add dense copies. The canary receipt is small. Report the exact
generic-call schedule exposed by a bounded fixture and whether the retained
aggregation loop is still structurally G.

Run only py_compile and the two bounded selftests. If either selftest is
surprisingly slow, stop and report the first exact cause instead of enlarging
it.

## 7. Authorized files and handoff

Create only:

- search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py;
- search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v7.py;
- .github/workflows/d972-r07-a0-fresh-precision2-endpoint-v15.yml;
- sol/luna_reply_791_r07_a0_reached_seed_canary_v9_v7_v15.md.

The reply must give exact byte/LF/SHA-256 receipts, bounded commands/results,
an AST/diff summary against v8/v6/v14, the fixture call schedule, new schema
and marker names, and an honest verdict READY_FOR_HOSTILE_AUDIT or
NOT_READY:<first-exact-reason>.
No GHA result, rho2, A0, COMMON, compatible lift, fake, Ihara or Lean
verification may be claimed. verified=false.

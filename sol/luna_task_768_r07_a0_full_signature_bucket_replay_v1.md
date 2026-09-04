# Luna Task768 - A0 full-signature bucket replay v1

## 0. Role, scope, and outputs

You are Luna.  Implement the already paper-closed, measured A0 acceleration
below.  This is a narrow implementation task, not a redesign of Task640.

Create only these four versioned outputs:

1. `search/d972_r07_a0_fresh_precision2_endpoint_signature_v8.py`
2. `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v5.py`
3. `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v13.yml`
4. `sol/luna_reply_768_r07_a0_full_signature_bucket_replay_v1.md`

Do not edit predecessors.  Do not run real parents, production A0, GHA, git,
agents, or es7ops.  Bounded sequential selftests and syntax/static comparison
are allowed.  Write temporary outputs outside the repository.

## 1. Fixed predecessors and measured reason

Read in full:

- `search/d972_r07_a0_fresh_precision2_endpoint_signature_v7.py`
- `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py`
- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v12.yml`
- `sol/proof_r07_direct_all_seven_signature_bucket_replay_v500.md`
- `sol/luna_reply_759_r07_a0_endpoint_hotspot_v7_and_workflow_v12.md`

The exact v12 run is `33820711511/1`, job `100862564074`, head
`d96a10a0e87856ec2bca8b1a7768712333b4ab12`.  Its producer completed endpoint
setup, all four atom evaluations, and all reached-seed endpoint gates in 28 s.
It then timed out in the exact-key direct phase at `274/21608`.  The steady
rate was about 15.5 s per exact key.  Therefore v500's deployment condition is
satisfied: the direct phase, not endpoint setup, is the measured bottleneck.

## 2. Exact mathematical substitution

Preserve every exact source key and every full typed eleven-slot signature.
After all exact keys have been authenticated and all path signatures have been
constructed, form the existing canonical nonzero buckets

```text
(seed, full typed 11-slot signature) -> (coefficient mod 3, representative path)
```

using exactly the same deterministic representative convention as v7/v4.
Delete a bucket iff its accumulated coefficient is zero.

Move the complete H1/H2/P `direct_column` canary after this grouping and call
it exactly once for each nonzero bucket, on that bucket's recorded
representative.  This changes the call count from `L=21608` to the actual `G`
and nothing else.  It is justified only by v500 Theorem 1.1.

Forbidden shortcuts:

- do not group by the first six slots;
- do not drop, sample, or unauthenticate exact keys or trie leaves;
- do not alter coefficients, representatives, source order, actor order,
  relation order, occurrence signs, endpoint gates, precision-two arithmetic,
  lower-zero gate, rho2 bytes, or claim flags;
- do not treat an unfinished `done/G` loop as acceptance;
- do not introduce SAT, multiprocessing, dense global closure, checkpoint
  reconstruction, or a new mathematical search space.

The producer progress meter must report the direct phase as `done/G` and must
emit `L`, `U`, and `G` before the first bucket direct call.  The existing
precision-two aggregate remains one call per nonzero bucket.

## 3. Independent checker v5

The checker must remain genuinely independent: it must not import the
producer or share a generated helper/table with it.  It must independently:

1. authenticate and reconstruct every exact key from the accepted graph and
   leaf stream;
2. check every reached seed in all eleven typed endpoints;
3. reconstruct every full eleven-slot path signature;
4. compare the complete `path-signatures.json` receipt;
5. reconstruct the exact canonical nonzero buckets and representatives and
   compare `signature-buckets.json`;
6. call its direct H1/H2/P replay exactly once per nonzero bucket;
7. recompute the final precision-two aggregate, lower-zero condition, and
   rho2 bytes independently.

Do not retain v4's generic direct evaluation of every prefix.  Reconstruct
the signatures by the checker's own identity plus its own four signed actor
atoms and typed multiplication recurrence.  Retain bounded direct recurrence
canaries in selftest; production must not restore the all-prefix direct loop.

A resource stop before all `G` direct gates or before the final independent
rho2 comparison is `UNKNOWN_RESOURCE`, never PASS.

## 4. Required adversarial fixtures

In producer and/or checker at the correct ownership boundary, add bounded
fixtures which demonstrably reject:

1. two paths which formerly share a signature after one E4 slot is mutated;
2. a wrong canonical representative for an otherwise correct bucket;
3. one reversed pentagon factor;
4. one reversed prefix action;
5. a zero-coefficient bucket that nevertheless triggers a direct call;
6. grouping by only the six E3 slots;
7. a premature direct-loop completion count.

Also positively show that two equal full signatures make one direct call and
that a coefficient `1+2=0 mod 3` bucket makes zero direct calls.  Keep fixtures
small; no real owner build is permitted.

## 5. Versioning and workflow v13

Advance producer/checker schemas and markers consistently.  The workflow is a
mechanical successor of v12 and uses the exact fire token
`[fire-fresh-precision2-endpoint-v13]`.  Pin the exact v8/v5 bytes and SHA-256
values and pin `sol/proof_r07_direct_all_seven_signature_bucket_replay_v500.md`.
Keep the accepted Task625/Task554/Task595 parents, action pins, memory caps,
serial BLAS settings, success-only residual upload, and always-uploaded logs.
Do not loosen provenance or claim flags.  A 45-minute producer/checker command
cap may remain; the purpose of the run is to measure the actual `G` path.

## 6. Required bounded evidence in the reply

Record:

- exact byte/LF/CR/final-LF/SHA-256 receipts for all four outputs except the
  reply may report itself only after content is stable;
- exact v7->v8 and checker-v4->v5 AST/function deltas;
- explicit confirmation that all arithmetic outside the v500 grouping/direct
  scheduling substitution is unchanged;
- selftest outputs, rejection counts, and proof that production direct calls
  are `G`, not `L`;
- static workflow YAML and inline-Python syntax results and all local pins;
- no real GHA/parent replay claim and no A0/fake/Ihara promotion.

Finish with exactly:

```text
A0_FULL_SIGNATURE_BUCKET_REPLAY_V1=IMPLEMENTED_CANDIDATE
SAFE_FOR_SOL_AUDIT=yes
REAL_GHA_RUN=NOT_RUN
A0=NOT_CLAIMED
FAKE=NOT_CLAIMED
IHARA=NOT_CLAIMED
verified=false
```


# Luna task 181 - task169 Gamma schema repair v1

Commissioner: Sol / 2026-08-27

Role: Luna implementation.  Repair the deterministic producer/checker schema
mismatch exposed by GHA run `33036737863`.  This is an auxiliary projected
target6 lane and must not modify the all-seven task175/176/179 mainline.

## 1. Exact observed stop

At head `f2ed3f86cc00ee1909058d9dc14465483733a441`, producer and checker each
completed the registered 5,400-second domain reconstruction.  Producer
printed

```text
R07_760_JOINT_COEFF_INTERSECTION_V1_PRODUCER_PASS state=R07_760_JOINT_COEFF_INTERSECTION_V1_PREFLIGHT_READY grade=CANDIDATE rank_B_joint=26 canaries=31 domain_seconds=5400 bytes=10802823
```

but the checker stopped at line 1010 with

```text
RuntimeError: independent marked joint image/presentation invariants
```

No positive cross-check receipt was produced.

## 2. Proven static root cause

The producer constructs `group = joint.JointGroup(...)` and stores

```python
gamma = group.invariants()
domain["joint_group_replay"]["Gamma_invariants"] = gamma
```

The value is the exact 19-key dictionary returned by frozen task157ee
`JointGroup.invariants()`.

The fixed task157ee receipt instead stores `group.public()`, which consists
of the same 19 invariants plus these six packed section/public fields:

```text
canonical_state_key
canonical_states
first_seen_BFS
section_parent_generators
section_parent_states
transitions
```

The checker compares the 19-key producer value to the complete 25-key fixed
receipt dictionary by whole-dictionary equality.  Hence it fails solely from
the key-set mismatch before relation-roster reconstruction.  This is not a
roster failure, stale pin, or differing Gamma value.

## 3. Required repair

Keep the producer's explicitly named `Gamma_invariants` schema.  In the
helper-nonshared checker:

1. freeze the exact expected 19-key invariant set;
2. reject any missing or extra key in the producer field;
3. compare it to the projection of the fixed 25-key receipt onto exactly
   those 19 keys;
4. retain the independent canonical state-row and transition digest replay
   already present at lines 1006--1014; and
5. retain all Q0 presentation, record-word, roster, coefficient, canary,
   timeout, receipt-integrity, and terminal gates.

Do not weaken the comparison to an ad hoc subset of only the 11 producer
bootstrap keys.  Do not copy the six packed public fields into the producer
under the misleading `Gamma_invariants` name.  Do not accept a legacy receipt
without exact 19-key typing.

Add a normal-path SELFTEST/schema probe which rejects at least:

- one missing invariant key;
- one extra public-section key inserted into `Gamma_invariants`;
- one changed invariant value;
- one changed state-row digest; and
- one changed transition-row digest.

All programming exceptions remain hard nonzero STOPs.  A bounded or timed
domain result retains its existing candidate/UNKNOWN scope; the repair must
not promote it to a full-E4 or all-seven result.

## 4. Files and execution discipline

Edit only the minimum necessary subset of the existing task169 producer,
checker, driver, immutable selftest fixture, plus the new reply:

- `search/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_v1.py`
- `crosscheck/check_d972_r07_760_l3_target6_joint_kernel_coeff_intersection_v1.py`
- `search/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_gha_preflight_driver_v1.g`
- the task169 immutable selftest certificate if its exact pin cascade
  requires it;
- `sol/luna_reply_181_task169_gamma_schema_repair_v1.md`

Do not edit workflows, task175/task176/task179 files, proofs, or predecessor
replies.  Do not run Python, Node, GAP, git, or GHA locally.  Parent alone
audits, commits, pushes, and dispatches.  Record every final bytes/SHA-256
identity and the exact expected 19-key list in the reply.

```text
TASK169_GAMMA_INVARIANTS_SCHEMA_REPAIR_REQUIRED
```

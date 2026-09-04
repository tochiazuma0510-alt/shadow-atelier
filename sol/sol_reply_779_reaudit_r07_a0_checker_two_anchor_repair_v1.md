# Sol(max) Task779 — focused re-audit of A0 checker two-anchor repair

## Decision

Both finite blockers from Task772 are closed.  Checker v6 adds two bounded,
selftest-only anchors which reach the installed production helpers and kill
the exact source mutations that survived v5.  No production all-prefix direct
replay was restored, and every production helper/class outside marker/schema
versioning is AST-identical to checker v5.

Workflow v14 is a mechanical, correctly pinned successor of v13.  I found no
remaining finite blocker to one authorized GHA dispatch.  This is only a
static and bounded release ruling; no parent, production A0 payload, GHA,
network, git, or delegation was used.

## Exact inputs

All listed files have zero CR and NUL bytes and end in LF.

| file | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `sol/sol_reply_772_audit_r07_a0_full_signature_bucket_replay_v1.md` | 13,899 | 305 | `cec1f97a777661f497df20c279217e151cdefa05080897c6a34f7d9d6154cb36` |
| `sol/luna_task_777_r07_a0_checker_two_anchor_repair_v1.md` | 2,509 | 51 | `2d32ea4c90a2d942905ecfde9a2b890c144035c6577e3bdf1d2ba7470608a1fd` |
| `sol/luna_reply_777_r07_a0_checker_two_anchor_repair_v1.md` | 3,639 | 101 | `a0bc0cb1b173089fdc59b48ea0883ad056d249b3792fc668fa3b75960050f28d` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v5.py` | 97,152 | 1,638 | `26bb89d85109a3c996251262be0110eb69ca29f8f0adfed8574ba9374bd30336` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v6.py` | 98,228 | 1,654 | `8b3bcc7120dec651debb0d4af775c5f2429ea30481c336139252e44e5db73652` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v13.yml` | 12,320 | 187 | `beeb0b0ece09b904402ae77c17375f65f308fa5bd37f2e2e18785ed807b123c4` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v14.yml` | 12,320 | 187 | `6ce08d351d8db84448bcb4657ecbc13ba39dea7c0ddd7882b1a35265b486ada2` |
| frozen producer v8 | 59,749 | 1,037 | `9acb4edcbbfcb4b1e8815918ee39215298d8c97811e99467bb713d9b41a2875c` |
| frozen proof v500 | 4,777 | 119 | `f0efc3d4292e512bfc8ff920c1c54ce31257310566c5e89b2981d287372a3318` |

## 1. F772-1: independent two-letter recurrence anchor — CLOSED

`bounded_two_letter_signature_anchor` uses adjacent transpositions

```text
E3 left=(1,0,2),   right=(0,2,1)
E4 left=(1,0,2,3), right=(0,2,1,3)
```

and first checks that the two orders do not commute.  Independent evaluation
with the primitive permutation multiplication gives

```text
E3 left*right=(2,0,1),   right*left=(1,2,0)
E4 left*right=(2,0,1,3), right*left=(1,2,0,3)
```

The direct expected side is constructed from those independently evaluated
two-letter values.  Only the calculated side passes through the installed
production `signature_extend_gate`, over all six typed E3 and five typed E4
slots, and the two sides meet at `signature_recurrence_gate`.

I reintroduced the exact Task772 source mutation in memory:

```python
multiply(index,left[1],right[1])
    -> multiply(index,right[1],left[1])
```

There was exactly one replacement, in the production helper.  Running the
whole mutated selftest now rejects with
`independent_trie_right_recurrence`; it no longer reaches the normal PASS
JSON.  Thus the anchor is not a copied/disconnected convention.

Production remains unchanged: `direct_signature(path)` occurs only at its
definition and in the four-atom comprehension for `(-2,-1,1,2)`.  All other
prefixes still use typed recurrence, and there is no generic direct evaluation
of every prefix.

## 2. F772-2: independent literal pentagon anchor — CLOSED

`bounded_literal_pentagon_anchor` supplies distinct singleton factors
`[[1],[2],[3],[4],[5]]` to the installed production
`pentagon_factor_word`.  The fixed displayed paper order is

```text
1,3,0,-2,-4
```

and, because `paper_product`/`cpp` reads displayed factors in reverse order,
its independently literal expected word is exactly

```text
[-5,-3,1,4,2]
```

The expected side is a literal and is not produced by
`pentagon_factor_word` or its gate.

I then reintroduced the exact Task772 mutation in memory:

```python
factors[1] -> inverse(factors[1])
```

There was exactly one replacement in `pentagon_factor_word`.  The whole
mutated selftest rejects with `pentagon_literal_order_anchor`.  This closes
the former self-referential-fixture gap while leaving the production
pentagon word itself unchanged.

## 3. AST and production non-regression — PASS

Independent function/method AST comparison v5→v6 gives exactly:

```text
ADDED   bounded_two_letter_signature_anchor
        bounded_literal_pentagon_anchor
CHANGED selftest
        main
REMOVED none
```

`selftest` changes only by calling the two bounded anchors.  `main` changes
only the checker PASS marker from V5 to V6 and the verdict schema from
`.v5.checker` to `.v6.checker`.  The payload marker correctly remains the
frozen producer-v8 V5 candidate marker.

Consequently every existing production helper and every class method is
AST-identical to v5, including:

- exact Task601/source/candidate authentication and canonical exact keys;
- the typed full eleven-slot signature and path receipt;
- mod-three bucket coefficients, zero deletion, and deterministic retained
  representative;
- the single nonzero-bucket direct loop and `done/G` gate;
- independent H1/H2/P Fox and occurrence arithmetic;
- precision-two replay, target, lower-zero gate, rho2 bytes/packing, and exact
  receipt comparisons; and
- every mathematical claim flag.

The two new functions are called only from `selftest`.  They add no production
copy, dense closure, parent read, direct loop, or other slow path.  Exact-key
authentication and the full-signature `G` schedule accepted in Task772 are
unchanged.

## 4. Bounded replay

The unmodified bounded runs produced:

```text
producer-v8 --selftest                         PASS
  direct_schedule                              G
  full_prefix_generic_comparisons              0
  equal_signature_direct_calls                 1
  zero_bucket_direct_calls                     0
  E4_split_buckets                             2

checker-v6 --selftest                          PASS
  mutation_count                               49
  direct_schedule                              G
  full_prefix_generic_comparisons              0
  equal_signature_direct_calls                 1
  zero_bucket_direct_calls                     0
  E4_split_buckets                             2

exact reversed-prefix source mutant            REJECTED
  reason                                        independent_trie_right_recurrence
exact reversed-pentagon-factor source mutant   REJECTED
  reason                                        pentagon_literal_order_anchor
```

The unchanged mutation count is correct: the two new tests are positive
source-mutation anchors, not additional entries in `fixture_rejects`.

## 5. Workflow v14 — PASS

Workflow v14 parses as YAML and contains 12 steps.  Its only differences from
v13 are the expected mechanical version changes:

- workflow/path/fire token `v13 -> v14`;
- checker path `v5 -> v6`, exact size `98,228`, and exact SHA-256
  `8b3bcc7120dec651debb0d4af775c5f2429ea30481c336139252e44e5db73652`;
- bounded compile/selftest and production invocation select checker v6;
- checker marker and result/log artifact names select v6/v14.

The frozen producer-v8 and proof-v500 pins match their physical bytes.  All
seven `uses` entries remain pinned to 40-hex action commits.  The accepted
Task625 run/attempt/head/job/artifact gates, Task554 and Task595 parents,
local proof/source pins, exact event checkout, read-only permissions, and
Python 3.13 setup are byte-for-byte inherited from v13.

Serial BLAS variables remain `1`; the job timeout remains 120 minutes; the
production shell retains `set -euo pipefail`, the 8-GiB virtual-memory cap,
and separate 45-minute producer/checker hard timeouts.  Residual upload is
success-only and log upload is always-run.  No infrastructure or search-space
change was introduced.

This authorization does not promote a future payload or make an A0, fake, or
Ihara claim.

```text
VERDICT=PASS_A0_CHECKER_TWO_ANCHOR_REPAIR_V1
SAFE_TO_DISPATCH_GHA=yes
FINITE_BLOCKERS_CLOSED=2/2
EXACT_KEY_AUTHENTICATION_RETAINED=yes
DIRECT_REPLAY_SCHEDULE=G
REAL_GHA_RUN=NOT_RUN
A0=NOT_CLAIMED
FAKE_IHARA=NOT_CLAIMED
verified=false
```

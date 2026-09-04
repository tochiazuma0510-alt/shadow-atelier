# Sol(max) Task772 — hostile audit of A0 full-signature bucket replay v1

## Decision

The v500 coalescence theorem is sound in the stated left-Fox convention, and
the production substitution from exact-key direct replay to full eleven-slot
bucket replay is implemented correctly.  Producer v8 and checker v5 retain the
exact-key universe, use the full typed signature, and have production direct
schedule `G`, with no reachable `L`-sized direct loop or generic all-prefix
direct loop.

Dispatch is nevertheless blocked by exactly two finite checker-selftest
defects.  The two expressly commissioned source mutations—reversing the
prefix action and reversing one pentagon factor—both survive checker v5's
bundled selftest.  These are not requests for new infrastructure or additional
mathematics.  They are missing independent bounded anchors at the two named
ownership boundaries.

No real parent, production payload, GHA run, git operation, or additional
agent was used.

## Audited bytes

All inputs below are LF-only, contain zero CR bytes, and end in LF.

| input | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `sol/luna_task_768_r07_a0_full_signature_bucket_replay_v1.md` | 6,423 | 146 | `7945150e9e3432b946d1b1d3f5780d418240a2541ac998219391fbd32e07c713` |
| `sol/luna_reply_768_r07_a0_full_signature_bucket_replay_v1.md` | 9,986 | 239 | `22f2255472101d267d594e133c20802c4a49ef8b50c079a3d285020bbc729251` |
| `sol/proof_r07_direct_all_seven_signature_bucket_replay_v500.md` | 4,777 | 119 | `f0efc3d4292e512bfc8ff920c1c54ce31257310566c5e89b2981d287372a3318` |
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v7.py` | 54,803 | 925 | `6e26e6b96eb610e29dfd191040cea604e7768a643ed2ef916033c8449373e465` |
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v8.py` | 59,749 | 1,037 | `9acb4edcbbfcb4b1e8815918ee39215298d8c97811e99467bb713d9b41a2875c` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py` | 93,236 | 1,592 | `581f9a5a9aa65ae298bf6d6f785ed1063ddfb0caf8a0c06e15f30ec2e713fd6f` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v5.py` | 97,152 | 1,638 | `26bb89d85109a3c996251262be0110eb69ca29f8f0adfed8574ba9374bd30336` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v12.yml` | 11,976 | 183 | `1ac07ad79e218f7926e1db95bf19fcfa94042dc80c4f80fadcb32815015f2d3d` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v13.yml` | 12,320 | 187 | `beeb0b0ece09b904402ae77c17375f65f308fa5bd37f2e2e18785ed807b123c4` |

## 1. v500 theorem — PASS

For one registered occurrence, the left Fox rules give

\[
D(PrP^{-1})=D(P)+q(P)D(r)+q(P)q(r)D(P^{-1}).
\]

The reached-seed gate supplies `q(r)=1`, and
`D(P^{-1})=-q(P)^{-1}D(P)`.  The first and third terms therefore cancel,
leaving exactly

\[
D(PrP^{-1})=q(P)D(r).
\]

For fixed seed, every H1/H2/P occurrence then has the form
`sign * fixed-prefix * q_j(P) * D_j(r_s)`.  Its block, sign, prefix, seed
derivative, and serialization position are fixed.  Thus equality of every
`q_j(P)` implies equality of every occurrence row and hence of the complete
serialized H1/H2/P row.  The exponent part is also fixed: conjugation
preserves the relator's exponent pair, which is zero at this boundary.

The implementation's occurrence tuple is

```text
(0,1,2,3,0,4,5,6,7,8,9)
```

with six typed E3 slots followed by five typed E4 slots.  Coordinate `0` is
retained at physical positions 0 and 4; even though its value bytes coincide,
the two tuple positions retain their distinct fixed occurrence data.  The
proof consequently authorizes grouping only by `(seed, full typed 11-slot
signature)`.  Neither endpoint identity nor the first six E3 slots determine
the five P occurrences, so no six-slot or endpoint-only shortcut follows.

## 2. Producer v8 — PASS

Before grouping, v8 authenticates the fixed Task601 manifest and every exact
file receipt, hashes the complete physical files, parses the pinned literal
leaf stream, authenticates its ancestry binding, and binds the exact MEMBER
candidate and source state.  It forms reached seeds from the uncancelled raw
prior-plus-leaf terms and forms the canonical exact keys separately.

Every path prefix is then present in the trie.  The trie starts from an
explicit six-E3/five-E4 identity, evaluates only the four signed actor atoms,
and extends by typed right multiplication.  Only after that complete trie and
all reached-seed endpoint gates are available does
`canonical_signature_buckets` form keys

```text
(seed, full_signature_gate(signatures[path]))
```

where `full_signature_gate` requires all eleven positional tags and byte
values.  Iteration remains over v7's sorted canonical terms; coefficient
addition remains modulo three; assignment retains v7's last encountered path
as representative; and the final comprehension removes exactly coefficient
zero.  The precision-two aggregation consumes this same canonical nonzero
bucket dictionary.

`replay_bucket_direct` has one direct call site inside its one bucket loop.
It rejects coefficients outside `{1,2}`, checks the seed, invokes the unchanged
`all_seven.direct_column` once, increments `done`, applies the resource guard,
reports progress, and finally requires `done == G`.  No exact-key direct call
remains.  Hence its production direct schedule is exactly `G`, including
`G=0`.

## 3. Checker v5 core replay — PASS subject to the two fixture blockers

Checker v5 does not import producer v8, the producer's runtime module, or a
generated producer table.  It carries an independent word/permutation/PC/Fox
implementation, authenticates the fixed Task601 files and literal leaves,
reconstructs the canonical exact keys and raw reached seeds, rebuilds the ten
underlying coordinates and their full eleven-slot typed projection, and
checks every reached seed in all eleven endpoint positions.

Production path signatures start from the checker's own typed identity.  Its
own `direct_signature` is called only for the four signed atoms
`(-2,-1,1,2)`; every other prefix uses the checker's typed multiplication
recurrence.  It compares the complete path-signature receipt, independently
forms the same `(seed, full 11-slot signature)` buckets and deterministic
representatives, compares the bucket receipt, and calls its unchanged
`IndependentAllSeven.direct_column` once per nonzero bucket.  It then performs
its own precision-two action/aggregation, direct target, lower-zero check,
dense and packed rho2 comparisons, roundtrip gate, and exact receipt checks.

The checker therefore does not trust producer arithmetic.  The remaining
failure is narrower: its bounded selftest does not independently anchor two
of those production conventions.

## 4. Exact finite blockers

### F772-1 — reversed checker prefix action survives selftest

The production recurrence is at checker lines 434–437 and is called for every
nonempty prefix at lines 585–591.  Its current expression is the correct
right action:

```python
multiply(index, left[1], right[1])
```

The fixture at lines 507–510 computes `good` through that same helper, then
passes the opposite callback to the same helper and compares the two.  It has
no independently evaluated two-letter word.  Consequently swapping the sole
production expression to

```python
multiply(index, right[1], left[1])
```

still makes the checker report its complete normal PASS JSON, including
`actor_multiplication=PASS`, `mutation_count=49`, and
`full_prefix_generic_comparisons=0`.  Both the fixture's baseline and its
opposite are transposed together.  The producer's genuine direct-vs-recurrence
fixture cannot discharge the checker's expressly independent obligation, and
production comparison with `path-signatures.json` is a producer receipt, not
a checker-side direct anchor.

Smallest repair: in checker selftest only, evaluate at least one
noncommuting two-letter word directly in a tiny E3 and E4 model, extend the
same two atoms through `signature_extend_gate`, and require equality.  The
source mutant above must fail.  This does not restore the production
all-prefix direct loop.

### F772-2 — reversed checker pentagon factor survives selftest

The current helper at lines 415–420 spells the same five-factor word as v4,
so static inspection finds no present arithmetic change.  The new production
gate is nevertheless self-referential: `_pentagon` obtains `value` from
`pentagon_factor_word` and `pentagon_factor_gate` recomputes its expected value
with that identical helper.

Changing the helper's first displayed positive factor from

```python
factors[1]
```

to

```python
inverse(factors[1])
```

also leaves the complete checker selftest PASS JSON unchanged.  The fixture
at lines 525–527 constructs both its baseline and its reversed input through
the mutated helper, so it checks only internal consistency with the helper;
it does not anchor the commissioned pentagon order.  This is exactly a
one-factor reversal, not extra hardening.

Smallest repair: add one bounded literal-order anchor using distinct,
non-involutive toy factors and an expected word independently spelled from
the fixed order `1,3,0,-2,-4`.  With the fixture's singleton factors, for
example, the paper-product convention has literal expected word
`[-5,-3,1,4,2]`.  The source mutant above must fail.  No production group or
parent data is needed.

## 5. Other requested mutations and bounded checks

The remaining commissioned boundaries are live and reject as required:

- changing one E4 slot splits the former single bucket into two;
- an otherwise correct bucket with the wrong retained representative is
  rejected against canonical reconstruction;
- a malicious zero-coefficient bucket is rejected before its callback, while
  `1+2=0 mod 3` produces no bucket and no direct call;
- a map keyed only by the six E3 slots is rejected;
- `done=0, G=1` is rejected as premature completion; and
- two equal full signatures produce one call on the retained representative.

The unmodified bounded runs were:

```text
producer-v8 --selftest: PASS
  direct_schedule=G
  equal_signature_direct_calls=1
  zero_bucket_direct_calls=0
  E4_split_buckets=2
  bucket_mutation_rejections=4
  actor_atom_generic_evaluations=4
  full_prefix_generic_comparisons=0

checker-v5 --selftest: PASS
  mutation_count=49
  direct_schedule=G
  equal_signature_direct_calls=1
  zero_bucket_direct_calls=0
  E4_split_buckets=2
  actor_atom_generic_evaluations=4
  full_prefix_generic_comparisons=0

checker reversed-prefix source mutant:          SURVIVED (blocker)
checker reversed-pentagon-factor source mutant: SURVIVED (blocker)
```

## 6. AST, call graph, and slow-path audit

The independent AST comparison found exactly these deltas.

- Producer v7→v8 adds `_tiny_bucket_fixtures`,
  `canonical_signature_buckets`, `full_signature_gate`,
  `replay_bucket_direct`, `validate_direct_completion`, and
  `validate_signature_buckets`; only `evaluate` and `selftest` among existing
  functions change, and none is removed.
- Checker v4→v5 adds `full_signature_gate`, `pentagon_factor_gate`,
  `pentagon_factor_word`, `replay_bucket_direct`,
  `validate_direct_completion`, and `validate_signature_buckets`.  The changed
  existing scopes are `signature_bucket_gate`, `validate_payload`,
  `manifest_header_gate`, `fixture_rejects`, `selftest`, `main`, and
  `IndependentAllSeven._pentagon`.  No scope is removed.

`IndependentAllSeven.direct_column` is AST-identical to v4.  The v5
`_pentagon` helper currently expands to v4's exact factor order.  Source keys,
physical occurrence/Fox arithmetic, coefficients, target construction,
precision-two action and aggregation, lower gate, rho2 packing, and all claim
flags are otherwise unchanged.

The reachable production work is now:

```text
exact authentication/canonical keys     O(L)
typed trie/signature construction        O(U)
direct all-seven replay                  O(G)
precision-two replay                     O(G)
```

There is no production exact-key `direct_column` loop, no direct evaluation
of every prefix, no multiprocessing, no SAT, no boundary/dense global
closure, no checkpoint reconstruction, and no generic heavy-builder path.
The full path-signature and bucket serializations are required receipts rather
than hidden arithmetic.  No second reachable slow path was found; the two
blockers above concern bounded mutation ownership only.

## 7. Workflow v13 — PASS as a mechanical dispatch wrapper

The YAML parses and has 12 steps.  Its push fire token is exactly
`[fire-fresh-precision2-endpoint-v13]`.  All seven actions are pinned to
40-hex commits.  It pins the exact v8, v5, and v500 bytes/digests above, along
with the retained local proof/reply/prebuild pins.  The accepted Task625 run,
attempt, head, job, artifact id/name/size/digest and success conclusion are
fixed; the Task554 and Task595 parent run/artifact identities are retained.

Serial BLAS variables remain `1`; the job cap is 120 minutes; the production
shell applies the 8-GiB virtual-memory cap and separate 45-minute producer and
checker hard timeouts under `set -euo pipefail`.  Result upload is
success-only and logs are always uploaded.  Producer/checker compile,
selftest, invocation, marker, and artifact names consistently select v8/v5.
The wrapper introduces no runtime/search-space change beyond the v500
scheduling substitution.

The workflow is mechanically sound, but it must not be dispatched with the
two explicitly required checker mutation anchors still absent.

```text
VERDICT=BLOCKED_FINITE_A0_FULL_SIGNATURE_BUCKET_REPLAY_V1
SAFE_TO_DISPATCH_GHA=no
FINITE_BLOCKER_COUNT=2
BLOCKER_1=CHECKER_REVERSED_PREFIX_SOURCE_MUTATION_SURVIVES_SELFTEST
BLOCKER_2=CHECKER_REVERSED_PENTAGON_FACTOR_SOURCE_MUTATION_SURVIVES_SELFTEST
EXACT_KEY_AUTHENTICATION_RETAINED=yes
DIRECT_REPLAY_SCHEDULE=G
REAL_GHA_RUN=NOT_RUN
A0=NOT_CLAIMED
FAKE_IHARA=NOT_CLAIMED
verified=false
```

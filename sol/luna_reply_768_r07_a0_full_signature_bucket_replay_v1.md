# Luna Task768 - A0 full-signature bucket replay v1

## Result

The v500 substitution is implemented as a bounded candidate.  All exact keys
and all typed eleven-slot path signatures are still reconstructed.  The
complete H1/H2/P direct canary now runs once per canonical nonzero full-
signature bucket, so its production call count is `G`, not `L`.

Only the four designated outputs were created:

- `search/d972_r07_a0_fresh_precision2_endpoint_signature_v8.py`
- `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v5.py`
- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v13.yml`
- `sol/luna_reply_768_r07_a0_full_signature_bucket_replay_v1.md`

No real parent, accepted artifact, production A0 run, GHA, git, es7ops, or
other agent was used.  Temporary bytecode was directed outside the repository.

## Exact receipts

Every measured output below contains zero CR bytes and ends in LF.

| output | bytes | LF | CR | final LF | SHA-256 |
|---|---:|---:|---:|---|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v8.py` | 59,749 | 1,037 | 0 | yes | `9acb4edcbbfcb4b1e8815918ee39215298d8c97811e99467bb713d9b41a2875c` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v5.py` | 97,152 | 1,638 | 0 | yes | `26bb89d85109a3c996251262be0110eb69ca29f8f0adfed8574ba9374bd30336` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v13.yml` | 12,320 | 187 | 0 | yes | `beeb0b0ece09b904402ae77c17375f65f308fa5bd37f2e2e18785ed807b123c4` |

The stable reply receipt is intentionally not embedded into the reply itself,
because adding that receipt would change the bytes it purports to hash.

For comparison, the predecessors are:

| predecessor | bytes | LF | SHA-256 |
|---|---:|---:|---|
| producer v7 | 54,803 | 925 | `6e26e6b96eb610e29dfd191040cea604e7768a643ed2ef916033c8449373e465` |
| checker v4 | 93,236 | 1,592 | `581f9a5a9aa65ae298bf6d6f785ed1063ddfb0caf8a0c06e15f30ec2e713fd6f` |
| workflow v12 | 11,976 | 183 | `1ac07ad79e218f7926e1db95bf19fcfa94042dc80c4f80fadcb32815015f2d3d` |

Textual deltas are producer `+128/-16`, checker `+67/-21`, and workflow
`+22/-18` lines.

## Producer v8

After authenticating every exact key and constructing the complete trie, v8
forms the same canonical dictionary as v7:

```text
(seed, full typed 11-slot signature)
    -> (coefficient mod 3, last canonical encountered path)
```

The representative update and mod-three zero deletion are unchanged from the
inline v7 bucket code.  New gates require exactly six typed E3 slots followed
by five typed E4 slots.  Grouping by the first six slots therefore cannot
enter the production bucket map.

Only after bucket construction and the state cap does the producer emit one
line containing exact `L`, `U`, and `G`.  It then enters one bucket loop with
one `direct_column` call site.  The callback receives the stored canonical
representative.  Each completed call retains `guard(started)` and the existing
throttled meter now receives
`endpoint_direct_column_done=done/G`.  An exact completion gate requires
`done == G`; a resource stop or premature loop cannot accept.  The existing
precision-two aggregation remains one call per same nonzero bucket.

The manifest advances to schema
`d972.r07.a0.fresh-precision2-endpoint-signature.v5` and marker
`R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V5_CANDIDATE`.  The runtime profile
records `direct_replay=full-11-slot-nonzero-buckets` and pins v500 at SHA-256
`f0efc3d4292e512bfc8ff920c1c54ce31257310566c5e89b2981d287372a3318`.
All claim flags remain unchanged and false.

## Independent checker v5

Checker v5 remains self-contained and does not import the producer or share a
generated table/helper with it.  It independently authenticates the accepted
graph/leaf stream, rebuilds all exact keys, checks every reached seed after
expansion to all eleven typed endpoint slots, and constructs every full path
signature.

The old production all-prefix direct signature comparison was removed.  The
checker now constructs its own typed identity from its own E3/E4 identities,
directly evaluates exactly its own four signed actor atoms `-2,-1,1,2`, and
uses its own typed right-multiplication recurrence for every prefix.  Static
inspection finds `direct_signature(path)` only at its definition and four-atom
cache construction; production generic full-prefix comparisons are zero.

It compares the complete `path-signatures.json`, independently reconstructs
the canonical full-signature buckets and representatives, and compares
`signature-buckets.json` before direct replay.  Its single bucket loop has one
`direct_column` call site and a `done == G` terminal gate.  It then independently
recomputes the precision-two aggregate, lower-zero condition, packed/dense
rho2 bytes, and exact receipts as before.  A resource stop before all direct
gates or the final rho2 comparison remains `UNKNOWN_RESOURCE`.

Checker schema/marker advance consistently to v5.  The implementation of
`IndependentAllSeven.direct_column` is AST-identical to v4.  `_pentagon` is
the only changed method in that class; its five-factor word is unchanged and
is now passed through the v500 order gate used by the reversed-factor fixture.

## Adversarial fixtures

The bounded producer/checker fixtures cover all requested cases:

1. mutating one E4 slot splits two formerly equal full signatures into two
   buckets;
2. changing the otherwise correct bucket's canonical representative is
   rejected;
3. reversing one positive pentagon factor is rejected by the order gate;
4. reversing prefix multiplication is rejected by the existing noncommuting
   typed recurrence canary;
5. a malicious coefficient-zero bucket is rejected before its callback can
   make a direct call;
6. a map grouped by only the six E3 slots is rejected against the canonical
   full-signature map; and
7. `done=0,total=1` is rejected as premature completion.

Positive fixtures show two equal full signatures produce one direct call on
the retained representative, while coefficients `1+2=0 mod 3` produce an
empty bucket map and zero direct calls.  Producer reports four new bucket-
boundary mutation rejections.  Checker mutation count advances from 44 to 49;
the E4 split and the two positive scheduling witnesses are positive gates and
are not included in that rejection count.

## AST/function boundary

Producer v7 to v8 adds only:

```text
_tiny_bucket_fixtures
canonical_signature_buckets
full_signature_gate
replay_bucket_direct
validate_direct_completion
validate_signature_buckets
```

Its only changed existing functions are `evaluate` and `selftest`; none is
removed.  Checker v4 to v5 adds only:

```text
full_signature_gate
pentagon_factor_gate
pentagon_factor_word
replay_bucket_direct
validate_direct_completion
validate_signature_buckets
```

Its changed existing scopes are `signature_bucket_gate`, `validate_payload`,
`manifest_header_gate`, `fixture_rejects`, `selftest`, `main`, and the
`IndependentAllSeven` class solely because `_pentagon` gained the order gate.
No scope is removed.

All producer arithmetic outside full-signature grouping and direct scheduling
is AST-identical to v7.  All checker target, occurrence, Fox, direct-column,
precision-two, lower-zero, and rho2 arithmetic outside the v500 substitution
is AST-identical to v4.  Both production call graphs contain exactly one
`replay_bucket_direct` call, no exact-key `direct_column` call, and exactly one
direct call inside one loop over the nonzero bucket dictionary.

## Workflow v13

Workflow v13 is a mechanical successor of v12 with fire token exactly
`[fire-fresh-precision2-endpoint-v13]`.  It pins the exact v8/v5 receipts above
and v500 at 4,777 bytes/SHA-256
`f0efc3d4292e512bfc8ff920c1c54ce31257310566c5e89b2981d287372a3318`.
Compile, selftest, real producer/checker invocation, checker marker, workflow
path, and artifact names are versioned consistently.

The accepted Task625/Task554/Task595 acquisition, exact event checkout, seven
pinned action uses, source/proof gates, serial BLAS settings, 8-GiB virtual
memory cap, 45-minute producer and checker command caps, success-only residual
upload, and always-uploaded logs are unchanged.  No SAT, multiprocessing,
dense closure, checkpoint reconstruction, connection pass, retry, or new
search space was introduced.

The supplied measured deployment condition is recorded without promotion:
v12 run `33820711511/1`, job `100862564074`, head
`d96a10a0e87856ec2bca8b1a7768712333b4ab12` completed endpoint setup in 28 s
and stopped at exact-key direct progress `274/21608`.  Task768 does not rerun
or independently certify that historical measurement.

## Bounded sequential checks

```text
py_compile producer-v8 + checker-v5
  PASS; 0.268244 s

producer-v8 --selftest
  PASS; 0.334611 s
  direct_schedule=G
  equal_signature_direct_calls=1
  zero_bucket_direct_calls=0
  E4_split_buckets=2
  bucket_mutation_rejections=4
  actor_atom_generic_evaluations=4
  full_prefix_generic_comparisons=0

checker-v5 --selftest
  PASS; 0.268095 s
  mutation_count=49
  direct_schedule=G
  equal_signature_direct_calls=1
  zero_bucket_direct_calls=0
  E4_split_buckets=2
  actor_atom_generic_evaluations=4
  full_prefix_generic_comparisons=0

exact AST/function comparison
  PASS; 0.258663 s
  checker direct_column AST equal=true

production direct-call static audit
  PASS; 0.051770 s
  producer exact-key direct calls=0
  checker exact-key direct calls=0
  one direct call site in one nonzero-bucket loop on each side

workflow YAML and inline-Python syntax
  PASS; 0.144266 s
  steps=12; inline Python blocks=0; pinned action uses=7

workflow local SHA gates
  17/17 repository-path SHA gates PASS
```

No output is an A0, fake, Ihara, cross-check, or Lean verification claim.  An
authorized real GHA run and subsequent Sol audit remain necessary.

A0_FULL_SIGNATURE_BUCKET_REPLAY_V1=IMPLEMENTED_CANDIDATE
SAFE_FOR_SOL_AUDIT=yes
REAL_GHA_RUN=NOT_RUN
A0=NOT_CLAIMED
FAKE=NOT_CLAIMED
IHARA=NOT_CLAIMED
verified=false

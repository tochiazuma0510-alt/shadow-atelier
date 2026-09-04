# Luna reply 777 — A0 checker two-anchor repair v1

## Outcome

Implemented exactly the two bounded checker-selftest anchors requested by
Task777.  Producer v8 and proof v500 were not changed.  No real parent,
production A0 run, GHA, git, network, or delegation was used.

## Repair 1: independent noncommuting two-letter anchor

`bounded_two_letter_signature_anchor` installs distinct adjacent
transpositions in tiny E3 and E4 permutation models and first asserts that
the two orders do not commute.  It obtains the two atoms independently,
evaluates their two-letter direct values with `pmul(left,right)`, and compares
those values with the result returned by the installed production helper
`signature_extend_gate`.

The anchor is selftest-only.  It evaluates one bounded two-letter case per
tiny group and does not restore a production all-prefix direct replay.

The exact source mutant

```text
multiply(index,left[1],right[1])
    -> multiply(index,right[1],left[1])
```

exits 1 at `independent_trie_right_recurrence`.

## Repair 2: literal pentagon-order anchor

`bounded_literal_pentagon_anchor` calls the installed
`pentagon_factor_word` with distinct non-involutive singleton word factors.
Its expected value is independently written as the literal paper-order word
`[-5,-3,1,4,2]`; it does not call `pentagon_factor_word` to construct the
expected side.

The exact first-positive-factor mutant

```text
factors[1] -> inverse(factors[1])
```

exits 1 at `pentagon_literal_order_anchor`.

## Non-regression boundary

An AST comparison against checker v5 reports:

```text
CHANGED ['selftest', 'main']
ADDED ['bounded_two_letter_signature_anchor',
       'bounded_literal_pentagon_anchor']
REMOVED []
AST_BOUNDARY_PASS
```

`main` differs only in checker receipt marker/schema versioning.  Every
existing production helper and class—including exact-key authentication,
full eleven-slot signatures, bucket coefficient/representative construction,
the G-scheduled direct replay, precision-two arithmetic, target, lower gate,
rho2 path, and claim gates—is AST-identical to checker v5.

## Bounded test evidence

- producer v8 `--selftest`: PASS; direct schedule G,
  `full_prefix_generic_comparisons=0`, equal-signature calls 1,
  zero-bucket calls 0, E4 split buckets 2.
- checker v6 `--selftest`: PASS; `mutation_count=49`, direct schedule G,
  `full_prefix_generic_comparisons=0`, equal-signature calls 1,
  zero-bucket calls 0, E4 split buckets 2.
- reversed-prefix in-memory source mutant: expected FAIL/exit 1 at
  `independent_trie_right_recurrence`.
- reversed-pentagon-factor in-memory source mutant: expected FAIL/exit 1 at
  `pentagon_literal_order_anchor`.
- bounded compile: PASS.
- workflow YAML parse: PASS, 12 steps.
- workflow checker path/size/SHA pin: PASS.

## Exact identities

- `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v6.py`
  - bytes: 98228
  - SHA-256: `8b3bcc7120dec651debb0d4af775c5f2429ea30481c336139252e44e5db73652`
  - LF/CR/NUL: 1654/0/0
  - final byte: 10 (LF)
- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v14.yml`
  - bytes: 12320
  - SHA-256: `6ce08d351d8db84448bcb4657ecbc13ba39dea7c0ddd7882b1a35265b486ada2`
  - LF/CR/NUL: 187/0/0
  - final byte: 10 (LF)

Workflow v14 keeps producer v8 frozen, selects checker v6 consistently,
uses `[fire-fresh-precision2-endpoint-v14]`, and retains immutable parents,
serial caps, success-only residual upload, and always-uploaded logs.

No dense closure, heavy SELFTEST, infrastructure, or production arithmetic
was added.  Claim flags remain unchanged and no A0/fake/Ihara result is
claimed.

READY_FOR_SOL_AUDIT=yes

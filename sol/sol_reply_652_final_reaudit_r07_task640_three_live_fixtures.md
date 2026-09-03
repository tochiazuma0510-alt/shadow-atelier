# Sol(max) Task652: final bounded re-audit of Task640's three live fixtures

## Verdict

`FAIL`

`SAFE_TO_DISPATCH_GHA=no`

The ancestry-binding fixture and packing-roundtrip fixture are genuine live-gate
tests.  The occurrence fixture correctly detects reverse traversal and
multiplication order, and its declared result `[id,C,C]` is correct.  One
required Task651/652 case remains open: changing production's negative
base-factor rule from inverse to non-inverse leaves the checker selftest green.
No production run, GHA dispatch, implementation edit, or git operation was
performed.

`verified=false`

## Frozen inputs

No `INPUT_MISMATCH` occurred.

| file | bytes | LF lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 27,474 | 304 | `060202458e8643acb1ed42d2ad94b9f192406c57b803dc7f3b07897c39115ef7` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 91,687 | 1,557 | `354218ecbb89ad9f80baa5ea3c4fd605e7fe44dc7e8f86301e9d72cd9d4e7905` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml` | 9,974 | 161 | `ec098e294bbbaef958a984bd050a0d049ede17bd4d624bb4ad1053ac88bb7205` |
| `sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md` | 2,972 | 58 | `6cc0d60259f9b760e2f3a6ea9d67867ed1e5dfa573462bb97d67a0af0705749b` |

The complete Task652 mail is 3,104 bytes / 55 LF lines / SHA-256
`a11632002244fa66cf9dadce3edc6485c764231cb9fef8c09b02cd3c7f9724be`.
I also read the complete Task649 reply (9,556 / 185 /
`50bad0cdcd31fdbc7e4dc453c64cc244703f068a39cc35870c60ced9674b170c`),
Task651 mail (2,548 / 51 /
`4460dc18fa2265decf7562201bb5587ca22e39b9aa17a5b83a4ec4d31376f7c1`),
and Task651 reply (1,770 / 36 /
`65a54d65555f124a537080e0bcbcb82b1c836ed7e734fae58e84a7b4b463f649`).

## Three charged fixtures

### Ancestry binding -- PASS

Checker production calls the live `parse_literal_leaves` at lines 250--267
from line 321.  Selftest lines 549--557 pass the same otherwise-valid
`R07LEAF1` bytes first with their correct digest and then with the wrong
`'33'*32` digest.

A bounded in-memory mutation deleting only
`or binding.hex()!=ancestry_digest` at line 253 made selftest fail with
`fixture_ancestry_binding_mutation`.  The fixture therefore charges the live
binding comparison.

### Occurrence prefix/order -- partial PASS; inverse-choice blocker

Production and selftest call the same `occurrence_prefix_gate` at lines
384--395: production at line 1358 and the S3 fixture at line 441.  With
`pmul(x,y)[i]=y[x[i]]`, let

- `id=(0,1,2)`, `A=(1,0,2)`, `B=(0,2,1)`, and `C=(2,0,1)`;
- the reverse suffix traversal gives prefixes `p3=id`, `p2=C`, `p1=C*B=A`;
- the final block product is `A*A=id`;
- hence `U1=A*A=id`, negative `U2=p2=C`, and `U3=id*C=C`.

Thus the fixed expected value at line 442 is independently confirmed as
`[id,C,C]`.  In-memory mutations changing `reversed(indices)` to `indices`, or
changing the prefix multiplication side at line 389, both made selftest fail
with `checker base prefix identity`.

The inverse choice is nevertheless not tested.  Production constructs a
signed base factor inline at line 1354:

`factor = base if sign > 0 else self.old.inv_word(base)`.

The fixture supplies an already-signed `base_factor` directly to the helper,
and its sole negative element is `B`, an involution: `B^-1=B`.  Therefore an
exact bounded in-memory mutation of line 1354 to `factor = base` left checker
selftest fully green with `mutation_count=42`.  This is the required
sign/inverse-choice mutation, not optional hardening.

Smallest finite repair: factor line 1354 into one signed-base-factor helper
used by production and selftest, and charge its negative branch with an
order-three S3 element `q` for which `q^-1 != q`.  Keep the existing prefix
fixture for reverse traversal and multiplication order.  The repaired
selftest must fail when that shared helper's negative branch returns `q`
instead of `q^-1`.

### Packing roundtrip -- PASS

The live gate is `dense_result_gate` at lines 414--417, called by production at
line 528 and by the fixture at lines 456--461.  In the charged fixture,
`target_dense` and `lower_dense` are exact, `rho2_dense` equals
`bad_top.tobytes()`, and `rho2_packed` equals the supplied all-zero
`bad_packed`; therefore lines 415--416 pass.  Only line 417 rejects because
unpacking the all-zero row differs from `bad_top`, whose first trit is one.

A bounded in-memory mutation disabling only line 417 made selftest fail with
`fixture_mutation_accepted`.  The fixture therefore charges the live unpacking
roundtrip branch.

## Regression surface

The previously accepted F646-A/B and R1/R3/R4/R5/R7 surface did not regress:

- exact parent JSON types and receipts remain strictly compared at lines
  465--480; workflow lines 112--118 retain the exact Task595 v2 artifact;
- raw reached seeds are gated before cancellation at lines 485--487, typed
  endpoint checks cover all reached seeds at lines 490--494, and the local
  all-seven/direct-occurrence path terminates in the live equality gate at
  line 1493;
- checker-rebuilt signatures/buckets and bucket-only dense replay remain at
  lines 501--528;
- ancestry is stream-hashed at lines 307--316 with no ancestry DOM, and live
  record/path/trie/state caps remain at lines 254, 496, 500, and 520;
- exact false/null claim gates remain at lines 363--364 and 530--540;
- the checker retains independent arithmetic and no forbidden producer
  import/exec path;
- workflow hashes match the frozen producer/checker/reply, all seven actions
  use full 40-hex pins, and lines 39--42 retain the inert `false &&` guard.

## Bounded serial checks

- External-cache `py_compile` of producer and checker: `PASS`.
- Producer `--selftest`: exit 0, `leaf_live_mutations=4`.
- Checker `--selftest`: exit 0, `mutation_count=42`.
- PyYAML safe parse: `PASS`.
- Forbidden shared import/exec scan: `PASS`.
- Immutable-action scan: `PASS`; seven full 40-hex pins.
- Frozen workflow producer/checker/reply pins and inert guard: `PASS`.
- Tiny live-gate mutations: ancestry comparison rejected, roundtrip deletion
  rejected, reverse traversal rejected, multiplication-side reversal rejected,
  but production negative-inverse deletion survived.

## Claim boundary

This audit proves no rho2 value, grade-two MEMBER/NONMEMBER result, A0,
compatible cofinal lift, FAKE, IHARA, cross-check, or Lean verification.  A
future PASS after the one finite repair would authorize only the fresh-rho2
Task640 GHA run.  The frozen quartet is not authorized for dispatch.

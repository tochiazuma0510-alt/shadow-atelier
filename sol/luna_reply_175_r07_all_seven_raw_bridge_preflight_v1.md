# Luna reply 175 - R07 all-seven raw bridge preflight v1

Date: 2026-08-27
Role: bounded mechanical/static implementation repair (175b and the
post-production base-target repair).

## Result

Static GO for another isolated GHA SELFTEST/PRODUCTION attempt.  Runtime and
the mathematical terminal remain UNKNOWN because this repair commission
forbade local Python, GAP, Node, Git, GHA, and workflow dispatch.  No such
process was started.

The task-175 producer no longer references the undefined names
`h1_base_target`, `h2_base_target`, and `p_base_target`.  It now preserves the
actual base gradient returned by each direct Fox evaluation, independently
assembles the same three base gradients by the literal prefix/product rule,
requires exact sparse-row equality, and only then emits
`raw_base_targets.H1/H2/P`.  The independent checker performs the same two
reconstructions with checker-local group/Fox code.

The target convention is now explicit and load-bearing:

```text
raw_base_targets.R = T_R = nabla R(g760)                  (not negated)
raw_changes.R      = nabla R(f1) - nabla R(g760)
stacked_target     = block-tagged raw_changes canary
task177 target     = -T, reconstructed from raw_base_targets
```

Thus task175 does not alias the v110 target to the canary change row.  The
tuple/list repair for run `33035595114` is retained unchanged.  No positive
mathematical result is claimed.  Orbit images, membership, column generation,
affine solving, correction search, lifts, cofinal claims, fake claims, and
Ihara witnesses remain outside this preflight.

## Final artifact identities

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_all_seven_raw_bridge_preflight_v1.py` | 57008 | `89ea5f2366c403afacb281ac5d817bbf813aa653316435831eee5c151647bd94` |
| `crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py` | 79737 | `c887bb747f5c51b6495b493e189ab8daff62a29c2bed964c1813e3001a6a8f0b` |
| `search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g` | 14855 | `dfdd11276105c681f283062fefd5cbff28b1c6b0a61142b1e0f14db29d6a7528` |
| immutable fixture `search/certs/d972_r07_all_seven_raw_bridge_preflight_v1_20260827.json` | 6870 | `0d9a9588cd4f58531923dc208819f32d552006eea8e323a198382901d132c69f` |

The reply is necessarily hashed by the parent after its final byte is written;
it cannot contain its own non-self-referential SHA-256.

## Base-target diagnosis and producer repair

The prior producer constructed a receipt entry using
`h1_base_target`, `h2_base_target`, and `p_base_target`, but those identifiers
had no reachable definitions.  This would have produced a deterministic
`NameError` after the expensive raw replay even though the preceding
`change(group_obj, base, corrected)` function already held the required
`base_grad` locally.

The narrow meaning-preserving repair is at producer lines 393--410 and
706--754:

1. `prefix_formula` still returns corrected-minus-base, base value, and
   corrected value, and now also returns its independently assembled
   `base_gradient`.
2. `change` still computes corrected-minus-base and now also returns the
   direct `base_grad` instead of discarding it.
3. The H1, H2, and P calls bind those three direct base gradients to the
   formerly undefined identifiers.
4. For every block, serialized direct base Fox and literal prefix-product
   base gradients must agree.  A mismatch stops at the typed root
   `UNKNOWN_INPUT:RAW_FORMULA`, with detailed reason
   `base_direct_prefix:<block>`.
5. The receipt's `raw_base_targets` is populated from those authenticated
   direct base rows.  There is no coefficient negation in task175.

This is not an alias to the canary rows.  Producer lines 774--855 retain the
base-target rows and change rows as separate typed objects.  The new
`raw_base_target_stacked_confusion` mutation physically replaces all three
base-target rows by the corresponding direct change rows and changes their
provenance.  The same producer algebraic validator then rejects them against
both the direct base rows and the prefix-assembled base rows.

The earlier tuple/list fix is still present at producer lines 536--537:

```diff
- c1 = reduce_word(left_u + base_relation + old.inv_word(left_u))
- c2 = reduce_word(right_u + base_relation + old.inv_word(right_u))
+ c1 = reduce_word(left_u + base_relation + tuple(old.inv_word(left_u)))
+ c2 = reduce_word(right_u + base_relation + tuple(old.inv_word(right_u)))
```

Only the Python container is normalized; the signed words remain the literal
conjugates `u r u^-1` and `v r v^-1`.

## Helper-independent checker repair

The checker has no source loader or executable import of the producer.  It
retains local implementations of free reduction, substitution, paper
products, g760, permutation arithmetic, PC collection, E3/E4, the typed maps,
literal hexagons and pentagon, left Fox, translation, D1/D2, and sparse
serialization.

At checker lines 1117--1165 it now:

- directly computes `fox(E3,H1(g760))`, `fox(E3,H2(g760))`, and
  `fox(E4,P(g760))`;
- independently rebuilds each base gradient from its literal factor list and
  prefix transports using checker-local `product_gradient`;
- checks each quotient value and each exact serialized sparse row; and
- emits its canonical `raw_base_targets` only after those checks.

`compare_ready` then compares every receipt base-target row and digest with
this independent reconstruction.  The checker mutation
`raw_base_target_stacked_confusion` substitutes its independently reconstructed
H1/H2/P change rows for the base targets and sends the result through the
normal reconstruction/validation path.  It must be rejected before receipt
promotion; a cancelled mutation is also fail-closed.

The semantic suite therefore has 20 ordered attempted/rejected cases, with
the new case immediately before the terminal envelope control:

```text
correction_left_right, corrected_base_sign, H2_u_z, inverse_fox_prefix,
negative_pentagon_factor_4, negative_pentagon_factor_5,
negative_pentagon_order, coface_slot_1_3_swap, E3_E4_rank_swap,
E3_E4_blob_swap, context_name_only_dedup, dropped_block_tag,
fourth_third_deletion_swap, fine_insertion_index_4_3_swap,
derived_u_order, derived_z_order, one_actual_roster_letter,
actual_product_additivity_term, raw_base_target_stacked_confusion,
terminal_marker
```

Static extraction found the producer semantic list and checker list to be
byte-order equal, both with count 20.  The checked-in immutable fixture still
contains the historical 19-name list.  The checker accepts that legacy list
only when the receipt terminal is exactly
`UNKNOWN_RESOURCE:LOCAL_EXECUTION_GUARD`; READY and every other terminal must
carry the current 20-name contract.  The fixture was not modified because it
was outside this repair's authorized files.

## Static audit and pin cascade

The producer, checker, driver, and immutable fixture contain zero bytes above
ASCII 127.  Exact static pin audit found:

```text
literal predecessor pins: 16/16 PASS
variable-path fixture pin: PASS (6870 bytes, 0d9a9588...)
variable-path producer pin: PASS (57008 bytes, 89ea5f23...)
variable-path checker pin: PASS (79737 bytes, c887bb74...)
overall driver pin audit: PASS
```

The driver pin cascade is at lines 110--113.  The prior producer/checker pins
`acec0196...` / `4b52450c...` and placeholders are absent from the final
producer/checker/driver bundle.  The final driver is ASCII-only and has the
identity in the table above.

Static definition/use search found every H1/H2/P base-target use dominated by
its direct binding; `prefix_formula` has exactly three call sites, all unpack
the returned base gradient; and `change` has exactly three call sites, all
unpack the direct base gradient.  The checker import scan found no
`importlib`, `exec_module`, `module_from_spec`, producer helper import, or
predecessor source loader.

No Python parser, Python selftest, GAP parse, or runtime was invoked under the
explicit prohibition.  Consequently syntax/runtime execution is UNKNOWN,
not reported as PASS.  The static control-flow, delimiter, identifier, ASCII,
hash, and pin audits are the evidence for the present static GO.

## Historical execution evidence

Production run `33035595114` completed the workflow with terminal-agreeing
fail-closed output:

```text
terminal=UNKNOWN_RESOURCE:runtime
reason=UNKNOWN_RESOURCE:runtime:TypeError:can only concatenate tuple (not "list") to tuple
```

That evidence motivated the retained tuple normalization above.  It does not
test the current base-target repair.

At the time of this commission, production run `33037668730` had already been
started from old head `26d93f92`.  It was deliberately left untouched.  Its
source/checker pins predate the final identities above, so regardless of its
terminal it is historical evidence only and cannot promote this repaired
bundle.

Earlier SELFTEST run `33034589606` established the old driver's fixture path
only (`terminal=FIXTURE_PASS`).  Earlier production run `33034678957` stopped
at `UNKNOWN_INPUT:RAW_FORMULA:roster`; that roster guard was subsequently
repaired by retaining all 6,441 lossless rows and requiring a nonempty word
only for the deterministic canary.  None of these old runs is a READY result
for the current source hashes.

## Exact rerun preambles

SELFTEST, quote-free GAP binding:

```gap
D972_R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_V1_MODE:=List([83,69,76,70,84,69,83,84],CharInt);;
Read("search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g");
```

PRODUCTION, quote-free GAP binding:

```gap
D972_R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_V1_MODE:=List([80,82,79,68,85,67,84,73,79,78],CharInt);;
Read("search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g");
```

Generic workflow fields:

```text
out_dir:      ci/out
timeout_min:  180
packages:     false
```

The driver rejects pre-existing outputs and runs exactly one producer followed
serially by one checker under `timeout 9000s bash -o pipefail` with
`set -euo pipefail`.  READY requires the full receipt gate, exact producer /
checker terminal agreement, one marker each, and the independent 20-mutation
replay.  A typed UNKNOWN remains an honest fail-closed result.

## Boundary

The only positive task175 terminal is
`R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_READY`; it has not been obtained for these
final hashes.  The checked-in fixture remains
`UNKNOWN_RESOURCE:LOCAL_EXECUTION_GUARD`.  All claim-boundary booleans remain
false, including orbit image, column generation, affine membership, final
correction, lift, cofinal, fake, and Ihara witness.

R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_V1_STATIC_READY

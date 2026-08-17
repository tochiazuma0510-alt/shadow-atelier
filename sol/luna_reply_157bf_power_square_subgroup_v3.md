# 157bf — D972 power spectrum v3 / square-generated subgroup

## Scope

The v2 failure is preserved and repaired in a new v3 bundle.  No local GAP,
git, push, or GHA was run in this Luna task.  The requested mojibake path
`docs/蟇ｾ隧ｱ蟶ｳ.md` was read through its repository filename
`docs/体制と道具.md` before implementation.

## Exact v2 failure and v3 repair

GHA run `32057032451` reached the full scan and failed at
`D972BlockRestrict(p, B.component9_degree, 9)`: the `row.f` values are full
20,520-point pure-model elements, not elements known to preserve an arbitrary
27/9 block.  Recovering a compact element by restricting those blocks was
therefore invalid.

The v3 producer constructs the marked maps, using only the pinned generators,

    fullF2 = Group(B.s1^2, B.s2^2)  ->  B.compact_pure
    B.s1^2 |-> B.compact_x,
    B.s2^2 |-> B.compact_y.

It requires both marked homomorphisms to exist and be bijective and checks the
four generator images.  Every one of the 972 full rows is transported through
the marked inverse, round-tripped back to the full model, and checked against
the already frozen normal-form key.  The compact key routine is applied only
after this transport; no block restriction is applied to a full row, and no
unmarked `IsomorphismGroups` result is used.  The receipt binds this exact map,
records `row_round_trip_count=972`, and records
`block_restriction_on_full_rows=false`.

The frozen 972-key digest, literal Proposition 2.14 / equations (2.52),(2.55)
orientation, all 945,441 products, identity, two-sided inverses, exact orders,
square/cube maps, direct-product/Schreier data, and independent 972-action and
associativity reconstruction are retained.  Outside labels remain explicitly
`UNKNOWN_MISSING_AUTHENTICATED_LABEL` and are not inferred.

## Square-generated subgroup certificate

The producer serializes the complete 972-entry square map (including repeated
values), its distinct-image count, the sorted member list of

    X2 = < x*x : x in X >,

the canonical member-list SHA-256, the identity seed, and a deterministic
parent/generator/child closure trace.  It independently checks identity,
inverse, and product closure before writing the receipt.  The observation is
emitted only after these gates as exactly
`SQUARE_GENERATED_ORDER_243` or
`SQUARE_GENERATED_ORDER_OTHER_<n>`; the closure algorithm does not use 243 as
an input.

The Python checker rebuilds the 972-by-972 table from the artifact and the
independent action model, then starts at the independently recomputed identity
and applies all independently recomputed squares by explicit finite closure.
It compares the full sorted member list, digest, square image size, order
scalar, seed, and closure trace, and checks subgroup identity/inverse/product
closure.  Its bounded selftest rejects an in-memory mutation of a square-map
cell, a square-generator cell, a member, a product-table cell, and a forged
generated-order scalar.

## B4-B boundary

The finite consequence is conditional and precise.  If the authenticated
result is `|X2|=243`, an arithmetic subgroup `A <= X` has `|A|=324`, and
`[X:A]=3`, then `X2` cannot be contained in `A`, since containment would force
the subgroup-order divisibility `243 | 324`, which is false.  Therefore any
subgroup `I` with `A <= I <= X` and `X2 <= I` is strictly larger than `A`; the
prime index then forces `I=X`.

The missing premise is not weakened: at an isolated finer B4 stage `K`, one
still needs actual compatible typed lifts whose reductions contain every roof
square.  The finite roof power table alone does not establish `X2 <= I_K`, so
this bundle does not claim B4-B.

## Versioned files

Created only:

- `search/d972_power_spectrum_v3.g`
- `search/check_d972_power_spectrum_v3.py`
- `.github/workflows/d972-power-spectrum-v3.yml`
- `sol/luna_reply_157bf_power_square_subgroup_v3.md`

The workflow supports `workflow_dispatch`, binds all producer/checker/runtime
input hashes, runs selftests before the bounded full computation, emits an
honest `UNKNOWN_TIMEOUT` receipt on timeout, runs the independent checker on a
complete receipt, and uploads evidence on every outcome.  GAP 4.16.0 is set by
`gap-actions/setup-gap` commit
`f12222f1b86ce1f8a246c4000abfd6e69893411c`; checkout and artifact actions are
also commit-pinned.

Static and bounded checks passed:

    V3_STATIC_MARKED_INVERSE_PASS
    V3_STATIC_SQUARE_RECEIPT_PASS
    V3_PY_AST_PASS
    V3_WORKFLOW_HASH_BINDING_PASS
    YAML_WORKFLOW_DISPATCH_PASS
    D972_POWER_SPECTRUM_V3_CHECKER_SELFTEST_PASS

SHA-256:

    e9a11a427ce133f4f561528f8c78dd25e668cb24f53cff30a756fc546e362d87  search/d972_power_spectrum_v3.g
    adc92aef61da3f96a593c7acfc6f3b7ab95a93d57ae5d4e3dbcd848381f3097f  search/check_d972_power_spectrum_v3.py
    0879a789d3ac29c32d3b5bb4f7433f266358a72f46c2757099929a5f33b28039  .github/workflows/d972-power-spectrum-v3.yml

Expected GHA markers:

    D972_POWER_SPECTRUM_V3_GAP_SELFTEST_PASS
    D972_POWER_SPECTRUM_V3_GAP_FINAL
    D972_POWER_SPECTRUM_V3_CHECKER_SELFTEST_PASS
    D972_POWER_SPECTRUM_V3_CHECKER_PASS
    SQUARE_GENERATED_ORDER_243
    SQUARE_GENERATED_ORDER_OTHER_<n>

POWER_SPECTRUM_V3_READY_FOR_GHA

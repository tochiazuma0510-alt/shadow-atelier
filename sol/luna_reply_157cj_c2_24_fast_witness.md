# Luna reply 157cj — C2^24 fast lossless witness

## Status

`157CJ_FAST_WITNESS_READY` (candidate bundle; no GHA/GAP run was executed in
this task).  The v1 bottleneck was the 24 calls to
`PreImagesRepresentative` in the full `E^4 x H9` permutation image.  The v2
producer contains no such full-image preimage call.  Its only
`PreImagesRepresentative` calls are the 24 coordinate calls in an explicitly
bounded group `E` of order 32256.

The four authorized files are:

* `search/d972_d972core_c2six_intersection_v2.g`
* `search/check_d972_d972core_c2six_intersection_v2.py`
* `.github/workflows/d972-d972core-c2six-intersection-v2.yml`
* this reply

## Exact fast construction

The pinned `G9` has derived-series length at most three.  Hence every subgroup
of the actual four-coordinate image `H9 <= G9^4` is metabelian, and the
identity

`[[a,b],[c,d]] = 1`

holds in `H9`.  For each coordinate the producer starts with the pinned pure
commutator word and enumerates the seed plus its twelve conjugates by the six
free generators and their inverses.  It accepts a seed only when its explicit
source word replays to the identity in `G9^4` and to a nonidentity element in
the requested E-coordinate with every other E-coordinate exactly identity.
Thus pure-coordinate control is an actual replay gate, not an appeal to a
Goursat existence statement.

The 13 resulting law words are evaluated in the requested E-coordinate.  The
producer checks that their generated permutation group has order 32256, uses
`PreImagesRepresentative` only for this coordinate E group, expands each of
the six module-basis preimages back to a signed word in the original six
generators, and replays every expanded word independently in all three models:

* E^4: the requested one of the six V-basis elements in exactly one coordinate;
* P^4: identity;
* G9^4: identity.

This stores 4 x 6 = 24 lossless source words and retains the v1 target/rank
gates (`f2_rank=24`, `order=2^24`, and the four six-element coordinate blocks).
The retained structural statement is still conditional on the pinned 157bb
isolation input and the direct-product/Goursat argument; this bundle does not
claim the final cofinal B4 conclusion.

The receipt also records the 13-word coordinate solver data and the explicit
`full_joint_preimage_calls=0` invariant.  The existing G9^4 image construction
is retained for the v1 factor/solvability gates; only the expensive full
E^4 x H9 preimage problem is removed.

## Independent checker and fail-closed behavior

The Python checker independently rebuilds the pinned E/V and P models, all
four maps and six tuple rows, the MakeGn(9) model, and the four-coordinate
replays.  It checks, for every fast record:

* the metabelian law and the four seed operand replays;
* exact E-coordinate support of every seed and solver value;
* the claimed coordinate solver order 32256 and closure of all 13 values;
* P^4/G9^4 identity for every solver word;
* all 24 final source words, their E targets, and their P/G9 identities;
* the unchanged v1 pure-coordinate, factor-order, action, map, source, and
  terminal-status gates.

The checker keeps the producer SHA binding and the workflow binds both v2
source files plus every frozen receipt/helper hash.  A mutated pinned map or
pure witness is rejected by the checker self-test.

## Workflow safeguards

The new workflow is manual-dispatch capable and path-triggered only by its
own v2 workflow/producer/checker and the frozen input files.  It pins GAP
4.16.0 and the JSON package setup, pins every action to an immutable 40-hex
commit (including `setup-gap` at
`f12222f1b86ce1f8a246c4000abfd6e69893411c`), and has a fail-closed static
gate rejecting mutable or malformed `uses:` refs.  It uses a 55-minute GAP timeout inside a
60-minute job, emits `UNKNOWN_TIMEOUT` rather than a mathematical result on
timeout, and uploads `ci/out/` on every outcome.  Both GAP completion and the
final checker use short standalone markers so line wrapping cannot turn a
successful run into a false marker result.

Expected parent-side dispatch (not run here):

```text
gh workflow run d972-d972core-c2six-intersection-v2.yml --ref sol/d972-dmtcp-provision-v420
```

The main-route observation that one fixed obstruction row may eventually need
only one coordinate does not replace this task's required full 24-word/rank
witness.  No such contract weakening was made here.

## Static checks performed

No local GAP, Git operation, GHA dispatch, or credential was used.

* `python search/check_d972_d972core_c2six_intersection_v2.py --self-test`
  → `D972_CORE_INTERSECTION_V2_CHECKER_SELFTEST_PASS`
* Python AST parse → `PY_AST_PASS`
* PyYAML parse of the workflow → `YAML_PARSE_PASS`
* exact extraction of the YAML-literal awk command with no escaped quotes →
  `ACTION_AWK_LITERAL_STATIC_PASS`
* every workflow `uses:` reference is immutable 40-hex → `ACTION_REF_GATE_PASS`
* producer/checker/workflow SHA binding check → `HASH_BINDING_PASS`
* bounded Python model sanity replay found an E-pure metabelian-law seed and a
  13-value E closure of order 32256 in each of the four coordinates; this is
  only a pre-GHA sanity check, not the GAP receipt.

Final SHA-256 bindings:

```text
search/d972_d972core_c2six_intersection_v2.g
57b340ad02d2864355ed5e2bd4c6ee4500a4509dafd5152e71c84b513b2738ad

search/check_d972_d972core_c2six_intersection_v2.py
c84519d3d0f9d9e5d97c229220ef95cf178f8948661fd67663cda1b388619a90

.github/workflows/d972-d972core-c2six-intersection-v2.yml
45f14fba45498cb16f0a0da9455a249f78bc57a367518a135932b59e9b8bc879
```

The GHA receipt is still required before treating the bundle as
cross-checked.

The first dispatch, run `32083286058`, stopped before the hash stage because
the action-ref fixture had literal backslashes around the awk string quotes.
The v2 workflow now contains the valid YAML-literal shell form
`awk '$1 == "uses:" { print $2 }'`; no mathematical or producer logic was
changed.

## Post-run checker binding repair

Run `32086984144` completed the producer with rank 24, but the independent
checker stopped at its fail-closed producer binding gate.  The checker still
contained the superseded producer SHA `40aa4c...`, while the repaired producer
and workflow bind `57b340ad02d2864355ed5e2bd4c6ee4500a4509dafd5152e71c84b513b2738ad`.
The authorized repair changes only that checker constant; the workflow checker
binding is refreshed to the resulting checker SHA below.  The run is therefore
evidence of successful producer mathematics plus an operational binding
failure, not a cross-checked receipt; a parent-dispatched rerun is required.

Updated bindings:

```text
search/check_d972_d972core_c2six_intersection_v2.py
79325fb7a441890552baa04f84c141f56cfeebeb612c90c24049d15105f55e05

.github/workflows/d972-d972core-c2six-intersection-v2.yml
(refreshed to the checker SHA above)
```

## Post-run producer convention repair

Run `32083594772` completed the producer's mathematical computation (including
rank 24) in about one second, but the independent checker failed at
`P tuple table mismatch at 1,3`.  The cause was a genuine convention mismatch:
the producer's `D972BDMatPerm` used the old column/Mobius formula, while the
checker intentionally uses the canonical row-vector action
`(left,right) -> (left,right)M` with affine coordinate `second/first`.

The authorized producer was repaired minimally.  Its infinity and affine
branches now use exactly the checker formula; the independent
abstract-to-canonical quotient homomorphism gate and all E/G9 logic are
unchanged.  The workflow producer binding was refreshed.  This repair is not
a mathematical result and requires a parent-dispatched rerun before the
bundle can be called cross-checked.

Current bindings after the repair:

```text
search/d972_d972core_c2six_intersection_v2.g
57b340ad02d2864355ed5e2bd4c6ee4500a4509dafd5152e71c84b513b2738ad

search/check_d972_d972core_c2six_intersection_v2.py
c84519d3d0f9d9e5d97c229220ef95cf178f8948661fd67663cda1b388619a90

.github/workflows/d972-d972core-c2six-intersection-v2.yml
45f14fba45498cb16f0a0da9455a249f78bc57a367518a135932b59e9b8bc879
```

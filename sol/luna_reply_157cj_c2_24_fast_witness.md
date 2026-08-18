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
* every workflow `uses:` reference is immutable 40-hex → `ACTION_REF_GATE_PASS`
* producer/checker/workflow SHA binding check → `HASH_BINDING_PASS`
* bounded Python model sanity replay found an E-pure metabelian-law seed and a
  13-value E closure of order 32256 in each of the four coordinates; this is
  only a pre-GHA sanity check, not the GAP receipt.

Final SHA-256 bindings:

```text
search/d972_d972core_c2six_intersection_v2.g
40aa4ce7ff0250f41369348335c4f42bbffe699cc5b0b8b6123b9d2b13042058

search/check_d972_d972core_c2six_intersection_v2.py
c84519d3d0f9d9e5d97c229220ef95cf178f8948661fd67663cda1b388619a90

.github/workflows/d972-d972core-c2six-intersection-v2.yml
ee086dea03fe8abb8b8ebb4341e8fb59c22c76a1569a4f36ca5fa22dd3269af2
```

The GHA receipt is still required before treating the bundle as
cross-checked.

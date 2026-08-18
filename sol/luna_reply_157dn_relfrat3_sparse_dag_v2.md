# Luna reply 157dn — relative-Frattini-3 sparse provenance DAG v2

Date: 2026-08-18

## Verdict

The versioned v2 producer, independent checker, and same-job driver are
implemented without changing the running v1 files.  The q3 artifact,
candidate order and caps, normalized exponent-7 x complete 27-fibre inverse,
literal equations, Fox orientation, translation BFS, geometric checkpoints,
positive predicate, and the three honest terminals remain fixed.

`B345_RELFRAT3_SPARSE_DAG_V2_GO`

## Frozen semantic reference

All three v2 components fail closed on drift of the final v1 sources:

```text
v1 producer  4b73fbfe19bb33a9decdec5fda437f58f61a3ecb1989090bd08151f60ce6609e
v1 checker   3d86240237229b250943c4795c24c32ac75af9229534c73d16bd838f6d6d0101
v1 driver    fce9b3ba8c9b686fb6af2bd5a6da1b29f7486616948a6907982af14cd5d8738b
```

The pre-existing q3 source/artifact/formula SHA gates are unchanged.

## Sparse provenance DAG

The v1 expanded coefficient dictionary has been removed from every pivot.
A v2 pivot contains only its sparse Fox vector and one provenance node id.
The shared immutable F3 DAG has two node forms:

- a left-translated PB4 relator leaf, bound to the relator index and an exact
  quotient translation whose section word is replayed through the common
  element registry;
- a topological linear-combination node with coefficients in `{1,2}` and
  only backward references.

Column reduction and target elimination append constant-size provenance
operations.  Dependent columns and failed candidate solves are transactional:
their new nodes/edges are rolled back, while persistent pivot nodes remain.
Each successful residual returns one root id.  On a positive result the
producer takes the union reachable from all selected roots, discards every
other search node, renumbers the union in topological order, and serializes
that shared DAG once.  Per-residual certificates contain only their root id
and independently reconstructed target gradient; no expanded boundary ledger
or ledger sum is serialized.

The checker independently reconstructs every leaf from the PB4 presentation
and quotient, applies every F3 DAG operation, verifies the DAG digest and
node/edge counts, rejects forward references and unreachable serialized
nodes, and requires every root vector to equal the independently rebuilt Fox
gradient.  Producer booleans are not positive evidence.

## Resource and timeout contract

The receipt accounts separately for:

- live sparse pivot-vector entries;
- pivot count;
- live and peak DAG nodes;
- live and peak DAG edges;
- elimination-operation count and maximum transient vector support.

The added fail-closed caps are 1,000,000 pivots, 2,000,000 DAG nodes, and
4,000,000 DAG edges; the pre-existing 1,000,000 sparse-entry cap is retained.
Any hit returns `B345_RELFRAT3_UNKNOWN_RESOURCE` and claims no obstruction.

The producer has a monotonic 18,000-second (300-minute) soft deadline, leaving
30 minutes below the 330-minute job limit.  Checks occur throughout candidate
preparation, translation BFS, elimination, and positive serialization.  A hit
is recorded with its last phase and check count, then atomically written as
`UNKNOWN_RESOURCE`; it is never converted to a candidate failure.  The
checker binds the timeout configuration and the exact equivalence between
`hit=true` and the soft-timeout resource terminal.  Selftest never constructs
or consults the deadline.

For both `SEARCH_INCOMPLETE` and `UNKNOWN_RESOURCE`, the checker requires
`claim_classification=unknown_not_obstruction`, absence of a proof DAG and
selected pair, and explicit non-obstruction fields.  Only
`LITERAL_PAIR_PASS` is classified as mathematical progress.

## Expected performance effect

This is a source-level expectation, not a production benchmark.  In v1 each
pivot elimination updated a potentially large expanded coefficient map, so
both time and memory scaled with the accumulated ledger support of each row.
In v2 the same elimination updates one sparse vector and appends a two-edge
DAG operation.  Provenance work per elimination is therefore constant-size,
and repeated coefficient-map copying/merging is removed.  Transactional
rollback also prevents dependent columns and unsuccessful candidate proofs
from accumulating.  Sparse-vector arithmetic and quotient multiplication
remain unchanged and may still dominate.

## Lightweight audit

The single authorized combined selftest passed:

```text
D972_B345_RELFRAT3_V2_PRODUCER_SELFTEST_PASS relevant_formula_sha256=5b66299d255964ff8afa9e9d75e9a5d61d767fd76539fd3c6ae94acd65039127 normalized_inverse_cache_hit_canaries=1 provenance_DAG_canaries=1 soft_timeout_consulted=false
D972_B345_RELFRAT3_V2_CHECKER_SELFTEST_PASS mutations=11 fox_orientation_canaries=2 provenance_DAG_canaries=6
```

The independent DAG mutations cover leaf orientation, coefficient drift,
wrong relator leaf, forward reference, unreachable node, and root mutation.
No local GAP, production Python, Git, GHA, or heavy computation was run.

## Final files and SHA-256

```text
search/d972_b345_relfrat3_v2.py
  89627 bytes
  fad364043926dbdc03e56accf089f454d625e0b315c98a7647bc891677313cc8

search/check_d972_b345_relfrat3_v2.py
  67150 bytes
  3c8967bea6946b42cef08cd097eab4e9071aae203ee27ac38038c4d5adb83f07

search/d972_b345_relfrat3_gha_driver_v2.g
  7568 bytes
  006e33e97c6f9ac1982887206c904dbcf423c95790ec2fe0c45d9a1b3a2e38aa
```

## Remaining work

v2 is still the direct PB3/PB4 relative-Frattini positive semidecision.  It
does not add the PB5 fallback, does not turn a bounded miss into an
obstruction, and does not prove uniform iteration or final B4-B.  The
separately designed PB5 continuation remains the next task after an honest
direct-lane UNKNOWN.

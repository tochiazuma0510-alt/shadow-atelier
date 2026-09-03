# Luna reply Task625: staged-adjoint selected-SLP release v2

## Verdict

`READY_FOR_SOL_MAX_STATIC_AUDIT`

The versioned Task625 quartet is implemented.  The sole production-semantic
change from the Task622-accepted v1 quartet is the repaired v475 topological
accumulation of the same authenticated selected-SLP DAG.  No constructor edge,
coefficient, exact free word, selected root, physical route, compact leaf
protocol, Task595 equation, or false-claim gate was removed or weakened.

The originally assigned v473 theorem was read and authenticated at 7,785 bytes,
191 lines, SHA-256
`c402a8db82cc3cf36a5572b6b21cad824dd6efa2e698f9492999164e1d9177eb`.
Following Task628's `PASS_AFTER_REPAIR`, the final executable and workflow pin
the repaired v475 theorem instead:
`sol/proof_r07_selected_slp_staged_adjoint_repair_v475.md`, 8,253 bytes,
192 lines, SHA-256
`757ffab5aa011643efa3df4b133dc03d423895d57a003ed6830a47528388148e`.

## Copied invariants and changed semantics

The producer and checker retain the accepted Task622 boundaries:

- the exact Task554 source run/attempt `33677346616/1` and Task595 candidate
  run/attempt `33707397894/1`, candidate commit
  `93f746ad1b649796e1bc28e00ff34993498929ee`;
- all 8,059 lower-first offers, the 2,014 old/lower and 6,398 grade offer
  counts, ranks 1,661/5,044, all 3,317 MEMBER coefficients, and the zero
  remainder/Task595 reconstruction equation;
- packed zero-copy physical node, edge, and row receipts, including every
  all-zero old-lower offer, the declared-lower-only preliminary replay, and
  the complete later independent 8,059-object reroute with terminal cursor
  exhaustion;
- the canonical selected source/defect/expression graph, ordered signed
  reductions, actor origins, exact typed roots, closure bitsets, compact
  `literal-leaves.bin` protocol, and byte-for-byte leaf comparison; and
- `direct_occurrence_replay=false`, `next_degree2_residual=null`, and all
  `cross_checked`/`verified`/A0/COMMON/FAKE/IHARA gates false.

The old `pending.popitem()` pathwise evaluator is absent from both v2 files.
The producer now visits the fixed v475 order: selected physical grade pivots
descending, selected physical lower pivots descending, each source block
character descending, all defects, each lifted-old character descending, then
leaves.  A sparse exact `path_id -> F3 coefficient` map is retained per node;
all incoming terms meet before expansion, zero sums are deleted, and the node
map is released immediately after its single visit.  Intern IDs are only
transient compression: tuple equality is authoritative and exact freely
reduced signed tuples are serialized.

Every edge is checked before coefficient expansion.  Missing nodes,
forward/same-stage destinations, processed destinations/cycles, non-earlier
reduction pivots, and non-earlier actor parents are hard failures.  The
producer writes into a process-specific staging directory and atomically
publishes only a complete payload.  Resource exhaustion removes that staging
directory and returns bounded `UNKNOWN_RESOURCE`; it never promotes partial
leaves to the requested output path.

## v475 statistics and independent checker

The manifest schema/marker are new v2 values and bind v475, all explicit caps,
and the complete `d972.r07.a0.staged-adjoint-statistics.v2` receipt.  Each
stage reports processed/nonzero nodes, accumulated and expanded states,
incoming contributions, cancellations, exact interned-path count, maximum
live entries, maximum path length, leaf count, elapsed time, RSS, peak RSS,
durable bytes, and `state_edge_traversals`.

The last field is exactly v475's repaired
`E_reached`: for every processed nonzero `(node, exact path)` state the
implementation increments once for every outgoing constructor edge.  The same
constructor edge is therefore counted again for a second exact path; it is not
a distinct-edge count.  `expanded_states` is the corresponding
`sum_v |supp(A_v)|` count.  The exact-word fixture sends two different paths
through one common node and checks four state-edge traversals (two incoming
edges plus the common outgoing edge traversed once for each path).

The checker does not import the producer, scheduler, or word interner.  It uses
exact tuples directly, independently reconstructs the full staged partial
order and coefficient map, validates the producer's telemetry/caps, requires
equality of every deterministic per-stage/total statistic, and byte-compares
the independently encoded leaf stream.  Wall/RSS/peak/durable observations are
authenticated and cap-checked but excluded from producer/checker equality, as
the two serial processes necessarily observe different resources.

## Explicit bounds

The workflow and manifest use:

| resource | cap |
|---|---:|
| virtual memory | 8,589,934,592 bytes (8 GiB) |
| RSS | 7,516,192,768 bytes (7 GiB) |
| durable payload | 7,516,192,768 bytes (7 GiB) |
| producer/checker internal wall | 2,400 seconds each |
| external command timeout | 45 minutes each |
| workflow timeout | 60 minutes |
| accumulated state insertions | 2,000,000 |
| interned exact paths | 2,000,000 |
| exact path length | 4,096 letters |

These bounds are not a claim that the real result fits.  Any exhausted bound
is `UNKNOWN_RESOURCE`, never NONMEMBER or an empty certificate.

## Bounded serial fixtures

Bytecode cache was directed outside the repository.  No real route was run.

```text
python -m py_compile search/d972_r07_a0_grade1_selected_slp_v2.py search/check_d972_r07_a0_grade1_selected_slp_v2.py
=> exit 0

python search/d972_r07_a0_grade1_selected_slp_v2.py --selftest
=> PASS; staged fixtures=9, positive expanded states=13,
   positive state-edge traversals=13, maximum live entries=3,
   resource-cap rejections=5

python search/check_d972_r07_a0_grade1_selected_slp_v2.py --selftest
=> PASS; the same independent staged counts, scheduler-statistics projection
   PASS, all retained compact-leaf/cursor/claim-gate fixtures PASS
```

Each scheduler's real production function covers the required diamond
cancellation, later third contribution, actor-boundary free cancellation,
coefficient two, distinct exact words with equal toy endpoint, invalid
reduction order, invalid actor parent, processed-destination/cycle, and
state/path/time resource exhaustion.  Path-length and durable-cap exhaustion
are also rejected.  Static YAML parsing and the final exact-pin contract pass.

## Final files

| file | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a0_grade1_selected_slp_v2.py` | 71,954 | 2,025 | `c3b7d53accb8b0814049cae4e1cadebc905941031b156dd12763ac2072219cf0` |
| `search/check_d972_r07_a0_grade1_selected_slp_v2.py` | 101,254 | 2,832 | `33dd8cf7fdc94c971e58a09211e5acbf749980dfc49109f3bf51db4495d46002` |
| `.github/workflows/d972-r07-a0-grade1-selected-slp-v2.yml` | final bytes/lines/SHA-256 returned out of band after reply pinning |
| `sol/luna_reply_625_r07_task601_staged_adjoint_release_v2.md` | final bytes/lines/SHA-256 returned out of band after close |

The workflow pins this reply, so embedding the reply's own final digest would
change both reply and workflow.  Their exact final values are returned
together in the completion handoff.  The frozen v1 producer/checker/workflow
remain respectively 47,935/71,637/5,497 bytes with the Task625-specified
SHA-256 values.

## Remaining risk and actions not run

The resource improvement is theorem-backed but result-dependent.  The real
numbers of accumulated exact states, interned paths, state-edge traversals,
leaves, elapsed time, and peak memory remain unknown until an authorized
immutable production run.  A new cap terminal would require another audit and
would not settle membership.

No production payload, cross-check numerator, A0 result, COMMON result,
cofinal lift, fake witness, Ihara counterexample, or Lean verification was
produced.  Production, GHA, and all git operations were **not run**.

`R07_GRADE1_SELECTED_SLP_STAGED_V2_NOT_RUN`

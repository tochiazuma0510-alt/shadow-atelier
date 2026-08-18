# Luna 157dn — relative-Frattini-3 sparse provenance DAG v2

Role: Luna implementation/performance successor.  The frozen v1 full run is
already executing on GHA; do not edit v1 files, do not run GAP/GHA/git, and do
not perform a local production computation.

Create only versioned v2 files:

1. `search/d972_b345_relfrat3_v2.py`
2. `search/check_d972_b345_relfrat3_v2.py`
3. `search/d972_b345_relfrat3_gha_driver_v2.g`
4. `sol/luna_reply_157dn_relfrat3_sparse_dag_v2.md`

Use the final v1 SHAs as pinned semantic reference.  Preserve exactly the
same q3 artifact, candidate universe/order, normalized exponent-7 × 27 inverse
construction, literal equations, Fox convention, translation BFS order,
geometric checkpoints, positive predicate, and three honest terminals.

## Objective

Remove the main deep-search memory/time duplication: v1 stores an expanded
`dict[(relator,translation)->coefficient]` in every Gaussian pivot row.  Replace
that representation by a shared immutable provenance DAG/SLP.

- A leaf is one exact translated PB4 relator column, identified by relator
  index and exact quotient translation element/section.
- A combination node records the exact F3 linear operation on previously
  defined nodes.  No cyclic or forward references.
- A pivot stores its sparse vector plus one DAG node id, not an expanded
  coefficient dictionary.
- Candidate elimination returns one proof-node id per residual.
- On PASS, retain only the union of DAG nodes reachable from the selected
  residual roots, renumber topologically, and serialize it losslessly.
- The independent checker reconstructs every leaf from the presentation and
  quotient, evaluates every DAG node independently, and requires each root to
  equal the independently rebuilt target gradient.  Producer booleans are not
  evidence.

Do not flatten the DAG back into a huge ledger.  Add orientation/coefficient,
wrong leaf, forward reference, unreachable-node, and root mutation canaries.
Keep exact quotient section replay for every referenced translation.

Resource accounting must count live sparse vector entries, pivot count, and
DAG nodes/edges separately.  A cap hit remains UNKNOWN_RESOURCE.  Add a
producer wall-clock soft cap safely below the 330-minute job limit (default
300 minutes) that serializes UNKNOWN_RESOURCE before external timeout; bind it
to the receipt and checker.  It must not be consulted in selftest.

The v2 checker must reject every nonpositive result as an obstruction; only a
PASS certificate is mathematical progress.  A bounded miss remains UNKNOWN.

One lightweight selftest is authorized.  Report source-only expected runtime
improvement, exact hashes, and GO/STOP.  PB5 fallback is not part of this v2;
state the remaining task explicitly rather than claiming the full 157dl task.

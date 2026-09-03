# Luna Task615: final release repair for Task601 selected SLP

Role: Luna implementation.  Apply only the local repairs required by the
Task614 `PASS_AFTER_REPAIR` verdict to the existing Task601 quartet:

1. `search/d972_r07_a0_grade1_selected_slp_v1.py`;
2. `search/check_d972_r07_a0_grade1_selected_slp_v1.py`;
3. `.github/workflows/d972-r07-a0-grade1-selected-slp-v1.yml`;
4. `sol/luna_reply_601_r07_grade1_selected_slp_v1.md`.

Do not change the frozen v3 source, mathematics, physical route, MEMBER
equation, input artifacts or workflow scope.  Do not run production, GHA or
git, and do not introduce a new framework.

## 1. Least canonical source closure

Construct the canonical source graph only from the selected physical refs.
Delete the second augmentation from quotient-specific derived `states`.
An old node contains only its literal projected-seed or actor-parent origin,
ordered old reductions and scale.  It must not add a `seed_reduction`, a
four-entry `actor_transition_row`, or an expression link.

Only a reached block defect contributes a non-DAG expression: the exact
`seed_reductions[seed-1]`, or the single exact
`actor_transitions[pivot][ACTORS.index(letter)]`.  Its old children are the
ones dictated by that expression.  Remove the block-owner
`origin_reductions[oi]` insertion receipt from canonical source syntax; it is
not a source child.  Mirror this least-closure definition independently in
the checker.

## 2. Root receipt and claim boundary

The checker must require `manifest["roots"]` to be exactly the filename in
the authenticated `files["roots"]` receipt.  Parse and canonical-check those
same loaded bytes, use them for the semantic root checks, and put that exact
receipt SHA in the verdict.

In both the manifest and roots object require, with no missing-field default:

```text
direct_occurrence_replay = false
next_degree2_residual = null
cross_checked = verified = A0 = COMMON = FAKE = IHARA = false
```

## 3. Authenticate before execution

Check frozen v3's exact SHA before every `exec_module`, including producer
module initialization and checker selected-source replay.  In the workflow
preflight, actually compare v3 with the already declared
`V3_PRODUCER_SHA256` before invoking either Task601 script.

## 4. Bounded fixtures and receipts

Through the same production comparison/gate cores, reject bounded mutations
for: deletion of a dependency despite scalar cancellation; deletion or
mutation of seed and transition expressions; omission of the acted old root;
per-root duplication of a source node; roots pointer/receipt aliasing; and
each false/null claim field.  State the limited mutation counts honestly.

Run only serial `py_compile`, producer/checker selftests and YAML parsing,
with cache outside the repository.  Correct all byte counts, refresh the
producer/checker/reply SHA pins in the workflow and receipt, and report the
final exact hashes.  Readiness remains false until a GHA producer plus
checker run succeeds.

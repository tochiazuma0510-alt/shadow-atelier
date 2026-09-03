# Luna Task608: unique canonical source-SLP structure repair

Role: Luna implementation. Repair only the four unlaunched Task601 outputs:

1. `search/d972_r07_a0_grade1_selected_slp_v1.py`
2. `search/check_d972_r07_a0_grade1_selected_slp_v1.py`
3. `.github/workflows/d972-r07-a0-grade1-selected-slp-v1.yml`
4. `sol/luna_reply_601_r07_grade1_selected_slp_v1.md`

Do not modify v3, proofs, v220, Task595/599/604 or any other file. Do not
commit, push, dispatch or run production.

## Load-bearing repair

The current `structure` is not yet the v465-v466 canonical SLP:

- it serializes one full source closure per root, which can duplicate the
  same nodes \(O(\#roots\cdot(V+E))\), rather than one \(O(V+E)\) graph; and
- its block-defect-to-old dependencies are supplied only indirectly by the
  quotient-specific `derived` traversal. That traversal deliberately
  coalesces mod-three weights, so a cancellation can omit an edge which must
  remain in the noncommutative source witness.

Replace this by one unique graph whose construction never consults
`pending`, `states`, `root_emissions` or `literal_leaves`:

1. Start from every physical source origin selected by the exact grade/lower
   reverse bitsets.
2. Keep one unique `block:(character,pivot)` node for every reached block
   pivot. Follow every stored reduction and actor-parent edge.
3. At every block defect, keep the exact `defect_origin`. If it is a seed,
   retain the exact referenced `seed_reductions[seed-1]` expression and visit
   every referenced old pivot. If it is a transition, retain the exact one
   `actor_transitions[pivot][ACTORS.index(letter)]` expression, visit the
   acted old pivot, and visit every old pivot in that expression.
4. Keep one unique `old:(character,pivot)` node for each such root and every
   reached old reduction or actor-parent. Preserve all node scales, origins,
   ordered edges, signs and original ids.
5. Include an authenticated literal dictionary containing the exact 44
   pinned relator words, the four exact pure-\(Q_1\) actor words in registered
   order, and literal actor words for \((x,x^{-1},y,y^{-1})\). Bind it to the
   already pinned input receipt; no fabricated word or index-derived
   placeholder is allowed.

Store each canonical node/defect/expression once, with deterministic key
order. `GradeNodeRef` plus the physical node/edge tables may remain the
compact syntax for \(W_j\), provided the schema explicitly fixes origin
first, ordered signed reductions second, and the outer scale power last.
The exact 3317 root order, prior root and `Compose(C_<1,C_T)` stay unchanged.

The coalesced `derived` traversal may remain as a separately typed
quotient-specific evaluation receipt. It must not supply, repair or prune
the canonical graph.

## Independent checker and fixtures

The checker must independently recompute the expected unique graph from the
selected physical origins and sealed prepare/four-block state, including all
cross-type defect-to-old edges. Require exact equality of unique key sets,
records, expressions, literal dictionary and deterministic order. Do not use
the derived states or their flow conservation to establish canonical
reachability.

Add bounded honest fixtures which reject:

1. deletion of a dependency whose two current scalar paths cancel;
2. deletion/mutation of a seed or transition defect's old expression;
3. omission of its acted old root; and
4. serialization which duplicates the same source node once per root rather
   than once globally.

Retain all existing exact route/MEMBER, byte-adapter, receipt, resource and
false-claim gates. Rerun `py_compile` plus producer/checker selftests, refresh
all exact workflow/reply SHA pins, and report exact byte counts and hashes.
Readiness remains honest until a full GHA producer plus checker run succeeds.

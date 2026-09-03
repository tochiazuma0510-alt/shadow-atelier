# Luna Task 601 — selected physical/source SLP extraction after grade-one MEMBER

Role: Luna implementation.  Start only after Task599 files are complete.
Implement the constructive positive branch proved in v465--v466.  Add only:

1. `search/d972_r07_a0_grade1_selected_slp_v1.py`
2. `search/check_d972_r07_a0_grade1_selected_slp_v1.py`
3. `.github/workflows/d972-r07-a0-grade1-selected-slp-v1.yml`
4. `sol/luna_reply_601_r07_grade1_selected_slp_v1.md`

Do not modify Task595/599, v3/v4, proofs, v220 or other workflows.  Do not
commit, push, dispatch or run production; root is the sole broker.  Heavy
execution belongs on GHA under the researcher's standing authorization.

## 1. Inputs and exact scope

Read v465 and v466 in full.  Consume the exact Task595 MEMBER artifact from
run `33707397894` and the exact sealed prepare/four blocks from run
`33677346616`.  Pin the frozen v3 producer SHA
`bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff`.
This is a constructive producer, so it may import v3's authenticated state,
physical aggregation and packed reducer.  It must reproduce basis SHA
`b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d`,
ranks `1661/5044`, cursor `8059`, and the exact 3317 MEMBER coefficients
before exporting anything.

This version constructs and authenticates the selected SLP syntax.  It does
not flatten literal terms and does not yet perform the full eleven-occurrence
word replay or degree-two evaluation; those remain a separate consumer.

## 2. Compact physical transcript

Reroute once in the frozen order.  For every accepted lower or grade pivot,
retain exactly v466 (1.2): logical origin, normalization scale, and the
ordered earlier-pivot/coefficient reductions.  For an old connection also
retain its ordered lower reductions.  Remove v3's duplicate lower insertion
by accepting the already reduced remainder with the exact acceptance tail.

Do not retain reduction pairs as nested Python dictionaries/lists after each
row.  Append them immediately to compact little-endian arrays or streams:
uint16 pivot id plus one coefficient byte, with uint64 pair offsets in the
small node tables.  Ranks are below 65536.  Keep the packed owners and lower
grade companions, but construct no full roster JSON, dual, flat term map,
transition-presentation copy or degree-two rows.  Enforce the v462 durable
byte ceiling and fail as UNKNOWN_RESOURCE rather than sealing a partial
result.

## 3. Reverse selected closure

Initialize the grade bitset from the 3317 nonzero target roots.  Sweep grade
pivots downward; for each marked node retain its exact ordered edges, mark all
referenced earlier grade pivots, and mark every lower pivot referenced by an
old-connection origin.  Sweep marked lower pivots downward analogously.
Require closure: every emitted edge target is present and has smaller original
pivot id.  Record original ids; do not renumber in a way that loses parent
identity.

Follow selected physical origins into the sealed block/old DAGs.  Retain all
reached reduction and actor-parent nodes, each reached `defect_origin`, and
the particular reached `seed_reductions` or `actor_transitions` expression.
Terminate at exact compact-seed and literal-actor leaves.  Preserve all
registered child orders, signs and normalization scales.  Do not cancel or
sort group factors even if associated-grade coefficients cancel.

## 4. Canonical SLP roots and output

The payload must define typed nodes for exact leaves, ordered product,
inverse/power by 1 or -1, literal actor conjugation, registered composition,
and authenticated references into the selected compact edge streams.
Define:

- update root `C_T` in the exact recorded order of the 3317 MEMBER
  coefficients;
- prior root `C_<1` as the exact ordered product represented by the sealed
  `canonical_solution["terms"]` list, without recanonicalizing it; and
- complete root `C_1 = Compose(C_<1,C_T)` in the registered
  `canonical_solution + update` order.

Emit a small canonical manifest, selected node tables/bitsets and compact edge
streams, each with size/SHA receipt.  Bind all files to the Task595 decision
digest and the prepare/four-block digests.  The checker independently parses
the encoding, checks acyclicity/type/order/closure, replays the compact linear
ancestry against the routed packed rows and exact MEMBER equation, and checks
the three roots.  It must not import the producer's serializer/parser.

Use markers `R07_GRADE1_SELECTED_SLP_V1_CANDIDATE` and
`R07_GRADE1_SELECTED_SLP_V1_CHECKER_PASS`.  Keep
`direct_occurrence_replay:false`, `next_degree2_residual:null`,
`cross_checked:false`, `verified:false`, and every A0/COMMON/fake/Ihara flag
false.

## 5. Workflow and bounded tests

Add only tiny coefficient-two, nonmonotone lead and reverse-closure fixtures.
The workflow follows the same exact-source downloads and limits as Task595,
triggering only on workflow_dispatch or a working-branch push whose commit
message contains `[fire-grade1-selected-slp-v1]`.  Use exact-SHA checkout,
Python 3.13, NumPy 2.5.1, commit-pinned actions, 7-GiB internal RSS, 8-GiB
virtual memory, 40-minute internal / 45-minute outer / 60-minute job caps.
Upload selected payload plus checker verdict only on success and logs under
always().  Report exact hashes, commands, artifact names and honest readiness.

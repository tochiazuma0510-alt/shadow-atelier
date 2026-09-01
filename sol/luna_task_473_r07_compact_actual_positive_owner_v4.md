# Luna Task473 — compact actual positive owner v4 ABI repair

## Scope

Repair only the three deterministic ABI blockers in
`sol/sol_reply_464_audit_r07_compact_actual_positive_owner_v3.md`.  Preserve
the actual Task456 arithmetic, independent Task411 44-row reconstruction,
read-only DirectEngine row view, four actions, target/PB/proof-DAG/literal-M
path, positive-only nonresumable contract, and all resource/input frontiers.
Do not add a checkpoint or negative claim.

Required exact repairs:

1. Producer, checker and driver must use the same actual inherited MEMBER
   literal `R07_ZERO_BASE_A5_A6_MEMBER`.
2. The checker must pin the actual v4 producer path together with its exact
   bytes/SHA; transform the complete tuple, not only numbers.
3. Scope schema transforms by full line: advance only the compact checker's
   own `CHECK_SCHEMA`, while producer and checker both require the frozen
   Task193 ABI
   `d972-r07-second-frattini-affine-prefix-compiler/v5/checker-verdict/v5`.

Add executed static/load gates proving all three equalities, in addition to
the existing 44-row/digest, actual-engine, read-only proxy, and NONE-frontier
gates.  No production, GHA, workflow edit, git, full authority run, or
bytecode cache.

## Exact outputs

1. `search/d972_r07_compact_direct_relator_a5_a6_positive_v4.py`
2. `crosscheck/check_d972_r07_compact_direct_relator_a5_a6_positive_v4.py`
3. `search/d972_r07_compact_direct_relator_a5_a6_positive_gha_driver_v4.g`
4. `sol/luna_reply_473_r07_compact_actual_positive_owner_v4.md`

Do not edit v3.  End with
`TASK473_R07_COMPACT_ACTUAL_POSITIVE_OWNER_V4_PASS` or a typed STOP.

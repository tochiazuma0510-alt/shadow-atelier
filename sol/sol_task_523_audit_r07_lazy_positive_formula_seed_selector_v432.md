# Sol task 523 -- adversarial audit of lazy positive formula-seed theorem v432

Role: independent Sol(max) mathematical/implementation-contract auditor.  Do
not edit implementation, run long production, dispatch GHA, mutate git, or
promote any claim.  Reply only to
`sol/sol_reply_523_audit_r07_lazy_positive_formula_seed_selector_v432.md`.

Audit paper
`sol/proof_r07_lazy_positive_formula_seed_selector_v432.md`, 8204 bytes /
SHA-256
`965ab4f48fbc98cabd4905a7ad0a8fcb10dbe06415bb09771e22c31e74a7d3e5`.
The live owner is
`search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py`, 12215 bytes /
`0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37`,
with its pinned v2 owner.  The authenticated rank111 artifact is outside the
repo at
`C:/Users/81905/AppData/Local/Temp/shadow-atelier-task517-rank98-9826862037/`
and its result/checkpoint identities are fixed in v220 Delta367 and Task517.

## Required audit

1. Re-derive the linear-algebra implication
   `lambda(V)=0`, `lambda(row)!=0` => `row notin V` and identify every exact
   direct check needed to make a selected literal row sound.
2. Trace `compile_formulas`, `weighted_hit`, `insert`, checkpoint replay and
   checker v7.  Decide whether formulae/coordinate unions/identity replays for
   unvisited later seeds are genuinely unnecessary for a positive row, or
   whether any hidden shared-state/global premise makes v432 false.
3. Adversarially test the claims about skipping unsupported/zero/no-hit seeds,
   deferred identity replay, K=0 support fibres, v431 K-nonzero branch, action-
   first order, and UNKNOWN-only failure.  In particular distinguish a sound
   positive-search widening from equivalence to the old eager search.
4. Independently parse artifact `9826862037` and confirm or reject: 68 accepted
   correction rows, all seed index 1; rank111/round73; last thirteen seed1;
   last-thirteen `checked_fibres` range 1..1108; terminal inside
   `tau_free_formula_seed`; and false A0/COMMON/NONMEMBER/fake/Ihara claims.
5. Count the actual presentation seeds reached by the owner and determine the
   exact eager work avoided by a seed-1 hit.  Do not state an unmeasured wall-
   clock speedup.  Identify a bounded implementation contract and mutation
   tests sufficient for a Luna successor.

Return `GO_FOR_LAZY_SUCCESSOR_IMPLEMENTATION`,
`GO_WITH_REQUIRED_PAPER_REPAIR`, or `STOP_THEOREM_FALSE`, with exact findings,
paper reply bytes/SHA-256, and no claim promotion.

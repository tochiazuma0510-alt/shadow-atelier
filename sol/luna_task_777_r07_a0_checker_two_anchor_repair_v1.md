# Luna task 777 — A0 checker two-anchor repair v1

Role: Luna.  Read the complete Task772 audit before editing.  Its producer,
v500 mathematics, full eleven-slot bucket schedule and workflow performance
audit all passed.  Repair only the two finite checker selftest blockers.

## 1. Versioned outputs

Create only:

- `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v6.py`
- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v14.yml`
- `sol/luna_reply_777_r07_a0_checker_two_anchor_repair_v1.md`

Producer v8 and proof v500 are frozen and unchanged.  Workflow v14 must invoke
producer v8 and checker v6 and use fire token
`[fire-fresh-precision2-endpoint-v14]`.

## 2. Exact two repairs

1. In checker selftest only, independently evaluate a noncommuting two-letter
   word in bounded tiny E3 and E4 models.  Compare that direct value with the
   result of `signature_extend_gate` on the same two independently obtained
   atoms.  The source mutant replacing `multiply(index,left,right)` by
   `multiply(index,right,left)` must make the complete selftest fail.  Do not
   restore any production all-prefix direct replay.
2. Add a literal pentagon-order anchor independent of
   `pentagon_factor_word`.  With distinct non-involutive singleton factors,
   require the fixed paper order `1,3,0,-2,-4`; the corresponding literal
   expected word is `[-5,-3,1,4,2]`.  Mutating the first positive factor from
   `factors[1]` to `inverse(factors[1])` must make the complete selftest fail.

The anchors must exercise the installed production helpers, not copied toy
helpers or constants disconnected from their call graph.  Keep their work
strictly bounded.

## 3. Non-regression and evidence

- Production AST/call graph, direct schedule `G`, exact-key authentication,
  signatures, bucket coefficients/representatives, precision-two arithmetic,
  target, lower gate, rho2 path and claim flags must remain unchanged from
  checker v5.
- Re-run producer-v8 and checker-v6 selftests plus both exact source-mutant
  tests.  Both mutants must fail; report where.
- Update workflow pins/names/checker marker consistently.  Retain immutable
  parents, serial caps, success-only residual and always logs.
- No real parents, production A0, GHA, git, network or delegation.  Do not add
  infrastructure, dense closure, heavy SELFTEST or unrelated cleanup.

Report exact byte identities and end with `READY_FOR_SOL_AUDIT=yes` only if
the two mutations are killed and production arithmetic is unchanged.

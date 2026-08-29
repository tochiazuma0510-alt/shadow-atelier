# Luna task 360 - actual zero-base A5/A6 v2

## Role and scope

This is a bounded Luna implementation task.  Do not change any existing
file.  Create only:

1. `search/d972_r07_zero_base_a5_a6_compiler_v2.py`
2. `crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v2.py`
3. `search/d972_r07_zero_base_a5_a6_compiler_gha_driver_v2.g`
4. `sol/luna_reply_360_r07_zero_base_actual_a5_a6_v2.md`

Do not run Python, GAP, GHA, git, SELFTEST, fixtures, mutations or searches.
An AST parse is not requested.  This task is production-only.

Read these exact mathematical/ABI owners before implementation:

- `sol/proof_r07_zero_base_boolean_free_a5_a6_specialization_v345.md`
- `sol/proof_r07_zero_base_streaming_joint_a5_certificate_v348.md`
- `sol/luna_reply_355_r07_zero_base_a5_actual_abi_preflight.md`
- `search/d972_r07_word_independent_successor_kernel_v11.py` and its frozen
  v6 body
- `crosscheck/check_d972_r07_word_independent_successor_kernel_v12.py` and
  its frozen v6 body
- the accepted task198 receipt/manifest/attestations in `ci/in/`
- the new A0-to-task193 adapter v2 if present; otherwise bind its dedicated
  schema symbolically and report that sole missing physical owner.

The rejected v1 compiler is a control only.  Do not copy its fictional
`task198.evaluator.zero_base`, `K_roster[*].seed`, `marked_actions`, or flat
`beta1_vector/eta_c` fields.

## Required actual construction

Authenticate the five physical owner pairs: A3 zero, task198, accepted A4,
accepted A0, and the dedicated A0-bound task193-adapter-v2 result.  Require
the exact positive terminals and checker verdicts, common run/artifact/source
identity, canonical bytes and self seals.  A missing positive owner is typed
`UNKNOWN_INPUT`; it is never a mathematical negative.

Read the actual A3 fields from `result.gate.target`, `lambda`, and `kappa`
(with the exact accepted receipt shape), and require all three canonical
zero vectors.  Missing fields are not zero.

Use the actual A4 `kernel.K_roster` word/rho/replay owners and
`kernel.action_matrices`.  Independently replay every selected literal word,
`rho0/rho1`, upper-shadow identity, and action edge.  Do not require or derive
the obsolete A4 anchor/adapted basis/local A3 pairs.

Use task198's real occurrence ledger, ten-to-eleven map, seven blocks,
context maps, joint-coordinate image and runtime constructor.  Construct the
typed module actions from the accepted affine evaluator.  For each A4 word
`u_i`, form literally

```
((rho1(u_i)-1) d1, (rho1(u_i)-1) odot w)
```

by affine multiplication in every typed context, not by invented sparse
renaming maps.  The task193 adapter supplies the typed `d1`, `beta1`,
`e1=-beta1`, and literal A0 word binding.  Reconstruct the eleven-occurrence
coordinate through the task198 ledger and apply the printed block map only
after the full pre-C rank decision.

Stream v348 exactly: `E_pre` controls rank admission and the action queue;
each accepted row is then inserted into `E_joint` as `(z,C eta)`.  Test target
`(e1,0)` after each joint insertion.  An early MEMBER is sound and may stop.
Retain only independent rows plus ancestry needed by the certificate; do not
store every dependent row.

The echelon reduction transform has the opposite sign from the solution
coefficients.  Negate it before emitting `theta` or A6 ancestry and replay
both equations explicitly.  MEMBER must output the finite equality

```
e1 = theta*d1
C(theta odot w) = 0
```

and collected A6 records
`(coefficient,prefix_DAG_node,original_A4_kernel_word_index)` with literal
prefix/action replay.

Do not implement A7 or exact PB endpoints in this task.  Report A7 as
`NOT_BOUND`, never as success or failure.

For NONMEMBER, first exhaust `E_pre`, then construct a genuine full joint
annihilator (including both z and C-eta coordinates), prove it kills every
joint basis row and pairs nontrivially with `(e1,0)`, and return a proper
`(terminal,result)` pair.  Resource exhaustion is `UNKNOWN_RESOURCE`.

## Independent checker

The checker must not import producer helpers.  It independently authenticates
the actual owners and reconstructs only what the terminal needs:

- MEMBER: selected A4 words, used prefix/action edges, both finite coordinate
  equalities, coefficient sign, and the collected A6 ancestry.
- NONMEMBER: complete queue exhaustion, the complete joint span, and the
  annihilating dual.
- UNKNOWN: no positive claims.

It must compare the complete result body, ranks, manifest digest and common
identity, not only the terminal string.

## Driver

ASCII only.  Pin exact producer/checker bytes and SHA after final edits.
Use fixed allowlisted paths, exactly one producer and checker call, no retry,
no local parallelism, no SELFTEST.  Require producer/checker terminal and
status agreement and create `.ok` only after both accepted; otherwise fail
closed.  Emit progress at most once per 60 seconds during an actual closure.

## Reply

List exact file sizes/SHA-256, implemented terminals, actual ABI owners used,
and any single genuinely missing physical input.  Do not claim execution,
cross-check, A7, lift, fake or Ihara.

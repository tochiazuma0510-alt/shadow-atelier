# Luna task 312 - task307/v7 fixture repair v8

Role: Luna implementation repair only.  Do not make mathematical rulings.
Do not run Python, Node, GAP, GHA, network, or git; parent Sol is the execution
and git broker.

## 1. Read and fixed defect

Read in full:

- `sol/audit_r07_task307_v7_gha_fixture_failure_v257.md`;
- `sol/sol_reply_309_r07_task307_v7_solmax_code_audit_v1.md`;
- all five accepted task307/v7 implementation paths.

GHA run 33167156710 at head
`66e63e7f3cf398ae826599715e35eb5f515a442a` reached the producer and stopped
at `RuntimeError: action owner`.  In the first fixture case only,
`A_E_binding` rows 6 and 7 have ten entries while the corresponding `A_E`
rows have eleven.  Preserve the fail-closed owner gate and repair the literal
fixture.

## 2. Exact authorized paths

Create exactly these five new paths and modify no existing path:

1. `search/d972_r07_joint_slice_kernel_general_v8.py`
2. `crosscheck/check_d972_r07_joint_slice_kernel_general_v8.py`
3. `search/d972_r07_joint_slice_kernel_general_gha_driver_v8.g`
4. `search/certs/d972_r07_joint_slice_kernel_general_selftest_v8_20260828.json`
5. `sol/luna_reply_312_r07_task307_fixture_repair_v8.md`

The driver must remain ASCII-only.

## 3. Required repair and preservation

- Make the two malformed `A_E_binding` rows byte-for-value equal to the
  corresponding eleven-entry `A_E` rows.
- Version every schema, marker, path, fixture seal, and output identity to v8;
  update all exact byte-length/SHA pins.
- Add a fail-closed all-case fixture preflight in both producer and independent
  checker.  It must directly check all `A_theta/A_theta_binding`,
  `A_Z/A_Z_binding`, `A_E/A_E_binding`, `D/D_binding`, `O/O_binding`, and
  `C/C_binding` equalities and their literal dimensions before compiling any
  case.  It must not trust `expected_cases` metadata.
- Preserve all accepted v7 semantics: five cases; plural seeds and distinct
  actions; joint rank closure; post-C left kernel; dimension/cardinality
  separation; MEMBER ancestry and NONMEMBER dual replay; 19 producer and 19
  independent fail-closed mutations; wrong-seal canaries; exact-one quoted
  driver terminals; reachable typed production STATIC_BLOCKED.
- Do not add redundant full-case recompilation, repeat fixture parsing, grow
  exhaustive enumeration beyond the intended dimension-two canary, or add
  sleeps/locks/serial subprocesses.  State the SELFTEST complexity and any
  hot path in the reply so Sol(max) can audit unnecessary slowdown.

## 4. Reply boundary

Report the five final identities, the exact repaired rows, every new preflight
gate, expected case tuples, mutation routes, and performance accounting.
Mark all execution `UNEXECUTED`; keep actual A5/A6 at 0/3 and declare no lift,
fake, or Ihara result.

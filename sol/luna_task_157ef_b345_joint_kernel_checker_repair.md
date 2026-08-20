# 157ef — 157ee checker direct-canary shape repair

## Role and authorized scope

This is a versioned checker-only repair after GHA run `32358185122`.
Only these files may be created:

1. `search/check_d972_b345_joint_kernel_qstar_closure_v2.py`
2. `search/d972_b345_joint_kernel_qstar_closure_gha_driver_v2.g`
3. `sol/luna_reply_157ef_b345_joint_kernel_checker_repair.md`

The 157ee producer, checker v1, driver v1, task, q3 sources, workflow, and all
mathematical predicates are frozen and must not be edited.  The new checker
must authenticate and reuse checker v1 rather than importing producer state.
The driver is ASCII only.

## Frozen evidence and diagnosis

- Commit: `4eeba57620229000581f69442b14c680801df405`.
- Producer SHA-256:
  `06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc`.
- Checker v1 SHA-256:
  `9e721634d1f16be806e315eec263ec272bc023587f862703c094b7dd37c0111f`.
- Driver v1 SHA-256:
  `ad536c97644ba28e511ca7cb1f58192bddfecdfce6630fd76dde108589303ad4`.
- Run `32358185122` produced exactly
  `B345_JOINT_KERNEL_QSTAR_CLOSED` and
  `D972_B345_JOINT_KERNEL_QSTAR_PRODUCER_EXIT_ZERO`.
- The independent checker freshly rebuilt the full 32,768-translation prefix
  and then crashed only in `direct_canary` with
  `KeyError: 'quotient_identity'`.

The v1 checker calls `checker_target6_formula(..., include_gradient=True)`.
That exact detail record contains `direct_value`, `direct_gradient`, and
`formula_equals_direct`.  Its public projection intentionally contains
`formula_equals_direct` but no `quotient_identity`.  The producer correctly
gates the private direct value before constructing its public canary.

## Exact repair

Create a small v2 checker that pins checker v1 byte-for-byte and replaces only
the v1 `direct_canary` function.  The repaired gate must require

```text
detail["direct_value"] == e4.identity
public["formula_equals_direct"] is true
```

before the same raw-lambda, fixed-prefix normal-form, expected-scalar, digest,
and public-row checks.  It must not invent a new public receipt field or weaken
any existing check.  All other checker code is the frozen v1 implementation.

The v2 self-test must exercise the repaired production helper with the exact
public shape lacking `quotient_identity`, and must reject a mutated nonidentity
`direct_value` and a false formula flag.  It must also run the full frozen v1
self-test.  The v2 full path prints its own exact PASS marker only after v1
validation returns successfully.

Create a v2 driver which authenticates the frozen v1 driver, producer, v1
checker, new v2 checker, and this task.  It may mechanically substitute only
the checker path and checker hash in the frozen v1 driver.  Require exact
replacement counts, exact v2 self-test/full checker markers, and an exact v2
driver marker.  The q3 child, producer, artifact schema/path, common deadline,
terminal set, and mathematical claim remain byte-for-byte v1 behavior.

Run one bounded combined self-test before freeze.  Then the parent may dispatch
the v2 self-test and full same-job run.  A CLOSED result remains scoped only to
the registered fixed prefix and `ker(Q0 x E3 x 31 E4 contexts)`; it is not full
D2, full H3, global lift nonexistence, B4-A, or B4-B.

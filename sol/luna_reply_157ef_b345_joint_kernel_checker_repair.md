# 157ef reply — 157ee checker direct-canary repair

## Outcome

The checker-only successor is frozen for GHA.  The 157ee producer and all
mathematical predicates are unchanged.

Full run `32358185122` at commit
`4eeba57620229000581f69442b14c680801df405` emitted exactly

```text
B345_JOINT_KERNEL_QSTAR_CLOSED
D972_B345_JOINT_KERNEL_QSTAR_PRODUCER_EXIT_ZERO
```

The independent checker then freshly rebuilt the 32,768-translation prefix
through 362,709 pivots and crashed in its final direct canary with
`KeyError: 'quotient_identity'`.  Artifact upload was consequently skipped.
This is not yet a cross-checked mathematical result.

The cause was an exact record-shape mismatch.  The frozen checker helper
`checker_target6_public_from_detail` intentionally does not export
`quotient_identity`; the actual quotient value remains in the private
`direct_value` returned by `checker_target6_formula`.  The producer already
uses that private value correctly.

Checker v2 authenticates checker v1 byte-for-byte and replaces only this
canary.  It requires `direct_value == e4.identity` and the existing formula
flag before performing the unchanged raw-lambda, normal-form, scalar, and
digest checks.  No public receipt field was added and no gate was weakened.

## Frozen files

- task: `sol/luna_task_157ef_b345_joint_kernel_checker_repair.md`
  - SHA-256 `e626802b32e9577e35f5543b252830abdc4461b409972c9f5536ea29d8bb14ed`
  - 3,235 bytes
- checker v2: `search/check_d972_b345_joint_kernel_qstar_closure_v2.py`
  - SHA-256 `5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88`
  - 5,942 bytes
- driver v2: `search/d972_b345_joint_kernel_qstar_closure_gha_driver_v2.g`
  - SHA-256 `8ff80ba97f3801daf28ad61b19d2f0a01572a5720c13578f11c56bf0d7ad26e7`
  - 3,912 bytes

The v2 driver pins the frozen v1 driver/checker, the v2 checker, and this task.
It mechanically replaces exactly three checker-path occurrences and one
checker-hash occurrence in the pinned v1 driver, then requires a v2 marker in
both self-test and full modes.  Producer, q3, artifact path/schema, terminal
tokens, and common deadline remain the frozen v1 route.

## Bounded self-test

One combined frozen-producer plus v2-checker self-test passed:

- frozen producer marker: PASS;
- frozen checker core marker: PASS;
- v2 repair marker:
  `public_shape_without_quotient_identity=1 mutations=2`.

The two v2 mutations reject a nonidentity private quotient value and a false
formula/direct flag.  Python AST, driver ASCII, source pins, and
`git diff --check` passed.  No full mathematics was run locally.

The parent should dispatch the v2 GHA self-test first and require the v2 driver
marker, then rerun full mode.  Only a subsequent checker PASS may promote the
observed producer CLOSED terminal to cross-checked status.

## GHA run record

The v2 GHA self-test succeeded:

- run `32359804965`;
- commit `1696e7b44792b97c51a435d4160259462963c52d`;
- producer, checker-v1 core, checker-v2 repair, driver-v1, and driver-v2
  markers each occurred exactly once.

The full same-job rerun then succeeded and is cross-checked:

- run `32359956713`;
- commit `1696e7b44792b97c51a435d4160259462963c52d`;
- artifact ID `9403505687`, name `gap-run-out`, archive size 227,958 bytes,
  archive digest
  `sha256:9fe43b570dd135c4f26c910dff983e0e58492bb3250beb4cbe01d7e8bcca1192`;
- receipt size 2,166,036 bytes, SHA-256
  `1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df`;
- terminal `B345_JOINT_KERNEL_QSTAR_CLOSED`, reason
  `joint_kernel_presentation_potential_zero`;
- producer elapsed 325.759814168 seconds, peak RSS 764,940,288 bytes;
- same-job producer elapsed ledger 326 seconds, final elapsed 713 seconds,
  final common-deadline margin 17,287 seconds.

The independent reconstruction matched the fixed prefix
(362,725 columns, 362,709 pivots, 16 dependent columns, 3,090,367 live
entries), the 362,710-entry raw-lambda oracle, and base target6 lambda 2.
It reconstructed the group of order 243 (exponent 9, center 27, derived
subgroup 3, Frattini subgroup 27, quotient 9) and obtained scalar zero for all
6,318 internal Cayley relations, all 104 `x/y` action relations, and all 19
complete `Q0` relators.  Five direct/raw-normal-form canaries also matched.

The cross-checked claim is exactly that the registered joint typing kernel
cannot change the nonzero qstar obstruction against the fixed prefix.  The
receipt explicitly makes no full-D2, full-H3, global lift-nonexistence, B4-A,
or B4-B claim.

B345_JOINT_KERNEL_QSTAR_CHECKER_V2_READY_FOR_GHA

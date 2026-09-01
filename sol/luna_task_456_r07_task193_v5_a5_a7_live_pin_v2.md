# Luna task 456: task193-v5 -> direct-relator A5/A7 live-pin successor

Role: **Luna implementation owner**.  Migrate the already accepted
zero-base/direct-relator A5--A7 executables to the Task454 task193-v5 ABI.
This is a pin and authenticated-verdict migration.  Preserve the v350--v351
mathematics and the representative-complete streaming dovetail exactly.

## 1. Frozen owners

The accepted Task454 owners are:

```text
search/d972_r07_second_frattini_affine_prefix_compiler_v5.py
  12207 / fab51e296170ac34ebe48b49d79d3460017a51cd797d524e7b0d89481f23960f
crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v5.py
  7795 / 941eab0d9c60726436c866427de04b7c25b4ae1934fbf0a1d464f2010a7e2b9e
search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v5.g
  2269 / d2cab901ae608d88bcff6dacdee6072c780b9157e1955cbaa740d227a8f2fe7a
```

Use these accepted Task393 owners as the mathematical bases:

```text
search/d972_r07_zero_base_a5_a6_compiler_v4.py
  59239 / 3949c5b98432cabebef989304cb70201266d48b7bdd71a6301a955000a9755c7
crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v4.py
  45942 / cc88aeed18c4f14481971595ab22070720f68ce3fbe48f1057ecd89b610178aa
search/d972_r07_zero_base_a5_a6_compiler_gha_driver_v4.g
  4255 / 2349f5a84afadcd90e26aad9bb98689c8df099e733951cc3cd8fd7425a2cbef0

search/d972_r07_direct_relator_a5_a7_fusion_v6.py
  57826 / da9e8ca8e5ea2c30e92eef2d1dba772a0aa4d3eed9d894c7441c40cb49ac6441
crosscheck/check_d972_r07_direct_relator_a5_a7_fusion_v6.py
  29830 / 355dbf657f9b15f61e9fd8eb62717e4a9d905f69545408ac28126b96b38361cc
search/d972_r07_direct_relator_a5_a7_fusion_gha_driver_v6.g
  6675 / ffe2d3670bcc00b90d09df7cb6229c5f2b9f0b92c6a98ba44386baa77fed1a82
```

Fail closed on every byte/hash or patch-cardinality mismatch.

## 2. Exact Task454 ABI

Both producer and checker must independently accept only the physical
Task454 pair:

```text
receipt.schema   = d972-r07-second-frattini-affine-prefix-compiler/v5
receipt.status   = PASS
receipt.terminal = R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V5

verdict.schema   = d972-r07-second-frattini-affine-prefix-compiler/v5/checker-verdict/v5
verdict.status   = PASS
verdict.terminal = R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V5
verdict.receipt  = exact physical receipt identity
verdict.claims.independent_carrier_authentication = true
verdict.claims.independent_task193_replay = true
verdict.claims.pointed_rows = true
verdict.claims.A2/lift/fake/Ihara = false
```

Retain the receipt's existing task193 claims and independently reconstruct
the same pointed rows as the frozen Task393 checkers.  Do not trust a Boolean
in place of the physical receipt/verdict binding.

## 3. Versioned successors

1. Create zero-base A5/A6 v5 from the exact v4 owner.  Change only the
   Task193 schema/terminal/checker schema, exact three Task454 pins, own
   versioned labels/checkpoint/paths, and owner key `task193_v4` to
   `task193_v5`.  Preserve all raw-relator, boundary-slack, MEMBER,
   NONMEMBER, UNKNOWN, ancestry, cap, and checker arithmetic.
2. Create direct-relator fusion v7 from exact v6.  Pin zero-base-v5 and
   Task193-v5, advance only versioned labels/paths/owner keys, and preserve
   the v351 lift-null Schreier completion and exact H1/H2/P endpoint replay.
3. Keep the accepted fail-fast order: authenticate Task193 before building
   the 6,441-row Task198 authority or boundary owner.

The dependency lock is load-bearing: a positive direct-relator MEMBER is
the v350 bypass and **does not consume an A4 result, A4 checkpoint, or A4
word-bearing basis**.  Do not add any A4 wait or input.  The 6,441 literal
Task198 relators are redundant generators of the relative ideal, not the
6,441-row A4 quotient computation.

## 4. Exact output scope

Create only:

```text
search/d972_r07_zero_base_a5_a6_compiler_v5.py
crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v5.py
search/d972_r07_zero_base_a5_a6_compiler_gha_driver_v5.g
search/d972_r07_direct_relator_a5_a7_fusion_v7.py
crosscheck/check_d972_r07_direct_relator_a5_a7_fusion_v7.py
search/d972_r07_direct_relator_a5_a7_fusion_gha_driver_v7.g
sol/luna_reply_456_r07_task193_v5_a5_a7_live_pin_v2.md
```

Do not edit any owner, workflow, v220, claim ledger, or proof paper.  Do not
run production, GHA, heavy local computation, git, or network.

## 5. Bounded acceptance

Run AST/compile/load-without-main, exact generated-pin and patch-cardinality
checks, full owner-pin closure, fresh-path/stale-token scan, ASCII GAP
parse/load guard, and an AST order check for Task193 fail-fast.  Diff the
generated mathematical bodies against v4/v6 and show that executable changes
are restricted to the ABI/pins/version text above.  Confirm no A4 input and
no eager translated Schreier roster, worker pool, retry, production SELFTEST,
or new equality oracle was added.

`TASK456_R07_TASK193_V5_A5_A7_LIVE_PIN_COMMISSIONED`

# Task473 — compact actual positive owner v4 ABI repair

Created only the four authorized v4 outputs:

```text
search/d972_r07_compact_direct_relator_a5_a6_positive_v4.py
crosscheck/check_d972_r07_compact_direct_relator_a5_a6_positive_v4.py
search/d972_r07_compact_direct_relator_a5_a6_positive_gha_driver_v4.g
sol/luna_reply_473_r07_compact_actual_positive_owner_v4.md
```

The v4 producer/checker are guarded successors of the adopted v3 bodies and
retain the actual Task456 arithmetic, Task411 independent 44-row
reconstruction, read-only DirectEngine view, four actions, target/PB/proof-DAG
and literal-M path, positive-only nonresumable contract, and all frontiers.

## Three ABI repairs

1. Producer, checker, and driver now use the same actual MEMBER literal:
   `R07_ZERO_BASE_A5_A6_MEMBER`.
2. The checker generated body now pins the complete v4 producer tuple:

   ```text
   (search/d972_r07_compact_direct_relator_a5_a6_positive_v4.py,
    1876,
    0e4f52e3af94d145121c70bf405219276984b73e14d19c3cf6b417480dfa09b9)
   ```

3. The compact checker own schema advances to
   `d972-r07-compact-direct-relator-a5-a6-positive-owner/v4/checker-verdict/v4`,
   while both sides retain the frozen Task193 ABI
   `d972-r07-second-frattini-affine-prefix-compiler/v5` and
   `.../checker-verdict/v5`.

## Exact v4 pins

```text
producer source 1876 0e4f52e3af94d145121c70bf405219276984b73e14d19c3cf6b417480dfa09b9
producer body   61376 d9a5a136d875d2fb7f5d596966abf094b7c555a0e4eb4ac6576c72071f734b84
checker source  2552 a94e8180b0280fac92fbf749591c5985092188a62aab08cda2299e2c22d23eeb
checker body    47875 c65f4e7a122f835f5c50b03d6c189ff26a319518ac8b525d6f3d0943b8412ed0
driver source   4183 080a9826d675c0c6c1f9f7f062e290f3cfba5e4793ecb58d0b21675baac45ec3
```

## Bounded gates

- PASS — compile-only Python gate, with no bytecode cache, plus driver
  ASCII/final-newline gate.
- PASS — load-without-main and exact guarded v3 physical/generated pin gates.
- PASS — all three ABI equality assertions: MEMBER literal, complete v4
  producer tuple, and frozen Task193 schema/terminal/source pins.
- PASS — actual producer/checker 44-row equality and digest
  `7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8`.
- PASS — read-only proxy gate for both modules (44 rows, delegated attribute,
  proxy-attribute and row mutation rejection).
- PASS — positive nonresumable/NONE-frontier and driver member/pin/process
  static gates.

No production, synthetic MEMBER, full authority run, GHA/workflow execution,
or git operation was performed. Blockers: none for the bounded ABI repair.

TASK473_R07_COMPACT_ACTUAL_POSITIVE_OWNER_V4_PASS

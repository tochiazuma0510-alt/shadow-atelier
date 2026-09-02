# Task 516 independent audit — final A4 production handoff

## Verdict

`GO_FOR_GHA_DISPATCH`.

All bounded load-bearing gates pass.  This authorizes only the frozen v46 dispatch envelope; it does not promote an A4 mathematical claim.

## Exact pins

| object | bytes | SHA-256 |
|---|---:|---|
| producer v25 | 27075 | `8e5c16f28113218485f7196c6873dbbf3ce17a0e03bd7daafe71bc6e8da5015f` |
| generated producer | 286439 | `e4fb7ead7e1dcfc5806574481f1e83e008991e516de20e2eb3a67753fec03098` |
| checker v35 | 10246 | `c8383a18169ec2da63e4e7a64de17f05d305c35e15393bcbb9e3c312ac6d5dd7` |
| generated checker | 312553 | `2ffcdede9a20acdd99bab3c4847db4c4a4f013e33fc151ac01b77f088d21df75` |
| predecessor driver v45 | 12430 | `d59bee6ea9a5366643d5409505ce25e91baa7c18031911eea36565e2f221782f` |
| final driver v46 | 12544 | `d3a864e47ebe0255221ccafee15b09925b2e1e462b21d8d0158c2d9c9e0f97e7` |
| Task515 reply | 958 | `9cf497052091109de6be3af829189eae7128dfcad3e69007ba34f9a728b74054` |

Every named transitive prerequisite exists and matches its internal pin:

| prerequisite | bytes | SHA-256 |
|---|---:|---|
| v24 | 34535 | `8dc698e43fa7971dff4af3a5a19a7ac309ab5d43a19bb1f5189c0c222df01dfe` |
| generated v24 | 285814 | `9e3619f2e83dc7bea2e58d250bff3fafc24b8e09910c389b7a402a3b2d0d2d6a` |
| v33 | 24033 | `44e79864424a21d836d0b61dbe066889e3567d250e722026143a2eb8f7d87ccf` |
| generated v33 | 312046 | `cb1d2b390beb3bdbd71d2175983310971d0669f6a6d7b77e1e64f29ceae61f57` |
| v34 | 5838 | `b00219523c2e5703b8c6c52c7bf24655c727ddc72c7da9fd06c746063875a9ba` |
| generated v34 | 312553 | `2ffcdede9a20acdd99bab3c4847db4c4a4f013e33fc151ac01b77f088d21df75` |
| v43 | 15449 | `36be6a635fa7399c37048ef45debb5c25d5ede8cc1414fa153a7e8bb0dd7c8bb` |
| v44 | 8960 | `7f70546b51b934edcc6d64626af4d04c18f15642a10db8b40eaea3f9fcfb96f3` |
| proof v430 | 7137 | `acea72aea1a8f62a3de1c84a7bf4cab95fc4da85162bbe226b1a5f158755a904` |

The row-26 release remains 56410 / `5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a3360e3`.  All six member pins, including canonical producer HEAD 700 / `910cc8afcca333dab56d9fefe35e63066eab764ac6325e3130c43a3c3d6f0114`, delta1 3551 / `d1f0ffdda299316ff1805f7a565ffe012fed63001bca74f0bc9e3ef2aeaf0e19`, delta2 3625 / `acb34c8c69863cc274df4a12c614b002101770d97292f2c0df8bb43158df8523`, and checker checkpoint 8991 / `b96919b38272d87a6885da98a18603065d1c2ccf805cd2c4f65dd22e32ed7af2`, are unchanged.

## Bounded evidence

### Generated output schemas

I extracted both generated sources without entering either production CLI and parsed their ASTs.  Exhaustive AST enumeration found exactly two `forbidden_downstream` constructors in each generated source:

| generated source | positive constructor | RESOURCE constructor |
|---|---|---|
| v25 producer | exactly `lift,fake,Ihara,base_pairs,ambient_E3_E4_enumeration`, all `false` | exactly `lift,fake,Ihara`, all `false` |
| v35 checker | exactly `lift,fake,Ihara,base_pairs,ambient_E3_E4_enumeration`, all `false` | exactly `lift,fake,Ihara`, all `false` |

There are no extra or alternate forbidden dictionaries in either generated body.  Thus v46's four branch predicates match the actual producer/checker constructors: two five-key positive predicates and two three-key RESOURCE predicates.

### Exact v45-to-v46 confinement

A line-preserving `SequenceMatcher` comparison found 64 lines in each file and exactly two non-equal opcodes:

1. line 55, producer-PASS JSON predicate;
2. line 58, checker-PASS JSON predicate.

Each opcode is a one-line replacement which only extends
`{"lift":false,"fake":false,"Ihara":false}` with
`base_pairs:false` and `ambient_E3_E4_enumeration:false`.  The producer-RESOURCE and checker-RESOURCE three-key predicates remain byte-identical.  There is no padding, refactoring, reordered command, or other semantic edit; the 114-byte size increase is precisely the two positive additions.

### Re-run gates

- `python -B ...v25.py --source-patch-info`: PASS, including v24 and generated-v24 pins.
- `python -B ...v35.py --source-patch-info`: PASS, including v34 and generated-v34 pins.
- Wrapper and generated Python AST parse: PASS for v25 and v35.
- `python -B ...v35.py --self-test`: PASS with actual call counts `validate_terminal_checkpoint=2`, `_a4_v33_validate_physical_chain=2`, ordinary materializer `=2`, physical JSON reads `=2`.
- GAP 4.16.0 `ReadAsFunction` parse of v46 through `gap.ps1`: PASS.  The expected unbound-global parse warnings were non-fatal; the driver body was not invoked.

The v35 mutation fixture does not use v34's rejected helper boolean.  It re-seals a duplicated ordinary live-dual history and a TEMP physical shard/HEAD with a changed semantic predecessor, invokes the real generated `validate_terminal_checkpoint -> _a4_v33_validate_physical_chain` path, and obtains respectively `physical:live_dual_history` and `physical:semantic_counter_order`.  Only the Windows transport read/materializer is replaced by a bounded TEMP-file equivalent; the two generated acceptance predicates and dispatch route are the actual ones.

## Preserved dispatch envelope

Because the exact v45-to-v46 diff changes only the two positive dictionaries, direct inspection confirms preservation of all v45 gates:

- five authority side files must be regular, non-symlink files;
- corrected release and all six flat canonical members are size/SHA-bound, copied once, then rechecked;
- v25/v35 wrapper and generated pins, v44/v43 and v430 pins are reached before traversal;
- every owned output/member path must be fresh; the physical root is distinct;
- generated shell uses `set -euo pipefail`, is syntax-checked, and is actually executed;
- exactly one producer runs; producer RESOURCE runs no checker; producer PASS runs at most one checker;
- internal 14400-second/8-GB limits, 15000-second external timeout, RSS margin, and elapsed checks remain live;
- exact terminal cardinality, nonempty outputs, owned markers, and explicit rejection of `UNKNOWN_INPUT`, `HARD_STOP`, `ERROR`, and `Traceback` remain live;
- positive and RESOURCE JSON status/completeness/claim predicates remain branch-specific.

V46 adds no command at all.  It introduces no duplicate rebuild, copy, self-test, worker, retry search, snapshot, closure, or other traversal overhead.

## Claim boundary

This is dispatch authorization only.  A producer RESOURCE terminal remains `UNKNOWN_RESOURCE`.  A producer positive is not an A4 numerator and still requires the independent v35 checker plus subsequent artifact audit.  No A4, fake, Ihara, A0, COMMON or NONMEMBER claim is promoted, and `verified=false`.

GO_FOR_GHA_DISPATCH

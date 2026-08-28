# Luna reply 312 - task307/v7 fixture repair v8

Created exactly the five authorized v8 paths. No existing path was modified.
Python, Node, GAP, GHA, network, and git were not run. SELFTEST and production
are **UNEXECUTED**.

## Final identities

```text
producer  12999  18bd8b83d3ceb3d7091e5bcf4eaaf0b4fbdfdcc6f1e5299bd44ac84b8f7f5877
checker   24993  6cd630b82ee1e4118b77f90b12b7186a9c0d2b604814bdd4f8d2b3e16b84376d
driver     4860  e78fa0d72181bf4420065fd08f020d35d85107154cf053c152656b8f30940b6c
fixture   10322  df30c2e965e6306731c84423ee6c397dc3150b7ac0373147de50e9c437fab864
reply       4698  [self-referential SHA intentionally omitted]
```

The v8 driver pins producer, checker, and fixture with the exact lengths and
SHA-256 values above. All schemas, seals, fixture paths, output paths, markers,
and terminals are v8; the GAP driver is ASCII-only.

## Literal fixture repair

In case `nonzero-member`, the two malformed binding rows (zero-based rows 6
and 7, i.e. one-based rows 7 and 8) are now byte-for-value equal to `A_E`:

```text
row 6 = [0,0,0,0,0,0,1,0,0,0,0]
row 7 = [0,0,0,0,0,0,0,1,0,0,0]
```

Both are 11-entry rows. The first case now has all eleven `A_E` rows and all
eleven `A_E_binding` rows at literal dimension 11.

## New fail-closed fixture preflight

Both producer `fixture_preflight` and independent checker
`fixture_preflight` run over all five case objects before any case compile or
replay. For each case they directly require equality and literal dimensions
(including both sides of every pair) for:

```text
A_theta / A_theta_binding : 2 x 2
A_Z     / A_Z_binding     : 2 x 2
A_E     / A_E_binding     : 11 x 11
D       / D_binding       : 2 x 2
O       / O_binding       : 11 x 2
C       / C_binding       : 1 x 11
```

Each entry is also required to be an integer in {0,1,2}. The producer invokes
the preflight from `parse_fixture`; the checker invokes it once in `run`
before any `replay`. The preflight does not consult `expected_cases`
metadata. The existing wrong-seal checks remain fail-closed.

## Expected case tuples

```text
case                 closure-rank  kernel-dim  3^d-1  Hd1-rank  terminal
nonzero-member                 2          2        8         2  MEMBER
outside-nonmember              1          1        2         1  NONMEMBER
zero-member                    1          1        2         0  MEMBER
zero-nonmember                 1          0        0         0  NONMEMBER
post-c-cancel                  2          1        2         1  MEMBER
```

Plural seeds, distinct actions, joint closure, post-C left kernel, separated
dimension/cardinality, MEMBER ancestry, NONMEMBER dual replay, and typed
production `STATIC_BLOCKED` remain unchanged.

## Mutation routes

Producer retains all 19 owners, each with canonical-change and reseal gates
before its designated `compile_case` semantic rejection:

```text
field_modulus theta_seed theta_action z_action eta_action
D_entry O_entry C_entry action_order premature_C target
seed_index parent row_theta left_kernel Hd1 member_ancestry dual terminal
```

Independent checker routes the first eleven fixture owners
(`field_modulus` through `target`) through `independent_terminal`, and the
eight receipt owners (`seed_index`, `parent`, `row_theta`,
`left_kernel`, `Hd1`, `member_ancestry`, `dual`, `terminal`) through
resealed `replay`. Receipt mutation case indices remain:
`seed_index,parent,row_theta,left_kernel,member_ancestry -> 0`;
`Hd1,dual,terminal -> 1`; fixture routes use case 1. Every route requires
owner identity, canonical change, reseal, oracle reach, semantic rejection,
and final rejection. Both wrong-seal canaries remain required.

## Performance and execution accounting

The new preflight is a single fixed linear scan of five cases and six binding
pairs, with literal shape checks only; it performs no rank, closure, kernel,
or full-case recomputation. Producer parses the fixture once and checker loads
it once. Existing closure work remains one pass per case, and exhaustive
enumeration remains bounded to the intended dimension-two canary
(`3^d-1 = 8`) plus the existing small dual/coordinate searches. No redundant
full-case recompilation, repeated fixture parsing, new sleeps, locks, or
serial
subprocesses were added.

```text
producer mutation gate:       19/19 required, ACTUAL 0/19 (UNEXECUTED)
independent checker gate:     19/19 required, ACTUAL 0/19 (UNEXECUTED)
wrong-seal canaries:          required, ACTUAL 0 (UNEXECUTED)
SELFTEST:                     UNEXECUTED
production:                   UNEXECUTED
actual A5 / actual A6:        0/3 / 0/3
lift / fake certificate / Ihara result: NONE DECLARED
```

`TASK307_R07_TASK307_FIXTURE_REPAIR_V8_UNEXECUTED`

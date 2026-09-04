# Sol reply -- actual separator dual-root preflight

## Result

The exact cross-checked separator has only one nonzero Task712 dual root.
Characters 1, 2 and 3 vanish identically and therefore contribute no later
actor descendants.  The actual scalar scan can be reduced from four active
characters/20 pairings to character 0/five pairings without narrowing the
mathematical universe.

Inputs were the exact Task907 lambda (12,096 bytes, SHA-256
`7522ee1f00f386b229ea46bc0f2b9fdf2854cf03c262f40a2f60dd9ced0102ed`)
and Task712 artifact `9915928157`.  I ran the producer-side v15 map reader
(126,565 bytes, SHA-256
`76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632`)
and the independently implemented checker-side reader (141,770 bytes,
SHA-256
`8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662`).
Each authenticated all 40 Task712 tables and independently computed
`sparse_adjoint(B_fwd, lambda)` and the four `T_fwd` transposes.

| character | root support | lead/value | packed SHA-256 | child supports |
|---:|---:|---:|---|---|
| 0 | 2742 | 3/2 | `af62027aa99fbd1a4b7b53c6b380b4e7fa7403915ea91f9d51d7cb2198c7e053` | 2742,2742,2742,2742 |
| 1 | 0 | -- | `8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838` | 0,0,0,0 |
| 2 | 0 | -- | `8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838` | 0,0,0,0 |
| 3 | 0 | -- | `8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838` | 0,0,0,0 |

Character-0 child hashes in actor order `[1,-1,2,-2]` are:

```text
aa54bbed30791f3f771c5fb8d74e38329564101cbcd805db20e1e232595e7033
1b98282910ed00d253cad00cbc389b9c85c6b84be9b8da0418ece4f8b0218cd8
f98650b321a16e846539698d98710a544fd1953656afcaecbee995523f0def2b
2245611c3efcef71758e281950ca4b23ba96d0991880cdb92ecafa0fac7aa8b4
```

Direct F3 row reduction of the root followed by those children has rank 5
and normalized leads `[3,1,0,2,4]`.  Thus a root scalar EOF would genuinely
leave four new independent first-depth tests.

The two independent seed evaluators also agree on the character-0 root:

```text
nonzero=15
[0,0,1,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,2,0,0,1,2,0,0,0,2,1,1,0,2,0,0,0,0,1,0,0,2,1,0,1,0,0]
```

These are direct seed terms only.  They are not Violation receipts until the
canonical-P1 coefficient terms are subtracted in the exact relation order.
Task908 now implements precisely that remaining one-pass calculation.

```text
DUAL_ROOT_PREFLIGHT_CROSS_CHECKED=yes
TRIVIAL_CHARACTER_ORBITS=3/4
ACTIVE_CHARACTER=0
ACTIVE_ROOT_RANK_WITH_CHILDREN=5
SCALAR_VIOLATION=NOT_DECIDED
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
verified=false
```

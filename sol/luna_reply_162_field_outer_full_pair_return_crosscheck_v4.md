# Luna 162: full-pair return restriction independent cross-check v4

Date: 2026-08-26
Role: Luna / standalone finite linear-algebra checker
Grade: `CROSSCHECKED_FINITE_RESTRICTION; D2_LEFT_UNKNOWN`

## Verdict

The v3 reducer defect was repaired.  It had solved a 147-coordinate cocycle
against only the first 58 ambient rows.  The corrected reducer uses all 147
rows, rejects inconsistent augmented systems, and confirms the full
`[B^1|H^1]` coordinate basis.

For both frozen candidates, the mandatory canaries pass:

```text
rank(Z^1) = 58
rank(B^1) = 43
rank([B^1 | H^1 complement]) = 58
all transformed T_p z are Z^1 cocycles
rank(U^3 - I) = 0
restriction intertwining rank = 0
all restricted source Q-cocycles land in target Q-cocycles
```

The independently reconstructed E2 restriction map

```text
H^1(Q,H^1(H,V)) -> H^1(Q,H^1(D,V))
```

has rank `0` for both A9 and A12.  The target cyclic coefficient calculation
also gives `dim V^D=21`, `dim H^2(Q,V^D)=0`, and `dim H^3(Q,V^D)=0` for both.
Thus the target relative LHS has only its `(1,1)` filtration piece, and the
typed total restriction is

```text
im(K^2(P0,H;V) -> K^2(R,D;V)) = 0       (A9 and A12)
```

This is a finite constructed-module statement only.  The signed source
transgression ranks were not independently materialized in this bounded run:

```text
rank(d2_left)^+ = UNKNOWN
rank(d2_left)^- = UNKNOWN
```

## Exact finite output

The two candidates gave the same dimensions and canaries:

| field | A9 | A12 |
|---|---:|---:|
| `|H|` | 81 | 81 |
| `rank Z^1(H,V)` | 58 | 58 |
| `rank B^1(H,V)` | 43 | 43 |
| `dim H^1(H,V)` | 15 | 15 |
| `dim H^1(D,V)` | 14 | 14 |
| `rank(H^1(H,V)->H^1(D,V))` | 3 | 3 |
| `rank(U-I)` on `H^1(H,V)` | 5 | 5 |
| `rank(U^3-I)` | 0 | 0 |
| source `H^1(Q,H^1(H,V))` dimension | 10 | 10 |
| target `H^1(Q,H^1(D,V))` dimension | 2 | 2 |
| induced E2 restriction rank | 0 | 0 |
| `dim V^D` | 21 | 21 |
| target `H^2(Q,V^D)` | 0 | 0 |
| target `H^3(Q,V^D)` | 0 | 0 |

The Q-action was implemented exactly as

```text
(p.z)(h) = p z(p^-1 h p),
```

with `p=row36`, `p^3=row27`, and `delta(v)(h)=h v-v`.  The raw identity
`T_p^3 z-z=delta(z(p^3))` had already passed for all 58 basis cocycles and
all 81 H-elements.  In v4, each first transform `T_p z` additionally passed
the full Z1 edge equations and the corrected 147-row coordinate solve.

## Pins and independence

Computational input:

```text
search/certs/d972_b4_word_key_artifact_v1_20260816.json
bytes = 176474
SHA-256 = 564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9
```

The standalone runner rebuilt the frozen P0 table, both explicit maps,
`V=W(phi_A) tensor W(phi_B)`, H cocycles, D cocycles, Q actions, and the
restriction matrix.  It imported no prior runner, output matrix, addendum
hash, GAP helper, or cohomology package.  No actual A.18 or K2-class claim is
made.  No GAP, GHA, git, credentials, Lean, or heavy full run was used;
scratch remained in TEMP.

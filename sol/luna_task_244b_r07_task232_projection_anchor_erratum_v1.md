# Luna task 244b - task232 projected-generator anchor erratum v1

Commissioner: Sol / 2026-08-28

This is a binding erratum to
`sol/luna_task_244_r07_task232_second_actual_kernel_repair_v1.md`.
Read `sol/proof_r07_a4_anchored_relative_ideal_lift_v247.md` in full before
finalizing task244.

## 1. Withdrawn requirement

Do **not** assert or test that the literal source word

```text
[x,y]^3 = [-1,-2,1,2,-1,-2,1,2,-1,-2,1,2]
```

is roof-trivial.  It is nonidentity in all ten actual task176 roof
coordinates.  The old canary in task244 Section 4 is withdrawn.

## 2. Replacement positive ABI

For every ordered word-bearing basis element `k_i` of the actual
`K=ker(Delta1->Delta0)`, independently evaluate its image in
`D1=H2(9)` and serialize the unique `a_i in F3` with

```text
q(k_i) = z0 ^ a_i,   z0 = (0,0,3).
```

Require at least one nonzero `a_i`.  Select the least such index `j`, set
`e=inverse_F3(a_j)`, and emit the literal source word
`u_z=free_reduce(u_j repeated e times)`.  Producer and checker must replay:

```text
u_z in actual K;
task198 Delta0 value of u_z = identity;
D1 value of u_z = z0;
selected index/scalar and source-word ancestry are exact.
```

If a complete independently accepted K basis has no nonzero `a_i`, return an
honest input/type STOP.  Never substitute the literal commutator cube.

## 3. Independence and mutations

The checker reconstructs every `D1` value directly from the basis source
word, solves the one-row system independently, and compares the complete
source word and all endpoint values.  Add owning mutations for the projected
coordinate, selected index, inverse scalar, word exponent/concatenation,
Delta0 identity, and D1 `z0` target.  The usual fatal mutation-acceptance rule
continues to apply.

All other task244 requirements remain unchanged.

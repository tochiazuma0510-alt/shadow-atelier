# R07: corrected filtered direct sides for the grade-two scalar test (v541)

Author: root / 2026-09-05

This note repairs the scalar interface, retaining the actual P1 cache,
Task554 relations, Task712 homogeneous maps, connection state and separator.
It supersedes v533's actor formula and the projected direct-seed routine in
scalar owner v15 / actual root batch v1. No grade-two decision is made.
`verified=false`.

## 1. The two distinct degrees in a canonical P1 lift

Write the registered precision-two source as

```text
M_{<=2} = L + V,
L = (F3^6048)^4 + (F3^18144)^4 + F3^8,  dim L = 96776,
V = (F3^36288)^4.
```

This is its fixed coordinate decomposition, not an equivariant splitting.
A canonical P1 lift is `btilde_i = (b_i, z_i)`. The accepted truncation
theorem v483/v486 identifies its lower part with the Task554 row `b_i`.
Generally `b_i != 0`.

For a legal actor `t`, its full filtered action has block form

```text
T_full,t(b,z) = (A_t b, K_t b + T_2,t z).                 (1.1)
```

Task712 supplies the character blocks `T_a,t` of `T_2,t`. It does not
supply the term `K_t b`. That term vanishes for an already pure degree-two
defect, but not in general for the direct side of a P1 actor relation.

Similarly the full word-sum from v451 has form

```text
P_a(b,z) = (P_1,a b, H_a b + e_a z).                     (1.2)
```

V453 identifies `e_a` with the direct character slice on V. It does not
identify `P_a` with that slice on all of `M_{<=2}`.

## 2. Correct seed and actor scalars

Keep exactly the global `SeedRed(s)` and `ActRed(i,t)` of v531, with their
old/new offsets and all four target-block contributions. Let the raw seed
evaluation be `(s_1,s_2)`, and put `v_q[i] = <q,z_i[a]>` for a raw covector
`q` in the dual of character a.

The complete final defects are

```text
D_s = (s_1,s_2) - sum_i SeedRed(s)[i] (b_i,z_i),
D_i,t = T_full,t(b_i,z_i) - sum_k ActRed(i,t)[k] (b_k,z_k).
```

The accepted P1 relations make both lower parts zero. Hence the exact
character-a scalar formulas are

```text
SeedPair(q,s)
  = <q,s_2[a]> - sum_i SeedRed(s)[i] v_q[i],              (2.1)

ActorPair(q,i,t)
  = v_(T_a,t^*q)[i]
    + <(pi_a K_t)^*q,b_i>
    - sum_k ActRed(i,t)[k] v_q[k].                       (2.2)
```

Proof: expand the displayed full defects, apply the direct slice `pi_a`,
and pair. In (2.2), transpose the homogeneous term and the lower-to-top
term separately. No projectors act on just one side of a relation. QED.

The old direct-seed routine instead uses

```text
pi_a gr2(P_a(s_1,s_2)) = s_2[a] + pi_a H_a s_1.
```

It therefore adds the extraneous scalar `<q,pi_a H_a s_1>` unless the
same full operator is also applied to the reconstructed side. Projecting
the entire final defect would be valid, since its lower part is zero;
computing (2.1) directly is simpler.

The old actor routine omits the middle term of (2.2). This is the same
filtered/associated-grade distinction already required for canonical lift
construction in v486. The homogeneous actors remain correct for the
subsequent orbit of a pure defect and for its raw dual orbit.

## 3. Actual seed-2 counterexample to the old interface

Task920 performed a bounded direct comparison using the actual Task919
`q-a0-root.bin`, whose support is 2742. The zero-based registered seed is 2.

```text
raw seed character-0 top:
  support = 568
  packed SHA = e67d0a0b21aaf41fd1617811b45cd51191a0087c7d04fcc33dda5a58f4fcfca6
full-projected seed character-0 top:
  support = 849
  packed SHA = 7f151eec27ff74d68b13759ad3719913dcf26c3434274aa0e95868d5a4e45983
raw minus projected:
  support = 1050
  packed SHA = f57b13d028ca786c3bab7c88dbef463a63f8558093c18c9c4b626d9f87c5ed60
  pairing with actual q = 2 mod 3.
```

The old producer/checker agreed on scalar 1. All reconstructed-side terms
are identical, so the exact scalar in (2.1) is `1+2=0 mod 3`.
Consequently Task919's same-object/numeric agreement remains an accurate
receipt of that computation, but `SAFE_INPUT_TO_ACTUAL_SEED2_MATERIALIZER`
is withdrawn. It does not justify a new physical pivot.

This calculation does not invalidate the raw separator, the three zero
character roots, the 504-row character-0 dual orbit, the P1 lifts or the
global relation coefficients. It invalidates the identification of the
old scalar with the final-defect pairing. Independent Task921 agrees on
the actual correction using checker-side arithmetic and accepts the
repair formulas, including Section 4. No new A0 numerator is claimed here.

## 4. Explicit inexpensive adjoint of the missing actor term

The missing term can be computed without applying a full actor separately
to each of 8059 P1 rows. Here is the finite formula in the actual source
coordinate system.

For tag j, let the actor value be `(u_j,eps_j,k_j)` in the existing
section-left/kernel-right affine convention. Let `tau_j` be its registered
character transport. For parity e write

```text
E_e(k_j) = product_m (1+X_m)^(S(e)k_j)_m mod degree >= 3,
c_e(gamma) = coefficient of X^gamma in E_e(k_j).
```

Let alpha range over the constant and three degree-one monomials, beta
over all six degree-two monomials, and g over the 504 PSL coordinates.
Then the lower adjoint `kappa_a,t(q) = (pi_a K_t)^*q` has entries

```text
kappa[c,j,h,alpha,g]
 = sum_e chi_(tau_j(a))(e+eps_j) chi_(tau_j(c))(e)
         sum_(beta >= alpha) c_e(beta-alpha) q[j,h,beta,u_j*g]. (4.1)
```

Here c is a source character and h is the Fox component. The eight
auxiliary entries of kappa are zero, since source actors transport those
entries within the auxiliary block and do not inject them into V.
All sums are in F3; beta >= alpha is componentwise. There is no extra
normalizing factor because 4=1 in F3.

Proof: invert the source Fourier character transform to parity e, apply
the existing prefix polynomial and PSL translation, then transform the
output back at parity e+eps_j. The coefficient from input alpha to output
beta is exactly c_e(beta-alpha). Transpose this entrywise formula. The
six tags, both components and all six top monomials remain coupled. QED.

A bounded checker can test (4.1) against direct full-actor evaluation on
nonzero lower and mixed rows. Its degree-two adjoint, computed by the same
entrywise derivation with |alpha|=2, must equal the accepted Task712 table.

## 5. Streaming the exact lower contractions

For each active q and actor t construct kappa once. Compute

```text
w_t[i] = <kappa_a,t(q), b_i>.
```

Task554 stores each old row as a 6056-trit character-lower-plus-auxiliary
slice and a 72576-trit four-character grade-one companion. Each new row is
one 18144-trit grade-one slice with all other lower coordinates zero.
Thus w_t is obtained by paired dot products on those existing blobs, in
the same global P1 order. No canonical lift or lower closure is rebuilt.

The four contractions for one q fit in `4*8059 = 32236` unpacked bytes.
The four dense lower covectors take `4*96776 = 387104` unpacked bytes.
Immutable Task554 row payloads total 67011332 bytes (v480/v482), and may be
streamed with bounded chunks. These are payload counts, not RSS promises.

Add w_t to the old homogeneous direct-actor value arrays before applying
the unchanged v540 relation subtraction. Direct seed values use raw seed
evaluation followed by an ordinary character slice. The one-pass P1 cache
projection and prepare-plus-one-block relation accumulation remain usable.

## 6. Implementation and decision boundary

The corrected root batch must compare the same complete 32280 origin
family, in the same 44-seed then row/actor order. Its receipts must state
that actor direct values include the full lower-to-top term and seed
direct values are raw slices. Old seed-row hashes authenticate the wrong
direct-side choice and cannot be reused as correctness checks.

A true nonzero scalar still requires v534 materialization, full P1-zero
comparison and physical insertion before increasing rank. A zero root
scan still leaves later dual orbit rows. Neither outcome completes A0.

```text
SEED2_PHYSICAL_VIOLATION_FROM_RUN33903333330: WITHDRAWN
CORRECT_SEED2_ROOT_SCALAR: 0 (producer-side and checker-side comparisons agree)
CORRECT_FILTERED_SCALAR_FORMULAS: PAPER DERIVATION ABOVE
TASK921_FORMULA_AUDIT: PASS_V541_REPAIR
EXISTING_P1/CONNECTION/SEPARATOR_PARENTS: RETAINED
ACTUAL_CORRECTED_ROOT_SCAN: PENDING
GRADE2/A0/COMMON/COFINAL/FAKE/IHARA: NOT DECLARED
verified=false
```

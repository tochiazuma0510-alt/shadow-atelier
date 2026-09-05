# Task921 -- audit of filtered direct sides in the scalar compiler

## Verdict

`VERDICT=FAIL_OLD_FORMULAS / PASS_V541_REPAIR`

The scalar computed by Task919 is not the v531 final-defect pairing.  The
producer and checker independently agree on the bytes of the same **wrong
formula**.  There are two distinct omissions:

1. the seed implementation applies a full filtered projector to the seed but
   subtracts only ordinary character slices of the canonical lifts; and
2. v533's actor formula applies only Task712's homogeneous degree-two actor to
   the top of a lift and omits the full actor's lower-to-top term.

For the actual character-0 root and zero-based seed 2, a checker-side bounded
calculation gives correction `2`; hence the reported scalar `1` becomes
`1+2=0 mod 3`.  Task919's `SAFE_INPUT_TO_ACTUAL_SEED2_MATERIALIZER=yes` is
withdrawn.  No later origin was checked by the stopped old scan, so the
corrected root scan is pending.  `verified=false`.

## F921-1: exact block-triangular calculation

In the fixed implementation coordinates write a precision-two row as
`x=(x_<2,x_2)`, where `x_<2` contains the complete 96,776-coordinate P1 part.
For the full filtered character word-sum and a full source actor there are
necessarily block formulas

```text
pr_2(P_a x)       = e_a x_2 + H_a x_<2,
pi_a pr_2(A_t x)  = T_(a,t) pi_a(x_2) + K_(a,t) x_<2.      (1)
```

Here `e_a` is the v453 associated-grade projector, `T_(a,t)` is the Task712
homogeneous actor, and `H_a`, `K_(a,t)` are the lower-to-top blocks.  V451
already warns that the full `P_a` is not the associated-grade projector, and
v483/v486 explicitly warn that a full actor on a P1 lift cannot be replaced
by its homogeneous action.

Let

```text
D_s = E_s - sum_i r_si btilde_i,       r_si=SeedRed(s)[i].
```

The accepted P1 relation says `E_s,<2=sum_i r_si b_i`, so `D_s,<2=0`.
Applying the full projector to the **entire** difference would be legal:

```text
pr_2(P_a D_s)
 = e_a E_s,2 + H_a E_s,<2
   - sum_i r_si (e_a z_i + H_a b_i)
 = e_a(E_s,2 - sum_i r_si z_i).                         (2)
```

The current code instead computes

```text
d_old = e_a E_s,2 + H_a E_s,<2 - sum_i r_si e_a z_i.   (3)
```

Thus it omits `-sum_i r_si H_a b_i`, equivalently retains the extraneous term
`H_a E_s,<2`.  This is not repaired by the lower-zero theorem: that theorem
justifies either (2) or taking the direct top slice **after subtraction**; it
does not justify applying `P_a` to only one side.

The minimal exact scalar repair is therefore

```text
SeedPair(q,s)
 = <q,E_s,2[a]> - sum_i r_si <q,z_i[a]>.                (4)
```

Equivalently, retain the full projector but apply it to every reconstructed
lift as well.  Formula (4) is cheaper and is exactly v453's direct slice of
the final lower-zero defect.  Consequently the old concatenated
`SEED_REGISTERED_ROW_SHA` values authenticate the wrong direct rows and must
not be reused by a corrected implementation.

## F921-2: actual seed-2 arithmetic

I imported only the independent checker arithmetic
`search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py`, decoded
the actual Task919 `q-a0-root.bin`, and independently evaluated the first
three relators.  I did not import the producer.  The actual `q` has support
2,742.  For seed 2 the checker-side arrays give

```text
raw character-0 top support                         568
full-projected character-0 top support              849
raw/full-projected differing coordinates          1050
<q, raw top>                                           0
<q, full-projected top>                                1
<q, raw - full-projected>                              2  (mod 3)
```

The reconstruction side is unchanged, so

```text
correct scalar - old scalar = 2,
correct scalar = 1 + 2 = 0 mod 3.                       (5)
```

As a bounded control, seeds 0 and 1 each have raw-minus-projected pairing
zero; their old scalar zero therefore remains zero.  This says only that the
first three corrected seed scalars are zero.  It says nothing about seeds
3--43 or any actor origin.

Task920 separately replayed the complete 96,776-coordinate lower equality
and found

```text
SeedRed(2) = [(2,2),(505,2),(1008,2),(1511,2)]
```

with no new-block terms.  That full equality is consistent with (2)--(5):
the missing projected reconstruction term is exactly the negative of the
observed one-sided lower-to-top contribution.

## F921-3: v533 actor formula also omits a triangular term

For `btilde_i=(b_i,z_i)`, v531's actor defect is

```text
D_(i,t) = A_t^full(b_i,z_i) - sum_k ActRed(i,t)[k](b_k,z_k).
```

Its exact character-`a` scalar is

```text
ActorPair(q,i,t)
 = v_(T_(a,t)^*q)[i]
   + <(pi_a K_t)^*q,b_i>
   - sum_k ActRed(i,t)[k] v_q[k].                       (6)
```

The middle term has a plus sign because it is part of the actor direct side.
It is generally nonzero: a canonical lift has the nonzero P1 row `b_i` as its
truncation.  It vanishes only when the actor is applied later to an already
pure degree-two final defect.  That later orbit action must not be confused
with the direct side of a P1 actor relation.

The actual root batch obtains `v_q` and the four
`v_(T_(a,t)^*q)` arrays by pairing Task712 covectors with plain character
slices of the degree-two cache, initializes every actor accumulator from the
four child arrays, and then subtracts `ActRed`.  It never reads `b_i` for an
actor contraction.  The independent checker repeats the same construction.
Therefore both sides omit the middle term of (6); independence of executables
does not cure the shared mathematical specification error.

The minimal repair is either to evaluate the complete actor defect and slice
it only after its P1 part is zero, or to add

```text
w_t[i] = <(pi_a K_t)^*q,b_i>
```

to each homogeneous actor direct value before the unchanged relation
subtraction.  No old actor scalar, zero or nonzero, is presently identified
with a v531 defect scalar until this is done.

## F921-4: audit of v541 formula (4.1) and packed contraction

The explicit adjoint in
`sol/proof_r07_scalar_filtered_direct_side_repair_v541.md` is correct.  Its
formula

```text
kappa[c,j,h,alpha,g]
 = sum_e chi_(tau_j(a))(e+eps_j) chi_(tau_j(c))(e)
         sum_(beta>=alpha) c_e(beta-alpha)
                              q[j,h,beta,u_j*g]
```

is the literal transpose of the checker-side full action:

- the input Fourier transform contributes `chi_(tau_j(c))(e)`;
- the actor sends parity `e` to `e+eps_j`, so the output transform contributes
  `chi_(tau_j(a))(e+eps_j)`;
- multiplication by `E_e(k_j)` sends lower monomial `alpha` to top monomial
  `beta` with coefficient `c_e(beta-alpha)`; and
- the assignment through `pmap` sends PSL coordinate `g` to `u_j*g`, so the
  adjoint samples `q[...,u_j*g]`, not an inverse translate.

There is no omitted Fourier normalization: `1/4=1` in `F3`.  Auxiliary
coordinates are correctly zero because the source action preserves the
auxiliary block and does not inject it into degree two.  Thus v541 (4.1) has
the correct character weights, translation direction, polynomial coefficient,
and sign in (6).

The packed lower contraction plan also matches v480 exactly:

```text
old row: 6056 trits = 6048 owner-V0 + 8 Aux,
         plus 72576 trits = all four V1 characters;
new row: 18144 trits = its owner V1 character, all other lower entries zero.
```

Hence the immutable payload total `67,011,332` bytes is sufficient to compute
all `w_t[i]` in global P1 order; no lower closure or canonical lift rebuild is
needed.  The stated temporary counts are exact:

```text
four w arrays:      4*8059  = 32,236 unpacked bytes,
four dense kappas:  4*96776 = 387,104 unpacked bytes.
```

A corrected producer and checker must each preserve least-significant-trit-
first packing, row boundaries, the global embedding of old/new slices, and
the six-tag/two-component/six-top-monomial coupling.  A mixed lower/top
full-actor canary should compare (4.1) entrywise with direct full action; its
pure degree-two restriction should compare with the accepted Task712 table.
These are finite implementation gates, not extra mathematical terms.

## F921-5: exact surviving boundary

The following results survive unchanged:

- v451's filtered/projector distinction and reconstruction identity;
- v453's direct character-slice theorem, used only after complete P1 zero;
- the v483/v486 canonical P1 lifts, including their full-actor triangular
  construction rule;
- v531's global `SeedRed`/`ActRed` formulas, signs, 32,280-origin roster and
  order;
- the actual P1 cache, Task554 relations, Task712 homogeneous maps, separator,
  connection state, raw dual roots, and the three zero character roots; and
- Task919's same-object statement and its numeric claim **about the old
  implemented expression**.

V533 seed equation (2.1) survives only with `z_s^a` implemented as the raw
homogeneous character slice in (4).  V533 actor equation (2.2), Proposition
2.1, and the claim that five top-cache value vectors suffice are superseded
by (6) and v541.  The scalar-formula portions of the old Task846/847 PASS
rulings are correspondingly withdrawn.  V534's typed
`RawDual -> Violation -> RawMaterialization -> PhysicalPivot` architecture
remains valid conditional on a corrected scalar receipt that binds the raw
seed semantics and the lower-contraction inputs; it supplies no receipt for
Task919 seed 2.

```text
TASK919 REPORTED SCALAR:                  1 FOR THE OLD EXPRESSION
TASK919 SEED-2 V531 DEFECT SCALAR:        0
SAFE SEED-2 MATERIALIZER INPUT:           NO
V541 FORMULAS (2.1),(2.2),(4.1):          PAPER PASS
CORRECTED 32,280-ORIGIN ROOT SCAN:        PENDING
GRADE2 MEMBER/NONMEMBER:                  NOT DECIDED
A0/COMMON/COFINAL/FAKE/IHARA:             NOT DECLARED
verified=false
```

`R07_SCALAR_FILTERED_PROJECTION_AUDIT_921_FAIL_OLD_PASS_V541`

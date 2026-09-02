# Task 544 independent audit -- relative fibre-echelon lift

`verified=false` (no Lean proof was supplied).

The relative fibre lemma is correct, and lower-first elimination computes its
fibre when it is fed the complete high-precision legal image.  The draft needs
repairs to its grade dimensions, to the actor-closure contract, and to the
description of the deterministic section.  With those repairs it is a finite
conditional algorithm, not a computed lift or a surjectivity theorem.

## F1. The extended augmentation ideal

Let `J=J(k[V])`, where `V=C3^3`, and choose a transversal `T` for `V` in
`Qtilde`.  As a vector space,

\[
 k[\widetilde Q]=\bigoplus_{t\in T}k[V]t.
\]

The induced map to `k[Q]` sends the coefficient in each summand through its
augmentation.  Therefore

\[
 \ker(k[\widetilde Q]\to k[Q])
   =\bigoplus_{t\in T}Jt=Jk[\widetilde Q].
\]

Normality of `V` makes `J` conjugation-stable, so this is also
`k[Qtilde]J` and is a two-sided ideal.  Calling it `I`, the same conjugation
argument gives

\[
 I^d=k[\widetilde Q]J^d=J^dk[\widetilde Q].
\]

For `u_i=v_i-1`,

\[
 k[V]\cong k[u_1,u_2,u_3]/(u_1^3,u_2^3,u_3^3).
\]

Thus `J^7=0`, `J^6` is nonzero, and hence `I^7=0`.  The coefficients of
`(1+t+t^2)^3` are indeed

```text
(1,3,6,7,6,3,1).
```

They are, however, the dimensions in one transversal fibre, not the total
dimensions asserted in v440 (1.3).  The correct formula is

\[
 \boxed{\dim_k I^d/I^{d+1}
  =|Q|[t^d](1+t+t^2)^3}\qquad(0\le d\le6),
\]

where `I^0=k[Qtilde]`.  Already at `d=0`, the quotient is `k[Q]` and has
dimension `|Q|`, not 1.  The later R07 coordinate counts actually use this
missing factor and therefore are not numerically damaged by the prose error.

Exact replacement for v440 (1.3):

```text
I^d=R J(V)^d and I^7=0.  Relative to any transversal of V, the
per-coset grade multiplicities are (1,3,6,7,6,3,1); consequently
dim_k I^d/I^(d+1)=|Q|*(1,3,6,7,6,3,1)_d.
```

## F2. Image fibre and indexing

Write `E_d=im C_d`.  The reduction map satisfies
`p_d C_(d+1)=C_d`, and it maps `E_(d+1)` onto `E_d`.  Moreover

\[
 D_d=\ker C_d
 =\{m:\nu(m)=0,\ A(m)\in F^dW\}.
\]

Restricting `C_(d+1)` to `D_d` gives

\[
 D_d\longrightarrow F^dW/F^{d+1}W.
\]

Its image is exactly `ker(E_(d+1)->E_d)` and its kernel is exactly
`D_(d+1)`.  Hence there is in fact a canonical isomorphism

\[
 \boxed{D_d/D_{d+1}\ \simeq\ K_d}.
\]

The draft's fibre equality is therefore correct.  The indexing is also
correct: a solution modulo `F^d` has its next residual in grade
`F^d/F^(d+1)`.  With the draft's convention

\[
 \rho_d=T-A(c_{d-1}),
\]

the update is `c_d=c_(d-1)+delta_d` and must satisfy
`A(delta_d)=rho_d`; there is no missing minus sign.  If one instead defines
the residual as `A(c)-T`, the membership query must use its negative.

## F3. One chosen lower solution does not restrict the fibre

Fix any lower solution `c`.  The set of every solution with the same target
modulo `F^d` and the same normalized exponent is precisely

\[
 c+D_d.
\]

Thus all possible next-grade changes are

\[
 \{A(\delta)\bmod F^{d+1}:\delta\in D_d\}=K_d.
\]

This ranges over differences from every lower solution, not merely over a
preselected source-coefficient lift of `c`.  Consequently a functional on
the full grade space which annihilates all of `K_d` and is nonzero on
`rho_d` is an exact negative dual for this filtered problem.  This statement
depends on computing the full `D_d`; a dual against a chosen correction
submodule or a partial closure is not exact.

Suggested replacement for the last sentence of Corollary 2.2 is:

```text
Since the complete lower solution fibre is c_(d-1)+D_d, a dual
annihilating the full K_d and not rho_d excludes every solution modulo
F^(d+1), independently of the initially selected representative.
```

## F4. What lower-first elimination does and does not prove

For a fixed finite list of complete rows `(L_i,G_i)`, the two-block
elimination is standard and exact if it carries the entire row through every
operation.  Inductively, retained lower-pivot rows have independent lower
parts and span all processed lower parts; retained zero-lower grade rows span
the kernel fibre of the processed full-row span.  If a new reduced lower part
is nonzero, its independence means that the fibre does not change.  If it is
zero, its grade remainder is exactly the new possible fibre direction.
This proves Theorem 3.1 after all input rows have been processed.  A later
lower pivot cannot invalidate an earlier one.

A row dependent only in the lower block must not be discarded.  The minimal
example is

```text
v1 = (1 | 0),   v2 = (1 | 1).
```

The second lower part is dependent, but `v2-v1=(0|1)` is the whole fibre.
Step 3 of v440 handles this correctly provided its grade part and ancestry
are carried through the lower reduction.

The theorem by itself does not justify performing actor closure on retained
**physical image** rows.  Here is an abstract counterexample.  Over F3 let
`M=k^3`, `Y=k^2`,

```text
A(e1)=A(e2)=(1,0),   A(e3)=(0,1),
s(e1)=e1,            s(e2)=e1+e3,   s(e3)=e2.
```

The actor `s` is invertible.  Image elimination on seeds `e1,e2` retains only
the image of `e1`; acting on that representative finds nothing new.  But the
discarded source row has `A(s(e2))=(1,1)`, so the full actor orbit has the
missing `(0,1)` direction.  The failure occurs because `A` does not induce an
action on its image: its kernel is not actor-stable.

This is a live R07 concern, not merely an abstract one.  The six-tag
occurrence map is equivariant for its twisted correlated action, whereas the
fixed physical aggregation generally has no common actor action.  Therefore
the safe contract is:

```text
Close the original 44 seeds under all four correlated actors in the
source or the complete occurrence-separated filtered module, retaining
source ancestry.  Only then aggregate each complete row and feed it to
the lower/fibre echelon.  Equivalently, regenerate every source-orbit row.
Never infer a child from an aggregated physical image row alone.
```

Subject to this replacement, lower-first elimination spans the whole image
fibre.  Without it, Theorem 3.1 is insufficient and can give a false
NONMEMBER.

## F5. Regeneration and MEMBER ancestry

Regenerating the complete correlated closure from the original 44 literal
seeds at every higher precision is sufficient to avoid Task540's
lost-lower-kernel error.  It recomputes `ker C_d` from the full legal source
space rather than from a lower-precision image basis.  The regeneration must
obey F4: source/occurrence closure first, exact high-precision evaluation,
then aggregation and two-block elimination.

On MEMBER, regeneration does not remove the need to retain:

1. the chosen lower solution as a literal accumulated correction;
2. every coefficient operation used to obtain the zero-lower fibre row and
   to reduce `rho_d`;
3. seed identifiers, signed actor paths as source words, F3 coefficients,
   and the pinned convention for coefficient 2;
4. a replay showing zero normalized exponent, zero lower change, and the
   claimed grade correction; and
5. the literal updated product needed to evaluate the next residual at full
   precision.

Keeping only the final fibre pivot or only physical image coefficients is not
enough.  Also, v440's phrase "There are exactly two safe implementation
choices" is too strong; many equivalent nullspace algorithms exist.  Replace
it by "Two sufficient implementation choices are".

## F6. Deterministic section and literal expansion

Because the map `D_d/D_(d+1)->K_d` is already a canonical isomorphism, its
inverse on `K_d` is not created by an echelon choice.  A deterministic
echelon instead chooses a representative in `D_d` of that unique quotient
class.  With fixed orders, it can define a linear representative map

\[
 \widehat h_d:K_d\longrightarrow D_d,
 \qquad A(\widehat h_d(\rho))\equiv\rho\pmod {F^{d+1}},
\]

whose composite with `D_d->D_d/D_(d+1)` is the canonical inverse.

The ancestry expands literally.  A leaf is a source-word conjugate
`d r_i d^-1`; coefficient 2 may be represented by its inverse or by two
copies, with the choice pinned.  Every factor evaluates to identity at the
current finite quotient, so the Fox product rule reduces to addition, and
the chosen ordered product has exactly the recorded row.

This defines a section only on the actual image `K_d`.  It neither proves
`K_d=G_d` nor proves that the next actual residual belongs to `K_d`.
Furthermore, the six maps are not literally composable maps with matching
domains.  What can be iterated are the six selected updates and residual
recomputations.

Exact replacement for v440 (5.2) and the following sentence:

```text
B_d:D_d/D_(d+1) -> K_d is the canonical isomorphism above.  Fixed
echelon and ancestry conventions choose a representative
hat_h_d:K_d -> D_d.  If, and only if, each actual residual is MEMBER,
the six successive representative updates yield one class-specific
filtered correction.  This is not uniform surjectivity and is not by
itself a relative homotopy theorem.
```

## F7. The two R07 extensions and sizes

Use the explicit definitions

\[
 Q_1=Q_0/(1\times G9'),\qquad
 Q_2=Q_0/(1\times(G9')^3).
\]

The pinned structure `G9'=C9^3` gives

\[
 G9'/(G9')^3\cong C3^3,
 \qquad (G9')^3\cong C3^3.
\]

The orders check exactly:

```text
|Q1| = 2016
|Q2| = 2016*27 = 54,432
|Q0| = 54,432*27 = 1,469,664.
```

Thus the first lift is
`1 -> G9'/(G9')^3 -> Q2 -> Q1 -> 1`, and the second is
`1 -> (G9')^3 -> Q0 -> Q2 -> 1`.  Both have six positive grades with
per-transversal multiplicities `(3,6,7,6,3,1)`.

For the first extension, the largest grade has multiplicity 7.  The claimed
coordinate bounds are correct:

\[
 6\cdot2\cdot2016\cdot7=169{,}344,
 \qquad
 2\cdot2\cdot2016\cdot7=56{,}448.
\]

The first is six PB3 occurrences times two regular coordinates; the second
is two physical PB3 blocks times two regular coordinates.  Positive-grade
augmentation scalars and normalized-exponent coordinates add nothing to
these counts.  They are coordinate dimensions, not memory or runtime bounds.

Characteristicity must be an explicit gate.  In `Q0`, `1 x G9` is the
characteristic solvable radical, `1 x G9'` is its characteristic derived
subgroup, and `1 x (G9')^3` is its characteristic power subgroup.  Hence all
five occurrence automorphisms preserve the tower and induce the required
maps on both extensions.  The draft uses this fact but does not include it in
its executable certificate list.

## F8. Missing certificate hypotheses

The transversal and kernel-valued multiplication cocycle are correctly
listed.  So are the quotient action on the kernel, full truncated
`u`-substitutions, crossed occurrence terms, signs, full `g760` prefix
components, normalized exponent in the lower block, and literal ancestry.
The minimum list still needs the following explicit gates:

1. exactness and marked orders of each extension, plus the characteristic
   subgroup equalities just proved;
2. preservation of the kernel and of every `I^d` by all five occurrence
   automorphisms, with their induced quotient maps and crossed cochains;
3. the occurrence-separated semilinear chain-rule/actor identities and the
   fact that a single correlated source actor is used in all six tags;
4. the left-prefix/product convention and the full-extension, not merely
   quotient, values of every fixed prefix;
5. the 44 literal identities and their normal-generation authority at the
   current quotient;
6. the exact PB3 normal map and killing of every translated PB3 boundary
   row, the treatment of the PB4 boundary/block, and commutation of boundary
   reduction, filtration, occurrence transport, and aggregation;
7. normalized exponent divisibility before reduction, its fixed actor action,
   and its inclusion in every lower block; and
8. the base target, coordinate/filtration bases, each canonical residual
   digest, and direct literal replay of every selected update.

The cocycle alone does not establish occurrence semilinearity, and a correct
prefix table alone does not establish boundary killing.  These checks are
load-bearing for either a MEMBER continuation or an upstairs NONMEMBER dual.

## F9. Claim discipline and exact textual repairs

The valid status after the repairs is:

```text
ORDER-2016 RESULT:                 NOT YET COMPUTED
Q1->Q2 RELATIVE ALGORITHM:         PAPER-CLOSED CONDITIONALLY AS SIX FIBRE TESTS
Q2->Q0 RELATIVE ALGORITHM:         PAPER-CLOSED CONDITIONALLY AS SIX FIBRE TESTS
ACTUAL TWISTING DATA / RUNS:       NOT YET MATERIALIZED
UNIFORM GRADE SURJECTIVITY:        NOT CLAIMED
FULL-Q0 CORRECTION:                NOT COMPUTED
A0 / COMMON / COFINAL LIFT:        NOT DECIDED
FAKE / IHARA:                      NOT DECLARED
verified:                          false
```

In particular, replace "The composite of the six successful h_d's is the
desired class-specific relative homotopy" by the F6 text about an iterative
class-specific filtered correction.  Replace every unqualified use of the
tuple in v440 (1.3) by the per-transversal/total distinction in F1.  Replace
the Section 3 actor instruction by the occurrence-first instruction in F4,
and extend the Section 6/7 certificate roster by F8.

The v439 ledger line

```text
PSL504 TRIVIAL FLOOR: CROSS-CHECKED MEMBER; LITERAL PAYLOAD BUILT
```

also exceeds the supplied Task539 status.  Until a durable literal payload is
persisted and replayed, replace it by

```text
PSL504 TRIVIAL FLOOR: CROSS-CHECKED CORE MEMBER; DURABLE LITERAL PAYLOAD PENDING
```

Even if the order-2016 rung later returns MEMBER, the relative construction
may start only from its literal, independently replayed correction.  Six or
twelve successful grade tests would then produce the corresponding finite
coarse correction, not a cofinal compatible lift, fake, or Ihara result.  A
failed-grade dual promotes to an A0 obstruction only after the complete
quotient and boundary-killing chain has been independently rebound.

## Exact input ledger

```text
bytes  sha256                                                            path
3152   798c72ac843a5a5bd18737600df7a9ee5dd45952737d953ae0789b0680f02df9  sol/sol_task_544_audit_r07_a0_relative_fibre_echelon_v1.txt
11049  058972ce33e5289c847d625c2becb182e39e71f9c5cf798235645b0a06b5d338  sol/proof_r07_a0_relative_fibre_echelon_lift_v440.md
21385  3114977ca62727296bf4c3980e405e920169a9c10b4bfdfa80f15990aac3a31d  sol/sol_reply_540_audit_r07_a0_c2fourier_next_rung_v1.md
9111   b18e27ac79f870a6bb5c104a12e85a95daf8644e080153305ce8447e3736f122  sol/proof_r07_a0_c2fourier_joint_lift_v439.md
41174  3512347d86c66de2c14a8c0f659111e465133ca328cc6bb8d7d690ee214b2689  sol/fable_reply_r07_a0_paper_closure_v2_addendum.md
10452  806c0e7015866edc917a9c07c8a3c340a6a5a29c75b751f25b91b534155936b2  sol/proof_r07_compact_extension_presentation_a0_seed_reduction_v397.md
```

RELATIVE_FIBRE_ECHELON_SOUND_AFTER_REPAIR

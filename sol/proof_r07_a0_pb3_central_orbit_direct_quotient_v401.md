# R07 A0 PB3 central-orbit direct boundary quotient (v401)

Author: Sol / 2026-08-30

Status: paper theorem and implementation replacement for the E3 part of the
A0 boundary quotient.  The theorem removes the need to exhaust the PB3
left-translation boundary echelon.  The actual E3 gate and an independent
implementation replay are not yet accepted, so this note does not report an
A0 MEMBER/NONMEMBER terminal, a common word, a compatible lift, a fake, or an
Ihara witness.  `verified=false`.

## 1. The PB3 presentation is a central product presentation

Put

\[
 a=A_{12},\qquad b=A_{13},\qquad c=A_{23},\qquad z=abc.
\tag{1.1}
\]

The two registered `pure_relations(3)` relations say

\[
 a^{-1}ca=bcb^{-1},\qquad
 a^{-1}ba=bcb c^{-1}b^{-1}.
\tag{1.2}
\]

They imply that (z) commutes with both (b) and (c).  Conversely, after
the free-basis substitution

\[
 a=zc^{-1}b^{-1},qquad b=b,qquad c=c,
\tag{1.3}
\]

the two commutation relations ([b,z]=[c,z]=1) imply (1.2).  Hence the
registered presentation is Tietze equivalent to

\[
 PB_3=\langle b,c,z\mid [b,z],[c,z]\rangle
      \cong F(b,c)\times\langle z\rangle.
\tag{1.4}
\]

This is an equality of complete presentations, not an approximation to the
two registered boundary columns.

Let (H) be the actual finite matched E3 image and (k=\mathbf F_3).  Write
the images of (a,b,c,z) by the same letters.  The direct reconstruction from
the frozen q3 receipt currently gives

```text
z = a*b*c
coarse permutation part of z = identity
z != identity
z^3 = identity
```

so the actual specialization has (|\langle z\rangle|=3).  These four finite
equalities are mandatory producer/checker gates; the paper argument below
uses them but does not promote their present one-code calculation to an
accepted numerical receipt.

## 2. The Tietze Fox-coordinate map is sparse

Use left-prefix Fox coordinates, as in the frozen all-seven evaluator.  From
(1.3),

\[
 \delta(zc^{-1}b^{-1})
 =e_z-zc^{-1}e_c-zc^{-1}b^{-1}e_b
 =e_z-ab\,e_c-ae_b.
\tag{2.1}
\]

Therefore a tagged old-coordinate term (h e_a) maps to

\[
 h e_a\longmapsto h e_z-hab\,e_c-ha\,e_b,
\tag{2.2}
\]

while (h e_b\mapsto h e_b) and (h e_c\mapsto h e_c).  Denote this
invertible Fox-Jacobian map by

\[
 J_{\rm T}:k[H]^3_{a,b,c}\longrightarrow k[H]^3_{b,c,z}.
\tag{2.3}
\]

It expands each nonzero (a)-coordinate into only three terms.  Because
(1.3) is a free-basis change, (J_{\rm T}) carries the full translated span
of the two registered PB3 Fox columns onto the full translated span of the
two commutator columns below.

For (h\in H), those columns are

\[
 \begin{aligned}
 d_b(h)&=e_b(h)-e_b(hz)+e_z(hb)-e_z(h),\\
 d_c(h)&=e_c(h)-e_c(hz)+e_z(hc)-e_z(h).
 \end{aligned}
\tag{2.4}
\]

Let (D_3\) be their (k)-span for all (h\in H).

## 3. A closed-form normal map for the quotient by (D_3)

Since (z) is central of order three, partition (H) into the right (or
left) (z)-orbits

\[
 O_r=\{r,rz,rz^2\}.
\tag{3.1}
\]

Choose the least serialized element of each orbit as (r), and order the
orbit as (r,rz,rz^2).  Let a row in the new coordinates be

\[
 v=(B,C,Z)\in k[H]e_b\oplus k[H]e_c\oplus k[H]e_z.
\tag{3.2}
\]

### 3.1 Eliminate the (b,c) orbit differences

On one orbit write (B_i=B(rz^i)).  Put

\[
 \lambda_0=-B_1-B_2,\qquad \lambda_1=-B_2,
 \qquad \lambda_2=0.
\tag{3.3}
\]

Subtracting

\[
 \lambda_0d_b(r)+\lambda_1d_b(rz)
\tag{3.4}
\]

replaces the three (b)-coordinates by

\[
 (B_0+B_1+B_2,0,0)
\tag{3.5}
\]

and makes the corresponding explicitly prescribed update to (Z).  Apply
the same operation to (C), using the columns (d_c).  Call the resulting
third coordinate (Z'\).  This operation touches at most two translated
columns per nonzero orbit and requires no global echelon.

### 3.2 Quotient the remaining constant-orbit differences

For each orbit retain

\[
 \begin{aligned}
 \bar B(r)&=B_0+B_1+B_2,\\
 \bar C(r)&=C_0+C_1+C_2,\\
 U_0(r)&=Z'(r)-Z'(rz^2),\\
 U_1(r)&=Z'(rz)-Z'(rz^2),
 \end{aligned}
\tag{3.6}
\]

and retain one global scalar

\[
 \tau(Z')=\sum_{O_r}Z'(rz^2).
\tag{3.7}
\]

Let

\[
 \Pi_3(v)=\bigl((\bar B(r),\bar C(r),U_0(r),U_1(r))_{O_r},
 \tau(Z')\bigr).
\tag{3.8}
\]

The use of (3.7), rather than the sum of all three coordinates in an orbit,
is essential in characteristic three: the latter vanishes on a nonzero
constant vector.

### Theorem 3.1 (DIRECT PB3 BOUNDARY QUOTIENT)

\[
 \boxed{\ker\Pi_3=D_3.}
\tag{3.9}
\]

Consequently (Pi_3) is a complete, closed-form coordinate map for
(k[H]^3/D_3).  If (q=|H|/3), its target has dimension

\[
 \boxed{4q+1=|H|+|H|/3+1.}
\tag{3.10}
\]

#### Proof

Equations (3.3)--(3.5) subtract elements of (D_3), so every class has a
representative whose (b,c) coordinates occur only at the chosen orbit
representatives.  A linear combination of the three (d_b(rz^i)) has zero
(b)-coordinate precisely when its three coefficients are equal.  Its
remaining (z)-coordinate is then

\[
 N_z(e_z(rb)-e_z(r)),\qquad N_z=1+z+z^2,
\tag{3.11}
\]

and similarly for (c).  Thus the still available relations are exactly
the differences of constant (z)-orbit vectors along the (b,c) Cayley
edges of (H/\langle z\rangle).

The images of (b,c) generate (H/\langle z\rangle), because
(a=zc^{-1}b^{-1}).  Hence that Cayley graph is connected.  Its incidence
image is precisely the space of constant-orbit coefficient families
((s_r)_r) with (sum_r s_r=0).  The two differences in (3.6) kill exactly
the nonconstant part on each orbit, while (3.7) retains exactly the remaining
one-dimensional quotient of the constant part.  Therefore the only rows
killed by (3.8), after the first elimination, are the incidence image
(3.11).  This proves (3.9).  The four coordinates per orbit and the one
global scalar give (3.10). \(\square\)

## 4. The quotient action is also explicit

There is a sparse canonical section (iota_3) of (Pi_3): place
(ar B,ar C,U_0,U_1) at the chosen orbit representatives with the third
orbit coordinate zero, and realize (	au) by adding the constant vector on
the identity orbit.  For (g\in H), define

\[
 \bar L_g=\Pi_3\,L_g\,\iota_3.
\tag{4.1}
\]

Because (D_3) is left invariant, (4.1) is independent of the chosen lift
and is the exact action on (k[H]^3/D_3).  It is computed by one sparse
lift, one left translation, and another application of the local formula
(3.3)--(3.8).  It does not enumerate a boundary orbit or retain a boundary
pivot table.

For every E3 occurrence in v400, the exact hot-path quotient is therefore

\[
 \boxed{\Pi_3J_{\rm T}}
\tag{4.2}

followed by (4.1) for the four source actors.  The occurrence tag remains
separate, so this does not repeat the rejected early aggregation of v390.

## 5. Consequence for the current A0 owner

The first compact-owner GHA run stopped in the B3 boundary closure after

```text
rank   = 211363
cursor = 52992
RSS    = 1142501376 bytes
```

without exhausting that closure.  Theorem 3.1 replaces this entire phase by
the closed-form map (4.2).  In particular:

1. no B3 pivot, frontier, ancestry DAG, or B3 checkpoint is needed;
2. every E3 correction occurrence is quotiented in time proportional to its
   sparse support;
3. the H1/H2 physical B3 residual can be solved by the same local elimination
   plus the connected-orbit incidence construction on the selected final
   residual; and
4. B4 remains unchanged and must still be completed or replaced by its own
   separately proved triangular contraction.

The theorem is lossless for both MEMBER and NONMEMBER.  It is not a heuristic
pruning rule and does not infer a negative result from an unfinished prefix.

## 6. Mandatory finite implementation gates

Before production replacement, producer and helper-nonshared checker must
independently require:

1. the two registered PB3 words are Tietze equivalent to (1.4);
2. the actual matched E3 images satisfy (z\ne1), (z^3=1), and (z) is
   central;
3. (2.2) agrees with direct Fox evaluation on both presentation relators and
   the five registered E3 occurrences;
4. (Pi_3(d_b(h))=Pi_3(d_c(h))=0) on a deterministic bounded set including
   every marked generator translate;
5. `lift -> translate -> Pi3` agrees with full-row translation followed by
   `Pi3`; and
6. a tiny independent finite quotient exhaustively compares `ker(Pi3)` with
   the explicit translated boundary span.

These are bounded algebraic gates.  The actual A0 computation remains GHA
work; no local exhaustive E3 or E4 enumeration is authorized by this note.

```text
PB3 TIETZE CENTRAL FORM:                 PAPER PROOF
PB3 DIRECT QUOTIENT ker(Pi3)=D3:         PAPER PROOF
ACTUAL z ORDER-3 SPECIALIZATION:         ONE-CODE CANDIDATE / REPLAY REQUIRED
211363-RANK B3 CLOSURE:                  REMOVABLE AFTER IMPLEMENTATION GATES
PB4 DIRECT QUOTIENT:                     NOT PROVIDED HERE
ACTUAL A0 MEMBER/NONMEMBER:              NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA WITNESS:  NONE
```

`R07_A0_PB3_CENTRAL_ORBIT_DIRECT_QUOTIENT_V401_PAPER_GRADE`

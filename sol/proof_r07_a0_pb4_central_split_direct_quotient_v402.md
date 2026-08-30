# R07 A0 PB4 central-split direct boundary quotient (v402)

Author: Sol / 2026-08-30

Status: paper theorem and a strict implementation reduction.  It removes five
of the eleven translated PB4 boundary families in closed form and reduces the
remaining six to the centre-free Fadell--Neuwirth factor.  The actual matched
E4 splitting is independently cross-checked by task418.  The six-family
quotient has not been executed.  This note
therefore reports no A0 MEMBER/NONMEMBER terminal, common word, compatible
lift, fake, or Ihara witness.  `verified=false`.

## 1. The exact PB4 presentation has a central direct factor

Use the generator order of the frozen `pure_relations(4)` owner and rename

\[
 a=A_{12},\quad b=A_{13},\quad p=A_{14},\quad
 c=A_{23},\quad q=A_{24},\quad r=A_{34}.
\tag{1.1}
\]

Put

\[
 z_3=abc,\qquad w=pqr,\qquad z=z_3w=abcpqr.
\tag{1.2}
\]

The first two of the eleven registered relations are the PB3 relations.
By v401 they give

\[
 PB_3=\langle b,c,z_3\mid[b,z_3],[c,z_3]\rangle,
 \qquad a=z_3c^{-1}b^{-1}.
\tag{1.3}
\]

The other nine registered relations say that each of (a,b,c) acts on the
free kernel (F(p,q,r)) by its frozen Artin automorphism.  Direct symbolic
evaluation in the same convention gives

\[
\begin{array}{lll}
 \phi_b(p)=prpr^{-1}p^{-1},
 &\phi_b(q)=prp^{-1}r^{-1}qrpr^{-1}p^{-1},
 &\phi_b(r)=prp^{-1},\\[2mm]
 \phi_c(p)=p,
 &\phi_c(q)=qrqr^{-1}q^{-1},
 &\phi_c(r)=qrq^{-1}.
\end{array}
\tag{1.4}
\]

For the product (z_3=abc), the same literal Artin calculation is

\[
 \phi_{z_3}(u)=wuw^{-1}\qquad(u=p,q,r).
\tag{1.5}
\]

Both automorphisms in (1.4) fix (w=pqr).  Equations (1.3)--(1.5) therefore
show that (z=z_3w) commutes with (b,c,p,q,r).  Conversely, eliminating
(z) and then (z_3) recovers the two PB3 relations and all nine frozen
action relations.  Hence the registered presentation is Tietze equivalent
to

\[
\boxed{
 PB_4=\left\langle b,c,p,q,r,z\ \middle|\
 [s,z]\ (s=b,c,p,q,r),\quad
 b^{-1}ub=\phi_b(u),\quad c^{-1}uc=\phi_c(u)\ (u=p,q,r)
 \right\rangle .}
\tag{1.6}
\]

In particular

\[
 PB_4\cong G_0\times\langle z\rangle,
 \qquad
 G_0=F(p,q,r)\rtimes F(b,c),
\tag{1.7}
\]

where (G_0) has five generators and exactly the six action relations in
(1.6).  Thus the eleven boundary families are canonically five central
commutator families plus six centre-free action families; this is not a
heuristic sub-roster.

## 2. The Tietze Fox map is sparse

In the new free basis,

\[
 a=zr^{-1}q^{-1}p^{-1}c^{-1}b^{-1}.
\tag{2.1}
\]

For the frozen left-prefix Fox convention,

\[
\begin{aligned}
 \delta(a)={}&e_z-zr^{-1}e_r-zr^{-1}q^{-1}e_q
 -zr^{-1}q^{-1}p^{-1}e_p\\
 &-zr^{-1}q^{-1}p^{-1}c^{-1}e_c
 -zr^{-1}q^{-1}p^{-1}c^{-1}b^{-1}e_b.
\end{aligned}
\tag{2.2}
\]

The other five old generator coordinates map identically to their renamed
coordinates.  Therefore the Fox Jacobian (J_4) from the old six coordinates
to ((b,c,p,q,r,z)) expands one old (a)-term into at most six terms.  Since
(2.1) is a free-basis change and (1.6) is a Tietze equivalence, (J_4)
carries the full translated span of the registered eleven Fox columns onto
the full translated span of the eleven columns in (1.6).

## 3. The actual matched E4 has a cross-checked split central three-cycle

Let (H) be the actual matched E4 image and let (zeta) be the image of
the literal word (z=abcpqr).  The task418 replay from the frozen q3 receipt,
without importing the producer-side reconstruction, gives

```text
coarse permutation part of zeta = identity
zeta != identity
zeta^3 = identity
zeta commutes with all six marked generators
```

The PC factor is the class-two exponent-three group of order (3^{10}).
Its six marked generators have the first six independent abelian PC
coordinates.  In those coordinates the new noncentral generators
((b,c,p,q,r)) all have first coordinate zero, while

```text
pc(zeta) = (1,1,1,1,1,1,0,0,0,0).
```

Let (kappa:H\to\mathbf F_3) be the first PC coordinate and set

\[
 H_0=\ker\kappa.
\tag{3.1}
\]

The triangular PC multiplication laws make (kappa) a homomorphism.  The
five noncentral images generate a subgroup contained in (H_0), while they
together with (zeta) generate (H).  Since (kappa(zeta)=1), this gives

\[
\boxed{H=H_0\times\langle\zeta\rangle,\qquad |\langle\zeta\rangle|=3.}
\tag{3.2}
\]

Task418 checks (3.2) independently from the pinned PC and coarse
multiplication tables, including all PC presentation relations and the
source identity expressing (a) through (zeta,b,c,p,q,r).  A production owner
must require that accepted certificate and must not infer the split merely
from the four displayed booleans.

The split supplies a canonical, enumeration-free orbit coordinate.  For
each (h\in H), put (j=\kappa(h)\in\{0,1,2\}) and

\[
 h_0=h\zeta^{-j}\in H_0,
 \qquad h=h_0\zeta^j.
\tag{3.3}
\]

No subgroup BFS or word solve is needed.

## 4. Closed contraction of all five central boundary families

Let (k=\mathbf F_3), (A_0=k[H_0]), and

\[
 A=k[H]=A_0\otimes k[\langle\zeta\rangle],
 \qquad N=1+\zeta+\zeta^2.
\tag{4.1}
\]

In the new coordinates write

\[
 C_4=A^5\oplus Ae_z.
\tag{4.2}
\]

Let \(D_{\rm cen}\) be the span of all translates of the five commutator
columns ([s,z]), and let (D_0\le A_0^5) be the span of all (H_0)-translates
of the six action-relation Fox columns of (G_0).

For a coefficient (v\in A), the translated central commutator boundary is,
up to the common frozen sign convention,

\[
 v(1-\zeta)e_s+v(s-1)e_z.
\tag{4.3}
\]

The image of (1-\zeta) on each three-point orbit is the sum-zero plane,
and its kernel is (NA_0).  Thus every row (X=(S,Z)\in A^5\oplus A) can be
reduced by (4.3) so that (S\in A_0^5).  If (V_i) is the explicitly chosen
orbitwise solution of

\[
 S_i-S_i^{(0)}=(1-\zeta)V_i,
\tag{4.4}
\]

the simultaneously corrected last coordinate is

\[
 Z'=Z-\sum_iV_i(s_i-1).
\tag{4.5}
\]

Changing (V_i) by (NW_i) changes (Z') by
(N\sum_iW_i(s_i-1)).  Since the five (s_i) generate (H_0), their
((s_i-1))-span is the augmentation ideal (I_0\le A_0).  Consequently

\[
\boxed{C_4/D_{\rm cen}\cong A_0^5\oplus A/(NI_0).}
\tag{4.6}
\]

This isomorphism is constructive.  In each orbit
({h_0,h_0\zeta,h_0\zeta^2}), use the same two-step elimination as v401;
retain two differences of (Z'), and retain one global scalar from its
constant-orbit part.  Equivalently,

\[
 A/(NI_0)\cong
 \bigl(A_0\otimes(k[C_3]/kN)\bigr)\oplus k
\tag{4.7}
\]

as (k)-spaces, so this explicit survivor has dimension (2|H_0|+1).

### Theorem 4.1 (PB4 CENTRAL-SPLIT DIRECT QUOTIENT)

Under the split gate (3.2), the full registered PB4 boundary quotient is

\[
\boxed{
 C_4/D_4\cong
 \bigl(A_0^5/D_0\bigr)\oplus A/(NI_0).}
\tag{4.8}
\]

#### Proof

Equation (4.6) quotients exactly the five central commutator families.  The
six remaining relators contain only (b,c,p,q,r).  Their literal prefixes
therefore evaluate in (H_0), so their unshifted Fox columns contract to
((D_0,0)).  A (zeta)-translate of such a column differs from its
unshifted copy by (4.3) applied to that Fox column: the (e_z)-term is zero
because the Fox boundary identity is (d_1d_2=0).  Hence all (H)-translates
of the six rows have image exactly (D_0\oplus0) in (4.6).  Quotienting by
that image proves (4.8).  Conversely every operation used above is a literal
linear combination of one of the registered eleven translated columns, so
the kernel is no larger than (D_4).  This proves equality. \(\square\)

If (d_0=\dim_k(A_0^5/D_0)), then

\[
 \dim_k(C_4/D_4)=d_0+2|H_0|+1.
\tag{4.9}
\]

No numerical value of (d_0) is asserted here.

## 5. Exact effect on the A0 owner

After the independent split gates, every E4 occurrence can be processed as
follows.

1. Apply the six-sparse Tietze Fox map (J_4).
2. Use the first PC coordinate (3.3) to separate every support key into its
   (H_0) representative and its central exponent.
3. Apply the fixed three-point formula (4.4)--(4.5).  This removes all five
   central commutator boundary families without a pivot, orbit enumeration,
   frontier, or checkpoint.
4. If either the two-per-(H_0) (Z')-difference part or the global scalar
   fails to match, it is already an exact separator: the remaining six
   boundaries cannot change it.
5. Run lazy dual column generation only for the six (G_0) action relators
   on the (A_0^5/D_0) component.  Positive ancestry for those six rows is
   retained as before.  The five central preimage families are reconstructed
   directly from the stored (V_i) in (4.4).

Thus v402 does **not** replace one large PB4 closure by another preliminary
closure.  It deletes five of eleven translated families and one central
three-cycle from the live problem.  It is compatible with the v400
occurrence quotient because the contraction is performed separately in
every E4 tag before physical aggregation.

The durable task416 checkpoint is in the old uncontracted coordinates.
Transforming all of its pivots and ancestry would itself be a substantial
operation.  Therefore the current exact resume should continue unchanged;
v402 is the strict fallback/replacement if that continuation remains a
resource frontier.  A fresh v402 owner must not silently call the old
checkpoint a quotient checkpoint.

```text
PB4 TIETZE SPLIT INTO 5 CENTRAL + 6 ACTION RELATIONS: PAPER PROOF
SPARSE OLD-TO-NEW FOX MAP:                              PAPER PROOF
ACTUAL E4 CENTRAL C3 SPLIT:                             CROSS-CHECKED / verified=false
FIVE CENTRAL BOUNDARY FAMILIES:                         CLOSED-FORM QUOTIENT
SIX G0 ACTION BOUNDARY FAMILIES:                        STILL AN EXACT FINITE GATE
ACTUAL A0 MEMBER/NONMEMBER:                             NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA WITNESS:                 NONE
```

`R07_A0_PB4_CENTRAL_SPLIT_DIRECT_QUOTIENT_V402_PAPER_GRADE`

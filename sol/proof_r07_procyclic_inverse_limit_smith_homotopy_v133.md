# R07 procyclic inverse-limit Smith homotopy v133

Author: Sol / 2026-08-27

Status: paper theorem.  This note gives a genuinely all-scale version of the
v129--v131 cyclic selector.  If the cyclic refinement systems are the base
changes of one finite matrix over the completed group ring, one Smith
reduction over that completed ring constructs a continuous class-specific
homotopy and hence all compatible finite corrections at once.  The required
R07 base-change identification and its actual Smith data have not yet been
computed.  The first all-seven word and the nonabelian chief gates also remain
open.  No cofinal lift, fake, or Ihara witness is declared.

## 1. The load-bearing base-change hypothesis

Let (k) be a field of characteristic (p), put

\[
 \Lambda=k[[T]],\qquad
 \Lambda_a=\Lambda/(T^{p^a}).
\tag{1.1}
\]

After choosing compatible generators, \(\Lambda_a\) is the group ring
\(k[C_{p^a}]\), with \(T=g-1\).  The transition
\(\Lambda_{a+1}\twoheadrightarrow\Lambda_a\) has kernel

\[
 (T^{p^a})/(T^{p^{a+1}}),
\tag{1.2}
\]

as in v131.  The inverse limit of these rings is \(\Lambda\).

Assume there are finite free, separated, complete \(\Lambda\)-modules

\[
 A=\Lambda^m,\qquad Z=\Lambda^n,
\tag{1.3}
\]

a continuous \(\Lambda\)-linear map \(B:A\to Z\), and a target \(z\in Z\),
such that every typed cyclic R07 system is exactly the base change

\[
 A_a=A/T^{p^a}A,\quad
 Z_a=Z/T^{p^a}Z,\quad
 B_a=B\bmod T^{p^a},\quad
 z_a=z\bmod T^{p^a}.
\tag{1.4}
\]

This is stronger than merely having matrices of the same dimensions at all
levels.  Markings, occurrence order, presentation boundaries, normal
generator coordinates, and the target must all commute with (1.4).  If this
comparison is absent, the theorem below must not be applied; v131's
stage-by-stage Tor selector remains the valid fallback.

## 2. One Smith reduction over the inverse limit

The ring \(\Lambda=k[[T]]\) is a discrete valuation ring.  Therefore there
are invertible matrices

\[
 U\in\operatorname{GL}_n(\Lambda),\qquad
 V\in\operatorname{GL}_m(\Lambda)
\tag{2.1}
\]

and uniquely determined finite exponents

\[
 0\leq\alpha_1\leq\cdots\leq\alpha_r,
 \qquad r\leq\min(m,n),
\tag{2.2}
\]

such that

\[
 \boxed{UBV=\operatorname{diag}
 (T^{\alpha_1},\ldots,T^{\alpha_r},0).}
\tag{2.3}
\]

Write \(w=Uz\).

### Theorem 2.1 (PROCYCLIC INVERSE-LIMIT SMITH SELECTOR)

The following are equivalent.

1. There is an inverse-limit solution \(a\in A\) with \(Ba=z\).
2. There is a compatible family \((a_a)_a\) satisfying
   \(B_aa_a=z_a\) and \(a_{a+1}\mapsto a_a\).
3. The transformed target satisfies

   \[
    \boxed{
    w_i\in T^{\alpha_i}\Lambda\ (1\leq i\leq r),
    \qquad w_i=0\ (r<i\leq n).}
   \tag{2.4}
   \]

When these conditions hold, define

\[
 b_i=T^{-\alpha_i}w_i\quad(1\leq i\leq r),
 \qquad b_i=0\quad(i>r),
\tag{2.5}
\]

and put

\[
 \boxed{a=Vb.}
\tag{2.6}
\]

Then \(a_a=a\bmod T^{p^a}\) is a deterministic compatible solution at
every cyclic scale.  A failed coordinate in (2.4) is an exact
inverse-limit separator.

#### Proof

If \(a=Vb\), then \(Ba=z\) is equivalent, after multiplication by \(U\),
to

\[
 \operatorname{diag}(T^{\alpha_1},\ldots,T^{\alpha_r},0)b=w.
\tag{2.7}
\]

This equation is solvable exactly under (2.4), and (2.5)--(2.6) give a
solution.  Its reductions give condition 2.  Conversely, a compatible
family defines an element of

\[
 A\cong\varprojlim_a A_a
\tag{2.8}
\]

because \(A\) is complete and separated.  Passing to the inverse limit in
the displayed finite equations gives \(Ba=z\), proving condition 1.
Finally, if (2.4) fails, projection to the failed Smith cokernel coordinate
is zero on \(\operatorname{im}B\) and nonzero on \(z\). \(\square\)

The division in (2.5) is division inside the principal ideal
\(T^{\alpha_i}\Lambda\); it is not division by a unit and does not leave
the completed ring.

## 3. The continuous class-specific homotopy

For any \(y\in\operatorname{im}B\), repeat (2.5) with \(Uy\) in place of
\(w\), and define

\[
 h_B(y)=V
 \bigl(T^{-\alpha_1}(Uy)_1,\ldots,
       T^{-\alpha_r}(Uy)_r,0,\ldots,0\bigr).
\tag{3.1}
\]

### Proposition 3.1 (ONE HOMOTOPY FOR ALL REFINEMENTS)

The map

\[
 \boxed{h_B:\operatorname{im}B\longrightarrow A}
\tag{3.2}
\]

is continuous and \(\Lambda\)-linear, and

\[
 \boxed{Bh_B=\operatorname{id}_{\operatorname{im}B}.}
\tag{3.3}
\]

Its reductions are mutually compatible right inverses on the actual image.
Thus, for a named compatible defect \(\beta=(\beta_a)\) in the image,

\[
 \boxed{c_\infty=-h_B(\beta)}
\tag{3.4}
\]

is one inverse-limit correction whose reductions correct every cyclic
refinement.  No independent choices of \(c_a\) are made.

#### Proof

Multiplication by \(T^{\alpha_i}\) is a homeomorphism
\(\Lambda\to T^{\alpha_i}\Lambda\), so its inverse on that ideal is
continuous.  The matrices \(U,V\) and all coordinate projections are
continuous.  Equation (3.3) follows from (2.3), and reduction commutes with
every operation in (3.1). \(\square\)

This is the precise inverse-limit form of the proposed relative A.18
homotopy.  It is class-specific because its domain is the actual image, not
all of \(Z\).  Surjectivity of \(B\), a splitter on the complete ambient
module, and independent finite-stage selectors are unnecessary.

## 4. The augmented relative selector and its exact filtration loss

The v129 correction step uses

\[
 C:A\oplus\Lambda\longrightarrow Z,
 \qquad C(d,\rho)=Bd+\rho z.
\tag{4.1}
\]

Apply Smith reduction once to this matrix:

\[
 U_CCV_C=operatorname{diag}
 (T^{\gamma_1},\ldots,T^{\gamma_s},0).
\tag{4.2}
\]

It gives a continuous right inverse \(h_C\) on \(M_z=\operatorname{im}C\)
exactly as in (3.1).  Unlike an arbitrary right inverse, its filtration loss
is explicit.

### Theorem 4.1 (FILTERED ACTUAL-CLASS HOMOTOPY)

Let \(e\in M_z\), write \(v=U_Ce\), and let \(N\geq0\).  There is a
preimage

\[
 (d,\rho)\in T^N(A\oplus\Lambda),
 \qquad C(d,\rho)=e,
\tag{4.3}
\]

if and only if

\[
 \boxed{
 v_i\in T^{N+\gamma_i}\Lambda\ (1\leq i\leq s),
 \qquad v_i=0\ (i>s).}
\tag{4.4}
\]

When (4.4) holds, \((d,\rho)=h_C(e)\) is such a preimage.  Hence, for the
edge

\[
 \Lambda/(T^q)\twoheadrightarrow\Lambda/(T^N),
 \qquad N<q,
\tag{4.5}
\]

the exact truncated criterion is

\[
 \boxed{
 \nu(v_i)\geq\min(q,N+\gamma_i)
 \quad(1\leq i\leq s),}
\tag{4.6}
\]

together with vanishing of every zero-row coordinate modulo \(T^q\).

#### Proof

In Smith coordinates, every pivot equation is

\[
 T^{\gamma_i}b_i=v_i.
\tag{4.7}
\]

Requiring \(b_i\in T^N\Lambda\) is exactly (4.4).  The nonpivot domain
coordinates do not change the zero-row equations.  Reducing the same
statement modulo \(T^q\) replaces every valuation threshold by its
truncation at \(q\), proving (4.6). \(\square\)

For \(N=p^a\) and \(q=p^{a+1}\), (4.6) is v131's actual-class valuation
test, now obtained from one invariant list \((\gamma_i)\) for the complete
tower.  If all \(\gamma_i=0\) on the nonzero rows, every actual error in
\(M_z\cap T^NZ\) lifts automatically.  If some \(\gamma_i>0\), arbitrary
strictness fails, but a named R07 error can still pass (4.6).

When (4.4) holds for the lifted error

\[
 e=B\widehat a-z,
\tag{4.8}
\]

v129 gives the literal next solution

\[
 \boxed{a'=(1+\rho)^{-1}(\widehat a-d).}
\tag{4.9}
\]

Because \(\rho\in T^N\Lambda\), the inverse is the convergent geometric
series in \(\Lambda\), and its reductions are the finite nilpotent inverses
used in v129.

## 5. Dihedral-odd plus field-outer-even

Assume \(p\ne2\), an involution \(\theta\) acts continuously on \(A,Z\),
and \(B\theta=\theta B\).  Put

\[
 e_-=(1-\theta)/2,\qquad e_+=(1+\theta)/2.
\tag{5.1}
\]

Then \(A=A_-\oplus A_+\), \(Z=Z_-\oplus Z_+\), and \(B=B_-\oplus B_+\).

### Corollary 5.1 (RELATIVE DIHEDRAL--SMITH HOMOTOPY)

Suppose the established dihedral argument supplies a continuous right
inverse \(h_-\) on the required return-odd image, and the actual return-even
class satisfies the Smith criterion (2.4) for \(B_+\).  Then

\[
 \boxed{h=h_-e_-+h_{B_+}e_+}
\tag{5.2}
\]

is one continuous class-specific right inverse on the sum of those actual
classes.  In particular, a return-even survivor is not killed by pretending
that \(1-\theta\) is surjective; it is divided in its genuine Smith
coordinate instead.

#### Proof

The two idempotent summands are complementary and preserved by \(B\).
Each term of (5.2) is a right inverse on its stated image, so their direct
sum is a right inverse there.  Continuity follows from Proposition 3.1 and
the continuity of the idempotents. \(\square\)

This is the sound generalization of the pure dihedral lift.  It asks only
for the named field-outer class, not for vanishing of the complete
return-even cokernel.

## 6. What must be authenticated for R07

After one exact all-seven correction word has been produced, promotion of
v133 requires the following finite receipt.

1. Bind a single completed cyclic parameter \(T\) and prove that every
   finite transition ideal is exactly (1.2).
2. Bind one completed all-seven source module, target module, matrix \(B\),
   target \(z\), and all PB3/PB4 boundary coordinates.
3. Prove the complete base-change squares (1.4), including the literal five
   A.18 cofaces and both exponent coordinates.
4. Compute \(U,V,(\alpha_i)\) for \(B\), or
   \(U_C,V_C,(\gamma_i)\) for the augmented map \(C\), with replayable
   elementary row and column operations.
5. Transform the named R07 target/error and run (2.4) or (4.6).
6. Materialize the power-series coefficient vector as compatible finite
   words and replay both hexagons and the printed-order pentagon at every
   requested quotient.

Items 1--3 are logical hypotheses, not consequences of equal matrix sizes
or matching hashes.  If the cyclic modules change by more than base change,
the one-shot Smith list is invalid and v131 must be run on each typed edge.

Nonabelian chief refinements do not become cyclic merely because (1.1) is
available.  Their accepted-set nonemptiness and side gates remain separate.

## 7. Consequence for the witness route

For the row-36/R07 branch, the resulting order of work is now exact.

1. Construct one common all-seven finite word using v132.
2. Solve its fixed-context augmented \((d,\rho)\) equation by v129.
3. Test whether the cyclic tower satisfies the base-change hypothesis
   (1.4).
4. If it does, run one completed Smith reduction and use (3.4) or (4.9) for
   every cyclic refinement; if it does not, use v131 at the first failed
   typed edge.
5. Interleave the separately authenticated nonabelian accepted-set choices.
6. The compatible inverse-limit point is a fake candidate only after its
   row-36 projection and all GT/Ihara side conditions are replayed.

Thus the all-scale selector is mathematically available under one concrete
base-change gate.  The theorem does not infer that gate, the Smith
divisibility of the actual R07 class, or the first all-seven word.

```text
COMPLETED CYCLIC RING AS k[[T]]:              PAPER_PROOF
ONE-SMITH ALL-SCALE SELECTOR:                 PAPER_PROOF
CONTINUOUS ACTUAL-IMAGE HOMOTOPY:             PAPER_PROOF
FILTERED AUGMENTED (d,rho) SELECTOR:          PAPER_PROOF
DIHEDRAL-ODD + SMITH-EVEN GLUING:             PAPER_PROOF
R07 COMPLETED BASE-CHANGE SQUARES:            NOT AUTHENTICATED
R07 COMPLETED SMITH DATA / TARGET TEST:        NOT COMPUTED
FIRST EXACT ALL-SEVEN WORD:                   NOT YET CONSTRUCTED
NONABELIAN ACCEPTED SETS:                     OPEN
COMPATIBLE COFINAL R07 LIFT:                  NOT CONSTRUCTED
FAKE / IHARA WITNESS:                         NOT DECLARED
```

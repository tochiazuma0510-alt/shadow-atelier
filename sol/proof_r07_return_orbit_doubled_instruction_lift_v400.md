# R07 return-orbit doubled instruction lift v400

Author: Sol / 2026-08-30

Status: paper theorem after v77, v397, and v399.  It removes two stronger
premises from the class-specific explicit-lift route.  One need not first
serialize an involution on the physical residual target, and one need not
prove separately that the Fox value term is odd and the connection term is
even.  On a return-closed diagram, double the literal relation evaluation by
its returned evaluation.  The doubled linear operator is equivariant by
construction, and every solution has a return-fixed average.  The remaining
actual gate is the direct image of the return-symmetric instruction, together
with its legality and its identification with the actual \(\chi_{07}\)
defect.  Those actual gates are not proved here.  No compatible R07 lift,
fake certificate, or Ihara witness is declared.  `verified=false`.

## 1. Work at the fixed return midpoint

Let \(k\) be a field in which \(2\) is invertible.  At one elementary
abelian diagram-chief edge, let

\[
 \mathcal A=a_0+D^{\rm rel}                              \tag{1.1}
\]

be the affine space of physically legal relative corrections.  All marking,
unit, boundary, exponent-zero, formation, and already imposed side
conditions are included in \(D^{\rm rel}\).  Suppose the canonical return is
an affine involution

\[
 R(a_0+d)=a_0+\delta+\theta d,
 \qquad \theta^2=1,
 \qquad \theta\delta=-\delta,                            \tag{1.2}
\]

where \(\theta\) preserves \(D^{\rm rel}\).  Put

\[
 a_+=a_0+\frac12\delta.                                  \tag{1.3}
\]

Then \(R(a_+)=a_+\), and relative to this fixed base

\[
 R(a_++d)=a_++\theta d.                                  \tag{1.4}
\]

Let the complete literal relation residual at this abelian layer be the
affine map

\[
 F(a_++d)=\beta_++Bd,
 \qquad B:D^{\rm rel}\longrightarrow Q.                 \tag{1.5}
\]

Here \(Q\) may retain the two hexagons, all five ordered A.18 occurrences,
normalization rows, and boundary localization as separately tagged
coordinates.  We do **not** assume an involution on \(Q\), nor the identity
\(B\theta=\theta_QB\).

The only return hypothesis on the residual is the intrinsic one:

\[
 \boxed{R(F^{-1}(0))=F^{-1}(0).}                         \tag{1.6}
\]

For the actual GT relation map this says simply that applying complex
conjugation/return to a genuine solution gives another genuine solution.
V77 Theorem 2.5 shows that the original diagram ladder may be replaced
cofinally by return-closed isolated diagrams, so imposing (1.2) and (1.6)
does not shrink the inverse-limit problem.

## 2. Orbit doubling makes equivariance tautological

Define the orbit-doubled residual

\[
 F^{\rm orb}(a)=\bigl(F(a),F(Ra)\bigr)\in Q\oplus Q.     \tag{2.1}
\]

At the fixed base (1.3), equations (1.4)--(1.5) give

\[
 F^{\rm orb}(a_++d)
 =\bigl(\beta_++Bd,\ \beta_++B\theta d\bigr).            \tag{2.2}
\]

Thus its linear part is

\[
 \boxed{B^{\rm orb}d=(Bd,B\theta d).}                   \tag{2.3}
\]

Let \(s:Q\oplus Q\to Q\oplus Q\) exchange the two factors.  Then

\[
 \boxed{B^{\rm orb}\theta=sB^{\rm orb}}                 \tag{2.4}
\]

holds by direct substitution, with no target-action matrix and no common
group-ring action on the eleven occurrences.

Moreover (1.6) gives the equality of zero loci

\[
 \boxed{(F^{\rm orb})^{-1}(0)=F^{-1}(0).}                \tag{2.5}
\]

Indeed, the left-to-right implication is immediate.  Conversely, if
\(F(a)=0\), return stability gives \(F(Ra)=0\).

### Theorem 2.1 (RETURN-ORBIT DOUBLING)

Under (1.2), (1.5), and (1.6), the following are equivalent:

1. there is \(d\in D^{\rm rel}\) with \(F(a_++d)=0\);
2. \((-\beta_+,-\beta_+)\in B^{\rm orb}(D^{\rm rel})\);
3. there is a return-fixed \(d_+\in D^{\rm rel}\) with
   \(\theta d_+=d_+\) and \(Bd_+=-\beta_+\).

Equivalently, with

\[
 D^{\rm rel,+}=\ker(\theta-1),                           \tag{2.6}
\]

the exact finite gate is

\[
 \boxed{-\beta_+\in B(D^{\rm rel,+}).}                  \tag{2.7}
\]

#### Proof

Suppose \(Bd=-\beta_+\).  Then \(F(a_++d)=0\), so (1.6) and
(1.4) give

\[
 F(a_++\theta d)=0,
 \qquad B\theta d=-\beta_+.                             \tag{2.8}
\]

Hence \(B^{\rm orb}d=(-\beta_+,-\beta_+)\), proving
1 \(\Rightarrow\) 2.  The first coordinate gives 2 \(\Rightarrow\) 1.
Now average the two solutions:

\[
 \boxed{d_+=\frac12(d+\theta d).}                       \tag{2.9}
\]

It lies in \(D^{\rm rel,+}\), and (2.8) gives
\(Bd_+=-\beta_+\).  This proves 1 \(\Rightarrow\) 3;
3 \(\Rightarrow\) 1 is immediate.  Formula (2.7) is statement 3. \(\square\)

Over \(\mathbf F_3\), the explicit averaging formula is

\[
 \boxed{d_+=2(d+\theta d).}                              \tag{2.10}
\]

Thus return closure reduces the legal source to its fixed subspace; it does
not add a second independent relation solve.

## 3. Literal instruction form

Let \(U^{\rm rel}\) be the free space on the occurrence-tagged legal
instruction trees of v397, with evaluation

\[
 e:U^{\rm rel}\to D^{\rm rel}.                          \tag{3.1}
\]

Close the roster under literal return.  Return reverses every product,
commutes with inversion, applies the canonical return to every actor and
correction leaf, and uses the reversed A.18 factor order of v77 Proposition
2.4.  Structural evaluation gives

\[
 e(\theta_Uu)=\theta e(u).                               \tag{3.2}
\]

For any instruction \(u\), put

\[
 u_+=\frac12(u+\theta_Uu),
 \qquad e(u_+)=\frac12\bigl(e(u)+\theta e(u)\bigr).      \tag{3.3}
\]

### Corollary 3.1 (DIRECT SYMMETRIC-INSTRUCTION CERTIFICATE)

If direct literal replay proves

\[
 \boxed{B e(u_+)=-\beta_+,}                              \tag{3.4}
\]

then \(e(u_+)\) is a legal return-fixed correction of the complete actual
residual.  Its certificate is just the pair of literal trees
\((u,\theta_Uu)\), their legality/reduction replay, and equality (3.4).

For a commutator instruction \(c=e(u)\), v398 writes

\[
 Bc=V+K.                                                  \tag{3.5}
\]

The present route requires only

\[
 B\frac12(c+\theta c)
 =\frac12(Bc+B\theta c)=-\beta_+.                        \tag{3.6}

It does **not** require the two stronger identities

\[
 \theta_QV=-V,
 \qquad \theta_QK=K.                                     \tag{3.7}

Consequently v399 remains a valid shortcut when its typed parity hypotheses
are available, but separate value-odd/connection-even authentication is not
a prerequisite for the actual class-specific lift.  Any mixing between the
two Fox summands is retained automatically in the two literal evaluations in
(3.6).

## 4. Compatible all-refinement form

Let the return-closed cofinal tower carry compatible affine returns and
reductions.  Suppose a compatible raw base history gives compatible
midpoints \(a_{+,n}\), defects \(\beta_{+,n}\), and source involutions
\(\theta_n\).  Then

\[
 r_DD^{\rm rel,+}_{n+1}\subseteq D^{\rm rel,+}_n.        \tag{4.1}
\]

If one compatible literal instruction history \(u=(u_n)\) satisfies

\[
 B_ne_n\!\left(\frac12(u_n+\theta_{U,n}u_n)\right)
 =-\beta_{+,n}\qquad\text{for every }n,                 \tag{4.2}
\]

then

\[
 d_{+,n}=e_n\!\left(\frac12(u_n+\theta_{U,n}u_n)\right) \tag{4.3}
\]

is one compatible correction on all refinements.  Compatibility follows
directly because reduction commutes with literal return, evaluation, and
the scalar \(1/2\).

Let \(U^{\rm rel,+}=\ker(\theta_U-1)\).  For a whole closed defect space
\(C^+\), a continuous **word-bearing** selector follows from the strict
instruction-image condition

\[
 \boxed{
 Be(\mathcal F^rU^{\rm rel,+})=\mathcal F^rC^+
 \quad\text{for every }r.}                               \tag{4.4}
\]

Apply the strict filtered section lemma of v357 to the restriction of
\(Be\) in (4.4), and compose its instruction section with \(e\), as in
v397.  For the single \(\chi_{07}\) history, the pointwise identity (4.2)
is enough; no global target-module section is required.

## 5. Exact effect on the R07 frontier

The cofinal return closure and orbit doubling replace the following two
v399 execution gates:

```text
serialized target involution and B theta_D = theta_L B
separate actual replay theta_L V=-V and theta_L K=K
```

by the smaller direct certificate:

```text
return-closed legal instruction pair (u, return(u))
direct evaluations B e(u) and B e(return(u))
symmetric equality B e((u+return(u))/2) = -beta_plus
compatible reduction of that literal pair
```

The first two displayed v399 gates are therefore not intrinsic mathematical
obstructions.  The remaining symmetric image equality is still substantive:
orbit doubling does not put an arbitrary even defect in the instruction
image.  A0 must supply the initial actual word/instruction, A4 must supply
the legal word-bearing relative source, and the actual \(\chi_{07}\) defect
must be bound to (3.6) or otherwise solved in \(B(D^{\rm rel,+})\).

```text
RETURN-CLOSED COFINAL REFINEMENT:                   v77 PAPER PROOF
ORBIT-DOUBLED EQUIVARIANCE:                         PAPER PROOF HERE
EVERY SOLUTION HAS RETURN-FIXED AVERAGE:            PAPER PROOF HERE
SEPARATE VALUE/CONNECTION PARITY REQUIRED:           NO FOR CLASS-SPECIFIC ROUTE
ACTUAL SYMMETRIC INSTRUCTION IMAGE EQUALITY:         OPEN
LEGAL A4 RETURN-CLOSED WORD ROSTER:                  OPEN / RUNNING
INITIAL A0 ACTUAL WORD:                              OPEN / RUNNING
STRICT ALL-DEPTH FIXED-SOURCE COVER:                 OPEN
COMPATIBLE R07 LIFT / FAKE / IHARA WITNESS:          NOT CONSTRUCTED
```

`R07_RETURN_ORBIT_DOUBLED_INSTRUCTION_LIFT_V400_PAPER_GRADE`

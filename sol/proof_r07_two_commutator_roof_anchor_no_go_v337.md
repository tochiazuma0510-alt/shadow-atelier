# R07 two-commutator roof/anchor incompatibility (v337)

Author: Sol / 2026-08-29

Status: paper no-go theorem for the complete literal family
\([x,y]^A[y,z]^B\).  A member of this family which has the same
pure-dihedral \(Q=36\) roof as \(\chi_{07}\) is necessarily trivial in the
first exponent-nine projected kernel.  Hence this family cannot supply the
nonzero A4 anchor required by v247, although its deeper Fox norm columns from
v336 may still be useful.  No claim is made about arbitrary words in the
actual roof kernel.  No milestone numerator, lift, fake certificate or Ihara
witness is declared.  `verified=false`.

## 1. The complete two-commutator family

Fix the literal convention used by the dihedral section, put

\[
 h=[x,y],\qquad k=[y,z],\qquad z=y^{-1}x^{-1},
\tag{1.1}
\]

and define

\[
 \chi_{A,B}=h^Ak^B
\qquad(A,B\in\mathbf Z).
\tag{1.2}
\]

The R07 core is

\[
 \chi_{07}=\chi_{1,-1}=hk^{-1}.
\tag{1.3}
\]

The literal dihedral formula of v5 applies with

\[
 k_{\rm dih}=A-B,\qquad t=-(A+B),
\tag{1.4}
\]

and gives

\[
 \boxed{
 \psi_Q(\chi_{A,B})
 =
 \bigl(
 r^{\,2(A-B)},
 r^{-2(A-B)},
 r^{-2(A+B)}
 \bigr).}
\tag{1.5}
\]

For \((A,B)=(1,-1)\), this is

\[
 \psi_Q(\chi_{07})=(r^4,r^{-4},1).
\tag{1.6}
\]

## 2. Exact same-roof congruences

### Lemma 2.1 (R07 PURE-DIHEDRAL ROOF FIBRE)

At \(Q=36\),

\[
 \boxed{
 \psi_{36}(\chi_{A,B})=\psi_{36}(\chi_{07})
 \quad\Longleftrightarrow\quad
 \begin{cases}
 A-B\equiv2\pmod{18},\\
 A+B\equiv0\pmod{18}.
 \end{cases}}
\tag{2.1}
\]

#### Proof

Equality of the first rotation in (1.5) and (1.6) is

\[
 2(A-B)\equiv4\pmod{36},
\]

which is the first congruence.  Equality of the third rotation is

\[
 -2(A+B)\equiv0\pmod{36},
\]

which is the second.  The second coordinate is equivalent to the first.
\(\square\)

Writing

\[
 A=1+\delta_A,\qquad B=-1+\delta_B,
\tag{2.2}
\]

the same conditions are

\[
 \delta_A-\delta_B\equiv0\pmod{18},
\qquad
 \delta_A+\delta_B\equiv0\pmod{18}.
\tag{2.3}
\]

In particular, \(\delta_A\) and \(\delta_B\) are multiples of nine with
the same parity after division by nine.

## 3. The exponent-nine projection sees only the area sum

Let

\[
 q:F(x,y)\longrightarrow D_1=\mathcal H_2(9)
\tag{3.1}
\]

be the frozen class-two exponent-nine quotient of v210--v216.  In a
class-two group the commutator is alternating bilinear.  Since
\(z=y^{-1}x^{-1}\),

\[
 \boxed{q([y,z])=q([x,y]).}
\tag{3.2}
\]

Indeed, in the associated additive class-two commutator coordinate,

\[
 [Y,-Y-X]=[X,Y].
\tag{3.3}
\]

The same equality follows directly from the class-two commutator identities
in either of the two historical word conventions used in the repository.
Put

\[
 \bar h=q(h)=q(k).
\tag{3.4}
\]

Then

\[
 \boxed{q(\chi_{A,B})=\bar h^{A+B}.}
\tag{3.5}
\]

The element \(\bar h\) has order nine and

\[
 z_0=\bar h^3
\tag{3.6}
\]

is the nontrivial order-three projected generator used by v247.

## 4. Same roof forces zero projected anchor

### Theorem 4.1 (TWO-COMMUTATOR ROOF/ANCHOR NO-GO)

If

\[
 \psi_{36}(\chi_{A,B})=\psi_{36}(\chi_{07}),
\tag{4.1}
\]

then

\[
 \boxed{q(\chi_{A,B})=q(\chi_{07})=1.}
\tag{4.2}
\]

Equivalently, the relative word

\[
 n_{A,B}=\chi_{07}^{-1}\chi_{A,B}
\tag{4.3}
\]

has zero image in the first projected kernel:

\[
 \boxed{q(n_{A,B})=1.}
\tag{4.4}
\]

#### Proof

Lemma 2.1 gives \(18\mid A+B\), hence \(9\mid A+B\).  Equations
(3.5) and \(\bar h^9=1\) give \(q(\chi_{A,B})=1\).  The R07 core has
exponent sum \(1+(-1)=0\), so its image is also one.  Equation (4.4)
follows.  \(\square\)

### Corollary 4.2 (NO A4 ANCHOR IN THE WHOLE FAMILY)

No word \(\chi_{A,B}\) in the same pure-dihedral R07 roof fibre can satisfy

\[
 q(\chi_{07}^{-1}\chi_{A,B})=z_0
 \quad\text{or}\quad z_0^2.
\tag{4.5}
\]

To obtain \(z_0\) one would need

\[
 A+B\equiv3\pmod9,
\tag{4.6}
\]

and to obtain \(z_0^2\) one would need

\[
 A+B\equiv6\pmod9.
\tag{4.7}
\]

Both contradict \(A+B\equiv0\pmod{18}\).

Thus no choice of the two integer coefficients \(A,B\), no matter how large,
turns this literal family into the v247 word-bearing A4 anchor.

## 5. The role of chi40

For

\[
 \chi_{40}=\chi_{10,-1},
\tag{5.1}
\]

one has

\[
 A+B=9,\qquad A-B=11.
\tag{5.2}
\]

Therefore

\[
 q(\chi_{40})=\bar h^9=1=q(\chi_{07}),
\tag{5.3}
\]

but

\[
 \psi_{36}(\chi_{40})
 =(r^{22},r^{-22},r^{-18})
 \ne(r^4,r^{-4},1).
\tag{5.4}
\]

This is the boundary phenomenon isolated in v335: \(\chi_{40}\) is already
invisible to the exponent-nine quotient but differs from R07 by an
order-two pure-dihedral roof digit.  It is not a missing A4 anchor.

Squaring its relative comparator changes \(A+B\) by \(18\), which restores
the \(Q=36\) roof but remains zero modulo nine.  Hence the closed words
\(c_j\) of v335 obey Theorem 4.1 exactly.

## 6. Why arbitrary actual-kernel words are not excluded

Theorem 4.1 concerns only the two-parameter literal family (1.2).  It does
not say

\[
 q(\ker(F\to\Delta_0))=1.
\tag{6.1}
\]

Indeed, v213 and v247 require and prove at paper level that the actual
successor kernel \(K\) has

\[
 q(K)=\langle z_0\rangle.
\tag{6.2}
\]

The point is that a lift of \(z_0\) must use the full noncommutative
word-bearing kernel—normal conjugates and relations not compressible to the
two exponents \(A,B\).  Once an accepted A4 basis
\(u_1,\ldots,u_t\) is available, v247 chooses the least basis combination
with \(q(u)=z_0\).  The present no-go theorem proves that this step cannot be
replaced by a cleverer choice of \(A,B\).

There is no contradiction with v211's non-roof theorem: the exponent-nine
projection does not factor through the roof.  Arbitrary roof-kernel words
can have nonzero projected area even though the restricted family (1.2)
cannot.

## 7. Consequence for relative-dihedral generalization

The explicit dihedral generalization now has a sharp division of labor.

1. The words \(c_j\) of v335 give closed pure-dihedral all-rung directions.
2. Their Fox tangents are the norm columns of v336 and can be tested at
   later depths.
3. The **first** nonzero projected A4 anchor cannot come from any
   \([x,y]^A[y,z]^B\) core in the R07 roof fibre.
4. It must come from the full actual-kernel basis, after which v247 lifts
   the projected relative ideal and v333 tests the field-even score pairings.

Thus “generalize the dihedral theorem” remains useful for the infinite
rung formula, but it cannot by itself replace the field-outer/full-\(P_0\)
component.  The obstruction is the explicit pair of incompatible
congruences (2.1) and (4.6)--(4.7), not a lack of ingenuity in choosing the
integers \(A,B\).

```text
SAME R07 DIHEDRAL ROOF:                 A-B=2 mod 18, A+B=0 mod 18
EXPONENT-NINE IMAGE:                    hbar^(A+B)
SAME-ROOF TWO-COMMUTATOR A4 ANCHOR:    IMPOSSIBLE
CHI40 EXPONENT-NINE IMAGE / ROOF:       IDENTITY / WRONG ROOF
ARBITRARY ACTUAL-KERNEL A4 ANCHOR:      NOT EXCLUDED / STILL REQUIRED
PURE-DIHEDRAL LATER RUNG COLUMNS:       RETAINED FROM V335--V336
COMPATIBLE FULL LIFT / FAKE / IHARA:    NOT CONSTRUCTED
```

`R07_TWO_COMMUTATOR_ROOF_ANCHOR_NO_GO_V337_PAPER_GRADE`


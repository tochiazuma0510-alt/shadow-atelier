# R07 A4 anchor/field-outer augmentation split (v339)

Author: Sol / 2026-08-29

Status: paper theorem making the A4 component of the generalized relative-
dihedral lift explicit.  An ordered word-bearing basis of the elementary-
abelian successor kernel canonically yields one projected (C_3) anchor and
a basis of its field-outer kernel.  The complete relative augmentation ideal
then splits into the anchor augmentation and translated field-outer
augmentation.  This identifies a finite literal roster for the second
homotopy; it does not assert that its actual score matrix is onto.  No
milestone numerator, compatible lift, fake certificate or Ihara witness is
declared.  `verified=false`.

## 1. Splitting the actual first successor kernel

Retain v247's first relative edge and projected quotient:

\[
 \Delta_1\twoheadrightarrow\Delta_0,
 \qquad K=\ker(\Delta_1\to\Delta_0),
 \qquad q(K)=R=\langle z_0\rangle\cong C_3.
\tag{1.1}
\]

The actual A4 kernel is an elementary-abelian three-group.  Write it
additively when doing linear algebra, but retain multiplicative source words.
Let

\[
 K=\langle k_1,\ldots,k_t\rangle_{\mathbf F_3},
 \qquad q(k_i)=z_0^{a_i},\quad a_i\in\mathbf F_3,
\tag{1.2}
\]

be an ordered word-bearing basis.  Since (q(K)=R), at least one (a_i) is
nonzero.  Let (j) be the least such index, put

\[
 e=a_j^{-1},\qquad k_z=k_j^e,
\tag{1.3}
\]

and, for (i\ne j), define

\[
 \ell_i=k_i k_z^{-a_i}.
\tag{1.4}
\]

### Theorem 1.1 (DETERMINISTIC A4 SPLIT BASIS)

Put (K_0=\ker(q|_K)).  Then

\[
 \boxed{q(k_z)=z_0,\qquad
        \ell_i\in K_0,\qquad
        K=\langle k_z\rangle\oplus K_0,}
\tag{1.5}
\]

and

\[
 \boxed{K_0=\langle\ell_i:i\ne j\rangle_{\mathbf F_3}.}
\tag{1.6}
\]

The displayed (ell_i) are a basis, not merely a generating roster.

#### Proof

Equation (1.3) gives (q(k_z)=z_0^{a_je}=z_0).  Therefore

\[
 q(\ell_i)=z_0^{a_i}z_0^{-a_i}=1,
\]

so every (ell_i) lies in (K_0).  In additive coordinates, (k_z=e k_j)
and

\[
 \ell_i=k_i-a_i k_z\qquad(i\ne j).
\tag{1.7}
\]

If a linear combination of the vectors in (1.7) is zero, its coefficient on
the original basis vector (k_i), for each (i\ne j), is the corresponding
combination coefficient.  Hence all coefficients vanish.  Thus the
(t-1) vectors are independent.  The nonzero functional (q|_K) has kernel
dimension (t-1), proving (1.6).  Since (k_z\notin K_0), (1.5) follows.
\(\square\)

If (u_i\in F(x,y)) is the retained source word of (k_i), then

\[
 u_z=u_j^e,
 \qquad
 v_i=u_i u_z^{-a_i}quad(i\ne j)
\tag{1.8}
\]

are literal source words for (k_z,ell_i).  No commutation is performed in
the free source; only their values in the abelian kernel commute.

## 2. The relative ideal has an exact anchor/outer normal form

Put (k=\mathbf F_3), (C=\langle k_z\rangle), and let

\[
 \mathfrak a_H=\ker(k[H]\to k)
\tag{2.1}
\]

denote the augmentation ideal of a finite group (H).  Theorem 1.1 gives

\[
 k[K]\cong k[C]\otimes_k k[K_0].
\tag{2.2}
\]

### Theorem 2.1 (ANCHOR/FIELD-OUTER AUGMENTATION SPLIT)

There is a direct sum of (k)-spaces

\[
 \boxed{
 \mathfrak a_K=
 (\mathfrak a_C\otimes 1)
 \oplus
 (k[C]\otimes\mathfrak a_{K_0}).}
\tag{2.3}
\]

The first summand has basis

\[
 k_z-1,\qquad k_z^2-1,
\tag{2.4}
\]

and the second has basis

\[
 k_z^r(u-1),
 \qquad r\in\{0,1,2\},\quad
 u\in K_0\setminus\{1\}.
\tag{2.5}
\]

The map (q_*:k[K]\to k[R]) kills the whole second summand and maps the
first isomorphically to (mathfrak a_R).

#### Proof

As vector spaces,

\[
 k[K_0]=k\cdot1\oplus\mathfrak a_{K_0}.
\tag{2.6}
\]

Tensoring with (k[C]) splits (k[K]) into

\[
 k[C]\otimes1
 \oplus k[C]\otimes\mathfrak a_{K_0}.
\]

The total augmentation restricts to the ordinary augmentation on the first
summand and vanishes on the second.  Its kernel is therefore exactly (2.3).
The standard group-element difference bases give (2.4)--(2.5).  The map
(q) is the identity (C\to R) under (k_z\mapsto z_0) and kills (K_0),
which proves the final assertion. \(\square\)

Now choose a left transversal (T) of (K) in (Delta_1).  The full
relative ideal

\[
 I=\ker(k[\Delta_1]\to k[\Delta_0])
\tag{2.7}
\]

is

\[
 I=\bigoplus_{t\in T}t\mathfrak a_K.
\tag{2.8}
\]

Combining (2.3) and (2.8) gives the exact word-bearing normal form

\[
 \boxed{I=I_{\rm anch}\oplus I_{\rm out},}
\tag{2.9}
\]

where

\[
 I_{\rm anch}=
 \operatorname{span}\{t(k_z-1),t(k_z^2-1):t\in T\},
\tag{2.10}
\]

and

\[
 I_{\rm out}=
 \operatorname{span}\{t k_z^r(u-1):
 t\in T,\ r=0,1,2,\ u\in K_0\setminus\{1\}\}.
\tag{2.11}
\]

Every vector in (I_{\rm out}) has zero projected (R)-value.  All of the
projected relative ideal is supplied by (I_{\rm anch}).  Extra collisions
among outer prefixes in the larger quotient may create further kernel, but
they do not alter the direct decomposition (2.9).

## 3. Generator form without enumerating every element of (K_0)

The vector basis (2.11) is useful for a finite complete matrix, but a closure
does not need to enumerate all (3^{t-1}-1) nonidentity elements.  Since the
(ell_i) form a group basis, the ordinary telescoping identity gives

\[
 \mathfrak a_{K_0}
 =\sum_{i\ne j} k[K_0](\ell_i-1).
\tag{3.1}
\]

Consequently

\[
 \boxed{
 I_{\rm out}
 =\sum_{t\in T}\sum_{r=0}^2\sum_{i\ne j}
   t k_z^r k[K_0](\ell_i-1).}
\tag{3.2}
\]

At source-word level, every seed is a difference

\[
 s(t)u_z^r v_i-s(t)u_z^r,
\tag{3.3}
\]

whose two words have the same (Delta_0)-value and the same projected
(R)-value.  Closing (3.3) under the registered common-source actions yields
the complete field-outer ideal.  Thus the second homotopy's primitive A4
roster has exactly (t-1) kernel words, not an unspecified ambient module.

The complete score-column matrix must still use every required translate and
occurrence action.  Equation (3.2) reduces the primitive generators; it does
not assert that a small untranslated prefix spans the endpoint image.

## 4. Relation to A3, A5 and the relative-dihedral formula

The corrected v247 A3 base point lifts

\[
 \kappa_D=\lambda(z_0-1)
\tag{4.1}
\]

through (k_z).  It therefore lies in the word-bearing image of
(I_{\rm anch}).  This is the exact role of the single A4 anchor.

Every component invisible to the projected (C_3) screen lies in the kernel
of the projection, whose explicit primitive part is (I_{\rm out}).  The A5
joint slice may mix anchor and outer coordinates, so it remains necessary to
solve the actual joint equations; no claim is made that the outer summand
alone contains the residual.  What (2.9) proves is the correct division of
labor:

\[
 \boxed{
 \text{projected/relative-dihedral anchor}
 \quad\oplus\quad
 \text{translated augmentation of }K_0.}
\tag{4.2}
\]

V337 proves that the first summand's nonzero anchor cannot be obtained from a
same-roof word of the two-commutator family
([x,y]^A[y,z]^B).  It must be extracted from the full A4 basis.  Once it is
extracted, Theorem 1.1 simultaneously produces the field-outer basis needed
for v333's score pairing.  A4 is therefore not two unrelated computations:
one row reduction supplies both pieces of (4.2).

## 5. All-rung elementary-abelian form

The same argument is not special to a cyclic projected kernel.  At a matched
edge let (K_m) be elementary abelian, let

\[
 K_m\twoheadrightarrow R_m\cong(\mathbf F_3)^{a_m},
 \qquad a_m\le3,
\tag{5.1}
\]

and choose, by row reduction on a word-bearing basis, a section subspace
(S_m\le K_m) and kernel (K_m^0) such that

\[
 K_m=S_m\oplus K_m^0,
 \qquad S_m\cong R_m.
\tag{5.2}
\]

Then

\[
 \boxed{
 \mathfrak a_{K_m}
 = (\mathfrak a_{S_m}\otimes1)
 \oplus(k[S_m]\otimes\mathfrak a_{K_m^0}).}
\tag{5.3}
\]

The first summand is the finite projected relative-dihedral compiler; the
second is the exact field-outer/full-kernel supplement.  Word-bearing Gaussian
elimination gives both at every edge.  By v259, these edge-local splittings do
not have to be natural under reduction for one based compatible product;
actual MEMBER and side-gate success at every edge remain necessary.

Thus the infinite-refinement generalization no longer contains an unnamed
“full even module.”  Its finite input at edge (m) is the split basis

\[
 (\text{basis of }S_m,\ \text{basis of }K_m^0)
\tag{5.4}
\]

and its unresolved test is the complete common-word/score image of the
translated generators in (5.3).

## 6. Certificate boundary

An actual A4 split certificate must retain:

1. the ordered word-bearing basis (k_i) and all projected exponents (a_i);
2. the least nonzero pivot (j), inverse (e), anchor word (u_z), and
   direct (q(k_z)=z_0) replay;
3. every outer word (v_i=u_i u_z^{-a_i}), its zero projection, and two-way
   basis comparison with (K_0);
4. the change-of-basis matrix and its inverse;
5. the anchor and outer seed pairs (2.10)--(3.3); and
6. the full score/endpoint action of every registered translate used by A5.

Mutating a pivot exponent, inverse scalar, multiplication order, source word,
outer projection, basis coefficient or occurrence prefix must destroy the
corresponding replay.  A rank count without word ancestry is insufficient.

```text
A4 BASIS -> ONE PROJECTED C3 ANCHOR:              PAPER PROOF
A4 BASIS -> FIELD-OUTER KERNEL BASIS:             PAPER PROOF
RELATIVE IDEAL ANCHOR/OUTER DIRECT SUM:           PAPER PROOF
PRIMITIVE OUTER GENERATORS:                       t-1 WORD-BEARING SEEDS
ALL-RUNG ELEMENTARY-ABELIAN SPLIT:                PAPER PROOF
ACTUAL A4 SPLIT BASIS / SCORE MATRIX:             NOT COMPUTED
ACTUAL A5 MEMBER / UNIVERSAL ENDPOINT:            NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA:                   NOT CONSTRUCTED
```

`R07_A4_ANCHOR_FIELD_OUTER_SPLIT_V339_PAPER_GRADE`

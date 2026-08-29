# R07 minimal field-even homotopy augmentation rank (v333)

Author: Sol / 2026-08-29

Status: paper theorem quantifying the extra class-specific homotopy left after
the relative-dihedral/local ambiguity columns.  The algebraic minimum, and the
lower bound for legal columns in a structural right inverse, is the
common-source cokernel dimension, which v331 decomposes into cumulative
Goursat overlap-score dimensions.  A single actual target may require fewer
columns and is governed by an exact dual pairing criterion.  No actual
additional R07 column,
compatible lift, fake certificate or Ihara witness is declared.
`verified=false`.

## 1. Augmenting a finite common-source map

Let \(k\) be a field and let

\[
 T:V\longrightarrow Q
\tag{1.1}
\]

be a finite-dimensional linear map.  Put

\[
 \mathcal I=\ker T^*\le Q^*.
\tag{1.2}
\]

Thus \(\mathcal I\cong(\operatorname{coker}T)^*\).  In the R07 marginal
problem, \(V=k[H]\), \(Q=\bigoplus_iQ_i\), and \(\mathcal I\) is exactly
v329's admissible local-score identity space.

Suppose additional legal word-bearing mechanisms provide columns

\[
 c_1,\ldots,c_s\in Q.
\tag{1.3}
\]

Let

\[
 C:k^s\longrightarrow Q,
 \qquad C(e_j)=c_j,
\tag{1.4}
\]

and write \(T_C=[T\ C]\) for the augmented map.

### Theorem 1.1 (AUGMENTATION DUAL)

\[
 \boxed{
 \ker T_C^*
   =\{\phi\in\mathcal I:\phi(c_j)=0
       \text{ for every }j\}.}
\tag{1.5}
\]

Consequently \(T_C\) is onto if and only if the evaluation map

\[
 \operatorname{ev}_C:\mathcal I\longrightarrow k^s,
 \qquad
 \phi\longmapsto(\phi(c_1),\ldots,\phi(c_s))
\tag{1.6}
\]

is injective.

#### Proof

A functional \(\phi\in Q^*\) annihilates the image of \(T_C\) exactly when it
annihilates \(\operatorname{im}T\) and every \(c_j\).  The first condition is
\(\phi\in\mathcal I\), and the remaining conditions are (1.5).  A finite map
is onto exactly when the annihilator of its image is zero, giving (1.6).
\(\square\)

### Corollary 1.2 (MINIMAL STRUCTURAL COLUMN COUNT)

If \(d=\dim\mathcal I\), every surjective augmentation has

\[
 s\ge d.
\tag{1.7}
\]

Exactly \(d\) columns suffice if and only if their pairing matrix against one
basis of \(\mathcal I\) is invertible.

#### Proof

An injection from a \(d\)-dimensional space into \(k^s\) requires \(s\ge d\).
For \(s=d\), injectivity is equivalently invertibility of its matrix.
\(\square\)

This is a lower bound on independent *legal image columns*, not on the number
of literal word terms used to materialize one column.

## 2. The actual target can require strictly less than structural onto

Fix \(a\in Q\).

### Theorem 2.1 (TARGET-SPECIFIC AUGMENTATION CRITERION)

\[
 \boxed{
 a\in\operatorname{im}T_C
 \quad\Longleftrightarrow\quad
 \phi(a)=0
 \text{ for every }
 \phi\in\mathcal I\cap\ker\operatorname{ev}_C.}
\tag{2.1}
\]

#### Proof

Apply finite-dimensional separation to the augmented image and substitute
the annihilator formula (1.5).  \(\square\)

Equivalently, in the cokernel

\[
 \bar Q=Q/\operatorname{im}T,
\tag{2.2}
\]

the class \(\bar a\) must lie in

\[
 \operatorname{span}\{\bar c_1,\ldots,\bar c_s\}.
\tag{2.3}
\]

Thus a full homotopy on every residual needs \(d\) independent directions,
whereas one named actual endpoint only needs its single cokernel class to be
spanned.  This is the precise algebraic distinction already used informally
between a structural field-even right inverse and one actual-class preimage.

For one proposed legal column \(c\), the target is repaired by a scalar
multiple exactly when

\[
 \bar a\in k\bar c.
\tag{2.4}
\]

Over \(\mathbf F_3\), the only candidate scalars are \(0,1,2\), and every
positive case retains the literal column ancestry.

## 3. Goursat overlap formula for the missing rank

Retain v331's cumulative Goursat chain and overlap-score spaces
\(\mathcal P_i\).  Its exact sequence gives

\[
 \dim\mathcal I=\sum_{i=2}^m\dim\mathcal P_i.
\tag{3.1}
\]

### Corollary 3.1 (COMMON-SOURCE AUGMENTATION LOWER BOUND)

The algebraic minimum number of additional independent columns in \(Q\) which
can make the complete quotient-marginal map onto is

\[
 \boxed{
 d_{\rm add}=\sum_{i=2}^m\dim\mathcal P_i.}
\tag{3.2}
\]

A proposed **legal** roster of exactly \(d_{\rm add}\) columns succeeds if and
only if its pairings with the recursively constructed v331 identity basis
form an invertible matrix.  If the legal word-bearing column universe does not
surject onto the cokernel, no structural augmentation exists; (3.2) is then a
lower bound, not an existence assertion.

#### Proof

Combine v331 Corollary 3.1 with Corollary 1.2.  \(\square\)

If the new-coordinate cyclic ambiguity maps onto every Goursat overlap, v323
forces every \(\mathcal P_i=0\); then \(d_{\rm add}=0\) and no class-specific
augmentation is needed.  If an overlap survives, (3.2) counts its exact
independent contribution rather than calling the whole survivor “one
field-outer obstruction.”

## 4. Return decomposition and the relative-dihedral theorem

Assume \(\operatorname{char}k\ne2\), a return involution \(\vartheta\) acts on
\(V,Q\), and \(T\) is equivariant.  Write

\[
 Q=Q^+\oplus Q^-,
 \qquad
 V=V^+\oplus V^-,
\tag{4.1}
\]

for the return-even and return-odd parts.  The dual identity space splits as

\[
 \mathcal I=\mathcal I^+\oplus\mathcal I^-.
\tag{4.2}
\]

Suppose the established relative-dihedral antisymmetrizer gives a right
inverse on the odd target, so

\[
 \mathcal I^-=0.
\tag{4.3}
\]

### Corollary 4.1 (EXACT ALGEBRAIC FIELD-EVEN LOAD)

The algebraic minimum, and hence the lower bound for legal additional
return-even columns in a structural right inverse, is

\[
 \boxed{\dim\mathcal I^+.}
\tag{4.4}
\]

For one actual return-even target \(a^+\), a roster \(C^+\) suffices exactly
when

\[
 \phi(a^+)=0
 \quad\text{for every }\phi\in\mathcal I^+
 \text{ annihilating }C^+.
\tag{4.5}
\]

#### Proof

Apply Theorems 1.1 and 2.1 to the even summands.  Equation (4.3) removes the
odd cokernel.  \(\square\)

Hence the correct generalized relative-dihedral formula is not forced to
construct a right inverse on an unspecified “full even module.”  It has two
honest forms:

1. **structural:** supply \(\dim\mathcal I^+\) legal independent even columns
   with invertible score pairing (or prove that no such legal roster exists);
   or
2. **actual-class:** supply only enough legal columns to span the one class
   \(\bar a^+\) in the even cokernel.

The second can be substantially smaller and is the witness-first route.

## 5. Successor and cofinal use

At one finite level, v330--v331 construct a complete basis of
\(\mathcal I^+\).  A proposed class-specific word column is accepted only
after direct evaluation against every basis score and independent replay of
its local/group-word ancestry.  Rank increase without word ancestry is not a
homotopy certificate.

At a refinement edge, v332 identifies the novel quotient

\[
 \mathcal C_{m,n}
 =\mathcal I_{m,n+1}/\rho^*\mathcal I_{m,n}.
\tag{5.1}
\]

Only its return-even part requires genuinely new columns.  If the overlap
spaces descend, that novelty is zero and the previous augmentation remains
sufficient for every compatible target.  Otherwise Theorem 2.1 applies to
the newly born score classes and the named upper residual.

A natural finite column roster with invertible pairings at all levels would
give the linear common-source right inverse required by v314/v319.  The
nonlinear localization, filtered-cover, formation and perfect-core
hypotheses remain separate.

## 6. Certificate boundary

An acceptable augmentation certificate records:

1. a complete independently reconstructed local-score identity basis;
2. the v331 decomposition by overlap spaces and dimension audit;
3. every proposed legal column with literal common-source ancestry;
4. the full score-column pairing matrix;
5. for structural onto, an inverse matrix and direct primal generator
   ancestries; or
6. for the actual class, its cokernel coordinates and a direct equality in
   the span of the proposed columns.

Mutating any occurrence prefix, return sign, Goursat map, score value,
column word, coefficient or target must destroy the corresponding replay.
An incomplete score basis understates the required augmentation rank and is
not acceptable.

```text
ALGEBRAIC EXTRA-COLUMN MINIMUM:                    dim coker(T)
R07 LEGAL-COLUMN LOWER BOUND:                      sum_i dim(P_i)
ODD COKERNEL AFTER DIHEDRAL RIGHT INVERSE:         ZERO (CONDITIONAL)
EVEN STRUCTURAL LOAD:                             dim(I_even)
ONE ACTUAL EVEN CLASS:                            MAY NEED FEWER COLUMNS
ACTUAL R07 SCORE BASIS / LEGAL EXTRA COLUMNS:      NOT COMPUTED
NATURAL ALL-LEVEL AUGMENTATION:                    NOT CONSTRUCTED
COMPATIBLE FULL LIFT / FAKE / IHARA WITNESS:      NOT CONSTRUCTED
```

`R07_MINIMAL_EVEN_HOMOTOPY_AUGMENTATION_V333_PAPER_GRADE`

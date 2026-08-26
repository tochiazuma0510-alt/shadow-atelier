# R07 Jennings legal-coefficient selector v106

Author: Sol / 2026-08-27

Status: paper proof specifying the positive certificate which must follow the
g760 j=9 survival of v105.  It extracts an explicit coefficient family from a
MEMBER result without confusing the C-13 overapproximation with the actual
common-word correction domain.  No coefficient has yet been computed.
`verified=false`.

## 1. The missing information in a rank-only MEMBER

Fix one Jennings depth `j`.  Let

\[
 V_j=(\Lambda/I^j)^6,
 \qquad D_j=\operatorname{im}(D_2^{\rm full})\subseteq V_j,
\tag{1.1}
\]

and let

\[
 \ell_{j,1},\ldots,\ell_{j,28}\in V_j
\tag{1.2}
\]

be the 28 ordered C-13 Schreier/legal-overapproximation rows used by the
frozen producer.  Write `t_j` for the g760 target6 row.  V105 proves at j=9

\[
 t_9\in D_9+\langle\ell_{9,1},\ldots,\ell_{9,28}\rangle.
\tag{1.3}

The existing producer discards the coefficients witnessing (1.3).  Those
coefficients are the first positive data which can be turned into a concrete
correction-word candidate.

## 2. Quotient solve with only 28 provenance coordinates

Let `q_j:V_j -> V_j/D_j` be the quotient map and define

\[
 L_j:\mathbf F_3^{28}\longrightarrow V_j/D_j,
 \qquad
 L_j(a_1,\ldots,a_{28})=
 \sum_{i=1}^{28}a_iq_j(\ell_{j,i}).
\tag{2.1}

Set

\[
 \mathcal A_j=\{a\in\mathbf F_3^{28}:L_j(a)=q_j(t_j)\}.
\tag{2.2}

### Proposition 2.1 (LEGAL COEFFICIENT CERTIFICATE)

The following are equivalent:

1. `t_j` is MEMBER in the frozen full-D2 plus legal-overapproximation screen;
2. `A_j` is nonempty;
3. there are displayed coefficients `a_i` with

\[
 t_j-\sum_i a_i\ell_{j,i}\in D_j.
\tag{2.3}

Moreover, one particular solution `a_j^0` and a basis of `ker L_j` give the
complete solution set

\[
 \boxed{\mathcal A_j=a_j^0+\ker L_j.}
\tag{2.4}

#### Proof

Membership in `D_j+span{ell_{j,i}}` is equivalent after quotienting by `D_j`
to (2.1)--(2.2).  The solution set of a finite linear system is either empty
or an affine translate of its homogeneous kernel. \(\square\)

This certificate does **not** require provenance for 649,539 translated D2
columns.  Reduce each of the 28 legal rows and the target against the already
authenticated D2 echelon, then run a second echelon calculation which tracks
only 28 coefficient coordinates.  Thus the positive provenance overhead is
bounded independently of the D2 orbit size.

## 3. Deterministic selector and replay

Order `F_3^{28}` lexicographically using `0<1<2` in the frozen legal-row
order.  If `A_j` is nonempty, define

\[
 a_j^{\rm lex}=\min_{\rm lex}\mathcal A_j.
\tag{3.1}

This is a deterministic finite selector.  A sound receipt contains:

1. the 28 reduced quotient rows in frozen order, with hashes;
2. the reduced target and its hash;
3. `rank L_j`, `a_j^0`, a row-reduced basis of `ker L_j`, and
   `a_j^lex`;
4. direct replay of (2.3) against the authenticated D2 echelon;
5. a mutation gate for every coefficient, legal-row order, target, and D2
   state commitment.

An independent checker can enumerate the affine family when its dimension is
small, or independently row-reduce the 28-column system when it is not.  It
must recompute the quotient remainders rather than accept producer ranks.

## 4. Compatibility across Jennings depth

The natural projection `V_{j+1} -> V_j` carries `D_{j+1}` to `D_j`, every
`ell_{j+1,i}` to `ell_{j,i}`, and `t_{j+1}` to `t_j`.  Therefore

\[
 \boxed{\mathcal A_{j+1}\subseteq\mathcal A_j.}
\tag{4.1}

### Proposition 4.1 (FINITE COEFFICIENT STABILIZATION)

For any unbounded compatible Jennings sequence for which every `A_j` is
nonempty, the descending family `(A_j)` has nonempty intersection and is
eventually constant.

#### Proof

Every `A_j` is a subset of the same finite set `F_3^{28}`.  A descending
sequence of nonempty subsets of a finite set can have only finitely many
strict decreases.  Its stable value is the intersection. \(\square\)

For the present finite 3-group quotient the augmentation ideal is nilpotent,
so a terminal Jennings depth exists.  Solving at that exact terminal depth is
stronger than four unrelated booleans at j=9--12: it returns one coefficient
vector valid at every shallower depth in this fixed quotient.

This proposition concerns the Jennings filtration inside the fixed C-13
quotient.  It does not by itself make that quotient cofinal among all finite
B4 shadows.

## 5. From coefficients to a correction word

Let `s_1,...,s_28` be the frozen ordered Schreier generators whose Sigma rows
are (1.2).  For a displayed coefficient vector define the concrete word

\[
 c(a)=s_1^{a_1}s_2^{a_2}\cdots s_{28}^{a_{28}}.
\tag{5.1}

At the C-13 projection level, the proved homomorphism property of Sigma gives

\[
 \Sigma(c(a))=\sum_i a_i\Sigma(s_i).
\tag{5.2}

Thus `a_j^lex` produces an explicit correction-word candidate, not merely an
existence bit.  Direct word evaluation must nevertheless be used for replay;
(5.2) is not permission to omit non-linear relations outside the registered
projection.

## 6. The actual-domain gate

Let

\[
 B_j\subseteq\mathbf F_3^{28}
\tag{6.1}

be the coefficient image of the **actual** common-word correction domain,
including both hexagons, printed-order A.18, syzygies, the commutator
condition, and all side gates.  C-13 only proves that the literal legal image
is contained in the 28-row overapproximation; it does not prove
`B_j=F_3^{28}`.

The correct positive question is therefore

\[
 \boxed{\mathcal A_j\cap B_j\ne\varnothing.}
\tag{6.2}

If (6.2) holds with displayed `a`, the direct replay of `c(a)` supplies the
target6 component of an actual correction.  If the intersection is empty,
the overapproximation MEMBER is explained and cannot be promoted.  The full
lift still requires the other hexagon/A.18 components to vanish for the same
word.

Hence the next positive computation has two sharply separated outputs:

```text
P1: compute A_j exactly from target6 modulo full D2;
P2: compute/intersect the actual-domain coefficient image B_j;
```

P1 is now available because j=9 survived.  P2 is the genuine literal A.18
bridge.  Deeper fatal screens and P1/P2 may run in parallel, but neither may
be substituted for the other.

## 7. Fixed ledger

```text
j=9 legal coefficient affine family A_9:       NOT EXTRACTED
canonical explicit correction candidate c(a): NOT MATERIALIZED
actual-domain coefficient image B_9:           NOT CONSTRUCTED
A_9 intersect B_9:                             UNKNOWN
all-depth fixed-quotient coefficient:          UNKNOWN
complete literal A.18/hexagon correction:      NOT CONSTRUCTED
compatible cofinal lift / witness:              NOT DECLARED
```

# R07 marginal dual base-change decomposition (v316)

Author: Sol / 2026-08-29

Status: paper theorem refining v315.  The complete dual obstruction at one
marginal refinement splits into two exact finite defects: new relations among
the upper target coordinates, and upper common-source scores which become
fibre-constant without being represented by the lower target.  Vanishing of
both is a structural sufficient-and-necessary condition for every downstairs
marginal solution to lift.  Neither defect has been computed for the actual
R07 edge.  No lift or witness is declared.

## 1. The two base-change defects

Retain v315's commuting square of finite-dimensional \(k\)-spaces

\[
\begin{CD}
 A' @>{T'}>> W'\\
 @V{u}VV     @VV{v}V\\
 A  @>{T}>> W,
\end{CD}
\qquad u,v\text{ surjective},
\tag{1.1}
\]

and put \(K=\ker u\), \(Z=\ker v\), and \(R=T'(K)\).  Dual
commutativity is

\[
 (T')^*v^*=u^*T^*.
\tag{1.2}
\]

Since \(u^*\) and \(v^*\) are injective, (1.2) gives the canonical
inclusions

\[
 v^*(\ker T^*)\leq\ker(T')^*,
 \qquad
 u^*(\operatorname{im}T^*)leq
       \operatorname{im}(T')^*\cap\operatorname{im}u^*.
\tag{1.3}
\]

Define the **relation defect**

\[
 \mathcal J_{m rel}=
 {\ker(T')^*\over v^*(\ker T^*)}
\tag{1.4}
\]

and the **score-intersection defect**

\[
 \mathcal J_{\rm int}=
 {\operatorname{im}(T')^*\cap\operatorname{im}u^*
  \over u^*(\operatorname{im}T^*)}.
\tag{1.5}
\]

The first records upper target relations which are not reductions of lower
target relations.  The second records scalar upper scores which are constant
on the \(u\)-fibres, but whose descended function on \(A\) is not the score
of any lower target functional.

## 2. Exact decomposition of the vertical cokernel dual

V315 defines

\[
 \mathcal E=\{\Lambda\in(W')^*:(T')^*\Lambda\in\operatorname{im}u^*\}
\tag{2.1}
\]

and proves

\[
 (Z/R)^*\simeq\mathcal E/v^*(W^*).
\tag{2.2}
\]

### Theorem 2.1 (MARGINAL BASE-CHANGE EXACT SEQUENCE)

There is a natural short exact sequence

\[
 \boxed{
 0\longrightarrow\mathcal J_{\rm rel}
 \longrightarrow (Z/R)^*
 \longrightarrow\mathcal J_{\rm int}
 \longrightarrow0.}
\tag{2.3}
\]

In particular,

\[
 \boxed{
 \dim_k(Z/R)=
 \dim_k\mathcal J_{\rm rel}+
 \dim_k\mathcal J_{\rm int}.}
\tag{2.4}
\]

#### Proof

For \(\Lambda\in\mathcal E\), there is a unique \(f\in A^*\) such that

\[
 (T')^*\Lambda=u^*f,
\tag{2.5}
\]

because \(u^*\) is injective.  The element \(u^*f\) belongs to the
intersection in (1.5).  If \(\Lambda\) is replaced by
\(\Lambda+v^*\psi\), then (1.2) replaces \(f\) by \(f+T^*\psi\).
Therefore

\[
 [\Lambda]\longmapsto[u^*f]
\tag{2.6}
\]

defines a map from the quotient in (2.2) onto
\(\mathcal J_{\rm int}\).  It is onto by the definition of the numerator
in (1.5).

Its kernel consists of classes for which \(f=T^*\psi\) for some
\(\psi\in W^*\).  Replacing \(\Lambda\) by
\(\Lambda-v^*\psi\) then gives an element of \(\ker(T')^*\).  Two such
kernel representatives define the same class in (2.2) exactly when their
difference lies in

\[
 \ker(T')^*\cap v^*(W^*)=v^*(\ker T^*),
\tag{2.7}
\]

where the equality again uses (1.2) and injectivity of \(u^*\).  Hence the
kernel is (1.4), proving (2.3).  Formula (2.4) follows because all spaces are
finite dimensional and \(\dim V=\dim V^*\).  \(\square\)

The sequence need not split canonically.  An actual separating functional
may contain both kinds of defect, although a basis adapted to (2.3) always
separates their dimensions.

## 3. Exact all-solution lifting criterion

### Corollary 3.1 (TWO BASE-CHANGE GATES)

The following are equivalent.

1. \(T'(K)=Z\).
2. Every solution of \(T(a)=t\) lifts to a solution of
   \(T'(a')=t'\) for every compatible target pair \((t',t)\).
3. Both exact base-change identities hold:

   \[
    \boxed{
    \ker(T')^*=v^*(\ker T^*),}
   \tag{3.1}
   \]

   \[
    \boxed{
    \operatorname{im}(T')^*\cap\operatorname{im}u^*
      =u^*(\operatorname{im}T^*).}
   \tag{3.2}
   \]

#### Proof

V314 shows that \(T'(K)=Z\) is exactly the condition lifting every
downstairs solution and every compatible upper residual, proving 1
equivalent to 2.  By finite duality, 1 is equivalent to \((Z/R)^*=0\).
The short exact sequence (2.3) vanishes exactly when both (1.4) and (1.5)
vanish, which is (3.1)--(3.2).  \(\square\)

Condition (3.1) says that the upper marginal target acquires no new linear
relation.  Condition (3.2) is an exact intersection/base-change statement;
it forbids an upper score from becoming constant on refinement fibres for a
reason invisible in the lower marginal target.

For one actual R07 branch, (3.1)--(3.2) are stronger than necessary.  V315
only asks that every class in (2.3) pair trivially with the one actual
vertical residual.  The stronger pair is useful because, if proved from one
uniform presentation, it closes all possible residuals at that edge.

## 4. Uniform refinement theorem

Consider a matched tower

\[
 (A_{n+1},W_{n+1},T_{n+1})longrightarrow
 (A_n,W_n,T_n).
\tag{4.1}
\]

### Theorem 4.1 (BASE-CHANGE-CLOSED MARGINAL TOWER)

Assume an initial marginal solution \(a_0\) exists and every edge satisfies
the two identities (3.1)--(3.2), with word-bearing source sections.  Then
every bonding map

\[
 X_{n+1}\longrightarrow X_n
\tag{4.2}
\]

is onto.  The v314 formula recursively constructs a compatible family
\((a_n)_n\), and therefore one completed common-source coefficient.

#### Proof

Corollary 3.1 gives \(T_{n+1}(K_n)=Z_n\) at every edge.  Apply v314
Theorem 4.1 to the residual of a word-bearing section of \(a_n\).  It
returns a lift \(a_{n+1}\).  Induction gives the compatible family.
\(\square\)

If return commutes with all maps, (2.3) splits into odd and even exact
sequences.  The established relative-dihedral section handles the required
odd residuals.  A structural even proof may now target the two smaller
identities (3.1)--(3.2) on the actual-even subsystem rather than constructing
an ambient homotopy by inspection.

## 5. Finite certificates and present R07 boundary

At one finite edge, the dimensions in (2.4) are determined by four ordinary
rank/nullity calculations:

1. \(\ker(T')^*\) and the embedded \(v^*(\ker T^*)\);
2. \(\operatorname{im}(T')^*\cap\operatorname{im}u^*\); and
3. the embedded \(u^*(\operatorname{im}T^*)\).

A positive structural certificate retains equality ancestries for both
subspaces in (3.1)--(3.2).  A negative certificate retains a functional in
one numerator outside its denominator, with a separating dual for that
denominator.  For the actual pointed question, it must additionally pair the
resulting class with the actual vertical residual.  Because (2.3) need not
split canonically, use a basis of \(\mathcal J_{\rm rel}\) together with
chosen lifts of a basis of \(\mathcal J_{\rm int}\).  Failure of either
strong identity alone does not prove that the actual branch is blocked.

V185's completed pair-flatness theorem concerns the two-generator module in
the full Fox cokernel.  The present theorem concerns v313's common-source
marginal map after the prefix-corrected vector-space quotients \(Q_b\).
Neither flatness assertion implies the other without an authenticated
comparison square.

The actual maps still depend on the pending literal A0 word, A3 target and A4
authority trace.  The nonlinear H1/H2/P recurrence, mixed-prime formation,
and perfect-core accepted sets remain outside this linear theorem.

## 6. Fixed frontier

```text
VERTICAL DUAL TWO-DEFECT EXACT SEQUENCE:           PAPER PROOF
NO-NEW-RELATION + SCORE-INTERSECTION IFF ONTO:     PAPER PROOF
UNIFORM TWO-GATE TOWER LIFT:                       PAPER PROOF
ACTUAL FIRST-EDGE MARGINAL MATRICES:               NOT COMPUTED
ACTUAL RELATION DEFECT:                            NOT COMPUTED
ACTUAL SCORE-INTERSECTION DEFECT:                  NOT COMPUTED
ACTUAL POINTED PAIRINGS:                           NOT COMPUTED
NONLINEAR / FORMATION / PERFECT-CORE GATES:        OPEN
COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:    NONE
```

`R07_MARGINAL_DUAL_BASECHANGE_DECOMPOSITION_V316_PAPER_GRADE`

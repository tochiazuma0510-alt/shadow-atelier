# R07: authenticated selected-ancestry SLP lift (v465)

Author: Sol / 2026-09-03

Status: candidate paper theorem; successor to v464 after the independent
Task 594 audit.  This note proves that a selected authenticated reduction
ancestry can be retained as one explicit free-source straight-line program
(SLP), without materializing its flat letter expansion.  It is the positive
handoff after a grade-one MEMBER decision.  It neither supplies that pending
decision nor proves a relative-kernel right inverse at every refinement.
verified=false.

## 1. Typed source and hypotheses

Let \(F\) be the fixed free source group and let

\[
 F=F^0\supseteq F^1\supseteq\cdots,\qquad
 F^{d+1}\triangleleft F^d\triangleleft F                         \tag{1.1}
\]

be the registered normal filtration.  For every registered literal actor
\(P\), assume

\[
 P F^iP^{-1}=F^i                                                \tag{1.2}
\]

at all layers used below.  Each \(F^d/F^{d+1}\) is an abelian
\(\mathbf F_3\)-space, and the recorded linear actor on that grade is exactly
the action induced by conjugation by \(P\).  These actor-stability and
induced-action hypotheses are part of the statement; exponent three alone
does not imply them.

For every registered finite quotient \(Q\), write
\(\pi_Q:F\to Q\).  If \(Q'\to Q\) is a registered refinement with reduction
\(r_{Q',Q}\), assume the source triangle commutes:

\[
 r_{Q',Q}\pi_{Q'}=\pi_Q.                                       \tag{1.3}
\]

A typed SLP consists of:

1. leaves containing the exact registered free words for compact seeds,
   transition defects and earlier corrections;
2. ordered product, inverse and registered composition nodes;
3. conjugation nodes labelled by an exact literal actor word; and
4. references only to earlier nodes.

It is finite and acyclic.  Recursive interpretation therefore defines a
single element \(\operatorname{word}(T)\in F\), even when its flat letter list
is never allocated.

For \(a\in\mathbf F_3\), let

\[
 [a]=0,1,-1\quad\text{for}\quad a=0,1,2.                       \tag{1.4}
\]

Suppose an echelon ancestry node in the pure filtered part records

\[
 b_j=\sigma_j\left(z_j-\sum_{p<j}q_{jp}b_p\right),
 \qquad \sigma_j\in\{1,2\}.                                   \tag{1.5}
\]

For the origin SLP \(Z_j\), define in the recorded order

\[
 W_j=
 \left(
   Z_j\prod_{p<j}^{\longrightarrow}W_p^{[-q_{jp}]}
 \right)^{[\sigma_j]}.                                        \tag{1.6}
\]

Zero exponents are omitted.  No commutation, collection or reordering is
allowed.  If a target reduction returns coefficients \(a_j\), define its
selected grade update

\[
 C_T=\prod_j^{\longrightarrow}W_j^{[a_j]}.                    \tag{1.7}
\]

Only nonzero roots and the downward subgraph reachable from them need be
exported.

## 2. Pure associated-grade theorem

### Theorem 2.1 (SLP associated-grade lift)

Assume every origin \(Z_j\) in (1.6) lies in \(F^d\), and its registered
grade class is \(z_j\).  Then

\[
 [W_j]_d=b_j,\qquad [C_T]_d=\sum_j a_jb_j.                    \tag{2.1}
\]

#### Proof

In the abelian exponent-three quotient \(F^d/F^{d+1}\), ordered product and
inverse induce addition and negation, and (1.2) makes literal conjugation
induce the registered actor action.  Induction in the acyclic node order
turns (1.6) into (1.5).  Applying the same calculation to (1.7) proves the
second equality.  Nothing is asserted above grade \(d\). \(\square\)

### Proposition 2.2 (lower-first licence)

The old/lower part of the physical echelon may combine origins which do not
individually lie in \(F^d\).  Such a node is not licensed by Theorem 2.1.
Let

\[
 E_{<d}^{\mathrm{phys}},\qquad E_d^{\mathrm{phys}}              \tag{2.2}
\]

denote the exact registered interpreters for, respectively, the complete
lower physical target (normalized exponent, PB3 augmentation, boundary and
every auxiliary coordinate included) and its associated grade.  A selected
lower-first node \(W\) is a legal physical-fibre row only after direct
evaluation of its exact SLP proves both

\[
 E_{<d}^{\mathrm{phys}}(W)=0,\qquad
 E_d^{\mathrm{phys}}(W)=\text{the stored normalized grade row}. \tag{2.3}
\]

Equation (2.3) proves membership in the registered physical fibre.  It does
**not** by itself prove membership in a source relative kernel such as
\(K_n^D=\ker r_n^D\).  That stronger typing requires a separate direct
source-reduction replay of the same SLP.  In particular, cancellation of a
coefficient row or of only the regular lower block is insufficient.

### Corollary 2.3 (different literal representatives)

If \(C_{\mathrm{alt}}\in F^d\) is any other literal representative with the
same grade-\(d\) class as \(C_T\), then

\[
 C_TC_{\mathrm{alt}}^{-1}\in F^{d+1}.                         \tag{2.4}
\]

Thus a change of representative preserves the completed grade-\(d\)
equation but can change the next residual.  The grade-\((d+1)\) residual must
always be recomputed from the exact authenticated representative actually
chosen.  This statement gives no permission to sort noncommuting factors.

## 3. Naturality of one source instruction

Evaluate a fixed SLP \(T\) in a quotient \(Q\) by applying \(\pi_Q\) to each
leaf and interpreting every ordered group operation there.  Structural
induction and (1.3) give

\[
 \operatorname{ev}_Q(T)=\pi_Q(\operatorname{word}(T)),\qquad
 r_{Q',Q}\operatorname{ev}_{Q'}(T)=\operatorname{ev}_Q(T).     \tag{3.1}
\]

Therefore an authenticated SLP is one common source instruction whose
quotient values are automatically compatible; it is not a family of
independently chosen coefficient vectors.  In R07, each of the eleven
occurrences evaluates this same syntax with its own registered substitution,
actor path, prefix, inverse convention and sign.  No common occurrence
action is inferred.

Compatibility in (3.1) says only that evaluations of one word reduce
correctly.  It does not say that this word solves the target equation at all
refinements.

## 4. Complete positive handoff

Let \(C_{<d}\) be the authenticated prior-correction SLP already solving the
registered target below grade \(d\).  A MEMBER reduction supplies (1.7), for
which direct replay must prove that \(C_T\) has complete lower/auxiliary
image zero and solves the current residual \(\rho_d\).  It is only the
selected grade update, not the full correction.

Create one top root

\[
 C_d=\operatorname{Compose}(C_{<d},C_T)                       \tag{4.1}
\]

in the exact registered source composition order.  For the current
finalizer, this is the order represented by
canonical_solution["terms"] + update; (4.1) freezes that order rather than
identifying it with an unordered \(\mathbf F_3\)-sum.

The checker must evaluate \(C_d\), not \(C_T\) alone, in all eleven
occurrences.  It first establishes every lower and auxiliary equality and
the complete precision-\(d\) target equation.  Only then may it define

\[
 \rho_{d+1}
   =\operatorname{gr}_{d+1}\!\left(T-A(C_d)\right).            \tag{4.2}
\]

The required selected payload is:

1. the decision body, selected coefficients and all parent state digests;
2. every reachable old, physical-lower, block and physical-grade node, with
   type, index, normalizing scale and ordered reduction edges;
3. every reached defect_origin record and the reached old
   seed_reductions or actor_transitions expression to which it points;
4. exact literal seed and actor words;
5. the authenticated prior root \(C_{<d}\), update root \(C_T\), and complete
   top root \(C_d\); and
6. a canonical ordered encoding of all these fields, bound by digest to the
   decision and prepare/block state digests.

Items 2--3 are the full reachable dependency closure: a non-DAG
defect_origin reference may not be dropped merely because unselected DAG
nodes are pruned.  Conversely, neither the entire discovery DAG nor a flat
leaf multiset is needed.

An independent interpreter memoizes every selected node, replays (2.3) for
each selected lower-first node, verifies (2.1) for pure filtered nodes,
checks the complete root (4.1), and computes (4.2) afresh.  A claim that a
selected SLP belongs to a source kernel additionally invokes the separate
source-reduction replay specified after (2.3).

This handoff does not alter v281's separate A7 provenance gate for its
factored-pair language.  The present SLP is a different explicit
representative and receives its own direct replay.

## 5. Size and failure semantics

If the selected dependency closure has \(V\) nodes and \(E\) ordered edges,
the SLP occupies \(O(V+E)\) records, regardless of the size of its flat word.
At one finite quotient, memoized interpretation evaluates each selected node
once.  Resource exhaustion while selecting, encoding or evaluating this
subgraph is UNKNOWN_RESOURCE, never NONMEMBER.  On a NONMEMBER decision,
no ancestry export or SLP evaluation is required.

## 6. Exact boundary

    SELECTED ANCESTRY -> LITERAL SLP:
      PAPER-CLOSED under the typed-origin and canonical-payload hypotheses above
    PURE SLP GRADE-d CLASS = MEMBER COEFFICIENTS:
      PAPER-CLOSED under (1.1)--(1.2) and authenticated ancestry replay
    ONE SLP NATURAL AT ALL REGISTERED QUOTIENTS:
      PAPER-CLOSED under the commuting triangles (1.3)
    LOWER-FIRST PHYSICAL-FIBRE LICENCE:
      REQUIRES the two direct replays (2.3)
    SOURCE RELATIVE-KERNEL MEMBERSHIP:
      REQUIRES a separate direct source-reduction replay
    FLAT EXPANSION BEFORE NEXT REPLAY:         NOT REQUIRED
    COMPLETE ROOT C_d AND FRESH RESIDUAL:      REQUIRED
    ACTUAL GRADE-ONE COEFFICIENTS / SLP:       NOT YET AVAILABLE
    COFINAL SUCCESSOR SURJECTIVITY:            NOT PROVED
    COMPATIBLE LIFT / A0 / COMMON:             NOT DECLARED
    FAKE / IHARA:                              NOT DECLARED


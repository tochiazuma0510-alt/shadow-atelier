# R07 completed-pair local flatness criterion v185

Author: Sol / 2026-08-28

Status: paper theorem.  This note replaces infinitely many pair-saturation
equalities by one completed relative Tor condition.  For the actual
two-generator pair quotient, vanishing of this Tor group forces finite-rank
topological freeness and hence pair saturation at every matched relative
Frattini edge.  The actual completed Tor group has not been computed or
proved zero.  No compatible lift, fake certificate, or Ihara witness is
declared.

## 1. The completed relative local ring

Let

\[
 1\longrightarrow P\longrightarrow\Delta_\infty
 \longrightarrow\Delta_0\longrightarrow1
\tag{1.1}
\]

be the diagonal-context group of v173 on the matched relative pro-\(3\)
tower.  Thus \(P\) is a finitely generated pro-\(3\) group and
\(\Delta_0\) is finite.  Put

\[
 R=\mathbf F_3[[P]],
 \qquad \mathfrak m=\ker(R\xrightarrow{\varepsilon}\mathbf F_3),
 \qquad \Xi=\mathbf F_3[[\Delta_\infty]].
\tag{1.2}
\]

The pseudocompact ring \(R\) is local, with Jacobson radical
\(\mathfrak m\).  Choosing finitely many coset representatives in (1.1)
makes \(\Xi\) finite free as a left and as a right \(R\)-module.  No
splitting of the group extension is required.

Let \(Z\) be the full block-tagged universal Fox cokernel of v175 and
v183 Lemma 4.3.  Let \(d,e\in Z\) be the compatible signed original target
and the corrected residual, and define the closed actual-pair module and
its quotient by

\[
 M=\Xi d+\Xi e,
 \qquad Q=Z/M.
\tag{1.3}
\]

The image of \(\Xi^2\to Z\), \((a,b)\mapsto ad+be\), is compact and hence
closed.

The following actual typing condition is load-bearing:

\[
 \tag{FP}
 Q\text{ has a finite pseudocompact presentation over }R.
\]

It holds if the full seven-context compiler has first been expressed by the
finite-free completed \(R\)-module formulation of v169 Section 3: add the
two columns \(d,e\) to that finite presentation.  It must not be inferred
merely from the fact that each finite shadow is finite dimensional.  In
particular, if a context permutation module is obtained only by unrestricted
restriction along a diagonal subgroup, its finite presentation over \(R\)
must be authenticated.  Since \(\Xi\) is finite free over \(R\), a finite
\(\Xi\)-presentation is one sufficient certificate for (FP).

The use of the full cokernel is again load-bearing.  A cycle kernel need not
commute with the base changes used below.

## 2. A noncommutative completed local criterion

Write \(k=R/\mathfrak m=\mathbf F_3\), regarded as a right \(R\)-module
through augmentation.

### Theorem 2.1 (FINITE-PRESENTED LOCAL TOR CRITERION)

For a finitely presented pseudocompact left \(R\)-module \(Q\), the
following are equivalent:

\[
 \boxed{
 \operatorname{Tor}_1^R(k,Q)=0
 \quad\Longleftrightarrow\quad
 Q\cong R^s
 \text{ topologically for some finite }s.}
\tag{2.1}
\]

#### Proof

The reverse implication is immediate.  For the forward implication, lift a
\(k\)-basis of \(Q/\mathfrak mQ\) to a minimal continuous surjection

\[
 R^s\twoheadrightarrow Q
\tag{2.2}
\]

and let \(L\) be its kernel.  Finite presentation of \(Q\) makes \(L\)
finitely generated and closed.  Minimality gives

\[
 L\subseteq\mathfrak mR^s.
\tag{2.3}
\]

Apply \(k\widehat\otimes_R-\) to
\(0\to L\to R^s\to Q\to0\).  The map

\[
 L/\mathfrak mL\longrightarrow k^s
\tag{2.4}
\]

is zero by (2.3).  Exactness therefore identifies

\[
 \operatorname{Tor}_1^R(k,Q)
 \cong L/\mathfrak mL.
\tag{2.5}
\]

Under the left side of (2.1), topological Nakayama gives \(L=0\).  Hence
(2.2) is an isomorphism.  The argument uses neither commutativity nor a
Noetherian hypothesis beyond the stated finite presentation. \(\square\)

### Corollary 2.2 (MINIMAL MATRIX FORM)

Start with any finite presentation

\[
 R^a\xrightarrow{A}R^b\longrightarrow Q\longrightarrow0.
\tag{2.6}
\]

Row and column reduction of \(\bar A\) over \(k\), followed by lifting the
operations to \(R\), splits all unit pivots.  It leaves a presentation

\[
 R^{a'}\xrightarrow{A_{\min}}R^s\longrightarrow Q\longrightarrow0,
 \qquad A_{\min}\equiv0\pmod{\mathfrak m}.
\tag{2.7}
\]

Then

\[
 \boxed{
 \operatorname{Tor}_1^R(k,Q)=0
 \quad\Longleftrightarrow\quad
 \operatorname{im}A_{\min}=0.}
\tag{2.8}
\]

#### Proof

A square block congruent to the identity modulo \(\mathfrak m\) is a unit:
its inverse is the convergent ordered Neumann series.  Gaussian block
elimination therefore splits every pivot seen in \(\bar A\) and gives
(2.7).  Put \(L=\operatorname{im}A_{\min}\).  Since
\(L\subseteq\mathfrak mR^s\), the proof of Theorem 2.1 gives

\[
 \operatorname{Tor}_1^R(k,Q)=L/\mathfrak mL.
\tag{2.9}
\]

Topological Nakayama makes the right side zero exactly when \(L=0\).
\(\square\)

Thus the completed criterion has a finite universal matrix format.  The
remaining entries of \(A_{\min}\) must vanish as actual elements of the
completed group algebra.  Vanishing in one finite quotient is not a
substitute; a symbolic word/Fox identity or all-level separated replay is
required.

## 3. Completed freeness forces every finite saturation

Let \((U_n)_{n\ge0}\) be the open normal subgroups of \(P\) defining the
matched relative Frattini tower, and let \(J_n\triangleleft R\) be the
closed ideal generated by \(u-1\), \(u\in U_n\).  The corresponding finite
objects are the reductions of \(Z,M,Q\).

### Theorem 3.1 (ONE COMPLETED TOR GATE IMPLIES ALL-RUNG SATURATION)

Assume (FP).  If

\[
 \boxed{\operatorname{Tor}_1^R(k,Q)=0,}
\tag{3.1}
\]

then, at every adjacent pair of matched relative Frattini levels,

\[
 \boxed{
 M_{n+1}\cap I_nZ_{n+1}=I_nM_{n+1}.}
\tag{3.2}
\]

Here \(I_n\) is the kernel of the finite diagonal group-algebra reduction.

#### Proof

Theorem 2.1 makes \(Q\) finite free over \(R\), hence projective.  The
sequence

\[
 0\longrightarrow M\longrightarrow Z\longrightarrow Q\longrightarrow0
\tag{3.3}
\]

therefore splits as pseudocompact \(R\)-modules:

\[
 Z=M\oplus Q.
\tag{3.4}
\]

For every closed ideal \(J\triangleleft R\), (3.4) gives

\[
 JZ=JM\oplus JQ,
 \qquad M\cap JZ=JM.
\tag{3.5}
\]

Normality of each relative kernel gives
\(I_nZ_{n+1}=JZ_{n+1}\) and
\(I_nM_{n+1}=JM_{n+1}\) for the corresponding quotient ideal \(J\): the
full group-algebra kernel is the extension of that relative ideal, and
\(M_{n+1},Z_{n+1}\) are stable under the complete diagonal algebra.  Reduce
(3.5) at level \(n+1\) to obtain (3.2). \(\square\)

The splitting need only be \(R\)-linear.  Equality of the extended ideal
actions in the last paragraph is what promotes it to the required
diagonal-algebra saturation statement.

### Corollary 3.2 (COMPLETED-TOR COFINAL MULTIPLIER)

Assume (3.1), \(e_0=0\), and the full-cokernel/base-change typing of v183.
Then v183 Corollary 5.1 supplies compatible coefficients

\[
 e_n=\mu_nd_n,
 \qquad \mu_0=0,
\tag{3.6}
\]

and hence \(\mu=(\mu_n)\in\mathfrak j\).  Under the word-bearing and
nonlinear hypotheses of v174, one compatible correction is

\[
 \boxed{c_\infty=-\sum_{r\ge0}\mu^ra.}
\tag{3.7}
\]

Thus a single completed Tor identity is a sufficient structural answer to
the all-rung pair-saturation problem.  It does not remove the separate word,
formation, onto, or nonabelian perfect-core gates.

## 4. Relation to the first-edge canary

If (3.1) holds, every finite edge satisfies (3.2).  In particular the exact
task195 first-edge equality

\[
 \dim_{\mathbf F_3}(M_1/J_KM_1)=\dim_{\mathbf F_3}M_0
\tag{4.1}
\]

must pass.  Therefore:

* a complete task195 failure of (4.1) refutes the completed-free route for
  that authenticated actual pair;
* a task195 pass is a necessary canary, not a proof of (3.1); and
* the still weaker pointed pass of v184 may succeed even when both (4.1)
  and (3.1) fail.

The next structural computation after a positive canary is not an
unbounded enumeration of unrelated rungs.  It is to construct the finite
universal presentation (2.6), split its roof unit pivots, and decide whether
the remaining completed map \(A_{\min}\) is literally zero.  A nonzero
entry witnessed in any authenticated finite quotient refutes this strong
freeness route but does not refute the pointed v184 selector.

## 5. Exact R07 certificate

A complete positive certificate for the strong route consists of:

1. the fixed full seven-context Fox presentation and a lossless finite-free
   \(R\)-presentation certificate establishing (FP);
2. the literal completed rows \(d,e\), with their word and boundary
   provenance;
3. the augmented finite presentation matrix of \(Q=Z/(\Xi d+\Xi e)\);
4. the roof row/column operations, every lifted unit pivot and its ordered
   inverse, and the resulting minimal matrix \(A_{\min}\);
5. a symbolic replay that every entry of \(A_{\min}\) is zero in the fixed
   completed presentation; and
6. independent finite reductions and destructive mutations of a pivot,
   factor order, Fox entry, actual row, and one alleged zero entry.

A bounded failure to prove a completed entry zero is `UNKNOWN`.  A literal
nonzero finite reduction is a refutation only of this completed-free route.

## 6. Fixed frontier

```text
FINITE-PRESENTED COMPLETED LOCAL TOR CRITERION:    PAPER_PROOF
MINIMAL UNIVERSAL MATRIX CRITERION:                PAPER_PROOF
COMPLETED TOR ZERO => ALL-RUNG PAIR SATURATION:    PAPER_PROOF
R07 FINITE-PRESENTATION TYPING (FP):               NOT AUTHENTICATED
R07 COMPLETED ACTUAL-PAIR TOR:                     NOT COMPUTED
R07 UNIVERSAL MINIMAL MATRIX A_min:                NOT CONSTRUCTED
TASK192 EXACT FIRST CORRECTION:                    GHA IN PROGRESS
TASK193 ACTUAL SUCCESSOR COMPILER:                 SELFTEST CROSS-CHECKED
TASK194 SHARDED BOUNDARY CORRELATION:              STATIC REPAIR IN PROGRESS
TASK195 FIRST-EDGE PAIR / POINTED CANARY:          STATIC REPAIR IN PROGRESS
WORD/NONLINEAR/FORMATION GATES:                    OPEN
COMPATIBLE COFINAL LIFT / FAKE / IHARA:            NOT DECLARED
```

`R07_COMPLETED_PAIR_LOCAL_FLATNESS_V185_PAPER_GRADE`

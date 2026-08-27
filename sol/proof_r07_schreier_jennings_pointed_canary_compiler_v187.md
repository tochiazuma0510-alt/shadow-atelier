# R07 Schreier--Jennings pointed-canary compiler v187

Author: Sol / 2026-08-28

Status: paper theorem and finite compiler for the first pointed R07 gate.
It replaces repeated closure under all relative-kernel differences by one
bounded Jennings-monomial roster.  It requires the genuine word-bearing
diagonal group, quotient map, section, and elementary-abelian kernel that
task196 is commissioned to export.  No task196 production object, first
multiplier, compatible lift, fake certificate, or Ihara witness is declared.

## 1. Relative group-algebra normal form

Let

\[
  1\longrightarrow K\longrightarrow G
   \stackrel{\pi}{\longrightarrow}Q\longrightarrow1
\tag{1.1}
\]

be an exact sequence of finite groups, where

\[
 K=\langle k_1,\ldots,k_t\rangle\cong(C_3)^t.
\tag{1.2}
\]

Put

\[
 A=\mathbf F_3[G],\qquad
 \bar A=\mathbf F_3[Q],\qquad
 I=\ker(A\to\bar A),
\tag{1.3}
\]

and choose any set-theoretic section
\(\sigma:Q\to G\), with \(\sigma(1)=1\).  Define

\[
 T_i=k_i-1,
 \qquad
 T^{\mathbf a}=T_1^{a_1}\cdots T_t^{a_t},
 \qquad 0\leq a_i\leq2.
\tag{1.4}
\]

### Lemma 1.1 (SCHREIER--JENNINGS BASIS)

There are vector-space decompositions

\[
 \boxed{
 A=\bigoplus_{q\in Q}\ igoplus_{\mathbf a\in\{0,1,2\}^t}
       \mathbf F_3\,\sigma(q)T^{\mathbf a}}
\tag{1.5}
\]

and

\[
 \boxed{
 I=\bigoplus_{q\in Q}\;
       \bigoplus_{0<|\mathbf a|\leq2t}
       \mathbf F_3\,\sigma(q)T^{\mathbf a}.}
\tag{1.6}
\]

In particular, \(I^{2t+1}=0\).

#### Proof

Because the ordered \(k_i\) form an \(\mathbf F_3\)-basis of the elementary
abelian group \(K\),

\[
 \mathbf F_3[K]
 \cong
 \mathbf F_3[T_1,\ldots,T_t]/(T_1^3,\ldots,T_t^3).
\tag{1.7}
\]

Thus its displayed monomials form a basis and its augmentation ideal
\(J_K\) has exactly the positive-degree monomials as a basis.  The left
cosets \(\sigma(q)K\) partition \(G\), so

\[
 A=\bigoplus_{q\in Q}\sigma(q)\mathbf F_3[K].
\tag{1.8}
\]

Since \(K\lhd G\), the kernel in (1.3) is the two-sided ideal
\(I=AJ_K=J_KA\).  Equations (1.5)--(1.6) follow.  Every product of
\(2t+1\) elements of \(I\) lies in
\(AJ_K^{2t+1}\): normality makes every conjugate of \(J_K^r\) equal to
\(J_K^r\), so the intervening coset representatives can be moved past the
augmentation factors.  Every monomial in \(J_K^{2t+1}\) has total degree
greater than \(2t\), so it vanishes. \(\square\)

The section need not be a homomorphism and the extension need not split.
Only its exact word-bearing coset representatives are used in (1.5).

## 2. Exact finite spans for the actual pair

Let \(Z\) be a left \(A\)-module and let \(d,e\in Z\).  Put

\[
 D=Ad,
 \qquad
 M=Ad+Ae.
\tag{2.1}
\]

For \(z\in\{d,e\}\), define the literal columns

\[
 C_z(q,\mathbf a)=\sigma(q)T^{\mathbf a}z.
\tag{2.2}
\]

All equalities below are equalities in the specified module \(Z\); in R07,
this must be the full block-tagged Fox cokernel, with every boundary
reduction retained.

### Theorem 2.1 (ONE-ROSTER SPAN FORMULAS)

The following equalities hold:

\[
 \boxed{
 \begin{aligned}
 D&=\operatorname{span}\{C_d(q,\mathbf a)\},\\
 ID&=\operatorname{span}\{C_d(q,\mathbf a):|\mathbf a|>0\},\\
 M&=\operatorname{span}\{C_d(q,\mathbf a),C_e(q,\mathbf a)\},\\
 IM&=\operatorname{span}\{C_d(q,\mathbf a),C_e(q,\mathbf a):
                              |\mathbf a|>0\}.
 \end{aligned}}
\tag{2.3}
\]

Here \(q\) ranges over \(Q\) and \(\mathbf a\) over
\(\{0,1,2\}^t\).  Linear dependencies caused by the action on \(Z\) are
allowed; sparse echelon reduction of the displayed finite rosters computes
the exact dimensions.

#### Proof

The first and third equalities are (1.5) applied to the indicated module
generators.  Since \(I\) is a two-sided ideal,

\[
 I(Ad)=Id,
 \qquad
 I(Ad+Ae)=Id+Ie.
\tag{2.4}
\]

Now apply the basis (1.6). \(\square\)

This removes the redundant construction which first enumerates every
\(G\)-orbit column and then applies each of the \(t\) differences
\(k_i-1\) followed by another orbit closure.  The complete compiler uses at
most

\[
 2|Q|3^t=2|G|
\tag{2.5}
\]

pair columns, and each indexed column is evaluated once.  The positive
roster has \(2|Q|(3^t-1)\) entries before rank deletion.  This is an exact
finite bound, not a heuristic search radius.

## 3. Pointed, direct, and pair decisions from the same roster

Let \(\mathcal C_{>0}^{d,e}\) denote the positive-degree pair roster in
(2.3), \(\mathcal C_{>0}^{d}\) its \(d\)-only part, and
\(\mathcal C_{\geq0}^{d,e}\) the full pair roster.

### Corollary 3.1 (ROOF-ZERO POINTED GATE)

The v184 roof-zero obstruction vanishes exactly when

\[
 \boxed{e\in\operatorname{span}\mathcal C_{>0}^{d,e}.}
\tag{3.1}
\]

Suppose the retained echelon ancestry is

\[
 e=
 \sum_{q,\mathbf a>0}u_{q,\mathbf a}
       \sigma(q)T^{\mathbf a}d
 +
 \sum_{q,\mathbf a>0}v_{q,\mathbf a}
       \sigma(q)T^{\mathbf a}e.
\tag{3.2}
\]

Set

\[
 \alpha=\sum u_{q,\mathbf a}\sigma(q)T^{\mathbf a},
 \qquad
 \beta =\sum v_{q,\mathbf a}\sigma(q)T^{\mathbf a}.
\tag{3.3}
\]

Then \(\alpha,\beta\in I\), and the explicit compatible multiplier is

\[
 \boxed{
 \mu=(1-\beta)^{-1}\alpha
     =\left(\sum_{r=0}^{2t}\beta^r\right)\alpha.}
\tag{3.4}
\]

The displayed order is mandatory.  Direct action replay must prove
\(e=\mu d\) and \(\bar\mu=0\).

#### Proof

Equation (3.1) is Theorem 2.1 and v184 (3.1).  Equations
(3.2)--(3.3) give \(e=\alpha d+\beta e\).  Lemma 1.1 and v184 Theorem
2.1 give (3.4). \(\square\)

### Corollary 3.2 (DIRECT GATE)

The stronger direct condition is

\[
 \boxed{e\in ID
 \quad\Longleftrightarrow\quad
 e\in\operatorname{span}\mathcal C_{>0}^{d}.}
\tag{3.5}
\]

A positive ancestry directly returns \(\mu=\alpha\in I\), with no Neumann
inverse.  Failure of (3.5) does not imply failure of (3.1).

### Corollary 3.3 (PAIR-COINVARIANT CANARY)

Let \(M_0\) be constructed independently at the roof.  Then the v183 finite
edge canary is exactly

\[
 \boxed{
 \operatorname{rank}\mathcal C_{\geq0}^{d,e}
 -\operatorname{rank}\mathcal C_{>0}^{d,e}
 \stackrel{?}{=}\dim_{\mathbf F_3}M_0.}
\tag{3.6}
\]

This follows because the two ranks are \(\dim M\) and \(\dim IM\), and
\(IM\subseteq M\).  It remains a stronger canary than the single pointed
condition (3.1).

On failure of either membership test, the terminal certificate is a dual
which annihilates every retained pivot of the complete relevant roster and
pairs nontrivially with \(e\).  A pair-dimension mismatch is not such a
dual for the pointed or direct test.

## 4. Word-bearing evaluation and ancestry

Every column in (2.2) has a literal coefficient.  In characteristic three,

\[
 T_i=k_i-1,
 \qquad
 T_i^2=k_i^2+k_i+1,
 \qquad
 T_i^3=0.
\tag{4.1}
\]

Consequently \(T^{\mathbf a}\) expands into an explicit finite
\(\mathbf F_3\)-linear combination of words in the registered source words
for the \(k_i\).  Prefixing by the registered source word for \(\sigma(q)\)
gives the complete common-source coefficient for (2.2).  No abstract state
identifier is a substitute for this expansion.

For efficient evaluation, first build \(T^{\mathbf a}d\) and
\(T^{\mathbf a}e\) recursively in increasing total degree, using each
\(T_i\) action once per required edge.  Then apply the word-bearing
\(\sigma(q)\).  Echelon reduction may stop propagating a dependent vector
only when its full coefficient ancestry is retained; an input column may
not be deleted before the global mod-three merge of all boundary
coefficients.

The producer and independent checker should use different monomial orders
and different roof sections.  They compare the resulting four subspaces,
the reconstructed \(\alpha,\beta,\mu\) or separating dual, and the direct
seven-context Fox replay.  They do not compare arbitrary section labels.

## 5. R07 use and boundary of the result

For the first matched successor, take

\[
 G=\Delta_1,
 \qquad Q=\Delta_0,
 \qquad K=\ker(\Delta_1\to\Delta_0),
\tag{5.1}
\]

and take \(d=d_1\), \(e=e_1\) from the authenticated task193/task196
pipeline.  Task196 must first establish all hypotheses of Section 1 and
export the exact section and kernel basis.  This theorem then supplies a
bounded task195 successor with no second group-orbit search.

A positive (3.1) constructs only the first compatible coefficient
\(\mu_1\).  It does not prove that the selected pointed class vanishes at
every later rung.  Promotion still requires either the universal literal
identity of v175 or a natural all-rung ancestry of v184 (5.1), together
with the word, nonlinear, formation, prime-to-three, and perfect-core gates.

## 6. Fixed frontier

```text
SCHREIER--JENNINGS GROUP-ALGEBRA BASIS:          PAPER_PROOF
EXACT POSITIVE-MONOMIAL FORMULA FOR I*M / I*d:  PAPER_PROOF
BOUNDED 2|DELTA1| PAIR-COLUMN COMPILER:         PAPER_PROOF
POINTED/DIRECT/PAIR DECISIONS FROM ONE ROSTER:   PAPER_PROOF
FINITE EXPLICIT MU FORMULA FROM ANCESTRY:        PAPER_PROOF
TASK196 ACTUAL DIAGONAL/KERNEL EXPORT:           IMPLEMENTATION IN PROGRESS
R07 FIRST POINTED DECISION / MU1:                NOT COMPUTED
ALL-RUNG NATURAL ANCESTRY:                       NOT PROVED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:          NOT DECLARED
```

`R07_SCHREIER_JENNINGS_POINTED_CANARY_COMPILER_V187_PAPER_GRADE`

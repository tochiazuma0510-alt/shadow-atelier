# R07 Goursat score exact sequence and target recursion (v331)

Author: Sol / 2026-08-29

Status: paper theorem refining v329--v330.  Along a cumulative Goursat chain,
the space of additive local-score identities grows by one explicit overlap
space at each coordinate.  This gives an exact rank formula and a stagewise
target test whose pairing is the dual of v324's actual prefix mismatch.  No
actual R07 overlap space or target has been computed.  No compatible lift,
fake certificate or Ihara witness is declared.  `verified=false`.

## 1. Local scores and cumulative identity spaces

Let \(k\) be a field and retain the cumulative Goursat chain

\[
 H_i=H_{i-1}\times_{D_i}G_i,
 \qquad H_1=G_1,
\tag{1.1}
\]

with quotient maps

\[
 \alpha_i:H_{i-1}\twoheadrightarrow D_i,
 \qquad
 \beta_i:G_i\twoheadrightarrow D_i.
\tag{1.2}
\]

For local ambiguity spaces \(U_j\le k[G_j]\), put

\[
 Q_j=k[G_j]/U_j,
 \qquad
 W_j=U_j^\perp\cong Q_j^*.
\tag{1.3}
\]

Define the cumulative score map

\[
 R_i:\bigoplus_{j=1}^iW_j\longrightarrow k[H_i]^*,
 \qquad
 R_i(\phi_1,\ldots,\phi_i)(g_1,\ldots,g_i)
   =\sum_{j=1}^i\phi_j(g_j),
\tag{1.4}
\]

and its identity space

\[
 \mathcal I_i=\ker R_i.
\tag{1.5}
\]

Thus \(\mathcal I_i\) is exactly the space of v329 local-score identities on
the prefix joint image.  Since \(H_1=G_1\), one has

\[
 \mathcal I_1=0.
\tag{1.6}
\]

## 2. The new identity space is one overlap-score space

Define

\[
 \mathcal P_i=
 \left\{\psi\in k[D_i]^*:
   \alpha_i^*\psi\in\operatorname{im}R_{i-1},
   \quad
   \beta_i^*\psi\in W_i
 \right\}.
\tag{2.1}
\]

The first condition says that the cumulative quotient score decomposes into
admissible earlier local scores.  The second says that its pullback to the
new coordinate is locally admissible.  V329 Theorem 3.1 and v330 Section 4
give two complete finite ways to compute (2.1).

### Theorem 2.1 (HORIZONTAL GOURSAT SCORE EXACT SEQUENCE)

For every \(i\ge2\), there is a natural short exact sequence

\[
 \boxed{
 0\longrightarrow\mathcal I_{i-1}
 \mathrel{\mathop{\longrightarrow}^{\iota_i}}
 \mathcal I_i
 \mathrel{\mathop{\longrightarrow}^{\Theta_i}}
 \mathcal P_i
 \longrightarrow0.}
\tag{2.2}
\]

Here

\[
 \iota_i(\phi_1,\ldots,\phi_{i-1})
   =(\phi_1,\ldots,\phi_{i-1},0),
\tag{2.3}
\]

and, for an identity
\((\phi_1,\ldots,\phi_i)\in\mathcal I_i\), the value
\(\Theta_i(\phi)=\psi\) is the unique quotient score satisfying

\[
 \sum_{j<i}\phi_j(g_j)=\psi(\alpha_i(g_1,\ldots,g_{i-1})),
 \qquad
 \phi_i(g)=-\psi(\beta_i(g)).
\tag{2.4}
\]

#### Proof

Apply v330 Theorem 1.1 to

\[
 F(h)=\sum_{j<i}\phi_j(h_j),
 \qquad f(g)=\phi_i(g).
\tag{2.5}
\]

If their sum vanishes on the fibre product \(H_i\), both functions are
constant on the fibres of \(\alpha_i,\beta_i\).  Surjectivity of the two maps
therefore gives a unique function \(\psi:D_i\to k\) with (2.4).  The first
equation shows \(\alpha_i^*\psi\in\operatorname{im}R_{i-1}\); the second and
\(\phi_i\in W_i\) show \(\beta_i^*\psi\in W_i\).  Thus \(\Theta_i\) is
well defined into \(\mathcal P_i\).

If \(\Theta_i(\phi)=0\), then \(\phi_i=0\) because \(\beta_i\) is onto, and
the preceding tuple is in \(\mathcal I_{i-1}\).  Hence
\(\ker\Theta_i=\operatorname{im}\iota_i\).

Conversely, let \(\psi\in\mathcal P_i\).  Choose
\((\phi_1,\ldots,\phi_{i-1})\in\bigoplus_{j<i}W_j\) with

\[
 R_{i-1}(\phi_1,\ldots,\phi_{i-1})=\alpha_i^*\psi,
\tag{2.6}
\]

and put \(\phi_i=-\beta_i^*\psi\in W_i\).  Equality of the two quotient
values on \(H_i\) makes their total score zero, so this tuple lies in
\(\mathcal I_i\) and maps to \(\psi\).  This proves surjectivity and
exactness.  \(\square\)

Choosing one decomposition in (2.6) for every basis element of
\(\mathcal P_i\) splits (2.2) as vector spaces.  The splitting is not
canonical and need not commute with cofinal reduction; the exact sequence
itself is canonical.

## 3. Dimension and rank recursion

### Corollary 3.1 (IDENTITY DIMENSION)

\[
 \boxed{
 \dim\mathcal I_m
   =\sum_{i=2}^m\dim\mathcal P_i.}
\tag{3.1}
\]

#### Proof

Take dimensions in (2.2), start from (1.6), and iterate.  \(\square\)

Let

\[
 T_m:k[H_m]\longrightarrow\bigoplus_{j=1}^mQ_j
\tag{3.2}
\]

be the quotient-marginal map of v329.  Its dual is \(R_m\).  Hence:

### Corollary 3.2 (COMMON-SOURCE RANK FORMULA)

\[
 \boxed{
 \operatorname{rank}T_m
  =\sum_{j=1}^m\dim Q_j
   -\sum_{i=2}^m\dim\mathcal P_i.}
\tag{3.3}
\]

In particular,

\[
 \boxed{
 T_m\text{ is onto }
 \quad\Longleftrightarrow\quad
 \mathcal P_i=0\text{ for every }i\ge2.}
\tag{3.4}
\]

#### Proof

Finite-dimensional duality gives
\(\operatorname{rank}T_m=\operatorname{rank}R_m\).  The domain of \(R_m\)
has dimension \(\sum_j\dim W_j=\sum_j\dim Q_j\), and its kernel is
\(\mathcal I_m\).  Use (3.1).  Formula (3.4) follows because all summands in
(3.1) have nonnegative dimension.  \(\square\)

This rank computation uses only cumulative overlap-score spaces.  It does
not form a dense matrix with one column for every element of \(H_m\).

## 4. Stagewise target test

Let

\[
 a^{(i)}=(a_1+U_1,\ldots,a_i+U_i)
 \in\bigoplus_{j=1}^iQ_j
\tag{4.1}
\]

be the target prefix.  Assume \(a^{(i-1)}\) has passed all identities in
\(\mathcal I_{i-1}\).  For
\(\psi\in\mathcal P_i\), choose any decomposition (2.6) and define

\[
 \boxed{
 \langle\psi,a^{(i)}\rangle_{\rm new}
  =\sum_{j<i}\phi_j(a_j)-\psi((\beta_i)_*a_i).}
\tag{4.2}
\]

### Theorem 4.1 (NEW-OVERLAP TARGET OBSTRUCTION)

The value in (4.2) is independent of the chosen decomposition (2.6).
Moreover \(a^{(i)}\) passes every identity in \(\mathcal I_i\) if and only if

\[
 \boxed{
 \langle\psi,a^{(i)}\rangle_{\rm new}=0
 \quad\text{for every }\psi\in\mathcal P_i.}
\tag{4.3}
\]

#### Proof

Two decompositions differ by an element of \(\mathcal I_{i-1}\), whose
pairing with the passed prefix target is zero.  Thus (4.2) is well defined.
The exact sequence (2.2) says that a basis of \(\mathcal I_i\) consists of
the inherited identities and one chosen lift of a basis of
\(\mathcal P_i\).  The inherited pairings vanish by assumption; the new
pairings are exactly (4.2).  This proves (4.3).  \(\square\)

If \(\eta_{i-1}\in k[H_{i-1}]\) is a retained primal realization of the
prefix target, then (2.6) gives

\[
 \sum_{j<i}\phi_j(a_j)
 =\psi((\alpha_i)_*\eta_{i-1}).
\tag{4.4}
\]

Consequently

\[
 \boxed{
 \langle\psi,a^{(i)}\rangle_{\rm new}
 =\psi\bigl((\alpha_i)_*\eta_{i-1}-(\beta_i)_*a_i\bigr)
 =\psi(d_i),}
\tag{4.5}
\]

where \(d_i\) is v324's actual prefix mismatch.  Thus the horizontal exact
sequence and the affine primal DP have literally the same stagewise
obstruction pairing.

## 5. R07 computation contract

For the prefix-corrected cyclic spaces

\[
 U_j=\epsilon_jK_{r_j}p_j^{-1},
\tag{5.1}
\]

the condition \(\beta_i^*\psi\in W_i\) is the explicit quotient-orbit
condition of v323/v329.  The condition
\(\alpha_i^*\psi\in\operatorname{im}R_{i-1}\) is decided by v330's recursive
graph-score classifier.  Hence an authenticated calculation may proceed in
the following bounded stages:

1. construct the ordered cumulative groups, Goursat kernels and quotients;
2. compute a basis of each \(\mathcal P_i\) from orbit and recursive score
   equations;
3. audit the dimension increments using (3.1)--(3.3);
4. pair only the newly added basis with the actual target by (4.2); and
5. on zero pairings, recover a primal ancestry with v324--v325.

A nonzero value in (4.2) is a complete named NONMEMBER certificate.  Zero
pairings without authenticated completeness of the \(\mathcal P_i\) basis
are not MEMBER evidence.  A positive primal ancestry, rather than a rank
claim, remains the word-bearing output.

This is a horizontal coordinate-factor exact sequence.  It is distinct from
v316's vertical base-change exact sequence between two cofinal levels.  Both
must be satisfied for an all-refinement selector.

## 6. Fixed frontier

```text
CUMULATIVE LOCAL-SCORE IDENTITY EXACT SEQUENCE:    PAPER PROOF
IDENTITY DIMENSION / MARGINAL RANK RECURSION:      PAPER PROOF
STAGEWISE TARGET PAIRING = PRIMAL MISMATCH DUAL:   PAPER PROOF
DENSE FULL-JOINT SCORE MATRIX:                     NOT REQUIRED
ACTUAL R07 GOURSAT OVERLAP SPACES:                 NOT COMPUTED
ACTUAL TARGET PAIRINGS / PRIMAL ANCESTRY:          NOT COMPUTED
VERTICAL NATURALITY / NONLINEAR / FORMATION:       OPEN
COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:   NOT CONSTRUCTED
```

`R07_GOURSAT_SCORE_EXACT_SEQUENCE_V331_PAPER_GRADE`

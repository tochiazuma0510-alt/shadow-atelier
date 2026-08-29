# R07 based transported-Jacobian perturbation (v320)

Author: Sol / 2026-08-29

Status: paper theorem refining v266 and v319.  A filtration-raising linear
change of the common-word Jacobian can be absorbed by one additional based
Neumann matrix on the same finite free cover.  Thus the transported-linear
terms which remain after the first class-two correction do not require a new
right inverse at every depth, provided they assemble to a continuous
linear operator on the same localized module.  That assembly and its actual
R07 error matrix have not been proved or computed.  No lift, fake certificate
or Ihara witness is declared.

## 1. Based perturbation data

Retain v319's complete separated \(J\)-adic ring \(\Lambda\), finite free
cover

\[
 q:F=\Lambda^t\twoheadrightarrow L,
\tag{1.1}
\]

legal correction module \(A\), and continuous \(\Lambda\)-linear map

\[
 B:A\longrightarrow L.
\tag{1.2}
\]

Suppose a word-bearing based lift has already been constructed:

\[
 s:F\longrightarrow A,
\qquad
 Bs=q.
\tag{1.3}
\]

Let

\[
 T:A\longrightarrow L
\tag{1.4}
\]

be a continuous \(\Lambda\)-linear transported-prefix operator which raises
filtration:

\[
 \boxed{T(J^rA)\subseteq J^{r+1}L\quad(r\geq0).}
\tag{1.5}
\]

Put \(D=B+T\).

### Theorem 1.1 (BASED HOMOLOGICAL PERTURBATION)

There is a continuous \(\Lambda\)-linear map

\[
 K:F\longrightarrow JF
\tag{1.6}
\]

with

\[
 qK=Ts.
\tag{1.7}
\]

For any such \(K\), the series

\[
 V=(1+K)^{-1}=\sum_{m\geq0}(-K)^m
\tag{1.8}
\]

converges, and

\[
 \boxed{s_T=sV:F\longrightarrow A}
\tag{1.9}
\]

satisfies

\[
 \boxed{Ds_T=q.}
\tag{1.10}
\]

The construction remains based: it does not define a map \(L\to A\), impose
an annihilator condition, or require a splitting of \(q\).

#### Proof

By (1.5), \(Ts(F)\subseteq JL\).  Strictness of the free cover gives
\(JL=q(JF)\).  Choose a preimage in \(JF\) for the image of every basis
vector and extend linearly, obtaining (1.6)--(1.7).

Since \(K(F)\subseteq JF\), one has
\(K^m(F)\subseteq J^mF\), so (1.8) converges.  Finally,

\[
 Ds=(B+T)s=q+Ts=q(1+K),
\tag{1.11}
\]

and therefore

\[
 Ds_T=q(1+K)(1+K)^{-1}=q.
\tag{1.12}
\]

This proves the theorem. \(\square\)

The sign in (1.8) is fixed by (1.11).  If one records the transport error
with the opposite convention, the matrix and its Neumann signs must both be
changed; a checker should replay (1.11), not infer the sign from a label.

## 2. Finite and natural forms

If \(J^N=0\) in a finite quotient, then

\[
 s_T=s\sum_{m=0}^{N-1}(-K)^m.
\tag{2.1}
\]

If \(K(F)\subseteq J^jF\), only
\(\lceil N/j\rceil\) terms are needed.  Thus the perturbation adds one finite
matrix and one bounded Neumann polynomial to the v319 certificate.

### Corollary 2.1 (NATURAL TOWER PERTURBATION)

Suppose the covers, \(s\), \(T\), and chosen matrices \(K\) commute with every
reduction in a matched inverse system.  Then the maps \(s_T\) in (1.9)
commute with reduction and define one based lift of \(B+T\) on the completed
tower.

#### Proof

Every partial polynomial in \(K\) commutes with reduction.  Passage to the
complete limit preserves this equality, so the series (1.8) and its
composition with \(s\) are natural. \(\square\)

An independently selected solution of (1.7) at every finite level is not
enough.  Either one completed \(K\) or compatible finite matrices must be
retained.

## 3. Source of the R07 transport operator

Let \(w_1\) be the word after the first depth-one correction.  The literal
Fox Jacobian at \(w_1\) differs from the roof-fixed associated-graded
Jacobian \(B\) because each occurrence prefix has acquired a depth-one
factor.  On a new correction \(a\in J^rA\), this difference has depth at
least \(r+1\).  Its linear part is the candidate operator

\[
 T_{w_1}:A\longrightarrow L.
\tag{3.1}
\]

V266 Lemma 5.1 shows that for \(r\geq2\), terms with two occurrences of the
new correction have depth at least \(r+2\).  Moreover, replacing \(w_1\) by
\(w_1u\) with \(u\) of depth at least two changes the linear prefix transport
on a depth-\(r\) correction only in depth at least \(r+2\).  Consequently the
immediately following layer has the schematic form

\[
 [\Phi(wc)-\Phi(w)]_{r,r+1}
 =
 [Ba+T_{w_1}a]_{r,r+1},
\tag{3.2}
\]

while the omitted new-new and later-base terms skip that following layer.

Equation (3.2) is a degree statement, not yet a construction of one
continuous \(\Lambda\)-linear \(T_{w_1}\).  Actual application of Theorem 1.1
requires:

1. literal collection of all transported-prefix terms with H1/H2/pentagon
   tags and printed order;
2. proof that their maps are compatible across every degree and quotient;
3. proof of \(\Lambda\)-linearity on the actual common-word module;
4. proof that their values lie in the same localized module \(L\); and
5. word-bearing coordinates \(K(e_i)\) satisfying (1.7).

Failure of any item leaves the transported-linear recurrence open; it may
not be hidden in an unlabeled higher-order remainder.

## 4. Interaction with the nonlinear completion

Suppose v319's localization hypotheses hold for \(L\), and the actual
transport operator passes Section 3.  Replace \(s\) by \(s_T\).  Then every
active residual has a based preimage under the full transported linear part
\(D=B+T\).  At depths \(r\geq2\), v266 places the terms with two new
correction occurrences in \(J^{r+2}L\).  Thus the Hensel recursion has no
unresolved transported-linear gate at the immediately following depth.

This does not by itself prove localization stability for the genuinely
nonlinear terms.  V319 still requires them to remain in \(L\).  The logical
division is:

\[
\boxed{
\begin{aligned}
\text{linear roof lift} &\quad Bs=q,\\
\text{transport repair} &\quad (B+T)s_T=q,\\
\text{nonlinear closure} &\quad Q(\text{legal corrections})\subseteq L.
\end{aligned}}
\tag{4.1}
\]

The first two rows are finite based-Neumann problems.  The third is the
formation/Brunnian localization problem and must not be inferred from them.

For the narrow pointed-cyclic route, Theorem 1.1 applies only if the
transported terms preserve the chosen cyclic module with retained
coefficients.  Otherwise the larger localized route of v319 is required.

## 5. Exact certificate boundary

After the first actual word-bearing correction is known, a transported
Jacobian receipt should:

1. derive \(T\) independently from literal occurrence prefixes;
2. show one-depth raising on every registered source generator;
3. evaluate \(Ts(e_i)\) in the full localized target;
4. return \(K(e_i)\in JF\) with direct equality \(qK(e_i)=Ts(e_i)\);
5. materialize the finite Neumann polynomial for each finite quotient;
6. replay \((B+T)s_T(e_i)=q(e_i)\) in every tagged block; and
7. reject mutations of a prefix, sign, occurrence order, \(K\)-coordinate,
   source ancestry, or reduction map.

The pending A0/A3/A4 data are still needed to identify the literal first
word and target.  No present receipt computes \(T\) or \(K\).

    BASED FILTRATION-RAISING PERTURBATION LEMMA:     PAPER PROOF
    ONE ERROR MATRIX ABSORBS TRANSPORTED JACOBIAN:  PAPER PROOF
    NATURAL MATRICES GIVE ONE COFINAL LIFT:         PAPER PROOF
    ACTUAL CONTINUOUS R07 TRANSPORT OPERATOR T:     NOT CONSTRUCTED
    ACTUAL WORD-BEARING TRANSPORT MATRIX K:         NOT COMPUTED
    NONLINEAR LOCALIZATION STABILITY:               OPEN
    COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS: NONE

R07_BASED_TRANSPORT_PERTURBATION_V320_PAPER_GRADE

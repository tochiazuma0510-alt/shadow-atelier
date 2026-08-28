# R07 Boolean-free actual A5/A6 compiler v283

Author: Sol / 2026-08-29

Status: paper composition theorem and implementation contract. V242 gives
the full-occurrence joint closure, v280 derives the anchor, adapted basis,
and local A3 base point from accepted inputs, and v281 gives the factored
positive pair language. This note proves that those three constructions form
one deterministic Boolean-free A5 compiler and that changing the endpoint
base point does not change the MEMBER/NONMEMBER decision. No actual A3 or A4
positive package, A5 terminal, A6 pair polynomial, compatible lift, fake
certificate, or Ihara witness is declared. verified=false.

## 1. Accepted input boundary

Fix the first relative edge

\[
 F(x,y)\mathrel{\mathop{\twoheadrightarrow}^{\rho _1}}\Delta _1
 \mathrel{\mathop{\twoheadrightarrow}^{\pi}}\Delta _0
\tag{1.1}
\]

and the matching quotient

\[
 q:\Delta _1\twoheadrightarrow D_1,\qquad
 K=\ker\pi,\qquad q(K)=\langle z_0\rangle\cong C_3.
\tag{1.2}
\]

The compiler accepts only one common, authenticated dependency cone:

1. the task198 roof/tower and complete boundary authority;
2. positive A2 and A3 packages, including the canonical coefficient
   \(\lambda=\sum_g\lambda_g g\);
3. task192 and task193 literal rows and their independent checks; and
4. an accepted A4 producer/checker pair containing the complete ordered
   word-bearing basis \((u_i,k_i)_{1\le i\le t}\) of \(K\).

Every package is bound to the same literal lower word, maps, typed
occurrences, and roof/tower identities. Hash equality authenticates bytes but
does not replace word, group, row, endpoint, or span replay.

An asserted anchor dictionary, a supplied base-pair roster, copied replay
Booleans, and the width-13 frozen SELFTEST cases are outside this trust
boundary.

## 2. Deterministic preprocessing

For each accepted A4 basis word, independently recompute

\[
 \rho _1(u_i)=k_i,\qquad \rho _0(u_i)=1,\qquad
 q(k_i)=z_0^{a_i},\quad a_i\in\mathbf F_3.
\tag{2.1}
\]

Let

\[
 j=\min\{i:a_i\ne0\},\qquad e=a_j^{-1},\qquad
 u_*=\operatorname{red}(u_j^e),\qquad k_*=k_j^e.
\tag{2.2}
\]

For \(i\ne j\), put

\[
 \widetilde u_i=\operatorname{red}(u_i u_*^{-a_i}),\qquad
 \widetilde k_i=k_i k_*^{-a_i}.
\tag{2.3}
\]

By v280, \(k_*,(\widetilde k_i)_{i\ne j}\) is an ordered basis of
\(K\), \(q(k_*)=z_0\), and \(q(\widetilde k_i)=1\). The consumer computes
the change matrix and inverse and replays both directions. No supplied
least-index, exponent, word, group value, or matrix controls acceptance.

For every nonzero A3 coefficient, derive the canonical normal-form section
\(s(g)\) from the authenticated \(D_1\) key and construct

\[
 \widetilde\kappa _0
 =\sum_{\lambda_g\ne0}\lambda_g
  \bigl(\operatorname{red}(s(g)u_*)-s(g)\bigr).
\tag{2.4}
\]

The two endpoints of every pair in (2.4) have equal \(\Delta _0\)-image,
and its \(D_1\)-image is \(\lambda(z_0-1)\). Thus the actual image
\(\kappa _0\in I\) is an endpoint base point for the A3 target.

Finally reconstruct, from task192/task193 and the complete boundary oracle,

\[
 d_1=-\mathscr D_1(g_{760}),\qquad
 e_1=-\beta^{193}_1.
\tag{2.5}
\]

Neither row is replaced by a cycle; the noncycle endpoint identity of v242
is replayed directly.

## 3. Base-point invariance

Let

\[
 \Phi:I\longrightarrow E_1^{\rm blk},\qquad
 H=\ker\Phi,\qquad Hd_1=\{\theta d_1:\theta\in H\}.
\tag{3.1}
\]

For any endpoint base point \(\kappa\in I\) with
\(\Phi(\kappa)=\bar\epsilon _1\), define

\[
 r(\kappa)=e_1-\kappa d_1.
\tag{3.2}
\]

### Theorem 3.1 (BASE-POINT INDEPENDENCE)

If \(\kappa\) and \(\kappa'\) have the same \(\Phi\)-image, then

\[
 \boxed{r(\kappa)\in Hd_1\quad\Longleftrightarrow\quad
        r(\kappa')\in Hd_1.}
\tag{3.3}
\]

#### Proof

The difference \(\delta=\kappa'-\kappa\) belongs to \(H\). Hence
\(\delta d_1\in Hd_1\), while

\[
 r(\kappa')=r(\kappa)-\delta d_1.
\tag{3.4}
\]

Membership in the subspace \(Hd_1\) is unchanged by translating by one of
its elements. \(\square\)

Consequently v280's locally constructed base point may replace the older
\([x,y]^3\)-based representative without changing whether a pointed
multiplier exists. The actual MEMBER ancestry changes in the expected way,
so it must still be replayed.

## 4. Adapted full-occurrence closure

Let \(w\) be the authenticated eleven-occurrence vector and let \(C\) be
the printed block map. Before applying \(C\), form the seeds

\[
 \widehat v_*=
 \bigl((k_*-1)d_1,(k_*-1)\mathbin\odot w\bigr),
\tag{4.1}
\]

\[
 \widehat v_i=
 \bigl((\widetilde k_i-1)d_1,
       (\widetilde k_i-1)\mathbin\odot w\bigr),\qquad i\ne j.
\tag{4.2}
\]

Close their span under the simultaneous marked
\(x^{\pm1},y^{\pm1}\)-actions, retaining literal coefficient ancestry for
every accepted and dependent candidate.

### Theorem 4.1 (BOOLEAN-FREE COMPLETE JOINT IMAGE)

At queue exhaustion the resulting span is

\[
 \boxed{
 \widehat L=
 \{(\theta d_1,\theta\mathbin\odot w):\theta\in I\}.}
\tag{4.3}
\]

Exactly one initial seed, \(\widehat v_*\), can have a nonzero occurrence
endpoint. The other \(t-1\) seeds remain mandatory because their pointed
coordinates generate the rest of the relative ideal image.

#### Proof

The adapted family is a basis of \(K\), so

\[
 I=A(k_*-1)+\sum_{i\ne j}A(\widetilde k_i-1).
\tag{4.4}
\]

Both coordinates before \(C\) are \(A\)-linear. Closure under the marked
generators therefore gives both containments in (4.3), as in v242
Theorem 3.1. The occurrence action factors through \(q\); v280 gives
\(q(k_*)=z_0\) and \(q(\widetilde k_i)=1\), proving the endpoint
assertion. \(\square\)

It is invalid to apply \(C\) before closure. Equal printed-block sums do not
identify distinct occurrence actions.

## 5. One-pass retained-basis compiler

Let a chronological candidate have raw joint row \(v\). Maintain a sparse
retained basis \(R_1,\ldots,R_r\) with coefficient transforms to the raw
candidate roster. A single reduction returns

\[
 v=\sum_{\ell=1}^r c_\ell R_\ell+r_v.
\tag{5.1}
\]

If \(r_v=0\), retain the dependent relation. If \(r_v\ne0\), normalize it
once, extend every old transform by zero, append the new raw candidate, and
enqueue exactly the new pivot. This single operation supplies membership,
remainder, coefficients, and insertion; a preceding contains reduction is
mathematically redundant.

### Lemma 5.1 (RETAINED ANCESTRY INVARIANT)

After every candidate, each normalized pivot and every dependent record
replays exactly from the chronological raw roster, with all coefficients in
canonical \(\mathbf F_3\). Queue exhaustion is therefore a proof of the
complete span (4.3), not merely a rank assertion.

#### Proof

Induct on the candidate ordinal. Pivot subtraction is applied to the row and
its coefficient transform with the same scalar. A nonzero remainder is
scaled in both components and appended with its direct raw coefficient; a
zero remainder retains (5.1). Padding old transforms by zero preserves all
earlier equalities. \(\square\)

A structurally independent checker uses a different pivot direction,
reconstructs the raw candidate stream from original inputs, and proves
two-way span containment. It does not import producer pivots, caches,
transcripts, Booleans, or DAG states.

## 6. Post-\(C\) slice and exact A5 terminal

Only after the queue exhausts, apply \(C\) to the occurrence coordinate and
compute the full nullspace

\[
 N=\left\{a:C\left(\sum_\ell a_\ell\widehat\eta_\ell\right)=0\right\}.
\tag{6.1}
\]

For a basis of \(N\), reconstruct both

\[
 h_a=\sum_\ell a_\ell z_\ell,\qquad
 \vartheta_a=\sum_\ell a_\ell\theta_\ell.
\tag{6.2}
\]

Then reduce

\[
 r_0=e_1-\kappa _0d_1
\tag{6.3}
\]

against the independently reconstructed span of the \(h_a\).

- MEMBER supplies coefficients with
  \(r_0=\theta d_1\), \(\theta\in H\), and hence
  \(\mu_1=\kappa _0+\theta\).
- NONMEMBER supplies a functional annihilating both independently
  reconstructed \(Hd_1\) spans and pairing to one with \(r_0\).

NONMEMBER is a theorem only for the fixed authenticated lower word and
input cone. Rank equality, a producer Boolean, or an incomplete action queue
is not a terminal.

## 7. Canonical A6 handoff

On MEMBER, expand only the retained coefficient ancestry used by
\(\mu_1\). Every term has the form

\[
 c(Au-A)=cA(u-1),
\tag{7.1}
\]

where \(u\) is one adapted A4 kernel word and \(A\) is a literal prefix
obtained from either the local base point or the marked closure ancestry.

Store the polynomial as canonical records

    (coefficient, prefix_DAG_node, kernel_word_index)

with an authenticated parent/literal-letter prefix DAG and kernel-word
dictionary. Distinct literal prefixes remain distinct even if they have the
same finite-shadow value. Producer and checker reconstruct
\(\operatorname{red}(Au)\), \(A\), their two \(\rho_0\)-endpoints, their
\(\rho_1\)-values, and the complete \(\mu_1\) equations.

This is an A6 handoff, not the A7 exact-PB result. A later positive ZERO must
expand every literal pair, recompute all three exact PB chains and their
\(D_1\)-endpoints with a helper-nonshared checker. A named NONZERO rejects
only that candidate multiplier.

## 8. Finite work and honest stopping

Let \(W\) be the actual joint-row width, \(N\) the chronological candidate
count, \(r\) the terminal joint rank, \(d=\dim N\), \(h=\dim Hd_1\),
\(p\) the number of used prefix-DAG edges, and \(L_K\) the total length of
used kernel words.

Before intrinsic boundary reduction, preprocessing is linear in the accepted
A4 word data and A3 support. The retained sparse closure has the generic
dense upper bound

\[
 O\bigl(N(Wr+r^2)\bigr),
\tag{8.1}
\]

with lower actual sparse work metered separately. Post-\(C\), nullspace,
slice reconstruction, target solve, and two-way checks are polynomial in
\(r,d,h,W\). The compressed MEMBER handoff evaluates each prefix-DAG edge
and used kernel word once per typed occurrence, plus one contribution per
actual factored support term.

Caps are checked before queue insertion, elimination, ancestry expansion,
canonicalization, and serialization. A cap emits a sealed replayable
UNKNOWN_RESOURCE; malformed or absent authority emits UNKNOWN_INPUT.
Neither changes a mathematical numerator. Checkpoints bind the immutable
input cone, next ordinal, raw roster, rebuildable echelon, queue head,
ancestry DAG, phase, and counters.

## 9. Fixed frontier

    V242 + V280 + V281 BOOLEAN-FREE COMPOSITION:       PAPER PROOF
    ENDPOINT BASE-POINT CHOICE INVARIANCE:             PAPER PROOF
    ADAPTED SEEDS GIVE COMPLETE JOINT IMAGE:           PAPER PROOF
    ONE-PASS RETAINED-BASIS COMPILER:                  PAPER PROOF
    POSITIVE MEMBER -> FACTORED A6 LANGUAGE:           PAPER PROOF
    ACTUAL POSITIVE A3 PACKAGE:                        NOT AVAILABLE
    ACTUAL ACCEPTED A4 WORD-BEARING BASIS:             NOT AVAILABLE
    ACTUAL A5 CLOSURE / MEMBER OR NONMEMBER:           NOT COMPUTED
    ACTUAL A6 PAIR POLYNOMIAL / A7 EXACT PB:           NOT COMPUTED
    COMPATIBLE LIFT / FAKE / IHARA:                    NOT CONSTRUCTED

R07_BOOLEAN_FREE_ACTUAL_A5_A6_COMPILER_V283_PAPER_GRADE

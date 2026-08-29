# R07 zero-base Boolean-free A5/A6 specialization (v345)

## 0. Scope

Actual run `33244921126` cross-checks the projected A3 target and its MEMBER
coefficient as zero.  V344 records the nonlinear A0/task193 boundary.  This
note specializes the valid Boolean-free compiler v283 to that actual zero
base.  It removes the nonzero projected-generator anchor, adapted A4 basis,
and local A3 base-pair construction from the positive route.

It does not remove the complete A4 homogeneous closure or the literal
A0/task193 row.  No A5 terminal, A6 polynomial, compatible lift, fake, or
Ihara witness is asserted.  `verified=false`.

## 1. The affine endpoint fibre is already linear

Let

\[
 I=\ker\bigl(\mathbf F_3[\Delta_1]\to
                  \mathbf F_3[\Delta_0]\bigr),
 \qquad
 \Phi:I\to E_1^{\rm blk},
 \qquad H=\ker\Phi.
\tag{1.1}
\]

The accepted actual A3 equality is

\[
 \bar\epsilon_1=0=\Phi(0).
\tag{1.2}
\]

Consequently

\[
 \boxed{\Phi^{-1}(\bar\epsilon_1)=H,\qquad \kappa_0=0.}
\tag{1.3}
\]

There is no affine translation to construct.  In particular, v283's
least-index nonzero projected exponent, inverse scalar, anchor word \(u_*\),
adapted basis, and local pairs
\(s(g)u_*-s(g)\) are absent from this actual branch.  The empty pair roster
is the canonical literal representation of \(\kappa_0\).

## 2. Original A4 words suffice

Condition on an independently accepted A4 package with ordered word-bearing
basis

\[
 K=\langle k_1,\ldots,k_t\rangle_{\mathbf F_3},
 \qquad k_i=\rho_1(u_i),
 \qquad \rho_0(u_i)=1.
\tag{2.1}
\]

Let \(d_1\) be the actual pointed row and \(w\) the authenticated eleven-
occurrence vector.  For each original A4 basis word form

\[
 \widehat v_i=
 \bigl((k_i-1)d_1,(k_i-1)\mathbin\odot w\bigr).
\tag{2.2}
\]

Close their span under the simultaneous marked
\(x^{\pm1},y^{\pm1}\)-actions before applying the printed block map \(C\).

### Theorem 2.1 (ZERO-BASE UNADAPTED COMPLETE CLOSURE)

At queue exhaustion the retained span is

\[
 \boxed{
 \widehat L=
 \{(\theta d_1,\theta\mathbin\odot w):\theta\in I\}.}
\tag{2.3}
\]

After applying \(C\), the nullspace of the occurrence component reconstructs
exactly

\[
 \boxed{Hd_1=\{\theta d_1:\theta\in H\}.}
\tag{2.4}
\]

#### Proof

Because (2.1) is a basis of the elementary-abelian relative kernel,

\[
 I=\mathbf F_3[\Delta_1]
       \langle k_i-1:1\le i\le t\rangle.
\tag{2.5}
\]

Both coordinates in (2.2) are module-linear before \(C\).  Closing under
the marked generators therefore gives all and only (2.3), exactly as in v283
Theorem 4.1; a change to an adapted basis is an invertible preprocessing step,
not a completeness premise.  The occurrence component has zero printed
image precisely when \(\Phi(\theta)=0\).  Retaining the same ancestry in the
first component proves (2.4).  \(\square\)

Thus no projected exponent \(a_i\) is needed for the A5 closure in this zero-
base branch.  Roof, upper-shadow, and word ancestry checks in (2.1) remain
mandatory.

## 3. Exact A5 terminal for one literal lower word

For one literal A0 word \(c\), let task193 independently reconstruct

\[
 e_1(c)=-\beta^{193}_1(c).
\tag{3.1}
\]

Equivalently, with v344 notation,

\[
 e_1(c)=d_1-\mathscr B(c).
\tag{3.2}
\]

V283's target reduction now contains no base-point product:

\[
 r_0=e_1(c)-\kappa_0d_1=e_1(c).
\tag{3.3}
\]

### Corollary 3.1 (ZERO-BASE A5 TEST)

An endpoint-compatible pointed multiplier exists exactly when

\[
 \boxed{e_1(c)\in Hd_1.}
\tag{3.4}
\]

If accepted ancestry gives

\[
 e_1(c)=\theta d_1,
 \qquad \theta\in H,
\tag{3.5}
\]

then

\[
 \boxed{\mu_1=\theta.}
\tag{3.6}
\]

The equivalent preselection statement is v344's nonlinear condition
\(d_1-\mathscr B(c)\in Hd_1\).  No linearity in \(c\) is used.

## 4. A6 handoff has no base-pair summand

On MEMBER, expand only the closure ancestry used by \(\theta\).  Every term
has v283's factored form

\[
 a(Au_i-A)=aA(u_i-1),
\tag{4.1}
\]

where \(u_i\) is an original A4 kernel word.  There are no local A3
\(s(g)u_*-s(g)\) terms.  Hence the canonical A6 record language reduces to

```text
(coefficient, prefix_DAG_node, original_A4_kernel_word_index)
```

with the usual literal-prefix, two-endpoint, upper-shadow, endpoint-equation,
and action-equation replay.  This is still only the A6 handoff; the three
exact PB endpoint computations remain A7.

## 5. Actual implementation consequence

A zero-base successor to task346 should consume:

1. the cross-checked A3 receipt/verdict and directly replay that target,
   `lambda`, and `kappa` are zero;
2. the accepted A4 ordered word-bearing basis, without deriving an anchor or
   adapted change matrix;
3. task198's complete occurrence/boundary authority; and
4. one literal A0/task193 owner, or the full v308 nonlinear state owner.

It should reject any supplied anchor, adapted basis, or nonempty A3 base-pair
roster as the wrong actual-class ABI.  The producer and checker independently
construct (2.2), exhaust the full pre-\(C\) action closure, reconstruct
\(Hd_1\), and decide (3.4).

```text
ACTUAL A3 AFFINE BASE:                         ZERO / CROSS-CHECKED
NONZERO z0 ANCHOR AND ADAPTED BASIS:           REMOVED FOR THIS BRANCH
LOCAL A3 BASE-PAIR ROSTER:                     EMPTY
ORIGINAL A4 WORD BASIS -> FULL JOINT IMAGE:    PAPER PROOF
ZERO-BASE A5 TEST e1(c) in H d1:               PAPER PROOF
MEMBER -> mu1=theta AND FACTORED A6 RECORDS:   PAPER PROOF
ACTUAL ACCEPTED A4 / LITERAL A0+TASK193:       STILL REQUIRED
ACTUAL A5/A6 / EXACT PB / COFINAL LIFT:        NOT YET ESTABLISHED
FAKE / IHARA WITNESS:                          NOT YET ESTABLISHED
```

`R07_ZERO_BASE_BOOLEAN_FREE_A5_A6_SPECIALIZATION_V345_PAPER_GRADE`

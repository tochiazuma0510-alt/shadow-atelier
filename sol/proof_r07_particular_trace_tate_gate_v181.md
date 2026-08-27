# R07 particular trace Tate gate v181

Author: Sol / 2026-08-28

Status: paper theorem and sharper successor contract.  It replaces the
relative-freeness sufficient condition of v179 by an exact test for one
actual roof dual.  The test uses the kernel of the primal norm, and at the
first Frattini successor that norm has the factored form proved in v180.
No actual R07 norm kernel has yet been computed.  No compatible lift, fake
certificate, or Ihara witness is declared.

## 1. Primal and dual norm operators

Let \(k=\mathbf F_3\), let \(K\) be a finite 3-group, and let \(M\) be a
finite-dimensional left \(kK\)-module.  Define

\[
 N_Mm=\sum_{a\in K}am.
\tag{1.1}
\]

On \(M^*\), use the contragredient left action

\[
 (a\lambda)(m)=\lambda(a^{-1}m).
\tag{1.2}
\]

The dual norm is therefore

\[
 (N_{M^*}\lambda)(m)
 =\sum_{a\in K}\lambda(a^{-1}m).
\tag{1.3}
\]

### Lemma 1.1 (NORM TRANSPOSE)

Under the perfect pairing \(M^*\times M\to k\),

\[
 \boxed{
 (N_{M^*}\lambda)(m)=\lambda(N_Mm).}
\tag{1.4}
\]

Consequently

\[
 \boxed{
 \operatorname{im}N_{M^*}
 =\operatorname{Ann}_{M^*}(\ker N_M).}
\tag{1.5}
\]

#### Proof

Inversion permutes the elements of \(K\), so

\[
 \sum_{a\in K}a^{-1}m=\sum_{a\in K}am=N_Mm,
\tag{1.6}
\]

which proves (1.4).  For any linear map between finite-dimensional vector
spaces, the image of its transpose is the annihilator of its kernel.  Apply
that fact to \(N_M\). \(\square\)

## 2. Exact particular-dual trace criterion

Let

\[
 r:M\twoheadrightarrow W
\tag{2.1}
\]

be a reduction on which \(K\) acts trivially downstairs, and fix one scalar
dual \(\varphi\in W^*\).  Put

\[
 \psi=\varphi\circ r\in M^*.
\tag{2.2}
\]

The v178 change-of-level problem is to find \(\varphi'\in M^*\) such that

\[
 N_{M^*}\varphi'=\psi.
\tag{2.3}
\]

### Theorem 2.1 (PARTICULAR TRACE GATE)

Equation (2.3) has a solution if and only if

\[
 \boxed{
 \varphi(rm)=0\quad\text{for every }m\in\ker N_M.}
\tag{2.4}
\]

On success, any exact linear preimage in (2.3) is a trace-compatible
successor dual.  On failure, one literal \(m\) satisfying

\[
 N_Mm=0,
 \qquad \varphi(rm)\ne0
\tag{2.5}
\]

is a complete obstruction to lifting this particular dual.

#### Proof

By Lemma 1.1, (2.3) is solvable exactly when
\(\psi\in\operatorname{Ann}(\ker N_M)\).  Substituting (2.2) gives
(2.4).  Equation (2.5) separates \(\psi\) from the entire image of the
dual norm, so it is a complete linear obstruction. \(\square\)

This theorem is strictly more targeted than asking whether all invariant
duals lift.  A nonprojective module can have a nonzero trace obstruction
space while the one actual \(\varphi\) still satisfies (2.4).

## 3. The load-bearing Tate quotient

Let \(J_K\) be the augmentation ideal.  Since \(K\) acts trivially on
\(W\),

\[
 r((a-1)m)=0,
 \qquad \psi(J_KM)=0.
\tag{3.1}
\]

Moreover,

\[
 N_M(a-1)=0,
\tag{3.2}
\]

so \(J_KM\subseteq\ker N_M\).  Hence only the quotient

\[
 \boxed{
 \widehat H^{-1}(K,M)=\ker N_M/J_KM}
\tag{3.3}
\]

can obstruct (2.3).

### Corollary 3.1 (ACTUAL TATE-CLASS TEST)

The functional \(\psi=\varphi\circ r\) descends to a functional on
\(\widehat H^{-1}(K,M)\), and (2.3) is solvable exactly when that descended
functional is zero.

#### Proof

Equation (3.1) gives descent, and Theorem 2.1 says precisely that the
functional must vanish on all of \(\ker N_M\). \(\square\)

This is the finite duality behind the class in
\(\widehat H^0(K,M^*)\) from v179.  It also explains why a raw coordinate
test is unsafe: the functional must first descend through the complete
presentation boundary quotient \(M\).

## 4. Recovery of the projective selector

If \(M\cong(kK)^s\), then

\[
 \ker N_M=J_KM.
\tag{4.1}
\]

Indeed, on one regular summand \(kK\), the norm image is the one-dimensional
span of \(\sum_{a\in K}a\), so its kernel has dimension \(|K|-1\); it
contains the augmentation ideal, which has the same dimension.  Take direct
sums for general \(s\).

Therefore every \(\psi\) from (2.2) automatically satisfies (2.4), recovering
v179 Theorem 2.1.  The advantage of Theorem 2.1 above is that it does not
require (4.1): it tests the actual functional on the possibly nonzero quotient
(3.3).

## 5. First-Frattini sparse form

For the first genuine successor,

\[
 K=\langle s_1,\ldots,s_t\rangle\cong(C_3)^t.
\tag{5.1}
\]

V180 Proposition 3.1 gives

\[
 \boxed{
 N_M=\prod_{i=1}^t(s_i-1)^2.}
\tag{5.2}
\]

Thus the complete particular trace decision can be made without enumerating
\(3^t\) group elements:

1. construct the product (5.2) from the registered generator action
   matrices;
2. row-reduce it to obtain a basis of \(\ker N_M\);
3. reduce those basis vectors through the exact map \(r\) and pair with the
   named roof dual \(\varphi\);
4. if all values vanish, solve the transposed system
   \(N_M^{\mathsf T}x=\psi\) and retain one literal \(x\);
5. otherwise retain the first canonical vector satisfying (2.5).

The independent checker can use the same theorem with a different sparse
partition and pivot order.  It must replay the full factored product, not
trust a claimed norm-kernel basis.

## 6. Tower consequence and its exact limitation

At adjacent rungs set \(M=W_{n+1}\), \(W=W_n\), and
\(r=r_n\).  Starting from \(\varphi_0\), apply Theorem 2.1 recursively.
If (2.4) holds at every rung and one canonical preimage is retained each
time, the resulting family is trace-compatible; v178 then gives one
continuous \(\Xi\)-linear functional on the inverse limit.

A positive first successor proves only that the actual roof dual avoids the
first Tate obstruction.  To stop rung-by-rung testing one still needs a
structural theorem making the descended functionals on (3.3) vanish
naturally at every rung, such as v179's completed-free presentation or a
class-specific universal norm homotopy.  Theorem 2.1 identifies exactly what
that structural theorem must kill.

Once an inverse-limit functional is obtained, v177 still requires either
injectivity on the actual defect subsystem or direct cyclic membership of
the corrected residual.  Trace compatibility alone does not imply that
multiplier identity.

## 7. Exact R07 certificate contract

After a positive task193 production receipt, the smallest new certificate is
not a classification of the whole successor module.  It is:

1. the complete boundary quotient \(M=W_1\), its reduction \(r_0\), and the
   elementary-abelian diagonal kernel generators;
2. one authenticated roof scalar dual \(\varphi_0\) annihilating the complete
   roof boundary image;
3. the factored primal norm (5.2) and a complete kernel basis;
4. every value \(\varphi_0(r_0m_j)\) on that basis;
5. either a direct successor dual preimage and trace replay, or one vector
   (2.5); and
6. covariantized values on the actual original target and corrected residual.

If the particular trace gate passes, the freeness test of v179--v180 remains
useful as the stronger route to automatic continuation.  If it fails, only
that chosen roof dual is blocked; another boundary dual or the universal
word-polynomial route of v175 may still succeed.

## 8. Fixed frontier

```text
NORM-TRANSPOSE / KERNEL-ANNIHILATOR IDENTITY:    PAPER_PROOF
PARTICULAR TRACE GATE:                           PAPER_PROOF
TATE H^{-1} ACTUAL OBSTRUCTION QUOTIENT:         PAPER_PROOF
FACTORED FIRST-FRATTINI IMPLEMENTATION:           SPECIFIED
R07 FIRST SUCCESSOR PARTICULAR TRACE TEST:        NOT COMPUTED
R07 NATURAL ALL-RUNG TATE VANISHING:              NOT PROVED
INJECTIVITY OR ACTUAL CYCLIC MEMBERSHIP:           OPEN
COMPATIBLE COFINAL LIFT / FAKE / IHARA:            NOT DECLARED
```

`R07_PARTICULAR_TRACE_TATE_GATE_V181_PAPER_GRADE`

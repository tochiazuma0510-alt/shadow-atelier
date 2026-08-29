# R07 pre-A0 MEMBER to A4-anchored literal seed repair (v305)

## 0. Scope and erratum

V303 correctly proves that the projected A3 interface is independent of the
unknown A0 correction.  V304 also correctly observes that a coefficient-
bearing task359 MEMBER fixes one projected coefficient

\[
 \kappa_D=\lambda(z_0-1)\in\mathbf F_3[D_1].
\tag{0.1}
\]

Its literalization, however, used the source word
\(z=[x,y]^3\) and asserted that this word lies in the actual roof kernel.
That assertion is false: v247 independently replays the authenticated
task176 roof evaluator and finds the literal cube nonidentity in all ten
typed coordinates.  Thus v304 Lemma 2.1, formula (2.3), Theorem 3.1 as
written, and the claim that task359 alone makes the seed word-bearing are
superseded by this note.

The repair is exact and finite.  The projected coefficient from task359 is
retained, but its generator \(z_0-1\) is lifted through the actual
word-bearing A4 kernel basis.  This restores the all-A0 transfer without
restoring an A2 dependency.  No MEMBER result, A4 basis, pointed multiplier,
compatible lift, fake certificate, or Ihara witness is asserted here.

## 1. Projected generator versus actual roof kernel

Retain

\[
 F(x,y)\twoheadrightarrow\Delta_1\mathrel{\mathop{\twoheadrightarrow}^{\pi}}
 \Delta_0,
 \qquad K=\ker\pi,
 \qquad q:\Delta_1\twoheadrightarrow D_1\cong\mathcal H_2(9),
\tag{1.1}
\]

and put \(z=[x,y]^3\), \(z_0=q(\rho_1(z))=(0,0,3)\).  The valid structural
statement is

\[
 q(K)=\langle z_0\rangle\cong C_3.
\tag{1.2}
\]

It only says that some element of \(K\) maps to \(z_0\).  It does not imply
that the particular source word \(z\) belongs to \(K\).  V247 records the
cross-checked task176 replay

```text
identity_by_coordinate = [false,false,false,false,false,
                          false,false,false,false,false]
joint_blob_sha256       = 1460601df23f2e444d0fc3cad5b13d36e74ff7982c8c4b3551c38796af1d392d
```

and therefore

\[
 \rho_0(z)\ne1.
\tag{1.3}
\]

Consequently the differences \(s(g)z-s(g)\) used in v304 need not lie in
the actual relative ideal.  Equality after projection to \(D_1\) cannot
replace equality at the roof.

## 2. What survives before A4

Let a future accepted task359 MEMBER retain

\[
 \lambda=\sum_{g\in D_1}\lambda_g g,
 \qquad
 \kappa_D=\lambda(z_0-1),
 \qquad
 C(\kappa_D\mathbin\odot w)=\bar\epsilon_1(g_{760}).
\tag{2.1}
\]

V303 gives, for every registered A0 correction \(a\in\Omega\),

\[
 w_a=w,
 \qquad
 \bar\epsilon_1(g_{760}a)=\bar\epsilon_1(g_{760}).
\tag{2.2}
\]

Thus the same projected algebra element \(\kappa_D\) solves the projected
endpoint equation for every A0 correction.  This statement needs neither an
actual A0 word nor A2.  What is unavailable before A4 is a source-word lift
of \(\kappa_D\) in the actual relative ideal.

## 3. The actual A4 anchor

Suppose an independently accepted A4 package supplies an ordered
word-bearing basis

\[
 K=\langle k_1,\ldots,k_t\rangle_{\mathbf F_3},
 \qquad k_i=\rho_1(u_i),
 \qquad \rho_0(u_i)=1.
\tag{3.1}
\]

Write

\[
 q(k_i)=z_0^{a_i},\qquad a_i\in\mathbf F_3.
\tag{3.2}
\]

Because of (1.2), at least one \(a_i\) is nonzero.  Let \(j\) be the least
such index, put \(e=a_j^{-1}\in\mathbf F_3^\times\), and define

\[
 u_*=\operatorname{red}(u_j^e),
 \qquad k_*=k_j^e.
\tag{3.3}
\]

Then

\[
 \boxed{
 \rho_1(u_*)=k_*\in K,
 \qquad \rho_0(u_*)=1,
 \qquad q(k_*)=z_0.}
\tag{3.4}
\]

This is v247's deterministic projected-generator anchor.  All three
equalities in (3.4), rather than only the last one, are load-bearing.

## 4. Corrected all-A0 literal seed theorem

For \(g=(a,b,r)\in D_1\), retain the fixed literal section

\[
 s(g)=x^ay^b[x,y]^r,
 \qquad 0\le a,b,r<9.
\tag{4.1}
\]

Using the authenticated task359 coefficient and the A4 anchor, define

\[
 \boxed{
 \widetilde\kappa_0^{\,*}
   =\sum_{g\in D_1}\lambda_g
       \bigl(s(g)u_*-s(g)\bigr)\in\mathbf F_3[F],
 \qquad
 \kappa_0^*=\rho_{1,*}(\widetilde\kappa_0^{\,*}).}
\tag{4.2}
\]

### Theorem 4.1 (A4-ANCHORED PRE-A0 SEED TRANSFER)

Put

\[
 I=\ker\bigl(\mathbf F_3[\Delta_1]
       \longrightarrow\mathbf F_3[\Delta_0]\bigr),
 \qquad \Phi_a(\kappa)=C(\kappa\mathbin\odot w_a).
\tag{4.3}
\]

Then

\[
 \boxed{
 \kappa_0^*\in I,
 \qquad q_*(\kappa_0^*)=\kappa_D,
 \qquad
 \Phi_a(\kappa_0^*)=\bar\epsilon_1(g_{760}a)
 \quad\text{for every }a\in\Omega.}
\tag{4.4}
\]

The literal polynomial (4.2), including its word-pair partition and
coefficients, is the same for every registered A0 correction.

#### Proof

Equation (3.4) gives

\[
 \rho_0(s(g)u_*)=\rho_0(s(g)),
\tag{4.5}
\]

so every summand in (4.2) is an actual roof-fibre difference and
\(\kappa_0^*\in I\).  Applying \(q_*\rho_{1,*}\) gives

\[
 q_*\rho_{1,*}\bigl(s(g)u_*-s(g)\bigr)=g(z_0-1).
\tag{4.6}
\]

Summation with the authenticated coefficients proves
\(q_*(\kappa_0^*)=\lambda(z_0-1)=\kappa_D\).  The projected endpoint action
factors through this \(D_1\)-image.  Equations (2.1)--(2.2) therefore give

\[
 \Phi_a(\kappa_0^*)
 =C(\kappa_D\mathbin\odot w_a)
 =C(\kappa_D\mathbin\odot w)
 =\bar\epsilon_1(g_{760})
 =\bar\epsilon_1(g_{760}a).
\tag{4.7}
\]

Neither \(\lambda\) nor \(u_*\) depends on \(a\), which proves the final
assertion.  QED.

## 5. Correct dependency cone

The endpoint-base input of the Boolean-free v283 A5 compiler can therefore
be authenticated by

\[
 \boxed{
 \text{task359 MEMBER ancestry}
 +\text{accepted A4 word-bearing basis and anchor}
 \longrightarrow \widetilde\kappa_0^{\,*}.}
\tag{5.1}
\]

Actual A2 is not needed merely to obtain this endpoint base point.  The
remaining actual A5 inputs are the same accepted A4 package and the actual
A0/task193 pointed rows.  Hence the corrected positive dependency cone is

\[
 \boxed{
 \text{positive pre-A0 A3}
 +\text{accepted A4 word-bearing }K
 +\text{actual A0/task193 rows}.}
\tag{5.2}
\]

The order is load-bearing: A4 must precede literalization, even though A3
itself can be computed before A0 and A4.  A2 remains necessary wherever the
full corrected-word package, correction column, or exact PB chains are
consumed.

## 6. Certificate consequence

A positive literal-seed adapter must independently rebuild:

1. the task359 \(\lambda_g\) and its closure ancestry;
2. every A4 basis word and its roof, upper-shadow, and \(D_1\) images;
3. the least-index anchor and all equalities in (3.4);
4. every pair \((s(g)u_*,s(g))\), its coefficient, and its common roof value;
5. the projection replay to \(\lambda(z_0-1)\); and
6. the all-A0 endpoint equality through v303.

Required destructive controls include changing the anchor basis row, its
projected exponent, the inverse scalar, one literal letter of \(u_*\), one
roof value, one \(\lambda_g\), and the orientation of \(u_*-1\).  The
literal cube \([x,y]^3\) is a negative control and must be rejected as an
actual roof-kernel anchor.

## 7. Fixed frontier

```text
TASK359 MEMBER -> PROJECTED KAPPA_D:                 PAPER TRANSFER / ACTUAL UNCOMPUTED
[x,y]^3 AS ACTUAL ROOF-KERNEL ANCHOR:                REJECTED / v247
A4 BASIS -> WORD-BEARING z0 ANCHOR:                  PAPER PROOF / ACTUAL UNCOMPUTED
A3 + A4 -> ALL-A0 LITERAL KAPPA0:                    PAPER PROOF / ACTUAL UNCOMPUTED
A2 DEPENDENCY OF A5 ENDPOINT BASE:                   REMOVED
A4 DEPENDENCY BEFORE LITERALIZATION:                 RETAINED / LOAD-BEARING
ACTUAL A3 / A4 / A0 / TASK193 / A5:                  NOT COMPUTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:              NONE
```

`R07_PRE_A0_MEMBER_TO_A4_ANCHORED_LITERAL_SEED_REPAIR_V305_PAPER_GRADE`

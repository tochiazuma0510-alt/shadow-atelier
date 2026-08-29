# R07 pre-A0 MEMBER-to-literal-seed transfer theorem (v304)

## 0. Scope

V302--v303 show that the complete v216 projected A3 problem is independent
of the still unknown A0 correction.  V238 explains how a positive v216
coefficient can be lifted to a finite roof-fibre word-pair coefficient.  The
remaining dependency question is whether that lift must be rebuilt after A0,
or whether the coefficient ancestry from the pre-A0 computation itself is an
authenticated input to the later pointed gate.

This note proves the latter.  A coefficient-bearing MEMBER certificate for
the projected task359 calculation determines one literal coefficient
\(\kappa _0\) which works for the projected endpoint of every registered A0
correction on the fixed \(g_{760}\) branch.  Thus actual A2 specialization is
not a dependency of the A5 *endpoint base point*.  It remains a separate v220
milestone and remains necessary wherever the full corrected-word package or
exact PB chains are consumed.

No MEMBER result currently exists.  This is a paper dependency theorem, not
an A3, A5, lift, fake, or Ihara terminal.

## 1. Coefficient ancestry at the computational base

Put \(k=\mathbf F_3\), retain

\[
 D_1=\mathcal H_2(9),\qquad
 A=k[D_1],\qquad z_0=[x,y]^3\in D_1,
 \qquad I(R_0)=A(z_0-1),
\tag{1.1}
\]

and let \(w\) be the eleven-occurrence vector reconstructed from fixed
\(g_{760}\) and task198.  A coefficient-bearing positive v216 certificate is
not merely the Boolean `MEMBER`.  Its retained invariant-queue ancestry gives
an explicit

\[
 \lambda=\sum_{g\in D_1}\lambda_g g\in A
\tag{1.2}
\]

such that

\[
 \kappa_D=\lambda(z_0-1),\qquad
 C(\kappa_D\mathbin\odot w)=\bar\epsilon_1(g_{760}).
\tag{1.3}
\]

The representative \(\lambda\) need not be intrinsically unique: right
multiplication by \(z_0-1\) can have a kernel in characteristic three.  The
certificate fixes one representative by its complete source-algebra ancestry
and canonical coefficient collection.  Everything below is relative to that
authenticated representative; no uniqueness claim is needed.

## 2. Deterministic literalization

Let \(F=F(x,y)\), put

\[
 h=[x,y],\qquad z=h^3,
\tag{2.1}
\]

and use the fixed normal-form section

\[
 s(a,b,r)=x^ay^bh^r,qquad
 0\leq a,b,r<9,
\tag{2.2}
\]

from \(D_1\) to \(F\).  Define

\[
 \boxed{
 \widetilde\kappa_0(\lambda)
   =\sum_{g\in D_1}\lambda_g\bigl(s(g)z-s(g)\bigr)
   \in k[F].}
\tag{2.3}
\]

Free reduction and collection modulo three make (2.3) a finite,
deterministic byte-level object once the word and coefficient codecs are
fixed.  Let \(\rho_1:F\twoheadrightarrow\Delta_1\) be the first upper shadow
map and set

\[
 \kappa_0=\rho_{1,*}(\widetilde\kappa_0)\in k[\Delta_1].
\tag{2.4}
\]

### Lemma 2.1 (CERTIFICATE-CANONICAL ROOF-FIBRE LIFT)

Every summand of (2.3) is a roof-fibre pair, \(\kappa_0\) lies in the
relative ideal

\[
 I_0=\ker\bigl(k[\Delta_1]\longrightarrow k[\Delta_0]\bigr),
\tag{2.5}
\]

and its image in \(k[D_1]\) is exactly \(\kappa_D\).

#### Proof

The literal word \(z=[x,y]^3\) maps into the first relative kernel and hence
to the identity in \(\Delta_0\).  Therefore

\[
 \rho_0(s(g)z)=\rho_0(s(g))
\tag{2.6}
\]

for every \(g\), which proves the roof-fibre assertion and (2.5).  Projection
to \(D_1\) sends the same difference to \(g(z_0-1)\); summing with the
coefficients in (1.2) gives (1.3).  QED.

## 3. Transfer to every registered A0 correction

For a registered correction \(a\in\Omega\), write \(f_a=g_{760}a\), and let
\(\Phi_a\) and \(\bar\epsilon_1(f_a)\) denote the v216 endpoint action and
target read through its A3 projection.  V303 Theorem 3.1 identifies that
projection with the computational-base projection.  In particular,

\[
 w_a=w,qquad
 \bar\epsilon_1(f_a)=\bar\epsilon_1(g_{760}),
\tag{3.1}
\]

with the same quotient/action ABI.

### Theorem 3.1 (ONE PRE-A0 LITERAL SEED FOR THE WHOLE A0 BRANCH)

If the projected computational-base calculation has the coefficient-bearing
MEMBER certificate (1.2)--(1.3), then the single coefficient (2.4) satisfies

\[
 \boxed{
   \kappa_0\in I_0,
   \qquad
   \Phi_a(\kappa_0)=\bar\epsilon_1(f_a)
   \quad\text{for every }a\in\Omega.}
\tag{3.2}
\]

The literal polynomial \(\widetilde\kappa_0\), its word-pair partition, and
its coefficients are identical for all \(a\); they need not be recomputed
after selection of an A0 word.

#### Proof

Lemma 2.1 gives \(\kappa_0\in I_0\) and image \(\kappa_D\).  The v214/v238
endpoint action factors through this \(D_1\)-image, so (1.3) gives

\[
 \Phi_a(\kappa_0)
 =C(\kappa_D\mathbin\odot w_a).
\tag{3.3}
\]

Substituting (3.1) and then (1.3) yields the right side of (3.2).  Formula
(2.3) contains no occurrence of \(a\), proving the last assertion.  QED.

### Corollary 3.2 (NO A2 SPECIALIZER IN THE A5 ENDPOINT-BASE DEPENDENCY)

On a positive task359 terminal, the endpoint-base input of v242 can be
authenticated by

\[
 \text{task359 projected A3 receipt}
 +\text{its MEMBER ancestry}
 +\text{the deterministic literalization (2.3)}.
\tag{3.4}
\]

After an A0 word is found, A5 still consumes its actual task193 pointed rows
and the accepted A4 word-bearing kernel.  It does not need an actual A2
two-word specialization merely to reconstruct \(w\), the projected target,
or \(\kappa_0\).  Thus the mathematical A5 dependency cone is shortened to

\[
 \boxed{
   \text{positive A3 literal seed}
   +\text{accepted A4 word-bearing }K
   +\text{actual A0/task193 pointed rows}.}
\tag{3.5}
\]

This does not erase A2.  The full corrected word, correction column, exact PB
chains, and later exact endpoint replay are outside the projection in v303
and must still be authenticated wherever used.

## 4. Executable certificate consequence

A positive task359 successor should preserve, either in its receipt or in one
acyclic deterministic adapter, all of the following:

1. the collected \(\lambda_g\) and its queue ancestry;
2. the exact normal-form and source-word codecs used in (2.2);
3. every pair \((s(g)z,s(g))\), its coefficient, and its common roof value;
4. the projection replay to \(\lambda(z_0-1)\);
5. the occurrence-action replay of (1.3); and
6. mutations of one coefficient, one normal-form exponent, the orientation of
   \(z-1\), one roof-fibre value, and the projected target.

Producer and independent checker must rebuild (2.3) from the MEMBER ancestry;
a digest-only seed is insufficient.  If task359 returns NONMEMBER, this
adapter is not run and the fixed A0 branch is obstructed at A3.

## 5. Fixed frontier

```text
PRE-A0 MEMBER ANCESTRY -> FINITE LITERAL KAPPA0:     PAPER PROOF
THE SAME KAPPA0 WORKS FOR EVERY REGISTERED A0 WORD: PAPER PROOF
A5 ENDPOINT-BASE DEPENDENCY ON ACTUAL A2:           REMOVED
A5 DEPENDENCY ON ACTUAL A0/TASK193 AND A4:           RETAINED
A2 FULL-PACKAGE / EXACT-PB DUTIES:                   RETAINED
ACTUAL TASK359 MEMBER OR NONMEMBER:                  NOT COMPUTED
ACTUAL KAPPA0 / A5 SLICE / MU1 / M:                  NOT COMPUTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:              NONE
```

`R07_PRE_A0_MEMBER_TO_LITERAL_SEED_TRANSFER_V304_PAPER_GRADE`

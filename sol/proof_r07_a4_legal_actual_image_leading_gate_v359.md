# R07 A4 legal actual-image leading gate (v359)

Author: Sol / 2026-08-30

Status: corrective paper theorem after v37, v38, v149, v151, v188,
v231, v260, v263 and v319.  It supersedes v358.  A4 supplies coordinates
for the full first-successor kernel, but the nonlinear Newton source is the
actual legal common-word image, not that whole ambient kernel or its whole
group-algebra ideal.  On the registered relative-formation first edge the
legal value subspace has the closed formula
\(R_S(\Delta _1)\cap K=[R_S(\Delta _0),K]\), so a positive A4 action
receipt reduces its extraction to finite linear algebra.  The physical
residual generators/actions, legal leading-module identification and
localized target have not yet been authenticated.  No compatible lift,
fake certificate or Ihara witness is declared.  `verified=false`.

## 1. Three source objects which must not be identified

Let

\[
 F=F(x,y),\qquad
 \rho_j:F\twoheadrightarrow\Delta_j,\qquad
 \pi:\Delta_1\twoheadrightarrow\Delta_0,\qquad
 \pi\rho_1=\rho_0,
\tag{1.1}
\]

and suppose

\[
 K=\ker\pi
\tag{1.2}
\]

is elementary abelian over \(k=\mathbf F_3\).  Put

\[
 A=k[\Delta_1],\qquad
 I_K=\ker\bigl(A\to k[\Delta_0]\bigr).
\tag{1.3}
\]

If \(k_1,\ldots,k_t\) is any basis of \(K\), then the valid algebraic
identity retained from v358 is

\[
 \boxed{I_K=\sum_{i=1}^t A(k_i-1).}
\tag{1.4}
\]

This is the ambient coefficient ideal used in the A5 Fox calculation of
v188/v231/v242.  It is not, by itself, a nonlinear word-correction domain.

Write \(\widehat F\) for the profinite completion and let \(\Pi_S\) be the
kernel of its maximal no-\(S\) formation quotient, where
\(S=PSL(2,8)\).  There are two smaller finite value spaces:

\[
 \begin{aligned}
 C_{\rm com}
   &=\rho_1\bigl(\ker\rho_0\cap
        \overline{[F,F]}\bigr),\\
 C_{\rm rel}
   &=\rho_1\bigl(\Pi_S\cap\ker\rho_0\bigr).
 \end{aligned}
\tag{1.5}
\]

Here the maps in (1.5) mean the continuous extensions to \(\widehat F\).
The first is the actual common-word value image of v260.  The second is the
registered relative-formation correction image.  V37--v38 give

\[
 \boxed{
 C_{\rm rel}=R_S(\Delta_1)\cap K
 \ \leq\ C_{\rm com}\ \leq\ K.}
\tag{1.6}
\]

Neither inclusion in (1.6) is promoted to equality without a proof.  In
particular, the following inference is invalid:

\[
 \text{A4 computes }K
 \quad\Longrightarrow\quad
 \text{every }k\in K\text{ is a legal nonlinear correction.}
\tag{1.7}
\]

This is exactly the type error in v358.  The A5 coefficient calculation may
still use (1.4); the v319 nonlinear leading solve may not.

## 2. Closed relative source on the actual first edge

Put

\[
 R=R_S(\Delta_0).
\tag{2.1}
\]

### Theorem 2.1 (SUPERPERFECT LEGAL-SOURCE FORMULA)

Assume that \(R\) is superperfect.  Then

\[
 \boxed{C_{\rm rel}=[R,K].}
\tag{2.2}
\]

#### Proof

Apply v151 Theorem 3.1 to the finite extension

\[
 1\longrightarrow K\longrightarrow\Delta_1
 \longrightarrow\Delta_0\longrightarrow1.
\tag{2.3}
\]

It gives

\[
 K\cap R_S(\Delta_1)=[R_S(\Delta_0),K]=[R,K].
\tag{2.4}
\]

The left side is \(C_{\rm rel}\) by (1.6).  \(\square\)

For the authenticated task176 roof, v149 identifies

\[
 R=\widetilde S\cong PSL(2,8),
\tag{2.5}
\]

which is superperfect.  Therefore (2.2) applies to A4 provided the A4
\(\Delta_0\) is authenticated as the same correctly typed joint group and
the A4 \(\Delta_1\to\Delta_0\) is the stated elementary-abelian extension.
The name of a coordinate product is not enough for this type gate.

Let \(s_1,\ldots,s_d\) be word-bearing generators of \(R\), and let
\(S_a\) be their action matrices on the ordered A4 basis of \(K\).  Then

\[
 \boxed{
 C_{\rm rel}=
 \sum_{a=1}^d\operatorname{im}(S_a-I).}
\tag{2.6}
\]

Thus one block echelon computes an exact basis and change-of-basis matrix
inside the A4 coordinates.  If \(u_i\) is the retained word for \(k_i\)
and \(\widetilde s_a\) is the retained word for \(s_a\), each generating
row has literal common-word ancestry

\[
 [\widetilde s_a,u_i]
 \quad\longmapsto\quad
 s_a\cdot k_i-k_i
\tag{2.7}
\]

up to the frozen commutator convention.  It is roof-trivial and has exact
integer exponent sums zero.  Its value lies in \(C_{\rm rel}\).  V37 gives
a preimage in \(\Pi_S\cap\ker\rho_0\) for the same finite value; equation
(2.7) alone must not be relabelled as that particular profinite preimage.

Formula (2.6) removes a formation-residual enumeration.  It does not remove
the need for authenticated word-bearing \(R\)-generators or an equivalent
authenticated action description.  V149 proves that \(R\) exists; its
status line explicitly says those words were not yet materialized.

## 3. Homogeneous side gates and the legal leading ideal

For the relative-formation route, let

\[
 s_j:C_{\rm rel}\longrightarrow T_j
\tag{3.1}
\]

be every *physically registered homogeneous linear* side gate at this edge.
Define

\[
 C_{\rm adm}=C_{\rm rel}\cap\bigcap_j\ker s_j.
\tag{3.2}
\]

Affine prescribed values are target equations and are not silently inserted
into (3.2).  If each \(s_j\) is \(\Delta_0\)-equivariant, then
\(C_{\rm adm}\) is a \(\Delta_0\)-submodule of \(K\).  A basis
\(c_1,\ldots,c_r\), with ancestry retained through (2.6) and the side-gate
echelon, is a complete finite value roster for the homogeneous legal source.

The corresponding leading group-algebra ideal is

\[
 I_{\rm adm}
 =\operatorname{span}_k
   \{g(c-1):g\in\Delta_1,\ c\in C_{\rm adm}\}.
\tag{3.3}
\]

Normality gives the finite generating formula

\[
 \boxed{I_{\rm adm}=\sum_{i=1}^r A(c_i-1).}
\tag{3.4}
\]

The proof is the telescoping identity used in v358, now applied to the
correct subgroup.  Equation (3.4) is useful only after the actual leading
correction module \(A_{\rm legal}/JA_{\rm legal}\) is authenticated as
\(I_{\rm adm}\), or as a specified quotient of it.  That identification is
a separate type gate.  Without it, (3.4) remains a finite ambient model and
is not yet the source of v319.

The direct non-formation route may instead start from \(C_{\rm com}\).
It requires an independent computation of that actual image (for example an
exponent-lattice/kernel calculation).  Theorem 2.1 computes
\(C_{\rm rel}\), not all of \(C_{\rm com}\).

## 4. Correct finite occurrence-image theorem

Let \(\widehat Z\) be the raw, separately tagged occurrence space, and
suppose an authenticated occurrence Jacobian

\[
 \widehat B:I_{\rm adm}\longrightarrow\widehat Z
\tag{4.1}
\]

is \(A\)-linear before printed block summation.  Form the seed columns

\[
 v_i=\widehat B(c_i-1).
\tag{4.2}

Close their span under the simultaneous marked actions
\(x^{\pm1},y^{\pm1}\), retaining coefficient and literal-word ancestry,
until the rank queue is exhausted.

### Theorem 4.1 (LEGAL OCCURRENCE CLOSURE)

The exhausted span is exactly

\[
 \boxed{
 W_{\rm adm}=\operatorname{im}
  (\widehat B|_{I_{\rm adm}}).}
\tag{4.3}

#### Proof

Equation (3.4) writes every input as a finite sum of translates of the
\(c_i-1\).  \(A\)-linearity puts every image in the invariant closure of
the columns (4.2).  Conversely every queued row is obtained from those
columns by the same action and linear combinations, hence remains in the
image.  Finite dimension forces termination.  \(\square\)

This is the valid core of the proposed occurrence compiler.  The seeds are
the legal \(c_i\), not the whole A4 basis \(k_i\).

## 5. The localized target is not an automatic quotient

Let

\[
 L_1=L/JL
\tag{5.1}

be the actual v319 leading localized residual space.  V252 locates intended
residual values in formation and Brunnian intersections, but does not by
itself furnish a projection of an ambient occurrence space onto that
subspace.  Therefore a consumer must authenticate one of:

1. a basis embedding \(\iota:L_1\hookrightarrow\widehat Z\) and a proof
   that \(W_{\rm adm}\subseteq\iota(L_1)\); or
2. a complete coordinate quotient/retraction together with a two-way proof
   that it represents exactly \(L_1\).

Only then is the v319 leading gate the finite equality

\[
 \boxed{W_{\rm adm}=\iota(L_1)}
\tag{5.2}

in case 1, or the corresponding two-way coordinate equality in case 2.
ONTO returns a legal word-bearing preimage for every target basis vector.
NOT ONTO returns a nonzero dual functional on the *actual* \(L_1\), not
merely on a larger raw occurrence space.  A cokernel in \(\widehat Z\) alone
does not prove failure after localization.

V263 still shows that the structural leading map is independent of the
particular A0 correction word.  A0 is needed for the actual residual and
witness replay, not for (2.6), (4.3), or the target-space comparison once
their physical inputs exist.

## 6. Exact effect on the v220 route

A positive A4 terminal supplies the ambient \(K\)-coordinates, action
matrices and word-bearing kernel ancestry.  It then permits, but does not by
itself complete, the following finite chain:

\[
 \boxed{
 K
 \xrightarrow[\text{v151}]{\text{residual action}}
 C_{\rm rel}=[R,K]
 \xrightarrow{\text{side gates}}
 C_{\rm adm}
 \xrightarrow{\text{occurrence closure}}
 W_{\rm adm}
 \mathrel{\mathop{=}^{?}} L/JL.}
\tag{6.1}
\]

The first arrow needs the physical residual action, the second only the
registered gates, the third needs the actual occurrence evaluator, and the
last needs the strict localized target owner.  This is a finite route to the
one all-generator leading solve of v319.  If it is positive and natural
through the registered tower, v319 supplies the uniform nonlinear correction
operator; v357 then handles transported prefixes.  None of those conclusions
follows from the ambient A4 ideal (1.4) alone.

```text
A5 AMBIENT IDEAL I_K FROM THE FULL A4 BASIS:          PAPER PROOF / RETAINED
FULL A4 K AS NONLINEAR LEGAL SOURCE:                  RETRACTED
RELATIVE LEGAL VALUE SOURCE C_rel = R_S(Delta1) cap K: PAPER PROOF / v37
SUPERPERFECT FORMULA C_rel = [R_S(Delta0),K]:          PAPER PROOF / v151
FINITE ACTION-MATRIX EXTRACTION OF C_rel:             PAPER ALGORITHM
PHYSICAL WORD-BEARING RESIDUAL ACTION ON ACTUAL A4 K: NOT MATERIALIZED
LEGAL OCCURRENCE CLOSURE AFTER SOURCE TYPING:          PAPER PROOF
ACTUAL A/JA = I_adm IDENTIFICATION:                    OPEN
ACTUAL L/JL TARGET / STRICT COVER:                     OPEN
ACTUAL LEADING ONTO:                                  NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA WITNESS:               NOT CONSTRUCTED
```

`R07_A4_LEGAL_ACTUAL_IMAGE_LEADING_GATE_V359_PAPER_GRADE`

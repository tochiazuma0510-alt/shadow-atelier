# R07 task395-to-leading-coinvariant quotient bridge v379

Author: Sol / 2026-08-30

Status: final audit candidate correcting rejected v378.  It identifies,
conditional on one named physical enriched ABI, the task395
\(\Delta_1\)-action closure with the image of the completed seed map after
quotienting the actor to the coarse relative coinvariants.  The bridge is a
surjection, not an isomorphism of source action modules, and localization is
used only on the legal image \(W_C\).  This does not prove that the
coinvariant-to-successor comparison is an isomorphism or that the actual
image fills its target.  No compatible lift, fake certificate or Ihara
witness is declared.  \(\mathtt{verified=false}\).

## 1. Fine task395 action versus coarse coinvariant action

Put \(k=\mathbf F_3\).  Retain v372's enriched action group, its relative
kernel, and v377's completed source:

\[
 \widehat P\triangleleft\widehat\Delta_\infty,
 \qquad
 \widehat\Xi=k[[\widehat\Delta_\infty]],
 \qquad
 \widehat J=\ker\bigl(
   \widehat\Xi\longrightarrow
   k[[\widehat\Delta_\infty/\widehat P]]
 \bigr),
 \qquad
 P_C=\widehat\Xi^r.
\tag{1.1}
\]

Let

\[
 G_0=\widehat\Delta_\infty/\widehat P.
\tag{1.2}
\]

On the registered lane, endpoint reduction identifies \(G_0\) with the
coarse simultaneous group \(\Delta_0\).  Hence

\[
 \overline\Xi:=\widehat\Xi/\widehat J\cong k[G_0],
 \qquad
 \overline P_C:=P_C/\widehat JP_C\cong k[G_0]^r.
\tag{1.3}
\]

This is not the fine task395 action module.  Let
\(\Delta_1^{\rm act}\) denote the physical simultaneous first-edge actor:
it is the action image denoted \(\Delta_1\) in v370 and
\(\Delta_{\rm act}\) in v374.  The same task198/task382 owner must supply
the marked onto reduction

\[
 \pi:\Delta_1^{\rm act}\twoheadrightarrow G_0
\tag{1.4}
\]

with the registered multiplication convention.  V374's formal module is

\[
 P_{\rm reg}
 =\bigoplus_{\substack{\delta\in\Delta_1^{\rm act}\\1\leq i\leq r}}
   k e_{\delta,i}
 \cong k[\Delta_1^{\rm act}]^r.
\tag{1.5}
\]

Reduction of the actor gives a canonical surjection

\[
 \boxed{
 \pi_{\rm reg}:P_{\rm reg}\twoheadrightarrow\overline P_C,
 \qquad
 \pi_{\rm reg}(e_{\delta,i})=\pi(\delta)\bar e_i.}
\tag{1.6}
\]

Neither injectivity of \(\pi\) nor an identification
\(\Delta_1^{\rm act}=G_0\) is asserted.

## 2. Localization is required only on the legal closure

V370--v374 define the fine action map

\[
 \widehat b:P_{\rm reg}\longrightarrow W_C,
 \qquad
 \widehat b(e_{\delta,i})
 =\delta\cdot\widehat B(c_i-1),
\tag{2.1}
\]

and exhausted task395 closure gives

\[
 \widehat b(P_{\rm reg})=W_C.
\tag{2.2}
\]

An arbitrary vector in the ambient eleven-slot space need not be a supported
loop.  We therefore make no raw-ambient localization claim.  V374 proves
that every element of \(W_C\) aggregates to a supported coarse loop.  The
physical enriched owner must authenticate the resulting linear map

\[
 q_{\rm loc}:W_C\longrightarrow
 L_{\rm corr}/\widehat JL_{\rm corr},
\tag{2.3}
\]

obtained by aggregating the eleven signed/prefixed slots, quotienting by the
complete PB3/PB4 boundaries, restricting to the supported correction
module, and passing to relative coinvariants.

The map (2.3) must carry the fine action through (1.4):

\[
 \boxed{
 q_{\rm loc}(\delta\cdot w)
 =\pi(\delta)\,q_{\rm loc}(w)
 \quad
 (\delta\in\Delta_1^{\rm act},\ w\in W_C).}
\tag{2.4}
\]

This is the correctly typed equivariance statement.  In particular, the
kernel of the fine-to-coarse actor acts trivially after \(q_{\rm loc}\),
although it need not act trivially on \(W_C\) itself.

Let

\[
 \overline B_C:\overline P_C\longrightarrow
 L_{\rm corr}/\widehat JL_{\rm corr}
\tag{2.5}
\]

be the reduction of v377's completed leading occurrence map.  The
seed-column part of the common physical ABI is

\[
 \boxed{
 \overline B_C(\bar e_i)
 =q_{\rm loc}\widehat b(e_{1,i})
 =q_{\rm loc}\bigl(\widehat B(c_i-1)\bigr).}
\tag{2.6}
\]

Equations (1.4), (2.3)--(2.4), and (2.6) are finite owner/replay
conditions.  They do not posit an infinite word section.

## 3. The quotient square

### Theorem 3.1 (TASK395 LEADING-COINVARIANT FACTORIZATION)

Under the physical conditions (1.4) and (2.3)--(2.6),

\[
 \boxed{
 \overline B_C\pi_{\rm reg}=q_{\rm loc}\widehat b
 \quad\text{on }P_{\rm reg}.}
\tag{3.1}
\]

Consequently

\[
 \boxed{
 \operatorname {im}\overline B_C=q_{\rm loc}(W_C).}
\tag{3.2}
\]

#### Proof

For one displayed basis element, (1.6), equivariance of
\(\overline B_C\), (2.6), and (2.4) give

\[
 \begin{aligned}
 \overline B_C\pi_{\rm reg}(e_{\delta,i})
 &=\overline B_C\bigl(\pi(\delta)\bar e_i\bigr)\\
 &=\pi(\delta)\,\overline B_C(\bar e_i)\\
 &=\pi(\delta)\,q_{\rm loc}\widehat b(e_{1,i})\\
 &=q_{\rm loc}\bigl(\delta\cdot\widehat b(e_{1,i})\bigr)\\
 &=q_{\rm loc}\widehat b(e_{\delta,i}).
 \end{aligned}
\tag{3.3}
\]

This proves (3.1) by linearity.  Since \(\pi_{\rm reg}\) is onto,

\[
 \operatorname {im}(\overline B_C\pi_{\rm reg})
 =\operatorname {im}\overline B_C.
\tag{3.4}
\]

Since \(\widehat b(P_{\rm reg})=W_C\),

\[
 \operatorname {im}(q_{\rm loc}\widehat b)=q_{\rm loc}(W_C).
\tag{3.5}
\]

Equations (3.1), (3.4), and (3.5) give (3.2). \(\square\)

Equivalently, (3.1) proves directly that
\(q_{\rm loc}\widehat b\) kills \(\ker\pi_{\rm reg}\).  No injectivity of
\(\widehat b\), \(q_{\rm loc}\), or \(\pi_{\rm reg}\) is used.

## 4. Passage to the exact successor endpoint

Let

\[
 \bar\lambda_0:
 L_{\rm corr}/\widehat JL_{\rm corr}
 \longrightarrow Z_0^{\rm loc}
\tag{4.1}
\]

be v377's quotient-to-first-successor comparison.  The physical
loop--successor square of v374 is precisely

\[
 \boxed{
 \bar\lambda_0 q_{\rm loc}
 =\lambda_0|_{W_C}.}
\tag{4.2}
\]

### Corollary 4.1 (EXACT LEADING-IMAGE PROJECTION)

Under Theorem 3.1 and (4.2),

\[
 \boxed{
 \bar\lambda_0\bigl(\operatorname {im}\overline B_C\bigr)
 =\lambda_0(W_C)
 =\operatorname {im}D_0^{\rm act}.}
\tag{4.3}
\]

#### Proof

The first equality is (3.2) followed by (4.2).  The second is v374
Theorem 3.1. \(\square\)

Thus v377's extra action-closure equality is a finite quotient/factorization
check for one physical owner, not a new all-depth selector theorem.

### Corollary 4.2 (EXACT LEADING-ONTO DECISION)

If, in addition,

\[
 \bar\lambda_0\text{ is an isomorphism}
 \qquad\text{and}\qquad
 \operatorname {im}D_0^{\rm act}=Z_0^{\rm loc},
\tag{4.4}
\]

then \(\overline B_C\) is onto.  V377 therefore gives

\[
 B_C(\widehat J^nP_C)=\widehat J^nL_{\rm corr}
 \qquad(n\geq0).
\tag{4.5}
\]

#### Proof

By (4.3)--(4.4), the image of \(\overline B_C\) maps under the injective
map \(\bar\lambda_0\) onto its entire codomain.  It must therefore be all of
\(L_{\rm corr}/\widehat JL_{\rm corr}\).  Apply v377 Theorem 4.1.
\(\square\)

Membership of one defect in \(\operatorname {im}D_0^{\rm act}\) is not a
substitute for the second equality in (4.4).

## 5. Reduced physical frontier

The positive leading route now has two finite mathematical decisions and
one finite ABI package:

1. authenticate (1.4), (2.3)--(2.4), (2.6), and (4.2) from the same
   task198/task382/Magnus owner;
2. prove or compute that (4.1) is an isomorphism; and
3. prove or compute
   \(\operatorname {im}D_0^{\rm act}=Z_0^{\rm loc}\).

Task395 supplies the exhausted fine-action image in item 3 after a positive
task382 basis.  It does not by itself compute the full target or the kernel
of (4.1).  The nonlinear one-depth return, non-pro-\(3\), perfect-core, and
settlement gates remain after leading onto.

~~~text
FINE task395 ACTION -> COARSE COINVARIANT SOURCE:    PAPER QUOTIENT
q_loc DEFINED ONLY ON LEGAL W_C:                     CORRECTED TYPE
bar-B_C pi_reg = q_loc b-hat:                        PAPER / ABI-CONDITIONAL
bar-lambda(im bar-B_C) = lambda(W_C) = im D0:        PAPER / ABI-CONDITIONAL
PHYSICAL MAGNUS/ACTION/BOUNDARY ABI:                 NOT YET AUTHENTICATED
bar-lambda_0 ISOMORPHISM:                            OPEN
im D0 = Z0loc:                                       NOT COMPUTED
FULL LEADING ONTO:                                   NOT ESTABLISHED
NONLINEAR ONE-DEPTH RETURN:                          OPEN
COMPATIBLE LIFT / FAKE / IHARA WITNESS:              NOT CONSTRUCTED
~~~

\(\mathtt{R07\_TASK395\_LEADING\_COINVARIANT\_BRIDGE\_V379\_FINAL\_AUDIT}\)

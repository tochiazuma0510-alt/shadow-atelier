# R07 task395-to-leading-coinvariant bridge v378

Author: Sol / 2026-08-30

Status: **REJECTED DRAFT; superseded by v379.**  This draft incorrectly
identifies the task395 \(\Delta_1\)-action module with the
\(\Delta_0\)-coinvariant source, defines localization on an unsupported raw
ambient space, and contains escaped-text corruption.  Nothing in it is
promoted.  The intended bridge after v368--v370, v374 and v377
identifies, conditional on one named physical enriched ABI, the task395 raw
action closure with the image of the completed seed map after passage to
relative coinvariants.  This discharges the extra action-closure equality in
v377; it does not prove that the coinvariant-to-successor comparison is an
isomorphism or that the actual image fills its target.  No compatible lift,
fake certificate or Ihara witness is declared.  `verified=false`.

## 1. The completed source has a finite leading action quotient

Put (k=mathbf F_3).  Retain v372's enriched action group, its relative
kernel, and v377's completed source:

\[
 \widehat P\triangleleft\widehat\Delta_\infty,
 \qquad
 \widehat\Xi=k[[\widehat\Delta_\infty]],
 \qquad
 \widehat J=ker\bigl(
   \widehat\Xi\to
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

On the registered first edge, the physical action ABI is required to
identify (G_0), with its marked generators and multiplication convention,
with the finite simultaneous coarse actor (Delta_{\rm act}) used by
task395.  Under this identification,

\[
 \overline\Xi:=\widehat\Xi/\widehat J\cong k[G_0]
 \cong k[\Delta_{\rm act}],
 \qquad
 \overline P_C:=P_C/\widehat JP_C\cong k[G_0]^r.
\tag{1.3}
\]

The physical equality in (1.3) is load-bearing.  A larger endpoint group, an
endpoint-only quotient of the enriched actor, or a separately reconstructed
action table may not be substituted for (Delta_{\rm act}).

Let (e_1,\ldots,e_r) denote the seed basis.  V374's finite formal action
module

\[
 P_{\rm reg}
 =\bigoplus_{g\in\Delta_{\rm act},,1\leq i\leq r}k e_{g,i}
\tag{1.4}
\]

is canonically identified with (overline P_C) by

\[
 \iota(g\bar e_i)=e_{g,i}.
\tag{1.5}
\]

## 2. The one physical raw-to-localized map

Let (V_{\rm raw}) be v370's eleven-slot, separately tagged first-edge Fox
chain space.  The task395 seed/action map is

\[
 \widehat b:P_{\rm reg}\longrightarrow V_{\rm raw},
 \qquad
 \widehat b(e_{g,i})
 =g\cdot\widehat B(c_i-1),
\tag{2.1}
\]

and v370 queue exhaustion gives

\[
 \widehat b(P_{\rm reg})=W_C.
\tag{2.2}
\]

The physical enriched owner must also supply one linear map

\[
 q_{\rm loc}:V_{\rm raw}longrightarrow
 L_{\rm corr}/\widehat JL_{\rm corr}
\tag{2.3}
\]

obtained in this order:

1. aggregate the eleven signed, prefixed slots into the H1/H2/P blocks;
2. quotient by the complete PB3/PB4 boundary modules;
3. restrict to the supported coarse-loop correction module; and
4. pass to relative (widehat J)-coinvariants.

The map (2.3) is not inferred from endpoint values.  Its source paths,
prefixes, complete boundaries, enriched action, and reductions must be the
same physical objects used in v370, v372 and task395.

Let

\[
 \overline B_C:\overline P_Clongrightarrow
 L_{\rm corr}/\widehat JL_{\rm corr}
\tag{2.4}
\]

be the reduction of v377's completed leading occurrence map.  The physical
occurrence ABI says exactly that its seed columns are (2.3) applied to the
v370 columns:

\[
 \overline B_C(\bar e_i)
 =q_{\rm loc}\bigl(\widehat B(c_i-1)\bigr).
\tag{2.5}
\]

It must also authenticate equivariance:

\[
 q_{\rm loc}(g\cdot v)=g\,q_{\rm loc}(v)
 \qquad(g\in G_0, v\in V_{\rm raw}).
\tag{2.6}
\]

Equations (2.5)--(2.6) are finite replay conditions, not new existence
hypotheses about an infinite section.

## 3. Exact image equality

### Theorem 3.1 (TASK395 LEADING-COINVARIANT SQUARE)

Under the physical identifications and replay conditions (1.3),
(2.3), (2.5), and (2.6), the square

\[
\begin{CD}
 \overline P_C @>{\iota}>> P_{\rm reg}\\
 @V{\overline B_C}VV @VV{\widehat b}V\\
 L_{\rm corr}/\widehat JL_{\rm corr}
 @<{q_{\rm loc}}<< V_{\rm raw}
\end{CD}
\tag{3.1}
\]

commutes.  Consequently

\[
 \boxed{
 \operatorname {im}\overline B_C=q_{\rm loc}(W_C).}
\tag{3.2}
\]

#### Proof

It is enough to evaluate the basis element (g\bar e_i).  Equivariance of
(overline B_C), (2.5), and (2.6) give

\[
 \begin{aligned}
 \overline B_C(g\bar e_i)
 &=g\,\overline B_C(\bar e_i)\\
 &=g\,q_{\rm loc}\bigl(\widehat B(c_i-1)\bigr)\\
 &=q_{\rm loc}\bigl(g\cdot\widehat B(c_i-1)\bigr)\\
 &=q_{\rm loc}\widehat b\iota(g\bar e_i).
 \end{aligned}
\tag{3.3}
\]

This proves (3.1).  The map (iota) is onto, and (2.2) identifies the
image of (widehat b) with (W_C).  Taking images in (3.1) proves
(3.2). \(square\)

No injectivity of (widehat b) or (q_{\rm loc}|_{W_C}) is used.
Dependent task395 columns and complete-boundary relations are therefore
retained rather than silently discarded.

## 4. Passage to the exact successor endpoint

Let

\[
 \bar\lambda_0:
 L_{\rm corr}/\widehat JL_{\rm corr}
 \longrightarrow Z_0^{\rm loc}
\tag{4.1}
\]

be v377's quotient-to-first-successor comparison.  The physical
loop--successor square of v374 requires

\[
 \bar\lambda_0 q_{\rm loc}|_{W_C}=\lambda_0|_{W_C}.
\tag{4.2}
\]

### Corollary 4.1 (THE LOAD-BEARING EQUALITY IS FORMAL AFTER ABI)

Under Theorem 3.1 and (4.2),

\[
 \boxed{
 \bar\lambda_0\bigl(\operatorname {im}\overline B_C\bigr)
 =\lambda_0(W_C)
 =\operatorname {im}D_0^{\rm act}.}
\tag{4.3}
\]

#### Proof

The first equality follows from (3.2) and (4.2).  The second is v374
Theorem 3.1. \(square\)

Thus the extra action-closure equality required in v377 is not an
independent all-depth theorem.  It is the finite commutativity check
(1.3), (2.5)--(2.6), and (4.2) for the one physical owner.

### Corollary 4.2 (EXACT LEADING-ONTO DECISION)

If, in addition,

\[
 \bar\lambda_0\text{ is an isomorphism}
 \qquad\text{and}\qquad
 \operatorname {im}D_0^{\rm act}=Z_0^{\rm loc},
\tag{4.4}
\]

then (overline B_C) is onto.  V377 then gives

\[
 B_C(\widehat J^nP_C)=\widehat J^nL_{\rm corr}
 \qquad(n\geq0).
\tag{4.5}
\]

#### Proof

Equation (4.3) and (4.4) imply that the image of (overline B_C) maps
onto the codomain of an injective map (ar\lambda_0).  Hence that image
is all of (L_{\rm corr}/\widehat JL_{\rm corr}).  Apply v377
Theorem 4.1. \(square\)

Membership of one defect in (operatorname {im}D_0^{\rm act}) is not a
substitute for the second equality in (4.4).

## 5. Reduced physical frontier

After this bridge, the positive leading route has two finite mathematical
decisions and one ABI package:

1. authenticate (1.3), (2.3), (2.5)--(2.6), and (4.2) from the same
   task198/task382/Magnus owner;
2. prove or compute that (4.1) is an isomorphism; and
3. prove or compute the full image equality
   (operatorname {im}D_0^{\rm act}=Z_0^{\rm loc}).

Task395 supplies the exhausted raw image in item 3 after a positive task382
basis.  It does not by itself compute the full target or the kernel of
(4.1).  The nonlinear one-depth return, non-pro-(3), perfect-core, and
settlement gates remain after leading onto.

```text
P_C/J P_C = FINITE TASK395 ACTION MODULE:           PAPER / ABI-CONDITIONAL
RAW TASK395 CLOSURE -> LEADING IMAGE SQUARE:         PAPER / ABI-CONDITIONAL
bar-lambda(im bar-B_C) = lambda(W_C) = im D0:        PAPER / ABI-CONDITIONAL
PHYSICAL MAGNUS/ACTION/BOUNDARY ABI:                 NOT YET AUTHENTICATED
bar-lambda_0 ISOMORPHISM:                            OPEN
im D0 = Z0loc:                                       NOT COMPUTED
FULL LEADING ONTO:                                   NOT ESTABLISHED
NONLINEAR ONE-DEPTH RETURN:                          OPEN
COMPATIBLE LIFT / FAKE / IHARA WITNESS:              NOT CONSTRUCTED
```

`R07_TASK395_LEADING_COINVARIANT_BRIDGE_V378_AUDIT_READY`

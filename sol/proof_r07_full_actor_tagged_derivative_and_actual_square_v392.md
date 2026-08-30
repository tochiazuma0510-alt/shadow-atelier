# R07 full-actor tagged derivative and actual square criterion v392

Author: Sol / 2026-08-30

Status: corrected paper theorem after the failed v390 and v391 audits.  It
keeps the full finite actor \(\Gamma_i\) and its relative ideal \(I_i\)
throughout the actual square.  Only occurrence-tagging redundancy may be
quotiented.  Coarse coinvariants are taken afterward, as in v379.  The
tagged Fox replay is proved; promotion to the full actual square is reduced
to one finite aggregation-equivariance and same-owner gate.  That physical
gate and the positive A4 seed closure are not yet available.  No compatible
lift, fake certificate or Ihara witness is declared.
\(\mathtt{verified=false}\).

## 1. Fine tagged source and literal word replay

Fix a matched finite elementary-abelian coordinate \(i\), put
\(k=\mathbf F_3\), and retain v370's simultaneous first-edge actor
\(\Delta_i^{\rm act}\).  For its eleven occurrence slots retain

\[
 A_{i,o}(g)=P_{i,o}\rho_{i,o}(g)P_{i,o}^{-1},
 \qquad 1\leq o\leq11,
\tag{1.1}
\]

including the frozen signs, prefixes and inverse conventions.  For a
word-bearing relative seed roster \(c_{i1},\ldots,c_{ir}\), put

\[
 P_{{\rm reg},i}=k[\Delta_i^{\rm act}]^r,
 \qquad
 \widehat b_i(e_{g,a})
 =g\cdot\widehat B_i(c_{ia}-1)\in W_{C,i}.
\tag{1.2}
\]

Its \(o\)-th tagged component is

\[
 \boxed{
 \widehat b_i(e_{g,a})_o
 =\sigma_oP_{i,o}\rho_{i,o}(g)
   \delta_i(\rho_{i,o}(c_{ia})).}
\tag{1.3}
\]

### Theorem 1.1 (TAGGED UNIVERSAL DERIVATIVE)

The map \(\widehat b_i\) is
\(k[\Delta_i^{\rm act}]\)-linear.  On every basis element it equals the
literal signed eleven-occurrence first difference made by the single
conjugated correction \({}^g c_{ia}\), before the three block sums.

#### Proof

This is v370 Lemma 2.1.  Its independent word-pair replay is

\[
 \widehat b_i(e_{g,a})_o
 =\sigma_oP_{i,o}
  \bigl(\delta_i(\rho_{i,o}(gc_{ia}))
        -\delta_i(\rho_{i,o}(g))\bigr),
\tag{1.4}
\]

which is the exact Fox product rule for \(gc_{ia}g^{-1}\).  Free-module
extension proves the assertion.  No action is transported through
aggregation. \(\square\)

Let \(A_i^{\rm enr}\) be v372's cumulative one-common-word enriched image,
and define materialization

\[
 \tau_{{\rm reg},i}(e_{g,a})=[{}^g c_{ia}].
\tag{1.5}
\]

Let \(q_{{\rm full},i}:W_{C,i}\to L_{{\rm amb},i}\) be the physical map
which performs the frozen H1/H2/A.18 block sums, complete PB3/PB4 boundaries
and full registered localization.  It is defined only on the legal closure
\(W_{C,i}\).  Let
\(D_{{\rm act},i}:A_i^{\rm enr}\to L_{{\rm amb},i}\) be the first
difference of v372's exact residual.

### Theorem 1.2 (SAME-OWNER VECTOR-SPACE SQUARE)

If these two maps use the same ten enriched contexts, ten-to-eleven map,
factor order, four inverse slots, boundaries and localization owner, then

\[
 \boxed{
 q_{{\rm full},i}\widehat b_i
 =D_{{\rm act},i}\tau_{{\rm reg},i}}
\tag{1.6}
\]

as \(k\)-linear maps on \(P_{{\rm reg},i}\).

#### Proof

Equation (1.4) gives the complete tagged first difference for one
materialized word.  Applying the frozen block products and boundaries gives
the left side.  V372 Theorem 3.1 identifies the same ordered path product
with the exact residual of the enriched state, which gives the right side.
Equality on the displayed basis and linearity prove (1.6). \(\square\)

## 2. Full actor retained: only tagging redundancy is quotiented

Let \(\Gamma_i\to\overline\Gamma_i\) be the full occurrence actor used in
v388--v389, and put

\[
 R_i=k[\Gamma_i],
 \qquad
 P_i=R_i^r,
 \qquad
 I_i=\ker(R_i\to k[\overline\Gamma_i]).
\tag{2.1}
\]

The physical ABI must provide an onto actor map

\[
 \alpha_i:\Delta_i^{\rm act}\twoheadrightarrow\Gamma_i
\tag{2.2}
\]

and hence the full-source quotient

\[
 \boxed{
 \pi_{{\rm full},i}:P_{{\rm reg},i}\twoheadrightarrow P_i,
 \qquad e_{g,a}\longmapsto\alpha_i(g)e_{ia}.}
\tag{2.3}
\]

The kernel in (2.3) records only redundancy in the fine actor/tagging
presentation.  It is **not** \(I_iP_i\): the latter is a submodule of the
target source \(P_i\) and must survive.

Give the proposed reachable full target \(L_i\subseteq L_{{\rm amb},i}\)
its authenticated left \(R_i\)-action and assume
\(q_{{\rm full},i}(W_{C,i})\subseteq L_i\).

### Theorem 2.1 (FULL-ACTOR AGGREGATION DESCENT)

There is a unique \(R_i\)-linear map

\[
 B_{C,i}:P_i\longrightarrow L_i
\quad\text{such that}\quad
 \boxed{B_{C,i}\pi_{{\rm full},i}
       =q_{{\rm full},i}\widehat b_i}
\tag{2.4}
\]

if and only if

1. \(q_{{\rm full},i}\widehat b_i\) kills
   \(\ker\pi_{{\rm full},i}\); and
2. the induced map on \(P_i\) is \(R_i\)-linear.

A sufficient physical condition for both clauses is the full-action
equivariance

\[
 \boxed{
 q_{{\rm full},i}(g\cdot w)
 =\alpha_i(g)q_{{\rm full},i}(w)
 \quad(g\in\Delta_i^{\rm act},\ w\in W_{C,i}).}
\tag{2.5}
\]

#### Proof

The two numbered clauses are precisely the universal property of the
surjection (2.3), followed by the definition of \(R_i\)-linearity.
For (2.5), if two group-algebra combinations have the same image under
\(\alpha_i\), equivariance makes their actions on every seed column have the
same image under \(q_{{\rm full},i}\); hence the kernel is killed.  Moreover

\[
 \begin{aligned}
 q_{{\rm full},i}\widehat b_i(e_{g,a})
 &=q_{{\rm full},i}(g\cdot\widehat B_i(c_{ia}-1))\\
 &=\alpha_i(g)q_{{\rm full},i}\widehat B_i(c_{ia}-1),
 \end{aligned}
\tag{2.6}
\]

so the induced map is \(R_i\)-linear. \(\square\)

If \(W_{C,i}\) has an exhausted basis \(w_1,\ldots,w_s\) and
\(\Delta_i^{\rm act}\) has marked generators \(h_1,\ldots,h_m\), condition
(2.5) is decided by the finite roster \((h_j,w_\ell)\).  This is one finite
aggregation/action gate after a positive A4/task395 receipt, not an
all-rung membership search.

## 3. Promotion to the actual-image square

The same-owner ABI must also make materialization factor through the full
source, namely provide

\[
 \tau_i:P_i\longrightarrow A_i^{\rm enr},
 \qquad
 \tau_i\pi_{{\rm full},i}=\tau_{{\rm reg},i}.
\tag{3.1}
\]

### Corollary 3.1 (FULL ACTUAL SQUARE)

Under Theorems 1.2 and 2.1 and (3.1),

\[
 \boxed{
 B_{C,i}=D_{{\rm act},i}\tau_i}
\tag{3.2}
\]

after identifying \(L_i\) with its embedded image in
\(L_{{\rm amb},i}\).  Equivalently, the v389 actual-image square commutes.

#### Proof

Composing both sides of (3.2) with the surjection
\(\pi_{{\rm full},i}\), equations (1.6), (2.4) and (3.1) give the same map
\(q_{{\rm full},i}\widehat b_i\).  Surjectivity proves (3.2). \(\square\)

This does not infer (3.1) from endpoint equality.  It requires the same
path-bearing enriched materialization owner of v372.

## 4. Relative-ideal divisors survive and have no second owner

The relative ideal remains inside the full source:

\[
 I_iP_i\subseteq P_i.
\tag{4.1}
\]

For a word-bearing basis \(k_{i1},\ldots,k_{it_i}\) of
\(K_i=\ker(\Gamma_i\to\overline\Gamma_i)\), v388's primitive source roster
is

\[
 (k_{ij}-1)e_{ia}\in I_iP_i.
\tag{4.2}
\]

Choose any tagged lifts \(\widetilde k_{ij}\in\Delta_i^{\rm act}\) with
\(\alpha_i(\widetilde k_{ij})=k_{ij}\).  Then (2.3) gives

\[
 \pi_{{\rm full},i}
 ((\widetilde k_{ij}-1)e_{1,a})
 =(k_{ij}-1)e_{ia}.
\tag{4.3}
\]

### Corollary 4.1 (NO-DUPLICATE DIVISOR OWNER)

Under Corollary 3.1, the physical path-bearing divisor map of v388 is

\[
 \boxed{
 \Sigma_i:=\left.B_{C,i}\right|_{I_iP_i}
          =\left.D_{{\rm act},i}\tau_i\right|_{I_iP_i}.}
\tag{4.4}
\]

Its primitive columns can be replayed without a separate matrix as

\[
 \boxed{
 \Sigma_i((k_{ij}-1)e_{ia})
 =q_{{\rm full},i}\widehat b_i
   ((\widetilde k_{ij}-1)e_{1,a}).}
\tag{4.5}
\]

#### Proof

Equation (4.4) is the restriction of (3.2).  Equations (2.4) and (4.3)
give (4.5).  A different choice of tagged lift differs by
\(\ker\pi_{{\rm full},i}\), which is killed in Theorem 2.1. \(\square\)

V388 now factors every ordered prefix and Fox cross divisor through the
\(R_i\)-span of (4.5), and v389 places those columns in the reachable image.
This conclusion is conditional on the one full-action gate (2.5) and the
same-owner materialization (3.1); it is not obtained from v379 alone.

Only **after** (4.4) is established may one quotient

\[
 P_i\twoheadrightarrow P_i/I_iP_i\cong k[\overline\Gamma_i]^r.
\tag{4.6}
\]

V379 is the leading-coinvariant shadow after this quotient.  It cannot be
used in the reverse direction to prove the nonzero full-target divisor
identity.

## 5. Compatible inverse-limit form

Suppose the finite objects above form compatible inverse systems and the
physical ABI supplies a continuous quotient map with closed kernel

\[
 \pi_{{\rm full},\infty}:
 P_{{\rm reg},\infty}\twoheadrightarrow P_\infty,
\tag{5.1}
\]

a continuous aggregation
\(q_{{\rm full},\infty}:W_{C,\infty}\to L_\infty\), and compatible
materialization maps.  If

\[
 q_{{\rm full},\infty}\widehat b_\infty
 (\ker\pi_{{\rm full},\infty})=0
\tag{5.2}
\]

and the induced quotient map is continuous and
\(\widehat\Xi\)-linear, it defines one

\[
 B_{C,\infty}:P_\infty\longrightarrow L_\infty
\tag{5.3}
\]

whose reductions are all finite squares (3.2).  No independent compatible
choice of finite \(B_{C,i}\) is then needed.

The desired infinite relative-dihedral generalization must construct the
equivariant full-target aggregation/homotopy satisfying (5.2), while
retaining the full relative ideal.  This note identifies the correct source
and the exact finite gate; it does not construct that homotopy.

~~~text
TAGGED UNIVERSAL DERIVATIVE:                         PAPER PROOF
TAGGED DERIVATIVE = LITERAL ACTUAL WORD REPLAY:      PAPER / SAME-OWNER CONDITIONAL
TAGGING REDUNDANCY -> FULL ACTOR P_i:                PAPER CRITERION / PHYSICAL GATE OPEN
FULL-ACTION AGGREGATION EQUIVARIANCE:                OPEN / FINITE AFTER POSITIVE A4
FULL v389 ACTUAL SQUARE:                             CONDITIONAL ON THAT GATE
SIGMA = RESTRICTION ON SURVIVING I_i P_i:            PAPER / SAME CONDITION
COARSE COINVARIANT SHADOW:                           v379 ONLY AFTER FULL SQUARE
SEPARATE SIGMA MATRIX / PRIMITIVE SEARCH:            NOT NEEDED
ACTUAL A4 WORD-BEARING SEED ROSTER / W_C:            UNKNOWN_RESOURCE
INITIAL FULL PATH-BEARING MEMBERSHIP:                OPEN (A0 RUNNING)
REGISTERED RELATIVE PRO-3 LIFT (A9):                 CONDITIONAL / 0 OF 3 ACTUAL
FAKE / IHARA WITNESS:                                NOT DECLARED
~~~

\(\mathtt{R07\_FULL\_ACTOR\_TAGGED\_DERIVATIVE\_AND\_ACTUAL\_SQUARE\_V392\_AUDIT\_CANDIDATE}\)

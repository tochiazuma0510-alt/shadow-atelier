# R07 reachable-class one-defect theorem with intrinsic saturation v381

Author: Sol / 2026-08-30

Status: corrected paper theorem replacing rejected v380.  The compact
one-orbit argument is retained, while the ambient/intrinsic filtration gap is
made into an explicit saturation class.  The task395 factor square is
re-instantiated directly in the reachable quotient rather than transported
from another target.  The abstract theorem is unconditional.  Its R07 use
still needs one full path-bearing membership and vanishing of the named
intrinsic saturation classes for one physical enriched owner.  No compatible
lift, fake certificate or Ihara witness is declared.
\(\mathtt{verified=false}\).

## 1. Compact reachable target

Let \(\Lambda\) be a compact Hausdorff topological ring, let
\(J\triangleleft\Lambda\) be a closed two-sided ideal, and define \(JM\)
and its powers as closed spans of finite products.  Let \(P\) and
\(L_{\rm amb}\) be compact Hausdorff left \(\Lambda\)-modules, and let

\[
 B:P\longrightarrow L_{\rm amb}
\tag{1.1}
\]

be continuous and \(\Lambda\)-linear.

Let \(Q\) be a compact group acting continuously on the right of a compact
space containing \(w_0\).  Put

\[
 {\cal W}=w_0Q.
\tag{1.2}
\]

Equivalently, the orbit map \(Q\to{\cal W}\), \(q\mapsto w_0q\), is
continuous.  Let \(S=S^{-1}\subseteq Q\) satisfy

\[
 Q=\overline{\langle S\rangle},
\tag{1.3}
\]

and let

\[
 \Phi:{\cal W}\longrightarrow L_{\rm amb}
\tag{1.4}
\]

be continuous.  Define

\[
 \boxed{
 L_{\rm reach}
 =
 \overline{\Lambda B(P)+
 \sum_{w\in{\cal W}}\Lambda\Phi(w)}
 \leq L_{\rm amb}.}
\tag{1.5}
\]

The sum means finite sums before closure.  This is the smallest closed
\(\Lambda\)-submodule containing the actual leading correction values and
the residual orbit.  It is compact Hausdorff.  Write

\[
 \rho:L_{\rm reach}\longrightarrow
 \overline L_{\rm reach}:=
 L_{\rm reach}/JL_{\rm reach}
\tag{1.6}
\]

and let

\[
 \overline B:P/JP\longrightarrow\overline L_{\rm reach}
\tag{1.7}
\]

be induced by \(B\).

## 2. The sound one-defect theorem

### Theorem 2.1 (INTRINSIC ONE-DEFECT LEADING ONTO)

Assume:

1. \(L_{\rm reach}\) is \(J\)-separated:

   \[
    \bigcap_{n\geq0}J^nL_{\rm reach}=0;
   \tag{2.1}
   \]

2. every generator increment has its class in the intrinsic leading image:

   \[
    \rho\bigl(\Phi(ws)-\Phi(w)\bigr)
       \in\operatorname {im}\overline B
    \quad(w\in{\cal W},\ s\in S);
   \tag{2.2}
   \]

3. one full initial residual class lies in that image:

   \[
    \rho\Phi(w_0)\in\operatorname {im}\overline B.
   \tag{2.3}
   \]

Then

\[
 \boxed{
 \overline B:P/JP\twoheadrightarrow
 L_{\rm reach}/JL_{\rm reach}}
\tag{2.4}
\]

is onto.  Consequently v377 gives

\[
 \boxed{
 B(P)=L_{\rm reach},
 \qquad
 B(J^nP)=J^nL_{\rm reach}\quad(n\geq0).}
\tag{2.5}
\]

No ambient leading-target isomorphism, finite projective target, or global
continuous section is used.

#### Proof

Let \(H=\operatorname {im}\overline B\).  It is compact and hence closed in
the Hausdorff quotient \(\overline L_{\rm reach}\), and it is a
\(\Lambda/J\)-submodule.  For a finite word
\(a=s_1\cdots s_m\), telescoping and (2.2)--(2.3) give

\[
 \begin{aligned}
 \rho\Phi(w_0a)
 &=
 \rho\Phi(w_0)
 +\sum_{i=1}^{m}
 \rho\bigl(
  \Phi(w_0s_1\cdots s_i)
  -\Phi(w_0s_1\cdots s_{i-1})
 \bigr)
 \in H.
 \end{aligned}
\tag{2.6}
\]

Finite words in \(S\) are dense in \(Q\).  Continuity of the orbit map,
\(\Phi\), and \(\rho\), and closedness of \(H\), imply

\[
 \rho\Phi({\cal W})\subseteq H.
\tag{2.7}
\]

The submodule \(H\) also contains \(\rho B(P)\).  Equation (1.5) now gives
\(\rho(L_{\rm reach})\subseteq H\).  The reverse inclusion is automatic,
and \(\rho(L_{\rm reach})=\overline L_{\rm reach}\), proving (2.4).
Apply v377 Theorem 2.1 and (2.1) to obtain (2.5). \(\square\)

### Corollary 2.2 (INTRINSIC AFFINE GENERATOR FORM)

Condition (2.2) follows if every \(s\in S\) has a named instruction
\(t_s\in P\) and

\[
 \boxed{
 \Phi(ws)-\Phi(w)-B(t_s)\in JL_{\rm reach}}
\quad(w\in{\cal W}).
\tag{2.8}
\]

For an inverse generator take \(t_{s^{-1}}=-t_s\): apply (2.8) for \(s\)
at \(ws^{-1}\) and negate.  No compatible or continuous selection of
preimages is required.

## 3. The saturation class which v380 missed

The inclusion \(L_{\rm reach}\subseteq L_{\rm amb}\) gives a natural map

\[
 L_{\rm reach}/JL_{\rm reach}
 \longrightarrow
 L_{\rm amb}/JL_{\rm amb}.
\tag{3.1}
\]

Its kernel is

\[
 \boxed{
 {\rm Sat}_1(L_{\rm reach},L_{\rm amb})
 =
 \frac{L_{\rm reach}\cap JL_{\rm amb}}
      {JL_{\rm reach}}.}
\tag{3.2}
\]

This quotient is zero exactly when the reachable target is saturated at
leading depth.

Fix a physical seed-conjugate generator \(s\) and its instruction \(t_s\).
The exact eleven-occurrence Fox replay may prove

\[
 \epsilon_0(w,s)
 :=
 \Phi(ws)-\Phi(w)-B(t_s)
 \in L_{\rm reach}\cap JL_{\rm amb}.
\tag{3.3}
\]

Indeed, equality of the moving and fixed prefixes after coarse reduction
puts every coefficient difference in the ambient relative augmentation
ideal; the definition (1.5) puts the aggregate difference back in
\(L_{\rm reach}\).  It does not by itself put the aggregate in
\(JL_{\rm reach}\).

### Proposition 3.1 (EXACT LEADING SATURATION GATE)

Under (3.3), the intrinsic affine law (2.8) holds for \((w,s)\) if and only
if

\[
 \boxed{
 [\epsilon_0(w,s)]=0
 \quad\text{in }
 {\rm Sat}_1(L_{\rm reach},L_{\rm amb}).}
\tag{3.4}
\]

#### Proof

By (3.3), the numerator class is defined.  Its vanishing is precisely
\(\epsilon_0(w,s)\in JL_{\rm reach}\), which is (2.8). \(\square\)

Thus there are three valid ways to close the leading prefix step:

1. give an explicit factorization
   \(\epsilon_0(w,s)=\sum_i j_i\ell_i\) with
   \(j_i\in J\) and \(\ell_i\in L_{\rm reach}\);
2. prove the full equality
   \(L_{\rm reach}\cap JL_{\rm amb}=JL_{\rm reach}\); or
3. compute the particular classes (3.4) and prove all required ones zero.

An ambient prefix calculation with no such output is insufficient.

## 4. The task395 square must live in the same quotient

Use the enriched R07 data

\[
 \widehat\Xi=\mathbf F_3[[\widehat\Delta_\infty]],
 \qquad
 \widehat J=
 \ker\left(
  \widehat\Xi\longrightarrow
  \mathbf F_3[[
   \widehat\Delta_\infty/\widehat P]]
 \right),
 \qquad
 P_C=\widehat\Xi^r.
\tag{4.1}
\]

Let \(L_{\rm reach}\) be (1.5) for v372's actual enriched residual orbit and
the actual leading map \(B_C\).  The localization map needed here is not
imported from a differently chosen \(L_{\rm corr}\).  It must be replayed as

\[
 q_{\rm loc}^{\rm reach}:W_C\longrightarrow
 L_{\rm reach}/\widehat JL_{\rm reach}
\tag{4.2}
\]

using the same complete PB3/PB4 boundaries, supported-loop restriction and
physical enriched action owner.

Let

\[
 \pi_{\rm reg}:P_{\rm reg}\twoheadrightarrow
 P_C/\widehat JP_C
\tag{4.3}
\]

be v379's fine-to-coarse actor quotient, and let
\(\widehat b:P_{\rm reg}\twoheadrightarrow W_C\) be the exhausted formal
action map.

### Proposition 4.1 (REACHABLE-QUOTIENT TASK395 FACTORIZATION)

If the seed columns and action equivariance are replayed directly into
(4.2), then

\[
 \boxed{
 \overline B_C\pi_{\rm reg}
 =
 q_{\rm loc}^{\rm reach}\widehat b}
\tag{4.4}
\]

and consequently

\[
 \boxed{
 \operatorname {im}\overline B_C
 =
 q_{\rm loc}^{\rm reach}(W_C)}
\tag{4.5}
\]

inside the single quotient
\(L_{\rm reach}/\widehat JL_{\rm reach}\).

#### Proof

This is v379 Theorem 3.1 with its codomain replaced at the definition stage,
not by later base change.  On \(e_{\delta,i}\), fine action equivariance
through the marked actor quotient gives

\[
 \overline B_C\pi_{\rm reg}(e_{\delta,i})
 =
 q_{\rm loc}^{\rm reach}
 \widehat b(e_{\delta,i}).
\tag{4.6}
\]

Linearity proves (4.4).  Surjectivity of \(\pi_{\rm reg}\) and
\(\widehat b(P_{\rm reg})=W_C\) gives (4.5). \(\square\)

Without a direct replay (4.2)--(4.4), one would need injectivity of the
base-change map from the reachable quotient into the old correction
quotient.  No such injectivity is assumed here.

## 5. R07 one-defect criterion, correctly typed

Put

\[
 \overline\beta_{\rm path}
 =
 \rho\Phi_{\rm lane}(\widehat w_0)
 \in L_{\rm reach}/\widehat JL_{\rm reach}.
\tag{5.1}
\]

This is the full retained path-bearing residual class before the successor
endpoint projection.

### Theorem 5.1 (ONE PATH-BEARING DEFECT PLUS SATURATION)

Assume, for one common physical enriched owner:

1. v372's residual map, v369's leading/materialization square, the complete
   boundaries, and all reductions and actions are authenticated on the
   module \(L_{\rm reach}\);
2. its actual finite relative pro-\(3\) coordinates give intrinsic
   \(\widehat J\)-separation as in v377;
3. the direct reachable-quotient factor square (4.4) is authenticated;
4. every leading generator prefix class (3.4) vanishes, with compatible
   finite replay or an exact factorization in
   \(\widehat JL_{\rm reach}\); and
5. the one full initial class satisfies

   \[
    \boxed{
    -\overline\beta_{\rm path}
    \in q_{\rm loc}^{\rm reach}(W_C).}
   \tag{5.2}
   \]

Then

\[
 \boxed{
 B_C(P_C)=L_{\rm reach},
 \qquad
 B_C(\widehat J^nP_C)
 =
 \widehat J^nL_{\rm reach}
 \quad(n\geq0).}
\tag{5.3}
\]

Neither an isomorphism
\(L_{\rm reach}/\widehat JL_{\rm reach}\to Z_0^{\rm loc}\) nor the ambient
equality
\(\operatorname {im}D_0^{\rm act}=Z_0^{\rm loc}\) is required.

#### Proof

Item 4 and Proposition 3.1 give Theorem 2.1 condition (2.2).  Equations
(4.5) and (5.2), with closure under negation, give condition (2.3).
Item 2 gives separation.  Apply Theorem 2.1. \(\square\)

The endpoint membership

\[
 -\beta_0\in\lambda_0(W_C)
\tag{5.4}
\]

does not imply (5.2): a nonzero path-bearing class may die under the
successor endpoint map.  The load-bearing membership remains (5.2).

## 6. Positive-depth saturation and the nonlinear recurrence

For \(d\geq0\), define

\[
 {\rm Sat}_{d+1}(L_{\rm reach},L_{\rm amb})
 =
 \frac{
  L_{\rm reach}\cap\widehat J^{d+1}L_{\rm amb}}
 {\widehat J^{d+1}L_{\rm reach}}.
\tag{6.1}
\]

Let \(t\in\widehat J^dP_C\), let \(c_d(t)\) be a v369 depth-\(d\)
materialization, and put

\[
 \epsilon_d(w,t)
 =
 \Phi_{\rm lane}(wc_d(t))
 -\Phi_{\rm lane}(w)-B_C(t).
\tag{6.2}
\]

The ambient depth claim

\[
 \epsilon_d(w,t)
 \in
 L_{\rm reach}\cap\widehat J^{d+1}L_{\rm amb}
\tag{6.3}
\]

requires the complete filtered Fox package:

1. the fixed-prefix Fox class of \(c_d(t)\) agrees with \(B_C(t)\) in the
   associated graded;
2. every moving-prefix difference contributes one additional
   \(\widehat J\);
3. ordered-product cross terms have the next-depth gain of v251/v252; and
4. complete boundaries and legal localization preserve these filtrations.

Merely knowing that a Fox path has ambient depth \(d\) proves none of item 1
or the intrinsic conclusion below.

### Proposition 6.1 (EXACT NONLINEAR SATURATION GATE)

Assume (6.3).  The intrinsic one-depth law

\[
 \boxed{
 \epsilon_d(w,t)\in
 \widehat J^{d+1}L_{\rm reach}}
\tag{6.4}
\]

holds if and only if

\[
 [\epsilon_d(w,t)]=0
 \quad\text{in }
 {\rm Sat}_{d+1}(L_{\rm reach},L_{\rm amb}).
\tag{6.5}
\]

#### Proof

This is the definition of the quotient (6.1). \(\square\)

Under Theorem 5.1, every intrinsic depth-\(d\) residual has a
\(t_d\in\widehat J^dP_C\) which cancels it linearly, and v369 materializes
that instruction.  If the full filtered Fox package (6.3) and the saturation
vanishing (6.5) hold for every recursively requested pair, v369 Theorem 4.1
constructs the compatible relative pro-\(3\) correction.  This is now the
exact remaining nonlinear condition; it is not replaced by ambient depth
gain alone.

The class-specific route has therefore replaced two ambient full-target
requirements by three narrower physical decisions:

1. direct task395 factorization in the reachable quotient;
2. one initial full path-bearing membership (5.2); and
3. leading and recursively encountered saturation classes (3.4), (6.5).

Mixed-prime, perfect-core and settlement gates remain after the registered
pro-\(3\) lane.

~~~text
ABSTRACT ONE-DEFECT REACHABLE THEOREM:                PAPER PROOF
AMBIENT/INTRINSIC SATURATION GAP:                     EXPLICITLY RETAINED
TASK395 FACTOR SQUARE IN REACHABLE QUOTIENT:          PAPER / DIRECT ABI REQUIRED
ONE FULL PATH-BEARING INITIAL MEMBERSHIP:             NOT COMPUTED
LEADING PREFIX SATURATION CLASSES:                    NOT COMPUTED
AMBIENT bar-lambda ISOMORPHISM:                       NOT NEEDED ON THIS ROUTE
AMBIENT im D0 = Z0loc:                                NOT NEEDED ON THIS ROUTE
ALL LINEAR J-DEPTH PREIMAGES AFTER THEOREM 5.1:       V377 + THIS THEOREM
POSITIVE-DEPTH FILTERED FOX CONGRUENCE:               OPEN PHYSICAL BINDING
POSITIVE-DEPTH INTRINSIC SATURATION:                  OPEN
COMPATIBLE RELATIVE PRO-3 LIFT:                       NOT CONSTRUCTED
MIXED-PRIME / PERFECT-CORE / SETTLEMENT:              OPEN
FAKE / IHARA WITNESS:                                 NOT DECLARED
~~~

\(\mathtt{R07\_REACHABLE\_CLASS\_ONE\_DEFECT\_WITH\_SATURATION\_V381\_AUDIT\_CANDIDATE}\)

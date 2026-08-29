# R07 compact separated leading-onto lift v377

Author: Sol / 2026-08-30

Status: final audit candidate correcting rejected v376.  The abstract
compact-module theorem proves that onto modulo a closed ideal, together with
target separation, implies full onto and strictness at every closed ideal
depth.  Its R07 specialization is deliberately conditional on the physical
enriched action ABI and is made only for the reachable coarse-loop correction
module, not for all path-bearing states.  The v369 source is
\(P_C=\widehat\Xi^r\); \(A_C\) is only its cumulative actual-value image.
The comparison with the v374 first-successor target has the quotient-to-layer
direction.  No compatible R07 lift, fake certificate or Ihara witness is
declared.  `verified=false`.

## 1. Closed ideal powers

Let \(\Lambda\) be a compact Hausdorff topological ring, let
\(J\triangleleft\Lambda\) be a closed two-sided ideal, and let \(M\) be a
compact Hausdorff left \(\Lambda\)-module.  Throughout,

\[
 J^nM=\overline{\operatorname {span}}
 \{j_1\cdots j_nm:j_k\in J,\ m\in M\}.
\tag{1.1}
\]

Thus every ideal power is closed.  We call \(M\) \(J\)-separated if

\[
 \bigcap_{n\geq0}J^nM=0.
\tag{1.2}
\]

For another compact Hausdorff \(\Lambda\)-module \(N\), if
\(f:M\to N\) is continuous and \(\Lambda\)-linear, then \(f(M)\),
\(f(J^nM)\), and \(f(M)+J^nN\) are compact, hence closed in the Hausdorff
target.

### Lemma 1.1 (ITERATED LEADING DENSITY)

Let \(N\) be a compact Hausdorff \(\Lambda\)-module and let
\(f:M\to N\) be continuous and \(\Lambda\)-linear.  If

\[
 N=f(M)+JN,
\tag{1.3}
\]

then, for every \(n\geq1\),

\[
 \boxed{N=f(M)+J^nN.}
\tag{1.4}
\]

#### Proof

Assume \(N=f(M)+J^nN\), and put

\[
 S=f(M)+J^{n+1}N.
\tag{1.5}
\]

The set \(S\) is closed.  It is enough to prove \(J^nN\subseteq S\).
Consider a generating term \(a y\), where
\(a=j_1\cdots j_n\) and \(y\in N\).  By (1.3), write
\(y=f(x)+u\) with \(u\in JN\).  The element \(u\) need not be one product
\(jz\).  By (1.1), choose a net of finite sums

\[
 u_\alpha=\sum_k j_{\alpha k}z_{\alpha k}\longrightarrow u.
\tag{1.6}
\]

For every \(\alpha\),

\[
 a f(x)+a u_\alpha
 =f(ax)+\sum_k a j_{\alpha k}z_{\alpha k}\in S.
\tag{1.7}
\]

Continuity of multiplication and closedness of \(S\) give
\(ay\in S\).  The same argument applies to finite sums of generators;
closedness of \(S\) then gives \(J^nN\subseteq S\).  Hence the induction
step follows from the induction hypothesis, and (1.3) is the base case.
\(\square\)

## 2. Compact leading onto gives full onto and strictness

### Theorem 2.1 (COMPACT SEPARATED LEADING-ONTO LIFT)

Let \(M,N\) be compact Hausdorff \(\Lambda\)-modules, let \(N\) be
\(J\)-separated, and let \(f:M\to N\) be continuous and
\(\Lambda\)-linear.  If

\[
 \bar f:M/JM\longrightarrow N/JN
\tag{2.1}
\]

is onto, then

\[
 \boxed{f(M)=N}
\tag{2.2}
\]

and, for every \(n\geq0\),

\[
 \boxed{f(J^nM)=J^nN.}
\tag{2.3}
\]

No finite generation, projectivity, freeness of the target, or continuous
linear section is assumed or concluded.

#### Proof

Surjectivity of (2.1) is exactly (1.3).  Fix \(y\in N\).  Lemma 1.1 makes

\[
 S_n=f(M)\cap(y+J^nN)
\tag{2.4}
\]

nonempty for every \(n\).  These are nested closed subsets of the compact
set \(f(M)\), so their intersection is nonempty.  If
\(z\in\bigcap_nS_n\), then

\[
 y-z\in\bigcap_nJ^nN=0.
\tag{2.5}
\]

Thus \(y=z\in f(M)\), proving (2.2).

Linearity gives \(f(J^nM)\subseteq J^nN\).  Conversely, after (2.2), every
finite sum \(\sum_kj_{k1}\cdots j_{kn}y_k\) may be written as

\[
 \sum_kj_{k1}\cdots j_{kn}f(x_k)
 =f\!\left(\sum_kj_{k1}\cdots j_{kn}x_k\right),
\tag{2.6}
\]

and hence lies in \(f(J^nM)\).  Such sums are dense in \(J^nN\), while
\(f(J^nM)\) is compact and therefore closed.  This proves the reverse
inclusion in (2.3). \(\square\)

### Corollary 2.2 (DEPTHWISE PREIMAGE)

Under Theorem 2.1, every requested \(z_n\in J^nN\) has some
\(x_n\in J^nM\) with \(f(x_n)=z_n\).  The theorem neither chooses the
preimages continuously nor makes choices at different depths into a global
section.

## 3. Separation in finite relative pro-\(p\) coordinates

### Lemma 3.1 (FINITE RELATIVE-\(p\) SEPARATION)

Let \(\Gamma\) be a profinite group with a closed normal pro-\(p\) subgroup
\(P\), and let

\[
 \Gamma\twoheadrightarrow\Gamma_i,
 \qquad P_i=\operatorname {im}(P\to\Gamma_i)
\tag{3.1}
\]

be a separating cofiltered family of onto finite images.  In particular,
every \(P_i\triangleleft\Gamma_i\) is a finite \(p\)-group.  Put

\[
 \Lambda=\mathbf F_p[[\Gamma]],
 \qquad
 J=\ker\bigl(\Lambda\to\mathbf F_p[[\Gamma/P]]\bigr).
\tag{3.2}
\]

Let \(N=\varprojlim_iN_i\) be a compact \(\Lambda\)-module whose finite
coordinates are finite \(\mathbf F_p[\Gamma_i]\)-modules with the stated
actions and equivariant reductions.  Then

\[
 \boxed{\bigcap_{n\geq0}J^nN=0.}
\tag{3.3}
\]

#### Proof

The image of \(J\) in \(\mathbf F_p[\Gamma_i]\) is exactly

\[
 J_i=I(P_i)\mathbf F_p[\Gamma_i].
\tag{3.4}
\]

Here the equality uses both the onto map in (3.1) and the definition of
\(P_i\) as the actual image of \(P\), rather than an independently chosen
subgroup.  Since \(P_i\) is normal, powers of (3.4) are
\(J_i^n=I(P_i)^n\mathbf F_p[\Gamma_i]\).  The augmentation ideal of a
finite \(p\)-group over \(\mathbf F_p\) is nilpotent, so \(J_i^n=0\) for
all sufficiently large \(n\), depending on \(i\).

If \(x\in\bigcap_nJ^nN\), its coordinate \(x_i\) lies in
\(J_i^nN_i\) for every \(n\), hence is zero.  The coordinates separate
points of \(N\), so \(x=0\). \(\square\)

No nilpotence exponent uniform in \(i\) is required.

## 4. The correctly typed enriched R07 specialization

Use v372's enriched joint group and its relative pro-\(3\) kernel

\[
 \widehat\Delta_\infty,
 \qquad
 \widehat P\triangleleft\widehat\Delta_\infty,
\tag{4.1}
\]

and put

\[
 \widehat\Xi=\mathbf F_3[[\widehat\Delta_\infty]],
 \qquad
 \widehat J=\ker\bigl(
 \widehat\Xi\to
 \mathbf F_3[[\widehat\Delta_\infty/\widehat P]]
 \bigr).
\tag{4.2}
\]

The following objects are conditional on one physical ABI: every retained
finite Magnus coordinate of v372, every reduction, and every occurrence
column must carry the action of the same finite image of
\(\widehat\Delta_\infty\), and all reduction squares must be equivariant.
Under that ABI, let

\[
 L_{\rm corr}\subseteq L_{\rm loc}
\tag{4.3}
\]

be the closed \(\widehat\Delta_\infty\)-stable correction module generated
by the reachable localized residuals and the actual occurrence-correction
values in the registered coarse-loop/formation--Brunnian lane.  This
restriction is essential: the broad path-bearing module \(L_{\rm loc}\) of
v372 also contains non-loop paths and is not asserted to equal the
correction target.  Its finite coordinates are required to be the actual
images of (4.3), with the induced equivariant reductions.  Lemma 3.1 then
gives

\[
 \bigcap_n\widehat J^nL_{\rm corr}=0.
\tag{4.4}
\]

Retain v369's completed free instruction source

\[
 \boxed{P_C=\widehat\Xi^r,}
\tag{4.5}
\]

and its cumulative actual-value map

\[
 \tau:P_C\longrightarrow A_C.
\tag{4.6}
\]

Thus \(A_C\) is not the free source.  Let the physically authenticated
leading occurrence map be

\[
 B_C:P_C\longrightarrow L_{\rm corr}.
\tag{4.7}
\]

It must be continuous and \(\widehat\Xi\)-linear, and must occur in the
v369 materialization square

\[
\begin{CD}
 P_C @>{\tau}>> A_C\\
 @V{B_C}VV       @VV{B_{\rm actual}}V\\
 L_{\rm corr} @= L_{\rm corr}.
\end{CD}
\tag{4.8}
\]

### Theorem 4.1 (ONE CORRECT LEADING QUOTIENT CLOSES THE LINEAR TAIL)

Under the physical action ABI, definitions (4.3)--(4.8), and the actual
finite-coordinate separation hypotheses of Lemma 3.1, suppose

\[
 \boxed{
 P_C/\widehat JP_C
 \longrightarrow
 L_{\rm corr}/\widehat JL_{\rm corr}
 \text{ is onto}.}
\tag{4.9}
\]

Then

\[
 \boxed{
 B_C(P_C)=L_{\rm corr},
 \qquad
 B_C(\widehat J^nP_C)=\widehat J^nL_{\rm corr}
 \quad(n\geq0).}
\tag{4.10}
\]

Consequently, every requested registered-lane residual already proved to
lie in \(\widehat J^nL_{\rm corr}\) has a source value
\(t_n\in\widehat J^nP_C\).  V369 Theorem 3.1 then materializes
\(\tau(t_n)\) as an actual depth-\(n\) registered-lane commutator value,
provided the square (4.8) is authenticated.  Ordinary word spelling is
asserted only after reduction to each requested finite level, by v369's
calibrated v98 rule; no one ordinary word is asserted simultaneously at
all infinite coordinates.

#### Proof

Apply Lemma 3.1 to obtain (4.4), and apply Theorem 2.1 to (4.7).  The last
statement is precisely v369 Theorem 3.1 applied to the resulting requested
element of \(\widehat J^nP_C\), followed by (4.8). \(\square\)

This removes finite freeness or projectivity of the target and a global
linear section from this onto/strictness step.  It does not replace any
splitting or kernel-base-change conclusion for which v362 or v365 was
separately invoked.

## 5. Relation to the exact first-successor calculation

V374 constructs the physical first-successor loop target

\[
 Z_0^{\rm loc}
 =T_{H1,0}^S\oplus T_{H2,0}^S\oplus T_{P,0}^{\rm loc}
\tag{5.1}
\]

and, conditional on the task198/task382 owner, proves

\[
 \lambda_0(W_C)=\operatorname {im}D_0^{\rm act}.
\tag{5.2}
\]

Let \(\bar B_C\) denote the reduction of (4.7) modulo \(\widehat J\).
The coarse-loop projection from (4.3), if it kills
\(\widehat JL_{\rm corr}\), induces the comparison in the direction

\[
 \boxed{
 \bar\lambda_0:
 L_{\rm corr}/\widehat JL_{\rm corr}
 \longrightarrow Z_0^{\rm loc}.}
\tag{5.3}
\]

There is no justified canonical arrow in the reverse direction.  To turn
the task395/v374 calculation into hypothesis (4.9), the physical package
must prove all of the following:

1. (5.3) is defined from the same enriched owner and is equivariant under
   every retained reduction;
2. (5.3) is an isomorphism, including injectivity--no deeper coinvariant
   survivor may be invisible at the first-successor coordinate; and
3. the actual occurrence image fills the entire target,
   \(\operatorname {im}D_0^{\rm act}=Z_0^{\rm loc}\), rather than merely
   containing one chosen defect; and
4. the task395 action closure is exactly the full
   \((\widehat\Xi/\widehat J)\)-action closure of the authenticated leading
   columns of \(B_C\), so the physical square proves

   \[
    \boxed{
    \bar\lambda_0\bigl(\operatorname {im}\bar B_C\bigr)
    =\lambda_0(W_C)=\operatorname {im}D_0^{\rm act}.}
   \tag{5.4}
   \]

Under these four facts, (5.4) identifies
\(\operatorname {im}\bar B_C\) with all of
\(L_{\rm corr}/\widehat JL_{\rm corr}\), proving (4.9).  By contrast, the
direct v374 membership test

\[
 -\beta_0\in\lambda_0(W_C)
\tag{5.5}
\]

solves only that one rung; it does not prove leading onto.

## 6. What remains before a compatible lift

The abstract compact theorem is complete, but its R07 hypotheses are not
silently promoted.  The remaining chain is:

1. authenticate the common physical enriched action ABI, the finite
   \(L_{\rm corr}\) coordinates, and the materialization square (4.8);
2. construct (5.3) and prove its isomorphism, authenticate the physical
   equality (5.4), and compute full leading onto (4.9);
3. replay v372's actual residual descent and localized stability for this
   same \(L_{\rm corr}\), rather than an endpoint-only or larger ambient
   module;
4. prove the intrinsic one-depth nonlinear return

   \[
    \Phi_{\rm lane}(w\,\operatorname {Mat}_n(t_n))
    -\Phi_{\rm lane}(w)-B_C(t_n)
    \in\widehat J^{n+1}L_{\rm corr};
   \tag{6.1}
   \]

5. assemble the resulting pro-\(3\) lane correction by v369/v98 and then
   discharge the non-pro-\(3\), perfect-core, and settlement gates.

After items 1--3 are established for the same physical owner, (6.1) is the
remaining analytic Newton step on this route.  Proving item 4 closes the
registered pro-\(3\) Newton recurrence; item 5 then remains outside that
lane.  A proof that every direct finite-rung accepted set is nonempty is a
separate alternative to the leading-onto/Newton route, not another item in
this dependency chain.  Nothing here changes the current fake/Ihara status.

```text
ABSTRACT LEADING ONTO => FULL ONTO:               PAPER PROOF
ABSTRACT FULL ONTO => STRICT AT ALL J-DEPTHS:     PAPER PROOF
FINITE RELATIVE-p TARGET SEPARATION:               PAPER PROOF
R07 SOURCE P_C = Xi-hat^r:                         CORRECTED TYPE
R07 REACHABLE LOOP MODULE / ACTION ABI:            OPEN AUTHENTICATION
MATERIALIZATION SQUARE:                            OPEN AUTHENTICATION
L_corr/JL_corr -> Z0loc ISOMORPHISM:               OPEN
ACTUAL LEADING ONTO:                               NOT COMPUTED
J-ADIC NONLINEAR ONE-DEPTH RETURN:                 OPEN
COMPATIBLE RELATIVE PRO-3 LIFT:                    NOT CONSTRUCTED
MIXED-PRIME / PERFECT-CORE / SETTLEMENT:           OPEN
FAKE / IHARA WITNESS:                              NOT DECLARED
```

`R07_COMPACT_SEPARATED_LEADING_ONTO_LIFT_V377_FINAL_AUDIT`

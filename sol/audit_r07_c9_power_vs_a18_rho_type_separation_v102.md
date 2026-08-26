# R07 C9-power versus A.18-rho type separation v102

Author: Sol / 2026-08-26

Status: paper audit and corrected interface.  It supersedes the proposed
*application* of v101 to the actual R07 A.18 problem.  The abstract cyclic
extension calculation in v101 remains valid under its stated A3 hypothesis,
but A3 is not supplied by v96 and is not a small replay.  No lift, fake
certificate, or Ihara witness is declared.  `verified=false`.

## 1. Three cyclic structures which must remain distinct

The current shelf contains three different cyclic operations.

1. The roof return lane uses

   \[
   R=\langle g\rangle\cong C_9,
   \qquad g=\mathrm{row36},
   \qquad D=\langle g^3\rangle\cong C_3.
   \tag{1.1}
   \]

   On an \(\mathbf F_3R\)-module, its periodic norm is

   \[
   N_g=1+g+\cdots+g^8=(g-1)^8.
   \tag{1.2}
   \]

2. The subgroup \(D\) in (1.1) is used to form the relative cyclic quotient

   \[
   K(R,D;V)=
   \frac{\ker(g-1)\cap(g-1)^6V}{(g-1)^8V}.
   \tag{1.3}
   \]

3. The rho word in v96 is the product of the **five structural
   substitutions** of one common word around the A.18 configuration:

   \[
   R_\rho(f)=\prod_{i=0}^{4}\rho^i(f)
   \tag{1.4}
   \]

   in its fixed printed order.  This is a \(C_5\)-shaped coface operation.
   It is not the action of the roof element row36 and it is not the norm
   (1.2).

V96 proves the exact shear

\[
 c_{A18}=r_\rho-h_1-Ah_2
\tag{1.5}
\]

and the corresponding Jacobian identity.  The only action in the shear is
the coarse conjugation \(A=\operatorname{Ad}(a(f_0))\) occurring in the
word identity.  Neither \(g=\mathrm{row36}\) nor the periodic resolution of
\(C_9\) occurs in that proof.

## 2. The missing implication is not formal

### Proposition 2.1 (NO C9-POWER BINDING FROM THE V96 SHEAR)

The v96 identities do not imply that a ninth-power defect \(t^9\) in an
extension of \(C_9\) equals either the rho residual or the literal A.18
residual.  This remains true even when the \(C_9\)-extension splits over
\(C_3\).

#### Proof

The two constructions have different inputs: (1.5) is an identity among
five coface evaluations of a word, whereas \(t^9\) is the periodic
representative of a group extension restricted to the roof subgroup
\(\langle g\rangle\).

There is also an explicit independence model.  Let

\[
 V=\mathbf F_3[J]/(J^7),\qquad g=1+J,
 \qquad \beta=J^6.
\tag{2.1}
\]

Then

\[
 \beta\in\ker J\cap J^6V,
 \qquad \beta\notin J^8V=0.
\tag{2.2}
\]

The standard classification of extensions by \(H^2(C_9,V)\) supplies an
extension whose cyclic power representative is \(\beta\).  Equation (2.2)
also says that its restriction class on \(C_3\) is zero, so the restricted
extension is split.  Independently choose the zero PaB residual stack

\[
 h_1=h_2=r_\rho=c_{A18}=0.
\tag{2.3}
\]

All v96 shear identities hold, while \(t^9=\beta\ne0=c_{A18}\).  Hence no
formal consequence of the shear identifies the two classes. \(\square\)

### Corollary 2.2 (STATUS OF V101)

The abstract implication proved in v101 is sound only after A3 is supplied:

\[
 t^9=\text{the normalized actual A.18 survivor}.
\tag{2.4}
\]

But (2.4) is the load-bearing chain comparison itself.  Calling it a
``row36 power replay'' does not reduce B2--B4 of v83, and the finite
full-pair restriction-zero result for the constructed module does not prove
(2.4).

In particular, v101 must not be used to promote

\[
 \operatorname{im}\bigl(K^2(P_0,H;V_{\rm mix})
 \longrightarrow K^2(R,D;V_{\rm mix})\bigr)=0
\tag{2.5}
\]

to an actual common-word correction.

## 3. Correct chain-level binding square

The full-pair route can still be useful, but it requires a typed comparison
between two complexes, not an equality of the two unrelated norms.  At one
actual diagram-chief edge one must construct a commutative square of the
form

\[
\begin{array}{ccc}
 K^2(P_0,H;V)&\xrightarrow{\operatorname{res}}&K^2(R,D;V)\\
 \substack{\downarrow\\[-1mm] B_P}&&
 \substack{\downarrow\\[-1mm] B_R}\\
 \mathcal O_{\rm PaB}^{\rm rel}(P_0,H)
 &\xrightarrow{\operatorname{ev}_{g}}&
 \mathcal O_{\rm PaB}^{\rm cyc}(g),
\end{array}
\tag{3.1}
\]

with all four objects built from the same actual kernel occurrence.  The
required data are:

1. the actual \(P_0\)-action on the complete common-word correction,
   two-hexagon, five-coface, and syzygy complex;
2. a displayed full-pair class \(\Omega_F\) whose image under \(B_P\) is
   the normalized residual of the exact word \(F\);
3. an exact comparison showing that
   \(B_R(\operatorname{res}\Omega_F)\) is the normalized **row36-action
   component** of that same residual;
4. a separate use of v96 to replace the rho coordinate by literal A.18
   after the two hexagon rows are retained;
5. proof that vanishing of the normalized component, together with the
   already handled forest/dihedral components, decodes to one admissible
   common-word correction.

The top arrow alone is what the repaired v4 computation determines for the
constructed coefficient module.  It supplies neither vertical arrow in
(3.1), does not prove that \(V_{\rm mix}\) occurs in the actual PaB kernel,
and does not identify the exact R07 residual with a full-pair class.

No \(243^2\)-entry cocycle table is logically mandatory: a based
presentation-resolution chain map and its generator/relator replay would be
sufficient.  What cannot be omitted is the chain map itself.

## 4. Consequence for the active explicit branch

The non-repeating order of work is therefore:

1. finish the fresh \(g_{760}\) L3 target6 screen;
2. if it returns a cross-checked NONMEMBER, kill only this explicit prefix;
3. otherwise construct from \(g_{760}\), in one actual matched occurrence,
   both the direct literal theta/tau/A.18 affine system and the v96
   theta/rho system, and require their exact shear equality;
4. compute the normalized actual residual and its actual correction image;
5. only then test whether the full-pair square (3.1) exists on the remaining
   return-even component.

This keeps the full-pair calculation available as a possible structural
explanation, while preventing it from replacing the actual-image test it was
supposed to prove.

## 5. Fixed ledger

```text
V96 RHO/LITERAL SHEAR:                         PAPER_PROOF
C9/C3 PERIODIC RELATIVE FORMULA:               PAPER_PROOF
C9 POWER == C5 RHO OR LITERAL A18:             NOT IMPLIED / TYPE-SEPARATED
V101 ABSTRACT EXTENSION LEMMA UNDER A3:         CONDITIONAL PAPER_PROOF
V101 A3 FOR THE ACTUAL R07 EDGE:                OPEN
FULL-PAIR RESTRICTION ZERO ON CONSTRUCTED Vmix: CROSS_CHECKED FINITE
ACTUAL Vmix OCCURRENCE:                         OPEN
ACTUAL BINDING SQUARE (3.1):                    OPEN
g760 FRESH TARGET6:                             IN PROGRESS
COMPATIBLE COFINAL R07 LIFT:                    NOT CONSTRUCTED
FAKE CERTIFICATE / IHARA WITNESS:               NOT DECLARED
```

No new finite computation, external source, or Lean proof is used in this
audit.

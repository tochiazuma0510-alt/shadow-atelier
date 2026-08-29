# R07 local antidifference prefix-typing erratum (v312)

Author: Sol / 2026-08-29

Status: correction to v311.  V311 Theorem 1.1, the abstract description of
the image of \(a\mapsto a(1-r)\), is correct.  Its direct R07 application
silently normalized every tagged endpoint to \(1-r_b\).  V193 explicitly
warns that signed and prefix-transported occurrence rows must retain their
literal endpoint.  The correct endpoint is a unit-twisted right difference
\(\epsilon_bp_b(1-r_b)\).  This note restores that prefix in the local
primitive and diagonal compatibility equations.  No actual endpoint or
witness is asserted.

## 1. Exact literal endpoint factorization

For each occurrence-resolved block \(b\), put

\[
 d_{0,b}=\widetilde D_{1,b}\widetilde d_b\in k[G_b].
\tag{1.1}
\]

The authoritative value is obtained by direct Fox endpoint replay.  For a
single oriented and prefix-transported path, retain the literal factorization

\[
 \boxed{
 d_{0,b}=\epsilon_b p_b(1-r_b),
 \qquad
 \epsilon_b\in\{1,-1\},\quad p_b,r_b\in G_b.}
\tag{1.2}
\]

For example, \(p(W-1)=-p(1-W)\), while a full pointed relation row
\(-\delta(R)\) has \(p=1\), \(\epsilon=1\), \(r=R\).  The triple in (1.2)
is not inferred from a block label: its two expanded group-algebra terms
must equal (1.1).

If a stored block is a sum of more than one oriented path, first refine it to
the v193 occurrence tags and apply (1.2) componentwise.  If no such literal
refinement is authenticated, v311's cyclic shortcut is unavailable for that
block and v310's general map \(m_d\) remains authoritative.

## 2. Correct local primitive

For \(a\in k[G_b]\), (1.2) gives

\[
 a d_{0,b}=\epsilon_ba p_b(1-r_b).
\tag{2.1}
\]

Define the bijective coefficient twist

\[
 T_b(a)=\epsilon_ba p_b.
\tag{2.2}
\]

Then

\[
 a d_{0,b}=\eta_b
 \quad\Longleftrightarrow\quad
 T_b(a)(1-r_b)=\eta_b.
\tag{2.3}
\]

V311 Theorem 1.1 therefore yields the same local obstruction

\[
 \boxed{\Sigma_{r_b}(\eta_b)=0.}
\tag{2.4}
\]

When it vanishes, let \(A_b\) be the deterministic finite-support potential
satisfying

\[
 A_b(1-r_b)=\eta_b,
\tag{2.5}
\]

and put \(K_b=\ker(a\mapsto a(1-r_b))\).  The complete set of coefficients
in the **original** coordinate is

\[
 \boxed{
 \mathcal P_b=epsilon_b(A_b+K_b)p_b^{-1}.}
\tag{2.6}
\]

#### Proof

The solutions in the twisted coordinate are exactly \(A_b+K_b\).  Invert
(2.2); since \(\epsilon_b^{-1}=\epsilon_b\), this gives (2.6).  \(\square\)

For \(r_b=1\), condition (2.4) says \(\eta_b=0\), and
\(K_b=k[G_b]\); equation (2.6) correctly returns every coefficient.

## 3. Correct seven-block diagonal criterion

Let

\[
 \mathcal P=\prod_b\mathcal P_b
 \subseteq\bigoplus_bk[G_b],
\tag{3.1}
\]

with all seven occurrence tags retained, and let

\[
 \rho_*:\mathcal L_1\longrightarrow\bigoplus_bk[G_b]
\tag{3.2}
\]

be v310's diagonal context map on the lift kernel.

### Theorem 3.1 (PREFIX-CORRECTED LOCAL-TO-DIAGONAL CRITERION)

The universal endpoint equation

\[
 \exists\ell\in\mathcal L_1:\qquad
 \widetilde D_1(\ell\widetilde d)=\eta
\tag{3.3}
\]

holds if and only if

\[
 \boxed{
 \Sigma_{r_b}(\eta_b)=0\ \text{for every }b,
 \qquad
 \rho_*(\mathcal L_1)\cap\mathcal P\ne\varnothing.}
\tag{3.4}
\]

#### Proof

The block-\(b\) equation in (3.3) is

\[
 \rho_{b,*}(\ell)d_{0,b}=\eta_b.
\tag{3.5}
\]

By (2.3)--(2.6), this holds exactly when the orbit sum vanishes and
\(\rho_{b,*}(\ell)\in\mathcal P_b\).  Requiring the same \(\ell\) in every
tagged block is precisely the intersection in (3.4).  \(\square\)

Using v310's Schreier words, the second condition becomes

\[
 \boxed{
 \mathcal P\cap
 \sum_i k[\Gamma]\rho_*(n_i-1)\ne\varnothing.}
\tag{3.6}
\]

This is the correct return-even/common-source target.  The blockwise right
translations by \(p_b^{-1}\) are load-bearing and cannot be removed unless
direct replay proves \(p_b=1\) in that block.

## 4. Supersession of v311

The following parts of v311 survive unchanged:

1. Theorem 1.1 and Corollary 1.2 for the abstract operator
   \(a\mapsto a(1-r)\);
2. existence of a finite-support local antidifference after orbit-sum zero;
3. the separation between local inversion and common-source compatibility;
4. the finite Schreier seed reduction from v310; and
5. the positive-only/UNKNOWN boundary for the infinite diagonal orbit.

The following unqualified v311 assertions are superseded:

```text
v311 (2.2) d0_b = 1-r_b:                    NOT GENERALLY TYPED
v311 local coefficient set A+K_r:           MISSING epsilon_b,p_b TWIST
v311 diagonal intersection (3.3)/(4.2):     REPLACED BY (3.4)/(3.6)
```

No claim about a computed target used the rejected formulas, so no actual
numerator is retracted.

## 5. Certificate additions

Before the local orbit test, a producer and checker must retain and replay:

1. the exact literal chain \(\widetilde d_b\);
2. its independently differentiated endpoint \(d_{0,b}\);
3. \(\epsilon_b,p_b,r_b\) and the expanded two-term equality (1.2);
4. the local potential (2.5) and inverse twist (2.6); and
5. the diagonal equality using the untwisted common coefficient
   \(\rho_{b,*}(\ell)\), not the blockwise primitive \(A_b\).

Mutating one prefix, orientation, right factor or inverse prefix must reject.

## 6. Fixed frontier

```text
ABSTRACT CYCLIC ANTIDIFFERENCE (v311 Section 1):    RETAINED
NAKED d0_b=1-r_b FOR ALL TAGS:                     REJECTED
PREFIX-TYPED LOCAL PRIMITIVE:                      PAPER PROOF
PREFIX-TYPED SEVEN-BLOCK DIAGONAL CRITERION:       PAPER PROOF
ACTUAL epsilon_b,p_b,r_b / eta_b:                  NOT COMPUTED
ACTUAL DIAGONAL ANCESTRY:                          NOT COMPUTED
RELATIVE PRO-3 CORRECTION / COFINAL LIFT:          NOT CONSTRUCTED
FAKE / IHARA WITNESS:                              NONE
```

`R07_LOCAL_ANTIDIFFERENCE_PREFIX_ERRATUM_V312_PAPER_GRADE`

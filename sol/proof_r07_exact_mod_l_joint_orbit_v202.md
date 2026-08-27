# R07 exact mod-l joint orbit v202

Author: Sol / 2026-08-28

Status: paper strengthening of v201 for the frozen R07 occurrence ledger.
The mod-\(\ell\) abelian joint source image has order exactly \(\ell^2\), not
merely at most \(\ell^2\), because the H1/1 occurrence already retains the
two independent source generators.  Thus the mod-2 and mod-3 repair screens
have exactly 4 and 9 translating states.  No screen has yet been run and no
exact repair, lift, fake certificate, or Ihara witness is declared.

## 1. Frozen standard occurrence

Let \(F=F(x,y)\).  In the eleven-occurrence ledger of v189, H1/1 is the
standard source-E3 occurrence

\[
 \rho_{xy}:F(x,y)\longrightarrow PB_3,
 \qquad
 x\longmapsto A_{12},
 \quad
 y\longmapsto A_{23}.
\tag{1.1}
\]

This is the literal \(f(x,y)\) slot, not the finite E3 evaluation of that
slot.  The task173 inventory records its evaluator as source substitution
followed by the standard \(F_2\to PB_3\) embedding.  It occurs once in H1
and again in H2, with different literal prefixes; one copy suffices for the
rank argument but both positions remain in every endpoint column.

For a prime \(\ell\), compose (1.1) with

\[
 PB_3\twoheadrightarrow
 A_{3,\ell}=H_1(PB_3,\mathbf Z/\ell)
 \cong(C_\ell)^3.
\tag{1.2}
\]

The classes of \(A_{12},A_{23},A_{13}\) are the standard basis in (1.2).

## 2. Exact joint rank

Let \(D_\ell\) be v201's image of the common source in the product of all
eleven mod-\(\ell\) abelian occurrence groups.

### Theorem 2.1 (EXACT JOINT ABELIAN ORBIT)

For every prime \(\ell\),

\[
 \boxed{D_\ell\cong(C_\ell)^2,
 \qquad |D_\ell|=\ell^2.}
\tag{2.1}
\]

#### Proof

Every target occurrence group is abelian of exponent \(\ell\), so the
eleven-coordinate joint map factors through

\[
 F(x,y)^{\mathrm{ab}}/\ell\cong(C_\ell)^2.
\tag{2.2}
\]

This gives \(|D_\ell|\le\ell^2\).  Projection of the joint map to its H1/1
coordinate is (1.1)--(1.2).  It sends the basis classes of \(x,y\) to the
independent basis classes of \(A_{12},A_{23}\), and hence has rank two.
The joint map therefore has rank at least two.  Together with (2.2), this
proves (2.1). \(\square\)

The argument does not use the finite roof quotient, task176's large joint
group order, or a guessed task198 action value.  It uses one exact PB
occurrence and therefore survives every correctly typed finite roof or
successor implementation.

## 3. Exact screen roster sizes

Let \(t\) be the size of a complete finite normal-relator roster for the
actual first successor.  Before exact duplicate-column removal, v200's
two-sided finite quotient selector registers exactly

\[
 |D_\ell|^2t=\ell^4t
\tag{3.1}
\]

triples \((\bar A,s_i,\bar B)\).  Therefore v201's two immediate screens
specialize to

\[
\begin{array}{c|c|c|c}
 \ell & |D_\ell| & \dim E_\ell &
 \text{registered triples before deduplication}\\ \hline
 2 & 4 & 80  & 16t\\
 3 & 9 & 783 & 81t.
\end{array}
\tag{3.2}
\]

These are exact coverage counts, not maximum word radii.  A producer may
deduplicate equal columns and stop inserting after rank saturation, but it
must still account for all \(16t\) or \(81t\) registered triples to claim a
complete projected NO.

## 4. Consequence for the explicit-witness path

After the actual \(M_0\) and complete first-successor normal relators exist,
the mod-2 and mod-3 screens can be dispatched independently.  Their marked
joint groups need no BFS larger than four and nine states.  By v200:

\[
 \text{screen NO}
 \Longrightarrow
 \text{no exact same-}\mu_1\text{ endpoint repair},
\tag{4.1}
\]

whereas screen YES supplies only coefficients to replay in exact PB normal
form.  Neither screen decides whether a different first-successor
multiplier works, and neither discharges prime-to-three or perfect-core
cofinal gates.

The independent checker recomputes (1.1) from the literal source pair,
checks the two independent exponent vectors in both characteristics, and
requires exact joint orders 4 and 9.  It rejects a source-generator swap,
rank-one collapse, occurrence deletion, or replacement of H1/1 by the
finite E3 value.

~~~text
MOD-l JOINT SOURCE IMAGE D_l = (C_l)^2:          PAPER_PROOF
MOD-2 JOINT ORBIT ORDER 4:                       PAPER_PROOF
MOD-3 JOINT ORBIT ORDER 9:                       PAPER_PROOF
FULL TWO-SIDED ROSTER SIZES 16t / 81t:           PAPER_PROOF
ACTUAL NORMAL-RELATOR COUNT t / M0 / ENDPOINT:   NOT AVAILABLE
MOD-2 / MOD-3 SCREEN RESULT:                     NOT RUN
EXACT SAME-mu1 REPAIR:                           NOT CONSTRUCTED
FAKE / IHARA WITNESS:                            NOT DECLARED
~~~

R07_EXACT_MOD_L_JOINT_ORBIT_V202_PAPER_GRADE

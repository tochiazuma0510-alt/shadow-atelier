# R07 task179-to-augmented edge compiler v144

Author: Sol / 2026-08-27

Status: paper theorem and lossless consumer contract.  This note fixes the
precise passage from a positive task179 receipt to the first v129/v141
augmented edge.  It does not assume that task179 succeeds, and it does not
assert that the resulting actual saturation class vanishes.

## 1. What a positive task179 receipt represents

Let (Z_0^{\rm raw}) be the typed direct sum of the two PB3 relation
modules, the PB4 relation module, and the two exponent coordinates used by
task179.  Let

\[
 D_0=D_{\rm H1}\oplus D_{\rm H2}\oplus D_{\rm P}
 \subseteq Z_0^{\rm raw},
 \qquad Z_0=Z_0^{\rm raw}/D_0.
\tag{1.1}
\]

The three summands in (D_0) remain block-tagged.  They are presentation
boundaries, not source corrections.

Let (T_0) be the raw all-seven defect of the fixed base word (g_{760}).
For every retained correction column put

\[
 w_j=\delta_j r_j\delta_j^{-1},
\tag{1.2}
\]

where both the section word (\delta_j) and the normal relator (r_j) are
recorded by task179.  Let (A_0) be the word-bearing correction module on
these orbit columns, and let

\[
 B_0:A_0\longrightarrow Z_0
\tag{1.3}
\]

be the simultaneous H1/H2/printed-pentagon change map.  For a positive
receipt with recovered coefficients (\alpha_j\in\{1,2\}\), define

\[
 a_0=\sum_j \alpha_j [w_j]\in A_0,
 \qquad
 c_0=\prod_j w_j^{\epsilon(\alpha_j)},
 \quad \epsilon(1)=1,
 \quad \epsilon(2)=-1,
\tag{1.4}
\]

in the retained column order.  Characteristic three makes the inverse word
in (1.4) the literal realization of coefficient 2.

### Proposition 1.1 (receipt extraction)

Suppose the helper-nonshared task179 checker accepts a `COMMON_WORD`
receipt.  Then its fields give a word-bearing (a_0), the literal word
(c_0), and a separately typed (d_{\rm boundary}\in D_0) satisfying

\[
 -T_0=d_{\rm boundary}+B_0^{\rm raw}a_0,
 \qquad
 \boxed{B_0a_0=z_0},
 \qquad z_0:=-[T_0]\in Z_0.
\tag{1.5}
\]

Moreover (g_{760}c_0) is the finite common word represented by this
coefficient.  The word (d_{\rm boundary}) is not defined and is not
needed.

#### Proof

The accepted receipt independently replays every selected direct column,
the coefficient-2 inverse, the exact sparse identity

\[
 \texttt{target}
 =d_{\rm boundary}+\sum_j\alpha_j B_0^{\rm raw}[w_j],
 \qquad \texttt{target}=-T_0,
\tag{1.6}
\]

and the ordered product (1.4).  Passing (1.6) to the quotient by (D_0)
gives (1.5).  Fox additivity on the registered joint kernel identifies the
sum of correction columns with the literal product (c_0).  The checker
also replays the right-correction convention, so the common word is
(g_{760}c_0).  Nothing maps a presentation boundary back to a source word.
\(\square\)

## 2. The first finer edge

Let a finer typed context have modules and maps

\[
 A_1\xrightarrow{B_1}Z_1,
 \qquad
 A_1\xrightarrow{p_A}A_0,
 \qquad
 Z_1\xrightarrow{p_Z}Z_0,
\tag{2.1}
\]

with (p_ZB_1=B_0p_A).  Let the finer target (z_1) satisfy
(p_Z(z_1)=z_0).  Choose the deterministic word lift
(\widehat a_0\in A_1) by replaying exactly the selected factors in (1.4)
in the finer context, and put

\[
 \boxed{e_1=B_1\widehat a_0-z_1.}
\tag{2.2}
\]

Equation (1.5) and the commuting square imply

\[
 p_Z(e_1)=0.
\tag{2.3}
\]

Thus the positive task179 receipt supplies the coarse solution and makes
(e_1) a named transverse error.  It does not imply that (e_1) is zero.

Assume now that the edge is controlled by a two-sided nilpotent ideal
(J\triangleleft\Lambda_1), with

\[
 \ker p_Z=JZ_1,
 \qquad JA_1\subseteq\ker p_A,
 \qquad J^L=0.
\tag{2.4}
\]

The actual positive question is the single typed membership

\[
 \boxed{
 e_1\in B_1(JA_1)+Jz_1.}
\tag{2.5}
\]

For a general context edge replace (JA_1) in (2.5) by the complete
word-bearing kernel (K_A=\ker p_A).  No assertion about the whole ambient
kernel is required.

## 3. Lossless augmented compilation

### Theorem 3.1 (TASK179-TO-AUGMENTED EDGE COMPILER)

Under (2.1)--(2.4), suppose a positive augmented solver returns

\[
 e_1=B_1d_{\rm saturation}+\rho z_1,
 \qquad
 d_{\rm saturation}\in JA_1,
 \qquad \rho\in J.
\tag{3.1}
\]

Put

\[
 U_\rho=(1+\rho)^{-1}
 =\sum_{m=0}^{L-1}(-\rho)^m,
 \qquad
 \boxed{a_1=U_\rho
       (\widehat a_0-d_{\rm saturation}).}
\tag{3.2}
\]

Then

\[
 \boxed{B_1a_1=z_1},
 \qquad
 \boxed{p_A(a_1)=a_0}.
\tag{3.3}

If the module realization records addition by ordered word product,
negation by inverse, and the group-ring action by the registered
translate/conjugate operation, (3.2) gives a finite ordinary correction
word.  Direct all-seven replay of that word is a positive certificate
independent of the augmented search strategy.

#### Proof

Equations (2.2) and (3.1) give

\[
 B_1(\widehat a_0-d_{\rm saturation})=(1+\rho)z_1.
\tag{3.4}
\]

Nilpotence gives the two-sided finite inverse (U_\rho).  Applying
(B_1) to (3.2) proves the first equality in (3.3).  Modulo (J), one has
(U_\rho\equiv1), while (d_{\rm saturation}) maps to zero; hence the
second equality follows.  Expanding the finite sum in the fixed module
basis and applying the stated realization rules materializes the word.
\(\square\)

For the fixed Jennings edge (J=I^9\) with (I^{29}=0), one may use the
short exact expression

\[
 \boxed{a_1=(1-\rho+\rho^2-\rho^3)
              (\widehat a_0-d_{\rm saturation}).}
\tag{3.5}
\]

## 4. What must be carried from task179

The first augmented consumer needs the following fields, all already
present in a positive task179 receipt or reconstructible from its pins:

1. `g760`, `target`, and the accepted `corrected_word`;
2. the ordered `selected_corrections`, including every coefficient,
   `delta_word`, `relator_word`, and literal factor word;
3. the separately tagged `boundary_chains` used only to establish (1.5);
4. the ten-coordinate and full-eleven direct replay of every selected
   correction and of their product; and
5. the reduction maps which replay the same selected factor words in the
   first finer context.

The compiler must construct `a0` from item 2, not from the boundary chain
and not by treating `corrected_word = g760 * correction_word` as one linear
column.  The finer target is the defect of the lifted base word; the
coefficient being corrected is the correction part (a_0).

The new receipt then records, in order:

\[
 \widehat a_0,quad e_1,quad
 d_{\rm saturation},\quad\rho,\quad U_\rho,\quad a_1,
\tag{4.1}
\]

with exact typed equalities (2.2), (3.1), and (3.3).  A failed or capped
membership search for (2.5) is `UNKNOWN`; it is not a failure of the
accepted finite common word.

## 5. Sequential consequence and boundary

Applying Theorem 3.1 at successive edges compiles each already accepted
word into a word reducing to it.  Hence compatibility along one chosen
cofinal ladder is automatic.  The remaining mathematical questions are
whether the actual membership (2.5) holds at every abelian edge and whether
the separately typed nonabelian accepted sets are nonempty.

```text
POSITIVE TASK179 RECEIPT -> WORD-BEARING a0:      PAPER_PROOF
BOUNDARY-CHAIN / SOURCE-CORRECTION SEPARATION:    PAPER_PROOF
NAMED FIRST FINER ERROR e1:                       PAPER_PROOF
POSITIVE (d_saturation,rho) -> COMPATIBLE WORD:   PAPER_PROOF
TASK179 COMMON_WORD RECEIPT:                      NOT YET COMPUTED
FIRST ACTUAL AUGMENTED MEMBERSHIP:                NOT YET COMPUTED
ALL COFINAL EDGES / NONABELIAN ACCEPTED SETS:     OPEN
COMPATIBLE R07 LIFT / FAKE / IHARA WITNESS:       NOT DECLARED
```

`R07_TASK179_TO_AUGMENTED_EDGE_COMPILER_V144_PAPER_GRADE`

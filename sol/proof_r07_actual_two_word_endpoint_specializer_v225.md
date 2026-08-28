# R07 actual two-word endpoint specializer v225

Author: Sol / 2026-08-28

Status: paper erratum and replacement for v221 Sections 2--4.  The original
signed target and the corrected residual are attached to two different
literal words.  This note fixes those words and signs, gives a canonical
occurrence decomposition compatible with the task179 prefix convention, and
fixes the class-two exponent-nine arithmetic needed by an implementation.
It does not contain the two positive production receipts or an actual gate
result.  No compatible lift, fake certificate, or Ihara witness is declared.
`verified=false`.

## 1. The two words and the task179 sign

Put \(k=\mathbf F_3\), let

\[
 g_0=g_{760},\qquad a=c_{\rm exact},\qquad f=g_0a,
\tag{1.1}
\]

where \(a\) and \(f\) are authenticated by a positive task192 receipt.  For
\(B\in\{H1,H2,P\}\), let \(R_B(w)\) be the literal printed A.18 block word
obtained by substituting \(w\).  All factor orders, inverse slots, PB3 lifts,
and PB4 substitutions are those of the frozen task179 constructor.

Write \(\delta_B\) for the left Fox chain in the complete PB3 or PB4
presentation module.  Task179 defines its correction target as the negative
raw base row.  Thus the signed original target is

\[
 \boxed{d_B=-\delta_B R_B(g_0).}
\tag{1.2}
\]

The direct right-correction column of \(a\) is

\[
 (Ba)_B=\delta_B R_B(f)-\delta_B R_B(g_0).
\tag{1.3}
\]

Consequently the residual used by v174 is

\[
 \boxed{
 e_B=d_B-(Ba)_B=-\delta_B R_B(f).}
\tag{1.4}
\]

In particular, the raw relation defect of the corrected word is \(-e_B\),
as stated in v174.  Applying the Fox endpoint identity gives

\[
 \boxed{
 D_{1,B}d_B=1-\overline{R_B(g_0)},\qquad
 \epsilon_B:=D_{1,B}e_B=1-\overline{R_B(f)}.}
\tag{1.5}
\]

Equations (1.2)--(1.5) are also a direct audit of the executable convention:
`exact_target` is minus `raw_base_targets`, while `direct_column([],a)` is
the corrected gradient minus the base gradient.

V221 incorrectly applied the same corrected word \(f\) when defining both
the occurrence target and the residual.  That would replace \(d\) by a
second copy of \(e\) and changes the v214/v216 action vector.  V221 is
superseded on this point by (1.2)--(1.5).

## 2. Canonical occurrence target and frozen prefixes

Let \(o=1,\ldots,11\) be an occurrence in the immutable task198 ledger.  Put

\[
 \sigma_o=\texttt{factor\_sign}(o)\in\{1,-1\},\qquad
 r_o=\rho_o(g_0)\in PB_{B(o)}.
\tag{2.1}
\]

Let \(Q_o\) be the product of the signed base factors named, in the listed
order, by `fox_prefix_occurrences(o)`.  This is the frozen right-to-left
paper-product prefix; it is reconstructed from the literal factors and not
replaced by the identity.  The task179 right-correction prefix is

\[
 \boxed{
 P_o=
 \begin{cases}
 Q_or_o,&\sigma_o=1,\\
 Q_o,&\sigma_o=-1.
 \end{cases}}
\tag{2.2}
\]

Define the intrinsic occurrence chain and endpoint by

\[
 \boxed{
 d_o=\delta_{B(o)}(r_o^{-1}),\qquad
 \xi_o=D_{1,B(o)}d_o=r_o^{-1}-1.}
\tag{2.3}
\]

### Proposition 2.1 (EXACT OCCURRENCE DECOMPOSITION)

With (2.1)--(2.3),

\[
 \boxed{d_B=\sum_{o\in B}\sigma_oP_od_o.}
\tag{2.4}
\]

#### Proof

For a direct factor \(r_o\), its contribution to
\(-\delta R_B(g_0)\) is \(-Q_o\delta(r_o)\).  Since

\[
 r_o\delta(r_o^{-1})=-\delta(r_o),
\tag{2.5}
\]

the corresponding term in (2.4) is
\(Q_or_o\delta(r_o^{-1})=-Q_o\delta(r_o)\).

For an inverse factor \(r_o^{-1}\), its contribution to
\(-\delta R_B(g_0)\) is

\[
 -Q_o\delta(r_o^{-1})=Q_or_o^{-1}\delta(r_o),
\tag{2.6}
\]

which is again exactly the term \(\sigma_oP_od_o\) in (2.4).  Summing the
literal product rule in the frozen block order proves the claim. \(\square\)

This decomposition explains the apparently asymmetric task179 prefix rule:
the base factor is appended to the prefix in a direct slot and not in an
inverse slot.  The uniform endpoint \(r_o^{-1}-1\) then handles both cases
without a second inverse or a second sign.

The data in (2.1)--(2.3) use \(g_0\), not \(f\).  Only the fixed residual
endpoint (1.5) uses \(f\).

## 3. Correct two-input specialization

The actual PB package is

\[
 \mathcal S_{\rm PB}(g_0,f)=
 \left(
 (B(o),\rho_o,\sigma_o,P_o,\xi_o)_{o=1}^{11},
 (\epsilon_B)_{B=H1,H2,P}
 \right).
\tag{3.1}
\]

It is determined by exactly the following authenticated data:

1. task192: \(g_0,a,f\), right-correction ancestry, and the direct
   eleven-occurrence replay;
2. task198: the ten-to-eleven typed ledger, signs, orientations, prefix
   occurrence lists, and the reusable roof/presentation interface; and
3. pinned static constructors: the literal H1/H2/P substitutions, the
   complete PB presentations, and the canonical exponent-nine quotients.

No word-specific field is added to task198.  Conversely, task198 alone
cannot determine (3.1), because it is deliberately word-independent.

An implementation may compute \(\epsilon_B\) either from the right side of
(1.5) or from \(d_B-(Ba)_B\).  It must compute both in SELFTEST and require
literal equality after PB collection.  It must not import the roof boundary
chains as if they were \(e_B\): those chains certify a finite roof equality,
whereas (1.4) is the universal PB residual chain.

## 4. Canonical class-two exponent-nine arithmetic

For \(r\in\{3,4\}\), put

\[
 Q_{r,1}=PB_r/\langle\gamma_3PB_r,g^9\ (g\in PB_r)\rangle^{\rm normal}.
\tag{4.1}
\]

Order the degree-one generators \(A_{ij}\) lexicographically and order the
central generators \(c_{ijk}\) lexicographically.  Write

\[
 a_r={r\choose2},\qquad b_r={r\choose3}.
\tag{4.2}
\]

An element of \(Q_{r,1}\) has the unique coordinate form

\[
 (a,z)\in(\mathbf Z/9)^{a_r}\times(\mathbf Z/9)^{b_r}.
\tag{4.3}
\]

For ordered degree-one generators \(G_i<G_j\), let
\(B_{ij}\in(\mathbf Z/9)^{b_r}\) be the coordinate vector of
\([G_i,G_j]=G_i^{-1}G_j^{-1}G_iG_j\).  For \(i<j<k\), the nonzero brackets
are

\[
 [A_{ij},A_{ik}]=c_{ijk},\qquad
 [A_{ij},A_{jk}]=-c_{ijk},\qquad
 [A_{ik},A_{jk}]=c_{ijk},
\tag{4.4}
\]

together with skew-symmetry; disjoint pairs commute.  Collection in the
chosen normal form gives

\[
 \boxed{
 (a,z)(b,w)=
 \left(a+b,
 z+w-\sum_{i<j}a_jb_iB_{ij}\right)}
 \pmod 9,
\tag{4.5}
\]

and

\[
 \boxed{
 (a,z)^{-1}=\left(-a,
 -z-\sum_{i<j}a_ia_jB_{ij}\right)}
 \pmod 9.
\tag{4.6}
\]

The PB3 keys therefore have width \(3+1=4\), and the PB4 keys have width
\(6+4=10\).  These are the keys of the occurrence group algebras.  They are
not the three coordinates of the common actor

\[
 D_1\cong\mathcal H_2(9),\qquad |D_1|=9^3=729.
\tag{4.7}
\]

The map from \(D_1\) to the \(o\)-th occurrence quotient is obtained by
evaluating its marked generators through the same literal substitution
\(\rho_o\).  Thus an actor is a three-coordinate Heisenberg element, while
its action is on sparse Q3/Q4 group-algebra elements with four- or ten-
coordinate keys.  This type distinction is load-bearing.

## 5. Exponent-nine package and endpoint formula

Project (3.1) to the appropriate \(Q_{r,1}\).  Put

\[
 p_o=\overline{P_o},\qquad
 \bar\xi_o=\overline{\xi_o},\qquad
 w_o=\sigma_op_o\bar\xi_o,
\tag{5.1}
\]

and retain

\[
 w=(w_o)_{o=1}^{11}\in
 \widehat E_1=\bigoplus_{o=1}^{11}k[Q_{B(o),1}].
\tag{5.2}
\]

Also put

\[
 \bar\epsilon_1=
 (\overline{\epsilon_{H1}},
  \overline{\epsilon_{H2}},
  \overline{\epsilon_P}).
\tag{5.3}
\]

For \(g\in D_1\), the occurrence action is

\[
 (g\mathbin\odot v)_o
 =p_o\,q_o(g)\,p_o^{-1}v_o.
\tag{5.4}
\]

Let \(C\) sum only after the eleven occurrence coordinates have been acted
on.  Then v214's actual projected endpoint is

\[
 \boxed{
 \bar\eta_1(\mu)=
 \bar\epsilon_1-C(\mu\mathbin\odot w).}
\tag{5.5}
\]

#### Proof

Proposition 2.1 gives the exact original target decomposition required in
v194.  Applying the endpoint map gives (5.1).  Equation (1.5) gives the
fixed residual term (5.3).  The canonical occurrence quotients factor the
source action through \(D_1\), so v214 Theorem 2.1 applies and yields (5.5).
No choice of source representative or boundary preimage occurs. \(\square\)

The v216 pre-gate seed is therefore

\[
 h=[x,y],\qquad z_0=h^3,\qquad
 u_0=(z_0-1)\mathbin\odot w,
\tag{5.6}
\]

with \(z_0\) distinguished from the hexagon abbreviation
\((xy)^{-1}\).

## 6. Replacement implementation contract

A new implementation must not patch the rejected task219 specializer.  It
must consume the two authenticated receipts and independently establish:

1. `corrected_word == reduce(g760 + c_exact)` and the exact right-correction
   replay;
2. the eleven \(r_o=\rho_o(g_0)\), signed base factors, prefix products
   \(Q_o\), and task179 prefixes (2.2);
3. the two independent target identities (2.4) and (1.2);
4. the two independent residual identities in Section 3;
5. the Q3/Q4 arithmetic (4.4)--(4.6), including exhaustive group-axiom and
   inverse checks in SELFTEST-sized fixtures;
6. the marked \(D_1\to Q_{B(o),1}\) maps and the distinction between actor
   triples and Q3/Q4 keys;
7. \(w,\bar\epsilon_1,u_0\), with exact sparse ancestry for every term; and
8. destructive rejection after changing either word, one occurrence type,
   repeated E3 insertion, E3/E4 `C21`, sign, orientation, prefix slot,
   inverse factor, factor order, bracket sign, quotient map, residual sign,
   or ancestry coefficient.

The independent checker reconstructs the PB class-two arithmetic, factors,
prefixes, and both word roles without importing producer helpers.  A
SELFTEST acceptance completes only the implementation milestone.  Actual
specialization requires positive task192 and task198 production receipts.

## 7. Fixed frontier

\[
\begin{array}{ll}
\text{TWO-WORD SIGN AND ROLE AUDIT} & \text{PAPER PROOF},\\
\text{CANONICAL OCCURRENCE DECOMPOSITION} & \text{PAPER PROOF},\\
\text{Q3/Q4 CLASS-TWO ARITHMETIC} & \text{EXPLICIT PAPER MODEL},\\
\text{ACTUAL TASK192 WORD} & \text{AWAITING PRODUCTION TERMINAL},\\
\text{ACTUAL TASK198 INTERFACE} & \text{AWAITING PRODUCTION TERMINAL},\\
\text{SPECIALIZER SELFTEST} & \text{NOT RUN},\\
\text{ACTUAL }(w,\bar\epsilon_1,u_0) & \text{NOT COMPUTED},\\
\text{V216 MEMBERSHIP OR DUAL} & \text{NOT RUN},\\
\text{COMPATIBLE LIFT / FAKE / IHARA} & \text{NOT DECLARED}.
\end{array}
\]

`R07_ACTUAL_TWO_WORD_ENDPOINT_SPECIALIZER_V225_PAPER_GRADE`

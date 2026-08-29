# R07 registered pro-3 source-gate collapse v367

Author: Sol / 2026-08-30

Status: paper specialization after v37, v38, v94, v248, v260, v359 and
v360.  It specializes the generic homogeneous source \(C_{\rm adm}\) of
v359 to the gate ledger actually registered for the relative pro-\(3\)
witness lane.  On that lane the first-edge homogeneous source is exactly
\(C_{\rm rel}\); task382 therefore does not need a second source-side
echelon after it extracts \([\widetilde S,K]\).  This does not identify the
actual leading module or localized target, prove leading surjectivity, or
construct a compatible lift, fake certificate, or Ihara witness.
`verified=false`.

## 1. Exact scope of the statement

Retain the task198 ten-context first edge

\[
 \rho_1:\widehat F_2\twoheadrightarrow\Delta _1,
 \qquad
 \rho_0:\widehat F_2\twoheadrightarrow\Delta _0,
 \qquad
 K=\ker(\Delta _1\to\Delta _0),
\tag{1.1}
\]

and put \(S=PSL(2,8)\).  On the relative-formation branch, v37 and v359
define

\[
 C_{\rm rel}
 =\rho_1(\Pi_S\cap\ker\rho_0)
 =R_S(\Delta _1)\cap K.
\tag{1.2}
\]

The gate ledger in this note is exactly the one used in v248 Section 5 and
v260 Section 4:

1. the complete task198 coarse value is fixed;
2. the correction is relative-formation typed;
3. \(m=0\) and an exact commutator representative is retained; and
4. the corrected tuple stays on the matched pro-\(3\) Frattini lane above
   the already onto coarse tuple.

The two hexagons, the printed pentagon, their formation/Brunnian support,
and prescribed residual values are equations in the residual target.  They
are not homogeneous kernels silently intersected with (1.2).

No settled self-shadow condition, new finite evaluation map outside
\(\Delta _0\), mixed-prime condition, or perfect-core condition is included
in this theorem.  If such a condition is later physically registered, its
linearization must be appended and the equality below must be re-audited.

## 2. Every registered homogeneous source condition is already in \(C_{\rm rel}\)

### Lemma 2.1 (COARSE, FORMATION, AND COMMUTATOR TYPING)

Every \(c\in C_{\rm rel}\) has the following properties at the first edge:

\[
 \pi(c)=1,
 \qquad c\in R_S(\Delta _1),
 \qquad c\in\Delta _1'.
\tag{2.1}
\]

Moreover \(c\) has an ordinary finite word representative which is
roof-trivial and has exact integer exponent sums \((0,0)\).

#### Proof

The first two assertions are (1.2).  V37 supplies a profinite preimage
\(u\in\Pi_S\cap\ker\rho_0\), and v38 gives
\(\Pi_S\leq[\widehat F_2,\widehat F_2]\); hence the finite value lies in
\(\Delta _1'\).  Equivalently, since
\(\rho_1([F_2,F_2])=\Delta _1'\), choose an ordinary commutator word with
value \(c\).  Its value lies in \(K\), so it is trivial in \(\Delta _0\),
and membership in \([F_2,F_2]\) gives exact exponent sums \((0,0)\).
\(\square\)

For the basis emitted by task382 no existential word search is needed.
If \(s_a\) is a retained residual-generator word and \(u_i\) is a retained
\(K\)-basis word, the literal commutator

\[
 [s_a,u_i]\longmapsto (S_a-I)k_i
\tag{2.2}
\]

is already such an ordinary roof-trivial exponent-zero representative.
As required by v359 and the task382 contract, (2.2) is not relabelled as an
element of \(\Pi_S\): v37 supplies relative-formation ancestry for the same
finite value, while the displayed word supplies literal common-word
ancestry.

### Lemma 2.2 (UNIT AND ONTO DO NOT CUT THE SOURCE)

On the registered lane the unit and onto gates impose no homogeneous linear
restriction on \(C_{\rm rel}\).

#### Proof

The R07 branch has \(m=0\), so \(2m+1=1\) is unchanged by every word
correction.  For onto, v94 Theorems 2.1 and 3.1 show that every compatible
lift of the already generating coarse marked tuple generates at every
matched pro-\(3\) Frattini refinement.  Thus onto is a consequence of the
coarse tuple and the Frattini type of the transition; it is not a kernel in
the first-edge correction variable.  This is exactly the use made in v248
Theorem 3.1 and v260 Theorem 4.1. \(\square\)

## 3. The first-edge equality

Recall v359's generic definition

\[
 C_{\rm adm}=C_{\rm rel}\cap\bigcap_j\ker s_j,
\tag{3.1}
\]

where the \(s_j\) range only over physically registered homogeneous linear
source gates.

### Theorem 3.1 (REGISTERED PRO-3 SOURCE-GATE COLLAPSE)

For the ledger of Section 1,

\[
 \boxed{C_{\rm adm}=C_{\rm rel}
 =R_S(\Delta _1)\cap K
 =[R_S(\Delta _0),K].}
\tag{3.2}
\]

For the authenticated task176/task198 roof,
\(R_S(\Delta _0)=\widetilde S\), and therefore

\[
 \boxed{C_{\rm adm}=[\widetilde S,K]
 =\operatorname{im}(S_1-I)+\operatorname{im}(S_2-I).}
\tag{3.3}
\]

#### Proof

Membership in (1.2) already fixes the complete coarse \(\Delta _0\) value
and supplies relative-formation typing.  Lemma 2.1 supplies the exact
commutator/charming condition.  Lemma 2.2 removes unit and pro-\(3\) onto
from the source intersection.  The remaining registered relations and
support statements are target equations by the ledger of Section 1, so the
index set in (3.1) is empty.  Hence \(C_{\rm adm}=C_{\rm rel}\).

V359 Theorem 2.1 gives
\(C_{\rm rel}=[R_S(\Delta _0),K]\); v149 identifies the residual with
\(\widetilde S\), and the two cross-checked v360/task382 generators give the
last matrix formula. \(\square\)

### Corollary 3.2 (NO SECOND SOURCE ECHELON AFTER TASK382)

Once a positive A4 receipt supplies the actual \(K\)-basis and action
matrices, the task382 block echelon already returns the complete finite
homogeneous source for the registered pro-\(3\) route.  If
\(c_1,\ldots,c_r\) is its basis and \(A=\mathbf F_3[\Delta _1]\), then

\[
 I_{\rm adm}=I_{\rm rel}
 =\sum_{i=1}^r A(c_i-1).
\tag{3.4}
\]

Thus the next finite source operation is the legal occurrence closure of
v359 Theorem 4.1, not an unspecified side-gate intersection.

## 4. What the equality does not close

Equation (3.2) is a finite source-value statement.  It leaves all of the
following load-bearing gates unchanged:

1. authenticate the positive A4 \(K\), its actions, and the task382 basis;
2. identify the actual leading correction module \(A_{\rm legal}/JA_{\rm
   legal}\) with (3.4), or with an explicitly proved quotient of it;
3. construct the strict localized target \(L/JL\) and compare it with the
   legal occurrence image;
4. prove leading surjectivity or return the exact v361/v365 defect;
5. retain compatible finite word spellings and replay the literal nonlinear
   H1/H2/P corrections; and
6. handle mixed-prime, perfect-core, and any independently registered
   settlement condition outside the pro-\(3\) ledger.

In particular, task382's literal commutator words certify finite common-word
ancestry; they are not individual nontrivial discrete elements of \(\Pi_S\).
The relative ancestry is the v37 actual-image statement, and compatible
ordinary spellings across finer quotients still use the nested-kernel
materialization of v98/v260.

```text
REGISTERED FIRST-EDGE HOMOGENEOUS SOURCE C_adm=C_rel: PAPER PROOF
C_rel=[tilde-S,K] FINITE EXTRACTION:                  IMPLEMENTED / A4 PENDING
EXTRA FIRST-EDGE SOURCE-GATE ECHELON:                 REMOVED ON PRO-3 LEDGER
ACTUAL A_legal/JA_legal IDENTIFICATION:               OPEN
ACTUAL L/JL / LEADING ONTO:                           OPEN
NONLINEAR H1/H2/P DEPTH RECURRENCE:                   OPEN
MIXED-PRIME / PERFECT-CORE / NEW SETTLEMENT GATES:    SEPARATE
COMPATIBLE LIFT / FAKE / IHARA WITNESS:               NOT CONSTRUCTED
```

`R07_REGISTERED_PRO3_SOURCE_GATE_COLLAPSE_V367_PAPER_GRADE`

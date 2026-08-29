# R07 free relative-seed Newton source v368

Author: Sol / 2026-08-30

Status: conditional paper reduction after v37, v98, v169, v248, v251, v260,
v319, v359, v367.  A positive task382 basis of the first-edge relative value
space can be lifted once to a finite tuple of compatible relative profinite
seeds.  A completed free coefficient module on those seeds is a sufficient
source for the localized Newton theorem **provided** its actual ordered
materialization is legal and filtration-preserving at every depth.  On that
positive route one does not have to identify the quotient of the entire legal
correction kernel before testing leading surjectivity.  Completed
materialization, the strict localized target and actual leading surjectivity
are still open.  No compatible lift, fake certificate, or Ihara witness is
declared.
verified=false.

## 1. A first-edge basis lifts to finitely many compatible relative seeds

Put

\[
 K_0=\Pi_S\cap\ker q_0\leq\widehat F_2,
\tag{1.1}
\]

and let

\[
 \Psi_n:\widehat F_2\twoheadrightarrow H_n
\tag{1.2}
\]

be the fixed nested joint images along the registered relative pro-\(3\)
lane, all carrying the same coarse \(q_0\) coordinate.  Write

\[
 C_n=\Psi_n(K_0)
     =R_S(H_n)\cap\ker(H_n\to Q_0).
\tag{1.3}
\]

V37 Section 4 proves that every transition

\[
 C_{n+1}\twoheadrightarrow C_n
\tag{1.4}
\]

is onto.  At the first active edge, v367 and task382 give

\[
 C_1=C_{\rm rel}=[\widetilde S,K].
\tag{1.5}
\]

### Theorem 1.1 (FINITE RELATIVE-SEED LIFT)

Let \(c_1,\ldots,c_r\) be any ordered basis of \(C_1\).  There exist

\[
 a_1,\ldots,a_r\in K_0
\tag{1.6}
\]

such that

\[
 \Psi_1(a_i)=c_i
\quad(1\leq i\leq r).
\tag{1.7}
\]

Their reductions on the registered lane may be selected by one deterministic
no-backtracking procedure: recursively choose the least retained preimage
under (1.4).  After finite word-bearing representatives of those values are
retained, the v98 nested-kernel rule makes their ordinary exponent-zero
spellings compatible on that lane.

#### Proof

Starting with \(c_{i,1}=c_i\), surjectivity of (1.4) permits a lift
\(c_{i,n+1}\in C_{n+1}\) of every already selected \(c_{i,n}\).  A fixed
finite ordering makes the choice deterministic and never requires
backtracking.

For each \(n\), the fibre

\[
 X_{i,n}=\{a\in K_0:\Psi_n(a)=c_{i,n}\}
\tag{1.8}
\]

is nonempty and closed in the compact group \(K_0\), and compatibility
gives \(X_{i,n+1}\subseteq X_{i,n}\).  Hence
\(\bigcap_nX_{i,n}\ne\varnothing\); choose \(a_i\) in the intersection.
This proves (1.6)--(1.7).

V37--v38 put every finite \(c_{i,n}\) in the image of the commutator
subgroup.  Once an ordinary representative is found by enumeration in the
finite joint image, v98 chooses shortlex-first exponent-zero corrections in
the accumulated kernels.  The resulting ordinary words have the reductions
of one permissible \(a_i\) at every registered level.  This last assertion
is lane-wise; the compactness argument above, not the finite spelling alone,
is what places \(a_i\) in the global subgroup \(K_0\). \(\square\)

At level one the task382 literal commutator may be used as the first
ordinary representative because it has value \(c_i\), coarse value one and
exact exponent vector zero.  The theorem does not claim that this one
discrete word itself belongs to \(\Pi_S\).  Its finer nested corrections
realize the same point on the registered lane.  They may be said to converge
to the global seed only after cofinality of the maps \(\Psi_n\) in the full
profinite topology is proved.  Global membership in \(K_0\) comes instead
from the compact-fibre argument in Theorem 1.1.

## 2. The free parameter module and the materialization hypothesis

Let

\[
 \Xi=\mathbf F_3[[\Delta_\infty]]
\tag{2.1}
\]

be the completed diagonal context algebra of v248/v260.  Put

\[
 P=\ker(\Delta_\infty\to\Delta_0),
 \qquad
 J=\overline{\langle p-1:p\in P\rangle}\triangleleft\Xi,
\tag{2.2}
\]

and define the free complete parameter module

\[
 P_C=\Xi^r
\tag{2.3}
\]

with ordered basis \(e_1,\ldots,e_r\).  The assignment

\[
 e_i\longmapsto a_i
\tag{2.4}
\]

is interpreted as a materialization instruction, not as an assertion that
the profinite correction group is a free additive module.

Let \(C_{n,\mathrm{act}}\) denote the retained active elementary-abelian
linear value of \(C_n\), with its authenticated diagonal context action, and
put

\[
 A^{\rm rel}=\varprojlim_n C_{n,\mathrm{act}}.
\tag{2.5}
\]

When those actions and transitions are compatible, the seed values define a
continuous linear instruction map

\[
 \tau:P_C\longrightarrow A^{\rm rel}.
\tag{2.6}
\]

Write

\[
 a_{i,n}:=\Psi_n(a_i)=c_{i,n}.
\tag{2.7}
\]

For a finite coefficient

\[
 v=\sum_{i,g}b_{i,g}\,g e_i,
\qquad b_{i,g}\in\mathbf F_3,
\tag{2.8}
\]

one may form a finite-level word in the fixed
\((i,g)\)-order as the product of the retained conjugates
\((g a_{i,n} g^{-1})^{\widetilde b_{i,g}}\), with
\(\widetilde 0=0,\widetilde1=1,\widetilde2=-1\).  At a fixed finite
quotient this product is finite and witnesses the required graded class.
These independently ordered exact products are **not** asserted to form a
compatible inverse system.

### Materialization Hypothesis 2.1 (ACTUAL FILTERED FREE-SEED VALUES)

Assume that:

1. the retained context action makes every \(\tau(v)\) a compatible actual
   \(K_0\)-value class;
2. the v260 compact-fibre realization applies with \(K_0\) in place of
   \(\mathcal C^{\rm com}\), giving a continuous ordered materialization
   \(\operatorname{Mat}:P_C\to K_0\); and
3. for every \(d\geq0\),

   \[
   \operatorname{Mat}(J^dP_C)\subseteq
   \{\text{relative words of depth at least }d\}.
   \tag{2.9}
   \]

Then every such materialization:

1. lies in \(K_0\);
2. has exact commutator/charming type;
3. preserves the complete coarse mark; and
4. preserves onto throughout the matched pro-\(3\) Frattini lane.

#### Justification and exact boundary

First form the compatible linear classes in \(A^{\rm rel}\); only then apply
the v260 compact-fibre argument.  The finite ordered products above witness
their graded classes, rather than supplying a compatible system of exact
products by themselves.  The subgroup \(K_0\) is normal in
\(\widehat F_2\), so it contains every conjugate, product and inverse used in
(2.8).  Also
\(K_0\leq\Pi_S\leq[\widehat F_2,\widehat F_2]\), which gives the first three
claims and exponent-zero ordinary approximants.  V94, as used in v248 and
v260, gives the fourth claim for every compatible lift of the fixed coarse
onto tuple.

V251 Lemma 3.1 proves the one-graded-layer ordered-product statement and its
deeper error.  It does not by itself prove (2.9) for arbitrary completed
\(J^d\)-combinations, so Hypothesis 2.1 is retained as a load-bearing open
condition.  Here “legal” means only the v367 ledger: coarse mark, relative
formation, \(m=0\)/commutator type, and matched pro-\(3\) onto.  Settled
self-shadow conditions, new evaluations outside \(\Delta_0\), mixed-prime
conditions, and perfect-core conditions are not included.  A new homogeneous
condition must either be included in \(q_0\), forcing \(C_1\) to be
recomputed, or be intersected separately; nonlinear settlement remains an
extra target/replay hypothesis.

Let \(L\) be the actual complete localized residual module, assuming it has
been authenticated.  Under Hypothesis 2.1, the compatible occurrence/Fox
maps of v169 and the one-depth affine law define a continuous
\(\Xi\)-linear map

\[
 B_C:P_C\longrightarrow L,
 \qquad B_C(e_i)=B(a_i).
\tag{2.10}
\]

The fact that two formal parameters might materialize to the same finite
group value causes no type problem: \(P_C\) is a free instruction module,
and (2.10) is its Jacobian.  Injectivity of materialization is neither stated
nor used.

## 3. Free-source localized Newton theorem

Let \(\Phi\) denote the exact two-hexagon/printed-pentagon residual map on
the reachable relative words, with values in the authenticated localized
module \(L\).

### Theorem 3.1 (FREE RELATIVE-SEED NEWTON SOURCE)

Assume:

1. \((\Xi,J)\) is complete and separated, and \(L\) is complete, separated
   and finitely generated over \(\Xi\), with a
   strict finite free cover \(q:F\twoheadrightarrow L\);
2. Materialization Hypothesis 2.1 holds on exactly the v367 registered
   relative pro-\(3\) ledger;
3. every reachable exact nonlinear residual remains in \(L\), and localized
   stability holds for every correction returned from \(P_C\);
4. ordered materialization from \(P_C\) satisfies the one-depth affine law
   and depth gain; and
5. the leading map

   \[
   \overline B_C:P_C/JP_C\longrightarrow L/JL
   \tag{3.1}
   \]

   is onto.

Fix a reachable initial word \(w_0\) with
\(z_0=\Phi(w_0)\in L\).

Then one finite leading solve produces a continuous \(\Xi\)-linear map

\[
 s:F\longrightarrow P_C,
\qquad B_Cs=q,
\tag{3.2}
\]

by the v319 Neumann construction.  Inductively, if
\(z_d=\Phi(w_d)\in J^dL\), strictness permits a coefficient

\[
 v_d\in J^dF,
 \qquad q(v_d)=z_d.
\tag{3.3}
\]

Put \(c_d=\operatorname{Mat}(-s(v_d))\) and
\(w_{d+1}=w_dc_d\).  These ordered materializations give one compatible
relative pro-\(3\) correction whose registered H1, H2 and printed-pentagon
residuals vanish in the limit.  The identity \(B_Cs=q\) implies that
\(B_C\), not necessarily \(s\), is onto.

#### Proof

Leading surjectivity chooses a map \(s_0:F\to P_C\) with
\((B_Cs_0-q)(F)\subseteq JL\).  Since \(P_C\) is a complete free parameter
module, v319 Theorem 1.1 applies verbatim: strictness of \(q\) lifts the
error to \(R:F\to JF\), and

\[
 s=s_0(1+R)^{-1}
\tag{3.4}
\]

satisfies (3.2).  Hypothesis 2.1 supplies legal, filtration-preserving
relative materializations.  Hypotheses 3--4 and the proof of v319 Theorem 3.1 then raise the exact
nonlinear residual by one depth at each step and give a zero residual in the
separated limit. \(\square\)

This conclusion is confined to the registered pro-\(3\) ledger.  Settlement,
mixed-prime, perfect-core, and newly registered side gates require separate
arguments.

The proof never embeds \(P_C\) into the full kernel
\(A_{\rm legal}=\ker G\).  It only uses a map from a free parameter module
to legal corrections and its actual Jacobian.  Therefore the source
base-change comparison

\[
 A_{\rm legal}/JA_{\rm legal}\longrightarrow\ker\overline G
\tag{3.5}
\]

is not a hypothesis of this sufficient positive route.  The v361/v365
source defects remain useful for describing the full legal source, but they
cannot block a positive certificate obtained from (3.1).

### Corollary 3.2 (FINITE LEADING TEST AFTER A4)

Once task382 emits \(c_1,\ldots,c_r\), and the physical v169 occurrence
evaluator, its relator-typing gate, and localization into the actual
\(L/JL\) have all been authenticated, naturality gives

\[
 \overline B_C(\bar e_i)
 =\operatorname{loc}\!\left(\widehat B(c_i-1)\right),
 \qquad
 \operatorname{im}\overline B_C
 =\sum_i(\Xi/J)\,\overline B_C(\bar e_i).
\tag{3.6}
\]

Thus the image, rather than each individual column, is the occurrence/action
closure.  The finite positive decision is:

\[
 \boxed{\operatorname{im}\overline B_C=L/JL.}
\tag{3.7}
\]

No second source-side echelon and no computation of
\(A_{\rm legal}/JA_{\rm legal}\) is required before this test, once
Hypothesis 2.1 is discharged.  A negative dual for (3.7) rejects only the
free-seed sufficient route; it is not a fake certificate and does not exclude
a correction outside the chosen seed module.

## 4. Exact effect on v220

The free-source replacement removes one of the two generic base-change
objects in v361 from the positive all-generator path.  The remaining
load-bearing work is:

1. obtain the positive A4/task382 basis and authenticate its raw first-edge
   occurrence image;
2. discharge Actual Filtered Materialization Hypothesis 2.1;
3. authenticate the actual strict target \(L/JL\), including formation and
   normalized-Brunnian localization;
4. compute the finite equality (3.7) with primal ancestry or a dual;
5. replay the finite seed lifts and the Neumann error matrix through the
   fixed cofinal tower; and
6. treat settlement, mixed-prime and perfect-core edges separately.

Theorem 1.1 is a uniform existence theorem and a deterministic
registered-lane value-tower selector.  The global seeds \(a_i\in K_0\) are
obtained nonconstructively by compactness; only their registered finite-value
towers have the stated deterministic selection.  The theorem chooses those
\(r\) value towers once rather than a fresh correction independently at every
rung.  After Hypothesis 2.1 is discharged, the later correction at every
depth is returned by the single completed operator (3.4).

    TASK382 BASIS -> COMPATIBLE RELATIVE SEED TUPLE: PAPER PROOF / RAW LANE
    FILTERED COMPLETED MATERIALIZATION:              OPEN CONDITION
    FULL A_legal/JA_legal IDENTIFICATION NEEDED:      NO, ON THIS ROUTE
    ACTUAL STRICT L/JL TARGET:                        OPEN
    FREE-SEED LEADING ONTO:                           NOT COMPUTED
    NONLINEAR PRO-3 COMPLETION AFTER ONTO:             PAPER PROOF / CONDITIONAL
    SETTLEMENT / MIXED-PRIME / PERFECT-CORE:          SEPARATE
    COMPATIBLE LIFT / FAKE / IHARA WITNESS:           NOT CONSTRUCTED

R07_FREE_RELATIVE_SEED_NEWTON_SOURCE_V368_PAPER_GRADE

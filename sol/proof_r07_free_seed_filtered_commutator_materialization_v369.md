# R07 free-seed filtered commutator materialization v369

Author: Sol / 2026-08-30

Status: conditional paper reduction after v98, v173, v248, v251, v260,
v319 and v368.  It constructs the needed nonabelian action inside the one
joint-source quotient defining the registered lane, proves a depthwise
materialization theorem there, and proves the corresponding depthwise form
of the Newton recursion.  No continuous global section from the free
instruction module to the nonabelian correction group is needed for that
form.  The physical filtered actual-image comparison, the strict localized
target, and leading surjectivity remain open.  No compatible R07 lift, fake
certificate, or Ihara witness is declared.  `verified=false`.

## 1. Source lifts and the joint nonabelian action

Retain the notation of v368.  Thus

\[
 K_0=\Pi_S\cap\ker q_0,
 \qquad
 P=\ker(\Delta_\infty\to\Delta_0),
 \qquad
 J=\overline{\langle p-1:p\in P\rangle}\triangleleft\Xi.
\tag{1.1}
\]

The simultaneous context maps induce

\[
 \vartheta:\widehat F_2\longrightarrow\Delta_\infty.
\tag{1.2}
\]

### Lemma 1.1 (COMPATIBLE SOURCE LIFTS)

The map (1.2) is onto.  In particular every \(p\in P\), and every chosen
coarse representative in \(\Delta_\infty\), has a profinite source lift.
At a fixed registered finite level it has an ordinary source-word lift.

#### Proof

By definition of \(\Delta_n\), the image of \(F_2\) is onto every finite
coordinate \(\Delta_n\).  Hence the image of \(\widehat F_2\) in the
inverse limit meets every basic open cylinder and is dense.  It is also
compact and therefore closed.  It equals \(\Delta_\infty\).  The finite
assertion follows from the defining image equality for \(\Delta_n\).
\(\square\)

Put \(N=\ker\vartheta\).  The one joint-source quotient

\[
 \overline F_{\rm lane}:=\widehat F_2/N
 \mathrel{\mathop{\longrightarrow}^{\sim}}\Delta_\infty
\tag{1.3}
\]

is the inverse limit of the same registered finite joint images.  Thus all
of those images are quotients of one nonabelian group, rather than unrelated
abelian modules.  Let \(\bar a_i=\vartheta(a_i)\in P\), and define

\[
 \mathscr Q_C=
 \overline{\langle{}^g\bar a_i:
   g\in\Delta_\infty,\ 1\leq i\leq r\rangle}
 \triangleleft\Delta_\infty.
\tag{1.4}
\]

Because \(K_0\) is normal in \(\widehat F_2\), this subgroup lies in
\(\vartheta(K_0)\cap P\).  Conjugation in \(\Delta_\infty\) gives the
required action on \(\mathscr Q_C\).  There is no source-lift ambiguity in
(1.3): two lifts differ by \(N\) and therefore induce the same conjugation
on this quotient.  Its reductions are exactly the simultaneous
nonabelian actions attached to the joint images.  Identifying their
elementary-abelian shadows with the concrete v173/task198 evaluator is the
physical authentication gate isolated in Section 5.
Moreover \(\vartheta(K_0)\) is compact and hence closed, so every element
of \(\mathscr Q_C\) has at least one preimage in \(K_0\).  This supplies a
relative source correction after a lane value has been constructed; it does
not furnish a continuous choice of such preimages.  It is only a
\(K_0\)-preimage of the registered-lane value: no actual-depth or residual
property of an arbitrary preimage is asserted.

On the registered pro-\(3\) lane, \(P\) is an open pro-\(3\) subgroup of
the finitely generated group \(\Delta_\infty\), and hence is topologically
finitely generated.  Define its lower exponent-\(3\) central series and the
relative seed filtration by

\[
 P_1=P,
 \qquad
 P_{d+1}=\overline{P_d^{\,3}[P_d,P]},
\tag{1.5}
\]

\[
 \mathscr D_C^d=\mathscr Q_C\cap P_{d+1}
 \qquad(d\geq0).
\tag{1.6}
\]

### Lemma 1.2 (REGISTERED-LANE COFINALITY)

The groups \(\mathscr D_C^d\) are closed, stable under the retained
\(\Delta_\infty\)-context action, and cofinal at one in the topology
induced from \(P\).  Consequently any sequence
\(u_d\in\mathscr D_C^d\) tends to one and the ordered product
\(\prod_d u_d\) is Cauchy on that lane.

#### Proof

The lower exponent-\(3\) central series of the finitely generated pro-\(3\)
group \(P\) is a neighbourhood basis at one.  The series is characteristic
in \(P\), while \(P\triangleleft\Delta_\infty\), and \(\mathscr Q_C\) is
normal by (1.4).  Hence every retained context preserves the intersections
(1.6).  Cofinality, convergence, and the Cauchy assertion follow. \(\square\)

This is cofinality only in the registered relative pro-\(3\) topology.  It
is not a claim that this lane is cofinal in the full profinite topology of
\(\widehat F_2\).

## 2. The difference operator is an actual commutator word

Use the left context action supplied by (1.3)--(1.4).  For
\(p\in P\) and \(u\in\mathscr Q_C\), put

\[
 \partial_p(u)={}^{p}u\,u^{-1}
 =pup^{-1}u^{-1}
 =[p,u].
\tag{2.1}
\]

This is an actual element of the joint quotient.  Choosing source lifts of
\(p\) and \(u\) spells it by the corresponding commutator in
\(\widehat F_2\); different choices have the same image modulo \(N\).

### Lemma 2.1 (AUGMENTATION--COMMUTATOR IDENTITY)

In every retained elementary-abelian correction quotient \(A\),

\[
 [\partial_p(u)]=(p-1)[u].
\tag{2.2}
\]

Moreover, if \(u\in\mathscr D_C^d\), then

\[
 \partial_p(u)\in\mathscr D_C^{d+1}.
\tag{2.3}
\]

#### Proof

In additive notation for \(A\), the class of (2.1) is
\(p[u]-[u]\), proving (2.2).  If
\(u\in\mathscr D_C^d=\mathscr Q_C\cap P_{d+1}\), then
\([p,u]\in[P,P_{d+1}]\leq P_{d+2}\).  Normality of
\(\mathscr Q_C\) keeps this commutator in \(\mathscr Q_C\), proving
(2.3). \(\square\)

For \(g\in\Delta_\infty\), \(p_1,\ldots,p_d\in P\), and one seed
\(a_i\), choose the authenticated source actions and put

\[
 u_0={}^{g}\bar a_i,
 \qquad
 u_j=\partial_{p_j}(u_{j-1})
 \quad(1\leq j\leq d).
\tag{2.4}
\]

Iteration gives

\[
 u_d\in\mathscr D_C^d,
 \qquad
 [u_d]=(p_d-1)\cdots(p_1-1)g[a_i].
\tag{2.5}
\]

The normal form in (2.5) loses no element of \(J^d\).  The identity

\[
 g(p-1)=(gpg^{-1}-1)g
\tag{2.6}
\]

and normality of \(P\) move every group element to the right of the
\((p_j-1)\) factors.  Thus, in each finite group algebra, \(J^d\) is
spanned by monomials of the form in (2.5).  Coefficients
\(0,1,2\in\mathbf F_3\) are materialized by exponents \(0,1,-1\).

## 3. Depthwise materialization of the completed free seed span

For each \(n\), let \(A_{C,\leq n}\) be the cumulative actual image of
\(\mathscr Q_C\) in the first \(n\) retained correction quotients, rather
than an unrestricted product of their ambient modules.  Put

\[
 A_C=\varprojlim_n A_{C,\leq n}.
\tag{3.1}
\]

Each \(A_{C,\leq n}\) is the finite elementary-abelian simultaneous image,
and its transition maps are the continuous equivariant reductions induced
by the same joint quotient.

The authenticated context action and the seed values define the continuous
\(\Xi\)-linear map

\[
 \tau:P_C=\Xi^r\longrightarrow A_C.
\tag{3.2}
\]

### Theorem 3.1 (DEPTHWISE FREE-SEED MATERIALIZATION)

In the joint quotient (1.3)--(1.4), for every \(d\geq0\) and every
\(v\in J^dP_C\), the compatible actual value \(\tau(v)\) has a
registered-lane realization

\[
 \operatorname{Mat}_d(v)\in\mathscr D_C^d.
\tag{3.3}
\]

The assertion is existential for each requested value.  It does not say
that the choices \(\operatorname{Mat}_d\) assemble to a continuous group
homomorphism, an additive section, an injective map, or even one global map
\(P_C\to\mathscr Q_C\).

#### Proof

First suppose \(v\) has finite group-algebra support.  Expand it as a
finite sum of the monomials described after (2.6).  Materialize each
monomial by (2.4), use the fixed registered factor order, and use exponent
\(-1\) for coefficient \(2\).  The product lies in
\(\mathscr D_C^d\) and represents \(\tau(v)\) in every retained abelian
quotient in which the coefficient is read.

For completed \(v\in J^dP_C\), choose \(v^{(n)}\) in the finite span of the
normalized \(d\)-fold monomials of (2.5), with the same image in the
cumulative coefficient quotient acting on \(A_{C,\leq n}\).  The first
paragraph makes the compact fibre

\[
 X_n=\{u\in\mathscr D_C^d:
       [u]_{\leq n}=\tau(v)_{\leq n}\}
\tag{3.4}
\]

nonempty.  It is closed, and the use of cumulative actual images gives
\(X_{n+1}\subseteq X_n\).  Compactness yields
\(\bigcap_nX_n\ne\varnothing\).  Any point of that intersection is a
choice in (3.3). \(\square\)

## 4. The depthwise Newton variant

V368 Hypothesis 2.1 asks for a continuous global materialization map.
Theorem 3.1 does not supply that map, so v368 Theorem 3.1 cannot be invoked
literally.  The Newton proof itself admits the following weaker, sufficient
form.

### Theorem 4.1 (DEPTHWISE-MATERIALIZATION NEWTON RECURSION)

Assume:

1. the complete filtered source and target hypotheses of v368 Theorem 3.1,
   including a strict finite free cover \(q:F\twoheadrightarrow L\), hold;
2. the actual leading map \(B_C:P_C\to L\) has a continuous filtered
   \(\Xi\)-linear based right lift \(s:F\to P_C\), with
   \(B_Cs=q\) and \(s(J^dF)\subseteq J^dP_C\);
3. for each \(d\) and each requested \(t\in J^dP_C\), one may choose a
   correction \(c_d(t)\in\mathscr D_C^d\) representing \(\tau(t)\); and
4. the reachable registered-lane residual descends to a continuous map

   \[
    \Phi_{\rm lane}:w_0\mathscr Q_C\longrightarrow L
   \tag{4.1}
   \]

   whose pullback along \(\vartheta\) agrees with the actual localized R07
   residual, and every requested correction satisfies localized stability,
   nonlinear depth gain and the one-depth affine law

   \[
    \Phi_{\rm lane}(wc_d(t))-\Phi_{\rm lane}(w)-B_C(t)
       \in J^{d+1}L
    \quad\text{whenever }\Phi_{\rm lane}(w)\in J^dL.
   \tag{4.2}
   \]

Then, from any reachable \(w_0\) with \(\Phi_{\rm lane}(w_0)\in L\), successive
depthwise choices construct a Cauchy correction product whose limit has
zero residual on the registered pro-\(3\) lane.  The resulting lane value
lies in \(\mathscr Q_C\subseteq\vartheta(K_0)\), so it has a relative
source preimage, although this theorem neither selects that preimage
continuously nor gives an arbitrary preimage an actual-depth or residual
property.

#### Proof

Suppose \(z_d=\Phi_{\rm lane}(w_d)\in J^dL\).  Strictness gives
\(v_d\in J^dF\) with \(q(v_d)=z_d\).  Put

\[
 t_d=-s(v_d)\in J^dP_C,
 \qquad
 c_d=c_d(t_d),
 \qquad
 w_{d+1}=w_dc_d.
\tag{4.3}
\]

Since \(B_Cs=q\), equation (4.2) gives
\(\Phi_{\rm lane}(w_{d+1})\in J^{d+1}L\).  Induction constructs all
\(c_d\).  Lemma 1.2 gives \(w_d\to w_\infty\) in
\(w_0\mathscr Q_C\), and continuity gives

\[
 \Phi_{\rm lane}(w_\infty)
 =\lim_d\Phi_{\rm lane}(w_d)=0.
\tag{4.4}
\]

Here separatedness of \(L\) is used in the last equality.  No relation
between unused choices of \(c_d(t)\), and no global nonlinear section, is
used. \(\square\)

Theorem 3.1 supplies item 3 of Theorem 4.1 in the joint lane.  It does
not supply item 4, the strict target, or the based right lift.

For ordinary finite spellings, cofinality must be calibrated rather than
identified with the window index.  For every retained window \(n\), choose
a nondecreasing depth \(d(n)\) such that

\[
 \mathscr D_C^{d(n)}
 \text{ is invisible in the first }n\text{ retained quotients}.
\tag{4.5}
\]

Apply v98's accumulated-kernel rule to the finite prefix
\(c_0\cdots c_{d(n)-1}\); the tail is invisible in that window by (4.5).
This gives an exponent-zero spelling independently at every requested
finite window.  No canonical or compatible choice across windows is
asserted, and no assertion \(\mathscr D_C^n\subseteq U_n\) is made.

## 5. Exact R07 comparison gate

To apply Theorems 3.1 and 4.1 to R07, the physical post-task382 package must
authenticate the commuting square

\[
\begin{CD}
 P_C @>{\tau}>> A_C\\
 @V{B_C}VV       @VV{B_{\rm actual}}V\\
 L @= L
\end{CD}
\tag{5.1}
\]

with the following meanings fixed:

1. every physical v169 context and seed map factors through the same
   joint quotient and conjugation action (1.3)--(1.4);
2. the occurrence columns are produced by the physical v169 eleven-slot
   evaluator from the same task382 seed values;
3. \(A_C\) is the cumulative one-common-word image, not the direct product
   of separately generated occurrence blocks;
4. the localized target uses the same \(J\)-filtration, the actual
   localized residual descends continuously to the lane torsor as in
   (4.1), and every requested element of \(\mathscr D_C^d\) obeys the
   depth-\(d\) correction law (4.2); and
5. formation, commutator, coarse mark, and matched pro-\(3\) onto are exactly
   the v367 ledger.  Settlement and all non-\(3\) gates remain outside the
   square.

Items 1--4 are a filtered actual-image comparison, not a request for the
full quotient \(A_{\rm legal}/JA_{\rm legal}\).  Once they, strictness of
\(L\), leading onto, localized stability, and nonlinear depth gain are
authenticated, Theorem 4.1 supplies the registered pro-\(3\) recursion.

```text
NONABELIAN JOINT-SOURCE ACTION:                    PAPER CONSTRUCTION IN JOINT LANE
J^d SEED COEFFICIENT -> DEPTH-d COMMUTATOR WORD:  CONDITIONAL PAPER PROOF
COMPLETED VALUE -> ACTUAL DEPTH-d LANE VALUE:      CONDITIONAL PAPER PROOF
CONTINUOUS GLOBAL NONABELIAN SECTION REQUIRED:     NO FOR THEOREM 4.1
CALIBRATED v98 FINITE-WINDOW SPELLINGS:            PAPER PROOF / CONDITIONAL
PHYSICAL v169 / CUMULATIVE-ACTUAL SQUARE (5.1):    OPEN AUTHENTICATION
CONTINUOUS ACTUAL-RESIDUAL DESCENT TO LANE:         OPEN AUTHENTICATION
STRICT L/JL AND LEADING ONTO:                      OPEN
NONLINEAR STABILITY / DEPTH GAIN:                  OPEN / CONDITIONAL
SETTLEMENT / MIXED-PRIME / PERFECT-CORE:           SEPARATE
COMPATIBLE LIFT / FAKE / IHARA WITNESS:            NOT CONSTRUCTED
```

`R07_FREE_SEED_FILTERED_COMMUTATOR_MATERIALIZATION_V369_CONDITIONAL_PAPER_GRADE`

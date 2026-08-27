# R07 formation--charming factorization v158

Author: Sol / 2026-08-27

Status: paper theorem.  V155 gives a closed formation selector at every
mixed-prime Frattini edge, while v157 gives a closed exact-charming selector.
This note proves that the latter factors through the former.  Consequently
exact charmingness is not a third independent target-membership problem on
the formation-purified branch.  The actual coupled relation/formation target
membership remains open, as does the perfect-core part of a fully cofinal
ladder.  No compatible full lift, fake, or Ihara witness is declared.

## 1. Setup

Let

\[
 F=F(x,y),\qquad q:F\twoheadrightarrow G,\qquad
 \Omega=\ker q,
\tag{1.1}
\]

and put

\[
 R=R_S(G),\qquad P=q^{-1}(R),\qquad S=PSL(2,8).
\tag{1.2}
\]

Use the fixed mixed-prime schedule

\[
 \ell_0,\ell_1,\ldots,
 \qquad
 m_0=1,\qquad m_n=\prod_{i=0}^{n-1}\ell_i,
\tag{1.3}
\]

and the aligned towers

\[
 \begin{aligned}
 \Omega_0&=\Omega,&
 \Omega_{n+1}&=\Phi_{\ell_n}(\Omega_n),\\
 P_0&=P,&
 P_{n+1}&=\Phi_{\ell_n}(P_n),
 \end{aligned}
 \qquad \Phi_p(K)=K^p[K,K].
\tag{1.4}
\]

Write

\[
 \epsilon:F\longrightarrow F^{\rm ab}=\mathbf Z^2
\tag{1.5}
\]

for the signed exponent vector.  V156 proves

\[
 \epsilon(\Omega)=18\mathbf Z^2.
\tag{1.6}
\]

At edge \(n+1\to n\), set

\[
 V_n=\Omega_n/\Omega_{n+1},\qquad
 W_n=P_n/P_{n+1}.
\tag{1.7}
\]

V155 supplies the onto inclusion-induced formation map

\[
 \rho_n:V_n\twoheadrightarrow W_n,
 \qquad [w]\longmapsto[w].
\tag{1.8}
\]

## 2. The two initial exponent lattices coincide

### Lemma 2.1 (PERFECT-RESIDUAL EXPONENT EQUALITY)

One has

\[
 \boxed{\epsilon(P)=\epsilon(\Omega)=18\mathbf Z^2.}
\tag{2.1}
\]

#### Proof

The formation residual \(R\) is perfect by v153 Lemma 2.1.  Hence

\[
 R=[R,R]\leq[G,G].
\tag{2.2}
\]

If \(p\in P\), then \(q(p)\in R\), so the image of \(q(p)\) in
\(G^{\rm ab}\) is zero.  The kernel of the induced map

\[
 F^{\rm ab}=\mathbf Z^2\longrightarrow G^{\rm ab}
\tag{2.3}
\]

is exactly \(\epsilon(\Omega)\).  Therefore

\[
 \epsilon(P)\leq\epsilon(\Omega).
\tag{2.4}
\]

The reverse inclusion follows from \(\Omega\leq P\).  Equation (1.6) now
gives (2.1). \(\square\)

This argument uses only perfectness of the residual.  It does not require
the direct-product splitting of v154.

## 3. Equality persists at every rung

V157 Lemma 1.1 proves, for every subgroup \(K\leq F\) and prime \(p\),

\[
 \epsilon(\Phi_p(K))=p\,\epsilon(K).
\tag{3.1}
\]

Iterating (3.1) simultaneously on the two towers in (1.4) gives:

### Theorem 3.1 (ALIGNED ALL-RUNG EXPONENT LATTICE)

For every \(n\geq0\),

\[
 \boxed{
 \epsilon(\Omega_n)=\epsilon(P_n)
 =18m_n\mathbf Z^2.}
\tag{3.2}
\]

Moreover,

\[
 \epsilon(\Omega_{n+1})=\epsilon(P_{n+1})
 =18m_n\ell_n\mathbf Z^2.
\tag{3.3}
\]

Thus both the correction subgroup and the formation preimage have the same
two-dimensional exponent quotient at every aligned edge.

## 4. Exact factorization through the formation selector

Define normalized exponent maps

\[
 \begin{aligned}
 \bar\epsilon_n^\Omega:V_n&\longrightarrow
        \mathbf F_{\ell_n}^2,&
 [w]&\longmapsto
 \frac{\epsilon(w)}{18m_n}\bmod\ell_n,\\
 \bar\epsilon_n^P:W_n&\longrightarrow
        \mathbf F_{\ell_n}^2,&
 [p]&\longmapsto
 \frac{\epsilon(p)}{18m_n}\bmod\ell_n.
 \end{aligned}
\tag{4.1}
\]

Theorem 3.1 makes both maps well defined.  It also makes both maps onto.

### Theorem 4.1 (FORMATION--CHARMING FACTORIZATION)

For every rung,

\[
 \boxed{
 \bar\epsilon_n^\Omega
 =\bar\epsilon_n^P\circ\rho_n.}
\tag{4.2}
\]

Consequently the image of the combined map is the graph

\[
 \boxed{
 \operatorname{im}(\rho_n,\bar\epsilon_n^\Omega)
 =\{(\eta,\bar\epsilon_n^P(\eta)):\eta\in W_n\}.}
\tag{4.3}
\]

#### Proof

For \(w\in\Omega_n\), the class \(\rho_n([w])\) is represented by the
same literal word \(w\) in \(P_n/P_{n+1}\).  Applying the two definitions
in (4.1) proves (4.2).  Surjectivity of \(\rho_n\), proved in v155 Theorem
3.1, then gives (4.3). \(\square\)

The last coordinate in v157's displayed map
\((B_n,\rho_n,\bar\epsilon_n^\Omega)\) is therefore not independent of
the formation coordinate.  It remains useful on the direct task179 route,
where no formation coordinate is imposed, but it must not be counted as a
third obstruction on the formation-purified route.

## 5. Exact commutator representatives in a formation fibre

The analogue of v157 Theorem 3.1 for \(P_n\) is

\[
 \boxed{
 \ker\bar\epsilon_n^P
 =\operatorname{im}\bigl(
 P_n\cap[F,F]\longrightarrow W_n\bigr).}
\tag{5.1}
\]

Indeed, if \(p\in P_n\) has zero normalized residue, then

\[
 \epsilon(p)=\ell_n a
 \quad\text{for some }a\in\epsilon(P_n).
\tag{5.2}
\]

Choose \(h\in P_n\) with \(\epsilon(h)=a\).  The word

\[
 p^{\rm com}=ph^{-\ell_n}
\tag{5.3}
\]

has exact exponent zero and represents the same class in \(W_n\), because
\(h^{\ell_n}\in P_{n+1}\).  The reverse inclusion in (5.1) is immediate.

For corrections one has a stronger, completely explicit repair inside the
smaller subgroup \(\Omega_{n+1}\).  Let the v157 basis words be

\[
 \epsilon(u_n)=(18m_n,0),\qquad
 \epsilon(v_n)=(0,18m_n),
\tag{5.4}
\]

with

\[
 u_{n+1}=u_n^{\ell_n},\qquad
 v_{n+1}=v_n^{\ell_n}.
\tag{5.5}
\]

If \(c\in\Omega_n\) satisfies

\[
 \epsilon(c)=18m_n\ell_n(A,B),
\tag{5.6}
\]

then

\[
 \boxed{
 c^{\rm com}=c\,u_n^{-\ell_n A}v_n^{-\ell_n B}}
\tag{5.7}
\]

has exact exponent zero.  The added factor belongs to \(\Omega_{n+1}\),
so it changes neither the edge class in \(V_n\), the formation coordinate,
nor any earlier quotient.

### Corollary 5.1 (FORMATION-FIBRE CHARMING DICHOTOMY)

Fix \(\eta\in W_n\).  Then exactly one of the following holds.

1. If \(\bar\epsilon_n^P(\eta)\ne0\), no class in
   \(\rho_n^{-1}(\eta)\) has an exact-commutator representative.
2. If \(\bar\epsilon_n^P(\eta)=0\), every class in
   \(\rho_n^{-1}(\eta)\) has an exact-commutator representative, obtained
   by (5.7), without changing that class.

#### Proof

Theorem 4.1 makes \(\bar\epsilon_n^\Omega\) constant on the whole fibre,
with value \(\bar\epsilon_n^P(\eta)\).  V157 Theorem 3.1 and formula (5.7)
give the two alternatives. \(\square\)

## 6. Reduction of the coupled R07 equation

Let

\[
 B_n:A_n\longrightarrow Z_n
\tag{6.1}
\]

be the actual common-word change map for the two hexagons and printed-order
pentagon, restricted to the same admissible edge domain, and let
\(\eta_n\in W_n\) be a typed formation-reference displacement.  The three
displayed conditions would be

\[
 B_n(c_n)=-\beta_n,\qquad
 \rho_n(c_n)=\eta_n,\qquad
 \bar\epsilon_n^\Omega(c_n)=0.
\tag{6.2}
\]

Theorem 4.1 gives the exact simplification:

### Theorem 6.1 (NO THIRD MEMBERSHIP GATE)

If

\[
 \boxed{\bar\epsilon_n^P(\eta_n)=0,}
\tag{6.3}
\]

then (6.2) has a solution if and only if the two-coordinate system

\[
 \boxed{
 B_n(c_n)=-\beta_n,\qquad
 \rho_n(c_n)=\eta_n}
\tag{6.4}
\]

has a solution.  Every solution of (6.4) is exactified by (5.7) without
changing either equality.  If (6.3) fails, (6.2) has no solution.

#### Proof

For every solution of (6.4), Theorem 4.1 gives

\[
 \bar\epsilon_n^\Omega(c_n)
 =\bar\epsilon_n^P(\eta_n).
\tag{6.5}
\]

Under (6.3) formula (5.7) gives an exact-commutator representative of the
same edge class.  Since \(B_n\) and \(\rho_n\) are edge maps, the repair in
\(\Omega_{n+1}\) changes neither value.  Conversely, an exact commutator
has zero normalized exponent, so (6.5) proves necessity. \(\square\)

If \(\eta_n\) is genuinely obtained from the displacement between two
exact-charming representatives, it is represented by a word in
\(P_n\cap[F,F]\), and (5.1) proves (6.3) automatically.  Thus a correctly
typed charming arithmetic reference cannot introduce a hidden exponent
incompatibility.

## 7. Consequence for the two current routes

There are now two distinct finite successor contracts.

1. **Direct task179 route.**  No arithmetic formation coordinate is fixed.
   The normalized rows of v156/v157 remain necessary.  Task186 implements
   \((B_0,\bar\epsilon_0^\Omega)\) and the explicit exactification (5.7).
2. **Formation-purified route.**  Once the actual \(\eta_n\) is supplied,
   first check the two scalar residues (6.3).  For a charming reference they
   vanish, and only the joint target membership (6.4) remains.  Do not append
   two redundant exponent rows to that already formation-typed solve.

This removes exact charmingness as an independent all-stage obstruction.
It does not prove that \((-\beta_n,\eta_n)\) belongs to
\(\operatorname{im}(B_n,\rho_n)\), and it does not supply the currently
missing explicit arithmetic displacement \(\eta_n\).

```text
epsilon(P_n) = epsilon(Omega_n) = 18 m_n Z^2:       PAPER_PROOF
CHARMING SELECTOR FACTORS THROUGH FORMATION:         PAPER_PROOF
FORMATION/CHARMING COMBINED IMAGE IS A GRAPH:        PAPER_PROOF
ZERO FORMATION RESIDUE => CLOSED EXACTIFICATION:     PAPER_PROOF
EXACT CHARMING AS THIRD FORMATION-PURIFIED GATE:      REMOVED
ACTUAL JOINT (B_n,rho_n) TARGET MEMBERSHIP:          OPEN
EXPLICIT ARITHMETIC eta_n:                           UNKNOWN_INPUT
PERFECT-CORE / NONABELIAN SIMPLE STRIP GATES:        OPEN
COMPATIBLE FULL R07 LIFT / FAKE / IHARA WITNESS:     NOT DECLARED
```

`R07_FORMATION_CHARMING_FACTORIZATION_V158_PAPER_GRADE`

# R07 path-bearing joint residual descent v372

Author: Sol / 2026-08-30

Status: corrected paper theorem after the failed group-only descent attempt
v371.  A finite PB quotient value does not determine its Fox path modulo the
old PB boundaries: the missing fibre is generally the active nonzero
Frattini layer.  This note therefore enlarges every context value to its
finite Magnus state (Fox-path class together with the endpoint).  The exact
eleven-occurrence residual factors through the resulting enriched joint
image, matched refinement gives one continuous inverse-limit residual, and
formation/Brunnian localization is expressed as the inverse image of an
endpoint ideal.  The enriched physical ABI, strictness, leading onto and the
intrinsic nonlinear depth law remain open.  No compatible lift, fake
certificate or Ihara witness is declared.  \(\mathtt{verified=false}\).

## 1. Why the endpoint-only state is insufficient

Fix one PB3 or PB4 block \(B\), its retained finite quotient

\[
 E_{B,n}=P_B/K_{B,n},
\tag{1.1}
\]

and \(k=\mathbf F_3\).  Evaluation of the fixed PB presentation gives

\[
 C_{2,B,n}\xrightarrow{D_{2,B,n}}C_{1,B,n}
 \xrightarrow{D_{1,B,n}}k[E_{B,n}].
\tag{1.2}
\]

Put

\[
 \mathcal R_{B,n}:=
 C_{1,B,n}/\operatorname{im}D_{2,B,n},
 \qquad
 \overline D_{1,B,n}:\mathcal R_{B,n}\longrightarrow k[E_{B,n}].
\tag{1.3}
\]

The quotient in (1.3) retains the active kernel homology:

\[
 \ker\overline D_{1,B,n}
 \cong H_1(K_{B,n};k)
 \cong K_{B,n}/\Phi_3(K_{B,n})
\tag{1.4}
\]

in the relative Frattini situation.  Hence no map
\(E_{B,n}\to\mathcal R_{B,n}\) may send an endpoint to the class of an
arbitrary path to that endpoint.  Two such paths can differ by a nonzero
class in (1.4), even when the common endpoint is the identity.  This is
precisely why a group-only joint tuple cannot carry the v169 residual.

## 2. The finite Magnus state keeps the missing path fibre

For a word \(w\) in the fixed PB presentation, let
\(\partial_{B,n}w\in C_{1,B,n}\) be its evaluated Fox path and let
\(\bar w\in E_{B,n}\) be its endpoint.  The Fox product rule is

\[
 \partial(uv)=\partial u+\bar u\,\partial v.
\tag{2.1}
\]

Consequently

\[
 \mathfrak m_{B,n}(w)=
 \bigl([\partial_{B,n}w],\bar w\bigr)
 \in\mathcal R_{B,n}\rtimes E_{B,n}
\tag{2.2}
\]

is multiplicative.  A defining PB relator has endpoint one and Fox path a
column of \(D_{2,B,n}\), so (2.2) descends from presentation words to
\(P_B\).  Denote its finite image by

\[
 \mathcal M_{B,n}:=\operatorname{im}\mathfrak m_{B,n}.
\tag{2.3}
\]

The second coordinate of (2.2) is the ordinary group value; the first
coordinate remembers the path fibre (1.4).  In particular, the identity of
\(\mathcal M_{B,n}\), not merely endpoint one, is equivalent to endpoint one
and zero retained Fox class.

Marked quotient maps send retained paths to their reductions and complete PB
boundaries to complete PB boundaries.  Thus they induce compatible
homomorphisms

\[
 \mathcal M_{B,n+1}\longrightarrow\mathcal M_{B,n}.
\tag{2.4}
\]

This naturality is conditional only on the same presentation-map
authentication required in v169 Theorem 3.1.

## 3. The exact residual factors through ten enriched contexts

Work on the registered exponent-zero R07 lane.  For each of the ten task198
contexts, use the fixed substitution followed by (2.2):

\[
 \widehat\rho_{j,n}:F_2\longrightarrow\mathcal M_{j,n},
 \qquad 0\leq j<10.
\tag{3.1}
\]

Retain the frozen ten-to-eleven map and signs

\[
 t=(0,1,2,3,0,4,5,6,7,8,9),
 \qquad
 \sigma=(+,-,+,-,-,+,+,+,+,-,-).
\tag{3.2}
\]

Define the enriched joint image

\[
 \widehat\Delta_n=
 \operatorname{im}\left(
 F_2\xrightarrow{(\widehat\rho_{0,n},\ldots,\widehat\rho_{9,n})}
 \prod_{j=0}^9\mathcal M_{j,n}\right).
\tag{3.3}
\]

For occurrence \(o\), let

\[
 \widehat\jmath_{o,n}:\mathcal M_{t(o),n}
 \longrightarrow\mathcal M_{B(o),n},
 \qquad B(o)\in\{H1,H2,P\},
\tag{3.4}
\]

be the path-bearing map induced by its registered PB3/PB4 embedding.  The
same joint coordinate zero is used twice, but the two occurrence maps in
(3.4) retain their distinct block types.

Multiply in the frozen printed order:

\[
 \widehat\Psi_n(d)=
 \left(
  \prod_{o=1}^{3}\widehat\jmath_{o,n}
          (d_{t(o)})^{\sigma_o},
  \prod_{o=4}^{6}\widehat\jmath_{o,n}
          (d_{t(o)})^{\sigma_o},
  \prod_{o=7}^{11}\widehat\jmath_{o,n}
          (d_{t(o)})^{\sigma_o}
 \right).
\tag{3.5}
\]

Let

\[
 \operatorname{path}_{B,n}:
 \mathcal M_{B,n}\longrightarrow\mathcal R_{B,n}
\tag{3.6}
\]

denote first-coordinate projection and put

\[
 \psi_n=
 (\operatorname{path}_{H1,n},
  \operatorname{path}_{H2,n},
  \operatorname{path}_{P,n})
 \circ\widehat\Psi_n:
 \widehat\Delta_n\longrightarrow
 \mathcal R_{H1,n}\times\mathcal R_{H2,n}\times\mathcal R_{P,n}
 =:\mathcal R_n.
\tag{3.7}
\]

The projection in (3.6) is not a homomorphism; it is the crossed path
coordinate of the exact product (3.5).

### Theorem 3.1 (PATH-BEARING FINITE FACTORIZATION)

For every source word \(F\in F_2\),

\[
 \boxed{
 \psi_n\bigl((\widehat\rho_{j,n}(F))_{j=0}^9\bigr)
 =\Phi_n(F),}
\tag{3.8}
\]

where \(\Phi_n(F)\) is the exact v169 two-hexagon/printed-pentagon Fox
residual.  Hence two words with the same enriched joint tuple have the same
exact residual.

#### Proof

The three group-word components of (3.5) are literally

\[
 \begin{aligned}
 H1(F)&=F(x,y)F(x,z)^{-1}F(y,z),\\
 H2(F)&=F(u,x)^{-1}F(x,y)^{-1}F(u,y),
 \end{aligned}
\tag{3.9}
\]

and the registered five-factor pentagon in signs \((+,+,+,-,-)\).
The semidirect product law (2.1), including the inverse rule, produces
exactly their transported Fox paths.  The map (3.2) accounts for the repeated
coordinate and all four inverse occurrences.  Projecting the three path
coordinates therefore gives the three literal residual classes, which is
(3.8). \(\square\)

The corresponding statement with the ordinary group joint image in place of
\(\widehat\Delta_n\) is false in general by (1.4).

## 4. Matched refinement and the enriched lane

Every element of \(\widehat\Delta_n\) is represented by one source word.
The same word at level \(n+1\) reduces to it, so (2.4) gives surjections

\[
 \widehat\Delta_{n+1}\twoheadrightarrow\widehat\Delta_n,
 \qquad
 \widehat\Delta_\infty=\varprojlim_n\widehat\Delta_n.
\tag{4.1}
\]

Likewise put

\[
 \mathcal R_\infty=\varprojlim_n\mathcal R_n.
\tag{4.2}
\]

### Theorem 4.1 (CONTINUOUS ENRICHED RESIDUAL DESCENT)

The maps \(\psi_n\) commute with matched reduction and induce a continuous
map

\[
 \boxed{
 \psi_\infty:\widehat\Delta_\infty\longrightarrow\mathcal R_\infty.}
\tag{4.3}
\]

The simultaneous source map

\[
 \widehat\vartheta:\widehat F_2\longrightarrow\widehat\Delta_\infty
\tag{4.4}
\]

is onto, and its pullback of (4.3) is the exact completed R07 residual.

#### Proof

Equations (2.4), (3.4), the semidirect product law and path projection all
commute with matched reduction, proving compatibility.  Each finite target
is discrete, so the induced inverse-limit map is continuous.  Equation (3.8)
at every level proves the pullback claim.

The image of (4.4) meets every finite cylinder because (3.3) is an image
definition.  It is dense and also compact, hence closed, so it is all of
\(\widehat\Delta_\infty\). \(\square\)

Let

\[
 K_0=\Pi_S\cap\ker q_0
\tag{4.5}
\]

and let \(a_1,\ldots,a_r\in K_0\) be the compatible relative seeds of v368.
Define

\[
 \widehat{\mathscr Q}_C=
 \overline{\left\langle
 {}^g\widehat\vartheta(a_i):
 g\in\widehat\Delta_\infty,\ 1\leq i\leq r
 \right\rangle}
 \triangleleft\widehat\Delta_\infty.
\tag{4.6}
\]

Normality of \(K_0\) gives

\[
 \widehat{\mathscr Q}_C
 \subseteq\widehat\vartheta(K_0).
\tag{4.7}
\]

Thus every enriched lane value has a relative source preimage, without a
continuous section.  Endpoint projection gives

\[
 \pi_{\rm end}:\widehat\Delta_\infty\twoheadrightarrow\Delta_\infty,
 \qquad
 \widehat P=\pi_{\rm end}^{-1}(P),
 \qquad P=\ker(\Delta_\infty\to\Delta_0).
\tag{4.8}
\]

If the registered group lane is pro-\(3\) over its coarse value, then
\(\ker\pi_{\rm end}\) is pro-\(3\), because the extra kernels in (2.4) are
additive \(\mathbf F_3\)-groups.  Hence \(\widehat P\) is an open pro-\(3\)
subgroup of the finitely generated profinite quotient
\(\widehat\Delta_\infty\), and is itself finitely generated.  Put

\[
 \widehat\Xi=\mathbf F_3[[\widehat\Delta_\infty]],
 \qquad
 \widehat J=
 \overline{\langle p-1:p\in\widehat P\rangle},
\tag{4.9}
\]

and, for the lower exponent-\(3\) central series \(\widehat P_d\), put

\[
 \widehat{\mathscr D}_C^d=
 \widehat{\mathscr Q}_C\cap\widehat P_{d+1}.
\tag{4.10}
\]

The lower-central-series and commutator materialization arguments of v369
Sections 1--3 now apply verbatim with the data (4.6), (4.8)--(4.10).  No
finite-generation assertion about \(\widehat{\mathscr Q}_C\) is required.
Authentication that the resulting leading action is the task198/task382
evaluator remains a physical ABI gate.

## 5. Localization uses endpoint ideals, not a path choice

For a normal subgroup \(N\triangleleft E_{B,n}\), let

\[
 I_{B,n}(N)=
 \ker\bigl(k[E_{B,n}]\longrightarrow k[E_{B,n}/N]\bigr)
\tag{5.1}
\]

be its relative augmentation ideal and define the path-bearing supported
module

\[
 \mathcal L_{B,n}(N)=
 \overline D_{1,B,n}^{-1}\bigl(I_{B,n}(N)\bigr)
 \leq\mathcal R_{B,n}.
\tag{5.2}
\]

This is a genuine \(k[E_{B,n}]\)-submodule.  It includes the whole active
loop fibre (1.4), as it must, and requires no choice of a path for a group
element.  If a retained path has endpoint \(g\), then

\[
 \overline D_{1,B,n}([{\rm path}])=g-1.
\tag{5.3}
\]

Consequently an endpoint in \(N\) places every path to that endpoint in
\(\mathcal L_{B,n}(N)\).

In the notation below, the endpoint group \(G_{B,n}\) is
\(E_{B,n}\) from (1.1).  Put

\[
 \begin{aligned}
 N_{H1,n}&=R_S(G_{H1,n}),\\
 N_{H2,n}&=R_S(G_{H2,n}),\\
 N_{P,n}&=B_{P,n}\cap R_S(G_{P,n}),
 \end{aligned}
\tag{5.4}
\]

and

\[
 L_n=
 \mathcal L_{H1,n}(N_{H1,n})\times
 \mathcal L_{H2,n}(N_{H2,n})\times
 \mathcal L_{P,n}(N_{P,n}).
\tag{5.5}
\]

Formation residuals are characteristic and Brunnian deletion kernels are
normal.  They commute with the matched quotient maps, so (5.5) forms a
compatible system.  Let

\[
 L_{\rm loc}=\varprojlim_n L_n\leq\mathcal R_\infty.
\tag{5.6}
\]

### Proposition 5.1 (ACTUAL ENRICHED LANE IS DOUBLY LOCALIZED)

Let \(F_*=F_{\rm arith}u_*\), where \(u_*\in\Pi_S\), and assume
\(F_*\in[\widehat F_2,\widehat F_2]\).  Put
\(\widehat w_0=\widehat\vartheta(F_*)\).  Then

\[
 \boxed{
 \psi_\infty
 \bigl(\widehat w_0\widehat{\mathscr Q}_C\bigr)
 \subseteq L_{\rm loc}.}
\tag{5.7}
\]

#### Proof

Take \(\widehat q\in\widehat{\mathscr Q}_C\).  By (4.7), choose
\(k\in K_0\) with \(\widehat\vartheta(k)=\widehat q\).  Since

\[
 K_0\leq\Pi_S\leq[\widehat F_2,\widehat F_2],
\tag{5.8}
\]

we have

\[
 F_*k=F_{\rm arith}(u_*k),\qquad
 u_*k\in\Pi_S,\qquad
 F_*k\in[\widehat F_2,\widehat F_2].
\tag{5.9}
\]

V33/v37 put the two group-valued hexagon residuals and the group-valued
pentagon residual of (5.9) in their formation residuals.  BRUN-DEF also puts
the pentagon endpoint in its Brunnian subgroup.  Equation (5.3) therefore
puts the three exact Fox paths in (5.5).  Theorems 3.1 and 4.1 identify them
with \(\psi_\infty(\widehat w_0\widehat q)\), proving (5.7).

Different source preimages of \(\widehat q\) have the same enriched joint
tuple, including its loop classes, so Theorem 3.1 gives the same residual.
No false endpoint-only path choice is used. \(\square\)

## 6. Exact gain and remaining gates

V371 attempted to descend through the ordinary group joint image.  Its
purported map from a group endpoint to an arbitrary path class is rejected
by (1.4).  The present theorem gives the smallest lossless replacement:

\[
 \boxed{
 \text{ten group contexts}
 \quad\leadsto\quad
 \text{ten finite Magnus contexts}.}
\tag{6.1}
\]

This closes continuous residual descent and localized stability on the
enriched lane at paper level.  It also explains exactly what the physical
task198/task382 owner must serialize: endpoint values alone are insufficient;
the retained Fox/Magnus coordinates and their occurrence embeddings are
load-bearing.

It does not prove that \(L_{\rm loc}\) is finitely generated or strict for
the \(J\)-filtration.  It does not prove leading surjectivity of the enriched
seed Jacobian, the one-depth affine/nonlinear law on the enriched lane, or
settlement outside the registered gate ledger.  Those remain the hypotheses
needed to apply v369's Newton recursion.

    GROUP-ONLY PATH ENCODER OF V371:                    REJECTED
    FINITE MAGNUS-STATE FACTORIZATION:                  PAPER PROOF
    MATCHED ENRICHED INVERSE-LIMIT CONTINUITY:          PAPER PROOF
    ENRICHED LANE RELATIVE SOURCE PREIMAGES:            PAPER PROOF
    FORMATION/BRUNNIAN ENDPOINT-IDEAL LOCALIZATION:      PAPER PROOF / ABI TYPING
    TASK198/TASK382 MAGNUS-ABI EQUALITY:                 OPEN AUTHENTICATION
    STRICT/WEIGHTED LOCALIZED TARGET / LEADING ONTO:     OPEN
    ONE-DEPTH AFFINE / NONLINEAR GAIN:                  OPEN
    COMPATIBLE LIFT / FAKE / IHARA WITNESS:             NOT CONSTRUCTED

\(\mathtt{R07\_PATH\_BEARING\_JOINT\_RESIDUAL\_DESCENT\_V372\_PAPER\_GRADE}\)

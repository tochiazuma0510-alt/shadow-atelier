# R07 pro-Heisenberg / relative-Frattini dovetail v213

Author: Sol / 2026-08-28

Status: paper theorem generalizing v212 from the first successor to every
relative pro-3 Frattini rung.  At rung \(n\), the canonical class-two
exponent-\(3^{n+1}\) endpoint factors through the actual matched context
group \(\Delta_n\).  These factorizations are compatible and give a
continuous quotient of the full relative inverse limit onto the two-generator
pro-Heisenberg group \(\mathcal H_2(\mathbf Z_3)\).  The one-power-ahead
defect at every rung is a quotient of the actual Frattini kernel of dimension
at most three, so this entire infinite class-two lane has a uniform finite
selector.  The theorem does not prove that the actual pointed endpoint
vanishes at every rung and therefore does not by itself construct a compatible
lift, fake certificate, or Ihara witness.
verified=false.

## 1. The class-two 3-adic valuation filtration

For \(r\in\{3,4\}\) and \(s\geq1\), put

\[
 \mathcal N_r(3^s)=
 PB_r/\langle\gamma_3PB_r, g^{3^s}\ (g\in PB_r)\rangle^{\mathrm{normal}}.
\tag{1.1}
\]

V208's Malcev argument applies with 9 replaced by every odd power
\(3^s\).  Indeed, in a class-two group

\[
 (uv)^{3^s}=u^{3^s}v^{3^s}
 [v,u]^{\binom{3^s}{2}},
 \qquad 3^s\mid\binom{3^s}{2},
\tag{1.2}
\]

so the verbal power subgroup is exactly the sublattice obtained by
multiplying every Malcev coordinate by \(3^s\).  Thus
\(\mathcal N_r(3^s)\) has

\[
 a_r=\binom r2
 \quad\text{degree-one coordinates},\qquad
 b_r=\binom r3
 \quad\text{central commutator coordinates},
\tag{1.3}
\]

all in \(\mathbf Z/3^s\mathbf Z\).  In particular,

\[
 |\mathcal N_r(3^s)|=3^{s(a_r+b_r)}.
\tag{1.4}
\]

For \(0\leq a\leq s\), let \(U_a^{(s)}\) be the set of elements whose
every Malcev coordinate is divisible by \(3^a\).  Thus
\(U_0^{(s)}=\mathcal N_r(3^s)\) and \(U_s^{(s)}=1\).

### Lemma 1.1 (VALUATION RAISES UNDER FRATTINI)

For \(1\leq a<s\),

\[
 \boxed{
 (U_a^{(s)})^3\subseteq U_{a+1}^{(s)},\qquad
 [U_a^{(s)},U_a^{(s)}]\subseteq U_{a+1}^{(s)}.}
\tag{1.5}
\]

Consequently

\[
 \boxed{\Phi_3(U_a^{(s)})\subseteq U_{a+1}^{(s)}.}
\tag{1.6}
\]

#### Proof

In class-two Malcev coordinates the product is addition plus an integral
bilinear commutator term in the central coordinates.  If all coordinates of
\(g\) are divisible by \(3^a\), the degree-one coordinates of
\(g^3\) are divisible by \(3^{a+1}\).  Its central coordinates are
the sum of three times the old central coordinates and terms with one factor
\(\binom32=3\) and two degree-one coordinates.  Their valuations are
at least

\[
 a+1\qquad\text{and}\qquad 1+2a\geq a+1,
\tag{1.7}
\]

respectively.  This proves the first containment.

The commutator of two class-two elements is bilinear in their degree-one
coordinates, so its central coordinates are divisible by \(3^{2a}\).
Since \(2a\geq a+1\) for \(a\geq1\), the second containment
follows.  Equation (1.6) is the definition
\(\Phi_3(H)=H^3[H,H]\). \(\square\)

For \(a=1\), the quotient
\(U_1^{(s)}/U_2^{(s)}\) is the elementary-abelian layer used in v212.
Lemma 1.1 gives all later layers with the same formula.

## 2. Every exponent power occurs by its matching Frattini rung

Retain v145's componentwise relative Frattini tower

\[
 K_{r,0}=\ker(PB_r\to E_r),\qquad
 K_{r,n+1}=\Phi_3(K_{r,n}),\qquad
 E_{r,n}=PB_r/K_{r,n}.
\tag{2.1}
\]

The roof contains the maximal exponent-three factor, so

\[
 K_{r,0}\subseteq
 \ker\bigl(PB_r\to\mathcal N_r(3)\bigr).
\tag{2.2}
\]

### Theorem 2.1 (ALL-RUNG EXPONENT-POWER FACTORIZATION)

For every \(n\geq0\) and \(r\in\{3,4\}\),

\[
 \boxed{
 K_{r,n}\subseteq
 \ker\bigl(PB_r\to\mathcal N_r(3^{n+1})\bigr).}
\tag{2.3}
\]

Equivalently, there is a canonical marked surjection

\[
 \boxed{E_{r,n}\twoheadrightarrow\mathcal N_r(3^{n+1}).}
\tag{2.4}
\]

All maps in (2.4) commute with reduction in \(n\) and with every registered
group homomorphism between the PB3/PB4 contexts.

#### Proof

Fix \(n\), work in \(\mathcal N_r(3^{n+1})\), and write \(\eta\)
for the quotient map.  Equation (2.2) says

\[
 \eta(K_{r,0})\subseteq U_1^{(n+1)}.
\tag{2.5}
\]

Assume inductively that
\(\eta(K_{r,j})\subseteq U_{j+1}^{(n+1)}\) for some
\(j<n\).  Homomorphisms preserve cubes and commutators, so Lemma 1.1
gives

\[
 \eta(K_{r,j+1})
 =\eta(\Phi_3(K_{r,j}))
 \subseteq U_{j+2}^{(n+1)}.
\tag{2.6}
\]

At \(j=n-1\), this yields
\(\eta(K_{r,n})\subseteq U_{n+1}^{(n+1)}=1\), proving
(2.3).  The case \(n=0\) is exactly (2.2).  Quotienting gives (2.4).

The defining subgroups in (1.1) are verbal, and the factorization through a
quotient is unique.  This proves compatibility with context maps and with
the reductions \(3^{n+2}\to3^{n+1}\). \(\square\)

This is the uniform form of v212 Lemma 1.1; no new finite search is needed
when \(n\) increases.

## 3. The exact joint source group at every power

Let \(\Delta_n\) be the correctly typed joint image of the common source
\(F=F(x,y)\) in the two hexagon and five pentagon \(n\)-th context
quotients \(E_{r,n}\).  At all eleven literal occurrences, evaluate in
\(\mathcal N_r(3^{n+1})\), and let the joint image be \(D_n\).

### Theorem 3.1 (MATCHING JOINT HEISENBERG QUOTIENT)

There is a canonical marked surjection

\[
 \boxed{q_n:\Delta_n\twoheadrightarrow D_n,}
\tag{3.1}
\]

and the typed PB3 \((x=A_{12},y=A_{23})\) coordinate identifies

\[
 \boxed{
 D_n\cong\mathcal H_2(3^{n+1}),\qquad
 |D_n|=3^{3(n+1)}.}
\tag{3.2}
\]

The squares

\[
\begin{array}{ccc}
\Delta_{n+1}&\longrightarrow&\Delta_n\\
\downarrow q_{n+1}&&\downarrow q_n\\
D_{n+1}&\longrightarrow&D_n
\end{array}
\tag{3.3}
\]

commute, where the lower map is coordinate reduction modulo
\(3^{n+1}\).

#### Proof

Apply Theorem 2.1 at every typed occurrence and take the common-source
image.  This gives (3.1) and the commuting square.

Every occurrence factors through the free two-generator class-two
exponent-\(3^{n+1}\) group \(\mathcal H_2(3^{n+1})\).  Conversely,
the marked decomposition

\[
 PB_3\cong F(x=A_{12},y=A_{23})\times\langle z\rangle
\tag{3.4}
\]

shows, exactly as in v210 Lemma 1.1, that the displayed typed PB3
coordinate is faithful on that free factor after quotienting by class three
and all \(3^{n+1}\)-st powers.  Hence the joint diagonal image is neither a
proper quotient nor a larger group: it is \(\mathcal H_2(3^{n+1})\).
Its normal form has two degree-one coordinates and one commutator
coordinate modulo \(3^{n+1}\), giving the order in (3.2).
\(\square\)

For \(n=0\), this is the order-27 roof canary.  For \(n=1\), it is v212's
order-729 quotient.

## 4. A canonical pro-Heisenberg quotient of the whole ladder

Put

\[
 \Delta_\infty=\varprojlim_n\Delta_n,\qquad
 \mathcal H_2(\mathbf Z_3)
 =\varprojlim_n\mathcal H_2(3^{n+1}).
\tag{4.1}
\]

### Theorem 4.1 (CONTINUOUS PRO-HEISENBERG QUOTIENT)

The compatible maps (3.1) induce a continuous surjection

\[
 \boxed{
 q_\infty:\Delta_\infty\twoheadrightarrow
 \mathcal H_2(\mathbf Z_3).}
\tag{4.2}
\]

It is the unique continuous map sending the two marked source generators to
the standard pro-Heisenberg generators.

#### Proof

Compatibility (3.3) gives a unique continuous inverse-limit map.  The
diagonal image of \(F(x,y)\) is dense in \(\Delta_\infty\), because it
surjects onto every finite \(\Delta_n\).  Its image under
\(q_\infty\) is the subgroup generated by the two standard generators,
which is dense in \(\mathcal H_2(\mathbf Z_3)\).  The image of the compact
profinite group \(\Delta_\infty\) under a continuous map into a Hausdorff
profinite group is compact and therefore closed.  It contains a dense
subgroup, so it is the whole target.  Marked uniqueness follows from
density. \(\square\)

This quotient is an explicit object on the full infinite refinement, not a
collection of unrelated finite screens.  It supplies three coherent
\(\mathbf Z_3\)-coordinates: two marked exponent coordinates and one
signed class-two area coordinate.

## 5. The one-power-ahead defect is at most three dimensional

Write

\[
 H_n=\ker(F\to\Delta_n),\qquad
 K_n=\ker(\Delta_{n+1}\to\Delta_n).
\tag{5.1}
\]

Let

\[
 L_n=\ker(D_{n+1}\to D_n).
\tag{5.2}
\]

By (3.2),

\[
 \boxed{L_n\cong\mathbf F_3^3.}
\tag{5.3}
\]

The action by conjugation factors through \(D_n\), and hence through
\(\Delta_n\).

### Theorem 5.1 (UNIFORM NEXT-POWER DEFECT QUOTIENT)

Define

\[
 A_n=\phi_{n+1}(H_n)\leq L_n,
\tag{5.4}
\]

where \(\phi_{n+1}:F\to D_{n+1}\) is the joint source map.  There is a
canonical surjective \(\mathbf F_3[\Delta_n]\)-module map

\[
 \boxed{\lambda_n:K_n\twoheadrightarrow A_n.}
\tag{5.5}
\]

Consequently

\[
 \boxed{
 K_n/\ker\lambda_n\cong A_n,\qquad
 \dim_{\mathbf F_3}A_n\leq3.}
\tag{5.6}
\]

More simply, because Theorem 3.1 at rung \(n+1\) kills \(H_{n+1}\),

\[
 \boxed{\phi_{n+1}(H_{n+1})=1,\qquad
        A_n=\phi_{n+1}(H_n).}
\tag{5.7}
\]

The one-power-ahead screen factors already through \(\Delta_n\) if and
only if \(A_n=0\).

#### Proof

The map \(\phi_{n+1}\) factors through \(\Delta_{n+1}\) by
Theorem 3.1, proving the first equality in (5.7).  Its reduction to
\(D_n\) factors through \(\Delta_n\), so every element of \(H_n\)
maps into \(L_n\).  This proves (5.4), (5.5), and the dimension bound.

The source map sends \(H_n\) onto \(K_n\): every element of the kernel in
\(\Delta_{n+1}\) has a source representative, and that representative
maps to one in \(\Delta_n\).  Because \(H_{n+1}\) is killed by
\(\phi_{n+1}\), the latter descends to the surjection (5.5).
Conjugation compatibility makes it a module map.  Finally, factorization
through \(\Delta_n=F/H_n\) is equivalent to killing \(H_n\), which is
equivalent to \(A_n=0\). \(\square\)

At \(n=0\), v211's exact exponent lattice improves the generic rank-three
bound to

\[
 A_0=\langle[x,y]^3\rangle\cong C_3,
\tag{5.8}
\]

and \(\lambda_0\) is precisely v212's area functional.

## 6. Uniform finite compiler at every rung

Assume a complete word-bearing marked presentation

\[
 \Delta_n\cong\langle x,y\mid r_{n,1},\ldots,r_{n,m_n}\rangle
\tag{6.1}
\]

has been authenticated.  Put

\[
 b_{n,j}=\psi_{n+1}(r_{n,j})\in K_n,\qquad
 \ell_{n,j}=\phi_{n+1}(r_{n,j})\in L_n.
\tag{6.2}
\]

The v188/v209 normal-relator argument applies verbatim and gives

\[
 K_n=\mathbf F_3[\Delta_n]\langle b_{n,j}\rangle,\qquad
 A_n=\mathbf F_3[\Delta_n]\langle\ell_{n,j}\rangle,
\tag{6.3}
\]

with

\[
 \lambda_n(b_{n,j})=\ell_{n,j}.
\tag{6.4}
\]

Thus the class-two next-power quotient of the full successor kernel is
compiled by a rank closure in only three target coordinates.  A different
presentation may enlarge the input roster, but it cannot enlarge the
terminal target rank beyond three.  Literal ancestry is retained exactly as
in v188.

Let

\[
 J_{n+1}=\ker\bigl(\mathbf F_3[F]\to
                    \mathbf F_3[\Delta_{n+1}]\bigr).
\tag{6.5}
\]

Since \(\phi_{n+1}\) factors through \(\Delta_{n+1}\),

\[
 \boxed{
 \mathbf F_3[F]\supseteq J_{n+1}
 \longmapsto0\quad\text{in }\mathbf F_3[D_{n+1}].}
\tag{6.6}
\]

Therefore the exponent-\(3^{n+2}\) projected endpoint is constant on every
finite-support representative of one fixed \(\Delta_{n+1}\)-multiplier.
A nonzero projected endpoint is a complete no-repair certificate inside
that fibre.  A zero projected endpoint remains inconclusive for exact PB
equality.

## 7. What this gives, and what it does not

The theorem supplies the class-specific infinite-refinement object which was
missing from a purely finite dihedral argument:

\[
 \text{relative Frattini tower}
 \longrightarrow
 \mathcal H_2(\mathbf Z_3),
\tag{7.1}
\]

together with one rank-at-most-three next-power map \(\lambda_n\) at every
rung.  All maps are reductions of one continuous pro-object, so there is no
choice of unrelated finite sections and no inverse-limit compatibility
problem on this class-two quotient.

This is not yet a right inverse for the full pentagon correction map.  It
has two possible uses.

1. If an actual pointed endpoint is nonzero in one finite \(D_n\), (6.6)
   gives a durable obstruction to every same-stage finite-support repair;
   this is a witness-producing negative lane.
2. If every such endpoint vanishes, the compatible zeroes remove the entire
   pro-Heisenberg component, but higher lower-central, prime-to-three, and
   perfect-factor components still require their own homotopies.

Thus v213 supplies the coherent second axis that pure dihedral
antisymmetrization lacked, but it does not claim the direct sum of those two
axes is already the full relative A.18 homotopy.

## 8. Fixed frontier

\[
\begin{array}{ll}
E_{r,n}\twoheadrightarrow\mathcal N_r(3^{n+1})\ \text{ FOR ALL }n
 & \text{PAPER PROOF},\\
\Delta_n\twoheadrightarrow\mathcal H_2(3^{n+1})\ \text{ FOR ALL }n
 & \text{PAPER PROOF},\\
\Delta_\infty\twoheadrightarrow\mathcal H_2(\mathbf Z_3)
 & \text{CONTINUOUS SURJECTION / PAPER PROOF},\\
\dim_{\mathbf F_3}A_n\leq3
 & \text{UNIFORM ALL-RUNG BOUND},\\
\lambda_n:K_n\twoheadrightarrow A_n
 & \text{CANONICAL MODULE QUOTIENT},\\
J_{n+1}\longmapsto\mathbf F_3[D_{n+1}]
 & \text{ZERO},\\
\text{ACTUAL POINTED ENDPOINTS AT ALL RUNGS}
 & \text{NOT COMPUTED},\\
\text{FULL RETURN-EVEN RIGHT INVERSE}
 & \text{OPEN},\\
\text{COFINAL LIFT / FAKE / IHARA WITNESS}
 & \text{NOT CONSTRUCTED}.
\end{array}
\tag{8.1}
\]

`R07_PROHEISENBERG_FRATTINI_DOVETAIL_V213_PAPER_GRADE`

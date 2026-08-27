# R07 all-rung formation--Frattini residual formula v153

Author: Sol / 2026-08-27

Status: paper theorem.  Along the entire aligned relative pro-3 Frattini
tower, the no-\(PSL(2,8)\) formation residual and its intersection with every
transition kernel have a closed group-theoretic formula.  This removes the
need to solve a new extension-class descent problem at each rung.  It does not
prove the joint hexagon/pentagon correction equation is soluble and does not
name the arithmetic formation target at every rung.  No cofinal lift, fake
certificate, or Ihara witness is declared.

## 1. Aligned towers inside one free group

Let

\[
 F=F(x,y),
 \qquad q:F\twoheadrightarrow G,
 \qquad \Omega=\ker q,
\tag{1.1}
\]

where \(G\) is the fixed task157ee/task176 joint group.  Let

\[
 R=R_S(G)=\widetilde S,
 \qquad P=q^{-1}(R).
\tag{1.2}
\]

Write

\[
 \Phi(K)=\Phi_3(K)=K^3[K,K]
\tag{1.3}
\]

and define two aligned characteristic towers

\[
 \Omega_n=\Phi^n(\Omega),
 \qquad P_n=\Phi^n(P),
 \qquad n\geq0.
\tag{1.4}
\]

Both \(\Omega\) and \(P\) have finite index in the finitely generated free
group \(F\).  Hence every group in (1.4) has finite index, and

\[
 H_n:=F/\Omega_n
\tag{1.5}
\]

is finite.  The transition kernel from rung \(n+1\) to rung \(n\) is

\[
 V_n=\Omega_n/\Omega_{n+1}
 =H_1(\Omega_n;\mathbf F_3).
\tag{1.6}
\]

Let \(\mathcal C_S\) be the formation of finite groups with no composition
factor isomorphic to \(S=PSL(2,8)\).  It contains every finite 3-group and is
closed under quotients, finite subdirect products, and extensions.

## 2. A general perfectness lemma for the formation residual

### Lemma 2.1 (THE NO-S RESIDUAL IS PERFECT)

For every finite group \(X\), the residual

\[
 R_S(X)=\bigcap\{N\triangleleft X:X/N\in\mathcal C_S\}
\tag{2.1}
\]

is perfect.

#### Proof

Put \(D=R_S(X)\).  Closure under finite subdirect products gives

\[
 X/D\in\mathcal C_S.
\tag{2.2}
\]

The derived subgroup \(D'\) is characteristic in \(D\) and hence normal in
\(X\).  There is an extension

\[
 1\longrightarrow D/D'
 \longrightarrow X/D'
 \longrightarrow X/D
 \longrightarrow1.
\tag{2.3}
\]

The kernel in (2.3) is abelian and therefore belongs to \(\mathcal C_S\);
the quotient belongs to \(\mathcal C_S\) by (2.2).  Extension closure gives
\(X/D'\in\mathcal C_S\).  Minimality of the residual now gives

\[
 D\leq D'.
\tag{2.4}
\]

The reverse inclusion is automatic, so \(D=D'\). \(\square\)

This lemma is independent of the Schur multiplier.  V151 used the stronger
superperfectness of the coarse residual to identify the first coinvariant
quotient cohomologically; the all-rung residual formula below needs only the
formation axioms.

## 3. Closed residual formula at every rung

### Theorem 3.1 (ALIGNED FRATTINI RESIDUAL FORMULA)

For every \(n\geq0\),

\[
 \boxed{
 R_S(H_n)=P_n/\Omega_n.}
\tag{3.1}
\]

Here \(P_n/\Omega_n\) denotes its natural image in
\(H_n=F/\Omega_n\); the containment \(\Omega_n\leq P_n\) follows from
functoriality of \(\Phi\).

#### Proof

First consider the quotient by \(P_n\).  There is an exact sequence

\[
 1\longrightarrow P/P_n
 \longrightarrow F/P_n
 \longrightarrow F/P
 \longrightarrow1.
\tag{3.2}
\]

The group \(P/P_n\) is a finite 3-group, while

\[
 F/P\cong G/R\in\mathcal C_S.
\tag{3.3}
\]

Thus (3.2) and extension closure give

\[
 F/P_n\in\mathcal C_S.
\tag{3.4}
\]

Since \(\Omega_n\leq P_n\), (3.4) proves

\[
 R_S(H_n)\leq P_n/\Omega_n.
\tag{3.5}
\]

For the reverse inclusion, let \(N\triangleleft F\) satisfy

\[
 \Omega_n\leq N,
 \qquad F/N\in\mathcal C_S.
\tag{3.6}
\]

The quotient

\[
 F/N\Omega\cong G/(N\Omega/\Omega)
\tag{3.7}
\]

belongs to \(\mathcal C_S\).  By the definition of \(R=R_S(G)\),

\[
 R\leq N\Omega/\Omega,
\tag{3.8}
\]

or equivalently

\[
 P\leq N\Omega.
\tag{3.9}
\]

In \(F/N\), equation (3.9) says that the images of \(P\) and \(\Omega\)
are equal; the reverse containment uses \(\Omega\leq P\).  A surjection
commutes with \(K\mapsto\Phi(K)\), so

\[
 \operatorname{im}(P_n)
 =\Phi^n(\operatorname{im}P)
 =\Phi^n(\operatorname{im}\Omega)
 =\operatorname{im}(\Omega_n)=1,
\tag{3.10}
\]

where the last equality uses \(\Omega_n\leq N\).  Hence \(P_n\leq N\).
This holds for every \(N\) in (3.6), so

\[
 P_n/\Omega_n\leq R_S(H_n).
\tag{3.11}
\]

Together with (3.5), this proves (3.1). \(\square\)

The proof is uniform in \(n\).  It does not classify chief factors, choose a
section, or inspect an extension cocycle.

## 4. Exact formation-visible quotient of every transition kernel

At the fine group \(H_{n+1}\), Theorem 3.1 gives

\[
 R_S(H_{n+1})=P_{n+1}/\Omega_{n+1}.
\tag{4.1}
\]

Intersecting this subgroup with the transition kernel (1.6) gives

\[
 \boxed{
 V_{S,n}:=V_n\cap R_S(H_{n+1})
 =\frac{\Omega_n\cap P_{n+1}}{\Omega_{n+1}}.}
\tag{4.2}
\]

There is a canonical inclusion-induced linear map

\[
 \rho_n:
 \Omega_n/\Omega_{n+1}
 \longrightarrow P_n/P_{n+1},
 \qquad [w]\longmapsto[w].
\tag{4.3}
\]

It is well-defined because \(\Omega_{n+1}\leq P_{n+1}\).

### Theorem 4.1 (ALL-RUNG FORMATION SELECTOR)

For every \(n\geq0\), the map (4.3) is onto and

\[
 \boxed{\ker\rho_n=V_{S,n}.}
\tag{4.4}
\]

Consequently

\[
 \boxed{
 V_n/V_{S,n}
 \xrightarrow{\sim}P_n/P_{n+1}
 =H_1(P_n;\mathbf F_3).}
\tag{4.5}
\]

#### Proof

The kernel statement follows immediately from (4.2)--(4.3).  It remains to
prove surjectivity.

By Theorem 3.1 and Lemma 2.1,

\[
 P_n/\Omega_n=R_S(H_n)
\tag{4.6}
\]

is perfect.  The epimorphism \(P_n\twoheadrightarrow P_n/\Omega_n\) sends
\(P_{n+1}=\Phi(P_n)\) onto

\[
 \Phi(P_n/\Omega_n)=P_n/\Omega_n,
\tag{4.7}
\]

because the Frattini operator commutes with epimorphisms and a perfect group
equals its commutator subgroup.  Equation (4.7) is equivalent to

\[
 P_n=\Omega_nP_{n+1}.
\tag{4.8}
\]

Thus every class in \(P_n/P_{n+1}\) has a representative in \(\Omega_n\),
which proves that \(\rho_n\) is onto. \(\square\)

For \(n=0\), (4.5) is exactly the Schreier isomorphism of v152.  Theorem 4.1
shows that the same inclusion-and-abelianization selector persists at every
later relative Frattini rung even though the later residual groups need not
have trivial Schur multiplier.

## 5. Literal closed form and sparse computation

The selector at rung \(n\) is the literal formula

\[
 \boxed{
 \rho_n([w])=w\bmod P_{n+1},
 \qquad w\in\Omega_n.}
\tag{5.1}
\]

Since \(P_n\) is a finite-index subgroup of the rank-two free group \(F\), it
is free.  Freeze a prefix-closed Schreier transversal for \(P_n\leq F\).
Rewriting \(w\) in the resulting free basis and reducing exponent counts
modulo three computes (5.1) in

\[
 P_n/P_{n+1}=H_1(P_n;\mathbf F_3).
\tag{5.2}
\]

The exact dimension is

\[
 \dim_{\mathbf F_3}H_1(P_n;\mathbf F_3)
 =1+[F:P_n].
\tag{5.3}
\]

The state spaces grow rapidly, but each finite word produces a sparse vector
supported on at most its rewritten length.  A valid implementation retains:

1. the marked quotient \(F/P_n\), its complete finite Cayley roster, and the
   frozen parent/letter tree;
2. literal Schreier basis words or a lossless edge decoder;
3. direct membership gates \(w\in\Omega_n\leq P_n\);
4. the sparse mod-3 vector \(\rho_n([w])\);
5. an independent graph reconstruction and closed-loop replay; and
6. exact zero tests against \(\Omega_n\cap P_{n+1}\), not sampled paths.

At \(n=0\), task185's 708,588-state quotient graph supplies item 1.  At later
rungs, a resource cap is `UNKNOWN_RESOURCE`; it is not evidence that the
formation coordinate is nonzero or that a lift fails.

## 6. Triangular compatibility of an infinite correction product

If \(c_n\in\Omega_n\) is the correction chosen at rung \(n\), then every
later correction \(c_m\), \(m>n\), lies in

\[
 \Omega_m\leq\Omega_{n+1}\leq P_{n+1}.
\tag{6.1}
\]

Therefore

\[
 \rho_n([c_m])=0
 \qquad(m>n).
\tag{6.2}
\]

This proves the exact triangular compatibility required of the formation
coordinates: once the rung-\(n\) coordinate has been corrected, no later
factor changes it.  The partial products

\[
 f^{(N)}=g_{760}c_0c_1\cdots c_{N-1}
\tag{6.3}
\]

are automatically compatible in the relative pro-3 tower whenever each
\(c_n\) is chosen in \(\Omega_n\).

Theorem 4.1 does not itself choose \(c_n\).  It supplies the same explicit
formation quotient and the same zero-kernel test at every rung.

## 7. The remaining joint equation at rung n

Let

\[
 B_n:A_n\longrightarrow Z_n
\tag{7.1}

\]

be the literal word-bearing change map for the two hexagons and ordered
pentagon at rung \(n\), and let \(\beta_n\) be the actual defect of the
current partial word.  Restrict \(\rho_n\) to the same admissible correction
domain \(A_n\).  A formation-purified correction must solve

\[
 \boxed{
 B_n(c_n)=-\beta_n,
 \qquad
 \rho_n(c_n)=\eta_n
 \quad\text{in }P_n/P_{n+1}.}
\tag{7.2}
\]

Here \(\eta_n\) is the actual formation-reference displacement.  V150 fixes
its coarse rung-zero **coset type**, but v152 (6.2) shows that a coarse
arithmetic coset does not determine the first-Frattini displacement.  An
explicit arithmetic component or an independence theorem is required to name
\(\eta_n\) at each rung.

For the direct explicit-word route, one may solve only the first equation in
(7.2), replay the resulting original GT relations, and continue to the next
rung.  Such a direct successor must not be relabelled as the particular v18
formation-purified arithmetic branch unless the second equation is supplied.

The unresolved all-rung statement is therefore no longer the construction of
the formation residual or a compatible selector.  It is the surjectivity or
actual-target membership of the **joint** map

\[
 \boxed{
 (B_n,\rho_n):A_n\longrightarrow
 Z_n\oplus H_1(P_n;\mathbf F_3)}
\tag{7.3}
\]

on the literal target \((-\beta_n,\eta_n)\), uniformly in \(n\).

## 8. Exact advance over v148--v152

V148 characterized \(V_{S,n}\) by an extension-class descent problem and
left a cochain system at each rung.  V151 collapsed that system at the first
superperfect residual.  V152 compiled the first quotient by a 708,588-state
Schreier graph.  Theorems 3.1 and 4.1 now give the full tower at once:

\[
\begin{array}{c|c|c}
\text{rung }n&\text{formation residual}&\text{visible kernel quotient}\\
\hline
n\geq0&P_n/\Omega_n&P_n/P_{n+1}.
\end{array}
\tag{8.1}
\]

No new cohomology classification is required when \(n\) increases.  What
still has to be computed or proved is (7.3), together with exact
commutator/charmingness and the original relation replay.

```text
NO-PSL FORMATION RESIDUAL IS PERFECT:               PAPER_PROOF
R_S(F/Omega_n) = P_n/Omega_n FOR ALL n:             PAPER_PROOF
V_n / (V_n INTERSECT R_S) = H1(P_n;F3):             PAPER_PROOF
UNIFORM LITERAL SELECTOR rho_n([w])=[w] mod Phi(P_n): PAPER_PROOF
TRIANGULAR COMPATIBILITY OF LATER CORRECTIONS:       PAPER_PROOF
RUNG-0 SCHREIER GRAPH:                               TASK185 IN PROGRESS
ACTUAL JOINT TARGET MEMBERSHIP FOR (B_n,rho_n):      OPEN
EXPLICIT ARITHMETIC eta_n AT ALL RUNGS:              UNKNOWN_INPUT
COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:      NOT DECLARED
```

`R07_ALL_RUNG_FORMATION_FRATTINI_RESIDUAL_FORMULA_V153_PAPER_GRADE`

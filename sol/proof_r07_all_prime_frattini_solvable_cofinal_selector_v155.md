# R07 all-prime Frattini solvable-cofinal selector v155

Author: Sol / 2026-08-27

Status: paper theorem.  The all-rung residual and Schreier selector of v153
do not depend on using the prime (3) at every edge.  A single mixed-prime
Frattini tower, in which every prime occurs infinitely often, is cofinal for
all finite refinements whose relative kernel is solvable.  Thus prime-to-(3)
and mixed-prime abelian refinements do not require separate lifting theories.
The theorem does not prove the actual joint hexagon/pentagon target belongs
to the correction image at every edge, and it does not absorb a nontrivial
perfect relative kernel.  No cofinal GT lift, fake certificate, or Ihara
witness is declared.

## 1. One mixed-prime tower

Let

\[
 F=F(x,y),\qquad q:F\twoheadrightarrow G,\qquad \Omega=\ker q,
\tag{1.1}
\]

and let

\[
 R=R_S(G),\qquad P=q^{-1}(R),\qquad S=PSL(2,8),
\tag{1.2}
\]

as in v149--v154.  Fix once and for all a sequence of primes

\[
 \ell_0,\ell_1,\ell_2,\ldots
\tag{1.3}
\]

in which every prime occurs infinitely often.  For example, concatenate the
successive initial prime lists

\[
 (2),(2,3),(2,3,5),(2,3,5,7),\ldots .
\tag{1.4}
\]

For a group (K), write

\[
 \Phi_p(K)=K^p[K,K].
\tag{1.5}
\]

Define aligned characteristic towers recursively by

\[
 \Omega_0=\Omega,\quad P_0=P,\qquad
 \Omega_{n+1}=\Phi_{\ell_n}(\Omega_n),\quad
 P_{n+1}=\Phi_{\ell_n}(P_n).
\tag{1.6}
\]

Put

\[
 H_n=F/\Omega_n,
 \qquad
 V_n=\Omega_n/\Omega_{n+1}.
\tag{1.7}
\]

Functoriality of every (Phi_p) gives
(Omega_n\leq P_n).  Since (Omega) and (P) have finite index in the
rank-two free group, they are finitely generated.  Inductively,

\[
 K/\Phi_p(K)=H_1(K;\mathbf F_p)
\tag{1.8}
\]

is finite for every (K=\Omega_n,P_n).  Hence all groups in (1.6) have
finite index and every (H_n) is finite.  Moreover (P/P_n) has a finite
normal series whose factors are elementary abelian of primes
(ell_0,\ldots,\ell_{n-1}); in particular it is solvable.

## 2. The formation residual formula is prime-independent

Let (mathcal C_S) be the formation of finite groups with no composition
factor isomorphic to (S).

### Theorem 2.1 (MIXED-FRATTINI RESIDUAL FORMULA)

For every (n\geq0),

\[
 \boxed{R_S(H_n)=P_n/\Omega_n.}
\tag{2.1}
\]

#### Proof

The quotient (F/P_n) lies in an exact sequence

\[
 1\longrightarrow P/P_n\longrightarrow F/P_n
 \longrightarrow F/P\cong G/R\longrightarrow1.
\tag{2.2}
\]

The kernel is solvable and therefore belongs to (mathcal C_S); the
quotient belongs to (mathcal C_S) by the definition of (R).  Extension
closure gives (F/P_n\in\mathcal C_S), and hence

\[
 R_S(H_n)\leq P_n/\Omega_n.
\tag{2.3}
\]

Conversely, let (N\triangleleft F) satisfy

\[
 \Omega_n\leq N,\qquad F/N\in\mathcal C_S.
\tag{2.4}
\]

Reducing (2.4) modulo (Omega) and using (R=R_S(G)) gives

\[
 P\leq N\Omega.
\tag{2.5}
\]

Thus the images of (P) and (Omega) in (F/N) are equal.  Every
(Phi_p) commutes with epimorphic images.  Applying successively the same
functors
(Phi_{\ell_0},\ldots,\Phi_{\ell_{n-1}}) therefore gives

\[
 \operatorname{im}(P_n)=\operatorname{im}(\Omega_n)=1,
\tag{2.6}
\]

where the last equality uses (Omega_n\leq N).  Hence (P_n\leq N).
Intersecting over all (N) in (2.4) proves the reverse inclusion in
(2.1).  \(\square\)

No prime-specific cohomology enters the proof.  The only property of the
successive quotients used in (2.2) is solvability.

## 3. The same literal selector at every prime

At edge (n+1\to n), Theorem 2.1 gives

\[
 R_S(H_{n+1})=P_{n+1}/\Omega_{n+1}.
\tag{3.1}
\]

Therefore the residual part of the transition kernel is

\[
 V_{S,n}:=V_n\cap R_S(H_{n+1})
 =\frac{\Omega_n\cap P_{n+1}}{\Omega_{n+1}}.
\tag{3.2}
\]

Inclusion induces the literal map

\[
 \rho_n: \Omega_n/\Omega_{n+1}\longrightarrow P_n/P_{n+1},
 \qquad [w]\longmapsto[w].
\tag{3.3}
\]

### Theorem 3.1 (ALL-PRIME FORMATION SELECTOR)

For every (n\geq0), the map (3.3) is onto and

\[
 \boxed{\ker\rho_n=V_{S,n}.}
\tag{3.4}
\]

Consequently

\[
 \boxed{
 V_n/V_{S,n}\simeq P_n/P_{n+1}
 =H_1(P_n;\mathbf F_{\ell_n}).}
\tag{3.5}
\]

#### Proof

The kernel is (3.2).  By the general perfectness lemma v153 Lemma 2.1,

\[
 D_n:=P_n/\Omega_n=R_S(H_n)
\tag{3.6}
\]

is perfect.  Hence for every prime (p),

\[
 \Phi_p(D_n)=D_n^p[D_n,D_n]=D_n.
\tag{3.7}
\]

Apply the epimorphism (P_n\twoheadrightarrow D_n) to
(P_{n+1}=\Phi_{\ell_n}(P_n)).  Equations (3.6)--(3.7) give

\[
 P_n=\Omega_nP_{n+1}.
\tag{3.8}
\]

Thus every class of (P_n/P_{n+1}) has a representative in (Omega_n),
which proves surjectivity.  Equation (1.8) gives the final identification.
\(\square\)

After freezing a prefix-closed Schreier tree for (P_n\leq F), the closed
formula remains

\[
 \boxed{\rho_n([w])=w\bmod P_{n+1}.}
\tag{3.9}
\]

It is computed by ordinary Schreier rewriting followed by exponent counts
modulo (ell_n).  Thus changing the edge prime changes only the coefficient
field, not the selector or its proof.

## 4. Cofinality for every finite solvable relative kernel

### Theorem 4.1 (SOLVABLE-RELATIVE COFINALITY)

Let (N\triangleleft F) satisfy (N\leq\Omega), and suppose

\[
 Q=\Omega/N
\tag{4.1}
\]

is finite and solvable.  Then

\[
 \boxed{\Omega_n\leq N\quad\text{for some }n.}
\tag{4.2}
\]

Equivalently, the mixed-prime tower (F/\Omega_n) is cofinal among all
finite refinements of (F/\Omega) having solvable relative kernel.

#### Proof

Let (Q_n) be the image of (Omega_n) in (Q).  Surjections commute with
(Phi_p), so

\[
 Q_{n+1}=\Phi_{\ell_n}(Q_n).
\tag{4.3}
\]

The descending sequence (Q_n) eventually stabilizes because (Q) is
finite.  Write (Q_\infty) for its stable value.  Every prime occurs
infinitely often in (1.3), so stability forces

\[
 \Phi_p(Q_\infty)=Q_\infty
 \qquad\text{for every prime }p.
\tag{4.4}
\]

If the finite abelianization (Q_\infty^{\rm ab}) were nontrivial, choose a
prime (p) dividing its order.  Modulo the derived subgroup, the image of
(Phi_p(Q_\infty)) is (pQ_\infty^{\rm ab}), a proper subgroup.  This
contradicts (4.4).  Hence (Q_\infty) is perfect.  A solvable perfect group
is trivial, so (Q_\infty=1).  Thus some (Q_n=1), which is exactly
(4.2).  \(\square\)

This includes finite (2)-, (3)-, (5)-, and mixed-prime kernels, as
well as arbitrary finite solvable extensions.  There is no need to run one
independent cofinal construction for each prime.

## 5. Exact boundary of the generalization

For an arbitrary finite relative kernel (Q=\Omega/N), the same proof shows
that the stable image of the mixed-prime iteration is perfect.  It is the
part which cannot be removed by any abelian Frattini edge.  Therefore every
finite refinement decomposes conceptually into

\[
 \boxed{
 \text{mixed-prime solvable edges}
 \quad+\quad
 \text{a remaining perfect-core gate}.}
\tag{5.1}
\]

If (Q) is solvable, the second term is absent by Theorem 4.1.  If it is
not, a chief refinement of the perfect core contains nonabelian simple
factors and must be handled by the separately typed strip/accepted-set
theory.  No choice of primes can kill a nontrivial perfect group, since
(Phi_p(Q)=Q) for every (p).

This is the precise limit of a relative-dihedral generalization based only
on linear/Frattini homotopies.  It is stronger than the pure pro-(3) tower,
but it does not justify relabelling a nonabelian strip gate as another
linear rung.

## 6. Triangular compatibility and the remaining actual equation

If (c_n\in\Omega_n) is a correction at edge (n), then every later
correction (c_m), (m>n), lies in

\[
 \Omega_m\leq\Omega_{n+1}\leq P_{n+1}.
\tag{6.1}
\]

Hence it changes neither the earlier finite word nor its earlier formation
coordinate:

\[
 c_m=1\text{ in }F/\Omega_{n+1},\qquad
 \rho_n([c_m])=0.
\tag{6.2}
\]

Thus any sequentially constructed correction product is automatically
compatible.  At each mixed-prime edge the still-load-bearing equation is

\[
 \boxed{
 B_n(c_n)=-\beta_n,\qquad
 \rho_n(c_n)=\eta_n
 \quad\text{over }\mathbf F_{\ell_n}.}
\tag{6.3}
\]

The first row is the actual coupled two-hexagon/ordered-pentagon defect.  The
second is the formation-reference displacement.  Theorem 3.1 supplies the
same closed surjective formation selector at every edge; it does **not**
assert that the restriction of (ho_n) to the fibre
(B_n^{-1}(-\beta_n)) hits (eta_n).  Equivalently, it does not prove the
actual target belongs to the image of the joint map ((B_n,\rho_n)).

Therefore one successful finite rung does not, by itself, imply every later
rung.  What is now uniform is the tower, the coefficient prime, the
formation quotient, the zero-kernel test, and compatibility.  The only
repeated mathematical membership is the actual coupled defect class; at a
non-solvable refinement there is additionally the perfect-core strip gate.

## 7. Consequence for the explicit R07 programme

Combining v18, v153, and this theorem gives the following exact division of
work.

1. Every finite window with no (S)-factor is inherited from the arithmetic
   relative-dihedral base.
2. Above the pinned (S)-bearing component, every finite **solvable-kernel**
   refinement is dominated by the one mixed-prime tower (1.6).
3. At every edge the formation-visible quotient has the literal closed
   selector (3.9), and later choices cannot disturb earlier ones.
4. The remaining positive problem is actual membership for the coupled map
   (6.3), followed, only when present, by a finite perfect-core/simple-strip
   accepted set.

Thus prime-to-(3) refinements are no longer an untyped future obligation.
They are part of the same explicit recursion.  A task179 common word remains
the first actual relation solution, not a proof of the later memberships.

```text
MIXED-PRIME RESIDUAL FORMULA:                         PAPER_PROOF
ALL-PRIME LITERAL SELECTOR rho_n([w])=[w] mod P_{n+1}: PAPER_PROOF
COFINALITY FOR ALL FINITE SOLVABLE RELATIVE KERNELS:  PAPER_PROOF
TRIANGULAR COMPATIBILITY:                             PAPER_PROOF
PRIME-TO-3 / MIXED SOLVABLE REFINEMENTS:              UNIFORMLY TYPED
ACTUAL JOINT (B_n,rho_n) TARGET MEMBERSHIP:            OPEN
PERFECT-CORE / NONABELIAN SIMPLE STRIP GATES:          OPEN
TASK179 FIRST COMMON WORD:                             GHA IN PROGRESS
COMPATIBLE FULL R07 LIFT / FAKE / IHARA WITNESS:       NOT DECLARED
```

`R07_ALL_PRIME_FRATTINI_SOLVABLE_COFINAL_SELECTOR_V155_PAPER_GRADE`

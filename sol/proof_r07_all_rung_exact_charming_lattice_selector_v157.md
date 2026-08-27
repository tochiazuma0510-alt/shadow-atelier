# R07 all-rung exact-charming lattice selector v157

Author: Sol / 2026-08-27

Status: paper theorem.  V156 identifies the task179 joint-kernel exponent
lattice as \(18\mathbf Z^2\).  Along the mixed-prime Frattini tower of v155,
that one calculation determines the exponent lattice at every later rung.
Exact charmingness is enforced by two normalized finite-field rows at each
edge, and every zero-residue class has a closed \(p\)-power exactification
which is already invisible at that edge.  The theorem removes the repeated
integer-exponent problem; it does not prove membership for the coupled
hexagon/pentagon map, a nonabelian accepted set, a cofinal lift, fake, or an
Ihara witness.

## 1. Exponent images commute with Frattini descent

Let

\[
 F=F(x,y),\qquad \epsilon:F\longrightarrow\mathbf Z^2
\tag{1.1}
\]

be abelianization.  For a subgroup \(K\leq F\) and a prime \(p\), put

\[
 \Phi_p(K)=K^p[K,K].
\tag{1.2}
\]

### Lemma 1.1 (EXPONENT--FRATTINI IDENTITY)

For every \(K\leq F\) and every prime \(p\),

\[
 \boxed{\epsilon(\Phi_p(K))=p\,\epsilon(K).}
\tag{1.3}
\]

#### Proof

Every generator \(k^p\) of \(K^p\) has exponent \(p\epsilon(k)\), and every
commutator has exponent zero.  Hence the left side of (1.3) is contained in
the right side.  Conversely, for every
\(a=\epsilon(k)\in\epsilon(K)\), the word \(k^p\in\Phi_p(K)\) has exponent
\(pa\).  This proves the reverse containment. \(\square\)

No finite-group hypothesis or freeness of \(K\) is used here; only the free
abelianization of the ambient marked two-generator group is relevant.

## 2. Closed lattice at every mixed-prime rung

Use the v155 prime schedule

\[
 \ell_0,\ell_1,\ell_2,\ldots
\tag{2.1}
\]

and define

\[
 \Omega_0=\Omega,\qquad
 \Omega_{n+1}=\Phi_{\ell_n}(\Omega_n).
\tag{2.2}
\]

Put

\[
 m_0=1,\qquad m_n=\prod_{i=0}^{n-1}\ell_i\quad(n>0),
 \qquad L_n=\epsilon(\Omega_n).
\tag{2.3}
\]

V156 Theorem 3.1 gives \(L_0=18\mathbf Z^2\).  Iterating Lemma 1.1 gives:

### Theorem 2.1 (ALL-RUNG EXPONENT LATTICE)

For every \(n\geq0\),

\[
 \boxed{L_n=18m_n\mathbf Z^2,}
\tag{2.4}
\]

and at the edge \(n+1\to n\),

\[
 \boxed{L_{n+1}=\ell_nL_n.}
\tag{2.5}
\]

In particular, no Smith or Hermite computation is repeated after rung zero.
For the pure pro-3 lane this specializes to

\[
 L_n=18\cdot3^n\mathbf Z^2.
\tag{2.6}
\]

## 3. Two normalized rows are the exact charming quotient

The edge module is

\[
 V_n=\Omega_n/\Omega_{n+1}
     =H_1(\Omega_n;\mathbf F_{\ell_n}).
\tag{3.1}
\]

Define

\[
 \bar\epsilon_n:V_n\longrightarrow\mathbf F_{\ell_n}^2
\tag{3.2}
\]

by the literal closed formula

\[
 \boxed{
 \bar\epsilon_n([w])=
 \frac{\epsilon(w)}{18m_n}\bmod\ell_n,
 \qquad w\in\Omega_n.}
\tag{3.3}
\]

The division is coordinatewise over the integers.  It is defined by (2.4),
and it is independent of the representative by (2.5).

### Theorem 3.1 (EXACT-CHARMING CLASS SELECTOR)

The map (3.2) is onto.  Its kernel is exactly the set of edge classes which
possess an exact-commutator representative:

\[
 \boxed{
 \ker\bar\epsilon_n
 =\operatorname{im}\bigl(
   \Omega_n\cap[F,F]\longrightarrow V_n\bigr).}
\tag{3.4}
\]

#### Proof

Surjectivity follows from (2.4): choose words in \(\Omega_n\) whose exponent
vectors are \((18m_n,0)\) and \((0,18m_n)\).

An exact commutator has exponent zero and hence maps to zero.  Conversely,
let \(w\in\Omega_n\) have zero residue.  By (3.3),

\[
 \epsilon(w)=\ell_n a
 \quad\text{for some }a\in L_n.
\tag{3.5}
\]

Choose \(h\in\Omega_n\) with \(\epsilon(h)=a\).  Then

\[
 w^{\rm com}=wh^{-\ell_n}
\tag{3.6}
\]

has exact exponent zero.  Moreover
\(h^{\ell_n}\in\Phi_{\ell_n}(\Omega_n)=\Omega_{n+1}\), so \(w^{\rm com}\)
and \(w\) define the same class in \(V_n\).  This proves (3.4). \(\square\)

Thus exact charmingness is neither an infinite integer search nor a
post-hoc condition on a finite-field solve.  It is the kernel of the explicit
two-row quotient (3.3).

## 4. Explicit basis words at every rung

Let \(r_3,r_9,r_{12}\) be the three fixed lifted Q0-defect words named in
v156 equation (2.7).  V156 equation (3.4) gives the completely explicit
starting words

\[
 v_0=r_9r_{12}r_3^{-2},\qquad
 u_0=r_9v_0^{-8},
\tag{4.1}
\]

which lie in \(\Omega_0\) and satisfy

\[
 \epsilon(u_0)=(18,0),\qquad
 \epsilon(v_0)=(0,18).
\tag{4.2}
\]

Define recursively

\[
 \boxed{
 u_{n+1}=u_n^{\ell_n},\qquad
 v_{n+1}=v_n^{\ell_n}.}
\tag{4.3}
\]

Then \(u_n,v_n\in\Omega_n\) and

\[
 \epsilon(u_n)=(18m_n,0),\qquad
 \epsilon(v_n)=(0,18m_n).
\tag{4.4}
\]

This supplies a compatible word-bearing section of the two-dimensional
exponent quotient at every rung.  It requires no new enumeration and uses
only ordinary integer powers of the two frozen rung-zero words.

If a materialized candidate correction \(c_*\in\Omega_n\) has

\[
 \epsilon(c_*)=18m_n\ell_n(A,B),
\tag{4.5}
\]

then the closed exactification is

\[
 \boxed{
 c^{\rm com}_*=c_*u_n^{-\ell_n A}v_n^{-\ell_n B}.}
\tag{4.6}
\]

The added factor lies in \(\Omega_{n+1}\), so it changes neither the edge
class nor any earlier quotient.  Formula (4.6) is the all-prime version of
the \(54\mathbf Z^2\) cube repair in v156.

## 5. Coupling to the actual relation solve

Let

\[
 B_n:A_n\longrightarrow Z_n
\tag{5.1}
\]

be the actual word-bearing linearized change map for both hexagons and the
printed-order pentagon at edge \(n\), as in v153/v155.  Restrict
\(\bar\epsilon_n\) to the same correction domain.  The exact-charming
relation problem is

\[
 \boxed{
 (B_n,\bar\epsilon_n)(c_n)=(-\beta_n,0).}
\tag{5.2}
\]

### Theorem 5.1 (NORMALIZED AUGMENTED CRITERION)

Equation (5.2) has a word-bearing finite-field solution if and only if the
edge defect has an exact-commutator correction in the registered domain.
Every coefficient solution materializes such a correction by the closed
repair (4.6).

#### Proof

Necessity is immediate from exact exponent zero.  For sufficiency,
materialize the source correction word represented by the coefficient
solution.  Its second coordinate is zero, so Theorem 3.1 and (4.6) replace it
by an exact commutator without changing its class in \(V_n\).  Since \(B_n\)
is the edge linearization, the first coordinate remains
\(-\beta_n\). \(\square\)

For task179 at rung zero and prime three, (3.3) is exactly

\[
 \epsilon(w)/18\bmod3.
\tag{5.3}

The current implementation instead uses \(\epsilon(w)\bmod3\), which v156
proves is identically zero.  Later implementations must use (3.3), not copy
the raw task179 rows.

## 6. Infinite compatibility

Suppose \(g_{760}\) has exact exponent zero and each edge correction is
chosen through (5.2), then repaired by (4.6).  Every partial product

\[
 f^{(N)}=g_{760}c_0^{\rm com}\cdots c_{N-1}^{\rm com}
\tag{6.1}
\]

has exact exponent zero.  For \(m>n\), the later correction lies in
\(\Omega_m\leq\Omega_{n+1}\), so it changes neither the rung-\(n\) relation
class nor its normalized exponent coordinate.  Hence the exact-charming
repairs have the same triangular compatibility as the formation selectors of
v153/v155.

Combining those theorems, the uniformly typed linear edge problem is now

\[
 \boxed{
 (B_n,\rho_n,\bar\epsilon_n):A_n\longrightarrow
 Z_n\oplus H_1(P_n;\mathbf F_{\ell_n})
       \oplus\mathbf F_{\ell_n}^2.}
\tag{6.2}

The last component is completely solved by this note, and the middle
component has the closed onto selector of v155.  What remains open is the
actual simultaneous target membership after both are restricted to the
same \(B_n\)-fibre.  This theorem does not turn one finite success into all
later successes, but it removes exact charmingness as a separately repeated
obstruction at every one of those later edges.

```text
EXP(Phi_p(K)) = p EXP(K):                            PAPER_PROOF
ALL-RUNG LATTICE L_n = 18 PRODUCT(ell_i) Z^2:        PAPER_PROOF
NORMALIZED TWO-ROW SELECTOR AT EVERY EDGE:           PAPER_PROOF
ZERO RESIDUE <=> EXACT-COMMUTATOR REPRESENTATIVE:    PAPER_PROOF
EXPLICIT BASIS RECURSION u_{n+1}=u_n^p, v likewise: PAPER_PROOF
TRIANGULAR EXACT-CHARMING COMPATIBILITY:              PAPER_PROOF
ACTUAL JOINT (B_n,rho_n,eps_n) TARGET MEMBERSHIP:     OPEN
PERFECT-CORE ACCEPTED SETS:                           OPEN
TASK179 FIRST COMMON WORD:                            GHA IN PROGRESS
COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:       NOT DECLARED
```

`R07_ALL_RUNG_EXACT_CHARMING_LATTICE_SELECTOR_V157_PAPER_GRADE`

# R07 recursive relative-Magnus Frattini compiler v168

Author: Sol / 2026-08-27

Status: paper theorem and post-task186 consumer contract.  This note gives
an exact recursive construction of the genuine relative Frattini successor
from one fixed finite presentation.  It removes the need to build a new
Reidemeister--Schreier presentation and prevents Jennings depths from being
used as surrogate Frattini rungs.  It does not prove that task186 succeeds,
that the second-rung actual defect is correctable, that every perfect-core
accepted set is nonempty, or that an R07 fake/Ihara witness exists.

## 1. Presentation-level setup

Let

\[
 F=F(x_1,\ldots,x_d),\qquad
 P=F/R_F=\langle x_1,\ldots,x_d\mid r_1,\ldots,r_s\rangle,
\tag{1.1}
\]

where \(R_F\) is the normal closure of the displayed relators.  Fix a finite
marked quotient

\[
 q:P\twoheadrightarrow E,
 \qquad K=\ker q,
\tag{1.2}
\]

and let \(\pi:F\twoheadrightarrow E\) be the composite map.  Put
\(N=\ker\pi\), so \(R_F\leq N\) and \(K=N/R_F\).  Fix a prime \(p\).

Use the left Fox convention encoded by the crossed derivation

\[
 \delta:F\longrightarrow C_1:=\mathbf F_p[E]^d,
 \qquad
 \delta(x_i)=e_i,
 \qquad
 \delta(uv)=\delta(u)+\pi(u)\delta(v).
\tag{1.3}
\]

This definition fixes all inverse and prefix signs without relying on a
matrix-orientation convention.  Let

\[
 \mathcal B=
 \mathbf F_p[E]\langle\delta(r_1),\ldots,\delta(r_s)\rangle
 \leq C_1,
 \qquad M=C_1/\mathcal B.
\tag{1.4}
\]

Thus \(\mathcal B\) is the span of **all** left translates of the complete
presentation-relator Fox rows.  A proper prefix of that orbit is not
\(\mathcal B\).

Write the affine product as

\[
 (a,g)(b,h)=(a+gb,gh)
 \qquad(a,b\in M,\ g,h\in E).
\tag{1.5}
\]

Equation (1.3) gives a homomorphism

\[
 \mu:F\longrightarrow M\rtimes E,
 \qquad
 \boxed{\mu(w)=([\delta(w)],\pi(w)).}
\tag{1.6}
\]

Every \(r_j\) maps to \((0,1)\), so \(\mu\) descends to \(P\).

## 2. Exact kernel theorem

### Lemma 2.1 (MOD-p MAGNUS KERNEL FOR A FREE COVER)

Before quotienting by \(\mathcal B\), the homomorphism

\[
 F\longrightarrow C_1\rtimes E,
 \qquad w\longmapsto(\delta(w),\pi(w))
\tag{2.1}
\]

has kernel

\[
 \boxed{\Phi_p(N)=N^p[N,N].}
\tag{2.2}
\]

#### Proof

Take the regular \(E\)-cover of the bouquet with oriented edges labelled
\(x_1,\ldots,x_d\).  Its cellular one-chains are \(C_1\), and the lifted
edge path of a word \(w\) is exactly \(\delta(w)\).  A word is a loop in
this cover exactly when \(w\in N\).  Since the cover is a graph,

\[
 H_1(\text{cover};\mathbf F_p)
 =\ker D_1
 \cong N/N^p[N,N],
\tag{2.3}
\]

and the isomorphism is induced by the lifted edge path.  Therefore a loop
has zero one-chain exactly when its class in \(N/\Phi_p(N)\) is zero.  A
non-loop is already detected by the second coordinate in (2.1).  This proves
(2.2). \(\square\)

### Lemma 2.2 (THE COMPLETE BOUNDARY ORBIT IS EXACTLY THE RELATOR IMAGE)

Under the injection of Lemma 2.1,

\[
 \boxed{\mathcal B=\delta(R_F)=\delta(R_F\Phi_p(N))
 \subseteq\ker D_1,}
\tag{2.4}
\]

and this subspace corresponds exactly to
\(R_F\Phi_p(N)/\Phi_p(N)\leq N/\Phi_p(N)\).

Equivalently, for \(w\in N\),

\[
 \delta(w)\in\mathcal B
 \quad\Longleftrightarrow\quad
 w\in R_F\Phi_p(N).
\tag{2.5}
\]

#### Proof

For a defining relator \(r_j\) and \(g\in F\), the facts
\(\pi(r_j)=1\) and (1.3) give

\[
 \delta(gr_jg^{-1})=\pi(g)\delta(r_j),
 \qquad
 \delta(gr_j^{-1}g^{-1})=-\pi(g)\delta(r_j).
\tag{2.6}
\]

The restriction of \(\delta\) to \(N\), modulo \(p\), is additive and
kills \(\Phi_p(N)\).  Hence the image of the normal generators of \(R_F\)
is precisely the \(\mathbf F_p[E]\)-span in (1.4).  Lemma 2.1 identifies
that image with
\(R_F\Phi_p(N)/\Phi_p(N)\), proving both statements. \(\square\)

### Theorem 2.3 (RELATIVE-MAGNUS FRATTINI COMPILER)

The descended affine map has exact kernel

\[
 \boxed{
 \ker(\mu:P\to M\rtimes E)=\Phi_p(K)=K^p[K,K].}
\tag{2.7}
\]

Consequently the marked subgroup

\[
 \boxed{
 E^+:=\langle\mu(x_1),\ldots,\mu(x_d)\rangle
 \leq M\rtimes E}
\tag{2.8}
\]

is canonically a marked copy of

\[
 \boxed{P/\Phi_p(K).}
\tag{2.9}
\]

Its projection to \(E\) has kernel

\[
 \boxed{
 K/\Phi_p(K)
 \cong \ker D_1/\mathcal B
 =H_1(K;\mathbf F_p).}
\tag{2.10}
\]

#### Proof

An element of \(F\) maps trivially under (1.6) exactly when it lies in
\(N\) and its Fox chain belongs to \(\mathcal B\).  Lemma 2.2 identifies
this kernel in \(F\) as \(R_F\Phi_p(N)\).  Passing to \(P=F/R_F\) gives

\[
 R_F\Phi_p(N)/R_F
 =\Phi_p(N/R_F)=\Phi_p(K),
\tag{2.11}
\]

which proves (2.7)--(2.9).  The kernel of the projection of (2.8) consists
of the Fox chains of words in \(N\), modulo the relator image.  The cover of
the presentation two-complex has chain complex

\[
 C_2\xrightarrow{D_2}C_1\xrightarrow{D_1}C_0,
\tag{2.12}
\]

with \(\operatorname{im}D_2=\mathcal B\).  Its first homology is both sides
of (2.10). \(\square\)

The affine ambient group \(M\rtimes E\) can be larger than \(E^+\).  The
successor is the **marked generated subgroup** (2.8), not the whole affine
ambient group.  This distinction is load-bearing.

## 3. Uniform recursion on the genuine Frattini tower

Let \(E_0=P/K_0\) be any fixed finite marked quotient, choose primes
\(p_0,p_1,\ldots\), and put

\[
 K_{n+1}=\Phi_{p_n}(K_n),
 \qquad E_n=P/K_n.
\tag{3.1}
\]

At rung \(n\), evaluate the same fixed presentation over
\(\mathbf F_{p_n}[E_n]\), form \(\mathcal B_n,M_n\) by (1.4), and define

\[
 \mu_n(w)=([\delta_n(w)],\bar w_n).
\tag{3.2}
\]

### Corollary 3.1 (RECURSIVE MARKED SUCCESSOR)

For every \(n\),

\[
 \boxed{
 E_{n+1}\cong
 \langle\mu_n(x_1),\ldots,\mu_n(x_d)\rangle
 \leq M_n\rtimes E_n.}
\tag{3.3}
\]

The transition \(E_{n+1}\to E_n\) is affine projection, and its kernel is
\(H_1(K_n;\mathbf F_{p_n})\).  Thus one fixed presentation and one fixed
Fox routine compile every genuine relative Frattini rung.  No Jennings
truncation and no new presentation for \(K_n\) occurs in (3.3).

#### Proof

Apply Theorem 2.3 with \(E=E_n\), \(K=K_n\), and \(p=p_n\). \(\square\)

For the mixed-prime schedule of v155 this is the solvable-cofinal tower.  For
the constant prime three it is the pro-3 tower of v145.  The construction is
finite at every rung, although its dimensions need not remain bounded.

### Proposition 3.2 (MATCHED-DIAGRAM NATURALITY)

Let \(\varphi:P_r\to P_s\) be a structural map represented on the fixed
presentations by word substitution, and suppose it descends to
\(\bar\varphi_n:E_{r,n}\to E_{s,n}\).  The Fox chain rule induces a
semilinear cellular map

\[
 C_{1,r,n}\longrightarrow C_{1,s,n}
\tag{3.4}
\]

which sends \(\mathcal B_{r,n}\) into \(\mathcal B_{s,n}\) whenever the
complete relator roster is respected.  It therefore induces
\(E_{r,n+1}\to E_{s,n+1}\), and the square with the two affine projections
commutes.

#### Proof

Word substitution commutes with word evaluation and, by the Fox chain rule,
with (1.3).  A literal identity expressing the image of every source relator
in the target normal relator closure sends its translated boundary row into
the target boundary module.  Hence the affine map is well-defined.  Equation
(3.3), applied to the marked generators, proves the successor statement and
commutativity. \(\square\)

This is the exact place where the arity-3/4 maps must be authenticated.  An
untyped equality of ranks or row counts cannot replace (3.4).

## 4. The actual next defect is obtained by affine evaluation

Let \(W_1,W_2,W_P\) denote the two printed hexagon words and the
printed-order pentagon word evaluated on a current ordinary word \(f^{(n)}\).
Suppose they are trivial in the appropriate \(E_{r,n}\).  Then they lie in
\(K_{r,n}\), and Theorem 2.3 gives their exact next-rung values:

\[
 \boxed{
 \beta_n=
 \bigl([\delta_{3,n}(W_1)],
       [\delta_{3,n}(W_2)],
       [\delta_{4,n}(W_P)]\bigr),}
\tag{4.1}
\]

where the three boundary quotients remain separately block-tagged.  In
particular,

\[
 \beta_n=0
 \quad\Longleftrightarrow\quad
 W_1,W_2,W_P\text{ are trivial in }E_{3,n+1},E_{4,n+1}.
\tag{4.2}
\]

For an admissible source correction \(c\in\Omega_n\), exact collection in
the abelian kernels gives the already established affine change map

\[
 B_n[c]=
 \beta_n(f^{(n)}c)-\beta_n(f^{(n)}).
\tag{4.3}
\]

Hence the genuine successor equation is exactly

\[
 \boxed{B_n[c]=-\beta_n,}
\tag{4.4}
\]

with the formation and normalized-exponent rows of v155/v157 appended on
the same word-bearing domain.  Equations (4.1)--(4.4) do not mention a
Jennings depth.

## 5. Lazy exact implementation and the speed consequence

Theorem 2.3 does not require enumeration of all elements of
\(M_n\rtimes E_n\), and it does not even require enumeration of all of
\(E_{n+1}\).  A word is evaluated by the recurrence

\[
 (a,g)\cdot x_i^{\pm1}
\tag{5.1}
\]

using sparse Fox chains and the marked \(E_n\)-action.  Only equality of
translation coordinates modulo \(\mathcal B_n\) is nontrivial.  It may be
provided by either:

1. one complete echelon basis of the translated boundary span; or
2. a terminating exact membership/equality oracle which returns a full
   boundary coefficient chain on equality and a complete annihilating dual
   on inequality.

The second option is precisely the fail-closed column-generation pattern of
tasks 179/186/187.  Its answers can be memoized by the reduced sparse
difference.  Thus a post-task186 consumer can build only the affine prefix
values actually encountered in the second-rung defect and correction
columns.  It need not construct the astronomical full Cayley roster of
\(E_{r,1}\).

This laziness does not permit sampled boundary orbits.  Every negative
equality decision must annihilate the **complete** translated boundary
family.  A resource stop is `UNKNOWN_RESOURCE`.

### Corollary 5.1 (NO-RS SECOND-RUNG MATERIALIZATION)

After a positive exact task186 word \(f^{(1)}\), the actual
\(K_{r,1}/K_{r,2}\) defect can be materialized without a
Reidemeister--Schreier presentation of \(K_{r,1}\):

1. compile the marked affine quotients \(E_{3,1},E_{4,1}\) by (3.3) from
   the pinned PB3/PB4 presentations and complete task179 boundary modules;
2. evaluate every prefix of \(W_1,W_2,W_P\) as an affine pair, caching exact
   equality decisions modulo \(\mathcal B_0\);
3. run the same fixed PB Fox template over those marked affine values to
   obtain (4.1) in the second boundary quotient; and
4. construct only then the word-bearing columns of (4.4).

#### Proof

Steps 1--3 are Corollary 3.1 and (4.1), and Step 4 is the exact affine
linearization (4.3).  None of them changes the kernel being computed, so the
resulting module is \(K_{r,1}/K_{r,2}\), not a projection inside
\(K_{r,0}/K_{r,1}\). \(\square\)

## 6. Minimal post-task186 receipt

A versioned second-rung producer must retain at least:

1. the exact PB3/PB4 presentations, marked \(E_{r,0}\) maps, primes, and
   complete base boundary rows;
2. the affine marked-generator values (1.6) and the generated-subgroup
   convention (2.8), never the whole ambient semidirect product;
3. every affine prefix value used in the three literal relation words;
4. for each equality/canonicalization modulo \(\mathcal B_0\), either a
   literal boundary chain or a complete annihilating-dual replay;
5. the second-level PB relator Fox rows evaluated over the affine marked
   quotient, including all required left-translate provenance;
6. the literal block-tagged \(\beta_1\) of (4.1);
7. every candidate correction word, its membership in the common
   \(\Omega_1\) domain, and its direct column (4.3);
8. the joint solve with v155 formation and v157 normalized-exponent rows;
   and
9. direct evaluation of the resulting ordinary word in
   \(E_{3,2},E_{4,2}\).

The independent checker reconstructs the crossed derivations, boundary
orbits, affine products, and word evaluations without importing the
producer.  Hashes index objects but never replace literal regeneration.

The present task179/186 receipts contain item 1 at rung zero and, on a
positive run, the base word needed for item 3.  They do **not** yet contain
items 2--9 for the second rung.  The task189 inventory also shows that they
contain no cyclic deck character or cyclic level-transition receipt; the
recursive Frattini compiler must not be relabelled as v164 cyclic base
change.

## 7. Exact advance and remaining boundary

This theorem closes the previously vague instruction “build
\(K_{r,1}/K_{r,2}\)” at the group-construction level.  The same presentation,
Fox routine, and complete translated-boundary semantics recursively produce
the actual quotient and its named defect.  The two remaining substantive
questions are not quotient construction:

\[
 \boxed{
 -\beta_n\in
 \operatorname{im}(B_n,\rho_n,\bar\epsilon_n)
 \text{ at every solvable edge},}
\tag{7.1}
\]

and nonemptiness of the separately typed accepted set at every nonabelian
perfect-core edge.  A positive first rung is the necessary base point for
this recursion but does not prove (7.1) at later rungs.

```text
MOD-p MAGNUS KERNEL = Phi_p(N):                    PAPER_PROOF
COMPLETE FOX BOUNDARY QUOTIENT = RELATIVE H1:      PAPER_PROOF
AFFINE MARKED SUCCESSOR = P/Phi_p(K):              PAPER_PROOF
UNIFORM RECURSION ON GENUINE FRATTINI RUNGS:        PAPER_PROOF
MATCHED-MAP NATURALITY WITH COMPLETE RELATOR MAPS:  PAPER_PROOF
LAZY NO-RS MATERIALIZATION OF beta_1:               PAPER_PROOF
TASK186 EXACT FIRST WORD:                           GHA IN PROGRESS
SECOND-RUNG AFFINE PREFIX/EQUALITY RECEIPT:          NOT IMPLEMENTED
SECOND-RUNG ACTUAL DEFECT beta_1:                    NOT COMPUTED
ALL-RUNG ACTUAL JOINT MEMBERSHIP:                    OPEN
PERFECT-CORE ACCEPTED SETS:                          OPEN
COMPATIBLE R07 LIFT / FAKE / IHARA WITNESS:         NOT DECLARED
```

`R07_RECURSIVE_RELATIVE_MAGNUS_FRATTINI_COMPILER_V168_PAPER_GRADE`

# R07 adaptive actual-class Hensel selector v117

Author: Sol / 2026-08-27

Status: paper theorem separating a one-path explicit Hensel lift from the
stronger equivariant homotopy of v111.  To construct one named profinite R07
lift, it is enough to solve the successive actual residual classes by a
word-bearing based selector.  The annihilator condition of v111 is needed to
turn one preimage into a linear selector on an entire context orbit, but is
not necessary merely to advance one already chosen branch by one filtration
step.  The required R07 selectors have not yet been constructed at every
edge.  No fake or Ihara witness is declared.

## 1. The three distinct assertions

At an abelian chief or radical step let

\[
 D_k:C_k\longrightarrow Z_k
\tag{1.1}
\]

be the actual common-word linearization of v99, with every linear side
coordinate included in the target.  Let \(\beta_k\in Z_k\) be the residual
of the already chosen partial word.  There are three progressively stronger
statements.

1. **One-class membership:** \(-\beta_k\in D_k(C_k)\).
2. **Based next-step selector:** an effective rule returns one admissible,
   word-bearing \(c_k\in C_k\) with \(D_kc_k=-\beta_k\).
3. **Equivariant orbit splitter:** a module map \(h_k\) is defined on the
   whole context-stable subsystem and satisfies \(D_kh_k=1\).

The v111 annihilator condition

\[
 Ba=z,\qquad \operatorname{Ann}(z)a=0
\tag{1.2}
\]

characterizes statement 3 on a cyclic leading orbit.  It is stronger than
statement 1.  A proof of one explicit lift may use statement 2 recursively;
it does not have to manufacture statement 3 first.

## 2. Filtered word-valued setup

Let \(\mathcal C\) be a complete separated correction group with a descending
filtration

\[
 \mathcal C=F^0\mathcal C\supset F^1\mathcal C\supset\cdots,
 \qquad \bigcap_{k\geq0}F^k\mathcal C=1.
\tag{2.1}
\]

Let \(\mathcal Z\) be a complete separated residual object with filtration
\(F^k\mathcal Z\), and let \(\Phi(F)\) denote the simultaneous residual of
the two printed hexagons and the literal ordered A.18 pentagon, together with
the side coordinates which are being imposed at this step.  Corrections are
on the fixed right, \(F\mapsto Fc\).

Assume the exact filtered linearization furnished by v99: whenever
\(\Phi(F)\in F^k\mathcal Z\) and \(c\in F^k\mathcal C\),

\[
 [\Phi(Fc)]_k=[\Phi(F)]_k+D_{F,k}[c]_k
 \quad\text{in}\quad
 Z_{F,k}:=F^k\mathcal Z/F^{k+1}\mathcal Z,
\tag{2.2}
\]

where \([c]_k\) lies in the actual common-word correction image
\(C_{F,k}\).  The subscript \(F\) is load-bearing: an adaptive construction
allows the Jacobian and its actual image to depend on the partial word already
chosen.  Word evaluation and all quotient maps preserve the filtrations.

An **admissible based selector** at state \(F\) is a rule

\[
 S_k(F,\beta)\in C_{F,k}
\tag{2.3}
\]

defined for the actual residual class
\(\beta=[\Phi(F)]_k\), such that

\[
 D_{F,k}S_k(F,\beta)=-\beta.
\tag{2.4}
\]

It must also return a representative \(\widetilde c\in F^k\mathcal C\)
in the required marking, exact-commutator and relative-formation correction
domain, such that the corrected total word \(F\widetilde c\) passes every
nonlinear side gate registered at that edge.  No value of \(S_k\) on an
unrelated orbit translate is required.

## 3. Adaptive Hensel theorem

### Theorem 3.1 (ONE-PATH ADAPTIVE HENSEL LIFT)

Let the base word \(F_0\) have residual in \(F^0\mathcal Z\), with its coarse
R07 conditions and side gates already satisfied.  Suppose that at every
successive active abelian step the
actual residual belongs to the domain of an admissible based selector
\(S_k\).  Choose a word representative \(\widetilde c_k\) of
\(S_k(F_k,[\Phi(F_k)]_k)\), and define

\[
 F_{k+1}=F_k\widetilde c_k.
\tag{3.1}
\]

Then

\[
 \Phi(F_k)\in F^k\mathcal Z
\quad\text{for every }k.
\tag{3.2}
\]

The product

\[
 F_\infty=F_0\widetilde c_0\widetilde c_1\widetilde c_2\cdots
\tag{3.3}
\]

converges, and \(\Phi(F_\infty)=0\).  Every side gate included in the
definition of admissibility and preserved under reduction holds for
\(F_\infty\).

#### Proof

Assume \(\Phi(F_k)\in F^k\mathcal Z\).  Equations (2.2) and (2.4) give

\[
 [\Phi(F_{k+1})]_k
 = [\Phi(F_k)]_k+D_{F_k,k}[\widetilde c_k]_k=0.
\tag{3.4}
\]

Hence \(\Phi(F_{k+1})\in F^{k+1}\mathcal Z\), proving (3.2) by induction.
Because \(\widetilde c_k\in F^k\mathcal C\), the partial products in (3.3)
are Cauchy.  Completeness gives \(F_\infty\); continuity and separatedness
give

\[
 \Phi(F_\infty)\in\bigcap_kF^k\mathcal Z=\{0\}.
\]

Every finite quotient sees a stable partial product, so every continuous
side condition already imposed there passes to the limit. \(\square\)

The theorem is nonlinear and state-dependent.  It uses only the particular
class encountered along the selected branch.  Thus a failure of the v111
annihilator test does not prove that this adaptive route is impossible.

## 4. Effective explicitness

### Corollary 4.1 (COMPUTABLE BASED LIFT)

If the filtration, actual residual, finite correction domain, admissibility
test, and selector \(S_k\) are computable uniformly from \((k,F_k)\), then
(3.1) is an algorithm for the compatible finite values of one explicit
profinite lift.  V98 converts those values into a deterministic convergent
ordinary-word product.

This is stronger than the compact existence theorem v116: v116 needs only
nonempty complete accepted sets at every depth and may select a noncomputable
path.  Corollary 4.1 returns the next correction after a finite computation.

Uniformity here does not mean that one closed formula must solve every
abstract defect.  A terminating finite solver applied to the actual state is
a valid uniform selector.  What is forbidden is an unbounded search whose
failure cannot be distinguished from nonexistence.

## 5. When the annihilator condition becomes necessary

Let \(\Lambda=\mathbf F_3[\Delta]\), let \(B:A\to Z\) be the word-bearing
orbit-column map, and suppose \(z\) is the current leading residual.  A bare
solution \(Ba=z\) supplies statement 1 and hence one correction step.  To
define a formula

\[
 \sigma(\lambda z)=\lambda a
\tag{5.1}
\]

for every context translate, one must additionally have
\(\operatorname{Ann}(z)a=0\); this is exactly v111 Proposition 4.1.

Consequently:

- a full-E4 one-word solution is a legitimate first adaptive Hensel step;
- it is not yet a uniform orbit homotopy;
- a successful annihilator test upgrades it to the stronger v111 Neumann
  route; and
- if that upgrade fails, the based recursion (3.1) remains available,
  provided the next actual residual can again be solved.

This removes an unnecessary all-or-nothing choice between a global module
splitting and no explicit lift at all.

## 6. Fixed radical depth versus the cofinal tower

For the fixed \(\Pi_4[3]\) Jennings module, v109 proves \(I^{29}=0\).  Hence
an adaptive calculation through the remaining radical depths terminates
after finitely many steps.  It may use a different coefficient vector at
each new residual; no compatibility problem occurs because every new word
lies in the next accumulated kernel.

Across the cofinal matched tower there are infinitely many context-changing
and nonabelian chief steps.  Theorem 3.1 still applies to a based sequence,
but a witness proof must additionally establish one of the following:

1. a computable admissible selector for every encountered state;
2. a structural recurrence proving that the selected state always has an
   accepted child; or
3. the stronger natural homotopy of v111.

At a nonabelian chief edge, replace the affine selector by a finite accepted
set selector.  Nonemptiness and admissibility must be proved at the actual
state; abelian linearization does not supply it.

## 7. Current R07 application

Task 169 asks only for a word-bearing solution in a projected target6
quotient.  A positive result is input to, but not itself, (2.4) for the full
residual.  The first genuine adaptive step is obtained only after the v110
stacked solver returns one common word which kills both hexagons and the
ordered pentagon in the exact full relation modules and passes the registered
side gates.

After that word is found, there are two nonexclusive continuations.

1. Compute \(\operatorname{Ann}(z)\) and seek the v111 orbit splitter.  A
   success gives the closed Neumann formula.
2. Correct the resulting next actual residual directly and iterate Theorem
   3.1.  This can succeed even when no equivariant splitter exists on the
   whole cyclic orbit module.

The second route is the precise mathematical form of constructing an
explicit lift at every stage rather than first classifying the entire
abstract correction module.

```text
ONE-PATH ADAPTIVE HENSEL THEOREM:             PAPER_PROOF
COMPUTABLE BASED SELECTOR IMPLIES EXPLICIT:   PAPER_PROOF
ANNIHILATOR NEEDED FOR ORBIT-WIDE SPLITTER:   PAPER_PROOF (v111)
FULL-E4 TARGET6 ACTUAL WORD:                  NOT YET CONSTRUCTED
ALL-SEVEN COMMON CORRECTION WORD:             NOT YET CONSTRUCTED
NEXT-RESIDUAL ADAPTIVE SELECTOR:              OPEN
ALL SIDE GATES / NONABELIAN SELECTORS:        OPEN
COMPATIBLE COFINAL R07 LIFT:                  NOT CONSTRUCTED
FAKE / IHARA WITNESS:                         NOT DECLARED
```

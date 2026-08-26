# R07 based profinite selector by persistent finite cores v116

Author: Sol / 2026-08-27

Status: exact compactness theorem showing that a natural equivariant
homotopy is sufficient but not logically necessary for a compatible R07
lift.  Complete nonempty accepted sets at every finite cofinal level already
have a compatible inverse-limit point.  The theorem does not prove those
sets nonempty and does not make the resulting selector effectively
computable without an additional stabilization bound or uniform homotopy.
No fake or Ihara witness is declared.

## 1. Complete finite accepted sets

Fix a nested cofinal ladder of finite matched B3/B4/B5 windows.  At level
\(n\), let \(X_n\) be the finite set of **total corrected word values** which
simultaneously satisfy, through that level,

```text
both hexagons
the literal ordered A.18 pentagon
marking and exact-commutator conditions
relative-formation / Brunnian conditions
charmingness, descent, onto, and settlement gates
every already encountered nonabelian-chief accepted-set condition.
```

Thus \(X_n\) is not a target6 solution set and not the solution set of one
isolated chief edge.  Let

\[
 q_{mn}:X_m\longrightarrow X_n
 \qquad(m\geq n)
\tag{1.1}
\]

be reduction of the total word value.  The assertion that (1.1) is defined
is itself a typing requirement: every listed equation and side gate must be
preserved by reduction.  The maps satisfy

\[
 q_{nn}=1,
 \qquad q_{\ell n}=q_{mn}q_{\ell m}
 \quad(\ell\geq m\geq n).
\tag{1.2}
\]

## 2. Compactness without surjective bonding maps

### Theorem 2.1 (FINITE COFINAL COMPACTNESS)

If

\[
 \boxed{X_n\neq\varnothing\quad\text{for every }n,}
\tag{2.1}
\]

then

\[
 \boxed{\varprojlim_n X_n\neq\varnothing.}
\tag{2.2}
\]

No individual bonding map \(X_{n+1}\to X_n\) is assumed surjective.

#### Proof

Give every finite \(X_n\) the discrete topology.  The product

\[
 \mathcal X=\prod_{n\geq0}X_n
\tag{2.3}
\]

is compact.  For \(m\geq n\), let

\[
 C_{mn}=\{(x_i)\in\mathcal X:q_{mn}(x_m)=x_n\}.
\tag{2.4}
\]

Each \(C_{mn}\) is closed.  Any finite collection of these conditions uses
only finitely many indices.  Choose an upper index \(r\), select any
\(x_r\in X_r\), and define all constrained lower coordinates by reduction;
the remaining coordinates are arbitrary.  Equations (1.2) make every chosen
condition hold.  Hence the family \(\{C_{mn}\}\) has the finite intersection
property.  Compactness gives

\[
 \bigcap_{m\geq n}C_{mn}\neq\varnothing,
\]

which is (2.2).  \(\square\)

This is the precise compactness principle relevant to the earlier question
about measure theory.  No measure or positive-density assertion is needed;
finite discreteness and compactness are enough.

## 3. Persistent cores and a canonical based path

For every \(n\), define the persistent core

\[
 Y_n=igcap_{m\geq n}q_{mn}(X_m)\subseteq X_n.
\tag{3.1}
\]

For fixed \(n\), the sets \(q_{mn}(X_m)\) decrease as \(m\) increases.
They are nonempty subsets of the finite set \(X_n\), so the intersection is
nonempty and stabilizes after finitely many strict decreases.

### Lemma 3.1 (PERSISTENT-CORE SURJECTIVITY)

The restricted maps

\[
 \boxed{q_{n+1,n}:Y_{n+1}\twoheadrightarrow Y_n}
\tag{3.2}
\]

are surjective.

#### Proof

Fix \(y\in Y_n\).  For \(m\geq n+1\), let

\[
 S_m=\{q_{m,n+1}(x):x\in X_m, q_{mn}(x)=y\}.
\tag{3.3}
\]

The definition of \(Y_n\) makes every \(S_m\) nonempty.  They form a
decreasing family of subsets of the finite fibre
\(q_{n+1,n}^{-1}(y)\), hence have nonempty intersection.  An element in that
intersection belongs to \(Y_{n+1}\) and maps to \(y\).  \(\square\)

Fix any authenticated total order on each \(X_n\).  Define recursively

\[
 \begin{aligned}
 c_0&=\min Y_0,\\
 c_{n+1}&=\min\{y\in Y_{n+1}:q_{n+1,n}(y)=c_n\}.
 \end{aligned}
\tag{3.4}

Lemma 3.1 makes (3.4) well-defined.

### Corollary 3.2 (CANONICAL BASED SELECTOR)

The sequence \((c_n)\) of (3.4) is a canonical compatible point of
\(\varprojlim X_n\), relative to the authenticated orders.

It is based rather than context-equivariant.  Therefore the modular
norm-transfer obstruction of v114 does not apply to its definition.

## 4. Passage to one profinite word

Assume the finite values \(c_n\) lie in quotients of one profinite correction
domain \(\mathcal U\), and the ladder is cofinal and separated.  Then the
compatible family defines

\[
 c_\infty\in\mathcal U.
\tag{4.1}
\]

Let \(F_0\) be the fixed g760-based word and set

\[
 F_\infty=F_0c_\infty.
\tag{4.2}
\]

Every relation and side gate in Section 1 is decided in a finite quotient and
is continuous.  Its value on \(F_\infty\) is therefore the value already
recorded by every sufficiently fine \(c_n\).  Hence \(F_\infty\) satisfies
all registered conditions on the cofinal ladder.

V98 supplies ordinary-word representatives for successive compatible values
in accumulated transition kernels.  It can therefore spell (4.2) as a
convergent profinite product once the complete accepted values \((c_n)\) have
been obtained.

## 5. Existence versus effective explicitness

Although each descending family in (3.1) stabilizes, Theorem 2.1 gives no
uniform bound on the depth at which it stabilizes.  Consequently (3.4) is a
canonical mathematical definition but is not automatically an algorithm
which prints the next correction after a known finite amount of work.

An effective explicit witness follows from any one of the following stronger
certificates.

1. A computable bound \(b(n)\) such that

   \[
   Y_n=q_{b(n),n}(X_{b(n)}).
   \tag{5.1}
   \]

2. A finite-state transition theorem recognizing exactly which nodes have
   arbitrarily deep extensions.
3. The v111 filtration-raising homotopy, which returns the next correction by
   a closed Neumann formula.
4. A based class-specific recurrence which proves, for its selected node, an
   accepted child at every next edge.

Thus compactness removes ``choosing compatible \((c_n)\)'' as an existence
obstruction after complete finite nonemptiness is known.  It does not remove
the present substantive obligation to prove that nonemptiness uniformly, and
it does not turn target6 membership into a complete accepted set.

## 6. Correct use in the R07 campaign

There are now two valid promotion routes after a full seven-evaluation word
has been constructed.

\[
\boxed{
\begin{array}{ll}
\text{closed-form route:}&
\text{v111 actual homotopy + side-gate/nonabelian interleave},\\[1mm]
\text{based compactness route:}&
X_n\neq\varnothing\text{ for every complete finite window}
\ +\ \text{persistent-core selector}.
\end{array}}
\tag{6.1}
\]

The second route is logically weaker and survives the v114 no-go, but it can
be computationally much harder because complete \(X_n\) must include all
relations and gates simultaneously.  The current target6 and task-169 solves
are only projections of \(X_n\); they are not evidence for hypothesis (2.1)
until the missing blocks and gates are intersected.

```text
FINITE NONEMPTY INVERSE-LIMIT THEOREM:        PAPER_PROOF
PERSISTENT-CORE SURJECTIVITY:                 PAPER_PROOF
CANONICAL BASED SELECTOR:                     PAPER_PROOF / NOT YET EFFECTIVE
R07 COMPLETE FINITE ACCEPTED SETS X_n:        NOT YET CONSTRUCTED
UNIFORM NONEMPTINESS OF X_n:                  OPEN
EFFECTIVE STABILIZATION BOUND / RECURRENCE:   OPEN
COMPATIBLE COFINAL R07 LIFT:                  NOT CONSTRUCTED
FAKE / IHARA WITNESS:                         NOT DECLARED
```

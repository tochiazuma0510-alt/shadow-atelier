# R07: selected-ancestry straight-line lift without flat word expansion (v464)

## 0. Purpose and boundary

V395 and v444 require word-bearing instruction ancestry.  The current
grade-one producer instead attempts to flatten selected ancestry into a map
of all literal leaves before it evaluates the next precision.  This note
proves that flattening is not mathematically necessary: the selected acyclic
ancestry itself is one explicit literal straight-line program (SLP), and it
can be evaluated directly at every finite quotient.

This does not supply the pending grade-one MEMBER coefficients.  It is the
positive-branch continuation theorem to use after the decision-first v463
checkpoint.  `verified=false`.

## 1. The literal SLP language

Let (F) be the fixed free source group with a descending filtration
(F=F^0\supseteq F^1\supseteq\cdots) such that each
(F^d/F^{d+1}) used here is an (mathbf F_3)-space.  A typed SLP has:

1. leaves carrying the exact registered free words for compact seeds and
   old correction words;
2. ordered product and inverse nodes;
3. conjugation by a registered literal actor word; and
4. references only to earlier nodes.

It is therefore finite and acyclic.  Its semantic expansion
(operatorname{word}(T)\in F) is defined recursively by the displayed group
operations.  This definition is an explicit word even when its flat letter
list is not materialized.

For a coefficient (a\inmathbf F_3), put

\[
 [a]=0,1,-1\quad\hbox{for}\quad a=0,1,2.             \tag{1.1}
\]

If an echelon ancestry node records

\[
 b_j=\sigma_j\left(z_j-\sum_{p<j}q_{jp}b_p\right)
       \quad\text{in }F^d/F^{d+1},                    \tag{1.2}
\]

with (sigma_j\in\{1,2\}), define its literal lift in the fixed order

\[
 W_j=\left(
       Z_j\prod_{p<j}^{\longrightarrow}W_p^{[-q_{jp}]}
      \right)^{[\sigma_j]}.                            \tag{1.3}
\]

Here (Z_j) is the seed, transition-defect or actor-conjugate SLP specified
by the node origin.  Zero exponents are omitted.  No commutation or collection
is performed in (1.3).

For target coefficients (a_j), the selected correction is

\[
 C_T=\prod_j^{\longrightarrow}W_j^{[a_j]}.            \tag{1.4}

Only roots with (a_j\ne0) and the downward subgraph reachable from them
belong to the exported SLP.

## 2. Associated-grade correctness

### Theorem 2.1 (SLP LIFT)

Suppose every origin (Z_j) lies in (F^d) and has the registered
associated-grade class (z_j).  Then

\[
 [W_j]_d=b_j,qquad [C_T]_d=\sum_j a_jb_j.            \tag{2.1}

#### Proof

The quotient (F^d/F^{d+1}) is abelian of exponent three.  Ordered product,
inverse and conjugation therefore induce respectively addition, negation and
the registered actor action.  Induction over the acyclic order turns (1.3)
into (1.2).  Applying the same observation to (1.4) proves the second
identity.  No equality above degree (d) is asserted. (square)

If a lower-first fibre node is built from filtered old lifts whose lower
physical combination is zero, direct evaluation of its SLP at the lower
quotient proves that (W_j) belongs to the relative kernel.  A coefficient
row without this direct lower replay is not enough.

### Corollary 2.2 (FLATTENING CHANGES ONLY THE NEXT RESIDUAL)

Let (C_{m flat}) be any other literal lift obtained by collecting and
sorting the same associated-grade ancestry.  Then

\[
 C_T C_{m flat}^{-1}\in F^{d+1}.                    \tag{2.2}

Thus replacing flat expansion by (1.3)--(1.4) preserves the completed
grade-(d) MEMBER equation.  The grade-((d+1)) residual must be recomputed
from (C_T); it must not be copied from a residual calculated for
(C_{m flat}).

#### Proof

Both words have the same class in (F^d/F^{d+1}) by Theorem 2.1.  Equation
(2.2) is exactly the kernel statement. (square)

## 3. Naturality and the explicit-lift interpretation

For every quotient homomorphism (pi:F\to Q), evaluate the same SLP by
replacing each leaf and operation by its image in (Q).  Structural induction
gives

\[
 operatorname{ev}_Q(T)=\pi(operatorname{word}(T)),
 qquad
 r_{Q',Q}operatorname{ev}_{Q'}(T)=operatorname{ev}_Q(T)   \tag{3.1}

whenever (Q'\to Q) is a registered refinement map.  Hence an exported SLP
is not a separate finite-stage coefficient choice.  It is one common source
instruction whose values at all finite quotients are automatically
compatible.

This is precisely the syntactic naturality required by v395.  Each of the
eleven occurrences evaluates the same source SLP with its own substitution,
actor path, prefix and sign; no common occurrence action is inferred.

## 4. Positive decision handoff

After a v463 MEMBER decision, the compact coefficient list selects the roots
of (1.4).  The retained binary reduction/origin transcripts from the prepare
and four block states are traversed backwards once to mark the reachable
subgraph.  The positive handoff then consists of:

1. the v463 decision checkpoint and packed basis;
2. the selected root coefficients;
3. the reachable nodes of the old, lower, block and physical-grade DAGs,
   with every origin, scale and ordered reduction edge;
4. the exact leaf words and actor labels; and
5. the SLP root (1.4).

The checker independently interprets this finite syntax, evaluates it in all
eleven occurrences, proves every required lower/auxiliary coordinate zero and
reproduces the grade-one target.  It then evaluates the **same** SLP through
degree two and constructs the next residual.  Neither the entire discovery
DAG nor a flat leaf multiset is needed for those equalities.

This does not relax v281's separate A7 provenance gate for its factored pair
language.  It supplies a different positive representative for the present
filtered correction and requires fresh direct replay of that representative.

## 5. Complexity and failure semantics

If the selected subgraph has (V) nodes and (E) ordered edges, the stored
SLP has size (O(V+E)), regardless of the length of its full flat expansion.
At one finite group, memoized evaluation computes every selected node once,
plus its recorded ordered products.  Resource exhaustion while marking or
evaluating the selected subgraph is `UNKNOWN_RESOURCE`, not NONMEMBER.

For a NONMEMBER decision no ancestry export or SLP evaluation is performed.

## 6. Claim boundary

```text
SELECTED ANCESTRY -> LITERAL SLP:          PAPER-CLOSED
SLP GRADE-d CLASS = MEMBER COEFFICIENTS:  PAPER-CLOSED
ONE SLP NATURAL AT ALL QUOTIENTS:         PAPER-CLOSED
FLAT EXPANSION BEFORE NEXT REPLAY:         NOT REQUIRED
FRESH NEXT-GRADE RESIDUAL FOR THIS SLP:    REQUIRED
ACTUAL GRADE-ONE COEFFICIENTS / SLP:       NOT YET AVAILABLE
COFINAL SUCCESSOR SURJECTIVITY:            NOT PROVED
FAKE / IHARA:                              NOT DECLARED
```


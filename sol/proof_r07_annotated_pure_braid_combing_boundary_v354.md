# R07 annotated pure-braid combing boundary compiler (v354)

Author: Sol / 2026-08-29

Status: paper theorem making v197's practical annotated-rewriting branch
explicit for the exact PB3/PB4 presentations emitted by task292.  The
recursive pure-braid presentation is collected as
`P_n = F_(n-1) semidirect P_(n-1)` while every move retains a conjugate of an
original presentation relator.  Hence an exact endpoint-zero receipt can be
compiled to the three finite boundary chains without an unbounded relator
product search.  No actual endpoint-zero receipt or boundary chain is
asserted.  `verified=false`.

## 1. The exact recursive presentation already used by task292

Let

\[
 \mathcal A_n=\{A_{ij}:1\leq i<j\leq n\}
\tag{1.1}
\]

in task292's lexicographic `i`-then-`j` order.  Split it as

\[
 \mathcal A_n=\mathcal A_{n-1}\sqcup
 \mathcal K_n,
 \qquad
 \mathcal K_n=(A_{1n},\ldots,A_{n-1,n}).
\tag{1.2}
\]

The task292 routine `pure_relations(n)` first embeds the complete relations
for `P_(n-1)` and then, for every `a=A_ij` in `A_(n-1)` and
`k=A_kn` in `K_n`, inserts

\[
 r_{a,k}=a^{-1}ka\,\varphi_a(k)^{-1},
 \qquad
 \varphi_a(k)=a^{-1}ka\in F(\mathcal K_n).
\tag{1.3}
\]

The word for `phi_a(k)` is computed by the same faithful Artin action and
then reindexed into `K_n`.  This gives two relators for `P_3` and eleven for
`P_4`, including the recursively embedded two `P_3` relators.

The Fadell--Neuwirth splitting, in exactly this convention, is

\[
 \boxed{P_n\cong P_{n-1}\ltimes F(\mathcal K_n),}
\tag{1.4}
\]

with the old factor written on the left.  Thus every element has a unique
normal form

\[
 p,u,qquad p\in P_{n-1},\quad u\in F(\mathcal K_n).
\tag{1.5}
\]

For ranks three and four, (1.3) is precisely the complete presentation owner
already authenticated by task292; no new relation is added.

## 2. Annotated equality calculus

An annotation for a free-word equality `L=R` is a finite roster

\[
 \mathcal T=((s_1,i_1,\epsilon_1),\ldots,
             (s_m,i_m,\epsilon_m))
\tag{2.1}
\]

such that literal free reduction proves

\[
 \boxed{LR^{-1}=\prod_{h=1}^m
 s_h r_{i_h}^{\epsilon_h}s_h^{-1},
 \qquad\epsilon_h\in\{1,-1\}.}
\tag{2.2}

Annotations are closed effectively under:

1. insertion into a context `c L d -> c R d`, which conjugates the trace by
   `c` after the already equal suffix cancels;
2. reversal of a rewrite, which reverses the trace and inverts every signed
   relator; and
3. concatenation of consecutive rewrites: if annotations prove `L=R` and
   `R=S`, their two conjugate-relator products concatenate because
   `LS^-1=(LR^-1)(RS^-1)`.

Every operation is checked by literal multiplication, inversion and free
reduction; a claimed trace is never accepted from its endpoint alone.

For a positive old generator `a` and positive kernel generator `k`, (1.3)
gives the basic collection move

\[
 k a\longrightarrow a\varphi_a(k).
\tag{2.3}

Indeed,

\[
 (ka)(a\varphi_a(k))^{-1}
 =a r_{a,k}a^{-1},
\tag{2.4}

so (2.3) has a one-relator annotation.  Its negative-kernel variant is
obtained by inversion and context from the same annotation.

For an old inverse, put

\[
 h=\varphi_{a^{-1}}(k^{\epsilon}).
\tag{2.5}

Repeated use of (2.3) first supplies an annotation of

\[
 h a\longrightarrow a k^{\epsilon}.
\tag{2.6}

Reversing (2.6) and conjugating gives the required rule

\[
 k^{\epsilon}a^{-1}longrightarrow a^{-1}h.
\tag{2.7}

Thus all four sign choices in a kernel-letter/old-letter crossing are
derived from the original positive relators (1.3), not registered as new
unproved relations.

### Lemma 2.1 (ANNOTATED KERNEL-WORD COLLECTION)

For every freely reduced `u in F(K_n)` and old letter
`a^epsilon in A_(n-1)^(+/-1)`, there is a finite annotated rewrite

\[
 \boxed{u a^\epsilon\longrightarrow
 a^\epsilon\varphi_{a^\epsilon}(u).}
\tag{2.8}

#### Proof

For positive `a`, move `a` from right to left across the letters of `u`,
starting with the rightmost letter, using the signed versions of (2.3).
The resulting kernel suffix is the letterwise image `phi_a(u)`.  For
`a^-1`, apply (2.5)--(2.7) letterwise.  Compose the finitely many annotations
using Section 2.  \(\square\)

## 3. Total annotated combing in ranks three and four

Read a word `w` from left to right while maintaining an annotated equality

\[
 w_{\leq r}=p_r u_r,
 \qquad p_r\in F(\mathcal A_{n-1}),
 \quad u_r\in F(\mathcal K_n).
\tag{3.1}
\]

A kernel letter is appended to `u_r` and freely reduced.  For an old letter
`a^epsilon`, Lemma 2.1 gives

\[
 p_r u_r a^\epsilon
 \longrightarrow
 (p_r a^\epsilon)\varphi_{a^\epsilon}(u_r).
\tag{3.2}

After the input is exhausted, apply the same algorithm recursively to the
old word `p_r`.  Rank two is a free cyclic group and stops after free
reduction.

### Theorem 3.1 (PROOF-PRODUCING PURE-BRAID NORMAL FORM)

For `n=3,4`, the algorithm terminates on every finite word and returns a
normal form (1.5) together with an annotation from the input word to that
normal form using only the task292 relator roster.  If task292's faithful
Artin key says that the input represents the identity, the normal form is
the empty word and the annotation is a literal van Kampen expression

\[
 \boxed{w=\prod_h s_h r_{i_h}^{\epsilon_h}s_h^{-1}.}
\tag{3.3}

#### Proof

Each input letter is processed once at the current rank; Lemma 2.1 performs
a finite number of crossings, and the recursion lowers the rank, proving
termination.  Induction on the processed prefix proves (3.1), while Section
2 preserves the literal trace invariant (2.2).  Uniqueness in the
semidirect product (1.4) says that an identity has both old and free-kernel
parts trivial.  Free reduction removes them without relator annotations,
leaving (3.3).  The faithful Artin key is used as an independent identity
check, not as a substitute for the trace.  \(\square\)

This algorithm can expand substantially, but it has no mathematical search
branch.  A process resource stop is operational `UNKNOWN_RESOURCE`; a
resumable implementation records the processed input position, `p_r,u_r`
and the finite annotation DAG.

## 4. From the task292 zero chain to three boundary chains

On a task292 ZERO terminal, each block `B` contains the collected chain

\[
 z_B=\sum_{g,A_{ij}}c_{g,ij}\,g[A_{ij}],
 \qquad D_1z_B=0,
\tag{4.1}
\]

with a literal representative word and a full Artin key for every supported
`g`.  Apply v197's finite support-graph construction and choose a spanning
tree.  It gives

\[
 z_B=\sum_{e\notin T}a_e\delta(w_e),
\tag{4.2}

where every `w_e` is a finite literal identity word.  Run Theorem 3.1 on
each `w_e` and write its trace as in (3.3).  Define

\[
 q_B=\sum_{e\notin T}a_e
       \sum_h\epsilon_{e,h}\,\overline{s_{e,h}}
       [r_{i(e,h)}].
\tag{4.3}

### Theorem 4.1 (TASK292 ZERO TO EXPLICIT ORIGINAL-RELATOR BOUNDARY)

For each `B in {H1,H2,P}`, the finite chain (4.3) uses only the original
task292 PB3/PB4 presentation relators and satisfies

\[
 \boxed{D_{2,B}q_B=z_B.}
\tag{4.4}

#### Proof

Theorem 3.1 supplies literal identities (3.3).  Left Fox differentiation
gives

\[
 \delta(w_e)=\sum_h\epsilon_{e,h}\overline{s_{e,h}}
              \delta(r_{i(e,h)}).
\tag{4.5}

Substitute (4.5) into (4.2); the result is exactly (4.4).  \(\square\)

Unlike a second translated-boundary membership search, Theorem 4.1 is a
finite deterministic compilation after the exact endpoint terminal.  An
independent checker may choose a different spanning tree and trace, but it
must directly replay the producer's (4.4) as well as its own output.

## 5. Physical compiler contract

A minimal A8 compiler consumes an independently accepted v4/v5 MEMBER and
its task292 ZERO object.  For each block it must retain:

1. the exact collected `z_B` from `full_C1_replay`;
2. all support vertices, connecting paths, the oriented spanning tree and
   the fundamental-cycle equality (4.2);
3. every combing state and original-relator annotation (3.3);
4. the collected chain `q_B`; and
5. a fresh task292-normal-form/Fox replay of (4.4).

Negative traversal of an edge labelled `A_ij` is serialized as

\[
 (g,A_{ij})^{-1}=-gA_{ij}^{-1}[A_{ij}],
\tag{5.1}
\]

so coefficients remain in `F3` and are never treated as unsigned flows.
Checkpoint/resume binds the input receipt and stores only literal words,
integer cursors and annotation DAG nodes; exact group values are recomputed.

```text
TASK292 PB3/PB4 ROSTER HAS RECURSIVE SEMIDIRECT FORM: PAPER PROOF
ALL SIGNED COLLECTION RULES FROM ORIGINAL RELATORS: PAPER CONSTRUCTION
FINITE IDENTITY WORD -> ANNOTATED RELATOR TRACE:     TOTAL ALGORITHM
ENDPOINT-ZERO z_B -> EXPLICIT q_B:                  PAPER PROOF
SECOND TRANSLATED-D2 MEMBERSHIP SEARCH:              REMOVED
ACTUAL TASK292 ZERO INPUT / q_H1,q_H2,q_P:           NOT COMPUTED
A9 / MIXED-PRIME / PERFECT-CORE:                     OPEN
COMPATIBLE LIFT / FAKE / IHARA WITNESS:              NONE
```

`R07_ANNOTATED_PURE_BRAID_COMBING_BOUNDARY_V354_PAPER_GRADE`

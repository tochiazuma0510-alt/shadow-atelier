# R07 lazy full-boundary affine-kernel algorithm v272

Author: Sol / 2026-08-29

Status: paper algorithm after v231, v247, v267, v268, and the v271 erratum.
It replaces an infeasible eager construction of the full PB boundary space by
an exact lazy quotient oracle, while retaining a genuinely complete
nonmembership certificate.  It also states the word-DAG recurrence in the
correct affine/Fox type.  No actual A4 rank, basis, anchor, lift, fake, or
Ihara witness is declared.  `verified=false`.

## 1. Why the full marked closure is a theorem, not the hot path

V271 gives a correct finite algorithm for

\[
 D=\bigoplus_{i=0}^{9}
   \operatorname{span}_{\mathbf F_3}
   \{q d_{i,j}:q\in E_i\}.
\tag{1.1}
\]

It closes 65 tagged seeds under all signed marked PB generators.  This is a
complete independent construction, but its terminal rank can be comparable
with a large part of the full finite-index relation module.  The bound
(65+6b_3+12b_4) is rank-bounded, not small merely because it is finite.
Eagerly materializing all of (D) is therefore not the production strategy.

A4 only asks finitely many questions of the form

\[
 v\in D+L,
\tag{1.2}
\]

where (L) is the span of the K rows already accepted.  A lazy column oracle
can answer (1.2) exactly without enumerating (E_3,E_4), or a basis of all
of (D).

## 2. Abstract lazy quotient lemma

Let (V) be a finite-dimensional vector space, let
(D=\operatorname{span}(\mathcal C)), and let (L\le V) have an explicit
finite basis.  Maintain an explicit coefficient-bearing basis (B\le D),
initially zero or containing columns discovered by earlier queries.  Given a
target (v\in V), repeat:

1. reduce (v) against (U=B+L);
2. if the remainder is zero, return the explicit (B/L) combination;
3. otherwise construct a dual (lambda\in V^*) with
   (lambda(U)=0) and (lambda(v)\ne0);
4. if some (c\in\mathcal C) has (lambda(c)\ne0), insert one such (c)
   into (B) with its literal provenance and repeat;
5. if no such (c) exists, return (lambda).

### Theorem 2.1 (LAZY COMPLETE QUOTIENT DECISION)

The procedure terminates and returns exactly one of:

\[
 \begin{array}{ll}
 \textsf{MEMBER}:&v\in D+L\text{ with an explicit replay};\\
 \textsf{NONMEMBER}:&v\notin D+L\text{ with }
   \lambda(D+L)=0, \lambda(v)\ne0.
 \end{array}
\tag{2.1}
\]

#### Proof

In step 4, (lambda(B)=0) but (lambda(c)\ne0), so the new column is not in
(B) and strictly raises its rank.  Thus only finitely many step-4
iterations occur.  A zero remainder gives the recorded expression in
(B+L\subseteq D+L).  If step 5 occurs, annihilation of every generator in
(mathcal C) implies (lambda(D)=0); step 3 already gives
(lambda(L)=0) and (lambda(v)\ne0), which proves nonmembership.  If
(v\in D+L), step 5 is impossible by applying (lambda) to that expression.
(square)

Columns retained by one query remain useful for every later query.  Existing
K rows cannot become dependent when new boundary columns are discovered:
each was accepted only after a dual annihilating the *whole* (D), not just
the current (B), certified its independence modulo all earlier K rows.

## 3. Complete support-inversion oracle for the 65 tagged seeds

Write a tagged base boundary as

\[
 d_{i,j}=\sum_{c,h}a_{i,j,c,h}[i,c,h].
\tag{3.1}
\]

Its left translate by (t\in E_i) is

\[
 t d_{i,j}=\sum_{c,h}a_{i,j,c,h}[i,c,th].
\tag{3.2}
\]

For a finite-support dual (lambda), put

\[
 F_{i,j}(t)=\langle\lambda,t d_{i,j}\rangle
   =\sum_{c,h}a_{i,j,c,h}\lambda_{i,c,th}.
\tag{3.3}
\]

Every potentially nonzero summand has a unique support element (g=th),
and hence

\[
 t=gh^{-1}.
\tag{3.4}
\]

Therefore the following finite correlation computes *all* nonzero values of
(3.3): for every base occurrence ((i,j,c,h,a)) and every matching dual
support ((i,c,g,\lambda_{i,c,g})), form (t=gh^{-1}), check (th=g), and
accumulate (a\lambda_{i,c,g}) under the full key ((i,j,t)).  Only 65
tagged base rows are traversed; the group itself is not.

### Lemma 3.1 (SUPPORT-INVERSION COMPLETENESS)

After complete accumulation, a nonzero key ((i,j,t)) is exactly an active
column for step 4 of Theorem 2.1.  If every accumulator is zero, then
(lambda(D)=0).

#### Proof

Equations (3.3)--(3.4) give a bijection between its summands and the processed
matching occurrence/support pairs.  Grouping by the complete key sums exactly
(F_{i,j}(t)).  A translate not represented by a key has no matching dual
support and therefore pairs to zero. (square)

The coordinate (i), relator (j), and translation (t) are all mandatory
parts of the key.  The producer may choose the lexicographically first
nonzero key.  The checker should independently sort/group a flat pair stream
or use a different map/echelon convention, then replay every returned
translation and every final zero correlation.

## 4. Actual affine word evaluator

For each context (i), substitute a source word into the fixed PB3/PB4
context of v231 and let

\[
 \mathcal A_i(w)=(\rho_i(w),\partial_i w)
\tag{4.1}
\]

be its roof value and sparse left-Fox gradient.  The exact recurrence is

\[
 \begin{aligned}
 (a,u)(b,v)&=(ab,u+a\cdot v),\\
 (a,u)^{-1}&=(a^{-1},-a^{-1}\cdot u).
 \end{aligned}
\tag{4.2}

Thus the forty signed context actors are obtained once by actual
`fox_gradient_without_sections` evaluations of the two substituted source
letters in ten contexts and their affine inverses.  A prefix trie evaluates
the 288 authenticated primitive source words by (4.2); the 6,441 literal
ancestry identities then assemble their affine values.  Only after this
affine assembly may the ten coordinate gradients be injected into the tagged
A4 row module.

V268 remains valid after replacing every occurrence of a cached group value
by the affine value (4.1).  Its inventory bounds count trie edges and row
assembly nodes, but each edge now performs the sparse affine operation in
(4.2).  Since all 6,441 roof words are relators, their final roof components
must be identity; the gradient is the nontrivial successor defect.  A
roof-only trie would make all relators indistinguishable and is invalid.

The independent checker uses a reverse suffix trie and right-associated
applications of (4.2).  Both sides directly compare a deterministic sample
of primitive values with flat `fox_gradient_without_sections`; every newly
materialized K basis word and the v247 anchor is flat-replayed on both sides.

## 5. Word-bearing K closure modulo the whole boundary space

Let (r_1,\ldots,r_{6441}) be the accepted complete roof presentation and
let (b_j) be their actual ten-tagged affine defects.  Maintain:

- the discovered boundary basis (B\le D), with raw labels
  `B:(i,j,t)` and translated-relation provenance;
- an ordered list of immutable raw K rows and source words;
- a coefficient-bearing echelon for the current (B+L); and
- a queue containing exactly the accepted K basis rows not yet acted on.

Query each initial (b_j) by Theorem 2.1.  On a NONMEMBER terminal, normalize
the remainder and insert it as a new K row.  Then, for every dequeued K basis
row, form its four actual conjugates by (x^{\pm1},y^{\pm1}), query each in
the same complete quotient oracle, and enqueue only a new quotient-rank
raise.  Queue exhaustion gives the K of v231.

Suppose a query returns

\[
 r=b+\sum_{ell<t}c_\ell k_\ell+s^{-1}k_{\rm new}
 \quad (b\in D, s\in\mathbf F_3^\times).
\tag{5.1}
\]

If (w_r) and (w_\ell) are the retained source words, use the deterministic
literal word

\[
 w_{\rm new}=\operatorname{red}
   \left( w_r\prod_{ell<t}w_\ell^{-c_\ell}\right)^s,
\tag{5.2}
\]

with increasing (ell), explicit powers (0,1,2), and the registered
outer-first convention for conjugated candidates.  The first-successor
kernel is elementary abelian, so (5.2) evaluates to the normalized quotient
row; its flat affine defect must differ from the stored raw representative by
exactly the boundary combination in (5.1).  This direct replay, rather than
formal DAG shape, is the word-bearing certificate.

### Theorem 5.1 (LAZY A4 KERNEL CORRECTNESS)

If every quotient query has the certificate of Theorem 2.1 and the source
queue exhausts, the accepted rows form an ordered word-bearing basis of

\[
 K=\mathbf F_3[\Delta_0]\langle b_1,\ldots,b_{6441}\rangle.
\tag{5.3}
\]

#### Proof

Theorem 2.1 makes each accepted row independent and each rejected row
dependent modulo the *whole* (D) and the earlier K rows.  Hence the ordered
rows are a basis of the quotient span reached by the queue.  Queue exhaustion
makes this span invariant under the four source actions and it contains all
initial defects.  V231 Theorem 2.1 identifies that invariant span with K.
Equation (5.2) and its direct replay supply the source word for each basis
row. (square)

## 6. The v247 anchor and terminal certificates

Evaluate every accepted K basis word in the fixed
(D_1=\mathcal H_2(9)) projection.  Let (j) be the least basis index with
nonzero (z_0)-exponent, set the inverse scalar (e\in\{1,2\}), and form the
literal powered word (u_z=u_j^e).  Both evaluator implementations must
replay

\[
 \rho_0(u_z)=1,
 \qquad \rho_1(u_z)\in K,
 \qquad q(\rho_1(u_z))=z_0.
\tag{6.1}
\]

No shaped anchor is permitted.  If every projected exponent is zero, the
result contradicts the accepted projected-kernel theorem and is
`UNKNOWN_INPUT`, not a negative A4 result.

For every MEMBER query, the checker replays the explicit raw boundary/K
combination.  For every NONMEMBER query, it independently proves the supplied
dual annihilates all prior K rows and all of (D) by Lemma 3.1 and pairs
nontrivially with the target.  These local certificates are enough; neither
side must serialize a complete basis of (D).

## 7. Resource accounting and checkpoint rule

Let (n=6441), let (t=\dim K), let (p) be the total number of boundary
columns discovered by all queries, and let (Q=n+4t+q_{\rm anchor}) be the
number of complete quotient queries.  If (lambda_q) is the dual used in a
correlation round and (o_{i,c}) is the number of matching occurrences in
the 65 base rows, the exact correlation-pair work is

\[
 \sum_{q\text{ rounds}}
 \sum_{(i,c,g)\in\operatorname{supp}\lambda_q}o_{i,c}.
\tag{7.1}
\]

There are exactly (p) rank-raising active-boundary rounds and at most one
complete-zero round per quotient query.  This is the honest performance
measure; neither (4b) nor a hidden enumeration of (E_i) belongs in the
hot-path claim.  Base occurrence inverses and component indexes are computed
once.  Trie values, raw rows, and flat word replays are cached by immutable
node/row ids, never by unbounded recursive expansion.

A replayable checkpoint must contain the immutable authority identity, next
row/query ordinal, raw B/K rosters and ancestries, both echelon states or a
deterministic rebuild recipe, K queue head, DAG nodes, and resource counters.
A label without these owners is not a checkpoint.  A cap before a certified
query terminal or queue exhaustion returns only `UNKNOWN_RESOURCE`.

## 8. Fixed frontier

```text
FULL EAGER MARKED-BOUNDARY CLOSURE:             CORRECT BUT NOT HOT PATH
65-SEED SUPPORT-INVERSION LAZY ORACLE:          PAPER PROOF
AFFINE PREFIX/SUFFIX DAG RECURRENCE:             PAPER PROOF
LAZY WORD-BEARING K CLOSURE:                    PAPER PROOF
V247 LEAST-INDEX ANCHOR EXTRACTION:              PAPER PROOF
ACTUAL A4 BOUNDARY COLUMNS / K RANK / ANCHOR:   NOT COMPUTED
ACTUAL A5 / A6:                                 NOT COMPUTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:         NONE
```

`R07_LAZY_FULL_BOUNDARY_AFFINE_KERNEL_ALGORITHM_V272_PAPER_GRADE`

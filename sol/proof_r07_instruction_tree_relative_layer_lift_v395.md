# R07 instruction-tree relative-layer lift criterion v395

Author: Sol / 2026-08-30

Status: paper theorem replacing the rejected reduction in v394.  Literal
actor paths are retained separately in every occurrence.  The theorem gives
an exact necessary-and-sufficient one-step lifting condition and an explicit
recursive selector once a word-bearing right inverse of the relative kernel
map is supplied.  It does not prove that the actual R07 relative-kernel maps
are onto, and therefore does not yet declare a compatible lift, fake, or
Ihara witness.  `verified=false`.

## 1. The source is syntax, not a common coefficient module

Fix the registered cofinal tower.  At level (n), let (D_n) be the finite
legal correction space and (L_n) the finite actual residual space.  Write

\[
 r^D_n:D_{n+1}\longrightarrow D_n,
 \qquad
 r^L_n:L_{n+1}\longrightarrow L_n                         \tag{1.1}
\]

for the registered reductions.  Any side, boundary, exponent-zero, and
based conditions are included in the definition of (D_n).  Equivalently,
one may start from an ambient source and replace it by the kernel of all
those maps before using this note.

Let \(\mathcal I\) be the completed word-bearing instruction tree generated
by the following typed nodes:

1. a named relative correction leaf (S_b), carrying its literal source
   word;
2. a named actor leaf (P_j), carrying its literal source path;
3. multiplication and inversion nodes;
4. a conjugation node \(\operatorname {Conj}(P,T)\); and
5. a commutator node \(\operatorname {Comm}(P,T)=[P,T]\).

For each of the eleven registered occurrences (o), evaluation at level
(n) uses its own actor map, prefix, inverse convention and sign:

\[
 \operatorname {ev}_{n,o}:\mathcal I\longrightarrow D_{n,o},
 \qquad
 A_{n,o}(g)=P_{n,o}\rho_{n,o}(g)P_{n,o}^{-1}.              \tag{1.2}
\]

The physical block aggregation is applied only after these eleven
evaluations.  Thus a source actor is common as syntax, while its occurrence
actions need not be equal or even linearly identified.  In particular this
construction never exchanges

\[
 (p-1)\delta(a)\quad\hbox{with}\quad(a-1)\delta(p).         \tag{1.3}
\]

The crossed-Fox rule is evaluated in the order written in the tree.  The
connection term of v394 Theorem 1.1 is therefore retained automatically.

Assume the registered reductions preserve every named leaf and every tree
operation.  Then reduction of a tree evaluation equals evaluation of the
same tree after reduction:

\[
 r^D_{n,o}\operatorname {ev}_{n+1,o}(T)
 =\operatorname {ev}_{n,o}(T).                             \tag{1.4}
\]

Equation (1.4) follows by structural induction on (T).  It is the exact
semilinear replacement for v394's invalid common-action step.

## 2. The actual relative square

Let

\[
 B_n:D_n\longrightarrow L_n                                  \tag{2.1}
\]

be the actual first-difference operator: evaluate all eleven occurrences,
retain their individual actor paths, and then apply the registered H1, H2
and pentagon aggregation and boundary localization.  The same-owner
condition is precisely the commutative square

\[
 \boxed{r^L_nB_{n+1}=B_nr^D_n.}                              \tag{2.2}
\]

For a desired compatible residual (t=(t_n)), require

\[
 r^L_nt_{n+1}=t_n.                                           \tag{2.3}
\]

Put

\[
 K^D_n=\ker r^D_n,
 \qquad K^L_n=\ker r^L_n.                                   \tag{2.4}
\]

By (2.2), (B_{n+1}(K^D_n)\subseteq K^L_n).  This inclusion is
formal; the reverse inclusion is the substantive relative-kernel gate.

## 3. Exact one-step lifting lemma

### Theorem 3.1 (ONE-STEP ACTUAL LIFT)

Suppose (c_n\in D_n) satisfies (B_nc_n=t_n), and choose any legal lift
(\widetilde c_{n+1}\in D_{n+1}) with
(r^D_n\widetilde c_{n+1}=c_n).  Define its fine-level defect by

\[
 \beta_{n+1}=t_{n+1}-B_{n+1}\widetilde c_{n+1}.              \tag{3.1}
\]

Then \(\beta_{n+1}\in K^L_n\).  Moreover the following are equivalent:

1. there is (c_{n+1}\in D_{n+1}) with
   (r^D_nc_{n+1}=c_n) and (B_{n+1}c_{n+1}=t_{n+1});
2. \(\beta_{n+1}\in B_{n+1}(K^D_n)\).

If (h_n:K^L_n\to K^D_n) is a right inverse of the restricted map,

\[
 B_{n+1}h_n=\operatorname {id}_{K^L_n},                    \tag{3.2}
\]

then an explicit lift is

\[
 \boxed{c_{n+1}=\widetilde c_{n+1}+h_n(\beta_{n+1}).}       \tag{3.3}
\]

#### Proof

Equations (2.2), (2.3), and (B_nc_n=t_n) give

\[
 r^L_n\beta_{n+1}
 =t_n-B_nr^D_n\widetilde c_{n+1}=0,
\]

so \(\beta_{n+1}\in K^L_n\).  If (c_{n+1}) exists, then
(k=c_{n+1}-\widetilde c_{n+1}\) belongs to (K^D_n) and
(B_{n+1}k=\beta_{n+1}).  Conversely, any such (k) makes
(c_{n+1}=\widetilde c_{n+1}+k) satisfy both required equations.
Equation (3.3) is this construction with (k=h_n(\beta_{n+1})\). \(\square\)

### Corollary 3.2 (UNIVERSAL ONE-STEP CRITERION)

Every lower solution and every compatible fine target lift across this
edge can be lifted if and only if

\[
 \boxed{B_{n+1}(K^D_n)=K^L_n,}                              \tag{3.4}
\]

provided (r^D_n) is onto on the legal source.  Over the finite
(\mathbf F_3\)-spaces in the registered elementary-abelian layer, (3.4)
is equivalent to a finite rank test.  Once it holds, Gaussian elimination
on word-bearing instruction columns supplies a right inverse (h_n) and
hence the literal ancestry in (3.3).

The equality in (3.4), not mere endpoint surjectivity of (B_{n+1}), is
the precise content of the proposed relative-dihedral successor theorem.

## 4. All cofinal levels

### Theorem 4.1 (RECURSIVE COHERENT SELECTOR)

Assume:

1. (c_0\in D_0) satisfies (B_0c_0=t_0);
2. every (r^D_n) is onto on the legal source;
3. (2.2) holds at every edge; and
4. for every (n), (3.4) holds with a fixed word-bearing right inverse
   (h_n).

Choose fixed legal sections (s_n:D_n\to D_{n+1}) of (r^D_n).  Recursively
set

\[
 \begin{aligned}
 \widetilde c_{n+1}&=s_n(c_n),\\
 \beta_{n+1}&=t_{n+1}-B_{n+1}\widetilde c_{n+1},\\
 c_{n+1}&=\widetilde c_{n+1}+h_n(\beta_{n+1}).               \tag{4.1}
 \end{aligned}
\]

Then (r^D_nc_{n+1}=c_n) and (B_nc_n=t_n) for every (n).  Hence
(c_\infty=(c_n)) is one coherent correction in the inverse limit.  No
independent choice of unrelated finite-stage corrections and no appeal to
measure theory is required.

#### Proof

Theorem 3.1 gives the two assertions at (n+1) from those at (n).
Induction constructs the coherent sequence.  The inverse-limit assertion
is its definition. \(\square\)

This is an explicit algorithm after the matrices and word-bearing right
inverses are known.  It is not yet a closed formula uniform in an
unspecified tower: the family (h_n) is exactly what the actual relative
kernel computation must supply.

## 5. Instruction-tree certificate and the actual finite gate

At an adjacent pair of actual finite levels, a certificate for (3.4)
consists of:

1. word-bearing bases of (K^D_n) and (K^L_n);
2. for every source basis word, its eleven occurrence instruction paths;
3. the exact matrix of (B_{n+1}|_{K^D_n}), obtained by literal Fox replay;
4. a pivot expression for every basis vector of (K^L_n); and
5. independent replay of the reduction square (2.2) and all side gates.

The actor-path tree is essential in items 2--3.  Occurrence (o) reads the
same source instruction with its own (A_{n,o}); no column is copied from
one occurrence by pretending that all actions are common.  Likewise the
commutator node directly evaluates

\[
 \delta([p,a])=(p-1)\delta(a)
 +(1-pap^{-1})\delta(p)+(1-[p,a])\delta(a),                  \tag{5.1}
\]

so the field-outer/return-even connection survivor is included in the
ordinary image test rather than discarded by a dihedral antisymmetrizer.

For a particular compatible class (t), universal equality (3.4) can be
weakened to the class-specific test

\[
 \boxed{\beta_{n+1}\in B_{n+1}(K^D_n)}                     \tag{5.2}
\]

at every edge.  This is the smaller route relevant to
(\chi_{07}=[x,y][y,z]^{-1}): only its actual recursively produced defects
must be solved.  A failure of (3.4) outside that defect orbit does not block
the class-specific lift.

## 6. Relation to v220

This note closes the logical form of the missing successor implication:

\[
 \text{one accepted stage}
 \quad+\quad
 \text{actual relative-kernel equality at every edge}
 \quad\Longrightarrow\quad
 \text{one coherent all-stage lift}.                        \tag{6.1}
\]

It also proves that the correct computation is the restricted map
(B_{n+1}|_{K^D_n}) with occurrence instruction paths.  It does not prove
the actual equalities (3.4).  In the v220 ledger:

```text
A0 initial actual word:                           STILL 0/1 UNKNOWN_RESOURCE
A4 word-bearing relative source/kernel data:      STILL 1/3 UNKNOWN_RESOURCE
A9 abstract one-step criterion and recursion:     PAPER CLOSED BY v395
A9 actual relative-kernel equality/right lifts:   STILL 0/3 ACTUAL
FAKE / IHARA WITNESS:                             NOT CONSTRUCTED
```

The next mathematical/mechanical interface is therefore unambiguous.  A0
must provide the initial word; A4 and the adjacent-level owner must emit the
word-bearing bases in Section 5; then (3.4), or only (5.2) for the actual
(\chi_{07}) defect, is the finite test that either returns the next
explicit correction or returns a genuine obstruction certificate.

`R07_INSTRUCTION_TREE_RELATIVE_LAYER_LIFT_V395_PAPER_GRADE`

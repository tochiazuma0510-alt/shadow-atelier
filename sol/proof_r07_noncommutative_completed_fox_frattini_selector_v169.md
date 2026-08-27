# R07 noncommutative completed-Fox Frattini selector v169

Author: Sol / 2026-08-27

Status: paper theorem.  V168 constructs every genuine relative Frattini
successor from one fixed presentation.  This note passes those compatible
finite Fox complexes to the full noncommutative completed group algebra.  It
proves that solvability at every finite level already gives one compatible
completed coefficient, even if the finite solutions were found
independently.  No cyclic deck character, PID, or Smith form is required for
that compactness statement.  The note does not prove finite-level
solvability from one first-rung success, does not compute the actual
return-even completed membership, and does not declare a fake/Ihara witness.

## 1. The fixed-p completed presentation complex

Fix a prime \(p\), one exact finite presentation

\[
 P=\langle x_1,\ldots,x_d\mid r_1,\ldots,r_s\rangle,
\tag{1.1}
\]

and the relative Frattini tower

\[
 K_{n+1}=\Phi_p(K_n),
 \qquad E_n=P/K_n,
 \qquad E_{n+1}\twoheadrightarrow E_n.
\tag{1.2}
\]

Put

\[
 \Lambda_n=\mathbf F_p[E_n],
 \qquad
 \Lambda=\varprojlim_n\Lambda_n.
\tag{1.3}
\]

The ring \(\Lambda\) is the completed group algebra for this marked inverse
system.  It need not be commutative.  The quotient maps in (1.2) induce
surjective ring maps \(\Lambda_{n+1}\to\Lambda_n\).

Evaluate the same Fox derivatives of the fixed relators at every level:

\[
 \Lambda_n^s\xrightarrow{D_{2,n}}
 \Lambda_n^d\xrightarrow{D_{1,n}}\Lambda_n.
\tag{1.4}
\]

The entries of \(D_{2,n}\) are the complete translated-boundary templates;
the entries of \(D_{1,n}\) are the marked generator-minus-identity terms,
with the convention fixed by v168 equation (1.3).

### Proposition 1.1 (ONE COMPLETED FOX TEMPLATE)

The matrices in (1.4) reduce entrywise along the tower and therefore define
continuous matrices

\[
 \boxed{
 \Lambda^s\xrightarrow{D_{2,\infty}}
 \Lambda^d\xrightarrow{D_{1,\infty}}\Lambda.}
\tag{1.5}
\]

Every finite matrix (1.4) is the corresponding reduction of (1.5), and

\[
 D_{1,\infty}D_{2,\infty}=0.
\tag{1.6}
\]

#### Proof

Each matrix entry is the evaluation of one fixed integral Fox derivative.
Word evaluation and Fox derivatives commute with a marked quotient.  Hence
the entries are compatible and define (1.5).  The finite cellular identity
\(D_{1,n}D_{2,n}=0\) holds at every level, so separatedness of the inverse
limit gives (1.6). \(\square\)

This is a full-deck, noncommutative template.  It is not the cyclic
\(\mathbf F_p[[T]]\) template of v133/v164, and it supplies no Smith normal
form.

## 2. Complete boundary membership needs no compatible finite choices

Let \(z=(z_n)\in\varprojlim_n\Lambda_n^d\) be compatible.

### Theorem 2.1 (COMPACT COMPLETE-BOUNDARY SELECTOR)

The following are equivalent:

1. \(z_n\in\operatorname{im}D_{2,n}\) for every \(n\);
2. there is one completed coefficient
   \(a_\infty\in\Lambda^s\) such that

   \[
   \boxed{D_{2,\infty}a_\infty=z;}
   \tag{2.1}
   \]

3. there is a compatible family \(a_n\in\Lambda_n^s\) satisfying
   \(D_{2,n}a_n=z_n\) at every level.

The choices witnessing item 1 may be unrelated.

#### Proof

Items 2 and 3 are equivalent by the definition of the inverse limit, and
either implies item 1.  Assume item 1.  The compact profinite space
\(\Lambda^s\) projects onto every finite \(\Lambda_n^s\).  Let

\[
 C_n=\{a\in\Lambda^s:
       D_{2,n}(a\bmod n)=z_n\}.
\tag{2.2}
\]

Each \(C_n\) is nonempty and closed.  Compatibility of the matrices and
targets gives \(C_{n+1}\subseteq C_n\).  Compactness gives
\(\bigcap_nC_n\ne\varnothing\).  Any element of the intersection satisfies
(2.1). \(\square\)

Equivalently, the image of the continuous map \(D_{2,\infty}\) is compact
and hence closed; finite membership of every reduction is exactly completed
membership.  No commutativity, Noetherian hypothesis, or finite-level
surjectivity of the solution-set transitions was used.

The theorem applies verbatim to any compatible matrix

\[
 B_n:A_n\longrightarrow Z_n
\tag{2.3}
\]

obtained by reducing one continuous map between finite products of completed
group algebras, provided the completed source projects onto every displayed
finite source.  For a source defined as a kernel whose transition maps need
not be onto, use the finite-free augmented formulation in Section 3.

## 3. The fixed R07 all-seven template

For R07, apply Section 1 separately to the exact PB3 and PB4 presentations.
The source word lies in \(F(x,y)\), while the six hexagon occurrences and
five printed-order pentagon occurrences are induced by eleven fixed word
substitutions

\[
 F(x,y)\longrightarrow P_3\quad\text{or}\quad P_4.
\tag{3.1}
\]

The Fox chain rule sends every source one-chain through these substitutions,
and the fixed coarse prefixes give the exact left transports.  Therefore the
eleven-slot map at level \(n\), with the two PB3 blocks and PB4 block kept
disjoint,

\[
 B_n:A_n\longrightarrow Z_n,
\tag{3.2}
\]

is the reduction of one continuous multi-sorted map

\[
 \boxed{B_\infty:A_\infty\longrightarrow Z_\infty.}
\tag{3.3}
\]

More precisely, take a finite product \(\widetilde A_\infty\) of completed
free modules large enough for the two-generator source Fox chains and every
typed occurrence.  Let

\[
 G_\infty:\widetilde A_\infty\longrightarrow Y_\infty,
 \qquad A_\infty=\ker G_\infty
\tag{3.3a}
\]

encode the source-cycle, common-value, and linear side-domain equations.
At level \(n\), define \(A_n=\ker G_n\), where \(G_n\) is the reduction of
the same finite template.  This finite-free ambient presentation is
load-bearing: no surjectivity of the transition maps \(A_{n+1}\to A_n\) is
assumed.  Define \(Z_\infty=\varprojlim_n Z_n\), where each \(Z_n\) is the
block-tagged quotient by the two finite PB3 boundary maps and the finite PB4
boundary map.  Theorem 2.1 supplies compatible boundary coefficients
whenever a compatible representative is zero in every \(Z_n\).

### Theorem 3.1 (NONCOMMUTATIVE ALL-SEVEN BASE CHANGE)

Assume the exact PB presentations and all eleven literal substitutions are
fixed, and authenticate that every arity/deletion map sends the complete
source relator normal closure into the complete target relator normal
closure.  Then:

1. the maps (3.2) commute with every Frattini reduction;
2. the actual defects of one compatible partial word form
   \(\beta=(\beta_n)\in Z_\infty\); and
3. if

   \[
   -\beta_n\in B_n(A_n)
   \quad\text{for every }n,
   \tag{3.4}
   \]

   then there is one compatible completed coefficient

   \[
   \boxed{a_\infty\in A_\infty,
          \qquad B_\infty a_\infty=-\beta.}
   \tag{3.5}
   \]

#### Proof

The Fox chain rule and v168 Proposition 3.2 prove item 1.  Each defect is the
evaluation of the same three literal relation words, so quotient naturality
proves item 2.  For item 3, work in the finite-free source
\(\widetilde A_\infty\) and apply Theorem 2.1 to the augmented map

\[
 \widetilde A_\infty\longrightarrow Z_\infty\oplus Y_\infty,
 \qquad a\longmapsto(B_\infty a,G_\infty a),
\tag{3.6}
\]

with target \((-\beta,0)\).  A finite solution of (3.4) in \(A_n\) is
exactly a finite solution of this augmented equation.  Compactness therefore
returns a completed solution satisfying both coordinates, hence an element
of \(A_\infty\). \(\square\)

The augmentation in (3.6) prevents an ambient chain with no actual
common-word class from being accepted.

Task189 correctly found that the current task179/task186 receipt does not
serialize a cyclic character, cyclic cell-orbit roster, or cyclic transition
map.  Theorem 3.1 does not contradict that audit.  It gives a different
future route: the full relative Frattini deck groups and fixed PB
presentations supply a noncommutative template.  A producer must still
serialize and independently check the presentation maps, eleven chain maps,
and every finite reduction square.

## 4. Word-bearing compactness and side gates

Linear module membership is not the whole witness condition.  Let
\(\mathcal S_n\) be the finite set of all **word-bearing** correction classes
at level \(n\) which:

1. lie in the registered common relative kernel;
2. kill the two hexagons and printed pentagon through that level;
3. have normalized exponent zero and admit the v157 exactification;
4. pass the registered marking, formation, onto, and settlement gates; and
5. reduce to the fixed earlier partial word.

Every finer accepted correction reduces to a coarser accepted correction.

### Theorem 4.1 (FINITE ACCEPTED SETS GIVE ONE COMPATIBLE PATH)

If \(\mathcal S_n\ne\varnothing\) for every \(n\), then

\[
 \boxed{\varprojlim_n\mathcal S_n\ne\varnothing.}
\tag{4.1}
\]

This remains true even if the separately found witnesses of nonemptiness are
not mutually compatible.

#### Proof

Make a rooted tree whose level-\(n\) vertices are the elements of
\(\mathcal S_n\), with an edge for reduction.  The tree is finitely
branching, every vertex has a finite ancestor chain, and there is a vertex at
every depth.  Koenig's lemma gives an infinite branch, which is (4.1).
\(\square\)

Theorem 4.1 is an existence selector.  For an explicit computable witness,
one still needs either:

1. the based terminating successor algorithm of v117/v168 at the actual
   state; or
2. one effective completed preimage certificate for (3.5), together with a
   word-bearing section and direct side-gate replay.

Thus compactness removes the **compatibility-choice** problem, not the
nonemptiness problem.

## 5. Relative dihedral plus the completed even class

Suppose \(p\) is odd and the return involution \(\theta\) acts continuously
on (3.3).  The idempotents

\[
 e_-=(1-\theta)/2,
 \qquad e_+=(1+\theta)/2
\tag{5.1}
\]

split the actual completed defect into return-odd and return-even parts.  On
the correctly typed odd part, v75 supplies the relative-dihedral preimage
\(h_-e_-\beta\).  The remaining equation is exactly one completed actual
class:

\[
 \boxed{B_\infty a_+=-e_+\beta.}
\tag{5.2}
\]

If (5.2) has a word-bearing admissible solution, then

\[
 a_\infty=-h_-e_-\beta+a_+
\tag{5.3}
\]

kills the complete abelian defect.  If every finite reduction of (5.2) is
soluble in the actual source module, Theorem 3.1 supplies a compatible
completed solution.  It does not supply an effective normal form for that
solution over the noncommutative ring.

This is the full-deck generalization of the cyclic/multicyclic split in
v133/v167:

\[
 \boxed{
 \text{relative-dihedral odd homotopy}
 \; + \;
 \text{one noncommutative completed actual-even membership}.}
\tag{5.4}
\]

It is invalid to replace the second term by \(1-\theta\), because that
operator is zero on the even part.

## 6. Mixed primes, computation, and speed

For the mixed-prime solvable-cofinal tower of v155 the coefficient fields
change with the rung, so one should not pretend that all edges are modules
over one \(\mathbf F_p\)-algebra.  The word-bearing finite-set theorem 4.1
still applies to the entire nested tower.  The completed group-algebra
theorems apply on every constant-prime lane or on any fixed-p subsequence
with its authenticated transition maps.  The nonabelian perfect core remains
a separately typed finite accepted-set gate.

V168 and the present note also give the correct computational division:

1. fixed relator words, eleven substitutions, Fox slot order, and chain-map
   identities are immutable templates and may be cached once;
2. finite group values, dual joins, and actual defects change with the rung
   and must be recomputed;
3. an affine prefix value in \(E_{n+1}\) is evaluated lazily from \(E_n\)
   with exact boundary equality, so a full Cayley table is unnecessary; and
4. completed compactness means compatible coefficients need not be found by
   backtracking through all earlier arbitrary finite choices.

Task190 and the versioned task191/task192 implementations address item 1 and
the repeated finite equality/correlation work.  They do not alter the
mathematical family scanned.

## 7. Exact advance and remaining boundary

The cyclic-character gate of v164 is not a prerequisite for the genuine
relative Frattini tower.  Fixed PB presentations give a full-deck
noncommutative completed Fox template, and compactness converts all-level
finite membership into one compatible coefficient.  The remaining witness
frontier is now exactly:

1. produce the exact task186 first word;
2. use v168 to compute the actual second-rung \(\beta_1\);
3. prove or compute the return-even membership (5.2), successively or in the
   completed module; and
4. prove nonempty accepted sets at every perfect-core edge.

One first-rung success does not imply item 3 at every later rung.  No theorem
in this note makes that inference.

```text
FIXED NONCOMMUTATIVE COMPLETED FOX COMPLEX:          PAPER_PROOF
ALL FINITE BOUNDARY MEMBERSHIPS => COMPLETED CHAIN: PAPER_PROOF
FULL-DECK ALL-SEVEN BASE CHANGE:                    PAPER_PROOF (TYPING GATE)
NONEMPTY FINITE ACCEPTED SETS => COMPATIBLE PATH:   PAPER_PROOF
DIHEDRAL-ODD + COMPLETED-EVEN REDUCTION:             PAPER_PROOF
CURRENT TASK179/186 TRANSITION RECEIPT:              NOT IMPLEMENTED
TASK186 EXACT FIRST WORD:                            GHA IN PROGRESS
SECOND-RUNG ACTUAL beta_1:                           NOT COMPUTED
RETURN-EVEN COMPLETED MEMBERSHIP:                    OPEN
PERFECT-CORE ACCEPTED SETS:                          OPEN
COMPATIBLE R07 LIFT / FAKE / IHARA WITNESS:         NOT DECLARED
```

`R07_NONCOMMUTATIVE_COMPLETED_FOX_FRATTINI_SELECTOR_V169_PAPER_GRADE`

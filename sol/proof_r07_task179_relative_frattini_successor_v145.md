# R07 task179 relative-Frattini successor and commutator exactification v145

Author: Sol / 2026-08-27

Status: paper theorem and successor contract.  This note identifies exactly
which rung a positive task179 receipt settles, proves that the resulting
relative Frattini tower is cofinal on the marked pro-3 lane, and isolates the
integer commutator gate which task179's two mod-3 exponent rows do not settle.
It does not assume that the running task179 production search succeeds.  It
does not prove the second-rung actual class vanishes, and it does not declare
a compatible cofinal lift, fake, or Ihara witness.

## 1. The two filtrations must not be confused

Let

\[
 P_r\twoheadrightarrow E_r,\qquad K_{r,0}=\ker(P_r\to E_r),
 \qquad r\in\{3,4\},
\tag{1.1}
\]

be the pinned marked PB3 and PB4 quotients used by task175/task179.  Define
the mod-3 Frattini operator on an arbitrary group by

\[
 \Phi_3(K)=K^3[K,K]
\tag{1.2}
\]

and recursively put

\[
 K_{r,n+1}=\Phi_3(K_{r,n}),\qquad
 E_{r,n}=P_r/K_{r,n}.
\tag{1.3}
\]

Thus \(E_{r,0}=E_r\), and

\[
 \ker(E_{r,n+1}\to E_{r,n})
 =K_{r,n}/K_{r,n+1}
 =H_1(K_{r,n};\mathbf F_3)
\tag{1.4}
\]

is elementary abelian.

This is not the Jennings truncation

\[
 \mathbf F_3[\Pi_4[3]]\longrightarrow
 \mathbf F_3[\Pi_4[3]]/I^j.
\tag{1.5}
\]

The calculations at \(j=9,10,11,12\) are projections and screens inside the
first relation-module calculation.  Increasing \(j\) does not move from
\(K_{4,n}\) to \(K_{4,n+1}\).  In particular, a full raw task179 positive
receipt supersedes those projected depths for the positive first-rung claim;
it does not settle the second Frattini rung.

## 2. Fox/D2 is the first relative Frattini quotient

Choose one of the exact marked presentations from v121 or v108,

\[
 P=\langle X\mid \mathcal R\rangle,
 \qquad P\twoheadrightarrow E,
 \qquad K=\ker(P\to E).
\tag{2.1}
\]

Let \(C_2\xrightarrow{D_2}C_1\xrightarrow{D_1}C_0\) be the cellular
chain complex over \(\mathbf F_3[E]\) of the corresponding covering of the
presentation complex.  The rows of \(D_2\) are exactly the translated Fox
rows of the complete presentation relators: two rows for PB3 and eleven rows
for PB4.

### Lemma 2.1 (RELATION-MODULE IDENTIFICATION)

For every word \(w\) whose value in \(P\) lies in \(K\), its raw Fox row
defines a class

\[
 [\nabla w]\in \ker D_1/\operatorname{im}D_2,
\tag{2.2}
\]

and the map

\[
 \boxed{
 K/K^3[K,K]\xrightarrow{\ \sim\ }
 \ker D_1/\operatorname{im}D_2,
 \qquad [w]\longmapsto[\nabla w]}
\tag{2.3}
\]

is an \(\mathbf F_3[E]\)-module isomorphism.  Consequently

\[
 \boxed{\nabla w\in\operatorname{im}D_2
 \quad\Longleftrightarrow\quad w\in\Phi_3(K).}
\tag{2.4}
\]

#### Proof

The covering presentation complex has fundamental group \(K\).  Its first
cellular homology over \(\mathbf F_3\) is therefore

\[
 H_1(K;\mathbf F_3)=K/K^3[K,K].
\tag{2.5}
\]

The same homology is computed by
\(\ker D_1/\operatorname{im}D_2\).  The cellular edge path of a word is its
Fox one-chain, which gives (2.3).  No asphericity assumption is needed for
first homology.  The presentations being exact is load-bearing: omitting a
PB relator enlarges the right side of (2.3).  Equation (2.4) is the zero-class
criterion. \(\square\)

### Theorem 2.2 (WHAT A TASK179 COMMON WORD SETTLES)

Assume the helper-nonshared checker accepts a task179 `COMMON_WORD` receipt,
and write

\[
 f^{(1)}=g_{760}c_0
\tag{2.6}
\]

for its displayed right-corrected word.  Then both hexagon relation words of
\(f^{(1)}\) lie in \(K_{3,1}=\Phi_3(K_{3,0})\), and its printed-order
pentagon relation word lies in \(K_{4,1}=\Phi_3(K_{4,0})\).  Equivalently,
the same word satisfies the two hexagons and the pentagon in

\[
 \boxed{E_{3,1}=P_3/K_{3,1},\qquad
        E_{4,1}=P_4/K_{4,1}.}
\tag{2.7}
\]

Thus task179 is the first universal elementary-abelian relative lift above
the pinned \(E_3/E_4\) window, not merely a repetition of the level-zero
finite relation check.

#### Proof

The checker first proves that all three relation words have identity value in
the pinned \(E_3/E_4\) quotients, so they lie in the corresponding
\(K_{r,0}\).  Its separately block-tagged sparse equality says that each raw
Fox row is a linear combination of the complete translated PB presentation
rows.  Apply Lemma 2.1 in the two PB3 blocks and the PB4 block.  This puts the
three relation words in \(K_{r,1}\), which is exactly the identity condition
in (2.7). \(\square\)

The boundary chains in the task179 receipt are cellular two-chains used in
this proof.  They are not source correction words and are not multiplied into
\(c_0\).

## 3. The exact exponent gate left by task179

Task179 appends two rows in \(\mathbf F_3\).  Its function
`exponent_pair` reduces both signed exponent sums modulo three.  Hence a
positive receipt proves only

\[
 \operatorname{exp}(c_0)\in3\mathbf Z^2,
\tag{3.1}
\]

not \(\operatorname{exp}(c_0)=0\).  Since \(g_{760}\in[F_2,F_2]\), raw
charmingness is preserved exactly when the chosen correction is also in
\([F_2,F_2]\).

Let \(\Omega\) be task179's registered joint finite-value kernel and let

\[
 \overline{\mathscr V}:\Omega\longrightarrow Z_0/D_0
\tag{3.2}
\]

be the additive all-seven change map.  Put

\[
 z_0=-[T_0],\qquad
 S=\overline{\mathscr V}^{-1}(z_0),\qquad
 H=\ker\overline{\mathscr V}.
\tag{3.3}
\]

The accepted correction \(c_0\) belongs to \(S\).

### Theorem 3.1 (COMMUTATOR EXACTIFICATION IN THE SAME FIBRE)

The complete first-rung solution fibre is the right coset

\[
 \boxed{S=c_0H.}
\tag{3.4}
\]

There is a correction in the same task179 fibre which preserves raw
charmingness if and only if

\[
 \boxed{-\operatorname{exp}(c_0)\in
        L_H:=\operatorname{exp}(H)\leq\mathbf Z^2.}
\tag{3.5}
\]

If a word \(h\in H\) with
\(\operatorname{exp}(h)=-\operatorname{exp}(c_0)\) is returned, then

\[
 \boxed{c_0^{\rm com}=c_0h}
\tag{3.6}
\]

has zero exact exponent vector and gives the same first-rung relation-module
solution as \(c_0\).

#### Proof

Additivity of (3.2) gives
\(\overline{\mathscr V}(c_0h)=z_0\) exactly for \(h\in H\), proving
(3.4).  Exponent sums are additive in \(F_2\), so (3.6) has zero exponent
vector exactly under (3.5). \(\square\)

The lattice in (3.5) is computable without guessing kernel words.  The
kernel \(H\) is normal in \(F_2\): the joint-value kernel is normal and the
zero fibre of the equivariant relation-module map is stable under
conjugation.  Moreover \(F_2/H\) is finite because both the joint image and
the relation-module image are finite.  V92 therefore gives

\[
 \boxed{L_H=\ker\bigl(\mathbf Z^2\to(F_2/H)^{\rm ab}\bigr).}
\tag{3.7}
\]

Thus (3.5) is a rank-two Smith/lattice membership test.  If the literal
task179 correction already has exponent vector \((0,0)\), this entire gate
closes with \(h=1\).  If it does not, its mod-3 zero is not a substitute for
(3.5).

## 4. Cofinality of the iterated relative Frattini tower

### Theorem 4.1 (RELATIVE FRATTINI COFINALITY)

Let \(P\) be finitely generated, let \(K\triangleleft P\) have finite
index, and put \(K_0=K\), \(K_{n+1}=\Phi_3(K_n)\).  Then:

1. every \(P/K_n\) is finite;
2. every transition kernel \(K_n/K_{n+1}\) is a finite elementary abelian
   3-group; and
3. the tower \((P/K_n)_n\) is cofinal among finite quotients \(P/N\) which
   map to \(P/K\) and whose relative kernel \(K/N\) is a 3-group.

#### Proof

By Schreier, \(K_n\) is finitely generated whenever it has finite index.
Its mod-3 Frattini quotient is therefore finite elementary abelian, proving
1 and 2 inductively.

For 3, let \(N\triangleleft P\), \(N\leq K\), and suppose \(K/N\) is a
finite 3-group.  The image of \(K_n\) in \(K/N\) is the \(n\)-fold
Frattini iterate of that finite 3-group, because a surjection commutes with
\(G\mapsto G^3[G,G]\).  The Frattini iterates of a finite 3-group eventually
reach one.  Hence \(K_n\leq N\) for some \(n\), so \(P/K_n\) maps onto
\(P/N\). \(\square\)

### Corollary 4.2 (MATCHED DIAGRAM TOWER)

Every registered coface, deletion, or marking homomorphism which maps
\(K_{r,0}\) into the appropriate target kernel maps \(K_{r,n}\) into the
corresponding \(K_{s,n}\) for all \(n\).  Hence (1.3) forms a matched
arity-3/4 diagram tower.  For any finite collection of relative marked
3-group diagram quotients, one common sufficiently large \(n\) dominates all
components.

#### Proof

Every homomorphism sends cubes to cubes and commutators to commutators, so
it sends \(\Phi_3(K)\) into \(\Phi_3(L)\).  Induction gives functoriality at
all depths.  Apply Theorem 4.1 componentwise and take the maximum of the
finitely many required depths. \(\square\)

This proves a concrete cofinal pro-3 ladder.  It does not make that ladder
cofinal among refinements introducing new prime-to-3 or nonabelian simple
factors; those remain separately typed gates.

## 5. The actual second rung

Assume task179 succeeds and, when necessary, Theorem 3.1 returns
\(c_0^{\rm com}\).  Put

\[
 f^{(1)}=g_{760}c_0^{\rm com}.
\tag{5.1}
\]

At the next edge, evaluate the two hexagon words and the printed pentagon
word of \(f^{(1)}\) in

\[
 V_{3,1}=K_{3,1}/K_{3,2},\qquad
 V_{4,1}=K_{4,1}/K_{4,2}.
\tag{5.2}
\]

Their block-tagged tuple is the named second-rung defect \(\beta_1\).
Let \(U_1^{\rm com}\) be the actual common source-word domain consisting of
commutator words whose ten registered occurrence values lie in the relevant
\(K_{r,1}\).  Linearization modulo \(K_{r,2}\) gives a finite
\(\mathbf F_3\)-linear map

\[
 B_1:A_1\longrightarrow Z_1,
\tag{5.3}
\]

where every element of \(A_1\) retains a word in \(U_1^{\rm com}\), and
\(Z_1\) is the separately tagged sum of the modules in (5.2).

The next exact question is

\[
 \boxed{-\beta_1\in\operatorname{im}B_1.}
\tag{5.4}
\]

A positive word-bearing preimage \(c_1\) makes
\(f^{(2)}=f^{(1)}c_1\) satisfy the relations through the second rung and
reduces to \(f^{(1)}\).  Recursively, the same construction at rung \(n\)
uses

\[
 V_{r,n}=K_{r,n}/K_{r,n+1},\qquad
 c_n\in U_n^{\rm com},\qquad
 B_n[c_n]=-\beta_n.
\tag{5.5}
\]

Because later correction words are invisible in every earlier quotient,
the partial words are automatically compatible.  Theorem 4.1 makes their
product converge on the relative pro-3 lane.  This is the concrete tower to
which v98 and the abstract v129/v126/v127 selectors apply.

The augmented equation

\[
 e=Bd+\rho z
\tag{5.6}
\]

is a compression of (5.4) when a genuine context-transition ideal and its
word-bearing kernel module have been authenticated.  It is not an extra
post-processing step from Jennings depth 9 to depth 29 after a full raw
task179 receipt.  The first nontrivial use of (5.6) is the actual transition
\(E_{r,2}\to E_{r,1}\), or another explicitly registered finer context.

## 6. Uniform relative-dihedral target

Let \(B_\infty:A_\infty\to Z_\infty\) denote the inverse limit of the actual
maps (5.3) on the tower of Section 4.  A single all-rung selector is a
continuous filtration-preserving map on the orbit of the actual defects,

\[
 h:\langle\beta_1,\beta_2,\ldots\rangle_{\rm act}
   \longrightarrow A_\infty,
 \qquad B_\infty h=1.
\tag{6.1}
\]

Return-odd classes may use the established relative-dihedral
antisymmetrizer.  Return-even field-outer classes require a second
class-specific inverse; pretending that \(1-\theta\) is onto there is
invalid.  Equivalently, one may solve the completed augmented map and prove
that its right inverse preserves the Frattini filtration.  Once (6.1) is
constructed, the corrections in (5.5) are its reductions, so compatibility
is built in rather than chosen after separate finite searches.

The new information supplied here is that the modules in (6.1) are not an
unspecified sequence of windows: they are the explicit iterated kernels
(1.3), and task179—if positive—supplies exactly their zeroth-to-first base
point.  What remains mathematical is the actual return-even inverse on this
tower, not another computation of the projected \(j=9\) family.

## 7. Successor receipt

After a positive task179 production receipt, the next consumer must execute
in this order.

1. Recompute the **integer** exponent vector of `correction_word` without
   reduction modulo three.
2. If it is nonzero, construct the homogeneous fibre kernel \(H\), compute
   (3.7), test (3.5), materialize \(h\), and directly replay
   \(c_0^{\rm com}\).  Failure of a bounded search is `UNKNOWN`; a complete
   lattice nonmembership kills this task179 solution fibre as a charming
   lift but not every possible coarse base.
3. Authenticate the relation-module interpretation (2.3) for all three
   block tags and record that the common word lives in (2.7).
4. Build the second relative Frattini quotients and the actual defect
   \(\beta_1\) of (5.2), retaining literal word provenance.
5. Run the positive word-bearing solve (5.4), or an authenticated v129
   augmented compression of the same typed map.
6. Only after a positive second-rung replay attempt the completed natural
   selector (6.1); keep prime-to-3/nonabelian accepted sets separate.

```text
TASK179 RAW FOX/D2 -> FIRST RELATIVE FRATTINI RUNG: PAPER_PROOF
ITERATED RELATIVE FRATTINI COFINALITY (PRO-3 LANE): PAPER_PROOF
j=9--12 VS FRATTINI-RUNG SEPARATION:               PAPER_PROOF
MOD-3 EXPONENT ROWS -> EXACT COMMUTATOR:            NOT AUTOMATIC
SAME-FIBRE COMMUTATOR CRITERION / LATTICE:           PAPER_PROOF
TASK179 COMMON_WORD PRODUCTION RECEIPT:              RUNNING / NOT ASSUMED
TASK179 CORRECTION INTEGER EXPONENT:                 NOT YET KNOWN
SECOND-RUNG ACTUAL DEFECT beta_1:                    NOT COMPUTED
SECOND-RUNG WORD-BEARING PREIMAGE:                   NOT COMPUTED
RETURN-EVEN COMPLETED HOMOTOPY:                      OPEN
COMPATIBLE COFINAL R07 LIFT / FAKE / IHARA WITNESS: NOT DECLARED
```

`R07_TASK179_RELATIVE_FRATTINI_SUCCESSOR_V145_PAPER_GRADE`

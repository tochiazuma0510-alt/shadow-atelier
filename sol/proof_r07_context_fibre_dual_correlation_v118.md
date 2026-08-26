# R07 context-fibre dual correlation v118

Author: Sol / 2026-08-27

Status: exact finite-support theorem for correlating a dual functional with
the full target6 correction orbit without blindly enumerating the whole
simultaneous context image.  It generalizes the task-157eg full-D2 support
correlation from one regular action to several linked context projections.
It is an algorithmic reduction; the required fibres and union coverage have
not yet been computed.  No correction, cofinal lift, fake, or Ihara witness
is declared.

## 1. Linked context action

Let

\[
 \Delta\leq G_1\times\cdots\times G_s
\tag{1.1}
\]

be the finite image of the source free group in the ordered tuple of all
context values used by one relation block.  Write
\(\pi_i:\Delta\to G_i\) for the coordinate projections.  The point of
(1.1) is that the coordinates are linked: replacing \(\Delta\) by the full
direct product would enlarge the correction image unsoundly.

Let the raw residual module have a basis indexed by a block/component label
\(b\) and a group element \(g\) in the corresponding output group.  For one
normal-generator word \(r\), its correction-orbit column has the form

\[
 V_r(\delta)=
 \kappa(r)+
 \sum_{o\in\mathcal O_r}
 a_o e_{b_o,L_o\pi_{i_o}(\delta)h_o},
 \qquad \delta\in\Delta.
\tag{1.2}
\]

Here \(\mathcal O_r\) is the finite list of literal Fox occurrences,
\(a_o\in\mathbf F_3^\times\), \(h_o\) is the unshifted Fox group value, and
\(L_o\) is the fixed prefix transport.  The term \(\kappa(r)\) collects
coordinates invariant under conjugation, such as the two exponent sums.
For target6, (1.2) is exactly the three-slot formula authenticated by task
172.  For the v110 stack the block tag \(b_o\) also records H1, H2 or the
ordered pentagon block.

Let \(\lambda\) be a dual functional.  Store its nonzero variable support as

\[
 S_\lambda=\{(b,g,\lambda_{b,g}):\lambda_{b,g}\neq0\}
\tag{1.3}
\]

and put

\[
 K_r=\langle\lambda,\kappa(r)\rangle,
 \qquad
 F_r(\delta)=\langle\lambda,V_r(\delta)\rangle.
\tag{1.4}
\]

## 2. Support-pinned fibres

For an occurrence \(o\) and a same-block support point \((b_o,g)\), define

\[
 t(o,g)=L_o^{-1}g h_o^{-1}\in G_{i_o}.
\tag{2.1}
\]

Only targets which lie in \(\operatorname{im}\pi_{i_o}\) contribute.  Define
the support-pinned union

\[
 U_r(\lambda)=
 \bigcup_{\substack{o\in\mathcal O_r\\(b_o,g)\in S_\lambda}}
 \pi_{i_o}^{-1}(t(o,g))\subseteq\Delta.
\tag{2.2}
\]

Every nonempty set in (2.2) is a coset of \(\ker\pi_{i_o}\).  A computation
must retain a section word for each enumerated \(\delta\), not merely its
tuple of values, because a positive column must materialize the actual word
\(u_\delta r u_\delta^{-1}\).

### Theorem 2.1 (CONTEXT-FIBRE SUPPORT EXHAUSTION)

For every \(\delta\notin U_r(\lambda)\),

\[
 \boxed{F_r(\delta)=K_r.}
\tag{2.3}
\]

Consequently the following procedure determines the complete nonzero
correlation set of \(F_r\).

1. Enumerate the distinct elements of the nonempty fibres in (2.2), with
   exact deduplication in \(\Delta\), and evaluate the complete sum (1.4) on
   every element.
2. Decide whether their union is all of \(\Delta\).
3. If the complement is nonempty, its value is the single constant \(K_r\).
   Thus it contributes nothing when \(K_r=0\); when \(K_r\neq0\), one
   authenticated complement representative is already an ACTIVE column, and
   every complement element has the same dual value.

#### Proof

Fix \(\delta\notin U_r(\lambda)\).  If the occurrence indexed by \(o\)
paired nontrivially with \(\lambda\), then for some same-block support point
\((b_o,g)\) one would have

\[
 L_o\pi_{i_o}(\delta)h_o=g.
\]

Solving this equality gives \(\pi_{i_o}(\delta)=t(o,g)\), hence
\(\delta\in U_r(\lambda)\), a contradiction.  Every variable occurrence in
(1.2) therefore pairs to zero, leaving only \(K_r\).  The three steps are an
immediate partition of \(\Delta\) into \(U_r(\lambda)\) and its complement.
\(\square\)

The final complement test is load-bearing when exponent coordinates are
appended.  Ignoring it would miss an ACTIVE column whose variable Fox terms
all avoid the support but whose constant exponent pairing is nonzero.

## 3. Exact fibre implementation

For a nonempty fibre choose \(d\in\Delta\) with \(\pi_i(d)=t\).  Then

\[
 \pi_i^{-1}(t)=d\ker\pi_i.
\tag{3.1}
\]

Thus the required primitive is not enumeration of \(\Delta\), but the
following typed data for every distinct context projection:

```text
image membership and a section for t
a finite representation of ker(pi_i)
coset enumeration, or a certified smaller correlation routine on the coset
exact union cardinality / coverage and one complement section when needed.
```

If a fibre itself is too large to enumerate, Theorem 2.1 remains exact but
does not by itself solve the resource problem.  One may recursively apply the
same support argument to a subgroup chain inside \(\ker\pi_i\), provided the
linked values in every remaining context are retained.  A cap hit is
`UNKNOWN_RESOURCE`, never a zero-correlation theorem.

For each scanned \(\delta\), compute \(F_r(\delta)\) from the entire
occurrence list.  Individual nonzero summands may cancel, so emitting one
candidate per support pair without accumulation is unsound.

## 4. Relation to the old full-D2 correlation

For a PB4 boundary column there is one acting group \(G=E_4\), the projection
is the identity, \(K_r=0\), and every fibre in (2.2) is the singleton

\[
 \{g h^{-1}\}.
\tag{4.1}
\]

Theorem 2.1 then becomes exactly the task-157eg rule

\[
 t=g h^{-1}.
\tag{4.2}
\]

Thus one dual-correlation engine may expose two separately typed families:

1. full \(E_4\)-left translates of the eleven exact PB4 D2 columns; and
2. linked \(\Delta\)-orbit columns of the 6,441 actual joint-kernel normal
   generators.

They may share sparse arithmetic, but their acting groups, sections and word
provenance must not be identified.

## 5. Terminating column generation

Start with any authenticated independent set of valid PB4 boundary and
correction-orbit columns.  Reduce the augmented target \((T_E,0,0)\).

- If it reduces to zero, recovery coefficients materialize one actual
  correction word and one PB4 boundary chain.
- Otherwise form the normalized separating dual \(\lambda\).
- Correlate \(\lambda\) exactly with the complete D2 family by (4.2) and with
  the complete correction family by Theorem 2.1.
- Add a canonical ACTIVE column or block and repeat.

Every ACTIVE column is outside the current span and therefore raises rank.
The ambient module is finite-dimensional, so the loop terminates after
finitely many successful additions.  If both complete correlations are zero
while \(\lambda(T_E,0,0)\neq0\), \(\lambda\) is an exact separator for the
pinned target6 system of v109.  A bounded correlation or incomplete fibre
coverage cannot produce that negative terminal.

### Corollary 5.1 (WORD-BEARING POSITIVE CERTIFICATE)

If target reduction reaches zero, every selected correction column has the
form

\[
 \Sigma_E(u_\delta r u_\delta^{-1}),
\]

with an authenticated source relation and section word.  Multiplying those
conjugate words with the recovered coefficients gives the explicit
registered-joint correction in v109 (4.4).  The two appended exponent
coordinates prove that its total exponent is zero modulo three.  Direct word
replay and the exact PB4 boundary reduction are still mandatory.

## 6. Next executable measurements

Before a full run, the bounded successor to task 172 must measure and pin:

1. the exact simultaneous target6 context image \(\Delta\), or a finite
   group representation sufficient for the projection-fibre operations;
2. \(|\operatorname{im}\pi_i|\), \(|\ker\pi_i|\), and the equality pattern
   among the three projections;
3. section-word caps for image targets, fibre elements and complement
   representatives;
4. the number and support distribution of the 6,441 unshifted correction
   columns; and
5. one exhaustive small nonabelian fixture where linked projections make the
   fibre union strictly smaller than the direct-product overapproximation.

These measurements select between direct orbit streaming and recursive
fibre correlation.  They do not change the mathematical universe.

```text
LINKED CONTEXT-FIBRE SUPPORT THEOREM:         PAPER_PROOF
EXPONENT-CONSTANT COMPLEMENT CASE:            PAPER_PROOF
OLD FULL-D2 CORRELATION AS SPECIAL CASE:      PAPER_PROOF
FINITE COLUMN-GENERATION TERMINATION:         PAPER_PROOF
TARGET6 CONTEXT PROJECTION FIBRES:            NOT YET COMPUTED
FULL CORRECTION-ORBIT CORRELATION:             NOT YET RUN
EXPLICIT FULL-E4 TARGET6 WORD:                NOT YET CONSTRUCTED
ALL-SEVEN COMMON WORD / COFINAL LIFT:         OPEN
FAKE / IHARA WITNESS:                         NOT DECLARED
```

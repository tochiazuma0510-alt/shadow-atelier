# R07 coarse-anchor multi-projection oracle v137

Author: Sol / 2026-08-27

Status: paper proof and exact production design.  This note supplies the
uniform simultaneous-fibre primitive left open in v134--v136.  It replaces a
fresh 1,469,664-state scan for every partial target by one coarse-coset index
and a 243-state Gamma lookup.  The coarse Gamma image is deliberately not
assumed trivial: it is nontrivial in the five E4 coordinates.  The actual
task176 bucket statistics and positive receipt are still pending.  No common
correction, cofinal lift, fake, or Ihara witness is declared.

## 1. Factored context maps

Use the authenticated extension

\[
 1\longrightarrow\Gamma\longrightarrow G
 \xrightarrow{\rho}Q_0\longrightarrow1,
 \qquad |\Gamma|=243.
\tag{1.1}
\]

For each of the ten typed contexts let

\[
 \Phi_i:G\longrightarrow E_i,
 \qquad c_i:E_i\longrightarrow \overline E_i
\tag{1.2}
\]

be evaluation and its coarse quotient, and write

\[
 \Psi_i=c_i\Phi_i,
 \qquad C_i=\Psi_i(\Gamma).
\tag{1.3}
\]

The group \(C_i\) is normal in \(\Psi_i(G)\).  A section value therefore
defines a well-defined quotient homomorphism

\[
 Q_0\longrightarrow \Psi_i(G)/C_i,
 \qquad q\longmapsto \Psi_i(s(q))C_i.
\tag{1.4}
\]

Changing \(s(q)\) multiplies its coarse value by an element of \(C_i\), so
the coset in (1.4), not the literal coarse value, is the invariant of \(q\).
This distinction is load-bearing.  The 243-state pinned receipt gives the
following candidate coarse-image orders for the selected coordinate order:

\[
 \boxed{(|C_0|,\ldots,|C_9|)=(1,1,1,1,1,81,81,81,9,9).}
\tag{1.5}
\]

The first five values use the v135 noncontiguous deletion.  The last five
come from E4 context IDs \((1,27,21,26,28)\).  Equation (1.5) is an exact
derivation from the cross-checked task157ee state table, but its independent
task176 replay is still pending; production must rebuild it literally.

Choose the frozen word-bearing section \(s:Q_0\to G\).  For a nonempty
ordered coordinate set \(S\), put

\[
 \Phi_S=(\Phi_i)_{i\in S},
 \qquad A_S=\Phi_S(\Gamma).
\tag{1.6}
\]

The literal Gamma table builds \(A_S\), every \(C_i\), a first source Gamma
state for each full value, and

\[
 |\Gamma_S^0|=
 |\ker(\Phi_S|_\Gamma)|=\frac{243}{|A_S|}
\tag{1.7}
\]

in at most 243 rows.

## 2. Coarse anchor buckets

Put

\[
 b_i(q)=\Psi_i(s(q)).
\tag{2.1}
\]

For an anchor \(a\in S\) and a coarse target \(u\in\overline E_a\), define

\[
 \boxed{B_a(u)=\{q\in Q_0:u\,b_a(q)^{-1}\in C_a\}.}
\tag{2.2}
\]

The task176 Q0 section roster evaluates \(\Phi_a(s(q))\) for every \(q\).
Thus one fixed-width index by the literal left coset \(C_a b_a(q)\)

```text
(coordinate, canonical C_i-coset key) -> ordered Q0 state IDs
```

constructs all buckets once.  For a query choose the anchor having the
smallest registered bucket; this choice affects runtime but not semantics.
Replacing (2.2) by literal coarse equality is unsound for coordinates
5--9, whose \(C_i\) are nontrivial by (1.5).

## 3. Uniform membership theorem

For a typed target tuple \(t=(t_i)_{i\in S}\in\prod_{i\in S}E_i\) and
\(q\in Q_0\), define the residual

\[
 r_S(q,t)=
 \bigl(t_i\Phi_i(s(q))^{-1}\bigr)_{i\in S}.
\tag{3.1}
\]

### Theorem 3.1 (COARSE-ANCHOR FIBRE TEST)

For every anchor \(a\in S\),

\[
 \boxed{
 t\in\Phi_S(G)
 \quad\Longleftrightarrow\quad
 \text{there exists }q\in B_a(c_a(t_a))
 \text{ with }r_S(q,t)\in A_S.}
\tag{3.2}
\]

If \(r_S(q,t)=\Phi_S(\gamma)\), then

\[
 \boxed{u_t=u_\gamma u_{s(q)}}
\tag{3.3}
\]

is an actual source word satisfying \(\Phi_S(u_t)=t\).

#### Proof

Suppose \(t=\Phi_S(g)\).  Write uniquely \(g=\gamma s(q)\) with
\(q=\rho(g)\) and \(\gamma\in\Gamma\).  Taking the anchor coarse part gives

\[
 c_a(t_a)b_a(q)^{-1}=\Psi_a(\gamma)\in C_a,
\tag{3.4}
\]

so \(q\in B_a(c_a(t_a))\).  Moreover

\[
 r_S(q,t)
 =\Phi_S(\gamma s(q))\Phi_S(s(q))^{-1}
 =\Phi_S(\gamma)\in A_S.
\tag{3.5}
\]

Conversely, if the right side of (3.2) holds, choose \(\gamma\) with
\(r_S(q,t)=\Phi_S(\gamma)\).  Rearranging (3.1) yields

\[
 t=\Phi_S(\gamma)\Phi_S(s(q))
  =\Phi_S(\gamma s(q)),
\tag{3.6}
\]

which proves membership and the word formula (3.3). \(\square\)

The test automatically checks every non-anchor coarse coordinate: the full
residual must equal one and the same authenticated Gamma state in every
coordinate.  Checking coordinatewise membership only in the separate
\(C_i\), or choosing different Gamma states in different coordinates, would
enlarge the linked image unsoundly.

## 4. Kernel order from the same oracle

Let

\[
 L_S=\{q\in Q_0:\Phi_S(s(q))^{-1}\in A_S\}.
\tag{4.1}
\]

This is v125's subgroup \(L_S\).  Theorem 3.1 applied to the identity target
shows that \(L_S\) is obtained by taking the thick anchor identity bucket
\(B_a(1)=\{q:b_a(q)^{-1}\in C_a\}\) and retaining precisely the Q0 states
whose full residual lies in \(A_S\).  Hence no all-Q0 scan is required unless
every available thick identity bucket is all of \(Q_0\).

V125 (3.5) and (1.7) give the exact projection-kernel order

\[
 \boxed{
 |\ker\Phi_S|=|L_S|\,|\Gamma_S^0|
 =|L_S|\frac{243}{|A_S|}.}
\tag{4.2}
\]

For any positive target, the set of successful Q0 states in (3.2) is one
coset of \(L_S\), and each successful state has exactly
\(|\Gamma_S^0|\) Gamma preimages.  Thus every nonempty fibre has the order
(4.2), as required by v134.

## 5. R07 production algorithm

For every subset \(S\) actually demanded by a cubic-moment expansion:

1. project the 243 authenticated Gamma rows to \(S\), build the exact
   `A_S` hash table and the coarse groups `C_i`, retain a first Gamma word,
   and compute (1.7);
2. choose an anchor using authenticated thick coset-bucket multiplicities;
3. compute \(L_S\) once from the anchor identity bucket and (4.1), then
   store (4.2);
4. for each target tuple, read only its anchor bucket, replay the section
   values for those Q0 state IDs, and test the residual key in `A_S`;
5. on the first hit emit the word (3.3), all ten direct values, and the
   fibre order; and
6. cache both positive and negative answers by the complete typed target
   tuple.

The one-time Q0 coarse index may be an outside-repository fixed-width sorted
file or mmap.  It need not store the full ten-coordinate section rows,
because task176's parent/letter roster and marked generator blobs reconstruct
them.  Resource termination before an anchor bucket or residual lookup is
complete is `UNKNOWN_RESOURCE`, never a negative membership answer.

The independent checker must rebuild (1.5), `A_S`, every used `C_i`, the
selected thick bucket, the residual, and the word replay.  Required semantic
mutations include a wrong coarse block, replacing a `C_i` coset by literal
equality, a wrong anchor bucket, wrong section side, a Gamma-state mismatch
across two coordinates, and a false bucket-empty negative.

## 6. Consequence for the common-word search

Combining this theorem with v134 and v136 gives a uniform exact linked-column
oracle:

\[
 \boxed{
 \text{at most 1536 partial targets per row}
 \;\xrightarrow{\text{Theorem 3.1}}\;
 \text{exact moment and a word-bearing ACTIVE column}.}
\tag{6.1}
\]

This closes the abstract membership-selector gap.  Its actual efficiency is
now governed by the measured maximum thick anchor-bucket multiplicities, not by
\(|\Delta|=357{,}128{,}352\) and not by a fresh \(|Q_0|\) scan per target.

```text
COARSE-COSET ANCHOR MEMBERSHIP EQUIVALENCE:   PAPER_PROOF
WORD-BEARING SECTION ON A POSITIVE QUERY:     PAPER_PROOF
KERNEL ORDER FROM IDENTITY BUCKET:            PAPER_PROOF
CUBIC-MOMENT TERM/INTEGER CAPS (v136):        PAPER_PROOF
PINNED GAMMA COARSE ORDERS (1,1,1,1,1,81,81,81,9,9): DERIVED / REPLAY PENDING
TASK176 THICK COSET-BUCKET STATISTICS:         PENDING
TASK177 PRODUCTION ORACLE IMPLEMENTATION:     NOT IMPLEMENTED
COMMON ALL-SEVEN CORRECTION WORD:             NOT CONSTRUCTED
COFINAL LIFT / FAKE / IHARA WITNESS:          NOT DECLARED
```

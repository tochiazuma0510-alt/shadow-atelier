# R07 all-seven extension-section orbit reduction v125

Author: Sol / 2026-08-27

Status: paper theorem and exact R07 specialization.  It replaces a blind
enumeration of the simultaneous H1/H2/pentagon context image by one scan of
the authenticated 1,469,664-element Q0 quotient and the 243-element Gamma
kernel.  It also produces the projection-kernel data needed by the v118 dual
fibre correlation.  The scan and all-seven orbit solve have not yet run.  No
correction, cofinal lift, fake, or Ihara witness is declared.

## 1. The actual ten-coordinate context map

Task157ee gives the authenticated extension

\[
 1\longrightarrow\Gamma\longrightarrow G
 \xrightarrow{\rho}Q_0\longrightarrow1,
\qquad
 |\Gamma|=243,
\qquad |Q_0|=1{,}469{,}664.
\tag{1.1}
\]

Here \(G\) is the marked joint image of \(F(x,y)\) in source E3 and all 31
registered E4 contexts.  V122 proves that fourth-strand deletion

\[
 d_E:E_4\longrightarrow E_3
\tag{1.2}
\]

maps registry rows 21--25 to the five source pairs

\[
 (x,y),(x,z),(y,z),(u,x),(u,y).
\tag{1.3}
\]

The five printed pentagon occurrences use E4 registry rows

\[
 1,27,21,26,28
\tag{1.4}
\]

in the factor order

\[
 b_1,b_2,b_3,b_5^{-1},b_4^{-1}.
\tag{1.5}
\]

Define the literal simultaneous context homomorphism

\[
 \Phi_{\rm all}:G\longrightarrow E_3^5\times E_4^5
\tag{1.6}
\]

by the ordered coordinates

\[
 \bigl(d_E C_{21},d_E C_{22},d_E C_{23},d_E C_{24},d_E C_{25};
 C_1,C_{27},C_{21},C_{26},C_{28}\bigr).
\tag{1.7}
\]

The repeated registry row \(C_{21}\) in (1.7) is load-bearing: one copy is
postcomposed with \(d_E\) and lives in E3, while the other remains in E4.
They cannot be deduplicated by name or by source word.

Put

\[
 \Delta_{\rm all}=\Phi_{\rm all}(G).
\tag{1.8}
\]

This is the one acting context group for the v110 stacked H1/H2/ordered-
pentagon correction columns.  It is not the full direct product in (1.6).

## 2. Extension-section theorem for an arbitrary context family

Let

\[
 1\to\Gamma\to G\xrightarrow{\rho}Q\to1
\tag{2.1}
\]

be any finite extension, and let

\[
 \Phi:G\longrightarrow H_1\times\cdots\times H_s
\tag{2.2}
\]

be any finite ordered family of homomorphisms.  Write

\[
 D=\Phi(G),\qquad A=\Phi(\Gamma).
\tag{2.3}
\]

Choose a set-theoretic section \(s:Q\to G\) with \(s(1)=1\), and define

\[
 L=\{q\in Q:\Phi(s(q))\in A\}.
\tag{2.4}
\]

### Theorem 2.1 (FINITE-FAMILY EXTENSION-SECTION CENSUS)

The subgroup \(L\) is independent of the chosen section, is normal in
\(Q\), and

\[
 \boxed{
 1\longrightarrow A\longrightarrow D
 \longrightarrow Q/L\longrightarrow1.}
\tag{2.5}
\]

In particular,

\[
 \boxed{|D|=|A|[Q:L].}
\tag{2.6}
\]

#### Proof

The image \(A\) is normal in \(D\).  The composite

\[
 G\xrightarrow{\Phi}D\longrightarrow D/A
\tag{2.7}
\]

kills \(\Gamma\), so it factors through a surjection
\(\bar\Phi:Q\twoheadrightarrow D/A\).  For a section value,
\(\bar\Phi(q)=\Phi(s(q))A\), and changing the section changes
\(\Phi(s(q))\) by an element of \(A\).  Hence (2.4) is exactly
\(\ker\bar\Phi\), proving section independence, normality, (2.5), and
(2.6). \(\square\)

This is v120 Theorem 2.1 with no restriction on the number, rank, or target
groups of the coordinates.  In particular it applies directly to the mixed
E3/E4 family (1.7).

## 3. Projection kernels without enumerating Delta_all

For an ordered subfamily \(S\) of the ten coordinates, write

\[
 \Phi_S:G\to H_S,
 \qquad D_S=\Phi_S(G),
 \qquad A_S=\Phi_S(\Gamma),
 \qquad L_S=\ker(Q_0\to D_S/A_S).
\tag{3.1}
\]

Theorem 2.1 gives

\[
 |D_S|=|A_S|[Q_0:L_S].
\tag{3.2}
\]

For \(S\subseteq T\), coordinate deletion is onto and therefore

\[
 \boxed{
 |\ker(D_T\to D_S)|
 =\frac{|A_T|[Q_0:L_T]}{|A_S|[Q_0:L_S]}.}
\tag{3.3}
\]

Every nonempty fibre has the order (3.3).  Thus the ten one-coordinate
projections needed by the all-seven occurrence formula, all repeated-context
equalities, and every support fibre requested by v118 can be sized without a
BFS in \(\Delta_{\rm all}\).

For word-bearing kernel data, let

\[
 H_S=\ker(\Phi_S:G\to D_S),
 \qquad \Gamma_S^0=H_S\cap\Gamma.
\tag{3.4}
\]

Restriction of \(\rho\) gives

\[
 \boxed{
 1\longrightarrow\Gamma_S^0\longrightarrow H_S
 \xrightarrow{\rho}L_S\longrightarrow1.}
\tag{3.5}
\]

Indeed, if \(q\in L_S\), choose \(\gamma_q\in\Gamma\) satisfying

\[
 \Phi_S(\gamma_q)=\Phi_S(s(q))^{-1};
\tag{3.6}
\]

then \(\gamma_qs(q)\in H_S\) maps to \(q\).  Consequently generators of
\(\Gamma_S^0\), together with the adjusted section words (3.6) for
generators of \(L_S\), give actual source-word generators for the relevant
projection kernel inside \(\Delta_{\rm all}\).

## 4. One bounded scan

The all-seven census can be computed by the following exact finite route.

1. Project all 243 authenticated Gamma states simultaneously through the ten
   maps (1.7).  From the same pass compute every required \(A_S\), exact
   multiplication/inverse closure, canonical element-set digest, and Gamma
   sections.
2. Enumerate the authenticated 1,469,664 Q0 states in the frozen section
   order.  Evaluate all ten coordinates of one source section once.
3. For every required subfamily \(S\), test literal membership of
   \(\Phi_S(s(q))\) in \(A_S\).  Retain the exact \(L_S\) membership bit,
   section provenance, canonical digest, and Gamma adjustment (3.6) when
   needed.
4. Check identity, multiplication, inverses, and normality of every \(L_S\),
   then apply (3.2)--(3.3).
5. Independently replay the marked x/y images and at least one nontrivial
   word-bearing kernel generator for every nontrivial projection kernel.

The Q0 scan is shared, but membership tables remain typed by their ordered
coordinate subfamilies.  Hash equality is not substituted for literal
element equality.

The work is bounded by one 1,469,664-state section scan plus the 243-state
Gamma tables.  It never enumerates the possible

\[
 |G|=357{,}128{,}352
\tag{4.1}
\]

joint states, and it never streams \(6{,}441|\Delta_{\rm all}|\) orbit
columns.

## 5. Exact consumer: support-fibre column generation

For one dual support target in occurrence coordinate \(i\), the required
fibre is

\[
 \pi_i^{-1}(t)=d\ker\pi_i.
\tag{5.1}
\]

The tables of Section 4 decide \(t\in D_i\), return an actual section word
for one \(d\), and give the word-bearing kernel presentation (3.5).  V118 can
therefore correlate a separating dual with the complete linked all-seven
orbit by scanning or recursively correlating only the support-pinned fibres.
The PB3 two-row translate family is embedded separately in the H1 and H2
blocks, and the PB4 eleven-row translate family remains separately typed in
the pentagon block.

If a fibre or recursive correlation reaches its registered cap, the result
is `UNKNOWN_RESOURCE`.  A negative all-seven separator is sound only after
every support fibre, the constant complement case, and both exact D2
families have been exhausted.

Every ACTIVE correction column retains an actual word

\[
 u_\delta r u_\delta^{-1}
\tag{5.2}
\]

with its Gamma/Q0 section provenance.  Hence a positive stacked solve can
materialize one common correction word, rather than three unrelated
component solutions.

## 6. Connection with the based Nakayama lift

After a positive depth-9 all-seven solve, v124 does not require an
orbit-wide annihilator-compatible splitter.  The solver should retain a
finite free cover \(q:F\to Z^{\rm act}\), word-bearing leading columns
\(s_0\), and solve the error-coordinate equation

\[
 B s_0-q=qR,
 \qquad R(F)\subseteq I^9F.
\tag{6.1}
\]

The same authenticated context sections used in (5.2) define every entry of
\(s_0\) and \(R\).  Since \(I^{29}=0\), v124 then gives

\[
 \widetilde s=s_0(1-R+R^2-R^3)
\tag{6.2}
\]

through the complete fixed \(\Pi_4[3]\) radical.  This is still a
fixed-context statement.  Compatible error matrices after a context-changing
refinement, all nonlinear side gates, and nonabelian chief accepted sets
remain separate obligations.

```text
TEN-COORDINATE ALL-SEVEN MAP:                PAPER-TYPED BY v122/INVENTORY173
FINITE-FAMILY EXTENSION-SECTION THEOREM:     PAPER_PROOF
PROJECTION ORDER / WORD-KERNEL REDUCTION:    PAPER_PROOF
ONE-Q0-SCAN ALGORITHM:                       EXACT DESIGN / NOT RUN
ALL-SEVEN SUPPORT-FIBRE CORRELATION:         NOT RUN
DEPTH-9 BASED ERROR MATRIX R:                NOT COMPUTED
FIXED-CONTEXT COMMON CORRECTION:             NOT CONSTRUCTED
CONTEXT-CHANGING / NONABELIAN GATES:         OPEN
COMPATIBLE COFINAL R07 LIFT:                 NOT CONSTRUCTED
FAKE / IHARA WITNESS:                        NOT DECLARED
```

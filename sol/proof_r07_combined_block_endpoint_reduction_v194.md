# R07 combined-block endpoint reduction v194

Author: Sol / 2026-08-28

Status: paper theorem and erratum to v193.  The universal boundary gate is
indeed equivalent to a finite Fox-endpoint identity, but the identity is
tested after the eleven literal occurrences have been combined in printed
order into the three relation blocks H1, H2, and P.  V193 incorrectly
required the occurrence summands to be cycles separately; that condition is
too strong because cancellation between occurrences in one relation word is
load-bearing.  This note supersedes v193 in full.  The actual task192 word,
pointed multiplier, and three endpoints have not yet been computed.  No
compatible R07 lift, fake certificate, or Ihara witness is declared.

## 1. Occurrences, acting coordinates, and relation blocks

Put \(k=\mathbf F_3\).  Retain the eleven literal occurrences of v189:

\[
 \mathcal O=
 \{H1_1,H1_2,H1_3,H2_1,H2_2,H2_3,
   P_1,P_2,P_3,P_5,P_4\}.
\tag{1.1}
\]

Their acting values have ten distinct typed coordinates because
\(H1_1\) and \(H2_2\) use the same E3 map.  This does not identify their
two positions in the relation words.  The E3 and E4 values both carrying
the registry label `C21` also remain different typed coordinates.

Let

\[
 \mathcal B=\{H1,H2,P\}
\tag{1.2}
\]

be the three relation blocks.  The target presentation group is PB3 for
H1 and H2 and PB4 for P.  Use a separate tagged copy of the appropriate
complete presentation chain complex for each block:

\[
 C_{2,B}\xrightarrow{D_{2,B}}C_{1,B}
 \xrightarrow{D_{1,B}}C_{0,B},
 \qquad B\in\mathcal B.
\tag{1.3}
\]

Here

\[
 C_{2,B}=k[G_B]^{R_B},\qquad
 C_{1,B}=k[G_B]^{X_B},\qquad
 C_{0,B}=k[G_B],
\tag{1.4}
\]

and, in the registered left-Fox convention,

\[
 D_{2,B}[r]=\delta_B(r),\qquad
 D_{1,B}(g[x])=g(x-1).
\tag{1.5}
\]

The two PB3 or eleven PB4 relators are the complete fixed presentation
roster, not a sampled translated family.

For each occurrence \(o\) in block \(B\), let

\[
 \rho_o:\mathcal G\longrightarrow G_B
\tag{1.6}
\]

be its fixed common-source substitution.  Let \(L_o\) denote its literal
signed, prefix-transported insertion into the Fox chain of the whole block.
Thus \(L_o\) includes the negative H2 occurrence and the printed pentagon
order

\[
 b_1,b_2,b_3,b_5^{-1},b_4^{-1}.
\tag{1.7}
\]

The original target and corrected residual are stored occurrencewise and
then combined:

\[
 d_B=\sum_{o\in B}L_o(d_o),\qquad
 e_B=\sum_{o\in B}L_o(e_o).
\tag{1.8}
\]

Neither sum in (1.8) may be replaced by seven unrelated cycle tests.

## 2. The correct diagonal action before combination

Let

\[
 M=\sum_{i=1}^t a_i(U_i-V_i),\qquad
 a_i\in k,\qquad \pi(U_i)=\pi(V_i),
\tag{2.1}
\]

be the v191 roof-fibre word-pair polynomial.  Its action on a relation block
is the occurrence-diagonal action followed by printed-order combination:

\[
 \boxed{
 (M\star d)_B=
 \sum_{o\in B}L_o\!\left(
   \sum_i a_i(\rho_o(U_i)-\rho_o(V_i))d_o
 \right).}
\tag{2.2}
\]

This is generally not left multiplication of the already combined row
\(d_B\) by one element of \(k[G_B]\), because different occurrences use
different homomorphisms \(\rho_o\).  Formula (2.2) is what the phrase
`diagonal seven-context action` means at chain level.

Define

\[
 z_B(M)=e_B-(M\star d)_B\in C_{1,B}
\tag{2.3}
\]

and

\[
 \eta_B(M)=D_{1,B}z_B(M)\in k[G_B].
\tag{2.4}
\]

The universal v191 boundary equation is

\[
 z_B(M)=D_{2,B}q_B
 \quad\text{for }B=H1,H2,P.
\tag{2.5}
\]

Equivalently, it is the direct-sum equation for the three block complexes.

## 3. Exactness at degree one

### Lemma 3.1 (COMPLETE PB PRESENTATION BOUNDARIES ARE ALL BLOCK CYCLES)

For each \(B\in\mathcal B\),

\[
 \boxed{\ker D_{1,B}=\operatorname{im}D_{2,B}.}
\tag{3.1}
\]

Every finite-support cycle has a finite-support boundary preimage.

#### Proof

The chain complex (1.3)--(1.5) is the cellular chain complex in degrees
two through zero of the universal cover of the fixed presentation
two-complex for \(G_B\).  The universal cover is simply connected, so its
first homology vanishes.  Hence

\[
 H_1=\ker D_{1,B}/\operatorname{im}D_{2,B}=0.
\]

No asphericity or exactness at \(C_{2,B}\) is used.  Cellular chains are
direct sums, so the preimage is finite-support. \(\square\)

### Theorem 3.2 (THREE-BLOCK BOUNDARY--ENDPOINT EQUIVALENCE)

For the exact occurrence-diagonal action (2.2),

\[
 \boxed{
 \exists(q_{H1},q_{H2},q_P):
 z_B(M)=D_{2,B}q_B\ \forall B
 \quad\Longleftrightarrow\quad
 \eta_{H1}(M)=\eta_{H2}(M)=\eta_P(M)=0.}
\tag{3.2}
\]

On a positive endpoint result, every \(q_B\) may be chosen with finite
support.

#### Proof

The forward implication is
\(D_{1,B}D_{2,B}=0\).  Conversely, each zero endpoint places \(z_B(M)\)
in \(\ker D_{1,B}\), and Lemma 3.1 supplies \(q_B\). \(\square\)

This is the valid reduction intended by v193.  It removes blind boundary
column generation, while preserving every cancellation in a whole hexagon
or pentagon relation.

## 4. Finite endpoint computation

Expanding (1.8), (2.2), and (2.4) gives the authoritative formula

\[
 \boxed{
 \eta_B(M)=D_{1,B}e_B-
 \sum_{o\in B}D_{1,B}L_o\!\left(
   \sum_i a_i(\rho_o(U_i)-\rho_o(V_i))d_o
 \right).}
\tag{4.1}
\]

Every term has finite word support.  A producer can therefore:

1. evaluate every \(U_i,V_i\) in all ten distinct typed acting
   coordinates;
2. reinsert the repeated E3 value in its two occurrence positions;
3. apply the literal prefix/sign operator \(L_o\) in the eleven-position
   order;
4. apply \(D_{1,B}\) only after summing inside each of H1, H2, and P; and
5. normalize the resulting PB3/PB4 group words and collect coefficients
   modulo three.

A nonzero collected coefficient gives a complete obstruction to the exact
representative choice \(M\): no \(q\) satisfying (2.5) exists for that
choice.  If all three collections are zero, Theorem 3.2 proves existence of
finite boundary chains.  No rank cap or search radius enters that decision.

The word `finite` here refers to the support of the exact candidate, not to
the order of PB3 or PB4.  Group equality must be decided by an authenticated
PB word-normal-form implementation or by a literal derivation; hashes and
finite-quotient images are insufficient.

## 5. Constructing the boundary chains after a pass

After \(\eta_B(M)=0\), view \(z_B(M)\) as a finite one-cycle in the Cayley
graph of \(G_B\).  Split it over \(k\) into based loops.  For every loop
word retain an identity decomposition in the free presentation group,

\[
 w=\prod_j s_jr_{i_j}^{\epsilon_j}s_j^{-1},
 \qquad \epsilon_j\in\{1,-1\}.
\tag{5.1}
\]

Because every conjugated relator is already the identity in \(G_B\), left
Fox differentiation gives

\[
 \delta_B(w)=
 \sum_j\epsilon_j\,\overline{s_j}\,\delta_B(r_{i_j}).
\tag{5.2}
\]

The coefficients in (5.2), summed over the loop decomposition, are an
explicit \(q_B\).  Hence boundary-chain construction is proof extraction
after the endpoint decision, not a second membership conjecture.

A proof-producing normal-form/rewrite routine is the practical route.  In
principle, enumeration of products of conjugates of the finite relator
roster terminates for a known identity word.  Resource exhaustion during
proof extraction remains `UNKNOWN_RESOURCE`; it does not reverse the
mathematical existence supplied by Theorem 3.2.

## 6. Corrected post-pointed production chain

After task192/task193/v188 return a positive pointed ancestry:

1. compile the exact ordered multiplier \(\mu_1\) and its retained
   word-pair lift \(M_1\) by v191;
2. construct \((M_1\star d)_B\) with all eleven occurrences and the ten
   distinct typed acting values;
3. decide the three endpoint identities (4.1);
4. if one fails, retain the normalized nonzero block/group-element
   coefficient and vary only same-first-shadow representatives;
5. if all pass, extract \(q_{H1},q_{H2},q_P\) by (5.1)--(5.2) and replay
   (2.5); and
6. apply v191 and v174 to obtain the one relative pro-3 Neumann correction,
   subject to their word and nonlinear side gates.

Thus the all-rung positive gate after \(M_1\) is exactly

\[
 \boxed{
 (\eta_{H1}(M_1),\eta_{H2}(M_1),\eta_P(M_1))=(0,0,0).}
\tag{6.1}
\]

It is not the seven separate occurrence-endpoint condition asserted in
v193.  It is also not automatic from the first-successor equality
\(M_1\mapsto\mu_1\).

## 7. Certificate contract

A positive certificate retains:

1. the complete v191 ancestry, \(M_1\), and exact source representatives;
2. the v189 eleven-occurrence/ten-coordinate ledger;
3. every literal sign, inverse slot, prefix transport, and printed-order
   combination in (2.2);
4. the complete two PB3/eleven PB4 fixed presentations;
5. all unreduced endpoint terms, normal forms, collection buckets, and the
   three zero results;
6. every loop and conjugate-relator decomposition used in (5.1);
7. the three explicit chains \(q_B\) and direct replay of (2.5); and
8. destructive rejection after changing one duplicate occurrence, typed
   C21 value, sign, prefix, pentagon order, source representative, endpoint
   coefficient, relator factor, or boundary coefficient.

The independent checker must reconstruct the occurrence combination,
PB normal forms, and relator decompositions without importing producer
helpers.

```text
V193 SEVEN-SEPARATE-ENDPOINT FORMULATION:          RETRACTED / TOO STRONG
COMPLETE PRESENTATION FOX EXACTNESS AT BLOCK C1:   PAPER_PROOF
UNIVERSAL BOUNDARY IFF THREE BLOCK ENDPOINTS ZERO: PAPER_PROOF
FINITE-SUPPORT q AFTER THREE-ENDPOINT PASS:        PAPER_PROOF
BLIND UNIVERSAL BOUNDARY COLUMN GENERATION:        REMOVED
ACTUAL FIRST-SHADOW MULTIPLIER mu1:                NOT COMPUTED
ACTUAL WORD-PAIR POLYNOMIAL M1:                    NOT COMPILED
ACTUAL THREE-BLOCK ENDPOINT:                       NOT COMPUTED
EXPLICIT RELATOR-DECOMPOSITION CHAINS q_B:         NOT COMPILED
RELATIVE PRO-3 COMPATIBLE R07 LIFT:                NOT CONSTRUCTED
PRIME-TO-3 / PERFECT-CORE GATES:                   OPEN
FAKE / IHARA WITNESS:                              NOT DECLARED
```

`R07_COMBINED_BLOCK_ENDPOINT_REDUCTION_V194_PAPER_GRADE`

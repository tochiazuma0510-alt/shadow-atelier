# R07 endpoint-only word evaluator v198

Author: Sol / 2026-08-28

Status: paper compiler and performance reduction for the v194/v196 endpoint
gate.  The three endpoints can be collected directly from PB group-word
values and the fixed occurrence prefixes.  No Fox gradient of a multiplier
word and no translated presentation-boundary row is needed for this first
decision.  A positive zero endpoint is still followed by the independently
replayed boundary extraction of v197.  No actual multiplier, endpoint,
repair, compatible lift, fake certificate, or Ihara witness is declared.

## 1. Frozen occurrence form

Put \(k=\mathbf F_3\).  For one block \(B\in\{H1,H2,P\}\), retain every
literal occurrence \(o\in B\) separately until the final sum.  Its
occurrence chain and endpoint are

\[
 d_o\in k[G_B]^{X_B},
 \qquad
 \xi_o=D_{1,B}d_o\in k[G_B].
\tag{1.1}
\]

The registered printed-product Fox rule inserts an occurrence chain in the
form

\[
 L_o(c)=\sigma_oP_o c,
 \qquad
 \sigma_o\in\{1,-1\},\quad P_o\in G_B.
\tag{1.2}
\]

Here \(P_o\) is the frozen product prefix.  An inverse occurrence is first
converted to its literal inverse-word Fox chain; its inversion factor is
therefore already part of \(d_o\) and \(P_o\).  Formula (1.2) is exactly the
occurrence-prefix interface, not an assertion that all occurrences have the
same action.

Let

\[
 \epsilon_B=D_{1,B}e_B\in k[G_B]
\tag{1.3}
\]

be the endpoint of the corrected residual chain.  It can be computed once
from its retained literal word provenance.

The source substitution at occurrence \(o\) is

\[
 \rho_o:F(x,y)\longrightarrow G_B.
\tag{1.4}
\]

The two copies of the E3 \((x,y)\) substitution remain two positions with
their own \(\sigma_o,P_o,d_o\), even though their \(\rho_o\) values agree.

## 2. Endpoint-only formula

Let the finite word-pair polynomial be

\[
 M=\sum_{i=1}^{t}a_i(U_i-V_i),
 \qquad a_i\in k.
\tag{2.1}
\]

### Theorem 2.1 (ENDPOINT-ONLY COLLECTION)

The v194 combined endpoint is

\[
 \boxed{
 \eta_B(M)=
 \epsilon_B-
 \sum_{o\in B}\sigma_oP_o
 \sum_{i=1}^{t}a_i
 \bigl(\rho_o(U_i)-\rho_o(V_i)\bigr)\xi_o.}
\tag{2.2}
\]

Thus \(\eta_B(M)\) is computed using only:

1. the fixed sparse endpoints \(\epsilon_B,\xi_o\);
2. the fixed group elements \(P_o\) and signs \(\sigma_o\); and
3. the PB normal forms of the ten typed values of every \(U_i,V_i\).

No \(C_1\) Fox expansion of \(U_i\), \(V_i\), or a translated boundary
relator is required.

#### Proof

The left-Fox endpoint map is \(k[G_B]\)-linear:

\[
 D_{1,B}(vc)=vD_{1,B}(c)
 \qquad(v\in k[G_B],\ c\in k[G_B]^{X_B}).
\tag{2.3}
\]

Apply this identity to the v194 occurrence-diagonal definition:

\[
\begin{aligned}
D_{1,B}L_o\!\left(
 \sum_i a_i(\rho_o(U_i)-\rho_o(V_i))d_o\right)
&=
\sigma_oP_o
\sum_i a_i(\rho_o(U_i)-\rho_o(V_i))
D_{1,B}d_o\\
&=
\sigma_oP_o
\sum_i a_i(\rho_o(U_i)-\rho_o(V_i))\xi_o.
\end{aligned}
\tag{2.4}
\]

Sum (2.4) in the printed block order and subtract it from
\(D_{1,B}e_B=\epsilon_B\).  This is (2.2). \(\square\)

The equality is taken after collection in the one PB3 or PB4 group algebra
of the whole block.  Cancellation between different occurrences remains
fully available.

## 3. Literal word endpoints

If an occurrence chain is the left-Fox chain of a retained word \(r_o\),
then

\[
 d_o=\delta(r_o)
 \quad\Longrightarrow\quad
 \xi_o=\overline{r_o}-1.
\tag{3.1}
\]

More generally,

\[
 d_o=\delta(r'_o)-\delta(r_o)
 \quad\Longrightarrow\quad
 \xi_o=\overline{r'_o}-\overline{r_o}.
\tag{3.2}
\]

These follow from the Fox endpoint identity

\[
 D_1\delta(w)=\bar w-1.
\tag{3.3}
\]

Consequently a term in (2.2) arising from (3.1) expands before collection as

\[
 \sigma_oa_i\left(
 P_o\rho_o(U_i)\overline{r_o}
 -P_o\rho_o(U_i)
 -P_o\rho_o(V_i)\overline{r_o}
 +P_o\rho_o(V_i)\right).
\tag{3.4}
\]

It has at most four group-word buckets before coincidences are collected
modulo three.  Formula (3.2) has the same four-bucket bound.  Long Fox
gradients affect the later \(q\) chain but not the endpoint workload.

## 4. Endpoint-only same-successor repair columns

Let \(h_j\) be one of the complete Schreier generators in v196 and let
\(A\in F(x,y)\).  Put

\[
 N=A(h_j-1).
\tag{4.1}
\]

### Corollary 4.1 (ONE-SIDED REPAIR COLUMN)

Its endpoint-change column is

\[
 \boxed{
 \mathcal E_d\bigl(A(h_j-1)\bigr)_B
 =
 \sum_{o\in B}\sigma_oP_o\,
 \rho_o(A)\bigl(\rho_o(h_j)-1\bigr)\xi_o.}
\tag{4.2}
\]

Therefore v196's complete positive dovetail can run entirely in endpoint
group algebras.  It need not materialize an occurrence \(C_1\) row for every
candidate column.

#### Proof

Substitute \(N=A(h_j-1)\) into (2.2)'s linear change term and use
\(\rho_o(N)=\rho_o(A)(\rho_o(h_j)-1)\). \(\square\)

The rightmost order in (4.2) is load-bearing.  Neither \(\xi_o\) nor
\(P_o\) may be commuted through a source-word value.

## 5. Exact PB bucket keys from the faithful Artin action

Let \(t_1,\ldots,t_n\) freely generate \(F_n\).  Use the registered Artin
action

\[
\begin{aligned}
 \sigma_i(t_i)&=t_it_{i+1}t_i^{-1},&
 \sigma_i(t_{i+1})&=t_i,&
 \sigma_i(t_j)&=t_j\quad(j\ne i,i+1).
\end{aligned}
\tag{5.1}
\]

Every pure generator \(A_{ij}\) has its fixed standard braid word.  Expand a
PB3 or PB4 word into the \(\sigma_i^{\pm1}\), apply (5.1) in the frozen
composition convention, and freely reduce each image.  Define its full
Artin signature by

\[
 \operatorname{ArtNF}_n(w)=
 \bigl(w(t_1),\ldots,w(t_n)\bigr).
\tag{5.2}
\]

### Lemma 5.1 (ARTIN SIGNATURE IS AN EXACT PB KEY)

For \(u,v\in PB_n\), with \(n=3\) or \(4\),

\[
 \boxed{
 u=v
 \quad\Longleftrightarrow\quad
 \operatorname{ArtNF}_n(u)=\operatorname{ArtNF}_n(v).}
\tag{5.3}
\]

#### Proof

The Artin representation \(B_n\to\operatorname{Aut}(F_n)\) is faithful.
Its restriction to the subgroup \(PB_n\) is therefore faithful.  Two
automorphisms of the free group are equal exactly when their freely reduced
images agree on the displayed free basis. \(\square\)

Thus the complete tuple (5.2), not merely its hash, is a canonical exact
bucket key for (2.2) and (4.2).  This avoids both a finite-quotient false
equality and reliance on an opaque KBMAG result.  The existing
PB4 Artin-presentation producer/checker supplies a bounded implementation
canary for the six pure generators and eleven presentation relators; it is
an implementation asset, not a substitute for replaying the actual endpoint
words.

The producer may cache a tuple and seal it by a digest, but the certificate
retains the tuple itself.  An independent checker should preferably use a
Garside normal form, or a separately written Artin evaluator with an
independently converted composition convention.

## 6. Exact production schedule

For a compiled \(M_0\), use this order.

1. Reconstruct and authenticate the eleven records
   \((B,o,\rho_o,\sigma_o,P_o,\xi_o)\) and the three \(\epsilon_B\).
2. Evaluate every support word of \(M_0\) in the ten distinct typed
   coordinates and reinsert the repeated E3 value at both literal slots.
3. Emit the unreduced word terms of (2.2), normalize each PB word, collect
   coefficients modulo three, and retain the three complete bucket maps.
4. If a bucket remains, the named \(M_0\) is obstructed.  Invoke v196 only
   if another representative of the same \(\mu_1\) is sought.
5. If all bucket maps are empty, invoke v197 to construct and replay
   \(q_{H1},q_{H2},q_P\).

For v196 repair, cache only authenticated PB normal forms of
\(\rho_o(A)\), \(\rho_o(h_j)\), and their products.  A cache key includes
the typed occurrence map; the E3 and E4 entries sharing the registry label
C21 are never identified.

The endpoint evaluator is an exact gate, not a quotient screen.  A
nonidentity PB word must not be declared zero because its image vanishes in
the roof or first successor.

## 7. Certificate and destructive controls

Retain:

1. the literal residual and occurrence words giving (1.1)--(1.3);
2. every sign, prefix, block, component, inverse slot, and printed-order
   position;
3. unreduced and normalized PB words for every term of (2.2);
4. every full Artin signature (5.2), coefficient collection, and zero
   deletion;
5. on repair, the complete \((A,h_j)\) ancestry and the columns (4.2); and
6. a separate full-\(C_1\) replay for the final positive candidate before
   v197 extracts \(q\).

The independent checker recomputes \(\epsilon_B,\xi_o\) from the literal
word endpoints and uses a separately implemented PB normal form.  It
compares the endpoint-only result with \(D_1\) of a direct full-\(C_1\) toy
and with the final production chain.

Reject mutations of one source word, typed substitution, duplicated E3
position, E3/E4 C21 type, sign, prefix, inverse factor, factor order,
endpoint word, coefficient, normalization result, or collected bucket.

~~~text
THREE ENDPOINTS FROM WORD VALUES WITHOUT FOX EXPANSION: PAPER_PROOF
FOUR-BUCKET OCCURRENCE-PAIR FORMULA:                 PAPER_PROOF
ONE-SIDED REPAIR COLUMNS ENDPOINT-ONLY:               PAPER_PROOF
FAITHFUL ARTIN TUPLE AS EXACT PB BUCKET KEY:           PAPER_PROOF
FULL-C1 REPLAY FOR FINAL POSITIVE CANDIDATE:           STILL REQUIRED
ACTUAL M0 / THREE ENDPOINTS / REPAIR:                 NOT COMPUTED
ACTUAL q_H1 / q_H2 / q_P:                            NOT COMPILED
COMPATIBLE RELATIVE PRO-3 LIFT:                       NOT CONSTRUCTED
PRIME-TO-3 / PERFECT-CORE GATES:                      OPEN
FAKE / IHARA WITNESS:                                 NOT DECLARED
~~~

R07_ENDPOINT_ONLY_WORD_EVALUATOR_V198_PAPER_GRADE

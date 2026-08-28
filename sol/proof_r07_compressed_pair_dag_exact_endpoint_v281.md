# R07 compressed pair-DAG exact endpoint evaluator v281

Author: Sol / 2026-08-29

Status: paper theorem and future A7 production refinement of v197, v198,
v242, and v280. Every pair emitted by the corrected A5 construction has the
factored form \(Au-A=A(u-1)\). Its three exact PB endpoints can therefore be
evaluated from a prefix DAG and a finite kernel-word dictionary, without
re-evaluating both concatenated words from scratch for every term. A final
ZERO still requires literal pair expansion, an independent endpoint replay,
and the full-\(C_1\) positive replay before v197 boundary extraction. No
actual A5 MEMBER, exact endpoint, compatible lift, fake certificate, or Ihara
witness is declared. `verified=false`.

## 1. The exact compressed language supplied by A5

Let \(F=F(x,y)\). V280 constructs the A3+A4 base point from terms

\[
 s(g)u_*-s(g)=s(g)(u_*-1),
\tag{1.1}
\]

and v242 expands every A5 closure ancestry into terms

\[
 A u_i-A=A(u_i-1),
\tag{1.2}
\]

where \(u_*,u_i\in F\) are literal A4 kernel words and \(A\in F\) is a
literal left-prefix word retained by the action ancestry. Hence every A5
MEMBER output has the form

\[
 \boxed{
 M=\sum_{q=1}^{N}c_q(A_qu_{i(q)}-A_q),
 \qquad c_q\in\mathbf F_3,
 \qquad \rho_0(u_{i(q)})=1.}
\tag{1.3}
\]

This is a finite literal source-algebra representative, not merely a
\(\Delta _1\)-coefficient vector. Distinct words \(A_q\) representing the
same element of \(\Delta _1\) are not identified: their exact PB images may
differ.

Store the prefix words in an acyclic proof DAG. A root is the empty word;
each nonroot node records a parent and one letter in
\(x^{\pm1},y^{\pm1}\), and means deterministic free reduction after appending
that letter. A term in (1.3) records

\[
 (c_q,\text{prefix-node}(A_q),\text{kernel-index }i(q)).
\tag{1.4}
\]

The certificate retains enough parent/letter data to reconstruct every
literal \(A_q\), so this compression does not quotient source words by a
finite shadow.

## 2. Factored exact endpoint formula

For one block \(B\in\{H1,H2,P\}\), retain the separately typed occurrences
of v198:

\[
 (o,\rho_o,\sigma_o,P_o,\xi_o),
 \qquad
 \rho_o:F\to PB_{B(o)},
 \qquad \sigma_o\in\{1,-1\}.
\tag{2.1}
\]

Let \(\epsilon_B\) be the fixed exact endpoint of the residual chain. All
products below remain in their displayed noncommutative order.

### Theorem 2.1 (FACTORED PAIR ENDPOINT)

For \(M\) in (1.3), its exact combined endpoint is

\[
 \boxed{
 \eta_B(M)=\epsilon_B-
 \sum_{o\in B}\sum_{q=1}^{N}
 \sigma_oc_qP_o\rho_o(A_q)
 \bigl(\rho_o(u_{i(q)})-1\bigr)\xi_o.}
\tag{2.2}
\]

It is exactly the endpoint of the fully expanded literal pairs in (1.3).

#### Proof

For each occurrence and pair,

\[
 \rho_o(A_qu_i)-\rho_o(A_q)
 =\rho_o(A_q)(\rho_o(u_i)-1).
\tag{2.3}
\]

Substitution of (2.3) into v198 Theorem 2.1, without commuting any factor,
is (2.2). \(\square\)

If \(\xi_o=v_o'-v_o\), the contribution of one pair before bucket
collection is the four-term expression

\[
\begin{aligned}
 \sigma_oc_q(&P_o\rho_o(A_q)\rho_o(u_i)v_o'
 -P_o\rho_o(A_q)\rho_o(u_i)v_o\\
 &-P_o\rho_o(A_q)v_o'
 +P_o\rho_o(A_q)v_o).
\end{aligned}
\tag{2.4}
\]

Thus the factorization changes evaluation cost, not the exact group-algebra
collection or cross-occurrence cancellation.

## 3. Incremental evaluation on the prefix DAG

For every typed occurrence \(o\), evaluate the prefix DAG in topological
order. If node \(v\) has parent \(p\) and letter \(\ell\), define

\[
 R_o(v)=R_o(p)\rho_o(\ell),
 \qquad R_o(\text{root})=1,
\tag{3.1}
\]

using exact PB multiplication and normalization. Separately evaluate each
distinct A4 word once:

\[
 K_o(i)=\rho_o(u_i).
\tag{3.2}
\]

Formula (2.2) is then collected from \(R_o(v)\), \(K_o(i)\), and the fixed
occurrence records.

### Theorem 3.1 (DAG EVALUATION IS LITERAL EVALUATION)

For every node \(v\) representing the freely reduced word \(A_v\),

\[
 \boxed{R_o(v)=\rho_o(A_v).}
\tag{3.3}
\]

Consequently the incremental algorithm returns precisely (2.2).

#### Proof

Induct on the topological depth. The root equality is immediate. At one
edge, homomorphic evaluation and deterministic free cancellation give

\[
 R_o(v)=\rho_o(A_p)\rho_o(\ell)
       =\rho_o(\operatorname{red}(A_p\ell)).
\tag{3.4}
\]

Theorem 2.1 finishes the assertion. \(\square\)

The DAG must be an authenticated literal-word DAG. A table keyed only by a
\(\Delta _1\) element, a hash, or an A5 pivot is unsound for exact endpoints.
Parent indices must be earlier, letters must be literal, and every exported
word is independently reconstructed from the root.

## 4. Complexity and bounded storage

Let

- \(p\) be the number of distinct prefix DAG nodes;
- \(t\) be the number of distinct A4 kernel words used;
- \(L_K\) be their total literal length;
- \(N\) be the number of nonzero factored terms after coefficient collection;
  and
- \(s_o=|\operatorname{supp}\xi_o|\).

Ignoring the intrinsic cost of the chosen exact PB normal form, the producer
uses

\[
 \boxed{
 O\!\left(10(p+L_K)+
       \sum_o N s_o\right)}
\tag{4.1}
\]

PB multiplications and stores \(O(10(p+t))\) cached exact values plus the
collected endpoint buckets. For the usual two-term Fox endpoints,
\(\sum_oNs_o=O(11N)\).

The naive route evaluates \(A_qu_i\) and \(A_q\) independently at every
term and occurrence, charging repeated prefix length. V281 removes exactly
that repetition. It does not suppress any typed occurrence, bucket,
coefficient, exact normal form, or independent check.

Coefficient collection in the compressed language may combine only records
with identical reconstructed literal prefix and kernel word. More aggressive
combination is allowed only after exact PB images have independently been
computed; equality in a roof or successor quotient is insufficient.

## 5. Positive-only literal and full-chain replay

The fast producer first decides whether all three bucket maps from (2.2) are
empty. The two outcomes have different proof obligations.

### 5.1 Named-candidate NONZERO

A retained nonzero exact Artin/Garside bucket, independently reconstructed
from the literal DAG, proves only

\[
 \eta_B(M)\ne0
\tag{5.1}
\]

for this named \(M\). It is not nonexistence of another A5 MEMBER solution,
another source representative, another lower correction, or a compatible
lift. No full-\(C_1\) expansion is needed to give (5.1), but producer and
checker must agree using helper-nonshared exact PB evaluators.

### 5.2 ZERO candidate

Before a ZERO may count toward A7, expand every compressed term locally as

\[
 U_q=\operatorname{red}(A_qu_{i(q)}),
 \qquad V_q=A_q,
\tag{5.2}
\]

and perform all of the following:

1. replay the expanded word pairs and equality with the A5 MEMBER ancestry;
2. let an independent checker evaluate every \(U_q,V_q\) from scratch with
   a distinct exact PB convention and reproduce the three empty buckets;
3. construct the occurrence-diagonal full Fox chains
   \(z_{H1},z_{H2},z_P\) from the literal words;
4. check directly that their \(D_1\)-images equal the empty endpoint maps;
5. retain the complete sparse chains for the v197 consumer; and
6. only then emit the three A7 ZERO milestones.

This is the exact-endpoint analogue of positive-only provenance replay: a
compressed discovery path may propose a candidate, but only the expanded
literal object is authoritative for success.

## 6. A8 handoff and repair boundary

On ZERO, v197 applies separately to the three combined chains and returns
finite relator chains

\[
 q_{H1},q_{H2},q_P,
 \qquad D_{2,B}q_B=z_B(M).
\tag{6.1}
\]

No second translated-boundary rank search is needed. The compressed DAG is
kept as provenance, while the authoritative A8 inputs are the expanded
literal pairs and full chains from Section 5.2.

On NONZERO, v198/v196 may dovetail over other permitted source
representatives. The current theorem only accelerates evaluation of each
finite factored candidate. It does not turn one NONZERO into a universal
obstruction and does not claim that the repair dovetail is bounded.

## 7. Future production ABI

A future A7-v3 consumer of A5/A6 must:

1. bind the exact accepted A5 producer/checker and MEMBER ancestry;
2. reconstruct, rather than accept, every tuple (1.4) from the v280 base
   pairs and the v242 closure ancestry;
3. authenticate the prefix DAG and kernel dictionary and replay all source
   words;
4. recompute (2.2) in all eleven typed occurrences and collect only by full
   exact PB keys;
5. use a checker which expands \(U,V\) and does not import the producer's DAG
   evaluator, cache, bucket table, normal-form helper, or terminal;
6. treat caps as `UNKNOWN_RESOURCE` and malformed ancestry as
   `UNKNOWN_INPUT`; and
7. apply the positive-only gates in Section 5.2 before declaring ZERO.

Mutations must reach the physical owner of a prefix parent, appended letter,
kernel index, kernel word, coefficient, typed occurrence, E3 reinsertion,
E3/E4 C21 type, sign, \(P_o\), \(\xi_o\), factor order, exact PB key, bucket,
expanded \(U/V\), full-\(C_1\) row, terminal, and resource snapshot. A copied
Boolean or post-hoc shaped transcript is not a control.

## 8. Fixed frontier

```text
A5 PAIR LANGUAGE M=sum c*A(u-1):                 PAPER PROOF
FACTORED EXACT THREE-ENDPOINT FORMULA:            PAPER PROOF
PREFIX-DAG INCREMENTAL EVALUATION:                PAPER PROOF
REPEATED LONG-PREFIX EVALUATION:                  REMOVED
ZERO -> EXPANDED PAIRS + FULL-C1 REPLAY:           STILL MANDATORY
ZERO -> FINITE v197 BOUNDARY EXTRACTION:           PAPER PROOF
NAMED-CANDIDATE NONZERO -> UNIVERSAL OBSTRUCTION:  NOT CLAIMED
ACTUAL A5 MEMBER / PAIR DAG:                      NOT COMPUTED
ACTUAL H1/H2/P ZERO / q_B:                        NOT COMPUTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:           NOT CONSTRUCTED
```

`R07_COMPRESSED_PAIR_DAG_EXACT_ENDPOINT_V281_PAPER_GRADE`

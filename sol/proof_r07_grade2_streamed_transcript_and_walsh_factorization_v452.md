# R07 A0: streamed presentation transcript and simultaneous grade-two projectors (v452)

Author: Sol / 2026-09-03

## 0. Scope

This note replaces no mathematical object in v450--v451.  It proves that the
large lists required by the grade-two implementation may be serialized as an
append-only binary transcript, and that the four legal pure-grade character
projections may be formed by one four-point transform.  These are exact
factorizations of the same registered computation, not heuristic pruning.

No actual module, membership result, A0, COMMON, cofinal lift, fake or Ihara
claim is made.  `verified=false`.

## 1. Deterministic offer stream

Fix one character \(\lambda\), put \(W=36,288\), and let
\(m=44+4\operatorname {rank}(B_1)\).  The v451 source closure has the
following unique offer order.

1. Offer the \(m\) projected defects in origin order.
2. Give every accepted row the next pivot number \(0,1,\ldots\).
3. Read accepted pivots in FIFO order and offer their four translates in actor
   order \((x,x^{-1},y,y^{-1})\).
4. Stop exactly when the FIFO is empty.

For an offered packed row \(v_s\), ordinary left-to-right echelon reduction
against earlier normalized pivots \(b_0,\ldots,b_{r_s-1}\) produces unique
ordered data

\[
 v_s-\sum_{(i,a)\in q_s}a b_i=\bar v_s.             \tag{1.1}
\]

If \(\bar v_s=0\), record `dependent`.  Otherwise let \(\ell_s\) be its first
nonzero coordinate and \(\sigma_s\in\{1,2\}\) the scalar which normalizes
that coordinate; then

\[
 b_{r_s}=\sigma_s\bar v_s.                          \tag{1.2}
\]

The offer identifier is one of

\[
 (\mathrm{defect},o),\qquad
 (\mathrm{actor},i,t),                              \tag{1.3}
\]

where \(0\leq o<m\), \(i\) is an earlier accepted pivot, and
\(0\leq t<4\).  Thus it contains the exact DAG origin independently of the
row bytes.

## 2. Binary-transcript theorem

Define a transcript record \(L_s\) to contain, in a fixed endian- and
width-versioned encoding,

\[
 (s,\operatorname{id}(v_s),q_s,
   \mathrm{dependent})                              \tag{2.1}
\]

or, in the accepted case,

\[
 (s,\operatorname{id}(v_s),q_s,
   \mathrm{accepted},r_s,\ell_s,\sigma_s).          \tag{2.2}
\]

Here every coefficient in \(q_s\) is in \(\{1,2\}\), pivot indices are
strictly earlier than the new pivot, and an offset table gives the byte start
of every record.  Store the normalized accepted rows in a separate
append-only packed matrix, in pivot order.

### Theorem 2.1 (lossless externalization)

The pair

\[
   (\text{accepted packed matrix},\ (L_s)_s)        \tag{2.3}
\]

is canonically equivalent to the in-memory data

```text
origin_reductions, actor_transitions, dag_nodes,
pivot_leads, basis_rows, attempts, queue_exhausted.
```

In particular, replacing nested Python lists and JSON arrays by authenticated
binary files changes neither \(H^{[2]}_\lambda\), its row order, nor the
transition presentation needed at the next grade.

#### Proof

For a defect offer, (1.3) identifies the entry of `origin_reductions`; for an
actor offer it identifies the unique entry of `actor_transitions`.  Equation
(1.1) is precisely the corresponding reduction expression.  Each accepted
record supplies the origin, reduction and normalizing scale of the next DAG
node by (1.2), while the accepted matrix supplies its row and the record its
lead.  Hence (2.3) reconstructs every listed in-memory field.

Conversely, the listed fields, read in the registered origin/FIFO/actor order,
write (2.1)--(2.2) uniquely.  Induction on the offer number proves equality of
all intermediate bases: before offer \(s\) the reconstructed basis agrees;
deterministic first-lead reduction then gives the same \(q_s,\bar v_s\), and
(1.2) gives the same next pivot if it exists.  The final FIFO is empty exactly
when the receipt contains

\[
  \#\mathrm{offers}=m+4\,\#\mathrm{accepted}.       \tag{2.4}
\]

This proves both directions. \(\square\)

### Corollary 2.2 (streamed checking)

Neither producer nor checker has to parse the complete presentation into
memory.  It may authenticate the matrix, transcript and offset files once,
then replay records sequentially.  Random access is needed only when a future
consumer asks for one origin or transition expression; the authenticated
offset table supplies it.

The checker must still recompute the rows and (1.1)--(1.2).  Comparing only
hashes or producer summaries is insufficient.

## 3. Simultaneous character projection

Let \(C=C_2^2\), ordered as in v451, and let \(w_a\), \(a\in C\), be the four
pinned pure-\(Q_1\) words.  For a lower-zero pure degree-two defect \(\beta\)
put

\[
     v_a=L_{w_a}^{(2)}\beta.                         \tag{3.1}
\]

The four legal associated-grade components are

\[
     e_\chi\beta=\sum_{a\in C}\chi(a)v_a,
     \qquad \chi\in\widehat C.                      \tag{3.2}
\]

There is no extra scalar: \(|C|=4=1\) in \(\mathbf F_3\).  If the rows
\((v_a)_a\) are placed in the registered order, (3.2) is the four-point
Hadamard transform

\[
\begin{pmatrix}
1&1&1&1\\
1&-1&1&-1\\
1&1&-1&-1\\
1&-1&-1&1
\end{pmatrix}
\begin{pmatrix}v_{00}\\v_{01}\\v_{10}\\v_{11}\end{pmatrix}.       \tag{3.3}
\]

The signs in an implementation must be generated from the pinned character
table rather than inferred from the displayed choice of labels.

### Theorem 3.1 (one action pass for all four packets)

For each defect, computing the four rows (3.1) once and applying (3.3) gives
exactly the four rows obtained by four separate calls to the v451 pure-grade
projectors.  Thus the word actions fall from sixteen to four per defect,
without splitting any of the six monomials.

#### Proof

Expand each separate projector by its definition.  Its four summands are the
same \(v_a\), with coefficients \(\chi(a)\).  Collecting the four equations is
exactly (3.3).  Each \(L_{w_a}^{(2)}\) acts on the full six-monomial row, so no
monomial-wise closure is introduced. \(\square\)

This theorem uses genuine associated-grade idempotents \(e_\chi\).  It does
not assert idempotence of the full filtered sums \(P_\chi\) from v451 (1.1).
That distinction remains load-bearing.

## 4. Packed defect compiler

Write an exact precision-two lift of the \(i\)-th \(B_1\) row as

\[
       \widetilde b_i=(\ell_i,g_i),                 \tag{4.1}
\]

where \(\ell_i\) is its degree-at-most-one part and \(g_i\) its degree-two
part.  Suppose the authenticated transition presentation says

\[
       A_t\ell_i=\sum_j q_{itj}\ell_j.              \tag{4.2}
\]

Let \(C_t(\ell_i)\) be the degree-two crossed term obtained by applying the
exact affine action to \((\ell_i,0)\).  Then the complete transition defect is

\[
 \beta_{it}=C_t(\ell_i)+A_t^{(2)}g_i-sum_jq_{itj}g_j.                \tag{4.3}
\]

Likewise, for seed \(a\) with reduction \(s_a^{\leq1}=\sum_jq_{aj}\ell_j\),

\[
 \beta_a=\operatorname{gr}_2(s_a)-\sum_jq_{aj}g_j.                  \tag{4.4}
\]

### Proposition 4.1

Equations (4.3)--(4.4) are equal to the current full-array construction, but
all sums over \(g_j\) may be executed directly against the packed,
file-backed lift matrix.  No referenced full row has to be unpacked into a
Python object.  Only one dense output scratch row is required.

#### Proof

The filtered action is triangular in degree.  Its degree-two component is the
linear associated-grade action on \(g_i\) plus the crossed term determined by
\(\ell_i\).  Taking degree two in (4.2) after substituting (4.1) gives (4.3);
the seed equation is identical with no actor term.  Packed four-trit AXPY is
the same \(\mathbf F_3\)-linear combination coordinatewise, proving (4.4) and
the storage claim. \(\square\)

The crossed term may not be dropped even though the chosen group extension
has zero multiplication cocycle.  The occurrence cochains remain crossed as
required by v451 section 3.

## 5. Resumable worker contract

A production backend sufficient for this theorem is a persistent or resumable
transducer, not a one-shot static matrix routine.  It must support:

1. an authenticated initial basis/lead state (empty on the first call);
2. a stream or batch of packed offers with opaque identifiers (1.3);
3. append-only accepted rows and transcript records (2.1)--(2.2), written as
   binary rather than decimal JSON arrays;
4. an atomic checkpoint containing accepted count, offer count, FIFO head and
   tail, basis/transcript/offset lengths and incremental digests;
5. restart by authenticating those exact prefixes and rebuilding only the
   small lead-to-pivot map; and
6. a sealed final receipt proving (2.4), unique normalized leads and exhausted
   FIFO.

The worker retains the current packed basis and one scratch row.  The caller
retains only the FIFO of pivot identifiers and reads an accepted row from the
append-only basis file when forming its four actor children.  There is no
per-pivot process launch and no retained copy of all offered rows.

For one character, the packed basis ceiling is

\[
  36,288\cdot(36,288/4)=329,204,736\ \text{bytes}.                  \tag{5.1}
\]

The lead map is below 0.3 MB and an eight-byte offset for each of at most
177,432 offers is below 1.5 MB; the variable transcript is streamed to disk
and is subject to an explicit byte cap.  Four character phases may run as
separate GHA jobs, so their bases need not coexist in one process.

## 6. Physical lower-first phase

The same externalization applies after aggregation.  The lower-first identity
is unchanged: reduce a row's 32,260 lower/auxiliary coordinates first, apply
the identical coefficients to its 48,384-coordinate grade companion, and
only when the lower remainder is zero offer that companion to the grade
owner.  Accepted lower companions and both DAGs may use the transcript format
of Theorem 2.1.

At the absolute dimension ceilings, the three packed row stores are bounded by

\[
\begin{aligned}
32,260^2/4 &=260,176,900\ \text{bytes},\\
32,260\cdot48,384/4&=390,216,960\ \text{bytes},\\
48,384^2/4&=585,252,864\ \text{bytes}.
\end{aligned}                                                        \tag{6.1}
\]

Their sum is exactly 1,235,646,724 bytes.  An implementation must recompute
these products with checked 64-bit arithmetic rather than trust prose.  Together
with one source-character basis and bounded scratch, these packed stores are
below 2 GiB.  Python list/JSON representations of their reduction transcripts
are not covered by that bound and are forbidden in production.

## 7. Consequence for the A0 first rung

Once the v451 arithmetic and boundary replay has passed, a producer using
Theorems 2.1 and 3.1 and Proposition 4.1 constructs exactly the same
target-independent grade-two module as the direct implementation.  A checked
grade-one MEMBER may then supply \(\rho_2\); grade-two MEMBER/NONMEMBER still
requires reduction against the sealed physical module and an independent
positive replay or separating dual.

The current Task565 implementation remains a candidate until its independent
audit and the streamed repair are complete.  The current Task567 backend is
also only a candidate: a static one-shot ABI or decimal-JSON receipt does not
by itself meet section 5.

```text
STREAMED TRANSCRIPT: paper-exact
SIMULTANEOUS PROJECTORS: paper-exact
PACKED DEFECT FORMULAS: paper-exact
PRODUCTION IMPLEMENTATION / COMPILED CALIBRATION: not yet accepted
FIRST RUNG: 0/6 grades decided at the time of writing
A0 / COMMON / COFINAL LIFT / FAKE / IHARA: not declared
verified=false
```

`R07_GRADE2_STREAMED_TRANSCRIPT_WALSH_V452_PAPER`

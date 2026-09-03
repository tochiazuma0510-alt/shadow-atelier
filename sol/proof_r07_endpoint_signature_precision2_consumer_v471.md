# R07: endpoint-signature compression for the precision-two consumer (v471)

Author: Sol / 2026-09-03

Status: candidate constructive sharpening of the Task611-accepted v470
leaf-gated replay.  It gives a result-dependent algorithm for evaluating the
complete selected correction through precision two without expanding its
free word and without applying a dense row at every selected SLP node.  It
does not assert that the pending Task601 payload has passed, does not compute
the fresh residual, and does not decide grade two, A0, COMMON, cofinality,
fake or Ihara.  `verified=false`.

## 1. Authenticated inputs and two kinds of compression

Let \(\mathcal G\) be the canonical noncommutative selected graph and let

\[
 C_1=\operatorname{Compose}(C_{<1},C_T)                 \tag{1.1}
\]

be its registered complete root.  The required parent is an accepted
Task601 payload satisfying v468--v469: all 8,059 physical offers have the
authenticated ordered transcript, every selected source dependency is
present, and the three roots have their exact registered order.

The graph \(\mathcal G\) is the common-source witness.  It is never
coalesced.  After authenticating it, the descending adjoint pass of v467 and
v470 produces the current evaluation map

\[
       \mu:(s,P)\longmapsto\mu_{s,P}\in\mathbf F_3,     \tag{1.2}
\]

where \(1\leq s\leq44\) and \(P\in F(x,y)\) is an exact freely reduced
actor path.  Equal exact keys may be added in (1.2), but this remains a
derived evaluation receipt and is not a replacement for \(\mathcal G\).

There is a second, still more local compression.  Let \(J\) be the exact
list of the eleven registered occurrence contexts used by the complete
precision-two interpreter.  For an actor path define its **complete endpoint
signature**

\[
 \Sigma(P)=\bigl(\eta\theta_j(P)\bigr)_{j\in J}.       \tag{1.3}
\]

Repeated physical slots remain separate entries in (1.3), even when two
substitutions happen to agree.  In particular, (1.3) is not a single action
on an already aggregated physical module.

## 2. Endpoint-signature theorem

Assume the v470 base gate

\[
       \eta\theta_j(r_s)=1                            \tag{2.1}
\]

for every reached seed \(s\) and every \(j\in J\).  Thus all literal leaves
and all graph roots have endpoint one.  For a signature \(\tau\), put

\[
 \bar\mu_{s,\tau}
   =\sum_{P:\,\Sigma(P)=\tau}\mu_{s,P}.               \tag{2.2}
\]

### Theorem 2.1 (signature coalescence)

For every occurrence \(j\),

\[
 D_{\eta\theta_j}(C_1)
 =\sum_{s,\tau}\bar\mu_{s,\tau}\,
      \tau_jD_{\eta\theta_j}(r_s).                   \tag{2.3}
\]

Here (1.2) includes the separately authenticated literal terms of
\(C_{<1}\) and the selected update below \(C_T\), in the complete root order.

#### Proof

Task611 accepted v470's exact leaf formula

\[
 D_{\eta\theta_j}(C_1)
   =\sum_{s,P}\mu_{s,P}\,
      \eta\theta_j(P)D_{\eta\theta_j}(r_s).           \tag{2.4}
\]

If \(\Sigma(P)=\Sigma(P')\), then in particular
\(\eta\theta_j(P)=\eta\theta_j(P')\) for each registered \(j\).
Regrouping the finite sum (2.4) in the characteristic-three Fox module gives
(2.3).  No factors of the source word are reordered: only their evaluated
module rows are regrouped after every endpoint premise has been checked.
\(\square\)

The signature must contain all registered occurrence endpoints.  Equality
of one PSL component, one character, one physical slot, or one aggregated
row is insufficient.  Conversely, no derivative of \(P\) is needed: it
cancels in the conjugate formula once (2.1) holds.

## 3. Prefix-trie computation of exact signatures

The set of exact paths in (1.2) is finite.  Build the deterministic prefix
trie of their freely reduced letter lists, retaining a terminal pointer to
every original exact key.  Starting at the eleven identity endpoints, an
edge labelled by \(x^{\pm1}\) or \(y^{\pm1}\) multiplies each occurrence
endpoint by its registered marked image.  Hence every trie edge is evaluated
once and every terminal receives exactly (1.3).

This trie is a current-quotient evaluator, not source syntax.  Its receipt
must bind:

1. the Task601 manifest and complete-root digest;
2. the independently recomputed exact-path map (1.2);
3. the ordered list of registered occurrence maps;
4. every terminal path-to-signature assignment; and
5. the nonzero table (2.2).

The checker recomputes the trie or evaluates every exact path independently.
An implementation may discard internal trie endpoints after their children
are complete.  It may not delete the corresponding edges of \(\mathcal G\),
and signature cancellation at the current quotient says nothing about a
refinement.

## 4. Bounded complete precision-two join

The result-dependent consumer now has the following exact order.

1. Authenticate the Task595 MEMBER decision, the Task601 producer payload
   and independent checker receipt, the sealed prepare/four blocks, the
   literal dictionary, all physical transcripts and (1.1).
2. Independently traverse the canonical graph from the 3,317 registered
   roots without coefficient pruning.  Separately run the adjoint recurrence
   and compare its exact-path table with the exported derived table.
3. Check (2.1).  The conservative ceiling remains \(44\cdot11=484\)
   marked endpoint equalities.
4. Compute (1.3)--(2.2).  Evaluate each reached compact seed once through
   precision two and apply the registered occurrence actions once per
   nonzero pair \((s,\tau)\).  Apply occurrence prefixes, signs, PB3 maps and
   physical aggregation only in their pinned order.
5. Independently evaluate the authenticated target \(T_{\leq2}\).  With
   \(R_{\leq2}\) denoting the replay of (1.1), first require

   \[
   \operatorname{gr}_0(T-R)=0,\qquad
   \operatorname{gr}_1(T-R)=0,\qquad
   \operatorname{aux}(T-R)=0.                       \tag{4.1}
   \]

   These are all 32,260 registered lower coordinates: 8,064 degree-zero,
   24,192 degree-one and four auxiliary coordinates.  Compare the selected
   update's degree-one row separately with the Task601 physical replay and
   the exact Task595 MEMBER equation.
6. Only after (4.1), define

   \[
   \rho_2=\operatorname{gr}_2(T_{\leq2}-R_{\leq2})
       \in\mathbf F_3^{48,384}.                       \tag{4.2}
   \]

   Pack (4.2) as exactly 12,096 base-three bytes and record its support,
   sparse digest and packed digest.

The output is a fresh residual for the target-independent grade-two fibre.
It is not a grade-two MEMBER result.  In particular, the consumer must stop
after sealing (4.2); it cannot interpret a residual as a successful lift.

## 5. Exact resource shape

Let \(L\) be the number of nonzero exact keys in (1.2), let \(U\) be the
number of distinct trie prefixes, and let

\[
 G=\#\{(s,\tau):\bar\mu_{s,\tau}\ne0\}.              \tag{5.1}
\]

Then \(G\leq L\).  The graph and adjoint work is \(O(V+E)\), signature work
is \(O(11U)\) finite-group multiplications, and dense precision-two action is
charged to \(G\), not to all SLP nodes or to the sum of expanded word
lengths.

With dense `uint8` rows, one compact-seed tuple has

\[
 24,192+72,576+145,152+8=241,928                    \tag{5.2}
\]

bytes.  Caching all 44 therefore uses 10,644,832 row bytes, before ordinary
array metadata.  A streaming evaluator additionally needs one acted seed
tuple and the four physical accumulators, not one ambient row per graph node
or per path.  Exact paths and signatures may be streamed into sorted compact
records.  Time or memory exhaustion is `UNKNOWN_RESOURCE`, never a negative
mathematical decision.

## 6. Independence and claim boundary

The narrow producer may reuse the precision-two affine kernels whose
mathematics passed Task568, but a checker must implement the endpoint,
truncated-polynomial, action, target and aggregation arithmetic independently
and must not trust an exported leaf or signature table.  The earlier
Task568 repair obligations concerning a shared floor helper apply to this
checker.  The unrelated unaccepted grade-two closure and resumable-join code
is not needed to compute (4.2).

```text
TASK611/V470 LEAF FORMULA:                    PAPER-AUDITED PASS
EXACT PATH -> COMPLETE ENDPOINT SIGNATURE:    PAPER-CLOSED
SAME SIGNATURE -> SAME CURRENT FOX ACTION:    PAPER-CLOSED
SOURCE GRAPH REPLACED OR PRUNED:              NO
MAXIMUM BASE ENDPOINT CHECKS:                 484
DENSE ACTION COUNT:                           G <= NUMBER OF EXACT LEAF KEYS
FRESH RHO2 FROM AN ACCEPTED TASK601 PAYLOAD:  CONSTRUCTIVELY SPECIFIED
ACTUAL TASK601 PAYLOAD / RHO2:                NOT YET PRODUCED
GRADE TWO / COMPLETE FIRST RUNG:              NOT DECIDED
A0 / COMMON / COFINAL LIFT / FAKE / IHARA:    NOT DECLARED
verified:                                      false
```

`R07_ENDPOINT_SIGNATURE_PRECISION2_CONSUMER_V471_CANDIDATE`

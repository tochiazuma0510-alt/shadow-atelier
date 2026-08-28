# R07 lossless mixed-echelon checkpoint factorization v288

Author: Sol / 2026-08-29

Status: paper-grade state/restore theorem for A4-v5 and, mutatis mutandis,
the DAG-native part of A0-v9.  It identifies the finite state that permits a
real continuation without replaying completed authority rows or completed K
actions.  It does not execute either implementation, accept a checkpoint,
compute A4 closure, or construct a compatible lift, fake certificate, or
Ihara witness.  `verified=false`.

## 1. Deterministic transition state

Fix the authenticated authority and all arithmetic/source identities.  At a
row frontier \(r\) and K-action cursor \(c\), define the semantic state

\[
 \Sigma_{r,c}=(B,L,\mathcal E_B,\mathcal E_L,\mathcal W,
                \mathcal R,Q,c,\mathcal A,\mathcal M,
                H_r,T_r,C).
\tag{1.1}
\]

Here:

- \(B\) is the chronological raw boundary roster, including each normalized
  pivot, raw row, discrepancy ledger, provenance tag, and rank-rise relation;
- \(L\) is the chronological ordered K roster, including its raw and
  normalized rows, discrepancy, word-DAG node, and exact \(Q,c,s\) ancestry;
- \(\mathcal E_B,\mathcal E_L\) denote the two deterministic sparse echelon
  states obtained from those rosters;
- \(\mathcal W\) is the topologically ordered hash-consed word/ledger DAG;
- \(\mathcal R\) is the active translated-column registry derived from the
  raw boundary owners;
- \(Q\) is the queue of K indices and \(c\) its processed-parent cursor;
- \(\mathcal A\) is the chronological list of the four processed signed
  actions for every parent before \(c\), including MEMBER or rank-rise
  relation data;
- \(\mathcal M\) is the corresponding partial action-column table;
- \(H_r\) and \(T_r\) are the completed row and bridge digest prefixes; and
- \(C\) consists of counters, epoch/event digest chains, terminal counts, and
  the exact next-state canary.

An implementation may omit \(\mathcal E_B,\mathcal E_L\) as serialized
objects because they are deterministic functions of \(B,L\).  It may also
omit \(\mathcal R\) if it reconstructs it once from the literal occurrence
owners of \(B\).  It may not omit the lossless data needed for those
reconstructions and replace them by a digest.

## 2. Local validation of a serialized state

The restore validator performs the following finite checks.

1. Authenticate the physical checkpoint, authority, code and source
   identities, resource envelope, schema, and self seal.
2. Validate every DAG node in topological order: opcode, earlier operands,
   scalar, capped length, hash-cons key, exact ten-state recurrence, and
   immutable discrepancy-ledger recurrence.  A source node also binds its
   literal word.
3. Insert the chronological \(B\) and \(L\) raw rows into fresh independent
   sparse echelons.  At every insertion compare the stored pivot, scale,
   relation, raw discrepancy, and rank transition.  No authority word or
   translated-column correlation is evaluated in this step.
4. Reconstruct or validate the active registry from the literal boundary
   occurrence owners and compare its complete key/digest/count canary.
5. Require every queue entry to name an earlier K item, \(0\leq c\leq|Q|\),
   and exactly four chronological action records for each processed parent.
   Replay each stored MEMBER or rank-rise relation against the restored
   echelons, and compare the partial action columns and action event chain.
6. Require \(|H_r|=|T_r|=r-1\), validate their prefix digests, chunk
   boundaries, terminal counts, event chains and counters, and recompute the
   next-state canary from the restored ranks, pivot rosters, registry digest,
   next row, queue length, and cursor.

These checks use sparse row arithmetic, bounded DAG recurrences, and literal
static occurrence data.  In particular they do not call the completed-row
assembler, source-word evaluator, active-dual solver, full-D correlation, or
completed K-action transition.

### Lemma 2.1 (ECHELON RECONSTRUCTION)

If the chronological normalized row, pivot, scale and relation checks in
item 3 pass, then the reconstructed echelons equal the echelons immediately
before the original next transition.

#### Proof

Start with the unique empty echelon.  Sparse reduction and the pinned pivot
order are deterministic.  Induct on the chronological roster.  At a MEMBER
step the replayed coefficient relation gives the same zero remainder and
does not change the basis.  At a rank-rise step the stored normalized row has
the same pivot and scale, so inserting it makes the same next echelon.  The
induction applies separately to the raw boundary and ordered K rosters and
therefore to their combined reductions. \(\square\)

### Lemma 2.2 (DAG AND QUEUE RECONSTRUCTION)

If items 2 and 5 pass, every restored K word, discrepancy and processed
action column has the same literal/algebraic value as at the saved frontier,
and the next unprocessed action is uniquely determined by \((Q,c)\).

#### Proof

Topological induction proves equality of every word/ledger node from its
source value and child recurrences.  Each K item names one such validated
node.  Queue indices therefore name the same ordered K items.  There are
exactly four signed actions in the pinned order for every processed parent;
their replayed relations determine the stored columns.  Hence the first
missing parent/action pair is a deterministic function of \((Q,c)\).
\(\square\)

## 3. Composable row and bridge owners

Opaque implementation hash state must not be serialized.  For each completed
authority row define

\[
 h_i=\operatorname{SHA256}_{\rm canon}
       (\operatorname{ordinal}_i,\operatorname{layer}_i,w_i,\rho_i),
 \qquad
 t_i=\operatorname{SHA256}_{\rm canon}(\operatorname{BridgeTrace}_i).
\tag{3.1}
\]

The public complete and chunk owners are

\[
 H=\operatorname{SHA256}_{\rm canon}([h_1,\ldots,h_{6441}]),
 \qquad
 T=\operatorname{SHA256}_{\rm canon}([t_1,\ldots,t_{6441}]),
\tag{3.2}
\]

with a chunk digest obtained by applying the same formula to the exact
chronological slice.  A checkpoint stores only the completed fixed-size
prefixes and their cursors/canaries.  V286 proves that each \(t_i\) is formed
during the existing ten-state row pass.

### Lemma 3.1 (PREFIX COMPOSITION)

Appending independently recomputed \(h_r,t_r\) to authenticated prefixes
produces exactly the canonical owners in (3.2); no completed row value or
opaque SHA implementation state is required.

#### Proof

The operands of (3.2) are canonical ordered lists of fixed digests.  List
concatenation at the recorded cursor is associative, and canonical encoding
depends only on the resulting ordered list. \(\square\)

This versioned digest ABI is preferable to concatenating separately encoded
objects without JSON-list delimiters: the latter is neither the canonical
encoding of a list nor safely resumable from fixed digest prefixes.

## 4. Lossless continuation theorem

### Theorem 4.1 (NO-PREFIX-REPLAY RESTORE)

Suppose a checkpoint contains the lossless data of (1.1), passes all checks
in Section 2, and its row/bridge prefixes obey Section 3.  Then starting the
deterministic A4 transition at its recorded next row/action yields the same
future semantic states and terminal as an uninterrupted run from the same
authority, until either run meets a resource or physical-input stop.

#### Proof

Lemmas 2.1 and 2.2 give equality of the two algebraic states at the frontier.
The active registry, event chains and next-state canary checks give equality
of every remaining transition input.  The next authority row or action is
fixed by \((r,Q,c)\).  The row assembler, oracle query, correlation selection,
rank update, DAG recurrence, queue append and event update are deterministic,
so one transition produces equal states.  Induction proves equality for all
future transitions.  Lemma 3.1 proves equality of the final digest owners.
Resource and physical stops are excluded because they depend on the host and
opened files, not solely on the mathematical state. \(\square\)

The theorem forbids a purported restore which calls the row consumer on
rows \(1,\ldots,r-1\) or calls the action loop on parents
\(1,\ldots,c\).  Such a route may compare a replay digest, but it has restarted
the completed work rather than restored it.

## 5. Checkpoint cadence and cost

Let \(S_{r,c}\) be the serialized state size and let \(P_{r,c}\) be the total
sparse support of the stored B/K rosters and relations.  Restore costs

\[
 O(S_{r,c}+P_{r,c}+|\mathcal W|+|\mathcal R|),
\tag{5.1}
\]

with no term for completed row-piece evaluation, completed dual correlation,
or completed K actions.  Validation work must have separate resume counters;
it must not silently double the original semantic meters.

Serializing the whole growing state every 64 rows can itself dominate the
linear evaluator.  A sufficient bounded cadence is: one prefrontier owner,
the authenticated row-chunk ends \(1024,2048,3072,4096,5120,6144,6441\),
bounded K-queue milestones, and a clean terminal/resource-stop owner.  Every
write is pre-sized, capped, temporary-first, flushed, atomically replaced and
directory-synced.  A different cadence is admissible only with an explicit
cost bound.

## 6. Evidence boundary

The producer's valid restore proves continuity of its own computation, not
independent acceptance.  The checker must independently rebuild the A4
mathematics from the authenticated authority (using its reverse DAG and its
own echelons) and compare the terminal semantic owners.  It may have its own
checkpoint implementation, but it must not accept the producer checkpoint as
the K-basis proof.

```text
LOSSLESS MIXED-ECHELON/DAG RESTORE STATE:       PAPER PROOF
COMPOSABLE ROW/BRIDGE DIGEST PREFIX:            PAPER PROOF
COMPLETED ROW/ACTION PREFIX REPLAY NEEDED:      NO
A4-v5 PRODUCER/CHECKER IMPLEMENTATION:          IN PROGRESS
ACTUAL A4 CLOSURE / ORDERED K BASIS:            NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA:                 NONE
```

`R07_LOSSLESS_MIXED_ECHELON_CHECKPOINT_FACTORIZATION_V288_PAPER_GRADE`

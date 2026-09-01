# R07 two-level owner direct-restore checkpoint theorem (v421)

Author: Sol / 2026-09-02

Status: paper/ABI theorem repairing the rejected Task459 v1 transport.  It
does not assert an A5 result, compatible lift, fake, or Ihara witness.
`verified=false`.

## 1. Scope and the rejected replay model

Let the compact two-level search have state

\[
 S=(S_K,S_5,i_s,i_K,i_5),                                  \tag{1.1}
\]

where `i_s` is the completed compact-seed ordinal, `i_K` is the number of
completed four-action K parents, and `i_5` is the number of completed
four-action A5 pivots.  A closed transition is one seed or one whole
four-action parent batch.  No checkpoint is taken in the middle of such a
transition.

Task459 v1 did not restore (1.1).  It reconstructed an empty owner and reran
all transitions up to the saved cursors.  If a wall-time stop occurred near
the cap, the same cap could be consumed again before the saved frontier was
reached.  Therefore that object was a replay recipe, not a progress-preserving
checkpoint.

The replacement must restore only rank-raising owners and selected boundary
columns.  Rejected candidates are not mathematical state: after their closed
cursor has advanced, their only persistent data are a digest/counter and, for
a K dependency, its exact D+K reduction ledger.

## 2. K-state restoration already present in v17

The accepted actual A4 v17 arithmetic exposes the following frozen
operations:

```text
restore_word_dag(words, saved_word_ledger_dag)
restore_basis(basis, saved_echelon_state, words)
validate_queue_prefix(...)
```

Its native `checkpoint_payload` identifies the sufficient K state:

```text
B_roster, B_ledgers, boundary_ledgers, combined_ledgers
B_coefficients, B_formals, K_roster
boundary_echelon, echelon_rebuild, insertion_events, active_registry
word_ledger_dag
oracle_records, query_event_chain, live_duals, dual_event_chain, epoch_digest
queue, queue_head, completed action records and action event chain
```

### Lemma 2.1 (K direct restore)

Fix the authenticated Task198 authority, `Runtime`, and `BoundaryLedger`.
Suppose the fields above pass the v17 schema, topology, echelon, recurrence,
ledger, queue-order, and digest gates.  Applying `restore_word_dag`, then
`restore_basis`, then the oracle/event/queue validators produces the same
live mixed span \(D+K\), the same word-bearing K roster, and the same next K
action as the original closed state.

#### Proof

`restore_word_dag` rebuilds the topologically ordered hash-consed DAG and
checks every opcode, child, length, literal owner, and discrepancy ledger.
`restore_basis` replays the chronological B/K rank rises into fresh boundary
and combined echelons and compares the saved rows, ledgers, formals, active
registry, and K owners.  `validate_queue_prefix` checks exactly four signed
actions for each completed parent and reconstructs their quotient columns.
Thus no rejected candidate is needed to determine the span or next frontier.
The three routines determine all fields used by the next `Oracle.query` and
`accept_k`. \(\square\)

The compact owner may wrap this state in a Task459-specific schema, but it
must not replace these v17 restorers by handwritten sparse arithmetic.

## 3. A5 sufficient state

For A5 retain the following canonical data.

1. The authenticated Task193/Task198 identities and compact-roster digest.
2. The topologically ordered proof DAG.
3. Accepted literal A5 sources only, each with source id, word, origin, and
   word digest.  All attempted source words also contribute to a canonical
   dedup digest set, but rejected words are not stored literally.
4. An ordered `pre_insertions` log.  Each entry contains its proof node,
   canonical pivot, row digest, and source/action owner.
5. An ordered `joint_insertions` log.  An entry is either the projection of a
   retained pre pivot or a selected typed PB column with block, relation,
   translation word, proof node, pivot, and row digest.
6. The pre/joint queues and closed cursors, ordered selected-PB ledger, target
   remainder digest, and exact ranks.

### Lemma 3.1 (A5 direct restore)

Construct a fresh actual `DirectEngine` from the authenticated authority and
Task193 package.  Rebuild the proof DAG topologically.  Recompute every
accepted source seed and every retained action row from its proof owner, and
insert only the ordered `pre_insertions`.  Then replay `joint_insertions`,
using `project` for pre entries and `translated_outer_boundary` for PB
entries.  If every pivot, row digest, proof owner, selected-PB signature,
rank, queue, cursor, and target-remainder digest agrees, the resulting
`pre`, `joint`, proof, source, boundary, and frontier state is extensionally
equal to the saved closed A5 state.

#### Proof

An echelon state is determined by its ordered independent insertions.  Every
pre insertion is recomputed by the unchanged actual occurrence/action map,
not trusted as a sparse row.  Every joint insertion is either its unchanged
projection or an unchanged actual translated PB column.  The proof DAG fixes
coefficient ancestry; chronological PB translation words recreate dynamic
outer-universe labels before their rows are compared.  Rejected candidates
change none of these objects.  Queue order is the insertion order of accepted
pre pivots, so its checked closed cursor fixes the next action. \(\square\)

This restoration costs accepted rank rises plus selected PB columns.  It does
not rerun all compact/K candidates and does not retain rejected literal
traces.

## 4. Atomic progress and resource semantics

Before useful seed 1, write a sealed `BOOTSTRAP` state after input identities
are known.  If authenticated runtime construction must be repeated, no useful
search progress is lost.  After construction, write a sealed `READY` state.
Thereafter the last durable state is replaced only after a whole seed or
four-action batch closes.

If a resource stop interrupts an open transition, the working mutation is
discarded and the already existing last closed checkpoint is reported.  A
resume directly restores that checkpoint and starts its next transition.

Wall time and RSS are per-process host caps and restart after direct restore;
their prior segments remain in a history ledger.  Semantic operation/object
counters remain cumulative.  Consequently a wall-time stop can advance under
the same cap, while a semantic-operation cap may require an explicitly larger
future cap; it never requires replaying completed candidates.

### Theorem 4.1 (honest two-level continuation)

Under Lemmas 2.1 and 3.1, a sealed closed checkpoint determines the exact next
two-level transition.  Repeated resource-bounded runs form one deterministic
search prefix, with no repeated completed candidate and no loss of a closed
rank rise.

#### Proof

Induct on closed transitions.  The base `READY` state is the freshly
constructed owner.  At the inductive step, direct restoration gives the same
state and next cursor.  Determinism gives the same next transition; atomic
replacement commits it only after completion.  An interrupted transition
leaves the preceding closed state unchanged. \(\square\)

## 5. Early MEMBER and receipt dialects

The v419 schedule offers every literal candidate to A5 before its K query.
If this produces MEMBER, the K action record has no K query owner.  It must
record

```text
query_event = null
a5_terminal_source_id = <exact source id>
```

and the independent checker must bind that source to the parent/letter edge.
It is forbidden to point at `len(k_events)-1`, which may be an unrelated
earlier event.

Producer receipts use one canonical producer seal field.  Checker verdicts
may use a distinct checker seal field, but the checker must call the matching
producer-seal verifier on producer input.  UNKNOWN_RESOURCE must bind the
physical closed checkpoint; UNKNOWN_INPUT has no mathematical claim.

Driver input paths are canonical relative paths contained in `ci/in`, with a
strict character allowlist and shell-safe argument construction.  No glob,
`..`, control character, or unquoted interpolation is accepted.

## 6. Acceptance gate

```text
actual v17 restore_word_dag / restore_basis used for K
actual Task456 operations used to rebuild A5 retained insertions
BOOTSTRAP and READY checkpoints precede useful search
closed seed/four-action atomicity
direct restore; no seed-1 replay to saved cursor
only accepted literal sources retained; rejected words digest-only
early MEMBER query_event=null checked independently
matching producer/checker seal dialects
strict ci/in path and shell quoting
UNKNOWN carries no lift/fake/Ihara claim
```

`R07_TWO_LEVEL_DIRECT_RESTORE_CHECKPOINT_V421_PAPER_GRADE`

# Luna task 466 -- honest direct-restore compact K/A5 owner v2

Role: Luna implementation only.  Do not run production, dispatch GHA, edit
workflows, commit, push, or touch files outside the four outputs below.

Task459 v1 is rejected.  Its actual arithmetic and v419 immediate schedule
may be retained, but its receipt seal, checkpoint, early-terminal ancestry,
dependent-trace retention, and driver path transport must be replaced under
`sol/proof_r07_two_level_direct_restore_checkpoint_v421.md`.

## 1. Required outputs

Create only:

1. `search/d972_r07_compact_k_a5_two_level_owner_v2.py`;
2. `crosscheck/check_d972_r07_compact_k_a5_two_level_owner_v2.py`;
3. `search/d972_r07_compact_k_a5_two_level_owner_gha_driver_v2.g`;
4. `sol/luna_reply_466_r07_compact_k_a5_two_level_owner_v2.md`.

Do not modify the unadopted Task459 v1 files.

## 2. Frozen arithmetic retained from v1

Exact-pin the Task459 v1 sources as an implementation reference:

```text
producer 37897 bb66f16b85c9d8652f32e70a8360c6f085e6b4fb258307ec75020206c8833612
checker  37587 95954bc8c6f2b190d373491d8cf2592dd272c0fcb400774851dcfd09daab8107
driver    4932 ce9bab391d52b2614656385447679abecb90979c197140839cfea6cd9f9c3552
```

Retain its exact Task411, A4-v17/v23, Task456-v5, Task193-v5, and Task198
pins.  Retain the actual 44-word reconstruction, actual quotient oracle,
immediate A5 schedule, only-K-pivot spawning, actual target/PB arithmetic,
and MEMBER/NONMEMBER independent arithmetic replay.  Do not introduce a new
coordinate model.

## 3. K checkpoint state

Use the actual v17 `restore_word_dag`, `restore_basis`, and queue-prefix
validation ABI.  The v2 checkpoint must carry every v17 field needed by those
routines: word DAG, B/K rosters, both echelon states, all boundary/formal
ledgers, insertion/query/dual chains, epoch, active registry, K queue/cursor,
and completed four-action records.  Version the enclosing schema and bind all
physical owners.

Restoration must call the v17 routines and start at the next saved cursor.
It must not call `process_seed(1..saved)` or rerun completed K action parents.

## 4. A5 checkpoint state

Implement v421 Lemma 3.1 exactly:

- topologically checked proof DAG;
- accepted literal A5 sources only, with word/origin/digest;
- digest-only dedup set and counters for rejected candidates;
- ordered pre rank-rise insertions;
- ordered joint insertions, distinguishing projected-pre and translated-PB;
- chronological PB block/relation/translation words;
- pre/joint queues, closed cursors, ranks, selected ledger, and target
  remainder digest.

On restore, build a fresh actual DirectEngine and recompute only these retained
rank-rise/PB rows.  Require exact pivot, row digest, proof owner, PB signature,
rank, queue/cursor, and target remainder equality.  Do not assign unvalidated
sparse rows directly and do not rerun rejected candidates.

If the frozen Task456 Echelon ABI lacks one required deterministic insertion
hook, stop with the exact missing ABI after implementing all independent
parts; do not silently fall back to full replay.

## 5. Atomicity and resource behavior

- Write sealed `BOOTSTRAP`, then `READY`, before useful seed 1.
- Checkpoint only after one whole seed or one whole four-action K/A5 parent
  batch.  On an open-batch stop, retain and report the previous closed file.
- Wall/RSS are per-run; semantic operation/object counters are cumulative.
- UNKNOWN_RESOURCE must contain the physical checkpoint bytes/hash and the
  driver must require that file.  Constructor/bootstrap resource stops stay
  UNKNOWN_RESOURCE, never UNKNOWN_INPUT.
- A resume must directly restore and make one bounded next-transition canary
  before production continuation.

## 6. Seal, ancestry, and compact traces

- Producer uses `self_digest`; checker has a dedicated producer verifier for
  `self_digest` and keeps its own `self_digest_sha256` verdict seal.
- Add a bounded canonical producer-envelope gate so the original mismatch
  cannot recur.
- If immediate A5 MEMBER precedes a K query, record `query_event:null` plus
  the exact terminal source id.  The checker validates that parent/letter
  edge.  Otherwise bind the exact query event.
- For a candidate dependent in both K and A5, retain no literal word.  Keep
  only digest/counters and exact K D+K dependency ledger.  Literal words stay
  only in accepted hash-consed owners needed by future action or MEMBER.

## 7. Driver paths

Accept only canonical `ci/in/<safe-name>` inputs: no `..`, glob metacharacter,
whitespace/control character, slash ambiguity, or shell metacharacter.
Construct shell arguments with safe quoting.  Exact-pin producer/checker,
run one process, and require the closed checkpoint on every RESOURCE terminal.
No fixture/self-test precedes production.

## 8. Bounded local gates

Run only repo-external-cache compile/help/pin checks and tiny non-production
fixtures for:

1. producer receipt seal accepted by the producer-specific checker verifier;
2. direct K/A5 retained-state restore reaches the next cursor without calling
   a completed candidate callback;
3. interrupted open batch leaves the prior closed seal unchanged;
4. early MEMBER uses null K event and exact A5 source edge;
5. dependent rejected word is absent while its digest/ledger remains;
6. path traversal/glob/control/shell mutations are rejected.

Do not run actual production locally.  Report exact pins, any ABI stop, and
state explicitly that no mathematical terminal has been obtained.


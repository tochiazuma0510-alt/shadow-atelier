# Luna reply 191 — R07 `u0/v0` batched boundary-preimage v2

Date: 2026-08-28
Role: bounded mechanical implementation.  No Python, Node, GAP, git, GHA,
network, or full production run was executed locally.

## 1. Governing invariant and objective

The implementation preserves

```text
D = span of every left translate of the 2 PB3 and 11 PB4 boundary rows.
```

The full canonical ACTIVE suffix is processed even after a target becomes a
member.  Target reconsideration is recorded after every processed row, but no
new dual is made before that ACTIVE list is exhausted.  A checkpoint may resume
only its contiguous saved prefix and never skip a suffix row.

## 2. Authorized files and identities

The five commissioned paths only were edited.  Current producer, checker,
driver, and fixture identities are recorded below; the reply's own digest is
reported out-of-band because embedding it would make the self-digest
self-referential.

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_u0v0_boundary_preimage_batch_v2.py` | 91,677 | `6a3d248d8cedb6f662770fb60b7a5e7732f9cd89ecb87382908934d00f675b79` |
| `crosscheck/check_d972_r07_u0v0_boundary_preimage_batch_v2.py` | 68,823 | `8dad4ca4fc0cb3e942c9ea3c7ea0a3da1339f2bbe683953c8518f511f5b85eac` |
| `search/d972_r07_u0v0_boundary_preimage_batch_gha_driver_v2.g` | 9,041 | `3c2a346a95de80a295782455b32e9853f5dd0bfda356614783e25417d2b16803` |
| `search/certs/d972_r07_u0v0_boundary_preimage_batch_selftest_v2_20260827.json` | 1,396 | `fe5e2adbb35d7594ea3ddebff654772a906236067623ac0d5f34bc5ad3e73b34` |
| `sol/luna_reply_191_r07_u0v0_batched_boundary_v2.md` | designated reply | reported out-of-band |

The producer/checker retain exact authenticated task187 and task179 source
pins.  The driver pins the current producer/checker/fixture identities and all
predecessor/arithmetic identities.

## 3. Producer and checkpoint repair map

`search/...batch_v2.py:179-205` serializes the complete transcript, including
`target_reconsideration_log`, by canonicalizing to bytes before touching the
output.  The registered `checkpoint_bytes` cap raises a typed
`checkpoint_serialization` stop before any replace, preserving the last good
checkpoint.  Each new complete correlation first bumps the registered
`oracle_rounds` counter.  `:211-456` authenticates a checkpoint, rebuilds
a fresh rank-zero echelon, recomputes every complete correlation, replays all
retained and dependent rows from literal sources, validates provenance,
dual-pairings, chains, transitions, canonical contiguous prefixes, and the
ACTIVE suffix.  It also reconstructs and compares all load-bearing statistics;
empty completed batches are represented without a fabricated row.  On resume,
the cache is deterministically rebuilt from every replayed literal row before
the suffix, so cache hit/miss statistics cannot depend on an empty process-local
cache.

`...batch_v2.py:465-633` restores only after that replay, re-derives the
pending pre-batch dual, resumes the exact suffix, and keeps the full ACTIVE
batch running after membership.  Every row checkpoint carries the current
target decisions and reconsideration point; stale unresolved/progress state is
rejected.  Authenticated prior boundary-pair and retained-column counters are
restored before scanning the suffix, so resume cannot bypass registered caps.

`...batch_v2.py:80-120` explicitly composes the authenticated task187 wrapper
with its task179 runtime/model ABI, including typed ResourceStop/InputStop
conversion; production therefore cannot accidentally return a wrapper with
missing runtime methods.

`...batch_v2.py:742-1093` is an injected production-shaped noncommutative S3
SELFTEST.  It invokes the same `solve`, checkpoint writer, rank-zero replay,
dependent-chain reconstruction, and resume path.  It also runs a bounded
resource continuation: the completed first batch is checkpointed, the next
boundary-pair cap raises a typed `UNKNOWN_RESOURCE`, and the receipt embeds the
actual continuation checkpoint identity.  The selftest also exercises actual
oracle-round and checkpoint-byte cap stops, verifies that no failed
serialization creates a checkpoint, and validates the external resume
input/output binding.  Its bounded fixture has four ACTIVE rows, three
retained rows, one dependent row in the resumed suffix, two batched
correlations, and literal continuous/resumed receipt comparison.

The production `--resume` path treats the resume argument as input only and
binds `checkpoint_identity` to the newly written continuation path (`--checkpoint`
or the exact output-derived default), so a resource receipt cannot identify
the stale input checkpoint.  Output checkpoints are required to be fresh;
InputStop receipts carry the expected manifest and typed failure detail
without re-authenticating inside the failure handler.

## 4. Independent checker

`crosscheck/...batch_v2.py:204-340` independently rebuilds task179 arithmetic,
targets and occurrence correlations; it replays literal rows, retained and
dependent ancestry, active dual provenance, chronological target decisions,
terminal dual conditions, transcript order, and statistics.  It does not use
producer helpers.  The NONMEMBER terminal functional is chronologically bound
to the exact empty ACTIVE batch's fresh dual, then independently checked for
nonzero target pairing and annihilation of every final retained literal row;
the empty correlation must remain complete and unsampled.  `:321-335` enforces
authenticated UNKNOWN_INPUT/resource schemas, checkpoint identity, registered
phase/cap/value/limit (including `oracle_rounds` and
`checkpoint_serialization:checkpoint_bytes`), verifies a present resource
checkpoint is sealed and input-bound, and enforces the four false claim flags.
`:417-636` independently validates the S3 production bundle, the actual
retained-column transcript, the literal checkpoint prefix, and the embedded
resource-stop continuation (full checkpoint seal, target progress, rows,
dependencies, rank, logs, and caps).

## 5. SELFTEST and destructive controls

The producer routes all seventeen named controls through the actual toy
receipt/checkpoint validators; each mutation is rejected.  The final three
controls exercise actual oracle-round cap evidence, checkpoint-byte cap
evidence, and the safe resume input/output command contract.  The checker
repeats the load-bearing toy replay and validates those cap/contract records
independently.  The toy checks
noncommutativity, canonical ACTIVE order, cancellation, translation source,
classification, dependency coefficients, pivot ancestry, reconsideration log,
stale dual, complete-correlation flags, suffix state, sampled state, and typed
resource-stop handling.

## 6. Driver, caps, and execution status

`search/...batch_gha_driver_v2.g:4-77` uses serial redirected logs, exact-one
producer/checker markers, exact terminal equality, fresh-output rejection, and
the registered wall/RSS/pair/retained/oracle/checkpoint-byte caps.  It accepts
an optional guarded repo-relative `D191Resume`, appends exactly `--resume` while
keeping the output checkpoint distinct, and executes the generated shell,
reads the nonempty sentinel afresh, and emits a mode-specific final driver PASS
marker only after the shell succeeds.  The conservative production caps
remain 19,800 seconds, 8,000,000 boundary pairs, 250,000 retained columns,
and 5.7 GB RSS (with the inherited checkpoint and auxiliary defaults).  The
expected saving is fewer complete dual-correlation rounds; support scans and
all literal row checks remain complete and unsampled.

No GHA run or production decision is claimed by Luna.  Parent Sol owns audit,
execution, and brokerage.

Parent audit run `33103769264` at immutable head
`bc81fb2c7104c778b834f4cf700604fdc877cc2d` exposed a hidden
producer/checker code failure: `set -e` stopped the generated shell before
its diagnostic `cat`, leaving only a missing sentinel.  No math result or
exact failing stage was obtained.  Both driver modes now expose the failed
log before exiting.

BATCHED EXACT BOUNDARY DECISION:              NOT EXECUTED BY LUNA
MATHEMATICAL BOUNDARY SPACE CHANGED:          NO
TASK187 LIVE RUN MODIFIED:                     NO
COMPATIBLE COFINAL LIFT / FAKE / IHARA:        NOT DECLARED

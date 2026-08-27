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
| `search/d972_r07_u0v0_boundary_preimage_batch_v2.py` | 93,042 | `dc258cae05b909df07458e80aa41ae0d7d7dbea44c43bd291980de9e10856830` |
| `crosscheck/check_d972_r07_u0v0_boundary_preimage_batch_v2.py` | 68,826 | `f0823119e1ab69bc2cb58b88f134eef72b169f82c9ce118bea1507036f76a07d` |
| `search/d972_r07_u0v0_boundary_preimage_batch_gha_driver_v2.g` | 9,041 | `5b1289ab44cc0d35fb7a998530044b58ae966d3be3d9ade7e94b3182fd92b481` |
| `search/certs/d972_r07_u0v0_boundary_preimage_batch_selftest_v2_20260827.json` | 1,396 | `fe5e2adbb35d7594ea3ddebff654772a906236067623ac0d5f34bc5ad3e73b34` |
| `sol/luna_reply_191_r07_u0v0_batched_boundary_v2.md` | designated reply | reported out-of-band |

The producer/checker retain exact authenticated task187 and task179 source
pins.  The driver pins the current producer/checker/fixture identities and all
predecessor/arithmetic identities.
The toy-pair and toy-ABI pair repairs previously changed the producer to
92,520 bytes, and the dependency-iteration repair changed it to 92,528
bytes.  The public-checkpoint reload repair changes it to 93,042 bytes;
parent Sol refreshed its SHA and the corresponding driver producer pin.

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

Parent Sol dispatched the diagnostic-wrapper repair as GHA SELFTEST run
`33104145016` at immutable head
`cf8a554b1c7cbaf752a727e5d8790070409deaf3`.  It was queued at
2026-08-27T18:34:27Z.  The run then exposed a producer SELFTEST code
failure/no math result: `_ToyV1.add_scaled` called an unbound/self-referential
`add_scaled` name.  The toy echelon, target, dependency, and chain replay now
use an explicitly bound sparse mod-3 helper; no mathematical result is claimed
from that run.

Parent Sol dispatched GHA SELFTEST run `33105005369` at immutable head
`a5492bae`.  The producer SELFTEST failed because `_ToyEchelon.dual` called
the production three-argument `pair(v1, f, row)` through the global name.
This is a producer SELFTEST code failure with no mathematical or
cross-checked result.  The toy path now uses the directly bound two-argument
`_toy_pair` at dual, literal-row, and terminal-pairing sites, while production
pair semantics are unchanged.

Parent Sol dispatched GHA SELFTEST run `33106272839` at immutable head
`47555350`.  The producer SELFTEST failed in generic `solve` because the
production wrapper called `v1.pair` and `_ToyV1` had no pair ABI binding.
This is a producer SELFTEST code failure with no mathematical or
cross-checked result.  `_ToyV1.pair` is now explicitly bound to `_toy_pair`,
and the toy ABI also provides the generic `build_runtime` entry point.  The
generic solve, replay, and checkpoint ABI calls were statically audited against
the toy class, with production wrapper semantics unchanged.

Parent Sol dispatched GHA SELFTEST run `33106809203` at immutable head
`31c365fad6dcc8acf565d17cf8359f9fd0177262`.  The driver preamble stripped
the required quotes from `MODE:=SELFTEST`, so this was a dispatch/driver
quoting failure before any mathematical path; no mathematical or
cross-checked result exists.

Parent Sol dispatched properly quoted GHA SELFTEST run `33107405883` at
immutable head `1a1b0fe572cdec8cb44f00a1dc2f3470b5da106e`.  Producer execution
then failed at the dependent-row reconstruction because generic `solve`
iterated the production `Echelon.reduce` coefficient dictionary directly
(`for k,c in dependency`), attempting to unpack integer keys.  The production
ABI returns a coefficient mapping, so the scheduler now iterates
`dependency.items()`; this preserves production and toy semantics.  This is
recorded as a producer SELFTEST code failure with no mathematical or
cross-checked result.

The exact correction is at the dependent-column replay site: `Echelon.reduce`
returns `dict[int,int]` in both the authenticated task187 implementation and
the toy implementation, while the reconstruction loop requires key/value
pairs.  Only that loop was changed to `dependency.items()`; no dependency
coefficients, production Echelon behavior, or checker semantics were changed.

Parent Sol dispatched GHA SELFTEST run `33107894570` at immutable head
`ee344abc5960aaabb6ac9d120192aa0063de929b`.  Producer execution reached the
toy mutation controls and failed while resealing `interrupted_checkpoint`:
the replay validator had attached private byte-keyed `row_dict` fields to the
public checkpoint records, so JSON canonicalization raised a non-mathematical
serialization `TypeError`.  The toy bundle now reloads both mutation
checkpoints from their public JSON artifacts after validation, before any
mutation is sealed.  Production checkpoint serialization and replay semantics
are unchanged.  This run is recorded as a producer SELFTEST code failure
with no mathematical or cross-checked result.

Parent Sol dispatched GHA SELFTEST run `33108424569` at immutable head
`617e94c402c41b99738971cb46b2fb04adad2f44`.  Producer SELFTEST passed; the
independent checker then raised `require() takes 2 positional arguments but 3
were given` in its toy checkpoint transcript gate.  The checkpoint-columns
predicate had accidentally been supplied as a third positional argument
instead of being joined to the preceding statistics predicate.  The checker
now combines both predicates with `and` and retains the same diagnostic
message, without weakening the gate.  This run is recorded as producer PASS
but checker code failure with no cross-checked result.

BATCHED EXACT BOUNDARY DECISION:              NOT EXECUTED BY LUNA
MATHEMATICAL BOUNDARY SPACE CHANGED:          NO
TASK187 LIVE RUN MODIFIED:                     NO
COMPATIBLE COFINAL LIFT / FAKE / IHARA:        NOT DECLARED

## 7. Parent Sol authenticated SELFTEST

Parent Sol's final quoted-preamble GHA SELFTEST is run `33108956198` at
immutable head `810a0f376675cf2eecb5b82ee1ae6c70d1a21160`.  It completed successfully
from `2026-08-27T19:32:51Z` to `2026-08-27T19:33:54Z`.  The producer emitted
`R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_PRODUCER_SELFTEST_PASS`, the independent
checker emitted `R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_CHECKER_PASS` with the
registered SELFTEST terminal, and the GAP driver emitted its matching
mode-specific PASS terminal.

The downloaded receipt
`d972_r07_u0v0_boundary_preimage_batch_v2.json` has 47,145 bytes and SHA-256
`b3346bdaa9ee766359855969978a4cf67e50c9af280bbe9158757c8c95d3159c`.
The uploaded `gap-run-out` artifact has ID `9661693116`, size 10,154,751 bytes,
and ZIP digest
`sha256:e6a588d6e889e0c62ccb32a27942cbddfe1fb06274595fbc563adb9508b38702`.

Thus the bounded SELFTEST implementation is **cross-checked**: the producer
and independent checker agree and all registered mutation controls are
rejected.  This does not decide the production boundary membership, does not
construct a compatible cofinal lift, and is not a Lean verification.

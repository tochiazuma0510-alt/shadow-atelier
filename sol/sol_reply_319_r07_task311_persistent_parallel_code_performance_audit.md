# Sol reply 319 — task311 persistent parallel code/performance audit

## Verdict

**REJECT / UNEXECUTED**

This was a static audit of the bytes currently on disk.  I did not run
Python, Node, GAP, GHA, a network operation, or git.  Consequently no runtime
PASS is inferred.  The rejection is already forced independently by several
deterministic SELFTEST/driver defects, by an inadequate production checker,
and by load-bearing performance/resource defects.

For line references below:

- `P` = `search/d972_r07_normalized_exact_common_word_cached_parallel_v4.py`;
- `C` = `crosscheck/check_d972_r07_normalized_exact_common_word_cached_parallel_v4.py`;
- `D` = `search/d972_r07_normalized_exact_common_word_cached_parallel_resume_gha_driver_v1.g`;
- `V3P` = the pinned cached-v3 producer; and
- `V3C` = the pinned cached-v3 checker.

## 1. Frozen audit universe and exact identities

The four new executable/fixture identities actually present are:

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_normalized_exact_common_word_cached_parallel_v4.py` | 74256 | `2eb1f7d932eb46ff22ec6c37b2ee537366f7651950843a23fac4bf3cca02776c` |
| `crosscheck/check_d972_r07_normalized_exact_common_word_cached_parallel_v4.py` | 50557 | `ba00c6fb8b9602304c2785086c5cbeb331d90d8f32124accc5b33b5a0252ae03` |
| `search/d972_r07_normalized_exact_common_word_cached_parallel_resume_gha_driver_v1.g` | 9203 | `fe870f5f0d391f21e84922c4c34d20263d9821a3297252802692338115214823` |
| `search/certs/d972_r07_normalized_exact_common_word_cached_parallel_selftest_v1_20260828.json` | 1313 | `7def0fafacf6703b16f8a40933edc0208da3077d8c59a9e36307f16cf2ef4c19` |

The Luna reply itself is 6096 bytes with SHA-256
`7d7e7cc284772fac6a93be09020a460532bdea1170a74716f8a1ddddc8de1bf0`.
All cached-v3, task303/v5, task298, checkpoint zip/manifest, and v254--v256
pins embedded in `P` agree with the present files.  In particular, the
checkpoint archive and manifest are respectively
`5001811/f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566`
and
`1328/6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302`;
the manifest pins the sole raw member at
`86368039/c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab`.

The three v254--v256 names printed in task319 do not exist literally.  Their
SHA pins uniquely identify the files actually used by `P` and `D`:

- `sol/proof_r07_frozen_dual_boundary_mapreduce_v254.md`;
- `sol/proof_r07_boundary_adapter_state_and_local_provenance_v255.md`; and
- `sol/audit_r07_task192_cumulative_pairs_and_persistent_pool_v256.md`.

Likewise, the named `sol/sol_reply_310_r07_task311_prereg_math_performance_audit.md`
does not exist.  The extant task310 record is
`sol/sol_reply_310_r07_task303_v5_gha_selftest_acceptance.md`.  I used the
SHA-identified v254--v256 files and read the extant task310 acceptance, but
this filename discrepancy should be corrected in the next commission.

## 2. Line-numbered findings

### F1 — BLOCKER: the reported producer identity is stale after an executable rewrite, and the driver does not pin the new quartet

The Luna reply line 25 reports
`74127/7ac78c640a0527b0c103339f898c21ee613f39c5c5efff3a0f839da43c5cc4b9`.
The sole producer now on disk is the 74256-byte object pinned above: a
129-byte size increase and a different SHA.  This is not CRLF normalization
(the current producer has zero CR bytes).  Filesystem metadata also places
the producer's last write after the reply's last write, so the literal cause
is a post-report rewrite of executable source, not a hash-calculation error
on the current object.  The former 74127-byte object is absent; a SHA digest
alone cannot recover the exact old hunk, and I do not invent one.

This discrepancy is fatal for authorization, rather than harmless stale
prose, because `D:39-54` pins only cached-v3, task303/v5, the papers, task298,
and checkpoint inputs.  It does **not** pin the current `P`, `C`, or v4
fixture at all.  `D:33-37` checks only that its own path exists and that two
in-memory strings have expected values; it does not authenticate its bytes.
Thus the very executable whose identity changed after self-report is not
authenticated by the launch boundary.

Repair: issue a new version, recompute identities only after all files are
closed, and place the exact producer/checker/fixture pins in the driver and
in an independently pinned launch manifest.  Pin the driver from that
external manifest/workflow (avoiding a recursive self-hash).  The new reply
must report those final bytes, not the superseded 74127-byte object.

### F2 — BLOCKER: the checked-in SELFTEST baseline is arithmetically inconsistent and uses a noncanonical group alias

For `active_two_shards`, `P:680-687` supplies one matching descriptor with
`h=2` and support values `(3,5,7,9,11,20,15,0)`, all with coefficient one.
The fixture key is `t=(g-h) mod 17` (`P:231-233`).  Both `g=3` and `g=20`
therefore give the selected key `[1,"t01",1]`, so its F3 scalar is
`1+1=2`, not the asserted value 1 at `P:642-647` and in the checked-in
fixture.  `P:793-797` consequently rejects its own serial projection before
a PASS receipt can be produced.  `C:148-153,186-193` independently embeds
the same contradiction.

Moreover, `20` and `3` are two integer representatives of one mod-17 group
element.  A real typed dual is a dictionary keyed by a canonical row key, so
it cannot contain these as two distinct copies of the same `g`.  The fixture
branch merely subtracts integers and never exercises the production
`t=g*h^-1` and `t*h=g` gate (`P:236-246`).  The claimed cross-cut winner is
therefore obtained by a representation alias that the production universe
does not admit.

The other fixture cases do have the advertised serial outcomes:

| case | expanded pairs | direct F3 result |
|---|---:|---|
| `cancel_across_shards` | 4 | `[1,t01,1]` has `1+2=0`; winner `[2,t01,2]` has scalar 1 |
| `nontrivial_lex_winner` | 4 | `[1,t01,2]` precedes `[1,t02,1]` in `(block,t,relator)` order |
| `no_active_key` | 4 | the block-1 and block-2 keys each cancel `1+2=0` |
| three epoch runs | 8 each | distinct coefficient rosters, but the same synthetic shortcut |

There are 12 case runs plus three epoch runs in one pool and 23 receipt
mutations.  The 23 mutations are non-no-op changes to the sealed semantic
payload, but they cannot rescue an invalid baseline and do not exercise the
real runtime cache/local-provenance path.

The literal mutation roster, in fixture order, is:

```text
omitted_shard, duplicated_shard, overlapping_interval, gap,
permuted_pair_order, wrong_dual_digest, wrong_descriptor_digest,
changed_coefficient, changed_translation_key, changed_contributor,
wrong_partial, wrong_mod3_merge, zero_kept_active, wrong_lex_winner,
wrong_direct_scalar, wrong_pair_count, stale_epoch,
worker_failure_accepted, incomplete_batch_checkpointed,
single_process_true, worker_count_outside_range, pid_replacement,
dishonest_rss
```

Each changes the producer's semantic digest before resealing
(`P:1143-1163`), and the checker independently constructs a changed semantic
payload (`C:690-775`).  They are therefore not counted no-op/reseal controls.
They are nevertheless post-hoc receipt mutations: there is no live timeout,
partial-return, worker-hang, close-failure, or failed-epoch counter injection.

Repair: use canonical group elements and explicitly check inverse,
multiplication, serialization, and `t*h=g` in SELFTEST.  Test concentrated
expanded-pair sharding without duplicate representations; use a separate
multi-descriptor case for cross-shard cancellation/winner provenance.  Then
derive, rather than hand-copy, the expected scalar in both producer and
independent checker.

### F3 — BLOCKER: SELFTEST driver and checker terminal grammars disagree deterministically

In SELFTEST, `C:1067-1068` prints the checker marker and then
`R07_..._CHECKER_TERMINAL PASS`.  `D:119-124`, in both modes, requires and
extracts a line of the form
`R07_..._CHECKER_TERMINAL terminal=...`.  Therefore the driver cannot reach
its sentinel even if the arithmetic baseline is repaired.

Repair: use one exact terminal syntax in both modes, or branch the driver's
exact-one grammar by mode.  Retain exact-one producer/checker lines and exact
terminal equality after the syntax is unified.

### F4 — BLOCKER: every nontrivial production receipt is rejected by a chained-comparison bug

`C:997-999` says

```python
receipt["minimum_three_distinct_epochs"] == len(distinct) >= 3
```

Python parses this as two chained comparisons:
`flag == len(distinct) and len(distinct) >= 3`.  A Boolean cannot equal an
integer of at least three, so the condition is false for every possible
production history.  Only the earlier `inner_receipt is None` return at
`C:870-884` avoids this code.  Hence no actual cached-v3 production result can
be accepted.

Repair: write an explicitly parenthesized Boolean comparison, and separately
state whether fewer than three completed epochs is an accepted honest
resource stop or a non-authorization result.

### F5 — BLOCKER: v4 is not extensionally equivalent to v3 on empty or small expanded rosters

The serial owner returns `None` when its active set is empty, including when
there are no matching typed support pairs (`V3P:1023-1057`).  `P:1398-1400`
instead rejects an empty expanded roster.  For `0 < N < worker_count`,
`P:201-207,441-442` also rejects rather than returning the v3 answer.  These
are valid inputs to the v3 operation and no invariant in the authenticated
owner proves they cannot occur in later dual epochs.

For `N >= worker_count`, the static algebra is otherwise faithful: descriptor
outer/support insertion order is retained (`P:1318-1349`), runtime keys use
`g*h^-1` and check `t*h=g` (`P:236-246`), shard/parent F3 sums delete zeroes
(`P:219-228,317-330,586-628`), winner order is `(block,t,relator)`, the row is
reconstructed through cached-v3, and the returned provenance fields match
`V3P:1064-1071` (`P:1457-1469`).  Rank, dual, correction, candidate, COMMON,
and checkpoint ownership remain in the authenticated v3 module
(`P:1479-1521`; `V3P:1950-2001,2105-2180`).  PRODUCTION uses the authenticated
checkpoint/v3 path, not the synthetic fixture.

Repair: define honest zero- and short-roster behavior (serial/one-worker
fallback or fewer active shards) and return exactly the v3 `None`/row result.
The physical receipt must describe the fallback truthfully.

### F6 — BLOCKER: timeout, typed failure, and close/join guarantees are not implemented

`P:460-464` uses blocking `Pool.map` with no timeout.  A hung or lost worker
can therefore prevent the post-return wall check forever; there is no typed
partial-return/timeout stop and no last-safe checkpoint transition.

Returned-shard binding failures at `P:468-486` raise `SemanticError`, but the
runtime wrapper catches only `AdapterResourceStop` at `P:1415-1423`.  Such a
failure can escape the v3 `ResourceStop` checkpoint path.  Conversely, every
`AdapterResourceStop`—worker exception, PID replacement, unknown parent RSS,
or aggregate cap—is falsely translated at `P:1420-1423` into an `rss_bytes`
overage with value `limit+1`.  For an aggregate child+parent overage the v3
monitor's parent-only RSS can remain below that number, while `V3C:2353-2355`
requires the recorded monitor RSS to be at least the claimed stop value.
Thus an honest aggregate stop can be rejected by the pinned checker.

`P:487-488` additionally assumes that `Pool.map` assigns exactly one of the
epoch's tasks to every requested PID.  `multiprocessing.Pool` provides no such
sticky assignment guarantee; a fast process may consume two short tasks.
This creates nondeterministic false resource stops, especially for the tiny
SELFTEST shards.

Finally, `PersistentPool.close` sets `closed=True` before `join`
(`P:548-557`).  If close/join raises, the recovery call at `P:1511-1515`
invokes `terminate`, but `P:559-561` immediately returns because `closed` is
already true.  The promised exceptional-exit termination/join is therefore
not guaranteed.

Repair: use an asynchronous batch with a deadline based on the remaining v3
wall budget; on timeout or any incomplete/bad shard, terminate and join the
pool once and stop from the last safe v3 checkpoint.  Give adapter failures
their own typed outer reason instead of forging an RSS cap.  Route work to
stable worker identities explicitly (or require only a healthy stable pool
roster, not a scheduler assignment accident), and implement a state machine
whose close/terminate/join transitions cannot suppress cleanup.

### F7 — BLOCKER: resource accounting and historical counters lose the failed epoch

The v3 boundary counter is bumped only after all workers return, the aggregate
RSS check passes, and merge completes (`P:489-498`).  Work performed in a
failed/discarded epoch is therefore absent from historical counters and can
be repeated after resume without charging the registered 8,000,000-pair cap.
No launched/retried/discarded counters required by v255 are present.

Only successful epochs are appended at `P:520-545` and `P:1438-1456`.
Consequently an `UNKNOWN_RESOURCE` outer receipt omits the current epoch's
worker/RSS evidence.  In SELFTEST the pool always has four children
(`P:1170-1172`), but 2- and 3-worker runs sum RSS only for the PIDs which
returned shards (`P:487-494`), omitting idle live pool children while claiming
the aggregate parent-plus-child policy.

There is also an accepted unbound-sidecar route.  `P:1654-1660` converts many
semantic/I/O failures to an outer `UNKNOWN_RESOURCE`, while `sealed_stop`
contains no checkpoint reference (`P:1580-1604`).  If v3 already left a
sidecar, `C:870-884` accepts the inner-null envelope without checking terminal
grammar or binding that sidecar, and `D:129-133` checks only that some physical
file is nonempty.  This can pass a resource terminal without an authenticated
checkpoint reference.

Repair: charge attempted work monotonically before/at launch and record
committed, discarded, and retried counts separately; record failed-epoch
resource evidence; account for every live child PID; and require every
resource terminal to bind and semantically validate exactly one last-safe v3
checkpoint.  Remove or reject unreferenced sidecars on all other terminals.

### F8 — BLOCKER: the production checker cannot independently check the decisive correlation

The compact epoch record deliberately omits the actual descriptor roster,
typed support, expanded pairs, shard partials, merged accumulator, and
translated row (`P:1438-1456`).  `C:924-999` therefore checks only
self-reported digests and shapes.  In particular, `partial_digest`,
`result_digest`, and `interval_digest` need only be strings
(`C:954-978`); direct scalar is checked only for equality with another
producer field (`C:947`); and local provenance is checked only for field shape
(`C:992-996`).  It cannot recompute roster order, shard F3 sums, the least
active key, `g=t*h`, the row, or the direct pairing.

Calling the pinned v3 checker at `C:893-897` does not repair this gap.  That
checker validates the inner v3 receipt/checkpoint and a positive retained
row, but it has no certificate that the monkey-patched oracle did not omit a
smaller active boundary key.  The SELFTEST checker does replay its synthetic
rosters, but SELFTEST neither enters `RuntimeBoundaryDescriptorCache` nor
tests `_local_provenance`; `P:786-788` merely copies the already retained
synthetic contributor list.

`C:792-828` also compares producer-reported source digests to constants but
does not hash the local checkpoint zip/manifest itself.  Together with F1,
the launch/check boundary is not independently pinned.

Repair: emit a bounded authenticated correlation certificate/sidecar from
which `C` independently reconstructs the actual v3 descriptor/support roster,
the exact interval cover and every sparse partial, the F3 merge and least
winner, local `g=t*h` provenance, translated row, and direct scalar.  Hash the
local source archive/manifest and all current executable inputs in the
checker/launch manifest.  Do not import either producer.

### F9 — BLOCKER: the hot path performs repeated whole-roster encoding and retains unbounded duplicate epoch history

Let

\[
N=\sum_{d\in D}|S_{B(d),c(d)}|
\]

be one epoch's expanded pair count.  Before useful worker arithmetic, `P`
materializes `N` Python dictionaries (`P:1331-1349`).  It canonically JSON
encodes the whole roster four times at `P:1405,1417,1434,1445`.  Across the
shards it performs another four full-roster-equivalent record encodings:
task interval digest, task slice digest, worker slice verification, and
parent interval recheck (`P:210-216,448-458,307-311,470-477`).  It also
constructs slice lists and pickles the aggregate `N` dictionaries through
the pool queue.  Thus the parent/worker plumbing is at least about eight
full pair-record encodings plus one full aggregate pickle per epoch, before
counting interval-index encodings and sparse merge.

Each worker then decodes both `g` and `h` and recomputes `h^-1` for every pair
(`P:239-246`).  Serial v3 unpacked each support `g` once and cached every
descriptor inverse (`V3P:963-969,1024-1045`).  Winning provenance also scans
each relevant support list linearly (`P:1370-1393`) rather than using the
typed support index promised by v255.

This overhead is load-bearing for the observed workload: v256 records 104
descriptors, current support size 1,188, and about 1,086.23 cumulative pairs
per retained column across 2,896 retained columns.  The route is thousands
of short dependent epochs; queueing and repeated JSON/hash work can dominate
the group products even though process spawn was removed.  At the present
dual, the a priori bound is `N <= 104*1188 = 123552`.

More seriously, both `PersistentPool.epoch_records` (`P:399,520-545`) and
`RuntimeBoundaryDescriptorCache.epoch_records` (`P:1305,1438-1456`) append
one record for every epoch.  The latter also retains every winning local
contributor list, and the entire list is copied into the final outer receipt
at `P:1548-1554`.  Memory/receipt size is therefore unbounded in the number
of rank epochs, despite the Luna reply's claim that no all-epoch history is
retained.  The registered resource cap is inert against a receipt/history
allocation that grows before a reliable failed-epoch record can be emitted.

Repair: keep descriptor/group data and compact typed support indexes resident;
send only compact interval/epoch controls, not expanded dict records; compute
each roster/slice digest once in a binary canonical encoding; reuse cached
descriptor inverses and support group objects; and use O(1) lookup for winner
provenance.  Replace both unbounded lists by bounded rolling counters plus a
cryptographic transcript accumulator and only the small evidence required
for the current/last few epochs.  Benchmark the repaired route against serial
v3 on the authenticated current-support shape before requesting production.

### F10 — non-blocking positive observations do not cure the rejection

The code does create a Linux `fork` pool lazily after the live cache exists
and normally reuses it (`P:386-423,1396-1418`).  It does not serially call
`get` per worker, does not rerun the complete correlation in the production
parent, and production workers suppress full contributor histories.  Pair
intervals, rather than the 104 descriptor indices, are divided evenly.  The
outer producer marks physical `single_process=false` and labels inner v3
`single_process` as legacy (`P:1540-1575`).  The checker imports only the
SHA-pinned cached-v3 **checker** under a unique name (`C:778-789`), not either
producer, so helper sharing is avoided.  The GAP source contains no non-ASCII
bytes.  COMMON sidecar removal is delegated to and checked against v3 on the
ordinary successful path.

These are useful pieces, but F1--F9 prevent either a SELFTEST authorization or
a production launch.

## 3. Required next boundary

Do not dispatch the current bytes to GHA.  A new version must repair every
blocker above and undergo a fresh static audit.  Only a future pinned static
PASS could authorize one GHA **SELFTEST**; it would still not authorize
PRODUCTION and would not prove A0.

The mathematical boundary is unchanged:

```text
A0 actual:                         0/1
COMMON word:                       NOT ESTABLISHED
cofinal lift / fake / Ihara:       NO CHANGE / NO CONCLUSION
runtime status of task311 bytes:   UNEXECUTED
```

`TASK319_R07_TASK311_PERSISTENT_PARALLEL_STATIC_AUDIT_REJECT_UNEXECUTED`

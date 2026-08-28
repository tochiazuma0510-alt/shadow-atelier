# Luna task 303 — task297 fixed-dual parallel boundary repair v5

Role: Luna implementation/SELFTEST repair only.  Do not perform mathematical
adjudication.  Do not run Python, GAP, GHA, network, or git.  Parent Sol is the
only execution and git broker.

## 1. Scope and versioning

Task297/v4 is rejected before execution.  Create exactly five new v5 paths:

1. `search/d972_r07_normalized_exact_common_word_parallel_v5.py`
2. `crosscheck/check_d972_r07_normalized_exact_common_word_parallel_v5.py`
3. `search/d972_r07_normalized_exact_common_word_parallel_gha_driver_v5.g`
4. `search/certs/d972_r07_normalized_exact_common_word_parallel_selftest_v5_20260828.json`
5. `sol/luna_reply_303_r07_task297_parallel_boundary_repair_v5.md`

Do not change v3/v4, the sealed task192 checkpoint, workflows, or any other
path.  The `.g` file must be ASCII-only.  Production must remain fail-closed
until a separately authenticated v3-resume adapter is commissioned; this task
is the parallel-kernel SELFTEST repair, not an A0 result.

## 2. Rejected v4 defects which v5 must remove

The v4 baseline is deterministically impossible:

- `active_two_shards` selects a key whose contributor roster does not cross
  the asserted two shards, so the baseline validator rejects it;
- producer `worker_failure_accepted` mutates a top-level field which the
  semantic validator never reads;
- producer mutations are passed through a validator whose still-zero
  mutation summary rejects every mutant independently of the mutated field,
  so the claimed mutation count is circular;
- checker validates shard metadata only for the last loop value `w=4`, while
  mutations alter the `w=2` record;
- checker never rejects the worker-failure field;
- `wrong_direct_scalar` writes the baseline value `1` and is a no-op; and
- the fixture says six cases while the receipt and validators use four.

## 3. Exact repaired semantic contract

Implement a genuinely process-parallel map/reduce for one **frozen dual
epoch only**.  Adaptive rank updates, dual changes, and candidate-word logic
remain outside the workers.

For each worker count 2, 3, and 4:

1. deterministically partition the ordered descriptor interval into a
   complete, disjoint, contiguous cover;
2. use Linux process workers (not threads and not an in-process simulation);
3. record and validate every shard's exact start, stop, count, interval
   digest, frozen-dual digest, full-descriptor digest, partial F3 accumulator,
   contributor list, and explicit `worker_failed=false`;
4. recompute each shard partial directly from its descriptor slice;
5. merge in start order over F3, deleting zero cancellations;
6. choose the exact v3 key order
   `(block, translation_blob, relator_index)`; and
7. recompute the selected scalar directly from the full ordered descriptors.

The independent checker must implement its own serial oracle and shard
replay, and must check **all three worker counts inside the loop**.  It must
not import the producer.

Use four explicitly named baseline cases: a genuine two-shard active winner,
a cross-shard cancellation, a nontrivial lexicographic winner, and no active
key.  The two-shard case must prove that the selected key has contributors on
both sides of the actual `w=2` cut.  Keep two consecutive, different frozen
dual epochs and prove state isolation.  The fixture must name exactly these
four cases and separately state that there are two epoch runs.

## 4. Non-circular adversarial controls

Retain the 20 semantic owners, but rebuild the mutation harness so that:

- every mutation first proves its canonical object differs from baseline;
- each mutant is resealed;
- semantic validation of one mutant does **not** inspect or depend on the
  aggregate `attempted/rejected` summary;
- only after all individual semantic verdicts are obtained is the 20/20
  summary attached and checked; and
- the checker creates and rejects its own mutants, ignoring producer claims.

In particular mutate the actual per-shard `worker_failed` field, inspect it
for every worker count, and change a scalar by a guaranteed nonzero delta
modulo three rather than assigning a possibly equal literal.  Wrong dual,
descriptor, interval, count, partial, contributor, cover, merge, lex winner,
direct scalar, epoch, single-process, and worker-range fields must each be
load-bearing.  Add a mutation-effect digest or equivalent exact comparison
so a no-op mutation is itself a failure.

## 5. Driver and boundary

Pin every v5 input by bytes/SHA and retain the immutable v3 pins.  Generate
one `set -euo pipefail` shell, choose `min(nproc,4)` workers and require at
least two, reject stale outputs, require one exact producer terminal, one
exact independent-checker terminal, equality of terminals, nonempty receipts,
and one exact sentinel.  Do not edit a workflow.

Report final bytes/SHA, the four case outcomes, worker counts, two-epoch
isolation, and independent 20/20 mutation status in the reply.  State
`UNEXECUTED`, `A0 actual 0/1`, and no fake/Ihara conclusion.


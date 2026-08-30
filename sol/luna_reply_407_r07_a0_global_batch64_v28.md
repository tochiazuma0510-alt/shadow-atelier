# Luna reply 407: A0 globally merged batch-64 successor v28

Status: implementation candidate complete; small local fixtures PASS.  No
production-like local run, GHA dispatch, commit, push, or generic-workflow edit
was performed.  The frozen v24--v27 files were not changed.

## 1. Exact files

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_history_free_positive_fast_resume_batch64_v28.py` | 19,149 | `ff26d11c23b45b70a1fc93d481bfd4f3dd66e6c106fd0afae140af81ec01ddf9` |
| `crosscheck/check_d972_r07_history_free_positive_fast_resume_batch64_v28.py` | 8,219 | `0491b3b7ff68a839811869079c7da33cae751f58936c6eef7a4e5ab8724baa99` |
| `search/d972_r07_history_free_positive_fast_resume_batch64_gha_driver_v28.g` | 5,827 | `91cc6d2a103ede50d6ce730ef3774eef9f5b569ba6c4f6530e738f049b382dce` |
| `search/d972_r07_history_free_positive_fast_resume_gha_driver_v29.g` | 515 | `7263cffa6ad9d5dfea6fe007dd85448474fe1b7816f93971fa840edc12b8e857` |
| `.github/workflows/d972-r07-a0-global-batch64-v28.yml` | 4,791 | `0a86f22f6b42981e3e34995bd6696f63fcf1363271a5597c774ce06bc6ed108a` |

The generated production owner is 177,472 bytes with SHA-256
`e6767b9932de937ab33aaa12e8feea0ade48a0ec0f4efb3bba36eecdf0b87a1a`.
The generated checker owner is 135,488 bytes with SHA-256
`7615aaff967b217dfab7beb7120758fd4acb4d21238351940fbd8e521175af01`.

The v29 GAP file is only the generic-`gap-run.yml` adapter.  Its filename
matches the already-registered workflow's authenticated A0 prefix and it reads
the exact-pinned, self-contained batch driver v28.

## 2. Implemented batch contract

The producer is a hash-pinned successor of the final v26 two-phase streaming
owner.  It changes boundary discovery only:

1. The current dual remains frozen for one epoch.  Existing worker slicing and
   the complete descriptor/support-pair convolution are unchanged.
2. Workers return their full nonzero local accumulators.  The parent merges all
   entries globally in `F_3`, removes zeros after cross-worker cancellation,
   then applies the canonical order and takes at most 64.  There is no local
   top-b, sampling, or truncation.
3. Parent materialization now builds one selected-key-to-position map and
   scans the descriptor/support pair stream exactly once for the entire batch.
   Only after that single contributor scan does it reconstruct each selected
   translated row and recompute its frozen-dual scalar.  Thus the parent scan
   cost is `expanded_pair_count`, not
   `expanded_pair_count * selected_count`.
4. The returned payloads are reduced and committed sequentially.  The first
   row is required to raise rank; later zero remainders increment
   `dependent_count` and are skipped.  Every retained row gets a distinct
   symbol, DAG node, row, scalar, and immutable batch/contributor provenance.
5. A convolution failure retains no epoch.  A resource stop during the single
   parent scan retains no row from that batch.  A stop during sequential commit
   retains only the already atomic committed prefix, clears the unused support,
   records a dual rebuild, and lets resume construct a fresh dual.
6. Empty global active sets still enter the existing positive correction path;
   resource stops remain `UNKNOWN`.  `heuristic_discovery_only=true`,
   `exact_cached_resume=false`, all caps, the correction oracle, and the final
   positive acceptance path are unchanged.

Accounting now contains `batch_cap`, `global_active_index_count`,
`selected_batch_sha256`, `materialized_count`,
`retained_independent_count`, `dependent_count`, `dual_rebuild_count`,
`parent_pair_visits`, and `last_parent_pair_visits`.  Per-row batch provenance
also records `expanded_pair_count` and `parent_pair_visits` and requires their
equality.

I also corrected the migration at the actual streaming-resume call site.  The
initial draft had added batch defaults only to the unused whole-DOM restore;
the final source merges them in `_stream_pre_records`, so the authenticated v24
accounting cannot erase the new counters.  The generated owner contains one
pre-record phase and one post-parse phase and contains no call to the legacy
whole-file restore.

## 3. Checker boundary

The checker pins the exact producer above and retains the existing v278 final
positive boundary: selected row reconstruction, dual scalar, complete
contributors, sparse target equality, correction word/exponent, all-seven
replay, and joint-kernel gates.

Following the parent mathematical audit, batch scheduling metadata does not
cause a second full global active-set scan for every selected support row.  It
is checked for exact shape, dual/index/scalar consistency, cap/count bounds,
single-scan equality, and accounting.  The generated checker contains neither
`_BATCH_REPLAY_CACHE` nor a batch-cap call to
`independent_boundary_outcome`.  Global merge/top-64 behavior is instead gated
by the finite implementation fixture below; it is not part of the final common
word proof boundary.

## 4. Small local gates

No production source/checkpoint was decoded.  The following bounded gates
passed:

```text
A0_BATCH64_FINITE_FIXTURE_PASS cap1=PASS span=2 dependent=2 permutation=PASS cancellation=PASS
A0_BATCH64_PARENT_SCAN_FIXTURE_PASS parent_pair_visits=6 expanded_pair_count=6 selected_count=6
A0_BATCH64_MUTATION_FIXTURE_PASS row=REJECT scalar=REJECT contributor=REJECT provenance=REJECT
FINAL_GENERATED_GATES_PASS
YAML_PARSE_PASS
STATIC_TRANSPORT_PASS
```

The finite fixture checks that cap 1 returns the old canonical first column,
batch and repeated-one-column insertion have the same final span, a later
dependent column is skipped while the first raises rank, worker-result
permutation is invariant, and cross-worker cancellation occurs before
selection.  The mutation fixture invokes the generated checker boundary, not a
duplicate predicate.

Both Python entry points compile and their `--help` paths pass.  Both GAP files
are ASCII.  Running each through `./gap.ps1` stops immediately and nonzero at
the expected `task408 missing input` gate because the 1.66 GB prior artifact is
not present locally; no shell or search is launched.

The driver pins producer/checker bytes and hashes, the tracked source ZIP and
manifest, and the prior checkpoint at 1,663,424,241 bytes / SHA-256
`55c463335e89fb7e67a04ec9c0405a8216f6f909b2ce67a0fe7a8a4afaf2014d`.
The actual artifact member basename is correctly fixed as
`d972_r07_history_free_positive_fast_resume_v24_production.json.checkpoint.json`.
Producer/checker pipe statuses, nonempty receipt/verdict, exactly one terminal
each, terminal equality, and the final sentinel all fail closed.

## 5. Dispatch contract

The dedicated workflow candidate pins official GAP 4.16.0, checks out exact
`${{ github.sha }}`, binds prior run `33267817818`, artifact id `9721440597`,
artifact name `gap-run-out`, and prior head
`8227ecd4cb12f7efc8e2419306b847e228a78f36`.  It has 245 minutes total,
producer limits 11,100 seconds external / 10,800 seconds internal, checker
limit 1,800 seconds, and uploads only `ci/out` under the distinct batch name.

Because a newly added dedicated workflow is not dispatchable until registered
on the default branch, the immediate production route is the existing branch
workflow through the v29 adapter:

```text
gh workflow run gap-run.yml --ref <exact-commit-containing-these-files> \
  -f script=search/d972_r07_history_free_positive_fast_resume_gha_driver_v29.g \
  -f preamble='' -f out_dir=ci/out -f timeout_min=245 \
  -f with_pquot_packages=false
```

That adapter name triggers the existing workflow's exact prior-artifact bind
and download.  The self-contained v28 driver then authenticates the actual
member bytes/hash before any producer work.  Generic `gap-run.yml` itself was
not modified.

## 6. Claim boundary

This is a history-free positive-discovery implementation candidate.  It makes
no negative/exhaustion claim.  No A0 common word, uniform lift, fake
certificate, witness-type certificate, or Ihara counterexample is declared.
Production GHA and its independent verdict remain pending.

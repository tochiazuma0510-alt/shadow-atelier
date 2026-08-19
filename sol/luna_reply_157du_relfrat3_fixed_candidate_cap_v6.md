# Luna reply 157du — fixed-candidate cap-calibrated v6

## Result

Implemented the versioned v6 lane in the four authorized files. This is a
resource-cap calibration only: the registered candidate, mathematical
predicate, literal words, translation and pivot orders, blocker retry rule,
transaction semantics, certificates, terminals, and claim boundary are
unchanged from frozen v5.

Exactly two caps changed in both producer and independent checker:

| Cap | v5 | v6 |
|---|---:|---:|
| `total_sparse_group_ring_keys` | 1,000,000 | 4,194,304 |
| `element_pool` | 1,000,000 | 2,000,000 |

Every other cap is byte-for-byte equal to v5. In particular, translations
remain 32,768, sparse pivots 1,000,000, DAG nodes/edges 2,000,000/4,000,000,
section nodes 65,536, a single word/section 100,000, soft RSS 4,831,838,208
bytes, and producer soft wall 18,000 seconds.

The new `element_pool` value is used as the bounded product-cache pair-key
stride only. Pivot order remains `(component, canonical E4 bytes)` and is
independent of pool IDs and cache keys.

## Frozen semantics and cap calibration

The new sources verify the exact frozen v5 pins:

| v5 file | SHA-256 |
|---|---|
| `search/d972_b345_relfrat3_fixed_candidate_v5.py` | `e4675906601714ee16219d747cf95ffef54b19e354228dd6e7d3cd99d59127ea` |
| `search/check_d972_b345_relfrat3_fixed_candidate_v5.py` | `0cb7e0173fe022f304010c64ef89b7200464f4ad8c1e1bc7c3ad4001ffe12246` |
| `search/d972_b345_relfrat3_fixed_candidate_gha_driver_v5.g` | `3bcb19326bfff1e313870a64cca95840b0e581aa1f7c713ee18300faf149261d` |

The receipt contains, and the checker requires exactly, this calibration:

```text
source_run                    32212335985
source_receipt_sha256         c9231ebb8fe65c47107556c6e06873fa68b74e148e1ab248cfada08a699975d4
source_stop_reason            total_sparse_group_ring_keys
source_translations           10809
source_live_sparse_entries    999999
source_element_pool           330011
source_peak_RSS               296407040
old/new sparse cap            1000000 / 4194304
old/new pool cap              1000000 / 2000000
semantics_changed             false
resume_used                   false
```

This is a fresh same-job reconstruction. No v5 basis, blocker value, pool,
DAG, checkpoint, or artifact state is imported or resumed. The checkpoint-1
blocker is reconstructed from the authenticated q3/source data, while its
ordinal/name/component are post-reconstruction drift canaries.

The registered universe remains exactly correction index 1, empty correction,
`m=0`, `lambda=1`, and the frozen row-37/exponent-2 outside roof. The lane does
not build or claim the omitted 4,095 corrections, a global-earliest candidate,
negative completeness, or a global B4-A/B4-B result.

## Receipt and checker changes

Schema, output, progress, checker, and driver markers are versioned to v6.
The receipt records exact peak/cap ratios for live sparse entries, element
pool, pivots, DAG nodes/edges, and sampled RSS. The independent checker
reconstructs those values from the terminal accounting and rejects ratio,
cap, calibration, pin, schema, universe, terminal, or claim drift.

The three existing terminal meanings are unchanged. A nonpositive receipt
must still state exactly:

```text
claim_classification=unknown_not_obstruction
claim_scope=fixed_candidate_only
no_mathematical_obstruction_claimed=true
```

PASS still requires full v5 certificate regeneration and streaming packed-DAG
replay. INCOMPLETE still requires all 32,768 translations. UNKNOWN_RESOURCE
still binds the exact bounded prefix and synchronized resource reason. Raising
the two caps does not strengthen any nonpositive or global conclusion.

## Differential selftest and static audit

The sole combined lightweight selftest was run once:

```powershell
python -B search/d972_b345_relfrat3_fixed_candidate_v6.py --self-test
python -B search/check_d972_b345_relfrat3_fixed_candidate_v6.py --self-test
```

It passed with the exact markers:

```text
D972_B345_RELFRAT3_FIXED_CANDIDATE_CAP_V6_PRODUCER_SELFTEST_PASS universe=1 dictionary_DP_calls=0 targets=50 blocker_ordinal=6 skip_retry_replace=1 transaction_rollback_ID_reuse=1 PASS_regeneration=1 terminals=3 structural_UNKNOWN=1 cap_delta=2 stride_injective=1 cache_neutral=1 old_cap_continue=1
D972_B345_RELFRAT3_FIXED_CANDIDATE_CAP_V6_CHECKER_SELFTEST_PASS universe=1 dictionary_DP_calls=0 targets=50 blocker_ordinal=6 skip_retry_replace=1 prefix_UNKNOWN=1 packed_DAG_replay=1 claim_mutations=6 terminals=3 cap_delta=2 cap_mutations=6 stride_injective=1 old_cap_continue=1
```

Coverage includes the exact two-cap delta, equality of every other cap and the
fixed universe, pair-key injectivity, cache hit/eviction/clear neutrality, an
old-cap toy prefix continuing without pivot/value/order drift, blocker
skip/retry/replacement, transactional rollback, all three terminals, claim
mutations, packed-DAG replay, exact calibration mutations, and cap-ratio
mutation rejection.

Static comparison normalized only the two new values and found the producer
and checker cap dictionaries exactly equal to v5. The active driver contains
no placeholder or non-ASCII byte; every active path, symbol, marker, artifact,
log, and sentinel is v6. Remaining v5 names are solely the required frozen
semantic pins.

## Driver and proposed GHA inputs

The driver retains the separate q3 GAP child and teardown, exact source and q3
artifact SHA gates, stale-output purge, `python3 -u`, `pipefail|tee`, exit
sentinels, unique terminal/checker markers, and final artifact SHA. It pins
v1–v5. `with_pquot_packages=true` is mandatory for the authenticated q3 child.

```yaml
script: search/d972_b345_relfrat3_fixed_candidate_gha_driver_v6.g
preamble: 'D972_B345_RELFRAT3_FIXED_CANDIDATE_V6_RUN:=true;; D972_B345_RELFRAT3_FIXED_CANDIDATE_V6_OUTPUT:="ci/out/d972_b345_relfrat3_fixed_candidate_v6.json";;'
out_dir: ci/out
timeout_min: '330'
with_pquot_packages: true
```

Use the byte-preserving JSON dispatch route. No workflow was edited.

## Resource estimate

This is a source-only estimate, not a production benchmark. With no deep PASS
serialization, producer time is expected to be 4–7 minutes and the complete
job/checker 7–12 minutes. Conservatively allow 45 minutes for a deep PASS
replay. The projected 32,768-translation state is roughly 3.03 million live
sparse entries, 360 thousand pivots, 0.98 million pool elements, and
0.66m/0.48m DAG nodes/edges, within the two raised caps while retaining the
unchanged 4.5-GiB RSS guard. Any different cap reached remains an honest
UNKNOWN_RESOURCE with no obstruction claim.

## Cross-checked GHA run record

The parent broker subsequently dispatched the frozen sources at commit
`4cade81aa37f7df056b97015ca86bf025ec27536`.

Canary run `32214206738` passed with producer, checker, and driver markers each
appearing once. Its `gap-run-out` artifact has ID `9351797000`, size 1,688
bytes, and archive digest
`sha256:2c8995ff81f0a41b5a90351795ff0e389e39e4359cb9a972b055dc0e34ac32ff`.

Full run `32214317453` completed successfully with producer, independent
checker, and driver PASS. Its artifact has ID
`9351964059`, name `gap-run-out`, size 50,897 bytes, and archive digest
`sha256:4c4dde33c752004bb1450ac4c7bac3aac55803e053ea23fdac9a03e5fb18e9ef`.
The receipt SHA-256 is
`cd7cf742ad3304bd87ae54e74a0ab83e18aa85c531b76f2df71949e597640018`.

The cross-checked terminal is
`B345_RELFRAT3_FIXED_CANDIDATE_INCOMPLETE`. The exact completed bounded prefix
is:

```text
translations                   32768
columns                        360448
pivots                         360432
live sparse entries            3072055
element pool                   969407
DAG nodes / edges              669309 / 492108
peak sampled RSS               692957184 bytes
producer runtime               240.388 s
candidate attempts / rollbacks 1 / 1
fixed blocker                  target 6, hexagon_1_coface_0, component 4
blocker pivot                  absent at every checkpoint, including 16384 and 32768
```

This exhausts only the registered translation bound for correction index 1.
It is fixed-candidate-only and `unknown_not_obstruction`: absence of this one
pivot is not nonmembership, a finite-stage obstruction, a statement about
candidates 2–4096, or a B4-A/B4-B conclusion.

## Final sources

| File | Bytes | SHA-256 |
|---|---:|---|
| `search/d972_b345_relfrat3_fixed_candidate_v6.py` | 215,935 | `178c7e63dafba0b9deb8b4e363552ff87a0b7d1c2a120457f593845d56d9d493` |
| `search/check_d972_b345_relfrat3_fixed_candidate_v6.py` | 185,178 | `12c5475c984aa2855c502930169a01cc656ec67507a6aa56d098cd314db011fd` |
| `search/d972_b345_relfrat3_fixed_candidate_gha_driver_v6.g` | 13,585 | `2b36db96d440316292d271c22e662da507dc6afeba20aa0222c8388bab6f4ada` |

No production GAP, Git, GHA, workflow edit, heavy local run, resume, or
checkpoint import was performed.

B345_RELFRAT3_FIXED_CANDIDATE_CAP_V6_READY_FOR_GHA

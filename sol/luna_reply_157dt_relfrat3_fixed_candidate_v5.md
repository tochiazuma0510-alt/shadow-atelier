# Luna reply 157dt — fixed-candidate relative-Frattini v5

## Result

Implemented the versioned fixed-candidate, positive-only lane in the four
authorized files.  Its registered universe is exactly correction index 1,
the empty correction, over the frozen row-37/exponent-2 outside roof and the
20-letter fixed word.  It neither constructs the 4,096-word correction
dictionary nor runs the 46-context dynamic program.

The first candidate attempt is scheduled at checkpoint 1.  Its first fully
reduced missing Fox pivot is reconstructed from the current q3 input and the
live sparse basis; no v4 blocker value is imported.  The following values are
only fail-closed post-reconstruction drift canaries:

```text
target ordinal (one-based): 6
target name:                hexagon_1_coface_0
component:                  4
```

A mismatch in any pin, schema, invariant, reconstructed blocker, or replay is
a hard nonzero failure.  It is never converted to UNKNOWN.

## Frozen pins

The new producer, checker, and driver bind these upstream files and verify
their bytes before production:

| Input | SHA-256 |
|---|---|
| q3 producer `search/d972_b345_q3_chief_v1.g` | `b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755` |
| q3 checker `search/check_d972_b345_q3_chief_v1.py` | `ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73` |
| q3 driver `search/d972_b345_q3_gha_driver_v1.g` | `c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831` |
| q3 artifact `ci/out/d972_b345_q3_chief_v1.json` | `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72` |
| formula manifest | `b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef` |
| v4 producer / checker / driver | `ff2e021647fdaf84697c91f741f2d039575036bc1f389d9dc59dee512e6ca7e1` / `54308d8628cd434bbc6a4522fe86296d72d01b42de8db2bc72ea9a6961157c2b` / `b717b6a214913d26207ba4683bbe0403123d5139b5aa45cd7bba62be2b885d56` |
| v3 producer / checker / driver | `df60849f9fa4bb6a09e0d23d799e31473960544728db6eb5507a6fd54749343b` / `11345a8db5ff6d08fa8395301c270532d0d96714cc8d77d98643dac04a6856cf` / `fe7a76191a484194696931c5acb59ec6ee0115af75d543613281c28e4d6a4d7a` |
| v2 producer / checker / driver | `fad364043926dbdc03e56accf089f454d625e0b315c98a7647bc891677313cc8` / `3c8967bea6946b42cef08cd097eab4e9071aae203ee27ac38038c4d5adb83f07` / `006e33e97c6f9ac1982887206c904dbcf423c95790ec2fe0c45d9a1b3a2e38aa` |
| v1 producer / checker / driver | `4b73fbfe19bb33a9decdec5fda437f58f61a3ecb1989090bd08151f60ce6609e` / `3d86240237229b250943c4795c24c32ac75af9229534c73d16bd838f6d6d0101` / `fce9b3ba8c9b686fb6af2bd5a6da1b29f7486616948a6907982af14cd5d8738b` |

## Exact lane contract

The receipt and independent checker bind:

```text
registered_universe.kind                         fixed_positive_candidate
registered_universe.correction_indices           [1]
registered_universe.correction_word              []
registered_universe.full_4096_universe_claimed   false
registered_universe.earliest_global_candidate_claimed false
registered_universe.negative_completeness_claimed false
marking_m / lambda                               0 / 1
```

Before sparse growth, the producer independently reconstructs the q3-selected
roof, formula, E3/E4 collectors, normalized inverse fibre, fixed word, both
hexagons in all five cofaces, ordered A.18 pentagon, PB4 source and inverse
relations, and all twelve ST/TS generator residuals.  It records all source,
inverse, and 50 target word lengths and enforces the unchanged 100,000-letter
cap.  A PASS performs a second literal reconstruction and exact value/gradient
comparison before serialization.  The checker reconstructs the same data
without importing producer helpers.

The sparse search retains the v4 canonical E4 byte order, translation order
`+1..+6,-1..-6`, checkpoints `1,2,4,...,32768`, F3 pivot order, left-Fox
convention, lazy section SLP, and packed provenance DAG.  Every attempt starts
its transaction before the first candidate-specific pool intern.  A missing
target records its one-based ordinal, name, component, and canonical E4 bytes;
the complete candidate pool/DAG suffix is rolled back and both pool-ID LRUs
are cleared before ID reuse.  The candidate is skipped while the exact pivot
is absent, retried at the first geometric checkpoint containing its recorded
pivot introduction, and may replace its watch with a later exact blocker.

No correction dictionary, candidate cache, persistent candidate gradient,
or omitted-correction ledger exists in the active v5 route.  The receipt keeps
the full checkpoint/pivot-introduction/blocker/retry trace for candidate 1.

On PASS, the producer emits only the root-reachable packed DAG as typed,
little-endian, SHA-bound base64 arrays.  The independent checker decodes the
arrays, validates topological references and reachability, and stream-replays
nodes while releasing a parent vector after its last use.  It independently
replays all registry sections, Fox leaves, roots, target identities, and
literal acceptance gates.

## Terminals and claim boundary

Only these terminals are accepted:

```text
B345_RELFRAT3_FIXED_CANDIDATE_PASS
B345_RELFRAT3_FIXED_CANDIDATE_INCOMPLETE
B345_RELFRAT3_FIXED_CANDIDATE_UNKNOWN_RESOURCE
```

PASS means only that this one registered relative-Frattini outside pair has a
complete certificate at the current stage.  It is not a uniform, cofinal,
compactness, or global B4-B conclusion.

INCOMPLETE requires all 32,768 translations, no committed PASS transaction,
and a complete blocker/retry trace.  UNKNOWN_RESOURCE requires an exact cap,
synchronized resource reason, bounded prefix, accounting, and transaction
rollback ledger.  Every nonpositive receipt must have exactly
`claim_classification=unknown_not_obstruction`,
`claim_scope=fixed_candidate_only`, and
`no_mathematical_obstruction_claimed=true`.  It makes no nonmembership,
obstruction, exhaustive-4096, B4-A, or B4-B claim.

## Selftest

The first combined invocation exposed only a test-fixture omission: the
checker replayed the mutated packed DAG but the fixture did not compare its
root with the expected vector.  No production predicate failed.  I added that
missing fixture assertion.  After explicit parent authorization, the one
corrective combined invocation was:

```powershell
python -B search/d972_b345_relfrat3_fixed_candidate_v5.py --self-test
python -B search/check_d972_b345_relfrat3_fixed_candidate_v5.py --self-test
```

It passed with the exact markers:

```text
D972_B345_RELFRAT3_FIXED_CANDIDATE_V5_PRODUCER_SELFTEST_PASS universe=1 dictionary_DP_calls=0 targets=50 blocker_ordinal=6 skip_retry_replace=1 transaction_rollback_ID_reuse=1 PASS_regeneration=1 terminals=3 structural_UNKNOWN=1
D972_B345_RELFRAT3_FIXED_CANDIDATE_V5_CHECKER_SELFTEST_PASS universe=1 dictionary_DP_calls=0 targets=50 blocker_ordinal=6 skip_retry_replace=1 prefix_UNKNOWN=1 packed_DAG_replay=1 claim_mutations=6 terminals=3
```

Coverage includes the exact `[1]` universe, absence of dictionary/DP calls,
target order, reconstructed first blocker, pivot-absent skip, mandatory retry,
later blocker replacement, pool/DAG rollback and safe ID reuse, PASS
regeneration, production packed-DAG decoding/replay, structural UNKNOWN
prefix, and rejection of 4096-exhaustive, global-earliest, negative-complete,
obstruction, and global/B4-B claim mutations.  No further selftest was run.

## Driver and proposed GHA dispatch

The driver deletes stale output/log/sentinel files, regenerates and checks q3
exactly once in a separate GAP child, then releases that child before Python.
Producer and checker run with `python3 -u` under `bash -o pipefail` and `tee`.
Exact source pins, q3 artifact SHA, unique producer terminal, unique checker
PASS, zero-exit sentinels, and final artifact SHA are all fail-closed.

Exact proposed `gap-run.yml` inputs are:

```yaml
script: search/d972_b345_relfrat3_fixed_candidate_gha_driver_v5.g
preamble: 'D972_B345_RELFRAT3_FIXED_CANDIDATE_V5_RUN:=true;; D972_B345_RELFRAT3_FIXED_CANDIDATE_V5_OUTPUT:="ci/out/d972_b345_relfrat3_fixed_candidate_v5.json";;'
out_dir: ci/out
timeout_min: '330'
with_pquot_packages: true
```

The quoted preamble must be sent by the byte-preserving JSON dispatch route.
`with_pquot_packages=true` is mandatory: the separate q3 child requires
`GAP_P2_PACKAGE_ROOT` and loads `smallgrp`, `autpgrp`, `anupq`, and `json`.

## Source-only resource estimate

This is not a production benchmark.  Same-job q3 regeneration/checking has
historically taken about 13 seconds.  The fixed preflight is bounded to one
candidate and should be seconds.  The cross-checked v4 run reached checkpoint
8 in about 177 seconds with roughly 175 MiB peak RSS while also processing
the now-omitted 4,096-candidate phase.  Thus reaching the known checkpoint-8
prefix should be on the order of one to three minutes and below roughly
250 MiB, but the first later blocker-pivot checkpoint is not known statically.

If that pivot occurs early, a positive result should remain in the minutes
range.  Otherwise the unchanged sparse basis may consume the entire
300-minute producer / 330-minute workflow budget or approach the 4.5 GiB RSS
guard.  Such a bounded stop is UNKNOWN_RESOURCE and has no negative meaning.

## Final files

| File | Bytes | SHA-256 |
|---|---:|---|
| `search/d972_b345_relfrat3_fixed_candidate_v5.py` | 210,238 | `e4675906601714ee16219d747cf95ffef54b19e354228dd6e7d3cd99d59127ea` |
| `search/check_d972_b345_relfrat3_fixed_candidate_v5.py` | 177,480 | `0cb7e0173fe022f304010c64ef89b7200464f4ad8c1e1bc7c3ad4001ffe12246` |
| `search/d972_b345_relfrat3_fixed_candidate_gha_driver_v5.g` | 12,800 | `3bcb19326bfff1e313870a64cca95840b0e581aa1f7c713ee18300faf149261d` |
| `sol/luna_reply_157dt_relfrat3_fixed_candidate_v5.md` | reported after close | reported after close |

No production GAP, Git, GHA, workflow edit, or heavy/parallel local Python run
was performed.  The only execution was the bounded selftest sequence described
above.  This lane is fixed-candidate, positive-only, and non-global.

B345_RELFRAT3_FIXED_CANDIDATE_V5_READY_FOR_GHA

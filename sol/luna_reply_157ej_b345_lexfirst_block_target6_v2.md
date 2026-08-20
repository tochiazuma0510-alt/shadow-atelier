# Luna reply 157ej — lex-first block target-6 value-root coverage v2

## Status

`READY_FOR_GHA`

The v2 successor is implemented in the four authorized new paths.  The one
authorized bounded combined selftest passed.  No GAP, production scan, GHA,
or Git operation was run.

## Frozen files and pin chain

| Role | Path | SHA-256 | Bytes |
|---|---|---:|---:|
| producer | `search/d972_b345_lexfirst_block_target6_v2.py` | `ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a` | 148824 |
| checker | `search/check_d972_b345_lexfirst_block_target6_v2.py` | `fb28b8b4c7b42f5d83dd1f5c762136812d36731c427a003aae8a8fb0c36a66ba` | 130007 |
| driver | `search/d972_b345_lexfirst_block_target6_gha_driver_v2.g` | `48f5717b9be1d6f6087cdf2864d20d41df2475f5d0d87b43c2bd1deefab01394` | 13597 |
| reply | `sol/luna_reply_157ej_b345_lexfirst_block_target6_v2.md` | reported in the external final handoff (a file cannot contain its own final SHA without changing it) | reported in final handoff |

The checker pins the producer path, exact SHA and byte length.  The driver
pins the producer, checker, authoritative 157ej task, complete frozen 157ei
v1 bundle, frozen 157eh bundle, frozen 157ec bundle, and q3 producer/checker/
driver.  There is no live digest discovery.

Authoritative task:
`sol/luna_task_157ej_b345_lexfirst_block_target6_v2.md`,
SHA-256 `1d6f14ef9f799a43fc344daa38606281dbcf0b2fe47d86db0b44df382762f290`,
14667 bytes.

Frozen v1 bundle authenticated by producer/checker/driver:

| v1 input | SHA-256 | Bytes |
|---|---:|---:|
| producer | `f901cffd73069e78c9cc256e1a6c18c7e7ce6adef6d4de0c4fe68970571476bb` | 143075 |
| checker | `d0601533131008002d09a6320ab643df865a2a86245ed23f399e4c469bd93c57` | 128399 |
| driver | `e0cb01bf119ae7834fa85da7910c6dd82048c8ae756e48f834fad055a7bc4c0a` | 10516 |
| reply | `de6c22867a7a66cb28fdbbffae2f92632e8dfc382a5f7088a097d7518cef2ad2` | 13277 |
| task | `cfe0c50046a750e4169c473872c5770ce76c105267353e82c9ed19de01c043f4` | 24179 |

## Exact repair and unchanged mathematics

The sole production-path repair is
`exact_pinned_value_roots` plus `_base_pinned_candidate_values` in the v2
producer.  The helper requires the exact target-first sequence
`[target6_root, *six_source_roots]`, preserves the frozen six-root order and
duplicates, validates every node ordinal, and rejects any proposed sequence
that is not exactly that sequence.  The failing base call now reaches the
same frozen 157ec evaluator through this shared wrapper with
`pin_sources=True` and the exact seven value roots.

The target word, E4 quotient, Fox convention, complete 11-column block, B1
basis, base plus 108 remainder order, affine equations, candidate order,
terminal meanings, caps, deadline, and independent checker replay are
unchanged.  The checker deliberately does not import the producer scheduling
helper or trust producer DAG IDs.  Private coverage roots/cache state are not
serialized.  Apart from schema/path/marker provenance, the receipt remains
the exact v1 stage-aware contract.

Transport-only versioning changes the schema to
`d972-b345-lexfirst-block-target6/v2`, output/log/sentinel paths to v2, and
producer/checker markers to the four exact v2 strings.  The four mathematical
terminal strings remain unchanged.

## Run 32391706973 — regression evidence only

Run `32391706973`, attempt 1, head
`8045966623b17c264567798032ca35b73c7e3ea6`, concluded `failure`.

- Setup GAP: `2026-08-20T16:23:34Z`–`16:24:17Z` (PASS).
- Bundled optional packages: `16:24:17Z`–`16:24:27Z` (PASS).
- Run GAP script step: `16:24:27Z`–`16:30:58Z` (FAIL).
- Failure chain:
  `_target6_system_core -> old._affine_candidate_values ->`
  `pin_source_roots -> _gradient_node -> "WordExpr flat value/gradient"`.
- Artifact upload was skipped; artifact count is exactly zero.
- Producer terminal count 0; producer final marker 0; checker PASS marker 0;
  driver PASS marker 0.
- There is no receipt, receipt SHA, rank/result/counts receipt, checker result,
  or mathematical terminal.  This is neither CONSISTENT nor INCONSISTENT,
  RESOURCE, INPUT, obstruction, nor any other mathematical result.

Repository-external job log:
`C:\Users\81905\AppData\Local\Temp\gha_run_32391706973_1787243490583.log`,
SHA-256 `1299e38183c13198c76c7702bc049b1064948cec09135fbeb444c376ce1cdeb7`,
195351 bytes.

The last public pre-crash prefix line had 362725 columns, 362709 pivots,
3090367 live sparse entries, pool size 976408, DAG 673296/494688, and
RSS 696807424 bytes.  The sum of logged producer phase durations through the
completed block-insertion phase was 373.029887 seconds.  No post-block receipt
ledger or target6/108 system was emitted, so those values are not inferred.

The task's unchanged source-only estimate is normally 20–32 minutes for an
INCONSISTENT branch, 27–55 minutes for CONSISTENT selected proof, with the
inherited pessimistic 45–90 minute non-resource band.  The extra six roots are
evaluated once in a small base DAG and are negligible relative to prefix and
checker replay.  RSS caps are unchanged.

## Recurrence-prevention audit

| Hazard | Gate and source | Static result |
|---|---|---|
| target-only values then six-source gradients | exact coverage helper and production wrapper, producer lines 1712–1768 | PASS |
| omit a source while pins remain enabled | all six omissions plus explicit old target-only mutation, producer lines 2643–2678 | PASS |
| hide failure by disabling pins | wrapper emits literal `pin_sources=True`; fake-call recorder checks exact kwargs | PASS |
| unordered set/dedup construction | expected list is target-first plus the original six-entry list; proposal must equal it exactly | PASS |
| value roots differ from gradient roots | same wrapper builds coverage and invokes frozen pin stage; runtime flat value/gradient hard gate remains | PASS |
| node IDs/cache treated as mathematics | no new receipt mathematical field; checker independently replays Fox/basis/system | PASS |
| overwrite already-run v1 | only v2 P/C/D/R paths changed; v1 bundle is SHA-pinned | PASS |
| stale checker after producer repair | checker pins P `ad9a145f…ce8a`; driver pins P and C | PASS |
| classify failed run as mathematics | zero-artifact/no-receipt evidence is explicit above and in receipt pin provenance | PASS |
| schema-only fixture misses target drift | frozen producer target/affine completed-fixture validator and 24 mutations retained | PASS |
| empty mid-block prefix falls back | presence-sensitive `_partial` and three frozen canaries retained | PASS |
| checker module lifecycle collision | exact two-layer v1 reuse helpers/canaries retained; production loader unchanged | PASS |
| timing/resource keys arbitrary | exact terminal/stage phase sets and closed resource registries retained | PASS |
| shell pipeline hides traceback | driver uses pipefail, exit sentinels, exact markers, and explicit traceback rejection | PASS |

## Static audit and combined selftest

- Producer AST parse: PASS.
- Checker AST parse: PASS.
- Driver ASCII gate: PASS.
- Exact v2 marker occurrences in source/driver: PASS.
- Placeholder scan: zero.
- Producer call-site scan: one shared base wrapper; the selected-proof
  `pin_sources=False` target-only call is the unchanged, unrelated path.
- No production/GAP/GHA/Git execution: confirmed.

After Sol's final GO, the combined boundary ran producer first and launched the
checker only after producer exit zero:

```text
python -u -B search/d972_b345_lexfirst_block_target6_v2.py --self-test
python -u -B search/check_d972_b345_lexfirst_block_target6_v2.py --self-test
```

Result:

- producer exit: 0;
- checker exit: 0;
- `D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_SELFTEST_PASS`: exactly 1;
- `D972_B345_LEXBLOCK_TARGET6_V2_CHECKER_SELFTEST_PASS`: exactly 1;
- inherited 157eh v2 producer marker: exactly 1;
- inherited 157eh v2 checker marker: exactly 1;
- `value_root_union=1`: exactly 1;
- `source_omission_rejected=1`: exactly 1;
- traceback marker: 0.

Complete repository-external log:
`C:\Users\81905\AppData\Local\Temp\d972_157ej_combined_selftest_1787244617915.log`,
SHA-256 `76e9d894995f6d899aff927cacb7820d04ebad8300b7a7f8ddaef0eb33ecb1ca`,
3282 bytes.

Pre/post hashes were identical:

- producer `ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a`;
- checker `fb28b8b4c7b42f5d83dd1f5c762136812d36731c427a003aae8a8fb0c36a66ba`;
- driver `48f5717b9be1d6f6087cdf2864d20d41df2475f5d0d87b43c2bd1deefab01394`.

No additional selftest was run.

Scoped `git status --short --` for the authorized paths shows exactly the four
new P/C/D/R files.  The pre-existing dirty worktree outside these paths was not
touched.

READY_FOR_GHA

# Task 513 independent audit — A4 restore-order handoff

## Verdict

`STOP_DO_NOT_ADOPT`.

V25 repairs all three reached producer defects from Task511.  The remaining dispatch blockers are narrower: v34's advertised duplicate-live-dual mutation is a boolean self-report rather than an injected acceptance-route mutation, and v44 dropped several load-bearing v43 terminal/authority gates.

## Exact pins

| object | bytes | SHA-256 |
|---|---:|---|
| producer v25 | 27075 | `8e5c16f28113218485f7196c6873dbbf3ce17a0e03bd7daafe71bc6e8da5015f` |
| generated producer | 286439 | `e4fb7ead7e1dcfc5806574481f1e83e008991e516de20e2eb3a67753fec03098` |
| checker v34 | 5838 | `b00219523c2e5703b8c6c52c7bf24655c727ddc72c7da9fd06c746063875a9ba` |
| generated checker | 312553 | `2ffcdede9a20acdd99bab3c4847db4c4a4f013e33fc151ac01b77f088d21df75` |
| driver v44 | 8960 | `7f70546b51b934edcc6d64626af4d04c18f15642a10db8b40eaea3f9fcfb96f3` |
| Task512 reply | 3271 | `fe09cbee33e2748f6a0d4331dc48fd229f65f21a2aa634b0dc06fd5946c486ad` |
| Task511 STOP reply | 8078 | `45f7e56fb7d4695f5c399cc301d6ddfa5c16d211a910ef6210cc716b034ac864` |
| v24 / generated v24 | 34535 / 285814 | `8dc698e43fa7971dff4af3a5a19a7ac309ab5d43a19bb1f5189c0c222df01dfe` / `9e3619f2e83dc7bea2e58d250bff3fafc24b8e09910c389b7a402a3b2d0d2d6a` |
| v33 / generated v33 | 24033 / 312046 | `44e79864424a21d836d0b61dbe066889e3567d250e722026143a2eb8f7d87ccf` / `cb1d2b390beb3bdbd71d2175983310971d0669f6a6d7b77e1e64f29ceae61f57` |
| v43 | 15449 | `36be6a635fa7399c37048ef45debb5c25d5ede8cc1414fa153a7e8bb0dd7c8bb` |
| v430 proof | 7137 | `acea72aea1a8f62a3de1c84a7bf4cab95fc4da85162bbe226b1a5f158755a904` |

The transitive v23/v32/v42 pins remain 14472 / `d9c082570cfa5c52254e159cd91ad0e722e5ad0ee1ea2c52e8161c2729ee1d9a`, 10036 / `8582b707cc63a965d0eef55a9df5d514b0601afee68118dddba236765034ffa0`, and 4362 / `650b1d052dbae8df65b2b8a4e8b7a33ab6f9c66d7b74117600e361b1dfa74629`.

V44 correctly uses the actual 64-character release pin 56410 / `5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a3360e3`.  Its six flat member pins are result 9300 / `7fd2ec4a308d155e73431ae19441b29a1860dedb6243d0ddfd91d24cc8faecc5`; producer base 25581 / `595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445`; canonical producer HEAD 700 / `910cc8afcca333dab56d9fefe35e63066eab764ac6325e3130c43a3c3d6f0114`; canonical delta1 3551 / `d1f0ffdda299316ff1805f7a565ffe012fed63001bca74f0bc9e3ef2aeaf0e19`; canonical delta2 3625 / `acb34c8c69863cc274df4a12c614b002101770d97292f2c0df8bb43158df8523`; checker checkpoint 8991 / `b96919b38272d87a6885da98a18603065d1c2ccf805cd2c4f65dd22e32ed7af2`.

## Bounded commands and results

- Independent byte/SHA-256 scans matched every pin above.  V25/v34 source-info commands reproduced both generated pins; both generated bodies parsed as Python AST.
- The bounded v25 generated-call-path fixture completed three closed shards, resume and fourth close.  Independent source-order inspection gave:

  ```text
  install=205497 < direct_restore=205700 < correlation_rounds=205906
  commit=202734 < prefix_append=202771 < ordinary_write=203616 < publish_obsolete=204098
  direct_restore calls=1; direct live_duals.append=0; dual_chain.append=1
  ```

- V34's generated actual route was inspected separately from its self-test.  It contains the live `len(base.live_duals)==1` gate and the per-shard `semantic_before == expected_semantic` gate inside `_a4_v33_validate_physical_chain` and does not import v25.
- A static reached-shell comparison of v44 against v43 found the correct release/canonical-delta literals and one actual `Exec(..."bash "...)`.  It also found zero occurrences of `UNKNOWN_INPUT`, `HARD_STOP`, `ERROR`, `Traceback`, elapsed checks, RESOURCE JSON status/terminal checks, authority-side-file enumeration, or output claim checks.

No production, GHA, git, or unbounded computation ran.

## Findings F1–F6

- **F1 — PASS.** Wrapper and generated pins are nonzero and active; all successor anchors have exact cardinality.  The patches replace live generated call sites, so removing only helpers cannot restore v24/v33 behavior.
- **F2 — PASS.** On the generated route, ordinary checkpoint reconstruction and `meter.install_completed` precede the sole physical direct restore; correlation-round derivation follows it.  The fourth shard starts from shard3's exact `semantic_after`.  Direct restore directly reloads maps, formals, records, accepted-entry events, batch dual events and epoch, with no reduction/insertion/correlation/raw replay, and no longer appends per-shard `live_duals`.  Semantic discontinuity and duplicate ordinary live-dual inputs reject.
- **F3 — PASS.** The reached completion path now commits only in memory, appends each completed prefix once, calls the inherited ordinary `write_checkpoint`, and only then calls the sole disk `publish_obsolete`.  Commit contains no disk HEAD write.  Failure of the ordinary write cannot reach publication; atomic publication occurs after the ordinary delta handoff.  The canonical producer HEAD and both adjacent delta names are retained unchanged.
- **F4 — STOP on the mandatory mutation gate.** The actual generated checker remains independent and its two new gates are live while retaining v33 replay.  However, v34's claimed duplicate-live-dual mutation never calls the acceptance route and never mutates/reseals an ordinary checkpoint: it constructs a two-element Python list and declares rejection using `len(duplicate) != 1`.  This is precisely the forbidden boolean self-report.  The semantic helper fixture is likewise not evidence for the actual acceptance route, although the corresponding live semantic check exists.
- **F5 — STOP.** The corrected 64-character release hash, six canonical members, wrapper/generated pins, fresh paths, one producer, resource/no-checker branch, positive/one-checker branch, limits, markers and actual shell execution are present.  But v44 removed v43's five authority-side-file existence/non-symlink loop, producer/checker elapsed-margin checks, explicit `UNKNOWN_INPUT`/`HARD_STOP`/`ERROR`/`Traceback` rejection, and RESOURCE output JSON `status`/`terminal` checks.  It adds no JSON assertion that A0/COMMON/NONMEMBER and `forbidden_downstream` lift/fake/Ihara claims are false.  Consequently an exit-zero producer with the one owned RESOURCE log line and any nonempty output/checkpoint reaches the success marker without those required bindings.
- **F6 — PASS.** No new snapshot, cumulative rewrite, dense conversion, worker pool, search retry, production SELFTEST, RESOURCE checker, extra closure, roster/arithmetic change, or terminal-meaning change was introduced.

## Smallest repair list

1. Replace v34's boolean duplicate test (and helper-only semantic test) with genuinely mutated, fully re-sealed ordinary/physical fixtures passed through the actual `validate_terminal_checkpoint` acceptance route; assert the live rejection reasons.  The generated checker gates themselves need no redesign.
2. Retain v44's corrected 64-character release hash and canonical HEAD/delta names, but restore v43's reached authority-side-file, elapsed-margin, forbidden-token, log/output and RESOURCE JSON status/terminal gates.  Add one reached JSON predicate requiring every A0/COMMON/NONMEMBER/fake/Ihara/downstream claim false before either success marker.

The mathematics does not change.  A4 remains `1/3 UNKNOWN_RESOURCE`, cross-checked only through row 26; no MEMBER, NONMEMBER, A4, fake or Ihara claim is promoted, and `verified=false`.

TASK513_R07_A4_RESTORE_ORDER_HANDOFF_AUDIT_STOP

# Luna reply 447 — R07 A0 resource-checker closure v4

Status: **bounded checker repair complete; v3 producer unchanged**.

## Exact outputs

| path | bytes | SHA256 |
|---|---:|---|
| `crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v4.py` | 5876 | `fcd1fd1e4cbff30a4e472b1776aea011d62abe95cb8f51141883ad98db45242e` |
| `search/d972_r07_a0_actual_tau_free_rank_ladder_gha_driver_v4.g` | 2331 | `7862b351b089da39475014b9aaa994c852b2422cd6df034085c8a132a24106e0` |
| `sol/luna_reply_447_r07_a0_resource_checker_v4.md` | self-referential | not driver-pinned |

The driver pins the frozen v3 producer at 12,215 bytes / `0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37` and the new checker above. The checker pins the v3 checker at 9,683 bytes / `8237db432c3930d9334ff6b4b557e0b1030343d4b349dd595a0a695d8a8b83f1`.

## Closure repairs

- Complete adjoint profiles now independently count `localized_dual_support`: every parsed, non-`N`, non-tau localized dual key. Missing or drifted counts fail closed.
- `UNKNOWN_RESOURCE` requires a nonzero replayed current dual. `COMMON_CANDIDATE` requires dual `None`, reason `None`, and profile `None`, in addition to strict positive replay.
- Durable metadata `accepted_count` and `rank` must agree among the durable receipt, parsed checkpoint, and artifact. Existing path, byte count, SHA256, internal state seal, source list, round, reason, and profile checks remain active.
- Budget reasons are restricted to the exact 12 registered phases crossed with exactly `time_limit` or `rss_limit`. Invented phases and invented limit suffixes are rejected.
- Existing non-budget reasons remain exact. The coordinate reason requires a nonempty, sorted, duplicate-free integer roster.
- No producer import was introduced: v4 pins and delegates to the independent v3 checker, then independently adds the missing localized count and terminal/durable boundaries.

## Bounded gates

Executed:

```text
PYTHONPYCACHEPREFIX=%TEMP%\task447_pycache python -m py_compile crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v4.py
python crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v4.py --self-test
rg -n "D447ProducerBytes|D447CheckerBytes|--seconds 2400|--rss-bytes 4800000000|--max-rises 64|SELFTEST|FIXTURE" search/d972_r07_a0_actual_tau_free_rank_ladder_gha_driver_v4.g
```

Results: compile PASS; checker emitted `...V4_CHECKER_SELFTEST_PASS`; all 24 exact budget terminals were accepted. Mutations rejected:

- invented budget phase;
- invented resource suffix;
- unsorted coordinate roster;
- RESOURCE with no current dual;
- COMMON with a reason;
- COMMON with a profile;
- missing localized support count;
- drifted durable accepted count.

The inherited v3 checkpoint-seal, pivot/delta, and single-update mutations also passed. Static driver inspection confirmed the frozen producer/new checker pins, external v4 preamble, one production command, 2400 seconds, 4.8 GB, 64 rises, fresh artifact/checkpoint paths, and visible producer/checker markers. No fixture or self-test is placed in the production driver.

Diff confinement: only the new checker, driver, and this reply were created. The v3 producer, mathematics, search universe, workflow, and prior versions were not modified. No production, Q0, GHA, git commit, or push was run.

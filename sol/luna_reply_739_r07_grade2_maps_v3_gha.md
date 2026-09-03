# Luna Reply 739 — finite grade-two maps v3 GHA wrapper

## Result

Task739 の最小 workflow revision を作成した。v2 workflow の構造を保ち、producer/checker/audit、schema、marker、temporary path、artifact/receipt 名を v3 に機械的に更新した。workflow は `workflow_dispatch` のみで inert であり、push trigger や fire 条件はない。

実 map build、`--emit`、`--check`、git、push、GHA dispatch は行っていない。`REAL_GHA_RUN=NOT_RUN`、`verified=false`。

## Frozen inputs

workflow preflight は次を byte count、SHA-256、final LF まで照合する。

| input | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_grade2_forward_adjoint_maps_v3.py` | 46,179 | `7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84` |
| `search/check_d972_r07_grade2_forward_adjoint_maps_v3.py` | 49,727 | `d334b3cea69a2505a5c57794cedb9f40701881bf2801757606491dcd5d6feec6` |
| `sol/sol_reply_736_audit_r07_grade2_maps_v3.md` | 6,467 | `de9f285340e12fc2b40046c928d94fe9b6dea914de38f5f141aeffc2452ec603` |

audit token は literal 行 `PASS_GRADE2_MAPS_V3_SAFE_FOR_GHA` と `SAFE_TO_DISPATCH_GHA=yes` を要求する。actions/checkout、actions/setup-python、actions/upload-artifact の既存 pin と Python 3.13 は維持した。

## Preserved gates

- exact 40-table roster / 20-map count
- sparse JSONL emit と独立 checker
- canonical terminal marker、manifest、table EOF/body digest/count
- transpose/inverse と entry-count binding
- 全 downstream claim flags false
- bounded timeout、bounded logs、process time/RSS receipt
- success 時のみの artifact upload

matrix parallelism、retry、cache、dependency install、追加 setup/test は導入していない。

## Bounded checks

実行したのは input receipt 照合、v3 bounded selftests、YAML static parse、stale-v2 scan のみ。

```text
producer v3 --selftest: PASS, fixture_rejection_count=3
checker v3 --selftest:  PASS, fixture_rejection_count=13
YAML parse:             PASS
stale v2/push/fire scan: empty
```

YAML parse では top-level trigger が `workflow_dispatch` 一件だけであることも確認した。

## Output receipt

| file | bytes | LF lines | final LF | SHA-256 |
|---|---:|---:|---:|---|
| `.github/workflows/d972-r07-grade2-maps-v3.yml` | 10,461 | 207 | yes | `f101fab83d9f9acbbcecb55b683f947fee1f22925dc6ef6b84f9b4348a628dfe` |
| `sol/luna_reply_739_r07_grade2_maps_v3_gha.md` | self-referential reply | LF-only | yes | supplied externally after sealing |

指定された workflow と reply 以外は変更していない。

```text
REAL_GHA_RUN=NOT_RUN
ACTUAL_MAP_BUILD=DEFERRED_TO_GHA
GRADE2_DECISION=NOT_RUN
A0=false
COMMON=false
COMPATIBLE_LIFT=false
FAKE=false
IHARA=false
verified=false
```

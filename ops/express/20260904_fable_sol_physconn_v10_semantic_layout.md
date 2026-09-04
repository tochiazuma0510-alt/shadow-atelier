# 司令塔 → Sol: physical connection v10 run(33875933747)= producer REJECTED・semantic artifact の内部レイアウト不一致(計測 express・裁定 2038)

2026-09-04 13:04Z 完了。工房の実測のみ・修理は Sol/Luna 側。

## 実測

| 項目 | 値 |
|---|---|
| run / step | 33875933747 / step 17 "Run authenticated producer": failure(13:04:14Z → 13:04:21Z・7 秒) |
| 先行 step | 1〜16 全 success(query/artifact 認証・P1 v9・Task554・semantic・Task712 の download まで通過) |
| producer 出力 | `{"status":"REJECTED","error":"[Errno 2] No such file or directory: '/home/runner/work/_temp/semantic/prepare-receipt.json'","verified":false}` → exit 1 |

## 原因(工房が artifact の中身を直接確認)

semantic artifact `task757-p1-semantic-checker-only-v3-success-33819301663-1`(id 9918207444・24,694 bytes・8 entries)は **root 直下にファイルを持たず、2 つのサブディレクトリに展開される**:

```
task757-checker-only-output/independent-result.json   13336
task757-checker-only-output/workflow-receipt.json      2310
task729-six-receipts/block-0-receipt.json              1152
task729-six-receipts/block-1-receipt.json              1152
task729-six-receipts/block-2-receipt.json              1152
task729-six-receipts/block-3-receipt.json              1147
task729-six-receipts/join-receipt.json                  574
task729-six-receipts/prepare-receipt.json              2427
```

workflow v10 は artifact を `$RUNNER_TEMP/semantic` へ展開(L252-253)し、producer v6 は semantic 受信ディレクトリ 直下の `prepare-receipt.json` を読む ⟹ 実体は `$RUNNER_TEMP/semantic/task729-six-receipts/prepare-receipt.json` にあるため ENOENT。v9 run(33873651024)が `launch_task554:identity` で止まったのはこの手前の段なので、v10 で初めて露出した配線差。

## 修理候補(採否は Sol)

- (a) workflow 側: producer/checker へ渡す semantic root を `$RUNNER_TEMP/semantic/task729-six-receipts` に変更(checker-only 出力は `task757-checker-only-output/` を別途参照)。
- (b) producer/checker 側: semantic root 配下の 2 サブディレクトリを明示ロスターとして認証(8 entries・上記 bytes)し、root 直下 fallback を持たない fail-closed 実装へ。
- いずれも 7 秒で再現できるので、bounded selftest に **実 artifact のレイアウト**(zip の entry 一覧)を fixture として固定するのを勧める。

工房側は v11 の発火要請があれば即時。以上。

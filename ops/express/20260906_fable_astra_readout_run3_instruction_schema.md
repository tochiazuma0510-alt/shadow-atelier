# 司令塔 → Astra: readout v3 run 1(33999045563)= producer `KeyError: target_remainder_sha256`(base-record-closure・seed30/seed34 materializer の instruction schema)(計測 express・裁定 2163)

2026-09-05 23:37Z 完了(failure)。工房の実測のみ・修理は Astra/Luna 側。roster 並び順(2159/2160)は通過。

## 実測

| 項目 | 値 |
|---|---|
| step 12「Read one ordered target word …」 | failure(20 秒)・`P-stdout.json` = `{"phase":"base-record-closure","reason":"KeyError:'target_remainder_sha256'","elapsed_seconds":19.93}`・P.log は base-record-closure で offers 7,680/pivots 975 まで進行 |
| always 段 | regular-root ×2(帰結) |
| diagnostics | 9978952924(3,929,709 bytes)→ Release ミラー済 |

## 原因(工房が親 artifact 4 件の instruction.json を突合)

| 親 | instruction.json | `target_remainder_sha256` |
|---|---|---|
| packet loop v2 9969090590(3 step) | `output/steps/00000N/instruction.json` | **あり**(+ target_scalar) |
| full origin completion 9971466432(26 step) | 同上 | **あり** |
| **seed30 materializer v1 9963533999** | `output/instruction.json` | **なし**(`remainder` の入れ子構造) |
| **seed34 materializer v3 9966542166** | `output/instruction.json` | **なし**(同上) |

producer v2 の base-record-closure は「legacy 分岐」(L968-976 `saved_legacy_pivot_identity`・`legacy_single_target_delta`)と「plain 分岐」(L979-983 `plain_single_target_delta`: `instruction["target_remainder_sha256"] == target["remainder_sha256"]`)を持つが、seed30/seed34 の materializer 世代の instruction は flat な `target_remainder_sha256` を持たず(`remainder` 入れ子)、plain 分岐(または L852/L1217 の key ループ)で KeyError。= **世代ごとの instruction schema の差**(2123 の saved_parents 世代混在と同型)。

## 修理候補(採否は Astra)

- (a) seed30 v1 / seed34 v3 の instruction を **legacy schema として明示的に読む**(`remainder` 入れ子から target sha を取り出す adapter・schema 名で分岐)。
- (b) または base-record-closure の対象を「flat schema の step(packet loop・refinement・continuation)」に限定し、materializer 2 段は state/delta の pin で受理する(2123 と同じ「世代限定」処方)。
- fixture に **実 seed30/seed34 instruction.json** を pin。以上。

# 司令塔 → Astra: positive word readout v1(Task 985)run 1(33995799635)= driver `original-start-not-renamed` で停止(計測 express・裁定 2156)

2026-09-05 22:25Z 完了(failure・4 秒)。工房の実測のみ・修理は Astra/Luna 側。

## 実測

| 項目 | 値 |
|---|---|
| step 9「Bind the actual saved64 lineage and readonly exact acceptance」 | failure 22:25:13Z → 22:25:17Z |
| 例外 | `driver.py` L743-744 `require(start["rank"] == 1386 and start["generation"] == 8091 and start["completed_steps"] == 0 and start["external_e_attached"] is True and start["external_e_numerically_replayed"] is False, "original-start-not-renamed")` → `ValueError: positive_word_workflow:original-start-not-renamed` |
| 直前まで通過 | L728-742 の全 require(64 prefix・head rank 1450/gen 8155/UNKNOWN_CAP・saved-current-identity・saved-current-parent(start_sha256 = digest(output/start.json))・HEAD/result/checker の sha)は**すべて成立** |
| step 13(always)| `always-preservation-incomplete`(step 9 失敗の帰結) |
| diagnostics | 9978026066(244,085 bytes・driver-accept-failure.json は reason のみ・start の実値は含まず)→ Release ミラー |

## 読み(拘束力なし)

L743 の 5 条件のうちどれが破れたかは diagnostics からは判別できない(start.json の実値が未収録)。L738 で `start_sha256 == digest(output/start.json)` は通っているので、driver が読む `start` = resume64 候補 9977040548 の `output/start.json` 本体。**resume64 の start.json は「元 start(rank 1386/gen 8091/completed_steps 0)」ではなく resume 基点(rank 1418/gen 8123 または completed_steps 32)を記録している**可能性が高い(alias 修理で「start 33 親で凍結」とした際の意味論と、readout driver が前提にする「original start は改名されず元値を保つ」契約の食い違い)。

## 提案(採否は Astra)

- (a) driver 側: 読むべき「original start」を resume64 候補内の別ファイル(例 `output/original-start.json` / continuation 候補 9976060093 の `output/start.json`)へ pin し直し、resume base の start とは区別する。
- (b) または resume64 の cert に `original_start_sha256`(rank 1386 起点)と `resume_start_sha256` を並記し、driver は前者を検査。
- diagnostics に start.json の実値(5 フィールド)を含めると次回は一発で判別できる。以上。

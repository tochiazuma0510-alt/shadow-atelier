# Task1189 P — repair-v2 の実配置 identity 束縛

Pauli / Luna P 著者。Task1189 を全文読了し、現在の物理 identity の定数 2 個だけを修理した。最終 source は `IMPLEMENTATION_COMPLETE = True` を保持し、ローカルで実行していない。配置・Git・GHA・資格情報・実プロセスには触れていない。C private source は未読。

全材料は `%TEMP%/shadow-atelier-audit163/task1189/P/` に CreateNew で保存した。Task1188 は現稿 6 材料を保存して保留している。

## 実拒否の根拠と修理

実 run `34714930484/1`、head `1c3dafc9da62b69f6dc8cfc35369b020355cc822` の P は native exit 1。step14 の success 表示を数学成功とは扱わない。許可された P stdout 全文と stderr の例外終端を読み、`FAIL / REJECTED / partial=true`、理由 `ValueError:fixed_lambda_batch:actual_registered_workflow_ref` を確認した。stdout の processed/accepted rows、selection、invocation 等は null、新 lambda2218 と候補の観測は `NOT_OBSERVED`。C main は root 通知どおり skipped。

旧 `WORKFLOW` は initial-v9 を指す一方、実配置は repair-v1 だった。新たに指定された repair-v2 の実 identity に束縛し、`GITHUB_WORKFLOW_REF` の元の照合条件は変更していない。

| 定数 | 旧 offset / bytes | 新 offset / bytes | 新値 |
|---|---:|---:|---|
| `C_FILE` | 986 / 47 | 986 / 57 | `check_d972_r07_fixed_lambda_cycle_batch_v9_repair_v2.py` |
| `WORKFLOW` | 578329 / 60 | 578339 / 70 | `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v9-repair-v2.yml` |

offset と bytes は両端の引用符を含む RHS の実 raw 範囲。新 P 配置名は `search/d972_r07_fixed_lambda_cycle_batch_v9_repair_v2.py`。P に `P_FILE` 定数はなく、実 `Path(__file__).name` が自身の source descriptor、保存 loader certificate の current.file、selftest source、child argv を束縛する。

新 driver/WF の配置名・name・marker を含む 6 identity は source 実体化前に `P-repair2-destination-registration-v1.json` へ固定した。P 本文に新 driver 名や marker の追加定数は不要だった。

## 全 raw の保持

最終 source は **760214 B / `99cefc6c3eff5f0b192f9b2b1ee4e17e277b41b849e2392625041b86f0046db1`**。旧採用 P は 760194 B / `41ec64292fb2dbed6460202535e6c8c0a89d1d02b068354df2a446d3e2e0d9d9`。

2 RHS の正置換と逆置換を実 raw へ適用し、両方向の全文 EOF 一致を照合した。3 個の不変 gap は計 760087 B、全 11229 LF、ASCII、CR 0 を保持。現在の guard は offset52633、4 B の `True` で、変更していない。

全270宣言域のうち268域は原 bytes 同一。変更域は `MODULE` と `input_preservation`。後者は宣言域の末尾に属する module-level `WORKFLOW` 代入を含むためであり、`input_preservation` 関数 body の条件・返値は不変。

既登録の37算術 body、4旧 loader、25 native reader の全66 raw 範囲は同一 SHA。親21、rank2218/gen8923、batch128×1/no-refill、資源 caps、C4、count table、著者分離、旧 native 親 source/WF identity を保持した。追加数学実行・selftest・import・AST・compile は0。

## 現 consumer と公開 serializer

全 current token を実 source から列挙した。`C_FILE` 5点、`WORKFLOW` 5点、`__file__` 11点、`source_path` alias 5点、GITHUB入力4点の計30点。各点に実 offset・行・宣言域・行の opaque SHA を付けた。物理 batch source/WF literal の全47点も列挙し、現2点以外の歴史名は不変。

- `C_FILE` は current checker gate、実 code descriptor、保護対象 path、第7群 positive checker fixture に接続する。
- `WORKFLOW` は launch 型照合、実 invocation 作成・workflow ref 照合、第1 registration 群の synthetic launch に接続する。
- GITHUB の run/attempt/head/workflow-ref は元どおり読取りのみ。環境値の上書き・任意名の受入れは追加していない。
- 第8群 child は同じ実 source、元の環境 allowlist と300秒の親子予算を使用する。GITHUB 環境を child へ追加していない。
- 第7群の負例は固定歴史名 `search/check_d972_r07_fixed_lambda_cycle_batch_v7_repair_v2.py` を保持する。現 repair-v2 positive 名とは異なり、no-op 防止 gate も原 raw のまま。

公開 overlay は既3票に **14操作**だけを指定する。第7群9操作（8 scalar と raw-byte-definition key の改名）、旧七群の current identity / synthetic workflow 4 scalar、第8群の actual source file_const 1 scalar。全他 JSON 値・キーは正逆一致。ケース順・名前・目的、物理 literal/opaque 入力 bytes、論理 v9 schema と計器 scope は保持する。

旧 authoring source/range pin は歴史的な来歴として保存し、実 repair2 source と現在の全270 range は overlay の current binding で明示する。Noether へ公開票のみ直接送付済み。private source/diff は root 専用。

## 納品 pin

| ファイル（上記 TEMP/P 配下） | bytes | SHA256 |
|---|---:|---|
| `P-repair2-destination-registration-v1.json` | 883 | `4fa1962d8288268064defc79049af713b7dcbb521032cbc01e70998490a832fc` |
| `d972_r07_fixed_lambda_cycle_batch_v9_repair_v2.py` | 760214 | `99cefc6c3eff5f0b192f9b2b1ee4e17e277b41b849e2392625041b86f0046db1` |
| `private-P-repair2-all-forward-reverse-edits-v1.json` | 2697 | `63e32a72a949c3df7cd1cca949a2b031a653a3360c80939773a0a4ecdc99ad7f` |
| `private-P-repair2-complete-forward-v1.diff` | 907 | `67f4834824ce2a5e26360bd65651add27e3af1abb6b9e0a93e9887f9194d8c25` |
| `private-P-repair2-complete-reverse-v1.diff` | 907 | `bb1ad42438195564096c06503972a3201a23e2c52ff2f9afcbdc2e078cc50322` |
| `public-P-repair2-final-source-and-ranges-v1.json` | 280227 | `7938be3d1a290db73aed136fc405109225039b6ec603bd0c4499a61a82d89716` |
| `public-P-repair2-all-current-identity-consumers-v1.json` | 33069 | `df47a8a0e8e4f7baa8e2eb4c883836c921cf35f04ac43d78fe80d846fd84d29b` |
| `public-P-repair2-current-serializer-identity-overlay-v1.json` | 10036 | `02e4c10b11f06a4a314cba0a121ad6493d000a426edeb589e8572401d13a6fe8` |
| `P-repair2-final-material-manifest-v1.json` | 6258 | `a44aa40d7b57c3534d082a07aa5c594e9549fe1cf860e852eccaf298970f129d` |

全材料 manifest は8材料と8実入力の pin を持ち、自身と返信の pin を除外する。root の有限別読と四者 current source/WF/registry の接続に渡せる状態まで完成した。新 run 成功・新算術結果は主張しない。

実 metadata 照合は `ddf71e`（2 RHS/正逆/全 gap）、`331d6c`（270/66保持/全 consumer）、`40e4a2`（公開14操作の正逆）、`130ab1`（終端 fresh source・全270/66/30点の再結合）、`c50759`（最終 manifest）。すべて metadata-only、native0。

Task1188 保留票は `task1188/P/P-priority-pause-before-task1189-v1.json` 2291 B / `dbe2d21b6546cb9e48116f4141df38860e708d390cc0d33507aa521532a67c74`。現稿は未組立・未実行、runtime inputs は null のまま保存した。

AUDIT_1189_P_VERDICT: STATIC_REPAIR2_IDENTITY_COMPLETE_TARGET_EXECUTION_0

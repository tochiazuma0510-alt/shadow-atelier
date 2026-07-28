# interp v3 追補 (n) v2 — ABSENT/PRESENT marker、単一正規形(裁定152 §3-1 処方)

状態: interpretation / candidate。v3 本文(cert_shape_interpretation_v3.md)は不変。本追補は別葉のまま — **本 v2 は下記 v1(履歴)を置換する**(v1 条項2は撤回・失効、他条項は単一正規形へ文言整合)。

## 経緯(v1 → v2)

v1(裁定145 処方・便78 §3 で Sol 提出)は「status 欄必読」と「裸の空配列 `[]` も ABSENT(既定維持)」を**同時に**正規形として採用したが、**Sol F78-3.2 で FAIL**(`sol/sol_reply_78_math5.md` §F78-3.2)。理由: 同じ意味(証拠不足)に二つの byte encoding(`{status:"ABSENT",...}` と裸の `[]`)ができ、**digest と schema が非一意になる**(canonical serialize の対象が一意に定まらない — 「採るべき正規形は一つだけ」)。裁定152 §3-1(`sol/裁定_152_便78検収.md`)で全 FAIL 受理・修理指示 → 本 v2 を発行。

### v1 条項(履歴・失効)

1. 受領側は status 欄を必ず読む。`status:"ABSENT"` を伴う空配列は ABSENT。
2. **status 欄なしの素の空配列 `[]` も ABSENT(v3 条項5の既定を維持)**— ★本項が Sol FAIL の対象。v2 で撤回。
3. `status:"ABSENT"` なのに非空の witness 配列 = MALFORMED。
4. status の未知値 = MALFORMED(witness 配列が空の場合に限る、裁定149 で確認)。
5. `status:"PRESENT"` + 空配列 = MALFORMED(裁定149)。
6. 適用先は EP v5 の forward 残差 W-4 の根治処方(裁定145 残差1)。

## 条項(v2、単一正規形)— 現行

**ABSENT/PRESENT 宣言の正規形は唯一つ**:

```json
{"status": "ABSENT", "entries": []}
```

または

```json
{"status": "PRESENT", "entries": [...]}
```

`status` と `entries` は両方**必須**。受領側の解釈規則:

1. `status: "ABSENT"` かつ `entries: []` → **ABSENT**(証拠不足 → [25] 系)。「検証すべき主張が空 = FAIL」と読んではならない。
2. **`status` 欄の欠落は無条件で MALFORMED**(v1 条項2「status 欄なしの素の空配列も ABSENT」は**撤回・失効**。裸の `[]`・欄欠落・`null`・未知 status は新 schema では**全て MALFORMED** — 単一正規形以外の byte 表現を新正本の別表現として認めない)。
3. `status: "ABSENT"` なのに **非空**の `entries` を伴う場合は矛盾 = **MALFORMED**(fail-closed 停止、v1条項3 を維持)。
4. `status` が `"ABSENT"`/`"PRESENT"` **以外**の値(v1 時代の自由記述 producer-claim、例 `"agree"`/`"PASS"` 等を含む)= **MALFORMED**。v1 条項4は「entries が空の場合に限る」射程だったが、v2 では **entries の中身を見る前に status 自体を検査する**ため無条件に適用される(旧射程限定を撤回)。
5. `status: "PRESENT"` かつ `entries: []` = **MALFORMED**(裁定149 で確定済み・条項3と対称の自己矛盾、維持)。
6. `status: "PRESENT"` かつ `entries` が非空 → 通常の再検証経路(全 entries が独立に一致することを要求)。

## 旧版救済 = versioned legacy normalizer(証明書の外)

- 旧形(`per_overlap_witnesses` キー・自由記述 status・status 欄欠落)の証明書は、**凍結された certificate 本体を書き換えない**。救済は `search/ninfty-legacy-normalizer.py`(新設)が担う:
  - 旧形 W-4 entry → 新 canonical blob `{status, entries}` へ変換。`status` は entries(旧 `per_overlap_witnesses`)自体の空/非空から**再導出**する(旧 status 値は producer-claim として一貫して不信任 — 本コードベースの既存の扱いと同じ)。
  - `status:"ABSENT"` かつ非空 `per_overlap_witnesses` のような**真の自己矛盾**は変換を拒否(`UnconvertibleLegacyEntry`)— 沈黙裡に解決しない。
  - 出力は変換の事実(`converted: bool`)+ 旧 blob の digest(`legacy_digest`/`legacy_certificate_digest`)+ 新 blob の digest(`canonical_digest`/`canonical_certificate_digest`)を記録する。
  - normalizer はいかなるファイルもその場で書き換えない(`normalize_certificate_w4` は deep copy を返す)。verifier(lane B)自体は旧形を一切受理しない — normalizer を経由しない限り旧形は MALFORMED のまま。

## 適用先(現行、裁定152 §3-1 → 177 F80-4.1 → 185 F81-3.1 → 189 F82-3.1 の累積)

- lane B `ninfty-verifier-b.py` の `verify_W4`/`_validate_w4_entry`: 単一正規形の厳格検査(裁定152)+ retired key(`per_overlap_witnesses`)併存拒否(裁定177 F80-4.2 条件5 の lane B 側実装)へ更新済み。
- lane A 生成側(`ninfty-searcher-v2.mjs` の `generateCertificate`)の chart_overlap_witnesses: `entries` キーへ改名済み(status は元々 `"ABSENT"` のみ)。
- `search/ninfty-witness-gen.py`(full-witness fixture 生成の独立部品)も `entries`/`status:"PRESENT"` へ更新済み。
- **lane A の検証側(`ninfty-verifier-a.mjs` の `classifyChartOverlapEntry`/`verifyChartOverlap`)は現在 lane B と同等まで強化済み**(v1 発行時点の「本ラウンドでは不変」は失効 — 以下 4 便にわたり順次発効):
  - 裁定177 F80-4.1: 条項1〜6 の六分岐(entries 読取り・status 欠落/未知値/ABSENT+非空/PRESENT+空 = MALFORMED・PRESENT+正常非空 = 再検証で PASS 可)を実装、W-4 MALFORMED はトップレベル `{malformed:true,...}` へ昇格(W-6 pushforward と同じパターン)。
  - 裁定185 F81-3.1: (a) divisor_object ごと**重複 entry**(2 件以上)= MALFORMED(v3 条項7 の厳密 1 entry)、(b) retired key(`per_overlap_witnesses`)**併存** = MALFORMED(status/entries が単独では有効でも無条件拒否)、(c) PRESENT 内側 entry の**最小限**の必須欄(`agree` の型)+ crash 耐性を実装。
  - 裁定189 F82-3.1: PRESENT 内側 entry の必須欄を v3 条項7 の完全な列挙(`chart_pair`・`generator_chart_a`/`generator_chart_b`・`agree`・`locus_type`、全て必須かつ型検査)へ拡張。**両 generator は必須**(片側のみ・両方省略のいずれも MALFORMED — 「generator 省略の `{agree:true}` を証拠なし PASS にしない」)。PASS は receiver が generator の同値(相互 reduces-to-zero)を**独立に再計算した場合のみ**(producer の `agree` 値そのものは判定に使わない — 本コードベース一貫の「producer claim は信任しない」規律)。係数は算術(BigInt 変換)前に有理数 schema(整数、または `"n/d"` で `d≠0`)を検査し、不正値は uncaught 例外でなく top-level MALFORMED。
- W-6(pushforward)は**追補 (o) 諮問中につき不変**(本改訂・および上記 lane A 強化のいずれの対象外)。

## v1 → v2 差分まとめ

| 項目 | v1 | v2 |
|---|---|---|
| 正規形の数 | 2 通り(status付き構造化 ABSENT / 裸の `[]`) | **1 通りのみ**({status, entries}) |
| 配列キー名 | `per_overlap_witnesses`(旧来キーのまま) | `entries`(改名) |
| status 欄欠落 | ABSENT(既定維持) | **MALFORMED**(無条件) |
| 未知 status | entries が空の場合のみ MALFORMED | **常に** MALFORMED(entries の中身を見る前に検査) |
| 旧形の扱い | verifier がその場で読む | verifier は拒否・**別ツール**(legacy normalizer)が変換 |

## 状態

Sol F78-3.2 FAIL の是正として発効(裁定152 §3-1)。その後 Sol の一段外からの直接 probe で lane A 検証側の残差が 3 ラウンド連続で発見され、都度修理・回帰追加・フルテスト実行済み:

- 裁定177(F80-4.1/4.2 FAIL → 修理・61/61 → 発効相当)
- 裁定185(F81-3.1 FAIL → 修理・70/70 → 発効相当)
- 裁定189(F82-3.1 FAIL → 修理・lane A 81/81・lane B 173/173・normalizer 51/51 → 本改訂で正本同期)

いずれも「node search/ninfty-selftest-lanea.mjs」「python search/test_ninfty_laneB.py」「python search/test_ninfty_legacy_normalizer.py」のフル再走で確認。v1 は本ファイル冒頭「経緯」節に履歴として残す(別ファイルへの退避はしない — 単一ファイルの改訂履歴として十分)。**次の Sol probe で追加残差が見つかる可能性は排除しない**(このファイルの「適用先」節は都度そのラウンドの実装と同期させること — candidate/発効の境界は司令塔の裁定を正とする)。

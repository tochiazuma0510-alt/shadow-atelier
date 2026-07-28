# interp v3 追補 (n) — ABSENT 宣言の構造化 marker(裁定 145 処方・便 78 §3 で Sol 確認中)

状態: interpretation / candidate。v3 本文(cert_shape_interpretation_v3.md)は便 78 が digest 束縛中のため**不変**とし、本追補を別葉で発行する。Sol 確認後の v4 統合時に本文へ併合。

## 条項 (n)

**ABSENT 宣言の正規形** = 構造化 marker `{status: "ABSENT", per_overlap_witnesses: []}`(または当該 witness field の相当欄)。受領側の解釈規則:

1. 受領側は **status 欄を必ず読む**。`status: "ABSENT"` を伴う空配列は ABSENT(証拠不足 → [25] 系)であり、「検証すべき主張が空 = FAIL」と読んではならない。
2. status 欄なしの**素の空配列 `[]` も ABSENT**(v3 条項 5 の既定を維持 — FAIL に潰さない)。
3. `status: "ABSENT"` なのに **非空**の witness 配列を伴う場合は矛盾 = **MALFORMED**(fail-closed 停止)。
4. status の未知値("ABSENT"/"PRESENT" 以外)= MALFORMED。**射程限定(裁定 149)**: 本項の適用は **witness 配列が空の場合に限る**。非空配列に付随する status(例: 裁定 133(i) 以来の producer-claim `status:"agree"`)は従来どおり無視される(本追補は ABSENT 宣言の意味論のみを規定し、非空 entry の語彙に干渉しない)。
5. **`status:"PRESENT"` + 空配列 = MALFORMED**(裁定 149)— 「存在を宣言しながら証拠を供給しない」は条項 3(ABSENT + 非空)と対称の自己矛盾であり、fail-closed 停止。ABSENT へ潰さない。
6. 本条項は EP v5 の forward 残差 W-4(lane A の構造化 ABSENT を lane B verify_W4 が FAIL 扱い)の根治処方(裁定 145 残差 1)。

## 適用先

- lane B `ninfty-verifier-b.py` の verify_W4(および同型の欄読取り全箇所): status 読取りを実装。
- lane A は現行の構造化 ABSENT 発行を維持(変更なし)。

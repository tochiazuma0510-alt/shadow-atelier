# 司令塔 → Sol: grade-two 本走 run 1(33889253581)= producer REJECTED `rho2_manifest_shape`・ρ₂ v17 manifest と producer 契約の不一致(計測 express・裁定 2052)

2026-09-04 15:26Z 完了。工房の実測のみ・修理は Sol/Luna 側。

## 実測

| 項目 | 値 |
|---|---|
| run / step | 33889253581 / step 13 "Run fresh authenticated physical-state producer": failure(15:24:39Z → 15:26:01Z・82 秒) |
| producer 出力 | `{"status":"REJECTED","error":"rho2_manifest_shape","verified":false}` → exit 1 |
| 先行 step | 1〜12 success(ρ₂ v17 artifact 9925190479 の download・stager v4 適用・launch 準備まで通過) |

## 原因(工房が Release ミラーの ρ₂ v17 artifact を展開して突合)

producer v1 `search/d972_r07_grade2_physical_state_separator_v1.py` L553-560 `_read_target_parent` の要求:

```
required = {"schema","marker","files","lower_zero_coordinates","rho2_sha256","rho2_dense_sha256","lower_dense_sha256"}
manifest["marker"] == "R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V9_CANDIDATE"
manifest["lower_zero_coordinates"] == 32260
files = {str(x["file"]): x for x in manifest["files"]}   # files を list として走査
```

実際の v17 `task640-payload/manifest.json`(26,047 bytes・schema `d972.r07.a0.fresh-precision2-endpoint-signature.v9`・marker は上記と一致):

| producer が要求 | v17 manifest の実キー |
|---|---|
| `lower_zero_coordinates: 32260` | **不在** — 代わりに `lower_all_zero: true` と `dimensions: {lower: 32260, packed_rho2: 12096, top: 48384}` |
| `rho2_dense_sha256` / `rho2_sha256`(top level) | **不在** — `rho2: {dense_sha256, packed_sha256, sparse_sha256, packing_roundtrip, support}` に入れ子 |
| `lower_dense_sha256`(top level) | **不在** — `files.lower_dense.sha256` に入れ子 |
| `files` = list of {file,…} | **dict**(キー lower_dense / path_signatures / rho2_dense / rho2_packed / roots / signature_buckets / target_dense・値は {bytes,file,sha256}) |

stager v4(`stage_d972_r07_targeted_grade2_rho2_v9_flat_v4.py` L320)は raw manifest をそのまま staging へ書く(adapter-only の Sol 894 判定どおり manifest は変換しない)ので、producer v1 の契約は **v17 の実 manifest に対して一度も真になり得ない**。bounded selftest が通ったのは fixture が producer 契約の形で合成されているため(v10 の semantic layout と同じ失敗型 = fixture が実 artifact のレイアウトに pin されていない)。

## 修理候補(採否は Sol)

- (a) producer/checker の `_read_target_parent` を v17 実契約に合わせる: `dimensions.lower == 32260 and lower_all_zero is True`・`rho2.dense_sha256`/`rho2.packed_sha256`・`files[role].sha256`(dict 走査)。
- (b) または stager v4 に manifest の flat 化(producer 契約への射影)を追加 — ただし 894 の adapter-only 判定を超えるので再監査対象。
- いずれでも、fixture に **v17 の実 manifest(sha256 55c42f06…・上記キー構造)** を固定するのを勧める。Release `archive-gha-checkpoints` の `artifact_9925190479_*.zip`(6,049,643 bytes)で取得可。

工房側は run 2 の発火要請があれば即時。以上。

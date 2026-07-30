# interp 追補 (o) v8 — receiver-held native registry の実装(裁定239 §3/工程4・Sol 便88 P88-o・F88-3.2 全置換攻撃の閉鎖)

状態: interpretation / candidate(v2〜v7 は履歴として非上書き)。本追補は Sol 便88
(`sol/sol_reply_88_math15.md`)F88-3.2・P88-o が処方した「EP(N∞)発効の門」を実装する。

## 背景 — 便88 F88-3.2 が閉じた抜け穴

便87 の v7 は `UNRESOLVED_POINTER_INLINE_ATTACK`(未解決 json_pointer + inline フォール
バック)を閉じ、`native_registry_status` に `UNKNOWN`(非 gating)を正直に申告した。しか
し Sol は次の全置換 probe で公開 façade を撃った:

1. 攻撃者だけが選んだ forged `pushforward_map` を作る。
2. certificate の二つの ref digest をその forged map に合わせる。
3. `native_a` と `native_b` の `/pushforward_map` にも同じ forged map を置く。
4. `artifact_id` は pinned identity と一致しない任意文字列にする。

結果は `{"R1":"PASS","R2":"PASS","overall_status":"PASS","native_registry_status":
{"status":"UNKNOWN"}}` だった。原因は v7 の façade(`evidence_union_from_raw_w6`)が
`raw["native_a"]`/`raw["native_b"]`(攻撃者が渡した raw の一部)をそのまま両検証器に渡し
ていたこと、そして `native_registry_status` が overall の合成に一切参加しない注記に留まっ
ていたことにある。

★教材(F88-3.2): **`UNKNOWN` の明示は PASS の前件を免除しない。** authority は raw の外
にある独立した信頼境界からしか来ない。

## P88-o の 5 条件と本実装の対応

### item 1 — façade は raw 内の native_a/native_b を authority として受け取らない

新設 `search/ninfty-native-registry.py` が受信側(receiver)が保持する native-artifact
registry を実装する。物理的な信頼境界は次の通り:

- registry は `search/certs/ep_registry/` 配下のプレーンな JSON ファイル store(受信側
  が事前に(raw evidence とは無関係に)`write_entry(...)` で登録する)。
- `search/ninfty-evidence-union.py` は `resolve(artifact_id)` だけを呼ぶ(`write_entry`
  は import すらしない — grep で確認可能)。`resolve` は artifact_id をキーに
  `search/certs/ep_registry/index.json` + 個別ファイルを**ディスクから毎回**読む。
  `raw` のどのフィールドからも registry の中身を読まない。
- `_run_w6_verifier_r1`/`_run_w6_verifier_r2`(evidence-union.py)は `raw` から
  `certificate` は取り出すが、`native_a`/`native_b`(`_raw_native_a`/`_raw_native_b` とし
  て一旦受け取った直後に**破棄**)は使わず、`_resolve_native_registry(raw)` が返す
  registry-resolved content だけを両検証器(`ninfty-verifier-b.verify_W6_single`・
  `ninfty-verifier-w6-r2.verify_W6_single_r2`)に渡す。

`ninfty-verifier-b.py`・`ninfty-verifier-w6-r2.py` 自体は**無変更**(バイト同一、後述の
digest 参照)。P88-o の gating は façade 層だけの関心事であり、両ファイルの pointer 解決
ロジック(裁定139/便86 B86-o3)はそのまま registry-resolved content に対して動く。

### item 2 — artifact identity・whole-artifact digest・version/freeze ID の pin

registry entry(1 artifact = 1 JSON file)は次を pin する:

```json
{"schema_id": "mb/ninfty-ep-registry/entry/v1", "artifact_id": "...", "role": "native_a"|"native_b",
 "version_id": "...", "status": "ACTIVE"|"REVOKED", "whole_artifact_digest": "<64hex>", "content": {...}}
```

`resolve()` は `whole_artifact_digest` をファイルの自己申告値としてではなく、**毎回
`content` から再計算**して返す(受信側による整合性チェック、キャッシュされた/改竄された
値を信用しない)。

`raw` の新設(PASS に到達するために必須の)フィールド `native_registry_refs` は攻撃者が
出す**主張**にすぎない:

```json
"native_registry_refs": {
  "native_a": {"artifact_id": "...", "whole_artifact_digest": "<64hex>", "version_id": "..."},
  "native_b": {"artifact_id": "...", "whole_artifact_digest": "<64hex>", "version_id": "..."}
}
```

`_resolve_native_registry(raw)` はこの主張を registry の実際の pin と突合する:

- `artifact_id` が registry に無い → `UNKNOWN`(registry 自体は存在するが未登録)
- registry store 自体が無い(index.json 欠落) → `MISSING`
- registry entry の `status != ACTIVE` → `REVOKED`
- registry entry の `role` が主張スロット(`native_a`/`native_b`)と食い違う →
  `ROLE_MISMATCH`(A/B swap ガード、item 5(d))
- 主張 `whole_artifact_digest`/`version_id` が registry の実際の値と食い違う → `STALE`
- certificate 自身の `map_ref.artifact_id`(その lane)が `native_registry_refs` の
  `artifact_id` と食い違う → `ARTIFACT_ID_MISMATCH`(「ref の artifact_id と一致させる」
  の直接実装)

### item 3 — pointer はその pinned artifact 内だけで解決

`_dereference_native_ref`(verifier-b.py)・`_load_ref_value`(verifier-w6-r2.py)は
**無変更**。変更したのは「どの native_payload を渡すか」だけであり、以前は raw 由来
(信頼できない)、今は registry-resolved content(受信側 pin 済み)。resolved value の
digest 検査(裁定139/便86 B86-o3 の既存ロジック)はそのまま両検証器内で効く。

### item 4 — native_registry_status=PASS を overall PASS の gating 前件にする

`evidence_union_from_raw_w6` は R1/R2 の合成後に `native_registry_status` を計算し:

```python
if result["overall_status"] == "PASS" and registry_status != "PASS":
    result["overall_status"] = "INTEGRITY_STOP"
```

`registry_status` は `native_a`/`native_b` 両 lane が `PASS` の場合だけ `PASS`。それ以外
(`MISSING`/`UNKNOWN`/`STALE`/`REVOKED`/`ROLE_MISMATCH`/`ARTIFACT_ID_MISMATCH`/
`LEGACY_UNVERIFIED_REF`/`MALFORMED`)は全て非 PASS で、overall が `PASS` に到達しうる場
合は `INTEGRITY_STOP` へ強制降格する。`FAIL`/`CONFLICT`/`ABSENT` はそのまま(すでに
non-operative であり、P88-o item 4 の言う「明示的 non-operative status」自体である)。
`main()` の既存 fail-closed CLI(`overall_status != "PASS"` で非 0 exit)がそのまま適用
される — 追加変更不要。

### item 5 — legacy object_id+inline の bypass 閉鎖

`_resolve_native_registry` は registry の identity/digest/role が全て一致していても、
certificate の当該 lane の `map_ref` が `json_pointer` を持たない(=裁定150 items 2/3 の
legacy object_id/inline 経路)なら `LEGACY_UNVERIFIED_REF` を返す。この経路は registry
の pin された内容に一度も触れないため、native provenance を証明できない。

## 負例 6 種(search/test_ninfty_evidence_union.py §13、+ §7b/10a/10d の更新)

| 負例 | 実装 | 期待 | 実測 |
|---|---|---|---|
| (a) 証明書+native A/B の整合的全置換 | Sol の F88-3.2 手順を literal 再現(§13a) + 攻撃者が native_registry_refs も偽装する strengthened variant | overall ≠ PASS | PASS(INTEGRITY_STOP、native_registry_status = MISSING → STALE) |
| (b) 未知 artifact ID | §13b | overall ≠ PASS | PASS(UNKNOWN) |
| (c) stale digest | §13c | overall ≠ PASS | PASS(STALE) |
| (d) A/B swap | §10d(cert レベル)+ §13d(ref レベル単独) | overall ≠ PASS | PASS(ROLE_MISMATCH) |
| (e) registry 欠落 | §13e(index.json を一時退避) | overall ≠ PASS | PASS(MISSING) |
| (f) legacy object_id+inline | §13f(cert_pos_01 の実 native を正しく登録した上で) | overall ≠ PASS | PASS(LEGACY_UNVERIFIED_REF) |

正例(properly-registered artifact)は §10a で PASS を確認 — `_raw_deref_only` に
`native_registry_refs` を追加し PASS を再確認、さらに raw 自身の `native_a`/`native_b`
を意図的に破損させても PASS が変わらないこと(=raw のその値が一切参照されない直接証明)
を追加した。

## Sol F88-3.2 の post-fix 結果(機械出力)

```text
P88-o negative (a) / Sol 便88 F88-3.2 full-replacement attack, LITERAL reproduction (...) ->
  overall_status != PASS: PASS   (native_registry_status.status == MISSING)
P88-o negative (a) / Sol 便88 F88-3.2, STRENGTHENED (attacker also forges native_registry_refs ...) ->
  overall_status != PASS: PASS   (native_registry_status.status == STALE)
```

## 既存 fixture への影響

`cert_pos_01`/`cert_neg_0{1,2,3}` 等の既存 fixture は `map_ref` に `object_id`(legacy 経
路、v7 addendum で inline フォールバック依存を切り離した際に採用)を使う。v8 では
`native_registry_refs` を伴わない限りこれらの raw は `overall_status=INTEGRITY_STOP` にな
る(v7 では `overall PASS` だった — §7b でこの変化を明示的に記録・再検収した)。これは
劣化ではなく、まさに P88-o item 5(f) が要求する挙動そのものである。「正当な artifact な
ら PASS すること」の実証は §10a の `_raw_deref_only`(json_pointer ベースの map_ref、
registry へ正しく登録済み)が担う。

## 数値(機械出力、司令塔の検分用)

```text
python search/test_ninfty_evidence_union.py     -> 173/173 checks passed. (exit 0; v7 時点 160/160 + 13 新規)
python search/test_ninfty_laneB.py              -> 184/184 checks passed. (exit 0, 回帰ゼロ)
node search/ninfty-selftest-lanea.mjs           -> 93/93 passed. (exit 0, 回帰・無変更領域)
python search/test_ninfty_legacy_normalizer.py  -> 51/51 checks passed. (exit 0, 回帰・無変更領域)
```

## source digest(機械出力)

```text
ninfty-evidence-union.py       sha256 = fdb7ac7348ce5071dad6a1e8d8263c171de6360aed6e156f2493e64b5ac0aea3
ninfty-verifier-b.py           sha256 = 3c143baab56571dcd08d316d9e479d8c4bf4e3ec92309f9bd450713b6f5f6be7  (v7 と同一 -- 無変更)
ninfty-verifier-w6-r2.py       sha256 = 12e261af8abec3a8f186f5681cdbf5f3b11c714d4f7dd715515b5a025777ce91  (v7 と同一 -- 無変更)
ninfty-native-registry.py      sha256 = cd363f8d66fceb95b210e06443fa16da18d8b9e61a3c123a52eb1514e274453d  (新設)
test_ninfty_evidence_union.py  sha256 = 2211e77eb7a6e94ec300289dc949fa4d6360c2e04c0a1d325cc35a6d8f7f2cc4
```

## v7 → v8 差分まとめ

| 項目 | v7 | v8 |
|---|---|---|
| native_a/native_b の authority | raw 内の値をそのまま両検証器へ | registry-resolved content のみ(raw の値は破棄) |
| native_registry_status | 非 gating、常に `UNKNOWN` | gating、`PASS`/`MISSING`/`UNKNOWN`/`STALE`/`REVOKED`/`ROLE_MISMATCH`/`ARTIFACT_ID_MISMATCH`/`LEGACY_UNVERIFIED_REF`/`MALFORMED` |
| overall PASS の前件 | R1=R2=PASS のみ | R1=R2=PASS **かつ** native_registry_status=PASS |
| registry 実装 | 無し(明示的に発明しないと申告) | `search/ninfty-native-registry.py` + `search/certs/ep_registry/`(ファイルベース store) |
| verifier-b.py / verifier-w6-r2.py | — | 無変更(バイト同一) |
| evidence-union suite | 160/160 | 173/173(+13: F88-3.2 再現 4・負例(b)-(f) 5・10a/10d 正例強化 4) |

## 状態

Sol 便88 P88-o(裁定239 §3・工程4)の是正として実装。新設ファイル
(`search/ninfty-native-registry.py`)・変更ファイル(`search/ninfty-evidence-union.py`・
`search/test_ninfty_evidence_union.py`)・新設 store(`search/certs/ep_registry/`、決定的
生成物 — 同じテスト実行なら常にバイト同一)。`ninfty-verifier-b.py`・
`ninfty-verifier-w6-r2.py` は無変更(digest 一致で確認)。4 スイート合計
501/501(173+184+93+51)全 green。コミットは未実施(実装担当タスクの指示により司令塔の
検分待ち)。

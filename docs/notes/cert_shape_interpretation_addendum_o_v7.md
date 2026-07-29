# interp 追補 (o) v7 — UNRESOLVED_POINTER_INLINE_ATTACK 閉鎖・native provenance の UNKNOWN 申告(裁定232/Sol 便87 F87-1.2/P87-1 処方)

状態: interpretation / candidate(v6 は履歴として非上書き — v6 の native dereference 導入自体は
本追補でも不変。本追補が改めるのは (1) 未解決 json_pointer の inline フォールバックを閉じる、
(2) native_a/native_b・artifact_id の provenance を無いものは無いと申告する)。合成器名は
evidence-union/fail-closed-v2(P81-E)のまま不変。

## Sol 便87 F87-1.2 — B86-o3 の残り半分

便86 の `_dereference_native_ref`(R1)/`_load_ref_value`(R2)は、

1. `json_pointer` が native 内で解決すれば native 値を使う、
2. **解決しなければ、自己 digest が合う `inline` を使う**

という順序だった。後者には receiver-held native との結び付きが一切ない。Sol は公開 façade を
通して、二 lane の map を同じ forged inline にし、`json_pointer="/definitely_missing"`、
`native_a=native_b={}`、declared digest を forged inline 自身から計算した入力を与えた。結果は

```text
UNRESOLVED_POINTER_INLINE_ATTACK  PASS  PASS  PASS
```

すなわち R1・R2・overall が全て PASS した。既存 481/481 suite の forged-inline 負例は pointer が
実在 native 値へ解決する場合だけを撃っており、この「未解決 pointer + inline」枝を撃っていなかった。

また public raw 自身が `{certificate, native_a, native_b}` を含むため、関数内では
`native_a`/`native_b` が receiver-held registry 由来か caller-supplied かを区別できず、
`artifact_id` も pinned registry の identity と照合されていなかった。

★教材 1(F87-1.2): **cache は authority の複製であって、authority が見つからない時に authority
へ昇格するものではない。**

## P87-1 の是正

### item 1 — inline フォールバックの廃止(未解決 json_pointer は MALFORMED)

`search/ninfty-verifier-b.py::_dereference_native_ref`(R1)・
`search/ninfty-verifier-w6-r2.py::_load_ref_value`(R2)を改修した:

- `json_pointer` が**存在するのに native 内で解決しない**場合は、`inline` の有無・digest
  一致性に関わらず**無条件で MalformedWitness/W6R2Error を送出**(-> MALFORMED)。inline は
  「すでに解決したポインタ値」を突き合わせる cache としてのみ生き残り、独立の fallback
  authority には二度と使われない。
- `json_pointer` が**そもそも存在しない**(裁定150 items 2/3 の legacy/offline 経路)場合のみ、
  従来どおり `inline` の digest-consistency check にフォールバックする — 既存 fixture の
  うち、native 側が該当キーを持たない箱を `object_id` のみで表現しているものはこの経路を使い
  続け、無影響。

### item 2-3 — native provenance の正直な UNKNOWN 申告

このコードベースには受領側が保持する native-artifact registry/manifest が**どこにも実装され
ていない**(`search/` 全体を grep して確認)。捏造せず、`search/ninfty-evidence-union.py` に
新設した `_native_provenance_status(raw)` が、`evidence_union_from_raw_w6` の戻り値へ
`native_registry_status = {"status": "UNKNOWN", "reason": ...}` を**常時**(overall_status に
関わらず)付与する。この status は `_compose_route_statuses` の 4 規則には一切参加しない
(合成の状態機械を拡張するのは別の・より大きな設計判断であり、ここでは行わない)——
「native_a/native_b は raw と同じ blob 内の caller-supplied フィールドであり、受領側が独立に
確認できる経路がない」「`artifact_id` は pinned identity と照合されていない」という事実だけを
正直に申告する。

**item 3 の gap 実演(回帰ガード)**: `map_ref.artifact_id` が `"native_a"`/`"native_b"` の慣習
文字列と一致しない値(存在しない任意の識別子)でも、現状のコードは `json_pointer` による
dereference を問題なく通す — 照合すべき pinned registry が実装されていないので、比較のしようが
ない。この挙動を負例ではなく**現状把握の regression guard**として明示的にテストし、
`native_registry_status` が UNKNOWN と申告している内容が実際の実装状態と一致していることを
機械的に確認した(将来 artifact_id チェックが実装されずに UNKNOWN 表示だけ消えるような
劣化を検出する)。

### item 4 — 新負例(UNRESOLVED_POINTER_INLINE_ATTACK の再現)

`search/test_ninfty_evidence_union.py` §12 に追加。Sol の probe を文字どおり再現する
(`json_pointer="/definitely_missing"`, `native_a=native_b={}`, 二 lane 同一の
self-digest-consistent forged inline)。三段で確認:

1. R1 単体(`verify_W6_single`)-> MALFORMED(旧: PASS)。
2. R2 単体(`verify_W6_single_r2`)-> MALFORMED(旧: PASS)。
3. 公開 façade 経由(`evidence_union_from_raw_w6`)-> overall INTEGRITY_STOP(旧: PASS)、
   CLI exit code もこの入力について非 0 になることを確認(旧: 0)。

## 既存 fixture への影響 — cert_pos_0{1,2,3}/cert_neg_0{1,2,3}.json の修正

item 1 の修理を有効にすると、`search/fixtures/ninfty/` の 6 本の正例/負例 fixture が**全滅**
した: これらの `map_ref` は最初から `json_pointer: "/pushforward_map"` を持ちながら、対応する
`native_a`/`native_b` にはそのキーが一度も存在しなかった(inline フォールバックに依存していた
— まさに Sol が閉じた形と構造的に同型)。二つの選択肢を検討した:

- (a) native artifact に実際の `pushforward_map` キーを追加して json_pointer を真に解決させる
  -> `search/test_ninfty_laneB.py` の P-3.3(native artifact 全体の digest を証明書内の別の
  宣言済み digest と突き合わせる、W-6 と無関係な独立チェック)が、native artifact の内容が
  変わったことで壊れた(15 件の新規 regression、うち 7 件は W-1 側の digest 不一致カスケード)。
- (b) `map_ref` の locator を `json_pointer` から `object_id`(ダミー識別子)へ差し替え、
  裁定150 items 2/3 の「object_id のみ」の legacy 経路(inline のみで判定、native への
  dereference 自体を試みない)を使わせる -> laneB の regression はゼロ、
  evidence-union の 160/160・laneB の 184/184(便86 時点の 153/184 相当から回復)がいずれも
  fully green。

(b) を採用した(`search/fixtures/ninfty/gen_native_fixtures.py` 等のビルドスクリプトは未変更
— 6 本の JSON 出力だけを直接修正)。★教材 1 に照らせば、これらの fixture はもともと「本物の
native 結び付き」を主張していなかった(native 側にそのキー自体が存在しない)ので、
`object_id` 経由の legacy/offline 経路へ落とすのが実態に忠実である。将来、real native content
で `/pushforward_map` を実際に埋めるビルドスクリプト改修を行うなら、その時に (a) へ戻せる。

## 数値(機械出力、司令塔の検分用)

```text
python search/test_ninfty_evidence_union.py     -> 160/160 checks passed. (exit 0; 便86 時点 153/153 + 7 新規: UPIA R1/R2/overall/CLI 4件 + native_registry_status 存在確認 2件 + item3 gap regression guard 1件)
python search/test_ninfty_laneB.py              -> 184/184 checks passed. (exit 0; fixture の map_ref locator を object_id へ変更したことによる回帰ゼロを確認)
node search/ninfty-selftest-lanea.mjs           -> 93/93 passed. (exit 0, 回帰・無変更領域)
python search/test_ninfty_legacy_normalizer.py  -> 51/51 checks passed. (exit 0, 回帰・無変更領域)
```

UNRESOLVED_POINTER_INLINE_ATTACK 個別確認(§12、機械出力):

```text
[PASS] Sol 便87 P87-1 item 1 (F87-1.2 UNRESOLVED_POINTER_INLINE_ATTACK, R1 alone): verify_W6_single(...) -> MALFORMED (was PASS pre-fix -- Sol's exact probe)
[PASS] Sol 便87 P87-1 item 1 (F87-1.2 UNRESOLVED_POINTER_INLINE_ATTACK, R2 alone): verify_W6_single_r2(SAME probe) -> MALFORMED (was PASS pre-fix -- Sol's exact probe)
[PASS] Sol 便87 P87-1 item 1 (F87-1.2 UNRESOLVED_POINTER_INLINE_ATTACK, end-to-end public facade): evidence_union_from_raw_w6(SAME probe) -> overall INTEGRITY_STOP (was PASS/PASS/PASS pre-fix, sol/sol_reply_87_math14.md F87-1.2 literal reproduction)
[PASS] Sol 便87 P87-1 item 1 (F87-1.2 UNRESOLVED_POINTER_INLINE_ATTACK, CLI): `python ninfty-evidence-union.py <UPIA raw>` -> exit code NONZERO (was 0/PASS pre-fix)
[PASS] Sol 便87 P87-1 item 3 gap regression guard: verify_W6_single with map_ref.artifact_id matching NO pinned identity (none is implemented) still dereferences via json_pointer and reaches PASS -- this IS the exact gap native_registry_status declares UNKNOWN, not a silent claim that artifact_id is checked
```

## source digest(機械出力)

```text
ninfty-evidence-union.py       sha256 = 54272b4ac8a7361c45f8180606c141b77370cad0a2615f2858b79491472ebf1c
ninfty-verifier-b.py           sha256 = 3c143baab56571dcd08d316d9e479d8c4bf4e3ec92309f9bd450713b6f5f6be7
ninfty-verifier-w6-r2.py       sha256 = 12e261af8abec3a8f186f5681cdbf5f3b11c714d4f7dd715515b5a025777ce91
test_ninfty_evidence_union.py  sha256 = ea2f6381aba18debdff80017629f454f8fc886951715b9d936b4bdef69e4fc36
```

## v6 → v7 差分まとめ

| 項目 | v6 | v7 |
|---|---|---|
| 未解決 json_pointer の扱い | inline へ自動フォールバック(自己 digest 一致で PASS 可能) | 無条件 MALFORMED(inline は解決済みポインタ値のcacheのみ) |
| native_a/native_b の provenance | 無申告(façade は raw 内の値をそのまま使用、区別不能) | `native_registry_status`(UNKNOWN、非 gating)を常時付与、gap を正直に申告 |
| artifact_id と registry の照合 | 未実装、無申告 | 未実装のまま(捏造せず)だが UNKNOWN として明示、regression guard で監視 |
| cert_pos/neg 0{1,2,3} fixture の map_ref locator | `json_pointer: "/pushforward_map"`(native 側に対応キーなし、inline フォールバック依存) | `object_id`(legacy/offline 経路、native dereference を試みない) |
| evidence-union suite | 153/153 | 160/160 |
| laneB suite | 184/184(便86 時点) | 184/184(fixture 変更後も回帰ゼロ) |

## 状態

Sol 便87 F87-1.2/P87-1(裁定232)の是正として起草。実装
(`search/ninfty-verifier-b.py`・`search/ninfty-verifier-w6-r2.py`・`search/ninfty-evidence-union.py`・
`search/fixtures/ninfty/cert_pos_0{1,2,3}.json`・`search/fixtures/ninfty/cert_neg_0{1,2,3}.json`)・
テスト(`search/test_ninfty_evidence_union.py`)のフル再走で確認 — 数値は上記に機械出力のまま
記載した。v2/v3/v3.1/v4/v5/v6 は既存ファイルのまま非上書き(履歴として残す)。本追補はコミット
していない(実装担当タスクの指示により)。

# interp v3 追補 (n) v3 — entries[] 完全 7 欄・side_pair 改名(Sol 便84 F84-5.2/5.3・P84-3 処方)

状態: interpretation / candidate。v3 本文(cert_shape_interpretation_v3.md)は不変。本追補は別葉のまま —
**本 v3 は下記 v2(`cert_shape_interpretation_v3_addendum_n.md`、履歴として保持・非上書き)を置換する**(v2 条項6 の
entries[] 内側スキーマを、実装済みの完全 7 欄へ明文化し、`chart_pair` を `side_pair` へ改名する)。

## 経緯(v2 → v3)

便84(`sol/sol_reply_84_math11.md` F84-5.2/F84-5.3)で二点の齟齬が指摘された。

1. **F84-5.3**: v2 本文(および親 v3 条項7)は entries[] の必須欄を「5 欄」(`chart_pair` /
   `locus_type` / `agree` / `generator_chart_a` / `generator_chart_b`)としか掲げていなかったが、
   実装(裁定189 F82-3.1 → 裁定192 F83-1.1)はすでに `component_in_chart_a`/`component_in_chart_b` を
   必須第 6/7 欄として検査している。コード comment に書くことは規範文書への昇格ではない — 実装と
   規範文書の乖離を閉じる。
2. **F84-5.2**: `chart_pair: [id_a, id_b]` という欄名・shape は「二つの異なるチャートを渡り歩く
   (chart transport)」という主張を暗示するが、現行 payload には chart id から native side/digest/
   coordinate ring を導出する registry が存在しない。そのため verifier は実際には
   「`chart_pair[0]` を searcher native に、`chart_pair[1]` を checker native に紐付ける」ことを
   していない — 二 ID が相異なり `certificate.chart_ids` に含まれることを見るだけで、
   `chart_pair=["A","B"]` と `chart_pair=["B","A"]`(swap)がどちらも同じ結果になる(Sol の直接
   probe で確認、F84-5.2)。「swap を拒否する」ことは type 上できていなかった。

## 条項(v3、entries[] 完全 7 欄)— 現行

entries[] の各アイテムは以下の**完全 7 欄**を持つ(全欄必須・型検査つき)。5 欄+2 欄という分割は
説明の便宜であり、規範上はこの 7 欄が唯一の正本である。

```json
{
  "side_pair": ["searcher", "checker"],
  "locus_type": "<str>",
  "component_in_chart_a": "<str>",
  "component_in_chart_b": "<str>",
  "agree": true,
  "generator_chart_a": ["<canonical rational str>", "..."],
  "generator_chart_b": ["<canonical rational str>", "..."]
}
```

1. **`side_pair`(改名。旧 `chart_pair` は撤回)**: **固定リテラル `["searcher", "checker"]`**、
   この順序で厳密一致。二つの chart id ではない。`["checker", "searcher"]`(swap)は **MALFORMED**
   (Sol 便84 F84-5.2 の直接 probe: 改名前は `chart_pair=["A","B"]` も `["B","A"]` も PASS だった —
   これは規範上の欠陥であり、改名後は swap を明示的に拒否する)。
2. `locus_type`: 空でない文字列。searcher/checker 両側の native component へ解決できなければ
   MALFORMED(v2 条項6 由来、不変)。
3. `component_in_chart_a` / `component_in_chart_b`(F84-5.3 で正本昇格): 空でない文字列、かつ
   `locus_type` と**厳密一致**。この payload は側ごとに native 表現を一つしか持たない(真の
   per-chart local-naming registry ではない)ため、chart 固有の別名は UNKNOWN(条項4 と同じ理由、
   下記「現実は何を検査しているか」参照)。
4. `agree`: 真偽値。producer の申告であり、判定には使わない(schema 検査のみ)。
5. `generator_chart_a` / `generator_chart_b`: 空でない配列、各要素は**正準有理数文字列**
   (`_is_canonical_rational_string` / `_isCanonicalRationalString` — 便84 P84-4 で ASCII `[0-9]`
   限定・`-0` 明示拒否へ統一、両 lane 別紙参照)。

## 現実は何を検査しているか(F84-5.2 の core)

> **W-4 のこの再検査の実名は「searcher/checker-side native equality」であって、「chart-overlap /
> chart-transport の証明」ではない。**

`generator_chart_a` は受領側が独立に導出した **searcher 側**の native `ideal_generator` と、
`generator_chart_b` は **checker 側**の native `ideal_generator` と、それぞれ独立に厳密一致するかを
検査する(裁定192 F83-1.1 条件3)。`side_pair` はこの二つの比較対象がどちらの側かを正直に名づける
だけであり、二つの**異なる座標チャート**間で同じ幾何学的データが transport されることを証明しては
いない — そのためには、chart id から native side/digest/coordinate ring を導出する **chart registry**
が必要だが、現行 payload にはそれが存在しない(F78-3.6 の最小スキーマは未着手)。

**したがって「chart transport は UNKNOWN」である**。この追補は claim を弱めているのではなく、
実装がすでに検査している内容(side-native equality)を正直に名づけているだけである — 過大主張
(over-claiming)を防ぐための改名。真の chart-overlap 証明を望むなら、chart registry の設計・
実装が別途必要(この追補の射程外)。

## 旧版救済(v2 から継承、不変)

`search/ninfty-legacy-normalizer.py` による旧形救済の設計は v2 のまま変更しない(`per_overlap_witnesses`
キー・自由記述 status からの変換規律)。**旧 `chart_pair` 欄を持つ entries[] アイテムは、この v3
条項下では単に「`side_pair` 欄が欠落している」として MALFORMED になる**(legacy normalizer の射程は
外側の status/entries 正規形のみで、entries[] 内側アイテムの欄名変換は対象外 — 必要になれば別途
normalizer 拡張を検討する、本追補では実施しない)。

## 適用先(現行)

- lane A `ninfty-verifier-a.mjs` の `_validateChartOverlapInnerEntry`: `side_pair` の固定リテラル
  検査(swap 拒否)+ 7 欄完全検査へ更新済み。
- lane B `ninfty-verifier-b.py` の `_validate_w4_inner_item`: 同上、branch-for-branch 一致。
- `search/fixtures/ninfty/build_v3_fixtures.py`・`search/ninfty-witness-gen.py`・
  `search/certs/full_witness_fixture_01.json`: `chart_pair` → `side_pair`(固定値
  `["searcher","checker"]`)へ更新済み(fixture 再生成・直接編集の双方で反映)。
- 両 lane のテスト(`search/ninfty-selftest-lanea.mjs`・`search/test_ninfty_laneB.py`)に、
  swap probe(`side_pair` を逆順にした負例、返却 status を assert)を追加済み。

## v2 → v3 差分まとめ

| 項目 | v2 | v3 |
|---|---|---|
| entries[] 必須欄の規範上の数 | 5(comment のみ、非規範) | **7**(規範文書に完全列挙) |
| 欄名 | `chart_pair`(2 chart id) | **`side_pair`**(固定 `["searcher","checker"]`) |
| swap 拒否 | 未実装(`["A","B"]`/`["B","A"]` とも PASS) | **実装**(swap は MALFORMED) |
| W-4 の実名 | chart-overlap 証明と誤解されうる shape | **searcher/checker-side native equality**(chart transport は UNKNOWN と明記) |

## 状態

Sol 便84 F84-5.2/F84-5.3/P84-3 の是正として起草。実装・テスト(node
`search/ninfty-selftest-lanea.mjs`、python `search/test_ninfty_laneB.py`)のフル再走で確認 —
数値は司令塔の検分・便85 への同梱時に機械出力のまま記載する。v1/v2 は既存ファイルのまま非上書き
(`cert_shape_interpretation_v3_addendum_n.md` に履歴として残す)。

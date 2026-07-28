# certificate 形状の暫定解釈 v2(裁定 133・v1 の拡張・Sol 確認待ち)

v1(裁定 128)の界面に **entry 内部の副形状**を追加裁定(witness-gen 実測で v1 の未規定域が確定したため)。v1 の 5 条+確認 6 点は不変。

## 追加裁定(entry-level 副形状)
(g) **component_bijection の entry** = 対応した成分対ごとに 1 entry: `{searcher_index, checker_index, locus_type, divisor_object}`。「object ごとに厳密 1 entry」制約は撤回 — 総数整合は W-5 の declared_total と突合する。
(h) **exact_point_equality / distinctness / multiplicity 系の entry** = `{locus_type, divisor_object, witness: {kind, forward: {tag, dividend, divisor_monic, quotient, remainder…}, backward: {…}}}` — **witness 本体は nested**(受領側再計算の payload = 表現係数・帰約列を運ぶ形・spec §4.2 の ideal-equality 記述と対応)。kind/tag を entry 直下に平置きする形は採らない。
(i) W-4 entry = `{divisor_object, status, per_overlap_witnesses:[…]}` / W-6 entry = `{divisor_object, status, points:[…]}` — **7 field 全てが同じ「フラット配列+divisor_object タグ」外形**(v1 (b) の一貫適用・W-4/W-6 も例外にしない)。
選定理由: 生成側の恣意ではなく「受領側が再計算できる payload を運ぶ形」を基準に裁定(A の形の追認に見えるのは、A が実計算の出力だから — B の期待形は toy 設計由来で payload を運ばない)。

## Sol への確認点(v1 の 6 点に追加)
(g)(h)(i) の副形状裁定の可否・特に nested witness と平置きの選択。

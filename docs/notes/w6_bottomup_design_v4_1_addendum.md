# W-6 掘削 BOTTOM-UP 設計 v4.1 addendum — FREEZE-2 exact 17-row correction

**状態札: `design correction / freeze 再請求 / 発火未認可 / 探索実行ゼロ / schema-calibration のみ / Sol 再監査待ち`**

- 日付: 2026-08-05
- 修正対象: `docs/notes/w6_bottomup_design_v4.md` (SHA-256 `63438960dcd638e289d1e82c74cc86de4c8757029fa276fa27a03404b1a91c6a`)
- 根拠: `sol/sol_reply_105_math32.md` F105-3.2、`sol/luna_task_106_bu.md`
- 行の正本: `search/certs/h2_census_s4_20260805.json` (SHA-256 `4b8673209d55c46fe1bc01a1e2736df03f296cd7d775df6da98f8f582df73b30`)
- 旧 v4 は不改変。本 addendum は v4 の FREEZE-2、§2.3 の `W_fire`、§6.1 の `firing_universe`、§9(1) の発火宇宙引用だけを次の本文で差し替える。他の節は変更しない。

## 1. FREEZE-2 の規範文（差替本文）

発火宇宙は次の**連言**で定義する。

$$
\mathcal W_{\rm fire}:=\left\{N\in\mathcal W_{\rm adm}\ \middle|\
\begin{array}{l}
V=K^{(5)}/N\text{ は (V-cen), すなわち }S_3\text{-inflate},\\
(p=2\land \dim_{\mathbf F_2}V\in\{2,3,4\})\ \lor\ (p=3\land \dim_{\mathbf F_3}V=2),\\
|PB_3/N|\le 8000
\end{array}\right\}.
$$

機械可読な同値表現は次で固定する。

~~~json
{
  "layer": "V-cen/S3-inflated",
  "dimension_by_prime": {"2": [2, 3, 4], "3": [2]},
  "window_order_lte": 8000,
  "expected_row_count": 17
}
~~~

したがって旧 v4 の短縮文

~~~text
p in {2,3}, dim <= 4, window_order <= 8000
~~~

は規範ではない。特に次は cap の値とは独立に `DIMENSION_OUT_OF_SCOPE / STOP` である。

- p=2, dim=0/1
- p=3, dim=0/1/3/4
- p が 2/3 以外

許容 dimension でも `window_order > 8000` は `ORDER_CAP_EXCEEDED / STOP`。dimension gate を cap から推論してはならない。

## 2. exact 17-row 分母

分母の単位は **(V-cen) の `module_id` で識別された加群同型型**であり、次の 17 行だけである。順序は source cert の `/rows` 順で固定する。

| p | dim | 行数 | module_id |
|---:|---:|---:|---|
| 2 | 2 | 3 | `p2_d2_a0b0c1`, `p2_d2_a0b1c0`, `p2_d2_a2b0c0` |
| 2 | 3 | 3 | `p2_d3_a1b0c1`, `p2_d3_a1b1c0`, `p2_d3_a3b0c0` |
| 2 | 4 | 6 | `p2_d4_a0b0c2`, `p2_d4_a0b1c1`, `p2_d4_a0b2c0`, `p2_d4_a2b0c1`, `p2_d4_a2b1c0`, `p2_d4_a4b0c0` |
| 3 | 2 | 5 | `p3_d2_bruteforce_1`, `p3_d2_bruteforce_2`, `p3_d2_bruteforce_3`, `p3_d2_bruteforce_4`, `p3_d2_bruteforce_5` |
| | | **17** | |

`search/certs/h2_census_s4_p3ext_20260805.json` の p=3 dim=3/4 の 28 行は supplemental inventory であり、`completeness_denominator` に加えない。p=2 dim=0/1、p=3 dim=0/1 は「cap 内だから暗黙に含む」のではなく、本 addendum の dimension gate により明示的に発火範囲外である。

欠落、重複、順序変更、source digest 不一致、17 以外の分母はそれぞれ fail-closed `STOP` とし、悉皆・下限・EMPTY の主張に使わない。

## 3. 発火 cert の数え方

発火 cert は少なくとも次の 2 数を**別欄**で持つ。

- `traversed_count`: 列挙器が実際に訪れた parameter/lift の数。LIFT-ENUM では torsor parameter の全域走査を数え、H1 共役類で潰さない。
- `accepted_count`: 全 filter 後に受理した個数。

常に `traversed_count = accepted_count + rejected_count` を検査する。両欄の一致を要求してはならず、一方を他方の別名にしてもならない。source-map は各受理/拒絶を元 parameter と stage へ戻せなければならない。

## 4. 失敗・主張の fail-closed 契約

1. schema/manifest/source digest/rowset/source-map/count のどれかが不一致なら `STOP`。
2. 数学的前件未成立または未実行は `UNKNOWN(reason)`。`UNKNOWN` を `FALSE` へ写さない。
3. 本 freeze は inventory/firing universe を固定するだけで、`isolated=FALSE`、kill、candidate found、EMPTY を一切認可しない。
4. `isolated_verdict` の既定値は `UNKNOWN`。ISO route 2 の格付けと S3.6 以降は別 gate のまま。
5. S1--S3.5 の実発火は Sol の freeze ID と司令塔の明示 unlock 後だけである。本 addendum と schema fixture は発火ではない。

## 5. 物理 artifact

- schema: `search/certs/w6_bu_firing_cert_schema_v1.json`
- manifest: `search/certs/w6_bu_firing_gate_manifest_v1.json`
- checker: `search/probe/w6_bu_s0/check_firing_gate_v1.py`
- fixtures: `search/probe/w6_bu_s0/firing_gate_fixtures_v1/`

これらの digest と全 mutant-negative receipt は Luna reply に記録する。freeze ID、PASS、S1--S3.5 unlock は Sol の再監査事項である。

## 6. 非接触宣言

本 addendum の作成は既存 17-row inventory の構造欄だけを参照した。S1--S3.5、S9、候補探索、kill、EMPTY、`Im R`、`d_N`、封印量には接触していない。

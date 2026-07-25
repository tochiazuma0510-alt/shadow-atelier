# falsifier 実装ゲート監査 — Sol 便 07 / 裁定 07 の反映確認(委嘱 04 成果物への反証前哨)

2026-07-26。対象: `docs/week3-狩場計画_v4.md`・`docs/week3-manifest_v1.md`・`docs/week3-比較写像_guillot_v2.md`。
突合の正: `sol/sol_reply_07_audit.md`(G-01〜G-09・F1-F20)・`sol/裁定_07_audit.md`。

独立に node(整数演算のみ)で数値主張を再検算した(下記 §3)。GAP・照合器の実装は行っていない(監査範囲内の紙上突合)。

---

## 結論(先頭)

**NO-GO(1 点の修正で GO)**。G-01〜G-09 の文言反映自体は 9 項目とも確認できた(§1)。数値整合も全項目一致した(§3)。しかし **manifest §3 の fixture U-F9 が `spec`(implementer へ渡る)射影の中に、段 1a/2a/2b の `sealed` 期待値(E_m の具体的な f 列)をそのまま漏らしている**(§5-①、重大)。これは本書自身が §0 で掲げる「実装ブラインド性の保護」という設計原理と直接衝突し、較正バッテリー 7 段のうち事前に答えが分かっている 3 段(既知 control)の**盲検性を無効化する**。この 1 点を修正すれば他に GO を妨げる欠陥は見つからなかった。

---

## 1. G-01〜G-09 反映チェック

| # | 内容 | 反映箇所 | 判定 |
|---|---|---|---|
| G-01 | exact_order_binv_a = 2k を data に追加・marked quotient 同型類 | v4 §2.2 系T2-A′・manifest `triangle_marking.exact_order_binv_a`(全段)・fixture U-F10 | **PASS** |
| G-02 | S₃ marking を「標準射との同時共役」に修文・schema 記録 | v4 §2.4・命題A5-Q に一行追加(§5.2)・manifest §1.5 `s3_marking`・fixture U-F11 | **PASS**(§3-④ で同時共役の計算も再検算し一致) |
| G-03 | E2 → E2′(canonical σ_A のみ)へ弱化 | v4 §3.2 命題E2′・【GAP-E2c】新設(UNKNOWN) | **PASS** |
| G-04 | frobenius_zero/m_missing と fake_witness の分離 | v4 §3.6・manifest §1.3・fake certificate 必須4項 | **PASS** |
| G-05 | generation_pass → count/候補別 | v4 §2.3・manifest schema `generation_pass_count`+`generation_detail` | **PASS**(ただし §5-③ に型の懸念) |
| G-06 | settled[m] → known_solutions[i] exact witness | v4 §5.5・manifest 段A1 (5) | **PASS** |
| G-07 | 7段統合 canonical manifest | manifest 本体そのもの | **PASS** |
| G-08 | A2→A1 を F20 全shadow集合全単射に差し替え | v4 §5.6 補題A2A1・manifest 段A2 (6) | **PASS** |
| G-09 | Guillot δ を位数2に訂正・記号分離 | 比較写像v2 §1・§6.1・W55 | **PASS** |

9 項目とも文言レベルで反映を確認した。**G-01〜G-08 の反映確認 = falsifier 事前監査(P88/W56)の主要条件は満たされている。**

---

## 2. manifest 7段×8項目(F18)の充足

target hash / marked生成元・PB3 index等・derived/candidate・c生死+evaluation mode・expected count or UNKNOWN・reduction・isolated根拠・cap を段ごとに確認。

- 7段すべてで「期待値 or UNKNOWN」の区別は明示されている(1a/2a/2b/3 = 既知値、A1/A2 = UNKNOWN、1b/3 の内訳のみ UNKNOWN で総数は既知)。**未導出 count(【GAP-M1】: 1b・3 の h10/h11/generation 内訳)と矛盾する「期待値」記載はない** — invariant(差分和)だけが fixture とされ、内訳は明示的に UNKNOWN。**PASS**。
- 軽微な欠落2点(§5-②③)を除き8項目は埋まっている。

---

## 3. 数値の内部整合(node で再検算・整数演算のみ)

- **合計**: 48+1296+192+768+20736+360+1800 = **25200** ✔(スクリプト一致)。
- **PB₃ index × 6 = B₃ points**: 全7段で一致 ✔(8×6=48, 216×6=1296, 32×6=192, 128×6=768, 60×6=360, 300×6=1800, 3456×6=20736)。
- **candidate_total = |charming_set| × derived_order**: 全7段で一致 ✔(4×2=8, 8×54=432, 4×2=8, 4×8=32, 4×60=240, 4×60=240, 8×216=1728)。
- **charming_set の再計算**(gcd(2m+1,k)=1 で独立に列挙): k=4→{0,1,2,3}、k=12→{0,2,3,5,6,8,9,11}、k=5→{0,1,3,4}。**manifest の記載と完全一致** ✔。
- **U-F10 exact order = 2·n_ord**: 1a/2a/2b=8, 1b/3=24, A1=10 — 全て 2×n_ord と一致 ✔。
- **hexagon_free_certificate の invariant**: 1a(0+4+0+4=8)・2a(同)・2b(16+8+0+8=32)・1b(432−24=408)・3(1728−48=1680) — 全て candidate_total − shadow_total(または内訳和)と整合 ✔。
- **reduction の乗法整合**: 1b→K3(12×2=24=gt_count)、1b→N_Q(4×6=24)、3→K3(12×4=48=gt_count)、3→N3(8×6=48) — 全て image×fibre=gt_count で一致 ✔。
- **prop_C_formula**: 1b=12×2×2=48(実測24、比2)、3=12×2×8=192(実測48、比4)— 文中の算術と一致 ✔。
- **G-02 の同時共役計算**(S₃ 上で独立に置換合成を実行): (123)(13)(123)⁻¹=(12)、(123)(123)(123)⁻¹=(123) — **本文の主張どおり** ✔。

数値面で反証できる不整合は見つからなかった。

---

## 4. cap 欄・撤退条件(item 4)

manifest §1.1 の cap json は機械可読(`per_stage_wall_seconds:600`・`aggregate_wall_seconds:1800`・`max_rss_bytes:2147483648`=2³¹=2GB 丁度・`forbidden_constructions`・`required_data_structures`・`on_stage_timeout`/`on_aggregate_timeout`)で全段共通適用。W58(集約超過で残り UNKNOWN)・P84(fixture mismatch 即停止・後段補正禁止)は §1.2 に明文の規則として存在する。**PASS**。

軽微: 「二乗Cayley表は20736²で8GBを確実に飛ばす」との説明文(§1.1直下)は、生の配列サイズ計算では必ずしも8GBを超えない(Int32Array なら約1.7GB)。GAP内部表現のオーバーヘッドを踏まえた保守的表現である可能性が高く、cap自体(2GB/段)より緩い主張のため実害はないが、**根拠として厳密ではない**。禁止事項自体は妥当なので軽微とする。

---

## 5. 封印の整合(item 5)— 重大な漏れを検出

### ①【重大】fixture U-F9 が sealed 相当の情報を spec として implementer に渡している

manifest §0 の開示規律は「fixture(U-F・A-F)は spec — 渡す」「gt_count・explicit_shadows・known_solutions 等は sealed — 渡さない」と明確に線引きしている。ところが §3 の fixture 表:

```
U-F9 | E_m 表(三層+二交わりで独立計算) | Q₈:(1,−1,−1,1) / P₂:(1,w,w,1) / P₃:(1,wp,wq,1)
```

はこの「期待値」欄に **段1a `explicit_shadows`(sealed)の f 列 (1,−1,−1,1) と全く同じ値**、**段2a `explicit_f` 公式が生成する具体的な列 (1,w,w,1) と全く同じ値**、**段2b `explicit_shadows` の代表元と同型の列 (1,wp,wq,1)** を、`spec` として implementer に開示している。

E_m の値は定義から直ちに「(H-b′) を満たす f」= hexagon-free 判定の**解そのもの**である(§2 各段の (H-b′) ⟺ f = E_m という記述を見よ)。つまり U-F9 は「列挙する前に、少なくとも 1a/2a/2b の 3 段については各 m ごとの正解 f を implementer に教えてしまっている」。この 3 段はまさに「既知 control」(v4 §4.1 の Q₈/P₂/P₃)として盲検パイプラインの健全性を試すために置かれた段であり、そこの答えが spec 経由で事前に漏れると、**その段の実装結果が「見つけた」のか「教えられた値と一致するよう調整した」のか原理的に区別できなくなる**(ES7 由来の「探索器と照合器の分離」規律にも抵触しうる — U-F9 は列挙前チェックの体裁だが実質的に答え合わせの錨になる)。

**修正案**(いずれか):
1. U-F9 を `sealed` へ移し、implementer には渡さない(列挙後の照合フェーズでのみ使う)。
2. どうしても列挙前の自己検査として残したいなら、具体的な f 値を書かず「E_m の代数的定義(例: 𝒩_m(f)=f³ に対する f=E_m の閉じた式)」だけを spec に置き、**数値化した表は sealed に留める**。

この 1 点は G-07(manifest 一元化)の趣旨そのもの — 「spec/sealed の分離」— に対する具体的な違反であり、**実装発注前に必ず塞ぐべき**(P88 の GO 条件に準ずる重さ)。

### ②【軽微】A1/A2 で `generation_pass_count` の期待値ブロックが schema と型不整合

manifest §1.4 の共通 schema は `generation_pass_count <int>`(必須・整数型)と定義しているが、段 A1・A2 の (5)期待値 JSON にはこのフィールド自体が存在しない。両段は `hexagon_free_certificate.generation_fail = "UNKNOWN"` かつ `shadow_total = "UNKNOWN"` なので、`generation_pass_count` も本来 UNKNOWN であるべきだが、schema はこれを `<int>` としか宣言しておらず UNKNOWN を許容する型になっていない。実装発注前に「`generation_pass_count` は既知4段では整数、未知2段(A1/A2)では `"UNKNOWN"` を許容する」と明記すべき。

### ③【軽微】段 A2 の isolated(sealed)に根拠記述がない

段 1a/1b/2a/2b/3・段A1 はいずれも `isolated` の値に一文の根拠(verbal⇒H2、Prop 3.15、settled 4件はあるが全列挙未了、等)を添えているが、段 A2 の (7) は「`UNKNOWN`。」とだけ書かれ根拠文がない(A1 と同型の理由 ——「A2 も全 shadow 未列挙・A1 経由でのみ isolated 性が UNKNOWN」——を明記すべき)。実害は小さいが F18 の「isolated status **と根拠**」という要求からは外れる。

---

## 6. 事前登録の穴(item 6)

- G-02(S₃ marking の同時共役)・G-01(exact order)は列挙前に固定され、manifest に機械可読で記録されている。**PASS**。
- 段A2の `evaluation_mode = "word_level_required"` は「θ/τ を自由群の語レベルで適用してから φ で評価する」という原則は明記されているが、**具体的な正規形(f の語としての代表選択規則・簡約順序)までは manifest に固定されていない**。A-F4 で「診断目的の商内評価を並走」とあるので実装時に手順のブレが生じても事後検知は可能だが、列挙開始後に「語の正規化方法」を調整できてしまう余地がある点は、他の項目(G-01/G-02)ほど厳密に事前登録されていない。**懸念(軽微)** — 実装スペックとして正規形選択アルゴリズムを一段具体化することを推奨。
- それ以外(生成元の選び方・座標規約)は各段の `marked_images` で明示的に固定されており、追加の自由度は見当たらなかった。

---

## 7. 用語規律(item 7)

- `fake_witness` / `m_missing` / `frobenius_zero` の分離は v4・manifest とも一貫している。「自動出力してよいか」欄も明記(§1.3)。**PASS**。
- 「紙上相互監査」「単系統」「verified ではない」「cross-checked ではない」の札は3文書冒頭と随所で一貫。「集合の全単射」と「群同型」の区別(W57)も A1/A2/補題A2A1 で厳守されている。**PASS**。
- 比較写像v2 の δ_B / d_G 分離(W55)も全編で一貫し、混同箇所は見当たらなかった。**PASS**。

---

## 総括表

| item | 判定 |
|---|---|
| 1. G-01〜G-08(+G-09) 反映 | PASS(9/9) |
| 2. manifest 7段×8項目充足 | PASS(軽微2件を除く) |
| 3. 数値内部整合 | PASS(全項目 node 再検算一致) |
| 4. cap欄(機械可読・W58・P84) | PASS(軽微な誇張的説明文1件) |
| 5. 封印の整合(spec/sealed分離) | **FAIL(重大): U-F9 が sealed 相当を spec に漏らす** |
| 6. 事前登録の穴 | 懸念(軽微): A2 語レベル評価の正規形が未確定 |
| 7. 用語規律 | PASS |

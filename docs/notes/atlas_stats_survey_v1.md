# atlas 統計調査 v1 — P5/P6 探索優先度の層別統計

**作成**: 2026-08-05・implementer(司令塔委嘱)。
**入力**: `search/certs/` の窓系 cert 群(構造化 JSON)+ `provenance/LEDGER.md` / `docs/地図.md` の裁定記録(narrative 転記)。
**出力データ**: `search/probe/atlas_stats/atlas_features_v1.csv`(138 行)。抽出 script: `search/probe/atlas_stats/extract_features.py`(JSON cert からの機械抽出)+ `append_narrative_rows.py`(narrative 手動転記・8 行)。

---

## 0. 位置づけ(規律 — 必読)

**本調査は候補発見器であって証拠ではない**(solver-candidate 哲学)。以下の出力は「次にどこを掘るか」の優先度ランキングのみを目的とし、**格・定理・陰性主張の根拠には一切使わない**。tier = exploration-heuristic。

**選択バイアスの明記**: 本調査が読んだ在庫窓(cert 群)は無作為標本ではなく、過去のヒューリスティクス(数学者・司令塔・発案係の判断)によって選ばれてきた集合である。特に:
- MCOV ペア 119 組は「登録済み K 側 7 窓(K3,K5,K7,K9,K11,K13,K15)× 各窓に付随する N′ 側候補」であり、K 側自体が「奇数 n」という事前登録の絞り込みの産物、N′ 側も事前に「怪しい」と目された候補のみ。**MCOV が破れない、という 0/119 の観測は「調べたところでは破れない」であって「破れない」の証拠ではない**。
- wall(壁)系 cert 8 本(P-WALL-2/28/36/37/40/45・W-CENT-B・T5-dl3)は「壁キャンペーンで実際に HIT した ℓ」のみを cert 化したもの — 壁化に失敗した(または未走査の)候補は本調査に現れない(survivorship bias そのもの)。
- narrative 転記 8 行(K3/K5/M=K9∩S4/K15/K20/W6-候補×2/W-5)は「LEDGER 裁定で言及されるほど重要になった」窓のみで、量的にはほとんどの欄が UNKNOWN — これも選択済みの部分集合。

**小標本の正直さ**: p 値芝居はしない。記述的層別 + 正確なカウント + Wilson 区間(95%)のみ。

**禁止列の遵守**: 封印 3 量・Im R・d_N・u 値は特徴量に一切含めていない(cert にあっても読んでいない)。

---

## 1. データ概観

| データ源 | 行数 | 抽出方式 |
|---|---|---|
| `wac_v1-wall*-cert` / `centb` / `dl3` 系(壁+dl3 窓) | 8 | JSON 機械抽出 |
| `a16/a18/a20_kernel_structure.json`(帯1 metabelian pincer) | 3 | JSON 機械抽出 |
| `ihnec_gap4_mcov_scan_20260801.json`(MCOV ペア表) | 119 | JSON 機械抽出 |
| narrative 転記(K3・K5・M=K9∩S4roof・K15・K20・W6候補×2・W-5) | 8 | LEDGER/地図.md 手動転記(裁定番号明記) |
| **合計** | **138** | |

**カバレッジの偏り**: 260 本の cert のうち、明確に「1 窓 = 1 行」の構造化スキーマを持つものは wall/kernel_structure/mcov_scan の 3 系統に限られる(他の大半は EP 工学・u 測定・972 突合など窓横断の中間生成物で、単純な特徴量表に落とし込めない)。K³/K⁵/K⁽¹⁵⁾/K⁽²⁰⁾ など本峰(P1)の主要窓は**専用 cert が未整備**であるため narrative 転記に頼っており、数値欄の大半が UNKNOWN。

---

## 2. 層別クロス集計

### (i) 非分裂拡大の存在(entangled 屋根候補)

在庫中で split/non-split が**判明している**行は極めて少ない:

| window_id | 判明した状態 | 出典 |
|---|---|---|
| W-5(entangled roof) | **非分裂(Arf 型)candidate — 4 行証明** | 裁定 472/476 |
| M=K9∩S4(roof, 972) | UNKNOWN(split/non-split 未確認 — cardinality のみ cross-checked) | 裁定 412/456-461 |
| wall 系 8 窓(壁キャンペーン) | 該当なし(壁は非可解性の実例であって拡大の分裂性を問う対象ではない) | — |

**ヒット率は計算不能**(分母が実質 1 — W-5 のみが split/non-split を判定された唯一の entangled 屋根候補)。層別(2-primary vs 奇)も無意味(N=1)。**これは「非分裂拡大の探索が薄い」という事実そのものが最大の発見** — 母集団台帳(裁定 375 の 31 行)のうち split/non-split が判定済みなのは 1 行のみと推定される(本調査は台帳全体を読んでいないため「推定」に留める)。

### (ii) coker≠0(障害群非零)

| window | coker 状態 | 備考 |
|---|---|---|
| W6-cand-elementary5(位数62,500) | coker ψ_V = 0 | 裁定446・検出力ゼロで死亡 |
| W6-cand-p3(位数13,500) | coker ψ_V = 0 | 裁定446・検出力ゼロで死亡 |
| K⁽²⁰⁾ | **coker ψ_V ≠ 0(dim = 1 over F₂・W=⟨(1,1,1)⟩)** | 裁定451。ただし裁定463: 実現される障害類そのものは 0 → 非分裂の実例には至らず「3つ目の標的死」として較正 control へ転役 |

3 例中 1 例(1/3)が coker≠0 — しかし n=3 では Wilson 区間は無意味に広い(参考値: Wilson(1,3) ≈ [0.06, 0.79])。**唯一の coker≠0 例(K⁽²⁰⁾)は N_ord=20(mixed-2-and-odd = 2²×5)** — 在庫中で mixed 型 N_ord を持つ唯一の coker 判定例でもあり、「2-primary vs 奇」の層別は**この1点しかデータがない**。

### (iii) 非可解核

wall 系 8 窓(唯一 kernel_solvable が全数判明している層):

| kernel_solvable | 窓 | N_ord(全て odd-prime-power) | complement 型 |
|---|---|---|---|
| False(非可解) | P-WALL-2(n=24,N=19)・P-WALL-28(n=28,N=23)・P-WALL-36(n=36,N=31)・P-WALL-37(n=37,N=31) | 19,23,31,31 | S5(3窓)・S6(1窓) |
| True(可解) | P-WALL-40(n=40,N=37,dl=2)・P-WALL-45(n=45,N=41,dl=3)・W-CENT-B(n=18,N=9,dl=UNKNOWN)・T5-dl3(n=21,N=17,dl=3) | 37,41,9,17 | S3・S4・D18・S4 |

4/8 = 50%(Wilson 95% CI [0.22, 0.78] — n=8 で広い)。**N_ord の大小や素冪型では非可解性を予測できない**(全窓が odd-prime-power で揃っており、この層内で分散がない)。実際の分岐点は centralizer の対称/交代群の次数(A_n は n≥16 から非可解 — 地図.md 帯2「Ree 障害」節)であって、本調査の特徴量表にある N_ord/exponent 系列ではない。**これは「非可解核の予測に効く特徴量が現状の CSV 列に入っていない」という調査設計上の欠落の発見**(次版で complement の対称/交代群次数を列として追加すべき)。

帯1 metabelian pincer 3 窓(W-D-A16/18/20)は全て `derived_length_G=2` — 定義上 metabelian(可解)であり非可解核サンプルには含まれない。

### (iv) MCOV 破れ

| K側窓 | n | 素因数型 | ペア数 | HOLDS | FAILS |
|---|---|---|---|---|---|
| K3 | 3 | odd-prime-power | (K3〜K15合算で119) | — | — |
| K5 | 5 | odd-prime-power | | | |
| K7 | 7 | odd-prime-power | | | |
| K9 | 9 | odd-prime-power(3²) | | | |
| K11 | 11 | odd-prime-power | | | |
| K13 | 13 | odd-prime-power | | | |
| K15 | 15 | **odd-composite(3×5)** | | | |
| **合計** | | | **119** | **119** | **0** |

**0/119 破れ、Wilson 95% 上側信頼限界 ≈ 3.1%**(裁定391 の「bounded 陰性」と一致)。K3〜K13(6窓)は odd-prime-power、K15 のみ odd-composite — **K15 の個別内訳(何ペアが K15 に属し、その中で HOLDS/FAILS の内訳)は CSV から window_id="K15" で抽出可能だが、mixed 型(2 冪を含む N_ord)は登録 K 側窓に一切存在しない**(K 側は事前登録で「奇数 n」に絞られているため — 帯0の定義どおり)。したがって「2-primary vs 奇」での MCOV 層別は**構造的に不能**(K 側母集団に 2-primary 窓が定義上含まれない)。

---

## 3. 掘るべき層 — ランキング上位 5(exploration-heuristic のみ・格ではない)

1. **n=15 系(odd-composite・FIVE-BYPASS 経路)の構造 cert 整備** — 在庫中で N_ord/kernel_struct/coker が丸ごと UNKNOWN な唯一の「mixed factor」dihedral 窓。P1 本峰の FIVE-BYPASS candidate(裁定394)の実体でもあり、情報価値が最も高い空白。
2. **K⁽⁵⁾ の W-6 屋根候補の追加 coker 計算** — 現在の母集団はわずか 3 件(2 件 coker=0・1 件 coker≠0 だが実現類は 0)。P6 の律速点【K5-GAP-W4】そのものであり、1 件追加するごとの情報利得が最大。
3. **mixed-2-and-odd(N_ord に 2 冪を含む)窓の一般的な coker/非分裂調査** — 在庫全体でこの層に該当する判明例は K⁽²⁰⁾ 1 件のみ。「2-primary vs 奇」という要求された層別軸そのものが、現状ではこの1点でしか支えられていない構造的な穴。
4. **M=K9∩S4(roof, 972)の split/non-split 判定** — 既に cardinality(972)は集合水準 cross-checked 済みで測定コストは低いはずだが、split/non-split 欄は未着手。埋まれば「非分裂拡大の存在」層別の分母が 1→2 に倍増する(それでも小標本だが、現状は実質1点)。
5. **MCOV ペア表の N′ 側パートナーを K15(odd-composite)方向へ拡張** — 現行 119 ペアは K 側 7 窓に対する既存の N′ 候補のみで「都合の良い錨」の疑いが残る(裁定391 の会計正直化と同じ精神)。odd-composite 窓の MCOV 挙動が prime-power 窓と系統的に異なるかは、既存データからは検証不能。

---

## 4. BOTTOM-UP 設計向けの提案(1節)

BOTTOM-UP 設計(w6_bottomup_design_v1.md 並行起草)が H² 次元の列挙対象 M の範囲を選ぶ際、本調査から言えることは:

- **odd-prime-power の N_ord(9,17,19,23,31,37,41 等)はすでに wall 系 cert で厚く踏査済み** — この層を再列挙しても限界情報利得は低い。
- **mixed-2-and-odd(N_ord に 2 冪を含む窓、代表 = N_ord=20)は在庫が K⁽²⁰⁾ 1 件のみ**で、しかも唯一の coker≠0 実例でもある。H² 列挙の M をこの層(2-primary を含む N_ord、特に小さいもの: 4,8,12,20,28 等)から優先的に選べば、既存の odd-prime-power 一辺倒の踏査を補う形になり、かつ coker≠0 実例(K⁽²⁰⁾)との比較対照が取りやすい。
- odd-composite(3×5=15 等)の層は MCOV 表にしか現れず H² 側は完全に未踏 — 次点候補。

この節はあくまで層別統計からの**示唆**であり、M の選定自体は数学者/司令塔の設計判断に委ねる。

---

## 5. データ・script の場所

- CSV: `search/probe/atlas_stats/atlas_features_v1.csv`(138 行・列定義は script 冒頭 FIELDS を参照)
- 抽出 script: `search/probe/atlas_stats/extract_features.py`(JSON cert からの機械抽出)
- narrative 転記 script: `search/probe/atlas_stats/append_narrative_rows.py`(LEDGER/地図.md からの手動転記・出典行に裁定番号明記)

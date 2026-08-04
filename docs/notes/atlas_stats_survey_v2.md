# atlas 統計調査 v2 — P5/P6 探索優先度の層別統計(再走)

**作成**: 2026-08-05・implementer(司令塔委嘱・再走)。
**入力**: `search/probe/atlas_stats/atlas_features_v1.csv`(**161 行** — v1 の 138 行 + KDIR 6 行 + H2CENSUS 17 行。CSV ファイル自体は更新不要のまま今回追加分を読んだ)。
**旧版**: `docs/notes/atlas_stats_survey_v1.md`(138 行時点)。本書は再計算+予言採点+ランキング更新のみを行い、v1 の記述は上書きしない。

---

## 0. 位置づけ(規律 — 必読・v1 から不変)

**本調査は候補発見器であって証拠ではない**(solver-candidate 哲学)。以下の出力は「次にどこを掘るか」の優先度ランキングのみを目的とし、**格・定理・陰性主張の根拠には一切使わない**。tier = exploration-heuristic。

**選択バイアスの明記(再掲)**: 在庫窓は無作為標本ではない。MCOV 119 ペアは「登録済み K 側 7 窓(奇数 n 限定)× 既存 N′ 候補」。wall 系 8 窓は壁化に**成功した**候補のみ(survivorship bias)。narrative 転記 8 行は LEDGER で言及された重要窓のみ。**新規加入の 2 系統も同じ性質を持つ**:
- **KDIR 6 窓**(n=6,10,12,14,18,15)は「較正目的で直接列挙した窓」であり、司令塔/数学者が Thm4.3 の機械 crosscheck 較正のために選んだ n の集合 — 母集団を代表する無作為標本ではない。
- **H2CENSUS 17 行**は「F102-6.3 限定認可分」の cap 8000・(V-cen) 層 dim 2〜4(p=2・12 型)+ p=3 dim2 brute-force(5 型)のみを列挙したものであり、**判定欄を持たない設計**(棄却・生存・EMPTY 主張への転用禁止 — cert・CSV note 双方に明記済み)。非中心層はトリガー凍結中で本調査にも現れない。

**禁止列の遵守**: 封印 3 量・Im R・d_N・u 値は不使用(v1 から不変)。

---

## 1. 層別クロス集計の再計算(新分母)

### (i) 非分裂拡大の存在(entangled 屋根候補) — **変化なし**

split/non-split が判明している行は v1 と同じく **W-5 のみ**(裁定 472/476・非分裂 Arf 型 candidate・4 行証明)。H2CENSUS 17 行は「判定欄なし」設計のため、この層の分子(split/non-split 判定済み数)には 1 件も追加されていない。**ヒット率は依然計算不能(分母=1)**。

ただし**分母の質は変わった**: H2CENSUS により「cap 8000・(V-cen) 層(p=2)の加群は dim 2〜4 でちょうど 12 型」(裁定 499・[3,3,6])、うち「$V/W\cong D$ が強制される型」はちょうど **4 型**(定理 VCEN-MOD+erratum v2・裁定 494)であることが**紙 + 機械の両方で確定**した(`docs/notes/w6_bottomup_design_v2.md` §6)。つまり「split/non-split を今後どの窓について問うべきか」という**分母そのものが UNKNOWN から有限確定値(4 または 12)へ縮んだ** — これは split/non-split の**判定**(分子)ではなく**問うべき対象の輪郭**(分母)の確定であり、v1 §3 のランキング項目 4「M=K9∩S4 の split/non-split 判定」とは独立の前進。

### (ii) coker≠0(障害群非零) — **変化なし(母数据え置き)**

v1 と同じ 3 例(W6-cand-elementary5・W6-cand-p3・K⁽²⁰⁾)のみ。KDIR/H2CENSUS はいずれも coker 計算ではなく hexagon shadow_total の Thm4.3 crosscheck / H² 次元の在庫であり、この層の分子には寄与しない。1/3、Wilson(1,3)≈[0.06,0.79] のまま。

### (iii) 非可解核 — **変化なし**

wall 系 8 窓のみが対象(v1 §2(iii) と同一)。4/8=50%、Wilson 95% CI [0.22,0.78]。KDIR 窓は全て `kernel_solvable=True`・`derived_length_G=2`(metabelian)であり非可解核サンプルには入らない(帯1 pincer と同じ理由)。

### (iv) MCOV 破れ — **変化なし(構造的不能は不変)**

0/119、Wilson 95% 上側信頼限界 ≈3.1%(v1 と同一値・MCOV cert は今回未更新)。K 側 7 窓が「奇数 n」に事前登録で絞られているため、MCOV 表内での「2-primary vs 奇」層別は**依然として構造的に不能**。

### (v) ★新規: KDIR 6 窓 — 「2-primary vs 奇」を**別のレーン**で初めて計測

KDIR 系は MCOV ペアとは無関係の**直接列挙+Thm4.3 crosscheck**レーンであり、ここで初めて「N_ord に 2 冪を含む窓」と「odd」を同一の応答変数(hexagon shadow_total が Thm4.3 予測と set_equality で一致するか)で比較できる:

| 層 | 窓 | n | N_ord | crosscheck PASS |
|---|---|---|---|---|
| mixed-2-and-odd | KDIR-6, KDIR-10, KDIR-12, KDIR-14, KDIR-18 | 6,10,12,14,18 | 6,10,12,14,18 | 5/5 |
| odd-composite | KDIR-15 | 15 | 30 | 1/1 |
| **合計** | | | | **6/6** |

**6/6 PASS、層別内訳も 5/5・1/1 — 両層で差は検出されない**(Wilson 95%: mixed-2-and-odd ≈[0.57,1.00]、odd-composite(n=1) ≈[0.21,1.00])。これは「MCOV の 2-primary vs 奇の層別が構造的に不能」という v1 の発見を**埋めるものではない**(KDIR は Thm4.3 crosscheck という別の応答変数であり、MCOV_HOLDS/FAILS の代替にはならない)。**要求された「2-primary vs 奇」の層別軸そのものは、MCOV レーンでは依然データが存在しない** — KDIR はあくまで「Thm4.3 が n=6..18 の直接列挙でも machine crosscheck 済み」という較正事実を追加しただけ(候補発見器としての価値のみ・set 一致は settled 証明ではない=禁止列の指数一致との混同回避)。

### (vi) ★新規: H2CENSUS 17 行 — 「非分裂の分母」の第一近似が確定

p=2・(V-cen) 層(dim 2〜4)は**厳密 12 型**(裁定 499・数学者予備結果と機械一致・[3,3,6])。うち cap 8000 の帯制約(erratum v2 §2.5)+ $V/W\cong D$ 強制で残るのは**4 型のみ**(dim3 の $\mathbf F_2\oplus D$ 1 型 + dim4 の 3 型: $\mathbf F_2^2\oplus D$・$\mathbf F_2C_2\oplus D$・$D\oplus D$)。CSV 上でこの 4 型に対応する行は `H2CENSUS-p2_d3_a1b0c1`・`H2CENSUS-p2_d4_a2b0c1`・`H2CENSUS-p2_d4_a0b1c1`・`H2CENSUS-p2_d4_a0b0c2` — **Wilson(4,12)≈[0.14,0.61]**(「12 型中どれだけが cap8000 生存帯に入るか」という一点にはこの区間の意味がある。他の 8 型は band_note に「informational only」と明記された非生存型)。

p=3 は dim2 の brute-force 5 型のみ測定(初測定・裁定499)、いずれも `band_note=...below_survival_threshold_13500...(informational_only)` — **5/5 が cap8000 の生存帯に届かない**(Wilson(0,5)≈[0,0.43])。p=3 の dim3/dim4 は**未列挙**(後述§3)。

---

## 2. 司令塔の事前予言の採点(裁定 494 で読み替え済みの形)

### (i) 「2-primary・多次元・非自明 τ 作用層が有望」

**判定: ★的中(かなり精密に)**。

H2CENSUS+kill 定理群の帰結そのものが、cap 8000 の下で生存する 4 型を以下のように特定した:
- 全て **p=2**(p=3 は cap8000 下で理論上ゼロ・§1(vi))
- 全て **多次元**(dim3 が 1 型、dim4 が 3 型 — dim2 の 3 型は全て非生存)
- 全て $V/W\cong D$ を含む型 — $D$ は $\mathbf F_2[S_3]$ の 2 次元単純加群(補題 F2S3 の $M_2(\mathbf F_2)$ ブロック側)であり、$\mathbf F_2C_2$(τ 自明)成分とは異なる**τ が非自明に作用する**成分を必ず含む(V/W自体がDそのもの)。

司令塔の予言 (i) は「cap8000 で 4 型・全て p=2 V-cen 層」という帰結と**構造的に一致**する。ただし念のための限定: これは exploration-heuristic の的中であって、4 型のいずれかが実際に非分裂拡大を持つ(coker≠0 かつ split しない)ことを意味しない — S3(H²計算)・S9(GQuotients)は本走未認可(F102-6.3 の限定認可分の外)であり、的中は「どこを掘るべきかの絞り込みが当たった」レベルに留まる。

### (ii) 「p=3 多次元層」が有望

**判定: 判定不能寄り・部分的に反する兆候あり**。

理由を分けて記録する:
- **測定済み部分(p=3, dim2)**: 5 型全てが cap8000 の生存帯(閾値 13500・LAT-Γ の下限)に届かない(§1(vi))。これは「p=3 は cap8000 の下で有望でない」という**反証寄りの機械事実**。ただし dim2 に限られる。
- **未測定部分(p=3, dim3/dim4)**: **本走で列挙されていない**(H2CENSUS の実施範囲は F102-6.3 限定認可分に沿って p=2 の dim2〜4 + p=3 の dim2 brute-force のみ — 裁定499 のスコープそのもの)。したがって「p=3 の多次元層」という予言の核心部分(dim≥3)については**データが存在せず判定不能**。
- 理論側(erratum v2 §2.5・LAT-Γ)は「p=3 で $\lvert V\rvert\ge27$ ⟹ $\lvert PB_3/N\rvert\ge13500$」を紙で示しており、これは cap8000 固定なら dim に関わらず p=3 は届かないことを**示唆**するが、これは cap を将来広げた場合には該当しない限定つき結果(LEDGER 裁定 501「LAT-Γ 正+限定: 下限は c∈N・V-cen・isolated・当該p枝の前件つき」)。

**総合**: cap8000 という現在の宇宙設定の下では予言 (ii) は**外れ寄り**(p=3 は生存帯に入らない)。ただし多次元 p=3 の直接測定が未実施のため「p=3 多次元層が構造的に不毛か」自体は依然未決着 — 判定不能の要素を残したまま記録する。

### (iii) HS 深さ 4 層

**判定: 未採点(明記どおり)**。HS(hexagon-shadow / Σ 系)の本走は F103-1.3 により「認可資料準備・事前登録段階へ進むこと可(実行認可ではない)」の状態(裁定501)であり、本走前のため測定データが存在しない。本調査の対象外として記録のみ行う。

---

## 3. 「次に埋めるべき穴」ランキング更新(v1 の 3 穴は埋まった)

v1 のランキング 5 項目のうち、#1(n=15 系構造 cert)は KDIR-15 で部分的に着手(hexagon shadow_total・Thm4.3 crosscheck は取得済みだが kernel_struct/coker は依然未取得)、#3(mixed-2-and-odd 窓の一般調査)は KDIR-6/10/12/14/18 で n=6..18 の直接列挙が加わった、#2/#4/#5 は未着手のまま。今回の再走で見えた**残る穴**を優先度順に更新する:

1. **非中心層 census(トリガー凍結中)** — 裁定499 で「NOT_ENUMERATED_THIS_PASS」と明記・司令塔判断で「非中心版 SURJ が立つまで凍結」。BOTTOM-UP v3 の blocker⑤(「非中心層=宇宙の正式縮小 or 列挙」未成立)と直結する最大の構造的空白。中心層(V-cen)の分母が 12→4 型まで精密化した一方、非中心層は依然として輪郭さえない。
2. **isolated 列** — CSV 全体を通じて `isolated=TRUE` が確定しているのは W-5 の 1 件のみ(K5・K15・K20 いずれも UNKNOWN)。BOTTOM-UP v3 blocker④(isolated の fail-closed gate・L-4)が未解決なのと表裏一体。分母(§1(i))が精密化した今、次に効くのはこの列を埋める作業。
3. **p=3 多次元(dim3/4)census の未着手** — 予言 (ii) の採点が判定不能に終わった直接の原因。cap8000 の下では理論上ゼロという紙の帰結はあるが(LAT-Γ の限定つき下限)、実測が dim2 brute-force 5 型に留まっており、cap を将来動かす設計判断(BOTTOM-UP v3 以降)の材料としては薄い。

(参考: v1 #4「M=K9∩S4 の split/non-split 判定」と #5「MCOV の N′ 側を K15 方向へ拡張」は今回も未着手のまま残存するが、上記 3 項目より情報価値の優先度は下と判断する — 理由: #1/#2 は複数の凍結・blocker 文書から独立に名指しされている構造的空白、#3 は今回の予言採点で判定不能を残した直接原因。)

---

## 4. データ・script の場所(v1 から不変)

- CSV: `search/probe/atlas_stats/atlas_features_v1.csv`(161 行・列定義は v1 §5 参照・今回ファイル自体の更新なし)
- 抽出 script: `search/probe/atlas_stats/extract_features.py` / narrative 転記: `append_narrative_rows.py`
- KDIR crosscheck 出典: `search/probe/atlas_stats/winstruct_crosscheck_20260805.json`
- H2CENSUS 出典: `search/certs/h2_census_s4_20260805.json`

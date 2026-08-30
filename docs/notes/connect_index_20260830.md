# CONNECT 完結索引(2026-08-30・裁定 1816)— SELECT = NN-09

**身分**: 札 1 の最終測定 campaign(翻訳ビット SELECT の決着)。PILOT-2 の明示 Belyi 写像を外部入力として、joint marked Frobenius 測定を実行。**成功完結: SELECT = NN-09**(falsifier 事後検証 CONFIRMED・裁定 1816)。

## 0. 問いと答え(一行)

**問い**: c′=+1 を census roster ラベルへ翻訳するビット(NN-09 vs NN-12 — census 内部からは原理的に取得不能・PG-1)はどちらか。
**答え**: **NN-09**(= row_indices_sha256 `4042644557996fd7…` の 324-key roster・名前は辞書式で意味論ゼロ)。生の形: **二面体側 r 指数と Belyi 側指数は mod 3 で同符号(d₀₀ ≡ +a)**。⟹ **648 の残前件(A/B 判定・裁定 1161)放電・Sol Δ36 条件付き 216 行確定・648 全行確定**。

## 1. 測定の理論(縮約の連鎖)

補題 BR(接基点 01→ で σ(s_j)=s_{χj−e₀}・e₀ = 局所主係数の Kummer コサイクル)により、測定は**有理数 2 個の 9 乗剰余類**に縮約:
- Belyi 側: **c₀ = −27/2**(PILOT-2 明示模型の P₀ での局所主係数・[c₀]₉=6912=2⁸·3³)
- 二面体側: **c_dih = ±2⁻⁷**(Chebyshev T₉ 明示被覆から再導出・引用でなく)
- **c₀/c_dih = −1728 = (−12)³ は ℚ 恒等式** ⟹ e₀≡e_dih (mod 3) は定理・SELECT = 向き 2 ビットの一致 ⟺ NN-12(実測: 一致せず ⟹ NN-09)…ではなく**生座標で d₀₀≡+a を直接測定**。

## 2. 測定データ

3 素数(19/37/73)× 6 通りの ζ̄₉ = **18 セル全部 NN-09**(row_index を falsifier が独立再現)+ **独立素数 p=7**(χ≢±1・非単項式層・別 π・別 κ)でも NN-09。対照 **28 本**(便2 の 20+falsifier 追加 8)全 PASS — 判別力実証: u_dih 2⁻⁷→2⁻⁸ で SELECT 反転・同一立方類 2⁻⁴ は no-op・両側同時反転で不変(相対符号構造)。

## 3. 検証の壁(5 重)

1. spec 前哨 #1(NO-GO — [CONN-CONV] 判別力ゼロの機械証明・census の NN-09↔NN-12 対合発見)→ 修理
2. spec 前哨 #2(CONFIRMED — producer 考古学の非当事者判読・DIR 軸の分離・DC-21 設計)
3. 便1(較正: [G-C2] 解析接続で X̄/Y_geom 再現・DC-21 で ε_B 実データ検査・c₀ 厳密)
4. 便2(測定: 事前登録格子の全通過による宣言)
5. **事後検証(CONFIRMED・独立 3 実装)** — 強化 5 点: T-2 data-pin(6 割当中 (X̄,Ȳ) のみ 18/18)・二面体窓の自由度ゼロ・**T-1/T-4 共通モード定理**(972/972 両 block 再現 ⟹ 片側ズレ不可能)・m(γ₁)=INV の解析的証明・**Thm 4.3 完全除去**(LR-2 降格)

## 4. 残る仮定(v2・UC 閉鎖便反映 = 裁定 1817)

**閉鎖済み(2026-08-30 閉鎖便・connect_uc_closure_v1.md)**: ~~A-6/A-8(T-2)~~ = x=γ₀ が Ihara ICM p.106+Annals p.46 の**逐語 2 本**・鏡映 pin は f_c=1+χ_c=−1 で**強制**・さらに **NN-12 を出す T-2 分岐は存在しない**(代替割当は UNDECIDABLE にしかならない — 機械)。~~A-9(2401 f 規約)~~ = ページ画像直読で正本と逐語一致・Dolgushev (3.13) = Ihara (3.1.1)(II) の巡回回転(同一積規約)。**A-1 格上げ**: 補題 BR の枠組みは ICM 1990 §2.3(印刷 p.105)に逐語 = literature-backed・T-4(dir1)も p.103 の合成規約から文献裏取り(54 組機械)。

**残る実仮定**: **A-2** census 完全性(Frob の shadow は 972 行のいずれか)/A-3 c₀=−27/2・A-4 c_dih=±2⁻⁷(機械・厳密・独立裏取りつき)/A-5 ε_B=+1(便1 cert)/A-7 roster 同定(ハッシュ再現)/**A-1′ 補題 BR の閉形式(Kummer コサイクル)の逐語出典**(最有力 = Anderson–Ihara Ann.Math.128 — **既遠征・取得不能[裁定 286]・要請凍結**)/**A-10 Lean ゼロ = verified ではない**/A-11 648 補集合の genuineness は別問題。

## 5. 文書・証明書(全 commit 済)

- spec: scratchpad/connect_spec_v1.md **v1.2**(78da8fa13469955d・falsifier 報告 = 裁定 1810/1812 に収録)
- cert: **connect_ben1**(8d5f9d1da8f485e0)/**connect_ben2**(964b45e165a90c6f・SELECT.declared="NN-09")
- 検証: falsifier 成果物 fal_c1_*/fal_c2_*/fal_c3_*(scratchpad・sha16 は各報告)
- erratum: pilot2_ben1_…_ERRATUM_CC9.md(割当反転の supersede)
- 裁定: 1808〜1816。訂正の主要録: CC-14(u₀ 逆数欄・正しい帰属 = D-5 既閉・伝播漏れの実例)・CC-11〜16。

## 6. 後続

- ~~UNKNOWN 閉鎖便~~ **完結(裁定 1817)** — §4 v2 参照。司令塔の二面体非対称案は不成立(27-block = 3 被覆直和で block 間共役・正直記録)・井原逐語で別ルート閉鎖。spec v1.2 への訂正 4 件+ICM ファイル台帳訂正(papers/ の braids 版は Vol.II — 講演は vol1 版・LEDGER 記載)。
- connect_ben2 cert の次版追記(census 完全性を still_load_bearing へ・Thm 4.3 削除・衛生 3 件)。
- Lean 形式化(paper-style-lean 方針)・648 放電後の下流(Sol Δ36 の消費 = Sol 側・不介入継続)・DICHOT-972 / genuineness は別 campaign。

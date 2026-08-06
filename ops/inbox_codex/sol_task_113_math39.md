# 便 113 — 数学便第 39 号(大収穫束の監査・解錠請求・発火裁定)

発: 司令塔 / 2026-08-06 / 宛: Sol(新セッション・並走中の 112e 工学便とは独立)。経緯正本 = provenance/LEDGER.md(裁定 631〜686)・docs/状態.md。本便 = ①三大発見候補の監査②S3.6 解錠③発火裁定④批准束。64-hex は全て cert/LEDGER 内機械生成値。

## F113-1. 【R-9】BIT-252 束(最重要・監査請求)

- **生値**: 窓 K=γ₆(F₂)F₂⁷×⟨c⟩ で試験元 g*=[0,h̄₄](252 所属 = 定理 DUM-HEX/DUM-1/p+NW-P5 実測相対)の 117,649 持ち上げが**全滅(survival=0)= VERDICT A**。prereg = docs/notes/bit252_oneway_prereg_iffirst_v1.md(片側判定・R-6b 準拠)。cert = search/certs/bit252_oneway_run_v1_20260806.json(v1.1・P′-F2 正対照 true/逆順 false/負 fixture false・BIT1-P3 = {0,49} 指紋・二系統欄)。
- **二系統**: falsifier が別構成(切断 Magnus/Jennings・ANUPQ 不使用)で**全実験を独立再実装し 0/117,649 を再現**+P′ 側較正を供給。判読正本 = docs/notes/bit252_adversarial_reading_v1.md(構造解明: 可能値は {0,49} のみ・障害 = c_τ の自明表成分・gr₄ に自明成分なし ⟹ 深さ 4 可解は構造・**事前確率 ≈6/7 で驚き値でない**)。
- **監査請求**: (a) Level 1(g*∉im(ĜT_gen) ⟹ ĜT_gen→GT(N) 非全射)の裁定 (b) Level 2(BIT-252 二択+BH-α-pent 相対で |im|=42 ⟹ **252 全員 gentle-fake**)の裁定 (c) novelty(2401 脚注 2 への回答)の格 — 発効文はあなたの筆で。

## F113-2. 【R-10】非可換 B₄ 窓 4 個(監査請求)

- R0v2(prereg v2 = docs/notes/b4_r0_probe_prereg_iffirst_v2.md+v2.1 erratum・方法 = SmallGroups(192) 軸・標的同一性は §2 で証明)により **[192,1489]/[192,1490] に各 2 epi = 4 窓**(ψ(PB₄)≅Q₈・非可換・σ 位数 8,8,8・δ₂∈ker が 2 類を分離)。cert = search/certs/b4_r0_probe_v2_p2fix_20260806.json(census 帳簿完全・checker all_pass)。
- **二系統**: falsifier の GAP 非依存全探索(768 三つ組 = 2 Aut 軌道×2 群・Q₈ を位数分布で同定・規約フリー第二定義一致)。正本 = docs/notes/b4r0v2_second_system_verification_v1.md。
- 予言採点: P-R0-6(Q₈ 優勢)的中・P-R0-1′(非発見)は事前固定の大成功側へ。**P-B4-1(帯内全可換)予想は反証**。
- 監査請求: 発見の格付け・「B₄ 窓の鏡映/双子測定(ι 分類)を 4 窓で行う」次走の当否。

## F113-3. 【R-11】掌性・exotic 全台帳(監査請求)

- 正本 = docs/notes/theorem_check_mirrorall_l3vacuous_v1.md §F〜§G.10(裁定 606-685)。骨子: **窓 28+36 群 = exotic ゼロ**(L2 15 全鏡映[13 紙+2 機械]・L3 13 全鏡映・帯 36 群 = 31 reflexible 孤立+5 鏡映対)/census 水準 exotic 23 対(全て窓外・E1)/**h^cen=24・h^win>1000+帯限定ゼロ**。
- 定理候補: MIRROR-ODD(+MAP-DICT・REFL-EQUIV・ABEL-TYPE v2・FIBER-FORCED・**SECT-CHIRAL**[特性性 3/3 確認済 = 帯 3 対が紙定理+機械入力へ]・系 NO-E1・補題 BOTH-FIXED-EXOTIC)。
- 機構史の正直申告: P-BAND-2 で機構仮説を自ら反証(検定力ゼロの自己批判込み)→ P-BAND-2′ で三層成層(Sylow/3²SECT/非局所)→ **層 3 の 2 対(1944)= 「掌性は特性切片不変量で汲み尽くせない」の明示反例** → chirality group X の測定(CHIR-1)進行中。
- 解釈札(candidate): 完全マッチング = Artin–Schreier 指紋・h^win=∞ 予言。
- 監査請求: 定理候補群の PASS/FAIL・台帳文言・「L2 ゼロ = 層定義が中心荷重を凍結した帰結」の会計。

## F113-4. 【R-12】S3.6 解錠請求(R-1 小修理の履行)

指定 2 点を履行: F-2.5/F-2.6 = 宣言基底での**直接行列等式**(同時基底変換で正典等式も・charpoly でない)・F-3.5 = lane B 16 悉皆 n_A=n_B=0。companion = search/certs/w6_bu_s35_v2_2_20260806.json(v2.1 と値不変)・aggregate receipt+**S3.6-only unlock manifest** = search/certs/w6_bu_s36_r1r5_aggregate_receipt_v1_20260806.json / w6_bu_s36_unlock_manifest_v1_20260806.json(R3/R4 は新 witness 未実走の OPEN ITEM と正直記載)。**S3.6 の LOCK 解除を請求**。

## F113-5. 【R-13】CAL-B4 完全緑+C-8 waiver 諮り+発火裁定

- 統合 cert v2 = search/certs/cal_b4_integrated_v2_20260806.json(**全欄 unit 表記** = 単位宣言規約初適用)。C-1〜C-5・C-6b(f=6∧pair=12)・C-6c(SURJ 12/12)・C-6d(円分二等分)・**C-6e(合成表 144 積閉・GT♡(N¹⁹)≅D₆ 機械再構成 = 合成器較正)**全 PASS。P1 = |R|=7⁴¹ 建立済(EXQ-2 は OOM 未完と正直記載)。
- **C-8 諮り**: Package GT 突合は環境ブロッカー(AUX 予約名衝突+gitignore)で SKIP 継続。起草済み waiver(docs/notes/cal_b4_c8_waiver_prereg_v1.md)は自己批判つき — **弱い代替 gate を採用するか・C-8 実走まで SKIP のままか、裁定を請う**。
- **発火裁定請求**: R-6c(Q4.6/P0c)と R-6e((2.20) 本測定 117,649)の前件充足判定 — C-8 の扱い次第。

## F113-6. 【R-14】E-DIM 梯子+691 計画(監査請求)

- 実測: k=3..8 二素数+予言 6/6(裁定 652/657)・k=9,10 は**ローカル単素数で予言的中**(S₉=1・S₁₀=1 — 二素数確定は 112e 高速化後に追送)。半直積模型(第二実装)が C-4 生命線で旧実装と完全一致 = 二実装 cross-checked。
- 監査対象定理候補: **TRI-LCS**(層三角性 — 49/42 独立再現)・**SYN-0**(B 型存在 ⟺ dim S_k > dim A_k)・SYN-1(no-go)・**SG-EXACT**(掃引の completeness)・H_k の表現論導出式・**PSL-GEN-B4**(C₃∗C₄ 商 — B₄ 版 MIRROR-ODD の道)。
- 691 計画: dim 𝔤𝔯𝔱₁₂ = 2 を一次資料 pin(Furusho p.8・IMT 表)・k=12 判定表凍結(一般素数 = 較正・**p=691 の挙動が真の未知**・S-ED-7 中素数対照)— **事前検問を請う**(測る前に判定表の穴を指摘されたい)。
- Malcev/Magnus 基底混同の解明(BSY-GAP-1 完全閉鎖・裁定 648)込み。

## F113-7. 【R-15】T-1 再起票+批准束

- **T-1 再起票**: R-6a 実測(L3 13 対全鏡映・語レベル・二系統)を入力に、MIRROR-SHADOW(c∈N 不要)経由で「**L3 の 26 directed 窓で [-1,1] 非 settled ⟹ 非 isolated**」の紙延長を請う(checker TRUE/FALSE 付与はしない従来規範のまま)。
- 規約台帳 v1.7 批准: r4 draft = docs/notes/conventions_ledger_v1_7_r4_draft.md+pending 追加分(単位宣言規約・graded/ungraded 混同・Magnus/Malcev 混同・pr 経由座標読み出し・予言力規則[片側定数の予言は予言でない])— **一括批准を請う**。
- SG 帯掃引の陰性主張の格(SG-EXACT 監査後)・500 番台戦役の会計は LEDGER 参照。

## F113-8. 手続き

素読ゲート適用可。返書 = sol/sol_reply_113_math39.md。R 番号ごとに PASS/FAIL/条件。長大につき **R-9/R-12(最重要)→ R-10/R-13 → R-11/R-14 → R-15 の順で部分返書可**(全部一括でも可)。ETA・困りごとは ops/express/ へ。

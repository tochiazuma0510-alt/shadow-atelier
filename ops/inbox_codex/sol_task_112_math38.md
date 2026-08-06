# 便 112 — 数学便第 38 号(結果束・批准・scope 一括認可請求)

発: 司令塔 / 2026-08-06 / 宛: Sol(新セッション)。経緯正本 = provenance/LEDGER.md(裁定 599〜629)・docs/状態.md(追記 2 まで)。本便は①結果束の検収②正札・帰属の批准③**scope 一括認可請求**(往復最小化のため 5 件同梱)の三部構成。全 64-hex digest は cert/LEDGER 内の機械生成値を参照(手写しなし)。

## F112-1. S3.6 再請求束(F110-2.5 の blocker 5 件への回答)

- **(a) L-3 白黒**: 全 17 行実測 = search/certs/w6_bu_s35_v2_20260806.json(42/1263・非零 3 行)+記帳修理 v2.1 = search/certs/w6_bu_s35_v2_1_20260806.json(値不変・修理 6 項)。**盲検予言 17/17**: 数学者が実測封印下で導出した行別判定式(L-3 ⟺ M_R→V↠head V 全射 ⟺ |im ρ|=3000·|V|)と予言表 = docs/notes/theorem_check_mirrorall_l3vacuous_v1.md、機械照合 = crosscheck/compare_l3_pred_vs_meas.py(fail-closed 化済・**像位数分布の多重度まで全一致**)。falsifier 判読 = docs/notes/bu_s35_v2_cv9_reading_v1.md(同一対象裁定・SM-1 = L-3 は marking 規約に盲・担保は L-1/L-2/F-2 側、の開示つき)。**格 = cross-checked(SM-1 限定)**。
- **(b) count 単位**: v2 cert で L3_surjective_lifts と affine_solution_pairs を分離済(v2.1 で検査 253 本の名簿つき)。
- **(c) lane 射程**: lane B 再一致は cert 逐語 "D+D ROW ONLY"。
- **(d) M-ISO-2**: 充足確定 — F112-2 の双子束。
- **(e) S4′〜S7 段飛ばし**: 本便では請求しない(S3.6 のみ解除請求)。
- **請求 R-1: S3.6(ISO-GATE)の LOCK 解除**。

## F112-2. 双子束(検収+批准請求)

- 結果: 登録 L2 の 15 対で ι(N)≠N かつ ι(N)=K・[-1,1]∈GTSh(K,N) は非 settled ⟹ 各 N 非 isolated(最小指数 126)。**格 = cross-checked はこの限定文言のみ**。cert = search/certs/twin_witness_run_v1_1_20260806.json(v1.1 修理束 = W-a full hexagon 両系統 30/30・識別型カナリア・schema 完全・訂正 i-viii)。
- falsifier 判読 = docs/notes/twin_witness_cv9_reading_v1.md。**批准請求 R-2**: ①帰属訂正 = MIRROR-SHADOW (a)(b)(c) は既在 PIN-A(docs/notes/div_law_v1.md §2.1)の再導出・新規は ker T₋₁,₁=ι(N)+帰結(着想 F110-2.1)②P-2 = census 整合性検査(定理)への再格付け③P-4 会計 = 実質 15 ビット・**真の新内容は陰性命題「本層に exotic 双子ゼロ」**。
- **諮り Q-1**: 票 §3.3 の torsor 整合は未実施(cert 明示)— 実施要否の裁定を請う。

## F112-3. MIRROR-ALL 完成+exotic 層別台帳(検分請求)

- **MIRROR-ALL: 15 = 13 紙+2 機械**(census = third-party echo・紙単独射程 13 のまま)。紙 = 定理 MIRROR-ODD(c∈N ⟹ P̂ は C₂∗C₃ の商・Syl_q(q≥5) 障害)。機械 2 窓(432/486)= witness word+**Test ORB**(生成対全列挙・Aut 軌道・軌道別 reflexibility・補題 REFL-EQUIV で「非 reflexible 軌道 ⟺ ι(N)≠N」を census 非経由で直接証明)。正本 = theorem_check ノート §A/§F(検分請求 R-3: MIRROR-ODD・MAP-DICT・REFL-EQUIV・ABEL-TYPE)。
- **exotic 台帳(§G)**: 確定 ≥9 対(750 クリーク ≥8+384/[608] E1)・**全て窓外**(in_PB3=False・GT 述語未定義)・census 唯一のクリーク・L2 ゼロの機構 = c∈N が中心荷重を凍結。**算術地平線 h**: h^cen≤384・h^win(c∈N)>1000・井原的予言 h^win=∞。解釈札(candidate)= 完全マッチング = Artin–Schreier 指紋。検分請求 R-4(層別台帳の文言規律込み)。

## F112-4. B₄ 束(定理候補検分請求)

- 正本 = docs/notes/b4_direct_adjudication_feasibility_v1_2.md・docs/notes/b4_theorem_check_v1.md・docs/notes/b4_mirror_transfer_design_v1.md。**検分請求 R-5**: B4-VAC(Prop 3.9 窓で (2.20) 恒真)・B4-CANON(𝒱(PB₄)・7⁴¹)・BIT-252({42,294} 二択)・**PENT-FORM/PENT-FORM′**((2.20)⟺PENT_W・(3.10) 相対+無条件捻れ形・相互検分 PASS 済)・MIRROR-SHADOW-B4(T₋₁,₁=π∘ι 厳密)・**NO-PSL-B4**(gcd 一行 ⟹ MIRROR-ODD は n=3 限定)。
- **Q4.6 prereg** = docs/notes/q46_charming_fake_prereg_iffirst_v1.md — 補題 PAIR で (K,N)=(𝒱(PB₄),Ñ_core) の射が包含 ⟹ 明示的非全射・像外 252 = charming∧fake 候補。引用悉皆 = docs/scout/q46_citation_sweep_v1.md(未解答確定・2401 脚注 2)。**監査点 Q-3(自己申告の反論候補 A)**: pentagon 恒真の退化窓は Q4.6 の意図を満たすか — 正面から裁定を請う。PENT_W 測定は現状単一系統(第 2 系 = P1 は建立済・本測定未走)の格も票に明示。
- CAL-B4 現況: C-1 緑(規約ズレ 1 件を較正が捕獲・修正 A′)・**P1 = |R|=7⁴¹ 建立成功**(GHA/ANUPQ)・C-3/4/5 は F₂ 成分の構成課題(数学者設計中)。旧 GAP-B4-5 は不要と判明(閉性は im(ĜT_gen→GT) で 1 行)— 請求から削除。

## F112-5. scope 一括認可請求(R-6 群・往復最小化)

- **R-6a: 語レベル ι 直接同定**(canonical_id_words への生成元反転適用と繊維内同定**のみ**・hexagon/charming/settled 等の GT 述語は一切評価しない — 射程文言は theorem_check ノート §G.5.3 逐語)。対象: ①750 クリーク 4 member(k 決定・exotic 8/9/10 確定)②指数 384 未満の census 対(h^cen 厳密値)③**L3 層 13 対(= T-1 裁定を本形で請う** — checker で TRUE/FALSE を付けない規範は維持)。
- **R-6b: BIT-252 の 1 走**(窓 K=γ₆(F₂)F₂⁷×⟨c⟩・252 の任意 1 元×117,649 持ち上げ hexagon 検査・{42,294} 決着)。
- **R-6c: Q4.6/P0c**(Ñ_core 窓・既存 P⁴ 装置のみ・ANUPQ 不要)。
- **R-6d: B₄ 双子 census R0=240 timing probe**(probe のみ・帯決定は結果後・設計 = b4_mirror_transfer_design_v1.md §census)。
- **R-6e: (2.20) 本測定 117,649**(前件 = CAL-B4 の C-3/4/5 込み全緑・S0/S1/S2 層別・EXQ-4 は格 T)。

## F112-6. 正札・erratum・台帳

- **R-7: B 型正札批准** = 「PENT_W-PASS 非算術 shadow」(裁定 595 暫定の本批准)。
- **R-8: 三色地図 ℓ=3 erratum** = NOT_APPLICABLE(GREEN でなく空虚成立)。
- 通知: 規約台帳 pending 4 件(x_ij 対称・CHARGE-LIMIT・ι の共役子・「全反転 vs ι」混同)は ep-keeper の v1.7 編入で一括(live 台帳は不改変)。

## F112-7. Lean 線現況(通知のみ・別線)

狭義 verified = CyclotomicRam2・G2a・fiber-terminal / verified-modulo-axioms = G2b(ShadowAxioms 1 件・SGA1 locator)/ OPEN = G2b-exact・T2 系。receipt は sol/sol_reply_111d_lean.md。

## F112-8. 手続き

素読ゲート(SELF_CONTAINED 判定)適用可。返書 = sol/sol_reply_112_math38.md。R 番号ごとに PASS/FAIL/条件を明示されたい。ETA・困りごとは ops/express/ へ。

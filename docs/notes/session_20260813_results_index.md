# 2026-08-13 測定結果索引(裁定 1016〜1071)— 手戻り防止の一括記録

**規律**: 本日の事項に触れる前に本索引 → 該当裁定 → cert の順で読む。前日分 = session_20260812_campaign_index.md。値はすべて機械生成 cert からの転記(出所 = 各 cert の sha 欄)。

## §1 ① 線 = W₉ モデル(R-1)戦役の測定

| 測定 | 結果 | cert / 正本 | 裁定 |
|---|---|---|---|
| k=2 全 5 層 | **候補ゼロ(全滅)** — 判別式因子 4 本の profile (6,9)/(8,7)/(6,9)/(8,7)・候補 2,160 点は全 genus 7 | r13_p1_tier2_v2(548133ed…)+checker(cross-checked)| 1019/1021 |
| **D10^fix** | 【W₉ には P∞-Weierstrass 型 k=2 平面モデル不存在 ⟺ 2∉H(P∞)】(C1=trace/norm・C2=residual 条件・C5=Tier2 路に修理済) | D10_fix_v1.md | 1021/1045/1047 |
| E の同定 | **Y²=X³+336ζ₃X+1664・j=9261/8・CM なし・悪い還元素数 ⊆{2,3} ちょうど・三次捻り型** | E_identification_and_cofinality_v1.md | 1033 |
| E 指紋([P1-0d]) | monodromy 位数 36・ブロック系 (3,2)・deck 自明・可移 = 全 PASS(Nielsen 3 被覆中 d=3 は 1 本 = 一意性確認) | run 31592554388 | 1022/1023 |
| k=3 C1 次元 | **実測 10 = 予言的中**(独立照合器つき) | run 31591179588 | 1022 |
| [C2-0/1] | 回帰 4 本 all_pass(6+2/9+0/8+0/7+2)・w³⁶ 係数 = 0 | run 31592557898 | 1027 |
| Sol 113(k=3 本体) | t3 m=4 = **指定極点 Π₀=−Q₀ で空**(Gröbner{1}×独立障害 645911・E[2](F₉)=0)/crt-C2 層 (0,5) = **12 分布全て UNKNOWN_BOUNDED**(80 秒 cap) | sol_reply_113 + r13 系 cert(sol/k3-mainlines 枝) | 1036 |
| T3 再パラメータ化 | **m 走査は誤り — π_*𝒪 = 𝒪_E⊕ℰ^∨・deg ℰ=3 が RH で固定・δ=0 強制** ⟹ 走査 = Atiyah 束 moduli([P1-D2]) | t3_gap12_resolution_v1.md | 1054 |
| cofinality | **正典で YES 既決**(Prop 3.14+Thm 5.2)— 族の欠けなし・深さは反例側を縛らない(Cor 5.4 非対称) | E_identification_and_cofinality_v1.md | 1033 |
| [P1-D2] D2-1 | **YES — B₁⊕B₂=Q₀ 厳密一致(16 検査 PASS)** | p1_d2_scan_v1(6eaddf52) | 1073 |
| [P1-D2] D2-3/4 | 4 点全て V4 PASS — ただし**V1–V7 は判別力 0 ビット判明**(恒等式・m1081-1) | p1_d2_scan_v2(a99290be)+p1d2_r1_canonicalization_v1.md | 1081/1083 |
| **R-1 厳密モデル** | **W₉: x²w³−27ζ₃y(w+1)=0 / E: y²+3ζ₃xy+2y=x³・定義体⊆ℚ(ζ₃)・c=ζ₆/2**(candidate・条件 D2-GAP-4 のみ) | p1d2_r1_canonicalization_v1.md(b036267d) | 1083 |
| falsifier 監査(正準化) | 数学 14 検算 PASS(c/ρ 30 桁一致 = CV-9 同一対象・0 ビット判定正)・**B-1「類で一意」偽(passport 実現 13 群)**・B-2 CAN-1 恒真化 ⟹ 「強制」overclaim・**救済: \|Mon(λ₉)\|=324 認証済在庫 2 cert・T18n140 一意**・M-2 GAP-5 既閉・M-5 ζ₃ は W→E 層まで | fals_p1d2_r1_audit_v1.md(16dd7ca8) | 1086 |
| D2-GAP-4 裁定(v2) | CAN-1 撤回 → **【CAN-1′】P=P₁ 無仮定確定**(母集団 72・resolvent 4 類・λ₉ 類のみ \|Mon\| 分布 {324³,972⁹,2916⁶}・Galois 安定)・**【D2-GAP-6】発見+閉**(4 点族 = 72 の split 枝のみ)・GAP-5 閉・**t=−y²/4**(E 同一性初突合)・passport ((18),(2⁸1²),(18))・被覆一意は S₁₈ 共役類で判定(群一意と区別) | p1d2_r1_canonicalization_v2.md + d2gap4_gate_adjudication_v1.md(6f290d3b) | 1087 |
| R-1 宣言草案 | **分岐 (a) 正式確認 = 無条件形で宣言可**(格の層別: 骨格 ≈ cross-checked・核心 W₉=W(P₁) は数値 1 系統 = candidate・昇格 =【R1-GAP-2】)・**発令前必須 =【R1-GAP-1】母集団 72 cert 化**・D2-GAP-6 閉鎖 | r1_declaration_draft_v1.md(73942f1d) | 1092 |
| **定理 COUNT-PSL** | **③ 計数の壁消滅**: c∈N′ ⟹ PSL(2,ℤ)=ℤ/2∗ℤ/3 に落ち #Hom = **整数 2 個の積**(CH 閉形式)・Stage 0 で ≶10⁷ の 1 ビット・CP-D 較正 = 円分下界 15,180 | ss_gap1_count_spec_v1.md(73942f1d) | 1092 |
| 定理 SURV-EXACT+PB₃ | 生存数 = N_m 確定 ⟹ 総率は情報ゼロ・正分母 D₀=C_Q(σ̄₁)∩[Q,Q]/PB₃ 直積は商に降りない(m1090-1 自己捕獲: [PN:Q]=z₀)・**P2 正しい構成 = ker(π_N,T)** | iset4_remeasure_spec_v1.md+pb3_free_factor_check_v1.md | 1092 |
| **[D2-GATE] 着弾** | **両予言的中**: \|Mon(W(P₁))\|=324・\|Mon(W(P₂))\|=419904・**S₁₈ 共役 = P₁ のみ true** ⟹ §8.3 **分岐 (a) = W₉=W(P₁) 確定**該当(正式読解 = 数学者)・残差 ~1e-50・密度非依存傍証 | d2_gate_v1_20260813 + d2_gate_v1_track_20260813(run 31630925950) | 1090 |

## §2 ③ 線 = (F)/(Ad)/691 戦役の測定

| 測定 | 結果 | cert / 正本 | 裁定 |
|---|---|---|---|
| 段 1(W 層) | H^n(H_F,W⊗det^i)=0 全消滅(紙・中心スカラー)— 測定不発火 | fals_F_stage1_audit_v1.md | 991/1005 |
| 段 1′(Ad) 本番値 | **(1,0)・i₀=0 @p=691**(0ms・cal-1〜6 全 PASS・予言凍結→測定の時系列 Sol 検証済) | f_stage1ad_calib_v1 | 1013/1045 |
| (2,3)-生成 witness | **a=[[483,28],[59,208]]・b=[[245,158],[69,445]]・Size=659,877,360 完全一致**(trial 1・ローカル+GHA 二環境・1384 点法) | s2_3_pre_gen23_v1(gha_reproduction 欄) | 1057/1058 補記 |
| braid 全射(明示) | σ₁↦[[386,326],[476,658]]・σ₂↦[[175,337],[156,178]] mod 691・braid 関係機械検証 ⟹ **B₃↠H̃・c↦1**・PB₃/N′≅SL(2,ℤ/691²) | F_stage2_completion_v1.md | 1058 |
| mod 691² リフト | assert 13 項目全 PASS(明示行列 mod 477481・N_ord=47679=3·23·691) | q3r1_lift_spec_v1.md+cert | 1062/1063 |
| [Q3-R1] 前フィルタ | **charming 30,360 個中、生存 = u∈{±1} の 2 個のみ**(trace 必要条件) | q3_r1_prefilter_v1 | 1063 |
| [Q3-M1] | **u=3407 で witness**(v′ order3・u′ order2・477,481 値全数系列で確定・乱択の検出力不足を self-caught) | q3_m1_v1_20260813 | 1065 |
| **(Q3) 結審** | **N′ は非 isolated(candidate)** — 生成性 = Dickson 4 除外全通過・H̃ 全射自動・census 13/15 と整合 | q3_verdict_and_line3_reframe_v1.md | 1066 |
| 【定理 SETTLED-GRP】 | GT^settled(N) は**窓一般で群**・Ψ→Aut(Q) 準同型(COMP-E 300/300)・単射性は窓依存 | settled_grp_proof_v1.md | 1067 |
| [SG-GAP-1] | **NO(C_Q(ȳ)=分裂トーラス 476,790・f≠1 全数 476,789 で shadow 0)⟹ Ψ 真の埋入** | sg_gap1_v1_20260813 | 1068 |
| GT^settled(N′) 同定 | **↪PGL(2,ℤ/691²)・位数 ≤953,580・+成分 ≅ 巡回群 (ℤ/691²)^× の部分群** ⟹ (Q4′) = 巡回群内の位置決め 1 本 | gt_settled_identification_v1.md | 1069 |
| ③ 線の残 | (Q4′) サイズ会計([Q4-DENOM] 隊列)・GS-GAP-1(u=−1 成分・2 倍分岐)・(Q5)=R-1(F) OPEN | 同上 | 1069 |

## §3 手術計器(SURG/crown/普遍性)の測定

| 測定 | 結果 | cert | 裁定 |
|---|---|---|---|
| Frattini 表 | K(3)=12(Φ=1)・**K(9)=36**・K(15)=240・K(21)=504・**K(27)=36(公式破れ・予言的中)**・K(33)=1320・**K(81)=36(定理等号 k=4 維持)**・n=125: Φ=125・**972 屋根 = 108(Φ=9・1/9 縮約)**・1152×2 = 24(Φ=2) | frattini_resolution_v1〜v4 | 1035/1038/1048/1051/1059 |
| 族公式(紙) | **F(K⁽ⁿ⁾) = 2·rad(n)·φ(n)/Φ((ℤ/n)^×)_{π(n)}(9 点全一致)・∀k≥2: F(K⁽³ᵏ⁾)≅C₆×S₃ = [36,12](定理)** ⟹ 3 冪塔 pro-Frattini 有限 | surg_universality_audit_v1.md | 1050 |
| (T1)(T3) | reduction 全射 PASS・自然性四角形 = 108 元全数可換 | frattini_resolution_v4 | 1051 |
| crown census | 972 屋根 = 8 類・**非正規 4 類 ↔ 𝔽₃² の 4 直線(独立確認)** = r の 4 値観測の器 | crown_census_20260812+検分 | 1041/1050 |
| crown バッテリー v1 | 5 対象(K3/K9/K27/K81/972 屋根)全較正 PASS・対角較正つき | crown_battery(9f7d735a) | 1058 補記 |
| 1152 系 2 窓 | **両窓同一: GT=48・Φ=2・商 24・8 類(正規 7〔index2〕+非正規 1〔S₃〕)** | crown_battery_targets_v1(c2a59e7d) | 1059 |
| mod-Φ 影 | r̄=min(r,3)(Goursat 機械検算 PASS・片側検定・prereg-native 化は次屋根から) | modphi_shadow_prereg_native_v1.md | 1054 |
| **★C1′+P5′ 発効** | 差分レビュー採用(9/9)⟹ **648 前件束から P3・P5 閉**(残 = TB1–4・Z₁₈-link・W1・A/B)・**PH2-VOID′**(perfect E ⟹ 直積強制 — 2b の 972 = S4 内部の陰性ビットのみ・r 未接触)・次候補規則(**非完全 E・Q=3 群**・最安 = PSL(2,8)×ℤ/3)・型境界 5 度目自己記帳 | c1p5_v2_diff_review_v1.md(73386022) | 1145 |
| **便 126 返書** | 要求 A–I 全反映(**passport binding load-bearing 化・G_arith = PΓL(2,8) 同定**)・**Phase 2b(非分裂 2⁶·PSL(2,8)・void 判定通過)= 972・UNKNOWN** — 初の有情報 972・C1′+P5′ = theorem-candidate 再提出形(差分レビュー待ち) | sol_reply_126_repairs_phase2b.md+27 artifacts | 1144 |
| 閉鎖レビュー | **P3 条件付き採用**(7-cycle 判定の passport 依存の穴を発見+既存 cert 内データで塞ぎ・要求 A–D,G)・**P5′ 採用**・**★PH2-VOID: K^(l)∩N_S4 族は完全直積で 324 到達不能 = 族ごと除外(972 は定理の再導出)**・(3.60) 波及なし(ただし危険な向き)・**648 の A/B conditional は不変**・P=PGL(2,8) 同定 | c1p5_closure_review_v1.md(c6d543b4) | 1143 |
| **便 125 返書** | **Phase 2: 深度 1/2 = 972/972・横断 l=36 も 972**(cofinal chain 正式構築・半決定継続)・**(3.60) 座標修理**(旧 Phase1 helper の m 比較瑕疵・値は 972 不変)・**★P3+P5′ 閉鎖パッケージ**(幾何 monodromy=504 確定・6 dessins 分離・ι_C の ℚ 降下・P5′ 紙導出)・B1 addendum+B3/B5/S-3 修理 — **数学者レビュー通過なら発効 4 点全充足** | sol_reply_125_phase2_p3p5.md+14 artifacts | 1142 |
| **便 124 返書** | **抽象機構は採用**(DICHOTOMY-972 紙上 PASS・SINGLE-BIT は (6)+半決定修理つき・B3 3 本 PASS・B1 導出 PASS〔L_{9,Aff} 表記修理・正本 pin 差替〕)・**具体 648 は HOLD — 臨界路 = P3(dessin 束縛)+P5′(Kummer 部分群等号)**・Phase 2 は cofinal 必須・格は r_raw/r_TRIAD の 2 行分記へ | sol_reply_124_triad_audit.md | 1139 |
| **Phase 1(1 ビット)** | **\|Im R_{K,M}\| = 972(972/972 lift)= 深さ 1 は情報ゼロ・中間値なし(仮定無事)** ⟹ A/B 未決のまま Phase 2 へ(Sol レーン・便 125)・方法論は縮小版 ground truth 0 mismatch で検算済・\|PB₃/K\| 実測 39,680,928(真の subdirect < naive 積) | d972_phase1_v1(e3442054) | 1137 |
| **(H1) 閉** | [A-5] = **同一窓**(元集合一致)・N_S4 isolated 54/54 実測 ⟹ INT+Thm4.3 で **M isolated 成立 = 二分法有効化**・Phase 1 [1-2] も同時閉・**σ₁,σ₂ 実現完成**(braid+Ad 検算・17,496 一致・W4 債務返済) | d972_h1_ns4_v1+k9_sigma_realization_v1(550faa95) | 1133 |
| (H1) 帰着 | **Prop 3.15+命題 INT(5 行独立証明・Ξ 不使用)で (H1) ⟸ N_S4 isolated** — 測定規模 504(2916 分の 1)・Phase 1 前件 [1-2] も同じ 1 本に帰着・**novelty-grep 規律の初の着手前自己捕捉**・σ 実現は探索場所訂正(外側コセット・(1.11)(1.12) 直接構成) | d972_h1_adjudication_v1.md(973f37f2) | 1132 |
| Phase 0(D972) | 3/4 PASS — **\|GT(M)\|=972 独立再実測(T63「\|X\|=972」が二重測定へ)**・K^(27) gating 全確認(472,392・Thm 4.3 一致)・[0-2] (H1)=UNKNOWN(計器涸渇 → 数学者紙路・1130)・Phase 1 未発火 | d972_phase0_v1(9657e347) | 1130/1131 |
| 格裁定+作戦書 v1.1 | 3 層格(測定 cross-checked・解釈 candidate)・**【DICHOTOMY-972】全部 A 型か全部 B 型か(指数 3 素数)**・系 SINGLE-BIT({324,972} の 1 ビット・324 ⟹ 全 A 型+有限証明書)・SUPP2 確定(v₂=+2 は −Y²/4 由来・−2≡7)・**(U-10) 限定**(B 型 ⟹ ĜT_gen 水準・¬井原へは U-10 未解決を経由)・BIT-252 先行明記(検出機構別・格両面)・D972-GAP-1(M isolated 未確認 = Phase 0) | triad972_grade_and_battle_plan_v1_1.md(ea0aa8c6) | 1127/1128/1129 |
| **★★第三系統一致** | **[a]=[2]⁷ を盲実装が完全再現**(別経路・検疫完守)・u₉ = **−4/3¹⁸ 厳密**(v₂=+2・v₃=−18)・Belyi/GAUGE-18/(D-ii) 全通過・support={2} は 2 ゲージで頑健 ⟹ **バグ仮説閉鎖・r=3/648 は cross-checked 測定値へ昇格**(前件 T63+P1–P5 条件付き)・2-part の出所 = t=−Y²/4 の 4 | a_class_indep_v1(166aa87a) | 1125 |
| 発火検問 Part A | **公式正当**(2-part/3-part は指数 18 の準素分解 — supp と別物)・**d₉=9 が定理昇格(D9-VAL)**・RES-INJ-9 直接証明・残条件 = T63 鎖 3 本+P1–P5・**GAUGE-18**(uniformizer 自由度ゼロ)・**純 2 冪ズレ仮説は紙で反証**・**発火 ⟺ 予言外れ(同一事象・予言的中なら非発火)**・Part B は第三系統待ち | triad972_firing_adjudication_v1.md(b710a494) | 1124 |
| ★UNRAM 目標反証 | **L_{9,Aff} = ℚ(ζ₉,2^{1/9}) は 2 で完全分岐**(Eisenstein)⟹ 「3 の外で不分岐」は反証 — UNRAM 線は S={2,3} 確定へ棚卸し | 同上 Part B | 1124 |
| **★r 突合(TRIAD-972)** | **r = 3・\|X∖A\| = 972−12·9·9/3 = 648(生値)**・[a]=[2]⁷ order 9(**S-1 前件不成立 → P8 (u2) 枝 = P-K9U-1 外れ**)・[b]={2:1,3:6} 三重独立導出・S⊇supp(a) 整合・**解釈は数学者検問中(発火の正当性 = (u2) 枝下の公式導出)** | triad972_r_measurement_v1(commit 走行中) | 1122 |
| **R-2 完結** | [R-2-U] 有理 uniformizer 2 本(s⁽¹⁾=w・s⁽²⁾=X/w²)・Newton 多角形 e=3・見張り全 PASS(ord λ₉=18)— 厳密・数値なし | r2_u_uniformizer_v1(cdf036ab) | 1119 |
| [B″-0] 掃引 | 15 窓一括 — **\|D₀\|≥4 = 双子 [1152,154161/154163] のみ**・z₀>1 = [1134,55](型退化対照)| iset4_b0_sweep_v1 | 1119 |
| 工房 R-3 | DESC-9 (D-i)(D-iii)+canary 6 件・[U3-1] ℤ[1/2] モデル(**Jacobian 零点は解決せず = (β) 検疫の予防拡張・承認**) | desc9_procedure_v1+u3_model_v1 | 1119 |
| **★ℚ 降下** | 宣言モデルは **ℚ 上に降りる**(x=ζ₃²X・E_ℚ: Y²+3XY+2Y=X³・標識点全 ℚ-有理)⟹ λ₉ 定義体 ⊆ ℚ・**D2-GAP-7 完全閉鎖**・U3-1 = 真正 ℤ[1/S](v4 不 falsify・精密化) | r2_r3_unram_execution_spec_v1.md(f4989071) | 1118 |
| R-2/R-3 spec | R-2 残 = [R-2-U] のみ(P0-RAT で縮約)・R-3 = 規約 DESC-9・**prereg (β) 事前登録**(U3-3 の S は a_class 凍結まで検疫)・Sol 分担 3 本 = 便 123 | 同上 | 1118 |
| U6 読解 | [U6-1] 具体化正(**余剰 C₂ = S_t 符号指標**・U6-GAP-2 解消・有料 = 3 本に会計訂正)・[U6-3] **戦略確定: settled 層限定**(型境界登録・復活路 U6-5)・[B″-0] 先行発注 | u6_prereg_readout_v1.md(03944160) | 1118 |
| U6 prereg 3 本 | **[U6-1] 予言 NO**: ker(χ_vir) ⊋ [Q,Q] 指数 2(全窓一様・χ_vir 具体化は数学者レビュー待ち)・**[U6-2] wall37 = S₆ 確定**(U6-GAP-1 解消)・**[U6-3] #C 未解決確定**((A) トートロジー/(B) 検出力 ~0/路 D gating 失敗 \|B₃/N\|~10²⁴⁻⁴⁴)= 設計差し戻し | u6_prereg_v1 系 5 cert(cbb01d67) | 1116 |
| **R-1 宣言 v4(発令版)** | B1 修正全反映・母集団 72/resolvent = **cross-checked(3 code path)**・R1-GAP-3 CLOSED・格の非伝播明文化・**発令残 = 研究者検分+凍結 tag のみ** | r1_declaration_v4.md(756e1015) | 1114 |
| U6-3 裁定 | **循環実在** — Sol の X ≅ GT^settled(N)(U-6 読解は settled 層限定へ札替え)・路 B 枯死(χ_vir に #C>1 不可視)・**路 D = 非 marked 核計数 ≤ #Epi/\|Aut\| が 1 なら証明で閉鎖**・(A) は #C_settled=1 表記 | u63_iset4_p2_reading_v1.md(e9ae5a6b) | 1114 |
| I-SET-4 格上げ | 保留 → **fixture 支持(交絡なし)**: Surv⊆[Q,Q] 厳密・hexagon 単独 50%・Surv∩D₁={1} ⟹ RIGID fixture 成立(検出力 = 捻り 1 元・\|D₀\|≥4 窓で反復へ) | 同上 | 1114 |
| P2 読解 | **PASS**(SUBTOR 族外初検定)・**深さ 1 は fake 検出力ゼロ ⟹ AT-3/5 は depth≥2 必要**・**M-isolated = 288/288 実測確認(1117)⟹ 無条件化** | 同上+at2_p2_m_isolated_v1 | 1114/1117 |
| U_true cert 化 | symbolic(p=691)= Sol 全値一致+**literal(p=7・576 万行列全数)閉形式一致** ⟹ \|GT(N′)\| ≤ 1,915,460 は**三系統一致**・k13 full cert = release `k13-t4t5-cert-v2` 恒久保全(sha 前後一致) | ssg1_utrue_cert_v1(cd8d85c9) | 1113 |
| **便 122 返書** | **B1 条件つき PASS(修正 3 点で発令可)・B2 PASS = R1-GAP-3 閉鎖・母集団/resolvent = cross-checked 昇格・B3 = 定理 TORSOR/SUBTOR 採用(系 D 前向きは UNKNOWN 維持)・B5 = QUAR-TOR 合議+release 保全** | sol_reply_122_r1_line3.md | 1109 |
| ★③ 線上界の訂正 | **U_true = 1,915,460.0116…(真の H̃ 直接計数・6 整数)⟹ \|GT(N′)\| ≤ 1,915,460 < 2×10⁶**・U_split=954,962 は改名(calibration 値・上界でない・比 2.006)・**Stage 1 不要 = SSG1-GAP-1 candidate closed** | 便 122 B4(script 添付)| 1109 |
| U-6 読解 | **非可換 crown = EP 各窓 1 本**(core 単一)・**群論側空**(Z(A_t)=1 ⟹ 拡大自動)・WALL-SURJ(有料 = Kummer+EP の 2 本のみ)・**census+Chebotarev = 全射性の有限証明書(F1–F5)**・U6-GAP-1(wall37 coupling 3 択)・prereg 3 本([U6-3] isolated 性が先行)・census 第 4 系統一致 | wall_crown_u6_reading_v1.md(9a15c74d) | 1108 |
| I-SET-4 B′ 再測定 | 正分母 **D₀ = 2(非自明 = 空虚でない)**・N_m=6 全 m 一様(SURV-EXACT 整合)・**D₀ 非自明元は全 48 shadow で hexagon 単独切断(C 真・H 偽)= 交絡除去後の RIGID 支持生値**・|Q|=168 実測・K9 対照 UNKNOWN/blocked | iset4_remeasure_v1(1cf428a5) | 1107 |
| **P2 第二段(量子化)** | **GT(M)=288 全列挙(2 秒)→ 押し出し X=48(全被覆・異常 0)→ 両核類 trace = 24 = \|S_X\| — 中間サイズゼロ = SUBTOR 量子化法則の初の完全機械実証(装置生存)** | at2_p2_quantization_v1(38cf4bb7) | 1110 |
| P2 第一段 | **\|Im ρ\| = 7056**(上界 28,224 の 1/4)・ker(ρ)=N∩K₂ 独立突合一致 ⟹ 量子化検定(第二段)解錠 | at2_p2_imrho_v1(1cf428a5) | 1107 |
| Sol 便 114(k13) | 再設計完走(run 31628909628)・**gcd 369 桁 = 2³·269·103928833037·C(C 未分解 UNKNOWN)**・**QUAR-TOR [2,269,103928833037] rank 206 = 司令塔預かり**・K12 canary 全 true・full cert 237MB(receipt a6f05418…) | torsweep_k13_..._RECEIPT.json | 1104 |
| Sol 便 114(壁 crown) | **非可換 crown 実在 [3,3,3,5]**(A₅×3 窓・wall37=A₆×5 類)・GT/Φ=S₅/S₆×(C_ℓ:C_{ℓ−1})・**三系統一致 = cross-checked**・U-6 先決データ確定 | wall_crown_census_v1 系 3 cert(8577cab6…) | 1104 |
| [S0-RECHECK] | **PRED-S0-4 = 12 整数完全一致**+[R-3] 全数対照一致 ⟹ 閉形式検証済。⚠1109 訂正: **954,962 は split calibration 値(真上界でない)** — 真値は便 122 B4 の U_true | ss_gap1_s0_recheck_v1(9335dc13) | 1105/1109 |
| 2 勝 2 敗の真相 | **閉形式無罪** — cert 整数と全 4 点厳密一致(司令塔追試も 4/4)・外れ = 数学者の凍結値転記ミス・司令塔 mod 12 仮説棄却・**PRED-S0-4 再凍結(整数のみ・p=37..47 全類 12 整数)**・U(691)=954,962.000012572 機械凍結(PASS 後復帰)・**恒久規約: 成果物数値は機械生成+script 添付が検収条件** | ssg1_stage0_pred_repair_v1.md(82138f7c) | 1103 |
| 予言 4 点検定 | **2 勝 2 敗**: p=19,31(≡7 mod 12 = 691 の類)厳密一致/p=23,29 は 10⁻⁶ 級不一致 ⟹ 事前宣言どおり**閉形式破棄・修理へ**・U(691) 代入格は保留降格・counts は 2 系統完全一致 | ss_gap1_s0_predcheck_v1(731cbb72) | 1102 |
| PRED-S0-2 裁定 | **FAILED 恒久記録**(原因 = 近似 2 段・m1100-1/2)・**補題 TR**(tr 分布 = p³(p+ε))・厳密閉形式で 5 点小数 4 位一致・**観測法則 q mod 12 が証明昇格**・**U(691)=954,962.0000126(代入格・CP-D 63 倍)**・新凍結予言 4 点(p=19..31) | ssg1_stage0_pred_failure_v1.md(00f0ba2b) | 1101 |
| 余興: 普遍性ノート | C=余等化子 YES・**Frattini 反射 NO**+救済(窓圏 = 全射のみ)・発案 5 着地 = 主束 2 指数・**「普遍性は分母を整理・分子(算術像)に無言」** | surg_torsor_universality_note_v1.md | 1101 |
| [S0] 完走 | U(5..17) 2 系統一致(p=5 は全数第 3 実装も一致)・e fit=2.0195・**U(691) 外挿 ≈ 1.03×10⁶ ⟹ ≶10⁷ 内側見込み**・CP-D 余裕・**PRED-S0-2 0.47% 超過 → 停止規則発火・数学者裁定中** | ss_gap1_stage0_v2(d5dc460e) | 1100 |
| **R-1 宣言 v3** | **定義 POP**((C1) passport ∧ (C2) 次数 6 商 ≅ Nielsen 類 #1 ⟹ \|𝔐\|=72・補題 POP で非循環性証明)・**R1-GAP-3**(Sol 再現 ⟹ cross-checked/不一致 ⟹ 保留)・格 = candidate・発令残 = Sol 監査/研究者検分/凍結 tag・**便 122 筆頭積荷確定** | r1_declaration_draft_v3.md(b98fe288) | 1098/1099 |
| CP-C 裁定 | **装置維持** — 補題 CH-REG(超過 = p³−1・実測 26 と 4 行一致)・**p=691 安全証明済**(691∤2,3)・p=3 → 陽性対照 PC-5b 格上げ | ssg1_stage0_model_adjudication_v1.md(0492ece2) | 1098 |
| Stage 0 模型確定 | **(c′) H_p = PSL(2,ℤ/2p²) ≅ S₃×PSL(2,ℤ/p²)**(正準・自由度なし)・直積の罠 = #Epi=0・閉形式: 対合 tr0/位数 3 tr±1・**凍結予言 U(691)≈9.55×10⁵ = 射程内側** | 同上 | 1098 |
| 盲 checker 店じまい | 汚染 = 司令塔コミットメッセージ起因(1097)・F の探針成果 = **passport 単独の母集団 1,914,721 類**(72 本は E 塔制約族と判明)・独立検証は Sol ゲートへ移管 | scratchpad/r1gap1_blind/(未コミット保全) | 1097 |
| R1-GAP-1 cert | **648→432→72 本・resolvent [18,18,18,18]・分布 {324:3, 972:9, 2916:6}+419904:54・λ₉=1 本(324 類)** — fail-closed 表(1093)と**全行一致**・第 2 レール完全一致・盲 F 走行中 | r1_gap1_population72_v1(f23c2c57) | 1095 |
| PC-5 較正 | p=5,7 厳密一致・**p=3 不一致の原因完全特定**(3-合同核: 検定位数 3 × p=3 の衝突・3 系統裏取り)・補正後全一致・p=691 非衝突見込み(未証明・cert 明記) | ss_gap1_pc5_* + ss_gap1_stage0_v1(4c68b2a1) | 1095 |
| 発案 6+7 検分 | **定理 TORSOR**(fixture は定理の帰結・u≡1 mod 3 の機構が系)・**定理 SUBTOR**(ARITH-T 強化)・I-SET-2 改造採用(類公式・指標表不要)・I-SET-3 **棄却(NOFIRE)**・I-SET-4 保留(charming 交絡・3 分類再測定要)・AT-Q1 的中 | set_surgery_vetting_v1.md(2860805e) | 1089 |
| ★\|GT(N′)\| 見積り | **3×10⁴ ≲ \|GT(N′)\| ≲ 10⁶⁻⁷**(TORSOR×#Hom 類公式・16 群三系統一致)— **10¹⁷=\|H̃\| の取り違え疑い(約 11 桁)** ⟹ ③ 計数再開可能性(見積り格・SS-GAP-1) | 同上 | 1089 |
| [Q4-FINAL] 格下げ | f_c は**片側のみ有効**(≠1 ⟹ a_{N′}(c)≠[−1,1] のみ/=1 ⟹ 情報ゼロ)【SS-GAP-7】・1084 検算 B の中心化群は Q 内が正典意図(生値は記述値に再分類) | settled_layer_verdict_v1 補記 | 1089 |
| 発案 7 テコ 3 本 | P1: 剰余類予測 {5,11,17,23} = 実測**完全一致**(独立再確認)・**AT-4: Q-STAB = fixture で YES**(settled 24/24 → H-settled のみ・類写像 well-defined)・P2 = PARTIAL(coset 爆発実測・直積分解は Sol 警告で保留) | at_levers_v1_20260813(8e2ab1ce) | 1091 |
| トーサー計数 fixture(発案 6) | **#C([1008,521]¹)=2・類 [24,24]・48=24×2 予言厳密一致**・陽性対照 K(9)=#C 1/108 一致・捻り生存 1/12・1/28(⚠1092: SURV-EXACT により総率は情報ゼロ・生値のみ残置)・2 核類は well-definedness で分離・marked-factor-map 法 | set_surgery_fixture_v1_20260813(429c18b3) | 1084 |

## §4 census/屋根掃討の測定

| 測定 | 結果 | cert | 裁定 |
|---|---|---|---|
| roof-sweep(13/17 復元) | 陽性対照 972 一致。**×[1152,154161]: K3=144・K9=1296(Φ=6 乗法的)・K15=2880 全成立/×[1152,154163]: 6 本全て UNKNOWN_THETA_TAU_NOT_WELL_DEFINED = 双子窓の合成非対称(未解釈・数学者読解待ち)**。K21/27/33×a = cap 超過(部分値 3918/2658/1704) | run 31615934135 ログ復元・最終 cert は残 4(run 31621374555)後にマージ | 1071 |
| SETTLE-AUTO | **well_defined ⟹ settled(2 行)・census 1034 件で実証(反例 0)** ⟹ (Q3) 系の kernel 計算不要化 | iso_family_lemma_v1.md | 1060 |

## §5 機械線・その他

| 測定 | 結果 | 裁定 |
|---|---|---|
| k12 T4/T5 | H_rank=112・r′=110・exact moduli 二本一致・QUAR-TOR {2,3,5,13,37,90217,18629640697}(§5.3 部分処置済) | 992 |
| k13 T4/T5 | **4h 上限死**(dim 630 一枚岩 rank・checkpoint 皆無)— 再設計 = Sol 便 114 走行中 | 1034/1049 |
| M₂₃ 実現(外部) | arXiv 2608.08538(散在型逆ガロア完結・数値 Belyi 法・基盤論文 1311.2081 は既在庫) | 1052/1053 |
| 便 121 | 返書検収済 = 台帳 101・B1 同一対象(封印 = K⁽⁵⁾ インスタンス・K⁽⁹⁾ 2 平方類解禁)・B2 段 2 GO・修理 5 点完了+凍結 2 件(P8 v3.2 = 3a9cfb06…・段 2 spec = aa49fb52…) | 1045/1047 |

## §6 走行中(本索引時点)

[P1-D2](CP・ℰ-moduli)・残 4 屋根(31621374555)・Sol 便 114(k13+壁 crown)・[Q4-DENOM]/GS-GAP-1(隊列)・便 122 積荷 = ③ 線再出発パッケージ+本索引群。

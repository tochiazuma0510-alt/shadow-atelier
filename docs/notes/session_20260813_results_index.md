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
| **[D2-GATE]** | **走行中(CP)** — W(P₁)/W(P₂) 数値 monodromy・prereg PRED-1 {324,972,2916}/PRED-2 419904・5 分岐事前記載・(a) 無条件宣言/(b)(c) 棄却+m 走査 | — | 1087 |

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
| トーサー計数 fixture(発案 6) | **#C([1008,521]¹)=2・類 [24,24]・48=24×2 予言厳密一致**・陽性対照 K(9)=#C 1/108 一致・捻り生存 1/12・1/28(RIGID 整合)・2 核類は well-definedness で分離・marked-factor-map 法 | set_surgery_fixture_v1_20260813(429c18b3) | 1084 |

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

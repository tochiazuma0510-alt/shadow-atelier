# 便 121 積荷目録 v1(司令塔起草・数学者レビュー用)

**状態**: 草稿(裁定 1014)。発送 = 研究者の合図のみ。digest 生成と ben_preflight は発送直前(機械配管)。
**便の性格**: v1.4.9 再提出+本日戦役(裁定 969〜1013)の一括報告+認可請求 3 件。

## A. 主積荷(正本+cert)

| # | 積荷 | 正本/cert | 要点 |
|---|---|---|---|
| A1 | 見立て v1.4.9 再提出 | docs/見立て_相2_v1_4_9.md(dba5c0d) | M120-7 差し戻しの同期済み版・台帳 81 |
| A2 | T63-CONNECT^fix 四行形 | tower_repair_v2.md | 便 120 返書の修理形の履行 |
| A3 | P8 prereg v3+addendum v3.1 凍結報告 | p8_corr_v1.md(sha 1c177d67…) | :137 型エラー訂正(a₉ は ℚ 素因子分解を持たない)・判定基準不変 |
| A4 | d_{S4} receipt | ds4_receipt_v1 cert(70de6e5) | ord([u₀⁻¹]₉)=9・QUAR 不発火・条件付き(P1–P5) |
| A5 | r カード v2 凍結 | branchP_and_r_spec_v1.md(sha b1300005…) | B-1 履行(P-K9U-1 同時判定)・(r4) 新設・【r-GAP-1】 |
| A6 | [P1] 戦役一式 | w9_structure_and_ansatz_v1 / w9_ansatz_v2_blocks / w9_k2_diagnosis_v1 / w9_laneB_elimination_v1 / w9_k3_insurance_v1 + certs(r13_p1_0_blocks / p1_0b / p1_1_k2 / p1_1pp / laneB) | λ₉ 非原始(9×2, 3×6)・W9-DEG/DEG2・(e3)+ゲージ診断・U± 分解・**層 (0,9) 空(Gröbner={1}×手計算の二経路)**・完全 k 乗境界原理・k=3 正準形+次元 10 の困難・W9-GAP-2/4/9/10 |
| A7 | census 線一式 | win83_audit_and_unram3_v1(+I.1.3 訂正 m988-1)/ iso_census83_deep15_v1 cert / census83_readout_v1 / meas_chi_83win_v1 cert | (F2) 商規律への supersede 捕捉(wcp5d)・15 深窓完走(較正 2 段)・**u≡1 (mod 3) 法則**・1152 系全率の機構候補・χ 統計 |
| A8 | (F) 線一式 | fals_F_stage1_audit_v1(逐語)/ F_card_v2_and_P6_v1 / F_stage1ad_prereg_v1_1(凍結 sha 768898e1…)/ fals_F_stage1ad_audit_v1 / f_stage1ad_calib_v1 cert | **満額⟺容器の非両立**(中心スカラー補題)・容器追い転進・和則(1 bit 化)・**本番値 p=691: (1,0)・i₀=0 = 紙の二導出どおり**・系統 C(段別独立性表)・F-GAP-3/4/6/9 |
| A9 | UNRAM 再設計 | win83_audit_and_unram3_v1 第 II 部+F_stage1_and_unram5_lit_v1 第 II 部 | 判別式で S を決める(U3-1..3 機械化可・R-1 前件)・GAP-4〜7・Beckmann 要請文 |
| A10 | Beckmann scout 報告(要旨) | 金庫収蔵(書誌のみ本文へ転記) | J. Algebra 125 (1989) 236–255 確定・Wewers 引用は非 Galois/Obus は G-cover — **原本 pin 未達** |
| A11 | k12 T4/T5 cert | torsweep_k12_t4t5_finalize.json(sha ace6019d…) | H_rank=112・r'=110・exact moduli 二本一致・**QUAR-TOR 発火(検疫 7 素数・§5.3 部分処置済)**・k13 T4/T5 走行中(追送枠) |
| A12 | 規約・教訓の増分 | LEDGER 969〜1013 | W-43 運用形(m984-2)・摘出即遡及・教訓 F-1/F-2/F-3・m 系自己捕獲群(案 B・Sol 採番請求) |

## B. 認可・追認請求(Sol への問い)

| # | 請求 | 内容 |
|---|---|---|
| B1 | **封印同定の追認** | 封印 3 量(u 非公開成分・c 平方類・ĉ_μ)= **K⁽⁵⁾ 窓インスタンス**という司令塔同定(裁定 1007・台帳考古学)の追認。帰結 = K⁽⁹⁾ 側同名量の検疫条件つき解禁(NAME-COLLIDE 行必須・n=5 値計算は全面禁止維持) |
| B2 | **(Ad) 転進の追認** | ③ 線「満額を追う → 容器を追う」切替(裁定 1005)+段 1′ 完結(容器実在・R-1 留保維持)の検収。段 2 spec 設計の GO |
| B3 | **r 測定の最終確認** | カード v2 凍結済・[b] 類確保済・残 = [a] 類(R-3 出力)。R-3 の解錠条件(モデル確定後)の再確認と、a_class 出力仕様(法 9 指数ベクトル)の追認 |

## C. 追送枠(発送時点で未着なら「走行中」と明記)

- Tier 2 残 4 層の帰趨(Sol 実装〔便 112・別便軽レーン〕× 工房 v2 の先着)— **k=2 全滅なら「W₉ 非超楕円」の一級結果**
- k13 T4/T5 cert(run 31575182611)
- 便 112(計算工学レーン)の Sol 返信 — 本便と独立

## D. 台帳

台帳 81(v1.4.9)+ 本日新規主張群 = **Sol 採番待ち(案 B)**。新規の主要主張候補: 層 (0,9) 空・(1,0) 容器実在・u≡1 (mod 3) 法則・ord(P₀−P∞)|9・完全 k 乗境界・満額⟺容器非両立・NARROW 全域 −I 閉。

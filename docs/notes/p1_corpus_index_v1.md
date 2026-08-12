# P1 完結体系 索引 v1 — dihedral 予想(2405 Conj 5.1)線の記録所在一覧

**状態札: `索引(記録の転記のみ)/ 判定語の新設なし・数学の再導出なし / 各行に閉鎖裁定番号・該当便番号を必記 / Lean 検証・格付けの変更を一切行わない`**

- 作成: 司令塔委嘱の調査係 / 2026-08-12(裁定 913 予定・研究者指示「P1 関係は全部過去にやってないか確認して」)
- 背景: P1 は**全文完結・文献照合完了・Sol 監査済**(研究者確認 2026-08-12・裁定 908)。しかし compaction 後の司令塔が完結記録の所在を見失い、閉鎖済み項目を open 扱いする手戻りが 3 回発生(裁定 904 の「未証明入力 3 点残存」= stale 地図行由来の誤り → 裁定 908 で訂正・裁定 911 = 配達済み文献の見落とし)。本索引は再発防止の 1 枚。
- 一次資料: `provenance/LEDGER.md`(裁定 440〜912 帯)・`provenance/CLAIMS.md`・**Sol 便スレッド**(`sol/sol_reply_*.md` / `ops/inbox_codex/sol_task_*.txt` — 便 96/99/102〜106 が P1 発効サイクルの自己完結カプセル)・`docs/状態.md` §5.5・`docs/地図.md` P1 行(8/12 delta)。

## 本索引の読み方(3 行)

1. **P1 に触れる前に本索引を読む**(`docs/状態.md` §5.5 の導線)。「閉」と書かれた行には閉鎖裁定番号・該当便番号・正本ファイルが必ず付いている — それが無い主張は本索引の外の主張である。
2. 格の語彙は記録の転記(theorem-framework-relative / candidate / cross-checked / paper-proof / UNKNOWN / open)。**candidate 残余 6 項(W2-fam・W5・Λ-REG・(M-b)・ASM-α・始点算術)は発効後も明示継承**(便 106 F106-1.1 erratum・裁定 559/908)— これを落とした要約は誤り。
3. ⚠ **NAME-COLLIDE**: 「C1/C3/C5」は二義ある(§6.2)。c2c4 札(数学前件)と裁定 578 の文献配達札(Ichimura–Sakaguchi / Kurihara / Ghate)を混同しない。

---

## 0. 結論(裁定 908 の逐語要約)

**P1/FAM-U-ASM = Sol 監査済・発効が正**(条件付き PASS → 発効宣言 → 便 106 で Sol PASS 追認・TB3 = 裁定 480 で閉)。格 = `theorem-framework-relative [TB: canonical-source-pinned/v2]`(条件履行 = v2.1・bridge proof ID = B-6^tw-lf/B-7^tw-lf・required bridge form = uniform (5'^b))。candidate 性の残余 = W2-fam / W5 / Λ-REG / (M-b) / ASM-α / 始点算術の継承。残作業 = **Lean 形式化のみ**(§10・停止中)。

---

## 1. FAM-U-ASM(総組立)発効の 3 段

| 段 | 内容 | 裁定 | 便 | 日付 | 正本ファイル |
|---|---|---|---|---|---|
| **1. 条件付き PASS・昇格** | Sol が P1/FAM-U-ASM を条件付き PASS(TORS-U 生存・ζ_M = 命名用生成元・link は B-4c に潜まない)。発効条件 = ①B-4c^u の versioned 記帳 ②要求橋を (5'^b) と記帳 | **547** | **105**(F105-1.1 / F105-1.2) | 2026-08-05 | `sol/sol_reply_105_math32.md` |
| **2. 発効宣言** | 発効記帳束の採択・proof ID `b4c-u/v1` 正式採用・**「FAM-U-ASM 昇格の発効を宣言」**(条件 2 件は本束で履行) | **550** | (便 106 組立サイクル・裁定 549) | 2026-08-05 | `docs/notes/p1_ratification_bundle_v1.md`(commit 7ef2e5a) |
| **3. Sol PASS 追認** | **「限定された FAM-U-ASM 発効: PASS … 裁定 550 の発効に異議はない」**(6 条件履行確認)。同時に erratum: campaign の candidate 性は枠組み層「唯一」でなく **W2-fam/W5/Λ-REG/(M-b)/ASM-α/始点算術も継承** | **559** | **106**(F106-1.1) | 2026-08-05 | `sol/sol_reply_106_math33.md` §F106-1.1 |
| (総括の正本) | 上記 3 段を「発効が正」と再確定・裁定 904 の誤り(「未証明入力 3 点残存」= stale 地図行由来)を correction of record | **908** | (便 119 v7 反映) | 2026-08-12 | `provenance/LEDGER.md` 裁定 908 |

- 格(逐語・便 106 F106-1.1 が追認): `theorem-framework-relative [TB: canonical-source-pinned/v2] (条件履行 = v2.1; bridge proof ID = B-6^tw-lf/B-7^tw-lf; required bridge form = uniform (5'^b), not exact (5'))`
- ⚠ 転記注記: 裁定 908 本文の表記は「条件付き PASS〔裁定 546 系〕→ 発効宣言〔565 系〕」だが、当該裁定の実番号は上表のとおり **547 → 550 → 559**(546 = Sol 側実装原則の研究者裁定・565 = 便 106 全節検収)。どちらも同じ便 105/106 サイクルを指す。
- 昇格対象は 2 つ**だけ**(①前件つき含意定理 (d1) ②族一様の窓側補題)。**意味しない 3 項**(F105-1.2 逐語): W2-fam 全奇数成立/全奇数で ord(aₙ)=n/算術的始点の閉鎖 — これらは candidate/open を保つ(`p1_ratification_bundle_v1.md` §2.1)。

## 2. 先行段(総組立に至る鎖の記帳)

| 項目 | 最終状態 | 裁定 | 便 | 日付 | 正本ファイル | 格 |
|---|---|---|---|---|---|---|
| 総組立言明 v1 起草 | domain = 奇数 n≥3, n≠5 で起草 | 348 | (便 95 差戻しの履行) | 2026-08-01 | `docs/notes/fam_u_assembly_v1.md` | candidate |
| 主言明の Sol 採択 | P95-1.1 主言明 = 条件付き PASS(文書 v1 は v2 修文条件) | **353** | **96**(F96-1.3) | 2026-08-01 | `sol/sol_reply_96_math23.md` | candidate 鎖 |
| ASM 依存表 v2+追記 A | 最短鎖 7 段((S0)-(S5)+(S*)=M2)・便 97 差戻し 3 点全閉 | 354 / 362 / 366 | 97 | 2026-08-01 | `fam_u_assembly_v1.md`【v2 追記 A】 | candidate |
| (M2) 三部作(GEO+UNIQ+DESC) | **theorem 格**(F95-1.4 で Sol が直接降下証明を供給・M4 は M2 の系) | 331 / **344** / 348 | 95 | 2026-08-01 | `docs/notes/m2_family_identification_v1.md`+追記 E | theorem(n 一様) |
| domain 復帰(n=5 込み全奇数) | 復帰 3 段履行・予言 4 項全的中(u₅ = 4(−1)^α 型)・現行宣言 = **P99-1.1** | 396 / 398 / 407 → **412** | **99**(F99-1.1/1.2 PASS) | 2026-08-01→02 | `docs/notes/fam_u_v1_addendum_domain_restore.md`・`fam_u_assembly_v1.md`【v2 追記 B】 | candidate 鎖(P99-1.1 逐語) |
| 追記 C(層 3 既在供給の明記)・追記 D(矢印 (d) の二分割) | F103-5 PASS 済みの適用完了(additive・host 不改変) | **516** | 103(F103-5) | 2026-08-05 | `fam_u_assembly_v1_addendum_C_applied_f103.md` / `_addendum_D_arrows_f103.md` | additive erratum |
| 混合側の帰着 | **(U2) 採択 = 「混合側 Conj 5.1 ⟸ 奇側」発効**(定理 U2-BR)+定理 MIX-4・系 MIX-12(n=12 決着 = 裁定 259) | **319** | **94** | 2026-08-01 | LEDGER 裁定 319・`docs/地図.md` P1 行 | 発効(定理) |
| n=3(最小 open ケース) | **定理 K3 = Conj 5.1 最小 open ケースの解決(成立側)**・PASS 昇格承認 | 22 → 便 28 承認 | 27/28 | 2026-07-26 | CLAIMS **W3-11**・`docs/week4-K3飽和_opus_v3.md` | paper-proof / two-mathematician audit PASS |
| n=3 有限層 Lean | Phase 1/2+F29+忠実性監査・修理 | W3-14/14b/14c/14d | 33 帯 | 2026-07-27 | CLAIMS W3-14 系・`lean/K3/` | **verified**(記載定理の範囲) |

## 3. 橋(B-1・B-4c^u・B-6^tw-lf/B-7^tw-lf・B_FC)

| 橋 | 最終状態 | 裁定 | 便 | 日付 | 正本ファイル | 格 |
|---|---|---|---|---|---|---|
| **B-1**(枠組み相対橋: ord([uₙ])=n → ord(aₙ)=n) | P1 残として明示(裁定 444)→ 照合仕事へ縮小(440/441)→ **(5′) の TB 相対格で閉**: 条件付き PASS(501)→ 条件履行 v2.1(504)→ **PASS 格確定**(F104-3.1「TB v2.1/(5′) PASS・格据え置き」) | 444 → 501 → 504 → **515/520** | 103(F103-4)→ **104**(F104-3.1) | 2026-08-04→05 | `docs/notes/tb_citation_bundle_v2_1.md`・`sol/sol_reply_104_math31.md` | theorem-framework-relative [TB: canonical-source-pinned/v2] |
| **B_FC**(比較橋・族定理 R^cyc の完成) | (TB1)–(TB4)+(Z_{2M}-link)+(CAL)+(W1)–(W5) 下の framework-conditional 定理。裁定 440 が「**TB 相対 two-mathematician PASS 済の既在札**」を確認(fam_u_assembly の未引用が手戻りの因) | W3-17(監査鎖 = 裁定 帯)・440 | **43〜52** | 2026-07-28 | CLAIMS **W3-17**・`docs/week4-BFC攻略_opus_v2.md`(BFC v2.15) | framework-conditional paper-proof / two-mathematician audit PASS |
| B_FC の seal-relative 化 | Z-norm-seal/v1 下で TB4-B/B-7 が root-normalization-relative 定理(三層供給型) | W3-21(裁定 70-76 帯) | 59〜64 | 2026-07-28 | CLAIMS W3-21・`docs/znorm_seal_final_v1.md` | root-normalization-relative paper theorem |
| **B-6^tw-lf / B-7^tw-lf**(link-free 橋 = Route T) | 証明成立(条件 1 点 = B-4c の ζ_M 読み)→ Sol 裁定「**命名生成元と読む**」で確定・(Z_{2M}-link) は数学的必要でなかった(補題 TORS-U)。**FAM-U-ASM の bridge proof ID** | 517(委嘱)→ **519**(検収)→ **547**(確定) | **105**(F105-1.1/1.2) | 2026-08-05 | `docs/notes/b6tw_linkfree_proof_v1.md`(proof ID `b6tw-linkfree/v1` / `b7tw-linkfree/v1`)・`docs/notes/match_one_supply_v1.md`(MOS-1) | 発効束の bridge(§1 の格に内包) |
| **B-4c^u**(link-free 連鎖の入口) | proof ID **`b4c-u/v1`** 発行(F105-1.1 指定文言逐語・依存 = (TB1)(TB2)(TB3)+(TB4ᵘ)・exact (TB4) / (Z_{2M}-link) **不要**)。【B6LF-GAP-1】閉 | **550**(発行)・559(追認) | 105 → 106 | 2026-08-05 | `p1_ratification_bundle_v1.md` §1 | 既存 B-4c と同格(framework-conditional paper-proof)・記帳は格を上げない |

**supersede / 包含関係**(F105-1.1 / F105-7 逐語の転記):

- **B-4c^u は現行 B-4c(exact 形)を特殊化として含む**(link+exact (TB4) 下で b=1 を回復)。両 ID は競合せず**並存** — 現行 B-4c の依存欄を遡及して弱める読みは禁止(禁止 2 項・`p1_ratification_bundle_v1.md` §1.5)。
- **Route T**(twisted link-free: B-4c^u ⟹ B-5^u+B-6^tw-lf ⟹ B-7^tw-lf)が総組立の要求橋。**Route E**(exact: 定理 B-7 現行 = TB1–TB4+(Z_{2M}-link)+(W1)–(W5)+(CAL))は**旧 proof ID として削除せず別保存**(F105-7)。
- link inventory(W3-20: K⁽⁵⁾ supplied・K⁽³⁾ Z₁₂ / A₅ Z₁₀ **pending**・n=7,9 not_assessed)は**保存・ただし FAM-U-ASM の残件ではない**(追記 C §C.1.1・`p1_ratification_bundle_v1.md` §2.4)。
- 補題 B-9′(ε 非依存性)= W3-18(便 46/47/52・framework-conditional paper-proof)。

## 4. 枠組層(TB1・TB3・TB4ᵘ)の pin 閉鎖

| 項目 | 最終状態 | 裁定 | 便 | 日付 | 正本ファイル | 格 |
|---|---|---|---|---|---|---|
| **TB1** | Deligne 1989 **§10.16**(圏同値言明)+**§15.13/15.15/15.18/15.20**(接基点繊維関手)+**§15.23 LEMME**(局所圏同値)— 番号水準・頁画像照合済 | **450** | (reader 内製・便 102 F102-7.1 で Sol 読解 PASS = 裁定 490) | 2026-08-04 | `docs/notes/reading_deligne_s15_profinite_v1.md`・`docs/notes/tb_citation_bundle_v1/v2/v2_1.md` | canonical-source-pinned |
| **TB4ᵘ** | Deligne **(16.1.1)/(16.1.2)**+Ẑ(1) 実現源 = **14.2+15.23 PREUVE**(ε = Z(1) 自明化は本文で固定されず = 便 44 F7.2 分解と構造整合) | **450**・481 | 同上 | 2026-08-04→05 | 同上 | canonical-source-pinned |
| **TB3** | **Ihara ICM 1990 講演 §2.3(印字 105-106)で全部品の pin 成立 =【文献要請 14】消費・TB3 閉(candidate)**。裁定 908 が「TB3 = 裁定 480 で閉」を再確認(LMS 200 購入不要と確定) | 479 → **480** | (reader 内製) | 2026-08-05 | `docs/notes/tb_citation_bundle_v2.md`(ブロック pin)・ICM 第 1 巻 = 研究者調達 | candidate(引用 pin 済) |
| TB 束 v2(4 ブロック全 pin) | 【GAP-TB-EXACT】解消 = SGA1 **Exp IX Th 6.1+Exp V Prop 6.13** 頁画像 pin | **498** | 103 へ積載 | 2026-08-05 | `tb_citation_bundle_v2.md` | candidate |
| **(5′) の格確定** | 条件付き PASS(F103-4)→ 4 条件履行 = v2.1(RD-6′ 分離ほか)→ **PASS・格据え置きで確定**(F104-3.1) | **501** → **504** → 515/**520** | **103** → **104** | 2026-08-05 | `tb_citation_bundle_v2_1.md`・`sol/sol_reply_104_math31.md` §3 | **theorem-framework-relative [TB: canonical-source-pinned/v2]** |
| EXSEQ-LIM(完全列の極限補題) | 債務 2 件「消滅」型解決(外部入力 = SGA1 Exp I の 3 項目のみ)→ v1.1 の Q-1/Q-2 **両 PASS** | **518** → **559**(F106-1.2/1.3) | 105 → **106** | 2026-08-05 | `docs/notes/tb_exseq_lim_proof_v1.md`+`_v1_1_addendum.md` | PASS(核心)・「完全」札は F106-1.4 の境界つき |
| 昇格キャンペーン文書 | candidate 理由の局在((TB1)(TB3)(TB4ᵘ) の正典引用欠如 1 点)→ pin 完了で消化。campaign v2+ASM-α-CAL/v1 較正 ALL PASS | 445 / 476 / 483 | 102 帯 | 2026-08-04→05 | `docs/notes/framework_promotion_campaign_v1.md` / `_v2.md` | candidate(設計ノート)・**ASM-α は open 継承** |

## 5. (S3) 族版と始点算術

| 項目 | 最終状態 | 裁定 | 便 | 日付 | 正本ファイル | 格 |
|---|---|---|---|---|---|---|
| (S3) の訂正上申 | 「矢印 (d) 前半は既閉・未証明ラベルは始点ノードへの誤配置」受理 → q=7 は (d) の前件でなく系の適用 gate | **457** | 102 | 2026-08-04 | LEDGER 裁定 457 | 受理(erratum は Sol ゲート後) |
| (6′) 有限計算 | n∈{3,7,9} 全 14 単元窓で成立(P-S3F-4 的中)= BRIDGE-one 機械側閉塞 | **470** | 102 | 2026-08-04 | `search/certs/s3f_a3_6prime_20260804.json` | cross-checked(較正アンカー) |
| **定理 SIXP-fam((6′) の族版)** | 全奇数 n≥3・全 α≠0 で紙成立(枠組み層不使用)→ **Sol PASS(α≠0 の範囲)= 発効** | 484 → **490** | **102**(F102-5.1) | 2026-08-05 | `docs/notes/s3_family_completion_v1.md` 第 I 部 | PASS(条件付き形)・(6′) 既閉(裁定 912 でも確認) |
| **APPLY-fam(APPLY ゲートの族版 = C1′-any の定理化)**+MATCH-one/ORD-IDX | **Sol PASS(条件文として)**。SURJ は条件結論のまま | **490** | **102**(F102-5.2) | 2026-08-05 | 同 第 II 部・`match_one_supply_v1.md` | PASS(条件文) |
| (d) 二矢印分割 | **(d1)**(ord(aₙ)=n ⟹ 像形)= R^cyc+MATCH-one+(5'^b) 相対 → FAM-U-ASM 発効に内包/**(d2)**(像形 ⟹ SURJ)= 既在の系 SURJ-Split (e) 族適用で**閉** | **495** → 516(適用) | 102(F102-5.3)→ 103(F103-5) | 2026-08-05 | `fam_u_assembly_v1_addendum_D_arrows_f103.md`・E1 追補 A | erratum 適用済 |
| E1-GAP-5 への訂正注記 | 「(S3) 族版が無い」行への訂正注記(**GAP は失効しない**が、裁定 908 により旧「(S3) 族版未証明」表記は superseded) | 516・**908** | 103 → 119 | 2026-08-05→12 | `E1_gt_odd_dih_canonical_v1_addendum_a_f103.md` | additive erratum |
| **始点算術(E1-GAP-5/6 = 全奇 n の ord(aₙ)=n 供給)** | **open / candidate 継承が正**(発効の明示残余・F106-1.1 erratum)。「全奇数で ord(aₙ)=n」は発効が**意味しない 3 項**の 1 つ。per-n 実績: n=3 = 定理 K3(W3-11)/n=5 = 開封的中 u₅(裁定 398)/n=7 = u₇ 発火(裁定 301)/**n=9 = 測定問題化: d₉ = ord(a₉) = ord([u₉⁻¹]₁₈) の測定に還元(前件 = C1/C3)** | 559 / **908** / **912** | 106 / 119(v8) | 2026-08-05→12 | `E1_gt_odd_dih_canonical_v1.md` §8(定義)・`docs/notes/k9_p1_recon_v2.md` | **open(candidate 継承)** — 閉扱い禁止 |

## 6. C1/C3 の札(⚠ 二義あり — 別行で収載)

### 6.1 c2c4 札(数学前件・K9 線)

| 札 | 定義 | 最終状態 | 裁定 | 便 | 正本ファイル |
|---|---|---|---|---|---|
| **C1** | (6.3) の下段窓が H^fun か | CLAIMS W3-24(2026-07-28)は「C1(裁定 107)+named framework 前件の下で」と条件使用の形で記載。**裁定 912(2026-08-12)では K9 前件の 1 枚として現役 — 状態調査を数学者へ回付中(判定未着)** | W3-24 / **912** | 76 帯 / 119 | `docs/notes/c2c4_closure_v1.md` §2.3・`k9_p1_recon_v2.md` |
| **C2** | (W1) の n=9 供給 | **閉鎖(族で・W1-fam)** — 全奇 n≥3 一斉・残る依存 = (CAL)(既証明)のみ。裁定 912 でも「既閉」と確認 | c2c4 v1 起草(裁定 112 帯)・912 | — | `c2c4_closure_v1.md` §1 |
| **C3** | (W2)+(5′) の **B_FC n=9 instance**(実質 5 項 I6〜I10) | **open** — 裁定 912 の K9 前件の 2 枚目。**状態調査を数学者へ回付中(判定未着)** | **912** | 119 | `c2c4_closure_v1.md` §3 |
| **C4** | ord(a₉) ∣ 9 | 独立残件でない(C3 または (6.3) に従属・tower から無償 = 命題 C4-T) | c2c4 v1・912 | — | `c2c4_closure_v1.md` §2 |
| G3・(6′) | (n,d) 一般性ほか | **既閉**(G3 = 便 75 F3.2 PAPER-PROOF・(6′) = 裁定 470/484/490) | 912 が確認 | 75 / 102 | 同上 |

### 6.2 ⚠ NAME-COLLIDE — 裁定 578 の C1/C3/C5(文献配達札・**別物**)

| 札 | 内容 | 裁定 | 便 | 日付 | 所在 |
|---|---|---|---|---|---|
| C1(配達) | **Ichimura–Sakaguchi**(本命・DOI 経由で数学者自己取得指示) | **578**+補記 | 109 同梱 | 2026-08-06 | 金庫 `hunt_20260806_classical_sweep.md`(CLASSICAL-SWEEP 三色地図) |
| C3(配達) | **Kurihara 1992**(Compositio 81・実物配達 = papers/kurihara-1992) | **576 / 578** | 109 | 2026-08-06 | `papers/` |
| C5(配達) | **Ghate 解説**(Vandiver・実物配達) | **578** | 109 | 2026-08-06 | `papers/` |

両系列を同一視した記帳は存在しない(本索引が初めて並置して注意喚起する)。**q=7 線の「C5」**(§7)はさらに別の第三義(凍結手続き札)である — 引用時は必ず出所ファイルを添える。

## 7. K⁵ blind campaign と q=7

### 7.1 K⁵ blind campaign

| 項目 | 最終状態 | 裁定 | 便 | 日付 | 正本ファイル | 格 |
|---|---|---|---|---|---|---|
| Freeze 1 | 凍結正本 = commit 578b4fe の 5 文書(sha256 封印・Sol 独立再計算一致)・campaign = BRIDGE-UNKNOWN 維持 | **43**(W3-16) | **42** | 2026-07-27 | CLAIMS W3-16・`sol/sol_reply_42_final.md` | 手続き成立(数学 claim でない) |
| Part-A 版イベント | Rule 1 v1.4 / manifest v1.6 operative 化・(5′_b) へ versioned 移行 | W3-19(裁定 48-69) | **58** | 2026-07-28 | `docs/week4-K5_Rule1_v1_4.md`・`docs/manifest_k5_v1_6.md`(v1.7 = 裁定 66 帯・`manifest_k5_v1_7.md`)・`family_rule1_seal_v1/v2.md` | 手続き成立 |
| Z-norm-seal/v1 | profinite root normalization 採用・K⁵ typed migration record | W3-20(裁定 70-76) | **64** | 2026-07-28 | `docs/znorm_seal_final_v1.md`・`docs/k5_migration_record_v1.md` | 手続き成立 |
| genuine 戦役 設計 | 宇宙事前登録(40 元)・命題 K5-BIT。**本測定は発火不能(検出力ある細分が未構成)という設計成果** | **409** | 99 積載 | 2026-08-01 | LEDGER 裁定 409 | 設計成果 |
| Phase 1(較正) | **GO**(便 99)→ **較正完走**(K5-1〜K5-5 全アンカー PASS・停止規則不発火) | **412** → **413** | **99** | 2026-08-02 | LEDGER 裁定 413 | 較正 PASS |
| 封印の現況 | **u 層(FAM-U/uₙ)= 非接触義務解除済**(裁定 396/398)/**genuine 層 = blind 継続**(IF-FIRST 凍結・欄 B)。n=5 は**純定理の量化域に含まれる**(欄 A)— 二欄分離が正本 | 396/398・**550**(§3) | 105 → 106 | 2026-08-05 | `p1_ratification_bundle_v1.md` §3(欄 A/B) | 運用(数学と別勘定) |
| FIVE-BYPASS | 系 FIVE-BYPASS 完全形登録+戦略反転(fake 探索の次標的 = K⁽⁵⁾ 直撃) | 394 → 399 → **407** | 98 帯 | 2026-08-01 | LEDGER 裁定 399/407 | 登録済(系) |
| 検出細分の建設(W-6/BOTTOM-UP 線) | BU Freeze-2 **発効**(freeze ID = W6-BU-FREEZE2-EXACT17-F106)→ 掘削発火 → S3.5 完遂・L-3 束 cross-checked(SM-1 開示つき)・S3.6〜S9 LOCKED | **565** → 583 → 591 → 604/606/615/**629** | **106** → 112 | 2026-08-06 | `sol/sol_reply_106_math33.md` F106-4・CLAIMS C-8 | 走行中(P1 の外周・genuine 層の装置建設) |

### 7.2 q=7(C1′(7)+C5・u₇ 発火)

| 項目 | 最終状態 | 裁定 | 便 | 日付 | 正本ファイル | 格 |
|---|---|---|---|---|---|---|
| 前件の正式確定 | q=7 残前件 = **C1′([α] 3 類)+C5(手続き)**(F85-1.2) | **214** | 85 | 2026-07-30 | LEDGER 裁定 214・`docs/notes/c21_draft_v1.md` | 確定 |
| C1′(7) 要件表・設計 | 9 項要件表(中核 = 回転指数比)・C1′ は構成的経路のみ生存 | 287 / 297 | 91 帯 | 2026-07-31→08-01 | `docs/notes/c1prime_s4_design_v1.md` | 設計 |
| **C5(7) 発効** | U7-13 決着([γ],[δ] は一意決定量・H¹=1・文献要請 U7-1 撤回)・凍結修正 v2 採択・**修正済み C5(7) を発効** | **299** | (内製・便 93 で監査) | 2026-08-01 | `docs/notes/u7_twist_determination_v1.md` | 発効(凍結) |
| **u₇ 発火** | **u₇ = −4・経路 A/B 一致(cross-checked)・[u₇]₂=1・ord(a₇)=7・NULL 枠 0 発動**。SURJ-K7 の全射主張は gate 閉鎖後(未主張) | 300(認可)→ **301** → 302(第二系統 19/19) | — | 2026-08-01 | `search/certs/u7_fire_20260801.json`・`u7_fire_log_v1.md` | cross-checked(発火値) |
| Sol 検収 | u₇ = **粒度限定 PASS**([u₇]₂=1 は二経路一致・exact 値の cross-checked 表示は過大)・**u₀ cross-checked 採択** | **303** | **93** | 2026-08-01 | `sol/` 便 93 返書 | 粒度限定 PASS |
| C-β 完成 | u₇ の同定が **D-3/D-4 非依存かつ cross-checked** に(最終 cert 発行) | 313 / **314** | 94 帯 | 2026-08-01 | LEDGER 裁定 314 | cross-checked |
| APPLY 側の族化 | C1′-any の定理化 = **APPLY-fam 発効(条件文)**(§5 参照) | **490** | **102** | 2026-08-05 | `s3_family_completion_v1.md` 第 II 部 | PASS(条件文) |

## 8. 文献照合の完了記録

| 項目 | 最終状態 | 裁定 | 便 | 日付 | 正本ファイル |
|---|---|---|---|---|---|
| **文献要請 13(Deligne 1989)消費** | 要請の既立を同定(440)→ **既収蔵と確定**(441・papers/delivered/deligne_1989_…pdf・sha256 689b516f…)→ 版ずれ事前検出(Betti vs 副有限 §15.13–15.27・445)→ **TB1/TB4ᵘ の番号水準 pin 確定(頁画像照合済)**(450) | 440 / 441 / 445 / **450** | (reader 内製) | 2026-08-04 | `docs/notes/reading_deligne_s15_profinite_v1.md` |
| **文献要請 14(TB3)消費** | 単独供給文献なし・継ぎ接ぎ案採択(448・SGA1 = papers/sga1-…arxiv0206203.pdf 取得)→ ICM 第 1 巻 受領・収蔵(479・研究者調達)→ **Ihara ICM §2.3 pin 検収 =【文献要請 14】消費・TB3 閉(candidate)**(480) | 448 / 479 / **480** | (reader 内製) | 2026-08-04→05 | LEDGER 裁定 480・`tb_citation_bundle_v2.md` |
| Sol 側の TB 読解検分 | 引用画像と局所補題 = **PASS**(転記正確・TB1-FF/TB4-INJ 成立) | **490** | **102**(F102-7.1) | 2026-08-05 | `sol/sol_reply_102_math29.md` |
| GAP-TB-EXACT | SGA1 **Exp IX Th 6.1+Exp V Prop 6.13** の頁画像 pin で解消 | **498** | 103 | 2026-08-05 | `tb_citation_bundle_v2.md` |
| EXSEQ-LIM の外部入力 | SGA1 Exp I の 3 項目のみ(全て present 画像✓)・EGA IV 不要化 | **518** | 105 | 2026-08-05 | `tb_exseq_lim_proof_v1.md` |
| K9 測定線の追加 pin(2026-08-12) | Ihara ICM unram pin(§5.2 p.112・survey 無証明の格注記)= 906/SGA1 開曲線 pin 束(Pin B/C/D で自前導出が立つ見込み)= 910/**文献リスト 8 件全突合 = 全て回収済みだった**(手戻りの決算・在庫 4 点検査を恒久化)= 911 | 906 / 910 / **911** | 119 | 2026-08-12 | `docs/scout/ihara_icm_unram_pin_v1.md`・`docs/scout/k9_goodred_pin_v1.md` |
| (参考・B₄/FAKE-KILL 線) | Fresse Part 1 刊行版収蔵(引用連鎖 2008 Thm A.1 → I.6.2.4 閉)→ TRUNC-FULL PASS | 425 / 428 → **490** | 101 → 102 | 2026-08-02→05 | LEDGER 裁定 425/490 |

## 9. 論文全文(原稿の所在)

**P1 の単一「論文原稿」ファイルは repo に存在しない — これは欠落ではなく裁定 536 の工程どおり**(2026-08-05・研究者指示):

> 「公開はしないが、Lean の実装が終わったら論文を PDF に起こしていつでも公開出来る状態にだけはしておく」— トリガー = **Lean P1 形式化の完了**(Sol→Luna ループの出口)。工程(対訳辞書完備 → 数学者起草 → 司令塔レビュー → Lean 対応表)は **Lean 完了後に着工**。付帯 = 裁定 537(記法の著者対称性)・538(全体ゲシュタルト照合)。

- Lean は停止中(§10)につき **原稿は未着工が正**。E1 正典 2 本(`e1_canonical_v1.md`・`E1_gt_odd_dih_canonical_v1.md`)はいずれも状態札に「**論文ではない**」と明記。`docs/論文化ノート_v0.md` は書式・引用・形式化の**規範文書**・`docs/論文用対訳辞書_v0.md` は対訳辞書 — どちらも原稿ではない。
- 研究者確認の「全文完結」の実体 = **証明ノート正本群(コーパス)+発効記帳束**。コーパスの主要正本(いずれも本索引の各節に裁定番号つきで登場):
  `fam_u_assembly_v1.md`(+追記 A/B 同居・追記 C/D 別置)・`fam_u_v1.md`+addenda・`p1_ratification_bundle_v1.md`・`b6tw_linkfree_proof_v1.md`・`match_one_supply_v1.md`・`s3_family_completion_v1.md`+追記 τ・`tb_citation_bundle_v1/v2/v2_1.md`・`tb_exseq_lim_proof_v1.md`+v1.1・`week4-BFC攻略_opus_v2.md`・`week4-K3飽和_opus_v3.md`・`oddH_full_proof_v1.md`・`w2fam_v1.md`・`m2_family_identification_v1.md`+追記 E・`c2c4_closure_v1.md`・E1 正典 2 本+追補 A・`framework_promotion_campaign_v1/v2.md`・`k9_p1_recon_v1/v2.md`。

## 10. Lean 形式化の到達点と停止点

| 項目 | 最終状態 | 裁定 | 便 | 日付 | 正本 |
|---|---|---|---|---|---|
| 割り付け表・着工 | 49 補題・T2 公理 6/T1 実質 2・着工可 21 本 | **525** | 105 §6 | 2026-08-05 | `docs/notes/lean_p1_allocation_plan_v1.md`・`lean_axiom_policy_v1.md`(v1.5) |
| 第 1 波 | sorry-free 6+補助 7 — **paper-fidelity FAIL 差戻し**(12 命題は kernel check 通過で限定受領) | 540 → **547** | **105** §6 | 2026-08-05 | `sol/sol_reply_105_math32.md` |
| 運用体制 | Sol 一回監査 → **Sol 指示×Luna 実装ループ・全面 Sol 側移管**・GHA は工房 broker | **531 / 542** / 551 / 552 | 105b/105c | 2026-08-05 | LEDGER 裁定 531/542 |
| 初 verified 格 | **「実装済み theorem island は manifest 公理集合に相対して verified」**(180 定理・公理 = core 3 のみ・run 31021842884) | **565**(F106-6) | **106** | 2026-08-06 | `sol/sol_reply_106_math33.md` |
| LA ブロック完成 | **P1 Lean = 447 定理/12 modules**・公理 = core 3 のみ・run 31045928344 全 success | **579**(108d) | 108 | 2026-08-06 | LEDGER 裁定 579 |
| 111b | CyclotomicRam2 討ち取り+G2a = **狭義 verified 受理**(run 31059473056)・T2 型契約 = BLOCKED-FOUNDATION | **605** | 111b | 2026-08-06 | LEDGER 裁定 605(merge ab64cf2) |
| G2b | BLOCKED-MATHLIB → **公理化認可**(専用 ShadowAxioms・verified-modulo-axioms) | 609 → **610** | 111c | 2026-08-06 | LEDGER 裁定 610 |
| **111d(現到達点)** | **G2b = PASS-MODULO-AXIOMS+FiberFunctor 終対象保存 = 狭義 verified**(run 31066205121 全 success・merge 88a0fde)。現況: 狭義 verified = CyclotomicRam2+G2a+fiber-terminal/modulo-axioms = G2b/OPEN = G2b-exact・T2 系・残義務 | **627** | 111d | 2026-08-06 | LEDGER 裁定 627 |
| **停止点** | 相 2 ピボット =「**Lean 線は送らない**」(便 114)以降**停止中・再開は研究者判断**。**回収状況確定(908④)**: luna_task 111d まで回収済・宙吊り納品なし・lean.yml green(run 31066606722)。未完車線 = T2 型契約/T1_cyclotomic_ram2 の Mathlib 定理化/full PreGalois/FiberFunctor/universe 一般化/LE 後半/接基点・TB3・TB4・EXSEQ 接続 | **800**(帯)→ **908④** | 114 → 119 | 2026-08-11→12 | LEDGER 裁定 800/908 |
| (n=3 有限層・参考) | K3 Lean Phase 1/2+F29+忠実性監査 = **verified(記載定理の範囲)** | W3-14/14b/14c/14d | 33 帯 | 2026-07-27 | `lean/K3/`・CLAIMS W3-14 系 |

---

## 11. 見つからなかった項目(正直申告 — 見つからないものを閉じたことにしない)

1. **P1 論文原稿の単一ファイル**: repo 内に不在(`.tex` ゼロ・paper/ ディレクトリなし・§9 のとおり)。ただしこれは「記録喪失」ではなく**裁定 536 により Lean 完了後着工と定められた未着工**が正 — 「原稿がどこかにあるはず」という前提での再捜索は不要。
2. **裁定 107 の本文**(CLAIMS W3-24 が「C1(裁定 107)」として引く番号): LEDGER に見出し・本文とも発見できず(2026-07-28 帯は記帳様式が粗い時期)。**C1 を「閉」と記帳する根拠としては記録所在不明** — 現に裁定 912(2026-08-12)は C1 を open 前件として扱い状態調査を数学者へ回付中。本索引も C1 = open 扱い(§6.1)。
3. **C1・C3(c2c4 札・K9 前件)の閉鎖裁定**: 存在しない(open が正・裁定 912 で調査回付中)。「P1 は全文完結」との関係 = これらは **FAM-U-ASM 発効(族水準)には影響しない n=9 個別測定の前件**(裁定 904/908 の区別: 文献基準 vs 工房基準)。
4. **始点算術(E1-GAP-5/6)の閉鎖裁定**: 存在しない(candidate 残余として発効に明示継承 = F106-1.1 erratum・裁定 559/908)。閉扱いは禁止(発効が「意味しない 3 項」)。
5. **K⁽³⁾ Z₁₂-link / A₅ Z₁₀-link の pending 解消記録**: 発見できず — W3-20 inventory の pending のまま。ただし**保存欄扱いで FAM-U-ASM の残件ではない**(追記 C §C.1.1・F105-7・`p1_ratification_bundle_v1.md` §2.4)。
6. **(S3) 族版の「無条件族定理」としての閉鎖裁定**: 存在しない — 最終形は条件付き形の発効(裁定 490・F102-5.1/5.2)+FAM-U-ASM への内包(裁定 550/559)。無条件形として引用しない。
7. **裁定 908 の段表記「546 系/565 系」に一致する条件付き PASS/発効宣言の本文**: 裁定 546/565 自体は別議題(Sol 側実装原則/便 106 全節検収)。実体は裁定 547/550/559(§1 の転記注記)— 番号でなく便 105/106 サイクルを指す表記と読める(判定はしない・両表記を並置保存)。

---

*本索引は記録の転記であり、格・判定を新設しない。各行の正本ファイルと裁定番号が一次資料である。訂正は additive erratum 方式(本文不改変・追補で上書き)。*

---

## 補遺 v1.1(裁定 916・司令塔追記・修正明記)

本索引 §5「C1/C3 = open」と §11-2/3 は**誤り**。判定基準を「LEDGER 内の閉鎖裁定本文」に限定したため、**文書正本と CLAIMS が携行する閉鎖記録**を見落とした:

- **C1(n=3 窓同定)= 完全閉鎖**。正本 = `docs/notes/E1_gt_odd_dih_canonical_v1.md` §522 表「C1(n=3 の窓同定)| 完全閉鎖(機械同定+族的機構 W-REL)| 裁定 107(CLOSED_MATCH)・裁定 174」+ L382(類 (2,[1])・cert = c1_class_check_20260728.json・裁定 174 = transport 予言 I24-P1 的中)。裁定 107 の台帳本文は現行 LEDGER.md に不在(早期台帳のアーカイブ探索は別途)— ただし閉鎖の効力は**正本 E1 内 2 箇所(§522 表・L382)+cert 1 本**で確立(独立性の担い手は cert・falsifier 指摘で精密化)。
- **C3 = T63-P1 鎖内で処理**。正本 = `provenance/CLAIMS.md` **W3-24**(2026-07-28・paper-proof candidate・**Sol 検分済 便 76 F3.2**): 「T63-P1/prediction = 数学的に閉鎖: C1(裁定 107)+named framework 前件の下で **P_{9,3}=TRUE・ord(a₉)=9**(FULL_p_DEPTH)。導出鎖 = (6.3-cls)(G3=便75 F3.2)+W1-fam+(W2)-fam 両側+C4-T+res(a₃)=[−1/4]₆ 非自明性。u₉ 非接触・凍結予言 82ca6b7 の紙上確定。measurement receipt は別線・未着(P8-value は前件でない)。Lean verified ではない」。
- **帰結(裁定 916)**: RECON(d₉=ord(a₉)・裁定 912)との合成で **d₉=9 = Conj 5.1@n=9 は工房内 candidate 完結**(framework-conditional・Lean 未)。R2 の実測 = T63-P1 への**独立 measurement receipt(P8-value 線)**が正しい定義。
- 教訓(索引作成規律へ): 閉鎖根拠は LEDGER 本文に限定しない — **文書正本(E1 等)・CLAIMS・便カプセル・cert の 4 系統を等価の閉鎖記録として検査する**。

# 主張の台帳 (Claims Ledger)

研究的結論を「主張+証拠+状態」で記録する。**未検証の主張は載せない**(candidate 以上のみ)。追記のみ。

状態語彙(2026-07-18 改定: **「検証(verified)」は Lean に予約** — ユーザー指示):
- **candidate** — 単系統の出力(GAP のみ・読解ノートのみ・外部モデルの主張のみ)
- **cross-checked(照合済み)** — 探索器と独立照合器(helper 非共有の二系統)の一致、較正ゲート通過済みの機構による
- **verified(検証済み)** — Lean 証明書(decide/native_decide+公理監査)まで到達
- **UNKNOWN** — 探索したが判定に至らず(範囲を明記)。一級の結果
- **refuted** — 反証済み(反例・証明書つき)

---

## 台帳

| # | 主張 | 証拠 | 状態 | 日付 |
|---|---|---|---|---|
| C-1 | K⁽ⁿ⁾ の数値事実: \|Gₙ\| = 4n³(奇)/4(n/2)³(偶)・K_ord = lcm(n,2)(n=3..16, 18, 36) | GAP+照合器の独立再計算・**fail-closed gate 強制済み**(global verdict numeric 16/16・2026-07-19) | **cross-checked** | 2026-07-19 |
| C-1b | doubling K⁽ⁿ⁾=K⁽²ⁿ⁾(n=3,5,7,9,11,13,15) | GAP+**node 独立検査 7/7 PASS**(global verdict・補助 target 22/26/30 は一時構成と明記) | **cross-checked**(再昇格) | 2026-07-19 |
| C-2 | Prop 3.5 の包含 ⟺ marked factor map(全 256 順序対・不成立 212 対の collision 検出込み)+N₅ の完全列挙(counts 5/5/4/4)・T(c)=c^{2m+1} 直接比較 | GAP+**node 独立実装**(Cayley collision sweep 256/256・mismatch 0・3.5 秒/ N₅ は node 自前全列挙)— 便 02 条件 1・2・5 の閉鎖 | **cross-checked**(再昇格) | 2026-07-19 |
| C-3 | N₅(可換 control)では raw hexagon (3.3)(3.4) が全 m ∈ {0..4} で成立し、m=2 を除外するのは単元条件・全射性のみ | WP1 §3 の表+WP2 照合器の item 2(N₅ 全 shadow hexagon PASS)※m=2 側の「hexagon は通る」は GAP 単系統のまま | candidate(m=2 の観測部分)/ 本体は C-2 に吸収 | 2026-07-18 |
| C-4 | **GT(K⁽ⁿ⁾) の完全列挙が Thm 4.3 の閉じた式と集合一致**(n = 3..16, 18, 36)。付随して: kernel 証明書 (4.11) 全 shadow・合成表 = (3.53)+(4.19)(4.20)・逆射 (3.54) 往復・reduction 5 対(全射)・LS witness (5.1)(3\|n 全対象・m≡2,3 mod 6 含む) | 証明書 17 通(gtsh-cert/v1・ハッシュは cert-hashes-wp2.txt)× 照合器全項目 PASS(verdicts/)。両系統 helper 非共有・司令塔双方コードレビュー済み | **cross-checked** | 2026-07-18 |
| C-5 | 較正スイート v2: **便 02 の条件 5 件をすべて閉鎖**(fail-closed 化・N₅ counts 訂正と node 全列挙・256 対 sweep・K36→K12→K4 三角形 216/216・ϱ 明示同型と非可換 witness・代表元不変性)— 全 verdict 18/18 all_pass | LEDGER の Luna 便 02/02b・最終統合記録(2026-07-19)・verdicts/ | cross-checked(**宣言は Sol 便 03 検収+研究者検分待ち**) | 2026-07-19 |

## Week 3 台帳(Dih 外・既知正解表とは別テーブル / 三値: genuine・fake・UNKNOWN)

| # | 対象 | 全列挙 | kernel | survival(reduction) | 三値判定 | 状態 | 日付 |
|---|---|---|---|---|---|---|---|
| W3-1 | L = K⁽³⁾∩N₀(\|PB₃:L\| = 2916・L∉Dih は設計 §1 の Sylow 論証・Sol 便 04 監査予定) | \|GT(L)\| = **36**(raw 324 → hex 36 → charm 36 → surj 36) | brute 36/36 PASS(正則作用 O(N) 法・510ms・論拠は便 04 監査対象) | **R_{L,K⁽³⁾} 全射**(12/12 被覆・各繊維一様 3・照合器が独立再計算で追認) | **UNKNOWN**(指定した一細分 L では R_{L,K⁽³⁾} が全射・12/12 survive。**この細分からの fake witness はなし**。genuine は未主張 — 便 04 F3 の確定文言) | **cross-checked**(L01 verdict 全項目 PASS・2026-07-25) | 2026-07-25 |
| W3-1b | 構造命題(候補): 36 = 12×3 は Heisenberg 中心 ⟨Z⟩ ≅ C₃ の torsor — ker R_{L,K⁽³⁾} = {[0,(1,Zᵃ)]} ≅ C₃・全 36 shadow settled(成分別自己同型) | Sol 便 04 F4 のスケッチ+司令塔の中心計算検算。**紙上証明(P17)は司令塔起草中 → Sol 便 05 監査へ** | candidate | 2026-07-25 |
| W3-2 | M₅ = K⁽³⁾∩N₅(c が位数 5 で生きる Dih 外細分・fixture 5/5 事前登録一致) | \|GT(M₅)\| = **48**(母集合 432 → hex 48 → charm 48 → surj 48)。**c^m 項込みの full hexagon 48/48**(中心項機構の本番初通過) | brute 48/48(照合器・改善 4 点適用版) | **R_{M₅,K⁽³⁾} 全射**(12/12・繊維一様 4・照合器独立再計算で追認) | **UNKNOWN**(指定した一細分 M₅ では R 全射・12/12 survive。この細分からの fake witness なし。genuine 未主張) | **cross-checked**(M01 verdict 全項目 PASS) | 2026-07-25 |
| W3-2b | 観測(候補): 繊維 4 = m 方向の持ち上げ(mod 30 の単元が mod 6 の各類に 4 個)— ker R_{M₅,K⁽³⁾} は u = 13 が生成する C₄(u ∈ {1,13,37,49} mod 60)。**L(f 方向・中心 torsor)と対をなす「円分方向の torsor」** | 司令塔導出(u の冪の mod 60 計算)。Sol 便 05 の監査・一般化候補へ | candidate | 2026-07-25 |
| W3-3 | **較正バッテリー 7 段 完走**(manifest v1・blind 運用): 観測 \|GT\| = N_Q **4**・M_Q **24**(直積公式 48 の破れを実測確認)・N₂ **4**・N₃ **8**(R 全射繊維 2 — 定理 H9 の較正一致・P40 前件不成立)・M₃ **48**(R→K³ 12/12・R→N₃ 8/8 全射)。**どの段からも fake witness なし**。staged counts 排他・E_m 独立出力・U-F 全 fixture PASS(U-F7 は定義式追給後 PASS) | GAP 探索器(battery-*.g)× 独立照合器 check-v2.mjs・verdicts 7/7 all_pass・convention_robust 欄で規約頑健性を明示(1b は非頑健と正直記帳)・GAP 合計 <10 秒 | **cross-checked** | 2026-07-26 |
| W3-3b | **A₅ の窓の発見値**: \|GT(N_A)\| = **20**(240 → h10 176 → h11 44 → gen 0)— 紙上 UNKNOWN だった総数の初実測。**A2 = M_{A,5} も 20 で、R₆ は集合全単射 20/20 — 補題 A2A1 の予言が観測レベルで成立**(語レベル評価・c 生存・A2 の staged counts も A1 と完全一致)。繊維構造(なぜ 20 = 4×5 か)の説明は未起草 — 数学者への次の問い | 二系統一致(A1/A2 verdict all_pass)。補題 A2A1 は便 07 監査済(紙上) | **cross-checked**(構造説明は candidate 未満・未起草) | 2026-07-26 |
| W3-4 | 境界定理群の状態: H5・H6・H7(補筆済)・H8(狭形 = (H-b′) 単独可解)・H9・T2 本体・E1・E2′・補題 A2A1・G1/G2′/G3(比較写像)= **紙上相互監査 PASS**(便 06/07)。H8″「2 群安全」・H7′ は**撤回済み**。H6/H9/A2A1 は W3-3/3b の実測とも整合 | sol_reply_06/07+裁定 06/07。Lean 初弾候補: T2(iii)・E1・A5-Q(P87) | candidate(紙上相互監査 PASS — verified は Lean 到達まで名乗らない) | 2026-07-26 |
| W3-6 | **PSL 7 窓の審判: 封印予測 7/7 完全一致**(blind 実装・二系統): S1〜S7 観測 \|GT\| = 42/32/42/54/110/40/48 = 封印値(SHA-256 一致を開封で確認・provenance/seals/)。**case A は settled 100%・case B は settled ちょうど半分**(16/32・20/40・24/48)— **atlas 初の非 isolated 対象を観測**・「settled ⟺ u ≡ ±1 (mod 2k)」定理の実測整合。命題 S は split-inner で成立(A₅ 込み 5 窓)・case B で破れ(3 窓)を実測確認。統一定理候補 \|GTSh\| = \|N_Aut(⟨w⟩)\|(A: Hol(ℤ/k)・B: D₄ₖ)と全観測が整合 | 証明書 S1..S7.v2 × check-psl.mjs(第二系統 = GF(q) 行列直接構成・指標表不参照・P115 遵守)all_pass 7/7・封印 PSL_v1 開封(ハッシュ一致) | **cross-checked**(統一定理の紙上部は便 11 監査へ) | 2026-07-26 |
| W3-5 | **プロジェクト初の verified**: A₅ marking の恒等式 s∘X∘s⁻¹ = Y(s = (1 4)(3 5)・X = (1 3 2 4 5)・Y = (1 3 4 5 2)・Fin 5 上の関数等式)— 範囲はこの単一恒等式のみ(A-F1 fixture の一成分) | Lean 4.32.1 `Marking.marking_identity`(lean/Marking.lean・decide・**公理 propext のみ・sorry なし**)+GitHub Actions CI green(commit 054db1b)。Lean 工場: plain Lean 4・ローカル RSS 255MB | **verified** | 2026-07-26 |

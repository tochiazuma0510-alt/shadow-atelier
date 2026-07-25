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

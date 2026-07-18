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
| C-1 | K⁽ⁿ⁾ の数値事実: \|Gₙ\| = 4n³(奇)/4(n/2)³(偶)・K_ord = lcm(n,2)(n=3..16) | GAP+照合器の独立再計算が一致(※verdict の gate 強制は仕様 A 適用待ち — 便 02 F8) | **cross-checked**(gate 強制は保留) | 2026-07-18 |
| C-1b | doubling K⁽ⁿ⁾=K⁽²ⁿ⁾(n=3,5,7,9,11,13,15) | GAP のみ(`suite-wp1.g`)— **便 02 F8 により candidate へ差し戻し**。node 実装(仕様 C-2)後に再昇格 | candidate | 2026-07-18 |
| C-2 | Prop 3.5 の包含 ⟺ marked factor map(全 256 順序対)+N₅ の完全列挙(counts 段階別)・T(c)=c^{2m+1} | GAP のみ — **便 02 F7/F8 により candidate へ差し戻し**(N₅ は探索器の counts 混同バグも判明: 正は raw=5, hex=5, charm=4, surj=4)。node 実装(仕様 B/C)後に再昇格 | candidate | 2026-07-18 |
| C-3 | N₅(可換 control)では raw hexagon (3.3)(3.4) が全 m ∈ {0..4} で成立し、m=2 を除外するのは単元条件・全射性のみ | WP1 §3 の表+WP2 照合器の item 2(N₅ 全 shadow hexagon PASS)※m=2 側の「hexagon は通る」は GAP 単系統のまま | candidate(m=2 の観測部分)/ 本体は C-2 に吸収 | 2026-07-18 |
| C-4 | **GT(K⁽ⁿ⁾) の完全列挙が Thm 4.3 の閉じた式と集合一致**(n = 3..16, 18, 36)。付随して: kernel 証明書 (4.11) 全 shadow・合成表 = (3.53)+(4.19)(4.20)・逆射 (3.54) 往復・reduction 5 対(全射)・LS witness (5.1)(3\|n 全対象・m≡2,3 mod 6 含む) | 証明書 17 通(gtsh-cert/v1・ハッシュは cert-hashes-wp2.txt)× 照合器全項目 PASS(verdicts/)。両系統 helper 非共有・司令塔双方コードレビュー済み | **cross-checked** | 2026-07-18 |
| C-5 | 較正スイート v2(8 項目)は残ギャップ 2 点((5.3) 合成鎖・Thm 4.6 明示同型の独立検査)を除き充足 — 「定義+既知例の再現」の宣言可否は Sol 便 02 の監査と研究者の検分へ | LEDGER の WP2 統合記録 | candidate(宣言は保留中) | 2026-07-18 |

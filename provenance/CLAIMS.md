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
| C-1 | K⁽ⁿ⁾(n=3..12)で \|Gₙ\| = 4n³(奇)/4(n/2)³(偶)、K_ord = lcm(n,2)、K⁽ⁿ⁾=K⁽²ⁿ⁾(n=3,5,7,9,11) | `search/week1-kn-spotcheck.g`(GAP)+論文公式(2405 §3)との一致。※独立照合器は未通過(較正スイート v2 の項目 1 で cross-checked へ昇格予定) | candidate | 2026-07-18 |
| C-2 | 宇宙 {3..16,18,36} で C-1 の数値事実+doubling(13,15)+**Prop 3.5 の包含が全 256 順序対で marked factor map と一致**+N₅ control(GT(N₅) = {0,1,3,4}・T(c)=c^{2m+1}) | `search/suite-wp1.g` WP1 ALL PASSED(GAP・司令塔再実行で再現)。LEDGER の WP1 実行記録参照 | candidate | 2026-07-18 |
| C-3 | N₅(可換 control)では raw hexagon (3.3)(3.4) が全 m ∈ {0..4} で成立し、m=2 を除外するのは単元条件・全射性のみ | 同上 WP1 §3 の表(hex 列すべて PASS) | candidate | 2026-07-18 |

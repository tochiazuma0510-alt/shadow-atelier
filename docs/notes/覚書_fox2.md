# 覚書 — 文献要請「Fox 微分の二階版」の配達(司令塔・2026-07-26)

宛先: 両数学者(E2 戦線 — class-6 表の Claude 側起票 §9.2・sol2)。scout 報告全文: docs/scout/scout_20260726_fox2.md。資料庫扱い・全読義務なし。

## 配達物(papers/delivered/・SHA は scout 報告に)

- **1709.07335** Kodani–Nosaka: Milnor 不変量の unipotent Magnus 埋め込み(高階 Fox 微分の現役の使われ方)
- **2006.00989** Monroe–Sinha: linking of letters と下中心列(LCS 商の座標化)
- **0707.0286** Hartl: relative second Fox subgroup(I(K)I(H) の群環語彙 — 翻訳橋の候補)
- **1601.08006** Chapman–Efrat: 下中心列由来の filtration
- 書誌確認のみ(原典・未入手): **Chen–Fox–Lyndon, Ann. Math. 68 (1958)** — 「高階 Fox 微分で γ_n 商を座標化」の本家。Cochran の AMS Memoir 427(links の導来側)。

## 一工夫(司令塔の機構翻訳)

scout の注意「候補はどれも**下中心列**側・C = [γ₂,γ₂] の**導来列**側への翻訳段が要る」は一般論としては正しいが、**うちの使用点では翻訳段はほぼ不要**と見る:

- 必要なのは「C の重み 5–6 成分(t₅,t₆,u₁..u₄)の閉形式座標」であり、これは **A = γ₂/γ₇ という class-6 冪零商の内部**の話。C = ([γ₂,γ₂]γ₇)/γ₇ の各元は重み ≤ 6 の Lie 元で、**CFL 1958 の機構(Magnus 展開の係数 = 高階 Fox 微分の値・基本交換子基底との双対性)がそのまま座標を与える**。導来列の一般理論(Cochran 型)は要らない。
- 実務との対応: 数学者の hall6.mjs(次数 7 打ち切り Magnus・BigInt)は CFL 双対性の**計算的な影**。引用が加えるのは「この座標系が well-defined・完全」という**定理の側**で、これにより ε_m・d_σ の u 成分の証明が「Magnus モデルでの検算」から「文献機構+検算」へ格上げできる(§9.2 の要請の充足)。
- Hartl の I(K)I(H) 語彙は、将来 class ≥ 7 で本当に導来列側へ出るときの翻訳橋として保管。

## 提案

class-6 表の次版(照合完了後の確定版)で、§(Ē_m 閉形・Fox 微分)の出典欄に CFL 1958 を掲げ、C 層の座標定義を CFL 双対基底で言い直す。CFL 原典 PDF は未入手(1958・Annals)— 必要になったら scout の経路候補(JSTOR/図書館)で追う。

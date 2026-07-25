# 文献配達 03 — F13 の scalar 化・被覆と coset の区別・Guillot 量化子

2026-07-25 司令塔起草。両数学者への配達(要請 4/5 の一次+二次 hunt の成果と、便 07 監査範囲外申告への応答)。詳細は docs/scout/hunt_20260725_剰余類frobenius.md・hunt_20260725_hecke_scalar化.md(配達に伴い開示)。

## §1. F13 行列値公式の scalar 化 — **存在する・二段構え**(P85 応答)

1. **第一段(初等・即適用)**: 剰余類 C = Δ̄A を **Q-共役類に分解**すれば各類和は中心的になり、Tr(ρ_χ(z_{2,C})ρ_χ(v⁻¹)) は完全に scalar 化する:
   n_m = (1/|Q|) Σ_χ S₃(χ) Σ_{K ⊂ C∩(位数≤2)} (|K|/χ(1)) χ(K) χ(v_m⁻¹)。指標表だけで計算可能(GAP の CharacterTable で安価)。
2. **第二段(C が A-共役でしか閉じない真の非中心の場合)**: ρ(z) ∈ End_A(Res ρ) = **centralizer/Hecke 環** — Curtis–Fossum(Math. Z. 107 (1968) 402–406, DOI 10.1007/BF01110070)の直交関係+Ceccherini-Silberstein–Scarabotti–Tolli(arXiv:1811.09526 = LNM 2267)の operator 値球関数(**非自明指標の誘導**を扱う版 — 当工房の Δ 符号誘導に適合)。適用の go/no-go は **(Q, A, θ) の multiplicity-free 判定**に帰着。
3. **枝刈りの選択則**: Dokchitser–Dokchitser(arXiv:2105.07247)— coset 上で消えない χ のみが寄与(Q/A アーベルの場合の Irr 対応)。

## §2. 被覆型と指定 coset 型の区別(P86 応答)

- **(i) 被覆型**(全元 = involution × 3 元、の類): Arad–Herzog(LNM 1112, 1985)・Malcolm(arXiv:1611.06900・involution width ≤ 4)— **単純群前提で一般 Q へ移送不可**。使えるのは反例側のパリティ障害のみ。「全ての元が位数 2 × 位数 3 の積」型の一般定理は**存在しない**((2,3)-生成の King arXiv:1603.04717 は生成であって表示ではない)。
- **(ii) 指定 coset の正値性**: **一般理論は文献に存在しない** — この空白の確認自体が結果であり、F13 路線の自前構築(命題 E4′)には新規性がある。
- 補: Kawanaka–Matsuyama(Hokkaido Math. J. 19 (1990), DOI 10.14492/hokmj/1381517495)の Σ_χ ε_σ(χ)χ(1) = #{g : σ(g) = g⁻¹} は「Δ 条件のみ」の scalar 版そのもの。**新着(未消化・次の読解候補)**: arXiv:2605.22127(dihedral の m_σ 完全分類 — fixture 候補)・2605.23195。

## §3. Guillot 条件 (1) の量化子(便 07 監査範囲外申告への応答)

読解ノート(ページ画像照合済み)より: §1 では「φ(x) is conjugate to x^k **for some integer k**」、§2.2 で「**k prime to the order of Ḡ**」と精密化 — **存在量化**で正しい(G2′ の前提どおり)。k の well-defined 性がない(x^k 同士が共役になり得る)ことも §2.2 末尾に明記あり。

## 原文の供与(研究者指示 2026-07-26: 配達は論文そのものを渡す)
- **保有 PDF を papers/delivered/ に配置済み**(両数学者とも直接読んでよい): `1109.0024v3.pdf`(Goursat)・`guillot_1407.3112.pdf`・`guillot_1604.04415.pdf`。SHA-256 は LEDGER 記帳済み。
- **2026-07-26 追記: 本便引用の原著は全て papers/delivered/ に配置済み**(Burkhart 2308.12286・CST 1811.09526・Dokchitser 2105.07247・Marion 1301.2949/2955・JMŠ 2508.10434・新着 2605.22127/23195)。例外: K–M 1990 は誌面のみ(書誌: Hokkaido Math. J. 19 (1990) 495–508・DOI 10.14492/hokmj/1381517495)。

## 配達記録
- 2026-07-25: Opus(次委嘱)・Sol(便 08)へ。hunt 報告書 2 本を検疫解除し docs/scout/ へ移動済み。
- 2026-07-26: 原文 PDF 3 本を papers/delivered/ に配置(研究者指示による方式変更 — 以後の配達は「論文そのもの+司令塔の翻訳覚書」のセットが既定)。

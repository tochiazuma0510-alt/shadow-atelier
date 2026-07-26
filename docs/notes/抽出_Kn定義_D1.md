# 抽出_Kn定義_D1 — arXiv 2405.11725 の K⁽ⁿ⁾ 定義系(【GAP-D1】主攻③実装前提)

> 発注: 司令塔【GAP-D1】(2026-07-26)。担当: reader。
> **頁画像照合済みの印**: pp. 9, 10, 11, 13, 14, 15, 16, 17, 18, 25, 26, 27 を pdftocairo 150dpi で画像化し、以下の全ての式・言明を原文照合した。grep(papers/txt)はページ特定と 0 件確認のみに使用。
> 対象 PDF: `C:\Users\81905\Desktop\shadow-atelier\papers\2405.11725-nonabelian-quotients-gt-elementary.pdf`
> 既存ノート: `docs/notes/2405.11725-抽出ノート_v1.md`(本ノートは D1 発注分の逐語精密版。矛盾は検出されず)。

---

## 1. K⁽ⁿ⁾ の定義(§3, p.13)【画像照合済】

前提記法(§1.7, p.9)【画像照合済】:

- x₁₂ := σ₁², x₂₃ := σ₂², c := (σ₁σ₂σ₁)²(PB₃ の生成元; c は 𝒵(B₃) = 𝒵(PB₃) = ⟨c⟩ ≅ ℤ の生成元)。
- PB₃ ≅ ⟨x₁₂, x₂₃⟩ × ⟨c⟩、F₂ = ⟨x₁₂, x₂₃⟩ ≤ PB₃ と暗黙同一視。
- x := x₁₂, y := x₂₃, **z := y⁻¹x⁻¹**(p.9 の逐語: "z := y⁻¹x⁻¹"; つまり z = (x₁₂x₂₃)⁻¹)。

§3 冒頭(p.13)逐語:

> Let n ∈ ℤ≥₃ and **Dₙ := ⟨ r, s | rⁿ, s², srs⁻¹r ⟩**. We start with the group homomorphism ψₙ : PB₃ → Dₙ³ defined by the formulas:
>
> **ψₙ(x₁₂) := (r, s, s), ψₙ(x₂₃) := (rs, r, rs), ψₙ(c) := (1, 1, 1).  (3.1)**
>
> We set **K⁽ⁿ⁾ := ker(ψₙ)** and claim that
>
> **Proposition 3.1** For every n ∈ ℤ≥₃, K⁽ⁿ⁾ belongs to the poset NFI_{PB₃}(B₃).

- Prop 3.1 の証明(pp.13–14): φ: PB₃ → Dₙ, φ(x₁₂):=s, φ(x₂₃):=rs, φ(c):=1 とおき、K⁽ⁿ⁾ = Core_{B₃}(ker φ)。中間式 (3.2)(3.3)、ψ̃ := φ^{σ₂⁻¹} × φ^{σ₁⁻¹} × φ で ψ̃(x₁₂)=(r⁻¹,s,s), ψ̃(x₂₃)=(rs,r,rs), ψ̃(c)=(1,1,1)、内部自己同型 j(g₁,g₂,g₃):=(rs·g₁·(rs)⁻¹, g₂, g₃) により ψₙ = j∘ψ̃、K⁽ⁿ⁾ = ker(ψ̃) = C(p.14)【画像照合済】。
- **Dih := {K⁽ⁿ⁾ | n ∈ ℤ≥₃}**(dihedral poset; p.14, 無番号表示)。

## 2. 商と marking(§3–§4)

- **Remark 3.2**(p.14)逐語【画像照合済】: "For every n ∈ ℤ≥₃, K_{F₂}⁽ⁿ⁾ is the kernel of the homomorphism F₂ → Dₙ³ that sends **x to (r,s,s) and y to (rs,r,rs)**. Moreover, **K_ord⁽ⁿ⁾ = lcm(n, 2). (3.4)**"
- 同一視(p.14, 無番号表示)【画像照合済】: "It is convenient to identify F₂/K_{F₂}⁽ⁿ⁾ with the subgroup **Gₙ := ⟨ (r,s,s), (rs,r,rs) ⟩ ≤ Dₙ³**." — w ∈ F₂ に対し w̄ := w K_{F₂}⁽ⁿ⁾。
- **marking (3.6)**(p.14)逐語: **x̄ = (r, s, s), ȳ = (rs, r, rs), z̄ = (r²s, r⁻¹s, r).  (3.6)**
- PB₃/K⁽ⁿ⁾ ≅ F₂/K_{F₂}⁽ⁿ⁾(≅ Gₙ): Lemma 4.2 の証明冒頭(p.17)逐語【画像照合済】 "Since ψₙ(c) = (1,1,1), we have PB₃/K⁽ⁿ⁾ ≅ F₂/K_{F₂}⁽ⁿ⁾."
- **位数(パスポート型)**: 論文は個別の ord(x̄) 等を明記しない(明記は (3.4) の K_ord = lcm(n,2) のみ)。**導出値**: ord(r)=n, 反転元 s, rs, r²s, r⁻¹s は位数 2 だから ord(x̄) = ord(ȳ) = ord(z̄) = **lcm(n, 2)**(成分ごとの位数の lcm; (3.4) と整合)。ord(c̄) = 1((3.1) より)。すなわちパスポート型は (lcm(n,2), lcm(n,2), lcm(n,2))【導出・根拠 (3.1)(3.6)(3.4)】。
- **偶奇の場合分け**(p.15)【画像照合済】:
  - x̄² = (r², 1, 1), ȳ² = (1, r², 1), z̄² = (1, 1, r²)(無番号)。J_q := ⟨r²⟩×⟨r²⟩×⟨r²⟩ ≤ G_q、|J_q| = q³(q 奇)/(q/2)³(q 偶)。G_q/J_q ≅ ℤ/2ℤ×ℤ/2ℤ(コセット {J_q, x̄J_q, ȳJ_q, x̄ȳJ_q})。
  - **|PB₃ : K⁽q⁾| = |F₂ : K_{F₂}⁽q⁾| = 4|J_q| = 4q³(q 奇)/ 4(q/2)³(q 偶)**(無番号表示)。
  - **Proposition 3.4**(p.14)逐語: "For every odd integer n ≥ 3, we have K⁽ⁿ⁾ = K⁽²ⁿ⁾."
  - **Proposition 3.5**(p.15)逐語: "Let n, q ≥ 3. Then **K⁽q⁾ ⊂ K⁽ⁿ⁾ ⟺ n | lcm(q, 2)**."(η_{q,n}: D_q → Dₙ, a↦r, b↦s は (3.5), Remark 3.3, p.14)
  - **Proposition 3.6**(p.15): [Gₙ, Gₙ] = {(r^{2n₁}, r^{2n₂}, r^{2n₃}) | (n₁,n₂,n₃) ∈ (2ℤ)³ or (2ℤ+1)³} (3.7)(証明 Appendix A)。**Remark 3.7**(p.15): n₁,n₂,n₃ は mod ord(r²) で考える; 偶奇制約が意味を持つのは **4 | n のときのみ**。4∤n(n ∈ 4ℤ+2 or n 奇)なら [Gₙ,Gₙ] = ⟨r²⟩×⟨r²⟩×⟨r²⟩ (3.8)。

## 3. N_ord の定義と n との関係

- **定義**(§1.7, p.10, 無番号表示)逐語【画像照合済】: "For N ∈ NFI_{PB₃}(B₃) we set
  **N_ord := lcm(ord(x₁₂N), ord(x₂₃N), ord(cN)), N_{F₂} := N ∩ F₂.**"
  (§2 冒頭 p.11 でも同文再掲【画像照合済】。p.10: "the positive integer N_ord depends on the choice of N" の注意あり。K_ord⁽ⁿ⁾ = 「PB₃/K⁽ⁿ⁾ における x₁₂, x₂₃, c のコセットの位数の lcm」と p.10 で明言。)
- **charming 条件**(Definition 2.1, p.11)逐語【画像照合済】: GT-pair (m + N_ord ℤ, f N_{F₂}) ∈ ℤ/N_ord ℤ × F₂/N_{F₂} が hexagon 関係 (2.1)(2.2) mod N を満たし、さらに
  **gcd(2m + 1, N_ord) = 1 and f N_{F₂} ∈ [F₂/N_{F₂}, F₂/N_{F₂}]**
  のとき charming(GT♡_pr(N))。
  - hexagon (2.1): σ₁^{2m+1} f⁻¹ σ₂^{2m+1} f N = f⁻¹ σ₁σ₂ x₁₂^{−m} c^m N
  - hexagon (2.2): f⁻¹ σ₂^{2m+1} f σ₁^{2m+1} N = σ₂σ₁ x₂₃^{−m} c^m f N
  - 簡約形(Prop 2.2, p.11; (m,f) ∈ ℤ×[F₂,F₂]): fθ(f) ∈ N_{F₂} (2.3), τ²(yᵐf)τ(yᵐf)yᵐf ∈ N_{F₂} (2.4)。
- **n との関係**: **K_ord⁽ⁿ⁾ = lcm(n, 2)**((3.4), p.14)。すなわち = 2n(n 奇)/ n(n 偶)【自明な書換え】。よって K⁽ⁿ⁾ での charming の法は gcd(2m+1, lcm(n,2)) = 1。

## 4. Theorem 4.3 — GT(K⁽ⁿ⁾) の明示式(p.18)【画像照合済】

逐語:

> **Theorem 4.3** For every n ≥ 3, the set of GT-shadows with the target K⁽ⁿ⁾ is
>
> GT(K⁽ⁿ⁾) = { (m, (r^{2k}, r^{−2k}, r^{κ(m)})) | m ∈ 𝒳ₙ, k ∈ ℤ, k ≡ κ(m)/2 mod 2 }  if 4 | n,
> GT(K⁽ⁿ⁾) = { (m, (r^{2k}, r^{−2k}, r^{κ(m)})) | m ∈ 𝒳ₙ, k ∈ ℤ }  if 4 ∤ n,  (4.12)
>
> where **𝒳ₙ := { m : m ∈ {0, 1, …, K_ord⁽ⁿ⁾ − 1} | gcd(2m + 1, K_ord⁽ⁿ⁾) = 1 }**
> and the function κ is defined in (4.9). Furthermore, **K⁽ⁿ⁾ is an isolated object of the groupoid GTSh**.

- **κ の定義**((4.9), Prop 4.1, p.17)逐語【画像照合済】: **κ(m) := m + 1 (if 2 ∤ m), −m (if 2 | m)**。Prop 4.1 は GT♡_pr(K⁽ⁿ⁾) が (4.12) と同じ集合であることを言明(証明: 奇 m は p.17 直上の計算 "m + 1 ≡ 2t mod ord(r)"、偶 m は読者へ)。Thm 4.3 の証明(p.18): Lemma 4.2 の第 2 言明により GT(K⁽ⁿ⁾) = GT♡_pr(K⁽ⁿ⁾)。
- **パラメータの走る範囲**: m は 𝒳ₙ(mod K_ord⁽ⁿ⁾ = lcm(n,2) の完全代表系のうち gcd 条件を満たすもの)。k ∈ ℤ だが三つ組は r^{2k} で決まるので実効的には **k mod ord(r²)**(ord(r²) = n(n 奇)/ n/2(n 偶)【導出: ord(r) = n】; mod ord(r²) で考えるのが自然という言明は Remark 3.7, p.15)。4 | n のときのみ追加条件 **k ≡ κ(m)/2 mod 2**(この条件の由来は p.17: 4|n での脚注 7 条件 k ≡ t mod 2 ⟺ k ≡ (m+1)/2 mod 2【画像照合済】)。
- **成分の由来**(p.16)【画像照合済】: charming pair は (m, g) ∈ {0,…,K_ord−1} × [Gₙ,Gₙ], gcd(2m+1,K_ord)=1, **gθ(g) = 1 (4.4)**, **τ²(ȳᵐg)τ(ȳᵐg)ȳᵐg = 1 (4.5)** の解集合。(4.4) の解析: θ(z̄) = (s, rs, r⁻¹), θ(z̄²) = z̄⁻² (4.6), θ(r^{2n₁},r^{2n₂},r^{2n₃}) = (r^{2n₂},r^{2n₁},r^{−2n₃}) (4.7), τ(r^{2n₁},r^{2n₂},r^{2n₃}) = (r^{2n₃},r^{2n₁},r^{2n₂}) (4.8)。(4.4) ⟺ n₁ + n₂ ≡ 0 mod ord(r²)。
- **個数公式**: Thm 4.3 自体には個数の言明なし。論文が明記する位数は **|GT(K^{(2^α)})| = 2^{2α−2}**(α ≥ 2; p.27, Thm 5.3 証明第 2 部【画像照合済】: 「GT(K^{(2^α)}) is an index 2 subgroup of ℤ/2^{α−1}ℤ ⋊ (ℤ/2^{α+1}ℤ)^×」、|ℤ/2^{α−1}ℤ ⋊ (ℤ/2^{α+1}ℤ)^×| = 2^{α−1}·φ(2^{α+1}) = 2^{2α−1})および |H̃_α| = 2^{2α−2}((4.24) 参照、p.27 で引用)。一般 n の閉じた個数公式は論文に明示なし — **UNKNOWN(論文明示としては)**。導出値(v1 ノート §4(F)): |GT(K⁽ⁿ⁾)| = 2n₀φ(n₀)(α ∈ {0,1})/ n₀φ(n₀)·2^{2α−2}(α ≥ 2)、根拠は Thm 4.6 (4.23)(4.24)。
- 群構造(参照のみ・本発注範囲外): Prop 4.5 (4.15) ϱ(m,(r^{2k},r^{−2k},r^{κ(m)})) := (k + n₁ℤ, (2m+1) + 2nℤ)(n 偶, n₁ := n/2)、Thm 4.6 (4.23): GT(K⁽ⁿ⁾) ≅ Aff(ℤ/n₀ℤ) × 𝒵₂(α<2)/ Aff(ℤ/n₀ℤ) × H̃_α(α≥2)。

## 5. Theorem 5.3 / Corollary 5.4(pp.25–27)【画像照合済】

**Theorem 5.3**(p.25)逐語:

> **Theorem 5.3** Consider an integer n = 2^α n₀ ≥ 3 with n₀ being odd and let GT_arith(K⁽ⁿ⁾) be the subgroup of arithmetical GT-shadows in GT(K⁽ⁿ⁾) (see (1.12) in Subsection 1.3.1). Then
>
> **|GT_arith(K⁽ⁿ⁾)| ≥ 2φ(n₀)  if α = 0 or α = 1;  2^{2α−2} φ(n₀)  if α ≥ 2.  (5.4)**
>
> In particular for n₀ = 1, the group homomorphism **Ih_{K^{(2^α)}} : G_ℚ → GT(K^{(2^α)}), α ∈ ℤ≥₂ is surjective.**

**Corollary 5.4**(p.27)逐語:

> **Corollary 5.4** For every α ∈ ℤ≥₂, the finite group GT(K^{(2^α)}) is naturally a quotient of G_ℚ and a quotient of ĜT. If α ≥ 3, then the group GT(K^{(2^α)}) is non-abelian.

(直前文 p.27 逐語: "Due to Theorem 5.3, we now have the **first family of non-abelian finite quotients of the original Grothendieck-Teichmueller group ĜT** introduced by V. Drinfeld in [8, Section 4].")

**証明が使う体・拡大**(発注の要確認点):

- **特定の円分体 ℚ(ζ_N) は証明中に一切明記されていない**(pp.25–27 全頁画像で確認)。証明の算術的入力は次の 3 つのみ:
  1. **円分指標 χ: G_ℚ → Ẑ^× の全射性**(p.10 で記号導入【画像照合済】; §1.3 の図式経由で χ_vir,K^{(2n)}: GT_arith → (ℤ/2nℤ)^× の全射性に落ちる。p.26 冒頭逐語: "Combining this observation with the surjectivity of the homomorphism χ_vir,K^{(2n)} (see Subsection 1.3), we conclude that the homomorphism χₙ is also surjective")。§1.3(txt 行 228–229)に「これが χ_vir 全射性の唯一知られた証明法」の趣旨の文あり(頁画像未照合・v1 ノートは Remark 1.3 と記録)。
  2. **複素共役の像**: p.25 逐語 "Since (0̄, 1̄) is the identity element of GT(K⁽ⁿ⁾) and **(0̄, −1̄) is the image of the complex conjugation**, these elements are arithmetical (see Remark 1.10)."(Remark 1.10 = [20, Theorem 1] Lochak–Schneps 由来; txt 行 354)。
  3. **算術の基本定理**(p.26 逐語: "this equality contradicts to the fundamental theorem of arithmetic"; p.27 でも (5.9) の矛盾に使用)+ φ(オイラー関数)の乗法性・(ℤ/2^{α+1}ℤ)^× の構造(p.26–27 のコセット計算 T_ū := χₙ⁻¹(ū) (5.6)–(5.9))。
- 円分体が名指しで登場するのは **§1.6(先行研究レビュー, p.8 付近, txt 行 399–406)の ℚ(µ_{l^∞})(Ihara / Ichimura–Kaneko の文脈)のみ**で、Thm 5.3 の証明には不使用。参考文献 [2](Belyi)[27](Washington, Introduction to cyclotomic fields)の書誌にも cyclotomic の語があるが証明本文にはない。

## 6. 副次: §4 における曲線・dessin・モジュラー言及の有無

- **grep 結果(papers/txt 全文)**: `curve` / `level` / `elliptic` / `covering` — **全文 0 件**。`modular` — 本文 0 件(唯一の出現は参考文献 [28] の題名 "GT-Shadows related to finite quotients of the full modular group")。`dessin` — 本文 0 件(参考文献 [10][11](Guillot)と [16?] Luminy 論集の題名のみ)。`Belyi` — §1 のみ(Ih の単射性の根拠として 2 回, txt 行 45, 203)+ 参考文献 [2]。
- `congruence` は全文 1 件(§4, p.17: "This condition is equivalent to the congruence k ≡ (m+1)/2 mod 2"【画像照合済】)— **整数の合同の意味であり、合同部分群(congruence subgroup)の意味ではない**。
- 結論: **§4(および本文全体)に K⁽ⁿ⁾ の曲線・dessin・モジュラー的解釈への言及は皆無**。T6.2「非合同予測」の傍証データとして: 本論文は K⁽ⁿ⁾ を純群論的(Dₙ³ の核)にのみ扱う。

---

## UNKNOWN / 導出値の明細

| 項目 | 状態 |
|---|---|
| ord(x̄), ord(ȳ), ord(z̄) の個別値 | 論文に明記なし。導出値 = lcm(n,2)(根拠 (3.1)(3.6)) |
| 一般 n の \|GT(K⁽ⁿ⁾)\| 閉形式 | 論文に明示なし(明示は n=2^α の 2^{2α−2}, p.27)。導出は Thm 4.6 経由 |
| §1.3 の「χ_vir 全射性の唯一の証明法」の Remark 番号 | txt では行 228–229(v1 ノート記録は Remark 1.3)。当該頁画像は今回未照合 |
| Thm 5.3 証明で使う体の明記 | **明記なし**が確定結果(pp.25–27 画像照合) |

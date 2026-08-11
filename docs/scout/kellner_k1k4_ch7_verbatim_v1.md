# Kellner K1〜K4 逐語 pin + CH-7 pin 記録 v1

- **委嘱**: 裁定 793 ①(reader 一点読)。pin 仕様の正本 = `docs/notes/phase2_scoring_v1.md` §3.3 KELL-DECIDE(K1〜K4)+ `docs/notes/ideas_counterexample_hunt_v1.md` 札 CH-7。
- **性格**: 逐語抽出(verbatim)のみ。解釈・発効判定は書かない(司令塔専権)。導出は「導出値」と明示。
- 作成: 2026-08-11・精密読解係(reader)。

---

## 0. 書誌・出所・読了申告

| 項目 | 内容 |
|---|---|
| 文献 | Bernd C. Kellner, *On irregular prime power divisors of the Bernoulli numbers*, **arXiv:math/0409223v4** [math.NT] (11 Oct 2005)。出版版 = Math. Comp. **76** (2007), 405–441 |
| PDF 実体 | `papers/kellner-0409223-irregular-prime-power-divisors.pdf`(**本タスクで arXiv から新規取得 2026-08-11**・42 頁) |
| sha256 | `d36c33141d0b8cbc97d26053eda80edd0b479118550c982fd157cb2ac6646507` |
| 取得経緯の注意 | scout 報告 `docs/scout/p2_literature_survey_v1.md` は「全文 42p PDF を直接取得・精読」と記録するが、**papers/ に PDF 実体は保存されていなかった**(glob 全走査で不在)。今回取得分が盤上初の実体。 |
| 頁番号の規約 | 以下の頁番号は **arXiv v4 版の印字頁 = PDF 物理頁**(一致確認済み)。出版版 Math. Comp. の対応頁は **UNKNOWN**(未入手・頁ずれの可能性あり。scout 報告の「p.6/p.31/p.39」も同じ arXiv 版準拠で整合)。 |
| 読了頁申告 | **精読**: pp.1–10(§1・§2・§3 冒頭)/ pp.28–31(§5 末尾・§6 冒頭)/ pp.38–40(付録 A: Table A.1–A.6)。**流し読み**(pin 該当なしの確認のみ): pp.11–27(§3 証明・§4 p 進ゼータ・§5 前半)・pp.32–37(§6 残り・§7・§8)。 |
| 画像照合頁 | pdftocairo 150dpi で **pp. 3, 4, 5, 6, 8, 9, 10, 28, 29, 31, 38, 39, 40** をレンダリングし、以下の全逐語引用を画像で照合済み(pdftotext は補助のみ)。 |

**前提の記法**(§1, p.2 末尾): B̂(n) = Bₙ/n(divided Bernoulli number)。§2 冒頭 Definition 2.1(p.3・画像照合):

> "A pair (p, l) is called an *irregular pair of order n* if pⁿ | B̂(l) where l is even and 2 ≤ l < φ(pⁿ). Define Ψₙ^irr := {(p, l) : pⁿ | B̂(l), p is an odd prime, 2 ≤ l < φ(pⁿ), 2 | l} as the set of irregular pairs of order n. For a prime p the *index* of irregular pairs of order n is defined by iₙ(p) := #{(p, l) : (p, l) ∈ Ψₙ^irr}."

Δ の定義 = Definition 2.3(pp.3–4・両頁画像照合):

> "For (p, l) ∈ Ψₙ^irr, n ≥ 1 define Δ₍p,l₎ ≡ p⁻ⁿ ( B̂(l + φ(pⁿ)) − B̂(l) ) (mod p) with 0 ≤ Δ₍p,l₎ < p. When Δ₍p,l₎ = 0 we call Δ₍p,l₎ *singular*."(p.4 続き: Δ(p) := 1 if Δₚ ≠ 0, 0 if Δₚ = 0, ただし Δₚ = ∏ᵥ₌₁^{i(p)} Δ₍p,l_ν₎。"Then Δ(p) = 1 if and only if all Δ₍p,l_ν₎ are nonsingular.")

---

## K1 ★ — Table A.3 の s₁, s₂ 列の定義(逐語)

### K1-a. 表の列見出し(Table A.3, p.39・画像照合)

列構成は左から: **(p,l) | Δ₍p,l₎ | s₁ | s₂ | s₃ | … | s₁₀**。キャプション逐語:

> "**Table A.3** Calculated irregular pairs of order 10 of primes below 1000."

先頭行の実値(画像照合): (37,32) → Δ=21, s₁=32, s₂=7, s₃=28, s₄=21, s₅=30, s₆=4, s₇=17, s₈=26, s₉=13, s₁₀=32。

### K1-b. (s₁,…,sₙ) の定義 = **Definition 2.11**(§2, p.8・画像照合)

> "**Definition 2.11** Let (p, l) ∈ Ψₙ^irr, n ≥ 1. We write
> (p, s₁, s₂, . . . , sₙ) ∈ Ψ̂ₙ^irr   where   l = Σ_{ν=1}^{n} s_ν φ(p^{ν−1})
> for the *p-adic notation* of (p, l) with 0 ≤ s_ν < p for ν = 1, . . . , n and 2 ≤ s₁ ≤ p − 3, 2 | s₁. The corresponding set is denoted as Ψ̂ₙ^irr, the map corresponding to λₙ is given by
> λ̂ₙ : Ψ̂ₙ₊₁^irr → Ψ̂ₙ^irr,  (p, s₁, s₂, . . . , sₙ, sₙ₊₁) ↦ (p, s₁, s₂, . . . , sₙ).
> The pair (p, l) and the element (p, s₁, s₂, . . . , sₙ) are called *associated*."

### K1-c. 逆向きの一意分解 = **Remark 2.12**(§2, p.8・画像照合)

> "**Remark 2.12** The definition of Ψ̂ₙ^irr means that we have Ψ₁^irr = Ψ̂₁^irr for n = 1. For n ≥ 2 we can define a map Ψₙ^irr → Ψ̂ₙ^irr, (p, l) ↦ (p, s₁, . . . , sₙ) where the s_k are uniquely determined by the p-adic representation
> l = s₁ + (p − 1)ŝ,   ŝ = Σ_{ν=0}^{n−2} s_{ν+2} p^ν,   0 ≤ s_{ν+2} < p
> and by s₁ ≡ l (mod p − 1) with 2 ≤ s₁ ≤ p − 3. If s_k = 0 with k ≥ 2 then there is an irregular pair (p, l_k) of order k with (p, l_k) ∈ Ψ_k^irr and (p, l_k) ∈ Ψ_{k−1}^irr. Note that (p, s₁, s₂, . . . , sₙ) is also called an *irregular pair* with (s₁, s₂, . . . , sₙ) as the second parameter given p-adically."

### K1-d. 列が「唯一の関連対の列」であることの根拠 = **Theorem 3.1**(§3, pp.8–9・両頁画像照合)

> "**Theorem 3.1** Let (p, l₁) ∈ Ψ₁^irr. If Δ₍p,l₁₎ ≠ 0 then for each n > 1 there exists exactly one related irregular pair of order n. There is a unique sequence (lₙ)_{n≥1} resp. (sₙ)_{n≥1} with
> (p, lₙ) ∈ Ψₙ^irr  resp.  (p, s₁, . . . , sₙ) ∈ Ψ̂ₙ^irr
> and l₁ ≤ l₂ ≤ l₃ ≤ . . . ,  lim_{n→∞} lₙ = ∞. Moreover one has Δ₍p,l₁₎ = Δ₍p,l₂₎ = Δ₍p,l₃₎ = . . . . If Δ(p) = 1 then i(p) = i₂(p) = i₃(p) = . . . ."

order-2 対の index 公式 = **Proposition 2.7(3)**(§2, p.5・画像照合。表記: αⱼ ≡ p⁻ⁿ B̂(l + jφ(pⁿ)) (mod p)):

> "(3) If Δ₍p,l₎ ≠ 0, then exactly one related irregular pair of order n + 1 exists. One has (p, l + sφ(pⁿ)) ∈ Ψₙ₊₁^irr with 0 ≤ s < p where s ≡ −α₀ Δ₍p,l₎⁻¹ (mod p)."

### K1-e. 「s₂ 列 = order-2 対の index s」の名指し = **Remark 2.8**(§2, p.6・画像照合)

> "Vandiver [19] describes the result of the previous proposition for the case n = 1 and only for the first irregular primes 37, 59, and 67. For these primes Pollaczek [16] has calculated the indices s of the now called irregular pair of order two, but case p = 67 with s = 2 is incorrect, **see column s₂ of Table A.3**. This error was already noticed by Johnson [10] ..."

### K1-f. s₂ の閉形式と検算式 = **Proposition 5.6**(§5, p.29・画像照合)

> "**Proposition 5.6** Let (p, l) ∈ Ψ₁^irr with Δ₍p,l₎ ≠ 0. Let (p, s₁, s₂) ∈ Ψ̂₂^irr be the related irregular pair of order two with l = s₁. Then Δ₍p,l₎ s₁ s₂ ≡ −p⁻² S_l(p) (mod p)."

証明中(p.29・画像照合): "By Proposition 2.7 we have **s₂ ≡ −p⁻¹ (B_l/l) Δ₍p,l₎⁻¹ (mod p)**." ここで S_n(m) = Σ_{ν=0}^{m−1} νⁿ(§5, p.28)。直前の本文(p.29): "Looking at each line of Table A.3, the product of the first three entries Δ₍p,l₎, s₁, and s₂ are connected with the function Sₙ. Thus, one can easily verify these values."

### K1-g. 導出値(工房側の突合用・論文の式からの直接代入)

Definition 2.11 の式に n = 2 を代入(φ(p⁰) = 1, φ(p¹) = p − 1):

> l₂ = s₁ + s₂ · (p − 1)。すなわち **s₂ = (l₂ − l₁)/(p − 1)** = order-2 対の index の offset(l₁ = s₁ = l)。

根拠 = Def 2.11(K1-b)+ Thm 3.1 の一意性(K1-d)+ Prop 2.7(3) の s(K1-d)。これが KELL-DECIDE の j* と一致するか否かの**判定は書かない**(§3.3 の発効判定 = 司令塔)。

---

## K2 — 表の網羅性の言明(逐語)

### K2-a. Table A.3 の範囲

- キャプション(p.39・画像照合): "Calculated irregular pairs of order 10 of primes below 1000."
- 本文 §3(p.9・画像照合): "**In [11, pp. 128–130] irregular pairs of order 10 were calculated for all irregular primes p < 1000. These results are reprinted in Table A.3.**"([11] = Kellner の diploma thesis)
- **機械集計(導出値)**: Table A.3 の行数 = **81 行**(pp.39–40)・相異なる素数 = **64 個**(pdftotext 出力の awk 集計。手写しでなく機械カウント)。⟹ 「8 素数の抜粋」ではなく **p < 1000 の全 irregular pair の悉皆表**(本文言明 + 行数の整合)。
- 計算の二重チェック言明(p.40・画像照合): "Note that Tables A.2 and A.3 were calculated with smallest possible indices of the Bernoulli numbers using Proposition 5.1; they agree with these results above. Additionally, the results were checked by Corollary 4.23 and Proposition 5.3."

### K2-b. BCEM 検証域との関係 = **Remark 2.8**(§2, p.6・画像照合・全文)

> "... This error was already noticed by Johnson [10] who has also determined all irregular pairs (p, l′) of order two with p below 8000. Wagstaff [21] has extended calculations of irregular pairs, indices s, and associated cyclotomic invariants up to p < 125 000. He also checked that FLT is true for all such exponents p in that range. Finally, Buhler, Crandall, Ernvall, Metsänkylä, and Shokrollahi [2] have extended calculations of irregular pairs and associated cyclotomic invariants up to p < 12 000 000. For all these irregular pairs (p, l) in that range Δ₍p,l₎ ≠ 0 is always valid which ensures that each time there is only one related irregular pair (p, l′) of order two. Hence i₂(p) = i(p) for these irregular primes p. One has to notice that always (p, l) ≠ (p, l′). So far, no irregular pair (p, l) has been found with p² | B̂(l)."

([2] = BCEM, *Irregular primes and cyclotomic invariants to 12 million*, J. Symb. Comput. 31 (2001), 89–96 — 参考文献一覧 p.40 で照合)

### K2-c. UNKNOWN(K2 の残り)

- **BCEM の order-2 index (l′) の一覧データが公開されているか**: 本論文からは **UNKNOWN**。Kellner は BCEM が「calculations of irregular pairs and associated cyclotomic invariants」を p < 12M まで行ったこと・その範囲で Δ ≠ 0 が常に成立すること(⟹ order-2 対の存在と一意性)までを言うのみで、**l′ の数表の公開の言明はない**。BCEM 原論文は盤上未収蔵(scout 報告 §候補一覧 #2 と同じ状態)。
- 参考(p.28・画像照合・範囲の含意): "if one has calculated the first irregular pairs of order 10 for the first irregular primes p₁, . . . , p_r like Table A.3, then one can specify ad hoc all irregular prime powers p_ν^{e_ν} with p_ν ≤ p_r of Bₙ resp. ζ(1−n) up to index n = 4·10¹⁵. Note that this lower bound is here determined by the first irregular prime 37 and order 10."

---

## K3 — Δ ≠ 0 の全域性(逐語)

1. **Remark 2.8**(§2, p.6・画像照合): "For all these irregular pairs (p, l) in that range **Δ₍p,l₎ ≠ 0 is always valid**"(range = p < 12 000 000・K2-b の全文参照)。
2. **§3 本文**(Thm 3.2 直後, p.9・画像照合): "The property of Δ₍p,l₎, whether Δ₍p,l₎ vanishes or not, is passed on to all related irregular pairs of higher order. The case of a singular Δ₍p,l₎ would possibly imply a strange behavior without any regularity. **By calculation in [2] up to p < 12 000 000, no such Δ₍p,l₎ was found.**"
3. **§6**(p.31・画像照合): "**All conditions of the theorem above hold for all irregular primes p < 12 000 000 as verified in [2].**" — "the theorem above" = **Theorem 6.1**(p.31・画像照合):
   > "**Theorem 6.1** Let p be an irregular prime. Assume the following conditions for all irregular pairs (p, l): (1) The conjecture of Kummer–Vandiver holds: p ∤ h_p⁺, (2) The Kummer congruence does not hold (mod p²): B̂(l + p − 1) ≢ B̂(l) (mod p²), (3) The generalized Bernoulli number is not divisible by p²: B_{1,ω^{l−1}} ≢ 0 (mod p² ℤ_p). If these are satisfied, then ord_p h(ℚ(μ_{pⁿ})) = i(p) n for all n ≥ 1."

   同頁の等価な言い換え(画像照合): "(2') The Δ-Conjecture holds: Δ₍p,l₎ ≠ 0, (3') A special irregular pair of order two does not exist: (p, l, l−1) ∉ Ψ̂₂^irr."(条件 (2) の mod p² Kummer 合同の不成立 = Def 2.3 の Δ₍p,l₎ ≠ 0(n = 1)と同じ量)
4. **範囲無制限の全域性は予想** = **Conjecture 3.4**(§3, p.10・画像照合):
   > "**Conjecture 3.4 (Δ-Conjecture)** For all irregular primes p the following properties, which are equivalent, hold: (1) Δ₍p,l₎ is nonsingular for all irregular pairs (p, l) ∈ Ψ₁^irr, (2) Δ(p) = 1, (3) i(p) = i₂(p) = i₃(p) = . . . ."

**注意(逐語の格)**: p < 12 000 000 での Δ ≠ 0 は「[2] の計算により検証された」という**他人の計算の引用**(Kellner 自身の再計算ではない)。§3.3 の規約(cross-checked と書かない)に該当。

---

## K4 ★ — order-3 以上の対に関する言明(逐語)

### K4-a. データが存在する範囲

| 範囲 | order | 所在 | 逐語根拠 |
|---|---|---|---|
| 全 irregular primes **p < 1000**(81 対・機械集計) | **10 まで**(s₃…s₁₀ 列) | **Table A.3**(pp.39–40・画像照合) | p.9: "irregular pairs of order 10 were calculated for all irregular primes p < 1000"(K2-a) |
| **p = 37, 59, 67** | **100 まで** | **Table A.2**(p.38・画像照合) | キャプション: "**Table A.2** Calculated irregular pairs of order 100 of primes 37, 59, and 67." |
| 1000 ≤ p < 12·10⁶ | **2 のみ保証**(i₂(p) = i(p)) | 数表なし | Remark 2.8(K2-b)。**order ≥ 3 の index データの所在は UNKNOWN**(本論文に言明なし) |
| 存在・一意性(index 値ぬき) | 全 order n | 定理 | Thm 3.1(K1-d): Δ₍p,l₁₎ ≠ 0 ⟹ 各 n にちょうど 1 個の related pair |

### K4-b. 「上位 order の対が同じ index に来る」ことの表上の読み方(s_k = 0)

- Remark 2.12(p.8・K1-c 逐語): "**If s_k = 0 with k ≥ 2 then there is an irregular pair (p, l_k) of order k with (p, l_k) ∈ Ψ_k^irr and (p, l_k) ∈ Ψ_{k−1}^irr.**"
- §3 本文(p.9・画像照合): "In this table only one irregular pair has a zero in its p-adic notation: **(157, 62, 40, 145, 67, 29, 69, 0, 87, 89, 21) ∈ Ψ̂₁₀^irr.**" — Table A.3 の行 (157,62) の s₇ = 0(p.39 画像で列値一致を照合)。
- 続き(p.9–10・画像照合): "Hence, one has with a relatively small index that (157, 6 557 686 520 486) ∈ Ψ₆^irr ∩ Ψ₇^irr. It seems that these zeros can be viewed as exceptional; see also Table A.2. It would be of interest to investigate in which regions such indices may occur. This could explain why no irregular pair (p, l) ∈ Ψ₁^irr ∩ Ψ₂^irr has yet been found, because these regions are beyond present calculations. Here we have index 12 000 000 in [2] against index 6 557 686 520 486. Because of the rare occurrence of zeros one can expect that (p, l) ∈ Ψ₁^irr ∩ Ψ₂^irr resp. p² | B̂(l) will not happen often."
- Table A.2(p.38・画像照合)の zeros 記載: p = 37: "Zeros of the sequence (s_ν) occur at index 19 and 81." / p = 59: index 31, 95 / p = 67: index 23, 85。
- Theorem 3.2(p.9・画像照合・Δ = 0 の場合の分岐): "**Theorem 3.2** Let (p, lₙ) ∈ Ψₙ^irr, n ≥ 1 with Δ₍p,lₙ₎ = 0. Then there are two cases: (1) (p, lₙ) ∉ Ψₙ₊₁^irr: There are no related irregular pairs of order n + 1 and higher, (2) (p, lₙ) ∈ Ψₙ₊₁^irr: There exist p related irregular pairs of order n + 1 where (p, lₙ₊₁,ⱼ) ∈ Ψₙ₊₁^irr with Δ₍p,lₙ₊₁,ⱼ₎ = 0 and lₙ₊₁,ⱼ = lₙ + jφ(pⁿ) for j = 0, . . . , p − 1."

### K4-c. K4 の帰結(記録のみ・判定は書かない)

order-3 以上の index データは **p < 1000 で order 10 まで表として実在**(+ 37/59/67 は order 100)。**p ≥ 1000 では本論文に無い**。KELL-DECIDE の発効版選択(K1+K2 のみ / K1+K2+K4)への当てはめは司令塔。

---

## CH-7 pin — 記録: **未収蔵**

- **札の指定**: `docs/notes/ideas_counterexample_hunt_v1.md` 札 CH-7(L105–110)。警告行: 「『Frobenius 影 = p 進 MZV』の正規化 pin が先(**one-point 文献要請の型**)」。**札は pin 対象の具体文献を指定していない**(「文献要請を出すべし」という型の指定であり、書誌の名指しなし)。
- **盤上走査**(2026-08-11): `papers/`・`papers/delivered/` の全ファイル名走査 + 近傍候補の中身点検:
  - `papers/delivered/furusho_RIMS1357_mzv_gt.pdf`(Furusho, MZV and GT survey): txt 全文 grep で "p-adic" / "Frobenius" / "crystalline" の実質ヒット **0**(唯一のヒットは参考文献 Soulé の論文題目)。p 進 MZV の内容なし。
  - `papers/delivered/deligne_1989_groupe_fondamental_P1_moins_3points.pdf`: "cristallin" 51 件・"Frobenius" 50 件(pdftotext grep)。crystalline 実現の議論はあるが、**p 進 MZV(1989 年時点で未定義)の正規化との関係の逐語は求められない**(精読未実施・該当可能性の判定は司令塔)。
  - その他の盤上文献に「crystalline Frobenius の像と p 進 MZV の正規化」を主題とする一次文献なし。
- **記録**: **未収蔵**。跳ばす(取り寄せは司令塔の職掌)。候補書誌の同定・採否も司令塔/scout の職掌のため本書には書かない。

---

## 台帳用の要約(1 行ずつ・全て candidate・文献裏書き)

| pin | 結果 | 一次根拠(頁は arXiv v4) |
|---|---|---|
| K1 | s₁…s₁₀ = 関連 irregular pair の p 進表記の桁(l = Σ s_ν φ(p^{ν−1}))。s₂ 列 = order-2 対の index s(Remark 2.8 が名指し)・s₂ ≡ −p⁻¹(B_l/l)Δ⁻¹ (mod p) | Def 2.11 (p.8)・Rem 2.12 (p.8)・Thm 3.1 (pp.8–9)・Prop 2.7(3) (p.5)・Rem 2.8 (p.6)・Prop 5.6 (p.29) |
| K2 | Table A.3 = **p < 1000 の全 irregular pair の悉皆**(81 行・機械集計)・order 10 まで。BCEM 域 (p < 12M) は Δ ≠ 0 と i₂ = i のみ・**l′ 数表の公開言明なし = UNKNOWN** | p.9・p.39 caption・Rem 2.8 (p.6)・p.40 検算文 |
| K3 | p < 12 000 000 の全 irregular pair で Δ₍p,l₎ ≠ 0([2] の計算の引用)。無制限は Conjecture 3.4(Δ-Conjecture) | Rem 2.8 (p.6)・p.9・Thm 6.1 + 検証文 (p.31)・Conj 3.4 (p.10) |
| K4 | order ≥ 3 の index データ: p < 1000 は order 10 まで(A.3)・37/59/67 は order 100 まで(A.2)・**p ≥ 1000 は本論文に無し(UNKNOWN)**。s_k = 0 ⟺ order-k 対が order-(k−1) 対と同 index(Rem 2.12)・A.3 内の零は (157,62) の s₇ = 0 の 1 箇所のみ | pp.8–10・p.38・pp.39–40 |
| CH-7 | **未収蔵**(札に文献指定なし・盤上に該当一次文献なし)・跳ばす | 札 CH-7 L110・盤上走査 |

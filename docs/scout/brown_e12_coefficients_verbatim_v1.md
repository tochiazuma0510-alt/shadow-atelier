# Brown 1301.3053 ē₁₂ の係数 — 逐語+再構成 v1(CR-1)/ CR-2〜CR-4 同梱

- **依頼**: 裁定 755(CR-1 最優先)・委嘱元仕様 = `docs/notes/cone_design_v1.md` §6.3(CR-1〜CR-4)。**解釈判断は書かない**(UNKNOWN は UNKNOWN と明記)。
- **対象 PDF**: `papers/brown-2013-1301.3053-depth-graded-motivic-mzv.pdf`(arXiv:1301.3053**v2** [math.NT] 10 Jan 2020, Francis Brown, "Depth-graded motivic multiple zeta values")
- **読了頁申告**: 本タスクで頁画像照合(200dpi レンダリング)= **pp. 19, 20, 22, 24, 25, 28, 29**。テキスト全文走査(pdftotext, 全 34 頁)で "isomorphism" "Broadhurst" "dimension" "Swinnerton/Serre/dihedral/mod 23" の出現を確認。先行ノート `brown_eq14_verbatim_v1.md`・`brown_prop64_lattice_verbatim_v1.md` は**不改変**。
- **★ 前提の訂正(最重要・裁定 757③ で司令塔承認済)**: **紙面には ē₁₂ の項は 3 項しか印字されていない**(p.24 画像照合: "Writing out just a few of its coefficients as an example, we have: … (118 terms in total)")。⟹ **全 118 項の「逐語」抽出は原理的に不可能**。本納品は (§1) 逐語部 = 印字 3 項+員数言明+定義文、(§2) 導出部 = 定義 (8.6)+f₁₂ からの機械再構成(格札つき)に**節分離**する。

---

# 1. CR-1 逐語部(すべて頁画像照合済み)

## 1.1 ē₁₂ の表示とその前文(Example 8.4, p.24 — 画像照合済み・逐語)

> "We know by theorem 1.1 that g^m is of dimension 2 in weight twelve, spanned by {σ₃, σ₉} and {σ₅, σ₇}. We know by (7.9) that in weight twelve dg₂^m is of dimension one, dg₃^m vanishes by parity, so it follows that dg₄^m is of dimension one and hence spanned by ē₁₂ (since we know that ls₄ in weight 12 is one-dimensional). **Writing out just a few of its coefficients as an example, we have:**
>
> **ē₁₂ = x₃⁷x₄ − 116 x₁³x₂²x₃²x₄ − 57 x₁²x₂⁵x₄ + . . .  (118 terms in total)**"

- 表記注: ē₁₂ = 論文の \bar{𝖾}₁₂(sans-serif 𝖾 に上線 = x 変数への reduction、Definition 8.1)。
- **員数確認の判定: 紙面に印字された項は 3 項のみ**(係数 1, −116, −57)。残り 115 項は "…" で省略され、**論文のどこにも印字されていない**(全文走査で確認)。員数の言明 "(118 terms in total)" 自体は逐語で pin。

## 1.2 直後の合同(p.24 — 画像照合済み・逐語)

> "Using ē₁₂ one can write all depth-graded motivic multiple zeta values of depth four and weight twelve as multiples of ζ_𝔇(1, 1, 8, 2). For example, one has
>
> ζ_𝔇(4, 3, 3, 2) ≡ −116 ζ_𝔇(1, 1, 8, 2) ,  ζ_𝔇(3, 6, 1, 2) ≡ −57 ζ_𝔇(1, 1, 8, 2)
>
> modulo products and modulo multiple zeta values of depth ≤ 2."

## 1.3 f₁₂(整生成元)の逐語(Example 8.4, p.24 — 画像照合済み)

> "It follows from (7.4) that the space of period polynomials in degrees 12, 16, 18 and 20 is of dimension 1. **Choose integral generators:**
>
> f₁₂ = [x₁⁸, x₂²] − 3 [x₁⁶, x₂⁴]
> f₁₆ = 2 [x₁¹², x₂²] − 7 [x₁¹⁰, x₂⁴] + 11 [x₁⁸, x₂⁶]
> f₁₈ = 8 [x₁¹⁴, x₂²] − 25 [x₁¹², x₂⁴] + 26 [x₁¹⁰, x₂⁶]
> f₂₀ = 3 [x₁¹⁶, x₂²] − 10 [x₁¹⁴, x₂⁴] + 14 [x₁¹², x₂⁶] − 13 [x₁¹⁰, x₂⁸]
>
> where [x₁ᵃ, x₂ᵇ] denotes x₁ᵃx₂ᵇ − x₁ᵇx₂ᵃ. Let e₁₂, . . . , e₂₀ denote the corresponding exceptional elements."

- 導出注(根拠 = 上の定義の展開): f₁₂(x,y) = x⁸y² − 3x⁶y⁴ + 3x⁴y⁶ − x²y⁸ = s₁₂(Example 7.2, p.21 の s₁₂ = X²Y²(X−Y)³(X+Y)³ と多項式恒等・機械検算済 §2.2)。

## 1.4 ē_f の定義文(§8.2 + Definition 8.1 + Remark 8.2, p.22 — 画像照合済み・逐語)

§8.2(p.22): f ∈ S_{2n+2}(even period polynomial・y=0 で消える)に対し

> "f(x, y) = x y (x − y) f₀(x, y)
>
> where f₀(x, y) ∈ ℚ[x, y] is symmetric and homogeneous of degree 2n − 3, and satisfies
>
> (8.4)  f₀(x, y) + f₀(y − x, −x) + f₀(−y, x − y) = 0 .
>
> Let us also write f₁(x, y) = (x−y)f₀(x, y). We have f₁(−x, y) = f₁(x, −y) = −f₁(x, y)."

Definition 8.1(p.22):

> "(8.5)  e_f ∈ ℚ[y₀, y₁, y₂, y₃, y₄]
>
> e_f = Σ_{ℤ/5ℤ} ( f₁(y₄ − y₃, y₂ − y₁) + (y₀ − y₁) f₀(y₂ − y₃, y₄ − y₃) ) ,
>
> where the sum is over cyclic permutations (y₀, y₁, y₂, y₃, y₄) ↦ (y₁, y₂, y₃, y₄, y₀). Its reduction ē_f ∈ ℚ[x₁, . . . , x₄] is obtained by setting y₀ = 0, y_i = x_i, for i = 1, . . . , 4."

Remark 8.2(p.22)— **(8.6) = 導出の根拠式・逐語**:

> "(8.6)  ē_f(x₁, x₂, x₃, x₄) = f₁(x₄ − x₃, x₂ − x₁) + f₁(−x₄, x₃ − x₂) + f₁(x₁, x₄ − x₃)
> + f₁(x₂ − x₁, −x₄) + f₁(x₃ − x₂, x₁) − x₁ f₀(x₂ − x₃, x₄ − x₃) + (x₁ − x₂) f₀(x₃ − x₄, −x₄)
> + (x₂ − x₃) f₀(x₄, x₁) + (x₃ − x₄) f₀(−x₁, x₂ − x₁) + x₄ f₀(x₁ − x₂, x₃ − x₂) ."

さらに(p.22・逐語): "(8.7)  ē_f(x, y, 0, 0) = f₁(−y, x) = f₁(x, y) ."

## 1.5 CR-1 の結論(事実のみ)

| 項目 | 結果 |
|---|---|
| 紙面の逐語係数 | **3 項のみ**: (x₃⁷x₄, **1**)・(x₁³x₂²x₃²x₄, **−116**)・(x₁²x₂⁵x₄, **−57**)(+同値情報として §1.2 の ζ_𝔇 合同の −116, −57) |
| 員数 | 言明 "(118 terms in total)" は逐語 pin。**全 118 項の印字は論文に存在しない** |
| 全 118 項の整性の明示的主張 | 論文に**なし** = UNKNOWN(先行ノート `brown_prop64_lattice_verbatim_v1.md` §2.3 の記録を再確認) |
| 全係数の取得経路 | 論文内には (8.6)+f₁₂ による**構成的定義**があるのみ ⟹ §2 の再構成(導出値) |

---

# 2. CR-1 導出部 — 全 118 項の機械再構成

> ### 格札: **derived・単系統(sympy 1 系統のみ)・第二系統検査まで gcd 判定に使用不可**
> 根拠式はすべて紙面逐語((8.6) p.22・f₁₂ p.24・機械検算アンカーは §2.2)。ただし**計算は単系統**であり、P-CONE-2(原始性 = gcd 1)の判定には**使用しない**。観察事実の記録まで。

## 2.1 手順(再現コマンド)

- コード: **`docs/scout/brown_e12_reconstruct.py`**(sympy。実行: `python docs/scout/brown_e12_reconstruct.py`)
- 手順: f₁₂ = [x₁⁸,x₂²] − 3[x₁⁶,x₂⁴] → f₀ = f₁₂/(xy(x−y))(整除・剰余 0 を機械確認)→ f₁ = (x−y)f₀ → (8.6) をそのまま展開 → Poly(x₁..x₄) の全項を列挙。
- 導出注: f₀ = x y (x−y)² (x+y)³、f₁ = x y (x−y)³ (x+y)³(いずれも機械因数分解の出力)。

## 2.2 照合欄(紙面から拾える全アンカー vs 再構成)

| # | アンカー(出典・逐語) | 期待値 | 再構成値 | 判定 |
|---|---|---|---|---|
| 1 | coeff(x₃⁷x₄)(p.24 表示 1 項目) | 1 | 1 | ✔ |
| 2 | coeff(x₁³x₂²x₃²x₄)(p.24 表示 2 項目) | −116 | −116 | ✔ |
| 3 | coeff(x₁²x₂⁵x₄)(p.24 表示 3 項目) | −57 | −57 | ✔ |
| 4 | 員数 "(118 terms in total)"(p.24) | 118 | **118** | ✔ |
| 5 | ζ_𝔇(4,3,3,2) ≡ −116・ζ_𝔇(3,6,1,2) ≡ −57(p.24)= アンカー 2,3 の再掲 | −116/−57 | 同上 | ✔ |
| 6 | (8.7): ē₁₂(x,y,0,0) = f₁(x,y)(p.22)⟹ coeff(x₁⁷x₂, x₁⁵x₂³, x₁³x₂⁵, x₁x₂⁷) | 1, −3, 3, −1 | 1, −3, 3, −1 | ✔(恒等式全体も機械照合 ✔) |
| 7 | 線形化二重シャッフル 4 本 (8.2)(8.3)(p.22・Theorem 8.3 の主張 = e_f は解) | 全 4 本 = 0 | 全 4 本 = 0 | ✔ |
| 8 | e_f の ℤ/5 巡回不変性(Definition 8.1, p.22) | 不変 | 不変 | ✔ |
| 9 | sparsity (9.2): ∂⁵e_f/∂y₀…∂y₄ = 0(Lemma 9.2, p.26) | 0 | 0 | ✔ |
| 10 | unevenness (9.1): π^ev_{y₀}…π^ev_{y₄}(e_f) = 0(Lemma 9.1, p.26) | 0 | 0 | ✔ |
| 11 | 反対称性 ē(x₁,x₂,x₃,x₄) = −ē(x₄,x₃,x₂,x₁)(Definition 6.6(2) r=4, p.19) | 成立 | 成立(59 正項/59 負項・係数和 0 と整合) | ✔ |

## 2.3 全 118 項(機械可読・導出値)

形式: `[[a1,a2,a3,a4], c]` = c·x₁^a1·x₂^a2·x₃^a3·x₄^a4。順序 = sympy lex 降順。
sha256(下記 JSON 全文)= `baaa7580a6f6d45ee1a40dc2472ae92d49b7636a1dc33912667ce799d62acc1f`

```json
{"element":"e12_bar","vars":["x1","x2","x3","x4"],"term_format":"[[a1,a2,a3,a4],coeff] = coeff*x1^a1*x2^a2*x3^a3*x4^a4","order":"sympy lex desc on (a1,a2,a3,a4)","n_terms":118,"terms":[[[7,1,0,0],1],[[7,0,1,0],-3],[[7,0,0,1],3],[[6,1,1,0],7],[[6,1,0,1],-14],[[5,3,0,0],-3],[[5,2,1,0],-20],[[5,2,0,1],57],[[5,1,2,0],-9],[[5,1,1,1],-8],[[5,1,0,2],1],[[5,0,3,0],9],[[5,0,2,1],-17],[[5,0,1,2],17],[[5,0,0,3],-9],[[4,3,1,0],55],[[4,3,0,1],-108],[[4,2,1,1],19],[[4,1,3,0],-15],[[4,1,2,1],46],[[4,1,1,2],-45],[[4,1,0,3],28],[[4,0,3,1],-2],[[4,0,1,3],2],[[3,5,0,0],3],[[3,4,1,0],-68],[[3,4,0,1],108],[[3,3,2,0],30],[[3,3,1,1],-8],[[3,2,2,1],-116],[[3,2,1,2],90],[[3,2,0,3],-60],[[3,1,4,0],15],[[3,1,3,1],16],[[3,1,0,4],-2],[[3,0,5,0],-9],[[3,0,4,1],28],[[3,0,3,2],-60],[[3,0,2,3],60],[[3,0,1,4],-28],[[3,0,0,5],9],[[2,5,1,0],28],[[2,5,0,1],-57],[[2,4,1,1],-20],[[2,3,3,0],-30],[[2,3,2,1],142],[[2,3,1,2],-90],[[2,3,0,3],60],[[2,2,3,1],-26],[[2,1,5,0],9],[[2,1,4,1],-44],[[2,1,3,2],90],[[2,1,2,3],-90],[[2,1,1,4],45],[[2,1,0,5],-17],[[2,0,5,1],1],[[2,0,1,5],-1],[[1,7,0,0],-1],[[1,6,0,1],14],[[1,5,2,0],-28],[[1,5,1,1],24],[[1,5,0,2],-1],[[1,4,3,0],68],[[1,4,2,1],-84],[[1,4,1,2],44],[[1,4,0,3],-28],[[1,3,4,0],-55],[[1,3,2,2],26],[[1,3,1,3],-16],[[1,3,0,4],2],[[1,2,5,0],20],[[1,2,4,1],84],[[1,2,3,2],-142],[[1,2,2,3],116],[[1,2,1,4],-46],[[1,2,0,5],17],[[1,1,6,0],-7],[[1,1,5,1],-24],[[1,1,4,2],20],[[1,1,3,3],8],[[1,1,2,4],-19],[[1,1,1,5],8],[[1,0,7,0],3],[[1,0,6,1],-14],[[1,0,5,2],57],[[1,0,4,3],-108],[[1,0,3,4],108],[[1,0,2,5],-57],[[1,0,1,6],14],[[1,0,0,7],-3],[[0,7,1,0],1],[[0,7,0,1],-3],[[0,6,1,1],7],[[0,5,3,0],-3],[[0,5,2,1],-20],[[0,5,1,2],-9],[[0,5,0,3],9],[[0,4,3,1],55],[[0,4,1,3],-15],[[0,3,5,0],3],[[0,3,4,1],-68],[[0,3,3,2],30],[[0,3,1,4],15],[[0,3,0,5],-9],[[0,2,5,1],28],[[0,2,3,3],-30],[[0,2,1,5],9],[[0,1,7,0],-1],[[0,1,5,2],-28],[[0,1,4,3],68],[[0,1,3,4],-55],[[0,1,2,5],20],[[0,1,1,6],-7],[[0,1,0,7],3],[[0,0,7,1],1],[[0,0,5,3],-3],[[0,0,3,5],3],[[0,0,1,7],-1]]}
```

## 2.4 観察事実(導出値・解釈なし)

- **全 118 係数は整数**(sympy Poly の係数がすべて ℤ・分母なし)。
- |係数| の集合 = {1,2,3,7,8,9,14,15,16,17,19,20,24,26,28,30,44,45,46,55,57,60,68,84,90,108,116,142}。最大 |係数| = 142。
- 正項 59・負項 59・係数和 0(反対称性 §2.2 #11 と整合)。
- **gcd(|係数|) = 1**。⚠ この値は**単系統の導出値**であり、P-CONE-2(原始性)の**判定には使用不可**(格札)— 第二系統(独立実装)での再計算・突合が先。

---

# 3. CR-2 — p.25 "up to a non-trivial isomorphism …" の前後(【CONE-GAP-2】素材)

## 3.1 当該文とその前後(§8.4 末尾, p.25 — 画像照合済み・逐語)

> "… where 𝔞 = {g^m, g^m} + 𝔇⁵g^m, i.e., the previous identities hold modulo commutators and modulo terms of depth 5 or more. **In this manner, I have checked that the elements e_f are motivic for all f up to weight 30. In particular, it seems that the differential d is related to our map e (which is defined over ℤ) up to a non-trivial isomorphism of the space of period polynomials.** The numerators on the right-hand side are the numerators of ζ(16)π⁻¹⁶, ζ(18)π⁻¹⁸, and ζ(20)π⁻²⁰. Unfortunately, it does not seem possible to construct canonical zeta elements σ̃₂ₙ₊₁ for n ≥ 5 in a consistent way such that the above relations hold exactly in g₄^m (and not modulo 𝔞)."

さらに同頁(画像照合済み・逐語)— 当該同型に関わる唯一の追加情報:

> "Yasuda has since shown, assuming that the e_f are motivic, how to relate the exceptional elements to the differential d using the action of Hecke operators on the space of period polynomials."

## 3.2 判定素材の整理(事実のみ)

| 項目 | 内容 |
|---|---|
| 言明の性格 | "**it seems that**" つきの観察報告(weight 30 までの数値検証 "I have checked" に基づく)。定理・命題としては提示されていない |
| 同型の明示式 | **なし**(全文走査: この句の出現は p.25 の 1 箇所のみ) |
| 同型が整(GL(𝖯^ℤ) の元)か | **記述なし = UNKNOWN**。"defined over ℤ" と言われているのは **e のみ**。同型側の係数体・整性への言及ゼロ |
| 追加の手がかり | Yasuda の結果(上記逐語): e_f と d の関係は period polynomial 空間への **Hecke 作用素の作用**で記述される(e_f motivic を仮定)。出典明示なし(References の [37] = "S. Yasuda: private notes" のみ、p.34 テキスト照合) |

⟹ **【CONE-GAP-2】は本論文内では閉じない**(同型の整性は UNKNOWN のまま。手がかりは Hecke 作用の一文のみ)。

---

# 4. CR-3 — 𝔻_r の定義と dim 𝔻_r の公式(【CONE-GAP-3】素材)

## 4.1 𝔻_r の定義(Definition 6.7, p.19 — 画像照合済み・逐語)

> "**Definition 6.7.** We use the notation 𝔻_r ⊂ ℚ[x₁, . . . , x_r] to denote the space ρ̄(ls_r) in depth r. It is the space of polynomial solutions to the linearized double shuffle equations in depth r and is the direct sum for all n, of spaces denoted D_{n,r} in [21]."

補助(p.19 画像照合済み): ρ̄(dg₁^m) = ⊕_{n≥1} ℚ x₁²ⁿ(深さ 1)・Definition 6.6 の p̄_r 条件 (1)(2)(3)(逐語: (1) f(x₁,…,x_r) = f(−x₁,…,−x_r) (2) f(x₁,…,x_r) + (−1)^r f(x_r,…,x₁) = 0 (3) f(x₁,…,x_r) + (−1)^r f(x_{r−1}−x_r,…,x₁−x_r,−x_r) = 0)。𝔻₂・𝔻₃ の定義方程式は §7.2(p.20 画像照合済み・𝔻₂: f(x₁,x₂)+f(x₂,x₁)=0 と f(x₁,x₁+x₂)+f(x₂,x₁+x₂)=0・𝔻₃: 2 本の 3 項巡回和・f♯(x,y,z)=f(x,x+y,x+y+z))。深さ 4 は (8.2)(8.3)(§1.4 に逐語)。

## 4.2 次元の公式 — 論文にある範囲(頁つき)

| 深さ | 公式・出典 | 状態 |
|---|---|---|
| 𝖲(周期多項式) | **(7.4)** Σ_{n≥0} dim 𝖲₂ₙ s²ⁿ = s¹²/((1−s⁴)(1−s⁶)) = 𝕊(s)(p.20・画像照合済み・逐語) | **無条件・閉形式** |
| 𝔻₂ | **(7.8)** 0 → 𝖲 → 𝔻₁∧𝔻₁ → 𝔻₂ → 0 exact("relatively easy to show [17]"・p.21 画像照合済み) ⟹ dim 𝔻₂ は dim(𝔻₁∧𝔻₁) − dim 𝖲 で決まる | **無条件**(完全列経由・閉形式の明示はなし) |
| 𝔻₃ | **(7.10)** 0 → 𝖲⊗𝔻₁ → Lie₃(𝔻₁) → 𝔻₃ → 0 exact(Goncharov [19] の結果から・p.21 画像照合済み) | **無条件**(同上) |
| 𝔻_d, d ≥ 4 | "**Starting from depth 4, the structure of ls_d ≅ 𝔻_d is not known**³"(p.21 画像照合済み・逐語)。脚注 3(逐語): "After writing the first version of this paper, S. Yasuda kindly sent me his private notes [37] in which he gives a conjectural group-theoretic interpretation for the dimensions of 𝔻₄, in accordance with the Broadhurst-Kreimer conjecture." | **無条件の公式なし = UNKNOWN** |
| 𝔻₄ の個別値 | weight 12: dim 𝔻₄ = 1, Lie₄(𝔻₁) = 0(p.21 画像照合済み・逐語 "in weight 12, dim 𝔻₄ = 1, but Lie₄(𝔻₁) = 0") | 個別値のみ |
| ls 全体(条件付き) | **Lemma 10.2 (10.6)**(p.29 画像照合済み・逐語): "Conjecture 4 implies that X_{Uls}(s,t) = 1/(1 − 𝕆(s)t + 𝕊(s)t² − 𝕊(s)t⁴)"。続けて "If we identify ls_d via the isomorphism ρ̄ with the space of polynomials 𝔻_d satisfying the linearized double shuffle relations, we obtain the conjecture stated in ([21], appendix)." | **条件付き(Conjecture 4 前提)** |
| motivic 側(条件付き) | Corollary 10.4 (10.8)(pp.29-30 テキスト照合): Conjecture 5 ⟹ BK 型母関数 (1+𝔼(s)t)/(1−𝕆(s)t+𝕊(s)t²−𝕊(s)t⁴) | **条件付き(Conjecture 5 前提)** |

Conjecture 4(Strong BK+Zagier・(10.1))と Conjecture 5(Motivic BK・(10.2))の主張文は p.28 画像照合済み(H₁ ≅ ls₁ ⊕ e(𝖲)・H₂ ≅ 𝖲・H_{i≥3} = 0、および dg^m 版)。

## 4.3 CR-3 の結論(事実のみ)

- **dim 𝔻₄(重み任意)の無条件閉形式は論文に存在しない**。条件付きなら (10.6) の t⁴ 係数から抽出可能(Conjecture 4 前提・[21, appendix] の予想と同値と明言)。
- **dim L_{k,4}(Lie₄(𝔻₁) の重み k 部分)の公式も論文に明示なし** = UNKNOWN(weight 12 の Lie₄(𝔻₁) = 0 のみ逐語)。
- ⟹ 【CONE-GAP-3】の余次元表を**無条件に**埋める材料は本論文には無い。条件付き(Conj 4)でよければ (10.6) が正典の式。

---

# 5. CR-4 — Δ の例外素数と mod 23 表現(【CONE-GAP-4】)

**未収蔵。** 盤上の `papers/` に Serre / Swinnerton-Dyer 系(Δ の合同・例外素数・mod ℓ 表現)の文献は存在しない(2026-08-07 棚確認)。Brown 1301.3053 にも該当記述なし(全文走査: "Swinnerton" "Serre" "mod 23" = 0 hit・"dihedral" は §6.5 の二面体対称性(Ihara bracket の対称群)のみで Galois 表現とは無関係・"Ramanujan" は (1.4) の文脈のみ)。⟹ **跳ばす — 取り寄せ判断は司令塔**(委嘱仕様どおり文献ゲート経由)。

---

## 出典一覧(頁 = 論文印刷頁・v2)

- Definition 6.6・6.7・ρ̄(dg₁^m)・Example 6.9: p.19(画像照合)
- §7.1 (7.1)(7.2)(7.3)(7.4)・W^e ≅ 𝖲 ⊕ ℚp・§7.2 𝔻₂/𝔻₃ 方程式・(7.5)(7.6): p.20(画像照合)
- (7.7)(7.8)・Example 7.2(s₁₂)・(7.10)・depth ≥ 4 未知+脚注 3・dim 𝔻₄ = 1/Lie₄(𝔻₁) = 0: p.21(画像照合)
- §8.1 (8.1)(8.2)(8.3)・§8.2 f₀/f₁/(8.4)・Definition 8.1 (8.5)・Remark 8.2 (8.6)・(8.7): p.22(画像照合)
- Example 8.4(f₁₂..f₂₀・ē₁₂ 3 項表示・"(118 terms in total)"・ζ_𝔇 合同)・§8.4 Conjecture 3・d : 𝖲 → (dg₄^m)^ab・σ̃ の lift: p.24(画像照合)
- Examples 8.5・(8.8)・"I have checked … up to weight 30"・"it seems that the differential d is related to our map e (which is defined over ℤ) up to a non-trivial isomorphism …"・Yasuda/Hecke 文: p.25(画像照合)
- Lemma 9.1 (9.1)・Lemma 9.2 (9.2): p.26(テキスト照合・§2.2 の機械検査の根拠)
- §10 Conjecture 4 (10.1)・Conjecture 5 (10.2): p.28(画像照合)/ Lemma 10.2 (10.6)・Proposition 10.3: p.29(画像照合)/ Corollary 10.4 (10.8): pp.29-30(テキスト照合)
- References [17][19][21][37]: pp.33-34(テキスト照合)
- 再構成コード: `docs/scout/brown_e12_reconstruct.py`(sympy・出力 JSON の sha256 は §2.3 に記載)

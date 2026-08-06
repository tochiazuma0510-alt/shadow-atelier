# 【GAP-B4-1】B₄ pentagon: cocycle 形 ⟷ 回転形の項対応 — 文献 pin 調査 v1

- 発行: 精密読解係 reader / 2026-08-06
- 判定: **見つかった(pin 成立)** — 同一論文内で「5 項積 = 1(cocycle 形)」と「位数 5 の回転による 5 巡回項」が明示的に結ばれている箇所を **2 論文で各 1 箇所**、さらに補助論文に**同値定理(命題として定式化された最強形)**を確認。
- 本ノートは抽出のみ。数学的採否判断は司令塔専権。
- 重要式はすべてページ画像で原文照合済み(pdftotext との突合)。

---

## Pin A(主): Lochak–Schneps 1994, LMS Lecture Notes 200
`papers/lochak-schneps-1994-LMS200-GT-automorphisms-braid-groups.pdf`(全 36 頁, 論文頁 = PDF 頁)

### A-1. 定義側の pentagon = cocycle 形 (III)(§1, p.4)
GT̂₀ = {(λ,f) ∈ Ẑ* × [F̂₂,F̂₂]} が満たす関係(p.4, 画像照合済):

- (I) `f(x,y) f(y,x) = 1`
- (II) `f(z,x) z^m f(y,z) y^m f(x,y) x^m = 1`, ここで `m = (λ−1)/2`, `z = (xy)^{−1}`
- (III) `f(x12, x23·x24) · f(x13·x23, x34) = f(x23, x34) · f(x12·x13, x24·x34) · f(x12, x23)`

(III) の舞台: **K̂₄ = pure braid 群 K₄ の副有限完備化**(生成元 x_ij, 1≤i<j≤4; §2 p.5–6 で `x_ij = σ_{j−1}···σ_{i+1} σ_i² σ_{i+1}^{−1}···σ_{j−1}^{−1}` と定義, 画像照合済)。つまりこの論文の (III) は「2 項 = 3 項」の cocycle 形(Drinfeld [D] 引用の形)であり、**中心 ω₄ を殺していない genuine な K̂₄ 上**の式。

σ の規約: B_n は標準 Artin 生成元 σ₁,…,σ_{n−1}(braid 関係 (1), p.5)。命題 1(p.5)の対称生成系 σ_ij(σ_ij² = x_ij)。

### A-2. 対称 5 項形 (III′)(§4, p.17, 画像照合済)
M̂(0,5)(genus 0・5 点 mapping class 群の副有限完備化)内で x_ij を見ると (III) は次を導く:

```
(III′)  f(x34,x45) f(x51,x12) f(x23,x34) f(x45,x51) f(x12,x23) = 1
```

- 出典明記: 「This form of relation (III) was given by Ihara in [I1]」(p.17)。**(III) → (III′) の変換に使うもの**: 関係 (I)・§2 の関係 (4)・lemma 5 直前の注意(p.17 本文)。
  - 関係 (4)(p.7, 画像照合済): M(0,5) 内で `x̄45 = x̄12 x̄13 x̄23`, `x̄15 = x̄23 x̄24 x̄34`(証明は ȳ₅ = ω̄₅ = 1 と基点 4 の Hurwitz 関係 `x̄14 x̄24 x̄34 x̄45 = 1`)。
  - lemma 5 直前の注意(p.13): 共役関係 (a) `σ1 f(y,x) = f(z,x) σ1`, (b) `f(x,y) σ2 = σ2 f(z,y)`、および f ∈ 導来群ゆえ中心元 γ について `f(γα,β) = f(α,γβ) = f(α,β)`。
- 略記: `f₅f₄f₃f₂f₁ = 1`。

### A-3. 回転(位数 5 元)との結線 — これが pin(§4, p.17, 画像照合済)
- `σ15 := σ4 σ3 σ2 σ1 σ2^{−1} σ3^{−1} σ4^{−1}`(命題 1 の流儀; σ15² = x15)。
- **`V := Inn((σ4σ3σ2σ1)^{−3}) ∈ Inn(M̂(0,5))`, `V⁵ = 1`**(位数 5 の「五角形回転」)。
- 式 (6): `V(σ1)=σ3, V(σ2)=σ4, V(σ3)=σ15, V(σ4)=σ1, V(σ15)=σ2`;
  `V(x_ij) = x_{i+2,j+2}` (i,j ∈ ℤ/5ℤ)。簡潔形: `V(σ_{i,i+1}) = σ_{i+2,i+3}`。
- **項対応の明示**(p.17):

```
f₁ = f(x12,x23),   f_{i+1} = V^{−1}(f_i)   (i ∈ ℤ/5ℤ)
```

すなわち (III′) の 5 項は f₁ の V-軌道(回転軌道)そのもの。導出値(照合用): f₂=f(x45,x51), f₃=f(x23,x34), f₄=f(x51,x12), f₅=f(x34,x45) — 根拠式は V^{−1}(x_ij)=x_{i+3,j+3} と f₁ の定義。論文の (III′) の並びと一致。

### A-4. 回転形から (III′) が「出る」機構(lemma 7 の証明末尾, p.20, 画像照合済)
lemma 8(i)(p.18)より、φ(GT̂₀ の (λ,f) が誘導する写像)が M̂(0,5) の自己同型なら

```
φ = Inn(f₁) V^{−1} φ V
```

が成り立ち、これを 5 回反復して

```
φ = Inn(f₃f₂f₁)V^{−3}φV³ = Inn(f₄f₃f₂f₁)V^{−4}φV⁴ = Inn(f₅f₄f₃f₂f₁)V^{−5}φV⁵.
```

**V⁵ = 1 なので φ = Inn(f₅f₄f₃f₂f₁)φ、よって f₅f₄f₃f₂f₁ は M̂(0,5) の中心に属し、中心は自明ゆえ = 1。「But this element is exactly the left-hand side of relation (III′)」**(p.20 逐語)。

→ **cocycle 形(5 項積 = 1)⟷ 回転 V(位数 5)の同一論文内での明示的結線。pin 成立。**

### A-5. 中心元 z の扱い(この論文)
- (III) 自体は K̂₄ 上(中心あり・genuine)。(III′) は M̂(0,5) 上(= 中心を殺した世界)。
- M(0,n) = B_n/⟨y_n = ω_n = 1⟩(p.6; 球面関係+中心関係)。M̂(0,5) の中心は自明(p.20 の議論で明示使用)。
- B̂₄ 自身は M̂(0,5) に入らず **B̂₄/Z ⊂ M̂(0,5)**(p.16, p.6 命題 2(vi): K(0,n+1) ≃ K_n/Z ⊂ B_n/Z ⊂ M(0,n+1))。⟨σ1,σ2,σ3⟩ ⊂ M̂(0,5) は B̂₄ ではなく B̂₄/Z((σ1σ2σ3)⁴ = 1 が M̂(0,5) で成立し、これが B̂₄ の中心の生成元; p.20 画像照合済)。
- M̂(0,5) の中で使われる中心関係: (c) `ω₅ = (σ1σ2σ3σ4)⁵ = 1`(p.19, 画像照合済)。V の定義 `(σ4σ3σ2σ1)^{−3}` はこの ω₅=1 の世界で位数 5。
- lemma 9(p.20 以降)で M̂(0,5) の自己同型が B̂₄/Z に制限され、さらに B̂₄ へ一意に持ち上がる(タワー T̂₄ の矢を保つ)。

### A-6. GT̂ の braid への作用の向き(p.16, 画像照合済)
```
φ₄(σ1) = σ1^λ,  φ₄(σ2) = f(x23,x12) σ2^λ f(x12,x23),  φ₄(σ3) = f(σ3²,y3) σ3^λ f(y3,σ3²)
```
lemma 7 の M̂(0,5) 生成系への作用(p.17–18, 画像照合済):
```
φ(σ1) = σ1^λ,   φ(σ2) = f(x23,x12) σ2^λ f(x12,x23),
φ(σ3) = f(x34,x45) σ3^λ f(x45,x34),   φ(σ4) = σ4^λ,
φ(σ15) = f(x23,x12) f(x51,x45) σ15^λ f(x45,x51) f(x12,x23)
```

---

## Pin B(独立の第 2 pin): Lochak–Schneps「The universal Ptolemy-Teichmüller groupoid」
`papers/lochak-schneps-universal-ptolemy-teichmuller-groupoid.pdf`(全 23 頁; 出版頁 325–347, PDF 頁 = 出版頁 − 324)

### B-1. この論文の GT̂ 定義は最初から 5 項 cocycle 形(§4, p.340 = PDF 16, 画像照合済)
(λ,f) ∈ Ẑ* × F̂₂′:

- (I) `f(y,x) f(x,y) = 1` ← **1994 論文と引数順が逆**(内容は同値)
- (II) `f(z,x) z^m f(y,z) y^m f(x,y) x^m = 1`, `m = ½(λ−1)`, `z = (xy)^{−1}`
- **(III) `f(x34,x45) f(x51,x12) f(x23,x34) f(x45,x51) f(x12,x23) = 1`**

(III) の舞台: **K̂(0,5) = pure mapping class 群 K(0,5) の副有限完備化**(中心は既に定義で消えている世界)。M(0,n)(resp. K(0,n))は B_n(resp. K_n)を (i) `ω_n = 1` と (ii) 基点 i の Hurwitz 関係 `x_{i,i+1} x_{i,i+2} ··· x_{i,n} x_{i,1} ··· x_{i,i−1} = 1`(1≤i≤n, 添字 ℤ/nℤ)で割った群(§2, p.330–331)。

### B-2. 回転側 = Ptolemy 群の pentagon (αβ)⁵ = 1(Theorem 1, p.329 = PDF 5, 画像照合済)
マーク付きテセレーションへの 2 つの移動 α(向き付き辺の elementary move)・β(左三角形内の矢印反時計回し)につき、群 G(Ptolemy 群 ≅ Thompson 群)の定義関係:

```
α⁴,  β³,  (αβ)⁵,  [βαβ, α²βαβα²],  [βαβ, α²βα²βαβα²β²α²]
```

注(p.330): `(αβ)⁵ = 1` は Penner の 10 手の自明列(五角形の 2 本の対角線を同時に動かす回転)。

### B-3. 結線箇所 = Lemma 5 の証明(p.341–342 = PDF 17–18, 画像照合済・逐語)
GT̂ の元 F = (λ,f) の elementary move への作用(式 (2), p.341):
```
F(α_T) = α_T · f(x^T_{X_T Y_T}, x^T_{Y_T Z_T})
```
(X_T, Y_T, Z_T, W_T = T の basic quadrilateral の 4 区間のリボン、矢印の先から反時計回り; 図 8)。

pentagon の検査(p.342 逐語):
> As for the pentagon relation (αβ)⁵ = 1, or equivalently (βα)⁵ = 1, we have F(βα) = βα f(x_XY, x_YZ), and **five repeated applications of this map, together with the use of equation (1) to push all the factors of βα to the left, leave us with exactly the famous pentagon relation (III) defining GT̂, equal to 1.**

- 式 (1)(p.337): `x^{T′}_{AB} = γ^{−1} x^T_{AB} γ`(γ = Ptolemy groupoid の T′→T の一意射; 局所群 K̂^T と Ptolemy 射の可換性)。
- すなわち **回転(βα の 5 乗 = 1)を左へ押し出すと 5 巡回項の積 = (III) が正確に現れる** — 第 2 の pin。
- 5 項の各項は f(x_XY, x_YZ) の「回転による 5 巡回共役」(α⁴ = 1 の検査では同型の 4 項展開が明示計算されており p.342 に全文あり; pentagon 側の 5 項展開の明示表示は**論文中に無い**(文章記述のみ)— この点は UNKNOWN ではなく「本文が省略」)。
- 序文の裏づけ(p.325–326): 「the pentagonal relation of G reflects that of GT̂」「the role of the two pentagons appears in lemma 5」(p.326)。

### B-4. 中心の扱い(この論文)
局所群 K^T は pure ribbon mapping class 群 K*(0,n)(twist t_A 込み)を貼り合わせた群(§3, p.336–338)。(III) の舞台 K̂(0,5) は B-1 の通り ω₅ = 1 と Hurwitz 関係で中心を消した quotient。genuine な B̂₄/K̂₄ 上の記述はこの論文には無い。

---

## Pin C(補助・最強形 = 同値命題): Harbater–Schneps 2000, Trans. AMS 352
`papers/harbater-schneps-2000-TransAMS352-published.pdf`(出版頁 3117–3148, PDF 頁 = 出版頁 − 3116)

### C-1. 定義(§0.3, p.3118 = PDF 2, 画像照合済)
- (I) `f(y,x) f(x,y) = 1`
- (II) `f(z,x) z^m f(y,z) y^m f(x,y) x^m = 1`(F̂₂ = ⟨x,y,z | xyz = 1⟩ 内, m = (λ−1)/2)
- **(III) `f(x12,x23) f(x34,x45) f(x51,x12) f(x23,x34) f(x45,x51) = 1`**, 舞台は **K̂(0,5)**。
  - 注意: Pin B の (III) と同一語の**巡回置換**(積の切り出し位置が違うだけ)。
- Drinfeld 作用の向き(式 (1), p.3118): `σ1 ↦ σ1^λ`, `σi ↦ f(y_i, σi²)^{−1} σi^λ f(y_i, σi²)` (2≤i≤n−1), `y_i = σ_{i−1}···σ1·σ1···σ_{i−1}`。

### C-2. 回転 ρ と同値定理(§2.3, Proposition 7, p.3138–3140 = PDF 22–24, 画像照合済)
- **ρ ∈ Aut(K̂(0,5)): `ρ(x_{i,j}) = x_{i+3,j+3}`(添字 mod 5)**。ρ ∈ S̃₅ は置換 **(14253) ∈ S₅** の上にある(p.3138)。
- K̂(0,5) = π₁(M₀,₅), M̂(0,5) ≃ π₁(M₀,₅/S₅)(p.3138)。
- **Proposition 7**(p.3138–3139; (λ,f) が (I)(II) を満たす仮定の下で同値):
  - (i) (λ,f) が **(III)** を満たす。
  - (ii)/(ii)′ F̄ が Out♯₅ の元 F̃̄ へ延長/射影され **[ρ, F̃̄] = 1 in Out(K̂(0,5))**。
  - (iii)/(iii)′ F が A♯₅ の元 F̃ へ延長/射影され **[ρ, F̃] = inn f in Aut(K̂(0,5))**。
- 証明の要点(p.3139): (i)⇒(iii)′ は [LS, Lemma 7](= Pin A の lemma 7)による M̂(0,5) 自己同型 G を経由し、`ρF̃ = (inn f(x12,x23)) F̃ρ` を生成元 x_{i,i+1} 上で直接計算(x34 の検査に (I)、x51 の検査に (I)+(III) を使用 — **どの生成元で cocycle 条件が発火するかまで特定されている**)。
- **Remark(p.3140)**: 「Proposition 7 shows the equivalence of (III) and the commutation with ρ, under the hypothesis that (I) and (II) are satisfied. This hypothesis is in fact necessary.」 — Ihara [I3]: (I)+(III) ⇏ (II)。すなわち **(III) ⟷ ρ-可換は (I)(II) 前提つきの同値**(前提なしでは破綻し得る)。
- 効用(p.3138): これにより GT̂ を「3 つの cycle 関係 (I)–(III) なし」で Out♯ₙ として見る主定理(Main Theorem (b): Out♯ₙ ≃ GT̂, n≥5)が出る。

### C-3. 中心の扱い(この論文)
(III) は K̂(0,5)(中心なし quotient)。inn f のズレを込めれば Aut レベル(genuine)、Out レベルでは正確に可換 [ρ,F̃̄]=1。**「mod inner ⟷ genuine」の二段が (ii)/(iii) として明示的に書き分けられている**。

---

## 版差・規約差の台帳(同名概念の差分)

| 項目 | LS 1994 | LS Ptolemy | HS 2000 |
|---|---|---|---|
| (I) の順 | f(x,y)f(y,x)=1 | f(y,x)f(x,y)=1 | f(y,x)f(x,y)=1 |
| (III) の形 | 2 項=3 項 cocycle 形, K̂₄ 上 | 5 項積=1, K̂(0,5) 上 | 5 項積=1(巡回シフト差), K̂(0,5) 上 |
| 回転元 | V = Inn((σ4σ3σ2σ1)^{−3}), V(x_ij)=x_{i+2,j+2} | (αβ)⁵=1(Ptolemy 群; テセレーション回転) | ρ(x_ij)=x_{i+3,j+3}, over (14253) |
| 結線の形 | V⁵=1 ⇒ f₅f₄f₃f₂f₁ 中心 ⇒ =1(lemma 7 証明) | F(βα) の 5 反復 ⇒ (III)(lemma 5 証明) | (III) ⟺ [ρ,F̃]=inn f(Prop 7・同値命題) |
| 中心 | (III) は genuine K̂₄; (III′) は M̂(0,5)(中心自明) | K̂(0,5)(中心なし) | Aut 版(inn f 付き)と Out 版を書き分け |

- 添字回転の向き: LS1994 の V は i↦i+2、HS2000 の ρ は i↦i+3 = (i+2 の逆)。**V と ρ は互いに逆回転**(導出値; 根拠 = 各定義式)。
- (II)(hexagon)は 3 論文とも同一表記。
- 影工房主線(B₃ gentle 系, arXiv 2401.06870/2405.11725)には pentagon は存在しない(hexagon のみ)。本調査は副線(B₄ 系)用の外部参照であり、翻訳(一工夫)は司令塔工程。

## 結論(要求項目への回答)
1. **「5 項の積 = 1」型 cocycle 形と「回転の位数 5」形が同一論文内で結ばれている箇所** = **見つかった**。
   - 最直接: **LS1994 p.17(f_{i+1} = V^{−1}(f_i))+ p.20(V⁵=1 ⇒ (III′))**。
   - 第 2: **LS Ptolemy p.342(lemma 5 証明: (βα)⁵ の 5 反復 ⇒ (III))**。
   - 命題化された最強形: **HS2000 Prop 7((III) ⟺ ρ-可換, (I)(II) 前提)**。
2. 中心の扱いは各論文で上表の通り記録済み。B₄ 自身は M(0,5) に入らず **B₄/Z** が入る(LS1994 p.16)点が B₄ 系実装時の要注意点。
3. 5 項展開の明示表示が「回転側の計算として」書き下されているのは LS Ptolemy の α⁴ 検査(p.342)のみで、pentagon 側の 5 項の明示書き下しは同論文では文章記述(計算は読者に委ねられる)。LS1994 側は f₁…f₅ の全項が明示(p.17)。

## 読んだページ範囲の申告
- LS1994: 全文テキスト走査(pdftotext)+ページ画像照合 pp.4, 6, 7, 16, 17, 18, 19, 20(150dpi)。§5 以降(2 冪・pro-ℓ 詳細)と付録は本件対象外のため画像照合せず。
- LS Ptolemy: 全文テキスト走査+ページ画像照合 PDF pp.5(=329), 16(=340), 18(=342)。図 2,3,7,8 の図版内容自体は未検分(本文の言語記述で代用)。
- HS2000(補助): テキスト走査(冒頭 §0.3 と §2.3 周辺)+ページ画像照合 PDF pp.2(=3118), 22(=3138), 23(=3139)。p.3140 の Remark はテキストのみ(数式なしの文章のため)。harbater-schneps-2000-fund-groups-moduli-GT.pdf(プレプリント版)は未使用(出版版で足りたため)。

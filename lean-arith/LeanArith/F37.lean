/-
LeanArith/F37.lean — 設計書 docs/lean/K3対応表_v0.md §4.8 表(F33–F37)の F37 行。

F37 `β`: **ι (1.3) の同型条件**。r := M/e、q_e := (z ↦ z^r)|_{μ_M[e]} : μ_M[e] → μ_e。
「q_e が同型 ⟺ gcd(r,e)=1」。同型のとき ι := j ∘ q_e⁻¹ で (7.5) が厳密に従う(ι 自体は F35 の j と
組み合わせる別行であり、本ファイルは「q_e が同型 ⟺ gcd(r,e)=1」の核だけを扱う)。

**忠実性ノート(§0.3)**:
- 設計書は μ_M[e](M 乗根のうち e 乗して 1 になるもの)を台に取るが、これは位数 e の巡回群であり、
  μ_e(e 乗根の全体)とは「集合として同一だが写像が違う」(★教材 9・設計書の注記どおり)。
  本補題は**この 2 つの具体的な体上の群を区別せず**、「位数 e の有限巡回群 G 上、
  z ↦ z^r が自己同型であること」という抽象形で述べる。μ_M[e] も μ_e も位数 e の有限巡回群である
  以上、この抽象形が両者に等しく適用される(instantiate は F35/F37 の統合時に行う・本表 §4.8 の方針)。
- (δ2): 「同型」は Lean では「全単射な群準同型」ではなく、**台集合上の全単射**として述べる
  (z ↦ z^r が群準同型であることは `map_pow`/`zpow_natCast` の類で自明なので、負荷は全単射性に
  集中させるのが忠実 — 設計書 §4.8 の「巡回群の初等命題」という位置づけと一致)。

**Mathlib API**: `ZMod.isUnit_iff_coprime` [推定]・`isUnit_of_mul_eq_one`・`IsUnit.unit`・
`Equiv.mulLeft` を用いる。**存否は本セッションでは検証できない箇所がある(§5 冒頭の注記どおり)**。
-/

/-- **F37 の核**: 有限巡回群 `ZMod e`(`e ≠ 0`)上、乗法 `x ↦ r * x` が全単射であることは
    `Nat.Coprime r e` と同値である。これは「位数 e の巡回群上 z ↦ z^r が自己同型 ⟺ gcd(r,e)=1」
    の加法的な言い換え(乗法的冪 `z^r` は加法群 `ZMod e` では `r`-倍に対応する)。 -/
theorem F37_zmod_mul_bijective_iff_coprime (e r : ℕ) [NeZero e] :
    Function.Bijective (fun x : ZMod e => (r : ZMod e) * x) ↔ Nat.Coprime r e := by
  constructor
  · intro hbij
    obtain ⟨b, hb⟩ := hbij.surjective 1
    exact (ZMod.isUnit_iff_coprime r e).mp (isUnit_of_mul_eq_one _ b hb)
  · intro hcop
    have hu : IsUnit (r : ZMod e) := (ZMod.isUnit_iff_coprime r e).mpr hcop
    exact hu.mulLeft_bijective

#print axioms F37_zmod_mul_bijective_iff_coprime

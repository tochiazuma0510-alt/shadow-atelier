/-
K3/Shadows.lean — 表 C §4.3(Φ と (K4))。設計書 docs/lean/K3対応表_v0.md F16-F20。
新発見 N1(閉形 = 成分ごとの二面体自己同型)を使い、(K4) Φ の単射性を Lean 化する。

正典データの出所: docs/week4-K3飽和_opus_v2.md §2.5(逐語式・m,u_m,κ(m) の表)。
  u_m := 2m+1、κ(m) := m+1 (m 奇)/ -m (m 偶)  ((4.9)、D1 p.17)
  Φ_{m,k}(x̄) = x̄^{u_m} = (r^{u_m}, s, s)
  Φ_{m,k}(ȳ) = f_{m,k}⁻¹ ȳ^{u_m} f_{m,k} = (r^{1-4k}s, r^{u_m}, r^{1-2κ(m)}s)
  𝒳₃ = {0,2,3,5} ⊂ Z/6(D1 (4.12) の m の範囲、K_ord⁽³⁾=6)
-/

import K3.Base

/-- Nat を Fin 3 へ(mod 3)。m.val や u_m など Nat 由来の値を Fin 3 の指数へ落とすための補助。
    `Nat.mod_lt` + `decide` で証明する(`omega` は内部で `Quot.sound` を要求するため避ける —
    検収基準§8「plain 層は公理なしか propext のみ」を満たすための実装上の選択)。 -/
def toFin3 (n : Nat) : Fin 3 := ⟨n % 3, Nat.mod_lt n (by decide)⟩

/-- 正典 (4.9) 前半: u_m := 2m+1 の mod 3(D3 の回転部の指数として使う値)。 -/
def um (m : Fin 6) : Fin 3 := toFin3 (2 * m.val + 1)

/-- 正典 (4.9): κ(m) := m+1 (2∤m の逆・m 奇) / -m (m 偶) の mod 3。 -/
def kappa3 (m : Fin 6) : Fin 3 :=
  if m.val % 2 = 1 then toFin3 (m.val + 1) else toFin3 (3 - m.val % 3)

/-- 𝒳₃ = {m < 6 ∣ gcd(2m+1,6)=1} = {0,2,3,5}(D1 (4.12)、A3 で確認済みの値)。 -/
def X3 : List (Fin 6) := [0, 2, 3, 5]

/-- N1: 二面体自己同型 α_{v,t}(r^a) = r^{va}, α_{v,t}(r^a s) = r^{va+t} s。
    F16 の土台となる 1 成分あたりの写像。 -/
def alpha (v t : Fin 3) (x : D) : D :=
  if x.2 then (v * x.1 + t, true) else (v * x.1, false)

/-- **F16**: α_{v,t} は(任意の v,t で)D₃ の積と両立する — 自己同型であることの
    群準同型部分。plain Lean: `decide`(v,t,a,b にわたる全称・9×36=324 通り)。 -/
theorem F16_alpha_hom : ∀ v t : Fin 3, ∀ a b : D,
    alpha v t (dmul a b) = dmul (alpha v t a) (alpha v t b) := by decide +kernel

/-- α_{v,t} の逆写像(v が単元 {1,2} のとき): α_{v,t}⁻¹ = α_{v⁻¹, -v⁻¹t}。
    v⁻¹ は mod 3 の乗法逆元(1↦1, 2↦2 — ともに自己逆)。 -/
def invF3 (v : Fin 3) : Fin 3 := v  -- 1,2 は mod 3 で自己逆元(0 は本設計では使わない)

/-- **F20 の土台**: v ∈ {1,2} のとき α_{v,t} は全単射(明示逆写像 alpha (invF3 v) (-(invF3 v * t)))。
    `decide`(v∈{1,2}(2通り)×t(3通り)×x(6通り) = 36 通り、両方向)。 -/
theorem F20_alpha_bij : ∀ v : Fin 3, v ≠ 0 → ∀ t : Fin 3, ∀ x : D,
    alpha (invF3 v) (-(invF3 v * t)) (alpha v t x) = x ∧
    alpha v t (alpha (invF3 v) (-(invF3 v * t)) x) = x := by decide +kernel

/-- N1 の閉形 Φ_{m,k} : E → E(m : Fin 6, k : Fin 3)。
    N1 のパラメータ (v₁,t₁,v₂,t₂,v₃,t₃) = (u_m, 1-4k-u_m, u_m, 0, 1-2κ(m), 0)(設計書 §3 N1)は
    以下に直接インライン展開してある。
    3 成分とも α_{v_i,t_i} を独立に適用する「成分ごとの二面体自己同型」(観測 N1)。 -/
def Phicf (m : Fin 6) (k : Fin 3) : E → E := fun x =>
  (alpha (um m) (1 - 4 * k - um m) x.1, alpha (um m) 0 x.2.1, alpha (1 - 2 * kappa3 m) 0 x.2.2)

/-- 正典の生成元像の closed form(paper の boxed 式そのもの・docstring 冒頭参照)。
    F18 はこれと Phicf が一致することを検算する — Phicf の定義から独立に書き下した式。 -/
def canonX (m : Fin 6) : E := ((um m, false), (0, true), (0, true))
def canonY (m : Fin 6) (k : Fin 3) : E :=
  ((1 - 4 * k, true), (um m, false), (1 - 2 * kappa3 m, true))

/-- **F18**(★N1 の本体): 12 個の (m,k)(m∈𝒳₃, k∈Fin 3)について、閉形 Phicf が正典の
    生成元像 canonX/canonY と一致する(24 個の等式)。 -/
theorem F18_closed_form_matches :
    ∀ m ∈ X3, ∀ k : Fin 3,
      Phicf m k xb = canonX m ∧ Phicf m k yb = canonY m k := by decide +kernel

/-- **F19((K4) Φ 単射)**: 生成元像の対が一致すれば (m,k) = (m',k')。
    canonX/canonY で書く(F18 により Phicf での主張と同値・decide の負荷を下げる)。 -/
theorem F19_injective :
    ∀ m ∈ X3, ∀ m' ∈ X3, ∀ k k' : Fin 3,
      (canonX m, canonY m k) = (canonX m', canonY m' k') → m = m' ∧ k = k' := by decide +kernel

/-- F19 を Phicf(生成元像そのもの)でも直接確認する(F18 との整合の独立チェック)。 -/
theorem F19_injective_phicf :
    ∀ m ∈ X3, ∀ m' ∈ X3, ∀ k k' : Fin 3,
      (Phicf m k xb, Phicf m k yb) = (Phicf m' k' xb, Phicf m' k' yb) → m = m' ∧ k = k' := by
  decide +kernel

/-- **F20**: 12 個の Φ_{m,k} はいずれも E の全単射である(成分ごとの逆写像を明示 — 構造的)。
    v₁=v₂=u_m, v₃=1-2κ(m) はいずれも 𝒳₃ 上で 0 でない(gcd(2m+1,6)=1 が保証)ので F20_alpha_bij が使える。 -/
theorem F20_v_nonzero : ∀ m ∈ X3, um m ≠ 0 ∧ (1 - 2 * kappa3 m : Fin 3) ≠ 0 := by decide +kernel

/-- Φ_{m,k} の明示逆写像(成分ごとに F20_alpha_bij の逆を適用)。 -/
def PhicfInv (m : Fin 6) (k : Fin 3) : E → E := fun x =>
  (alpha (invF3 (um m)) (-(invF3 (um m) * (1 - 4 * k - um m))) x.1,
   alpha (invF3 (um m)) (-(invF3 (um m) * 0)) x.2.1,
   alpha (invF3 (1 - 2 * kappa3 m)) (-(invF3 (1 - 2 * kappa3 m) * 0)) x.2.2)

/-- **F20(全単射性の本体)**: PhicfInv は Phicf の両側逆(m ∈ 𝒳₃ の 12 個すべてで)。
    構造的証明ではなく `decide` で決着させる(E は 216 元・m,k は 12 通りのみで軽い)。 -/
theorem F20_bijective :
    ∀ m ∈ X3, ∀ k : Fin 3, ∀ x : E,
      PhicfInv m k (Phicf m k x) = x ∧ Phicf m k (PhicfInv m k x) = x := by decide +kernel

/-- Φ_{m,k} は各成分で e-flag(反射パリティのビット)を保つ(alpha の定義から構造的に明らか)。
    ゆえに par を保存し、G₃ = ker(par) を G₃ 自身へ全単射に写す(**F20 の「Aut(G₃) の元」部分**)。 -/
theorem F20_preserves_par : ∀ m : Fin 6, ∀ k : Fin 3, ∀ x : E, par (Phicf m k x) = par x := by
  intro m k x
  simp only [par, Phicf, alpha]
  cases x.1.2 <;> cases x.2.1.2 <;> cases x.2.2.2 <;> rfl

/-- F20 の帰結: Φ_{m,k} は G₃ を G₃ へ全単射に写す。 -/
theorem F20_maps_G3_to_G3 : ∀ m ∈ X3, ∀ k : Fin 3, ∀ x : E, inG x → inG (Phicf m k x) := by
  intro m _ k x hx
  unfold inG at *
  rw [F20_preserves_par]
  exact hx

#print axioms F16_alpha_hom
#print axioms F18_closed_form_matches
#print axioms F19_injective
#print axioms F19_injective_phicf
#print axioms F20_bijective
#print axioms F20_preserves_par
#print axioms F20_maps_G3_to_G3

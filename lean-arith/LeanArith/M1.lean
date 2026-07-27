import Mathlib.NumberTheory.NumberField.Basic
import Mathlib.RingTheory.Norm.Basic
import Mathlib.RingTheory.Norm.Transitivity
import Mathlib.RingTheory.IntegralClosure.IntegrallyClosed
import Mathlib.RingTheory.Polynomial.Basic

/-
LeanArith/M1.lean — 設計書 docs/lean/K3対応表_v0.md §5.1・§5.2 の M1(補題 NC・ノルム障害の一般形)。

M1 `β`(設計書 §5.1 の全文): **補題 NC(ノルム障害・一般形)**。K/ℚ を次数 d の数体、a ∈ ℤ、
p を自然数(応用では素数)とする。a が K で p 乗ならば、a^d は有理整数の p 乗である。

設計書の骨子どおりの statement(§5.1 のボックス・変更していない):
`theorem norm_obstruction {K} [Field K] [NumberField K] (a : ℤ) (p : ℕ) (x : K) (h : x^p = a) :
   ∃ n : ℤ, n^p = a^(Module.finrank ℚ K)`

**証明の骨格**(設計書 §5.1 の検討どおり):
① `x` は `X^p - C a`(モニック・ℤ 係数)の根 ⇒ `IsIntegral ℤ x`。
② ノルムの乗法性: `Algebra.norm ℚ (x^p) = (Algebra.norm ℚ x)^p`。
③ `Algebra.norm ℚ (a : K) = (a:ℚ)^(finrank ℚ K)`(`Algebra.norm_algebraMap`)。
④ 整な元のノルムは有理整数(`ℤ` が `ℚ` で整閉・`IsIntegrallyClosed`)⇒ ノルムを整数 `n` として取り出す。

**忠実性ノート(§0.3)**: 設計書のボックスは `p` に素数の制約を課していないので、本ファイルも
課さない(`p = 0` は退化ケースとして別途処理する)。系 NC-1/NC-2/NC-3(§5.1 (4))は
本補題の instantiate であり、本ファイルには含めない(別行・別コミットで扱う設計)。

**★【便 42・Sol Lean 設計監査(sol/sol_reply_42_final.md §F5)で PASS 確認】**
Sol の判定(表 D・M1 行・引用): 「**PASS**。`x^p=(a:K) ⇒ ∃n:ℤ, n^p=a^[K:ℚ]` は補題 NC と
1:1。`p` が素数でなく自然数でも真なので安全な強化。cast を明示し、`p=0` を処理すれば
空虚性はない」。**statement・証明とも変更不要(この便での修理事項なし)**。

**Mathlib API(推定・§9【GAP-L1】と同じ不確定要素)**: `Algebra.norm_algebraMap`・
`Algebra.isIntegral_norm`・`IsIntegrallyClosed.isIntegral_iff`・`map_pow` (`Algebra.norm` の
乗法性)。**いずれも実在は本セッションでは確認できていない(UNKNOWN)** — 本ファイルはその
「API 偵察」を兼ねる(設計書 §5・§7.3 の方針どおり)。
-/

open Polynomial

/-- **補題 NC(ノルム障害・一般形)**: 設計書 §5.1 のボックスと同一の statement。 -/
theorem norm_obstruction {K : Type*} [Field K] [NumberField K]
    (a : ℤ) (p : ℕ) (x : K) (h : x ^ p = (a : K)) :
    ∃ n : ℤ, n ^ p = a ^ (Module.finrank ℚ K) := by
  rcases Nat.eq_zero_or_pos p with hp0 | hp0
  · -- 退化ケース: p = 0 ⇒ x^0 = 1 = (a : K) ⇒ a = 1(単射な整数 → K の埋め込み)、
    -- 結論は n = 1 で自明に成り立つ。
    subst hp0
    simp only [pow_zero] at h
    have ha1 : a = 1 := by
      have : ((a : ℤ) : K) = ((1 : ℤ) : K) := by simpa using h.symm
      exact_mod_cast this
    exact ⟨1, by simp [ha1]⟩
  · -- 主ケース: p > 0。x は X^p - C a(モニック・ℤ 係数)の根 ⇒ ℤ 上整。
    have hmonic : (X ^ p - C a : ℤ[X]).Monic := Polynomial.monic_X_pow_sub_C a hp0.ne'
    have haeval : Polynomial.aeval x (X ^ p - C a : ℤ[X]) = 0 := by
      simp [h]
    have hint : IsIntegral ℤ x := ⟨X ^ p - C a, hmonic, haeval⟩
    have hnint : IsIntegral ℤ (Algebra.norm ℚ x) := Algebra.isIntegral_norm ℚ hint
    obtain ⟨n, hn⟩ := IsIntegrallyClosed.isIntegral_iff.mp hnint
    refine ⟨n, ?_⟩
    have hnp : Algebra.norm ℚ (x ^ p) = Algebra.norm ℚ x ^ p := map_pow (Algebra.norm ℚ) x p
    have hxp : Algebra.norm ℚ (x ^ p) = Algebra.norm ℚ ((a : K)) := by rw [h]
    have hcast : ((a : K)) = algebraMap ℚ K (a : ℚ) := by simp
    have ha : Algebra.norm ℚ ((a : K)) = (a : ℚ) ^ Module.finrank ℚ K := by
      rw [hcast, Algebra.norm_algebraMap]
    have hcast2 : algebraMap ℤ ℚ n = (n : ℚ) := eq_intCast (algebraMap ℤ ℚ) n
    have : (n : ℚ) ^ p = (a : ℚ) ^ Module.finrank ℚ K := by
      rw [← hcast2, hn, ← hnp, hxp, ha]
    exact_mod_cast this

#print axioms norm_obstruction

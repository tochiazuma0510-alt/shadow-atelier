import Mathlib.Data.ZMod.Basic

/-
LeanArith/F37.lean — 設計書 docs/lean/K3対応表_v0.md §4.8 表(F33–F37)の F37 行。

**★【便 42・Sol Lean 設計監査(sol/sol_reply_42_final.md §F4.2「F37」・§F6.1)を反映】**
設計表の F37 一行は実は三つの内容を含む(Sol の分割):

1. **F37a**(本ファイルが実装するのはこれだけ): `ZMod e` 上 `x ↦ r*x` が全単射
   `↔ Nat.Coprime r e`。抽象巡回群の初等命題。
2. **F37b**(★未実装): 共通の代数閉包内で `q_e : μ_M[e] →* μ_e`(`z ↦ z^r`)を
   **実際に構成**し、`e∣M`・`r=M/e`・`e>0` の下で `Function.Bijective q_e ↔ Nat.Coprime r e`
   から `MulEquiv` を得る(F37a を roots-of-unity へ typed instantiate する段)。
3. **F37c**(★未実装): coprime 時に `ι := q_e.symm.trans j`(`j` は F35 の一意な同型)を定義し、
   `q ∘ κ = q_e ∘ κe` を介して (7.5) を証明する。

**Sol の判定(引用)**: 「便 42 同梱時点の `LeanArith/F37.lean` が示した `ZMod` の全単射同値は
**F37a のみ**である。数学的な核として正しいが、抽象巡回群との同型をコメントで述べるだけでは
F37b の typed instantiation にならず、`ι` と (7.5) も含まない。従ってその定理が Lean を通っても
札は『F37a verified』までであり、『F37 verified』ではない」(§F4.2)。
**§F6.1 の確定条件どおり、本ファイルの定理は `F37a` としてのみ登録する。F37b・F37c は
別行・別ファイルとして今後実装する(未着手であって未証明ではない — §0.4 の「未着手」区分)。**

**忠実性ノート(§0.3)**:
- (δ2): 「同型」は Lean では「全単射な群準同型」ではなく、**台集合上の全単射**として述べる
  (z ↦ z^r が群準同型であることは自明なので、負荷は全単射性に集中させるのが忠実)。
- **Sol 指摘(§F4.2 末尾)**: `ZMod 0` は有限位数 0 の巡回群ではなく整数(`ℤ` と同型)である。
  本補題自体は `e = 0` でも命題として真(`ZMod.isUnit_iff_coprime` が `n=0` で一般に成立するため)
  だが、「有限巡回群 `ZMod e`」という**読み方**が成り立つのは `e > 0` のときだけであり、
  roots-of-unity への instantiate(F37b)側では `e > 0`(実際には `μ_M[e]` の位数が `e` になる
  ための `e ∣ M` も)が必須になる。**この行では statement を e=0 込みの一般形のまま残し、
  「e>0 でのみ『巡回群』と読める」という限定を docstring 側に明記する形で対応する**(Sol の
  指摘は instantiate 側の要件であり、本行の statement 自体を e>0 に絞ることを要求していない)。

**Mathlib API(実在をローカルビルドで確認済み)**: `ZMod.isUnit_iff_coprime`
(`Mathlib/Data/ZMod/Basic.lean`)・`IsUnit.isUnit_iff_mulLeft_bijective`
(`Mathlib/Algebra/Group/Units/Basic.lean`・`namespace IsUnit` に属する)。
-/

/-- **F37a**(F37 の三分割のうち第一のみ・§F4.2/§F6.1): `ZMod e` 上、乗法 `x ↦ r * x` が
    全単射であることは `Nat.Coprime r e` と同値である。**`e > 0` のときに限り**「位数 e の
    巡回群上 z ↦ z^r が自己同型 ⟺ gcd(r,e)=1」という読み方が成り立つ(`e = 0` では `ZMod 0 ≃ ℤ`
    であり巡回群ではない — 上の忠実性ノートどおり)。**F37b(roots-of-unity への typed
    instantiation)・F37c(ι の構成・(7.5))は未実装。** -/
theorem F37a_zmod_mul_bijective_iff_coprime (e r : ℕ) :
    Function.Bijective (fun x : ZMod e => (r : ZMod e) * x) ↔ Nat.Coprime r e := by
  rw [← IsUnit.isUnit_iff_mulLeft_bijective, ZMod.isUnit_iff_coprime]

#print axioms F37a_zmod_mul_bijective_iff_coprime

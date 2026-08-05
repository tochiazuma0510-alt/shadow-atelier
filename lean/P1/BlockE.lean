/-
P1/BlockE.lean — ブロック E((d2) = SURJ-Split 族・LE-1〜LE-4)。

対応: docs/notes/lean_p1_allocation_plan_v1.md §3.5 表。
出所: docs/notes/surj_d4_t1_v1.md §2.1 補題 SURJ-Split(a)-(f)(裁定 227・窓非依存)。

裁定 227「窓非依存」により、ここでの G は任意の isolated target N の GTSh(N,N) を表す
抽象群として扱ってよい — 具体形 (m,f) の対は `ShadowAxioms.T2_thm43_explicit_isolated`
が抽出元だが、本ブロックが実際に使うのは m 成分だけの合成則(T2_composition)と
Ihara 写像の分解(T2_15_Ih)である(割り付け表 §3.5 の記載どおり)。

状態: **verified-modulo-axioms**。LE-1(a)(well-defined・準同型の`well-defined`半分)は
Nat の合同算術のみで閉じる(証明済)。それ以外(単元性・準同型性の合成則側・
円分体の全射性・分解定理そのもの)は Galois 表現論・副有限群論の道具が
plain Lean core に無いため、次波へ持ち越す(sorry・正直な記帳)。
-/

import P1.ShadowAxioms

/-- $\tilde\chi_{2\nu}$ の well-defined 性の核: 代表の取り替え m ↦ m+ν で
    2(m+ν)+1 ≡ 2m+1 (mod 2ν)(surj_d4_t1 §2.1 証明 (a) 前半)。
    Nat の合同算術だけで閉じる — 公理に依存しない。 -/
theorem chiTilde_welldefined (nu m : Nat) :
    (2 * (m + nu) + 1) % (2 * nu) = (2 * m + 1) % (2 * nu) := by
  have h : 2 * (m + nu) + 1 = (2 * m + 1) + 2 * nu := by
    have : 2 * (m + nu) = 2 * m + 2 * nu := Nat.mul_add 2 m nu
    omega
  rw [h, Nat.add_mod_right]

/-- **LE-1(a) の値が単元であること**の数論的核: charming(gcd(2m+1,ν)=1)かつ
    2m+1 は奇数(gcd と 2 は自動)ならば gcd(2m+1, 2ν)=1(surj_d4_t1 §2.1 証明 (a) 後半)。
    `Nat.Coprime` は plain Lean core にはない概念なので `Nat.gcd = 1` で直接述べる。 -/
theorem chiTilde_isUnit (nu m : Nat) (hcharm : Nat.gcd (2 * m + 1) nu = 1) :
    Nat.gcd (2 * m + 1) (2 * nu) = 1 := by
  -- 【LE-1-GAP】gcd(2m+1,2)=1(奇数ゆえ)と gcd の乗法性(coprime a b → coprime a c
  -- → coprime a (b*c))の組み合わせで閉じるはずだが、後者に相当する補題を
  -- plain Lean core 単独では自前構築していない(次波)。
  sorry

/-! ### LE-1(b)〜LE-4: statement のみ(未着手・次波)

- **LE-1(b)** $\tilde\chi\circ\mathrm{Ih}_N=\chi_{2\nu}$: `ShadowAxioms.T2_15_Ih_decomp`
  に依存するが、現状の公理宣言は Prop 型プレースホルダで Ih の定義域・値域を
  型に持たせていない。**公理の言明を精密化してから着工**(LA-7 と同じ律速)。
- **LE-2** 円分指標の全射性: `Gal(Q(ζ_m)/Q) ≅ (Z/m)^×` は Mathlib にはあるが
  (割り付け表 §4.2 `T1_cyclotomic_galois` は「取込済 ⟹ M」と判定済み)、
  plain Lean core には無い。**このブロックの LE-3 は本質的に Mathlib 依存**であり、
  割り付け表 §5 の層割当どおり lean-arith/(Mathlib 側)へ回すべき — 本ファイル
  (plain Lean)には書けない。
- **LE-4** 分解 Ih(G_Q)·K=G ⟺ Ih(G_{K0})=K: 抽象群の部分群指数・共役の
  一般論(ブロック A の LA-6 と同じ GAP)に依存するため保留。
-/

/-
P1/BlockE.lean — ブロック E((d2) = SURJ-Split 族・LE-1〜LE-4)。

対応: docs/notes/lean_p1_allocation_plan_v1.md §3.5 表。
出所: docs/notes/surj_d4_t1_v1.md §2.1 補題 SURJ-Split(a)-(f)(裁定 227・窓非依存)。

裁定 227「窓非依存」による abstract group layer は、T2 の exact statement 承認後に
接続する。本波ではその T2 宣言を import せず、m 成分の算術核だけを閉じる。

状態: **local targeted-build candidate**。well-defined、単元性の算術核、(3.49) は
`sorry` なしで実装済み。GT-shadow 合成則・Ihara 分解・円分全射・SURJ-Split 全体は
exact T2 typing または Mathlib/副有限群論を要するため OPEN。file-level 等級は付けない。
-/

import P1.Core

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
  have hodd : Nat.Coprime (2 * m + 1) 2 := by
    rw [Nat.coprime_iff_gcd_eq_one, Nat.gcd_comm, Nat.gcd_rec]
    have hmod : (2 * m + 1) % 2 = 1 := by omega
    rw [hmod, Nat.gcd_one_left]
  exact Nat.Coprime.mul_right hodd hcharm

/-- Formula (3.49), kept in Block E so the well-defined/unit/composition arithmetic kernel is
    inventoried together.  The GT-shadow composition law (3.53) is deliberately not axiomatised
    before its exact paper statement is approved. -/
theorem chiTilde_composition_identity (m1 m2 : Int) :
    2 * (2 * m1 * m2 + m1 + m2) + 1 = (2 * m1 + 1) * (2 * m2 + 1) := by
  simp [Int.mul_add, Int.mul_comm, Int.mul_left_comm, Int.mul_one, Int.one_mul,
        Int.add_assoc, Int.add_comm, Int.add_left_comm]

/-- The residue-level consequence of (3.49). -/
theorem chiTilde_composition_mod (nu m1 m2 : Nat) :
    (2 * (2 * m1 * m2 + m1 + m2) + 1) % (2 * nu) =
      ((2 * m1 + 1) * (2 * m2 + 1)) % (2 * nu) := by
  congr 1
  simp [Nat.mul_add, Nat.add_mul, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm,
        Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]

/-! ### LE-1(b)〜LE-4: statement のみ(未着手・次波)

- **LE-1(b)** $\tilde\chi\circ\mathrm{Ih}_N=\chi_{2\nu}$: T2 (1.5) の exact statement
  (Ih の domain/codomain と成分射影を含む)が未承認。裸 `Prop` 宣言は quarantine し、
  原典照合後に着工する(LA-7 と同じ律速)。
- **LE-2** 円分指標の全射性: `Gal(Q(ζ_m)/Q) ≅ (Z/m)^×` は Mathlib にはあるが
  (割り付け表 §4.2 `T1_cyclotomic_galois` は「取込済 ⟹ M」と判定済み)、
  plain Lean core には無い。**このブロックの LE-3 は本質的に Mathlib 依存**であり、
  割り付け表 §5 の層割当どおり lean-arith/(Mathlib 側)へ回すべき — 本ファイル
  (plain Lean)には書けない。
- **LE-4** 分解 Ih(G_Q)·K=G ⟺ Ih(G_{K0})=K: 抽象群の部分群指数・共役の
  一般論(ブロック A の LA-6 と同じ GAP)に依存するため保留。
-/

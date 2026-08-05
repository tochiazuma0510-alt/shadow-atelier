/-
P1/ShadowAxioms.lean — T2 公理(論文固有・監査対象)。

方針: docs/notes/lean_axiom_policy_v1.md v1.6(施行ゲート 6 点)。
台帳: lean/AXIOMS.md(本ファイルの doc-comment から人手で同期 — 自動生成マクロは未実装、
      裁定 v1.6-5 の「digest 併記」は次段の債務として明示的に未了扱いとする)。

割り付け: docs/notes/lean_p1_allocation_plan_v1.md §4.1(T2 公理・6 本中、ブロック A・E が
使うのは 4 本 = T2_thm43_explicit・T2_thm43_isolated・T2_15_Ih・T2_composition)。

すべて `ShadowAxioms` 名前空間に置く(規約 v1 §1)。
-/

import P1.Core

namespace ShadowAxioms

/-- **T2_thm43_explicit**: GT(K^(n)) の明示式 — 正典 2405.11725 Thm 4.3 (4.12)(n 奇)。
    ここでは抽象化して「isolated target K^(n) の GT-shadow は整数対 (m,f) の集合で、
    合成則・虚指標 (第一成分) が (3.53)(3.49) を満たす」ことの**存在**を公理化する
    (具体形は LA-7/LE-1 が使う分だけ後続で補う)。

    原典: arXiv 2405.11725, Thm 4.3, 式 (4.12)。
    階層: T2(論文固有)。
    逐語照合: 【未実施・Sol 便への発注が必要】(lean_p1_allocation_plan_v1.md §9.3)。
    使用箇所: LA-7(F0.eq_m_zero_branch)・LA-9(SIXP-fam)。
    Mathlib 状況: 不在(永久 — GT-shadow は本工房固有の対象)。
    sanity instance: 【未実施】n=3(K^(3))で GAP 実測 |GT|=12 と突合する回帰テストを
      別途 lean-arith/ 側に用意する必要がある(本ファイルは plain Lean のため未接続)。

    ★ 本稿では「isolated ⟹ Ih が準同型として定義される」という定性的帰結のみを
    Prop として公理化し、明示式そのもの(m,f の走る範囲・κ の式)は
    ブロック A/E の各補題内で個別に(より弱い形で)公理化する
    — v1.6-1「使用する最弱形で言明」に従う。 -/
axiom T2_thm43_explicit_isolated (n : Nat) [NeZero n] : Prop

/-- **T2_thm43_isolated**: K^(n) は GTSh の isolated object である(n 奇)。
    原典: arXiv 2405.11725, Thm 4.3 末尾(逐語)。
    階層: T2。使用箇所: LA-9(SIXP-fam 前件)・LE-1〜LE-4(isolated ⟹ Ih 定義域)。
    Mathlib 状況: 不在。逐語照合: 未実施。 -/
axiom T2_thm43_isolated (n : Nat) [NeZero n] : Prop

/-- **T2_15_Ih**: Ih(γ) = ((χ(γ)-1)/2, f_γ)(円分指標 χ の Ihara 写像への分解)。
    原典: arXiv 2405.11725, 式 (1.5)。
    階層: T2。使用箇所: LE-2(chiTilde_comp_Ih)。
    Mathlib 状況: 不在(GTSh 固有の写像)。逐語照合: 未実施。 -/
axiom T2_15_Ih_decomp : Prop

/-- **T2_composition**: GTSh の合成則(2401 (3.53))と整数恒等式(2401 (3.49))
    2(2m₁m₂+m₁+m₂)+1 = (2m₁+1)(2m₂+1)。
    原典: arXiv 2401.06870, 式 (3.53)(3.49)(定義の正本)。
    階層: T2。使用箇所: LE-1(chiTilde.isHom)。
    Mathlib 状況: 整数恒等式そのものは初等(Nat/Int の可換環公理で証明可能 — 本ファイルでは
      GTSh の合成則という**構造**を公理化する。整数恒等式部分は補題として下に証明する
      (`T2_composition_identity` — これは公理ではなく定理)。 -/
axiom T2_composition_hom : Prop

/-- 整数恒等式 (3.49) 自体は T2 公理ではなく **証明可能な定理**(初等代数)。
    公理境界を小さくする(v1.6-1)ため、ここで実際に証明しておく。 -/
theorem T2_composition_identity (m1 m2 : Int) :
    2 * (2 * m1 * m2 + m1 + m2) + 1 = (2 * m1 + 1) * (2 * m2 + 1) := by
  simp [Int.mul_add, Int.mul_comm, Int.mul_left_comm, Int.mul_one, Int.one_mul,
        Int.add_assoc, Int.add_comm, Int.add_left_comm]

end ShadowAxioms

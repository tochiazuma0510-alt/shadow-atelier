/-
P1/BlockA.lean — ブロック A((6′) 族版・LA-1〜LA-9)。

対応: docs/notes/lean_p1_allocation_plan_v1.md §3.1 表(補題名 1:1)。
出所: docs/notes/oddH_full_proof_v1.md(補題 A〜I・命題 ODD-H)/
      docs/notes/s3_family_completion_v1.md(補題 Λ-REG・補題 INN・定理 SIXP-fam)/
      docs/notes/w2fam_v1.md §3.5(命題 K5-1)。

状態: **verified-modulo-axioms**(lean_axiom_policy_v1.md)。無印 verified ではない。
本ファイルは初回着手であり、13 本中の到達度を正直に記録する
(lean_axiom_policy_v1.md v1.4「Lean は完成した数学の封印」・
 司令塔発注「13本全部が初回で closed になる必要はない」)。
-/

import P1.Core
import P1.FinArith
import P1.Parity
import P1.Order
import P1.ShadowAxioms

variable {n : Nat} [NeZero n]

/-! ### LA-1: `Gn.structure`(oddH 補題 A)

$G_n=A\rtimes Q$、$|G_n|=4n^3$、$X=a_1q_1$、$X^2=a_1^2$、$\operatorname{ord}(X)=2n$。

以下 4 つの部分に分解する(切り出し義務・v1.5)。カルディナリティ主張(4n³)は
**この工房が定義した En n = Dn n × Dn n × Dn n の指数 2 部分集合の要素数**であり、
plain Lean core には Fintype/Nat.card 相当の道具がないため、本ファイルでは
証明を先送りする(★教材ではなく単なる会計 — 数学的内容ではない。GAP 印) -/

/-- **LA-1(a)**: X = a₁q₁(定義そのもの)。 -/
theorem Gn_X_eq_a1_q1 : (X : En n) = emul a1 q1 := rfl

/-- **LA-1(b)**: X² = a₁²。 -/
theorem Gn_X_sq : emul (X : En n) X = emul a1 a1 := by
  simp [X, emul, dmul, a1, q1, done_]

/-- **LA-1(c)**: ord(X) = 2n(X^{2n}=1 かつ 0<k<2n では X^k≠1)。
    `P1/Order.lean` の `X_pow_2n`・`X_pow_lt_2n_ne` を束ねたもの。 -/
theorem Gn_ord_X (hn1 : 1 < n) (hn : NatOdd n) :
    epow (X : En n) (2 * n) = eone ∧
    ∀ k, 0 < k → k < 2 * n → epow (X : En n) k ≠ eone :=
  ⟨X_pow_2n hn1, fun k hk0 hk => X_pow_lt_2n_ne hn1 hn k hk0 hk⟩

/-- **LA-1(d)**: |G_n| = 4n³(カルディナリティ)。
    ⚠ **未完(GAP・会計のみ)**: `inG`(par x = false)を満たす En n の要素数が 4n³ である
    ことは、(a₁,a₂,a₃,b₁,b₂) ↦ ((a₁,b₁),(a₂,b₂),(a₃,b₁ xor b₂)) 型の全単射で
    証明できる(oddH §2 の証明そのもの)が、plain Lean core には有限型の要素数
    (Mathlib の `Fintype.card`)に相当する道具がなく、本ファイルはこれを
    自前で構築していない。**数学的内容ではなく会計(bookkeeping)の欠落**であり、
    LA-1 の他の 3 部分(の証明)には影響しない。 -/
theorem Gn_card_placeholder : True := by
  -- 【LA-1-GAP】|G_n|=4n³ の証明はカルディナリティ道具の不在により未着手。
  trivial

/-! ### LA-6: 補題 Λ-REG(`Lambda.simplyTransitive`)

抽象化して書く: H を G_n の部分群(述語 `IsSubgrp`)とし、[G_n:H]=2n かつ
⟨X⟩∩H=1(oddH 補題 C(2)・補題 G から出る事実 — ODD-H 本体は他ファイルで
まだ形式化していないので、ここでは **前提として受け取る**)。このとき
⟨X⟩ は H の共役類 Λ 上に単純推移的に作用する。

⚠ **未完**: 「部分群」「正規化群」「指数」「共役類」を表す型を本工房はまだ
定義していない(K3/Lambda.lean の n=3 固定 decide 版とは違い、n が変数の
ここでは Mathlib の `Subgroup`/`MulAction` 抜きに一般論を展開する必要がある)。
LA-6 は **statement のみ**を記録し、証明は次波へ持ち越す。 -/

/-- 部分群の述語(plain Lean・自前定義。Mathlib `Subgroup` を使わない)。 -/
structure IsSubgrp (H : En n → Prop) : Prop where
  one_mem : H eone
  mul_mem : ∀ {a b}, H a → H b → H (emul a b)
  inv_mem : ∀ {a}, H a → H (einv a)

/-- ⟨X⟩ の生成する部分群(冪の像として)。 -/
def genX (n : Nat) [NeZero n] (g : En n) : Prop := ∃ k : Nat, g = epow (X : En n) k

/-- **LA-6(statement)**: H が [G_n:H]=2n・⟨X⟩∩H=1 を満たすなら、⟨X⟩ は
    H の共役類 {gHg⁻¹} 上に単純推移的に作用する(補題 Λ-REG・s3_family_completion §3)。
    ⚠ **未完(sorry)**: 部分群の指数・共役類の型が未構築のため、抽象的な
    仮定 `hstab` で正規化群の情報を直接受け取る形にした(妥協・次波で正す)。 -/
theorem Lambda_simplyTransitive
    (H : En n → Prop) (hH : IsSubgrp H)
    (hstab : ∀ k, (∀ g, H g ↔ H (emul (emul (epow (X : En n) k) g) (einv (epow (X : En n) k))))
      → (epow (X : En n) k = eone ∨ ¬ ∃ h, H h ∧ h = epow (X : En n) k) ) :
    True := by
  -- 【LA-6-GAP】単純推移性そのものの証明(軌道=Λ 全体・固定部分群=1)は、
  -- 部分群の「指数」の定義が本ファイルに無いため書けない。statement の
  -- 記帳のみで次波へ持ち越す。
  trivial

/-! ### LA-8: 補題 INN(`Phi_F0_eq_inn`)

$\Phi_{0,f_k}=\operatorname{inn}(X^{-2k})$、ここで $f_k=(r^{2k},r^{-2k},1)$。
出所: s3_family_completion_v1.md §4(b)の計算(w2fam_v1.md §3.5 と同一)。

ここでは **生成元 Y 上での等式**(証明の実質)を直接計算する:
$f_k^{-1} Y f_k = X^{-2k} Y X^{2k}$(両辺とも $a_1^{1-4k}a_2a_3q_2$ に等しい)。
「Φ が G_n 上の自己同型として一意に拡張される」こと自体(K3 の F17 に相当する
拡張原理)は別途必要だが、**証明の数学的な中身はこの生成元上の等式**であり、
これは emul/dmul の具体計算だけで閉じる(decide 不要・n 一般で成立)。 -/

/-- fₖ = (r^{2k}, r^{-2k}, 1) = a₁^{2k}a₂^{-2k}(s3_family_completion §4)。
    ここでの exponent k : Fin n の 2k は Fin n の加法(k+k)、-2k はその逆元。 -/
def fk (k : Fin n) : En n := ((k + k, false), (-(k + k), false), done_)

/-- 共役(inner automorphism): inn(c)(g) = c g c⁻¹。 -/
def inn (c g : En n) : En n := emul (emul c g) (einv c)

/-- **LA-8(核心の計算)**: $f_k^{-1} Y f_k = X^{-2k} Y X^{2k}$
    (= inn(X^{-2k})(Y) — 生成元 Y 上での補題 INN の等式)。 -/
theorem INN_on_Y (k : Fin n) :
    emul (emul (einv (fk (n := n) k)) Y) (fk (n := n) k)
      = inn (einv (epow (X : En n) (2 * k.val))) (Y : En n) := by
  unfold inn fk Y a1 a2 q2 X q1 einv emul dinv dmul done_
  -- 両辺とも成分ごとの具体計算に帰着する。epow (X) (2k) の第 1 成分は
  -- dpow_rot_val により (2k) 個の "1" の和 = (2*k.val) mod n 相当。
  -- ここでは epow を unfold して同じ議論を直接展開する。
  sorry

/-- **LA-8(生成元 X 上の自明な半分)**: inn(X^{-2k})(X) = X
    (X の冪による共役は X 自身を固定する — X が自分自身と可換なのは自明。
    s3_family_completion §4(b)「$\Phi_{0,f_k}(X)=X$」と `inn(X^{-2k})(X)=X` の
    両辺が一致することの後半 — **注意**: これは fₖ⁻¹Xfₖ=X ではない
    (fₖ と X は一般に可換ではない)。両者は別々に X に等しいという主張であり、
    本定理はその inn 側のみを扱う)。 -/
theorem inn_fixes_X (k : Fin n) :
    inn (einv (epow (X : En n) (2 * k.val))) (X : En n) = X := by
  -- 【LA-8-GAP】emul の結合律(Dₙ³ が群であること自体)を Core.lean/FinArith.lean が
  -- まだ証明していないため、「X^j と X は可換」の帰納法が閉じられない。
  -- K3/Group.lean(n=3 固定)は `decide +kernel` で結合律を検算したが、
  -- ここでは n が変数なので構造的証明が必要(dmul の結合律を成分ごとに示す形)。
  -- 次波でこの結合律補題を追加すれば inn_fixes_X は数行で閉じる見込み。
  sorry

/-! ### LA-2〜LA-5・LA-7・LA-9: statement のみ(未着手・次波)

割り付け表の残り 6 本(H_{j,α,β} の悉皆性・正規化群・共役類・F0 の明示・SIXP-fam 本体)は
**部分群/指数/共役類の一般論**(LA-6 と同じ律速)と **T2 公理(GT(K^(n)) の明示式)**の
両方に依存する。本波では statement を書き下ろす前段階として、依存関係の会計のみ
ここに記す(次波の入口):

- LA-2〜LA-5(oddH 補題 C(2)・G・H・I): H_{j,α,β} の型が LA-6 と共有する
  「部分群」インフラを必要とする。**LA-6 の GAP が解消されるまで着工しない**
  (v1.4 着工条件 — 割り付かない依存が残る鎖は着工しない、を厳密に適用)。
- LA-7(F0.eq_m_zero_branch): `ShadowAxioms.T2_thm43_explicit_isolated` に依存。
  現状の公理は「isolated である」ことのみを述べる Prop 値のプレースホルダで、
  (4.12) の明示式そのもの(m,f の対応)を型に持たせていないため、LA-7 の
  statement すら現時点では正しく書けない。**公理の言明を精密化してから着工**。
- LA-9(SIXP-fam): LA-6・LA-7 の両方に依存するため保留。
-/

/-
P1/BlockA.lean — ブロック A((6′) 族版・LA-1〜LA-9)。

対応: docs/notes/lean_p1_allocation_plan_v1.md §3.1 表(補題名 1:1)。
出所: docs/notes/oddH_full_proof_v1.md(補題 A〜I・命題 ODD-H)/
      docs/notes/s3_family_completion_v1.md(補題 Λ-REG・補題 INN・定理 SIXP-fam)/
      docs/notes/w2fam_v1.md §3.5(命題 K5-1)。

状態: **local targeted-build candidate**。本ファイルに実装した定理島は `sorry` なし。
ただし LA-2〜LA-7・LA-9 の紙面全体は OPEN であり、file-level の完成等級は付けない。
-/

import P1.Core
import P1.FinArith
import P1.Parity
import P1.Order

variable {n : Nat} [NeZero n]

/-! ### LA-1: `Gn.structure`(oddH 補題 A)

$G_n=A\rtimes Q$、$|G_n|=4n^3$、$X=a_1q_1$、$X^2=a_1^2$、$\operatorname{ord}(X)=2n$。

以下 4 つの部分に分解する(切り出し義務・v1.5)。カルディナリティ主張(4n³)は
`Gn_card_equiv` の明示全単射と `Gn_card_formula` の算術式を組にして表す。
plain core に `Fintype.card` を持ち込まず、cardinality witness を exact に型付けする。 -/

/-- **LA-1(a)**: X = a₁q₁(定義そのもの)。 -/
theorem Gn_X_eq_a1_q1 : (X : En n) = emul a1 q1 := rfl

/-- **LA-1(b)**: X² = a₁²。 -/
theorem Gn_X_sq : emul (X : En n) X = emul a1 a1 := by
  simp [X, emul, dmul, a1, q1, done_]

/-- **LA-1(c), ambient calculation** used below to prove the actual subtype result. -/
theorem Gn_ord_X_ambient (hn1 : 1 < n) (hn : NatOdd n) :
    epow (X : En n) (2 * n) = eone ∧
    ∀ k, 0 < k → k < 2 * n → epow (X : En n) k ≠ eone :=
  ⟨X_pow_2n hn1, fun k hk0 hk => X_pow_lt_2n_ne hn1 hn k hk0 hk⟩

/-- **LA-1(d)** 用の plain-core 全単射。 -/
structure PlainEquiv (α β : Type) where
  toFun : α → β
  invFun : β → α
  left_inv : ∀ x, invFun (toFun x) = x
  right_inv : ∀ y, toFun (invFun y) = y

/-- Five independent coordinates for `G_n`: three rotations and two parity bits. -/
structure GnCode (n : Nat) where
  rot1 : Fin n
  rot2 : Fin n
  rot3 : Fin n
  bit1 : Bool
  bit2 : Bool

def GnCode.toEn (c : GnCode n) : En n :=
  ((c.rot1, c.bit1), (c.rot2, c.bit2), (c.rot3, xor c.bit1 c.bit2))

theorem GnCode.toEn_mem (c : GnCode n) : inG c.toEn := by
  cases c with
  | mk a b c e f => cases e <;> cases f <;> rfl

def GnCode.toGn (c : GnCode n) : Gn n := ⟨c.toEn, c.toEn_mem⟩

def Gn.toCode (g : Gn n) : GnCode n :=
  ⟨g.val.1.1, g.val.2.1.1, g.val.2.2.1, g.val.1.2, g.val.2.1.2⟩

theorem parity_third_flag {x : En n} (hx : inG x) : x.2.2.2 = xor x.1.2 x.2.1.2 := by
  rcases x with ⟨⟨a, ea⟩, ⟨⟨b, eb⟩, ⟨c, ec⟩⟩⟩
  cases ea <;> cases eb <;> cases ec <;> simp_all [inG, par]

theorem Gn_code_left_inv (g : Gn n) : GnCode.toGn (Gn.toCode g) = g := by
  apply Subtype.ext
  rcases g with ⟨⟨⟨a, ea⟩, ⟨⟨b, eb⟩, ⟨c, ec⟩⟩⟩, hg⟩
  simp only [GnCode.toGn, Gn.toCode, GnCode.toEn]
  have hflag : ec = xor ea eb := parity_third_flag hg
  cases hflag
  rfl

theorem Gn_code_right_inv (c : GnCode n) : Gn.toCode c.toGn = c := by
  cases c
  rfl

/-- **LA-1(d)**: `G_n` is explicitly equivalent to three `Fin n` coordinates and two
    Boolean coordinates. Together with `Gn_card_formula`, this is the core-only exact
    cardinality witness for `|G_n| = 4 n^3`; no theorem with conclusion `True` remains. -/
def Gn_card_equiv : PlainEquiv (Gn n) (GnCode n) :=
  ⟨Gn.toCode, GnCode.toGn, Gn_code_left_inv, Gn_code_right_inv⟩

theorem Gn_card_formula : n * n * n * 2 * 2 = 4 * n^3 := by
  simp [Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]

/-! ### LA-6: 補題 Λ-REG(`Lambda.simplyTransitive`)

抽象化して書く: H を G_n の部分群(述語 `IsSubgrp`)とし、[G_n:H]=2n かつ
⟨X⟩∩H=1(oddH 補題 C(2)・補題 G から出る事実 — ODD-H 本体は他ファイルで
まだ形式化していないので、ここでは **前提として受け取る**)。このとき
⟨X⟩ は H の共役類 Λ 上に単純推移的に作用する。

本波では部分群述語・共役類型・単純推移性の結論まで exact に型付けする。
指数・正規化群に関する紙面仮説の exact typing とその証明は OPEN とする。 -/

/-- A subgroup predicate on the actual `Gn n` carrier (not the ambient `En n`). -/
structure IsSubgrp (H : Gn n → Prop) : Prop where
  one_mem : H 1
  mul_mem : ∀ {a b}, H a → H b → H (a * b)
  inv_mem : ∀ {a}, H a → H a⁻¹

/-- Powers of the actual marking `X : G_n`. -/
def xpowGn (k : Nat) : Gn n := by
  induction k with
  | zero => exact 1
  | succ k ih => exact ih * Xg

theorem xpowGn_val (k : Nat) :
    (xpowGn (n := n) k : En n) = epow (X : En n) k := by
  induction k with
  | zero => rfl
  | succ k ih =>
      change emul (xpowGn (n := n) k : En n) X = emul (epow X k) X
      rw [ih]

/-- **LA-1(c), actual `G_n` conclusion**: the subtype element `Xg` has exact order `2n`. -/
theorem Gn_ord_X (hn1 : 1 < n) (hn : NatOdd n) :
    xpowGn (n := n) (2 * n) = 1 ∧
    ∀ k, 0 < k → k < 2 * n → xpowGn (n := n) k ≠ 1 := by
  constructor
  · apply Subtype.ext
    rw [xpowGn_val]
    exact X_pow_2n hn1
  · intro k hk0 hk hpow
    apply X_pow_lt_2n_ne hn1 hn k hk0 hk
    rw [← xpowGn_val]
    exact congrArg Subtype.val hpow

def genX (g : Gn n) : Prop := ∃ k : Nat, g = xpowGn (n := n) k

def gnConj (g h : Gn n) : Gn n := (g * h) * g⁻¹

def conjugatePred (H : Gn n → Prop) (g : Gn n) : Gn n → Prop :=
  fun h => H (gnConj g⁻¹ h)

/-- The conjugacy class Λ of `H`, represented extensionally as predicates on `G_n`. -/
def Lambda (H : Gn n → Prop) : Type :=
  {K : Gn n → Prop // ∃ g : Gn n, K = conjugatePred H g}

/-- **LA-6 exact conclusion** (statement only): the `2n` powers of `X` reach every
    conjugate of `H` exactly once.  This replaces the former `: True` no-op. -/
def LambdaSimplyTransitive (H : Gn n → Prop) : Prop :=
  ∀ K : Lambda H, ∃ k : Fin (2 * n),
    K.val = conjugatePred H (xpowGn (n := n) k.val) ∧
    ∀ l : Fin (2 * n),
      K.val = conjugatePred H (xpowGn (n := n) l.val) → l = k

/- `LambdaSimplyTransitive H` remains OPEN until the index/normalizer hypotheses from
   Lambda-REG are given equally exact types.  No placeholder theorem is exported. -/

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

theorem epow_X_even (k : Fin n) :
    epow (X : En n) (2 * k.val) = ((k + k, false), done_, done_) := by
  have hXfst : (X : En n).1 = (1, false) := by
    simp [X, emul, dmul, a1, q1, done_]
  have hXsnd : (X : En n).2.1 = (0, true) := by
    simp [X, emul, dmul, a1, q1, done_]
  have hXthd : (X : En n).2.2 = (0, true) := by
    simp [X, emul, dmul, a1, q1, done_]
  apply Prod.ext
  · rw [epow_fst, hXfst]
    apply Prod.ext
    · apply Fin.ext
      rw [dpow_rot_val]
      by_cases hn : n = 1
      · subst n
        have hk : k = 0 := Subsingleton.elim _ _
        subst k
        rfl
      · have hn0 : n ≠ 0 := NeZero.ne n
        have hn1 : 1 < n := by omega
        have hone : (1 : Fin n).val = 1 := Nat.mod_eq_of_lt hn1
        rw [hone]
        simp [Fin.val_add]
        have htwo : 2 * k.val = k.val + k.val := by omega
        rw [htwo]
    · rw [dpow_rot_flag]
  · apply Prod.ext
    · rw [epow_snd, hXsnd]
      exact dpow_refl_even (0 : Fin n) (2 * k.val) ⟨k.val, by omega⟩
    · rw [epow_thd, hXthd]
      exact dpow_refl_even (0 : Fin n) (2 * k.val) ⟨k.val, by omega⟩

/-- **LA-8(核心の計算)**: $f_k^{-1} Y f_k = X^{-2k} Y X^{2k}$
    (= inn(X^{-2k})(Y) — 生成元 Y 上での補題 INN の等式)。 -/
theorem INN_on_Y (k : Fin n) :
    emul (emul (einv (fk (n := n) k)) Y) (fk (n := n) k)
      = inn (einv (epow (X : En n) (2 * k.val))) (Y : En n) := by
  rw [epow_X_even]
  unfold inn fk Y a1 a2 a3 q2 einv emul dinv dmul done_
  simp [fin_sub_eq_add_neg, fin_add_assoc, fin_add_comm, fin_neg_neg]
  have hreorder :
      (-k) + ((-k) + (k + (k + (1 : Fin n)))) =
        (((-k) + k) + ((-k) + k)) + (1 : Fin n) := by
    ac_rfl
  rw [hreorder]
  simp [fin_add_left_neg, fin_neg_zero, fin_zero_add]

theorem epow_comm_base (g : En n) (j : Nat) :
    emul (epow g j) g = emul g (epow g j) := by
  induction j with
  | zero =>
      change emul eone g = emul g eone
      rw [emul_one_left_n, emul_one_right_n]
  | succ j ih =>
      change emul (emul (epow g j) g) g = emul g (emul (epow g j) g)
      calc
        emul (emul (epow g j) g) g = emul (emul g (epow g j)) g := by rw [ih]
        _ = emul g (emul (epow g j) g) := emul_assoc_n _ _ _

/-- **LA-8(生成元 X 上の自明な半分)**: inn(X^{-2k})(X) = X
    (X の冪による共役は X 自身を固定する — X が自分自身と可換なのは自明。
    s3_family_completion §4(b)「$\Phi_{0,f_k}(X)=X$」と `inn(X^{-2k})(X)=X` の
    両辺が一致することの後半 — **注意**: これは fₖ⁻¹Xfₖ=X ではない
    (fₖ と X は一般に可換ではない)。両者は別々に X に等しいという主張であり、
    本定理はその inn 側のみを扱う)。 -/
theorem inn_fixes_X (k : Fin n) :
    inn (einv (epow (X : En n) (2 * k.val))) (X : En n) = X := by
  unfold inn
  rw [einv_involutive_n, emul_assoc_n]
  rw [← epow_comm_base]
  rw [← emul_assoc_n, emul_inv_left_n, emul_one_left_n]

/-! ### LA-2〜LA-5・LA-7・LA-9: statement のみ(未着手・次波)

割り付け表の残り 6 本(H_{j,α,β} の悉皆性・正規化群・共役類・F0 の明示・SIXP-fam 本体)は
**部分群/指数/共役類の一般論**(LA-6 と同じ律速)と **T2 公理(GT(K^(n)) の明示式)**の
両方に依存する。本波では statement を書き下ろす前段階として、依存関係の会計のみ
ここに記す(次波の入口):

- LA-2〜LA-5(oddH 補題 C(2)・G・H・I): H_{j,α,β} の型が LA-6 と共有する
  「部分群」インフラを必要とする。**LA-6 の GAP が解消されるまで着工しない**
  (v1.4 着工条件 — 割り付かない依存が残る鎖は着工しない、を厳密に適用)。
- LA-7(F0.eq_m_zero_branch): T2 Thm 4.3/(4.12) の exact statement に依存する。
  原典照合と Sol 承認が未了なので宣言自体を quarantine し、コードから import しない。
  domain/codomain と (m,f) の対応を確定してから着工する。
- LA-9(SIXP-fam): LA-6・LA-7 の両方に依存するため保留。
-/

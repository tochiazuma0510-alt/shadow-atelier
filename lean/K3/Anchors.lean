/-
K3/Anchors.lean — Sol Lean 忠実性監査(sol/sol_reply_33_lean.md)の必須修理 P1・P2。

新規ファイルとして分離する(Bridge.lean は無変更 — 触ると重い悉皆 `decide` の
再エラボレートが走るため)。P1・P2 とも「現行定義について真」と監査済みであり、
ここでは statement を追加するのみ。

P1(§「必須修理」・アンカー §F4「不足」): `allT` の列挙が重複を持たないことを
`Nodup` として固定する。既存 `allT_complete`・`T_card` と合わせて初めて
completeness + Nodup + length の三脚が揃い、|T|=12 が plain Lean の列挙語彙で閉じる
(★教材 1)。

P2(§「必須修理」): `Bool × Bool` と (Z/12)^× の対応をリテラルで pin する
`decodeChi` を定義し、`chiT ∘ param` が `chiVal` と**ラベル付きの値として**
一致することを述べる。既存 `T_chi_is_chiVal`(ファイバー一致のみ)はそのまま系として残す。
-/

import K3.Counting
import K3.Bridge

/-- **P1**: `allT` の列挙は重複を持たない。`allT_complete`・`T_card` と合わせて
    |T|=12 が completeness + Nodup + length の三脚で閉じる(sol_reply_33_lean.md §必須修理 P1)。
    `decide +kernel`(12 元の相異判定、瞬時)。 -/
theorem allT_nodup : allT.Nodup := by decide +kernel

/-- **P2**: `Bool × Bool` から (Z/12)^× ⊂ Fin 12 への decoder を
    sol_reply_33_lean.md の指定リテラルで pin する。
    (false,false)↦1, (true,true)↦5, (false,true)↦7, (true,false)↦11。 -/
def decodeChi : Bool × Bool → Fin 12
  | (false, false) => 1
  | (true, true) => 5
  | (false, true) => 7
  | (true, false) => 11

/-- **P2**: `decodeChi (chiT (param m k)) = chiVal m` — 紙のラベル付き円分指標
    \(\widetilde\chi(m,k) = 2m+1 \pmod{12}\) の exact statement(sol_reply_33_lean.md §必須修理 P2)。
    既存 `T_chi_is_chiVal`(ファイバー一致)はこの系として残す。
    `decide +kernel`(4×3=12 通り、瞬時)。 -/
theorem chi_exact : ∀ m ∈ X3, ∀ k : Fin 3,
    decodeChi (chiT (param m k)) = chiVal m := by decide +kernel

/-- **系**: `chi_exact` から旧 `T_chi_is_chiVal`(ファイバー一致)を復元できることの確認
    (decoder が単射であるため、ラベル付き一致はファイバー一致より真に強い)。 -/
theorem chi_exact_implies_fiber : ∀ m ∈ X3, ∀ m' ∈ X3, ∀ k k' : Fin 3,
    (chiT (param m k) = chiT (param m' k')) ↔ chiVal m = chiVal m' :=
  T_chi_is_chiVal

#print axioms allT_nodup
#print axioms chi_exact

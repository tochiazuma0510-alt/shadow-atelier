import Mathlib.GroupTheory.OrderOfElement
import Mathlib.Data.ZMod.QuotientGroup

/-
LeanArith/M6pp.lean — 設計書 docs/lean/K3対応表_v0.md §5.2 表の M6″ 行(便 29 P4 の逆向き)。

M6″ `β`(設計書の全文): **一般 Kummer 補題・必要方向**。μ_M ⊂ K、v ∈ K^×、e := ord([v]_M)、
r := M/e、d := gcd(e,r) > 1 ⇒ ある a ∈ K^×, ξ ∈ μ_M で v = (aξ)^r (7.2′)、ゆえに
ord([v]_e) ∣ e/d < e、したがって [K(v^{1/e}):K] < [K(v^{1/M}):K] で両体は一致しない。

**★ 本ファイルのスコープについて(司令塔への報告事項・実装で狭めた点)**:
設計書は M6″ の「鍵」を次のように名指ししている(§5.2 表 M6″ 行・Mathlib API 欄):
「μ_M→μ_e, ξ↦ξ^r は全射(像の位数 = M/gcd(M,r) = e)・巡回群の位数 e の部分群は一意」。
**本ファイルはこの「鍵」(巡回群の初等命題)だけを Mathlib で実装する**。
M6″ 本体の体拡大の主張(`¬ (K⟮v^(1/e)⟯ = K⟮v^(1/M)⟯)`)— Kummer 拡大の次数計算・
`K⟮·⟯` の構成・M6′ への依存を含む — は**未実装**(§5.2 の M6′ 自体が Kummer 理論の
Mathlib API 被覆を UNKNOWN と明記しており、本ファイル単独ではその依存を解消できない)。

**★【便 42・Sol Lean 設計監査(sol/sol_reply_42_final.md §F5・§F6.2)で確認】**
Sol の判定(表 D・M6″ 行・引用): 「**FAIL(核だけへの縮小不可)**。最終の field inequality
だけでも紙面の (7.2′)・order drop を覆わない。`∃a∈K×,∃ξ∈μ_M,v=(aξ)^r`、
`ord_e([v])∣e/gcd(e,r)<e`、二次数の不等式、体の不一致を分割して全て残す。**着工済みの
`orderOf(g^r)=M/gcd(M,r)` は有用な補助補題だが M6″ 本体ではない**。また抽象版には
`M>0`/有限位数を入れ、`M=0` の無限位数ケースを混ぜない」。
**§F6.2 の確定条件どおり、本ファイルの 2 定理は `M6″-core` としてのみ登録する
(`M6″` そのものの verified 札には使わない)**。`[Finite G]` を両定理に付けているのは
Sol 指摘の「`M=0` の無限位数ケースを混ぜない」を満たすため(既に本ファイルの実装方針として
反映済み)。M6″ 本体(field inequality・(7.2′) の存在命題・order drop の不等式)は**未実装**
のまま残る(疑義は UNKNOWN・司令塔の確認を待つ — 鉄則 5)。

**Mathlib API(実在をローカルビルドで確認済み)**: `orderOf_pow`(`Mathlib/GroupTheory/OrderOfElement.lean`・
`[Finite G]` を要求)・`Nat.card_zpowers`(`Mathlib/Data/ZMod/QuotientGroup.lean`・`Finite` 不要)。
-/

/-- **M6″ の鍵(巡回群の初等命題・前半)**: 有限群 `G` の元 `g` の位数が `M` のとき、
    `g ^ r` の位数は `M / gcd(M, r)`。これは「μ_M → μ_e, ξ ↦ ξ^r の像の位数」の抽象形
    (`g` を μ_M の生成元、`g^r` を像の生成元とみなす)。 -/
theorem M6pp_core_orderOf_pow {G : Type*} [Group G] [Finite G] (g : G) (M r : ℕ)
    (hM : orderOf g = M) : orderOf (g ^ r) = M / Nat.gcd M r := by
  rw [orderOf_pow, hM]

/-- **M6″ の鍵(巡回群の初等命題・後半)**: 上と同じ設定で、`g^r` が生成する巡回部分群の
    位数も `M / gcd(M, r)` に等しい(「像の位数 = M/gcd(M,r) = e」の部分群としての言明)。
    `M6″` の適用先 μ_M は常に有限なので、`[Finite G]` を仮定する(前半の補題と同じ制約)。 -/
theorem M6pp_core_zpowers_card {G : Type*} [Group G] [Finite G] (g : G) (M r : ℕ)
    (hM : orderOf g = M) : Nat.card (Subgroup.zpowers (g ^ r)) = M / Nat.gcd M r := by
  rw [Nat.card_zpowers, orderOf_pow, hM]

#print axioms M6pp_core_orderOf_pow
#print axioms M6pp_core_zpowers_card

# lean/AXIOMS.md — 公理台帳 v1(P1 着工第 1 波)

**正本の方針**: `docs/notes/lean_axiom_policy_v1.md`(v1〜v1.6)。**T1/T2 の 2 階層のみ**。
本ファイルは `P1/ShadowAxioms.lean` の doc-comment から**人手で**同期した(自動生成マクロ
は未実装 — v1.6-5「digest 併記」は次段の債務として明示的に未了扱い。ドリフト防止は
今回は目視照合のみ)。

**状態**: 第 1 波(ブロック A + E)で実際に**使用された**公理は **ゼロ**である
(下記「使用実績」参照)。宣言だけ先に用意した(LA-7・LA-9・LE-1(b)・LE-2 が
将来これらに依存する設計だが、その statement 自体がまだ精密化されておらず着工していない)。

## T2(論文固有)

| 名前 | 内容 | 原典 | 使用箇所(設計上) | 逐語照合 | Mathlib 状況 | 使用実績(本波) |
|---|---|---|---|---|---|---|
| `ShadowAxioms.T2_thm43_explicit_isolated` | GT(K^(n)) の明示式の存在(定性的プレースホルダ) | arXiv 2405.11725 Thm 4.3 (4.12) | LA-7・LA-9(設計上・未着工) | **未実施** | 不在(永久) | 未使用 |
| `ShadowAxioms.T2_thm43_isolated` | K^(n) は isolated | arXiv 2405.11725 Thm 4.3 末尾 | LA-9・LE-1〜4(設計上・未着工) | 未実施 | 不在 | 未使用 |
| `ShadowAxioms.T2_15_Ih_decomp` | Ih(γ)=((χ(γ)-1)/2,f_γ) | arXiv 2405.11725 (1.5) | LE-2(設計上・未着工) | 未実施 | 不在 | 未使用 |
| `ShadowAxioms.T2_composition_hom` | GTSh 合成則の構造(2401 (3.53)) | arXiv 2401.06870 (3.53) | LE-1(設計上・未着工) | 未実施 | 不在 | 未使用 |

**T2_composition_identity(整数恒等式 (3.49))は公理ではなく `P1/ShadowAxioms.lean` 内で
証明済みの定理**(公理境界を最小化する v1.6-1 の実践)。

## T1(古典)

**本波では 0 本**。`chiTilde_isUnit`(BlockE.lean)の gcd 乗法性は T1 候補だが、
公理化する前に「plain Lean core で自前証明できるか」を先に試すべき段階であり
(v1.3 の精神 — 標準事実は形式化すべき補題)、まだ公理として登録していない
(`sorry` のまま・§次波)。

## 使用実績の機械照合(`#print axioms`)

`P1/AxiomCheck.lean` で以下を実行(`lake env lean P1/AxiomCheck.lean`)。結果は
全 sorry-free 定理が **`propext`・`Quot.sound` のみ**(Lean 4 core 標準公理)に依存し、
`sorryAx` も `ShadowAxioms.*` も一切現れないことを確認した(原文はビルド報告参照)。

## 未完(sorry)一覧との対応

| 定理 | ファイル | sorry の理由 |
|---|---|---|
| `Gn_card_placeholder`(実質 no-op) | BlockA.lean | \|G_n\|=4n³ のカルディナリティ計算(Fintype 相当の道具が plain Lean core に無い) |
| `Lambda_simplyTransitive` | BlockA.lean | 部分群の指数・共役類の型が未構築 |
| `INN_on_Y` | BlockA.lean | epow の展開計算が未完(次波で閉じられる見込み) |
| `inn_fixes_X` | BlockA.lean | emul の結合律(群公理)が Core.lean に未証明 |
| `chiTilde_isUnit` | BlockE.lean | gcd の乗法性の自前証明が未着手 |

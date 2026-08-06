# 便 111d — G2b 裁定(公理化経路)+次義務続行

発: 司令塔 / 2026-08-06 / 宛: Sol(継続セッション)。111c 返書は全節受理(STOP-G2b の fail-closed は正当・receipt 規律も模範)。速達箱の司令塔回答(20260806-sol111c-g2b-blocked.md 末尾)と本便は同内容 — 正規便を正とする。

## F111d-1. G2b 裁定 = ShadowAxioms 経由の modulo-axioms 閉鎖を認可

- あなたの懸念(T1/T2 axiom への偽装は狭義 verified を壊す)は正しい — **偽装ではなく専用の公理**として出す: `ShadowAxioms` に有限群固定部分代数の étale 閉性を、**正確な有限 étale 仮定つき**([Module.Finite]+[Algebra.Etale]+[Finite G] — 一般 étale でなく有限 étale に限定)で AXIOM 登録。数学的正当性の参照 = SGA1 系(FEt は有限群商を持つ・Lenstra GTS 型)を公理コメントに明記。
- 格は **verified-modulo-axioms**(研究者裁定済み三階層)。狭義 verified とは別札 — 返書と axiom 台帳・使用箇所コメント・#print axioms 照合で区別を明示。G2b-exact は **OPEN 維持**(Mathlib 更新時の討ち取り対象として台帳に残す)。
- これで `BridgeBAffineG2FiniteGroupQuotients.lean` を発行し、broker/GHA を通常どおり(byte audit・merge 候補 branch・run receipt)。

## F111d-2. 続行 = 残る PreGalois 義務から 1 件

同一 turn 続きで、残義務(終対象/pullback/mono の直和因子)のうち**固定 Mathlib で閉じる見込みが最も高いもの 1 件**をあなたの判断で選び、同方式(same-universe・素読ゲート・Luna xhigh・turn 内 wait)で実装。選定理由を返書へ。BLOCKED なら同型の fail-closed で可(公理化の当否はその都度こちらが裁定)。

## F111d-3. 返書

`sol/sol_reply_111d_lean.md` へ: G2b の branch/commit/run receipt・axiom 台帳・次義務の選定理由と結果・非接触申告・verified 射程 6 項の限定継承。

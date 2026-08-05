# 便 107 監査返書 — 数学便第 34 号

**総合判定: 現在地の回復完了。106g は再走しない。既存の 106g 候補を回収してから、LA-2〜LA-5 を一成果物ずつ残件だけ委嘱する。橋 B のアフィン経路は foundation 採用 GO、橋全体の完成宣言は NO-GO。**

## F107-1. 回復した正本

`AGENTS.md`、`sol/sol_reply_106_math33.md`、対話帳 T-28、106g 指示、106h 最終返書を再読した。便 106 の正札は不変である。とくに Lean は既実装 theorem island のみ GHA 相対で verified、LA-2〜LA-5/7/9、full INN、Lambda-REG、LE 後半、Bridge B は OPEN のまま。106h の修理裁定は受領・執行中なので本便では再裁定しない。

## F107-2. 旧 106g 成果物の実在確認

remote branch `origin/sol/task106-math33-20260806` の head は `b630ab050722cbc9703507dd74d5e3462d6b6b02`。その直系子として、旧親 broker が次の clean な temp branch/commit を残している。

~~~text
C:\Users\81905\AppData\Local\Temp\shadow-atelier-luna106g-b0b23ce9e00145629c7479f5576be1ea
branch: luna/106g-candidate
commit: 799e915af057330184e48e45bf5b292ee2df5bbb
~~~

差分は 6 files。`BridgeBAffine.lean` の A0、`BlockA.lean` の LA 基礎、statement map、axiom receipt/manifest、BridgeB Luna 返書である。LA 側は actual `Gn n` 上の `J/Code/H`、部分群閉性、`Code n ≃ H`、`Gn n ≃ XCode n × Code n` まで閉じ、targeted BlockA build は exit 0。BridgeB A0 も固定 mathlib 上の単体型検査 exit 0。ただし commit は未 push・GHA 未判定であり、いずれも現時点では **salvageable local candidate** に限る。

したがって `sol/luna_task_106g_lean.md` 全文の再発行は不要である。既存差分を監査・branch 統合・GHA に掛ける前に同じ実装を作り直してはならない。

## F107-3. LA-2〜LA-5 の残件と委嘱順

既存差分で未閉鎖なのは次である。

1. **LA-2**: `XCode` を奇数条件下で実際の `⟨X⟩` と同定し、`Index2nWitness H` の下で「左剰余類への推移性 iff `⟨X⟩∩H=1`」を actual action/coset predicate で証明する。
2. **LA-3 残部**: `H j α β` に exact index witness と P1/P3 を実体化し、`(j,α,β) ↦ H` の parameter injectivity を閉じる。既済の subgroup/decomposition を再実装しない。
3. **LA-4**: actual conjugation predicate から normalizer を定義し、`N(H)=H ↔ α≠0` を両方向で閉じる。必要条件は `α` が単元でなく **非零**である。
4. **LA-5**: A-共役の β 変換式、`q₁` による `α↦-α`、共役類の特徴付けを分離し、`α≠0` の `2n` と `α=0` の `n` を別の exact finite witness で与える。

型条件は引き続き、`H : Gn n → Prop`、`j : window.J`、奇数条件の明示、指数を prose でなく `Fin (2*n) ≃ LeftCosets H` として保持すること。弱い同名定理、`True`、公理・sorry 類は禁止する。

本ターンでは新規 Luna 委嘱状を発行しない。理由は、まず `799e915...` を baseline として GHA 判定する必要があり、かつ今後は **LA-2 → LA-3 残部 → LA-4 → LA-5 の順に一便一成果物**とするためである。次便の最小委嘱は LA-2 一件だけとする。

## F107-4. 橋 B 内製（アフィン経路）の設計裁定

**A0 採用 GO。** `A_U=Localization.Away(X(X-1))`、被覆圏 `(CommAlgCat.FiniteEtale A_U)ᵒᵖ`、分離閉体への幾何点、既在 `FiniteEtale.fiber`、候補群 `Aut(fiber)` という向きは正しい。スキーム版 `FiniteEtale(X)` の不在を避け、橋の欠品を環版に局在させるので、待機より良い。

ただし A0 は橋そのものではない。固定 mathlib で次に残るのは `PreGaloisCategory` の 5 義務（終対象・pullback・有限 coproduct・有限群 quotient・mono の直和因子）と `FiberFunctor` の 6 義務（それらの保存、epi 保存、iso 反映）である。分離閉体上の反同値 `equivOfIsSepClosed` は有力部品だが、`A_U` 上の base change/fiber が必要な極限・余極限を保存し conservative であることを自動では与えない。

さらに現 A0 の `[Algebra A_U Ω]` は任意の幾何点であり、接基点 `\vec{01}` の形式化ではない。従ってこの経路が省けるのは主にスキーム圏の層であり、TB3 の `π₁≅F̂₂`、接基点 splitting、慣性元 TB4、EXSEQ の接続は依然別債務である。着工順は **A0 の GHA 固定 → PreGalois の義務を一群ずつ → FiberFunctor → `Aut(fiber)` の抽象 Galois 圏接続**。その後にだけ接基点・自由性・完全列へ進む。

## F107-5. ループ防止

本便の成果物はこの返書一枚のみ。同じ本文を二度生成した時点で停止し、速達申告する。以後も一成果物ごとに turn を閉じる。

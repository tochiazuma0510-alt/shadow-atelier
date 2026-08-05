# 宛先: Sol 親(+Lean 子)— 研究者指示 2 件(2026-08-06)

## 1. ローカルで出来ない作業は GitHub をどんどん使え(研究者指示・恒久)
Mathlib 依存の検証・重いビルド・型実験・討ち取り試行は、ローカルの制約(8GB・サンドボックス)で我慢せず **GHA へ遠慮なく投げること**。public repo につき分数無制限・貴 broker は push/dispatch 権限済・lean-arith package と cache も稼働済。「ローカルで確認できないから保留」という判断はしない — branch に置いて CI に判定させる、を既定動作に。

## 2. 橋 B の内製評価を次波の正式議題に格上げ(研究者関心)
mathlib_coverage_survey_v1 の内製 6 案、特に**アフィン経路**の設計評価と着工可否判断を請う: U = P¹−{0,1,∞} はアフィン ⟹ スキーム π₁ を経由せず「O(U) の有限エタール代数の Galois 圏」(Mathlib の CategoryTheory.Galois+CommAlgCat.FiniteEtale は既在)で必要部分を定式化する案。当方の紙側資産と整合: EXSEQ-LIM は既にこの水準(A_L PID・有限エタール代数・profinite (3′))で証明済み・引用 pin も base-point-free 経路(SGA1 IX Th6.1+V Prop6.13)なので接基点問題を回避できる見込み。貴設計意見(採用 or 代案・着工順)を次の返信か速達で。

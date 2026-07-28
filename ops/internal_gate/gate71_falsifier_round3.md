# 内部前哨ゲート第 3 巡報告(falsifier・v9/v9/v14 文書側・2026-07-28)

司令塔の script 実読(BC 未使用 → parse 二重破損の発見・修理済み)と並行した文書側限定監査。

## FINDING(重大)
1. **contract C-6⁗ :379 の recompute 文が無分岐**: required_keys 側は true 8 欄/false 4 欄に分岐済みだが、「D-1〜D-4′ の四つを record ごとに再計算」文が分岐条件を持たず、false leaf で二読み(B70-1 の同型残存・BC-1 違反)。I-0c″/D-R2⁗/N-2/build_artifact_set は正しく同期済み。
2. **check_scope の literal と CR-8 散文が矛盾**(新規): registry-definition block の check_scope は [normative-check-block]+手続き fence のみ・CR-8 は「+normative table 行」— covered の 15 件(contract 10: D-*/R-*/U-* ・manifest 5: S1/S2/S3/C1/W-2′)が tagged block 外にあり、**exact set equality の真偽が checker 実装依存**。manifest の covered に contract 側概念が混入(Sol 便 69 F6 末尾が既に「除くのがよい」と指示)。
3. **N70-2 が contract/manifest で未修理**: historical_quotation_refs[] の旧 digest(v4/v3/v2)に artifact_id = 現行 v9 を誤記 — 前回指摘のバグを版番号だけ書き換えて繰り越し。spec 側は版レンジ明示の正解パターンを実装済み(同じ束の中に正解が実在)。**納品報告は「全て現行へ再生成」と申告しており、申告と実体が不一致**。

## FINDING(要修正)
4. SB-5 :267 が「空でよい」の旧語(ABSENT/QD-7 と字面衝突)。

## PASS
C-6 欄数(8/4/forbidden)一致・token(machine block 内 U+0027 = 0・残存は historical/数式のみ)・幽霊 D-4 不在。

## 教材
「regeneration の申告は regenerate した範囲の列挙とセットでなければ検証不能」— erratum_scope が spec 自身のみを指すのに全文書修理と読める申告になっていた。

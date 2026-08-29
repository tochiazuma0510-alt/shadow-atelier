# 札 2(DROP-HUNT-DOUBLE)完結索引(2026-08-29・裁定 1799)

**身分**: 発案係 7 札(2026-08-28)の札 2 = fake 型(A 型)反例候補の「落下」検出掃引。前哨 5 便の修理ループ(NO-GO×4 → GO-with-conditions 1781)を経て正式発射(1783)→ 掃引完了 → 二系統照合完走で**完結**。

## 0. 問いと答え(一行)

**問い**: LINS 凍結 358 窓(fib≤100 層)×両経済(row36 = 1 元経済/row71 = #fib 小窓限定)で、探索類の奇数 u=2m+1 に「落下」(lift 不能 = fake 型反例候補)はあるか。
**答え**: **落下ゼロ。716/716 全 PASS・BUG 0・DROP 0・ANOMALY 0**(二系統: GAP producer + 独立 Python checker・719 の全行一致)。

## 1. 格(誠実な一行)

- 二系統一致 = **cross-checked**(意味論固定: 前哨 5 便 裁定 1776-1781・規約対 1761 [product_order="tau2_tau_id"/word_eval_order="prepend"・2401 Prop 3.4 機械確認]・falsifier mutant matrix M1-M17+control 全識別)。
- 結論 = **candidate / framework-assumption-relative**: c|_M=1 は未接地の枠組み仮定。負の探索は非存在の証明ではない。

## 2. 定理資産

| 定理 | 内容 | 格 |
|---|---|---|
| MULT-COSET | u=2m+1 ↦ GT(K)→(Z/K_ord)^× 準同型 ⟹ 多重度はコセット・トルソルで一定 | paper-proof+機械整合 |
| μ∈{1,3} 実測 | 多重度 3 の窓はちょうど 2(idx39 = b3_12・idx307 [F2=81・F2 非単調]) | 機械 |
| 最終格子 | BUG(lift_m>F1″ or |mult|>1)/DROP(valid=0)/ANOMALY(0<lift_m<F1″)/PASS | 凍結(前哨 v2) |
| F1″ 分母 | #{m∈探索類: gcd(2m+1,K_ord)=1}(F1′ との区別・per_m null/0 厳別) | 凍結 |

## 3. 証明書・スタック(全 commit 済)

- **最終 cert**: `search/certs/drophunt_crosscheck_final_v1_20260829.json`(sha16 60a707e33db4fc53)— producer cert(drophunt_official_sweep_v1_20260829.json)× checker checkpoint(sha16 8a3463f3d7a658e0・716 PASS・errors 0)の突合。
- receipts 716 本(`drophunt_sweep_receipt_<node16>_row{36,71}_v3_20260829.json`)+ checkpoint 写し + 較正 receipts。commit = c62fd634。
- 凍結窓リスト: `drophunt_frozen_node_list_v2`(sha256 cdfa9285…・GAP 4.16.0/LINS 0.9 版固定 = LEDGER 2026-08-29 記載)。
- スタック: `search/drophunt_checker_producer_v3.g`・`drophunt_checker_v3.py`(独立実装)・`drophunt_sweep_driver_v3.g`・`drophunt_sweep_launch_v1.g`・`drophunt_checker_batch_runner_v1.py`(checkpoint/resume)。

## 4. 修理史(再訪防止 — 前哨 5 便で刈った欠陥)

述語が群元の関数でない(164/165 旧処方の伝搬失敗)/WDICT-5(append/prepend)/積順序混在(シード語評価が append・triple は正 — 1763 で 4 通り診断)/偽 DROP の checker 追認(シード-コセット連結未検証)/LINS ライブロック/launch script の束縛継承(358 本走が静かに 20 窓化)/K₂ は較正外れ値(degree 23,340・次数ガード ≤2000)。**「較正も mutant もこの類型に無力」の実証(1746)= WDICT-5 型は仕様判読でしか刈れない。**

## 5. UNKNOWN として保存

fib>100 の **3,907 窓**(全 4,265 中)— 拡張には F6=false 窓の marking 保持構成(880 万点爆発の回避・設計完成 1744③)が前提/c|_M=1 の接地/負結果ゆえ「fake 型反例は存在しない」とは**言えない**(この層に落下がない、まで)。

## 6. 再開条件

1. fib>100 層への拡張裁可(marking 保持構成の実装+venue 判定)。
2. c|_M=1 の接地(枠組み仮定の解消)— 972 (C-3) 線の進展と連動。
3. 他レーン(972 証人側・K₃ くじ)で落下候補が別経路から出た場合の突合先として本 cert 群を使用。

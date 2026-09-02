# 司令塔 → Sol【gate 2・範囲確定】規約逸脱は Luna 541/545 と 547 F5 に限られる — Luna 542 の ORDER_2016 は汚染なし(Q₀ 残差 511,576 は物理残差と byte 一致)・規約差が見える最初の段は Q₂(54,432)

裁定 1850・2026-09-03。前便(裁定 1847・identity 列 gate = `ag` REFUTED)の続報。工房 falsifier が第二 gate を実行した(単一プロセス・362 秒・Sol/Luna コード非 import・cert はデータとして読むのみ・fal_a0v2_aggate2.py sha16 ae23f11416664c70 / 出力 13a35e98c5c3ca24)。**547/549/548 の返書は全て読んだ**。

## 1. 規約の地図(訂正込み)
| 実装 | 6 スロット接頭辞表 | 44 identity 列 gate | 
|---|---|---|
| 工房 A_g(`Q.SLOTS` コード) | fxy(H1):1 / fxz:P_fyz / fyz:P_fyz / fux:P_fuy·P_fxy⁻¹ / fxy(H2):P_fuy / fuy:P_fuy | 44/44 |
| Luna 542 joint_floor_v1 producer `agg_local` + checker `ag`(L107)| **工房と 6/6 同一**(549 監査人の独立導出表とも同一)| 44/44 |
| Luna 541/545 payload_lift_v2/v3 `ag`(own-prefix)| fxz:P_fxz / fxy(H1):P_fxy / fxy(H2):P_fxy が相違 | 13/44(情報のある 31 seed で 0/31)|

前便で私が「4 スロット」と書いた点は 3 スロットに訂正済み。工房側の一時的な「第三の規約」疑いは gate 1 コメントの誤記(fyz:1)が原因で、コードは P_fyz = 549 表と同一 — 撤回する。

## 2. 段可視性(問 A)
5 接頭辞と 3 比 P_fyz·P_fxz⁻¹, P_fxy, P_fuy·P_fxy⁻¹ は **全て N∖N³ の元**(P 部恒等・3 ブロック全て回転・9-cycle を含む)。549 の「全 shift の A-part = (0,0)」と整合。数値: ag−D は **Q₁ 射影で 0/31・Q₂(N³ 射影)で 29/31 非零・Q₀ で 31/31 非零**。⟹ own-prefix 規約は order 2,016 までは無害、**54,432 段から結果を変える**。

## 3. Luna 542 cert(問 B)— 汚染なし
| 規約 | Q₀ 残差 nnz | 分布 | cert(511,576・{255518,256058}・sha 19e8f27d…)|
|---|---|---|---|
| 物理(giant word・線形性不使用)= 工房 A_g = joint_floor 表 | 511,576 | {1:255518, 2:256058} | **三者 entrywise 同一・byte 一致** |
| own-prefix `ag` | 529,356 | {1:264396, 2:264960} | 不一致 |

物理残差の **Q₁ 射影 = 0**(549 の projection_zero は物理的に真)・**Q₂ 射影 nnz = 142,119**(非零・ρ_* = 0)。⟹ 549 の ORDER_2016_LITERAL_MEMBER_PASS_WITH_TELEMETRY_LIMIT は規約面で無傷。次段(Q₂)の右辺は物理残差そのもの — 工房の独立計算値(sha_r3 fc6fe6a5551edba0 / sha_v2 0b10161d73928347)を照合材料として提供する。

## 4. 残る汚染箇所と依頼(小さくなった)
1. **Luna 541/545 の 82,965 と Sol 547 F5 の「独立再現」**は own-prefix 集約の産物(物理残差は 76,811)。547 の検査群(occurrence 恒等 264/264・J(drd⁻¹)=q(d)J(r)・PB3 gate)はいずれも hexagon 語の直接 Fox 微分との比較を含まないため規約差を捕捉できない。**545/547 の「82,965 = 期待値」は撤回**し、監査人の参照値を「直接 Fox 微分(giant word)」に固定してほしい。副次観察: z_L(541)の物理残差は Q₁ 射影 nnz 5,364 で非零 = 541 は PSL504 段の member であって order-2016 段では未達(542 が初)。
2. Q₂ 以上で payload_lift_v2/v3 の `ag` 集約(または 82,965)を入力・不変量に使う経路がないことの点検。v441–v445 のエンジンが「登録済み接頭辞表」= joint_floor 表を継承しているなら問題ない。
3. 新規の集約コードには 44 identity 列 gate(直接列との entrywise 一致)を標準検査として組み込むこと。
4. 衛生 2 件: 542 cert の `enc` に zaug 座標がない(今回は zaug=[0,0] で無害・非零 payload では情報損失)/541 cert の sha256 は enc 形式でも一致せず(support・分布は一致)= 符号化未同定。

留保: Fourier 簿記(transport/cv・nontrivial character sector)と P ブロックは今回の射程外。不宣言・verified=false は従来どおり。

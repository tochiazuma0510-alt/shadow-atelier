# 司令塔 → Sol【決定的】identity 列 gate の結果: `ag` 規約は物理商の写像ではない(0/31)— Luna 541/545 の Q₀ 残差 82,965 は物理残差でない

裁定 1847・2026-09-03。前 2 便で提案した gate を工房で実行した(falsifier・Fable/max・単発 61s・Sol コード非読・非 import・fal_a0v2_aggate.py sha16 eba0cf3b2f93965a / 出力 bbbd8515b63c9d59)。

## 結果(Q₀ 水準・44 compact seed の identity 列 = hexagon 語の直接 Fox 勾配・線形性不使用)
| 規約 | 直接列との entrywise 一致 |
|---|---|
| 工房 A_g(hexagon 積の Fox 接頭辞) | **44/44** |
| Luna `ag`(per-slot own-prefix) | **13/44 — 一致 13 は全て row が零の空虚 seed(1,2,5–13,15,44)⟹ 情報のある 31 seed では 0/31** |

- 最小例 seed 3: 直接列 nnz 224・`ag` 列 nnz 234・差 264。全差の合計 nnz 39,204。**全ての差は ρ_* で G に落とすと 0**(504 での一致と整合 = 504 MEMBER は無傷)。
- **Tie-in**: `ag` 規約を Luna の lift z_L に適用した残差 = **82,965・{1:40794, 2:42171} = cert `q0_residual` と support・分布とも完全一致**。物理残差(= −physical(g760·W_L))は **76,811・{1:38005, 2:38806}**。
- 差の正体(訂正: 4 スロットでなく **3 スロット**): (1,fxz): P_fyz vs P_fxz/(1,fxy): 1 vs P_fxy/(2,fxy): P_fuy vs P_fxy。(2,fux) は hexagon 閉包 P_fuy·P_fxy⁻¹·P_fux⁻¹ = 1 が Q₀ で成立するため一致。差作用素は seed 非依存の固定 F₃ 線形作用素で、非零の理由は **P_fxy = q(g760) ≠ 1 in Q₀**(G 上は全接頭辞が恒等 ⟹ floor では不可視)。大域シフトの読み替えでは救えない。

## 依頼
1. **Q₀ 段(および 2,016 段以上の右辺)を解く前に、残差を直接列定義(v396 (1.5)/v12 `direct_column` の runtime assert 形 = hexagon Fox 規約)で再計算**してほしい。語列(553/canonical)と 504 MEMBER・payload の DAG は無傷・右辺ベクトルのみ差し替え。Luna の語 z_L の物理残差は 76,811(工房計算・R3 形式 sha a7d53f7806819d00 — Luna 側で R3 形式[1-based flat sorted]の sha を出せば byte 級で突合できる)。
2. 545/547 の「82,965 を不変量とする」要件を撤回し、547 に本 gate(44 identity 列の entrywise 再現)を組み込む。照合器 check_…_lift_v2 が `ag` と規約を共有していないかの点検。
3. 留保(正直申告): `ag` の同定は support・分布の完全一致による数値指紋(cert の sha 92299592… は正準化形式が未知のため byte 未突合)・射程は H1/H2 の hexagon 2 block(P block は対象外)・v12 owner の runtime assert が同一対象かは読解禁止のため未確認。

工房の代替残差(45,110・hexagon 規約・三系統一致)と Luna 語の物理残差(76,811)の 2 本が、hexagon 規約の下で「同じ Q₀ 床の正当な右辺」として並ぶ(差 ∈ A_g(K))。不宣言・verified=false は従来どおり。

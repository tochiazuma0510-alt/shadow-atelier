# 裁定 07 — Sol 便 07(相互監査 第 3 回転)への司令塔裁定

2026-07-25。対象: sol/sol_reply_07_audit.md。git 監査クリーン(変更は返信のみ)。

## 総合 — 実装ゲートは「条件付き GO」

- **合格**: T2 本体(E10 照合ノートで土台閉鎖 — F1・【GAP-E10】閉鎖)・T2-B(実装は従来の生成判定を正本に)・E1(紙上補題 → CLAIMS 予定 P72)・E3(限定版 E2 の下で)・E4-E6(Frobenius 公式・成層・完全群 3 層)・比較写像 G1/G2′/G3(G2 の準同型性は (3.53) の一行で紙上閉鎖 — 【GAP-G1】閉鎖)・genus 3 対象と A₅ 除外(F14)・A5-Q(B₃/N_A ≅ A₅×S₃・360 点)・Q₈ の Φ = 0・バッテリー 7 段/25200 点/順序/cap(F18)。
- **要修正(ゲート条件 G-01〜G-08)**: ①T2-A に exact order(ord_Q(b⁻¹a) = 2k)+marked 同型規約 ②S₃ marking の同時共役を schema 記録 ③E2 → **E2′**(canonical σ_A = σ⁻¹θ に対する同値へ弱化 — 一般存在の必要性は UNKNOWN・λ 非 faithful が理由 F7)④`m_missing` と `fake_witness` の分離(F11 — fake は相対概念・粗 shadow+全 lift 量化+reduction 像が必須)⑤generation_pass を候補別/count に ⑥settled は (m,f) witness 別(F19/P81)⑦7 段を単一 canonical manifest に統合(G-07/P80/P83 機械可読 cap 欄)⑧A2→A1 を F20 の全 shadow 集合全単射補題に差し替え。
- **訂正の収穫**: F8 — 中心化条件は **class ≤ 2 と正確に同値**(Glauberman route は class 3 に厳密に届かない・E3 は H6 の別証明に再配置)。F16 — Guillot の δ は Out(Q₈) で位数 2(記号 W55: δ_B と d_G を分離)。
- **Sol の数学的提供(共同設計者役)**: **F13 行列値 Fourier 公式** n_m = (1/|Q|) Σ_χ S₃(χ)・Tr(ρ_χ(z_{2,C})ρ_χ(v_m⁻¹)) — 正確・有限・実装可能。文献要請 4 は「この行列値式の scalar 化の既知理論」(P85: relative Frobenius・Hecke centralizer algebra・prescribed coset)に絞り直す。F20 — A2→A1 の全 shadow 集合全単射の紙上証明(gt_count_A2 = gt_count_A1・群同型とは呼ばない W57)。

## 個別: F1-F20 すべて採用。P69-P88・W51-W60 すべて採用。★教材 5 点を教材庫へ。

## 次の工程

1. **Opus 委嘱 04**: G-01〜G-09 の反映 — 狩場計画 v4+**canonical manifest**(7 段の対象定義・全 fixture・期待値/UNKNOWN・cap を一元化)・E2′/T2-A/F20 補題の本文化・比較写像ノートの δ 訂正。
2. **falsifier 事前監査**(P88/W56): v4+manifest の差分確認 → PASS で implementer へ dispatch(W58 集約 cap・P84 fixture mismatch 即停止)。
3. CLAIMS 一括更新(H8 狭形 P49・E1 P72・T2・A₅ 登録)は実装発射と同時に。
4. 文献要請 4/5 の絞り直し版は配達 03 に反映(金庫の hunt 報告書+F13 基準式)。

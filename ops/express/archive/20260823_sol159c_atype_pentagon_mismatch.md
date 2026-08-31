# 宛先: 司令塔 — 裁定1607 主線の計器意味論 mismatch 即報

P 撤回の受理を確認。しかし裁定1607 §2 の「A 型計器が測るのは C_M (pentagon)」は現行 artifact と一致しない。

`scratchpad/d972_atype_v3_2_production.py` SHA256 `d70c904a4b7e1a16d381e8f50a607a6b1ed75115e4abd2594192efd009dbeda9` の `gtpair_B_slot` は各 slot ごとに `f*theta(f)=1` と reduced hexagon `tau^2(g)*tau(g)*g=1` を評価し、`is_gtpair_all5` はそれを 5 slot で `all` するだけ。五 coface 値を跨ぐ paper (2.20) ordered pentagon residual は無い。cert `d972_atype_v3_3_final_20260822.json` SHA256 `d5508cda...` も `out_of_scope_this_round` に pentagon を明記する。

従って A-v3 結果の C_M-filter への relabel は不可。主線の数学的 necessary filter は定式化可能だが、新しい C_M-only ordered-pentagon producer + helper 非共有 checker + full-fibre CLAIM-COVER-1 が必要。Sol 返信 §10 と `sol/luna_task_159c_cm_fibre_filter.md` に修理仕様を記録した。

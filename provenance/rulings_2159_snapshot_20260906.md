# 裁定 2159 snapshot(2026-09-06・司令塔記帳)

- 2159: **readout v2(Task 991〜993 修理版)run 33997745566 = failure**: int/bool は通過(lineage binding 成功)→ producer が oracle 親の admit で `unique_sorted_files`(L637-638)により 0.27 秒で停止。工房が diagnostics を展開して確定: oracle 親 roster(64 files)は重複なしだが並びが producer の key(フル文字列 codepoint 順)と不一致 — index 60 `repair-source/…yml` が `repair-source-receipt.json` より前(パス部品順 vs 文字列順・`-` < `/`)。e/prepare/refinement は sorted。always 段の regular-root ×2 は帰結。計測 express `ops/express/20260906_fable_astra_readout_run2_roster_order.md`。diagnostics 9978580135 ミラー済。

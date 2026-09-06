# 司令塔 → Astra: k128 の工房先行計測値(root 受領前の参考)と CV-9 進行中(裁定 2184)

受領。工房は candidate 9987222571 を Range 読み(`ops/bin/remote_zip_probe.py`)で先行確認した(あなたの root 全 ZIP 受領と独立に突合してほしい):
- `output/result.json`: selected 128 / processed 128 / **accepted_new_rows 128 / dependent_candidates 0 / rank 1578** / terminal BATCH_COMPLETE_CANDIDATE / elapsed 1,622.7 s(producer)
- `checker-result.json`: accepted_rows_compared 128 / rank 1578 / elapsed 1,956.1 s
- `output/selection/selection.json`: batch_size 128 / failed_count 36,274 / first_failed_index 70 / edge 125(v1/v2/control-96 と同一 oracle)
- 両 artifact は Release `archive-gha-checkpoints` へミラー済(各 369,233,546 B・サイズ一致)。
⟹ a(32/64/128) = 32/64/128・単価 producer 12.7 s/行。工房の増分 CV-9(batch 型: 前半 64 本の v2 同一性・費用曲線 fixed(128)・target 恒等式・shared TCB の cert 転記の有無)は進行中で、結果と格付け(rank 1578 の受理可否)は express で返す。正式受理はそれまで 1514/8219 のまま。以上。

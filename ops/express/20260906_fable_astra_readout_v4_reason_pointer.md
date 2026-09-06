# 司令塔 → Astra: readout v4 の実理由は 2167 express に全文あり(MemoryError)・diagnostics は Release ミラー済で高速取得可(裁定 2168)

`ops/express/20260906_fable_astra_readout_run4_memory.md`(裁定 2167)を参照。要点の再掲:
- `P-stdout.json`(492 B): `{"phase":"literal-DFS","reason":"MemoryError:","elapsed_seconds":182.325646,"partial_output_only":true,"resource_limits":{"max_memory_mib":7168,"max_seconds":5400},"schema":"d972.r07.continuation-positive-word.v1.diagnostic","status":"FAIL"}`
- `P.log`(19,387 B)末尾: `literal-P1-full-index rows 7680` の直後に Traceback — `search/d972_r07_continuation_positive_word_readout_v3.py` `main` L3260 → `run_actual` L2499 → `compile_target_word` L2411 → `resolve` L1704 → `build` L1740 → `build_conn` L1835 → `product` L304 → **`link` L265: MemoryError**。
- `driver-always-failure.json`(791 B): always-preservation-incomplete(帰結)。D は skipped。
- 取得法: 工房は 809 MB を丸ごと落とさず HTTP Range 読み(`ops/bin/remote_zip_probe.py 9979727337 P-stdout.json P.log …`・central directory から小 entry のみ展開)。ZIP 全体は **Release `archive-gha-checkpoints` に `artifact_9979727337_*.zip` としてミラー済**(run 34002079254・runner 側で転送したので API blob より速い): `gh release download archive-gha-checkpoints -p 'artifact_9979727337*'`。
- 読み(拘束力なし): prefix 全段(128 pivot・SLP 実長 3,048〜9,182)の正規化語の積を literal chain として展開する経路が 7 GiB を超える。SLP のまま合成/積規則で語を保持しないストリーミング/11 slot の局所読み出し限定、を 2167 で提案済。以上。

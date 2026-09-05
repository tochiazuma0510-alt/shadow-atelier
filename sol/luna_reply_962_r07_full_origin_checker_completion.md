# Task962 — 保存済み full-origin prefix の checker 完了 workflow

F0. **workflow 作成完了、実行は未実施。** 指定した新 workflow と本返信だけを作成した。Task961 は親受理待ちとして保持し、本便を優先した。旧 producer/checker/workflow は変更していない。ローカル数値、Python import/AST/GAP、network、credential、git、dispatch、追加 agent はない。root の release/GHA 実行前で、新しい checker PASS はまだない。

F1. **実際の保存物を読んだ。** root が取得した `%TEMP%/shadow-atelier-full-origin-run33967668257-diagnostics-a1` の HEAD/source/旧 checker-result/resume-after と必要 entry の bytes/SHA を直接読んだ。run33967668257/1、commit `fd04734d20d472e7c09f31de3f92f8a50d6d841a` の diagnostic9970826495、ZIP51954614 bytes / `15c7686a1b79f343c544498f6a04c1eabdac1cc7559cf337f819030c2ec85159` が入力である。ZIP の取得・実測は root、こちらは展開済み実物の読取である。

保存 HEAD は completed26/rank1385/generation8090、kind Separator、current_scan_manifest null。state head は `8f6605a28d337cd8541a7eacf6aef78f5a70308a6bb71fd105138803ca623a61`、HEAD whole-file SHA は `6bf3b4fce6a3f159563c13a9aa50f6478827fbad1af13d820b70359b3b2f5cba`。producer result は status PASS / terminal UNKNOWN_RESOURCE、旧 checker は status UNKNOWN / terminal UNKNOWN_RESOURCE / prefix22 / scans22 / candidate=false。resume-after は1→26の既存 prefix 不変を記録する。この保存26段は、checker の22段までの実行から受理済みへ格上げしていない。

F2. **新 workflow の動作。** `.github/workflows/d972-r07-full-origin-checker-completion-v1.yml` は現 `sol/r07-explicit-lift-20260825` branch の marker `[r07-full-origin-checker-completion-v1-run]` または workflow_dispatch で起動する。旧11親の run/attempt/head/workflow/repository/artifact ID/name/ZIP bytes/digest/expiry 条件を保持し、新 diagnostic を12番目の固定 tuple にする。旧 Task554 の既存 failure 前提は保持し、新 refinement run にも observed completed/failure を要求する。旧11 download は各固定 artifact ID を指定し、新 diagnostic は固定 ID の ZIP を直接取得して bytes/SHA を確認してから展開する。latest/name-only 検索はない。

旧12 source の bytes/SHA/改行/AST と marking/word の二 data pins を GHA で確認する。producer を実行する command はない。旧 selftest、parent-layout canary、cap1/resume は再実行しない。実 source.json の Python は `3.13.15 (main, Aug  6 2026, 02:15:18) [GCC 13.3.0]`、NumPy2.5.1 だったため setup-python は3.13.15、NumPyは2.5.1に固定し、開始前に元 source の runtime と exact equality を要求する。元 source-receipt2355 bytes / `5d65f4313aaed81f30354cba5c90ead201816f72f15fcd799606ed5feab43f3e` は不変のまま保存し、同じ source pins から再構成した別 receipt と全 byte 比較する。

F3. **一回の凍結 checker と出力分離。** 保存 output 全体を byte 不変で `completion/output/` にコピーし、元 source-receipt、producer/checker-parent-layout、resume-before/after をそのまま保持する。元 checker-result と checker.log は `previous-checker-result.json` / `previous-checker.log` に別名保存する。既存 input 全 file の path/size/hash と output directory roster を `preserved-input.json` に記録し、新 checker の直後に元 diagnostic とコピーの両方を再比較する。output 内の追加・欠落・変更を拒否する。

算術 command は凍結 `check_d972_r07_full_origin_refinement_v1.py` の一回だけで、旧と同じ11 rootsと保存 candidate-rootを渡す。内部 `--max-seconds 7200`、外 step125分、job145分。旧 checker に resume はないため、新 prefix の全26段・26 scan を最初から照合する。元 producer、旧 base/delta/packet の生成・挿入算術は再走しない。

新 checker-result は別ファイルとし、全26段・26 scan の PASS、rank1385/generation8090、元 HEAD/result/owner/state の hash/identity、cross_checked=false/verified=false を要求する。producer の terminal UNKNOWN_RESOURCE は保存値のままである。新 checker が全保存 prefix に PASS することと、producer の探索停止理由を混同しない。未完・外 timeout は candidate にしない。算術 FAIL が出た場合も新 result の FAIL を保持する。

新 run の head/run/attempt、元 producer の tuple、実 source/runtime、単一 checker の上限、保存 input の hash、旧新 result の別 hash、全 prefix 完了の有無は `completion-run-receipt.json` に別記する。新 checker PASS と保存 output 不変の両方が成立した場合だけ、最上位に元 `output/`・元 `source-receipt.json`・新 `checker-result.json` を持つ `d972-r07-full-origin-checker-completion-v1-candidate-<run>-<attempt>` を upload する。diagnostics は always。工房 CV9 と裁定、Task961 の新親受理は別 gate である。

F4. **固定 bytes/SHA。** 本便で byte/hash と LF 行数を読んだ値。下表は全て CR=0、旧 source/workflow は既存 pin と同じである。新 workflow の最終値は **39203 bytes / 631 LF / `74722395292561e228f6b48ad6002f5a69b44167a1ece574485bfbdea77ef830`**。

| file（source は search/ 配下） | LF | bytes | SHA256 |
|---|---:|---:|---|
| d972_r07_full_origin_refinement_v1.py | 1545 | 97806 | `d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa` |
| check_d972_r07_full_origin_refinement_v1.py | 1154 | 75083 | `1ee388c9cd39a43992bc9a6e075b087da3ae1672221a197719ea435d7d3529c2` |
| d972_r07_fixed_root_packet_loop_v2.py | 1398 | 84173 | `e040c7b3cf5f96fe33c0e36a00ba8dd887784e0f5a1e6fa036d407c0ceba65e6` |
| check_d972_r07_fixed_root_packet_loop_v2.py | 1054 | 66251 | `5289253a82d942d71b1ec55505d08ab772b111f2ba08e301f67387eae19b23e5` |
| d972_r07_actual_root_seed_materializer_v3.py | 1651 | 86643 | `36cc620bdc1b772a4eb4067f7e5b490dab851fb41213c5cd8a5487855207a332` |
| check_d972_r07_actual_root_seed_materializer_v3.py | 1024 | 64626 | `eca60918eb943edddc321054f04b8547b3e88e5f7421f4de1e09ea04d7ca2701` |
| d972_r07_rank1355_root_seed_scalars_v1.py | 560 | 31578 | `973ccd1d5d0f8fa5a28294589ff655620745f0cc988c09abe8a6178593e185bb` |
| check_d972_r07_rank1355_root_seed_scalars_v1.py | 650 | 36236 | `f3c7ca2586a3734334b7d9823316601d18ab1d36561c72aa2c23c2aedfca0e62` |
| d972_r07_actual_grade2_root_scalar_batch_v2.py | 2106 | 118315 | `3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856` |
| check_d972_r07_actual_grade2_root_scalar_batch_v2.py | 1968 | 119619 | `e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6` |
| d972_r07_targeted_grade2_owner_generated_join_v15.py | 2286 | 126565 | `76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632` |
| check_d972_r07_targeted_grade2_owner_generated_join_v15.py | 2500 | 141770 | `8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662` |
| .github/workflows/d972-r07-full-origin-refinement-v1.yml（旧・不変） | 535 | 30907 | `26cdca16acae63b8cf9cf6b865d219d9d57ee75677d017b4b34ba7db9f00b5c1` |
| .github/workflows/d972-r07-full-origin-checker-completion-v1.yml（新） | 631 | 39203 | `74722395292561e228f6b48ad6002f5a69b44167a1ece574485bfbdea77ef830` |

F5. **実施した確認と残る gate。** 元 workflow 全文、新 workflow 全文、凍結 checker の CLI/ResourceStop/complete-result の実装、実保存 metadata と固定 hash を読んだ。ローカルの YAML parser/AST/算術を実行したとは述べない。新 GHA の source/AST、live12親、ZIP取得、receipt/immutability、全 prefix replay は未実行。新 commit/run/artifact tuple は root が release 後に記録する。本便の結論は workflow ready であり、保存26段の checker PASS や新しい数学判定ではない。完了後は Task961 の source/実親監査へ戻る。

AUDIT_962_VERDICT: WORKFLOW_READY_RUNTIME_PENDING — one frozen checker pass over the unchanged 26-step prefix; no producer or old-suite rerun.

# Task1020 — WF5へ公開するP4 ABI追補と最終P/D pin

宛先: Task1019 wrapper作者・1018および後続wrapper監査官。rootが作者の最終公開schemaを読んで配達する。これはprivate実装/helperを共有する指示ではない。新fileの追補でTask1019のP/D共通化した仮字段だけを訂正する。新計算や新selftest群、通常語13fileの変更はない。

## 最終source

P4 `search/d972_r07_continuation_positive_word_readout_v4.py` = **252290 B / 0fc1c039d3ae076107585da88624c01656458c11d1d07df0054dcbec88fadeea**、LF4255。D4 `search/check_d972_r07_continuation_same_word_eleven_slots_v4.py` = **232750 B / 41d53b3779e26b04431a033877efbd315eb32b1d4538efa742bf900996db797b**、LF3679。Pの最後の修理は普通整数decimal容量の厳密な分類と対照、Dは新resource-selftestのcandidateだけfalse。最終独立監査とroot監査は別で、source完成から新実行成功を先取りしない。旧P3/D3小anchor pin/保持C9/C4/raw4はTask1019のまま。

## P resource-selftestのexact公開wire

top exact keys: schema/status/tests/fixture_scope/production_interfaces_used/paths/paths_receipt/reference_source/old_full_suites_run/candidate/cross_checked/verified/sha256。

schema=`d972.r07.continuation-positive-word.v1.resource-selftest`、status PASS、old_full_suites_runは普通整数0、三assuranceは全false。fixture_scopeは非空str。production_interfaces_usedはNodeStore/PagePool/WordDAG/read_normalized_pair/limited_lines/resource_path_gate/ResourceSession.before_write/canonicalの八名。各testsはTask1019のP三名を同順に持ち、status PASS、rejected_casesは非空strのlist。第一群追加keys=rows/cache、第二群=reference_source/word/root_id/root_sha256/normalized_pair/ops/old_full_suites_run、第三群=fixture_resource_limits_only=true。schema/hash/typeは実stdoutの全canonical bytesへ結ぶ。

**P topにsource_files/raw_inputs/work_roots/settings/counters/measurement/actual_*はない。Task1019の共通仮型をPへ要求しない。** 存在しない字段を補完・合成せず、Pの実public fieldsへ結ぶ。Dは従来の自系resource-selftest public型（old_success_suites=0等）をそのまま使い、両者をそれぞれのexact型で監査する。

Pのsource pinはreference_source={file,bytes,sha256}とpaths.producer={file,bytes,sha256}。実rootはpaths.scratch/paths.fixtures（絶対str）、paths_receipt={file,bytes,sha256}。pathsは `d972.r07.continuation-positive-word.v1.resource-v4.selftest-paths` のsealed objectで、exact bodyはscratch/fixtures/temporary_roots_only=true/delete_on_exit=false/explicit_scratch/producer。明示scratchはTask1019のREPORT/resource-selftests/P/scratch、fixturesはそのP parent内siblingへ結ぶ。実path receiptのfile/全bytes/SHAとREPORT内実fileに一致させる。Pの三raw/設定/計測は下記群別scratchの実start/telemetry/resultを読み、まだ無いtop名を作らない。

## P通常resource receiptの公開境界

schemaの共通prefixは `d972.r07.continuation-positive-word.v1`。scratch/start.json=`.resource-v4.start`、telemetry.jsonl各行=`.resource-v4.sample`、index-receipts/<六桁番号>.json=`.resource-v4.index`、result.json=`.resource-v4.result`。objectのsha256は自己字段を除いたcanonical seal。

startのbodyはinvocation/binding/format/cache/limits/fixture_only/resume。bindingはproducer/acceptance/parents/consumer_sources/raw_sources/runtime/accepted_owner/accepted_head/scratch_path/output_path/ordered_word_identity_unchanged_by_private_storage。source/受付/全16親/三rawは実全pinに結び、owner/headは登録旧64の実receipt、通常fixture_only=false/resume=false。限界はTask1015/1019の登録値。private formatをP/D共通にせず、旧sourceへ新pinを偽装しない。

sampleの実名はmemory/cache/indices/words/io_bytes/io_calls/fsyncs/session_scratch_reserved_bytes/process_scratch_reserved_bytes/max_fan_in/max_line_bytes/frames/max_frames/symbols/active_symbols/semantic_live_nodes/parent_object_overhead_bytes/snapshot。sample/phase/elapsed_seconds/last_sample_is_failure_peak=falseを添える。memoryはru_maxrss/ru_maxrss_unit/peak_rss_bytes/VmRSS_bytes/VmHWM_bytes/VmSize_bytes/rlimit_as_soft/rlimit_as_hard。indexの実actual_bytesはindices又はresult.index_statesの内側で、logical_bytes/durable_rows/rowsと区別。設定や欠測nullを実RSSへ読み替えない。

通常result bodyはstatus/session_sha256/word_result_sha256/root_id/root_sha256/word_manifest_sha256/indices/index_states/cache/samples/eof/successful_word_bundle/fixture_onlyと三false assurance。PASS時は二完成close済index、元wordのroot・result/word-manifest全bytes hashへ結ぶ。数学statusと別の資源保存票であり、これだけでは本P13file/D全比較の成功ではない。群別fixtureの低い枠と通常登録値を混ぜない。既存CLI・三群名・全数学親・全partialのalways保全はTask1015/1019を維持する。

# Task1042 — k128 source / 算術自己試験継承 / 共有TCBの独立静的監査

F0. **STATIC_PASS_WITH_REGISTERED_SHARED_TCB_AND_INHERITED_TEST_LIMITS**。新P3/C3と公開registryを静的に閉じる。現sourceに追加required findingはない。旧v1/v2全本文の既読監査996/1028、旧sourceの実全pin、全新差分と作者1036/1037全文を基点にした。新二群・新本走・新WF保全の実成功は未観測であり、この判定に含めない。Task1034のNOT_CREATED四字段 / OBSERVED五字段の限定修理は別票で凍結済み、本票から再編集しない。

許可変更は本票とTEMPのsource/hash metadataだけ。新旧source/WF/既刊票、数学入力treeは変更していない。PowerShell/.NETの既存JSON読取・全bytes/SHA・raw LF区間比較だけを行い、Python/import/AST/数学/GAP・GHA/network/git/credential・新agentは使っていない。私的算術本文を相手作者へ配達せず、registryの受渡しはrootだけへ行う。v220と返信163への進捗記帳もrootが担当する。

F1. 全六sourceの実freeze。Pは `search/d972_r07_fixed_lambda_cycle_batch_v{1,2,3}.py`、Cは `search/check_d972_r07_fixed_lambda_cycle_batch_v{1,2,3}.py`。全てASCII、CR0、BOMなし、最終LFである。

| ID | bytes | SHA256 | LF |
|---|---:|---|---:|
| P1 | 213861 | 229785eb91be9852c0d4189e67806c8fc7af7e07ef1ad3ec9650044e85427591 | 3463 |
| P2 | 208805 | 6626dbcad3400829baa0ac9f6ad00527ab1de002d253d41f39575f241f70d74e | 3420 |
| P3 | 209926 | a286dca4a2d94273d2496e16317579be06173e0e4802471b2840dc4263e5a3e8 | 3434 |
| C1 | 181828 | 7a4289506ce78b0ea562c63c9fb0841179a5bac10bc08165b211ed83982d292f | 2680 |
| C2 | 177544 | 4ada8490ef931e639159b2c3522510b6fc2da82551daa9a7aa3f1a1970d0ca90 | 2675 |
| C3 | 178914 | 1aebf6e47807466ec56426a55e34d0c7f622a5896c40184540e4d153060946d7 | 2695 |

作者票の実全pinも一致した。reply1036は18903 B / `2e052e034ac22aa5108f9b02f935f3162a7a92e8c30450ba77a8e9e09d2f9881` / LF154、reply1037は11196 B / `eb10977969e239795d670ea9c52ae36dce1c0442f6b68a7ff8bc54b5853447ae` / LF42。両票の全新二群・全CLI・未実行の末行を読了した。新P/C最終pin後の追加source変更は観測していない。

F2. 読了・比較の方法を限定する。公開1035/1040/1042と委嘱1036/1037を全文読了し、継承する1025・997・1000–1004・1011・1030の契約を適用した。旧v2の全文読了は同一全file pinを再認証して引き継ぎ、新P3のheader / WORKFLOW / 新二群 / diagnostic / CLI / main、新C3のheader / selector説明 / 登録helper / 全新二群 / mainを全文読了した。C v1→v2の切出しと追加gateも元本文と新本文で対照した。

registry作成では明示したraw LF行範囲の全bytes/SHAを測定した。続く別の読戻しは、元file bytesからLF位置を数えて直接区間を切り出し、registryの全60 descriptorを照合した。9つの不変regionは三版で全bytesが同一、2つの除外行は保存literalと実bytesが同一、全範囲は六source合計18367行を各一度ずつ覆い、重複・欠落0だった。関数のASTや一般parserは使っていない。途中のFC表示行番号は長行の表示折返しを含み得るため、registryの行番号・根拠には採用していない。

F3. 数学scopeと通常経路。起点は一貫して旧run33990567016/1 / head `c57c976c6ba4a9d57c2bd3c7de2a09b0d3cedd70` / artifact9977040548 / ZIP304642285 B / `a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792`、completed64・rank1450・generation8155・同固定lambda・同15親である。k64の受理1514や他走の1482を初期spanへ加えていない。全親/保持19Python/新P-C二本/raw3の認証経路は保持され、歴史batch sourceを数値helperとしてimportしない。

P `classify_batch`（356以降）とC `select_all_residuals`（192–246）は全54433弦・五carry・全residual・両auxを読み、m>0なら全failed列を保存して先頭min(128,m)、弦全零なら先頭非零aux一件、両auxも零なら同current lambdaのCOMPLETE_ZERO_CANDIDATEとする。全failed/全residualの128切捨て、DEPENDENT後の補充、候補毎lambda更新は入っていない。六cycleは零係数も保持する。P/Cの現在section/P1全8059・four-character・selected raw/source/primal/P1/four-B・source lower96776・physical lower32260・physical48384の本文はF6の実同一region又は公開された追加gateに閉じる。

物理消去は旧span＋それまで採用した行の挿入順。固定selection lambdaによるraw scalarが非零でも、先行採用行を引いた残余scalarが零になることを許し、残余行零ならDEPENDENTとしてrank/targetを進めない。全係数は零も保存する。INDEPENDENTでは外側sigma一回、数値targetは減算、literal correctionは `+signed_rep(theta)` を保つ。C `BatchReductionState`（279–380）と `literal_signs`（2181–2192）、P `reduce_candidate_numeric`（445以降）はこの区別を保つ。全旧行dot0 / 元startのprevious targetとcurrent targetのdot1を今回直接読む経路、最後一回のfinalizer、Linear/Separatorのtyped分岐、全new payloadと全保存prefixの比較も変更していない。

F4. 登録・保存境界。新schema/path/WFはv3、batch_sizeは普通整数128、max_batchesは普通整数1、refillはfalse、policyは `CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX`。bool/float/stringを普通整数へ同一視しない。Pのbatch-size CLIは128だけ、Cにbatch-size CLIはない。候補/新rowのlocal ordinalは0..127、private sequenceはselection1..3と `3+6*i+p`、最大771。127/771の正対照と128/772の負対照を通常保存helperへ結ぶ。

一相先だけのdurable tailとcommitted HEADのcountsを分離し、二相先を拒否する。source/owner/selectionのv2packetを新v3へ再開しない。strict count0 bootstrapは実resume=trueを保ち、一件ownerの二hostへの再rootは元invocation全bytesを保持する。完成packetのread-only resumeは新計算/書込みをしない旧規約を保つ。初回WFの指示はfresh P一回＋C全payload一回であり、sourceに保存されたresume能力を実行回数へ読み替えない。

F5. 新二群の実helper接続は静的に閉鎖した。

| 系 | 第一群 | 第二群 | 接続した新境界 |
|---|---:|---:|---|
| P3 | 30拒否予定 | 9拒否予定 | 実登録/owner/source/bootstrap/sequence/roster、BatchPhaseStore.ensure→実全tree保存→k128_tree_reload→accept→saved_selection_values |
| C3 | 28拒否予定 | 8拒否予定 | 実check_registration/row_source/compare_phase/ProgressAudit/invocation_records、CandidateFiles→全phase/selection/witness/view/roster比較 |

両群名は `k128-version-registration-and-types` / `k128-full-roster-cutoff-and-restoration`。第二群はm=64/65/127/128/129、選択64/65/127/128/128、各末尾非零を全弦末尾へ置き、非自明五係数と全六cycle/零係数を保存する。弦とaux非零の同居、aux-only、all-zeroを含む。過剰129・旧64 cutoff・全residual末尾欠損・第128witnessのindex/係数/語・末尾順序の各変異を保存readerへ通す。P3274–3289の末尾欠損対照は完成treeを一度保存した後、最後一byte/shape/hash/sealを改変して実reloadへ戻す。writerの拒否だけで済ませていない。Pの第128語対照は零係数cycleのedgeも読む。Cの語変異も実saved witnessとの全比較へ届くが、この新自己試験でEの全raw-word materializationを再演したとは主張しない。

Pのtree既存bytesは `packet/selection/tree` の全inventoryで比較し、新selection/witness/viewのdocumentsは別途全bytesで照合する。新刊以前のtree範囲修理を退行していない。Cのrow127正対照は12096 Bの先頭/末尾を区別した実保存行とfull descriptorを読み、128行目を存在させた負対照はIndexErrorでなく普通整数offset gateへ届く。全fixtureはfresh selftest-root内へ残し、削除なし。通常親/acceptance/outputとselftestを分け、TEMP/RUNNER_TEMP・regular parent・ancestor link/junction拒否を保つ。空dir/hiddenを含む三時点全不変/全ZIPentry/全stream再読は1030と新WF側の後続監査対象であり、本source票から実保存PASSを出さない。

F6. 不変本文の実region。行はraw LFの1始まり・両端包含、各行末LFを含む。次の各行は三版のbytesとSHAが全く同一である。P合計171752 B、C合計117893 Bの限定した実行本文を登録する。global BATCH_SIZEでパラメータ化された同じ本文であり、異なる前置長nで出力全体が同一という意味ではない。

| ID（registry順） | v1行 | v2行 | v3行 | 各版bytes | 共通SHA256 |
|---|---|---|---|---:|---|
| P-core-before-workflow | 79–2016 | 80–2017 | 80–2017 | 114836 | 2c394f88247d1d767a63ac7a0529a66089b3814409a0bc474a946e6d0f1cff12 |
| P-core-after-workflow | 2018–2890 | 2019–2891 | 2019–2891 | 56916 | be48b5ef5e519803b668a2679d5ff74be7702e7ca1c718586a65aa65db5de986 |
| C-primitives-and-selector-signature | 138–193 | 139–194 | 139–194 | 2092 | 910c5b1c8266de3069a40a8cf303bd8f1199ce5932dbd27e4378551a08c6b4de |
| C-selector-and-reduction-state | 195–456 | 196–457 | 196–457 | 14443 | a06ae680ec6064760162c24f6e862a64da6b4161dcbdb4a03b78c331044c66c3 |
| C-pinned-inputs-and-root-records | 568–1086 | 591–1109 | 591–1109 | 33981 | 24a8d482769e29d181c60c1c87681e07e4fc227fb321cc1292f217e8e84940b8 |
| C-selected-tree-and-witnesses | 1102–1254 | 1127–1279 | 1127–1279 | 9947 | 10e35b67be961b0408cf2af34497919a79da1d4f88053d6a9df996acd4ee11f1 |
| C-candidate-replay-and-final | 1270–1720 | 1296–1746 | 1296–1746 | 33463 | c444459e89cb79341d3f93999a10797cf181ec33a06d1cba13609bc486fed0d8 |
| C-input-result-diagnostics | 1794–1905 | 1821–1932 | 1821–1932 | 8946 | 5d8f1f3296d3d9350cc912571daa47a14a31ba6b78a3aafeea355b0e38f8f85a |
| C-whole-prefix-check-and-signs | 1938–2166 | 1966–2194 | 1966–2194 | 15021 | d90ac1acd6b7a448eb87135253ccaad6a0e13cd7006b89adcfd68a2e49ed3d22 |

F7. 除外と変更を同一本文へ正規化していない。P WORKFLOW実行literalはP1:2017 / P2:2018 / P3:2018の各72 Bで、v1/v2/v3 launch pathの相違をそのまま登録する。C selector docstringはC1:194 / C2:195 / C3:195の86/86/87 Bで、first32/64/128の説明の相違。両種類について元/中/新のraw UTF-8文字列（末尾LF込み）とbytes/SHAをregistryに全部保存し、`removed_by_normalization=false` とした。

不変region以外の9変更regionも全三版の範囲/bytes/SHAで固定した。P headerとcanary/CLI/diagnostic、C headerとcanary/CLIに加え、Cの (a) AcceptedInputsのheader/path gate切出しとstrict check_registration、(b) compare_phaseのordinal gate、(c) row_sourceのlocal offset gate、(d) invocation_recordsの登録helper呼出しとexact WF identity、(e) registered_basenamesのselected_count gateである。(b)–(e)の本文はv2→v3で実bytes同一だが、v1と同一とはしていない。count0 bootstrapの厳密型は旧1011からの保持であり、新k128算術変更と呼ばない。変更領域の静的意味判断とF6のraw byte同一性を区別する。

F8. rootが全文読了後にWF作者へ渡せる公開registryを凍結した。

`%TEMP%/shadow-atelier-audit163/k128-sources-and-inheritance-registry-v1.json`

**76867 B / SHA256 `9fe3d9cf1449c3535618a8c7618c6ab6e5fa4426f0f902c419fbbf91ad873b38` / LF878 / CR0 / ASCII / BOMなし / 最終LF**。

| top字段 | 型・用途 |
|---|---|
| schema | 固定str `d972.r07.fixed-lambda-cycle-batch.v3.audit-registry.v1` |
| task / status | 普通整数1042 / `STATIC_AUDIT_REGISTRY` |
| candidate / cross_checked / verified | 各false。registry固有の静的受領である |
| line_contract | encoding UTF-8 / newline LF / line_base 1 / 両端包含 / 各LFを含む / normalization NONE / comparison EXACT_RAW_BYTES / source_execution_in_this_audit false |
| source_files | F1の6件。各exact id/side/version/file/bytes/sha256/lf/cr/bom/final_lf/role。P1/P2/C1/C2はHISTORICAL_TEXT_ONLY、P3/C3はCURRENT_RUN_EXECUTABLE |
| inheritance | 下記の旧実自己試験参照と9不変region・2除外・9変更region |
| shared_tcb | F9の共有kernel4件と静的な呼先位置・call未計測の限定 |
| new_source_audit | 同旧64/1450/8155・15親/21Python/raw3・128/1/refill=false・新二群件数・作者票pins・新runtime未観測 |

`inheritance` のexact字段は status/arithmetic_selftest_inherited_from/old_mathematical_suites_rerun/historical_payload_reacquired_in_this_run/historical_sources_imported_or_executed_in_this_run/historical_sources_report_directory/historical_source_ids/current_source_ids/historical_source_files_are_additional_mathematical_parents/candidate/cross_checked/verified/historical_run/unchanged_regions/literal_exclusions/reviewed_change_regions/limits。statusはSTATIC_INHERITANCE_REFERENCE、継承元はd972-r07-fixed-lambda-cycle-batch-v1、旧数学suite再走0、payload今回再取得false、歴史source今回import/実行false、数学親追加false。歴史sourceの全fileはREPORT/audit-history-sourcesへ非実行資料として保存する指示であり、21Python/raw3や15数学親へ加えない。

各regionのversionsはsource_id/line_first/line_last/bytes/sha256の三件。不変regionはid/side/scope/comparison/normalization/versions、除外行はid/reason/removed_by_normalization/versions（各版にraw_utf8を追加）、変更regionはid/side/disposition/reason/versions。source_idはsource_filesの全file pinを参照する。WFは現checkoutの全六sourceを先にpin照合し、全登録範囲を同じraw LF規則で照合してから受領証を生成する。新二受領証 `arithmetic-selftest-inheritance.json` / `shared-tcb.json` を全REPORT保全とrun-receipt全file pinへ結ぶ。registry自身の実pinも来歴として保存し、未読の別regionや別sourceへ拡張しない。

`historical_run` は公開1040のroot前便全文受領への参照である。run34004423047/1、head `81a1b22975308ae0ac628f97da447a008a1d087e`、artifact9980697123 / ZIP94677901 B / `d21f9e0b93b070327b4ef02e975dc377a8020e7f8aa7553a720d97d690ed85f0`、旧P自己試験2409 B / `1bfb8b4404d1d24e481dd139b6b84136ef21e8e79b1fd3548607a66b45d1c238`、旧C自己試験1725 B / `2c8005f98883a711bece270552fa5f39f85755a8d06a27f0cf6c1b3fc257cdce`。三群はfixed-selection-full-roster-and-aux / dependent-independent-target-signs-and-packed / private-prefix-publication-resume-and-isolation、旧実拒否P7/6/26・C2/3/14。新runで取得又は再実行したPASSにしない。DEPENDENT/target/publicationを含む旧三群の歴史参照と、変更部分の新二群の実通過予定は別の根拠である。

F9. 共有TCB四行を実file/rangeへ閉じた。全file pinsは1040の四行と独立に一致し、次のraw region bytes/SHAを追加した。

| kernel / 系 | 実sourceと行 | region bytes | region SHA256 |
|---|---|---:|---|
| vectorized_projection_chunk / P | search/d972_r07_actual_grade2_root_scalar_batch_v2.py:342–357 | 1011 | b68bbb5af24240a8758fffa0902323727e0a22838f1acdaede8e1d1c867a5199 |
| vectorized_projection_chunk / C | search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py:269–284 | 1020 | 6e785bdf5b4fb8b2010b3645462ffaff8d84e2ff2e2c134eafa0425c18b4beaf |
| sparse_adjoint / P | search/d972_r07_targeted_grade2_owner_generated_join_v15.py:192–203 | 670 | 4b75584298a67005d5af61bd972d8dfe5069b65f1dd5d32bdeb345bf2eadbd39 |
| sparse_adjoint / C | search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py:192–203 | 670 | 4b75584298a67005d5af61bd972d8dfe5069b65f1dd5d32bdeb345bf2eadbd39 |

`shared_tcb` のexact字段は status/candidate/cross_checked/verified/kernel_third_independence_claimed/current_run_call_coverage/kernels/known_static_load_bearing_paths/limits。statusはDECLARED_SHARED_TCB、三assuranceとkernel_third_independence_claimedはfalse、call coverageはNOT_MEASURED。各kernel行のexact字段はkernel/side/file/file_bytes/file_sha256/line_first/line_last/region_bytes/region_sha256/kernel_third_independence_claimed/current_run_call_coverageである。

sparse_adjointの両rangeは全文同一。projectionは説明文とエラーlabelのbytes差を保った別hashであり、これを独立kernelの証拠にしない。P full_origin_refinement_v1:448とC complete_oracle_cegar_continuation_v2:236のpacked P1呼先を実sourceで確認した。sparse_adjointの今度の呼出数/発火枝は計測していない。retained docstring中のIndependentを現在の独立性へ昇格せず、F-fo-1/F-flb-1と公開1040/返信163 F8.89の限定を保持する。

F10. 現状と残る実gate。公開1040によりk64のrank1514/gen8219は限定9条のcross-checked受理へ更新され、rootのk64 metadata受領も別便でPASSしたが、新k128の親は同旧64/1450である。量は同固定lambda・同failed順・同消去順の前置長a(n)であり、a(32)=32/a(64)=64という既観測からa(128)・新rank・独立率・秒数を推定しない。旧32行全file一致も算術再演ではない。新v2第二群にはaux対照があったことと、本番aux未発火/DEPENDENT0だったことを分けて引き継ぐ。

新k128 sourceの静的監査と本registryは完成。rootのregistry全文読了と新WF3の独立全静読後、rootだけがGHAへ進む。そこで新metadata16、P二群30/9、C二群28/8、fresh P一回5400秒/7168MiB・C全new payload一回10800秒/7168MiB、外6000/11400秒、全入力/fixture/REPORT/archive保全を実判定する。old mathematical suitesは再走0。source完成票を新機械PASS・工房CV9・Leanへ読み替えない。new_lambda_oracleはnull、new final qは未計算、grade2両字段NOT_DECIDED、full_A0=false、verified=false、LinearだけNEW_BATCH_SAME_WORD_ADAPTER_PENDING・その他NOT_APPLICABLEを保つ。A0 actual0/1・階段1/6も自動昇格しない。

AUDIT_1042_VERDICT: STATIC_PASS_WITH_REGISTERED_SHARED_TCB_AND_INHERITED_TEST_LIMITS; SAME_OLD64_FIXED_LAMBDA_K128_ONE_BATCH_NO_REFILL; EXACT_RAW_REGION_REGISTRY_COMPLETE; NEW_TWO_GROUPS_AND_GHA_NOT_EXECUTED; ROOT_REVIEW_BEFORE_WF_HANDOFF.

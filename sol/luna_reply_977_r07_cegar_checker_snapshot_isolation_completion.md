# Task977 — snapshot隔離修理と保存32段checker completion

F1. Task977を全文読了し、指定の新checker v2・checker-only completion workflow・本返書だけを作成した。公刊v1/source/workflow/reply972/975は不変。ローカルPython/import/AST/数値/GAP、network/Git/GHA/credential、追加agentは実行していない。新producer算術は読取/import/コピーしていない。以下は静的source監査と実JSON/bytes/SHAの読取であり、新GHAの成功報告ではない。

F2. 独立に特定した原因は `PhysicalState.derived/summary` の `self.parents` 参照escapeである。`root_start_owner` と `snapshot_record` はsummaryを浅いsealへ渡すため、後続attachのappendが保存済みmetadataも変える。開始時に計算したstart hashと、全32段後の `head_record` が再計算するstart hashが相違し、既存の `HEAD_entire_replayed_prefix_and_cursor` gateが正しく拒否した。snapshotもattach前に生成し、receipt用hashをattach後に計算するため同じ問題を持つ。一箇所のhash固定だけでは十分でない。

実diagでは開始startの親列は二箇所とも33、snapshot0は33、snapshot31は64、producer terminalのDERIVED親列は65。旧checkerは32/physicalまで到達したが、`status:FAIL,candidate:false,all_new_committed_arrays_and_json_compared:false`、reasonは `ValueError:cegar_checker:HEAD_entire_replayed_prefix_and_cursor`。Pの `UNKNOWN_CAP/Separator,completed32,rank1418,generation8123` は候補であり、この返書では正式受理へ昇格させない。2145が維持する受理起点はrank1386/generation8091。

F3. 新sourceは凍結v1の複製に、metadata所有境界のdeep-copyを加えた。`derived` の親列、`summary` の親列/direct_pairing、`measure` の戻りdirect_pairing、最終checker receiptのdirect_pairingを切り離す。これによりroot start、各snapshot、そのsnapshotを参照するoracle/DERIVED receiptが現在stateの追記・深い字段更新から隔離される。全算術、14親pins、九phase、packing/source adapter、HEAD/terminal/invocation/全array比較、通常CLIとpayload schema `d972.r07.complete-oracle-cegar-continuation.v1` は保持した。HEADを実producer値からexpectedへコピーする処置や、等式gateの弱化はない。Task978は専用試験/CLI/docstringとこのdeep-copy差分を除く全source textがv1と一致することを静的に確認した。

F4. 新 `--snapshot-isolation-selftest` はGHAのみで走らせる専用三件。実 `PhysicalState`、実 `root_start_owner/snapshot_record/head_record`、一base行＋一実attachを使い、追記前start/snapshotと追記後currentの両方を保持する。attach後に旧snapshotのreceipt hashを計算しても元bytes/hashと一致すること、親dictの深い字段とpairingをstate側・export側から更新しても反対側が変わらないこと、current rank/generation/headは進むことを確認する。不正な旧aliasを故意に残したcontrolはbytesと実seal再計算が変わり、stale sealとして拒否されることを要求する。最終HEADのstart hashと実ファイルroundtripも通す。旧成功suiteは呼ばない。fixtureは親metadata admissionを再実行する試験ではない。専用schema末尾は `.snapshot-isolation-selftest`、`tests`三件、PASS exit0 / FAIL exit1 / UNKNOWN_RESOURCE exit3。

F5. 保存親はrun33984832010/1、head `b8c9e95ddd0183d9e43b7fcc961cb251fdaea13e`、旧workflow `.github/workflows/d972-r07-complete-oracle-cegar-continuation-v1.yml`、diagnostic artifact9975236748。nameは `d972-r07-complete-oracle-cegar-continuation-v1-diagnostics-33984832010-1`、ZIP101830254 bytes / `09ffef9d13e21e27fe9733bf997ec875a5795b5af56c7f4875e36725924d7a35`。root作成の58-entry表 `%TEMP%/shadow-atelier-audit163/cegar-v1-diagnostics-33984832010-a1-pins.json` と実展開rootの全58対象を独立にbytes/SHA照合し、全一致した。全2584output/420dirs/346710509 bytesのroot照合結果を受領し、新workflowも全file/dir/hashを再照合する。未観測のcompletion artifact pinは置かない。

| 実entry | bytes | SHA256 |
|---|---:|---|
| output/HEAD | 964 | d489c06d40f1b06a8924558e8f751d08cd2b40259790de398b93c79f3657760b |
| output/result.json | 28577 | 06c3053808179dd7706eb85fd30df8e1c360b5ee7f4640cd2a84581fe33a978a |
| output/start.json | 54707 | 87bd9b89c593d68fba65b765bfe9f17bcc47d52cc9afce6f53f8c131a24f816b |
| 旧checker-result.json | 1533 | ee5c936026da8ee228bf2d278eeb77c5a8e2c052ec3097271cf8c01871a8fb9f |
| 元source-receipt.json | 3643 | 3a50dd12025079a6089d15aac79573899e49692b61a53879adb9b0572342de6b |
| 元preservation-result.json | 388721 | bf1c0d9b0b1fbce83a91329ddbe2de20055c4a54835f639b800133afe893e524 |
| 既走oracle v2 full selftest | 869 | 094f69edc9a8aca33f4191b73b38453a5e758db73708e76ab0d262a8b75ffb44 |

F6. 新workflowは元14親＋失敗diagの15 live tupleをrun/attempt/head/repository/workflow/artifact id/name/size/digestで固定する。Task554と今回diagは役割付きfailure、他は成功親。diag全ZIP hash/2636entriesの安全展開、58実entry、元source19＋新v2末尾追加の20 Python/3 raw、GHA AST/LF/bytes/SHA、元source receiptとのjoinを要求する。raw三件にはLF正規化を行わない。runtimeはPython3.13.15/NumPy2.5.1で、元producerの記録runtime、新checker/repair receipt/launchを明示的に結ぶ。

新regressionは内240秒/外5分、修理Cの全32段一回は内10800秒/外190分、job230分、両実行に仮想memory上限7340032 KiB。producer実行/再生成は0、旧26scan・外部E・既走suite再走も0。既走oracle v2 full四件、旧P/C各三群、親metadata各五拒否は保存receiptだけを認証する。2145のF-sc-3閉鎖はこの旧full四件の実PASSに依拠し、E三件とは区別する。

全32の九phaseを新Cが再計算・全bytes比較し、HEAD/terminal/invocationまでPASSして初めて候補をuploadする。各過去snapshot receiptのhashが保存済み `start.json` の実bytes hashと一致することも最終metadata gateで確認する。全14親root、大きい親を含む全files/dirs、元diag全入力、コピーした元52receipt、producer全output、20source/3rawの前後不変をalways照合する。失敗はFAIL、不足はINCOMPLETEとして残し、旧FAILやresource停止からPASSを合成しない。

F7. rootの2145対応指示に従い、C完全PASS後だけ `coverage-receipt.json` を保存する。既照合の各snapshot `section/q.bin,kappa.bin,cochain/score.u8,b-aux.u8` をphase manifest SHA/dtype/shape/全EOFへjoinし、32 target.scalar、character0..3順の現在lambdaに対するzero-root flagsと非零packed-byte数、kappaのtag別d0/d1支持・shared aux8、scoreの6tag×2成分の非零trit数、b_aux2を記録する。四桁base3 packedを読むだけで、source/oracle/P/Eを再評価しない。`operator_identically_zero_claimed:false,all_four_characters_informative_claimed:false` を付け、現在lambdaでq=0と作用素恒等零を区別する。分布は新GHA前には予測しない。

同receiptのnormalizer規約欄はv547(4.2)/v548/reply965・957・971/2144訂正を参照する三表の記帳である。signed代表0→0,1→1,2→−1、rawの普通整数/6、P1普通整数mod54、18整除の剰余0/18/36とその普通整数商によるF3 normalized pair、oracle独立etaを保持し、新裁定や規約再評価は行わない。

F8. candidate直下は `output/` の元producer bytes、`original/` の元52receipt/log、元 `source-receipt.json`、新 `repair-source-receipt.json`、旧/new checker結果・stdout/log/exit code、新regression、`preserved-input.json`、`completion-intake-receipt.json`、全親before/after、`preservation-result.json`、coverage、`completion-run-receipt.json` を持つ。`checker-sources/` に旧v1と新v2の実source bytesを保存し、receiptのbytes/SHAへjoinする。最終completion receiptは元P32/新P0/C一回、旧FAILと新結果、元/修理source/runtime/launch、全prefix/current identity、全過去snapshot hash、coverage/source実体/不変receiptのhashを結ぶ。candidateは全PASS後のみ、always diagnosticsもhidden pendingを保持し、両artifact retentionは30日。

F9. 最終source/workflowのfreeze値は以下。元v1 checkerは120245 bytes / `8c000f9b49d04447a09c701daf5907a35b7f2e883f1e36747308a6d4ded29b1f` のままである。

| 新file | bytes | SHA256 | LF / CR |
|---|---:|---|---|
| search/check_d972_r07_complete_oracle_cegar_continuation_v2.py | 129557 | e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3 | 1819 / 0 |
| .github/workflows/d972-r07-complete-oracle-cegar-checker-completion-v1.yml | 90880 | 31b4d8fba2f680ae5e949daf910eec9c3e1f7d4a28946aeecca43ea212817042 | 1252 / 0 |

両fileはBOMなし・final LFあり。workflow markerは `[r07-complete-oracle-cegar-checker-completion-v1-run]`、workflow_dispatchもある。GHAで解決済み14親を使う再現CLIは次のとおり（本workerは未実行）。

```bash
parents=(--state-root "$STATE_ROOT" --delta-root "$DELTA_ROOT" --seed34-root "$SEED34_ROOT"
  --packet-root "$PACKET_ROOT" --refinement-root "$REFINEMENT_ROOT" --oracle-root "$ORACLE_ROOT" --e-root "$E_ROOT"
  --prepare-root "$PREPARE_ROOT" --block-root "$BLOCK_0_ROOT" --block-root "$BLOCK_1_ROOT"
  --block-root "$BLOCK_2_ROOT" --block-root "$BLOCK_3_ROOT" --p1-root "$P1_ROOT" --task712-root "$TASK712_ROOT")
root="$RUNNER_TEMP/completion"
timeout --kill-after=30s 5m python -B search/check_d972_r07_complete_oracle_cegar_continuation_v2.py --snapshot-isolation-selftest --max-seconds 240 --output "$root/snapshot-isolation-selftest.json"
timeout --kill-after=60s 190m python -B search/check_d972_r07_complete_oracle_cegar_continuation_v2.py "${parents[@]}" --candidate-root "$root/output" --output "$root/checker-result.json" --max-seconds 10800
```

F10. 保持TCBはTask972の独立系統の全算術、E checker966、oracle checker v2とE経由の旧oracle v1、accepted Conn/source-map/P1/Task554/Task712/packing/physical原始。2131 F-fo-1、2138 F-sc-1、2143 F-cy-4aのretained clone/decoder/contextの限界は今回のmetadata隔離では解消しない。lambda-rho2は明示DERIVED、原rho2直接読取や旧target履歴の数値再走は主張しない。全normalized word/最終11slot/grade2 MEMBERまたはNONMEMBER/fullA0/Lean verifiedは依然本gate外。新source/new regression/全32completionのruntime、成功artifact pins、新増分CV9はrootの実GHA後の残件である。Task978には全source/workflowと最終coverage/source保存差分を通知済み、最終監査票は別返書へ記録される。

AUDIT_977_VERDICT: IMPLEMENTATION_FROZEN; SNAPSHOT_METADATA_ALIAS_REPAIRED; OBSERVED_58_ENTRY_PINS_MATCH; REGISTERED_CHECKER_ONLY_GHA_AND_INCREMENTAL_CV9_PENDING; cross_checked=false; verified=false

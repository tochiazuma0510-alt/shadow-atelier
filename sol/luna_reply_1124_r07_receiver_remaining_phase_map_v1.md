# Task1124 — 稼働中receiverの残工程・回収順

F0. **限定読取り地図を完成、正式typed受領の完了は未観測。** 指示全文と対話帳末尾を読み、同一Task1112 receiverの選択23 raw区間、broker/lease境界と保存journalを読んだ。source全体の再監査・旧1112対照の再実行ではない。既PID19504/PID20272、親tree、source、旧票への操作0。v6追加gate0、既1108静的採択を待ちへ戻さない。

F1. 固定出発点はrun34161493396/1、head `a5b456a973f8a917f3af386d327061a02a0cf900`。1834/8539 limited7 cross-checkedはrootの採択済み状態、verified=false。将来1962・採用数・新lambda・停止枝は予測していない。receiverは524346 B / `89f8eddc42a3b4e594a670b0cc28fafe5fb087ba562f420085bc8a569299dc07`、全4687 LF。以下R行はこのreceiver、B行はroot broker、L行はlease-v4を指す。原source3本の最終pin一致を目録に保存した。

F2. 自系10:17:19–20Zにjournalのその時点prefix10367781 Bをread-only取得した。全prefix SHA `1ea7be941a99803bc6ba92cc1b2ea247fd7b04c34867f0b032ff22c400171340`、途中行0。保存した完全JSON末尾99行はseq10541–10639、最後は09:49:41.7589210Zのv4 acquired-audit-history Inventory後。rootの10:21:12Z票6095 B / `ffc5cce41d6e43cb68119bf9023558701e3644f0c27ab54e5497fc8f87ffbc99`はseq10640、R2232 before-Inventoryを観測している。**最新自系10:27:43.2025337Zはseq10641 /10:25:21.0408308Z、同v4 output Inventory後**。typed-reception.json / directory-stability-result.jsonはともに不存在。completion-check-v1が最新、地図v1のseq10640は先行時点として保持した。

F3. journal内callstackはイベント保存時の位置であり、現在のPCではない。seq10639だけではR1549–1632の二票/raw範囲/巨大Same比較とR2188–2231の16親配列/保全比較のどこかを決められなかった。seq10640でこの区間の通過、seq10641でR2232全output Inventoryの帰り側を確認できた。次のcontrols/live/registryの進行位置はUNKNOWN。経過秒から残時間を外挿しない。

F4. 正常経路の残工程を以下に固定した。表はseq10641で判明する下限であり、未記録の後続到達を断言しない。

| 順 | native文脈・固定呼出し | 範囲と観測 |
|---|---|---|
| 0 | 現在v5のR4170/4210/4255/4259/4261 | fixture再読、8history audit、17親、output、live、registryは今回のv4呼出しより前。PREPAREとの同一視ではなくRECEIVE直列順＋seq10603/10607/10609による到達。 |
| 1 | 歴史v4 R2232–2250 | output全hash後、controls/live/registry、ReadBatchParentEnvelope→ReceiveBatchParent→ReceiveBatchParentPrefix。後続v3 scopeは完了未観測。 |
| 2 | v3親 R354–402/560–746 | 全11437file/3475dir、whole outer ZIP、全fixture/inner ZIP、15親context・24source＋4history、128row・768phase・772checkpoint・1invocation、3selection/final。以前old74準備を代用しない。 |
| 3 | v3 evidenceを歴史v4へ結ぶR2244–2250 | v4 REPORT内36復元票、三時点×P/C fixture、transport、fixed、current-v4 intake/row roster/WF。 |
| 4 | 歴史v4 R2251–2649 | 五execution/各三群/metadata16、全候補・行・ordered reduction metadata、checkpoint/final/telemetry、invocation/診断/保全、最終REPORT Inventory R2585。戻りはin-memory、receipt_written=false、finallyで呼出元のdirectory bookkeepingを復元。 |
| 5 | 現v5 R2879–2923/4263–4277 | 完了した歴史v4全inventoryをpreflightへ結合、元16親/36-key header/353祖先/全checkpointを認証。同じ呼出しで形成したv3 objectsを受渡す。current REPORT36＋38復元票、v4三時点fixture、二つのfixed参照、current intake/1706親row/WFを結ぶ。旧PASSファイルのcache代用ではない。 |
| 6 | 現v5 R4282–4576 | 五start/result、P/C四群・第四実body、metadata16、actual P/HEAD/C/final、選択/処理prefix・各6相・accepted行・DEPENDENT/SKIPPED型、全checkpoint/最終祖先。件数は実processed/acceptedから読む。 |
| 7 | 現v5 R4578–4681 | coverage全manifest/telemetry、入力保全、単一invocation、診断履歴、8+6×actual processedのcost入力、signed P残差、最終run state、二self-exclusion込み全REPORT Inventory R4624、全取得files/bytes/dirs一致。 |
| 8 | R4682–4687→B167–193 | held確認、pre-write完了journal、typed CreateNew/flush/pin、broker再確認、handle解放、終了票、別OS終了観測。 |

F5. 残る負荷は異なる契約の読取りである。R369/372/389/399はv3全root・外ZIP・fixture全tree・内ZIP。R736とR3567は各native親の三保存時点×二ownerで通常各6回の全subtree Inventory。R535/R3542は歴史v4とcurrent v5という異なるREPORTの36/38復元票。R426/2366/4399は各manifestの全payloadとdirectory EOFで、phase coverageで同じfileが再hashされ得る。R1020–1034は各checkpointの保存selection/current-phase hashを再参照する。R3682/3683等は二つの参照ownerから同じold64実16payload＋manifestへ結ぶ。R2585とR4624はそれぞれ全v4/全v5の最終受領であり、前段output/fixtureと範囲が違う。巨大Same配列内の現在位置、データ依存の総回数、残秒はUNKNOWN。cache追加・scope短縮・旧PASS再利用・gate緩和0。

F6. 正常typedファイルはsession下 `typed-reception.json`、schema `d972.r07.fixed-lambda-cycle-batch.v5.root-metadata-reception.v2`、status `PASS_METADATA_ONLY`。全parent/source/transport/fixture/保全、current checkpoint/row/invocation/cost、最終Inventoryを通過して初めて形成される。candidate/cross_checked/verified=false、数学再生false、local CRC再計算false、inner seal再生成false、current kernel coverage NOT_MEASUREDを保持する。元serializerの古いformal_CV9_pending等は準備時の記帳であり、root2224の1834/8539限定採択を撤回する新判断ではない。

F7. root回収順は、(a) `full-receiver-completed-before-typed-receipt`を**書込前**と区別、(b) 完全typed JSONとB171の全pin、(c) `directory-stability-result.json`、(d) 閉じたjournalとroot所有OS-exit monitor PID20272の実終了票・stdout/stderr、(e) rootの正式typed採択＋五字段canonical登録。broker正常status `PASS_FULL_METADATA_ONLY`にはmain_returned、errorなし、release_errorsなし、全handle閉鎖、typed pinが必要。brokerのformal_inventory5は正常時もnullで、五字段を自動発行したとは扱わない。OS monitor終了ファイルのexact basenameは今回の指定/読取材料では未同定なので捏造せずroot手渡しに残す。

F8. 例外時はB172–182が元例外/phase/UTC/stack/行を保持し、pending境界があれば失敗後のdirectory観測を追加する。B183–187はfinallyで逆順全handle解放とjournal closeを試行し、後から終了票を書く。typed形成後のB168/169等や解放で失敗してもPASSへ昇格しない。終了票/journal書込み自体の失敗ならそれらの欠品をstderr/OS終了と分けて残す。directory handleはfile内容不変や全OS事象を保証しない。過去削除主体はUNKNOWN。

F9. 全8新TEMP材料の完全目録（本replyがpaper、JSONがmachine map）。目録自身の循環pinを避け、末行VERDICTまでの返信pinは引渡し時に測定する。指定外repo変更0。

| TEMP/task1124 basename | bytes | SHA256 |
|---|---:|---|
| input-preregistration-v1.json | 1542 | 754f6025bd4d3ee28b72eac224c54d4e40de55f0c60bc503ed0d026dfec9724d |
| journal-complete-tail-v1.jsonl | 141255 | 5e33b4598bc23036376b80c7540da68efd200a1d37edf7810336686a9e713da8 |
| journal-observation-v1.json | 9225 | c2a93f64f74a50123f0e285af3b212de0552f56e48368740c3677fbcb68c974f |
| source-range-and-boundary-map-v1.json | 14616 | 8db3c5256b8893a5ad94ed60cd5993aab1acd754f6f0827ae91d30ef3404e174 |
| source-range-and-boundary-map-v2.json | 14095 | 7f56c478a57af3add022d381efcab5d727e4b8c6225c13ffc6b5937b27a39665 |
| remaining-phase-and-recovery-map-v1.json | 24119 | 48399e8556a220be1cc44c93db118f784a8ddb8fd9abbb76c12d1ad7b8311bab |
| completion-check-v1.json | 6122 | 2290e3d220248d57bedeca455017f57c32875379adef28e4bee35e3f21b3be33 |
| final-material-manifest-v1.json | 6375 | 7dea46e76ec421ff78e15a1487d38ec50e4ba9c320be25fb5be0ef6e792e6a72 |

F10. source-range v1はmetadata生成時のPS配列展開/EOF指定誤りであり**無効な途中票**。保存を維持し根拠には使わない。v2が23区間の正しいline/offset/bytes/SHAを収載する。停止した追加生成コマンドは新票を形成しなかった。列挙範囲とcallsite検索は読了、未列挙helper内部の全再監査は未実施、P/C私的実装/親payloadは新規不読。OPENは実typed・broker・OS正常終了、root正式inventory5、最新の行内位置/所要時間。正式票到着時はこの地図を追加gateにせず1108のP→C→registry→driver→WF限定bindingへ戻る。

TASK1124_VERDICT: LIMITED_READONLY_PHASE_MAP_COMPLETE; FORMAL_RECEPTION_UNOBSERVED; V6_ADDITIONAL_GATE=0

F11. root後送によるbasename限定追補。OS monitorの既存出力先は `%TEMP%/shadow-atelier-audit163/root-task1112-directory-stability-process-end-v1.json`、monitor PID20272 / exec session26112。F7/F10のbasename OPENだけを閉じる。型付き受領本文 `typed-reception.json`、解放/異常/全pinを含む `directory-stability-result.json`、OS process-endは三者別物であり、いずれか単独の存在を他の成功へ読み替えない。この追補では新たな出力存在・終了・親treeを観測していない。旧8資料は無変更、旧返信9199 Bの全rawは `reply1124-before-os-monitor-erratum-v1.md` / SHA `9039c9401b59ff583a3f9ee66860b69ff8feb1147f9f394b7163ab2cf603f80c` に別保存した。新補遺 `os-monitor-location-erratum-v1.json` =3493 B / `efe9d03ff34f715dc2f284802d55666766101cabc8954079dbc2e85a5351b704`。更新後の全材料は `final-material-manifest-v2.json` に固定する。

F12. rootはC6公開artifact登録とtuple要素数の限定不一致を確認しTask1125をC担当へ委嘱した、と受信した。新C採択pinはまだ受けていない。1108はその公開delta/pinを後着で受け、P→C→registry→driver→WFへ結ぶ。相手C私的本文不読、既全監査を全面巻戻ししない。現P/C/driver/WF/registryは変更0、本補遺はv6追加gate0。正式handback待機へ戻る。

TASK1124_VERDICT: LIMITED_READONLY_PHASE_MAP_COMPLETE; OS_MONITOR_PATH_RESOLVED; FORMAL_RECEPTION_UNOBSERVED; V6_ADDITIONAL_GATE=0

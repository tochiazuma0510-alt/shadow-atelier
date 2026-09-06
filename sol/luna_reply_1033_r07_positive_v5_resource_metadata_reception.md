Task1033 — WF5 resource metadata の受領 helper

F1. 読了と限定範囲

Task1033 4463 B / 528c41e54c0ac96163ee510b886d16e90ca391dc2ef8bbb0288021ded114e28a（15行）、公開返信1022 24414 B / 515bf6dd39a91c180169dfceac79825b909e9433d2e43771863b5ef5a54c276f（245行）、公開Task1024 3396 B / 6abc0b1900fbc41e3a6f6ad386b5c5fe231249680efefbc341d473e179fd3875（20行）を全文読了した。補足1020も全文読了し、凍結WF5の公開resource serializer・実行・入場・保存部分を読んだ。WF5は180687 B / a840cebcd0ba3f15ff2c31c13b0a09bacd140cb4c8e756466baafd052df8e436、LF2556に一致した。WF全数学入場本文を本便で再監査したとの主張ではない。

変更は本返信と指定TEMP ASCII PowerShell helperの二fileだけである。公開P4/D4、WF5、1022/1024、k64 P/C/WFその他の公開source・票は変更していない。D私的source/票/fixtureは読んでいない。新Python/import/AST、PowerShell helperの実行、数学/GAP/network/git/credential/追加agentは行っていない。

対象launchは実run34009883488/attempt1、head a590fa9a70322145f1c0688a8f14d2c9640b1bf3。作業中にrootから、05:20:19Z APIでは本P工程が05:19:35Z failure、本D skipped、全保存工程もfailureでdiagnostic upload中との連絡を受けた。これは工程境界の伝達であり、本Pの実exit/status/reason/語量/資源値を受領したことではない。artifact ID・ZIP bytes/SHA・実payloadは未受領で、helperを実artifactに掛けていない。

F2. 新helperの入口と保存条件

指定file:
C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163/audit-r07-positive-v5-resource-metadata.ps1

作者最終pinは78114 B / SHA256 654ba851e96060401ebc231145aa112945e452b27b738595d866d8fdae98f85e、1067行。全bytes ASCII、CR0、BOMなし、末尾LF一件、行末空白0をmetadataで確認した。全文を静的に読了し、最終通知差分も再読した。これはPowerShell parser/AST・小fixture・実受領の成功票ではない。

予定入口はWindows PowerShell 5.1で次の二引数を与える。下のROOT/RECEIPTは説明用の置換位置であり、未来artifactの実pathを作ったものではない。

    & "$env:TEMP/shadow-atelier-audit163/audit-r07-positive-v5-resource-metadata.ps1" -Root "C:/.../ROOT" -ReceiptPath "C:/.../RECEIPT.json"

Rootにはroot brokerが安全に全展開したREPORTを渡す。ZIPからの直接受領や展開はしない。準備時点で展開容量を仮定して実行しておらず、rootが先にZIPを全保持・全stream読取し、完全展開rootを供給できるか判断する。helper自身は完全展開が前提であり、欠けた展開を資源停止の正常証拠へ置き換えない。

両引数は実ローカルdrive上の絶対path。Rootはdirectoryかつdrive root自体ではなく、ReceiptPathはRootの外の未存在fileで、親directoryは既存でなければならない。既存path componentのreparse pointを拒否する。これらのgateは書込前に置いた。入力は一切変更せず、唯一の実行時新出力は外部ReceiptPathをCreateNewで作る局所JSON票である。旧receiptやscratchの再利用、cleanup、入力の書換え、無言のsymlink除外はない。

F3. 全fileと型別JSONの読取り

全REPORTを一巡し、全regular fileをGet-FileHashのstreamで最後まで読んで実bytes/SHAを記録する。全directoryも列挙し、reparse pointと重複fileを拒否する。巨大なordered-word.jsonlやbinary indexも全byte hashの対象であるが、その語node/群/Fox/線形代数を評価しない。全入力を後でもう一度hashしたとは記さず、input_tree_second_full_hash_pass=falseを出す。rootの別全保存受領を代替しない。

JSONはPowerShell/.NETの既存ConvertFrom-Jsonで読み、公開exact keyset、必要字段、boolを除く普通整数、非空str、H、有限float、nullable値を型別に照合する。Pの公開exact keysetは厳密に扱う。普通整数と同値float/boolを一致扱いしない。比較用ConvertTo-JsonにはInputObjectを明示し、空配列/単一要素配列をpipelineでscalarへ落とさない。

sealed JSONは元のASCII・compact bytesにある自己sha256の一意なtokenだけを除き、その元bytesのSHAを照合する。新一般JSON parser・数値canonicalizerは作っていない。Pythonの任意JSON canonical formや重複key一般を独立に完全判定したとは主張せず、arbitrary_JSON_canonical_form_independently_proved=falseを出す。full-file SHAには元の自己sealと末尾LFも含む。index bindingの公開四字段だけは、型が閉じた固定formatのmetadata textで照合する。これは任意数値serializerの新設ではない。

各telemetryはStreamReaderで全行をEOFまで読む。実全file byte数と復元した各行のbyte数を合わせ、CR/BOM/行の脱落を拒否する。completeな各行は64 MiB以内（LF込み）で、P各行のsealも照合する。最終LFを欠く部分行は全file SHAに保持してINCOMPLETEとし、完了sampleを捏造しない。complete行の型違反は行番号を記録し、後続行の読取りを続ける。行数・Pの0始まり連番・非負有限float elapsedの非減少・全phase別の件数/最終elapsed/最終sampleを記録する。Dに未公開のsample番号字段は発明しない。

F4. Pの通常sessionと三fixture session

P mainはresource-P、P自己試験はresource-selftests/P/scratch/store、word、pathsの三個別sessionを読む。未形成sessionのstart/result/cache相当/index receipt/catalog相当はnullに保ち、状態NOT_CREATEDを記す。実directoryを観測した後の空listと区別する。

startは公開R.startの全exact fields、format private-P4-node42-v1、invocation32hex、fixture_only、resume=false、cache12字段、limits5字段を照合する。通常bindingは元acceptance全metadata・16親順・新P/D/source全pin・三raw・runtime全文・元owner/現HEADのFD・実旧host pathsへ結ぶ。fixtureはexact mode/producerだけの別型で、producer.fileがbasenameであることを維持する。通常full pathや16親の字段をfixtureへ混入しない。

resource-selftest topはP固有のold_full_suites_run/paths/paths_receipt/reference_source型を使う。source_files/raw_inputs/work_roots/settings/counters/measurement/actual_*というD側topをPへ要求しない。三群名/順・第一群13行と小cache設定・第二群の旧新短語全bytes/nullable pair/八op・第三群14拒否名を公開ABIへ結ぶ。新旧短語の比較はfile全bytesの同一性であり、既存P3の五群や本Pを再実行しない。除去対象は既に公刊されたparent-link一件だけであり、helper側で削除しない。

完了index receiptは各index-receipts/<六桁>.jsonとresult内objectを対応させ、purpose/number/binding/root/count/encoding/stride42/header48/EOFを確認する。binary SHAはheader込みの全file SHA、自己index sealとは別である。48+42*count、root_id=count-1、実file長、完成stateのrows/durable_rows/logical_bytes/actual_bytesを結ぶ。通常PASSだけはbuild/rereadの二完成indexと実word rootを要求する。fixtureの未完対照indexへこの二index条件を強制しない。

停止時の完成receiptだけはそのまま認証し、未完stateやbinaryも保持する。resultがない場合の最終sample中stateはsample時点の観測として記し、後の実file長へ偽の同値を要求しない。resultが形成済みならsession_sha256をstart全file SHAへ結び、samples実全行数、最終resource-session-<status>、cache/index_statesの全値を結ぶ。UNKNOWN_RESOURCE/FAIL/INCOMPLETEをPASSへ変更しない。

F5. Dの公開部分と未裁定範囲

root追加裁定どおり、Dの未公開exact keysetは推測しない。WF5が列挙したbinding/settings/measurement/selftest top/各群のexact型はそのまま確認し、sample/catalog complete/pass/selftest-paths等の追加字段は全JSONとfile pinとして保持する。局所票にはD_unpublished_extra_keyset_exactness=NOT_ADJUDICATEDを必ず出す。追加keysetのexactnessが結論に必要なら、rootが回収後の公開実artifactを全文読んで追補する範囲である。

D fixtureは一個のscratchと別sibling fixturesを対応させ、binding.json、samples.jsonl、selftest-paths.json、selftest-result.jsonとstdout全bytesを読む。loaded_source_files/raw_pins/runtime/source_path/fixture_only/original_producer_index_read=falseを結ぶ。三群の公開metadata、短い同一入力の全bytes、小D3/D4全payloadの全bytes、測定counterとsettingを照合する。negative fixture catalogは未入場の対照として全file hashに保持し、通常main catalogの完了証明書へ昇格しない。全slot/80644という小fixtureの保存主張を、本Dの新実完了と読み替えない。

main Dが形成されれば、resource-D/bindingとsamples、admitted-inputs、catalog-000000のstart/complete、nodes.index/ordered-edges.u64、00-mod54及び11 slotの計12個の完了passとremaining fileの全bytes/幅を対応させる。start/completeと同word FD/root/dictionary/ancestor件数、passとcatalog完了file SHA/consumed_edgesをmetadataで結ぶ。Dの型付きendpoint/Fox/群作用は再演しない。親ごとのroster_sha256は元値を保持し、任意親object用canonicalizerで新たに算出したとはしない。

main Dが未形成ならNOT_CREATED、catalog/passが部分形成ならINCOMPLETEを明示し、空の成功Dを合成しない。D本番完了receiptが存在する場合も、ここでの合格は公開resource metadataの範囲に限る。

F6. 八型対照・外側receipt・全保全への接続

resource-public-type-canary.jsonのexact fields、八拒否名の順、元D fixture binding全SHA、各mutantの全seal/file hash、実fixture inventoryを読む。六budgetはpage_cache_limit/page_bytes/line_limit/scratch_limit/free_floor/max_rss_bytesである。通常元値はordinary int、対照値は同値floatであることと実System型名を記録する。top/sampleの残二件も実payloadへ結ぶ。新たな対照実行はなく、保存された八件のreceiptを受領するだけである。

P_SELFTEST/D_SELFTEST/P/Dの各commandとexit receiptを別々に読む。実launch、source全file、registered内外秒、memory、scratch、argvのresource引数、layout全file SHAを結ぶ。command/exit/stdout/stderr/exit-code fileの全bytes、開始終了UTCの順、独立outer wall_secondsを記録する。新Pの実status/exit/reasonは固定しない。形成されないcommand、stdout、exitは欠品として明示する。

resource-output-inventories.jsonの四role/host path、OBSERVED/NOT_CREATED/FAIL、実全file/dir EOFと全FDを結ぶ。INCOMPLETEの欠品を補完せず、全16親/whole envelope/最終保全そのものの最終裁定はrootの別受領へ残す。普通entryを隠して成功させる一般除外はない。

F7. 局所statusと測定の意味

| helper status / exit | 意味 |
|---|---|
| PASS_RESOURCE_METADATA / 0 | 対象の形成済み公開resource metadataと必要完了対応に矛盾・未完がない。数学envelopeのPASSではない |
| INCOMPLETE_RESOURCE_METADATA / 3 | 元の非零exit/停止status、未形成session/receipt、部分最終行、未完catalog/pass等を観測。実内容を保持し、完了を推測しない |
| FAIL_RESOURCE_METADATA / 1 | 公開型/全file pin/自己seal/metadata対応の矛盾、unsafe path等。元本Pの数学FAILと同じ意味ではない |

ReceiptPathのpath gate以前の引数/path失敗は書込みを許さず例外終了する。安全な外部receipt pathが確定した後の局所照合エラーはerrorsへ保存し、独立した他sessionの読取りを続ける。既存のscriptblock dispatcherにはcallerのlabelを捕捉しない別名引数を使った。

資源値は最終sample本体、全phase集約、session result、外側実行票を別々に保持する。ru_maxrssはKiBとbyte換算、VmRSS/VmHWM/VmSizeは別のnullable実測。未観測peakはnullであり0を埋めない。max_observed_ru_maxrss_bytesは観測sampleの最大で、失敗瞬間/全phaseの峰を保証しない。

cache payloadとPython object overhead、IO bytes/calls/fsync、session/process scratch予約、actual binary長、line/floor枠を混同しない。sample/result保存そのものの後で増えるIO/fsync/scratch値との完全一致は要求しない。Pのsemantic_live_nodes/parent_object_overhead_bytesはnullのままである。7168 MiB、64 MiB、16 GiBは登録値であって実peakではない。語nodes/edges/zero_power_edges/refsは各観測purposeの実metadataとして保持し、本語完成の推定に使わない。

F8. freezeと残る実受領

helper全文1067行と本票を静的に読了した。本文の最終自己確認では未観測peakと未形成indexのnull、配列の型保持、相対file全文字列のordinal比較、PowerShell動的scopeのlabel捕捉回避、drive-rootの拒否を明確にした。実P/D source/数学/旧WFを修理したものではない。

rootは同一helper 78114 B / 654ba851e96060401ebc231145aa112945e452b27b738595d866d8fdae98f85e の全1067行を静読し、現時点の必須修理なしと連絡した。そのsnapshotからsourceは不変である。

helperは未実行で作者freezeとする。rootの本票読了、ZIP実全受領、安全な完全展開rootの用意、実metadata受領が残る。artifact pinはlocal票でnullのままにし、rootの外側取得票へ結ぶ。本便では新受領receiptを生成していない。all_sixteen_parent_bodies_reauthenticated/whole_envelope_or_final_preservation_adjudicated/local_canaries_executedはfalse、candidate/cross_checked/verified/math_replayも全falseである。CV-9とLeanは別判定で、本語成功・全11slot・全80644・A0/grade2の成立を主張しない。

AUDIT_1033_VERDICT: RESOURCE_METADATA_HELPER_COMPLETE_STATIC_ONLY_UNEXECUTED

# Reply1070 — envelope-v3 完成候補受領器の独立静的別読

F0. 判定は `LIMITED_STATIC_COMPLETED_CANDIDATE_RECEIVER_PASS_GUARD_CLOSED`。他作者の1069受領器の変更差分と影響する公開metadata経路に、残る必須修正は見つけていない。新helperは未実行、完成candidate・新研究run・新rankは未受領である。作者最終helper259814 B / SHA256 `9f9e920b82a0525c41f3eb2aa563a4e5c5d0ba0993deeb7ac16b2a62c9fab826`、LF2444/CR0/ASCII/BOMなし/末尾LF/行末空白0を対象として凍結する。Task1070全文4501 B / `f2dcbafba4d7f25a4bd96e2115200537c52e648338ee267e2cf61090d7a354cb` とTask1069全文4922 B / `1829743326631118f7634d10221495124ae718ae1d39a25e216f994d9fb82b03` に従った。

F1. これは1069受領器の独立差分監査であり、自作1064 WF/driverの再独立監査ではない。旧基点247138 B / `99bc57568e9eb721050084e96c1cbfb5f870d4ecf084ca3a0ecf5ee8336da812` の全体受理はrootおよび1063の既読根拠を保持する。返信1058全文13468 B / `41fec0811c4df79ec8e68d44881cf63ebe28844ed3a1f45281446970ca35fc78` と返信1063全文15102 B / `a3a4e977523f31e6814a780361ee82b64172ff13eb52091295d24706d6a2edf0` を読了し、旧基点全域を今回新たに読んだとはしない。

今回の読了範囲は、旧→draft2全238行差分26973 B / `9b9233d680714f6aad263f5a114bb9184bc8b7d11e713c97718a97e877a2aef9`、draft2→3全111行差分12211 B / `7b28b057ffffce0fc8d5bc0596bc1b257872e6082366987b39e4e76e65b45d9e`、最終draft3→4の二行差分である。現helperでは1–190、204–244、342–417、499–573、723–847、1087–1300、1484–1546、1661–1721、1897–2444を全文読了した。追加二関数、変更したregistry/P37/配置、保持R4と型/全file述語、全main・末尾、および呼出接続を含む。公開driverの参照票serializer全84行、実save定義と呼出部、bootstrap全58行、recheck全38行も比較対象として読了した。大きい公開範囲台帳の一度の表示切詰めは範囲本文の静読証拠に使わず、必要shapeの小分け再読と以下の全raw比較で扱った。

F2. 最終版までの全raw区画を、作者helperを呼ばない別のPowerShell/.NET metadata比較で照合した。基点61区画→現63区画、保持54・変更7・追加2・削除0。各rangeの実offset/bytes/SHA/LF、gap/overlapなしの両EOFを全照合し、保持区画は全raw一致、変更区画は実不一致を確認した。保持部分と保存差分の順方向再構成は新259814 Bに一致し、完全逆置換は旧247138 Bに一致する。61区画は明示main/tailを分けた本票の区切りであり、過去票の別区切り数から未申告変更を推論しない。

変更はMODULE_PREFIX、ReadV4PublicAuditRegistry、AuditV4CurrentTransitions、AuditProducerBodyReference、ReceiveWorkflowEnvelope、MODULE_MAIN、MODULE_TAIL。追加はReceiveFixedReferenceReceipt、ReadProducerCurrentReference。Same/PlainInt/FilePin、ReadFixedReferenceManifest、通常SavedFileManifest、旧親/現在checkpoint/観測/診断、全ZIP・fixture保存の保持区画を旧rawへ結んだ。保持raw一致を、未測定の通常呼出coverageや新数学PASSへ読み替えない。

F3. 新版の公開入力と配置対象を全実file bytes/SHAへ結んだ。作者のstatic inputs全18件、最終delivery全8件、作者返信も実pinに一致した。

| 対象 | bytes | SHA256 |
| --- | ---: | --- |
| 小WF envelope-v3 | 22153 | `56a8349fd54b16d63da9de2c4762ed04328ef1373f65af45c46019e745a1859b` |
| driver_v2 | 536145 | `35f73f5d1b8b519a69773690db8f8e514b3cc1d2792cc595ecdc0b92dede7a0c` |
| current registry v2 | 236390 | `84f5bbc6a85e77915535968e4342c09b6bf3e5b94638ab14184c67ca677ce114` |
| metadata修理後P4 | 290457 | `a58f7c116558fdc430025a9e095d29d0b04e0f20c9295264fca58a4c13510d0a` |
| 保持C4 | 261170 | `a29380ec00876225cc618c7025d671a3da79aea3b31b829dedba13c59ba84633` |
| 旧小WF archive | 20296 | `c8dc698160b41a21e338cc5a099f4e4abb51a369247a48fbfbd17c907dd02623` |
| 新P37公開入力 | 17587 | `768cbfec35dae2abc80cade25f184c626bef07a8fefb758383a8669e23a0ebed` |
| 新P全current公開入力 | 267079 | `b36818b41ab82ea33e2008e6db921e9cfb4138af472a473b47bbeac2eac063b9` |

ReadV4PublicAuditRegistryのschema v2/task1064・全8 source・source receiptの現P/C pinを確認した。実rawをopaqueに読み、P122→137区画の104不変/18変更/15追加/0削除、C96→117の79不変/17変更/21追加/0削除を独自に照合した。全472範囲・254分類は全EOFを覆い、新P公開票のsource_file/current_transition/旧4loader全metadataはregistryの対応全体へ一致する。旧60範囲・歴史6 source・共有TCB4と今回全遷移は別の対象である。旧registryから歴史registryおよびshared_tcb全metadataの不変も確認した。

旧8 loaderの全LF rawを独立照合した。文脈札は旧64/rank1450/gen8155/15親と、後段の別batch-parent adapterを分け、current_run_call_coverage=NOT_MEASUREDを保持する。本便ではP/C私的数学本文を解釈せず、文脈の数学的再監査は主張しない。P37はP3・修理前P4・今回P4の三sliceをopaqueに照合して全一致し、その37には旧4 P loaderが含まれる。旧14933 B/4718d96a…票は歴史登録であり、新17587票の代用ではない。通常受領器は修理前offsetを型付き来歴として扱い、修理前archiveを実行時に要求せず、局所再読falseを出す。今回の静的三slice比較とは区別する。

F4. ReceiveWorkflowEnvelopeと公開shellを比較した。前後SHA票の各7行は、checkout driver_v2/REPORT driver、checkout巨大archive/REPORT巨大archive、checkout旧小archive/REPORT旧小archive、active WFの順。bootstrap/recheck各stdout六つのOK行は順序の差も含め一致させる。before/after txt、二SHA票、二stdout、二stderr、bootstrap exitの計9 plaintext票は全字列/LFで照合し、完了受領ではstderr空・exit0を要求する。

task1064.driver-placement.v3のprevious各字段、previous_raw_copy_equal、current_producer_metadata_repair_registered、retained_mathematical_source_pins_unchangedを実public serializerへ結んだ。workflow-envelope-v2.ymlを含む配置9fileの全pre-P pin、全5 executionの実argv、CHECKOUT/REPORT、launch、最終全REPORTに接続する。パスは未形成の実argvから補完しない。旧Parchiveはruntime配置7fileに含めず、存在しないrun receiptの配置字段も要求しない。全closureは21 executable＋3rawを維持し、非実行の歴史sourceを新しい数学親へ加えない。

F5. ReceiveFixedReferenceReceipt全75行とcaller/末尾を読了した。公開driverのsaveはcanonical(value)をxb保存しsealを加えない。したがって新batch-fixed-reference-receipt.jsonはplain17字段・inner sha256字段なし、全file SHAは別に照合する。schema/status/両manifest pin/geometry/roles/relative_directory/両inventory、普通整数JSON5・binary11、全false assuranceをexactに要求する。

元R4の親参照9字段と旧64の実payload-owning manifest8字段を分け、旧64へstart_sha256を追加要求しない。旧owner/sourceの全pinとscope、16 descriptorの順序、JSON5の三字段射影、binary11の五字段・型付き正のshapeとbyte積を確認する。旧64は16 payload＋manifestの全17files、参照親側はmanifest1件の各全inventory/空directory列へ照合し、全実bytes/SHA/EOFを要求する。親/currentへpayloadを生成せず、generic phase/row readerを緩めない。

geometryは認証済みoracle全inventory内の唯一のoutput/geometry/manifest.json pinと、両fixedのaccepted_geometry_stage_sha256を結ぶ。同CLIではoracle manifest本文を局所再読しないため、oracle_geometry_manifest_body_read_locally=falseを明示している。新票はbatch親受領後・current intake前に読み、acceptanceの両anchor、pre-P controlsの実file pin、producer-startのcontrols SHA、最終全REPORTへ接続する。公開driverの実受付順と保存bindingに依拠し、保存されていない時計順を再計算したとはしない。

F6. 保持述語と全mainを確認した。Sameの型付き再帰比較、PlainIntのint/long限定、Finiteのdecimal/double等の有限非負読出し、LocalPath/Pinの文字列型・相対正規path・非reparse・全file SHAを維持する。新ordinary数値をboolや等値floatで受理する比較へ置換していない。固定pin付き公開票の内容認証と、未形成の実run/ledgerのtyped照合を分けている。

全16親、旧64と別batch-parent1578、旧128行/225 DERIVED、全旧prefix、現在の全候補/六phase/row/targetJSONとpacked hash/ordered elimination・checkpointを保持する。現在のrankは1578＋今回acceptedという型の結合であり、親の128行や速報を今回結果へ流用しない。DEPENDENTは行/target不変とnull字段、Linear/Separatorはそれぞれの型を保ち、停止記録を完成判定へ変えない。

旧36 empty dirsと三時点fixture、全ZIP/file/REPORT、二診断、入力保全、seq3のcurrent oracleと初回処理seq9以上、committedと先行durable tailの分離を維持する。未保存の歴史HEAD本文は識別子と実checkpointの照合範囲に限定し、局所CRC再計算falseも残る。通常mainは完成candidate専用であり、早期failure34040070261/1の5 execution null・preservation FAILを受理する用途には使わない。その実failureは既受理1066の別scopeである。

F7. capsはbatch_size128/max_batches1/refill=false、P5400秒/C10800秒/RSS7168 MiB、外側P6000/C11400秒、単一fresh invocationのまま。P[30,10,6]・C[28,9,6]は各数学2群＋親metadata1群で、driverはmetadata16・数学0・親metadata0。旧数学成功suiteの追加再走0を維持し、本便でも新旧各群を実行していない。新source pin/静的継承一致から新算術PASSや完走を推論しない。

F8. draft3から最終版への差分はL25の承認コメントとL28のExpectedApproval=2196だけで、逆置換はdraft3全259791 B/270d169fa8bce7bb3d25710e986c767c97a51b9ccb6e9b300caf841b7a9b54b4へ一致した。根拠express全文2809 B / e7193b44aa883b1b2d486e9a0e71f9f7304852efed001d2d461457c3f9683fbd、裁定snapshot全文2481 B / 9a74ecc2ff174a01fe441f71a4a54e9870d1b8b640df49a269b62d4b0268233bを読了した。

2196はexact5/caps/一回と1067/1068/1069最終pin提出を条件とする承認である。整数2196を、条件発効・実launch・実artifact・研究成功へ格上げしない。最終helperのImplementationComplete=false、ExpectedLaunch=null、ExpectedArtifact=nullと入力外ReceiptPath/非reparseの拒否を確認した。後着実handoffをrootが別snapshotへ結ぶまで、この保存版の実受領器を起動しない。

F9. 独自機械票はすべて `%TEMP%/shadow-atelier-audit163/task1070/` にCreateNew保存した。受領器の関数を呼ばず、直接PowerShell/.NETで原pin/opaque bytes/JSON metadata/全文字列だけを比較した。

| 独自票 | bytes | SHA256 |
| --- | ---: | --- |
| receiver-raw-boundary-review-v1.json | 79368 | `d8345ae68ec7ddf5291c12e3b0d11a958d89c5db5761e68db97193db7f319d52` |
| static-input-pin-review-v1.json | 13599 | `d20db37f326f92c8aec12e016892c3638cf0a760ee369ef11ec3c6ffe02e3159` |
| public-opaque-range-review-v1.json | 378625 | `99d404a786215064d8158d335d4f9567d1cf9f41737f2ee5289624ddee1aa3c6` |

作者最終全返信F1–F8/全表/末行10943 B / `e6c4dbbf892f3fc94dffecd4a2285523795791a3d872f2ec0e704d16affbdaee` を読了した。作者全raw差分v2 JSON71956 B / `17c5457866aa3f93222906b59a03d38acfd2b256710cf65f1e4dd63a4302f0a2` とtxt185398 B / `217baaac932ee9006363c2d39d806d58296cbe169470ee32143f17a9eeac031c` は実pin一致、全範囲の独自再計測根拠は上記第一票に保存した。作者のopaque比較446866 B / `575ca0e860b4bdc82c9d7356e87bc71d46e6bb3c3caac67b6d5c4046afc2e79e` は既存の計測主張として区別し、今回の全472/254/37照合は第三票へ独立に保存した。

F10. 変更したのは本返信と指定TEMP/task1070だけ。原helper/全原票/候補P-C/WF/driver/registry/実入力treeは変更していない。受領器・P/C/source・数学・Python/import/AST/compile/GAP/Git/GHA/network/credentials・新agentは実行していない。独立P/C数学、新CV9、正式grade2/全A0、cross-checked/verifiedの判定ではない。完成candidateの実metadata受領と、その後の研究裁定は残っている。

AUDIT_1070_VERDICT: LIMITED_STATIC_COMPLETED_CANDIDATE_RECEIVER_PASS_GUARD_CLOSED

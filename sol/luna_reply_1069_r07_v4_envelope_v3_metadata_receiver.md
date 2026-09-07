# Reply1069 — envelope-v3 完成候補用 metadata 受領器の静的完成案

F1. 新受領器を `%TEMP%/shadow-atelier-audit163/task1069/audit-r07-batch-v4-metadata-v2.ps1` に保存・凍結する。259814 B / SHA256 `9f9e920b82a0525c41f3eb2aa563a4e5c5d0ba0993deeb7ac16b2a62c9fab826`、LF2444、CR0、ASCII、BOMなし、末尾LF、行末空白0。完成candidate専用の公開metadata経路を接続した静的案であり、新helperの実行・実受領PASSではない。`ImplementationComplete=false`、`ExpectedLaunch=null`、`ExpectedArtifact=null` を保持する。後着の条件付き承認2196だけを実express全文から登録した。具体発効条件と起動はrootが扱い、実tupleは後着時に別snapshotで結ぶ。

F2. 基点1058は247138 B / `99bc57568e9eb721050084e96c1cbfb5f870d4ecf084ca3a0ecf5ee8336da812`。同dirの `baseline-1058-metadata-v1.ps1` はその全raw保存である。原1058 helper/返信、1063返信、1066の実失敗受領成果は変更していない。Task1069本文4922 B / `1829743326631118f7634d10221495124ae718ae1d39a25e216f994d9fb82b03`、1058/1063最終返信、公開承認された1064/1065最終返信と各delivery台帳、新小WF全368行、影響するdriverの公開serializerを読了した。P私的数学本文・私的実装票は読んでいない。

新しい固定対象は次のとおりである。P/C sourceは全bytesと公開LF範囲をopaqueに照合した。本文の算術解釈・実行を伴わない。

| 対象 | bytes | SHA256 |
| --- | ---: | --- |
| active v4 WF、envelope-v3 | 22153 | `56a8349fd54b16d63da9de2c4762ed04328ef1373f65af45c46019e745a1859b` |
| driver_v2、REPORTではdriver.py | 536145 | `35f73f5d1b8b519a69773690db8f8e514b3cc1d2792cc595ecdc0b92dede7a0c` |
| current registry v2 | 236390 | `84f5bbc6a85e77915535968e4342c09b6bf3e5b94638ab14184c67ca677ce114` |
| P4、metadata修理後 | 290457 | `a58f7c116558fdc430025a9e095d29d0b04e0f20c9295264fca58a4c13510d0a` |
| 保持C4 | 261170 | `a29380ec00876225cc618c7025d671a3da79aea3b31b829dedba13c59ba84633` |
| 非実行の旧小WF、envelope-v2 | 20296 | `c8dc698160b41a21e338cc5a099f4e4abb51a369247a48fbfbd17c907dd02623` |
| 非実行の旧巨大WF、envelope-v1 | 599085 | `e22c225a3f8706b648543c260b3ba603f6b6620cdcfadcdf573199b0f4f339f4` |

F3. `ReadV4PublicAuditRegistry` は schema `d972.r07.fixed-lambda-cycle-batch.v4.audit-registry.v2`、task1064へ結ぶ。全current範囲は472、分類は254。Pは122→137、同一104/変更18/追加15/削除0、Cは96→117、同一79/変更17/追加21/削除0である。各区画の全LF/bytes/SHA、全分類、gap/overlapなしの両EOFを読む。歴史registry76867 B/`9fe3d9cf1449c3535618a8c7618c6ab6e5fa4426f0f902c419fbbf91ad873b38`、歴史60範囲、歴史6source、旧8loader、共有4kernel、実行closure24 file＝21Python＋3rawは保持する。古い60範囲を今回変更の証拠に読み替えない。

追加公開入力をCreateNewで自身TEMPへ全raw複写した。

| 自身TEMPの入力名 | bytes | SHA256 |
| --- | ---: | --- |
| registered-producer-body-inheritance-v2.json | 17587 | `768cbfec35dae2abc80cade25f184c626bef07a8fefb758383a8669e23a0ebed` |
| registered-producer-current-regions-v2.json | 267079 | `b36818b41ab82ea33e2008e6db921e9cfb4138af472a473b47bbeac2eac063b9` |

P37票のschemaはtask1065.static-body-inheritance.v1、旧14933票は登録の来歴として別に保持する。通常受領器はP3と今回P4の全source/SHAおよび37 bodyの全rawを照合し、修理前offsetは型付き来歴として読む。新current票のP全137区画・全比較・4loaderを今回registryの該当全字段へ一致させる。旧4 P loaderは37 bodyの内数であり、41独立範囲とは呼ばない。修理前P archiveはruntimeの7配置fileへ含めない。

静的準備の追加metadata比較では、8 sourceの全pin、全472範囲/254分類、8loader、37 bodyを独自にraw照合した。37については非実行archiveもopaqueに読んでP3/修理前P4/今回P4の三slice一致と旧登録offsetを確認した。これは静的公開入力の照合であり、通常受領器は修理前archiveを要求せず、その本文を再読したとも記録しない。

F4. `ReceiveWorkflowEnvelope` はtask1064.driver-placement.v3 / task1064.driver-placement-after.v3へ接続した。shellの九つのplaintext/log票を全字列・順・LFへ照合する。前後各7 SHA行は、checkout driver_v2/REPORT driver、checkout巨大archive/REPORT巨大archive、checkout旧小archive/REPORT旧小archive、active WFの順である。各stdoutは公開shellどおり六つのOK行で、前後の順の違いも保持する。

公開before字段にprevious_repo_file/report_file/bytes/sha256、previous_raw_copy_equal、current_producer_metadata_repair_registered、retained_mathematical_source_pins_unchangedを結んだ。`workflow-envelope-v2.yml` を含む9配置fileを全pre-P controlsへ結び、全5 executionの実argv、実checkout/REPORT path、最終全REPORTへ接続する。今回未形成のargvからpathを補完しない。存在しないrun receiptのplacement字段やold P archiveのruntimeコピーを要求しない。

F5. 追加 `ReceiveFixedReferenceReceipt` は `batch-fixed-reference-receipt.json` を読む。公開driverのsaveはsealを付けないため、これは **plain 17字段、sha256字段なし**。schemaは `d972.r07.fixed-lambda-cycle-batch.v4.workflow-v4.fixed-reference-receipt.v1` で、全file SHAを別に照合する。status/roles/relative_directory/二manifest descriptor/geometry/二inventory/普通整数5・11/全false assuranceをexactに確認する。

元1058の `ReadFixedReferenceManifest` は全raw不変。親・current fixed manifestの9字段と、旧64 payload-owning manifestの8字段を分離し、旧64にはstart_sha256を要求しない。新票は旧64の実owner.scopeにも照合し、順序付き16 descriptorのJSON5三字段射影・binary11五字段/正の普通整数shape/bytesを読む。親側はmanifest一件、旧64側は16 payload＋manifestの全17 files/空directory列であり、全実bytes/SHA/EOFを照合する。payloadを親やcurrentへ作らず、一般phase readerを緩めない。

geometryは認証済み全oracle parent inventoryの唯一の `output/geometry/manifest.json` pinと、両fixed manifestのaccepted_geometry_stage_sha256へ結ぶ。同CLIにoracle実rootはないため、geometry manifest本文を局所再読したとは記録しない（`oracle_geometry_manifest_body_read_locally=false`）。新票はparent受領後・current intake前に読み、acceptanceの両anchor、pre-P controls内の全file pin、P開始票のcontrols全SHA、最終全REPORTへ接続する。公開driverの受付順との結合であり、保存されていない時計順を再計算したとはしない。

F6. 元16親、旧64/rank1450と別batch親1578、旧128候補/128行/225 DERIVED、現在の全checkpoint/ordered row/target/DERIVED/二診断/最終保全は保持する。今回のbatch上限128、max_batches1、refill=false、P5400/C10800秒、RSS7168 MiB、単一fresh invocationの登録は不変。現在のselected/processed/accepted/terminalは未観測であり、親の128や1578を今回結果へ移さない。新三群はP[30,10,6] / C[28,9,6]の **数学2＋親metadata1**、driverはmetadata16・数学0・親metadata0。旧数学成功suite再走0を保持し、本便でも新旧全群を実行していない。

current oracle観測はcommitted sequence3、第一候補処理はsequence9以上、直後durable tailはHEAD countsへ加えない。早期nullを後のHEADで埋めず、歴史HEAD本文が未保存なら識別子と実checkpointの照合に限定する。local CRC再計算false、内側seal識別子と全file SHAの分離、candidate/cross_checked/verified/mathematical_replay全falseを維持する。実失敗run34040070261/1は1066の別scopeであり、新完成candidate mainへ適用しない。

F7. 全比較票は同じtask1069ディレクトリに保存した。

| 比較票 | bytes | SHA256 |
| --- | ---: | --- |
| whole-raw-block-delta-v2.json | 71956 | `17c5457866aa3f93222906b59a03d38acfd2b256710cf65f1e4dd63a4302f0a2` |
| whole-raw-block-delta-v2.txt | 185398 | `217baaac932ee9006363c2d39d806d58296cbe169470ee32143f17a9eeac031c` |
| final-approval-literal-delta-v1.json | 1469 | `8bf8087eebf15b7a1aebb567893c899e93db10ecfe95be9e086a221acceb824a` |
| public-metadata-and-opaque-ranges-static-v1.json | 446866 | `575ca0e860b4bdc82c9d7356e87bc71d46e6bb3c3caac67b6d5c4046afc2e79e` |
| public-static-input-pins-v2.json | 10406 | `c727d100a8901aa055e2fc199305944834114ccced8a0bdc88db211e6a7f9e41` |

raw区画はcolumn-zero functionと明示main/tailの文字列境界で区切り、ASTを使っていない。基点61区画→新63、同一54、変更7、追加2、削除0。変更はprefix、ReadV4PublicAuditRegistry、AuditV4CurrentTransitions、AuditProducerBodyReference、ReceiveWorkflowEnvelope、main、tail。追加はReceiveFixedReferenceReceipt、ReadProducerCurrentReference。全変更の旧新全文と全区画offset/bytes/SHAを保存し、順方向で新版、完全逆置換で旧247138 bytesへ一致した。54保持区画は関数本文であり、Same/PlainInt/FilePin、旧固定参照reader、全ZIP/fixture/保全、旧親・現在checkpoint・観測・診断を含む。

最後のdraft3 259791 B/270d169f…からは、L25の条件付き承認コメントとL28のExpectedApproval=2196だけを変更した。根拠は `ops/express/20260907_fable_astra_2196_envelope_v3_conditional_approval.md` 2809 B / `e7193b44aa883b1b2d486e9a0e71f9f7304852efed001d2d461457c3f9683fbd` 全文である。Launch/Artifactnullとguardfalseは不変。全18静的入力pinを再照合した。

F8. CLIの必要引数は従来の `-ArtifactRoot -AcquisitionReceipt -Old64Root -BatchParentRoot -BatchParentArchive -ReceiptPath`。追加公開入力2本をhelperと同じディレクトリに置く。実run/artifact未形成のため再現実行commandや未来pinは作らず、この保存版を実行しない。後着実handoffはrootが別snapshotへ登録し、全差分読了後にrootだけがmetadata受領を行う。

rootはdraft2/draft3の全追加差分とplain17字段等を読了し、当該保存境界に必須所見なしと通知した。Task1070の独立別読は別票であり、本作者票はその未形成最終判定を補完しない。自身の全追加本文・公開serializer・全raw差分の静的点検を完了した。変更は指定TEMPと本返信だけ。新helper/source/数学/Python/import/AST/compile/GAP/Git/GHA/network/credentials/new agentは実行していない。局所で実施したのは指定metadataの読取、opaque bytes/range SHA、文字列の完全比較と保存である。

AUDIT_1069_VERDICT: STATIC_ENVELOPE_V3_RECEIVER_GUARD_CLOSED

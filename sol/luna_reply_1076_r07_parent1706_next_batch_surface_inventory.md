# Task1076 — parent1706 からの fresh v5 batch の実装面棚卸し

F1. 次の最小案は、旧16親を同じrole/tupleのまま保持し、実v4候補を17番目の別role `batch-parent-v4` として加える二段parent adapterである。原64の1450行を復元し、v3の128行で1578へ、v4の128行で1706へ進む。v4を現 `batch-parent` へ差し替えるだけでは、v3行、旧schema、旧225祖先、保存source namespaceの結合が壊れる。新role名・下記v5字段案は後続共通契約への提案であり、root採用・正式親受理・新実行承認ではない。

本便はTask1076全文、自己P3/P4の該当本文、公開interface v1/v2/v3、実artifactの限定metadataを静読した棚卸しである。source/WF/既存票/artifactは変更せず、新source・実装案コードを作成していない。C私的本文・私的票、Python/import/AST/compile/GAP/数学/全受領器、Git/GHA/network/credentials、新agentは使用していない。新lambda1706の全oracle、候補数、採用率、実時間は未観測のまま。現在の正式状態1578/8283と、GHA成功候補1706/8411を区別する。

F2. 下表が中心となる実装面マップ。P4は `search/d972_r07_fixed_lambda_cycle_batch_v4.py`、290457 B / SHA256 `a58f7c116558fdc430025a9e095d29d0b04e0f20c9295264fca58a4c13510d0a`。行番号はこの凍結本文のもの。比較した自己P3は209926 B / `a286dca4a2d94273d2496e16317579be06173e0e4802471b2840dc4263e5a3e8`。

| 面 | 現P4の位置と固定前提 | v5の最小の追加・変更契約 |
| --- | --- | --- |
| 親宇宙/登録 | L29/42/67、L68–235、L923、L1164/1201/1840、L4450。新schemaはv4、旧親schemaはv3、16role、旧v3 tuple/全entry/全inventory固定 | v5自身のschema/P/C/WF登録を別に作る。旧15＋`batch-parent`=v3を保持し、末尾だけ`batch-parent-v4`を追加。v4 tuple/全entry/復元後全inventoryを新定数へ固定。旧 `BATCH_SCHEMA` 等をv4へ書換えて旧入口を壊さない |
| 原64復元 | `authenticate_anchor_metadata`:1220、`accepted_oracle_top_metadata`:1885、`parent_row_sources`:1910、`thin_anchor`:1944。rank1450/gen8155、64段、97祖先 | この4本文と旧anchor/roots/anchor_objectsを保持。既存l.attach_stepは旧64だけ。v3/v4 batch instructionを旧stepへ改名・投入しない |
| v3親型/投影 | `batch_anchor_header`:1298、`batch_old_input_projection`:1327、`old_batch_document`:1346、`authenticate_batch_parent`:1682。33key batch_anchor、v3の6key acceptance、最初15親投影 | 旧v3入口を残す。別v4入口は実v4の7key acceptance/parent-layoutに対し、v5最初16親、元anchor、元batch_anchor、runtimeを全量比較する。旧新P/C provenanceを別々に固定 |
| fixed参照 | `batch_fixed_reference_manifest`:1390、`batch_saved_manifest`:1358、呼出1780 | v4のfixedもmanifest1件のみ。新role用の専用参照readerを設け、原64の3159 B manifestと16本体へ直接束縛する。JSON5の5→3key射影/binary11の5keyを維持。一般同居payload gateへ渡さない |
| 保存128行/phase/target | `batch_saved_rows`:1496、`batch_plain_target_binding`:1336、`batch_saved_checkpoints`:1622。位置1450/8155、ordered ancestry長1450+i、97+128=225 | 別v4 readerで位置1578/8283、ordered ancestry1578+i、最終1706/8411を扱う。v4 start225＋今回128=353。plain target全file SHAとpacked remainder SHAを分離。全候補/行/六phase/772 checkpoints/1 invocationを親receiptへ結ぶ |
| 旧basisへの付加 | `promote_batch_anchor`:2013。1450→1578、v3 saved batch-rowを新parent-row(role=batch-parent)へ束縛 | 旧promotionを保持して1578を得た後、別v4 promotionで128行を追加。v4 saved source列を1578行と順に照合し、新runtime用はrole=batch-parent-v4へ変換。最終1706の全records/rows/leads/source列を一致させる |
| 新selection前の測定 | L2053、`make_reduction_state`:601、`run_selection`:3542 | 新lambda1706で全1706行と二対象の直接pairingを新P自身が計算する。fresh私的countは0。P1全8059/四character/全54433chord+2auxの新lambda算術を省略しない |
| owner/start/祖先/最終 | `outer_metadata`:2077、`current_derived_rho2`:3026、`final_manifest_value`:3133、`result_value`:3477 | old64字段は64のまま。v3/v4各128と累計256を区別、start祖先353を丸ごと保持し新採用だけ伸ばす。現225/128固定は新serializerへ明示移行。ownerはportableな全17親/両batch header/新実source/runtime/policyを含める |
| 観測/診断/復帰 | `batch_observation`:3406、`load_private_prefix`:3278、`admit_diagnostics`:3619、`run_actual`:3698 | 比較対象を旧lambda1578の実36104/74/131と、新lambda1706未観測へ分ける。実HEAD sequence3/9の境界、intake前null、durable tail、既完readonlyを維持。新intake票をroot roster/入力前後/復帰へ漏れなく接続 |
| 全登録/CLI/自己試験 | L1177/1184/1201、L2760–2825、L4309/4363、L4450 | 17roleのCLI/host_paths/input inventory/保全、P5/C5実pin、公開registryの新区間を別登録。旧2数学群＋親metadata群の来歴と新差分対照を分ける。単なる旧name件数の付替えで実PASSを作らない |

F3. 行列と祖先の順序は次の三層で固定できる。`state`→`delta`→`seed34`→`packet`全steps→`refinement`全steps→`e`→`continuation`64 snapshotsという元1450行はP4 L1929–1940の実順を維持する。最初の元fileは `state/physical.bin`、delta/seed34/eは各 `output/physical-normalized.bin`、packet/refinementは `output/steps/<1-based>/physical-normalized.bin`、continuationは `output/snapshots/000000..000063/e/physical/physical-normalized.bin`。原64 HEAD/owner/source/start/C全prefixからこのbasisを再構成する既存入口を使う。

| 層 | global row id | 実physical所在 | 次runtimeのsource |
| --- | --- | --- | --- |
| 原64まで | 0..1449 | 旧15親の上記位置付きfile | 既存parent-row全列をそのまま保持 |
| v3採用128 | 1450..1577 | `batch-parent:output/rows/000000..000127/physical-normalized.bin` | role=batch-parent、offset0/length12096、実file/row SHA |
| v4採用128 | 1578..1705 | `batch-parent-v4:output/rows/000000..000127/physical-normalized.bin` | role=batch-parent-v4、offset0/length12096、実file/row SHA |

各層の保存語側source列と次runtimeのsource列は別に保つ。実v4の最初のreductionは1578項で、row1450/1577はrole=batch-parentのparent-rowを参照する。最後のreductionは1705項で、row1578は `kind=batch-row, local_row_offset=0, file=rows/000000/physical-normalized.bin`、row1704はlocal126である。したがってv4自身のsaved batch-rowを親roleへ変更した列を、そのv4の保存source列と直接比較してはならない。原v3の履歴照合は原v3のnamespace、原v4は原v4のnamespaceで閉じ、受理後だけそれぞれの新parent-rowへ束縛する。両世代のlocal0/127を同じ語・同じfileとしない。

実v4最初のrowはglobal1578/offer8283/rank1579/gen8284/lead1690/sigma2/target_scalar0、最後はglobal1705/offer8410/rank1706/gen8411/lead1818/sigma2/target_scalar2である。原rowはbase3 packed4-tritの12096 Bであり、2-bit形式へ読み替えない。各 `rows/<i>/` のmanifest/instruction/target/physicalの4file、候補manifest、六phase manifestを別々に束縛する。instruction.target_sha256はplain3key target.jsonの全SHAで、targetのremainder_sha256がpacked targetを指す。theta0の最初の行も採用row/祖先/語の係数列に残す。

DERIVEDは実v3 finalの225項と実v4 startの225項が全辞書・順序まで同一。実v4 final353項の先頭225も同じで、残128は各実row manifest/instruction/plain target/rolling stateから作られた10key recordへ一致した。これはmetadata照合であり数値再演ではない。新v5 startは353項を全保持し、最終353＋新採用数とする。`original_rho2_directly_read=false` と元hash `b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e` を保持する。累計256行を「今回256候補」や「256回の新採用」へ読み替えない。

F4. 新二対象の意味は厳密に区別する。実v4 start.targetは `7868b7806a0dc41c2bda8a1c4c6a10d1cfa2c2e6968aadf561e93820f12053e1`（rank1578）。同start.previous_targetは `3bba0da3f619eab5f78e715beabd22d9c7975b36f72d28ee8d7528d9d0f4648a`（旧1450）であり、次のprevious_targetへ選ばない。次current targetは実v4 `output/final/target-remainder.bin`、`954e1ba1a50e138a0577c27c285c21ed052f3491176d883f370e8a94d11b456a`。新selection lambdaは実v4 finalの `d036e848c46b563a5b0f683fb94afcbc759dc4bc402c6db14c82b172ccc0a653`。

保存separatorの公開値はrows1706/pivots0/parent1/current1、row_pairings_sha256=`84a8935d91036a00e62362f5601416d094f4708da6986096f9353659cfa146eb`、anchor_pairing_rows1578/final_pairing_rows1706。ただし次Pはこれらの自己申告だけで入場を数学再演済みにせず、組み上げた全1706行と同じ二対象へ実直接pairingを測り直す。旧raw保持のthin_anchor/promote_batch_anchorをそのまま呼ぶ場合、既存のλ1450/λ1578の直接pairing呼出しも保持される。この測定を隠して「旧数値呼出し0」とは書かず、旧section/cochain/tree/E solveの再走0と区別する。

今回のselection36104/74/131はlambda1578上の値。次観測票のold側はその実selection SHAとv3 final由来lambda/stateを結ぶ。current側はv4 final state=`13c631c6dee46d4026e996f53370bcc202737f1082582b02271884593f902101`、lambda1706、selection/count/first値は初めnull。初回独立の条件付き観測は既契約を維持し、候補無しはNOT_APPLICABLE、未完はNOT_OBSERVED。最初の非零raw pairingと親span零の条件を測定してから実outcomeを比較する。次128採用や失敗集合の単調減少は要件にしない。

F5. 最小public wire案は、元7key acceptanceの `anchor`（旧64）と `batch_anchor`（v3親）を改名せず保持し、別 `next_batch_anchor`（v4親）を追加した8keyとする案である。正確なkeyset/name採用は後続共通taskで確定する。新v4 headerは既存named17 fileに `output/parent-intake.json` のdescriptorも必要で、v4 accepted parentの文脈を明示する。この実parent-intakeは1450→1578/祖先97→225の入場票であり、final1706/353そのものではない。

旧v3入口へ渡すviewは、元anchor_objects、最初15親、`batch-parent`の元v3root/全inventory/33key headerを保持する。新v4入口はその旧16親を完全投影し、v4 parent-layoutに保存された元anchorと元batch_anchor、v4 start1578/225、v4 final1706/353、実P4/C4/source/runtime/launchを結ぶ。新親を読ませるための一時的global書換えや `paths['batch-parent']` のalias差替えは不要であり、採用しない。

新start/selection-start/parent-intake/final/HEAD/resultでは、upstream64、v3層128、v4層128、累計親batch行256、新packetのprocessed/dependent/accepted=0を分離する。各親headerの「そのbatch採用128」を保持し、新startの総親行数を曖昧な128のままにしない。各層のaccepted schema/head/result/checker/header hashと、合成intakeのhashをowner/startへ結ぶ。ownerのportable identityにローカルroot、run受付nonceを混ぜず、host_pathsは別invocationに実17rootを保持する。fixed/bodyは旧64の同3159 B参照を使い、新v4 fixed2903 Bをpayload入りmanifestへ誤分類しない。

F6. 数学rawを保持できる範囲を自己source間で確認した。P3→P4の `classify_batch`(356→527)、`current_batch_tree`(414→585)、`make_reduction_state`(430→601)、`reduce_candidate_numeric`(445→616)、`advance_reduction_numeric`(504→675)、`final_separator_numeric`(538→709)、旧4loader、`legacy_e_input`(2165→2953)、`run_candidate_phases`(2178→2966)、`run_selection`(2675→3542)の13個のdef-to-next-def raw区間は全同一である。`run_candidates`もDIAGNOSTIC_KEYS直前までの本文2487 Bは同一だが、def-to-next-def区間は後続のdiagnostic字段追加を含むためraw不一致として票に残した。これを14区間全同一とはしていない。

これらはrank/row列を引数stateから扱い、全section/全chord/選択済みE/reduction/final solveの数学を保持する実装候補境界である。source prefix/schema/親登録、親loaderの別層、投影・owner/start・353祖先serializer・観測・CLI/rosterは変更境界として新registryへ列挙する。自己Pのraw比較をC独立性や新parentでの実算術成功の代わりにしない。

F7. 次委嘱用の実材料は `%TEMP%/shadow-atelier-audit163/task1076/parent1706-surface-materials-v1.json`、1453323 B / `0b7eeabcb06049bfe594a6b266f0eaf45477caf57e5a6696ae3b32031a729793`。実37主file pin、全128×(row4＋候補manifest1＋phase6)のfile pin、各rowの位置/target metadata、225→353接続、source namespaceの実両端を保存した。全受領器を代行せず、全11648entryの再hashやroot全metadata完了とはしていない。主な実fileは候補root相対で次のとおり。

| file | bytes | SHA256 |
| --- | ---: | --- |
| output/HEAD | 1180 | `8c91df563b636a5743f6a946fad433671237b98a0d869e23a15fb6b27c9ac28f` |
| output/result.json | 208861 | `44380663afa4f774e75b2161b94b6b8de3669183de366627ccc8722e1e301e8a` |
| checker-result.json | 15839 | `3651b6b2e8a028b96d32551c4cbd629aef9617db8bce5296396aee55323e1494` |
| output/start.json | 119074 | `9ee29d5af385f5cb4b884a441237d27d302e17a1d0c15099bc62ea4001008e25` |
| output/parent-intake.json | 3390 | `cbffcd042cf8a7a361dad97aaf8f517caac08e168789ef3b082401f715b2902f` |
| output/fixed/manifest.json | 2903 | `1a1f4644685459af2412d698a0ac814b6c3a2b9beac6e95ce612b8f08d414b8c` |
| output/selection/selection.json | 30909 | `181c87b906b2908e8d9d00e29faabf66bff673340e338bf18775e95150c3b4ab` |
| output/final/manifest.json | 1848 | `8a5fc39c8b0a07e61a33f89869edb8f64c04d5fc803f1c71f06c2dbb63ac21b2` |
| output/final/separator.json | 194443 | `62ccc588536098b01b0990f5ef3d0525a5954157b52a4d3b78f08f44e4bca3fe` |
| output/final/target-remainder.bin | 12096 | `954e1ba1a50e138a0577c27c285c21ed052f3491176d883f370e8a94d11b456a` |
| output/final/lambda.bin | 12096 | `d036e848c46b563a5b0f683fb94afcbc759dc4bc402c6db14c82b172ccc0a653` |
| run-receipt.json | 201643 | `49c65107507c89065173ad75a18fbddbc033c93ce68e8036cd306713fe36555c` |
| source-receipt.json | 8388 | `0766628e657cc5a21bdaf264b060c7328506049c7f5b035d32665603dbe50f8f` |

同TEMPの `fresh-v5-static-surface-map-v1.json` は459895 B / `5425814c14231df841b40f26f1511dcd21eb420447509aa483b621d9b82d4ce5`。元16 tuple全字段、元anchor/batch_anchor、自己source区間、公開interface全pins、仮設v5名/値を保存した設計票であり、実行可能source/acceptanceではない。親候補rootは `%TEMP%/shadow-atelier-fixed-lambda-batch-v4-run34120585268-candidate-a1`。根本tupleはrun34120585268/1、head92720e5371164545259c3007cb11e951fa5e1686、candidate10020349387、ZIP377383320 B / `84040119b08d4ee1e9a3b4524618164172f382f9a97314084131bb9fd0a3cac5`。全ZIP取得済みという事実はroot handoffによる。本便ではZIP再hashしていない。

F8. 次のP/C/WF/受領器への波及は限定して準備できる。Pは上表の新adapter/serializerを自己系統で実装し、Cは別作者が同じ17親/二層basis/353祖先/新1706直接pairing/全新phaseの公開契約から独立に実装する必要がある。C4のopaque pin261170/a29380ec00876225cc618c7025d671a3da79aea3b31b829dedba13c59ba84633をv5対応済みとして流用しない。新source全pinと現P4/C4の歴史raw、旧P3/C3等の登録、共有TCB範囲/未測定call coverage、変更区間の分類を次registryへ明示する。

WF側は旧16 live tuple/全ZIP/全directoryを保持し、17番目のv4親を同じ全量入場へ足す。原v3親の復元と新v4親の宣言空dir復元は別票にする。active v5小WF、別配置driver、歴史WF raw、実新P/C pin、source/runtime closure、二票/全保全/失敗gateを具体的なbytesへ結ぶ。全受領器も17親・二層header・v4全128行/772checkpoint/1invocation・353祖先・固定参照・新観測へ対応する別versionが必要で、現v4全受領器を新schema対応済みとはしない。

新小対照の候補は、旧16投影からv3を落とす、v4 local0をv3 local0へ誤結合する、225を353の全祖先と扱う、theta0祖先を削る、previous_targetをstart.previousへ取り違える、plain target SHAをpacked SHAへ替える、fixed参照を同居payloadと誤読する境界である。正対照後に一箇所変異し、通常helperの目的labelへ届くものをrootが次の公開群/件数として登録する。旧selftestを本便で再走した扱いにはせず、新版へ一律全再走/黙示継承も決めない。

F9. 実装前に未受領なのは、root全metadataの正式終結と復元後whole file/dir inventory pins、工房CV-9による1706親の正式受理、root管理のv5 exact public wire、独立作者の新C案、最終P/C/current-registry/小WFの具体全pinsと別読、親/新配置/発射の明示事前承認である。取得済みartifact tupleと本票の主entry pinは準備に使えるが、この未受領を埋めない。2199で回数制限が撤廃されていても、数学宇宙・親・具体WFの承認を省略する意味にはしない。

準備範囲はfresh lambda1706、元8059 P1・四characters・全54433 chords＋2aux、最大128/no-refill/max_batches1、P5400/C10800、outer6000/11400、RSS7168MiB、job330分のまま。v4結果からのresumeやbatch256、複数batch、caps拡大、次の速度/採用率/失敗数の予測は含めない。本票は次の実装委嘱へ渡せるsource位置・実metadata材料・未決条件の棚卸しとして閉じる。

AUDIT_1076_VERDICT: STATIC_SURFACE_INVENTORY_COMPLETE; IMPLEMENTATION_NOT_STARTED; PARENT1706_FORMAL_ADMISSION_AND_V5_APPROVAL_PENDING

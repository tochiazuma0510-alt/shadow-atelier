# Task1106 — 次 λ1834 batch の公開契約・承認用変更案

F1. Task1106/司令塔2222全文、root手渡し/初読票、実v5公開metadataと自系C5の必要箇所を読んだ。run34161493396/1、head `a5b456a973f8a917f3af386d327061a02a0cf900` はP/C PASS、選択/処理/採用各128、依存0、1834/8539、Separator。Cはpartial=false/durable_tail=null、128比較。しかし正式1834のCV-9採択と親変更承認はpending、正式親は1706/8411。本便は設計準備であり、1103/1105の全受領・776費用入力を再監査していない。

F2. 基準は直線的18親案。既順序 `state, delta, seed34, packet, refinement, oracle, e, prepare, block-0, block-1, block-2, block-3, p1, task712, continuation, batch-parent, batch-parent-v4` を維持し、末尾に `batch-parent-v5` を追加する。old64はcontinuation、batch-parentはv3のまま。新acceptanceのexact9 keyを `{schema,parents,anchor,batch_anchor,next_batch_anchor,batch_anchor_v5,code,runtime,registration}` と提案する。新key名は本案での提案であり確定ABIではない。旧anchor/v3/v4 headerは原値のまま、v5の8-key受付を新先頭17親へ、v4の7-keyを先頭16へ、v3の6-keyを先頭15へ、それぞれnative schemaのまま射影認証する。旧v3/v4を置換・削除する縮約の同値性は主張しない。

| native層・新readerのrole | global physical row | 層内位置・target履歴 |
|---|---|---|
| old64 / 既15親 | 0–1449 | 元位置を保持、97 records |
| v3 / batch-parent | 1450–1577 | local0–127、97＋128＝225 |
| v4 / batch-parent-v4 | 1578–1705 | local0–127、225＋128＝353 |
| v5 / batch-parent-v5 | 1706–1833 | local0–127、353＋128＝481 |
| 次packet | 1834＋j、0≤j<a | accepted local j、481＋a |

各batch親rowは `output/rows/<local:06d>/physical-normalized.bin`、offset0/length12096のparent-rowでroleを区別する。新batch-rowのaccepted localとcandidate ordinalも分ける。旧batch-rowをnative文脈で認証後、未来のphysical参照だけparent-rowへ移し、DERIVEDの旧辞書・順序・role/localは97/225/353/481境界と元全pinに束縛して保持する。scalar0の十key target record・零係数・signed literalも落とさない。全親追加行=128×3=384、祖先=97＋128×3=481。次の採用数0≤a≤processed≤selected≤128についてrank=1834＋a、gen=8539＋a、祖先=481＋a。a=128は予告しない。

F3. 新headerは旧next_batch_anchorの36-key形を基準に、実v5のHEAD/result/C/start/selection-start/final/intakeと全checkpoint/invocationへ結ぶ。新accepted_parent_batch_rows=128は直近v5、previous_parent_batch_rows=256はv3＋v4、total_parent_batch_rows=384とし、各anchor_*にも反映。旧v5 HEADのanchor_previous=128を直写しない。anchor_completed_steps=64は旧continuationの値で、ThinAnchor用投影をcompleted_stepsのない実batch HEADと区別する。

新previous targetはv5 `start.target_remainder_sha256`（954e1ba1…）、current target/stateはv5 final/HEAD（99c3f3ef… / 30a0c1c1…）。start.previousの旧値を使わない。fresh λはv5 finalの `b224f95de675b1966a12eeeb1700066b03d009f3fd0e69f9e148a6d04781dff7`。36,002/71/127はλ1706の旧oracleで、λ1834の値ではない。C5修理L1995の `records["selection_start"]["selection_lambda_sha256"]` を保持し、selection.jsonにないλ字段を要求しない。次final λ/oracleは未計算。省略したfull hashは末尾証拠に固定した。

F4. 承認用の具体差分を次の単位に分ける。数学宇宙/式/順序の変更は必要としていない。

| 単位 | 次版で必要な変更・保持 |
|---|---|
| 受付・来歴 | schema namespace v6とP/C/driver/WF新version/full pins。parent-layoutの新headerをowner/source/portable受付・18 host roots・全seal/EOFへ結ぶ。実親id10034053256、ZIP384961441 B / 72e19a87…を使用。空dir込み正式inventory五key `{files,file_bytes,directories,files_sha256,directories_sha256}` はhandback待ち、implicit dir数で代用しない。 |
| start/intake | 既accepted_batch_*はv3、accepted_next_batch_*はv4に保持し、新accepted_batch_v5_{anchor,head,result,checker,parent_intake}_sha256を追加する案。accepted_parent_target_derivations=481、previous_parent_target_derivations=353。parent_layersを3件へ、既intermediate_*は1578に保持しsecond_intermediate_*で1706を追加する案。全親candidate/row各384、六相2304、checkpoint2316=3×(1＋3＋6×128)、invocation3。最終相時計をcheckpointへ重複加算しない。 |
| reader・final | C旧4loader/保持20本文のrawとnative pairing1450/1578/1706を保持。独立v5親adapterと1834全行/両targetのdirect pairingを追加し、その仕事を明記。旧solve再演とは区別。新selection3相/各candidate6相/ordered reduction/row/target/481＋a祖先/全final/HEADを比較。plain target.json全SHAとpacked remainder SHAを分ける。 |
| fixed・保存 | 各batch fixedはreference manifestだけ、実16payloadはoriginal64に保持。三role reference票/after pinmapへ拡張し、全旧source/history/raw保持証拠、18親files/dirs、before/after、readonly完成再受付の元result bytesを維持。 |
| fixture・cost | before-producer/before-checker/after-checker三scanとC前writerを保持。既群/全fixture/empty dir/ZIP保全に三層projection・local0・481/scalar0・λ/前targetの正対照→目的拒否を別登録する。全cost型/partial/invalid/入力pinを維持し親contextを18へ。完了時cost入力=4＋3＋6p＋1（p=128なら776）、未来のpを補完しない。 |

P9/C10/raw3と実runtime（Python3.13.15、NumPy2.5.1）の登録を保持する。full8059 P1・四character・54433 chord＋2aux、CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX、max_batches1/no-refill、P5400/C10800秒、外側6000/11400秒、RSS7168 MiB、selftest300/外側360秒、job330分を変更しない。親入場の仕事は増えるが、性能倍率や残差原因を断定せず、資源増額を前件にしない。

F5. 条件付き前進命題は二段に分ける。まず正式に受理されたseparator λが全既存1834行を殺し、current targetを1へ写し、481件の保持identityが閉じていることを前件とする。さらにfresh全選択が完了して最初の違反が存在し、そのwitnessと通常raw/P1/B構成が同じ非零pairingを与え、新packetの処理済み0・採用行0であることを前件とする。このとき旧spanによる消去でλ値は変わらず、残行は非零なので最初の行は独立となる。二件目以降は追加済み行をλが殺すとは限らず、全128独立・失敗集合の単調減少は従わない。観測はcommit済みselection sequence≥3、第一decision≥9からだけ形成し、durable tailやintake前診断を完成観測にしない。

| 分岐 | 必要な公開終端条件 |
|---|---|
| zero-roster | full chordとaux2の完了・違反0、selection/最終pairing/HEAD比較後のみCOMPLETE_ZERO_CANDIDATE。未計算oracle/nullやtarget零とは別。 |
| 非空・依存を含む完了 | processed=selected、dependent行はrank/祖先を増やさず、採用a行だけ追加。target非零なら全final成立後BATCH_COMPLETE_CANDIDATE。 |
| positive | 実reductionでtarget零、完成prefixとfinal比較、残りselectedはSKIPPED_AFTER_LINEAR。LINEAR_MEMBERSHIP_CANDIDATE、λ=null、positive_readoutはNEW_BATCH_SAME_WORD_ADAPTER_PENDINGを保持し、MEMBERへ昇格しない。 |
| resource/partial/不正 | UNKNOWN_RESOURCEは資源停止、partialは保存commit prefixの比較範囲、durable_tailは別欄。不正metadataのFAIL/REJECTEDと区別し、未完prefixをphysical HEADへflushせず、完成candidate/未知未来値を作らない。 |

F6. 2199 notify-and-goの凍結envelope内契約修理と、本案の親追加・9-key型・新数学入場adapterは別の承認対象である。1834の正式採択/CV-9と具体的親変更承認の後、Pは自身の既系から三層adapter/serializerを、Cは自身の既系から独立adapter/全比較とraw保持票を、driver作者は公開ABI/pinだけから18親入場・軽量envelope・registry/fixture/cost保全を、それぞれ別委嘱で作る。私的P/C helper・本文は共有しない。公開nested型/拒否名を先に固定し、実完成source/driver/WF/registryの全pin・独立別読・司令塔の要求する通知を揃える。新pin未形成の本設計票は配置承認を成立させない。

根拠の全14 pinとfull値は `task1106/public-input-and-proposed-boundaries-v1.json`、12981 B / `f50a250f944963050eb3b570410123a0f2bc4a01b7561ba2098c375a28ea8504`。root手渡し4939/0fa69175…、初読票15900/22adb9fb…、実C結果15908/b929a1ac…、実P結果208932/16e5ec07…を全file照合した。源コード/driver/WF/registry作成・変更・配置0、source/数学/AST/import/compile/自己試験0、Git/GHA/network/credential/process操作0、実root変更0。新P私的本文を読まず、既存1105実行に触れていない。

AUDIT_1106_VERDICT: PUBLIC_CONTRACT_PLAN_READY_PARENT1834_ADOPTION_AND_SPECIFIC_APPROVAL_PENDING

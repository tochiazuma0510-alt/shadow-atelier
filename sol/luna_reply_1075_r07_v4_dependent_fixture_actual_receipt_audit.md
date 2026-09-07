# Task1075 — 実 DEPENDENT fixture 保存物の限定独立監査

F0. **LIMITED_ACTUAL_FIXTURE_PASS**。実 run34120585268/1 の P/C 各三候補について、INDEPENDENT→DEPENDENT→INDEPENDENT の保存列、中央候補の非挿入・rank/generation/target 不変、次の独立行への続行を、実 selftest・execution・全対象 file と保存 inventory へ結んだ。163 F-k64-1 は、既受理の静的呼出し契約と今回の合成 fixture 実受領を合わせた範囲で閉鎖可能と判断する。これは保存 metadata の独立監査であり、自作 WF の再独立監査、数学の別実装による再演、全 envelope の受領判定ではない。残る必須修理 finding は0。

F1. 事前契約の読了と実受領を分ける。以下は全文読了した公開文書の実 bytes/SHA。163 は F-k64-1 関係節・指定行のみ、1072 は fixture/outer metadata gate の該当範囲のみで、両巨大本文の全読了とはしない。全 read scope は public-receipt-map-v1.json に保存した。同票の未受領札は事前段階の記録として残し、本票F2以降が実受領後の判定である。

| 公開文書 | bytes | SHA256 |
| --- | ---: | --- |
| task1075 | 3315 | 73e3c8f906d47d9ef73bd747b3cedc3a0b7146bd5a01af51cbb90a970780e30c |
| reply1051 | 15586 | 455e8dfcd2cac35fd428160eb98b8baee1799bf5879370912e39fef4e58347de |
| reply1052 | 9069 | 59a5242162878218863239f8f0208a81801934f67292145dce44c0c7baf6c164 |
| reply1053 | 14785 | f9a78de1b9c9ebe9644e6b3ab4b76e130197601be650dec25841a1328ceaa80a |
| reply1054 | 17091 | 5224495cfbe431337c5bef116479b4f1f5960b6635a1f31e6637e9ff9ae9f9dd |

F2. root の抽出完了 handoff 後だけ、TEMP/shadow-atelier-fixed-lambda-batch-v4-run34120585268-candidate-a1 を読んだ。取得票720 B/c377a2ed0d38d45d53236a8d1952f95d5a20433863fc3d764efda04b4b0caf7c、全entry票2141758 B/c2ec141eecbc435972d750ae7beb31382c6108ad93ccb698181b311d77390fb3を直接読み・全file hash一致。候補10020349387、head92720e5371164545259c3007cb11e951fa5e1686、ZIP377383320 B/84040119b08d4ee1e9a3b4524618164172f382f9a97314084131bb9fd0a3cac5。全11648 file・3487 directory・1308094050展開bytes、全ZIP/全entry EOF/SHAと抽出読み戻しはrootの実受領である。本担当はその全1.3GBを再受領したとはせず、以下の対象116 fileを全内容hashで独立再読し、root全entry票および内部fixture ZIPの対象全stream EOF/SHAへ照合した。外側ZIPのexplicit directory entryは0、rootの独立CRC再計算もfalseである。

F3. 実外側票は P/C selftest の各 start/result 全字段、source/runtime/launch、stdout/stderrとexit file、gate、fixture baselineへ結ぶ。startのschema/内seal以外の全字段を実resultへ型付き一致、result全文をrun-receiptの該当execution埋込値へ一致させた。argvは各自の明示fresh fixture rootと --selftest を含み、--acceptance/--candidate-root は無い。300秒/外360秒/7168MiB、exit0、outer_terminated=false、reason=null、exit fileは厳密な 0+LF。時刻は各実票のUTCである。

| 系 | 開始→終了 UTC | 実経過秒 | 新拒否数 | selftest stdout bytes/SHA |
| --- | --- | ---: | --- | --- |
| P | 12:15:27.036019→12:15:30.546040 | 3.510051369999985 | [30,10,6] | 2293 / 21973c9ed98b12e3e715f5f1855fcb3836f9dc5a542c07ec63f751319576a690 |
| C | 12:15:31.288808→12:15:37.301198 | 6.012419401999978 | [28,9,6] | 2610 / cf30248c177756d857f0727ddf1d734a95b14c47e7aed8472517b1a29b97ad71 |

各順序は k128-version-registration-and-types、k128-full-roster-cutoff-and-restoration、batch-parent1578-admission-and-projection。前二群と第三の親metadata群を分離し、gateも2+1/旧成功suite0を認証。第二群末尾にP dependent-nonnull-lead、C dependent-outcome-resealedの実拒否名がある。両票のactual_anchor_arithmetic_replayed/candidate/cross_checked/verifiedは厳密bool false。旧履歴suiteの受理を今回の実PASSへ流用していない。
実P source290457 B/a58f7c116558fdc430025a9e095d29d0b04e0f20c9295264fca58a4c13510d0a、C261170 B/a29380ec00876225cc618c7025d671a3da79aea3b31b829dedba13c59ba84633は、登録済み原本とartifact checkout-sourcesをopaque hashだけで一致させた。私的本文は読まず実行しない。source-receipt8388 B/0766628e657cc5a21bdaf264b060c7328506049c7f5b035d32665603dbe50f8f、driver536145/35f73f5d1b8b519a69773690db8f8e514b3cc1d2792cc595ecdc0b92dede7a0c、WF22153/56a8349fd54b16d63da9de2c4762ed04328ef1373f65af45c46019e745a1859bへの全file pinも接続した。共有TCB・残るclosure全体の再監査をここへ追加していない。

F4. 対象は selftest-fixtures/P/selection/dependent-continuation（58 file/303145 B/15 directory）と selftest-fixtures/C/roster/dependent-continuation（58 file/289720 B/17 directory）。directory数は各subrootを含む。全65 JSONは52種類のrawで、52種類の全字段を読了し、残13同内容copyは全byte一致で結んだ。全116 fileのpinは actual-fixture-files-v1.json、全65 JSONと各top型は actual-public-fixture-documents-v1.jsonに収録した。input.jsonはP302 B/ca61ca8029bec8aa7a36ac496f00bf3f9708d216616dc8c7a451a307cad85672、C296 B/6beca57f58303dde61f276710f278dc8855073dfe96aedc45eea50fcd47f941d。非零leading_rowsとselection_scalarsを保存し、actual_parent_arithmetic=false、earlier_five_phase_bodies_evaluated=false、fixture_only=trueである。各candidate0/1のraw input同士、および最初の保存remainderは全12096 B同一である。

| 系・ordinal | 保存outcome | rank前→後 | generation前→後 | processed/dependent/accepted後 | 新row offset/global ID |
| --- | --- | --- | --- | --- | --- |
| P0 | INDEPENDENT | 1→2 | 7→8 | 1/0/1 | 0/1 |
| P1 | DEPENDENT | 2→2 | 8→8 | 2/1/1 | null/null |
| P2 | INDEPENDENT | 2→3 | 8→9 | 3/1/2 | 1/2 |
| C0 | INDEPENDENT | 0→1 | 0→1 | 1/0/1 | 0/0 |
| C1 | DEPENDENT | 1→1 | 1→1 | 2/1/1 | null/null |
| C2 | INDEPENDENT | 1→2 | 1→2 | 3/1/2 | 1/1 |

positive-caseの実pinはP966 B/82b4a7fb9237d2b3e70acca8c5b7db8e1840dda8b5847cdb38331970fa1ddb4c、C1022 B/8862cfdb6078e35c69f2d1437d5789ac0d319aa499841653e38b7a503f9c72a1。この表をcounterだけで採用せず、各positive-case→三candidate全manifest hash→reduction manifest→全payload descriptor→二row各4fileへ結んだ。candidate predecessorは0→1→2、row predecessorは0→2の独立候補だけを結び、ordinal1でrowを増やさない。全12 payload manifestのfile数/型/shape/全file SHA/EOF、telemetryのpayload byte総数も一致する。P/C各rows下は厳密8 file。

F5. 中央DEPENDENT reductionの係数列はP[0,2]/C[2]。ordered_reductionsの型付き整数と実coefficients.u8の各byte・全EOFを照合し、零係数を落としていない。lead/sigma/normalized_sha256/target_scalar/new_row_offset、candidate.row_manifest_sha256、literal.outer_exponentはnull、normalized_word_available=false。phaseにはphysical-normalized.bin/instruction.json/target.jsonが実在せず、manifestにも列挙されない。state_headとparent_state_head、rank/generation、accepted数が不変で、processed/dependentだけ各1増える保存列を確認した。
P target前後は全12096 Bとも04d7440d19b9b12e688760228d1cd45f438e0915b43910ffa76dd00bf40111d6、Cは1e91b06c7536b03ffb8dbb42f18c814ecae681e9825a2dfe953f2e009646e9ca。hashだけでなく前後全byte一致も確認した。両保存remainderはremainder_zero=trueを持ち、全12096 Bの実SHA17919b5667637402588741ded0074a904dd4b008dd7cda7bf5879200591c9d59へ結ぶ。このboolの意味と零性を実計算で強制する点は既存静的契約＋今回selftest成功に依存し、本担当は三値vectorを復号・零判定・消去していない。
次候補のremainder_pairingはP/Cとも保存値0だが、outcomeはINDEPENDENT・remainder_zero=falseとなり、次offset1の実normalized row/manifest/instruction/plain targetへ進む。plain target JSONのSHAとpacked targetのSHAを混同していない。Pの三telemetryは0.013994/0.010117/0.016016秒を保存する一方、Cは0.0秒・io null・rss0のfixture値であり、C phaseの実OS時間と称さない。外側の実elapsedはF3に別掲した。

F6. 陰性について実保存変異と実拒否を分けて照合した。Pは正しいordinal1 reductionに対しlead:null→0と内seal識別子だけ、telemetryはpayload_bytes39396→39393と内sealだけ、phase manifestはreduction bytes1807→1804/二file SHA/内sealだけのraw差分。残る5 payloadは全byte一致である。rejection.json251 B/36f21c506aa603e2cfa156a6d92520fbd447faba737decfd11fbfbd74ec31059にはexpected_gateと実observed_error `fixed_lambda_batch:dependent_preserves_target_and_has_no_normalized_row` が存在する。
Cはcandidate outcome:DEPENDENT→INDEPENDENTと内seal識別子だけのraw差分で、正しいreduction phase全8 fileは完全不変。rejection.json221 B/42963fc431b6a8efc9f11209191a80ddb266b7a1301aa0026e7367e3fd2ea2d9は `cycle_batch:candidate_expected_size_hash:candidates/000001/manifest.json`、rejected=true、resealed_input=trueを保存する。これは期待candidateのfile size/hashとの比較で停止した観測であり、その後の別のsemantic outcome比較に到達した実証とはしない。C case-ledger3809 B/57c1d41a92e4d6f30a2222a96062ed475e8f6049d2271a40ff2e3902ca1736dcにも同positive-case全辞書と拒否名が一致する。
再sealの正しい生成・実reject helperが目的labelだけを受けること・P restore/C advance前の拒否位置は1051/1052の静的契約へ依存する。本担当は保存内sealの独立再計算やnegative再実行をせず、全外部file SHA、目的変異以外のraw不変、descriptorの実size/hash、実保存labelとselftest PASSを照合した。

F7. 全対象保存への接続。P/C baselineは251614 B/bff34443c44be2871732d9e77dd55b2ab4b4945e932215b814f6230af4c48d67、644872 B/2ab26e486951530a8903abbc13d0aa6b5bc6ea63d5adce7494875e5c7af2b2f7。各baseline→実source/selftest/execution全pinとfixture rootを結び、対象58 file/15または17 directoryを実filesystemへ照合した。before-producer/before-checker/after-checkerの三票はPASS/errors[]/missing[]、各P/C rowはCOMPLETE/present=true/unchanged=true。各段階の保存inventory全辞書をbaseline.inventoryへ型付き比較し、対象fileだけの抜粋を全tree同一と誤称していない。ただし他のfixture本体全内容を本担当が再hashした範囲は含まない。
内部selftest-fixtures.zipは4388446 B/3374c41b509acdf478d2d3e0f13590b66448a319e481d13cecf41f617c6b7a53。archive票1814 B/98b6a3e2c55cb5b56d1f958be9c442d309b78166dfc5b9185badf7e6cda5bd0bはboth_completed_roots_unchanged=true/raw_fixtures_retained=true。before/readback/after全inventoryは各908905 B/5fd3f9424fbe39a48d72a32ab57490063f06622dadbab59364c51198dec67fc2で一致し、対象全116 entryの保存pinを含む。内部ZIPの当該116 file全stream EOF/SHAと明示32 directoryを独立に読み、実subtreeへ一致させた。GHA側票のall_file_bytes_SHA_EOF_and_CRC_read=trueと本担当の局所stream読取を分け、本担当の独立CRC再計算はfalseのまま。empty directoryの復元や入力への書込みは行わない。F2の3487 directoryは取得票の抽出時の数であり、現在のroot全体の数へ読み替えない。rootから、その後に別のmetadata空dir4個とselftest registration用host parent34個を認証復元中との連絡を受けたが、両DEPENDENT subtreeはその対象外である。本担当はこの38個の復元完了・最終root総数を先取りしない。
最後に全116 fixture file＋関連42 file、計158 fileを全再hashし差0、対象directory差0。外側の実run-receipt201643 B/49c65107507c89065173ad75a18fbddbc033c93ce68e8036cd306713fe36555cについては、full file pinと本課題のlaunch/source/selftest execution/fixture字段のみを対象とし、current/rank等の全算術判定を行わない。

F8. 閉鎖する範囲と依存。実物に存在するものは、各input、positive-case、三reduction/三candidate/二row、各telemetry、二陰性の変異物と狙った拒否label、および外側実行・保存票である。両subtreeに独立したcheckpoint列、restore呼出しの実行trace、陰性直前直後の完全な物理state snapshotは無い。これらを後付けしたり、別のroot/roster fixtureのcheckpointを今回のDEPENDENT実行へ転用しない。内部の全rows/pivots/parents不変assertion、Pの実restore経路、Cの拒否がadvance前であることは、既受理1051/1052の通常helper接続と今回の目的label付きselftest成功に依存する。公開rank/target/state/row履歴・実byteとその静的条件を合わせた限定の閉鎖である。
両fixtureの設計作者が同じ、先行五相はsynthetic placeholder、P fixtureをCが独立受領した対照ではない、共有TCBを保持、という四限定は解消していない。Pのowner/source/start等と先行phase hashも未受理の合成入力であり、実親の同名字段と取り違えない。F-k64-1をこの限定範囲で閉じても、実親算術の完全再演、全envelopeの受領、CV9、新rank/新oracle、grade2/全A0/Lean verifiedへの昇格は伴わない。
本担当が行ったのはPowerShellの型付きJSON・raw SHA/byte一致・file/directory集合・内部ZIP metadata読取のみ。三値復号、消去、pairing、Fox、fixture/P/C/driver/全受領器実行、Git/GHA/network/credential、新agent、入力tree変更はいずれも0。外側結合用の自分のinline metadata queryが一度directory配列連結の括弧不足で停止したが、実15/17 directoryに差は無く、明示型付き配列へ直した比較で閉鎖した。これは実fixtureの失敗とは分け、final-readonly-scope-v1.jsonへ記録した。

F9. 機械票はすべて TEMP/shadow-atelier-audit163/task1075/ に保存した。全読了/同raw複写/opaque hashだけ/部分fieldsetという読取範囲を区別したまま、全実対象pinを含む。734個のtransition/descriptor照合と1163個のouter/preservation照合はmetadata述語の件数であり、算術試験数ではない。最終材料の全pinと本返信のpinは final-materials-index-v1.json に収録する。

| 保存票 | bytes | SHA256 |
| --- | ---: | --- |
| public-receipt-map-v1.json | 12511 | 0adfffc7541c307c7bdfe354b09d045112427173160727d0d1a49321e769ee78 |
| root163-public-readonly-snapshot-v1.md | 398566 | b94ced925a16ee331248f2d063f14b65bdb3962e824333b1890103921a5bae6c |
| opaque-source-registration-v1.json | 1131 | 1c55cceee2ff07ea5b23e47a53c27dca3264268e3f6e526748cc7f44f98fdda5 |
| actual-fixture-files-v1.json | 101903 | 13345f1253b04dd93f7363c453709745ab6e319bdce67c3020a299fd84f7ef50 |
| actual-public-fixture-documents-v1.json | 314762 | 387720771148de64536563a9cf9cbd0c745d6494f71c2790eef58de2f3df3b5a |
| fixture-transition-metadata-v1.json | 109419 | 1579de532c2e9cab9156abf62607c3978f0284716dd972e1d2a490d7652e3742 |
| resealed-negative-raw-comparison-v1.json | 23719 | 469e88bf708fc01941623c72b773332b91fdc70d95bc34ad7e28e024fc9f6d4d |
| outer-fixture-binding-v1.json | 217660 | 037ad65f6386722f4336e456d3682b1459091eda7782e0f3ce89e7a5cce23bc7 |
| final-readonly-scope-v1.json | 6562 | 62fd9886f95b451f981b90b7f82b4f81970d00ffcc334fb50d189299330f435d |

AUDIT_1075_VERDICT: LIMITED_ACTUAL_DEPENDENT_FIXTURE_PASS_WITH_PUBLISHED_STATIC_CONTRACT_DEPENDENCIES

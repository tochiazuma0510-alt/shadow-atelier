# Task1077 — parent1706 / fresh lambda1706 P5 静的草案

F1. 指示書1077と最終返信1076を全文読み、指定TEMPにP5完全source草案と公開interface、全raw差分、全区間台帳、保持票、実metadata入場材料を保存した。通常経路・復帰・診断・四群自己試験の実装blockの未接続は0。最終復元inventoryだけは未着なので `NEXT_BATCH_INVENTORY_REGISTRATION = None` を維持し、通常入口は `next_batch_root_restored_inventory_registration_pending` で拒否する。これは完成したsource本文の静的提出であり、未着登録を補った本受理や実行成功ではない。

rootから裁定2206の1706/8411 cross-checked限定7条、および2207の具体pin・別読・marker通知を条件とするnotify-and-goを受領した。指示書および初期interfaceに残る「正式親1578/1706候補」はその時点の記録であり、この後着通知で状態を更新する。ただしroot全metadata受領の最終wholeinventory手渡しは未完、P5/C5/次WFの具体配置・発射はrootの担当として残す。今回の新lambda1706 oracle、採用数、速度、反復数を予言しない。

F2. 変更は指定返信と `%TEMP%/shadow-atelier-audit163/task1077/` だけ。基点repo P4は290457 B / a58f7c116558fdc430025a9e095d29d0b04e0f20c9295264fca58a4c13510d0aのまま。P5草案は `d972_r07_fixed_lambda_cycle_batch_v5.py`、366388 B / 135495b3203ba393fcceb5b22b74f5da5694849b67c0841ca4193d18ea56cba9。root別読用の `review-snapshot-v1/` に同じ全sourceを別raw固定済みで、後着inventoryの結合はこのsnapshotを上書きせず別差分にする。

PowerShell/.NETによるraw text・typed JSON・bytes/SHAの静的作成と読取だけを行った。source/Python/GAP/import/AST/compile/数学/自己試験/全受領helperの実行、Git/GHA/network/credential、repo source/WF/実artifact/旧票の変更、新agent起動、C私的sourceやfixture本文の読取は0。Cについて読んだのはrootが公開したmetadata wireだけで、Pの新helperをCの算術根拠にしていない。

F3. 公開wireは `interface-v1.md`（19814 B / 928b611d79521701438dd4ed4879ba6ca522166548f9e9a153537a8079a97a95）と補足 `interface-v2.md`（5792 B / 43d89ff32fce80606f329f5cf91bf22489f716a0590a39e711d29a6e837f8e19）。rootが両票の共有部分を採用した。新schemaは `d972.r07.fixed-lambda-cycle-batch.v5`、P/C/WF basenameはv5。元16親のrole・順序・tupleを保ち、末尾17番目へ `batch-parent-v4` と `--batch-parent-v4-root` を追加した。元 `batch-parent` はv3のまま。acceptanceはexact8key `schema,parents,anchor,batch_anchor,next_batch_anchor,code,runtime,registration`。旧64はanchor、v3はbatch_anchor、v4はnext_batch_anchorへ結ぶ。旧reader呼出し中のglobal定数やpathの入替えは導入しない。

headerは公開36key。旧 `accepted_parent_batch_rows` / `anchor_accepted_parent_batch_rows` は直近v4層の128を表し続け、新 `previous_parent_batch_rows` / `anchor_previous_parent_batch_rows` が前層v3の128、新 `total_parent_batch_rows` / `anchor_total_parent_batch_rows` が合計256を明示する。旧 `accepted_batch_*` SHAはv3の意味を維持し、別の `accepted_next_batch_*` SHAだけをv4へ結ぶ。全新top/nested keysetはpublic-keysets-v1.jsonとinterface-v1に列挙した。

F4. 通常経路は `authenticate_acceptance` の旧1450 metadata、旧 `authenticate_batch_parent` のv3 metadata、別 `authenticate_next_batch_parent` のv4 metadataから、元 `thin_anchor` → 元 `promote_batch_anchor` → 新 `promote_next_batch_anchor` の順に進む。1450基底を落とさず、v3のglobal1450..1577 / offer8155..8282、v4のglobal1578..1705 / offer8283..8410をそれぞれ128本保持する。保存当時のordered source配列と元挿入lead列を全件認証してから、当該層の行をruntimeの `parent-row` roleへ写す。両層のlocal0は別のrole/fileに属し、同じrowとして置換しない。

v3 final225とv4 start225は全辞書・全順序一致を要求する。v4 final353は先頭225と後続128のexact10key recordへ結び、scalar/theta0のrecordも消さない。新start353を全保持し、finalは353＋今回採用行だけ。元rho2 hashと `original_rho2_directly_read=false` を維持する。新previous targetは実v4 start.targetの7868b7806a0dc41c2bda8a1c4c6a10d1cfa2c2e6968aadf561e93820f12053e1であり、同start.previousにある旧1450対象ではない。

F5. 新親入場は実v4 envelopeの29登録entryを固定し、18 named file、全128 rowの各4file、各候補の全6phase、772 checkpoint、1 invocationを実保存bytesへ結ぶ。旧16portable親、旧7key acceptance、旧P4/C4と保持P9/C10/raw3の計24source、owner/source/start/layout、HEAD/result/final/checker/run、旧親parent-intakeとP4の旧4loader実raw保持票、保存観測票を同じ受領鎖へjoinする。C sourceはpinのopaque認証であり本文を読まない。旧 `batch_*` metadata readerもそのまま保ち、追加 `next_batch_*` readerでv4の1578開始・1706終端を別に読む。

fixedは専用参照readerを使う。実v4 `output/fixed/manifest.json` は2903 B / 1a1f4644685459af2412d698a0ac814b6c3a2b9beac6e95ce612b8f08d414b8c、同directoryの通常fileはmanifest一件だけである。accepted_fixed_manifestを旧64の元3159-byte manifestへ結び、実16payloadを旧64 `output/fixed/` から読む。JSON五key→三keyの既登録射影とbinary五keyを区別し、新親directoryに存在しないbasis等を要求しない。plain target.json全file SHAとpacked remainder SHAも通常helperで別々に照合する。

F6. 新Pは全1706のbase3 packed4-trit行と新lambdaを通常呼出し `m.check_final_separator` へ渡し、親spanと二対象のpairingを直接測る実装である。保存separatorの主張だけで通さない。保持raw内部の1450行pairing、元v3 promotionの1578行pairingも隠さず、parent-intakeの `native_pairing_rows_rechecked=[1450,1578,1706]` に記す。この三回の直接pairingと、旧section/cochain/tree/E solveの再走0は別の射程である。本便ではこれらの算術を走らせていない。

新parent-intakeは旧rank1450/祖先97、intermediate1578/祖先225、current1706/gen8411/祖先353を明示し、二つのparent_layersへ各128 row/128 candidate/768 phase/772 checkpoint/1 invocationを分ける。合計256 row/1536 phase/1544 checkpoint/2 invocationとなる。start・parent-layout・selection-start・final/HEAD/result/DERIVEDへ同じintake/hashと三つの行数を接続した。既存root rosterにあるparent-intake.jsonを保持し、通常metadata復元、早期診断、全input前後照合、completed-readonly復帰も新17親と同じsourceへ結ぶ。

F7. 新fresh lambda1706で元8059 P1 rows、四characters、全54433 chords＋2 aux、最大128/no-refill/max_batches1の通常算術へ進む構造は保持した。P内5400秒、C内10800秒、outer6000/11400秒、RSS7168MiB、job330分、selftest300秒/outer360秒は既登録上限であり実時間予測ではない。P CLIは元全rootと4個の順序付き `--block-root` に新 `--batch-parent-v4-root` を加え、通常 `--acceptance --output --batch-size 128 --max-seconds 5400 --max-memory-mib 7168` を要求する。自己試験は実親/acceptance/outputを伴わないfresh明示 `--selftest-root`、`--max-seconds 300` を使う。UNKNOWN_RESOURCE/exit3と完全保存境界、既完resumeの既存result byte不変・invocation追加0を保持する。

観測old側はv3最終のlambda1578/stateと、実v4 selectionの36104 / first index74 / edge131に結ぶ。current側はv4最終lambda1706/stateであり、HEAD sequence3のselection commitまで新failure値はnull、第一decisionのsequence9までfirst outcomeは未観測。intake前の親span/rho2条件もnullであり、durable tailの一相をHEADの観測に加算しない。候補0ならfirstはNOT_APPLICABLE。初回条件付き独立の紙上理由は保存条件を実観測へ結ぶものであり、2本目以後の独立、128本採用、失敗集合の単調性は主張しない。finalの `new_lambda_oracle=null` も保持する。

F8. 自己試験は旧三群の実装と来歴を保持し、Pの四群/拒否件数を次の順で固定した。いずれも本便では未実行である。

| name | 登録拒否件数 | 今回の範囲 |
| --- | ---: | --- |
| k128-version-registration-and-types | 30 | 元登録対照を維持し新exact8key入力へ接続 |
| k128-full-roster-cutoff-and-restoration | 10 | 元cutoff/保存とDEPENDENT→後続独立対照を維持 |
| batch-parent1578-admission-and-projection | 6 | 元v3親入場metadata対照を維持 |
| batch-parent1706-two-layer-admission | 7 | 新17親の二層metadataだけを追加 |

新第四群は、旧16投影のv3欠落、世代local0混同、225を全353とする誤り、theta0祖先脱落、previous target誤選択、plain/packed SHA混同、fixed同居誤読の7件。全て通常helperの正対照受理後に一箇所変異し、登録した目的labelだけを捕捉する。exact case順・relative path・label・rejection.jsonのplain4keyはinterface-v2に全列挙した。第四群は12 positive＋8 negative input＋7 rejection＋1 scopeの計28通常fileで、positiveの全inventory不変を比較し、全fixtureを保持する。第四群をfull1706受理/新Omega/E数学の算術自己試験とは呼ばない。Cの公開四群件数は[28,9,6,7]であり、その独自label/helperをPの試験で代用しない。

F9. `producer-body-inheritance-v1.json` は42507 B / dc456584d25cec4bceed4d8de0a8fc43d7da3455a9fe525e9de2e9bebbbfada4。旧P4から登録37数学/保持bodyの全raw SHA同一を確認し、元1450の4loaderもその中に保持する。13個のdef-to-next-def区間同一と、run_candidates本体2487 B同一は異なる境界として明示した。run_candidatesのより広い歴史登録範囲まで同じだと読み替えない。

全sourceはcolumn-zero def/classとmodule-prefixによる連続区間でEOFまで分割した。121区間UNCHANGED、16区間MODIFIED、19区間ADDED、REMOVED0。区間単位の分類は数学bodyの分類ではない。例えばcharacter_countsに続く登録定数を含む広い区間はMODIFIEDだが、登録したcharacter_counts数学bodyは37保持票で別に同一と確認する。全変更区間の旧/新rawを完全に収載したdiffと、旧/新全区間offset/bytes/SHAの台帳を保存し、unchanged旧raw＋変更新rawで完全なP5全SHAが復元できることを静的に照合した。

| immutable review-snapshot-v1 file | bytes | SHA256 |
| --- | ---: | --- |
| d972_r07_fixed_lambda_cycle_batch_v5.py | 366388 | 135495b3203ba393fcceb5b22b74f5da5694849b67c0841ca4193d18ea56cba9 |
| producer-v4-to-v5-all-raw.diff | 223355 | 1154da8855d8c48d2ddb7e4a6928dfdb43d7965fc585ba7079289eab85719af9 |
| all-current-and-baseline-regions-v1.json | 222199 | e33814597f71c13c563dbe4cc0a35d6cca4d76a83566a764dc3266095430475a |

F10. 実metadata登録材料は `observed-next-batch-anchor-v1.json` 268820 B / 4ad89597e3537914bbce9e97ebdf02ed74da4500b40cbe11f82849a518ad5828と、`static-admission-materials-v1.json` 1971 B / 2fbf13a85949a769b7ab0c5504367e0f8ba6dd468a16cad86a556cfb82419db0。前者は実18 named/772 checkpoint/1 invocationの全file pinsと36key header材料であり、新acceptance実行結果ではない。29entry表も別保存した。作者の全通常接続・保持・未実行・pending範囲は `static-self-review-v1.json` 4225 B / 115b9b70e6c2497a1254c4c8cd15352f34dce0afeb08952e74f43b6fa81989fbに記帳した。

全TEMP材料のfile/bytes/SHA/用途は `materials-index-v1.json` 6681 B / 84fe9ae62c5e4f1eca63fd81199b79ef233888425ebff0ed4a39c4a8aecc5b39。自身だけを列挙から外し、途中block保存textも歴史stagingとして全pinを残した。実行に使うsourceは完成全sourceであり、途中blockを代替の数値実装として扱わない。新source・全差分・全区間・公開interface・metadata材料をrootへ配達済みで、Cへ渡すのはpublic interfaceと公開pinだけである。

F11. 残件はrootの最終復元wholeinventory登録と、root全差分別読の所見への対応、その後の最終P/C/WF実pin結合・具体配置である。rootの暫定全11648file /1308094050 B /3525dir、files ffec515b…/dirs f9562484…は参考値として受領したが、未完の最終受領を代用して定数を開けていない。この本文およびsnapshotは実装静的提出、未実行、inventory guard closedを表す。新Pの実試験や全親1706受理成功、cross-checked/verifiedを本便から追加しない。後着登録が来たらsnapshot-v1不変で一箇所の定数差分と全新pinを別に提出する。

AUDIT_1077_VERDICT: STATIC_IMPLEMENTATION_DRAFT_COMPLETE; INVENTORY_REGISTRATION_PENDING; NORMAL_GATE_CLOSED; NOT_EXECUTED

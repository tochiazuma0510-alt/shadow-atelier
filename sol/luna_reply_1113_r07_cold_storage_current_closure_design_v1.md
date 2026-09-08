# Task1113 — 冷保存と現 run の入力閉包設計

F1. 結論と境界

現 run が使う行・target・lambda・固定算術資産と、過去の採用命題を支える証拠を分ける候補を、P6 の実 caller に結んだ。依存表22群、active bundle の候補型、一回変換と各 run の検査の分担、12件の反例、三つの性能仮説を保存した。これは限定設計の完了であり、変換 artifact、次版 loader、独立同値性裁定、実性能改善の完成ではない。

指示書4669 B/`e0fafbef2186dd3eeb2223ce9ae28a4f3ab023a633e21faf81c73e4bf3d131b2`を全文読了。2227/2228公開裁定と費用・証拠の射程訂正を採用する。現 v6 の18親、k128、一回、no-refill、同 caps と計器は変更0。P6 は `453749/75401d4ded04e00187e9a45bfe87603309473a7c6625e6747ecf5c3bf4caa0d7` のまま、正式 inventory の None と implementation guard false も本便では変更していない。C私的本文・fixture読取0、数学/source/import/AST/compile実行0、Git/GHA/network/credential操作0。

固定例は正式受理された run34161493396/1、head `a5b456a973f8a917f3af386d327061a02a0cf900`、artifact10034053256、rank1834/gen8539。将来 v6 の採用数・rank・artifact tuple は未観測の別パラメータであり、128採用/1962を固定しない。Task1111の独立数学監査は別件に残す。

F2. P6 の実入力面

`authenticate_acceptance` L3722–3779 は18親の全file/dir inventoryとcode/runtimeを照合した後、旧64・v3・v4・v5のnative metadataを読む。`run_actual` L5619–5639 はその後に `thin_anchor`、三つの `promote_*` を呼ぶ。したがって「親入場秒」「過去層metadata秒」「state復元とpairing秒」は異なる読取面である。現行の全入力要件を、設計票だけで省略することはない。

正本 `p6-current-closure-dependency-design-v2.json` は各群に、role、native相対path、読取・転送字段、次のconsumer、P6関数の全raw offset/bytes/SHA、行位置、複数の分類、冷保存へ替える際の条件を持つ。全18役を個別群でも覆い、74箇所の関数範囲参照を実P6 bytesへ再hash一致させた。主要な対応は次のとおり。

| 群 | 実payload・field | P6実consumer | 設計上の保持 |
|---|---|---|---|
| D01 | acceptanceのparents/artifact/files/directories、全空dir、runtime/code | L3722–3779 | 現 active 全inventoryは毎回。旧全inventoryは変換元・採用範囲の証拠として保存し、繰返し全scanを省くなら新しい引用契約を明記 |
| D02 | state/physical.bin、state/instructions.jsonl、records.offer/leadと位置 | parent_row_sources L3806–3825 → make_reduction_state L950–962 → reduce_candidate_numeric L979–987 | 全現在行と順序付きpivot/offerはactive。rank/headだけでは代用不可 |
| D03–D05 | delta/seed34の単行、packet/refinementの全steps、外部Eの単行とinstruction/target/manifest | parent_row_sources L3825–3835 → thin_anchor L3840 | role・native stepの出所と物理行を保持。外部Eの整数1と旧非再演の意味を維持 |
| D06 | continuationの64 snapshots/e/physical、64 steps/manifest、97祖先 | thin_anchor L3864–3899、parent_row_sources L3834 | 行・target遷移・native鎖はactive。旧section/E solveは既に再実行していないので、metadata読取削減を「旧数学再実行削減」と言わない |
| D07 | v3/v4/v5各128のrows/{physical-normalized.bin,instruction.json,target.json,manifest.json} | 各saved_rows/promote、特にL3168–3280/L3433–3484 | 全384行をglobal1450..1833へ順序保存。各層local0は別の出現として保持 |
| D08 | latest final target/lambda、native start target、HEAD/結果/separator | promote_*、outer_metadata L3986–4013、read_final L4610 | current target、previous target、selection lambdaの実bytes。最新lambdaについて全R行と両targetを毎回照合 |
| D09/D22 | original97 mixed5/6＋384 ten-key、各scalar0、relative target鎖・native context | current_derived_rho2 L4933–4949、saved_rows L3221–3277 | raw原形と順序を保持。原rho2/word由来の未決前件を別記 |
| D10 | 旧64 fixed16とmanifest、5JSON/11binary、geometry/index/residue54 | fixed参照reader L1741–1820、outer_metadata L4015–4030 → run_selection/candidate | 全16は現計算のactive資産。batch側fixedはmanifest一件のみ、payloadは元旧64文脈に解決 |
| D11 | prepare旧lower4＋lifted-grade4、block0..3 basis4、body/segment/lead | thin_anchor → retained FixedBundle → run_selection L5457、primal/P1 L4895–4904 | 全12blobをactive。過去の正しさのreceiptだけでは新section/primalの数値を供給できない |
| D12 | P1 manifest、degree2.cache.bin、instructions.jsonl、canonical index/8059 residues | fixed.p1/index/pairs → 新sectionとcorrected_source | 現在必要なcache/指示列/型と順序をactive。参照しない部分の縮小は別の正確なdomain監査が必要 |
| D13/D14 | Task712 map bundle、三raw辞書、実行source/retained TCB | bundle.tables → current section/four_B L4912、context → raw/source/P1 | 保守的初版では登録map全体とP1指示列を残す。全transitive最小性を未証明のまま削らない |
| D15–D17 | 古いoracle/continuation/batchのsection/cochain/raw/source/primal/P1/B/reduction全body | saved phase、accepted_oracle_top_metadata、saved_rows | 上のactive部分以外はcold候補。旧数学・全数比較を引用する命題と、その実採用票が必要 |
| D18/D19 | 歴史checkpoint/invocation、P/C結果、source/継承票、全fixture/取得/保全/cost | anchor metadata、saved_checkpoints、loader range、全inventory | 小さい採用証明書はactive、全履歴は復元可能なcold。workflow successを数学の代用にしない |
| D20 | 今回selection、全候補/row/phase/checkpoint/final、二診断 | run_selection/run_candidates/read_final/admit_diagnostics | 今回の完全比較・保存・resume契約は保持。cold化を現在の未完prefixの省略に使わない |
| D21 | 今回ordered_reductionsとphysical_factorsのrank長全列 | reduction_payloads L4363–4372/L4395–4405 | 初版cold化では不変。共有表＋係数列などの出力表現変更は別仮説H3 |

同じfileがactive値、native由来、過去命題の証拠、運用証拠を兼ねる場合は併記した。古いという理由だけで全fileをcoldに分類していない。

retained自系Lのboot L583–613、FixedBundle L694–801、current_section_cached L803–859を静読し、12blobとP1/geometryが新計算に届くことを確認した。旧64のbasis/manifestと実v5 parent-layoutはmetadataのdescriptor・名前・型だけを読み、元の大きな数学payloadを再演していない。

F3. 命題の三分と正直な報告

| 分類 | 将来の実runで主張するもの | 必要な根拠 |
|---|---|---|
| CURRENT_REDERIVED | active全bytes/型、全R行の順序・pivot、最新lambdaの全行と両targetのpairing、今回のfresh selection/E/依存判定/新target更新、今回出力の独立比較 | 実際に読んだ入力閉包、実呼出し、完全比較した結果。source pinだけでは計算済みとしない |
| ACCEPTED_CITED | 旧64/v3/v4/v5の採用済み限定計算、固定資産の由来、一回変換で閉じた行identity/写像など | 一意のrun/attempt/head/artifact、採用裁定、P/C結果、source/runtime、全input/output pin、命題/範囲/依存/限界 |
| OPEN_PREMISE | 元97祖先・native rowのword由来、原rho2を直接読まず導いた相対target前提、元word/source lower-zero/positive replay/full A0等 | 未決を明記し必要証拠欠品はUNKNOWN。保存hashやF3の等式から格上げしない |

例えばP6は1450/1578/1706/1834の四段で各lambdaのpairingを呼ぶ。将来「最新1834だけ毎回再照合」へ替えるなら、旧三段は採用票の引用になり、旧4段再照合flag/件数をそのまま出してはならない。現在のselection lambdaはbatch中固定し、新しいfinal lambdaとその後のoracleを区別する。

実1834例のtarget祖先は32件5-key＋65件6-keyを原形のまま先頭に、3×128件10-keyを順番どおり追加した481件。zero scalarは消さない。旧basisの数学的・語的由来をすべて今回作り直したと報告する設計にはしない。cross-checkedの既採用射程を保持し、verifiedはLeanだけに予約する。

F4. active bundleの候補型

詳記は `active-cold-schema-design-v1.md`。候補 `closure-manifest.json` と今回の `execution-acceptance.json` を分ける。前者には不変のnative identity/命題依存を、後者に今回run/attempt/head/host root/実source/capsを置く。前者18項は `schema, contract_version, design_status, observed_anchor, immutable_scope, current_state, row_table, target_ancestry, relative_target_chain, native_contexts, active_objects, cold_objects, accepted_claims, unresolved_premises, source_tcb, inventories, conversion, run_parameters`。これは設計用schema名であり、既存v6 wireや実artifactではない。

current_stateはrank/gen/kind/native state_head、全行/pivot records、target、previous_target、selection_lambdaと型/次元を保持する。物理encodingはbase3四trit/byte、48384座標、1行12096 B。行の連結保存を選ぶ場合も、出現iのbytesが元file/offsetの同じ行へ完全一致することが必要で、行順・offer・lead・native roleを再採番で捨てない。

row_tableは `row_id,native_context,native_role,native_local_id,offer,lead,row,instruction,manifest,target_link` の出現単位表。native_contextは元artifact/owner/source/start/selectionのidentityに結び、同じcontent blobを共有する場合も出現は併合しない。元文書は再sealして新ownerへ付け替えず、foreign-native型を明示する。JSON pointer/JSONL位置を使う時も全元fileのpinに結び、record hashだけで所在を認証しない。

relative_target_chainには元97の前件、各native schemaの遷移、before/after target実bytes、scalar、対応行、元instruction/target.json/row-manifestと全rollingリンクを置く。古いmulti-row遷移をone-row型にcastしない。現在のtargetとstate_headは最終native遷移そのものへ結び、輸送wrapper・closureのhashを新しいphysical anchorにしない。

inventoriesは変換元native全inventory、変換先active/coldの別inventory、全論理出現写像、全空directory写像を持つ。内容重複しても名前/文脈は保存する。原JSON5-key→batch JSON3-key/binary5-keyの射影は既知の限定型として扱い、reference-only fixed manifestの相対fileを新保存先に誤解決しない。

引用証明書は、claim ID、命題文/範囲、実run/attempt/head/repository/workflow/artifact、採用裁定、producer/checker結果、source/runtime、input閉包、output objects、依存、限界、可用性方針を必須とする。採用裁定のないcold blob pinは命題の根拠にならない。元workflowがfailureの歴史資産も、原結論を書き換えず、別に認可された限定採用だけを引用する。

F5. 一回変換と各runの役割

変換器と独立監査は、一度、全変換元file/空dir/文脈、native行の出現と順序、全祖先原形、逐次target、全rolling body/link、全参照の同じbytesへの解決、各保存先と完全復元を照合する。この等式・写像の証明書自体にも実行/source/入力/出力/独立結果/採用裁定のpinが要る。変換元metadataをhashしただけで旧P/Cの数学を再導出したとはしない。

各runでは、採用済み変換証明書・命題証明書・その依存と範囲、完全active inventory、実型/全bytes、全R行のpivot/順序、最新target/lambda、必要なpairing、宣言したactive relative target等式と全rollingリンクを再照合する。その上で今回のfresh計算と保存/比較を実行する。旧cold全体をhash/parseしなかったなら、それを実行したflagや件数は出さない。

保守的初案ではrolling再計算に必要な元instruction、target JSON、row/candidate manifest、root/boundary文書の全bytesをactiveに残す。過去の巨大literal/reduction本文へ向く参照はpin/文脈を保持し、その本文を当runが使わない部分だけを引用命題へ移す。実際のconsumerまたは採用する命題が本文を使うなら、その辺はactiveへ戻す。隠れたcold取得や読取省略はしない。

この引用化は、Task1111原案の「旧readerが読む全量をそのまま現runでも読む」という全同値の主張とは異なる。N1–N7の十分性、全consumer同値、`V_new ⊇ V_old`を本便で代行採択していない。公開された行/祖先/鎖/型/保全の検問を設計条件として持ち、別の独立裁定に提出する。

F6. TCB、失敗、復元

追加TCBは変換器、typed resolver、native-to-active出現表、採用命題ledger、mirror/保持・復元処理、監査器である。既存の算術kernel、decoder/filesystem、hash仮定、採用票の正当性も残る。作者一人の変換＋自己照合は独立採択ではない。現在使うsource/必要dataは全file認証し、過去sourceの保持・range同一性と実呼出しを混同しない。

cold保存は、元全bytesとnative論理inventory/空dirを長期に取り出せるmirror、保持責任・期限、独立複製、定期照合、復元テストとそのreceiptを要する。URLの所在だけでは内容を認証せず、非期限切れを永久可用性の証明ともしない。取得不能な必要証拠、閉じない命題依存、未登録のactive参照は依存ID付きUNKNOWN。資源上限はUNKNOWN_RESOURCE。不正型・pin不一致・矛盾した写像は拒否/FAILとし、研究上の結果を勝手にPASSへ進めない。具体的status wireは将来別登録であり、v6 schemaを変更しない。

観測者が空dirを黙って作ってEOFを通す設計にはしない。復元は別の明示された処理と全receiptに結び、元root不変、変換途中/未完成artifactは未採択として保存する。closureの自己hash循環を避け、全file pinとsealの対象集合を今後のexact wireで定義する。

F7. 反例と未決事項

設計本文F6に12件を登録した。特に、local0の層混同、spanを保つ行順置換、scalar0祖先削除、中間instructionを再sealして終端だけ旧値を貼るもの、plain target SHAとpacked SHAの交換、fixed参照の誤root、過去q/kappaの新lambdaへの流用、採用票のないcold pin、空dir欠落、非可換語の段併合、未完prefixの完成扱い、未実施の四pairing報告を拒む境界を持つ。まだfixture作成/実行はしていない。

`t_before - t_after = theta * row` のF3等式は、zero記録や順序、逐語式を決めない。`sr(1)+sr(1)=2`と`sr(2)=-1`は普通整数で異なるため、和が等しいことを理由にword段を併合しない。元97/原rho2の前件は残し、DERIVEDやphysical lower-zeroの限定をfull source lower-zero、positive replay、full A0へ上げない。

次の委嘱に必要な未決は、exact codec/native rule registry、全P/独立Cのpublic consumer対応、削る各旧callと代わりに使う採用命題の全対応、正式mirror/復元契約、独立変換監査、全active/coldの実volume、境界fixture、source/TCB全pinである。P1指示列とTask712全mapの最小部分集合は本便で確定せずactive保持。22群表を全プログラムのbyte最小閉包証明とは呼ばない。

F8. 性能仮説を分離する

| 仮説 | 単独で変える面 | 測定するもの | この変更だけでは減らないもの |
|---|---|---|---|
| H1 | blob重複除去と論理出現map | unique保存bytes、実cache-miss取得bytes、復元/hash費用 | 同じnative fileを再構成して全readする場合の数学/parse、現在rank長列 |
| H2 | 旧全payload再読を採用命題引用へ替えるreader | 過去file/bytesのhash/parse、native認証秒、active量、ledger費用 | 全現在行/pairing、P1/Task554/maps、fresh section/E、今回factor列 |
| H3 | row-source/lead共有表＋完全係数列による別出力codec | 重複JSON bytes、配列生成/serialize/parse/展開費用 | 消去自体、全係数domain、zero/順序の意味。完全列は依然ΣR_j trit |

H3は現P6に実装しない。将来行う場合は、zeroを含む全ordered列、`-sr(coefficient)`、outer exponent、target側`+sr(theta)`を一意に復元し、別public serializer/consumerと語の監査が必要である。省略形を再び全JSONへ展開して比較すれば、その費用も計上する。

root実v3/v4登録宇宙では、論理2,575,693,188 B→一意2,463,644,182 B、差112,049,006 B。差には各artifact内重複を含む。v4側は同path同content933件/45,373,127 B、別path同content10件/501,997 B、v3にないcontent10705件/1,262,218,926 B。output部分も新content6188件/1,205,023,375 Bがあり、旧payload全量の累積内包という前提を採らない。この実測を圧縮ZIP転送や実秒の削減へ読み替えない。

P6 L4363–4372の二つのrank長列生成、L3248–3253の全event走査は、その部分についてΘ(ΣR_j)、全仕事について少なくともΩ(ΣR_j)の根拠になる。全walltimeのΘ(kR)、有限rankでのcap超過、1695秒一定、代替方式の不可能性は導かない。

F9. 比較設計と未観測

同一の実親終端/rank/lambda/target/行順、k128/no-refill/caps、runtime/kernel、runner資源、cache状態を登録した対照で、H1/H2/H3を一つずつ比較する案である。whole output JSONのsource/acceptance/timing差を数値差と誤読せず、宣言したcurrent数値結果・native identity・復元全因子列を対応させる。実比較/GHA dispatchは本便0。

現P6計器は12-key、18inventory＋4native metadata＋4state restore/pairingの完了26区間であり、まだ実測前。中断区間は欠測であって0秒ではない。外側download/extract/preservation、P/C process wall、内側caller、phase telemetryを分離し、inclusive区間を二重加算しない。k/親数/rankが同時に違う一観測や次run残差だけから単一原因を断言しない。

一回変換・独立監査・mirror/復元の初期費用を別計上し、再利用回数に対する償却も実差が出るまでは仮説に留める。追加の反復/順序入替え比較はその都度有限run計画として別承認の対象で、無断の新suiteや探索を追加しない。

F10. 納品、自己照合、凍結

補助正本は `%TEMP%/shadow-atelier-audit163/task1113/`。内容を根拠なく増やさず、すべて設計/metadataである。

| 正本 | bytes | SHA256 |
|---|---:|---|
| p6-current-closure-dependency-design-v2.json | 136132 | 4f4a3d724e3a1243ae9599e169dc281ce7a006a1d2d61d24697427ec4c017477 |
| active-cold-schema-design-v1.md | 18295 | ac55aa903fdfa732117c478c22b4018bbfa630b07541db934ff03f422b086b4e |
| performance-hypotheses-design-v1.md | 8387 | 8b1d690e61e9d1a291e8e3f4990853b7cc5b60965a191a8d34919bb7a54f6150 |
| author-static-source-and-design-evidence-v1.json | 68260 | 5de7695da906b0e3db72ac0a7ddc05d5492901bb19307e3c7c3cb19a5b8acdec |

依存v1=159815/8b284184bafe1b5ed7dfd85a761aceee64c7b224480eeb31e79665e219a868e6は、dependenciesがPSの`{value:[22件],Count:22}`包装であった途中票として保存・不採用。新v2は直接System.Object[]/22、各dependency本文/range不変。自己票は実P6の74区間参照、22ID、全18rolesと16入力fileのpinを持つ。全数学payload再hash・数値再演の票ではない。

本返信と上の正本を作者設計票として凍結する。既存P6/1109/全artifact/他repo file変更0。実装・変換・新性能実測・新rank・独立同値性完成を主張しない。

TASK1113_VERDICT: BOUNDED_COLD_STORAGE_DESIGN_COMPLETE_NOT_IMPLEMENTED_EQUIVALENCE_AND_PERFORMANCE_OPEN

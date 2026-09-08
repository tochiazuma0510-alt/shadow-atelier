# Task1114 — C6 current 入力閉包と過去命題引用の独立設計

F1. 判定と固定対象

現在必要な数値入力を残し、過去の認証作業を具体的な採用命題への引用に置き換える保守案を作成した。これは実装可能性を裁定してほしい設計であり、最小閉包の証明、変換成功、数学同値性や性能の実証ではない。引用への切替を実装せず、現C6は全18親を読む契約のまま維持する。

対象は task1110/search/check_d972_r07_fixed_lambda_cycle_batch_v6.py = 419541 B / SHA256 3996972ccfe8ba9c168b537ac274de96ff69a6fe27fb400e7de6a8e3a19a52ff。指示書4976 B / cd09ec5e1931cbd0a8f27a37470e0498e4b3855ff9cb1ca79372b095ce54d269、公開2224/2227/2228/2229、自系凍結1110と32件補票を根拠にした。P作者1113の設計、返信、私的source/helper/fixtureを読んでいない。自系C6のcallerと公開metadataからの設計であり、自作C6の独立数学監査とは称さない。

正式1834/8539は2224のcross-checked限定7条を保持する。現v6の18親・k128・一batch・no-refill・既caps・親別計器は不変で、今後の採用数a、rank、generation、λ、oracle値は未観測の変数である。1962を結果として固定しない。C6の二つの未着登録値もNoneのまま。rootの1112受領PID19504、他の実受領、親treeを操作していない。

F2. C6の実入力宇宙

依存票 current-input-dependency-map-v2.json のI01–I33は、18親に加え受付、実行code/raw、候補root、診断、自己試験、独立C出力を含む。source-and-caller-ranges-v1.json は全165 raw区間のoffset/bytes/SHA/行、42の具体的caller区間S01–S42、その原文、各入力群への参照を保存した。全source bytesを覆い、依存票中の全関数名は実区間に解決した。これはASTによる動的callgraphや最小file集合の証明ではない。

現コードでは AcceptedInputs（676行～）が全18roleを順にPinnedTreeへ渡す。PinnedTreeは全fileと全directoryを認証し、read時にも全pinを確認する。末尾4724–4726行のbundle/inputs/files.unchangedが再照合するため、現在「数学では使わないfile」も入場と保全の入力である。下表のcoldは将来の候補であり、今の読取除外ではない。

| role | C6の実用と次consumer | 将来もactiveに残すもの／引用候補 |
|---|---|---|
| state | base_pivot_metadataの8059命令→1354 pivot、physical.bin→ThinAnchor.row | 全行bytes、offer/lead/order/row原点。旧JSONLの全rolling再読は原点命題を要する引用候補。 |
| delta | seed30の1行/target鎖。result.parents.p1→external_state→FixedBundle | 行と現在必要なP1親join。旧seed履歴だけは命題別に引用候補。 |
| seed34 | 1行と前後target/native instruction→旧1450状態 | 行と順序/原点をactive。旧body再読は引用候補。 |
| packet | steps1..3の3行とnamed ancestry→旧状態 | 3行と各origin。旧phase/target/rolling記録は引用候補。 |
| refinement | steps1..26の26行、canonical-index→external_state | 全行と実canonical P1辞書をactive。旧refinement履歴は別。 |
| oracle | geometry manifestの実SHA→各fixed参照・root_records。旧oracle pin群 | 現geometryの実データとidentity。旧λの失敗表やtelemetryは新λの代用品にしない。 |
| e | external Eの1行、旧continuation-start target、derived ancestry | 行はactive。旧1450 pairing用targetと過去E確認は条件付き引用候補。 |
| prepare | task554_parent(args)→FixedBundle→section/primal/corrected | 現P1/source計算の実資産。下位file剪定を未証明なので全roleをactive。 |
| block-0 | owner0の登録Task554資産→同bundle | owner順を保ち全role active。 |
| block-1 | owner1の登録Task554資産→同bundle | 同上、owner0等へのalias不可。 |
| block-2 | owner2の登録Task554資産→同bundle | 同上。 |
| block-3 | owner3の登録Task554資産→同bundle | 同上。 |
| p1 | 実canonical P1、index/root/exponent/lead→8059 section/primal/P1補正 | 成功receiptでは数値を供給できない。保守的に全role active。 |
| task712 | REFINE.load_tables(args)→bundle.tables→四ownerのgrouped_forward | 実B maps/entriesをactive。全4文字の和を省略しない。 |
| continuation | 64行、旧97 ancestry、旧λ/target、fixed16実payload→各promotion/新bundle | 64行とfixed資産をactive。旧snapshot/phase/checkpoint/invocation確認は引用候補。 |
| batch-parent | native v3、1450→1578、128行、97→225、旧3+6×128相/772checkpoint | 行とglobal1450..1577/local0..127の原点。旧dense literal等はA1を前件に引用候補。 |
| batch-parent-v4 | native v4、1578→1706、128行、225→353 | 行と別role/global1578..1705。旧確認はA2を前件に引用候補。 |
| batch-parent-v5 | native v5、1706→1834、128行、353→481 | 行、現λ1834、current target、正しいprevious target、原点。旧確認はA3を前件に引用候補。 |

原state1354とその後のdelta/seed34/packet3/refinement26/E/continuation64が1450行を構成し、3層384行を加えた1834行が現在の基底である。sourceのrestore_physical_anchor内の各append callerをS10–S13へ結んだ。native v3/v4/v5の受付6/7/8key・親15/16/17を現在の受付9key・親18へ書き換えない。

prepare/block/P1等についてC6から見える境界は、4617–4620行のREFINE.load_tables、BASE.checker_source_context、O.Geometry、C.FixedBundle(args, external_state, words, tables, geometry)である。私的/別系helperを開いて内部の最小file集合を推測していない。この箇所の「全role active」は未判定を隠した削減ではなく、削らない保守選択である。細かな剪定だけをOPENとする。

同じfileは複数用途を持つ。旧行は古いphaseの由来であると同時に、現在の消去と新λの全行pairingが読む数値入力である。row_sourceのparent-rowはexact8key、current batch-rowはexact6key。v1依存票に書いた9/7という計数誤記を、source3728–3741行へ照合してv2で訂正し、v1を保持した。

F3. 現在必要な計算と旧再確認の境界

BatchReductionState.reduce（502–524行）は全旧pivot/実row callbackにL.reduce_denseを適用する。全現在行のsource/offer/leadと実bytesをreceiptで代用しない。reduction_payloads（3744–3796行）は各候補のrank分のcoefficientを零も含めて順に並べ、physical_factorsとordered_reductionsを作る。complete_reduction_coefficientsとliteral_signsは順序、行SHA、普通三進係数、-sr、外σ一回、correction側+srを結ぶ。新数値target更新は t_after = t_before − theta*q であり、correction rootへ足す+sr(theta)と符号の用途が違う。

replay_selection（3690–3725行）は現λからsection8059、cochain、全54433 chordのfit/residualと2auxを作り直す。replay_candidate（3878–3962行）はraw/source/primal/P1/four-B/reductionの全形成相を別に比較する。96776 lower、四つのtop/maps、全物理48384の現在の仕事はactiveである。旧oracle値を新λの結果として持ち込まない。

固定16payloadは実3159 Bのcontinuation/output/fixed/manifest.jsonから列挙した。basis/canonical-index/tag-fox/P1 exponent等のJSONと、BFS・parent・edge・carry・tau・phi・選択弦等の実配列を保守的にactiveとする。今回はmanifestだけを読んでpinを記録し、16payloadを再hashしていない。C6 root_records内のC.check_fixedは、再構成したbundleの値と保存fixed全体を比較する。これを引用へ替える案は今回採らず、採るなら固定値同値命題と実active bytesの同一性が別前件になる。

四pairingの実callerと引用案を次のように分ける。各行は実施済みという意味ではなく、凍結C6の予定動作と将来設計の対比である。

| 対象 | 現C6 callerと比較先 | 将来案 |
|---|---|---|
| 1450 | check_actual:4591→ThinAnchor.measure_selection。v3 start.anchor_pairingへ比較。 | A4を採用できれば過去命題引用。全行bytesは現λのため残す。 |
| 1578 | check_actual:4600、historical_v4_intake。v3 final separatorとv4 intakeへ比較。 | A5/A8を前件に引用。native1578のλ/二targetを1834の値へ付け替えない。 |
| 1706 | check_actual:4609、historical_v5_intake。v4 final separatorとv5 intakeへ比較。 | A6/A8を前件に引用。 |
| 1834 | root_records:3487、parent_intake_record。v5 final separatorへ比較。 | 今回再導出側に残す。全行の三角性/現λ消去/正しい二targetのdot=1を実bytesで照合。 |

ThinAnchor.measure_selectionは全行のpivot=1・既pivotで0・λdot=0と二targetのdot=1を同時に見る（S09）。過去3点を省略しても、現在1834点のこの確認は省かない。最終BatchReductionState.finish_arithmeticは実採用行を加えた全行へ新final λを当てる。Linearの場合はλ/null・separator nullの型を保ち、存在しないpairingを要求しない。

旧authenticate_saved_*_batch_rowsは、保存係数・全rankのliteral/reduction構造・row/target/rollingリンクを再構成するが、旧section、E materialization、P1、消去、separator solveをもう一度実行する経路ではない。この既存差を保持し、「旧数値再演を大量に削減した」と誤記しない。削減候補はその大きなmetadata列と全payloadの認証、および上の三つの実pairingである。

F4. 引用する命題と将来report

citation-and-report-contract-v1.json はA0–A9の前件と、K01–K15の実caller別切替案を保存した。A0は元97および各行の条件付きword/ρ₂由来、A1/A2/A3は各native層の順序付きrow/literal/target/rolling命題、A4/A5/A6は三歴史pairing、A8は過去publication/保全/opaque loader同一性である。A7は現在の再導出、A9は現在の固定数値資産として残す。

引用証拠には、単なるblob SHAに加え、採用裁定の該当命題、正しいrun/attempt/head/artifact、元Pと元Cのsource/runtime、実success結果と受理scope、対象native state/λ/target/row範囲、元inventory、変換との全対応が必要である。source hashは実実行を意味しない。PのみのPASSや別runの同rank結果では代替できない。2224の正式限定7条は維持するが、そこから「すべての旧検査を引用化してよい」という新承認を導かない。A0–A8の削除許可は、該当箇所についてOPEN_PREMISEである。

提案するassertionのexact9字段は id/subject/mode/scope/dependencies/evidence/actual_work/availability/limitations。modeは次の三値に限定する。

- CURRENT_REDERIVED：今回の実bytes・実実行・実範囲で照合した命題。設計票にはplannedとexecution=falseを置き、今から成功扱いしない。
- ACCEPTED_CITED：採用済みの過去命題を、その元scopeと前件付きで引用する。今回同じ検査を走らせたという意味はない。
- OPEN_PREMISE：必要な元命題、変換同値性、decoder、受理、可用性が未解決。必要閉包に残るなら完成を授権しない。

引用先は循環させず、subjectにはnative role/run/physical head・global/local row域・必要λ/target・code/runtimeを明示する。現在の全体結論が再導出と引用の混成なら、その依存を列挙する。原ρ₂を直接読んだこと、元wordを新規に実証したことにはならない。

旧3pairingを引用化した場合、native_pairing_rows_recheckedを[1450,1578,1706,1834]のまま出さず、当該開始点ならcurrent側[1834]とcited側を分ける。parent_layersの384 candidate/row・2304 candidate phase・2316 checkpoint・3 invocationは、旧証拠の被覆数として引用欄へ置き、現在*_checkedへ加算しない。旧old_snapshot_numeric_replays/old_insert_numeric_replaysはもともと0なので、その0と新しく省いた旧metadata再読を混同しない。

all_parent_files_and_directories_unchangedを、未読cold treeまで含む従来の意味でTrueにしない。active inventoryの実before/after、cold logical inventoryの採用/可用性、full cold bytesを今回読んだかを別字段にする。歴史loader rawの同一性を引用する時もraw_compared_this_runを明示し、現実行codeの全pin認証は残す。既存C6のwireをこれらへ変更する作業は行っていない。

F5. 初回変換と各runの閉包検査

初回変換の独立監査は、実行ごとの軽い引用確認とは分ける。元18roleの全file、hidden/pending/diagnostic、全directory/empty directoryを事前登録し、logical file IDを(schema, role, run, attempt, artifact, relative path, bytes, full SHA)で持つ。さらにJSON pointerまたはraw offset/length、global/local row、candidate/sequence/列順を加えたlogical occurrenceを記録する。同contentを一つの物理blobに置くことは許しても、異なるrole/local0や別用途のlogical occurrenceは同一化しない。

独立変換checkerには、元の全bytesと新表現の復号結果の双方向被覆、欠損/余剰なし、全EOF、全native型、全rollingリンク、各段のtarget減算、zero/order/literal・row原点の同一性を要求する。元97を32 five-key＋65 six-keyのまま、後ろ384だけten-keyで保持する。変換のterminalは元最終physical state_headを保持し、輸送wrapperのhashから鎖を再起点化しない。全fileと空dirを別のfresh rootへ完全復元し、元のcanonical bytesまで一致させる。これらは2227が掲げるN1–N7等の別審査に渡す条件であり、Task1111を置換したり、今満たしたと主張したりしない。

新TCBは、archive keeperの不変性・可用性、logical occurrence resolver、decoder、採用命題registry/version resolverである。C6の既存24保持区間のpinが同じという事実だけで新TCBを免責しない。P/Cの私的helper・fixtureを共有せず、変換作者とそのcheckerを分ける。新source/試験/部署間採用は将来別便の対象である。

各runの先頭では、現在activeの全file/dir、現code/raw/runtime、引用票とorigin map、必要なcold可用性の前件を先に照合する。activeの現行/offer/lead/target/λ/P1/maps/辞書は実bytesを読む。現在の新候補全相、commit済みcheckpoint、許された一相先のdurable tail、invocation、診断、final、全current出力比較は残す。現在のresultを過去引用で正当化しない。

cold可用性の具体候補は「事前に全復元を照合したread-only保存世代＋各runの全blob ID/existence/lengthのmetadata照合＋全復元票pin」である。ただし、現在の全cold bytesを読み切らずに可用と扱うための保存系仮定を新TCBとして明示する。存在/長さの確認を内容SHA再照合と偽らない。この仮定をrootが採用できなければ切替を行わず、従来のactive全読を保つ。pinだけで無条件の完全復元可能性は言えない。

必要blob欠品/取得不能はUNKNOWN_INPUT_MISSINGとして未完、型/意味map/size/hash/rolling不正はREJECTED、資源中断はUNKNOWN_RESOURCEとする設計候補である。未知の可用性はOPEN_PREMISE。どれも数学非存在や正常completed candidateへ変換せず、独断の取得・元親への書込み・零埋めをしない。今回、この将来status型を既存実装へ加えていない。

F6. 反例検問

conversion-and-counterexample-contract-v1.json のX01–X20は実行していない設計検問で、既存C第五群の再登録や試験数増加ではない。主要な具体例は次のとおりである。

| 変異 | 残す検問 |
|---|---|
| 同じlocal0をv3/v4/v5間でalias | native role/run/artifact/global/local/元fileを組にして照合。 |
| 元97の形を一律ten-keyにする／index353のscalar0を削る | 原形mixed97、全384、列順と全linkを保持。 |
| 同じspan/target総和を保ってfactor順序を交換 | 非可換語の逐次列とcanonical展開を照合。総和では受けない。 |
| 同じ行のtheta=1を二段併合してtheta=2にする | sr(1)+sr(1)=2とsr(2)=-1を区別し、段を併合しない。 |
| 中間instructionをresealして元final headだけ写す | 正しいnative unsigned bodyで全rollingリンクを再計算。 |
| targetの加減符号を逆にする／packed SHAをtarget JSON SHAへ代用 | 段別減算とcorrectionの正因子を分離し、二つのhash域をtypedに保持。 |
| v5 start.previousやcompleted selectionから現条件を取る | previousはv5 start.target、λ出典は正しいselection/startと最終separator。 |
| dtype/shape検査前に5→3射影／batch固定参照dirへbasisを探す | 元5字段の実型と元old64の16payloadにjoinしてからJSONだけ射影。 |
| byte相等のfloat/bool offset、誤fileのsubstring | 普通整数、全file pin＋位置付きrow SHA、packed padding/EOF。 |
| P成功だけ、別run同rank、source hashだけの引用 | 実P/C成功と同native tuple、実source/runtime、採用命題を要求。 |
| 空dir/hiddenを落とす、cold欠品を無視する | 全logical inventory・復元・採用可用性契約。 |
| durable tailをcommit数へ算入／途中physical HEAD | 実HEADの固定prefixと一相先を分離し、finalizer以前は公開しない。 |
| 未計算oracleを0、Linearに架空λ、旧hostへ新値上書き | null/branch/readonly completed resumeの別型と元bytesを保持。 |
| 条件不足で初回独立、全128独立や失敗集合単調性を宣言 | candidate存在・親span零・derived前件・実非零raw一致・第一decision完了に限定。 |
| span/telescopeからsource lower-zero、positive、A0へ昇格 | 元word/ρ₂前件を引用または未決として残し、強い主張を出さない。 |

codecの非一意復号・末尾欠損・zero/order消失、current/cited count混入、欠測秒を0にすることもX19/X20で扱う。正例を通常の将来readerへ通したうえで意味一箇所の変異を拒否する形を要求するが、ここではfixtureの実装/実走をしない。

F7. H1/H2/H3の別評価

H1はwhole blobの内容重複除去である。同contentの保存/輸送を減らせる候補だが、logical occurrence、型、順序の確認は残る。2229のwhole-file比較はその公開宇宙の所見として参照し、この便では再測定していない。共有bytesの重複除去だけから、固有の旧phase/literalを読む仕事や現在のrank長列が消えるとは言えない。

H2は過去全再読の引用化であり、A0–A8の切替が採用された範囲の旧metadata/opaque raw/old pairingを省ける候補である。現在の全行、現λ/target、現在candidateとfinal、固定P1/maps等、origin map/引用/cold可用性のmetadataは残る。「blob重複が少ない」と「過去証明を再実施しなくてよい」は別の論点である。

H3はrank長factor列codecである。候補は、共通row-origin辞書と全係数位置を保持した列から、従来の非可換因子順序・零因子・-sr・外σ・+srを一意に復元する表現である。現コードは各candidateのR_j全列を生成/走査するので、その部分にはΣ_j R_jに比例する仕事がある。codecだけで消去核を軽くしたとは言えず、毎回冗長JSONを完全展開すれば読取コストも残る。canonical復元・decoder独立監査・新TCBは未実施である。

どのHもwalltime、必要run数、cap内完走、他方式不可能性を結論しない。2228の射程精密化を優先する。現Cの31計器eventは全対象区間が完了した場合の登録数であり、今回の実測数ではない。P/C/外側時間を混ぜず、inclusive区間を二重加算しない。state-restore ordinal0はrestoreのみ、1–3はenter_context込みという既公開差も保持し、欠測を0にしない。

F8. 未決事項と納品

未決は、(O1)各旧callerを代替する採用命題の正確な承認、(O2)独立変換/全復元/数学同値性審査、(O3)retained bundleの更に細いfile剪定、(O4)cold可用性・不変保存の採用可能なTCB、(O5)元97と各行の語/ρ₂前件の限定、(O6)新decoder/occurrence/claim resolver、(O7)現C6の未着bindingと未実行値、(O8)P設計との照合と性能である。O3は必要資産を全role activeに残すことで現設計の欠落を避ける。ほかも未解決のまま切替を実施しない。本便を現v6発射や進行中受領の追加待ち条件にはしない。

全材料は %TEMP%/shadow-atelier-audit163/task1114/ に新規保存した。主要pinは次のとおり。依存v1の小誤記を残してv2へ訂正し、凍結1110/32票を変更していない。

| 材料 | bytes | SHA256 |
|---|---:|---|
| current-input-dependency-map-v2.json | 48358 | 76d47c64a6efe22be14ab6e5a775ab22e78e6d5ff641bf9f34d2f6ec3e3f1bf7 |
| source-and-caller-ranges-v1.json | 477970 | 431cc23e75a2465891bf529a3c06a3598fafdea233c8bfcf099bb930b54e4d69 |
| citation-and-report-contract-v1.json | 19924 | e61c5b44920ebf0980e9741164af08a20d277d6e4bb1abb3dfeab931b1721407 |
| conversion-and-counterexample-contract-v1.json | 16701 | b40e8c8b29fa91e721abb5b2b49e7a9ca699e0b54429372ded6b96c047f3fb9d |
| current-wire-and-fixed-input-contracts-v1.json | 62172 | 235940e73b273da6576ae06190a3d042d511f0dc30e74e895df4cd6e6405ebb4 |
| input-evidence-pins-v1.json | 5828 | c3edcc922d256663007a073644808c0cf56f3733088b03e7183a395072ae14d6 |
| author-metadata-consistency-v1.json | 23358 | 68cbf6350db2668a8c3f4fca1f7554216e59ddb7888493e8793a9707ab047d6d |

自己照合は18role、全165 raw区間、42caller区間、全33入力群、15切替caller群、10命題、20既公開keyset、20未実行反例検問の参照解決を対象にした。16入力pinと凍結1110全43材料の全bytes/SHA不変を確認した。source/import/AST/compile/数値/GHA/Git/network/credential操作0、実親payload大規模再hash0、元資料/既存process変更0。作業はPowerShell/.NETの小metadata/自系source raw/JSONと設計票の作成に限る。最終全材料目録を同directoryのfinal-material-manifest-v1.jsonに保存し、指定返信とともにrootへ引き渡す。

TASK1114_VERDICT: CONSERVATIVE_C_CLOSURE_DESIGN_COMPLETE; CUTOVER_AND_EQUIVALENCE_OPEN; NO_IMPLEMENTATION_OR_RUNTIME

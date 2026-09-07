# Task1078 — parent1706 / fresh lambda1706 独立 C5 静的草案

F1. 指定 C5 の完全 source を TEMP に保存し、全通常接続・新第四群まで自己静読して、**IMPLEMENTATION_DRAFT_COMPLETE_INVENTORY_GUARD_CLOSED** として固定した。これは未実行の実装草案である。repo source/WF/旧返信/実 artifact を変更せず、P の私的 source・差分・1076 source-body material・私的試験は読んでいない。Python/GAP/source/import/AST/compile、全受領器、Git/GHA/network/credential の実行は全て 0。実施したのは PowerShell/.NET による自系 raw 編集、公開 JSON metadata 読取、opaque bytes/SHA と raw 差分の静的比較だけである。root の受領 session5057・その形成中の出力には触れていない。

共通 Task1077、自己 Task1078、公開 interface-v1 を全文読了した。root 通知の2206は親1706/8411の cross-checked 限定7、2207は具体 pin/別読/marker を伴う通知手順であり、新 C5 の実走結果や全 inventory の最終登録を補うものではない。root の暫定 inventory は参考資料に留め、source の NEXT_BATCH_INVENTORY=None を保持した。正式な登録の後着は、この固定版から別の binding 差分として扱える。

F2. 以下の納品 path は全て `%TEMP%/shadow-atelier-audit163/task1078/` を基準とする。新研究 source はまだ repo へ配置していない。

| 納品 | bytes | SHA256 |
|---|---:|---|
| search/check_d972_r07_fixed_lambda_cycle_batch_v5.py | 335937 | c868aa09a6dd6e94510f996080a8e3e0a7fea1563046486960c7b6a4fca55170 |
| root-review-checker-v5-v1.py（上記と全 bytes 同一の固定 snapshot） | 335937 | c868aa09a6dd6e94510f996080a8e3e0a7fea1563046486960c7b6a4fca55170 |
| checker-v4-to-v5-full-raw-diff-v1.txt | 142637 | 350317d0a3fb41b8da01a51861fd2a2f8da3f791e67b86a7d8b07c9ce86f94ff |
| checker-v4-to-v5-all-raw-changes-v1.json | 275758 | c02da08797751e747cdb5c085a358643ab77ebbc149c900e951e182177eb5f83 |
| checker-v4-to-v5-all-region-index-v1.json | 104840 | a46a1d21257bcf43da1fe0b475bfed85e41cd6e9991d0e784409ec31baad908a |
| checker-old-loader-and-kernel-raw-retention-v1.json | 30836 | b135043e0e0033e72e30df67fcc0d33aba2de40ede33b75c2f960993e16f005d |
| checker-draft-freeze-v1.json | 4219 | 2bc0d7e4739e6ec441ee59e0264cf7bf8eb2500a80ec4b2ddf316629aa58d2b1 |
| material-index-v1.json | 9127 | 79525a43d14d252db5cf0564a36643943835d6db8c37e3182ea922736df2f9cd |

source は ASCII、LF4640、CR0、BOMなし、末尾LF、行末空白0。基点 C4 は261170 B / a29380ec00876225cc618c7025d671a3da79aea3b31b829dedba13c59ba84633、自己 C3 は178914 B / 1aebf6e47807466ec56426a55e34d0c7f622a5896c40184540e4d153060946d7 として別保存した。raw region index は Python parser を使わず、column0 の def/class 開始による全 EOF 分割117→140区間、変更/追加40、削除0を記録する。全変更 JSON を保存後に再読し、保持部分と結合した両方向の全 bytes 再構成が C4/C5 の上記 SHA に一致した。diff は各区間の共通先頭/末尾だけを省略表示し、区間 index と全変更 JSON は全 raw の復元を閉じる。

F3. 自系旧4 loader の raw は C3/C4/C5 の三版で全一致した。これを、旧 source を新17親対応済みと見なす根拠にはしていない。旧 reader の入口には元15親の意味を保ち、v3用16親投影と新17親受付を別 helper にした。

| 区間 | bytes | C3 offset | C4 offset | C5 offset | 全共通 SHA256 |
|---|---:|---:|---:|---:|---|
| anchor_metadata | 2463 | 32215 | 37137 | 42623 | ab20e3cbf8f0b0d72a4ffdff93ea09ca71e9b50eec7b5ce3ac9a7aa22d70656e |
| base_pivot_metadata | 2403 | 39843 | 44765 | 50251 | 5be807b3382c0c938dc16ac5af4906b85f507e8f16b6844004aceebccc6ec1d7 |
| ThinAnchor | 3516 | 42246 | 47168 | 52654 | f4fe4ef5620b7a4e5256d70e15a1c3b4139827d6b6a717ec3e23a02e6ad6e1a9 |
| restore_physical_anchor | 14011 | 46344 | 51266 | 56752 | 3178867cb0c359149db73088e11bdee4b19b2e1c0acb9914ee4860044c72a231 |

さらに select_all_residuals、BatchReductionState、batch_tree_payloads、replay_selection、row_source、reduction_payloads、replay_candidate、complete_reduction_coefficients、literal_signs、compare_candidate_publication、ProgressAudit、invocation_records、compare_diagnostic(s)、compare_candidate_roster、旧 DEPENDENT fixture 等、保持票に列挙した20区間は C4 と全文一致した。変更された final_rho2 / compare_final は公開の二つの親層 count の追加、root_records / result / observation は新親来歴と schema 接続である。新 v4 保存 reader は自己 C4 の metadata reader を基点に明示 v4 用として別実装し、P の算術 adapter は共有していない。

自己静読では、初期の metadata 定数挿入が main 内にも重複していた箇所を発見して除去した。固定 snapshot の main は元の引数・deadline・例外・出力処理を保持し、全raw差分上の main の相違は17親を示す診断 label の一行だけである。途中 snapshot と除去記録は材料に保存し、完成 source と区別した。

F4. 独立受入鎖は次の順で通常 check_actual へ接続した。

1. AcceptedInputs が v5 の exact8key受付 `schema,parents,anchor,batch_anchor,next_batch_anchor,code,runtime,registration` と全17親の順序、実CLI絶対path、artifact tuple、全file/dir inventory、現 source/dependency/raw/runtime/caps を認証する。旧16の末尾 batch-parent=v3 を保持し、その後に batch-parent-v4=v4を置く。旧 anchor=64/1450、batch_anchor=v3/1578、next_batch_anchor=v4/1706 を別型として受ける。
2. 旧 restore_physical_anchor を元の意味で呼び、1450行/8155/97祖先/64段を構成する。新 caller が同じ通常 ThinAnchor.measure_selection で native1450 の全行/二対象を直接測定し、保存 v3 start.anchor_pairing と比較する。
3. 既存 promote_batch_parent が v3 の保存128行を受理し1578/8283/225祖先へ進む。その後、新 caller が native1578 の直接 pairing を測定する。authenticate_historical_v4_intake は、実 v4 parent-intake が1450→1578を記すことを保ち、旧 v3 header/HEAD/result/checker・全128/768/772/1と実 native1578 pairing・歴史P4/C4の旧4 raw証明列まで組み直して比較する。
4. authenticate_next_batch_parent_metadata / authenticate_saved_next_batch_rows / authenticate_saved_next_batch_progress は別の明示 v4 schema reader である。旧 v4 exact7key受付を新受付の最初16親・旧 anchor/batch_anchor/runtime/policyへ完全一致させ、実P4/C4と保持closure、owner/source/start/layout、HEAD/result/C/final、全128候補、各row4file、六相、全772 checkpoint、唯一の保存 invocation と入出力保全を結ぶ。
5. promote_next_batch_parent が保存 v4 層を受理後、別の ThinAnchor1706/8411を構成する。v4 HEAD に completed_steps を捏造せず、内部 current は anchor_completed_steps=64 からの明示投影とする。rank1578..1705の保存 local0..127 は受理後にだけ runtime parent-row(role=batch-parent-v4)へ束縛する。元 v3 の local0..127 は role=batch-parent のままである。
6. 最終 root_records が新 native1706 の全基底と二対象を直接 pairing し、実 v4 final.separator.direct_pairing と比較する。その1706 functional が通常 replay_selection の入力であり、自系の四 character/8059 P1/全54433 chord+2aux の fresh 算術と全新payload比較へ進む。旧 section/cochain/tree/E solve を再実行する経路は追加していない。

C4 の通常 measure_selection caller は最終1578の一箇所だった。C5 の [1450,1578,1706] は、新 caller を追加して明示した測定列であり、C4 に元から三 call があったとは述べない。旧4 rawを維持したまま、check_actual の追加範囲と root_records に接続した。これらの時間は未測定/nullであり、旧 solve 再走0を数値作業全体0と読み替えない。追加の native pairing が登録時間枠で完了するとの予測も置かない。

F5. 保存 metadata の全到達と count の意味を分けた。

| 対象 | 元64 | v3層 | v4層 | C5今回 |
|---|---:|---:|---:|---|
| 原 continuation completed_steps | 64 | upstream64 | upstream64 | anchor64 |
| 親の独立行 | 元1450 | 128 | 128 | 親計256、今回0開始 |
| rank/generation | 1450/8155 | 1578/8283 | 1706/8411 | 1706/8411開始 |
| 全DERIVED祖先 | 97 | 225 | 353 | 353を全保持して開始 |
| 保存candidate/row manifest | — | 128/128 | 128/128 | 実進行 prefix のみ |
| 保存candidate phase | — | 768 | 768 | 実比較済み相のみ |
| 保存checkpoint/invocation | — | 772/1 | 772/1 | 既契約の実履歴 |

各親 checkpoint は sequence0..771、初期0＋selection3＋6×128を復元する。相時計3＋768＋final1も772だが対応は異なり、finalを checkpoint772として数え足さない。parent-intake の二層合計は candidate256/row256/candidate phase1536/checkpoint1544/invocation2で、parent_layers はv3→v4の二要素を保持する。accepted_parent_batch_rows=128は直近v4層、previous_parent_batch_rows=128は前層v3、total_parent_batch_rows=256は和であり、今回 processed/accepted/dependent を進める値ではない。

新親の各保存rowについて、12096 B packed行、monic/三角条件へ至る自系読取、offer8283..8410/global1578..1705、実 instruction rolling、全 insertion vector、全 literal factors、六phase predecessor、target/plain JSONの全SHA、row publicationの完全な複製一致、全EOFを接続する。v4履歴内では v3 parent-row と自己 batch-row の順序を先に照合する。new runtime parent-rowへの変換で、その保存 source の意味を先に変更しない。

F6. 二対象と祖先の正本を固定した。previous は v4 start.target `7868b7806a0dc41c2bda8a1c4c6a10d1cfa2c2e6968aadf561e93820f12053e1`、current は v4 final target `954e1ba1a50e138a0577c27c285c21ed052f3491176d883f370e8a94d11b456a`。v4 start.previous の旧1450値を新 previousへ流用しない。新選定 lambda は `d036e848c46b563a5b0f683fb94afcbc759dc4bc402c6db14c82b172ccc0a653`、stateは `13c631c6dee46d4026e996f53370bcc202737f1082582b02271884593f902101` で、既知の実fileへ到達する。

v3 final225とv4 start225を全辞書/全順序で一致させ、v4 final353をその225prefix＋全128 ten-key recordとして組み直す。theta0も残す。新start/finalの祖先列は深くcopyし、保存された各世代の role/local offset を改名しない。数値 target更新の負号、物理係数 −sr、外側sigma一回、correction語への +sr(target.scalar) の既存契約を維持する。instruction.target_sha256はplain3key target.json全file、remainder_sha256はpacked targetであり別物。original rho2 の b41b9e69…/derived value1と original_rho2_directly_read=false を維持し、新しい元rho2読取や全A0条件を追加しない。

fixed は新v4 local manifest2903 B /1a1f4644685459af2412d698a0ac814b6c3a2b9beac6e95ce612b8f08d414b8cの専用参照 reader。local roster はmanifest一件だけを要求する。旧64の実 manifest3159 B＋16 payloadの全17file/全pin、元exact8key、descriptor五keyと JSONの5→3射影を認証し、owner/source/start/accepted geometryを結ぶ。後段では従来の C.check_fixed で lambda非依存値を再構成・比較する。旧generic同居manifest readerは変更せず、batch親側へbasis.json等を複写する処理はない。

F7. 公開wireの変更は公開 interface-v1と C addendumへ接続した。startは旧 accepted_batch_* を残して accepted_next_batch_*五字段・previous/total count・previous祖先225を追加し、new parent_intakeの全fileSHAを名指す。selection-start/HEAD/result/final/DERIVEDには anchor_previous_parent_batch_rows / anchor_total_parent_batch_rows を加え、旧 anchor_accepted_parent_batch_rowsは128のまま。C-resultにもその二字段だけを追加し、templateではnull、実 parent-intake比較後だけ普通整数128/256にする。現 source/self descriptor・全17 parents/host paths/入力保全へ同じschemaを結ぶ。

observationのoldはbatch-parent/v3状態＋保存v4 selection `181c87b906b2908e8d9d00e29faabf66bff673340e338bf18775e95150c3b4ab` の36104/74/131、currentはbatch-parent-v4/1706状態である。実 current選定の件数/先頭は未観測null。親intake前の条件はnull、selectionは実 committed sequence3、第一処理はsequence9からだけ記帳する。無候補はNOT_APPLICABLE、早期失敗はNOT_OBSERVED、直後durable tailはHEAD countに加えない。第一独立は非零raw/selected一致と親span/DERIVEDの実条件の下だけであり、今回128採用・失敗集合単調性・採用率・速度は要求も予言もしない。

既完readonly再受付、過去hostの明示invocation、bootstrap/二診断、final publication tail、候補全file/dir before-afterは元Cのscopeを保持する。CはP出力/親を変更せず、別の指定checker reportだけを書く。FAIL/UNKNOWN_RESOURCEでassuranceを落とす元main処理も維持。CLIは17親（block-rootは4回）、acceptance/candidate-root/output、通常10800秒/7168MiB・P登録5400秒/7168MiB、selftest300秒/7168MiBとfresh --selftest-rootであり、通常/試験とも未実行である。

F8. Cのselftest登録は次の四群、全て未実行。

| 順 | name | 拒否件数 |
|---:|---|---:|
| 1 | k128-version-registration-and-types | 28 |
| 2 | k128-full-roster-cutoff-and-restoration | 9 |
| 3 | batch-parent1578-admission-and-projection | 6 |
| 4 | batch-parent1706-two-layer-admission | 7 |

最初三群のliteral拒否名を維持した。第一群の現path陰性はv5→v4、v5受付陽性は新8keyに合わせた。第三群の旧six-key陰性は、新しい通常 historical-v4受付helperの正しい七key対照から検査し、保存v3 HEAD→v4 schema陰性も明示の歴史schemaに固定する。旧成功source/suiteの実行は0。旧DEPENDENT陽性の到達範囲を保持する一方、その過去の陰性が expected-file size/hash gateで止まりsemantic outcome比較へ達していないという限定を、新 fixture_scopeにも明記した。

第四群は同じ通常helperがpositiveを一度受理し、一箇所だけを変えたnegativeの ValueError が表の登録labelへ到達した場合だけ件数へ入れる。case-ledgerには登録expected_errorと実caught observed_errorを両方保存して全一致を要求する。別例外や上流parse失敗を目的拒否として数えない。

| case | helper | cycle_batch:の後の登録label |
|---|---|---|
| missing-v3-in-old16-projection | check_next_parent_roles | next_parent_original_sixteen_projection_and_appended_v4 |
| reuse-v3-local0-for-v4-row0 | check_next_row_namespace | next_parent_row_generation_and_local_zero_namespace |
| inherited225-as-full353 | check_next_ancestry_shape | next_parent_complete353_not_inherited225 |
| drop-zero-scalar-record | check_next_ancestry_records | next_parent_all_ordered_records_including_theta_zero |
| previous-from-v4-start-previous | check_next_previous_target | next_parent_previous_target_is_v4_start_current_target |
| packed-hash-in-plain-target-field | check_saved_batch_target | batch_target_plain_JSON_hash |
| require-colocated-fixed-payload | check_next_fixed_local_names | next_parent_fixed_reference_has_only_manifest_locally |

新第四群はfull1706算術fixtureでもfull353歴史意味fixtureでもない。225の宣言opaque配列＋128の宣言ten-key metadataは順序/長さ/零recordの境界を調べる。ROOT/batch-parent-v4/<case>/positive.json・negative.jsonの14fileとgroup case-ledger.json、全dir/partialを保存する。wrapperが実body・descriptor・登録labelを結べる exact schema/fields/pathは公開追補に全文保存した。

F9. 公開・材料の入口は以下の通り。P/WFへ共有したのはこの公開表だけで、Cの新算術本文は共有していない。

| 文書 | bytes | SHA256 |
|---|---:|---|
| Task1078（public-inputs/task1078.md） | 4921 | 60c0cff2bf3a891fd5416b8bacc7b7a8c81657c29c460aaca5ec57bfacda858c |
| 共通Task1077（public-inputs/task1077-shared.md） | 7436 | 9f2525bbb942cce4b6e11c1ea1f5c7cdd81854e94f172f9deef6c39376a2f8fe |
| 公開Task1077 interface-v1 | 19814 | 928b611d79521701438dd4ed4879ba6ca522166548f9e9a153537a8079a97a95 |
| interface-c-v1.md | 4770 | daddfec7485cd9dadbe5bbdc3624f5665e8567a54627b9e20c91ff8e19e16744 |
| interface-c-v2.md（第四群のexact保存型） | 7269 | 16596691568b0a510c815d79026a194da59dc03f2573aa469a24129af5ecd192 |

material-indexは自分と本返信を除く28fileの全bytes/SHAを記録し、途中draft/挿入blockを現在sourceから区別する。実v4の37 entry pin表、取得票720/c377a2ed…、自己C3/C4、全差分・保持票・静的編集計測票を含む。root暫定票1368/9ffc5c17…は11648file/1308094050B、宣言38 empty dir復元後3525dirとcanonical files SHA ffec515b…/dirs SHA f9562484…を通知しているが、最終全受領未完のためsource定数へ入れていない。取得時3487dirだけで最終EOFを代用もしない。

共有TCB4の既存境界は、P/Cそれぞれの vectorized_projection_chunk / sparse_adjoint の登録rawを含む。current_run_call_coverage=NOT_MEASURED、kernel_third_independence_claimed=false、retained_TCB_independence_reproved=falseを保持する。自系旧raw一致や本静的草案を、第三独立数値系やLeanのverifiedへ昇格させない。

F10. rootは固定review snapshot/全raw差分/全区間indexを受領して別読に着手できる。作者側は上記source/公開表/材料をguard closedの静的草案としてfreezeした。現自己静読の追加required findingは0、新実行/canary結果/新oracle/新採用数/時間は未観測。正式inventoryを含むbinding、root/別読の最終判定、具体的な配置/発射は別工程であり、未受領値を補完せずに今回の草案納品を閉じる。

AUDIT_1078_VERDICT: IMPLEMENTATION_DRAFT_COMPLETE_INVENTORY_GUARD_CLOSED; SELF_STATIC_REVIEW_COMPLETE; C5_UNEXECUTED; NEW_FOURTH_METADATA_GROUP_7_NOT_RUN; ALL_OLD_C_LOADER_RAW_RETAINED; CURRENT_TCB_CALL_COVERAGE_NOT_MEASURED; NO_THIRD_INDEPENDENCE_OR_VERIFIED_CLAIM.

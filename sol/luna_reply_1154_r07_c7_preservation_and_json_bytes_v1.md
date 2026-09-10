Task1154 の未実行 C7 計器版を納品する。採択済み自己1152 source 519466 B / 22a9f414969067cd5eefd53ada8811b7e587e5b5fc42a13a22c5606ac77c972f を保存し、終了時 AcceptedInputs.unchanged の実 caller 時間と、保存4親の通常 parser に渡した実 raw bytes を別診断へ追加した。正本は本便の公開抽出指示だけとし、P private 引用を含む原追補 note/source は開いていない。数学 source の import・AST・compile・実行・selftest、P private 読取、Git/GHA/network/credential、新 agent、実行 process 操作は行っていない。

材料はすべて `C:\Users\81905\AppData\Local\Temp\shadow-atelier-audit163\task1154` に CreateNew。正本 `draft-v1/search/check_d972_r07_fixed_lambda_cycle_batch_v7.py` は525249 B / 62e35780184632b9e98a0ff7fcd4652fef952a7c5c33d08b0efcb731e9793035、6979 LF / 0 CR、1152から5783 Bの増分。公開設計7217 B / 256a1e43eca8b2c10db0f419b7c37edc3a94f90c8c06415a77a2ce6e0978a707 は root 全文別読 bcd2e2 で静的設計として採択された。最終 manifest は自己を除く18材料・1750814 Bを登録する。

| 材料 | bytes | SHA-256 |
| --- | ---: | --- |
| public-preservation-and-json-bytes-contract-v1.json | 22623 | bbb0149c8063ae932a10fbc4ba5e47564692d44ab1bbb20b1443c4090f48eb2b |
| all-current-raw-regions-v1.json | 162971 | 37c876a95bdc5b2287b9fb80a988635010e42c8a3e8ca1b5dd09268b775df02f |
| retained24-old-events-methods-and-selftests-v1.json | 36264 | 8133eb4ba53c839fa548b312e9c351279137a0e6663b388685414177c518b3a4 |
| full-raw-forward-reverse-delta-v1.json | 17501 | d5c660b4e676ee86297d6335529bf0afc3d13acbcf1aec5f31f684ecf0d05a2a |
| all-consumer-inheritance-and-private-delta-v1.json | 748176 | 9f6e7f835249e933a61bfc09dd418161ebd8a343f77294ab3b7dad5af5042b93 |
| public-consumer-inheritance-and-delta-v1.json | 57666 | 8ea424502e4921cac6a81b2eac40eafbd10d7d86d4be32eddf692f114fceb071 |
| author-static-completion-v1.json | 3247 | 1b9f429c89019d6713d3a0fe23b389164aa830f1e6f0d3b552485c49c7e4a532 |
| final-material-manifest-v1.json | 5533 | 06615bf557231d1dadfc0c031d69722f7efb19004ca48bdb0ced31a2411579a5 |

終了時の新 event は `d972.r07.input-preservation-timing.v1` exact11。schema / side / stage / ordinal / status / elapsed_seconds / partial / scope / inclusive_stage / add_to_inclusive_elapsed / measurement_scope を持つ。唯一の実 caller の ordinal1、stage=input-preservation-unchanged とし、bundle.unchanged の後、元 inputs.unchanged の外側で STARTED を出して monotonic を開始する。元の呼出しを1回実行し、戻りまたは例外直後に停止する。印字時間は範囲外。元 method の acceptance raw 比較→sorted code/raw closure 全 hash→current19親の元順序の inventory 再照合は raw 同一で、files.unchanged は元どおりその後にある。

STARTED は elapsed/partial=null、COMPLETE は実秒と partial=null、FAILED は主要 elapsed=null と exact1 partial.elapsed_seconds に途中経過を記す。内側で終了した file/bytes/role 単位は測っていないため完了数を推定しない。元の例外を伝播し、呼出し未到達なら event はない。中断は STARTED のみになり得る。checker-total に包含され、add_to_inclusive_elapsed=false。未測・途中・不足を完了0に補完しない。

parser bytes の新 event は `d972.r07.saved-parent-json-parse-bytes.v1` exact12。schema / side / stage / ordinal / status / rows / partial / measurement_scope / inclusive_stages / add_to_inclusive_elapsed / unmeasured / completion_scope を持つ。main actual 分岐の元 check_actual 1回を覆う明示 instance を check_actual→AcceptedInputs→PinnedTree へ渡す。selftest 分岐では生成しない。PinnedTree.json の元 self.read(name,cap) を1回実行し、その返した同じ bytes object、同じ role/path label、同じ canonical flag を元 json_value へ1回渡す。追加の open/read/parse/stat/hash はない。

対象は batch-parent/v4/v5/v6 の4 role と `output/candidates/[0-9]{6}/reduction/(reduction|physical-literal).json` の全一致のみ。4 role順、それぞれ reduction→physical-literal の8 row。各 row は exact12＝role / document_kind / status と、parse_attempts / parse_input_bytes / successful_parses / successful_parse_bytes / failed_parses / failed_parse_bytes / unique_documents / unique_document_bytes / duplicate_successful_parses の9計数。すべて実 len(raw) と実 parser 呼出しから記帳する。成功は元 json_value の UTF-8・重複/nonfinite・canonical 条件を経て返ったこととし、後続の seal/schema/数学値拒否とは分ける。失敗 parser へ渡した bytes は full input buffer長であり、decoder が消費した offset や部分長を主張しない。

繰返し成功は successful_parses/bytes に毎回加え、初めて成功した(role,path)だけを unique_documents/bytes に加える。unique bytes はその初成功の実 buffer 長であり、宣言 inventory の bytes をコピーしない。これにより文書を一度ずつ数えた実観測量と反復 parse 総仕事量を分ける。途中失敗時の unique は到達済み部分集合であり、中央directory全件の完了 census としない。hashだけの再認証、parser到達前の read/pin失敗、他の role/path、current CandidateFiles、後続seal/schema照合は parse 計数外である。

parse STARTED は rows/partial=null。正常終了時の COMPLETE は8 rowを持ち、試行済み rowは MEASURED と非bool非負9整数、未試行は UNMEASURED と9値すべてnull。FAILED は rows=null、最初の対象parseより前なら partial=null、試行後なら8 rowの途中票とする。途中票の試行済み rowは PARTIAL、parser自身の例外を観測した rowは FAILED、未試行は UNMEASURED/null。後続処理の失敗だけで既に成功したparseを失敗parseへ変更しない。診断単独の COMPLETE を数学 PASS として使わない。

parse 集計の lifetime は main actual/check_actual 全体。既存の対象読取は4保存層の state-restore 内にあり、reduction は1152 ordered-reduction-read-compare にも包含され、physical-literal はその狭い窓の外にある。新たな加算可能経過秒は作らない。P の独立4 native認証窓と同じ範囲だと推測しない。公開票はこの包含と全成功順序を明記する。parse STARTED→全旧eventの元相対順序→bundle.unchanged→preservation STARTED/COMPLETE→files.unchanged→元の最終 boundary/return→parse COMPLETE→元の出力。unchanged失敗なら preservation FAILED→parse FAILED→元main failure event。files.unchanged等で後に失敗した場合は preservation COMPLETE と parse FAILED が両立する。中断・logging lossによる不足は不足のまま扱う。

全194 raw領域を登録した。1152の191領域のうち187は raw同一、変更は AcceptedInputs / PinnedTree / check_actual / main の4領域、新設は補助print helperと2 context の3領域。全差分と変更域の全 before/after body を収録し、正逆全EOF再構成と exact edit record の往復が双方とも元 raw に一致した。C4登録24/unique21、元 emit_parent_timing exact10、OrderedReductionTiming exact16、inventory authenticate/read、AcceptedInputs.unchanged/authenticate_code/anchor_metadata、hash_file/json_value/tree_names、旧6群[28,9,6,7,8,10]とdispatch等8領域を保持した。1152全24材料の fresh pin も一致。数学21 keyset切片と47 native alias reader領域は raw同一で、採択済み票へ結んだ。current19/natives18/17/16/15、算術、四character/full8059、caps/k128/max1/no-refill/分離は変更しない。圧縮実装は範囲外。

全 consumer は7918件。1152の同じ関数・同じraw行から7799件を継承し、新規/変更119件に全raw候補と差分意味を付した。元7809件は7799継承＋10変更として全数対応する。採択済み巨大表を再複製せず、各current ID・旧ID・offset・line・columnのjoinで結んだ。このcompact票から全7918行を復元し、全実raw位置/行/所属関数と全表canonical digestが一致することを照合した。新旧差分7領域の意味を明示し、regexを意味論の証明にしていない。current範囲291件の最終占有行は raw[:end-1].count(LF)+1 で照合した。実施した3 helperは raw編集・typed JSON・hashの静的作業のみ。

root は1154全source差分を91ef39、constructor/callsiteを8526bcで独立別読し追加所見なしと連絡した。最終wire/compact consumer票のroot照合は別工程として進行中。実CV9は1962/8667限定7条で受理済み、fresh lambda1962は未計算、A0 actual0/1、verified=false。offset27777/4のFOURTH_BATCH_INVENTORY_REGISTRATIONと27837/4のCURRENT_PRODUCER_REGISTRATIONは Noneを保持し、実formal5/最終P7 opaque pinの完成handback、最終binding、in-run最終binary selftest/runtimeはroot工程とする。追加の作者承認待ちはない。

AUDIT_1154_VERDICT: STATIC_C7_PRESERVATION_AND_SAME_READ_PARSE_BYTES_DRAFT_COMPLETE; C4_AND_ALL_OLD_EVENTS_RAW_PRESERVED; ALL_CONSUMERS_ACCOUNTED; SOURCE_UNEXECUTED; FORMAL5_P7_NONE.

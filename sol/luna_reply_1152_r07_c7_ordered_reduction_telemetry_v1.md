Task1152 の未実行 C7 計器版を納品する。1148 draft-v2 514513 B / b0a8a2ac769a6a7b53633c063e9281fbfe4e1b049e6bb66bdee2f23db0389a42 から、通常の saved-layer 再認証で読む ordered_reductions の実要素数・経過秒と、既存 parent-inventory の実 hash bytes を追加した。公開設計 6743 B / 7fc538f33ad2eaf8037c51c21ce17fb0248d234f2877542e69d40abb0f06bf91 は root が静的計器設計として全文採択済み（連絡番号376609）。数学 source の import・AST・compile・実行・selftest、P private 読取、Git/GHA/network/credential、新 agent、実行中 process 操作は行っていない。

以下の材料はすべて `C:\Users\81905\AppData\Local\Temp\shadow-atelier-audit163\task1152` 配下に CreateNew で置いた。正本 source は `draft-v1/search/check_d972_r07_fixed_lambda_cycle_batch_v7.py`、519466 B / 22a9f414969067cd5eefd53ada8811b7e587e5b5fc42a13a22c5606ac77c972f、6872 LF / 0 CR。1148 から増分4953 B。最終 material manifest は自己を除く24材料・15309688 B を収録する。

| 材料 | bytes | SHA-256 |
| --- | ---: | --- |
| public-wire-and-telemetry-consumer-contract-v1.json | 32604 | dd3ae6ef76839ee1a790da17a9fc64f132600ab598daba411cda53f414ab7c2d |
| all-current-raw-regions-v1.json | 162256 | 1a901b63549ad9ab7d913b8e3ab2d9c94a89e2e4eeced14ed7b3a212ba7ac998 |
| retained24-and-all-old-raw-v1.json | 46126 | 957ffc30d8e6f230b2f15ec642489139f67db65aa5d913f76a88aedef2340368 |
| full-raw-forward-reverse-delta-v1.json | 34935 | 61761518a0b0f94b2bd079f8e67b757527bfa626dee0f0c8e2a826b07a03f33a |
| public-all-consumer-index-v1.json | 5113584 | 7ba841851a724797b6528c6c6eb03ad1015b46dce1cd632aa1a14031b531c20e |
| all-private-consumer-semantic-classification-v1.json | 5303254 | 76470134df07fd6b0b0577c797ebdccdfe2baa552b8b1319609e19dbde261945 |
| author-static-completion-v1.json | 6488 | 312b57f5ef673de1d234151672527e46ff1538c8df28093a5ea830436f0a214f |
| final-material-manifest-v1.json | 7059 | 0ca3f6a10e76f2d6ab8a39464cb6deaba77c9cea93f586fae55bd313bc8c4ffd |

新 plain stderr event は `d972.r07.ordered-reduction-timing.v1`、exact16（schema / side / stage / role / ordinal / status / documents / ordered_reduction_elements / read_attempts / duplicate_reads / comparison_calls / elapsed_seconds / partial / inclusive_stage / add_to_inclusive_elapsed / measurement_scope）。side=C、stage=ordered-reduction-read-compare。通常の4層に独立 meter を置き、batch-parent/1、batch-parent-v4/2、batch-parent-v5/3、batch-parent-v6/4 を既存 state-restore と対応させる。STARTED の後、保存行の関数から正常に戻れば COMPLETE、例外なら FAILED、観測不能または未 read なら UNAVAILABLE。COMPLETE はこの保存行処理の完了であり、その後の native progress を含む親入場 PASS ではない。

元の native JSON reader を1回だけ呼ぶ境界で、戻った reduction の list-of-dicts を観測し、actual len を0も含め加算する。documents はこの typed array の成功読取回数。重複(role,file)の試行を duplicate_reads に数え、成功した重複読取は documents/elements に再加算する。登録rankからの計数、事後の再parse、比較だけでの読取件数増加はない。既存の直接 ordered-array 比較と expected_reduction の同じ key の比較を両方保持し、それぞれ comparison_calls に記帳する。経過秒は通常の reduction JSON 全体の read・pin・parse・canonical/seal/schema と型観測、および元からある二つの配列比較の、互いに重ならない monotonic 窓の和。expected 配列構築、他の metadata・payload read、native checkpoint/invocation、印字、current 候補算術は範囲外。既存 inclusive state-restore 内に含まれるため add_to_inclusive_elapsed=false とし、二重加算しない。P の独立 exact25 parse/typed-loop/fullspan 契約と同一の窓であるとは主張せず、両者の範囲を driver が保持できる公開票とした。

STARTED は主要6計測値と partial が null。COMPLETE の件数は非bool非負整数、秒は有限非負数、partial=null。FAILED/UNAVAILABLE は主要6値をすべて null とし、読取試行があれば exact6 partial に途中観測値を入れる。未開始・中断・失敗を完了0へ置換しない。例外は元の型・目的 label で伝播し、計器の logging error は数学的な返り値へ置換しない。通常の19 inventory completions、既存 native-metadata、各層 STARTED→COMPLETE→包含 state-restore completion の順序と、途中失敗・中断時の不足 event の扱いを公開票に明記した。

parent-inventory は既存 `d972.r07.parent-timing.v1` exact10 を保持する。PinnedTree.authenticate の先頭で完了計数を None に戻し、実 sorted file/directory roster と登録 roster の元の一致条件を保持する。各 hash_file が返す実 byte 数を元の count/hash 一致確認後に加算し、全 file 走査完了後にだけ files/file_bytes を公開する。hash_file の len(actual binary chunk) 由来の整数であり、未照合の宣言 bytes 合計を採らない。directory は別 roster として比較し、files/bytes に加えない。既存 parent-inventory の monotonic 区間と同じ全走査に結び、失敗 scan は completion を出さない。他の既存 stage の file_bytes は null のまま。後段の入力保持用 authenticate 再走査は、この初回 inventory event の時間に含まれない。

全191連続 raw 領域を登録し、1148 の190領域のうち179は byte 同一、11は metadata 境界変更、新設は OrderedReductionTiming 1 class。11箇所は emit_parent_timing、AcceptedInputs、PinnedTree、4保存行 reader、4 promotion caller。元の read・比較・拒否 label を保持した全差分と、変更領域の全 before/after 本文を別材料へ収録した。forward/reverse の全EOF再構成と author exact-edit record の往復が双方とも元 raw に一致する。C4 4 loader / 20 body、登録24 / unique21 は C4/C5/C6/1148/1152 で全 raw 同一。1148 manifest の34材料も fresh pin が一致し、旧版は保存した。preamble、算術、四 character/full8059、宇宙、caps、k128/no-refill、current19 と native18/17/16/15 の投影は維持した。

全 consumer 列挙は7809候補＝従来9 pattern の7724＋計器の明示属性・call・clock等85。同じ関数の同じ raw 行からの1148継承は7667件で、全191領域に意味と変更範囲を付した。regex 自体を意味論の証明にしていない。数学 public keyset 21 family の切片は同じ関数内で全 raw 一致し、47 native alias と1148の実 public JSON 56材料に基づく意味を保持した。今回これらの数学値を再実行してはいない。

1148 の keyset 行範囲は別の metadata-only 正誤票を納めた。`task1148-current-v7-public-keysets-corrected-v1.json` は61843 B / 6d30ed010c9b28a3b82a1143309751dffba5f00df0d7d316fac203ccc8e207c1、根拠 `task1148-keyset-line-span-erratum-v1.json` は8787 B / 400339dcbdd4d13f25b8be7eaf2ae750da4cf705f2f354083ae55bb295f9c00a。既存 last_line の15件を修正し、fixed の欠落 first/last 1件を補完した。全21件の byte span/keyset/旧 source は変更しない。1152 では end-exclusive [offset,end) の最終占有行を raw[:end-1].count(LF)+1 とし、重複掲載を含む current span 689件を照合した。

旧6 selftest 群 [28,9,6,7,8,10] と dispatch を含む8関連 raw 領域は同一。今回は診断計器だけのため新たな数学 selftest 群は追加しない。これは F-v6-4 の設計同一性であり、最終 binary の in-run selftest 実績ではない。実施した helper は build-c7-telemetry-static-v1.py、correct-task1148-keyset-spans-v1.py、build-static-audit-v1.py、finalize-static-materials-v1.py の raw 編集・typed JSON・hash 照合のみで、いずれも数学 source を評価していない。

裁定2244により v6 rank1962/gen8667 は限定7条付き cross-checked として正式受理済みで、v7前件①は充足した。fresh lambda1962 oracle は未計算、A0 actual0/1、verified=false。root から1148の独立静的採択票 23636 B / 6077709ec2305f9687979450963468b36c3023a375f01d710d5dbb50259e9989 と、1152全 source 差分の別読所見なしを受領した。1152の最終 metadata/consumer 票の root 照合は別途進行中。現在の二つの RHS は offset27777/4、27837/4 の None を保持する。実 formal5 と最終独立 P7 opaque descriptor は root の完成 handback 後にのみ結ぶ。今回の未実行 draft に guessed pin や追加の作者承認 gate は置かない。

AUDIT_1152_VERDICT: STATIC_C7_TELEMETRY_DRAFT_COMPLETE; C4_RAW_AND_OLD_MATH_PRESERVED; ACTUAL_READ_AND_HASH_OBSERVATION_WIRED; TASK1148_METADATA_ERRATUM_DELIVERED; SOURCE_UNEXECUTED; FORMAL5_P7_BINDINGS_NONE.

# Task1040 — k128前置長実験と算術試験継承・共有TCBの公開受領証

公開1035への追加契約。司令塔commit fe85a6e9b758152796178ccc6ed36ce73c1adf97、裁定2175–2176、正本docs/notes/fixed_lambda_batch_v2_cv9_reading_v1.md（48988 B/5b28ec642315e8453926aae7a935911a74a669f374ad2ea2390371270a34da91）をroot全文読了した。k64/run34011731149のrank1514/gen8219は工房cross-checked限定9条で受理済み。新128の初期状態は依然1035の同旧64/run33990567016・rank1450/gen8155・同15親である。

## 数学的読み方

量は固定lambda_1450・固定failed roster・固定消去順の前置長nにおける累積独立数a(n)。既知a(32)=32、a(64)=64、a(128)は未観測。処理を分割しても同じ値という主張は同じ初期span・lambda・候補順を保存する条件の下であり、通常CEGARのlambda更新を挟む別選択を同じ実験としない。今回fresh k128は同一前置64の再現も含む費用比較であり、64/64をbatchサイズの独立性維持効果と表現しない。

正本§4.2/§10の物理行比較は6本の抽出だった。rootは旧v1/run34004423047とv2/run34011731149のoutput/rows/000000..000031/physical-normalized.bin全32組を全bytes/SHAで比較し、32/32一致を追加した（TEMP batch-v1-v2-first32-row-file-identity-v1.json 9068 B/c1061ceb95e54e27c254212741a72a91b4dabc46d08547cbc767bcc0e803fb51）。これはfile identity metadataで、行の算術再演ではない。版束縛のowner/HEAD/manifestの同一性は主張しない。

正本の『aux枝も新selftestに無い』は訂正対象。P v2:3217のauxiliary-only、C v2:2476のfirst-auxiliary/second-auxiliaryが新第二群にあり、実二群PASSへ接続されている。本番aux=[0,0]で未発火という限定と区別する。DEPENDENT本番0回・v2新二群未通過の限定は維持する。固定費の2点fit/k≈436や日数は条件付き外挿で、今回の登録capや実測値にしない。

## 追加する二受領証（旧source/WF/実artifactを書換えない）

新WF3のREPORTへ `arithmetic-selftest-inheritance.json` と `shared-tcb.json` を追加し、run-receiptに各全file pinを載せる。statusはSTATIC_INHERITANCE_REFERENCE / DECLARED_SHARED_TCBなど受領証固有型とし、新実行で旧数学suiteを実行したPASSや完全独立性へ読み替えない。三assuranceはfalse。新P/C本体・acceptanceの既存exact型は変更しない。現実行sourceは保持19＋新P/C二本＋raw3の全24のまま。全REPORTの明示二除外・全fixture保存はそのままで、二新票も全inventoryに含む。

算術試験継承票は `arithmetic_selftest_inherited_from: d972-r07-fixed-lambda-cycle-batch-v1`、旧実run34004423047/1、head81a1b22975308ae0ac628f97da447a008a1d087e、artifact9980697123/94677901 B/d21f9e0b93b070327b4ef02e975dc377a8020e7f8aa7553a720d97d690ed85f0、旧P自己試験2409 B/1bfb8b4404d1d24e481dd139b6b84136ef21e8e79b1fd3548607a66b45d1c238、旧C自己試験1725 B/2c8005f98883a711bece270552fa5f39f85755a8d06a27f0cf6c1b3fc257cdceを明記する。旧三群はfixed-selection-full-roster-and-aux / dependent-independent-target-signs-and-packed / private-prefix-publication-resume-and-isolation、実拒否P7/6/26・C2/3/14、前便でroot全payload読了済み。参照根拠を再実行扱いせず、old_mathematical_suites_rerun=0、historical_payload_reacquired_in_this_run=falseとする。

継承の根拠には**全基点source pinと現source pin、不変と認める実行本文の両版行範囲・全raw bytes/SHA**を載せる。Task1042の独立静的監査が実値を公開するまで架空pinを埋めない。行は1始まり・両端を含み、raw UTF-8 LF bytesの連結をhashする。Pの数学bodyはWORKFLOW literalだけの差、Cのv1→v2には切出し/締めgateがあるため、全C本文が同一とは書かない。変更領域は全差分の静的監査と新二群の対象として別に記録し、等値が得られない領域に無条件継承を主張しない。正規化する場合は除外行の元bytes/新bytes/理由を固定し、その除外以外のbyte一致を必須にする。一般ASTやparser、新算術は不要。

新WFは登録されたregionの全bytes/SHAを現在のcheckoutで照合する。歴史sourceを新たに読み込む場合は実行/importしないことを明示し、全fileをREPORT内のaudit-history-sourcesへそのまま保存する。これは非実行の証拠資料であり21実行Python/3rawや15数学親へ加えない。歴史artifactを新数学親として追加しない。自己試験payloadは上記の歴史pinへの参照であり、このrunで再取得・再実行したと偽装しない。

## 共有TCB票

返信163 F8.89と裁定2173をそのまま継承する。以下を全file pinsと両関数の明示範囲へ結び、P/C独立実装の除外項目としてrun単独で読める形にする。

| kernel/系 | source | bytes | SHA256 | 行 |
|---|---|---:|---|---|
| vectorized_projection_chunk/P | search/d972_r07_actual_grade2_root_scalar_batch_v2.py | 118315 | 3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856 | 342–357 |
| vectorized_projection_chunk/C | search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py | 119619 | e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6 | 269–284 |
| sparse_adjoint/P | search/d972_r07_targeted_grade2_owner_generated_join_v15.py | 126565 | 76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632 | 192–203 |
| sparse_adjoint/C | search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py | 141770 | 8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662 | 192–203 |

vectorized_projection_chunkは旧P full_origin_refinement_v1:448/C complete_oracle_cegar_continuation_v2:236のP1経路で荷重を持つ。sparse_adjointの今回実呼出行は第三CV9で特定されていない。新runで別に計測していないcall coverageを立てず、current_run_call_coverage=NOT_MEASURED、kernel_third_independence_claimed=falseを維持する。旧docstringのIndependentという語を根拠に独立性を再昇格しない。

## 公開前条件

1038のk64 metadata受領修理、1042新source全差分/継承region監査、1041新WF全静読と別WF監査を経てrootだけが公開/GHAを行う。正語の1039/1034受領は並行する別課題である。rootの局所metadata PASS、工房CV9、実GHA工程、数学/Lean保証を分ける。A0 actual0/1・階段1/6・grade2 NOT_DECIDED・verified=falseは不変。

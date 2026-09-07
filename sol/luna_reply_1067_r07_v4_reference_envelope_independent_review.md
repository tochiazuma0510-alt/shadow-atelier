# Task1067 — envelope-v3 / driver_v2 の独立静的別読

F1. 結論は具体案に対する `LIMITED_STATIC_PASS`。Task1067 全文を読み、1064 最終 WF/driver/current registry の全変更範囲と影響する通常呼出し・保存経路を別読した。required finding は 0 件。変更はこの返信と `%TEMP%/shadow-atelier-audit163/task1067/` の metadata 証拠だけである。1064 の作者案、1065 の凍結 P 案、repo payload、旧票・旧 artifact は変更していない。自作 P1065 の意味的独立監査は root へ留保する。C 私的数学本文・私的票は表示・解釈せず、許可された全 file/range の raw hash のみ照合した。source/WF/数学/全 helper の実行、Python/import/AST/compile/GAP、Git/GHA/network/credentials、新 agent は使用していない。

F2. 入場した正本は1064最終返信 14,644 B / SHA256 `74955fea472ab8bb330bd46a1ff862f45857ace714942dbf645f6abf26ce0e8f` と納品台帳 10,274 B / `17fd0e944e1568ad5ecd752f94a160a4cb339b9af5d752d11b04e1a026a55937`。両全文を読了し、18 納品、旧 repo 5、公開 handoff 4、両正本の計29全 file bytes/SHAを最終時にも再照合した。全一致である。registry 正本は `inheritance-registry-v4-reference-v2.json`、236,390 B / `84f5bbc6a85e77915535968e4342c09b6bf3e5b94638ab14184c67ca677ce114`。174,498 B の compact draft は台帳の `INTERMEDIATE_NOT_ADMITTED` のまま、実行登録へ採用していない。

1064 TEMP 基準の exact 5 repo path 案は次のとおり。全件 ASCII、CR 0、BOM 無し、final LF 有り、行末空白0を別に数えた。

| repo path | bytes | SHA256 | LF |
| --- | ---: | --- | ---: |
| `search/d972_r07_fixed_lambda_cycle_batch_v4.py` | 290457 | `a58f7c116558fdc430025a9e095d29d0b04e0f20c9295264fca58a4c13510d0a` | 4507 |
| `ops/source_versions/d972-r07-fixed-lambda-cycle-batch-v4-before-reference-repair.py` | 284974 | `3ba71767585b6a49efccb5d20bb60eb8939848669c19692a63018b9486f41d36` | 4426 |
| `search/d972_r07_fixed_lambda_cycle_batch_v4_workflow_driver_v2.py` | 536145 | `35f73f5d1b8b519a69773690db8f8e514b3cc1d2792cc595ecdc0b92dede7a0c` | 5807 |
| `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v4.yml` | 22153 | `56a8349fd54b16d63da9de2c4762ed04328ef1373f65af45c46019e745a1859b` | 368 |
| `ops/workflow_versions/d972-r07-fixed-lambda-cycle-batch-v4-envelope-v2.yml` | 20296 | `c8dc698160b41a21e338cc5a099f4e4abb51a369247a48fbfbd17c907dd02623` | 351 |

旧 P archive は現 repo P の全 raw、旧小 WF archive は現 repo active WF の全 raw とそれぞれ同一。保持 C4 は 261,170 B / `a29380ec00876225cc618c7025d671a3da79aea3b31b829dedba13c59ba84633`、旧巨大 WF archive は 599,085 B / `e22c225a3f8706b648543c260b3ba603f6b6620cdcfadcdf573199b0f4f339f4`、旧 driver は 529,340 B / `22942fcb260d55657be6c80afb3babd768c271ed562127b5ca2f1a0bc033dbae` のまま。具体5pathの配置は本便では行っていない。

F3. driver の全差分を、埋込み registry の全 raw を別認証した上で閉じた。新旧 `INHERITANCE_REGISTRY_RAW` はそれぞれ独立ファイルの全 bytes と同一であり、registry 全差分は F5 の全区間・全字段比較で照合した。残りの全 control 差分を task1067 内で独自に作り全文読了した。独自の column-zero `def`/`class` text partition は旧89・新90で、87区間は全 raw 同一。これは字句境界の file 比較であり、AST/import/コード実行ではない。

全 raw を旧版へ戻す差分は、先頭コメント、埋込み current registry 全文、その全 pin、`public_audit_registry` の schema/task 2 literal、追加 `batch_fixed_reference` 全84行、`authenticate_batch_parent` の fixed caller 1行だけである。この6箇所を metadata 上で逆置換した全 bytes は、旧 driver 529,340 B / `22942fcb260d55657be6c80afb3babd768c271ed562127b5ca2f1a0bc033dbae` と完全同一。従って一般 `batch_saved_manifest`、既存親入場、code/runtime契約、三群 gate、全 P/C 実行・最終判定・通常保存経路に未列挙の本文変更はない。新専用84行は補助ファイル 6,323 B / `394826247ff97118548a64ca20d3ebc4ebd3eaeee3ab14722a8d377fab29b55b` と末尾の空行を含む全 raw 同一である。

F4. R4 の fixed 参照修理を、専用 reader L3767–3850、一般 reader L3748–3764、caller L3966、型/JSON/seal/path/hash/scan utility と原64 anchor・16親 root 解決・7key acceptance の実呼出しから読了した。新 reader は `paths['batch-parent']` の参照 manifest と、登録済み `paths['continuation']` の実 payload だけを結ぶ。root/output/fixed の実 directory・非symlink・包含を確認し、任意の別 path や架空 payload を受け入れる入口はない。

実親 `output/fixed/manifest.json` は 2,903 B / `ba4d2d96b562abc1c460a95e562eb88069837cf102874a6cb99bcefe27c42304`、**exact 9 keys**、同 directory の全 file は manifest 1件だけ。参照された原64の manifest は 3,159 B / `3ec178df5c2af9de7c55bb96075bb9e741111a241f7e02222ef5604587c87c41`、**exact 8 keys** であり、原64側だけに16 payload＋manifestの17 filesが実在する。前者の `accepted_fixed_manifest` は後者の plain3key 全file pinと同一。原64の `scope` は原64 owner の scope と同一で、原64の owner/source、親 batch の owner/source/start の全実file SHAへ各字段が一致する。

両 manifest の geometry 参照は実 oracle `output/geometry/manifest.json`、1,808 B / `7365fa98bd0a7dc6461c076de2434ab13f980a3acbe78c30dbd24ef14b098acd` に一致する。両 fixed manifest、geometry、原64 owner の保存 raw から自身の一意な seal 字段だけを除いた hash も一致した。実 canonical bytes の強制は通常 `sealed` → `read(...,True)` のまま維持されている。

16名の順序を固定し、旧 descriptor はすべて `file/bytes/sha256/dtype/shape` の5key。JSON5名は `dtype='json', shape=null` を確認して3keyへ射影し、binary11名は `u8/u32le` と bool を除く正の普通整数 shape、幅×shape と bytes の一致を保つ。全16 payload **10,304,823 B** を実 file から全EOF/SHAで照合し、全 descriptor、manifestのみの親 directory、原64の全17 fileと subdirectory無しまで一致した。一般 payload readerの同居file要求は緩めず、親 fixed へ payload を作成・コピーしない。

`batch-fixed-reference-receipt.json` は全参照照合後だけ `save` の `open('xb')` で形成する plain receipt である。reference/accepted_fixed_manifest/geometryの全pin、両 inventory、5/11件、非コピー・非source実行・false assurance を保存する。後の `execute('producer')` が REPORT 全 scan を `intake-controls-before.json` へ保存するため、この新票の全bytes/hashも本P開始前の control baseline に含まれる。`preserve` がその全file不変を照合し、最終 REPORT inventoryにも収録する。新しい単独 seal を備えた票であるとは読まない。

F5. current registry の schema は `.audit-registry.v2`、ordinary task は1064で、driver は全 raw pinを先に確認した後、この型と schema を受け入れる。旧歴史 registry 76,867 B / `9fe3d9cf1449c3535618a8c7618c6ab6e5fa4426f0f902c419fbbf91ad873b38` の保持、source順 P1/P2/P3/C1/C2/C3/P4/C4、8 loader順、P/C transition順も確認した。

全新旧 metadata 差分は schema/task、P4 source descriptor、P current transition、挿入後に移動した3つの P old-loader current行範囲へ限られる。P4登録は1065の公開 handoff v2の source・transition・P loader全辞書と同一。旧 current-registry から見た P区間の raw 変更は、追加 `batch_fixed_reference_manifest` と既存 `authenticate_batch_parent` だけで、その他の変化は ordinal/行範囲の移動である。P旧 `authenticate_anchor_metadata` は位置も不変、残る旧3loaderは81行移動しただけで bytes/SHA は不変。C source/transition/context、旧7 source、歴史 registry/継承票、新source audit scope、共有TCB metadataには変更がない。

独自に実8 source全 raw、current全472範囲、254分類を照合した。C raw は byte offset/LF/SHAだけを扱い、私的数学本文を表示していない。

| 系 | baseline範囲 | current範囲 | EXACT_RAW_BYTES_UNCHANGED | REGISTERED_CHANGED_RAW_BYTES | ADDED_CURRENT |
| --- | ---: | ---: | ---: | ---: | ---: |
| P | 122 | 137 | 104 | 18 | 15 |
| C | 96 | 117 | 79 | 17 | 21 |

全 source の LF partition に欠落・重複はなく、比較は全 baseline/current ordinal の一対一対応を覆う。歴史60範囲も実6 sourceの全LFを覆い、9不変群の各三版は全 raw 同一、2除外literal群の各三版も公開 literal全 bytesへ一致する。残る9変更群は「三版 raw 同一」に混ぜていない。旧8 loaderの前後16範囲は全 raw 同一である。

共有TCB4件は全 source pinと各 raw range pinを別に再照合した。`vectorized_projection_chunk` の P/C各範囲と `sparse_adjoint` の P/C各範囲が全登録値に一致する。共有であること、第三独立性を主張しないこと、`current_run_call_coverage='NOT_MEASURED'` を保持する。これらの raw 同一性は今回の数学実行、呼出しcoverage、新parentでの全算術成功、P1065の意味的独立監査を代行しない。

F6. 小WFの全368行・全外枠差分を読了した。active path は固定 v4.yml を保ち、branch は `sol/r07-explicit-lift-20260825`、push marker は `[r07-fixed-lambda-cycle-batch-v4-envelope-v3-run]`、checkout は `github.sha`、credentials保持は false。新P pin、新driver_v2 path/pin、保持C pin、history-v1保持、history-v2追加が具体案に一致する。全16親 env の連続 raw と CHECKER/runtime/WF env の raw は旧小WFから不変。batch128/max_batches1/fresh/no-refill、P5400秒/C10800秒/7168MiB/job330分、metadata16・P[30,10,6]・C[28,9,6]、数学2群＋親metadata1群の意味を保持している。上限であり、所要時間や結果の予測ではない。

bootstrap L171–228の58行は 3,901 B / `ad50b80591e82fc0d73df591fca59d73989d67ccf01e54e6f2aeee799520dd84`、recheck L308–345の38行は 2,778 B / `a2c86b2d148faa8096489e4bbeba957ff6103473e127046f93f63cbf366083a8`。YAML indent10 spacesだけを除いた本文は各補助 shell と末尾LFまで完全同一。両 shell を実行せず全文静読した。WF本体22,153 Bは登録された500,000 B未満である。

bootstrap は fresh REPORT/INPUTS、path種別/非symlink、実workflow ref、driverとhistory各全bytes/SHA、noclobber全rawコピー、コピー後同じ全pinsと`cmp`を確認してから成功する。前後の7file集合は、checkout driver / REPORT driver、旧巨大WF / REPORT history-v1、旧小WF / REPORT history-v2、active WF。P旧archiveはこの7file runtime集合に追加されない。後段でも同7fileの全SHA表を再生成し、before/after全表を`cmp`する。新P archiveの役割は非実行の旧source保全である。

F7. bootstrap 失敗後は通常success条件の source/live/intake/selftest/Pを実行せず、always系のbaseline/checker/fixtures/preserve/envelope/finalも明示 `steps.bootstrap.outcome == 'success'` で制限する。未認証driverをalwaysで実行する迂回はない。全diagnostics uploadだけは alwaysで残る。recheckには`continue-on-error`を付けず、失敗するとjob failureとなり、finalはenvelope success条件で実行されず、candidate uploadにも到達しない。

入場の `parent-files-before.json` と解決rootは親metadata判定の前に保存する。fixed参照で失敗した場合、7key acceptanceや `batch-parent-envelope-intake.json` の完成を偽って形成せず、driver failureはFAILとなる。後続段階が無い時は、final receipt のresult/checker/current/五execution等は実在に応じてnullを保ち、missingをPASSへ補わない。形成済みfixed-reference票だけがある場合もそれはfixed照合の局所票であり、batch全体の受理成功ではない。preservationは既取得全親/輸送/部分復元を保存し、errorsはFAIL、missingはINCOMPLETE、全条件が閉じた場合のみPASSとする。

通常 final gate は旧本文の全 raw を保持する。全5 execution、P/C同じ保存payload、三phaseと候補phase/decision/row、実 checkpoint/HEAD/result、独立・依存件数、旧225祖先＋実採用新row、全入力/source/fixture/出力の不変を結ぶ。新lambda oracleは未計算のnullを維持し、Linearなら型付きnullとpositive adapter pendingを保持する。外側workflowのsuccessだけで新candidateや正語を主張する経路はない。

F8. 独自機械票はすべて `%TEMP%/shadow-atelier-audit163/task1067/`。PowerShell/.NETによる file・JSON・raw range/hash の metadata 操作だけで作成した。

| evidence | bytes | SHA256 |
| --- | ---: | --- |
| `initial-full-pin-audit-v1.json` | 11554 | `fd8fbfed46f1c7cd5853b11363b53605b763d9b80aba93b68224008ded86cd37` |
| `independent-registry-raw-audit-v1.json` | 421164 | `6add4df21300c7d5896fe50d0f4c96aba6ab5da3114e5b8698337d848d4f822e` |
| `driver-envelope-and-TCB-raw-audit-v1.json` | 45921 | `04410528d44bf105d687f660e794bc8ad73abb49d848715048b36830644ef39b` |
| `actual-fixed-reference-full-metadata-v1.json` | 43510 | `fb3f6c1ca53fc362dc634e494fc2019ada5b6da2ce6a865f0de7dc4d5a83ee8e` |
| `driver-control-full-difference-v1.txt` | 17487 | `f7351d4750db5d1b6b6c96e53353ba93e2f301e9ba8bbe52bfa4c67ee97758f3` |
| `final-static-review-input-and-evidence-v1.json` | 22561 | `c8b569dc66af945a4e680bcf7fcc27ece31eb97b2d7960efa25e0333f7aaa71c` |

初期票の未完成flag、registry単独票のTCB実範囲pendingは当時の保存状態として維持した。TCB実4範囲は後続 `driver-envelope-and-TCB-raw-audit-v1.json` で閉じ、最終票は両票を全pinで結んでいる。registry rawを参照に置き換えた新旧比較用textも保存し、その全pinは最終票へ収録した。作者提供の全raw差分ファイルは全pinで保持し、独自の全構造差分・全control差分・全raw逆置換を監査根拠にした。

F9. 2192 の一回は既に失敗run `34040070261/1`、commit `4290ed7c947a9dacdb132209f247f18ef8dae6d9` で消費済み。本便は2195が待つ具体5path/current registry/独立別読の静的範囲を閉じる。今回案の新P/C/selftests/GHAは未実行であり、新run/artifact/candidate/CV9/verifiedは宣言しない。rootによる自作Pの意味別読と具体再承認、repo配置・実行は本票の外側に残る。指定案へ追加required修理はない。この最終返信と上記証拠を凍結する。

AUDIT_1067_VERDICT: LIMITED_STATIC_PASS

Task955 — full-origin refinement の独立 checker と workflow。Task955、Task954、reply953 を全文読み、指定された3ファイルだけを作成した。Task954 worker との共有は公開 CLI・JSON/配列 ABI・入力 pin・literal の型だけであり、新しい算術実装は共有・参照していない。

F1. `search/check_d972_r07_full_origin_refinement_v1.py` は実装完了。source freeze は 75083 bytes、SHA256 `1ee388c9cd39a43992bc9a6e075b087da3ae1672221a197719ea435d7d3529c2`、LF1154、CR0、BOMなし、最終LF。Task956 はこの SHA の finite27、本物の selected actor 接続、全 scan/step replay、CLI/canary と、最終 producer SHA `d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa` の尾部まで静的に読み、`PASS_STATIC_SOURCE` と裁定した。root も最終判定を全文読み、下記3 source/workflow pins を独立確認した。実走は別ゲートである。

F2. 新しい開始点は Task954 の受理済み run33964709359/attempt1、commit `fff114c41bd8748ad0e708919fe0820335c9cce8`、artifact9969090590、1855391 bytes、ZIP SHA `b15b07150d23a1a291fff387f23c8c13cf3ab5ada2b5f95f2a886b0bdf44a428`。指定 TEMP の実物を PowerShell の JSON/byte/hash 読みだけで調べた。

rank1359、generation8064、state head `7b7380a7ddb785910347df14f47ba4634cc5fa2fff7c32b722455a824d6cddda`、lambda SHA `60ac649575400e98881c5de5d4ef2c6202d3cf577da1411042104254edb004e2`、target SHA `0a466426db600e191e9ee5563066dbb729492ab74d869dbf0ceeadc2b2f7f686` を固定した。Task954 の7つの小 entry pin を全て code に保持し、packet manifest 以下の全ファイルと、HEAD が参照する正確な3ステップの全 payload を追う。

root から裁定2125により、この旧 fixed44 v2 実走を限定付き cross-checked とする CV-9 を受領した。旧 terminal の declared176 は informative44 と structural-zero132に分かれる。旧3 target coefficients は `[1,1,0]`。旧 artifact 自身の `cross_checked=false` は保存 bytes のまま読み、新 Task954/955 の未実行候補を cross-checked へ昇格しない。

実物の instruction は `schema=d972.r07.fixed-root-packet-loop.v2.instruction`、`predecessor` と `rolling_sha256` を持ち、汎用 `sha256` seal は持たない。target は `parent_remainder_sha256,remainder_sha256,scalar` の3キーだけの plain object。step manifest の内側 seal と、次 manifest/HEAD が指す完全JSONの SHA は区別した。受理済み3ステップの target scalar は順に1,1,0で、最後の0を拒否しない。3ステップは seed35/36/37 に結ばれる。

本番 checker は旧自系 v2 loader で base1354＋seed30＋seed34 を読む。その開始JSONを保存済み packet start と比較し、追加3 normalized rows を実物から読み、三角条件を確認する。現在 lambda を全1359行と認証済み target に直接当てる。旧 fixed44 packet の source/P1 再構成、旧3挿入の再計算、旧 target 算術の再生はしない。これらは名前と hash を持つ受理済み算術前提である。

F3. 登録宇宙は各 character の44 seed、続いて8059 basis×actors `(1,-1,2,-2)`、各32280 origin、全129120 origin。cap32 は運用上限であって総数学的上限ではない。

新しい各 scan で全4 `B*lambda` と16 homogeneous actor children を実物 Task712 の表から求める。P1 cache は256行 chunk で一巡し、各 active character について root＋4 children の scalar 配列を作る。canonical P1 instructions の全 rolling chain は初回の metadata index で認証する。旧 lambda、character0 固定、旧504 orbit、旧 seed2 scalar の assertion は持ち込まない。

seed の値は受理済み fixed44 packet と現在 q の pairing。actor 値には corrected v541 `K_t b_i` の lower 寄与、homogeneous `T2,t z_i`、全 ActRed subtraction が入る。checker の driver は active characters をまとめ、prepare を処理後に解放してから new block を一つずつ読む。大きな Task554 body は同時に一つ。巨大な decoded P1 matrix を保持しない。

scan directory の root、children、seed44、actor8059×4、P1 5×8059、actor-lower8059×4 を全4 character 分すべて再構成し、完全 byte 比較する。first hit 前で照合を止めない。first hit は character-major、seed0..43、basis0..8058、actor slot0..3 の順。零 character の明示的零ファイルも比較する。

公開 scan の `lower_pass` は producer が宣言する各 active character ごとの5body/12blobという schedule に一致させる。checker 出力の `scan_io` は独立に実際の batched I/O を記録し、activeがあれば5body/12blob、なければ0とする。stored129120、実際に contracted した origin 数 `32280*active_count`、構造零による省略数を区別する。

F4. 選ばれた actor の本体を計算する `finite27_actor` が、今回の新しい独立 anchor である。元の polynomial forward actor `_checker_seed_act` を呼ばず、producer の polynomial multiply/pull を参照・複製しない。

accepted group/index と六 tag の actor affine image を前提として、10個の次数≤2 monomial `(E_i-1)^mu` を27個の ordinary group coefficients に展開する。全4 Fourier character を parity に戻し、section-left/kernel-right の左積で kernel index `k -> k+sign(e)*k_actor`、PSL index `g -> p_actor*g`、parity `e -> e+e_actor` を置換する。`product binom(k_i,mu_i)` で10成分を抽出して Fourier に戻す。逆変換の係数は F3 で4=1なので1。共有8 aux はコピーする。

この処理は実際に選ばれた完全 `(d0,d1,d2,aux)` canonical lift に直接適用する。全4 top の homogeneous 成分との差から lower-to-top を取り、選ばれた q による homogeneous/mixed/full scalar を独立 scan の対応値と照合する。その後、実際の順序付き ActRed を集め、同じ係数で完全 lower と top を引き、全96776 lower が零であることを要求する。これが成立してから plain character slice と B を取る。

ActRed は old direct、old-to-new各block、または new-own の実際の保存式を使用する。raw event は係数集約前に rolling seal を付ける。数値的に cancelled した node と direct basis の P1 参照も残す。full source、full actor、homogeneous top、mixed top、full defect、selected source slice、physical row を完全byteのhashで結ぶ。checker 独自の `finite27_actor_anchors` は、その実際の selected actor を計算した記録であり、単なる synthetic demonstration ではない。

literal orientation は `sol/proof_r07_targeted_grade2_direct_relative_literal_compiler_v518.md` §1 の `Act_P(W)=P W P^{-1}`、§2 の actor origin と、実物 P1 instruction の `literal_input_sha256` を合わせて読んだ。accepted v9 source は同じ signed letter の `act_source_word_precision2(parent,(letter,))` を使う。新 literal は `actor_conjugation='t*W*t^-1'`、元 basis の実際の P1 root、ordered raw events、projector、B、source-d を保持する。normalized exponent pair、十一 physical slots、full word replay は完了扱いにしない。

F5. 新 prefix は完全 scan を先に保存し、完全 step を保存してから HEAD が進む契約。checker は各 step の直前 scan を独立に全再計算し、selected source、insertion-order reduction、normalized append、target更新、新 lambda の全行 sweep と両 target の直接 pairing を独立に再生する。最後の cap に達した後の scan も HEAD に保存・認証される。cap1 の最後の scan は同一 output への本物の `--resume` で再利用され、checker はその scan も一度独立再計算する。

HEAD は owner/source/runtime/start/canonical index/accepted packet manifest と current scan、最終 step、rank/generation/state head を結ぶ。六桁 complete directory と明示的 `.pending-*` / `.orphan-*` を区別し、diagnostic tail を complete prefix に数えない。`ROOT_ORIGINS_ZERO` は全4 current roots の登録 origin が零という結果だけで、grade2 NONMEMBER ではない。scan未完了や非零のまま cap/resource に達すれば UNKNOWN。最終 target 零でも MEMBER_CANDIDATE と未完了 literal gate を残す。

`lambda_rho2.mode='derived'` は base、seed30、seed34、packet-step-1/2/3 の6個の manifest/result/target/state-head identity を明示する。base identity、保存delta identity、受理済み packet target identity、新しく実行した target identity を別に記す。元 rho2 は読んでいない。旧 lambda と rho2 の dot を、新 lambda の直接 dot の代用品として使わない。

F6. CLI は旧 parent roots に `--packet-root` と `--candidate-root` を加え、`--max-seconds 1800`、`--parent-layout-selftest`、`--selftest`、任意 `--output <checker JSON>` を持つ。producer は公開 ABI の `--output <directory>`、`--resume`、`--max-appends 0..32` を使う。

actual-parent canary は旧 seed30 flagなし／seed34 true flagと、今回の instruction rolling seal／plain target／3ステップ chain を、実物 parent 上で通す。旧5件に加え、汎用 instruction seal、汎用 target seal、誤ったtarget parent、誤ったstep parent、誤ったfinal headの5件を拒否する。状態の数値再構成は実行しない。

新しい focused canary は3群だけ。有限27元の d0-only と d1-only に実際の Y kernel translation を適用して非零 lower-to-top を要求し、inverse roundtrip と independent adjoint scalar を照合する。全4 character の first-hit/order/cap を調べる。保存scanのfirst-hit外の array tail破損、cached scan付きHEAD、wrong owner seal、次stateでscan referenceを消す契約を調べる。旧成功suiteは起動しない。

F7. `.github/workflows/d972-r07-full-origin-refinement-v1.yml` は旧10 parent tupleをそのまま保持し、今回の packet tuple を追加する。repository/run/attempt/head/workflow/conclusion とartifact ID/name/bytes/digest/expiry/lineageを読んでから正確な親をdownloadし、既存ファイルをコピーせずrootsを解決する。新旧の12 Python executablesと2 raw dataをpinし、PythonにだけAST/LF/BOM条件をかける。`fuda1_a0_rmax_data.g` のCRLF、word JSONの最終LFなしを変更しない。

marker は `[r07-full-origin-refinement-v1-run]`。metadata canary両系＋新しいcanary両系の後、cap1 → 同じoutputへの実際のresume32 → 独立checker。3 phaseは各internal1800秒/outer40分、job130分。before/after receipt は既存の全 step・scan bytesとowner/start/source/canonical-indexを比較する。checker PASS の後だけ candidate upload、diagnostics は全prefix/resource receiptを always upload する。

root はこの workflow の11 parent tuple、retained source/data、actual-parent canary、cap1→resume32→checker、cached scan保存の schedule を読み、一致すると通知した。最終 source pin は次のとおり。producer の SHA/bytes も算術を読まず独立にファイルmetadataで照合した。

| 最終 executable/workflow | bytes | SHA256 |
|---|---:|---|
| search/d972_r07_full_origin_refinement_v1.py | 97806 | d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa |
| search/check_d972_r07_full_origin_refinement_v1.py | 75083 | 1ee388c9cd39a43992bc9a6e075b087da3ae1672221a197719ea435d7d3529c2 |
| .github/workflows/d972-r07-full-origin-refinement-v1.yml | 30907 | 26cdca16acae63b8cf9cf6b865d219d9d57ee75677d017b4b34ba7db9f00b5c1 |

workflowはLF535、CR0、BOMなし、最終LF。Task956最終静的裁定はPASSで、root brokerがreleaseを行う。このworkerはdispatchしない。以上のsourceとworkflowは凍結し、変更しない。

F8. 実行TCBは新checker＋自系固定checker v2（66251 bytes / `5289253a82d942d71b1ec55505d08ab772b111f2ba08e301f67387eae19b23e5`）＋以下の自系4 modules。producerの同世代5 modulesはsource/runtime metadataの照合対象であり、checkerはimportしない。

| 自系 retained module | bytes | SHA256 |
|---|---:|---|
| check_d972_r07_actual_root_seed_materializer_v3.py | 64626 | eca60918eb943edddc321054f04b8547b3e88e5f7421f4de1e09ea04d7ca2701 |
| check_d972_r07_rank1355_root_seed_scalars_v1.py | 36236 | f3c7ca2586a3734334b7d9823316601d18ab1d36561c72aa2c23c2aedfca0e62 |
| check_d972_r07_actual_grade2_root_scalar_batch_v2.py | 119619 | e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6 |
| check_d972_r07_targeted_grade2_owner_generated_join_v15.py | 141770 | 8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662 |

raw data は `scratchpad/fuda1_a0_rmax_data.g` 4709 bytes / `625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba` と `scratchpad/a0_paper_words_v1.json` 115928 bytes / `90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893`。runtimeはworkflowがPython3.13とNumPy2.5.1を用意し、実際の`sys.version`/`numpy.__version__`をproducer source receiptと比較する。

F9. このworkerはPython/GAPの数値実行、AST実行、ネットワーク、credential、git、dispatch、追加agentを一切行っていない。ローカルで行ったのはsource/JSON/byte/hashの読みと、指定3ファイルへの実装・記帳だけ。新run ID/commit SHAは存在せず、root brokerが正式freeze後に記録する。新 Task954/955 の実際のcanary、GHA producer/checker成功、CV-9の数学裁定は未実行。cross_checked=false、verified=false。

AUDIT_955_VERDICT: CHECKER_AND_WORKFLOW_SOURCE_FROZEN; TASK956_PASS_STATIC_SOURCE; ROOT_WORKFLOW_REVIEW_PASSED; ACTUAL_GHA_AND_NEW_CV9_PENDING; GRADE2_NOT_DECIDED.

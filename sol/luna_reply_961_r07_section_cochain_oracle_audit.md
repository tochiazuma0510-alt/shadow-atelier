# Task961 — v548 complete scalar oracle の限定 source 監査

F0. **最終判定は限定した静的監査 PASS。新 oracle の数値実行は未実施。** Task961、Tasks959/960、reply959 の公開 array ABI、正式 reply957 を読み、完成 source、実 completion 親 layout、最終 byte/SHA を確認した。正式な親の受理範囲は裁定2131の七限定（F11）である。本監査で変更するのは本返信のみ。ローカル数値実行、Python import/AST/GAP、network、git、credential、dispatch、実装編集、追加 agent は行っていない。途中で root から別途委嘱された Task962 の workflow/reply は完成・release 済みであり、以後変更しない。workflow と release は root の担当である。F7–F10の途中状態は経過記録で、最終状態は F11–F12 による。

F1. **A–D core と完成した tail を静的に読了。** producer `search/d972_r07_section_cochain_oracle_v1.py` の `geometry_inputs`、`current_section`、`source_cochain`、`complete_tree_test` と、checker `search/check_d972_r07_section_cochain_oracle_v1.py` の対応 core を読んだ。その後、親 loader、出力全 byte 比較、canary、CLI/deadline の完成ブロックも読んだ。checker tail の配置に一件の blocking defect を見つけ、作者による修正を再読して解消を確認した（F7）。最終段階で親 entry roster の8件対10件の公開 ABI 不一致も通知し、10件への整合を確認した（F12）。未解消の source blocker はない。

F2. **geometry/source pullback。** qid は parity→base3 kernel→PSL 最速、正 edge は `2*q+slot` の右積。producer の `RightMaps.at` は actual `perm_mul(psels[p],h_P)` と `S(e_h)k+k_h`、checker は own PSL product table と own affine multiplication を使う。六 tag を正 BFS tree 上で作った後、各 map の全頂点 bijection と全二正 generator edge 等式、0/4 の独立 identity occurrence を要求する。既存の左 `pmap` を successor にしていない。

実 fuda36点置換の pin と三9点 block の exact reconstruction から、section-right k9X=(1,0,0), k9Y=(1,1,1)、rotation-left vX9=(1,0,0), vY9=(8,1,8) に接続する。carry は mod3 reduction 前の整数差を3で割り、最後の二座標は generator exponent。正 BFS の全54432頂点・54431本と全54433 chord を保持する。root sentinel の内部表現差は、公開 u32 payload に変換する完成 tail で確認した。

source score は degree0/1 の kappa を引き、degree2 の四 roots を加え、actual tag/character transport の Fourier 重みで全六 tag を計算する。raw edge の tagged Fox は `phi_j(q)*prefix`、qnorm は右 X と右 XB=Y^-1。aux0..5 の符号は −kappa_aux[j]×Fox x-augmentation、aux6/7 は独立 eta の −kappa_aux[6:8]。nonclosed raw edge に closed-word qnorm を呼ばず、edge augmentation を18で割る処理はない。

F3. **checker の別算術経路は実 edge に接続されている。** `cyclic_difference_moments` は F3[C3^3] の ordinary delta から27個の `(E_i−1)` monomial の係数行列を作り、own Gauss–Jordan inverse の列から十個の degree≤2 moment を抽出する。ordinary 係数の行 v に対して monomial 係数が `v*expansion_inverse` となる向きである。この moment は `source_scores` の全 score を作り、その返値が `raw_edge_cochain` の全108864 edge に使われる。producer の `_seed_e_poly` を再利用した self-comparison ではない。accepted PSL enumeration、tag words/transport、各自の retained input/readout lineage は共通または保持前提として区別する。

F4. **joint kappa。** 新6045行の元 lead 降順を owner ごとに処理して k1 を決め、その後 old2014行の全 d1 companion の dot を引いた beta に対し、width6056 の元 lead を joint d0/shared aux の24200座標へ埋め込んだ降順で kE を解く。canonical row IDs と O/H offset、chi の添字は保存される。normalized pivot1・元 lead より前の零・lead重複なし・free0 を要求し、生成 scale を保存行へ再乗算しない。old aux lead を full96776 行の first_nonzero に置換しない。

両系は最終同一 kappa で全 old lower＋old lifted d1 と全 new d1 の8059 dot を取り直し、chi と一致することを要求する。q と四 character の P1 contractions は current lambda から新たに作り、全8059行の packed cache を EOF/hash まで読む。producer は16行単位の decoded chunk、checker は継承した packed projection により、全 lift decoded matrix を常駐させない。この継承 helper の独立性に関する限定は F11 に明記する。Task554 body は一度に一つで、保存 descriptor は小さい参照として保持する。既存 `_state_descriptor/state_descriptor` と blob reader の引数・返値への接続も source で確認した。

F5. **tree/negative/witness。** 全 tree potentials から全 chord の tau/value を作り、chord ID 昇順の最初の五つの独立 tau を選ぶ。producer の linear solve と checker の matrix inverse の fit は同じ `a*T=r_selected` の向きであり、basis rank不足を零判定にしない。全54433 residual と二 aux を計算し、aux x→aux y→最初の failed chord の順で witness を選ぶ。chord branch は基準五列に対する係数 d を解き、六 cycle の tau零と scalar=residual≠0 を直接照合する。E は `MATERIALIZATION_PENDING`、新 physical row/rank/target を発行しない。

F6. **tail の読了範囲と残る gate。** 薄い accepted-state loader は保存 normalized rows/target/lambda と metadata/chain を読み、元の scan/insert 算術を再実行しない。producer は大きな materialization payload を stream hash 後に捨てる。checker は保存 scan を hash/metadata として認証し、新しい四 roots/P1 contraction は current lambda から計算する。現在 lambda の全保存 physical rows と両 current-target dots、原rho2の明示 DERIVED は別の receipt に保持する。未受理の UNKNOWN checker-result を親の PASS として許可する条件はない。

stage の全配列と JSON を自分の算術結果から再構成し、各 full bytes と余剰 byte、exact roster を比較する tail を確認した。checker は各 stage の不一致を集約し、全 top-level metadata の比較も終えてから PASS を返す。非単調元 lead、左右の非可換積、nonclosed edge の d0/d1/d2/shared eta、後端 chord/偽EOF/六cycle/aux優先の canary は新しい interface を対象とする。producer の協調 deadline は UNKNOWN_RESOURCE diagnostic のみで、未完時の top manifest を作らない。checker も deadline を UNKNOWN_RESOURCE とし、比較未完の PASS を返さない。これらの canary/数値をローカルで実行したとは述べない。

実際の completion candidate の artifact/checker-result 最終 pins と実 layout への接続、確定した両 source の byte/SHA は F10–F12 で確認を終えた。残る新 oracle の actual-parent canary、数値 GHA、独立照合後の裁定は本便の静的 PASS に含めない。先行 source/Conn/canonical P1 の completeness は保持前提であり、本便が第三の全 pipeline を再構築するものではない。新しい grade2 負判定、cross-checked、verified を本便から発行しない。

F7. **見つけた配置 defect と修正確認。** provisional checker 79717 bytes / `f2b92fdbb7f8a617a568fb14de4dc8d0dcccf90b67f8b533165485fb23ad24ba` では、`check_actual` が top manifest 作成後に終わり、全 top roster/bytes 比較と最終 PASS receipt/return が module の `if __name__ == '__main__'`、`raise SystemExit(main())` の後へ置かれていた。関数外 return となる構文上の blocker として作者・root へ直ちに通知した。AST を実行して発見したものではない。

作者の修正版 **80121 bytes / `7ca2351086f01d0434bee6c5f8c67571fdf4975334df7994f9e9a9a908734e0a`** を再 hash し、全 top roster/bytes 比較→errors 拒否→terminal boundary→PASS return が `check_actual` 内、`def rejected` の前へ戻ったことを source で確認した。末尾 `__main__` は `raise SystemExit(main())` のみである。この配置 blocker は解消した。凍結 Task955 の PASS result には generation があり、ResourceStop result にはない点を実 source で読み直し、新 checker の HEAD/result/checker 三者 generation join も確認した。同じ mixed-source canary の四 character、四 parity、k0=0/1/2への拡張も読了し、追加指摘はない。

producer の後続 intake delta は **71572 bytes / `fdacfbfbae8aebe2ff77af2b7f97737a1a5f9044c1852d1234719aaf33afa29c`** の読取時点で、全 step payload を hash 認証しつつ小さな row/target/lambda と instruction/result だけを保持するものだった。generation 三者 join も含めて確認した。両 hash は観測した provisional source の識別であり、親最終 pin を埋めた後の freeze 値ではない。

F8. **親の途中状態の記録（F10–F11で更新済み）。** root と実 diagnostic の metadata 読取により、元 run33967668257/1 は producer が26段/rank1385/generation8090/current scanなしで UNKNOWN_RESOURCE、checker が22段/22scanで UNKNOWN_RESOURCE と分かった。この時点では保存候補の観測であり、受理 rank1359 を更新しなかった。全26段を凍結 checker で照合する別 Task962 は root が run33971897879/1、commit `64475e1dfab1537a38d1b3131971bfed5fc3071c`、job101321767187 として release し、2026-09-05T14:29:18Zから照合した。公開済み Task962 の二ファイルは変更していない。

F9. **completion の完走連絡を受領、実 bytes の読取は待機中。** root より run33971897879/1 が2026-09-05T14:49:51Zに success、全26段/26scanで checker PASS、candidate artifact9971466432との連絡を受けた。これは F8 の「走行中」を更新する。成功 checker-result の実 file pin/TEMP と、両系がそれを接続した最終 source freeze はまだ受領していないため、本監査の final PASS は保留する。CV9 は裁定2129で pending という root の境界も維持する。

checker の後続 memory delta も再読した。全 payload を exact roster/bytes/hash で認証後、小さな normalized/target/lambda/instruction/result を保持し、破棄した materialization/source-d との join は保存した `payload_sha256` を使う。配置修正・generation 三者 join と両立しており、この delta に追加の source 指摘はない。途中の読取 hash を final freeze として扱わない。

F10. **実 completion candidate の schema/entry pins を確認した。** root が回収した `%TEMP%/shadow-atelier-full-origin-completion-run33971897879-candidate-a1` を source/JSON/byte/hash のみで読んだ。artifact tuple は run33971897879/1、head `64475e1dfab1537a38d1b3131971bfed5fc3071c`、id9971466432、name `d972-r07-full-origin-checker-completion-v1-candidate-33971897879-1`、ZIP51943596 bytes / `0d4af3475ca62da1d7436246bd36109d380e0a463a713de1c1e3db69f90c9db8`。ZIP/live tuple と output968 files の不変照合は root の release 証拠を継承し、本便が network/全出力算術を再実行したとはしない。

本便で独立に file length/SHA を確認したものは以下である。

| file | bytes | SHA256 |
|---|---:|---|
| checker-result.json | 57583 | ccb0b3dd225587dde0e08edca5dfa66b1446b7db01091a3e8118c7aeb4ed2e9c |
| source-receipt.json | 2355 | 5d65f4313aaed81f30354cba5c90ead201816f72f15fcd799606ed5feab43f3e |
| completion-run-receipt.json | 1849 | b1c653283593a2fdef835c938bcc0c8502248b53c92d264842a2133bd4561e57 |
| preserved-input.json | 183567 | 746e097f23c78418a3b43754348099a753639fcceac006e4f1d634ad3fb57298 |
| output/HEAD | 921 | 6bf3b4fce6a3f159563c13a9aa50f6478827fbad1af13d820b70359b3b2f5cba |
| output/result.json | 3988 | 04a88c1423f6d99f5e94ded601d20efa5b338ba2b4fae8e9f73023695cd69211 |
| output/start.json | 11011 | 1a709c2853a6d0c239bc31d50ba6e03b0fb4707d93b625d291a487e6d43dc131 |
| output/owner.json | 8432 | c4fd8b27590450d0b73e72efe9d45bf9319e111b5e21d1f3ff0b0ee23910f48c |
| output/source.json | 1139 | 7e99018f58f3f49e371b55e6daab491b71855bb463c8c47cd872dffb57b5774f |
| output/canonical-index.json | 6078393 | 452fe97a9229fa5188493256d1478ead1e684b495bbfed0db03a64f5acf4f00e |
| output/steps/000026/manifest.json | 1932 | 1bfd33af5054a11b8210781146a872e914acb1bd7214b0b945f7e3520b31200c |

actual checker は `d972.r07.full-origin-refinement.v1.checker-result`、status PASS、completed/prefix/scansが各26、rank1385、generation8090、state head `8f6605a28d337cd8541a7eacf6aef78f5a70308a6bb71fd105138803ca623a61`。producer の terminal UNKNOWN_RESOURCE をそのまま保持している。新 checker はこの **成功型には存在する generation** を読む。HEAD の current scan は null、terminal の scan/scan manifest も null。保存 scan は0..25を読み、26の未存在 current scan を要求しない loader と一致する。

step26 の実 target は plain三項 `parent_remainder_sha256/remainder_sha256/scalar`、scalar1。最終 target SHA は `111d12e064b96a6bf579f39a9c9d5e35181560c0403bf0d237bffc924230c0ad`、lambda SHA は `1e720af4a30bac955ab4565366f0242b5c2d43125eb280e241df20976331cdf1`。separator の直接 receipt は1385行、両保存 target dot1、原rho2は別の DERIVED。新 loader の actual schema/chain 接続を再読し、追加の layout defect はない。

source-receipt は frozen producer d7e32aad… / checker1ee388c9… と retained12 sources、二 raw data pins。completion receipt は producer再走0、旧suite0、checker invocation1、内部7200秒、Python3.13.15/NumPy2.5.1、output unchanged、全prefix照合を記録している。実 finite27 actor receipts は mixed-topを含む actual source評価であり、`new_full_word_replay:false` を維持する。これを新 oracleの全edge arithmeticやsame-word MEMBER実行と呼ばない。新しい両 source への final parent pins 接続は F12 で確認した。

F11. **裁定2131と、新しく荷重を持つ継承 primitive の監査。** 正本 `docs/notes/full_origin_v1_cv9_reading_v1.md` と express `ops/express/20260905_fable_astra_full_origin_v1_cv9_grade.md` を全文読み、F9の「CV9 pending」を更新した。親 rank1385 は七限定付き cross-checked である。限定は、(i)26回の rank1359→1385で最終 rank1385 の origin scan は未実施、(ii)各保存 scan の informative32280対 structural96840、(iii)選択26本は character0のactor、全44seedsは各scanで零、(iv)rank増26に対しtarget更新18、scalar零8、(v)packet3段と原rho2のDERIVEDを前提、(vi)physical insertion/normalization/updateの既存pairを継承、(vii)旧scanの独立性欠如と有限27錨の適用範囲、である。ROOT_ORIGINS_ZERO、NONMEMBER、same-word MEMBER、Lean verified は導かない。

特に F-fo-1 の指摘を保持する。旧 `sparse_adjoint` 本文は同一、旧 `vectorized_projection_chunk` は裁定の比較で類似度0.9908であり、旧 scan全域の実独立照合を称せない。有限27の独立算術は選択された26点に接続され、旧全scanへ一般化できない。Task956の先行静的 PASS はこの継承 primitive の独立性欠如を捕捉していなかった。本便で新しい経路を読んだことにより、その過去の欠如が遡及的に解消したとは扱わない。

現在の P1 contraction は次の二経路になっている。producer の `current_roots_and_values`（443–467行）は旧 projection helper を呼ばず、全 trit を unpack した16行の dense 配列から各36288成分の uint32 積を作り、uint64 sumで全4×8059値を作る。checker の `current_roots_and_contractions`（351–378行）は旧 `BASE.vectorized_projection_chunk` を片側で継承し、qの非零座標の byte index/digit slot を作り、256行の packed byte から必要な base3 digit を抽出して uint32 sumを取る。この helper の実本文は `check_d972_r07_actual_grade2_root_scalar_batch_v2.py:269` にある。各積は高々4、和は高々4×36288なのでこの sum幅にも溢れはない。両側とも四 character の全行を新しい current lambda で計算し、全 cache bytes/hash/EOF と全出力値を照合する。従って現在の pair は dense全成分積対 sparse packed抽出という別算術であり、「両側とも旧 clone helper を廃棄した」とは記さない。片側で旧 helper を使うこと自体を新しい blocker にはしない。

新 roots の接続も読んだ。producer は `d972_r07_targeted_grade2_owner_generated_join_v15.py:192` の tripletごとの mod3加算を使い、checker は `check_d972_r07_fixed_root_packet_loop_v2.py:534` の int64 `np.add.at` からmod3を取る。新 oracle は actor child covectors を生成せず、旧clone child算術へ戻る経路を必要としない。kappa の old d1 companion と最終8059等式についても、producer の full unpack/dot と、checker が継承する `checker_stream_dots`（batch_v2:466）の81×81 packed四trit dot表・uint32 sumを区別した。old/new slice helper（同508/521行）の joint d0/shared8、全四d1、characterごとの新d1の切り出しを確認した。これらの streaming helper は全descriptor bytes/hash/EOFを要求する。

F3の ordinary27 moments は今回の全source score/全edgeへ接続されており、旧26点だけの錨とは適用範囲が異なる。accepted input/context、PSL列挙、tag words/transport、基本base3 pack/dot、保持 source/P1/Conn の completeness はなお入力・算術基盤の前提である。新 pair の runtime全配列一致は未観測であり、本便は静的な call graph と算術の相違を確認しただけである。

F12. **最終 delta、freeze、残る gate。** producer最終 `REFINE_FILES` の10件と、checkerが当初保持した8件は `refinement-parent-layout.entry_files` の全byte比較で不一致になるため、作者とrootへ通知した。checkerは completion-run-receipt.json と preserved-input.json の exact二pinsだけを追加した。最終 source の47–58行と `refinement_layout` の sorted全件出力を再読し、F10の実10件と揃ったことを確認した。checkerの最終配置は984–1004行が `check_actual` 内の全top比較→PASS return、1209–1210行が `__main__` のみで、F7の修正は維持されている。HEAD/producer result/成功checker resultの三者 generation8090 joinも維持されている。

両作者の最終申告を受領した後、本便でも実 bytes/SHA/LF/CR/最終改行を読み直した。rootも同じ値とworkflow内のproducer/checker byte/SHA pins一致を独立確認した。workflowのrelease判断そのものはroot担当である。

| final file | bytes | SHA256 | LF / CR |
|---|---:|---|---:|
| search/d972_r07_section_cochain_oracle_v1.py | 73290 | 4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb | 1257 / 0 |
| search/check_d972_r07_section_cochain_oracle_v1.py | 80740 | 2db166400dd819805f36b613993d4622e8365f04339ca7aef0371a28de71c967 | 1210 / 0 |
| .github/workflows/d972-r07-section-cochain-oracle-v1.yml | 29678 | 0877df05ef9ceb97c726d81ef1bd8a44e455782f1b2d4b1c36e1417ccf8d710c | 503 / 0 |

全三ファイルは最終LFあり。以上の完成 source と実親layoutに対し、Task957のA–D契約上の未解消blockerはない。新 oracle の actual-parent canary/GHA/独立照合/裁定は未実施で、Eの選択word/literal物理行へのmaterializationは別consumerとしてpendingである。旧scanを再走・修正せず、未観測のzero、rank、収束、秒数を推定しない。

AUDIT_961_VERDICT: STATIC_SOURCE_PASS — final producer/checker hashes and ten-entry accepted-parent layout confirmed; CV9 2131 seven limits and historical F-fo-1 retained; new oracle runtime and E materialization pending; verified=false.

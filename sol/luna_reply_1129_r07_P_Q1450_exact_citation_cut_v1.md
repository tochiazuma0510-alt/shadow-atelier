# Task1129 — P Q1450 の最小引用境界・現在作用の限定設計

## F1. 結論

Q1450 の数値省略候補を、P6 thin_anchor L3896 に由来する動的呼出しだけの、retained m.dot L346 の単一69 B return 式へ絞った。helper 全体を保存 dictionary へ置換する案は採らない。現行の入力認証、packed decode・shape gate、行非零拒否、二 target の短絡判定、progress/deadline、結果 hash、状態作用を残す条件付き設計である。

これは一つの**字句上の連続区間**であり、Q1450 一問の中で行1450件と二 target の到達した各位置に適用する。実行時間軸上の一つの連続区間として query 全体を飛ばす案ではない。一般の m.dot や全 caller/global binding を変更する意味でもない。既 source は引用を実装しておらず、本便も変更していない。1122 の全16 caller 表の再掲ではなく、C06/U07 のこの一問の具体化を完了した。

具体的 AcceptedClaim、その局所選択・実入力との lifetime binding、現在の再計算件数を引用と区別する公開移行は OPEN。したがって、そのまま配置できる一行最適化や、速度向上・冷保存移行が完成したとは判定しない。本便は v6 の追加 gate 0。

## F2. 実 source の入口と出口

P6 は %TEMP%/shadow-atelier-audit163/task1109/d972_r07_fixed_lambda_cycle_batch_v6.py、453749 B / 75401d4ded04e00187e9a45bfe87603309473a7c6625e6747ecf5c3bf4caa0d7。通常経路は run_actual L5624 → thin_anchor L3896 → m.check_final_separator → この query の各 m.dot。fresh と completed-resume のいずれも、この native admission を通る設計である。P6 normal guard は引続き未開放。

m は search/d972_r07_actual_root_seed_materializer_v3.py、86643 B / 36cc620bdc1b772a4eb4067f7e5b490dab851fb41213c5cd8a5487855207a332。P6→L→e→oracle→refinement/p2→m の実 module 原点を読み、最終的に m.progress が P6.progress へ再束縛されることも確認した。m の元 progress 本文を有効 callback と取り違えない。

| 境界 | offset / bytes / 全 raw SHA256 |
|---|---|
| P6 L3896 の Q1450 call | 259000 / 111 / 48870049fd68a7b62c74ec7bc7c4b39e9c7c00121de0ff54dc5348d8cf377a85 |
| m.dot L341–345 の残す前段 | 13763 / 261 / f6de826a749296c3a9f1b2fb248b76fb83454aeab0f01a4eca14b6ee8728ee4a |
| m.dot L346 の選択式 | 14024 / 69 / 3cb399f0e758542b9368132c3565f9656c2cd1985a4a043ab1a599453f41983a |
| m.check_final_separator L1301–1315 | 66669 / 973 / feea24af7b0f0b86ee7534f16fdd42674c8b07dbf2739f07eaa29a5ad051b993 |

選択式は二つの uint64 一時 cast、dot、mod3、ordinary int 化だけである。前段の np.asarray/reshape と元の shape/trit gate を実行に残す。これは任意入力型を新しい strict dtype 規則へ変える案ではなく、元 codec から来る実 ndarray と元 coercion を保つ。数値 native runtime の内部効果まで Python 本文から不在を証明したとはしない。

## F3. 一問の実主体と二 target

Q1450 の lambda は continuation/output/snapshots/000063/e/physical/lambda.bin、12096 B packed3、shape [48384]、SHA 7c0dbe475f9b162f4648f5468ee1098eb86b43dbee247d71f811076559ab88fe。旧 HEAD、P result、最終 physical manifest/result の公開 metadata を結んだ。

開始 target は external E **後**の e/output/target-remainder.bin、SHA e902cf3b2d9a5a58ac47459877e017fa4d6a44c5868751b8690543665ae269c1。continuation/output/start.json は rank1386/generation8091、P6 L3851 は64段の前にその immutable bytes 値を保持する。終了 target は continuation/output/snapshots/000063/e/physical/target-remainder.bin、SHA 3bba0da3f619eab5f78e715beabd22d9c7975b36f72d28ee8d7528d9d0f4648a、rank1450/generation8155。前者を pre-E target や最後の一段の parent target へ差し替えない。

行 SEQUENCE は元の位置を保つ：state [0,1354)、delta [1354,1355)、seed34 [1355,1356)、packet steps1–3 [1356,1359)、refinement steps1–26 [1359,1385)、external E [1385,1386)、continuation snapshots0–63 [1386,1450)。P6 parent_row_sources L3806–3837 の元 role/file/whole pin/frame offset/length/row SHA と現在 state.rows の全bytes比較を残す。物理内容の一致だけで役、重複、元 local 位置を併合しない。

原8059はこの1450行数と別の native instruction/意味前提、原97祖先は32件5-key＋65件6-keyの別 SEQUENCE。元 shape・順序・零・relative target・namespace を保持する。辞書/基底/codec/source/runtime/Gamma の context を切断から落とさない。saved normal runtime は Python 3.13.15 (main, Aug  6 2026, 02:15:18) [GCC 13.3.0] / NumPy2.5.1。先の公開 selftest の Python3.12.3を同一環境としない。

元 vector と全1450 descriptor/8059 stream を本便で新scanしていない。登録した8小P JSONは実全pin・metadataを読んだが、vector pinは保存descriptorからの結合であり、新しい vector EOF読取の主張ではない。

## F4. 数値返値と現在作用

必要な採択条項は、同じ context/lambda/ordered row subjects/二targetについて、各元 row[j] の pairing=0、開始 target pairing=1、終了 target pairing=1、という exact E である。1/2を許す nonzero 一般命題だけでは足りない。両 target の関係を別採択した完全な相対方程式から導く場合だけ、一方の exact pairing から他方を結べる。元97の metadata/rolling を保持したことを、その新数値方程式の実施へ昇格しない。

局所返値は Python ordinary int の trit。元 helper の成功辞書は rows、row_pairings_sha256、lambda_pivots、lambda_parent_remainder、lambda_new_remainder の既存5字段をそのまま保つ。row bytearray への append とその全raw SHA計算も現在側に残す。本便は1450 zero bytesの新hashを計算していない。

行ごとの unpack/packed gate、dot 前段の型形状処理、最初の非零行での RuntimeError、二targetの短絡評価を残す。完全到達時の静的 progress 位置は256/512/768/1024/1280/1450。実 P6 callback は CURRENT_PHASE 更新と実 stop/deadline 判定後に stderr write/flush を行う。現在の到達prefix・停止・件数・時刻は将来 run の実測であり、旧値をコピーしない。

また旧 bootstrap、全64 snapshot/9phase/step/checkpoint、rolling、固定 bundle/readers/cache、parent_row_sources、直後の P6 ordinary rows/rank/pairing gate、state.previous_target_raw/direct_pairing、bundle/state の alias、結果全hash、例外時・通常時の fixed.close を残す。Materializer の bare RuntimeError理由と、P6 require の fixed_lambda_batch:付き ValueErrorを混同しない。現行 main の ResourceStop/MemoryError→UNKNOWN_RESOURCE/exit3、他 Exception→FAIL/exit1も維持。引用で費用が変われば同じcapで到達する位置まで同一とは主張できない。

## F5. 報告値の実 reader まで追跡した残件

現在の P6 L5627 は実 Q1450 の rows を native_pairing_rows_rechecked へ置く。L5632の次件追加後、L2847が[1450,1578]を要求し、L2915/L2918が次の current intakeへ載せる。L3443が[1450,1578,1706]を要求し、L3515/L3518が current intakeの四件へ進める。L4004はその whole parent-intakeを startへhashし、L4040は保存 metadataとして返す。

さらに L5195–5201→read_only_documents L5172–5178の全raw比較、recover_private_metadata L5288–5289→write_once L752–757の不変保存、completed-resume L5426–5438の全result再構成比較まで確認した。引用後に1450を「今回数値を再計算した件数」として残すことはできない。新 current/cited の意味、実 serializer/consumer/gate とwholehashの移行を別版で具体承認する必要がある。progress の実 work 説明も同じ区別が必要である。

一方、L3418–3421が照合する**歴史的**intakeの旧件数・全bodyは過去実績であり、不変に保持する。歴史票を新 current modeに合わせて書き直す案ではない。この具体的未実装を残したことは調査未了や旧 source defectを意味せず、実装可能性の次の委嘱境界である。

## F6. 同じ辞書でも同じ Q 証拠ではない

今回読んだ旧64 P resultの direct_pairingは、最終 physical resultからstateへ、さらにcurrent_resultへコピーされたものだった。その最後の一段の parent targetは rank1449の ba110fc8b4f3bfe9c1fb77dc3e62f295cab7ca2fa4c130f33ca7a9ace2a22b9f。Q1450の開始target1386とは異なる。

両保存辞書の0/1/1やrow hashが一致していても、これを開始1386も含む完全な採択Eへ昇格しない。Rootの新公開 exact lemmaはこの二主体を先に固定しており、具体的採択E/元P-C/source/runtime/input closure/制限/非循環性は別途必要。本便は架空AcceptedClaim・採択pin・新scalarを作っていない。

U07/Q1450の現在の区分は、呼出し・二target/row起源・最小式・残す現在作用・後続reporting readerが bounded source-static に具体化済み、exact E と必要なら相対式、局所 selector/lifetime 実装、reporting移行が OPEN、Γ/availability B/TCB/converter/性能も従来どおり OPEN。Q1578/Q1706/Q1834/新lambdaの命題を追加調査・閉鎖していない。

## F7. 納品・自己照合

全資料は %TEMP%/shadow-atelier-audit163/task1129/。final-design-delivery-v1.json は全材料と本返信の実 bytes/SHAを列挙し、自己自身だけを除く。主要正本は次。

| 材料 | bytes / SHA256 |
|---|---|
| public-Q1450-query-result-effect-contract-v2.md | 15514 / 888f4e6c690f459c31972869ebd242c604a2970bb3383a0314f31659c3a371f2 |
| public-Q1450-subject-binding-v1.json | 23963 / 7bcfc25c3a0382c3370596652bbc0d56c8403b9c0abb413a79c29b7bbb443c9d |
| private-Q1450-occurrence-and-effect-audit-v2.md | 18072 / b1910b829f9c964a64ac5270ce7c893d1dee049afffcc5120fdc9523fbb469a6 |
| private-source-range-evidence-v1.json | 101554 / d482bc2f33f6b0fa50fb95b24d8cdc42ee0a6652117bd8c9ce67ea554ea8160e |
| private-reporting-range-addendum-v1.json | 8524 / 8f2e6d3d98b31bfbd9c205634ba8c4914bffbde674c167a4acd9d6cc4a326bea |
| author-static-closure-v1.json | 50361 / dcd015f8d5ff8e66b8d6012768dfac78f08e64d67771f001453eb65ab4e39435 |

入力39件を登録前後の全pinへ再結合し、7 source・53＋6＝59の保存raw範囲を全元bytesへ再照合した。既採択設計全宇宙や全 source全文を今回再読した主張ではなく、本票は明示したQ1450本文・範囲と前件を使う。v1設計票は保持し、v2でverbose=Trueの全引数、bytesの非強制copy、native runtime効果前提を明記した。

PS metadata自己照合器の初稿は関数名Hが内蔵aliasに衝突して中断した。元を保持したv2でTask固有名へ直し、最終39入力/59raw照合は正常完了した。P/sourceや数値処理の失敗ではない。

## F8. 不変・権限・判定

本便のP/source/親/guard/WF変更0、source/数学/Python/GAP/AST/import/compile/selftest/GHA/Git/network/credential/新agent/既process操作0。実行したのは許可されたPS/.NET metadata読取・hash・新設計資料保存のみ。rootが採択したP6公開5群selftestは再実行していない。正式inventory5到着時はTask1109 final bindingを最優先する。

数値省略候補は実在するが、その保存層への引用導入は上記未閉前件つき。全ファイルcold化、availability Bや最小TCB、Gamma、正語/A0/grade2、実速度の昇格はない。正式1834/8539 cross-checked限定7条、A0 actual0/1、grade2 NOT_DECIDED、verified=falseを維持する。

TASK1129_VERDICT: BOUNDED_Q1450_EXACT_LOCAL_CUT_AND_RETAINED_EFFECTS_DESIGN_COMPLETE; ADOPTED_E_INSTANCE_AND_REPORTING_IMPLEMENTATION_OPEN; SOURCE_UNCHANGED; EXECUTION_0; V6_ADDITIONAL_GATE_0; VERIFIED_FALSE

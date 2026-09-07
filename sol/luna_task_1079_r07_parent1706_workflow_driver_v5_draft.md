# Task1079 — parent1706 / v5 の小WF・driver・登録草案

宛先: packet_bounds_audit。Luna/外側実装作者。本便とTask1077/1078の共通公開契約、公開 `TEMP/shadow-atelier-audit163/task1077/interface-v1.md` (19814 B / 928b611d79521701438dd4ed4879ba6ca522166548f9e9a153537a8079a97a95)を全文読む。後続公開addendumだけ共有可。返信は新 `sol/luna_reply_1079_r07_parent1706_workflow_driver_v5_draft.md`、末行 `AUDIT_1079_VERDICT:`。書込はこの返信と新 `%TEMP%/shadow-atelier-audit163/task1079/` のみ。repo source/WF/旧票/実artifact/進行中受領を変更しない。

Git/GHA/network/credential/secret環境読取、Python/GAP/import/AST/compile/source実行、新agentは禁止。PowerShell/.NETのraw/型付きJSON/bytes/SHA静的編集のみ。P5/C5の私的算術本文や差分を読まない。現登録public symbol/range/source pinをopaque metadataとして扱い、全raw pin/range比較に必要な読取だけ認める。外側driverは自己1064系を基点にする。自己WF/driverの最終別読は別作者へrootが委嘱するため、自分の静的点検を独立別読と称さない。

裁定2206 snapshotと正本 `docs/notes/fixed_lambda_batch_v4_cv9_reading_v1.md` の§7/§9、裁定2207 snapshot/expressを読む。2206で正式rank1706/gen8411がcross-checked限定7条、F-k64-1閉鎖。2207はv5の元16親+別17親batch-parent-v4/8key acceptance/fresh lambda1706/128/no-refill/同capsを明示認可し、具体P5/C5/WF/driver pin＋独立別読＋marker/nameのexpress通知で返答待ちせず配置・発射可とした。root全metadata受領は同一一回進行中で、最終wholeinventory未着は補わない。

新草案の固有名を固定する。小WF `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v5.yml`、name `d972-r07-fixed-lambda-cycle-batch-v5-envelope-v1`、marker `[r07-fixed-lambda-cycle-batch-v5-envelope-v1-run]`。別配置driver `search/d972_r07_fixed_lambda_cycle_batch_v5_workflow_driver_v1.py`。新P/CはTask1077/1078のv5 basename。現v4小WF22153/56a8349fd54b16d63da9de2c4762ed04328ef1373f65af45c46019e745a1859b、driver_v2 536145/35f73f5d1b8b519a69773690db8f8e514b3cc1d2792cc595ecdc0b92dede7a0cと全P4/C4/旧source/WF/registryを既存場所に全raw保持する。v5別名なので旧activeを上書きする必要はない。

実装要件:

1. 旧16親の全tuple/全ZIP/全file-dir roster/個別payload到達を保持し、17番目のv4親tupleをTask1077 exact値で追加する。batch-parent=v3とbatch-parent-v4=v4を別root/roleへ取得し、各世代の宣言emptydir復元を別票へ保存する。取得3487dirと復元後expected3525は実最終票で確認後登録する。full outerZIP EOF/readback/pin/source/strict typedJSON/symlink/casefold/unknown/readonly/disjointnessを保持。巨大親を薄く切り詰めない。
2. 公開8key acceptance/36key next header/二層intake/全主要出力exact keysetsを実装する。旧v3とv4のnamespace/33key header/旧code provenanceを分離し、旧16投影/元anchor/元batch_anchor/runtimeの完全一致をgateにする。旧128+新親128は合計256親行/353祖先、今回上限128。全plain/packed target区別とfixed-reference専用入場を両世代へ適用し、同居payload gateを緩めない。
3. current registryは新v5として作り、旧P4/C4全rawと新P5/C5の全source区間・UNCHANGED/CHANGED/ADDEDを実bytesで登録する。過去v4registry v2 236390/84f5bbc6a85e77915535968e4342c09b6bf3e5b94638ab14184c67ca677ce114と全履歴は保持。共有TCB4/未測定call coverage/第三独立false、公開old-loader/body保持証明、source closure/親内歴史sourceの全照合を維持。未着のP5/C5全pinや区間は捏造せず、草案は実行guard閉鎖・最終freeze未了として明示する。
4. 事前登録は四群 P[30,10,6,7]/C[28,9,6,7]、群名は旧三群+batch-parent1706-two-layer-admission。新第四群literal/目的labelは各作者の公開票へ束縛し、同群数の推測を実selftest成功の代用にしない。旧driver metadata16群を維持し、新scope固有対照が必要なら別件数をrootへ提案する。全fixture正負body/全archive/元inventory/全entry EOF/hash/readback/3inventory/最終保全を省かない。
5. 本P/C cap/outer/自己試験/RSS/jobを固定する。P5400/C10800、outer6000/11400、selftest300/outer360、RSS7168MiB、job330分。元全8059P1/四character/全54433chords+2aux、fresh lambda1706/最大128/no-refill/max_batches1。seq3 selection/seq9初回decision、early NOT_OBSERVED/null、候補無しNOT_APPLICABLE、diagnostic名指しcheckpoint/直後durable tail/既完readonlyを維持。全128独立や未来oracle値をgateで強制しない。
6. 起動前全source/driver/WF pinと終了時同一性、親pre/post、harness開始/終了/exit、全最終join、candidateとdiagnostics両upload、失敗時も可能な全保全を新具体bytesへ接続する。実run/head/artifact未観測値はregistrationへ後着するものとして扱い、凍結方法を明記する。WFは小さいenvelopeのまま、CLIを登録した実runをrootがAPI観測できること。

F-v4-1の計測は次runの既存公開telemetryから再現可能にする。root読解ではCV-9 §7.1/§7.2の232.786秒は **P elapsed − P selection − P候補六相合計 − P final separator** の残差であり、P+C合計の計測外時間ではない。Cは段別timestamp無しなので、Cの対応残差を勝手に作らない。新driverで結果を集計するなら別の明示schemaの公開cost票として、P total/selection/六相合計/final/差、C total、P+C totalを区別し、各入力実file/字段/単位を保存する。新数学相を実行せず既保存telemetryの加算だけ。失敗/途中票は不明値nullと理由を保持する。追加の自己計測を旧P/C数値kernel本文へ混ぜない。

次v5は旧16親を保持し第17親と別adaptersを足すため、「同一コードで単一親が369→377 MBへ置換」という対照ではない。fixed-cost一数値だけから原因を断定するhard gateや234〜236/270〜280の期待accept条件は設けない。両親別の実file/dir/ZIP規模・layer数・source版をcost票の文脈へ結び、数値そのものと比較できる前提をrootへ報告する。工房へこの留保はrootが正式返信する。

先に外側差分面とcost票の公開exact keyset/集計入力を短く提案し、自己driver/WFの草案を進める。root全inventoryとP5/C5最終pinが後着したらversioned最終化へ。納品は完全小WF/driver/public registry/保持raw全差分/全material pin/全未実行境界。最終独立別読とroot採否前に配置/発射可能とはしない。

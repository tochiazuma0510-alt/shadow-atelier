# Task971 — 完全oracle＋Eの動的継続器 producer

役: Luna 実装。Task970の完成設計を新sourceとして実装する。変更可は次の二ファイルのみ。

- `search/d972_r07_complete_oracle_cegar_continuation_v1.py`
- `sol/luna_reply_971_r07_complete_oracle_cegar_continuation.md`

rootがgit/GHAの単一broker。ローカル数値/Python/import/AST/GAP実行、network/git/credential、
追加agent、workflow変更は禁止。既存source/返信は公刊前freezeも含め不変。
通常のsource編集/読取/bytes/hashのみ可。完成blockを順次保存してrootへ知らせる。
reply970は変更せず、2138以降の更新は本replyへ記す。今回Eのrelease条件ではない。

## 正本と登録宇宙

reply970全文、Task957/958/963/964、source959/968/965、既存full-origin cap/resumeを保持。
Q2全54432点/108864辺、六tag/四character、D=ker(five carry)＋二eta、全8059 P1、
lower96776、四B/48384 physical、Conn/source-map/同一語v547/v548前提は同一。
一般的拡張、Gamma、固定complete packetの実装は加えない。

起点はrank1385/gen8090の成功oracle completion33977701313/1と、これから実測される
Task965/966 E結果。**E run/head/artifact/source checker最終pinはまだ未観測**。
外部Eを取り込む新CLI `--e-root` のpin表はmissingならfail-closedにし、rootが実観測値を
渡してから固定する。未来rank1386を起点定数にしない。実親Eが線形零ならTask958 pendingへ
直ちに分岐し、余分なoracleは計算しない。実Eが失敗なら保存済み非零oracleの修理が先である。

工房2138の同一対象・限定8条を継承。F-sc-1 envelope/word loader/context/transport TCB、
F-sc-2 現lambdaのq1..3/aux等が零（作用素全入力の恒等零ではない）、F-sc-3 v2 full selftest
未実行を記載。次のchecker実v2使用GHAでfull selftest一回はrootが手配する。
現在の度数から確率/独立行本数/反復数や実時間を予測しない。

## 実装契約

1. **薄い動的attach/DERIVED start**。受理済みrank1385 prefixと外部Eの一行をmetadata/
   exact bytes/hash/rolling chain/target identityで取り込み、新current rows/records/target/lambdaへ
   一度だけattachする。旧26scan/insertと外部Eを数値再走せず、新loopのcompleted_stepsは0。
   元rho2はDERIVEDを保持し、E separator内のtarget_derivationからoriginal hashと型付き親列を
   明示的に構築する。旧startの直接字段へ盲目的代入しない。P1 Refとphysical Refを分離する。
2. **固定bundle**。geometry/group/tag/BFS/carry/RightMaps、P1/index/同一語mod54 metadata、
   Task554全12blobs、四BとConnのsource/data/hashを一度認証して保持できるbundleを作る。
   q/chi/kappa/P1 contractions/cochain/tree/witnessは毎current lambdaで全数再計算。
   旧geometry manifestは旧snapshotに結ばれているので、新固定owner/manifestへ配列のbytesを
   認証して登録する。単なる旧manifestの改称は禁止。固定I/Oの反復hashをcache化してよいが、
   各lambdaの8059全式や各Eの全lower/P1補正を省略しない。全ファイル長/EOFを保持。
3. **一つの新step**。現在lambda/physical headに結ぶ全oracle section/cochain/treeを完成し、
   全8059式、54433 chord/二auxを満たす完了manifestを保存。非零なら同じwitness一つの
   raw SLP/普通epsilon・omega/全endpoint/六tag source、元lead昇順primal、mod54同一語、
   fresh raw tupleから一回の全P1補正/96776 lower零、四B、全current rowsの挿入順reduction、
   normalize一回、target/freshlambdaを実行。rank/genは実親+1でtarget scalar0も保存。
   原scalar非零・新target scalar・normalizationを混同しない。元rx/ryではなくrx³/ry³/commの
   Fox零というTask966の訂正を保つ。新lambdaの全row/両targetのpairingを確認する。
4. **型付き分岐**。COMPLETE_ZEROはv548/Conn前提付き完全separator候補まで、target零は
   LINEAR_MEMBERSHIP_CANDIDATE/Task958全11slot pendingまで。新MEMBER/NONMEMBERの裁定は
   checker/CV9/rootの後。未計算/UNKNOWN_CAP/UNKNOWN_RESOURCE/REJECTEDと零を分ける。
   同一stepの旧witnessを新lambdaへ使い回さない。外部Eは新stepへ二重計上しない。
5. **phase保存/resume**。Task970§4の固定owner/source/start、snapshots/stepのoracleとE、
   step manifest、checkpoint、atomic HEADを具体化する。capは同じoutputでcommitした新E数の
   絶対上限、resumeでresetせず、invocationのcap/時間はimmutable ownerへ含めない。
   oracle section/cochain/tree、E raw/source/primal/P1/B/physicalの完成phaseを型付きloaderで
   再利用し、未完phaseだけをやり直す。完成E全payload→step manifest→HEADを連続publishし、
   中間に協調停止判定を挟まない。HEADの前後/到達不能tailを認証して扱い、未完を完成と推測
   しない。再開は全新chain/bytesを認証して薄くattach、最後のlambdaを全row/両targetへ測る。
6. **公開ABI**。新schema `d972.r07.complete-oracle-cegar-continuation.v1` と exact roster /
   dtype/shape/bytes/hash/EOF/rolling predecessorを早めにreplyへ保存。frozen Eのserializerが
   起点oracle pinをhardcodeする箇所は新動的wrapperで正しく生成し、module constantsや親pinを
   monkeypatchしない。保持算術helperのimportは既存producer系統内のみ、checker import禁止。
   source receiptは実import/source/data全由来と原producer/completion/Eの由来を分ける。
7. **新interface canaryだけ**。cap持越し、stale lambda/witness、完成phase→HEAD前の停止と
   resume、plain target scalar0、target零≠MEMBER、source/owner変更の拒否を本番関数へ結ぶ。
   未実測の合成大規模成功fixtureを作らず、旧成功suite/旧数値prefixは再実行しない。
   CLI resource/signal handlingと各phase開始/EOF実時間・payload bytes（I/O量とは別）を保存。

最初に具体的ABI/関数接続と想定importを短く報告し、実装を継続する。難所は実在する型や
signatureを示して速達、独立に進められるblockは止めない。数学の再解説や性能予測で代えない。
全実装/新canary/CLIを静的に読み、最終bytes/SHA/再現GHAコマンド案と保持TCBをreplyに書く。
数値/ASTはrootのGHAでのみ行う。最終行 `AUDIT_971_VERDICT:`、`verified=false`。

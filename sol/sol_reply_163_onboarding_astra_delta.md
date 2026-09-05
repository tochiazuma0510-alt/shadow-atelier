# Sol 163 — Astra 差分引継ぎと固定 root packet への移行

著者: root / 2026-09-05。便163を全文読み、継承された便162の読了順と
work orderを適用した。正式な裁定は以下のF番号で記す。campaignは再開中。

現在の受理済み到達点は **rank1385 / generation8090 / Separator**。
**A0は0/1 actual、2016→54432段はgrade1の1/6、grade2はNOT_DECIDED**。
run33964709359/1で固定44 seedのpacketと3行追加、実resume、独立checkerが
成功し、工房裁定2125で限定付きcross-checkedとなった。informative44件は零、
残り132件は零rootによる構造零。rankは3増加しtargetは2回変化した。
actorを含むfull-origin実走33967668257/1では候補rank1385/gen8090へ26行進んだ。
保存出力の照合専用GHA33971897879/1で全26段・26scanの独立checkerがPASS。
工房裁定2131で限定7条のcross-checked。旧走査表の算術に共有コードの限定がある。
v548完全scalar oracleのproducerは完走。run33975617653/1のcheckerに出力型エラーが
出たため、保存出力を不変にした修理checkerのcompletionをTask968/969で固定した。
source限定差分と全704行workflowをrootが読了、969の静的監査PASS。新GHAへ進む。

## F1 — A1: stale前件6件と前提訂正2件を受理

1. dihedral予想は工房のP1正本§0において完全証明済み・発効として扱う。
   W2fam/W5/ΛREG/(M-b)/ASMαと算術起点の保持条件は同正本どおりであり、
   Lean化と算術起点まで無条件に完成したという意味へ広げない。
   「一般にopen」という古い現在地へ戻さない。
2. A0はMEMBER塔を登り切って証人構成へ進む課題である。NONMEMBER分岐は
   誤った肯定を防ぐ正当な出口だが、それを目的達成と取り替えない。
3. A0そのものはΔ上の有限な共同所属問題である。H/Pの完全fibre、正規化と
   literal direct replayを揃えた有限MEMBERは、その有限問題を閉じる。
   無限精密化T2のcofinal liftは別の義務であり、有限解の追加前提にしない。
   一方、今回のHのgrade2一個だけでは全H/PもA0も閉じない。
4. `verified`はLeanに予約する。既存runをcross-checkedと呼ぶ根拠は工房の
   CV-9裁定番号と限定条件であり、Solが自己昇格させない。第三のsha/封の
   replayを、第三の算術再計算とは数えない。
5. producerとcheckerの著者・実装分離を維持する。fixtureは実artifactの
   layoutと契約に合わせる。共有核・親前提を列記し、TCB変更時には工房の
   独立性測定を受ける。二実装が同じ規約誤りを共有する危険は残る。
6. GHAはroot単一brokerから明示markerまたは適切な`--ref`で一度発火する。
   6h job/7GiBの枠内、内部Meterはwrapper timeoutより短くし、phase markerと
   fail-closed receiptを残す。親artifactは実体にpinし、Releaseミラーを継承する。

返書162§0の訂正も保持する。

- 現在のprecision-twoは **2016→54432** のT1の辺である。
  便162の「54432→Q0」は段の取り違えだった。
- run33903333330/1のseed2 scalar1は、旧式のdirect側の型が誤っていた。
  Task920/921とv541、工房裁定2083によりcorrected scalar0へ訂正済み。
  返書919のsame-byte受領事実は歴史として残すが、そのseed2を実違反として
  materializeする許可は失効している。

正しいsourceは、raw seedから**全canonical P1再構成を引いた完全な差**で
ある。そのlower96776座標が零になった後でplain top sliceを使う。
actor直結項は`K_t b_i + T_(2,t) z_i`であり、`T_(2,t) z_i`だけではない
(v541 (2.1)–(2.3))。Task712の同次表だけでは前者の混合項の錨を供給しない。

## F2 — A2: 固定packetを継続採用。回数は有限上界と実測を分ける

同じP1 basis/section、Task554、44 raw seed、Bを固定し、F3上で

```text
D_s = Eval_le2(seed_s) - sum_i SeedRed(s)[i] tilde_b_i,
d_(a,s) = pi_a gr2(D_s),  v_(a,s) = B_a d_(a,s),
R = span{v_(a,s): a=0..3, s=0..43}.
```

全lower-zero後、v541により
`<B_a^*lambda,d_(a,s)> = <lambda,v_(a,s)>`。
したがってDとpacketはlambda非依存で、一度の実構成を後続周回で再利用できる。
rank1356のroot scalarを単発で出し直す方式から、この固定packetへ切り替える。
新しい数学的前提を先に増設する必要はない(独立紙監査: 返書948 F1/F6)。

S_*を保存済みrank1356状態とすると、非零pairingで選んだvは現在のSの外に
あり、一追加でrankは厳密に1増える。成功追加回数tは

```text
t <= dim(S_* + R) - 1356
   = dim(R) - dim(R intersect S_*).
```

| 上界 | 根拠と限定 |
|---|---|
| 176追加 | 固定リストが4×44本。実装の保守的安全上界。 |
| 174追加 | packetのchar0 seed30/34と保存source-dのbyte一致を通した後。両行は初期Connを法として独立で、既にS_*に含まれる。 |
| 全物理像では残り12090追加以下 | v546のstrict source filtrationと完全source、lower rank6705、Conn rank1354を継承する場合。 |
| 条件を使わない物理ambient上界47028 | 物理幅48384から現在rank1356を引いたもの(v535定理4.1)。 |

3行目の導出は`dim ker(pi)=12092`、`dim W1=8059`より
`dim W2=20151`、`dim ker(ell)=20151-6705=13446`で、
`M2=Conn+G(ker pi)`、`dim M2<=1354+12092=13446`。
よって`13446-1356=12090`である。**12092はpure sourceの次元で、全物理像の
rankではない**。上記は紙上の条件付き上界で、packetの実rankや所要時間の予測では
ない(返書948 F2、v546§5)。今回のpacketには174の方が強い。

非零seed集合が30/35/36から34/35/36へ変わったことは、残り2回等の予測を
支えない。Sのannihilatorは狭まるが、選び直すcanonical lambdaは変わる。
未追加の行は旧lambdaで零でも次のlambdaで非零になり得る。必ず零に残るのは
既にSへ加えた行である。各更新後に四つのB-adjointを作り直す。

`ROOT_SEEDS_ZERO`は現在lambdaがRを消すという有限事実である。target導出と
lambda(S)=0、lambda(rho2)=1を保持すればrho2∉S+Rも従うが、R⊆SやRのrank
飽和は従わない。actor32236 originやその先の軌道は範囲外なので、これを
grade2 NONMEMBERへ昇格させない。cap到達も全零の代わりにしない。

## F3 — A2続: oracleの切替条件

自然な切替点は固定rootの全零終端である。資源限界なら最後の完全prefixを
保存し、UNKNOWNとして別の同じlambda用oracleへ移ってよい。

**dual orbit経路**: 新しい四つのrootを現在state/lambdaに結合し、Task712随伴の
完全閉包を取り直す。返書910/911の「504本」は初期lambda
`7522ee1f00f386b229ea46bc0f2b9fdf2854cf03c262f40a2f60dd9ced0102ed`
に対する実測であり、rank1356以降のlambdaへそのまま移せない。同じ閉包が使える
ことを新rootの所属係数または新たな閉包receiptで示して初めて「504行sweep」と
呼べる。全像非所属にはConn直交、全四characterの閉包、各dual基底に対する
**全32280 origin**のscalar EOFが必要である。actor directのK_t項を省略しない。
非零ならword originを保持して完全P1減算→lower-zero→物理追加へ進み、古い
lambda依存の探索結果を次周回へ持ち越さない(v531 (4.2)、v535§3、v541)。

**v548/v543の紙経路**: v548のsection補正
`F_lambda = lambda H - (lambda H s) pi = lambda G(id-s pi)`を採用できる。
新しい四rootと8059本のchiから、全source96776座標上で
`<kappa,b_i>=chi_i`を全8059本満たすkappaを実装する。さらにmixed項とmarkingを
含む実SOURCE随伴を与え、Q2の固定marked treeの**全54433基本閉路**に対して
`f(z_e)=a tau(z_e)`とauxiliary2値零を調べる。これがConn直交と併せて全像零の
完全な試験となる(v543§3–4、v548§3–5)。現在の紙は実adapterの代わりではない。

違反時には高々6基本閉路の合法な組合せまたはauxiliary方向が出る。
v547のliteral repairを使えばv542の27-entry endpoint表を省けるが、固定語、
整数指数、符号、P1 section減算、lower-zero、物理replayはなお必要である。
full sourceの試験を固定44 seedへ再投影して済ませない(返書948 F4/F5)。

## F4 — A3: 939〜945の継承表と欠落

| 文書/到達点 | 継承すること | 継承しないこと・残作業 |
|---|---|---|
| 939 / run33954712636 | rank1355で全保存1355行へのFINAL lambda sweep、char0の44 scalar、非零34/35/36、工房2110限定3条件 | 「176本独立の走査成果」、旧lambdaでのseed35/36を次の選択根拠とすること |
| 942 / v548 | section補正の紙上恒等式と同値性PASS | kappa/実SOURCE随伴/marked-tree oracleの実装・本走 |
| 943 / run33956437467 | seed34追加、rank1356、gen8061、全1356行と親/現target剰余への直接内積、工房2117限定4条件 | 原rho2への直接内積、grade2/full A0の終端 |
| 944 task+reply | lambda非依存packetの具体的layout、1回のP1/lower走査、現stateの結合設計 | 実装済みという解釈 |
| 945/946 task | 44完全差、固定packet、耐久prefix、同owner resumeという採用済み契約 | 着任時点でproducer/checker/workflow/reply実体は存在しなかった。Task947で二著者へ再委嘱して再開 |

保存済み現stateのpinは以下。これは前runの機械受領値の引用であり、今回の
新しい算術ではない(返書162§18、v220 Delta535、工房2117)。

```text
run=33956437467/1
source_commit=b9ae78b0950b186463849c3ec874f6474f359851
state_head=d467e4e60b8bff88272cddd4b01d630d763e863b4500015c7c6c077b23ddf26b
lambda_sha256=f7406d70211ab02acf08a895d127d17e7dab179454916a90ea40cb11152e12dd
target_remainder_sha256=46a6b8281587a13236fd9af00eab9825a2d956dd878613af14182b5f9ae94c49
candidate_id=9966542166
candidate_zip_bytes=984053
candidate_zip_sha256=a4cb9f63a470636628d9ef02a5b5e55d90fe3b0a2c70f2012d32c9517d87defc
diagnostics_id=9966542318
diagnostics_zip_bytes=1002755
diagnostics_zip_sha256=a8c147acf7da6b6246e33b20d3491bad9458214772762ef1d1bea17866c58f62
```

追加で引継ぎ票の「v2.3 Q6〜Q8未回答」は誤りだった。返書162§6で回答済み。
今回の発見を工房が状態裁定2120へ追記した。v2.3も全文読了し、同節を継承する。

## F5 — CV-9残件の採否。M3-1はDERIVEDで処理

M3-1の許された二案のうち、Task947では明示的DERIVEDを採る。
親の`lambda_old(rho2)=1`をコピーするだけでは、新lambdaの主張にならない。
保持するのはTask904の**target減算恒等式**とその後のdeltaである。

```text
rho2-r_base in S_base,
r_(j-1)-r_j = c_j p_j in S_j,
therefore rho2-r_n in S_n.
lambda_n(S_n)=0 and direct lambda_n(r_n)=1
imply lambda_n(rho2)=1.
```

certでTask904とseed30/34の実parent、および今回のprefixを特定し、
`lambda_rho2_mode=derived`、`original_rho2_directly_read=false`を宣言する。
原rho2 v17(artifact9925190479)をstage・直接内積したとは書かない。
これで数学的曖昧さは解消できるが、cert実装の閉鎖と新run格付けは別ゲートで
ある(返書948 F7)。過去の成功artifactは変更しない。

- **2110 R1-1採用**: declared176、非零rootのblock数、情報を持つpairing数と
  構造零132を分ける。rank1355 runの実成果はchar0の44値と他3root零である。
- **2110 R1-2採用**: raw seed2 char0のSHA
  `e67d0a0b21aaf41fd1617811b45cd51191a0087c7d04fcc33dda5a58f4fcfca6`
  とsupport568はlambda非依存の回帰pinとして保持し、旧scalar条件だけを退役させる。
- **2096 w_t独立錨は未閉鎖**: クローン内のlower actor錨を第三導出と数えない。
  今回はroot-onlyなので新しいw_t再計算を前提に加えないが、全actor/orbit完了時の
  意味論監査から外さない。raw seed核の共有・canonical P1 topの親依存も明記する。
- **2048/2060の限定を保持**: d2 cache内容とAgg規約の正しさはphysical connection
  二実装の射程外。原Connへの直接dotと還元後stateへのdotを区別する。保存stateの
  全行sweepは原Connを今回再読したという意味ではない。
- **既閉鎖分を再開しない**: v544は「strictly increasing」をunique/in-rangeで
  元順序保持へ訂正済み。source順の非単調性をもう一度ソートして修理しない。
  FINAL lambda全行sweepは2110でF1閉鎖済み、今回も実行する。
- 新TCBの規約表diffは毎回、輸入経路とAST/類似度は変更に応じて工房CV-9へ渡す。
  この返信の紙上PASSはcross-checked格の代行ではない。

## F6 — v2.3 Q6〜Q8の継承確認とA4

Q6: pointed syzygyの存在は、固定word-pair、contracting operator、boundaryと
全精密化への自然性を供給しない限り、v191の有限なuniversal certificateへ自動吸収
されない。「一つの有限schemaが実務上欲しい」を数学的必要条件へ強めない。

Q7: 実A0のownerはphysical側を採るが、unaggregated側との同値には比較データが
要る。返書162§6の記号で`J=q'(ker r_U)⊆K_E`、`K_N=K_E∩ker A'`とすると

```text
0 -> K_N/(K_N intersect J) -> K_E/J -> K_L/A'J
  -> K_L/A'K_E -> 0.
```

従って一方のfull-fibreから他方への主張には対応するkernel/image条件が必要で、
有限dimというだけで同値としない。抽象比較は回答済み、actualデータは未産出。

Q8: marked DLLから登録Frattini契約への比較は未供給。固定m/g760、coarse H/Pの
正規化、許容preimageと失敗保存を明示する必要がある。有限商のFurusho反例から
副有限版を否定しない(裁定2092の訂正、副有限版はQ14)。

v2.3は上記の限定を保って条件付き受理を継承する。A4 bordered resumeは今回の
A0の前提でなく、production未受理のままrow26/次row27を保留する。旧v4〜v9や
未受理v10を追加再走してA0の実行を遅らせない。

### F6追記 — 作業中に届いたv2.4の差分確認

`ops/express/20260905_fable_astra_a0_note_v2_4_delivery.md`を受領した。
正本SHA256は`eaef59ee9c67c84f379e0bbccc85e65e05da6da94add9ebb425998ba8c1643ae`。
読んだ範囲は注C.1、§5.2のN1a分離と表、§5.4の補題5.4.1・帰結・自己評価、
§8のQ6〜Q8回答、差分D26〜D33である。v2.4全体の再監査とはしない。

**差分PASS**。中央写像の核は`(K_N+J)/J`、余核は`K_L/A'K_E`であり、記載の
完全列は未証明の全射性を使っていない。A'全射時のδについても、代表の差は
ker A'に入り、δが零ならker A'の元を引いてker rEに入るので`ker δ=A'K_E`。
rEも全射ならδも全射、記載のgap判定が従う。N1a-DLLとN1a-R07の分離、4点の
bridge、R07側UNKNOWNへの訂正も返書162§6の趣旨どおりである。
命題Cの語と単一有限schemaの要求をoperationalに限定する読みを保持する。
これは既存回答の正しい採録で、actual kernel coverやA0の新規完了ではない。

## F7 — 読了・preflightと進捗台帳

便163の順に便162全文、返書162全文、状態504行の2083〜2117、地図9/4・9/5、
939/942/943、944 task/replyと945、四CV-9正本とexpressを読んだ。継承指定の
AGENTS/CLAUDE/体制と道具、状態504行全体(1847〜2078を含む)、地図9/3、CLAIMS、
906/909/910/911/919、Task920、旧CV-9三本とexpress、用語正本も読了した。
追加読了は対話帳新着T67〜T70、所在と能力、道具と検証の序列、P1 corpus§0、
v541/v546/v548、v2.3全文、独立返書948である。v542/v543/v547の追加照合は
返書162/942/948の記載範囲を用いている。

便163のdigest表のstate以外7対象はbyte数とSHA256[:16]一致。
stateはgitの`d7821871dd7cf05cbeecf1b245d3a04a8e0888d0:docs/状態.md`のraw bytesが
99268/SHA256`9dd936b28150d97b25e7a0d00529dac849ec0d334389bc7545951f695016fc62`
で配達pinに一致した。2026-09-05 10:14 UTC前の現物との差分は、共通prefix96821
byte・共通suffix2447 byte・削除0 byte・追記409 byte(裁定2118〜2120)のみ。
全文が古い値と一致したと偽らず、既存部分の同一性をこの形で確認した。

再現に用いたread-only操作は`Get-Content -Encoding UTF8`、`rg --files`、
`Get-FileHash -Algorithm SHA256`、`git log -5 -- sol/`、`git show`のraw byte読出し。
この段階の読了・監査は算術replayではない。既存のdirty treeは開始時に
`%TEMP%/shadow-atelier-audit163/status-before.txt`へ保存し、無関係ファイルを
編集・stageしない。新旧の親artifactは既存TEMP所在を確認した。

ユーザーの明示指示によりv220へDelta536を追記した。
**CLOSED**: 今回新たなactual gate閉鎖なし。
**ADVANCED**: J2/J3の固定packet実装再開、回数上界と切替条件の紙監査PASS。
**UNCHANGED**: J4、A0 0/1、当該段1/6、A1 4/4、A2 2/3、A3 3/3、A4 1/3、
compact A5。full A0/COMMON/cofinal lift/fake/Iharaは宣言しない。

## F8 — campaign実行記録(進行に合わせて追記)

Task947でTask945/946を二著者へ再委嘱し、Task948の独立紙監査に続き、
Task949の全source静的監査もPASSした。耐久化前の一時ディレクトリをcheckerが
拒否する不整合は修理済み。完成したHEADのprefixだけを計算対象とし、原本と
完成packet/stepのrosterは厳格なまま、明示された一時出力を診断として保持する。
初期packet中の内部期限、UNKNOWN_RESOURCE receipt、raw marking/word dataの
byte pinも追加した。checkerの最終返信と凍結実体は受領済みである。

rootは全workflow配線、10親artifact、10 executableとraw data2件の閉包を点検し、
既存依存8本とdata2件の実byte/SHA一致、既存dataのGit上の改行属性を確認した。
GHAのAST・小canary後、producer cap1→同ownerの実`--resume` cap176→checkerを
直列実行する。内部1800秒<外側40分、job130分。数値計算のローカル実行はない。

| 新規凍結ファイル | bytes | SHA256 |
|---|---:|---|
| search/d972_r07_fixed_root_packet_loop_v1.py | 70509 | 65169d7a26b6daf29152d5afa1352387766ac4024b078caf82a295ca57fbc3fd |
| search/check_d972_r07_fixed_root_packet_loop_v1.py | 56545 | c6a4202180342471d6e8938c0ca50c88d0fcd11bf5d2a8f9d100b83e993dfb3f |
| .github/workflows/d972-r07-fixed-root-packet-loop-v1.yml | 26054 | 7586d9cdd2483d648d4f6a677e93916f02cb20bc8e039ea7113f4e208f8161d7 |

**STATIC_RELEASE: PASS**。ユーザーは「終わったらGHAで自由に実行していい」と
明示した。必要なcanaryをworkflow内で先行する一回の本走をrootから投入する。
工房CV-9は本走後の別格付けであり、この静的PASSに含めない。

### F8.1 — 本走を開始

- source/launch commit: `25501f62c326290bafd223fe3b7a1d7b0ba51f0c`。
  rootが関係12ファイルだけをcommitし、作業branchへ一回pushした。
- run: **33963515077/1**、job **101299441533**、eventはmarker付きpush。
  run作成`2026-09-05T11:30:35Z`、job開始`11:30:38Z`。
  workflowは`.github/workflows/d972-r07-fixed-root-packet-loop-v1.yml`。
- `11:31:09Z`のread-only確認でin_progress。親live pinの照合はsuccess、
  P1等の取得中。AST/canary/本算術はこの時点では未了。
- 新workflowがdefault branchにないため、`gh run list --workflow <path>`は404。
  pushは成功し、commit指定のREST run一覧で上記一件の起動を確認した。
  再dispatchはしていない。

### F8.2 — 初回停止と実親形式に基づくv2修理

run **33963515077/1** は **failure** (job終了11:31:55Z)。source/data pinとAST、
実親の取得・root所在確認、producer3/checker4件の小canaryはsuccess。
本走は11:31:33Z〜11:31:54Z、producer実測19.99秒で`REJECTED`となった。
Task904の8059 instruction metadataと現lambdaの全1356行内積までは通過したが、
`owner_and_tables`で`KeyError('target_derivation_accepted_as_premise')`。
packet作成と新行追加には到達せず、resume/checker本走はskipされた。

工房の裁定2123 expressと、TEMPにある実seed30/seed34 resultをrootも突合した。
欠けているのは**seed30 v1**のrho2欄であり、**seed34 v3にはtrueがある**。
異なる世代の全親に新しい欄を要求した実装不整合で、静的PASS949とsynthetic
canaryはこの実レイアウト差を捕捉していなかった。数学的反例やrank変化ではない。

diagnostics artifact **9968702711**、18902 bytes、ZIP SHA256
`265a61aa1109c87622121300fe19c4a6330d4619d0d62974de48f8839c06076b`。
rootが`gh run download 33963515077`でTEMPへ取得し、実停止logを読んだ。

Task950/951/952でv2 producer、独立checker/workflow、実親形式の差分監査を
開始した。既走v1は凍結のまま。旧世代はその固定result/target/payloadの同一性と
明示DERIVED連鎖でのみ受け入れ、v3の欄欠落/falseやrho2 identity不一致を拒否する。
`get(key, True)`で穴を埋めない。実際の固定親JSONを使うmetadata-only canaryを
GHA本走の前に追加する。原rho2の直接実測や古いtarget再solveには格上げしない。

### F8.3 — v2差分を凍結、再投入へ

Task950/951が実装を凍結し、独立Task952の差分監査でblocking defectなし。
rootも両側のv1→v2 diff、実seed34 parent-stateの各参照、依存API、workflow
差分と実byte/SHAを点検した。packetの算術・物理行追加・target更新・耐久resume
の関数本体は前版と同一で、旧v1三ファイルも元のSHAを保持している。

| v2凍結ファイル | bytes | SHA256 |
|---|---:|---|
| search/d972_r07_fixed_root_packet_loop_v2.py | 84173 | e040c7b3cf5f96fe33c0e36a00ba8dd887784e0f5a1e6fa036d407c0ceba65e6 |
| search/check_d972_r07_fixed_root_packet_loop_v2.py | 66251 | 5289253a82d942d71b1ec55505d08ab772b111f2ba08e301f67387eae19b23e5 |
| .github/workflows/d972-r07-fixed-root-packet-loop-v2.yml | 27963 | 329429a3e8bda8461db4bc872f9c3aa614f5f346d20a398fb3480e8c8fd4e711 |

実親metadata CLIは各著者の本番validatorを使い、base/seed30/seed34の固定
JSONと保存delta payloadを読み、legacy欄不在/v3 trueの事実を明示する。
v3 false、v3欠落、rho2 identity、未登録schema、base manifestの改変を各側5件
拒否する。GHAで両側の封付き`parent_layout`一致を要求してから、既存canary、
cap1本走→同owner実resume cap176→全packet/新prefix独立replayの順に進む。
この段階は静的release PASSであり、CLI実行PASSも新rankもまだ宣言しない。

Task953は走行中に行う次oracleのread-only intakeとして事前登録した。
固定root全零をgrade2負判定にせず、現lambdaのfull-origin/dual閉包経路と
v548のkappa/source cochain/tree経路の実adapterを比較する。走行中のv2の範囲を
広げるものではない。v543/v547は今回追加で全文を読んだ。

### F8.4 — v2本走を開始

rootが関係12ファイルのみをcommitし、marker付きpushを一回実行した。
source/launch commit **`fff114c41bd8748ad0e708919fe0820335c9cce8`**。
run **33964709359/1**、job **101302680212**、event=push。
run作成`2026-09-05T11:57:41Z`、job開始`11:57:43Z`。
11:58:08Z以降のread-only確認でin_progress、親live照合とP1取得はsuccess、
Task554取得中。AST・実親canary・本算術の結果はまだ未了。
Task952の正式返信も全文読み、静的差分PASSと前回の見落としの明記を確認した。
v220へDelta542を追記。重複dispatch、旧成功runの再走、ローカル数値計算なし。

### F8.5 — 固定44 packetの本走・実resume・独立checker成功

run **33964709359/1**、commit **`fff114c41bd8748ad0e708919fe0820335c9cce8`**
は **success**、job終了`12:01:23Z`、run更新`12:01:24Z`。
実親metadata両側・五つずつの改変拒否・封付きlayout一致は11:58:26Z〜28Zに
通過、既存canaryもsuccess。producerの初回は実測**67.825秒**、実resumeは
**22.388秒**、独立checkerは**78.489秒**。初回保存step1の全prefix byteが
二度目の起動後も同じであることをworkflow receiptがPASSとしている。

| 新step | character / seed / scalar | rank / generation | 新lead / scale | 物理reduce件数 | target減算係数 |
|---|---|---|---|---:|---:|
| 1 | 0 / 35 / 2 | 1357 / 8062 | 1419 / 2 | 877 | 1 |
| 2 | 0 / 36 / 1 | 1358 / 8063 | 1420 / 1 | 910 | 1 |
| 3 | 0 / 37 / 2 | 1359 / 8064 | 1421 / 2 | 891 | 0 |

値の出典はactual `output/steps/000001..000003/result.json`。
checkerは44個のraw seedと全96776 lowerを再構成し、packet全byteと新3stepの
算術を再計算した。終端は **ROOT_SEEDS_ZERO**、declared176 pairのうち
非零rootに対するinformative pairは44、非零seed scalarは0。最終q0は
support2781、SHA`f192e3a9c68a6dd555b591462ec7dd506ebf1d2f6005862ce31b7e611ae072bf`、
q1/q2/q3は零。actor originsとorbit rowsの実行数はどちらも0である。

最終state headは`7b7380a7ddb785910347df14f47ba4634cc5fa2fff7c32b722455a824d6cddda`、
lambda SHAは`60ac649575400e98881c5de5d4ef2c6202d3cf577da1411042104254edb004e2`、
target remainder SHAは`0a466426db600e191e9ee5563066dbb729492ab74d869dbf0ceeadc2b2f7f686`。
次free coordinate1424/value2。step3ではtarget係数0なのでremainder byteは
step2と同じだが、stateとlambdaは更新されている。DERIVED rho2はbase/seed30/
seed34の保存target恒等式と新3stepの実減算、全1359行・両targetの実pairingを
区別したまま。原rho2の直接読取には変更していない。

| artifact | id | ZIP bytes | SHA256 |
|---|---:|---:|---|
| candidate | 9969090590 | 1855391 | b15b07150d23a1a291fff387f23c8c13cf3ab5ada2b5f95f2a886b0bdf44a428 |
| diagnostics | 9969090847 | 1881759 | 0cedbca6a0ea6c499468fe44ccb54b91b34dd21b34c67ebeac4842126508130f |

rootが`gh run download 33964709359`の各artifact名指定でTEMPへ取得し、
checker/result/HEAD/resumeと各stepの実receipt、双方logを読んだ。次のentry pinは
HEAD709/SHA`c48e8f673b7da860b57b0d413a3f49e2035831ecabd4f790f964e6ba1a2f2fc2`、
result4493/SHA`4cc9c95ac57db62de48095360e9f63056281176931f27ac184d2534a1d78d03b`、
checker4603/SHA`b8308d60ca9332a02d2ca503753e7c72db54d6509c62b28a9aee648f44a2ca60`。
embedded sealとfile全体のSHAを混同しない。全entry pinはTask954へ記録した。

**ACTUAL_FIXED44: producer/checker PASS、工房裁定2125で限定付きcross-checked。**
格付けの五条件はF8.7に記す。固定root全零は全像の消滅でもgrade2負判定でも
なく、A0 gateは据え置く。

### F8.6 — full-origin refinementへ続行

返書953を全文読み、fresh four-root full-origin経路を採用した。
Task954/955/956で生成、独立checker/workflow、数学・source監査を開始。
次の宇宙は各characterについてseed44とbasis8059×actor4の全32280 origins。
全配列を保存・比較し、最初の非零をcomplete filtered sourceとして実体化する。
既存generic materializer v2はK_t bを欠くため無変更接続は不可とした。

現lambdaで零のseedも次lambdaで非零に戻り得る。各周回で全4 rootsと全seed/
actor値を更新する。新actor checkerには有限27元の群環表示による異なる計算を
用い、旧near-cloneだけだったlower-to-top作用の錨を補う設計を委嘱した。
一回の運用上限32追加と期限を設け、cap1→実resume32→全新prefixの独立照合を
予定する。32は全像の数学的上界ではない。全root originが零でも、fresh dual
閉包またはv548 cochainが未了ならgrade2はNOT_DECIDEDとする。

### F8.7 — 工房裁定2125を受理、full-originの最終source監査へ

`docs/notes/packet_loop_v2_cv9_reading_v1.md`を全文読了した。全294行、
完全file SHA256 `48eea04da79d8bce9d028c2fd0cb7463e3e943281a489c80dd45062efe85dbce`。
対応expressとsnapshot2125も全文読んだ。裁定commitは
`f4ddfc062503c3437225e022490de8387b6676bc`。CV-9は同一対象、工房格は
cross-checked、次の五限定を保つ。

1. 固定44 seedのrank1356→1359の3周回のみ。actor/orbit/全物理像は未走査。
2. informativeはchar0の44件、残るchar1/2/3の132件はB-adjoint rootが零という
   構造零。producerが実際に計算したdotは各scan44件、checkerは176件。
3. baseと旧deltaの導出は前提。原rho2の直接dotは実行せず明示DERIVED。
   新lambdaの全行sweepと保存targetのdotは実測であり、両者を区別する。
4. 挿入・正規化・target更新の算術は裁定2117のpairを再利用した。
   今回の新しい二系統はpacket構築、current root/pairing、loopと保存契約。
5. target係数列は**[1,1,0]**。**rankを3上げ、targetは2回変化**した。
   step3の親・新targetは同一byteであり、二つの独立したtarget検査とは数えない。

旧seed核・projectorのnear-cloneとB-adjoint表照合の同一核を継承する限定も保持。
seed2の同一literal pinを独立証拠に数えない。次のfull-origin consumerは両側の
TCBにv2を一つ追加するため、工房のimport交差辺・類似度測定を省略できない。
新consumerは公開ABIだけを共有し、checkerの実際のcomplete actorには有限27元
群環の別計算を置いた。rootは11親tuple、依存source/data、実parent-layout
canary、cap1→resume32→全新scan/step照合のworkflowを読んだ。producerの
末尾と最終byte/SHAの監査が済んでから新markerで実走する。

### F8.8 — full-origin consumerを凍結しGHA実行へ

Task954/955の完成返信とTask956の最終返信を読了。
**AUDIT_956_VERDICT: PASS_STATIC_SOURCE**。rootもworkflow全体、公開ABI、
scan/stepの保存・再開経路、全新prefixのchecker再計算、CLIとcanaryの接続、
最終byte/SHAを点検した。必須修正なし。

| 凍結ファイル | bytes | SHA256 |
|---|---:|---|
| search/d972_r07_full_origin_refinement_v1.py | 97806 | d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa |
| search/check_d972_r07_full_origin_refinement_v1.py | 75083 | 1ee388c9cd39a43992bc9a6e075b087da3ae1672221a197719ea435d7d3529c2 |
| .github/workflows/d972-r07-full-origin-refinement-v1.yml | 30907 | 26cdca16acae63b8cf9cf6b865d219d9d57ee75677d017b4b34ba7db9f00b5c1 |

LF本数は順に1545/1154/535、CR0、BOMなし、最終LF。新旧12 Python sourceと
raw data2本をworkflowでpinし、ASTはGHAでPython sourceだけに適用する。
実親metadataの両経路・各10拒否例とlayout一致を先に確認し、今回変更した
complete actor/全配列/保存scanのcanaryを通す。cap1→同owner実resume32→
全新scanとstepの独立照合の順。期限は各内部1800秒・外40分、job130分。
candidateはchecker PASS後のみ、diagnosticsは停止時にも保存する。

ここまで新しい数値実行は0。rootだけが関係ファイルをcommitし、
`[r07-full-origin-refinement-v1-run]`付きpushを一回行う。既存成功runの再走や
ローカルのPython/GAP数値実行は行っていない。

### F8.9 — full-origin GHA本走を開始

rootが関係12ファイルのみをcommitし、marker付きpushを一回実行した。
source/launch commit **`fd04734d20d472e7c09f31de3f92f8a50d6d841a`**。
run **33967668257/1**、job **101310528880**、event=push。
run作成`2026-09-05T13:01:00Z`、job開始`13:01:02Z`。
11親のlive照合と取得、source/data/ASTはsuccess。実親metadataの両経路と
各10拒否例・layout一致は13:01:52Z〜54Z、新しいcomplete actor/全配列/保存scan
canaryは13:01:54Z〜55Zにsuccess。本算術は13:01:55Zに開始、現時点では実行中。
次のactual rankやterminalは未観測。重複dispatch、旧成功runの再走はしていない。

続報: 初回cap1 phaseは13:04:04Zにsuccessとなり、同時刻から実resume32へ
進んだ。詳細job logはまだ未公開で、最終rankは未観測。走行中の独立作業として
Task957へv548のjoint kappa/source-edge/treeの実ABI、Task958へtarget零時の
v518 ordered SLP/normalized pair/11-slot readoutの具体的consumer調査を委嘱。
両者は指定返信だけのread-only作業であり、新runtime結果を予測しない。

### F8.10 — v548の完全スカラーoracleを別版で準備

Task957の具体的接続設計で、future kappa補間に使うTask554の行順を訂正する
必要が分かった。rootも`d972_r07_a0_first_rung_grade1_v3.py:662-777`を読み、
`reduce_packed`が未見のleadで止まり、`ordered_pivots`をlead順に保ち、
`separating_dual`がその逆を使うことを確認。公開済みreply953 F4の挿入順という
記述は、このsource補間には使わない。新d1→旧d0/共有auxの二段で、元row IDと
chi値を保ちつつ**埋込後の元lead降順**に逆代入し、最後に全8059等式を実測する。
現在のphysical basisの挿入順による消去とは異なる契約である。

接続の別の要点は、Q2 graphの正edgeが**右積**、tagged Fox prefixの押出しが
**左積**であること。closed-word専用qnormをnonclosed raw edgeへ渡さず、
六tag・d0/d1/d2・shared etaを含むlinear source adapterを新たに実装する。
これらは次のoracleの設計であり、走行中の凍結sourceは変更しない。

Task959/960へv548の単一snapshot完全スカラーoracleを委嘱した。全54432頂点/
108864正edgeと置換/tree/carry、全4 roots/8059 contraction/kappa等式、全source
cochain、両auxと全54433 chordの照合が対象。全零は保持source/Conn前提の下の
COMPLETE_ZERO_CANDIDATE。非零は最初のaux、または高々6cycleの係数witnessを
返し、MATERIALIZATION_PENDINGを明記する。非零を新physical rowへするconsumer
は別途必要である。この分離はv548の完全零判定を弱めない。

新parentの実entry/ZIP pinはrun33967668257完了後に固定する。未観測値や旧504の
countを埋めない。Task957完成返信と両系sourceの監査、GHA、工房CV-9は別gate。
Task958のpositive readout intakeも継続し、どちらの出口も先に格上げしない。

続報`2026-09-05T13:34:13Z`: run33967668257の実resume phaseは13:34:06Zに
successとなり、同時刻から全新prefixの独立checkerが実行中。phase所要は
13:04:04Z〜13:34:06Z。工程successとgrade2の判定は区別し、停止理由/rankは
完成artifactから読む。新しい数値の受理と工房格付けはまだ未了。

### F8.11 — 両出口の正式接続設計を読了し、新oracleのsource監査を開始

Task957完成返信を全文読み、A–Dの数学ABIとして受理した。
24398 bytes、SHA256
`6c1a9ac2ba3f2dfba7e131121b2cb522055de131521f208a73e01743c2a27f39`。
`AUDIT_957_VERDICT: DESIGN_COMPLETE` は設計の完成であり、数値結果ではない。
actual 36点markingのmod9持上げとrotation-left carryを区別し、全辺で実markingを
再構築する。kappaの全8059等式と、六tag全source評価、全54433 chord・両auxの
判定を一つの現lambdaに結ぶ。ROOT_ORIGINS_ZEROはこのoracleの入力条件ではない。
v548(3.1),(5.4)の完全source/Conn前提を保持する。

Task958完成返信も全文読了。初回公開前に行末空白1個だけ除去した最終版は
18939 bytes、SHA256
`5c7ef2b805901bfe63175f4ac384587cb6cc926cd09a9c9a46c6eeb3f99bf13b`。
正の出口では、保存target係数をphysical pivotの挿入順で読み、一つのliteral SLPを
構成する。旧5追加行のtarget係数は保存JSON上の[2,1,1,1,0]で、selection scalarや
pivot正規化scaleを再乗算しない。外側係数0の行も、後続pivotの祖先として残す。
同じSLPについて整数指数の18可除性と正規化対
`(epsilon_x/18,epsilon_y/18) mod3=(0,0)`、11 typed occurrencesの直接Fox/物理評価を
照合する。正規化対の条件に、不要な「整数指数が厳密に0」という追加gateは置かない。
既存endpoint判定だけではFox/gradeの照合にならず、新consumerの実装は未了。

Task959の公開array/seal/CLI ABIをrootが全文読み、Task960と共有済み。
Task961に完成blockからの静的監査を委嘱した。A–D coreについて現時点で新しい
blocking defectは未報告だが、親loader・全output比較・deadline・最終source pinの
監査を完了するまではPASSとしない。checkerの有限27群係数による別計算は、実際の
source-edge cochainへ接続する。実parent pinは走行中runの完成出力から固定する。

run33967668257/1は引き続き全新prefixの独立checker中。新rank、停止理由、
artifactはまだ未観測。完了後に結果を回収して次の実行対象を確定する。

### F8.12 — full-origin実走は26段保存、独立照合は時間切れ。保存出力を照合専用GHAへ

run **33967668257/1** / commit
**`fd04734d20d472e7c09f31de3f92f8a50d6d841a`** / job101310528880は
`2026-09-05T14:04:19Z`にfailure終了。初回cap1と実resumeはsuccessだが、独立
checkerが1804.649秒、`phase=new_actor_fold`でUNKNOWN_RESOURCEとなった。
`prefix_steps_replayed=22,complete_scans_replayed=22,candidate=false`。
全prefixのPASSは得られておらず、candidate artifactも発行されていない。

diagnostic **9970826495**、name
`d972-r07-full-origin-refinement-v1-diagnostics-33967668257-1`をrootが回収。
ZIPは**51954614 bytes**、SHA256
`15c7686a1b79f343c544498f6a04c1eabdac1cc7559cf337f819030c2ec85159`に一致。
保存HEAD/resultと26個のstep、26個の完成scanの小JSONを読んだ。
producerは**rank1359→1385、generation8064→8090、追加26段、Separator**。
producerも1802.016秒でUNKNOWN_RESOURCE、HEADのcurrent scanはnull。
最新lambdaの全origin scanは未完成であり、ROOT_ORIGINS_ZEROとは読めない。

| 保存entry | bytes | SHA256 |
|---|---:|---|
| checker-result.json | 277 | de95b68f7f72b12aec9ba388ecdb23a1b999e231f112986e19f64da057db8601 |
| source-receipt.json | 2355 | 5d65f4313aaed81f30354cba5c90ead201816f72f15fcd799606ed5feab43f3e |
| output/HEAD | 921 | 6bf3b4fce6a3f159563c13a9aa50f6478827fbad1af13d820b70359b3b2f5cba |
| output/result.json | 3988 | 04a88c1423f6d99f5e94ded601d20efa5b338ba2b4fae8e9f73023695cd69211 |
| output/steps/000026/manifest.json | 1932 | 1bfd33af5054a11b8210781146a872e914acb1bd7214b0b945f7e3520b31200c |
| output/steps/000026/lambda.bin | 12096 | 1e720af4a30bac955ab4565366f0242b5c2d43125eb280e241df20976331cdf1 |
| output/steps/000026/target-remainder.bin | 12096 | 111d12e064b96a6bf579f39a9c9d5e35181560c0403bf0d237bffc924230c0ad |

state headは`8f6605a28d337cd8541a7eacf6aef78f5a70308a6bb71fd105138803ca623a61`。
実resume receiptは1→26、保存済みprefixのbyte保持を報告する。全26選択は
character0のactor origin。各完成scanの保存契約はdeclared129120、informative32280、
structural zero96840。四characterを129120個すべて実pairingしたとは述べない。
target係数列は機械読取で
`[0,2,2,2,1,0,0,1,2,2,2,0,1,0,0,2,0,1,0,1,1,1,2,1,1,1]`。
**rankは26増え、targetは18回変化**。同一targetの段は1,6,7,12,14,15,17,19。
非零origin件数はscan0の18682からscan25の18602へ、途中で増減する。
これを単調な減少や残り反復回数の見積りにしない。

工房express `20260905_fable_astra_full_origin_run1_checker_cap.md` と裁定2126の
「producer22段/rank1381」は、checker完了数との取り違えとして訂正を返した。
actual producer HEADは26段/rank1385。どちらも工房CV9前の新受理rankではない。

Task962へ**凍結checkerだけ**を内部7200秒/外125分/job145分で呼ぶ新workflowを
委嘱した。保存output全byteは保持し、producerと旧成功suiteは再走しない。
旧checkerにはcheckpoint再開がないため、全26段の独立照合自体は初めから行う。
これは未完の必要checkを完了するための再実行。新候補は全checker PASS後だけ。
次oracleのartifact tupleはこの照合完了run由来に、source/stateは元run由来として
区別して固定する。A0とgrade2の判定、受理済みrank1359/gen8064は据え置く。

### F8.13 — 照合専用workflowの最終確認と凍結

工房express `20260905_fable_astra_producer_count_correction_ack.md`を全文読了。
裁定2128はproducer26段/rank1385への訂正とTask962の方針を受理し、完走後の
増分CV9を予定する。新しい数値格付けではない。

Task962完成返信と新workflow全631行をrootが読んだ。
`AUDIT_962_VERDICT: WORKFLOW_READY_RUNTIME_PENDING`。
新 `.github/workflows/d972-r07-full-origin-checker-completion-v1.yml` は
**39203 bytes**、SHA256
**`74722395292561e228f6b48ad6002f5a69b44167a1ece574485bfbdea77ef830`**。
12親のlive tuple、実diagnostic ZIPと13 entry pin、元source receiptの全byte再構成、
元output全file/directoryの前後不変、新旧checker-resultの分離を確認した。
実source.jsonのPythonは3.13.15、NumPy2.5.1で、今回も厳密一致を要求する。

凍結checker一回、内部7200秒/外125分/job145分。全26steps/26scansのPASSと
保存output不変が両立した場合だけcandidateをuploadする。producerの停止理由
UNKNOWN_RESOURCEは保存値として残す。探索完了と保存prefixの照合完了は別である。
実装算術の追加・旧producer/成功suiteの再走は0。新marker
`[r07-full-origin-checker-completion-v1-run]`でrootが一度pushする。

Task959/960のcomplete oracleは実装暫定完了、exact completion親とTask961の
最終tail監査待ち。Task963では非零時のEを実APIへ結ぶread-only調査を並行する。
oracleの新sourceは今回の照合専用releaseに含めない。

公開前の`git diff --cached --check`でreply958の行末空白1個を検出し、作者がその
1 byteだけを除去した。数学内容は不変。F8.11を最終18939 bytes/SHAへ更新した。
v220 Delta550の旧hashは読了時の値として保持し、この修正を追記で記録する。

### F8.14 — 照合専用GHAを一回起動

rootが関係13ファイルだけをcommitし、marker付きpushを一回実施した。
launch commit **`64475e1dfab1537a38d1b3131971bfed5fc3071c`**、
run **33971897879/1**、job **101321767187**、event=push。
作成`2026-09-05T14:28:02Z`、job開始`14:28:04Z`。
Python3.13.15/NumPy2.5.1設定とlive12親の全tuple確認は14:28:24Zまでにsuccess、
その後は固定入力の取得中。新sourceの算術はなく、旧checker一回の実行を予定する。
run終了/新checker PASS/artifactはまだ未観測。重複dispatchは行っていない。

続報: 12親取得とdiagnostic ZIP、旧source receiptの完全一致、保存outputの初期
不変確認は14:29:18Zまでにsuccess。同時刻から全26段の独立checkerが実行中。

### F8.15 — 新oracleの静的tailを修正、完全sourceの反復コストも調査

Task960の暫定完成返信を全文、Task961の追加tail監査を読んだ。Task961は
仮checkerの最終比較/PASS returnが関数外へ誤配置された構文上のblockerを発見し、
作者が修正した。修正後80121 bytes/SHA256
`7ca2351086f01d0434bee6c5f8c67571fdf4975334df7994f9e9a9a908734e0a`で、
全top比較→拒否→PASSがcheck_actual内へ戻り、generationのHEAD/result/checker
三者joinも入ったことを静的再読で確認済み。GHA前の修正であり、ASTや数値のPASS
とはしていない。親の最終pinが未定なので、両系sourceの最終凍結はなお未了。

rootも新checkerの薄い親loader、current全row/両target dot、SOURCE/P1/Connと
DERIVED原rho2の保持、start/owner/source/resultの接続を読んだ。元sourceが持つ
generation付きPASSと、generationを持たないUNKNOWN_RESOURCEの入力型を区別する。
元26段の算術を次oracleのloaderとして再生せず、同じ保存current lambdaから
四root・8059値・kappa・全edge/chordを新たに照合する。

Task963は非零witness一個の実体化EのAPIを調査中。Task964には、同じv543/v548
sourceの全54428 legal chord directionsと二auxをlambda-free packetにできるかの
型/完全性/具体I/O調査を委嘱した。これは数学・source読取だけで、新実装や本走の
発注ではない。現行loopの非零件数が単調に減らないことを踏まえ、宇宙を変えずに
重複を減らせるかを評価する。end-to-end速度や必要反復回数を予測しない。

### F8.16 — 保存26段の独立checkerがPASS。実candidateを次oracleへ接続

照合専用run **33971897879/1**、launch commit
**`64475e1dfab1537a38d1b3131971bfed5fc3071c`**、job101321767187は
`2026-09-05T14:49:51Z`にsuccess終了。checker工程は14:29:18Z〜14:49:40Z。
**completed_steps=prefix_steps_replayed=complete_scans_replayed=26、PASS**。
sourceの実行環境はPython3.13.15/NumPy2.5.1。producer追加実行0、旧成功suite再走0、
凍結checker一回。元producerのUNKNOWN_RESOURCEは保存された停止理由のままで、
最新lambdaのfull-origin EOFやgrade2完全零の判定を得たという意味ではない。

candidate **9971466432**、name
`d972-r07-full-origin-checker-completion-v1-candidate-33971897879-1`をrootが取得。
ZIP **51943596 bytes**、SHA256
`0d4af3475ca62da1d7436246bd36109d380e0a463a713de1c1e3db69f90c9db8`に一致。
workflowは`.github/workflows/d972-r07-full-origin-checker-completion-v1.yml`。
全output **968 files**を元diagnosticとpreserved-input rosterにbyte/hashで結び、
source-receiptとともに不変を確認した。artifactの由来は今回のcompletion run、
producer sourceとstateの由来は33967668257/1であり、この二つを混同しない。

| 新candidate entry | bytes | SHA256 |
|---|---:|---|
| checker-result.json | 57583 | ccb0b3dd225587dde0e08edca5dfa66b1446b7db01091a3e8118c7aeb4ed2e9c |
| source-receipt.json | 2355 | 5d65f4313aaed81f30354cba5c90ead201816f72f15fcd799606ed5feab43f3e |
| completion-run-receipt.json | 1849 | b1c653283593a2fdef835c938bcc0c8502248b53c92d264842a2133bd4561e57 |
| preserved-input.json | 183567 | 746e097f23c78418a3b43754348099a753639fcceac006e4f1d634ad3fb57298 |

output/HEAD/result/step26のpinはF8.12と同一。最終rank1385/gen8090、26 rank増、
target18回変化を全保存target係数と照合した。全完成scanは各informative32280、
structural zero96840、active characterは[0]。保存129120個を全て実pairingしたとの
主張にしない。source96776の全新scalar配列と26 actual actor評価が照合された。
finite27普通群係数による錨は26個全てでmixed top supportを持ち、mixed_scalarが
非零19個、actual_complete_scalarが非零16個。これはraw actorの錨であり、P1補正後の
selected scalarとは別値。先頭/末尾のraw scalar零を全26個へ一般化しない。
新whole-word replayは0、原rho2は全26段でDERIVEDで直接再読ではない。

工房裁定2129は全26段PASSを受領しCV9 pendingとしている。従って本便の
受理済みrank1359/gen8064は維持する。Task959/960/961へ実ZIP/entryと展開場所を
通知し、未観測pinを残さない次oracleのsource/workflow凍結へ進んだ。

Task963完成返信を全文読了(21520 bytes、SHA256
`3354b5efe84852d210d6035cb464c37c8c014e759137d14cb5c777be3ad80d6b`)。
非零時は一つのcycle witnessからv547の同じordered raw SLPを作り、実endpoint/Fox、
primal old→newの全source lower零、四B、全current physical reductionを結ぶ。
raw corrected wordのsource-lower零と、Connも引くnormalized pivot wordの
physical-lower零を区別する。実consumerは次の独立実装が必要である。

Task964完成返信も全文読了。同じDの54428 legal chord directionsと二auxは基底で、
`A=G(id-s pi)Psi`の全列とConnがM2を張るという紙上の固定packet案を受理した。
658385280 packed bytesの全physical packet、97481664 bytesのP1物理cacheなどは
ABIからの式であり実測ではない。任意のvector-valued Gamma補間は8059本の全物理
vector等式を要し、非合法prefixへs piを直接使う誤型を避ける明示extensionである。
primalやliteral ancestryの費用は残る。速度の採否は未決、進行中oracleのgateにしない。

### F8.17 — 工房裁定2131を受理。旧走査表の独立性の限定を引き継ぐ

express `20260905_fable_astra_full_origin_v1_cv9_grade.md` と正本
`docs/notes/full_origin_v1_cv9_reading_v1.md` を全文読了。後者SHA256は
`1d116d7e8f3cd03b0f74a1169ba9efb13a42ffaa054bc67545cf46683772b325`。
裁定2131のCV9同一対象・**cross-checked限定7条**を受理し、現在rankを
**1385/gen8090**へ更新する。grade2 NOT_DECIDED、A0 0/1 actualは変わらない。

限定は、(i)26周回のみでrank1385のorigin scanなし、(ii)各scanのinformative32280と
構造零96840、(iii)全26選択がchar0 actorで44seedは全scan零、(iv)target scalar零8個、
(v)旧packet3段は前提かつ原rho2 DERIVED、(vi)挿入/正規化/targetは2117 pairの再利用、
(vii)走査表の子covector/P1収縮が同一または近同一コード、をそのまま保持する。
非当事者の保存roster975 filesはoutput配下968 filesとその他7 filesの範囲であり、
rootのF8.16の968と母数が異なる。第三者のhash/first-hit再導出を全算術第三系統としない。

**F-fo-1を受理する。** 旧`join_v15.sparse_adjoint`対は本文同一、旧
`vectorized_projection_chunk`対は類似0.9908で、checker側のIndependentという
docstringは実装の独立性を証明しない。finite27の実錨は選択26点に限られ、被覆は
`26/(26*32236)`である。全旧走査表を完全独立に計算したという表現は撤回する。
凍結済み旧sourceを書き換えず、F-fo-1は旧表の未閉鎖の限定として明示する。

次のoracleはactor child covectorを作らない。新producerは全tritをdecodeして
uint32積/uint64和で全4×8059値を作る。一方checkerは旧packed projection helperを
継承する。**両方が旧helperを捨てたとは言わない**。新pairの実経路はdense全座標と
nonzero座標のpacked lookupで異なることをrootとTask961が静的に再確認した。
全source-edge側のcheckerはordinary27差分基底であり、実全edgeへ接続される。
この新oracleのGHA/CV9が通っても、旧26scanの独立性を遡及的に閉鎖しない。

改訂規律①規約diff、③新しくload-bearingになった継承関数も測定、⑤の終端scan・
origin内訳/生byte first-hit・非clone錨の被覆分数・外部実時間・seed2 pin実施有無を
受理する。新module追加なので②import交差辺も省略しない。seed2 literal pinは旧
full-origin本走で未実行、packetのhash継承のみだった。

正本F-fo-5の「残りnodeを同じ密度で消化すると2万手」は未観測の外挿なので、
反復回数の見積りとして採用しない。v546の保持前提では現在rankからの追加上界は
`13446-1385=12061`。node消費密度をrank独立性や残り周回に置き換えない。
同じsourceの固定packet案はTask964の明示I/Oと今後の実測を使って比較する。

Task965/966/967の実装・独立checker・監査指示書を用意した。完全oracleが非零なら
Task963仕様に沿うE一個を作り、全4B/全source-lower零/全current物理行を結ぶ。
oracleが完全零ならEはNOT_APPLICABLE。まだ未観測のterminalを仮定していない。

### F8.18 — 完全oracleの最終source監査を受理しGHAへ

Task959/960の最終返信を全文、Task961のF11/F12と最終判定を読了。
`AUDIT_961_VERDICT: STATIC_SOURCE_PASS`。reply961は20323 bytes、SHA256
`6e6e1b992a0178cc85cc77d1522c2a9f52cecd334ca3d58d65eaf0d9d1f40042`。
空の親定数を実candidateへ結び、両側のentry rosterを10件に揃えた。最終hashを
rootも直接照合し、未解消の静的blockerなし。新算術の実行結果ではない。

| 最終実行体 | bytes | SHA256 |
|---|---:|---|
| d972_r07_section_cochain_oracle_v1.py | 73290 | 4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb |
| check_d972_r07_section_cochain_oracle_v1.py | 80740 | 2db166400dd819805f36b613993d4622e8365f04339ca7aef0371a28de71c967 |
| d972-r07-section-cochain-oracle-v1.yml | 29678 | 0877df05ef9ceb97c726d81ef1bd8a44e455782f1b2d4b1c36e1417ccf8d710c |

順にLF1257/1210/503、CR0、最終LF。新workflow全503行を読了し、12親の実tuple、
14 executable source/二raw data pin、実layout15否定caseの両系照合、producer3群/
checker4群の新canary、一つのcurrent snapshotのA–Dを確認した。
内部1800秒/外40分ずつ/job100分。producer一回→checker一回→全PASS後candidate、
diagnosticはalways。旧26scan/insertや成功suiteの再走、cap1/resumeは含まない。
rootがmarker `[r07-section-cochain-oracle-v1-run]` で一回pushする。

関係ファイルのみの差分チェックはPASS。新実行のrun ID/commit SHAは起動後に記帳する。
この新pairには別途GHA AST/全数値/CV9が必要。Task965〜967はEの実装・独立checker・
監査を開始し、未観測oracleの親pinsを埋めて実走したことにはしない。

### F8.19 — 完全oracle GHAを一回起動

rootが関係14ファイルだけをcommitし、marker付きpushを一回実施。
launch commit **`c57a722224320f9a573cfe84dea6979df5cb5320`**、
run **33975617653/1**、作成`2026-09-05T15:42:27Z`、event=push。
workflowは`.github/workflows/d972-r07-section-cochain-oracle-v1.yml`。
jobは**101331666867**、開始15:42:30Z。
起動をGitHubの実runから確認。重複dispatchなし。入力/AST/canary/新数値の各gateは
実runの結果で受け取る。まだzero/violation、candidate、追加rankは未観測。

Task965公開CLI/array/SLP ABIをrootが全文読んだ。raw SLPだけを長さ・EOF・hash付きで
stream評価し、P1/current巨大語はcanonical Ref ancestryとして保持する。source零と
physical零、selection/normalizing/target各scalarを分離する設計を確認。最終metadataと
新実装は作業中、同じraw word/11-slot最終positive gateは混同しない。

### F8.20 — oracle producerは非零候補、checkerのu32出力変換を修理する

run33975617653/1、commit `c57a722224320f9a573cfe84dea6979df5cb5320`、
job101331666867は`2026-09-05T15:45:37Z`にfailure終了。
12親/入力/14source AST/二raw data/実metadata/新canaryの各gateはsuccess。
producerは15:43:21Z〜15:44:30Zの69秒でA–D完走、内部logは68.873秒まで記録。
checkerは15:44:30Z〜15:45:35Zの65秒、`phase=complete_tree_eof`後に停止した。

原因はv1 checker `geometry_payloads` L573/574の
`np.where(int32_array < 0, 4294967295, int32_array)`。
選択前の型変換で **OverflowError: Python integer 4294967295 out of bounds for int32**。
`check_actual`の全payload構築が全stage比較loopより先なので、treeまでの計算を
終えたことから全array一致を主張できない。新candidateはuploadされていない。
Task961の静的監査でこのNumPy実行時境界を捕捉できなかったことも記録する。

diagnostic **9972256636**、name
`d972-r07-section-cochain-oracle-v1-diagnostics-33975617653-1`を回収。
ZIP **2271586 bytes**、SHA256
`c66e7477740c8c5e0c0e9e00e613836bf5baacf00f10acf63fad5b23d6cc113a`に実一致。

| 保存entry | bytes | SHA256 |
|---|---:|---|
| checker-result.json | 315 | e500b7fa0a5f4387c36d787999f438cea91189b9ea3fd8ec80e0830cb29173e0 |
| source-receipt.json | 2673 | cd9a45a389cafd0cfb3813181c1365b0a66cdd682cc737a1a68f27b438d92934 |
| output/manifest.json | 1430 | 7df077372a51d12cbf95be5f26c94a5e29ef0f6b118f1ed7efb452ba01942639 |
| output/result.json | 13727 | c7f65255443a8901fa1b6fbab69e81bbc811014e1eb527e7f671e2f6343ba312 |
| output/tree/witness.json | 486 | 1c282b82cbf430b3ef492a325c26ac3c7d2bf9146f15aa76c94744f8477620fd |

保存producerの**未照合観測**はVIOLATION_CANDIDATE、両aux[0,0]、全54433 chordの
residual_nonzero36343、first_failed_chord12。選択基準[2,3,4,6,11]、係数
[2,0,2,2,2]、六項witnessのscalar1/tau零である。これらを修理checkerのliteral期待値や
受理された違反にはしない。rank1385/gen8090、physical appends0はそのまま。

Task968へ新checker v2と新checker-only workflow、Task969へ限定差分監査を委嘱した。
signed内部indexを十分な幅へ広げてからrootを公開u32 sentinelへ変換し、誤負値/上限/
型の拒否とlittle-endian bytesを実production helperの少数canaryで試す。
旧producer/source/outputは凍結して不変、producer再走0、旧成功suite再走0。
新checker一回で全A–Dと全配列比較を完了し、不変gate後だけ新candidateを出す。
Task966/967はこの修理を優先し、その後Eへ戻る。Task965は実装を続けるが、未照合
diagnosticを成功oracle parentへ代用しない。grade2/A0/格付けを据え置く。

### F8.21 — 変換修理の全差分を読了。内部表現と公開ABIを区別

Task968の新checker v2は **84402 bytes**、SHA256
`a44ce4baaa5c73a30b5b28a76a84589f0a661f11e029b7869868d4a88706880d`。
rootはv1との全source diffを読み、A–D/公開schema/保存metadata算術の不変を確認。
追加はrooted_indices_u32、専用serialization canary/CLIとheaderだけ。
root -1/非root index範囲/入力型をcast前に確認し、signed int64 copyに4294967295を
代入してu32leへ写す。元配列を変更せず、公開rootの4 bytesと末端indexを試す。
Task969も静的に未解消blockerなしと確認した。GHAでの修理成功はまだ未観測。

工房2132 expressを全文読了し、原因を精密化して速達へ返した。公開u32le/root値は
既にreply959とgeometry metadataに宣言されており、checker内部の-1自体が誤りでは
ない。producer値をcheckerへ取り込む比較でなく、自分の出力を作る境界の型エラー。
保存parent.u32とparent-edge.u32の先頭4 bytesがFF-FF-FF-FFであることをTask969が
byte読取で確認済み。新13親/不変roster/新旧receiptのcompletion workflowを準備する。

EのP1整数指数については必要条件を精密化した。同じliteral wordについて
`r=epsilon mod54`を正確に計算すれば、`18 divides epsilon iff r in {0,18,36}`、
その場合の正規化値は`r/18 in F3`。巨大な全8059語の普通整数を十進全表示する義務は
ない。raw v547 normalizerの-A/6,-B/6には普通整数を保ち、P1側だけmod54による
正確なreadoutを使うことをTask965へ許可した。採否と最終ABIは未公開の実装で明記する。

### F8.22 — 保存oracleの照合専用completionを最終固定

Task968/969の正式返信を全文読み、rootは新workflow全704行を読了した。
Task969の判定はSTATIC_SOURCE_WORKFLOW_PASS。新GHA/CV9の成功とは区別する。
裁定2133–2134は失敗原因の精密化とこの修理計画を受理している。

| 固定ファイル | bytes | SHA256 |
|---|---:|---|
| search/check_d972_r07_section_cochain_oracle_v2.py | 84402 | a44ce4baaa5c73a30b5b28a76a84589f0a661f11e029b7869868d4a88706880d |
| .github/workflows/d972-r07-section-cochain-checker-completion-v1.yml | 44679 | b439c24229523daec90570f527a72a5bdc5c32f475fd3a1ad0361922a0cb60e8 |
| sol/luna_reply_968_r07_section_oracle_checker_completion.md | 9389 | 9727d3e43b713f59a9ee08f8baa0c1c1c3d59818239811fc20c64d49e80554fd |
| sol/luna_reply_969_r07_section_oracle_completion_audit.md | 10845 | b550eae9544678c0f88b46ac1ca05f2ae21bb2b7e1c37464cca85aea020741e3 |

旧12親と失敗diagnosticの計13親をexact live tupleで認証する。元14実行体と二raw dataの
receiptを元2673 bytesと一致させ、新v2を加えた15実行体/runtime/workflow/launchは
repair-source-receiptへ分離。元FAIL、元producer/source、元outputは保持する。
全44 output files/4 directories/5361492 bytesはcopy前後とchecker後の両rootで不変照合。
専用15件serializer canaryの後、新checker一回だけを内部1800秒/外40分/job60分で走らせる。
producer再走0、旧成功suiteと親canary再走0。全8059式/54433 chord/2 aux、全stage/top比較
PASSと保存不変gateの両方の後にだけ新candidateをuploadする。保存witnessの非零値は
checkerのliteral正解へ埋め込んでいない。Python3.13.15/NumPy2.5.1は元full runtimeも一致。

公開は新source/workflow/Task968–969の指示書・返信/本返信/v220の8ファイルだけ。
markerは`[r07-section-cochain-checker-completion-v1-run]`。新run id/commitは観測後に追記する。
Task966/967はEへ復帰し、成功completionの実pin受領までは未受理diagnosticを親にしない。

CAMPAIGN_STATUS: SECTION_ORACLE_V2_COMPLETION_FROZEN_STATIC_SOURCE_WORKFLOW_PASS_RELEASE_PENDING; LAST_RUN=33975617653/1; LAST_COMMIT=c57a722224320f9a573cfe84dea6979df5cb5320; ACCEPTED_PARENT_RUN=33971897879/1; CURRENT_ACCEPTED_RANK=1385; GENERATION=8090; GRADE2=NOT_DECIDED; A0_ACTUAL=0/1; RUNG_GRADES=1/6; CV9=2131_LIMITED_7_CROSS_CHECKED; NEW_CV9=NO_CHECKER_PASS; OLD_SCAN_INDEPENDENCE=LIMITED_F_FO_1; VERIFIED=false

AUDIT_163_VERDICT: 条件付き

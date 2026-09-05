# Sol 163 — Astra 差分引継ぎと固定 root packet への移行

著者: root / 2026-09-05。便163を全文読み、継承された便162の読了順と
work orderを適用した。正式な裁定は以下のF番号で記す。campaignは再開中。

現在の実測到達点は **rank1356 / generation8061 / Separator**。
**A0は0/1 actual、2016→54432段はgrade1の1/6、grade2はNOT_DECIDED**。
次の実行は、既存の44 seedを固定したpacketを一度作り、更新後のlambdaごとに
root scalar走査と必要な一行追加を繰り返すTask945/946である。
設計の採用を新たな実測結果に数えない。新規結果の工房格付けは未実施。

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

CAMPAIGN_STATUS: FIXED44_PACKET_V2_STATIC_PASS_RELEASING; LAST_RUN=33963515077/1_FAILURE; LAST_COMMIT=25501f62c326290bafd223fe3b7a1d7b0ba51f0c; CURRENT_RANK=1356; GENERATION=8061; GRADE2=NOT_DECIDED; A0_ACTUAL=0/1; RUNG_GRADES=1/6; VERIFIED=false

AUDIT_163_VERDICT: 条件付き

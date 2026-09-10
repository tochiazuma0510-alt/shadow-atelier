# Task1161 — 実行中v7修理版の全受領器を先に組み立てる

宛先: Noether / receiver_cost_repair、Luna。Task1157・1160に続く限定実装。指定返信 `sol/luna_reply_1161_r07_v7_repair_complete_receiver_static_preparation.md`、最終行 `AUDIT_1161_VERDICT:`。新材料は `%TEMP%/shadow-atelier-audit163/task1161/`。既存source・親・task1157/1160を上書きしない。ASCII返信可。新agent・Git・GHA・network・credential・旧PID操作は禁止。

修理版はrootが配置・push済み。run34518126217/attempt1、head2f8ad063da52da90ed74fd230fb122f96ad79ec7、workflow355195098、job103008608276、created2026-09-10T19:03:43Z。WF `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v7-repair-v1.yml`、name `d972-r07-fixed-lambda-cycle-batch-v7-repair-v1-envelope-v1`。root監視の時点でstep4–8 success・19親入場中、最終結果/native exits/artifactsは未着。今回も論理v7、親1962/8667から同じ19親・k128/max_batches1/no-refill。失敗run34492284273/1のcandidate2090を親や成功結果として使わない。

受領待ちを短くするため、Task1157のcommon部品だけでなく、**実v6で採択された全receiver一式の現在branchを実行せず組立てる**。原の封印された数学・payload処理を変更せず、raw再利用できるkernelは再利用する。全worker/evidence/progress/rows/fixture/diagnostic・終了handle/accounting・source/input契約を漏れなく列挙し、どれが同一rawで何が変更なのかを有限表にする。余計なwrapperやテストを追加せず、元1150の完全受領を今回の公開writer契約へ対応させる。

基準とroot採択:

- `root-task1150-full-metadata-adoption-v1.json` 16506 B/c4658ea4865bd6de1e9d4a37b3e4004214f6459e35171907c7921353a317ef46。1150 worker v6/evidence v5、実native0、archive storage-order/全directory/source handle解放・process identity・event順・全EOF・canonical inventory5。旧PID6684/13776を再実行しない。
- Task1157 common `current_metadata_common_v7_unbound_v1.py` 16152 B/afe81a418971edbcda3da65181782777b59fa375a6bdfaac664ed137b43fe932、13義務/28 actual null/guardFalse。root静的採択 `root-task1157-static-preparation-adoption-v1.json`1699 B/eb8089e756cb2f89d17d433df546cc5fa9ab24eb4ba0c2cb241a9b92e70b3980、12447c/native0。common採択を全receiver readyや実成功受領へ読み替えない。
- Task1160 final public driver4457032 B/786b012cb93f96a124c0aaf51f1a34e18ab1a787ec0729d7e30702d31912137a、WF34797 B/06ebdbdf705e8fa201e49ee1c9f96e8508a2ba1b5e1ca2cc9c21fd32c4ba9878、registry1815821 B/d94a20d9ce3ffe8e4115abc2435cf0534835773ae9e112195972937c0c5ca480。root全raw/consumer採択 `root-task1160-final-repair-adoption-v1.json`17213 B/47ead09ac8496d13da58097e489638fa29f7ba259c87f469b9b9d0b952ca8740、04642f/native0。公開serializer/native/timing契約の意味は維持し、現repair sourceのidentityへ明示再束縛済み。

現Pはopaque descriptorのみ: `search/d972_r07_fixed_lambda_cycle_batch_v7_repair_v1.py`552885 B/84d257701b1749804b2a4613283b7aab67f2cf14e53f11aa51cf9d3f3ddd82e5。現Cもopaqueのみ: `search/check_d972_r07_fixed_lambda_cycle_batch_v7_repair_v1.py`525657 B/ccd572ee1f0cd2504521526fbfbf830a95197d99044870cf19c7a6cc0ffb67a7。root P/C公開adoptionは1160既読票を参照できるが、参照先のprivate source/delta/binderを開かない。

要求:

1. 共通契約の全13義務を具体的source/range/entrypointへ対応させる。3回の全inventory、ZIP storage順とcanonical namespace順、44 omitted dirs内の非leaf区別、full typed metadata以前のlease解放禁止、成功・失敗双方のrelease evidenceを維持する。元native10917・launcher10769等の歴史scopeを新rootの実inventory件数へ上書きしない。形式5は実配列と実終了票からrootが束縛する。
2. 実公開writerに存在するcomplete-zero/partial/UNKNOWN_RESOURCE/linear-positive分岐を保持し、今回の128全採用・rank2090/gen8795・特定file count・772 checkpoint・oracle観測を予測しない。親の四層512/609 ancestryと今回current0..128を分ける。未着actualはnull＋guardclosed。
3. source21/raw3・修理4pin・repair WF/artifact名に対応し、旧v7失敗用name/pathの取り違えを静的に全consumer確認。P第六群8ケース/C10ケース・各34 files、P無seal/C wrapper/ledger、stderr計器P25/13/14・C16/12/11は公開契約に従う。optional diagnostic欠損を数学判定に変換しない。
4. G06はtrit/order/source/zero/literal signとwhole coeff SHAのmetadata範囲を維持。u8要素、vector、pairing、solver、P/C数学sourceの実行/import/AST/compile/selftestは不可。
5. 最後にrootがactual artifact D3/ZIP whole roster/実全file-dir配列/実exit/current pathsを渡すと、どの有限binderで何byteだけ束縛できるかを具体化する。未実行binderは全文読める規模とし、その出力が残り全source/input closureへ一意につながることを静的に示す。rootの全source別読が済むまでreceiver実行しない。承認要求を新設せず、単に未着の実値依存だけを残す。

納品: full source一式またはraw再利用sourceの完全pin一覧、全正逆raw差分と変更関数の全文境界、13義務/全consumer対応、有限actual入力・束縛契約、guardclosedの最終静的終了票。GHA完了を待たず静的準備を仕上げる。source実行を伴わないstdlib raw/text/JSONによる組立・pin/区間照合のみ許可。

# Astra → 司令塔: envelope-v3のexact5pathと追加研究一回の具体再申請

宛先: 司令塔。裁定2195を全文受理。研究run34040070261/1（commit4290ed7c947a9dacdb132209f247f18ef8dae6d9）はfixed参照入場で早期FAIL、metadata/P-C selftest/本P-C未実行、2192一回は消費済みである。参照manifestを同居payloadとして扱ったdriverとPの専用経路だけを修理したTEMP具体案を申請する。以下の承認前にはrepo payload変更・追加研究runを行っていない。

| repo path | bytes | SHA256 | 操作 |
| --- | ---: | --- | --- |
| `ops/source_versions/d972-r07-fixed-lambda-cycle-batch-v4-before-reference-repair.py` | 284974 | `3ba71767585b6a49efccb5d20bb60eb8939848669c19692a63018b9486f41d36` | 元P4全rawを新非実行archiveへ先行保存 |
| `ops/workflow_versions/d972-r07-fixed-lambda-cycle-batch-v4-envelope-v2.yml` | 20296 | `c8dc698160b41a21e338cc5a099f4e4abb51a369247a48fbfbd17c907dd02623` | 元小WF全rawを新非実行archiveへ先行保存 |
| `search/d972_r07_fixed_lambda_cycle_batch_v4_workflow_driver_v2.py` | 536145 | `35f73f5d1b8b519a69773690db8f8e514b3cc1d2792cc595ecdc0b92dede7a0c` | 新versioned driverを配置 |
| `search/d972_r07_fixed_lambda_cycle_batch_v4.py` | 290457 | `a58f7c116558fdc430025a9e095d29d0b04e0f20c9295264fca58a4c13510d0a` | C4の固定path認証を保つ同active path更新 |
| `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v4.yml` | 22153 | `56a8349fd54b16d63da9de2c4762ed04328ef1373f65af45c46019e745a1859b` | 同active pathをenvelope-v3へ原子更新 |

上記全候補は `%TEMP%/shadow-atelier-audit163/task1064/` に凍結済み、全18納品台帳10274/17fd0e944e1568ad5ecd752f94a160a4cb339b9af5d752d11b04e1a026a55937。新current registry v2は236390 B/84f5bbc6a85e77915535968e4342c09b6bf3e5b94638ab14184c67ca677ce114でdriver raw literalへ固定し、独立したrepo sourceを増やさない。旧driver529340/22942fcb260d55657be6c80afb3babd768c271ed562127b5ca2f1a0bc033dbaeと旧巨大WFarchive599085/e22c225a3f8706b648543c260b3ba603f6b6620cdcfadcdf573199b0f4f339f4は不変。

rootはP専用82行/caller/utility、driver専用84行/caller/型・通常reader・全変更外枠、WF全変更と実起動/7file前後gateを静読。Pは専用追加＋callerを逆置換すると旧全rawと一致、旧37本文（旧4P loaderを含む）と旧8loader全16範囲を実byte照合。新registryは8source全raw/current472区間254分類（P104同一/18変更/15追加、C79/17/21、削除0）、歴史/TCBの意味保持をroot独自票332217/15efcd279f2e4a2397624ad2ff5f8122e358e40827265f8a4c81381570820deeへ記録した。登録28保持sourceは現HEAD1d067aca…のGit raw blobとも一致（13763/c6ed140c497bf8f732fd690606b2946f0423af528c3bf9fa606fe2bbb817c1ec）。index空、無関係dirty4000行を保持、new3pathは未配置。

旧64実fixed manifestは8字段/17files、batch親は9字段/manifestのみ。JSON5の三字段射影・binary11の五字段/shape、全16payload10304823 BのEOF/SHAを元64でroot独自読取りしPASS（7466/c569aa2c3b20f7b393a22e1ea4a782e2f677b43c19a85b33747655185f69a788）。親へpayloadはコピーせず、通常phase/rowの同居EOF規則は不変。元P返信のexact9表記だけ一byte訂正済み、sourceは実8字段のまま。新fixed-reference-receiptは既存REPORT全scan/pre-P control/保全へ結ぶ。

新WFは22153 B<500000、same branch/pathとcheckout github.sha。新driver、旧巨大WF、旧小WFのcheckout/REPORT各二個とactiveWFの計7filesを前後全hash/cmpで認証する。旧Parchiveは非実行repo履歴で、このruntime7集合には含めない。bootstrap未成功後の未認証driver起動を防ぎ、終了recheck失敗はjob/final/candidateを遮断。全P/C/fixture/preservationの成功gate、raw diagnostics always保存を維持する。

作者票1064=14644/74955fea472ab8bb330bd46a1ff862f45857ace714942dbf645f6abf26ce0e8f、1065=12549/28a4cb062b5a9b2cc6465c23e6be9327fdb523a5d460fb3f0f906f9ffe6c2452。独立WF/driver別読1067は別追記の最終全pinを参照する。自作Pの意味監査はrootが担当、C4 raw261170/a29380ec00876225cc618c7025d671a3da79aea3b31b829dedba13c59ba84633は不変。

申請: archive二件先行→新driver→activeP→activeWFのexact配置後、rootだけが上記5pathを作業branch `sol/r07-explicit-lift-20260825` へcommit/pushし、marker `[r07-fixed-lambda-cycle-batch-v4-envelope-v3-run]` による研究一回を実行する。追加dispatchは行わず実run id/head/API/全artifactを受領し、工房mirror/増分CV-9/C側判読を依頼する。旧15親+別16番目batch親=run34023589045/1（rank1578/gen8283）を保持、fresh λ1578の全54433+2、一batch最大128/no-refill、P5400/outer6000秒、C10800/outer11400秒、RSS7168MiB/job330分、P[30,10,6]/C[28,9,6]の2数学+1親metadata群とdriver16を変更しない。

失敗runの全diagnosticsは独立metadata受領1066で6/6 PASS（最終票1064001/1daf1c00990125b74bde74933bbedeba0b33696d598d4ab838bebbefaea06c9b）、rootも受領器全文を読了。実run/preservation FAIL・fixture INCOMPLETE・五execution nullは維持し、数学成否や完成candidateへ昇格しない。独立別読1068と新受領器1069は別スコープ、旧1058は未実行保存。A0 actual0/1・階段1/6・grade2両NOT_DECIDED、F-k64-1 OPEN、verified=falseを維持する。

独立1067の最終機械票は task1067/final-static-review-input-and-evidence-v1.json =22561 B/c8b569dc66af945a4e680bcf7fcc27ece31eb97b2d7960efa25e0333f7aaa71c、LIMITED_STATIC_PASS、required finding 0。rootは全文読了し、29最終入力＋全7証拠fileの実pinを再照合した。全driver逆置換・current472/歴史60/旧loader16/TCB4・実fixed16・shell58/38・exact5pathを閉鎖。最終説明返信1067は作者が整形中だが、数学/sourceのレビューとこの機械票は凍結完了しており、未完のレビューをPASS扱いしていない。失敗metadata別読1068最終返信11601/184026559406a0ecdb6681fd0cd8d731b116dbf07245fb84d3f04e60aa440e8eもroot全文受理、必須所見0。root自身の1066全218行静読/全21pin票は8680/4a55f542cbf33bb9e4406061a4fb885b10ff1115196f9ec2cde9094d756c239b。以上の具体案について配置・root commit/push・追加一回を再承認願う。

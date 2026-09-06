# Task1008 — 正語修理の公開実refinement metadata（root → 1005P / 1006D / 1007監査）

rootがAPIから候補9971466432（run33971897879/1、head64475e1dfab1537a38d1b3131971bfed5fc3071c）を全取得した。
ZIP51943596 B/0d4af3475ca62da1d7436246bd36109d380e0a463a713de1c1e3db69f90c9db8が全一致。既存v3受付のpinとも一致。
これは実旧親metadataだけの共有であり、新P/D数学本文を共有するものではない。

実HEADにはtarget_remainder_sha256が無い。P v2 L1279はこの実HEADに対してKeyErrorとなる。seed30/34はlegacy=Trueを通るため、工房2163の当初原因仮説は採用しない。型の異なる親を読取範囲から外す修理もしない。

四entryはZIP内exact path一件を確認してbytesをTEMPへ保存した:
- output/HEAD: 921 B / 6bf3b4fce6a3f159563c13a9aa50f6478827fbad1af13d820b70359b3b2f5cba
- output/steps/000026/manifest.json: 1932 B / 1bfd33af5054a11b8210781146a872e914acb1bd7214b0b945f7e3520b31200c
- output/steps/000026/instruction.json: 147304 B / db5327c34a6447220a4309bd4f606a9372849977221bb1c290730c53df52ddc9
- output/steps/000026/result.json: 151584 B / 45588d8b319fe4c3497bb9ae6d7768119711aa2c8779779945bdf5fcbf78edd7

最後の実instruction.target_remainder_sha256は111d12e064b96a6bf579f39a9c9d5e35181560c0403bf0d237bffc924230c0ad、target_scalar=1、rolling_sha256=8f6605a28d337cd8541a7eacf6aef78f5a70308a6bb71fd105138803ca623a61。
result.targetはexact {parent_remainder_sha256:5cb563ec85586ff7653ded61edb51dfb8748576a8e42d92323625552b5c96427,remainder_sha256:111d12e064b96a6bf579f39a9c9d5e35181560c0403bf0d237bffc924230c0ad,scalar:1}。

実HEAD全文（元bytesを保持し、以下はその表示）:
```json
{"canonical_index_sha256":"452fe97a9229fa5188493256d1478ead1e684b495bbfed0db03a64f5acf4f00e","completed_steps":26,"current_scan_manifest_sha256":null,"generation":8090,"kind":"Separator","owner_sha256":"c4fd8b27590450d0b73e72efe9d45bf9319e111b5e21d1f3ff0b0ee23910f48c","packet_manifest_sha256":"d5e3ef0c0d691131b6bd1293d066d6e994c572086dc0c89a6e5ec766a8474199","producer_sha256":"d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa","rank":1385,"schema":"d972.r07.full-origin-refinement.v1.head","sha256":"a756db9a15f9bfce5b9919cea13582164bd6095ba11de05dc393e4a1f125dc12","source_sha256":"7e99018f58f3f49e371b55e6daab491b71855bb463c8c47cd872dffb57b5774f","start_sha256":"1a709c2853a6d0c239bc31d50ba6e03b0fb4707d93b625d291a487e6d43dc131","state_head":"8f6605a28d337cd8541a7eacf6aef78f5a70308a6bb71fd105138803ca623a61","step_manifest_sha256":"1bfd33af5054a11b8210781146a872e914acb1bd7214b0b945f7e3520b31200c"}
```

実最終step manifest全文:
```json
{"files":[{"bytes":147304,"file":"instruction.json","sha256":"db5327c34a6447220a4309bd4f606a9372849977221bb1c290730c53df52ddc9"},{"bytes":12096,"file":"lambda.bin","sha256":"1e720af4a30bac955ab4565366f0242b5c2d43125eb280e241df20976331cdf1"},{"bytes":5892217,"file":"materialization.json","sha256":"e98048839da8b75f4ebf434a7f8599cfd148ce656a4acf43f46668ebe566749c"},{"bytes":12096,"file":"physical-normalized.bin","sha256":"1ed0c6c5c35b5ae13ab528e6151be9d8d1c753c3cf02b6e62842cce76ee2c678"},{"bytes":12096,"file":"physical-raw.bin","sha256":"cac07ac713c35ee927d091ef382557f18f0d45bd847bc9de08602540541398c4"},{"bytes":12096,"file":"physical-remainder.bin","sha256":"468e0ffd03bab1cbb747162d1003275fb21a334cedbaa5d8d58371163da1ee56"},{"bytes":151584,"file":"result.json","sha256":"45588d8b319fe4c3497bb9ae6d7768119711aa2c8779779945bdf5fcbf78edd7"},{"bytes":9072,"file":"source-d.bin","sha256":"bc4d3a101a97d55a5db0c067dac88777b6efffdfd302d3a9f97d665b6b0a365d"},{"bytes":36288,"file":"source-full-top.bin","sha256":"d137424dafa0a4a3fc5079c8f2f90c6592930998c752f933aa69c48428d1d0f9"},{"bytes":12096,"file":"target-remainder.bin","sha256":"111d12e064b96a6bf579f39a9c9d5e35181560c0403bf0d237bffc924230c0ad"}],"generation":8090,"kind":"Separator","owner_sha256":"c4fd8b27590450d0b73e72efe9d45bf9319e111b5e21d1f3ff0b0ee23910f48c","packet_manifest_sha256":"d5e3ef0c0d691131b6bd1293d066d6e994c572086dc0c89a6e5ec766a8474199","parent_state_head":"b086ddbe49eb75ca6b7380442efd81186cb669c70360e7ebdc1b98e26369846e","predecessor_step_manifest_sha256":"a96afde3c0a0d38018f88d1224d7a3673492df7e45ac984ebbeea4e910a26dd1","rank":1385,"scan_manifest_sha256":"d0e54809d04b84e2936989fee47fb8386b538d8c264807823b57b10750916028","schema":"d972.r07.full-origin-refinement.v1.step-manifest","sha256":"8c34c9b3ac8d7d97955c7614034592f632c2b609690eb2addb4c115cd1a8f9fc","state_head":"8f6605a28d337cd8541a7eacf6aef78f5a70308a6bb71fd105138803ca623a61","step":26}
```

TEMP根は %TEMP%/shadow-atelier-audit163。全ZIP refinement-run33971897879-candidate-a1.zip、選択保存は refinement-actual-output-HEAD、refinement-actual-output-steps-000026-{manifest,instruction,result}.json。
メタデータの読取/全file hashは許可、ローカルPython/import/AST/数値計算は引き続き禁止。
実HEADはinner sealを含むexact15key。targetをHEADへ後付けせず、全26stepの最終manifestと既に読んだ実target payloadを結ぶ。本番とfixtureは同じ認証helperを通す。

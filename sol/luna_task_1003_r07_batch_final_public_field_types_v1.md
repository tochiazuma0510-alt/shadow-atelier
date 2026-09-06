# Task1003 — batch 公開字段の最終型追補（root → 994P / 995C / 996監査）

Task997/1000/1001/1002を維持し、両作者から独立に届いた公開型の二点を確定する。新P/C本文の相互共有はしない。

1. invocation.launch は exact {run,attempt,head,workflow}。run/attempt は boolを除く正の ordinary integer。GHA環境変数の文字列を厳密に読み、この型で保存する。headは40桁小文字hex、workflowは登録された .github/workflows/ の全相対path。started_utc は UTC文字列。host_paths は exact {parents,acceptance,output}、parentsは登録15roleから実絶対pathへの辞書、他二値も実絶対path。これは invocation のみの実行metadataで portable owner/source/start へ混入させない。
2. 新 physical-instruction.target_sha256 は rows/<local>/target.json の plain三key本文の全file SHA256。packed target のhashは reduction.target_after_sha256 と target.remainder_sha256 に保持する。Task1000 D3の新target親.target_sha256と同義。旧E instruction.target_remainder_sha256は旧名のまま別に認証する。新字段は足さない。

根拠はTask997 F2/F6/F10、Task1000 D3。rootが両作者へ同一文を配達する。実行はGHAのみ、root単独broker、初回親64/rank1450の登録とk32/max_batches1/refill=falseは不変。

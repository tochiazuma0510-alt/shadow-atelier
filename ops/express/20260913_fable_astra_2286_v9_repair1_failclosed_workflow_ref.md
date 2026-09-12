# 司令塔 → Astra: 2286 = v9 repair-v1 run 34714930484 は P 本走の入口で fail-closed(WORKFLOW literal と改名 WF の不一致)・notify-and-go で修理を

run 34714930484/1 は step 14(batch)が 4 分 22 秒で exit 1(continue-on-error)・checker 比較 skipped・step 22 join exit 1・candidate なし(diagnostics 10304703122 のみ)。根因は execution/producer-result.json と producer-stderr.log から:

```
File ".../search/d972_r07_fixed_lambda_cycle_batch_v9.py", line 8730, in begin_invocation
    require("/" + WORKFLOW + "@" in workflow_ref, "actual_registered_workflow_ref")
ValueError: fixed_lambda_batch:actual_registered_workflow_ref
```

P9 の登録 WORKFLOW literal(search/d972_r07_fixed_lambda_cycle_batch_v9.py:8617:WORKFLOW = ".github/workflows/d972-r07-fixed-lambda-cycle-batch-v9.yml")は v9.yml を指すが、修理版は WF を d972-r07-fixed-lambda-cycle-batch-v9-repair-v1.yml に改名して発射したため GITHUB_WORKFLOW_REF と一致しない(P9/C9 据置のため)。数学は無傷、消去は未着手。
(1) 2199 の凍結 envelope 内修理として notify-and-go で修理してよい。方式(WF 名を v9.yml に戻す/P9・C9 の literal を repair 名へ更新して新 pin + 別読)は Astra の設計に委ねる。著者分離と旧配置物保存は維持。
(2) F-v9-1(v10 前件): WF の識別子(file 名・name・marker)を P/C/driver/WF で literal 重複保持しないこと。登録表 1 箇所から導出し、配置前の静的突合 checklist に「WF file 名 = P/C の WORKFLOW literal」を加える(2255 の改名空振りと同系列)。
(3) 修理版の CV-9 には v7 repair-v2 と同型の「同一数学・別 seal」検問と逆置換票の継承を含める。以上。

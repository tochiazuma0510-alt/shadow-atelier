# 司令塔 → Astra: 2312 = v11 repair-1 run 34753243056 は P selftest(step 12)で fail-closed・k128 canary「old-acceptance」fixture の 14-key 更新漏れ・notify-and-go で修理を

run 34753243056/1 は 11:10:07Z に completed/failure。step 11(metadata admission)は success(2310 修理は有効)。step 12 の P selftest が 6 秒で exit 1・P 本走未到達・candidate なし(diagnostics 10316003345)。根因は producer-selftest-stderr.log と P11 source から:

```
P11 L11789 k128_registration_canary → case "old-acceptance"(L11783-11791): v2 schema の旧 acceptance fixture(batch_anchor_v10 を欠く 13 key)
  期待 gate "new_batch_acceptance_schema" だが、authenticate_acceptance は先に L9575
  exact_keys(value, current_count("current_exact_keys")["acceptance"], "acceptance_fourteen_plain_keys") で落ちる
ValueError: fixed_lambda_batch:k128_rejection_reached_expected_gate:old-acceptance:fixed_lambda_batch:acceptance_fourteen_plain_keys
```

分類: selftest fixture の key 集合が第 23 親(batch_anchor_v10)入場に合わせて更新されていない literal(登録表から導出されていない)。判定経路は無傷(14-key gate が先に効いた = 強化)。
(1) 2199 の凍結 envelope 内修理として notify-and-go で修理してよい。P11 source の変更を伴うので新 P pin + driver pin + 別読 + marker/name の express を。fixture の key 集合を登録表 current_exact_keys.acceptance から導出するか、期待 gate を実際に到達する gate に合わせる(どちらでも意味論不変・Astra の設計)。C/登録 metadata は不変のはず(変わるなら明記)。
(2) F-v11-2(lane checklist): selftest fixture の key 集合・schema 版は登録表から導出し literal 重複を禁止・配置前に「全 k128 canary が期待 gate に到達する」静的自己整合(dry canary)を driver selftest に含める。
(3) 修理版 CV-9 で逆置換 2 段(repair-1 driver + repair-2 P)の弱化なしを検問する。以上。

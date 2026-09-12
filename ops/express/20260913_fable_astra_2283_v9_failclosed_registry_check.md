# 司令塔 → Astra: 2283 = v9 run 34714029903 が step 7 で fail-closed(registry 検査)・notify-and-go で修理を

run 34714029903/1 は 19:23:58Z に completed/failure(起動から 29 s・P/C 本走に未到達・sealed object なし)。失敗 step 7「Save registered executable and three raw sources and authenticate their exact runtime」・driver.py L5896 `public_audit_registry` の require:

```
ValueError: batch_workflow:formal-file-directory-registration-separate-from-full-typed-parent-reception
```

検査は現 registry の parent_inventory_registration に対する 5 連言(key 集合 / registration == v8_batch_registration() / V8_PARENT_FORMAL_RECEPTION is not None / root_receipt == V8_PARENT_FORMAL_RECEPTION / full_typed_parent_metadata_complete ∧ scope)で、単一 why のため失敗連言は特定できない。分類は第 21 親の登録表 vs driver literal の静的不一致(F-v7-4 型)と読む。
(1) 2199 の凍結 envelope 内修理として notify-and-go で修理してよい(pin + 別読 + marker/name の express・工房は事後 pin 再計測)。(2) 計器の要請: この require を 5 連言それぞれ別 why に分けること(意味論不変・失敗箇所の特定可能性)。(3) 修理版の CV-9 では修理前後の逆置換が旧 raw に一致すること(弱化でない)を検問に含める。以上。

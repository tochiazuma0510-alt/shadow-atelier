# 司令塔 → Astra: 2310 = v11 run 34746915217 は step 11(metadata admission)で fail-closed・driver canary の期待理由文字列の prefix 欠落・notify-and-go で修理を

run 34746915217/1 は 08:20:19Z に completed/failure。失敗 step 11(`driver.py execute metadata`・08:16:00 → 08:17:15 exit 1)・P 本走未到達・candidate なし(diagnostics 10314313921 のみ)。根因は metadata-stderr.log と driver source から:

```
driver.py L18010 v11_public_wire_negative_canaries → L17793 v11_public_wire_compare
  require(canonical(value) == canonical(registered_value), 'v11-public-wire-whole-registered-value:' + name)
ValueError: batch_workflow:v11-public-wire-whole-registered-value:P_timing   ← 意図どおりの拒否
L18012 require(str(error) == wanted, ...)   wanted = 'v11-public-wire-whole-registered-value:' + name   ← prefix 'batch_workflow:' を欠く
ValueError: batch_workflow:v11-public-wire-exact-normal-comparator-reason:P_timing
```

分類: driver 自己 canary の期待理由文字列の literal 重複(require の書式と二重保持)= F-v9-1 と同族。P/C source・登録 metadata・数学は無傷。5 canary すべて同型で失敗する構造。
(1) 2199 の凍結 envelope 内修理として notify-and-go で修理してよい(driver のみ・期待理由を require の書式から導出するか prefix 込みで比較・意味論不変・逆置換票・pin + 別読 + marker/name の express)。P/C/登録 metadata 12 本の pin は不変のはず(変わるなら明記)。
(2) F-v11-1(lane checklist): canary の期待エラー文字列は require() の書式から導出し literal 重複を禁止・配置前の静的自己整合(全 canary の wanted = 実 require 文字列)を driver selftest に含める。
(3) 修理版の CV-9 で逆置換(driver 1 hunk 想定)の弱化なしを検問する。以上。

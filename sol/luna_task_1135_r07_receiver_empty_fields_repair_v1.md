# Task1135 — 1112 の空 diagnostic object を正確に扱う受信器修理

宛先: Luna / packet_bounds_audit。1132 は凍結保存し、本件を最優先する。既 1108/1127 は正式 handback 後に戻る。返信は `sol/luna_reply_1135_r07_receiver_empty_fields_repair_v1.md`、最終行 `TASK1135_VERDICT:`。新 agent / Git / credential / network / 親本受領起動 / 親への書込みは禁止。TEMP の新 versioned source と限定 metadata 対照を担当し、root が独立静読して採択・起動する。

## 実停止と登録対象

`%TEMP%/shadow-atelier-audit163/task1112/root-activation-v1/session-be2ebb260b73445e8d60551bbd3b39b0/directory-stability-result.json` は FAIL、2026-09-08T15:03:31.8634363Z、main_returned=false、typed/formal5=null、all_handles_closed=true、release_errors=[]。journal は 24461946 B / 1ba1c40fd56e7197bc738152e7407f31eadfa37f41f6e927e1137ae72c4b87c0。元 error は seq14276 / 15:02:01.1629849Z、`all and only the two actually present diagnostic filenames: exact fields: array length/type`。receiver `task1112/root-activation-v1/receiver/root-review-receiver-v5-directory-stability-draft-v2.ps1` 524346 B / 89f8eddc42a3b4e594a670b0cc28fafe5fb087ba562f420085bc8a569299dc07、L1144→Fields L184→Same L85、historical v4 L2564 である。

root の限定読取りでは v4 `run-receipt.json` の producer_resource_or_failure_diagnostics は空 PSCustomObject、output の resource-stop.json と rejected.json は共に存在しない。Fields は `[string[]]@($value.PSObject.Properties.Name)` を使っている。空 collection の property enumeration が null を一要素として扱う可能性を、推測で断定せず同じ PowerShell 5.1 の小対照で確定する。元 source・最終 broker/journal・小さな v4 run receipt の全 pin を先に登録する。巨大 broker の held paths 全出力は不要。

## 限定成果

1. 本停止を source の最小切片と実 JSON keyset に結ぶ。旧 Fields と修理 Fields の空 `{}`、一字段、二字段、余分字段、欠品字段、null、array、ordinary scalar の拒否/受理を自作の小 JSON/metadata だけで確認する。source 数学/Python/AST/import/compile/selftest は 0。artifact 数学本文や全親 tree の再走査はしない。
2. 正確な empty keyset を保持し、非 object や余分 key を受け入れない最小修理を新 TEMP receiver へ作る。旧 source の全 raw 順逆差分、全残存本文同一、変更行を提出する。診断件数を必ず二つとする訳ではないため、label/return metadata が zero/one/two の実存在を適切に表すかも静読する。ただし既受領出力契約を無用に変更しない。
3. 同じ .PSObject.Properties.Name / 空 array の仮定が、未到達の v4 後段及び v5 段の typed 検査に現れる箇所を source 限定検索し、同じ helper 修理で覆えるものと別問題を区別する。数学条件・file/hash/ZIP/全範囲・directory lease/失敗 journal・typed 完了条件は緩めない。重い再読を始める前に本停止の実 JSON に対して修理 helper が通り、余分字段対照が失敗する短い metadata preflight を root へ渡す。
4. 新 receiver を結ぶ broker/runtime/source pin の最小新 versioned closure と root 用起動引数案を作る。失敗した session は永久保存、新 session の全範囲再受領とする。過去 PASS や途中処理を全受領の代わりに再利用しない。agent が receiver/broker 全本走、既 process 停止、親復元を実施しない。root の既存認可内の内部採択が済み次第再起動できる形にする。

数学格付けは 1834/8539 limited7 cross-checked、A0 actual 0/1、verified=false のまま。今回 FAIL は正式 metadata 受領の停止であり、数学反例とはしない。既 P/C public selftest GHA 成功は保持し、未変更 source の重複 selftest を要求しない。


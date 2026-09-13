宛先: 司令塔・研究者
緊急度: 今すぐ（配置・GHA発射の notify-and-go 通知。返答待ちは置かない）

裁定2199/2293/2295と研究者の継続GHA認可に従い、既登録V10 envelope の最終4 source を以下のpinで配置・commit/pushする。P/Cの著者分離、22親、k128/max1/no-refill、C4 raw、数学宇宙、P5400/C10800・外側6000/11400・RSS7168MiB・selftest300/360・job330分は固定。

| 配置先 | bytes | SHA256 |
| --- | ---: | --- |
| search/d972_r07_fixed_lambda_cycle_batch_v10.py | 1034265 | 33c4bbb97313bc1ea2017b6ac6ad2cc0932ae15d1affc8bcd6a8aaedd0c76085 |
| search/check_d972_r07_fixed_lambda_cycle_batch_v10.py | 870249 | a21fd2b54958f84ea67e7b3a079893cff70544961005d6c79a0f6ff47e752ca8 |
| search/d972_r07_fixed_lambda_cycle_batch_v10_workflow_driver_v1.py | 32326911 | acf206e5fe423288f3449e5e034a1bd125a6c203e6c274b64f41fc36ab94c802 |
| .github/workflows/d972-r07-fixed-lambda-cycle-batch-v10.yml | 47555 | 88856a3329ccb59750c427fd27ba6857d89953b75a65f93a11f260783f67f34a |

name: d972-r07-fixed-lambda-cycle-batch-v10-envelope-v1
marker: [r07-fixed-lambda-cycle-batch-v10-envelope-v1-run]
branch: sol/r07-explicit-lift-20260825

別読票: %TEMP%/shadow-atelier-audit163/root-v10-final-launch-closure-v1.json = 15447 B / 67844e92b012f7e4f7125c7a2a70a2ed26dbaae7246858e352aec90bbfba5613（root e39aff/native0、ROOT_FINAL_SOURCE_CLOSURE_GO）。著者票: 同/task1191/public/v10-final-source-regions-consumer-closure-v1.json = 336954 B / 9e910b8d7d23f7b3b8903701346e318b3101d1a297f5e20eec3b809c9546eb68。全319区間/318関数、154310 tokens/67862字句片、全54編集/55保持gap/17追加片/16公開carrier、15 caller窓と2順序条件、WF6 pin、53入力の前後一致を照合済み。F2宣言はroot審査provenance、F5の2子は元300秒を共有、F7の2固定文/新親3項のみ、F8は実WF raw前後照合で循環selfhashなし。

V9 run34717506638の正式受領は終了済み。V10の結果はまだ未観測。今回の配置前対象実行/import/AST/compile/selftest・fixture実体化・archive decodeは0。A0 actual=0/1、Lean verified=false、full A0=falseを保持。発射後のrun idとcommit shaは指定返信とv220へ追記する。

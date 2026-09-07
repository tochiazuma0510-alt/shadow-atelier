# Task1082 P reply — 正式 wholeinventory の一箇所結合

## F1 範囲と根拠

Task1082 全文と root 正式票 `v4-run34120585268-final-parent-inventory-registration-v1.json`（7022 B / `64e3f8e6a434be335a88c1dee6efa4aae7b3d669faac28e704aefd0f8e3f4753`）を読了した。root が新たに全11648 fileを再hashし、保存envelope・acquisition全entry・全3525dirと一致させた結果の登録である。全typed metadata受領は未完のまま区別し、工房2206限定7条の格付けをこの便で追加昇格しない。

## F2 正確な差分

旧 `task1077/review-snapshot-v1/d972_r07_fixed_lambda_cycle_batch_v5.py` 366388 B / `135495b3203ba393fcceb5b22b74f5da5694849b67c0841ca4193d18ea56cba9` の `NEXT_BATCH_INVENTORY_REGISTRATION = None` 一箇所だけを次の五key辞書へ置換した。旧snapshot、作業中旧P5、返信1077は不変である。

```python
NEXT_BATCH_INVENTORY_REGISTRATION = {
    "files": 11648,
    "file_bytes": 1308094050,
    "directories": 3525,
    "files_sha256": "ffec515b0a235ce2dd99770e51619252c725269970b71e32180be5f14cafaff5",
    "directories_sha256": "f9562484c91c05c517b50065d86e1a88f16af6b1e3198b1d0ba1adb645f9dc64",
}
```

新sourceは `%TEMP%/shadow-atelier-audit163/task1082-P/d972_r07_fixed_lambda_cycle_batch_v5.py`、366644 B / `664f593a4c9b6eb5d088960215674175a123d7f5a5f2bb3e134d3cb0e16c1c66`。ASCII、LF5536、CR0、BOMなし、final LFあり。差分は+256 bytes / +6 LFだけで、逆置換した全rawが旧sourceへbyte完全一致し、旧全SHAへ戻る。直前の旧pending commentも本便の「一箇所だけ」に従ってraw不変とし、実状態はこの正式辞書と本票で明示する。

## F3 保持と納品

全156 current raw区間を旧EOF台帳から新offsetへ移し、全sourceの欠落・重複なしを照合した。P4に対する登録37本文の各新offset/全bytes/SHAを照合し全件不変、其中4旧1450 loaderも不変。通常算術・各selftest・全語/行順・診断/保存/CLIに変更はない。新sourceの本文実行、AST、import、compile、数学再演は行っていない。

同 `task1082-P/` の公開納品は次のとおり。

|file|bytes|SHA256|
|---|---:|---|
|producer-full-one-change-v1.diff|493|9f08c3913ae45a4127b9f65e2c8909b87bd144accb409adce8c7c80330011862|
|all-current-raw-regions-v1.json|205090|eb6ab0a942026633ce9041cb2f479df899e9a1c83654911915052f1917181dee|
|producer-body-inheritance-v1.json|42516|ff07e4c1c4d42fa827e094012f0c701b9dc31923d2ab3df817c6e671394b854a|
|binding-self-review-v1.json|3444|39ad76ab8cb41715b5542982c0b5abec5931a29c7bf72786e48d80d3609acb4c|

`materials-index-v1.json` は読取材料と全納品pinを収載する。正式canonical files 1931889 B / `ffec515b0a235ce2dd99770e51619252c725269970b71e32180be5f14cafaff5`、directories 200290 B / `f9562484c91c05c517b50065d86e1a88f16af6b1e3198b1d0ba1adb645f9dc64` の実全file pinも本便で照合した。artifact本体全件の再hashはroot票の根拠であり、本便で重複実行したとは主張しない。

## F4 閉鎖範囲

この一箇所結合・全逆差分・全EOF台帳・保持範囲の静的自己点検は閉じた。root/1079へ公開新pinとmetadata rangeを配達済み。v5実親入場、四群、新P/C、全WF最終別読、配置/GHAは未実行である。source/返信は本便で凍結し、1081の独立WF監査を継続する。

AUDIT_1082_VERDICT: STATIC_EXACT_ONE_LITERAL_BINDING_PASS; SOURCE_EXECUTION_0; SELFTEST_NOT_RUN; ROOT_FULL_TYPED_METADATA_NOT_COMPLETE; NEW_GHA_NOT_RUN.

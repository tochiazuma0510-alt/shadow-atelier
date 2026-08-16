# Luna reply: independent fixed-basis dense Tietze checker

実装対象は `crosscheck/check_d972_b4_norm_tietze_dense_v1.py` のみ。producer の import は行わず、canonical input と word artifact から独立に次を再構成する。

- 固定 `C2^5` mask-major transversal、161 Schreier generators、5056 RS relators。
- 972 exact norm rows と norm-RS rows。
- 入力・alphabet・source/relator/rows/norm digest の fail-closed 検査。
- `d972-b4-norm-tietze-trace/v2` の全34 elementary eventを、defining index、pivot/sign/position、replacement、signed substitution、定義行削除、active before/after、presentation/norm digest、old_to_new/new_to_old とともに再生。
- step-34 の final relators/norms、127以下の dense old→new / new→old map、map digestを再計算・照合。

固定完全digest:

- raw RS relators: `29c65a6cf9d0308e25ca462c752d7b540a6856e7d99d5d1d016919240b575c0e`
- norm RS rows: `f7134e15e92c80a5ceeede38e94314539815a665ba7d279443208de1696041f8`
- source: `c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9`
- normalized rows: `283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930`
- exact norm words: `ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e`

checker output schema は `d972-b4-norm-tietze-dense-check/v1`。partial ledger、forged step/map/digest/alphabet、または dense final artifact の偽造は拒否し、有限探索を terminal claim に昇格しない。

検査済み:

```text
python -m py_compile crosscheck/check_d972_b4_norm_tietze_dense_v1.py
python crosscheck/check_d972_b4_norm_tietze_dense_v1.py --selftest
D972_B4_NORM_TIETZE_DENSE_SELFTEST_PASS
```

selftest は tiny fixture のみで、canonical 5056/972 replay・GAP・重計算は未実行。commit/push/dispatchなし。

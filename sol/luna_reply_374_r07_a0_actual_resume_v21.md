# Luna 374 — A0 v21 actual resume 最小接続

## 結論

v20 を frozen owner とする actual-resume successor を完成した。既存
`restore_checkpoint` の定義・数学には手を加えず、production parser と main の
未接続箇所だけを接続した。2 workers、RSS/DAG 修理、caps、UNKNOWN、探索順序は
v20 のままである。

| role | path | bytes | SHA-256 |
|---|---|---:|---|
| producer | `search/d972_r07_history_free_positive_fast_resume_v21.py` | 3035 | `18aef3a1619b076b32002a9083ba9763116d984b761b7f8d181059293dbdf1fd` |
| checker | `crosscheck/check_d972_r07_history_free_positive_fast_resume_v21.py` | 2027 | `a2d913328fef890477305ae5b2cec6978c0dc3882e7c47af35d3444ac16f7c22` |
| driver | `search/d972_r07_history_free_positive_fast_resume_gha_driver_v21.g` | 8260 | `1dfbd79f642f85a50b08e17e7f554adbaf5a2c62574681c80ee527481df4cc7b` |

producer は optional `--resume PATH` を持つ。resume 時だけ `Search(...,
defer_owner_start=True)` とし、その生成直後、`search.run()` より前に既存
`restore_checkpoint(search, resume_path)` をコード上 exactly once 呼ぶ。restore
終端が boundary owner を開始する。fresh 時は `defer_owner_start=False` なので v20
と同じ constructor/start/run 経路である。

driver は `D374ResumePath`, `D374ResumeBytes`, `D374ResumeSHA` が全部未定義なら
fresh、3つ全部定義なら path/bytes/SHA-256 を物理照合して `--resume` を渡す。
1つまたは2つだけの指定は実行前 REJECT。resume artifact の既定 path/仮 pin は
置いていない。restore の `source.path` 完全一致 gate のため、fresh/resume の
双方で raw source path を v20 と同じ
`ci/resume/d972_r07_history_free_positive_fast_resume_v20.raw.json` に固定した。

checker は v21 producer の exact bytes/SHA のみに版上げし、v20 の独立 COMMON
selected-support replay と UNKNOWN_RESOURCE checkpoint DAG/new-record/epoch/counter/
cleanup 検査をそのまま保持する。driver は resume input を先に物理 pin し、最終
producer/checker terminal の完全一致後だけ v21 sentinel を出す。

静的 definition load と生成 source assertion（`--resume`、deferred owner、restore
call 1個、既存 restore 定義保持）は PASS。retry、SELFTEST、production run は
実行していない。

# Luna reply 595 — grade-one decision probe v2 / bounded recovery workflow

指定4ファイルのみを追加・更新しました。v1の decision-only scope と frozen v3 vectorized reducer を維持し、v2 repairを適用しました。

- decision body/workflowに frozen v3 producer SHA-256 `bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff` を固定。
- old ranks `[505,503,503,503]`、block ranks `[1509,1512,1512,1512]`、counts `2014 + 6045 = 8059` を body に記録。
- 起動時に v3実ファイルSHAを再計算して frozen 値と比較し、body は v2自身の `producer_sha256` と `v3_producer_sha256` を分離保持。local accept-already-reduced helper は v3の ordered pivot/key更新を再現し、coefficient-2 accepted と dependent row をfixtureで直接同値確認。
- lower accepted rowの二重挿入を避ける lower-first route、coefficient-2/dependent fixture、actual MEMBER/NONMEMBER fixture、既存 HEAD拒否、atomic temporary cleanupを実装。
- workflowは candidate-decision 1 jobのみ。workflow_dispatch と指定branch上の `[fire-grade1-decision-v2]` push、exact SHA checkout、Python 3.13 / numpy 2.5.1、pinned actions、source artifact fan-in、`ulimit -v` / 2400s / 45m、decision-v2の4ファイルだけのstage/upload、always logsを定義。
- v1/v3/v4、certificate、v220、既存workflow、commit/push/dispatch、実8,059-row calculationは触れていません。

ローカル検査（bounded fixtureのみ）:

```text
python -B -m py_compile search/d972_r07_a0_first_rung_grade1_decision_probe_v2.py search/check_d972_r07_a0_first_rung_grade1_decision_probe_v2.py
=> exit 0
python -B search/check_d972_r07_a0_first_rung_grade1_decision_probe_v2.py
=> {"fixture":"PASS","fixture_cursor":8,"forbidden_fields":"PASS","markers":"PASS","member":"PASS","mutation_rejections":5,"nonmember":"PASS","registered_cursor":8059,"routing":"PASS","segments":4,"target_coefficients":"PASS","truncated_missing":"PASS"}
```

サイズ / SHA-256:

```text
12106  5A445CF9A263C1968C004F04227D9F5BD5349E433F4DFD8776AF80B1D53D9748  search/d972_r07_a0_first_rung_grade1_decision_probe_v2.py
4447   8D757763FF8EBD7787FEF513C732A81411FDAC43FB672787B028F8CAEDBD4696  search/check_d972_r07_a0_first_rung_grade1_decision_probe_v2.py
6841   81EB842CE83C20E0E8CEEB68ED78363EF0B9C5B8B290C0D9373DAAC16BBDA92B  .github/workflows/d972-r07-a0-first-rung-grade1-decision-v2-recovery.yml
```

実8,059-row calculationとGHAは未実行（root brokerの範囲）。fixture-only evidenceのため、workflow readinessは `NOT_READY` とします。

GRADE1_DECISION_PROBE_V2_NOT_READY

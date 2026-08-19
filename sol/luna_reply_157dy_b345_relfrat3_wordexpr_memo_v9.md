# Luna reply 157dy — B345 relative-Frattini WordExpr v9 memo/fusion accelerator

## 判定

指定された新規4ファイルだけで v9 を実装し、hostile audit の STOP 項目を修理した。frozen v8 の登録4096候補、候補順、33 acceptance / 17 diagnostic、operational first-PASS、fixed saturated basis、proof regeneration は変更していない。

修理後の corrective combined selftest は exactly once で PASS した。GAP production、full search、Git、GHA、workflow 編集は行っていない。current v8 run `32247008986` にも触れていない。

## Frozen files

| file | bytes | SHA256 |
|---|---:|---|
| `search/d972_b345_relfrat3_wordexpr_memo_v9.py` | 392086 | `7dede323c3c52bc7cf7d99af6d542b3683823879a4bb3e340aca8ce53dcf196f` |
| `search/check_d972_b345_relfrat3_wordexpr_memo_v9.py` | 403737 | `d5695fdb5f56cdc23c012a09488786efacb16a1c4ee85f2297dc66c045092f4d` |
| `search/d972_b345_relfrat3_wordexpr_memo_gha_driver_v9.g` | 15625 | `9a81de13460d751ed720c01cb13e0b06196452b1e982e5a7b0d03404cad14d0f` |

driver は上記 producer/checker SHA を hard-pin する。v1–v8 の既存 pins は不変で、placeholder / stale v9 pin は0件である。この reply 自身の SHA/bytes は自己参照を避け、外側の完了報告で固定する。

## Hostile-audit repair

1. Cache は純粋な best-effort 高速化に限定した。node/sparse 容量不足や pin 保持不能は eviction または exact cold recomputation へ落ち、candidate reject / ResourceStop / terminal の理由にはならない。`candidate_live_gradient_entries_total` は cache を先に追い出した後の実 working set にだけ適用する。
2. 各候補は WordExpr value を構成した後、correction coface と33 acceptance の direct E4 quotient gate を最初に通す。ここで落ちた候補は source-gradient pin を一切行わない。
3. ordinary candidate は target 1..16 を frozen 順で評価し、実際に target 17 へ到達した時だけ six source anchors を lazy request する。target 17 未満で落ちる候補は pin しない。
4. candidate 1 は direct gate 通過後にだけ pin stage を開始する。既存の50本 flat-vs-WordExpr bridgeを全完走し、acceptance 1..6 の membership を bridge と融合する。frozen blocker `target 6 = hexagon_1_coface_0, component 4` は一度だけ求め、残り44 canary は membership を再実行せず完走する。
5. prospective PASS は membership evaluator を捨て、dictionary index から新しい evaluator を生成する。proof 用 six anchors も新しい pin stageで、33 gradients/bindings の一致後にだけ lossless provenance proof を作る。
6. E4 presentation / marked leaves / quotient binding SHA は scan 前に一度だけ計算し、同一 quotient object と次元を gate して各 evaluator に read-only 注入する。fixed inverse tuple は immutable tupleへ正規化して SHA を一度だけ計算する。acceptance/diagnostic order SHA も初回 exact order gate 後に再利用し、4096回の大きい JSON/hash 再計算を除いた。
7. receipt/checker は pin stage を candidate1 bridge / ordinary target17 / proof regeneration に分け、request数、保持不能数、pin eviction、direct-before-pin failure、target17前 exit、partial RESOURCE prefix を exact schema で照合する。cache capacity が数学 terminal に昇格する mutation と lazy target ordinal drift は reject する。

## Semantic invariants

- registered correction order: `1..4096` exactly once
- acceptance / diagnostics: `33 / 17`; diagnostic は acceptance に昇格しない
- first-PASS: operational registered orderの最初だけ
- candidate 1 bridge: 50本全部、target 6 membership は一回
- failed-candidate transaction: element-pool / provenance-DAG suffixを完全 rollback
- cross-candidate memo entries: 0
- memo key: typed node、rank/arity、candidate binding、E4 presentation/marked leavesを束縛し、同じ群値を key にしない
- selected proof: memoを信用せずfresh evaluatorで再生成
- SEARCH_INCOMPLETE / UNKNOWN_RESOURCE / UNKNOWN_INPUT: すべて `unknown_not_obstruction`

## Corrective combined selftest

許可された1回だけ、次の producer→checker sequential command を実行した。

`python -B search/d972_b345_relfrat3_wordexpr_memo_v9.py --self-test` の成功後に、同一 command 内で `python -B search/check_d972_b345_relfrat3_wordexpr_memo_v9.py --self-test` を実行。

結果:

- producer PASS: product/inverse/substitution/negative-prefix、262144-letter unflattened chain、typed key、equal-value nonalias、hit/miss/eviction/rollback/recompute、six anchors、tiny-cache cold fallback、4096 scan schema、4 terminals
- checker PASS: shared production envelope/source-preflight/scan/selected/proof core entry counts `20/17/16/10/5`、4096 source tuples、33/17、17 mutations、5 terminal fixtures
- marker:
  - `D972_B345_RELFRAT3_WORDEXPR_MEMO_V9_PRODUCER_SELFTEST_PASS`
  - `D972_B345_RELFRAT3_WORDEXPR_MEMO_V9_CHECKER_SELFTEST_PASS`

修理後は追加の Python/GAP 実行をしていない。`git diff --check` と static pin/schema scan は PASS。

## Claim boundary

PASS が主張するのは frozen v8/v9 の登録4096候補内の typed positive certificate だけである。SEARCH_INCOMPLETE / UNKNOWN_RESOURCE / UNKNOWN_INPUT は、非存在、full H3 fibre、cofinality、uniform iteration、B4-A/B を主張しない。candidate sharding、checkpoint/resume、v8 receipt import、W-FORM-first、UU/FC-22、integer-linking prefilterも追加していない。

B345_RELFRAT3_WORDEXPR_MEMO_V9_READY_FOR_GHA

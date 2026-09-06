# 司令塔 → Astra: batch v2(k = 64)の工房格付け = cross-checked(限定 9 条)・**rank 1514 を受理**・「k を上げて a/k を測る」枠組みの言い換え(裁定 2176)

falsifier の増分 CV-9(正本 `docs/notes/fixed_lambda_batch_v2_cv9_reading_v1.md`)。

## 裁定

**CV-9 = 同一対象**(第三実装: 全 54,433 弦の残差再計算で失敗 36,274/先頭 70/edge 125 を再現し failed-indices.u32 と全件一致(v1・control-96 と三点一致)・階段形 64/64・λ ⊥ 新 64 行・λ·t = 1・row_pairings = sha(0x00×1514)・λ の新 64 lead 成分を後退代入で完全再現・target 恒等式の逆順足し戻しで親 anchor 3bba0da3… 一致(θ ≠ 0 が 42/64)・head 鎖 64/64・checkout-sources 24/24 バイト一致・事前登録健全(SELFTEST_REJECTIONS が literal 登録・rank == 1450 + accepted なので独立率 1.00 は gate の強制ではない))。工房格 = **checker PASS・cross-checked 限定 9 条 → batch v2 状態 rank 1514/gen 8219 を受理**(v1 の 1482・control-96 の 1482 と別状態・合算しない)。

## k = 64 の実測(v1 比較)

| | v1 k=32 | v2 k=64 |
|---|---:|---:|
| offered / INDEPENDENT / DEPENDENT | 32/32/0 | **64/64/0** |
| rank | 1450 → 1482 | **1450 → 1514** |
| P / C 秒 | 432 / 551 | **825 / 1,024** |
| P+C / 行 | 30.7 | **28.9**(限界単価 27.0 = 逐次 42.4 の 1.57 倍速) |
| 候補あたり(primal+p1 の比率)| 10.97 s(76 % of P) | **11.06 s(80 % of P)** |

## F-k64-2(重要・枠組みの言い換え)

**a/k は batch サイズの関数ではない**: `BATCH_SIZE` が算術に効くのは `failed[:BATCH_SIZE]` の 1 箇所だけで、消去は候補ごと逐次(rank_before = 1450 + i が 64/64)。しかも**前半 32 本は v1 と物理行までバイト同一**(witness 数学 field 32/32・差は版束縛の 3 印のみ)⟹ 本 run の新規情報は roster index 123..177 の 32 本だけ。正しい量は「**roster 前置長 n における独立数 a(n)**」で、a(32) = 32・a(64) = 64・**a(128) は「k = 128 の batch」でも「k = 64 の続き」でも同じ数**になる。k を上げる価値は**費用側にしかない**。F4 反例は未排除(64/36,274 = 0.18 %)。⟹ 工房の 2172 推奨「k = 64/128 で a/k を測る」は「roster 前置長を伸ばして a(n) を測る(k は費用最適で決める)」に言い換える。

## F-k64-1(要修正・再走コスト 0)

v2 の selftest は 3 群 → 2 群になり、`dependent-independent-target-signs-and-packed` と `private-prefix-publication-resume-and-isolation` が消え、producer の `canary_reduction`(F4 第二反例を張っていた)が削除された ⟹ **本 run で DEPENDENT 枝は合成でも実データでも一度も通っていない**。緩和材料: 算術領域は v1 と `WORKFLOW` 1 行を除きバイト同一・独立性の主張は canary でなく階段形実測に依拠(silent な誤りは通らず、リスクは soundness でなく liveness)。**ただし継承が cert に一切記録されていない**(v1 由来を明記するのは metadata canary の `metadata_regression_from` のみ)。提案: 同型の `arithmetic_selftest_inherited_from` と不変算術領域の行範囲/sha を受領証に足す。

## F-k64-4(費用)

「固定費」は固定でない: 68.7 → 104.7 s(出力 ZIP 94.7 → 187.1 MB)・fixed(k) ≈ 32.7 + 1.124k ⟹ producer cap から取れる k は 484 → **≈ 436**・必要 run 98 → **≈ 107**。

## その他

- F-k64-3(軽微): 空き座標の債務 112 → 114(lead 1625/1626 が飛ばされる)= v1 F-flb-5 の「債務は増えない」を反証。
- F-flb-3 解消: diagnostics = candidate 同一バイト数は仕様(run-receipt が `candidate_and_diagnostics_upload_the_same_envelope_root: True` を宣言)— 欠陥ではないが 187 MB の情報ゼロ重複。
- F-flb-1 継続: 共有 TCB 2 本は sha 不変・P1 経路(候補時間 72 %)で load-bearing・docstring "Independent bounded implementation" が run の checkout-sources に同梱・**F8.89 の登録は返信側にあり run の cert には無い** → cert への転記を。
- F-k64-5: 候補秒 ≈ 10.794 + 0.0424×(語長/1000)— 語長は費用の 3.5 %。
- 限定 9 条は正本参照。以上。

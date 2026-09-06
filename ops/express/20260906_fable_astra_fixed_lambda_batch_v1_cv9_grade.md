# 司令塔 → Astra: fixed-lambda cycle batch v1 の工房格付け = cross-checked(限定 9 条)・**batch 状態 rank 1482 を受理**・checker の構造的天井は解消・次は k = 64/128(裁定 2172)

falsifier の増分 CV-9(正本 `docs/notes/fixed_lambda_batch_v1_cv9_reading_v1.md`)。

## 裁定

**CV-9 = 同一対象**(第三実装で全量再導出: target 恒等式の逆順足し戻し t₀ = 親 target sha 3bba0da3…(θ ≠ 0 が 20/32)・選定 oracle が control-96 step 64 と完全一致(first_failed_index 70・residual_nonzero 36,274 = 別 workflow・別実装で同じ oracle)・row_pairings = sha(0x00×1482)・λ_new の新 32 lead 成分を逆順後退代入で完全再現・消去は挿入順前進消去とデータが判別)。工房格 = **checker PASS・cross-checked 限定 9 条 → batch 状態 rank 1482/gen 8187 を受理**(逐次経路の 1482 とは行の由来が異なる別状態として並記)。

## 実効前進率(対照 control-96 と頭付き比較)

| | control-96(逐次 32 段) | batch v1 |
|---|---:|---:|
| oracle 回数 | 32 | **1** |
| producer / checker 秒 | 822.5 / 2,139.8 | **432.4 / 551.3** |
| 1 行あたり P+C | 92.6 s | **30.7 s(3.01 倍速)** |
| 独立率 | — | **32/32 = 1.00**(dependent 0) |

相分解: 候補 1 本 10.97 s のうち **P1 補正 7.93 s(72 %)+ primal 2.39 s(22 %)** — 律速は固定次元の配列作業で、SLP 語長(34〜12,354 letters・363 倍)は時間を 5.7 % しか動かさない。batch 化が削ったのは oracle 分(11.88 s/段 → 1 回)そのもの。

## F-flb-6(重大・朗報)

**2164 の checker 構造的天井(rank ≈ 1,890)は解消**: batch checker は thin anchor から始まり prefix を再生しない(551 s = 枠の 5.1 %)。撤退/切替条件(2164 の 3 本)は書き直しが要る。新しい律速 = (a) P1 補正相の単価 (b) **k を上げたときの独立率 a/k(未知)**。

## F-flb-1(要修正・独立性)

P/C で実行コードが文字一致する数値カーネル 2 本 — `vectorized_projection_chunk`(checker docstring は "Independent bounded implementation" だがコピー)と `sparse_adjoint`(正規化 sha 完全一致)— が producer 時間 94 % を占める P1 相を通る load-bearing(2131 F-fo-1・2138 F-sc-1 と同根)。docstring の表現訂正か、**共有 TCB としての明示登録**(cert に "shared kernel: file/sha" を書く)のどちらかを。

## 次の実験(推奨・採否は Astra)

32/32 独立は **k = 32 の一点観測**で、Task 988 F4 の反例(同 λ 違反の従属)は排除されていない。外挿(残 46,902 行・k ≈ 480/run・98 run・16.7〜25 日)は全てこの一点に乗る ⟹ **k = 64 と 128 で独立率 a/k を測る**のが情報量最大(DEPENDENT 枝・aux 枝は本番未発火なので、従属が出た時の挙動もここで初めて実データで踏める)。

## その他

- `elapsed_seconds` は cross-check されない(cert 外)。checker に段別 timestamp が無く候補あたり限界単価は分離測定不能(P 側の相分解のみ)。
- diagnostics と candidate は同一バイト数(F-c96-3 継続)。
- 新 lead は 1562..1593 の連続 32 整数(空き座標 112 は前後不変)。
- 限定 9 条は正本参照。工房の判読規律(batch 型)に「offered/accepted/dependent・独立率・相分解の秒・target 恒等式の逆順足し戻し」を恒久追加。以上。

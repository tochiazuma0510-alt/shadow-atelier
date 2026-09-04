# 司令塔 → Sol: J3 本走 run 1(33902091912)= producer REJECTED `task554_seed:entry`・原因 = validator の pivot 単調増加要求が実データ(還元順)と不一致(計測 express・裁定 2070)

2026-09-04 17:44Z 完了。工房が Task554 prepare artifact(9865061266・Release ミラー)を展開して全数分類した実測。修理は Sol/Luna 側。

## 実測

| 項目 | 値 |
|---|---|
| run / step | 33902091912 / step 16 "Run actual producer with minute-scale progress": failure(17:44:30Z → 17:44:53Z・23 秒) |
| producer.log | `{"error": "task554_seed:entry", "status": "REJECTED", "verified": false}` |
| 出力済 | `output/q-a0-root.bin`, `q-a0-t0..t3.bin`(各 9,072 bytes)= character-0 dual root と 4 adjoint 像は生成後に停止 |
| diagnostics artifact | 9948055636(55,523 bytes) |

## 原因(全数分類・prepare body `prepare.1f191d88…json`)

producer v1 `_expression(value, bound, reason)` は各 [pivot, coeff] に **`previous < item[0] < bound`(pivot の狭義増加)** を要求する。実データは還元順で並び、単調ではない(例: char 0 seed 3 = `[[2, 2], [0, 1]]`)。

| character | rank | seed_reductions 違反/44 | actor_transitions 違反/全 | 違反種別 | 重複 pivot |
|---|---|---|---|---|---|
| 0 | 505 | 15 | 2008 / 2020 | **order のみ** | 0 |
| 1 | 503 | 2 | 2005 / 2012 | order のみ | 0 |
| 2 | 503 | 2 | 1993 / 2012 | order のみ | 0 |
| 3 | 503 | 13 | 2009 / 2012 | order のみ | 0 |

- 形(2-list・int)・範囲(0 ≤ pivot < rank)・係数(∈{1,2})の違反は **ゼロ**。違反は順序のみ。pivot の重複もゼロ。
- semantic replay v5(`record['seed_reductions'][local]` を順に適用・順序仮定なし)と physical connection v6 は同じ body を消費済み ⟹ 新 validator の文法だけが実データより厳しい。seed が通っても直後の `task554_actor` で同じ理由により停止する(actor 側はほぼ全件違反)。

## 修理候補(採否は Sol)

- (a) `_expression` の `previous < item[0]` を**除去**し、代わりに pivot の相異(集合サイズ = 長さ)を要求(実データで成立・上表)。範囲・係数・形の検査は維持。
- (b) 契約を「還元順の列」として明文化(順序は意味を持つ: 逐次適用)。sort して受理するのは意味論を変えるので不可。
- fixture に**実 body の seed 3(char 0)**を固定して再発防止。

工房側は run 2 の発火要請があれば即時。以上。

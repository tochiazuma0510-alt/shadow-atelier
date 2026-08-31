# 宛先: Fable — 157dn run id 訂正

前便の `32174026086` は generic runner の `with_pquot_packages=false` を検出し、
GAP setup 中に取消済み（heavy script は未実行）。

正しい run は ANUPQ 3.3.3 を有効にした
`32174498056` / commit `9d7cc8cc9acc3d776acddd40ad9513ec180d9080`。
数学対象・source SHA・見積り・conditional glue は不変。

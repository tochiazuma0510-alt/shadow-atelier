# 宛先: Fable — 157dn external-timeout 修正再走

run `32175268482` は数学 terminal ではなく、job 開始から 120 分 03 秒で
workflow の外側 hard timeout により kill されたものと訂正する。artifact は 0 件で、
PASS/negative/UNKNOWN のいずれも出ていない。

同じ frozen commit `9d7cc8cc9acc3d776acddd40ad9513ec180d9080`、同じ
producer/checker/driver と同じ preamble のまま、外側入力だけ
`timeout_min="350"` に変更して run **`32186874185`** を発射した。

URL: https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/32186874185

workflow は未変更。内部 soft stop/3-terminal/checker 契約も不変。結果は artifact と
独立 checker が揃うまで未判定として扱う。T-50 の縮小 chief fallback は並行設計として
維持するが、この再走の数学対象は 157dn full Phi lane のまま。

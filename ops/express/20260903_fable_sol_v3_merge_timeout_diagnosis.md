# 司令塔 → Sol【GHA 計測】grade-1 v3 run 33677346616 = merge timeout の失速点(工房の結果確認・参考)

裁定 1896・2026-09-03。工房の GHA 監視と merge-log artifact(9875030711・3,964 B)からの読み取り。数学判定なし。

## 事実
| 項目 | 値 |
|---|---|
| merge job「joint lower-first physical fibre」 | 20:17:37Z 開始 → 01:52:59Z `timeout` kill(exit 124)・job 5h35m |
| 最後の進捗行 | 20:24:20Z・elapsed 344.6 s・attempts 7,936・character 3・retained_rank 5,044・queue 0・RSS 5,591,011,328 B |
| retained_rank の推移 | 7,168 で 5,044 に到達後、7,424/7,680/7,936 で不変(末尾 offer は全て拒否) |
| RSS の推移 | 5.45 GB(6,144)→ 5.59 GB(7,936)・256 attempts あたり ≈25 MB 増・7 GiB gate 内 |
| 沈黙区間 | 20:24:20Z 以降 5h28m 出力なし。roster が 8,059 で尽きるため次の進捗行(8,192)は原理的に出ない ⟹ 沈黙 = 進捗出力を持たない次局面(lower-first 物理 fibre / finalize) |
| 結果 | merge.HEAD なし・cert なし・checker job skipped・merge 状態 artifact なし(log 4 KB のみ)・prepare/4 block artifact は 2026-12-01 まで保持 |

## 含意(工房の読み・拘束力なし)
1. 失速は offer roster の消化(≈6 分で 7,936)ではなく、その後の**無出力局面**にある。v4 の hot-loop 修理(reduce_packed の suffix scan・lower 行の二重簡約)がその局面を狙っているなら妥当。v4 recovery run 33687595111 は merge 開始 ≈21:57Z・cap ≈03:27Z。
2. 次回以降の run では、無出力局面にも**heartbeat 進捗行**(処理済み行数/経過秒/RSS)と、cap 前の**耐久 checkpoint の定期書き出し**(merge 状態を artifact に残す)を入れると、timeout 時に 5 時間分の状態を失わずに済み、v462 の external-owner 設計の入力にもなる。
3. 8,059 行消去が Python で 5.5h を超えるなら、v462 の packed external owner(C)の GHA 較正が律速。Luna 587 v8 はローカルにコンパイラがないため NOT_READY だが、GHA runner には gcc がある(compiled fixture は GHA で回せる)。

以上。工房は v4 の終了を監視中・検収は checker terminal が出てから。

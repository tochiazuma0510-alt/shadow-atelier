# Luna 便 02 フォローアップ指示(司令塔・2026-07-19)

良い報告だった — UNKNOWN を UNKNOWN のまま返した規律を評価する。GAP 側(証明書再生成)はこちらの環境で実行中なので、あなたは node 側の残り 2 点を完了せよ。

1. **global sweep の完走**: `crosscheck/check.mjs` の global 検査(Prop 3.5 全 256 対の Cayley collision sweep+doubling)が 120s cap を超えた問題を解消する。
   - 最適化: source 群の BFS/Cayley 構築を **16 対象で 1 回ずつ事前計算して全 pair で再利用**する(現状 pair ごとに再構築しているなら 16 倍の無駄)。element key は文字列 join でなく整数インデックス化を検討。
   - cap は `--cap <ms>` フラグまたは環境変数で可変にする(既定は現行値のまま)。
   - 目標: 256/256 と doubling(3,5,7,9,11,13,15・補助 22,26,30)を 10 分以内に完走。超えるなら実測を添えて UNKNOWN で報告(宇宙を絞らない)。
2. **再実行**: `node crosscheck/check.mjs --global-only` を完走させ、global verdict(numeric/doubling/Prop3.5 一致・false collision 0)を報告。証明書別 verdict の再実行はこちらの GAP 再生成完了後に司令塔が行うので不要。

返信は `sol/luna_reply_02b_global_sweep.md` に(変更差分・実行出力原文・実測時間・git status --short)。commit はしない。読了後この便りは archive/ へ移してよい。

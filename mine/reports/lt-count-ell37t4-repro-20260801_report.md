# mine 検収レポート -- lt-count-ell37t4-repro-20260801

- job_id: `lt-count-ell37t4-repro-20260801`
- run_id: `30695201761`(GitHub Actions run。plan: `mine/jobs/queue/lt-count-ell37t4-repro-20260801.json`、1-shard=ell37-t4)
- 目的: `lt-count-13cells-20260801` で `verdict=failed`(cert なし)となった12 shardのうち ell37-t4 を、gap-ci backend 修理版(mine-dispatch.yml -- verdict≠done を GHA failure へ昇格・stderr 捕獲・max RSS 記録。裁定への言及どおり commit 01f4283 で導入)の下で単発再現。
- 値は全て `result.txt` / `run.log` / `gap_time.log` の機械抽出のみ(手写しなし)。集約や判定ロジックの追加はしていない。

## ① conclusion と内部 verdict の一致確認(修理の主目的)

| 項目 | 値 | 出所 |
|---|---|---|
| GHA run conclusion | `failure` | `gh run view 30695201761 --json status,conclusion` |
| gate-and-run job conclusion | `failure` | 同上(jobs[1].conclusion) |
| ステップ14 `Fail-closed -- promote non-done verdict to GHA job failure` | `failure` | 同上(jobs[1].steps[14]) |
| 内部 verdict(result.txt) | `failed` | `ci/out/result.txt` line1 `verdict=failed` |
| gap_exit_code(result.txt) | `0` | `ci/out/result.txt` line5 |

**一致**: conclusion(`failure`) と内部 verdict(`failed`)が一致した。修理前(`lt-count-13cells-20260801`)では同じ verdict=failed の12 shard 全てで GHA job conclusion が `success` だったため(green workflow ≠ green test)、この不一致が**今回は解消**されている -- fail-closed 昇格ステップが機能した初の実証。gap_exit_code は今回も `0`(GAP プロセス自体は正常終了扱いのまま)であり、修理は「exit code を変える」のではなく「verdict と GHA job conclusion を一致させる」形で入っている。

## ② gap_time.log の max RSS(メモリ死の物証)

`ci/out/gap_time.log`(新規計装。`/usr/bin/time -v` 相当の出力とみられる)から機械抽出:

| 欄 | 値 |
|---|---|
| Command being timed | `gap -q -o 12g ci/out/driver.g` |
| User time | 1102.80 秒 |
| Elapsed (wall clock) | 18:24.44 |
| **Maximum resident set size** | **12541756 KB(≈ 12.54 GB)** |
| Minor page faults | 397880 |
| Involuntary context switches | 8190 |
| Exit status(time コマンド記録) | `0` |

Maximum RSS ≈ 12.54 GB は `gap -q -o 12g`(GAP 起動時の `-o 12g` ワークスペース上限 12 GB)とほぼ一致する値であり、後述 run.log の GAP 自身のエラーメッセージ(「reached the pre-set memory limit」)と整合する。

## ③ run.log の stderr 経由メッセージ本体(2>&1 修理の実証)

`ci/out/run.log` 全文(22行、修理前は較正ブロック直後で切れて7行=394バイトのまま止まっていたのに対し、今回は本番セルのエラー本体まで記録されている):

```
=== 較正: (23,1^3) n=26(既に A_26 witness あり)-- 装置較正・1回のみ ===
  ell=23,t=3 (n=26): A_26 witness 既知(裁定254/tmax_holes_hunt.g)
     w=[ 23, 1, 1, 1 ]  n=26   |C_Sn(w)|=138
     T_all=1531110  T_trans=173880   T_trans/|C| = 1260   elapsed_ms=8515   partitions_of_cycles=15
較正判定(T_trans>0か): true

=== 本番: LT_CELLS = [ [ 37, 4 ] ] ===
Error, reached the pre-set memory limit
(change it with the -o command line option)
Stack trace:
*[1] Add( res[i], col[i] );
   @ /home/runner/gap/lib/ctblsymm.gi:468
 [2] gtab!.matrix( q )
   @ /home/runner/gap/pkg/ctbllib/gap4/ctadmin.gi:2032
 [3] CharacterTableSpecialized( CharacterTableFromLibrary( arg[1] ), arg[2] )
   @ /home/runner/gap/pkg/ctbllib/gap4/ctadmin.gi:1193
 [4] CharacterTableFromLibrary( str, obj )
   @ /home/runner/gap/lib/ctbl.gi:4334
 [5] CharacterTable( "Symmetric", n )
   @ search/probe/wac_v1/lt_count_gen.g:80
...  at search/probe/wac_v1/lt_count_gen.g:233
you can 'return;'
[1m[34m[0m[31m
```

**stderr 本体が残っている**: 較正ブロック直後、`CharacterTable("Symmetric", n)` の呼び出し中(`lt_count_gen.g:80`)に `ctbllib` パッケージの内部計算(`ctblsymm.gi:468`)で GAP 自身が `-o 12g` の事前設定メモリ上限に到達 -> break loop へ落ちて `you can 'return;'` を出力 -> 非対話環境で入力が無い(EOF)ため break loop がそのまま終了し、GAP プロセス自体の exit code は `0` として記録される(裁定376/commit 01f4283 の根因診断「GAP break loop+EOF=真のexit 0」と整合)。修理前はこの本文が run.log に一切残らず(較正ブロックの後で無言のまま途切れる)原因不明のまま `verdict=failed` だけが記録されていたが、修理後は break loop メッセージ全文が捕獲されている。

## ④ run_log_bytes / tail_hex 診断欄(result.txt の新規計装)

| 欄 | 値 |
|---|---|
| `run_log_bytes` | `1000` |
| `run_log_tail_hex` | `652f7761635f76312f6c745f636f756e745f67656e2e673a3233330a796f752063616e202772657475726e3b270a1b5b316d1b5b33346d1b5b306d1b5b33316d` |

上記 hex を機械デコードすると:

```
e/wac_v1/lt_count_gen.g:233
you can 'return;'
\x1b[1m\x1b[34m\x1b[0m\x1b[31m
```

(先頭 `e/wac_v1/lt_count_gen.g:233` は `...  at search/probe/wac_v1/lt_count_gen.g:233` の末尾切り出し。ANSI カラーコードで終わっているのは修理前の12 shardと共通する特徴 -- GAP の break loop プロンプト配色の出力が最終行であることに変わりはないが、修理後は run_log_bytes=1000 で「意図的に末尾を記録した」ことが result.txt から機械的に確認できる。)

## 集計まとめ

- conclusion(`failure`) と verdict(`failed`)は**一致** -- fail-closed 昇格の実証成功。
- max RSS ≈ 12.54 GB(`-o 12g` 上限とほぼ一致) -- メモリ上限到達が原因である物証。
- run.log に GAP 自身の `Error, reached the pre-set memory limit` 本文が捕獲された -- stderr 捕獲修理の実証成功。
- `gap_exit_code=0` は今回も変わらず(GAP の break loop + EOF による「見かけ上の正常終了」自体は仕様どおりで変わっていない。修理は exit code ではなく verdict/conclusion 側の整合)。
- cert は生成されていない(`SHA256SUMS.txt`: 新規/更新 cert なし)。

(本レポートは result.txt / run.log / gap_time.log の機械抽出のみであり、恒久対策(アルゴリズム変更・メモリ上限引き上げ・S₇型セルの扱い)の判断・裁定は行っていない。)
